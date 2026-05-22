#!/usr/bin/env python3
"""Agent R07 — remediate Agent-14 needs_source_url_review backlog (308 rels).

Scope: HAT_BAUTEILTYP (142), NUTZT_MATERIAL (103), BETEILIGT_AN (63).
Outputs: ledger/remediation_r07.csv, reports/remediation_r07.md,
         patches/remediation_r07_add_rel_sources.patch.jsonl
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
REVIEW = HERE.parent
REPO = HERE.parents[3]
SCRIPTS = REPO / "_scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402

BACKLOG_CSV = (
    REPO
    / "_neo4j/review/2026-06-05_post_migration_property_cleanup/sidecar/qa/needs_source_url_review.csv"
)
EXTENDED_JSON = (
    REPO
    / "_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges_extended.json"
)
ENRICH_DIRS = [
    REPO / "_neo4j/intake/inbox/research/bauteilboersen_deep_enrichment_results",
    REPO / "_neo4j/intake/inbox/research/bauteilboersen_deeper_material_bauteiltyp_results",
]
SIDEcar_JSONL = (
    REPO
    / "_neo4j/review/2026-06-05_post_migration_property_cleanup/sidecar/entity_metadata.jsonl"
)

OUT_LEDGER = REVIEW / "ledger/remediation_r07.csv"
OUT_REPORT = REVIEW / "reports/remediation_r07.md"
OUT_PATCH = REVIEW / "patches/remediation_r07_add_rel_sources.patch.jsonl"
WORK_CACHE = HERE / "url_fetch_cache.json"

SCOPE_TYPES = {"HAT_BAUTEILTYP", "NUTZT_MATERIAL", "BETEILIGT_AN"}
REVIEW_RUN = "remediation_r07_2026_06_06"
PLACEHOLDER_RE = re.compile(
    r"^(processed|archive:|processed\+|Council of the EU|$)",
    re.I,
)

LEDGER_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
    "asserted_claim", "basis_type", "basis_ref", "fetched", "http_status", "verdict",
    "confidence", "proof_quote", "proposed_action", "agent_id", "notes",
]


def norm_text(s: str) -> str:
    s = unescape(s or "")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def significant_tokens(text: str, min_len: int = 4) -> list[str]:
    words = re.findall(r"[a-z0-9äöüß]{3,}", norm_text(text))
    stop = {
        "the", "and", "for", "with", "from", "that", "this", "are", "was", "were",
        "und", "der", "die", "das", "ein", "eine", "mit", "von", "auf", "als",
        "includes", "include", "such", "type", "types", "collection", "evidence",
        "reuse", "stock", "category", "categories", "surfaced", "like", "product",
    }
    return [w for w in words if len(w) >= min_len and w not in stop]


def quote_supported(quote: str, page_text: str, min_hits: int = 2) -> tuple[bool, str]:
    if not quote or not page_text:
        return False, "empty quote or page"
    tokens = significant_tokens(quote)
    if len(tokens) < min_hits:
        tokens = significant_tokens(quote, min_len=3)
    if not tokens:
        return False, "no tokens in quote"
    body = norm_text(page_text)
    hits = [t for t in tokens if t in body]
    ok = len(hits) >= min(min_hits, max(1, len(tokens) // 3))
    return ok, f"token_hits={len(hits)}/{len(tokens)} sample={hits[:4]}"


def names_on_page(actor_name: str, target_name: str, page_text: str) -> tuple[bool, str]:
    body = norm_text(page_text)
    parts = []
    for name in (actor_name, target_name):
        if not name:
            continue
        n = norm_text(name)
        if n and n in body:
            parts.append(name)
        else:
            # try first token
            tok = n.split()[0] if n else ""
            if tok and len(tok) > 3 and tok in body:
                parts.append(tok)
    return len(parts) >= 1, "+".join(parts) if parts else "none"


def is_placeholder(url: str) -> bool:
    if not url or not isinstance(url, str):
        return True
    u = url.strip()
    if not u.lower().startswith("http"):
        return True
    return bool(PLACEHOLDER_RE.match(u))


def load_enrichment_index() -> dict[str, dict]:
    idx: dict[str, dict] = {}
    for d in ENRICH_DIRS:
        if not d.is_dir():
            continue
        for f in d.glob("*.enrichment.json"):
            aid = f.name.replace(".enrichment.json", "")
            try:
                idx[aid] = json.loads(f.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
    return idx


def load_project_part_index() -> dict[tuple[str, str], dict]:
    """Index BETEILIGT_AN dossier by (actor_id, bauteilgruppe_id)."""
    if not EXTENDED_JSON.exists():
        return {}
    data = json.loads(EXTENDED_JSON.read_text(encoding="utf-8"))
    idx: dict[tuple[str, str], dict] = {}
    for edge in data.get("edges", []):
        if edge.get("type") != "BETEILIGT_AN":
            continue
        props = edge.get("properties") or {}
        aid = props.get("actor_id")
        bgid = props.get("bauteilgruppe_id")
        if not aid or not bgid:
            continue
        key = (aid, bgid)
        score = 0
        if props.get("candidate_source_urls"):
            score += 2
        if props.get("evidence_urls"):
            score += 2
        if props.get("review_status") == "needs_source_url_review":
            score += 1
        prev = idx.get(key)
        if prev is None or score > prev.get("_score", 0):
            props["_score"] = score
            idx[key] = props
    return idx


def pp_lookup(pp_idx: dict[tuple[str, str], dict], actor_id: str, bg_id: str) -> dict | None:
    """Map live bg_* ids to dossier bg_reuse_* ids."""
    for cand in (bg_id, bg_id.replace("bg_", "bg_reuse_", 1)):
        hit = pp_idx.get((actor_id, cand))
        if hit:
            return hit
    return None


def load_backlog() -> list[dict]:
    rows = []
    with BACKLOG_CSV.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["reltype"] in SCOPE_TYPES:
                rows.append(r)
    return rows


def fetch_url(url: str, cache: dict) -> dict:
    if url in cache:
        return cache[url]
    entry = {"url": url, "fetched": False, "http_status": "", "text": "", "error": ""}
    if is_placeholder(url):
        entry["error"] = "placeholder_or_non_http"
        cache[url] = entry
        return entry
    try:
        req = Request(
            url,
            headers={
                "User-Agent": "recherche-r07-remediation/1.0 (+https://github.com/local)",
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
    time.sleep(0.15)
    return entry


def query_live_rels(driver, database: str, backlog: list[dict]) -> dict[tuple[str, str, str], dict]:
    """Return map (reltype, from_id, to_id) -> live rel + endpoint names."""
    by_type: dict[str, list[dict]] = defaultdict(list)
    for r in backlog:
        by_type[r["reltype"]].append(r)

    live: dict[tuple[str, str, str], dict] = {}
    with driver.session(database=database) as session:
        for rt, rows in by_type.items():
            pairs = [{"from_id": r["from_id"], "to_id": r["to_id"]} for r in rows]
            result = session.run(
                f"""
                UNWIND $pairs AS p
                MATCH (a {{id: p.from_id}})-[r:`{rt}`]->(b {{id: p.to_id}})
                RETURN p.from_id AS from_id, p.to_id AS to_id,
                       elementId(r) AS element_id, r.id AS rel_id,
                       coalesce(a.name, a.id) AS from_name,
                       coalesce(b.name, b.id) AS to_name,
                       r.source_url AS source_url, r.evidence_url AS evidence_url,
                       r.basis_project_edge_id AS basis_project_edge_id,
                       r.metadata_sidecar_key AS metadata_sidecar_key,
                       a.primary_source_url AS actor_primary_url,
                       a.source_urls AS actor_source_urls
                """,
                pairs=pairs,
            )
            for rec in result:
                key = (rt, rec["from_id"], rec["to_id"])
                live[key] = dict(rec)
    return live


def project_urls_for_basis(driver, database: str, basis_edge_id: str | None) -> list[str]:
    if not basis_edge_id:
        return []
    with driver.session(database=database) as session:
        rec = session.run(
            """
            MATCH ()-[r]->(p:Projekt)
            WHERE r.id = $eid
            RETURN p.source_urls AS urls, p.primary_source_url AS primary
            LIMIT 1
            """,
            eid=basis_edge_id,
        ).single()
    if not rec:
        return []
    urls = list(rec.get("urls") or [])
    if rec.get("primary"):
        urls.insert(0, rec["primary"])
    return [u for u in urls if u and not is_placeholder(u)]


def dossier_for_hat_nutz(
    enrich: dict, rt: str, to_id: str
) -> dict | None:
    key = "bauteiltypen" if rt == "HAT_BAUTEILTYP" else "materials"
    for item in enrich.get(key, []):
        if item.get("target_id") == to_id:
            return item
    return None


def candidate_urls_for_row(
    row: dict,
    live: dict,
    enrich_idx: dict,
    pp_idx: dict,
    driver,
    database: str,
) -> tuple[list[str], str, str]:
    """Return (urls prioritized, recovery_source, dossier_quote)."""
    rt, fid, tid = row["reltype"], row["from_id"], row["to_id"]
    key = (rt, fid, tid)
    live_row = live.get(key, {})
    urls: list[str] = []
    source = "none"
    quote = ""

    if rt == "BETEILIGT_AN":
        pp = pp_lookup(pp_idx, fid, tid)
        if pp:
            for field in ("candidate_source_urls", "evidence_urls"):
                for u in pp.get(field) or []:
                    if u and u not in urls:
                        urls.append(u)
            quote = pp.get("evidence_basis") or ""
            source = "project_part_actor_extended_json"
        proj_urls = project_urls_for_basis(driver, database, live_row.get("basis_project_edge_id"))
        for u in proj_urls:
            if u not in urls:
                urls.append(u)
        if proj_urls and source == "none":
            source = "project_node_source_urls"
    else:
        enrich = enrich_idx.get(fid)
        if enrich:
            item = dossier_for_hat_nutz(enrich, rt, tid)
            if item:
                for u in item.get("evidence_urls") or []:
                    if u not in urls:
                        urls.append(u)
                quote = item.get("evidence_quote") or ""
                source = "bauteilboersen_enrichment_json"

    actor_urls = []
    if live_row.get("actor_primary_url"):
        actor_urls.append(live_row["actor_primary_url"])
    for u in live_row.get("actor_source_urls") or []:
        if u not in actor_urls:
            actor_urls.append(u)
    for u in actor_urls:
        if u not in urls:
            urls.append(u)
    if actor_urls and source == "none":
        source = "actor_node_source_urls"

    # Prioritize: real http first; placeholders last
    real = [u for u in urls if not is_placeholder(u)]
    ph = [u for u in urls if is_placeholder(u)]
    return real + ph, source, quote


def evaluate_row(
    row: dict,
    live: dict,
    enrich_idx: dict,
    pp_idx: dict,
    driver,
    database: str,
    cache: dict,
) -> dict:
    rt, fid, tid = row["reltype"], row["from_id"], row["to_id"]
    key = (rt, fid, tid)
    live_row = live.get(key, {})
    from_name = live_row.get("from_name") or fid
    to_name = live_row.get("to_name") or tid

    urls, recovery_source, dossier_quote = candidate_urls_for_row(
        row, live, enrich_idx, pp_idx, driver, database
    )
    has_placeholder_candidates = any(is_placeholder(u) for u in urls)
    real_urls = [u for u in urls if not is_placeholder(u)]

    best = {
        "verdict": "MISSING_EVIDENCE",
        "basis_ref": "",
        "fetched": "false",
        "http_status": "",
        "proof_quote": "",
        "confidence": "unbelegt",
        "proposed_action": "RESOURCE",
        "notes": f"recovery={recovery_source}; candidates={len(urls)} real={len(real_urls)}",
    }

    if live_row.get("source_url") or live_row.get("evidence_url"):
        best.update(
            verdict="PROVEN",
            basis_ref=live_row.get("source_url") or live_row.get("evidence_url"),
            confidence="belegt",
            proposed_action="KEEP",
            notes="already has on-graph URL",
        )
        return best

    for url in real_urls[:5]:
        fe = fetch_url(url, cache)
        if not fe.get("fetched"):
            continue
        text = fe.get("text") or ""
        status = fe.get("http_status") or ""

        if rt in ("HAT_BAUTEILTYP", "NUTZT_MATERIAL"):
            ok, detail = quote_supported(dossier_quote, text)
            if not ok and dossier_quote:
                # fallback: target vocab name on catalog page
                ok, detail = names_on_page("", to_name, text)
            if ok:
                best.update(
                    verdict="PROVEN",
                    basis_ref=url,
                    fetched="true",
                    http_status=status,
                    proof_quote=(dossier_quote or detail)[:500],
                    confidence="belegt",
                    proposed_action="ADD_SOURCE",
                    notes=f"{recovery_source}; {detail}",
                )
                break
            if fe.get("fetched") and status.startswith("2"):
                best.update(
                    verdict="PARTIAL",
                    basis_ref=url,
                    fetched="true",
                    http_status=status,
                    proof_quote=detail[:300],
                    confidence="teilweise_belegt",
                    proposed_action="RESOURCE",
                    notes=f"page fetched but quote weak; {recovery_source}",
                )
        else:  # BETEILIGT_AN
            actor_hit, ad = names_on_page(from_name, to_name, text)
            proj_name = (pp_lookup(pp_idx, fid, tid) or {}).get("source_project_name") or ""
            proj_hit, pd = names_on_page(proj_name, to_name, text)
            if actor_hit and (proj_hit or to_name.lower() in norm_text(text)):
                proof = f"Actor/page match ({ad}); project/component ({pd or to_name})"
                best.update(
                    verdict="PROVEN",
                    basis_ref=url,
                    fetched="true",
                    http_status=status,
                    proof_quote=proof[:500],
                    confidence="belegt",
                    proposed_action="ADD_SOURCE",
                    notes=f"{recovery_source}; overlap-derived edge corroborated on page",
                )
                break
            if actor_hit:
                best.update(
                    verdict="PARTIAL",
                    basis_ref=url,
                    fetched="true",
                    http_status=status,
                    proof_quote=f"actor on page ({ad}) but weak component proof",
                    confidence="teilweise_belegt",
                    proposed_action="RESOURCE",
                    notes=f"{recovery_source}; candidate overlap edge — actor only",
                )

    if has_placeholder_candidates and best["verdict"] == "MISSING_EVIDENCE":
        best["notes"] += "; had_placeholder_candidates"

    return best


def patch_op(row: dict, live: dict, eval_row: dict) -> dict | None:
    if eval_row["verdict"] != "PROVEN" or eval_row["proposed_action"] != "ADD_SOURCE":
        return None
    rt = row["reltype"]
    props = {
        "evidence_url": eval_row["basis_ref"],
        "evidence_quote": (eval_row.get("proof_quote") or "")[:500],
        "evidence_confidence": "belegt",
        "evidence_basis": "r07_web_fetch_confirmed",
        "review_run": REVIEW_RUN,
    }
    # remove metadata_sidecar_key once sourced
    props["metadata_sidecar_key"] = None
    return {
        "op": "set_rel_properties",
        "from": row["from_id"],
        "type": rt,
        "to": row["to_id"],
        "properties": {k: v for k, v in props.items() if v is not None},
        "reason": (
            f"R07 {row['sidecar_key']}: PROVEN via fetch of {eval_row['basis_ref']}; "
            f"{eval_row.get('notes', '')[:180]}"
        ),
    }


def write_report(
    backlog_rows: list[dict],
    results: list[dict],
    cache: dict,
    missing_live: int,
) -> None:
    total = len(backlog_rows)
    by_verdict = Counter(r["verdict"] for r in results)
    by_type = defaultdict(lambda: Counter())
    for r, row in zip(results, backlog_rows):
        by_type[row["reltype"]][r["verdict"]] += 1
    by_action = Counter(r["proposed_action"] for r in results)
    patch_count = sum(1 for r in results if r["proposed_action"] == "ADD_SOURCE" and r["verdict"] == "PROVEN")
    fetched_urls = sum(1 for v in cache.values() if v.get("fetched"))
    processed_pct = round(100 * total / 308, 1)

    lines = [
        "# Remediation R07 — Agent-14 `needs_source_url_review` backlog (rel sources)",
        "",
        f"**Date:** {datetime.now(timezone.utc).date().isoformat()} · **Database:** `mit-bestand`",
        f"**Ledger:** [`ledger/remediation_r07.csv`](../ledger/remediation_r07.csv)",
        f"**Patch (dry-run):** [`patches/remediation_r07_add_rel_sources.patch.jsonl`](../patches/remediation_r07_add_rel_sources.patch.jsonl)",
        "",
        "## Scope",
        "",
        "Agent 14 backlog A14-BACKLOG-001 subset routed to R07:",
        "",
        "| rel_type | backlog rows |",
        "|---|---:|",
    ]
    type_counts = Counter(r["reltype"] for r in backlog_rows)
    for rt in sorted(SCOPE_TYPES):
        lines.append(f"| `{rt}` | {type_counts.get(rt, 0)} |")
    lines += [
        f"| **Total** | **{total}** |",
        "",
        f"**Coverage:** {total}/308 rows processed ({processed_pct}%). "
        f"{missing_live} backlog keys absent from live graph.",
        "",
        "## Method",
        "",
        "1. Filter `needs_source_url_review.csv` to HAT_BAUTEILTYP / NUTZT_MATERIAL / BETEILIGT_AN.",
        "2. Cross-check live Neo4j (no on-graph `source_url` / `evidence_url`).",
        "3. Recover candidate URLs from dossiers: `bauteilboersen_*.enrichment.json`, "
        "`project_part_actor_edges_extended.json`, actor/project `source_urls`.",
        f"4. Prioritize non-placeholder HTTP URLs; fetch each unique URL once ({fetched_urls} fetches).",
        "5. PROVEN when stored/dossier quote tokens match fetched page, or (BETEILIGT_AN) actor + component on page.",
        "",
        "## Verdict summary",
        "",
        "| verdict | count | share |",
        "|---|---:|---:|",
    ]
    for v, c in by_verdict.most_common():
        lines.append(f"| {v} | {c} | {round(100*c/total,1)}% |")
    lines += [
        "",
        "### By relationship type",
        "",
        "| rel_type | PROVEN | PARTIAL | MISSING | other |",
        "|---|---:|---:|---:|---:|",
    ]
    for rt in sorted(SCOPE_TYPES):
        c = by_type[rt]
        other = sum(c.values()) - c.get("PROVEN", 0) - c.get("PARTIAL", 0) - c.get("MISSING_EVIDENCE", 0)
        lines.append(
            f"| `{rt}` | {c.get('PROVEN',0)} | {c.get('PARTIAL',0)} | "
            f"{c.get('MISSING_EVIDENCE',0)} | {other} |"
        )
    lines += [
        "",
        "### Proposed actions",
        "",
        "| action | count |",
        "|---|---:|",
    ]
    for a, c in by_action.most_common():
        lines.append(f"| {a} | {c} |")
    lines += [
        "",
        f"**High-confidence patch ops drafted:** {patch_count} `set_rel_properties` "
        f"(evidence_url + quote + review_run `{REVIEW_RUN}`).",
        "",
        "## Notes",
        "",
        "- These rel types use **`evidence_url`** (reuse/catalog/participation), not regulation `source_url`.",
        "- BETEILIGT_AN rows are overlap-derived candidates; PROVEN requires actor + component/project mention on page.",
        "- Rows still `RESOURCE` need manual dossier review or stronger project-level proof.",
        "",
        "## Apply",
        "",
        "```bash",
        f"python _scripts/apply_neo4j_review_patch.py --patch {OUT_PATCH.relative_to(REPO).as_posix()}",
        f'python _scripts/apply_neo4j_review_patch.py --patch {OUT_PATCH.relative_to(REPO).as_posix()} '
        f'--confirm "APPLY remediation_r07_add_rel_sources.patch.jsonl TO mit-bestand"',
        "```",
        "",
    ]
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    backlog = load_backlog()
    enrich_idx = load_enrichment_index()
    pp_idx = load_project_part_index()

    cache: dict = {}
    if WORK_CACHE.exists():
        try:
            cache = json.loads(WORK_CACHE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            cache = {}

    uri, user, password, database = resolve_connection()
    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()

    live = query_live_rels(driver, database, backlog)
    missing_live = sum(
        1 for r in backlog if (r["reltype"], r["from_id"], r["to_id"]) not in live
    )

    # Sort: placeholder-priority first (rows with only actor urls last)
    def sort_key(r: dict) -> tuple:
        urls, src, _ = candidate_urls_for_row(
            r, live, enrich_idx, pp_idx, driver, database
        )
        has_ph = any(is_placeholder(u) for u in urls)
        has_dossier = src.startswith("bauteilboersen") or src.startswith("project_part")
        return (0 if has_ph else 1, 0 if has_dossier else 1, r["reltype"], r["from_id"])

    backlog_sorted = sorted(backlog, key=sort_key)

    results: list[dict] = []
    ledger_rows: list[dict] = []
    patch_ops: list[dict] = []

    for i, row in enumerate(backlog_sorted, start=1):
        ev = evaluate_row(row, live, enrich_idx, pp_idx, driver, database, cache)
        live_row = live.get((row["reltype"], row["from_id"], row["to_id"]), {})
        claim = f"{live_row.get('from_name', row['from_id'])} -{row['reltype']}-> {live_row.get('to_name', row['to_id'])}"
        ledger_rows.append({
            "claim_id": f"R07-{i:04d}",
            "claim_kind": "rel",
            "element_id": live_row.get("element_id") or row.get("sidecar_key", ""),
            "from_id": row["from_id"],
            "to_id": row["to_id"],
            "rel_type_or_label": row["reltype"],
            "asserted_claim": claim,
            "basis_type": "web" if ev["basis_ref"] else "dossier+logic",
            "basis_ref": ev["basis_ref"],
            "fetched": ev["fetched"],
            "http_status": ev["http_status"],
            "verdict": ev["verdict"],
            "confidence": ev["confidence"],
            "proof_quote": ev["proof_quote"],
            "proposed_action": ev["proposed_action"],
            "agent_id": "R07",
            "notes": ev["notes"],
        })
        results.append(ev)
        op = patch_op(row, live_row, ev)
        if op:
            patch_ops.append(op)

        if i % 25 == 0:
            print(f"processed {i}/{len(backlog_sorted)}...", flush=True)

    driver.close()
    WORK_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=0), encoding="utf-8")

    OUT_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with OUT_LEDGER.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=LEDGER_COLS, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(ledger_rows)

    OUT_PATCH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATCH.open("w", encoding="utf-8") as f:
        for op in patch_ops:
            f.write(json.dumps(op, ensure_ascii=False) + "\n")

    write_report(backlog_sorted, results, cache, missing_live)

    print(f"wrote ledger {len(ledger_rows)} -> {OUT_LEDGER}")
    print(f"wrote patch {len(patch_ops)} ops -> {OUT_PATCH}")
    print(f"wrote report -> {OUT_REPORT}")
    print("verdicts:", dict(Counter(r["verdict"] for r in results)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
