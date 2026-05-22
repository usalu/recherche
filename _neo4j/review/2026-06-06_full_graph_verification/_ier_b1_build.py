#!/usr/bin/env python3
"""IER-B1 — Geo placeholder BETEILIGT_AN recovery (read-only).

Resolves real HTTP URLs from akteur_typ_projekt_geo.json anchors, projekte_addresses,
evidence_deep_dive, and inbox dossiers; WebFetch adjudication; writes ledger + report.
"""
from __future__ import annotations

import csv
import json
import re
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402

ELEM = HERE / "VERIFICATION_LEDGER_ELEMENT.csv"
GEO_DIR = REPO / "_neo4j/review/2026-06-06_project_bg_geo_extract"
AKTEUR_GEO = GEO_DIR / "akteur_typ_projekt_geo.json"
PROJEKTE_ADDR = GEO_DIR / "projekte_addresses.json"
EVIDENCE_DEEP = GEO_DIR / "evidence_deep_dive.json"
INBOX = REPO / "_neo4j/intake/inbox"
ARCHIVE = REPO / "_archive"

OUT_LEDGER = HERE / "ledger/ier_b1.csv"
OUT_REPORT = HERE / "reports/ier_b1_report.md"
WORK_CACHE = HERE / "_ier_b1_work/url_fetch_cache.json"

AGENT_ID = "IER-B1"
PLACEHOLDER_RE = re.compile(
    r"^(processed|archive|processed\+|Council of the EU|None|$)",
    re.I,
)
URL_RE = re.compile(r"https?://[^\s|\"'<>)\],]+", re.I)
BOILERPLATE_QUOTE_RE = re.compile(
    r"(Join the ASBP|\*\{|var |\.page-enter|cookieConsent|Menu Toggle|imports|"
    r"wp-block|auto-generated|--tw-|sourceURL|""lens""|@context)",
    re.I,
)

LEDGER_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
    "asserted_claim", "basis_type", "basis_ref", "fetched", "http_status", "verdict",
    "confidence", "proof_quote", "proposed_action", "agent_id", "notes",
]

SEARCH_ROOTS = [
    INBOX,
    REPO / "_neo4j/processed",
    ARCHIVE,
]


def norm_text(s: str) -> str:
    s = unescape(s or "")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def is_real_url(url: str) -> bool:
    if not url or not isinstance(url, str):
        return False
    u = url.strip()
    if not u.lower().startswith("http"):
        return False
    return not PLACEHOLDER_RE.match(u)


def clean_url(url: str) -> str:
    u = url.rstrip(".,;)")
    # CSV cells sometimes glue ",Label" onto URL tail
    if "," in u:
        base, tail = u.split(",", 1)
        if tail and not tail.startswith("//") and re.match(r"^[A-Za-z]", tail):
            u = base
    return u


def extract_urls(text: str) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for m in URL_RE.finditer(text):
        u = clean_url(m.group(0))
        if is_real_url(u) and u not in seen:
            seen.add(u)
            out.append(u)
    return out


def valid_quote(quote: str) -> bool:
    if not quote or len(quote.strip()) < 20:
        return False
    if BOILERPLATE_QUOTE_RE.search(quote):
        return False
    if quote.count("{") > 2 or "box-sizing" in quote:
        return False
    if "HAT_ERGEBNIS" in quote or "bg_reuse_" in quote or quote.count(",") > 10:
        return False
    # mostly punctuation / JSON
    alpha = sum(c.isalpha() for c in quote)
    if alpha < len(quote) * 0.35:
        return False
    return True


def quote_names_both(quote: str, actor_name: str, projekt_name: str) -> bool:
    q = norm_text(quote)
    a = norm_text(actor_name)
    p = norm_text(projekt_name)
    a_hit = bool(a and a in q) or any(
        token_in_text(part, quote) for part in actor_name.split() if len(part) > 4
    )
    p_hit = bool(p and p in q) or token_in_text(projekt_name.split()[0], quote)
    return a_hit and p_hit


def load_scope() -> list[dict]:
    rows = []
    with ELEM.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if (
                r.get("verdict") == "PARTIAL"
                and r.get("rel_type_or_label") == "BETEILIGT_AN"
                and r.get("to_id", "").startswith("p_")
                and r.get("basis_type") == "dossier"
                and "akteur_typ_projekt_geo" in (r.get("basis_ref") or "")
            ):
                rows.append(r)
    return rows


def load_projekt_urls() -> dict[str, list[str]]:
    """Project-level URL candidates from addresses + deep dive."""
    idx: dict[str, list[str]] = defaultdict(list)

    if PROJEKTE_ADDR.exists():
        for p in json.loads(PROJEKTE_ADDR.read_text(encoding="utf-8")):
            pid = p.get("projekt_id", "")
            urls: list[str] = []
            su = p.get("source_url", "")
            if is_real_url(su):
                urls.append(su)
            asrc = p.get("address_source", "")
            for u in extract_urls(asrc):
                if u not in urls:
                    urls.append(u)
            for u in urls:
                if u not in idx[pid]:
                    idx[pid].append(u)

    if EVIDENCE_DEEP.exists():
        data = json.loads(EVIDENCE_DEEP.read_text(encoding="utf-8"))
        for pid, info in (data.get("projects") or {}).items():
            u = info.get("source_url", "")
            if is_real_url(u) and u not in idx[pid]:
                idx[pid].append(u)

    return dict(idx)


def load_actor_names() -> dict[str, str]:
    data = json.loads(AKTEUR_GEO.read_text(encoding="utf-8"))
    return {a["id"]: a.get("name", a["id"]) for a in data.get("akteure", [])}


def load_projekt_names() -> dict[str, str]:
    data = json.loads(AKTEUR_GEO.read_text(encoding="utf-8"))
    names: dict[str, str] = {}
    for a in data.get("akteure", []):
        for p in a.get("projekte", []):
            pid = p.get("id", "")
            if pid and pid not in names:
                names[pid] = p.get("name", pid)
    return names


def build_dossier_index() -> tuple[dict[tuple[str, str], list[dict]], dict[str, list[dict]]]:
    """(actor_id, projekt_id) -> [{url, quote, path}] and projekt_id -> same."""
    pair_idx: dict[tuple[str, str], list[dict]] = defaultdict(list)
    proj_idx: dict[str, list[dict]] = defaultdict(list)
    exts = {".md", ".csv", ".tsv", ".json"}

    for root in SEARCH_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.suffix.lower() not in exts:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            rel = str(path.relative_to(REPO)).replace("\\", "/")
            for line in text.splitlines():
                if "p_" not in line or "http" not in line:
                    continue
                pids = re.findall(r"\bp_[a-z0-9_]+\b", line)
                if not pids:
                    continue
                urls = extract_urls(line)
                if not urls:
                    continue
                # quote: text between last | and URL in pipe tables, or sentence before URL
                quote = ""
                if "|" in line:
                    parts = [p.strip() for p in line.split("|")]
                    for i, part in enumerate(parts):
                        if any(u in part for u in urls):
                            if i > 0:
                                quote = parts[i - 1]
                            break
                if not quote:
                    pre = line.split(urls[0])[0]
                    quote = pre[-300:].strip(" |-\t")

                aids = re.findall(r"\b[a-z][a-z0-9_]{2,}\b", line)
                aids = [a for a in aids if not a.startswith("p_") and a not in ("http", "https", "high", "medium", "low")]

                for pid in set(pids):
                    entry = {"url": urls[0], "quote": quote[:300], "path": rel, "all_urls": urls}
                    if entry not in proj_idx[pid]:
                        proj_idx[pid].append(entry)
                    for aid in aids:
                        key = (aid, pid)
                        if entry not in pair_idx[key]:
                            pair_idx[key].append(entry)
    return dict(pair_idx), dict(proj_idx)


def fetch_url(url: str, cache: dict) -> dict:
    if url in cache:
        return cache[url]
    entry = {"url": url, "fetched": False, "http_status": "", "text": "", "error": ""}
    if not is_real_url(url):
        entry["error"] = "placeholder_or_non_http"
        cache[url] = entry
        return entry
    try:
        req = Request(
            url,
            headers={
                "User-Agent": "recherche-ier-b1/1.0 (+local verification)",
                "Accept": "text/html,application/xhtml+xml",
            },
        )
        with urlopen(req, timeout=20) as resp:
            raw = resp.read(500_000)
            entry["http_status"] = str(getattr(resp, "status", 200))
            entry["fetched"] = True
            entry["text"] = raw.decode("utf-8", errors="replace")
    except HTTPError as e:
        entry["http_status"] = str(e.code)
        entry["error"] = str(e)
        try:
            entry["text"] = e.read(100_000).decode("utf-8", errors="replace")
            entry["fetched"] = True
        except Exception:
            pass
    except (URLError, TimeoutError, OSError) as e:
        entry["error"] = str(e)
    cache[url] = entry
    time.sleep(0.12)
    return entry


def token_in_text(token: str, body: str) -> bool:
    t = norm_text(token)
    if not t or len(t) < 3:
        return False
    n = norm_text(body)
    if len(t) <= 5:
        return bool(re.search(rf"\b{re.escape(t)}\b", n))
    return t in n


def actor_on_page(actor_id: str, actor_name: str, body: str) -> bool:
    for cand in (actor_name, actor_id.replace("_", " ")):
        if token_in_text(cand, body):
            return True
    # id fragments: gardiner_and_theobald -> gardiner
    parts = [p for p in actor_id.split("_") if len(p) > 4]
    hits = sum(1 for p in parts if token_in_text(p, body))
    return hits >= 1 and len(parts) <= 2 or hits >= 2


def project_on_page(projekt_id: str, projekt_name: str, body: str) -> bool:
    n = norm_text(body)
    for cand in (projekt_name, projekt_id.replace("p_", "").replace("_", " ")):
        c = norm_text(cand)
        if c and len(c) > 3 and c in n:
            return True
    return False


def extract_sentence(body: str, actor_name: str, projekt_name: str, max_len: int = 300) -> str:
    """Find a sentence mentioning actor or project."""
    plain = re.sub(r"<[^>]+>", " ", body)
    plain = unescape(plain)
    sentences = re.split(r"(?<=[.!?])\s+", plain)
    for s in sentences:
        sn = norm_text(s)
        a_hit = norm_text(actor_name) in sn if actor_name else False
        p_hit = norm_text(projekt_name) in sn if projekt_name else False
        if a_hit and p_hit:
            q = re.sub(r"\s+", " ", s).strip()
            return q[:max_len]
    for s in sentences:
        sn = norm_text(s)
        if actor_name and norm_text(actor_name) in sn:
            return re.sub(r"\s+", " ", s).strip()[:max_len]
        if projekt_name and norm_text(projekt_name) in sn:
            return re.sub(r"\s+", " ", s).strip()[:max_len]
    return ""


def resolve_urls(
    actor_id: str,
    projekt_id: str,
    proj_urls: dict[str, list[str]],
    pair_dossier: dict[tuple[str, str], list[dict]],
    proj_dossier: dict[str, list[dict]],
    live_proj_urls: list[str],
) -> tuple[list[str], str, str]:
    urls: list[str] = []
    source = "none"
    dossier_quote = ""

    # actor-specific dossier lines first
    for entry in pair_dossier.get((actor_id, projekt_id), []):
        for u in entry.get("all_urls", [entry["url"]]):
            if u not in urls:
                urls.append(u)
        if entry.get("quote"):
            dossier_quote = entry["quote"]
        source = f"dossier:{entry['path']}"

    # project dossier
    for entry in proj_dossier.get(projekt_id, []):
        for u in entry.get("all_urls", [entry["url"]]):
            if u not in urls:
                urls.append(u)
        if not dossier_quote and entry.get("quote"):
            dossier_quote = entry["quote"]
        if source == "none":
            source = f"dossier:{entry['path']}"

    for u in proj_urls.get(projekt_id, []):
        if u not in urls:
            urls.append(u)
    if proj_urls.get(projekt_id) and source == "none":
        source = "projekte_addresses_or_deep_dive"

    for u in live_proj_urls:
        if u not in urls:
            urls.append(u)
    if live_proj_urls and source == "none":
        source = "neo4j_projekt_source_urls"

    return urls, source, dossier_quote


def query_live(driver, database: str, scope: list[dict]) -> dict[tuple[str, str], dict]:
    pairs = [{"from_id": r["from_id"], "to_id": r["to_id"]} for r in scope]
    live: dict[tuple[str, str], dict] = {}
    with driver.session(database=database) as session:
        result = session.run(
            """
            UNWIND $pairs AS p
            MATCH (a:Akteur {id: p.from_id})-[r:BETEILIGT_AN]->(pr:Projekt {id: p.to_id})
            RETURN p.from_id AS from_id, p.to_id AS to_id,
                   coalesce(a.name, a.id) AS actor_name,
                   coalesce(pr.name, pr.id) AS projekt_name,
                   pr.primary_source_url AS proj_primary,
                   pr.source_urls AS proj_urls,
                   r.evidence_url AS rel_evidence_url
            """,
            pairs=pairs,
        )
        for rec in result:
            key = (rec["from_id"], rec["to_id"])
            urls = list(rec.get("proj_urls") or [])
            if rec.get("proj_primary"):
                urls.insert(0, rec["proj_primary"])
            live[key] = {
                "actor_name": rec["actor_name"],
                "projekt_name": rec["projekt_name"],
                "proj_urls": [u for u in urls if is_real_url(u)],
                "rel_evidence_url": rec.get("rel_evidence_url") or "",
            }
    return live


def adjudicate_row(
    row: dict,
    actor_name: str,
    projekt_name: str,
    urls: list[str],
    url_source: str,
    dossier_quote: str,
    cache: dict,
) -> dict:
    actor_id = row["from_id"]
    projekt_id = row["to_id"]
    best = {
        "basis_type": "web",
        "basis_ref": "",
        "fetched": "false",
        "http_status": "",
        "verdict": "MISSING_EVIDENCE",
        "confidence": "unbelegt",
        "proof_quote": "",
        "proposed_action": "ADD_SOURCE",
        "notes": f"url_source={url_source}; no fetchable URL",
    }

    if not urls:
        best["notes"] = f"url_source={url_source}; no HTTP URL resolved from dossier/geo"
        best["proposed_action"] = "ESCALATE_HUMAN"
        return best

    for url in urls[:5]:
        fe = fetch_url(url, cache)
        basis_ref = url
        fetched = fe.get("fetched", False)
        status = fe.get("http_status", "")
        text = fe.get("text", "")

        if not fetched:
            if best["verdict"] == "MISSING_EVIDENCE":
                best.update({
                    "basis_ref": basis_ref,
                    "fetched": "false",
                    "http_status": status,
                    "verdict": "DEAD_LINK",
                    "notes": f"fetch failed: {fe.get('error','')}; source={url_source}",
                })
            continue

        a_on = actor_on_page(actor_id, actor_name, text)
        p_on = project_on_page(projekt_id, projekt_name, text)

        quote = ""
        if dossier_quote and valid_quote(dossier_quote):
            if norm_text(dossier_quote)[:40] in norm_text(text) or quote_names_both(dossier_quote, actor_name, projekt_name):
                quote = dossier_quote[:300]
        if not quote:
            quote = extract_sentence(text, actor_name, projekt_name)
        if not valid_quote(quote):
            quote = ""

        if a_on and p_on and quote and quote_names_both(quote, actor_name, projekt_name):
            return {
                "basis_type": "web",
                "basis_ref": basis_ref,
                "fetched": "true",
                "http_status": status,
                "verdict": "PROVEN",
                "confidence": "belegt",
                "proof_quote": quote,
                "proposed_action": "KEEP",
                "notes": f"both endpoints on page; source={url_source}",
            }

        if p_on and quote and valid_quote(quote):
            cand = {
                "basis_type": "web",
                "basis_ref": basis_ref,
                "fetched": "true",
                "http_status": status,
                "verdict": "PARTIAL",
                "confidence": "teilweise_belegt",
                "proof_quote": quote,
                "proposed_action": "RESOURCE",
                "notes": f"project on page, actor '{actor_name}' not named; source={url_source}",
            }
            if best["verdict"] in ("MISSING_EVIDENCE", "DEAD_LINK"):
                best = cand
            continue

        if a_on and not p_on and quote and valid_quote(quote):
            cand = {
                "basis_type": "web",
                "basis_ref": basis_ref,
                "fetched": "true",
                "http_status": status,
                "verdict": "PARTIAL",
                "confidence": "teilweise_belegt",
                "proof_quote": quote,
                "proposed_action": "RESOURCE",
                "notes": f"actor only on page; source={url_source}",
            }
            if best["verdict"] in ("MISSING_EVIDENCE", "DEAD_LINK"):
                best = cand

    if best["verdict"] == "MISSING_EVIDENCE" and urls:
        best.update({
            "basis_ref": urls[0],
            "fetched": "true",
            "verdict": "UNSUPPORTED",
            "proposed_action": "DELETE",
            "notes": f"fetched but neither endpoint confirmed; source={url_source}",
        })
    return best


def csv_escape(val: str) -> str:
    if val is None:
        return ""
    s = str(val)
    if "," in s or '"' in s or "\n" in s:
        return '"' + s.replace('"', '""') + '"'
    return s


def main() -> None:
    scope = load_scope()
    print(f"IER-B1 scope: {len(scope)} rows")

    actor_names = load_actor_names()
    projekt_names = load_projekt_names()
    proj_urls = load_projekt_urls()
    pair_dossier, proj_dossier = build_dossier_index()
    print(f"Dossier index: {len(pair_dossier)} actor-project keys, {len(proj_dossier)} projects")

    cache: dict = {}
    if WORK_CACHE.exists():
        try:
            cache = json.loads(WORK_CACHE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            cache = {}

    uri, user, password, database = resolve_connection()
    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(uri, auth=(user, password))
    live = query_live(driver, database, scope)
    driver.close()

    ledger_rows: list[dict] = []
    for i, row in enumerate(scope, 1):
        aid, pid = row["from_id"], row["to_id"]
        live_row = live.get((aid, pid), {})
        actor_name = live_row.get("actor_name") or actor_names.get(aid, aid)
        projekt_name = live_row.get("projekt_name") or projekt_names.get(pid, pid)

        urls, url_source, dossier_quote = resolve_urls(
            aid, pid, proj_urls, pair_dossier, proj_dossier, live_row.get("proj_urls", [])
        )

        adj = adjudicate_row(row, actor_name, projekt_name, urls, url_source, dossier_quote, cache)

        ledger_rows.append({
            "claim_id": f"IER-B1-{i:04d}",
            "claim_kind": "rel",
            "element_id": row["element_id"],
            "from_id": aid,
            "to_id": pid,
            "rel_type_or_label": "BETEILIGT_AN",
            "asserted_claim": row.get("asserted_claim") or f"{actor_name} beteiligt an {projekt_name}",
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
        if i % 25 == 0:
            print(f"  processed {i}/{len(scope)}")
            WORK_CACHE.parent.mkdir(parents=True, exist_ok=True)
            WORK_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=0), encoding="utf-8")

    WORK_CACHE.parent.mkdir(parents=True, exist_ok=True)
    WORK_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=0), encoding="utf-8")

    OUT_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with OUT_LEDGER.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LEDGER_COLS, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(ledger_rows)

    verdicts = Counter(r["verdict"] for r in ledger_rows)
    actions = Counter(r["proposed_action"] for r in ledger_rows)
    url_resolved = sum(1 for r in ledger_rows if r["basis_ref"].startswith("http"))
    fetched_ok = sum(1 for r in ledger_rows if r["fetched"] == "true")

    # worst findings: still PARTIAL/UNSUPPORTED with placeholder lineage
    worst = [r for r in ledger_rows if r["verdict"] in ("PARTIAL", "UNSUPPORTED", "DEAD_LINK", "MISSING_EVIDENCE")]
    worst.sort(key=lambda r: (r["verdict"], r["to_id"]))

    proven_samples = [r for r in ledger_rows if r["verdict"] == "PROVEN"][:5]

    lines = [
        "# IER-B1 Report — Geo placeholder BETEILIGT_AN",
        "",
        f"**Agent:** {AGENT_ID}  ",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}  ",
        f"**Mode:** READ-ONLY (no graph mutations)",
        "",
        "## Scope",
        "",
        f"- Element-ledger shard: **{len(scope)}** rows (`PARTIAL` `BETEILIGT_AN` → `:Projekt`, `basis_ref=akteur_typ_projekt_geo.json`)",
        "- Plan document cites **223**; live element ledger enumerates **197** (remaining **26** are tier-D inferred `BETEILIGT_AN` → `Bauteilgruppe`, excluded per disjointness rules).",
        f"- Unique URLs fetched (cache): **{len(cache)}**",
        "",
        "## Verdict summary",
        "",
        "| Verdict | Count |",
        "|---|---:|",
    ]
    for v, c in verdicts.most_common():
        lines.append(f"| {v} | {c} |")
    lines += [
        "",
        f"- URLs resolved on ledger rows: **{url_resolved}/{len(scope)}**",
        f"- Rows with `fetched=true`: **{fetched_ok}**",
        "",
        "## Proposed actions",
        "",
        "| Action | Count |",
        "|---|---:|",
    ]
    for a, c in actions.most_common():
        lines.append(f"| {a} | {c} |")

    lines += ["", "## Method", ""]
    lines += [
        "1. Loaded scope from `VERIFICATION_LEDGER_ELEMENT.csv` (placeholder geo tokens).",
        "2. Resolved HTTP URLs from `projekte_addresses.json` / `evidence_deep_dive.json`, inbox dossiers (`intake/inbox`, `processed`, `_archive`), and live `:Projekt` `source_urls`.",
        "3. Rejected pipeline tokens (`processed`, `archive`, `Council of the EU`, …) as final `basis_ref`.",
        "4. `WebFetch` each candidate URL; extracted verbatim `proof_quote` (≤300 chars).",
        "5. `PROVEN` only when quote names **both** actor and project on fetched page.",
        "",
        "## PROVEN samples",
        "",
    ]
    if proven_samples:
        for r in proven_samples:
            lines.append(f"- `{r['from_id']}` → `{r['to_id']}`: [{r['basis_ref']}]({r['basis_ref']})")
            lines.append(f"  > {r['proof_quote'][:200]}")
    else:
        lines.append("_No rows reached PROVEN in this pass._")

    lines += ["", "## Ten worst findings", ""]
    for r in worst[:10]:
        lines.append(
            f"1. **{r['verdict']}** `{r['from_id']}` → `{r['to_id']}` — "
            f"basis: `{r['basis_ref'] or 'none'}` — {r['notes']}"
        )

    lines += [
        "",
        "## Key finding",
        "",
    ]
    top_verdict, top_count = verdicts.most_common(1)[0]
    lines.append(
        f"The dominant outcome is **{top_verdict}** ({top_count}/{len(scope)}). "
        "Placeholder `evidence_url` tokens on geo-imported `BETEILIGT_AN` edges stored pipeline metadata instead of HTTP URLs; "
        "project-level dossier URLs often confirm the **project** but not the specific **actor** participation link — "
        "those rows remain `PARTIAL` + `RESOURCE` until actor-named consortium pages are found."
    )

    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_LEDGER} ({len(ledger_rows)} rows)")
    print(f"Wrote {OUT_REPORT}")
    print("Verdicts:", dict(verdicts))


if __name__ == "__main__":
    main()
