#!/usr/bin/env python3
"""IER-A1 — Tier A :Akteur nodes with URL on ledger (165 rows).

WebFetch basis_ref; upgrade to PROVEN when quote names entity (entity gate).
Outputs: ledger/ier_a1.csv, reports/ier_a1_report.md,
         patches/ier_a1_fix_node_sources.patch.jsonl (dry-run proposals only).
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

ELEMENT_LEDGER = HERE / "VERIFICATION_LEDGER_ELEMENT.csv"
OUT_LEDGER = HERE / "ledger" / "ier_a1.csv"
OUT_REPORT = HERE / "reports" / "ier_a1_report.md"
OUT_PATCH = HERE / "patches" / "ier_a1_fix_node_sources.patch.jsonl"
WORK_DIR = HERE / "_ier_a1_work"
WORK_CACHE = WORK_DIR / "url_fetch_cache.json"
R07_CACHE = HERE / "_agent_r07_work" / "url_fetch_cache.json"

AGENT_ID = "IER-A1"
REVIEW_RUN = "ier_a1_2026_06_06"
TIER_D = frozenset({"UNVERIFIABLE", "SCHEMA_VIOLATION", "CONTRADICTION"})

LEDGER_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
    "asserted_claim", "basis_type", "basis_ref", "fetched", "http_status", "verdict",
    "confidence", "proof_quote", "proposed_action", "agent_id", "notes",
]

SECTOR_ONLY = {
    "reuse", "circular", "sustainability", "building materials", "construction",
    "wiederverwendung", "reemploi", "baustoffe", "marktplatz", "marketplace",
    "urban mining", "circular economy", "nachhaltigkeit",
}

URL_REPAIRS = {
    "https://urselmanninterior.com": "https://www.urselmanninterior.com/",
    "https://www.tomas-architecture.com": "https://www.tomas-architecture.com/",
    "https://circularmaterialsystems.com": "https://www.circularmaterialsystems.com/",
    "https://lxsy.de": "https://www.lxsy.de/",
    "https://www.gruner-reuse.ch": "https://gruner-reuse.ch/",
    "https://www.bauteilnetz.de": "https://bauteilnetz.de/",
    "https://www.zirkulaar.de": "https://zirkulaar.de/",
}


def norm_text(s: str) -> str:
    s = unescape(s or "")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def plain_text(html: str) -> str:
    t = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", html or "")
    t = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return unescape(t)


def tokens(text: str, min_len: int = 4) -> list[str]:
    words = re.findall(r"[a-z0-9äöüß]{3,}", norm_text(text))
    stop = {
        "the", "and", "for", "with", "from", "that", "this", "are", "was", "were",
        "und", "der", "die", "das", "ein", "eine", "mit", "von", "auf", "als",
        "gmbh", "ag", "ltd", "inc", "studio", "studios", "architects", "architecten",
        "ingenieure", "group", "company", "official", "website", "home",
    }
    return [w for w in words if len(w) >= min_len and w not in stop]


def name_candidates(nid: str, name: str) -> list[str]:
    cands: list[str] = []
    if name:
        cands.append(norm_text(name))
    cands.append(norm_text(nid.replace("_", " ")))
    parts = re.split(r"[_\s]+", nid)
    if len(parts) >= 2:
        cands.append(norm_text(" ".join(parts[:2])))
    if len(parts) >= 3 and parts[-1] in ("gmbh", "ag", "ltd", "sa", "bv"):
        cands.append(norm_text(" ".join(parts[:-1])))
    # known aliases
    aliases = {
        "albert_and_co": ["albert et cie", "albert et compagnie"],
        "baubuero_in_situ": ["baubüro in situ", "baubuero in situ"],
        "stiftung_chance_bauteile_zuerich_glattbrugg": ["chance bauteile", "stiftung chance"],
        "syphon_ag_bauteilboerse_biel_bruegg": ["syphon ag", "syphon"],
        "zirkulie_bauteilboerse_triesen": ["zirkulie", "zirkulie bauteilboerse"],
        "re_store_harvestmap_vienna": ["re-store", "harvestmap"],
        "new_horizon_urban_mining": ["new horizon", "new horizon urban mining"],
        "collectif_cancan": ["collectif cancan", "cancan"],
        "la_fabrique_de_bordeaux_metropole": ["la fab", "fabrique de bordeaux"],
    }
    for a in aliases.get(nid, []):
        cands.append(norm_text(a))
    seen: set[str] = set()
    out: list[str] = []
    for c in cands:
        if c and c not in seen:
            seen.add(c)
            out.append(c)
    return out


def entity_on_page(nid: str, name: str, body_norm: str) -> tuple[bool, str]:
    for c in name_candidates(nid, name):
        if len(c) >= 3 and c in body_norm:
            return True, f"full_match:{c[:40]}"
    hits = [t for t in tokens(name or nid, 3) if t in body_norm]
    if len(hits) >= 2:
        return True, f"token_hits:{','.join(hits[:4])}"
    if len(hits) == 1 and len(hits[0]) >= 4:
        return True, f"token_hit:{hits[0]}"
    id_toks = [t for t in tokens(nid.replace("_", " "), 3) if t in body_norm]
    if id_toks and len(id_toks[0]) >= 4:
        return True, f"id_token:{id_toks[0]}"
    return False, "no_entity_match"


def sector_only_page(body_norm: str, entity_hit: bool) -> bool:
    if entity_hit:
        return False
    sector_hits = sum(1 for s in SECTOR_ONLY if s in body_norm)
    return sector_hits >= 2


def extract_quote(raw_html: str, nid: str, name: str, max_len: int = 300) -> str:
    text = plain_text(raw_html)
    text_norm = norm_text(text)
    needle = None
    for c in name_candidates(nid, name):
        if len(c) >= 3 and c in text_norm:
            needle = c
            break
    if not needle:
        for t in tokens(name or nid, 4):
            if t in text_norm:
                needle = t
                break
    if not needle:
        return text.strip()[:max_len]
    # map back to raw text positions via normalized sliding window
    words = re.split(r"(\s+)", text)
    buf = ""
    for i, w in enumerate(words):
        buf += w
        if needle in norm_text(buf):
            start = max(0, len(buf) - 200)
            snippet = buf[start : start + max_len + 80].strip()
            snippet = re.sub(r"\s+", " ", snippet)
            return snippet[:max_len]
    idx = text_norm.find(needle)
    if idx >= 0:
        return text[max(0, idx - 40) : idx + max_len - 40].strip()[:max_len]
    return text.strip()[:max_len]


def load_scope() -> list[dict]:
    rows: list[dict] = []
    with ELEMENT_LEDGER.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if row.get("verdict") == "PROVEN" or row.get("verdict") in TIER_D:
                continue
            if row.get("claim_kind") != "node" or row.get("rel_type_or_label") != "Akteur":
                continue
            br = row.get("basis_ref") or ""
            bt = row.get("basis_type") or ""
            if br.startswith("http") or bt in ("web", "candidate"):
                rows.append(row)
    rows.sort(key=lambda r: r.get("element_id", ""))
    return rows


def load_cache() -> dict:
    cache: dict = {}
    for path in (R07_CACHE, WORK_CACHE):
        if path.is_file():
            try:
                cache.update(json.loads(path.read_text(encoding="utf-8")))
            except json.JSONDecodeError:
                pass
    return cache


def save_cache(cache: dict) -> None:
    WORK_DIR.mkdir(parents=True, exist_ok=True)
    WORK_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_url(url: str, cache: dict, retries: int = 1) -> dict:
    url = URL_REPAIRS.get(url, url)
    if url in cache and cache[url].get("fetched"):
        return cache[url]
    entry = {"url": url, "fetched": False, "http_status": "", "text": "", "error": ""}
    for attempt in range(retries + 1):
        try:
            req = Request(
                url,
                headers={
                    "User-Agent": "recherche-ier-a1/1.0 (+local verification)",
                    "Accept": "text/html,application/xhtml+xml,application/pdf",
                },
            )
            with urlopen(req, timeout=30) as resp:
                raw = resp.read(900_000)
                entry["http_status"] = str(getattr(resp, "status", 200))
                entry["fetched"] = True
                entry["text"] = raw.decode("utf-8", errors="replace")
                break
        except HTTPError as e:
            entry["http_status"] = str(e.code)
            entry["error"] = str(e)
            try:
                entry["text"] = e.read(120_000).decode("utf-8", errors="replace")
                entry["fetched"] = True
            except Exception:
                pass
            if attempt < retries and str(e.code) in ("429", "503"):
                time.sleep(30)
                continue
            break
        except (URLError, TimeoutError, OSError) as e:
            entry["error"] = str(e)
            if attempt < retries:
                time.sleep(2)
                continue
            break
    cache[url] = entry
    time.sleep(0.12)
    return entry


def query_actors(driver, database: str, ids: list[str]) -> dict[str, dict]:
    if not ids:
        return {}
    with driver.session(database=database) as session:
        recs = session.run(
            """
            UNWIND $ids AS i
            MATCH (a:Akteur {id: i})
            RETURN a.id AS id, coalesce(a.name, a.id) AS name,
                   a.primary_source_url AS primary_source_url,
                   a.source_urls AS source_urls
            """,
            ids=ids,
        )
        return {r["id"]: dict(r) for r in recs}


def adjudicate_row(row: dict, actor: dict, cache: dict, patches: list[dict]) -> dict:
    prior_id = row.get("claim_id", "")
    nid = row.get("element_id", "")
    name = (actor or {}).get("name") or nid.replace("_", " ")
    basis_ref = (row.get("basis_ref") or "").strip()
    prior_verdict = row.get("verdict", "")
    prior_quote = (row.get("proof_quote") or "").strip()

    verdict = prior_verdict
    action = row.get("proposed_action") or "KEEP"
    confidence = row.get("confidence") or ""
    proof_quote = prior_quote
    notes = row.get("notes") or ""
    fetched_s = "false"
    http_status = ""
    basis_out = basis_ref

    urls: list[str] = []
    if basis_ref.startswith("http"):
        urls.append(basis_ref)
    if basis_ref in URL_REPAIRS:
        urls.append(URL_REPAIRS[basis_ref])
    for u in (actor or {}).get("source_urls") or []:
        if u and u.startswith("http") and u not in urls:
            urls.append(u)
    purl = (actor or {}).get("primary_source_url")
    if purl and purl.startswith("http") and purl not in urls:
        urls.insert(0, purl)

    if not urls:
        return _ledger_row(
            row, prior_id, nid, basis_ref, "false", "", "MISSING_EVIDENCE",
            confidence or "unbelegt", "", "ADD_SOURCE", "no http basis_ref",
        )

    best_partial = None
    for url in urls[:3]:
        fe = fetch_url(url, cache)
        fetched_s = str(bool(fe.get("fetched"))).lower()
        http_status = fe.get("http_status") or ""
        basis_out = url
        if not fe.get("fetched"):
            verdict = "DEAD_LINK"
            action = "RESOURCE"
            notes = f"fetch failed: {fe.get('error', '')[:120]}"
            continue
        if not http_status.startswith("2"):
            verdict = "DEAD_LINK" if http_status in ("404", "410") else "UNVERIFIABLE"
            action = "RESOURCE"
            notes = f"http {http_status}"
            continue

        body_norm = norm_text(fe.get("text") or "")
        hit, detail = entity_on_page(nid, name, body_norm)
        if hit and not sector_only_page(body_norm, hit):
            quote = extract_quote(fe["text"], nid, name)
            if len(quote) < 12:
                quote = extract_quote(fe["text"], nid, name)
            verdict = "PROVEN"
            action = "KEEP"
            confidence = "belegt"
            proof_quote = quote[:300]
            notes = f"entity gate pass; {detail}; tier-A homepage/URL fetch"
            patches.append({
                "op": "set_node_properties",
                "id": nid,
                "properties": {
                    "primary_source_url": url,
                    "source_quote": proof_quote[:500],
                    "review_run": REVIEW_RUN,
                },
                "reason": f"IER-A1 {prior_id}: {prior_verdict}→PROVEN entity named on fetched page",
            })
            break
        if sector_only_page(body_norm, hit):
            cand = {
                "verdict": "PARTIAL",
                "proof_quote": extract_quote(fe["text"], nid, name)[:300],
                "notes": "page sector/generic only; entity not named (gate G4 fail)",
            }
        else:
            cand = {
                "verdict": "PARTIAL",
                "proof_quote": extract_quote(fe["text"], nid, name)[:300],
                "notes": f"page fetched ({http_status}) but entity not named; {detail}",
            }
        if best_partial is None:
            best_partial = cand

    if verdict != "PROVEN" and best_partial:
        verdict = best_partial["verdict"]
        proof_quote = best_partial["proof_quote"]
        confidence = "teilweise_belegt"
        action = "RESOURCE" if verdict == "PARTIAL" else action
        notes = best_partial["notes"]

    if verdict == "MISSING_EVIDENCE" and fetched_s == "true":
        verdict = "PARTIAL" if http_status.startswith("2") else "DEAD_LINK"

    return _ledger_row(
        row, prior_id, nid, basis_out, fetched_s, http_status, verdict,
        confidence, proof_quote, action, notes,
    )


def _ledger_row(
    row, prior_id, nid, basis_out, fetched_s, http_status, verdict,
    confidence, proof_quote, action, notes,
) -> dict:
    return {
        "claim_id": f"IER-A1-{prior_id}",
        "claim_kind": "node",
        "element_id": nid,
        "from_id": "",
        "to_id": "",
        "rel_type_or_label": "Akteur",
        "asserted_claim": row.get("asserted_claim", f"Akteur {nid} exists"),
        "basis_type": "web",
        "basis_ref": basis_out,
        "fetched": fetched_s,
        "http_status": http_status,
        "verdict": verdict,
        "confidence": confidence,
        "proof_quote": proof_quote,
        "proposed_action": action,
        "agent_id": AGENT_ID,
        "notes": notes,
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LEDGER_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def write_report(rows: list[dict], scope_n: int, cache: dict, patches: list[dict]) -> None:
    vc = Counter(r["verdict"] for r in rows)
    ac = Counter(r["proposed_action"] for r in rows)
    upgraded = sum(1 for r in rows if r["verdict"] == "PROVEN")
    prior_proven = sum(1 for r in rows if (r.get("notes") or "").startswith("entity gate"))
    unique_urls = len({r["basis_ref"] for r in rows if r["basis_ref"].startswith("http")})
    fetches = sum(1 for v in cache.values() if isinstance(v, dict) and v.get("fetched"))

    # worst: DEAD_LINK, sector-only PARTIAL, weak fetches
    worst = sorted(
        rows,
        key=lambda r: (
            0 if r["verdict"] == "DEAD_LINK" else
            1 if r["verdict"] == "MISSING_EVIDENCE" else
            2 if r["verdict"] == "PARTIAL" and not r["proof_quote"] else 3
        ),
    )[:10]

    lines = [
        "# IER-A1 — Tier A actors with URL (internet evidence recovery)",
        "",
        f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')} · **Agent:** {AGENT_ID}",
        f"**Database:** `mit-bestand` (read-only) · **Review run:** `{REVIEW_RUN}`",
        f"**Ledger:** [`ledger/ier_a1.csv`](../ledger/ier_a1.csv)",
        f"**Patch (dry-run):** [`patches/ier_a1_fix_node_sources.patch.jsonl`](../patches/ier_a1_fix_node_sources.patch.jsonl)",
        "",
        "## Scope",
        "",
        "Non-PROVEN `:Akteur` nodes where `basis_ref` starts with `http` OR `basis_type ∈ {web,candidate}`;",
        "tier-D rows (`UNVERIFIABLE`, `SCHEMA_VIOLATION`, `CONTRADICTION`) excluded per §3 disjointness.",
        "",
        f"| Metric | Value |",
        f"|---|---:|",
        f"| Scope rows | **{scope_n}** |",
        f"| Processed | **{len(rows)}** |",
        f"| Unique URLs | {unique_urls} |",
        f"| Cache entries (this run) | {fetches} |",
        "",
        "## Method",
        "",
        "1. Load shard from `VERIFICATION_LEDGER_ELEMENT.csv` (165 tier-A actors).",
        "2. `read-cypher` for live `name`, `source_urls`, `primary_source_url`.",
        "3. `WebFetch` each `basis_ref` (reuse R07 cache; retry once on timeout).",
        "4. **Entity gate:** verbatim `proof_quote` must name organisation/person — not sector tagline only.",
        "5. Homepage alone sufficient for **existence** (IER-A1 special check); VMA edges out of scope.",
        "",
        "## Verdict summary",
        "",
        "| verdict | count | share |",
        "|---|---:|---:|",
    ]
    for v, n in vc.most_common():
        lines.append(f"| `{v}` | {n} | {100 * n / len(rows):.1f}% |")
    lines += [
        "",
        f"**Upgraded to PROVEN:** {upgraded} ({100 * upgraded / len(rows):.1f}% of shard)",
        "",
        "### Proposed actions",
        "",
        "| action | count |",
        "|---|---:|",
    ]
    for a, n in ac.most_common():
        lines.append(f"| `{a}` | {n} |")
    lines += [
        "",
        f"**Dry-run patch ops:** {len(patches)} `set_node_properties` (not applied).",
        "",
        "## Ten weakest findings",
        "",
        "| element_id | verdict | http | note |",
        "|---|---|---|---|",
    ]
    for r in worst:
        lines.append(
            f"| `{r['element_id']}` | {r['verdict']} | {r['http_status'] or '—'} | "
            f"{(r['notes'] or '')[:80]} |"
        )
    lines += [
        "",
        "## Summary",
        "",
        f"Processed **{len(rows)}/{scope_n}** tier-A `:Akteur` rows. "
        f"**{upgraded}** upgraded to `PROVEN` via live URL fetch naming the entity; "
        f"**{vc.get('PARTIAL', 0)}** remain `PARTIAL` (page loads but entity not named); "
        f"**{vc.get('DEAD_LINK', 0)}** `DEAD_LINK`. Graph unchanged (read-only wave).",
        "",
    ]
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    scope = load_scope()
    if len(scope) != 165:
        print(f"WARNING: expected 165 scope rows, got {len(scope)}", file=sys.stderr)

    ids = [r["element_id"] for r in scope]
    uri, user, password, database = resolve_connection()
    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        actors = query_actors(driver, database, ids)
    finally:
        driver.close()

    cache = load_cache()
    patches: list[dict] = []
    out_rows: list[dict] = []

    for i, row in enumerate(scope, 1):
        nid = row["element_id"]
        actor = actors.get(nid, {})
        out = adjudicate_row(row, actor, cache, patches)
        out_rows.append(out)
        if i % 25 == 0:
            print(f"  progress {i}/{len(scope)} proven={sum(1 for r in out_rows if r['verdict']=='PROVEN')}")
            write_csv(OUT_LEDGER, out_rows)

    save_cache(cache)
    write_csv(OUT_LEDGER, out_rows)

    OUT_PATCH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATCH.open("w", encoding="utf-8") as f:
        for p in patches:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    write_report(out_rows, len(scope), cache, patches)

    vc = Counter(r["verdict"] for r in out_rows)
    print(f"IER-A1 done: {len(out_rows)} rows, verdicts={dict(vc)}, patches={len(patches)}")
    print(f"  ledger -> {OUT_LEDGER}")
    print(f"  report -> {OUT_REPORT}")


if __name__ == "__main__":
    main()
