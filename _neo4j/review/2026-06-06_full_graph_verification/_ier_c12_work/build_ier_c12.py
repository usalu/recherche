#!/usr/bin/env python3
"""IER-C1+C2 merged — never-sourced :Akteur tier-C internet evidence recovery.

Scope: 292 MISSING_EVIDENCE :Akteur nodes with no tier-A URL (ledger filter).
Search ladder: official site → imprint → registry (§4 tier C).
READ-ONLY Neo4j. Outputs ledger/ier_c12.csv + reports/ier_c12_report.md.
"""
from __future__ import annotations

import csv
import json
import re
import sys
import time
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin, urlparse
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent
REPO = HERE.parents[3]
SCRIPTS = REPO / "_scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from neo4j import GraphDatabase  # noqa: E402
from neo4j_env import resolve_connection  # noqa: E402

LEDGER_IN = REVIEW / "VERIFICATION_LEDGER_ELEMENT.csv"
GEO_JSON = REPO / "_neo4j/review/2026-06-06_project_bg_geo_extract/akteur_typ_projekt_geo.json"
OUT_LEDGER = REVIEW / "ledger/ier_c12.csv"
OUT_REPORT = REVIEW / "reports/ier_c12_report.md"
WORK_CACHE = HERE / "url_fetch_cache.json"
SCOPE_JSON = HERE / "scope.json"

AGENT_ID = "IER-C12"
LEDGER_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
    "asserted_claim", "basis_type", "basis_ref", "fetched", "http_status", "verdict",
    "confidence", "proof_quote", "proposed_action", "agent_id", "notes",
]

HEADERS = {
    "User-Agent": "recherche-ier-c12/1.0 (+local-verification)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

IMPRINT_PATHS = (
    "/impressum", "/imprint", "/legal", "/legal-notice", "/mentions-legales",
    "/contact", "/about", "/about-us", "/ueber-uns", "/a-propos",
)

TLD_BY_COUNTRY = {
    "deutschland": (".de", ".eu"),
    "germany": (".de", ".eu"),
    "belgien": (".be", ".eu"),
    "belgium": (".be", ".eu"),
    "belgique": (".be", ".eu"),
    "frankreich": (".fr", ".eu"),
    "france": (".fr", ".eu"),
    "niederlande": (".nl", ".eu"),
    "netherlands": (".nl", ".eu"),
    "österreich": (".at", ".eu"),
    "austria": (".at", ".eu"),
    "schweiz": (".ch", ".eu"),
    "switzerland": (".ch", ".eu"),
    "united kingdom": (".uk", ".co.uk", ".org.uk"),
    "uk": (".uk", ".co.uk"),
    "italien": (".it", ".eu"),
    "italy": (".it", ".eu"),
    "spanien": (".es", ".eu"),
    "spain": (".es", ".eu"),
}

PERSON_TYP_RE = re.compile(r"\b(person|privatperson|einzelperson)\b", re.I)
PUBLIC_TYP_RE = re.compile(
    r"\b(oeffentliche|öffentliche|commune|ville|stadt|gemeinde|region|"
    r"universit|hochschul|ministry|ministerium|agency|behörde)\b",
    re.I,
)


def norm_text(s: str) -> str:
    s = unescape(s or "")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def slug_tokens(text: str) -> list[str]:
    t = norm_text(text)
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return [w for w in t.split() if len(w) > 2]


def entity_on_page(name: str, page_text: str) -> tuple[bool, str]:
    if not name or not page_text:
        return False, "empty"
    body = norm_text(page_text)
    n = norm_text(name)
    if n in body:
        return True, "full_name"
    # try without legal suffixes
    short = re.sub(r"\b(gmbh|ag|sa|nv|bv|srl|ltd|inc|stiftung|asbl|vzw)\b", "", n).strip()
    short = re.sub(r"\s+", " ", short)
    if short and len(short) > 4 and short in body:
        return True, "short_name"
    tokens = [t for t in slug_tokens(name) if len(t) > 3]
    if not tokens:
        tokens = slug_tokens(name)
    hits = sum(1 for t in tokens if t in body)
    need = max(1, min(2, len(tokens) // 2))
    if hits >= need:
        return True, f"tokens={hits}/{len(tokens)}"
    return False, f"tokens={hits}/{len(tokens)}"


def extract_quote(name: str, page_text: str, max_len: int = 280) -> str:
    """Pull a verbatim sentence mentioning the entity."""
    plain = re.sub(r"<script[^>]*>.*?</script>", " ", page_text, flags=re.I | re.S)
    plain = re.sub(r"<style[^>]*>.*?</style>", " ", plain, flags=re.I | re.S)
    plain = unescape(re.sub(r"<[^>]+>", " ", plain))
    plain = re.sub(r"\s+", " ", plain).strip()
    tokens = slug_tokens(name)
    if not tokens:
        return plain[:max_len]
    # sentence split (rough)
    sentences = re.split(r"(?<=[.!?])\s+", plain)
    for sent in sentences:
        s_norm = norm_text(sent)
        hits = sum(1 for t in tokens if t in s_norm)
        if hits >= max(1, len(tokens) // 2) and 20 < len(sent) < 400:
            return sent.strip()[:max_len]
    # fallback: window around first token hit
    body_lower = plain.lower()
    for t in tokens:
        idx = body_lower.find(t)
        if idx >= 0:
            start = max(0, idx - 80)
            end = min(len(plain), idx + 200)
            return plain[start:end].strip()[:max_len]
    return plain[:max_len]


def load_scope() -> list[dict]:
    rows = []
    with LEDGER_IN.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if (
                row["verdict"] == "MISSING_EVIDENCE"
                and row["rel_type_or_label"] == "Akteur"
                and row["claim_kind"] == "node"
            ):
                bt = row.get("basis_type", "") or ""
                br = row.get("basis_ref", "") or ""
                if not (br.startswith("http") or bt in ("web", "candidate")):
                    rows.append(row)
    for r in rows:
        aid = r.get("element_id", "")
        if aid.startswith("4:"):
            aid = r.get("from_id") or ""
            if not aid and "F09-new-node-" in (r.get("claim_id") or ""):
                aid = (r.get("claim_id") or "").replace("F09-new-node-", "")
            r["_actor_id"] = aid
        else:
            r["_actor_id"] = aid
    rows.sort(key=lambda r: r.get("graph_element_id") or r.get("element_id", ""))
    return rows


def load_geo() -> dict[str, dict]:
    if not GEO_JSON.exists():
        return {}
    data = json.loads(GEO_JSON.read_text(encoding="utf-8"))
    return {a["id"]: a for a in data.get("akteure", [])}


def is_valid_http_url(url: str) -> bool:
    try:
        u = url.strip()
        if not u.startswith(("http://", "https://")):
            return False
        if u.count(":") > 2:  # reject neo4j elementId-like strings
            return False
        p = urlparse(u)
        if p.scheme not in ("http", "https") or not p.netloc:
            return False
        host = p.hostname or ""
        if not host or "." not in host:
            return False
        if p.port is not None and not (1 <= p.port <= 65535):
            return False
        if re.search(r"[^a-z0-9.\-]", host, re.I):
            return False
        return True
    except Exception:
        return False


def fetch_url(url: str, cache: dict) -> dict:
    if not is_valid_http_url(url):
        return {"url": url, "fetched": False, "http_status": "", "text": "", "error": "invalid_url"}
    key = url.rstrip("/")
    if key in cache:
        return cache[key]
    entry = {"url": url, "fetched": False, "http_status": "", "text": "", "error": ""}
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=18) as resp:
            raw = resp.read(400_000)
            entry["http_status"] = str(getattr(resp, "status", 200))
            entry["fetched"] = True
            entry["text"] = raw.decode("utf-8", errors="replace")
    except HTTPError as e:
        entry["http_status"] = str(e.code)
        entry["error"] = str(e)
        try:
            entry["text"] = e.read(80_000).decode("utf-8", errors="replace")
            entry["fetched"] = True
        except Exception:
            pass
    except (URLError, TimeoutError, OSError, ValueError) as e:
        entry["error"] = str(e)
    except Exception as e:
        entry["error"] = f"fetch_error:{e}"
    cache[key] = entry
    time.sleep(0.05)
    return entry


def ddg_search(query: str, cache: dict, max_results: int = 5) -> list[str]:
    ck = f"ddg:{query}"
    if ck in cache:
        return cache[ck]
    urls: list[str] = []
    try:
        q = quote(query)
        url = f"https://html.duckduckgo.com/html/?q={q}"
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=15) as resp:
            html = resp.read(200_000).decode("utf-8", errors="replace")
        for m in re.finditer(r'uddg=([^&"]+)', html):
            u = unescape(m.group(1))
            if u.startswith("http") and "duckduckgo" not in u:
                urls.append(u)
            if len(urls) >= max_results:
                break
    except Exception:
        pass
    cache[ck] = urls
    time.sleep(0.35)
    return urls


def guess_domains(actor_id: str, name: str, country: str | None) -> list[str]:
    domains: list[str] = []
    slug = actor_id.replace("_", "-")
    domains.append(f"https://www.{slug}.com")
    domains.append(f"https://{slug}.de")
    domains.append(f"https://www.{slug}.de")
    domains.append(f"https://www.{slug}.be")
    domains.append(f"https://www.{slug}.fr")
    # commune patterns
    if actor_id.startswith("commune_") or actor_id.startswith("commune_de_"):
        slug = actor_id.replace("commune_de_", "").replace("commune_", "")
        domains.insert(0, f"https://www.{slug}.be")
        domains.append(f"https://{slug}.be")
    if actor_id.startswith("ville_de_"):
        slug = actor_id.replace("ville_de_", "")
        domains.insert(0, f"https://www.{slug}.be")
        domains.append(f"https://{slug}.brussels")
    if "tu_" in actor_id or actor_id.endswith("_tu_berlin"):
        domains.insert(0, "https://www.tu-berlin.de")
    tlds = TLD_BY_COUNTRY.get(norm_text(country or ""), (".com", ".de", ".be", ".fr", ".eu"))
    tokens = slug_tokens(name)
    if len(tokens) >= 2:
        joined = "-".join(tokens[:3])
        for tld in tlds[:2]:
            domains.append(f"https://www.{joined}{tld}")
            domains.append(f"https://{joined}{tld}")
    # dedupe preserve order
    seen: set[str] = set()
    out = []
    for d in domains:
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out


def registry_search(name: str, country: str | None, cache: dict) -> list[str]:
    c = norm_text(country or "")
    urls: list[str] = []
    if any(x in c for x in ("deutschland", "germany")):
        urls.extend(ddg_search(f'"{name}" Handelsregister site:handelsregister.de', cache, 3))
        urls.extend(ddg_search(f'"{name}" site:unternehmensregister.de', cache, 2))
    if any(x in c for x in ("belgien", "belgium", "belgique")):
        urls.extend(ddg_search(f'"{name}" site:kbopub.economie.fgov.be', cache, 3))
        urls.extend(ddg_search(f'"{name}" BCE KBO', cache, 2))
    if any(x in c for x in ("frankreich", "france")):
        urls.extend(ddg_search(f'"{name}" site:societe.com OR site:infogreffe.fr', cache, 3))
    if any(x in c for x in ("niederlande", "netherlands")):
        urls.extend(ddg_search(f'"{name}" site:kvk.nl', cache, 3))
    if any(x in c for x in ("united kingdom", "uk")):
        urls.extend(ddg_search(f'"{name}" site:find-and-update.company-information.service.gov.uk', cache, 2))
    return urls


def search_ladder(actor: dict, cache: dict) -> tuple[str | None, dict, str]:
    """Return (url, fetch_entry, ladder_step) or (None, {}, step)."""
    aid = actor["id"]
    name = actor["name"] or aid
    country = actor.get("country")
    akteur_typ = actor.get("akteur_typ") or ""
    asserted = actor.get("asserted_claim") or ""

    is_person = bool(PERSON_TYP_RE.search(asserted) or PERSON_TYP_RE.search(akteur_typ))
    if is_person:
        return None, {}, "person_skip"

    candidates: list[tuple[str, str]] = []

    # Step 1: official site search (one query unless public)
    queries = [f'"{name}" official site']
    if PUBLIC_TYP_RE.search(name) or PUBLIC_TYP_RE.search(aid):
        queries.append(f'"{name}" {country or ""} site officiel')
    for q in queries:
        for u in ddg_search(q, cache, 5):
            candidates.append((u, "search_official"))

    # domain guessing (limited)
    for u in guess_domains(aid, name, country)[:5]:
        candidates.append((u, "domain_guess"))

    tried: set[str] = set()
    max_tries = 14
    imprint_paths = IMPRINT_PATHS[:4]
    for url, step in candidates:
        if len(tried) >= max_tries:
            break
        if not is_valid_http_url(url):
            continue
        base = url.split("?")[0].rstrip("/")
        if base in tried:
            continue
        tried.add(base)

        # try base URL
        entry = fetch_url(url, cache)
        if entry.get("fetched") and entry.get("http_status", "").startswith("2"):
            ok, how = entity_on_page(name, entry.get("text", ""))
            if ok:
                return url, entry, step

        # Step 2: imprint paths
        parsed = urlparse(url if entry.get("fetched") else url)
        if parsed.scheme and parsed.netloc:
            origin = f"{parsed.scheme}://{parsed.netloc}"
            for path in imprint_paths:
                imp = origin + path
                if imp in tried:
                    continue
                tried.add(imp)
                imp_entry = fetch_url(imp, cache)
                if imp_entry.get("fetched") and imp_entry.get("http_status", "").startswith("2"):
                    ok, _ = entity_on_page(name, imp_entry.get("text", ""))
                    if ok:
                        return imp, imp_entry, f"imprint:{path}"

    # Step 3: registry (only when country known)
    if country:
        for u in registry_search(name, country, cache)[:4]:
            if u in tried:
                continue
            tried.add(u)
            entry = fetch_url(u, cache)
            if entry.get("fetched") and entry.get("http_status", "").startswith("2"):
                ok, _ = entity_on_page(name, entry.get("text", ""))
                if ok:
                    return u, entry, "registry"

    # archive fallback (single query)
    for u in ddg_search(f'site:web.archive.org "{name}"', cache, 1):
        entry = fetch_url(u, cache)
        if entry.get("fetched"):
            ok, _ = entity_on_page(name, entry.get("text", ""))
            if ok:
                return u, entry, "archive"

    return None, {}, "exhausted"


def query_actors(driver, database: str, ids: list[str]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    batch = 80
    for i in range(0, len(ids), batch):
        chunk = ids[i : i + batch]
        with driver.session(database=database) as session:
            result = session.run(
                """
                UNWIND $ids AS aid
                MATCH (a:Akteur {id: aid})
                OPTIONAL MATCH (a)-[:LIEGT_IN_LAND]->(l:Land)
                RETURN a.id AS id, a.name AS name,
                       a.note AS note, a.source_scope AS source_scope,
                       elementId(a) AS graph_element_id,
                       l.name AS country
                """,
                ids=chunk,
            )
            for rec in result:
                out[rec["id"]] = dict(rec)
    return out


def adjudicate(actor: dict, url: str | None, entry: dict, step: str) -> dict:
    name = actor["name"] or actor["id"]
    asserted = actor.get("asserted_claim") or f"{name} exists as organisation in graph"
    is_person = step == "person_skip"

    if is_person:
        return {
            "basis_type": "none",
            "basis_ref": "",
            "fetched": "false",
            "http_status": "",
            "verdict": "UNVERIFIABLE",
            "confidence": "unbelegt",
            "proof_quote": "",
            "proposed_action": "ESCALATE_HUMAN",
            "notes": "private person; no org homepage policy; tier-D crossover",
        }

    if url and entry.get("fetched"):
        quote = extract_quote(name, entry.get("text", ""))
        ok, how = entity_on_page(name, entry.get("text", ""))
        if ok and quote:
            return {
                "basis_type": "web",
                "basis_ref": url,
                "fetched": "true",
                "http_status": entry.get("http_status", ""),
                "verdict": "PROVEN",
                "confidence": "belegt",
                "proof_quote": quote,
                "proposed_action": "ADD_SOURCE",
                "notes": f"ladder={step}; match={how}",
            }
        if entry.get("http_status", "").startswith("2"):
            return {
                "basis_type": "web",
                "basis_ref": url,
                "fetched": "true",
                "http_status": entry.get("http_status", ""),
                "verdict": "PARTIAL",
                "confidence": "teilweise_belegt",
                "proof_quote": quote or "",
                "proposed_action": "RESOURCE",
                "notes": f"ladder={step}; page fetched but weak name match",
            }

    if step == "exhausted":
        return {
            "basis_type": "search",
            "basis_ref": "",
            "fetched": "false",
            "http_status": "",
            "verdict": "UNVERIFIABLE",
            "confidence": "unbelegt",
            "proof_quote": "",
            "proposed_action": "ESCALATE_HUMAN" if PUBLIC_TYP_RE.search(name) else "RESOURCE",
            "notes": "search ladder exhausted; no first-party URL found",
        }

    return {
        "basis_type": "none",
        "basis_ref": "",
        "fetched": "false",
        "http_status": "",
        "verdict": "MISSING_EVIDENCE",
        "confidence": "unbelegt",
        "proof_quote": "",
        "proposed_action": "ADD_SOURCE",
        "notes": f"ladder={step}; unresolved",
    }


def write_csv_row(writer, ledger_row: dict, adj: dict) -> None:
    writer.writerow({
        "claim_id": ledger_row.get("claim_id", f"IER-C12-{ledger_row['element_id']}"),
        "claim_kind": "node",
        "element_id": ledger_row.get("graph_element_id") or ledger_row["element_id"],
        "from_id": ledger_row["element_id"],
        "to_id": "",
        "rel_type_or_label": "Akteur",
        "asserted_claim": ledger_row.get("asserted_claim") or f"{ledger_row['element_id']} exists",
        "basis_type": adj["basis_type"],
        "basis_ref": adj["basis_ref"],
        "fetched": adj["fetched"],
        "http_status": adj["http_status"],
        "verdict": adj["verdict"],
        "confidence": adj["confidence"],
        "proof_quote": adj["proof_quote"],
        "proposed_action": adj["proposed_action"],
        "agent_id": AGENT_ID,
        "notes": adj["notes"],
    })


def load_existing_ledger() -> tuple[list[dict], set[str]]:
    if not OUT_LEDGER.exists():
        return [], set()
    rows = list(csv.DictReader(OUT_LEDGER.open(encoding="utf-8")))
    done = {r["from_id"] for r in rows if r.get("from_id")}
    return rows, done


def main() -> int:
    scope = load_scope()
    print(f"scope rows: {len(scope)}")
    geo = load_geo()

    cache: dict = {}
    if WORK_CACHE.exists():
        try:
            cache = json.loads(WORK_CACHE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            cache = {}

    existing_rows, done_ids = load_existing_ledger()
    if done_ids:
        print(f"resume: skipping {len(done_ids)} already ledgered actors")

    ids = [r["_actor_id"] for r in scope if r["_actor_id"] not in done_ids]
    uri, user, pwd, db = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, pwd))
    live = query_actors(driver, db, ids)
    driver.close()

    OUT_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

    verdicts: Counter = Counter(r["verdict"] for r in existing_rows)
    actions: Counter = Counter(r["proposed_action"] for r in existing_rows)
    worst: list[dict] = []
    ledger_rows: list[dict] = list(existing_rows)

    file_mode = "a" if done_ids else "w"
    with OUT_LEDGER.open(file_mode, encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LEDGER_COLS, quoting=csv.QUOTE_MINIMAL)
        if not done_ids:
            writer.writeheader()

        pending = [r for r in scope if r["_actor_id"] not in done_ids]
        for i, row in enumerate(pending):
            aid = row["_actor_id"]
            actor = live.get(aid, {"id": aid, "name": aid})
            actor["asserted_claim"] = row.get("asserted_claim", "")
            ac = row.get("asserted_claim") or ""
            actor["akteur_typ"] = ac.split(" - ")[-1] if " - " in ac else ""
            g = geo.get(aid, {})
            if not actor.get("country"):
                loc = g.get("primary_location") if g else None
                actor["country"] = loc.get("country") if isinstance(loc, dict) else loc

            url, entry, step = search_ladder(actor, cache)
            adj = adjudicate(actor, url, entry, step)

            out = {
                "claim_id": row.get("claim_id", f"IER-C12-{aid}"),
                "claim_kind": "node",
                "element_id": row.get("graph_element_id") or aid,
                "from_id": aid,
                "to_id": "",
                "rel_type_or_label": "Akteur",
                "asserted_claim": row.get("asserted_claim") or f"{actor.get('name', aid)} exists",
                **adj,
                "agent_id": AGENT_ID,
            }
            ledger_rows.append(out)
            verdicts[adj["verdict"]] += 1
            actions[adj["proposed_action"]] += 1

            if adj["verdict"] in ("UNVERIFIABLE", "MISSING_EVIDENCE", "PARTIAL"):
                worst.append({
                    "id": aid,
                    "name": actor.get("name"),
                    "verdict": adj["verdict"],
                    "notes": adj["notes"],
                })

            writer.writerow({k: out.get(k, "") for k in LEDGER_COLS})
            f.flush()

            if (i + 1) % 25 == 0:
                print(f"  processed {len(done_ids)+i+1}/{len(scope)} proven={verdicts.get('PROVEN',0)}")
                WORK_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=0)[:5_000_000], encoding="utf-8")

    WORK_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=0)[:5_000_000], encoding="utf-8")

    proven = verdicts.get("PROVEN", 0)
    total = len(scope)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    report_lines = [
        "# IER-C1+C2 merged — Never-sourced `:Akteur` recovery report",
        "",
        f"**Agent:** `{AGENT_ID}` · **Generated:** {now}",
        f"**Database:** `mit-bestand` (read-only) · **Scope:** {total} rows (IER-C1 174 + IER-C2 118)",
        "",
        "## Scope recap",
        "",
        "Tier-C `:Akteur` nodes with `verdict=MISSING_EVIDENCE` in canonical ledger, no tier-A URL "
        "(`source_urls` / `primary_source_url` null on live graph). Search ladder: official site → "
        "imprint/legal → registry (Handelsregister / KBO / etc.) → archive fallback.",
        "",
        "## Verdict counts",
        "",
        "| Verdict | Count | Share |",
        "|---|---:|---:|",
    ]
    for v, c in verdicts.most_common():
        report_lines.append(f"| {v} | {c} | {100*c/total:.1f}% |")
    report_lines += [
        "",
        "## Proposed actions",
        "",
        "| Action | Count |",
        "|---|---:|",
    ]
    for a, c in actions.most_common():
        report_lines.append(f"| {a} | {c} |")
    report_lines += [
        "",
        f"**PROVEN upgrades:** {proven} / {total} ({100*proven/total:.1f}%)",
        "",
        "## Ten hardest unresolved (sample)",
        "",
    ]
    for w in worst[:10]:
        report_lines.append(f"- `{w['id']}` ({w['name']}): **{w['verdict']}** — {w['notes']}")
    report_lines += [
        "",
        "## Anomalies",
        "",
        f"- Persons flagged for ESCALATE_HUMAN: {sum(1 for r in ledger_rows if 'private person' in r.get('notes',''))}",
        f"- Search ladder exhausted: {sum(1 for r in ledger_rows if 'exhausted' in r.get('notes',''))}",
        f"- URL cache entries: {len(cache)}",
        "",
        "## Summary",
        "",
        f"Processed all **{total}** never-sourced tier-C actors. "
        f"**{proven}** upgraded to PROVEN with fetched first-party or registry evidence; "
        f"remainder mostly UNVERIFIABLE after ladder exhaustion or person-policy ESCALATE.",
        "",
    ]
    OUT_REPORT.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Wrote {OUT_LEDGER} ({total} rows), {OUT_REPORT}")
    print("verdicts:", dict(verdicts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
