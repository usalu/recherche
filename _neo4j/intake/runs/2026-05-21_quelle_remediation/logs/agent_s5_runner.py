"""Agent S5 — visibility surfacing
===================================
Denormalises source quality, freshness and trust summaries onto
:Projekt, :Bauwerk, :Akteur nodes so that a single click in Neo4j
Browser shows the complete provenance picture.

Actual graph topology used (verified against live db 2026-05-22):
  Projekt  -[:BELEGT_IN]->  :ExternalLink              (2 756 edges)
  Projekt  -[:BELEGT_IN]->  :Dossier -[:ZITIERT_QUELLE]-> :ExternalLink
  Projekt  -[:ZITIERT_QUELLE]-> :ExternalLink           (1 edge)
  Bauwerk  -[:BELEGT_IN]->  :Dossier -[:ZITIERT_QUELLE]-> :ExternalLink
  Akteur   -[:BELEGT_IN]->  :ExternalLink               (361 edges)
  Akteur   -[:BELEGT_IN]->  :Dossier -[:ZITIERT_QUELLE]-> :ExternalLink
  Akteur   -[:ZITIERT_QUELLE]-> :ExternalLink           (366 edges)
  HAS_SOURCE_LINK only on :ReuseRule — not used here.

Writes on every :Projekt/:Bauwerk/:Akteur:
  source_urls               list<string> (capped at 100)
  source_count              int
  source_quality_summary    map
  source_freshness_summary  map
  source_trust_score        float | NULL
  source_urls_updated_at    date string

Also seeds :DataIssue {kind:'excessive_sources_on_node'} for > 50 URLs.

Run from repo root:
    python _neo4j/intake/runs/2026-05-21_quelle_remediation/logs/agent_s5_runner.py
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve().parents[5]
_SCRIPTS = _REPO / "_scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402
from neo4j import GraphDatabase  # noqa: E402

# ─── paths ────────────────────────────────────────────────────────────────────

RUN_DIR = Path(__file__).resolve().parent.parent
S3_DIR = RUN_DIR / "agent_s3_content_verifier"
S4_DIR = RUN_DIR / "agent_s4_schema_cleanup"
S5_DIR = RUN_DIR / "agent_s5_visibility"
LOG_DIR = S5_DIR / "logs"
REPORT_DIR = S5_DIR / "reports"
FLAG_FILE = S5_DIR / "PHASE_S5_DONE.flag"
S3_FLAG = S3_DIR / "PHASE_S3_DONE.flag"
S4_FLAG = S4_DIR / "PHASE_S4_DONE.flag"

LOG_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ─── Cypher: fetch all (node_id, ExternalLink props, citation edge props) ─────

# Paths from a given node type to ExternalLink via every relationship route.
# UNION ALL so one result-row = one citation path.
# Returns: node_id, url, url_status, wayback, last_checked, vs, vscore

_PROJEKT_PATHS_Q = """
MATCH (p:Projekt)-[r:BELEGT_IN]->(ext:ExternalLink)
RETURN p.id AS node_id,
       ext.url AS url,
       ext.url_status AS url_status,
       ext.url_wayback_snapshot AS wayback,
       ext.url_last_checked_at AS last_checked,
       r.verification_status AS vs,
       r.verification_score AS vscore

UNION ALL

MATCH (p:Projekt)-[:BELEGT_IN]->(:Dossier)-[r:ZITIERT_QUELLE]->(ext:ExternalLink)
RETURN p.id AS node_id,
       ext.url AS url,
       ext.url_status AS url_status,
       ext.url_wayback_snapshot AS wayback,
       ext.url_last_checked_at AS last_checked,
       r.verification_status AS vs,
       r.verification_score AS vscore

UNION ALL

MATCH (p:Projekt)-[r:ZITIERT_QUELLE]->(ext:ExternalLink)
RETURN p.id AS node_id,
       ext.url AS url,
       ext.url_status AS url_status,
       ext.url_wayback_snapshot AS wayback,
       ext.url_last_checked_at AS last_checked,
       r.verification_status AS vs,
       r.verification_score AS vscore
"""

_BAUWERK_PATHS_Q = """
MATCH (b:Bauwerk)-[:BELEGT_IN]->(:Dossier)-[r:ZITIERT_QUELLE]->(ext:ExternalLink)
RETURN b.id AS node_id,
       ext.url AS url,
       ext.url_status AS url_status,
       ext.url_wayback_snapshot AS wayback,
       ext.url_last_checked_at AS last_checked,
       r.verification_status AS vs,
       r.verification_score AS vscore
"""

_AKTEUR_PATHS_Q = """
MATCH (a:Akteur)-[r:BELEGT_IN]->(ext:ExternalLink)
RETURN a.id AS node_id,
       ext.url AS url,
       ext.url_status AS url_status,
       ext.url_wayback_snapshot AS wayback,
       ext.url_last_checked_at AS last_checked,
       r.verification_status AS vs,
       r.verification_score AS vscore

UNION ALL

MATCH (a:Akteur)-[:BELEGT_IN]->(:Dossier)-[r:ZITIERT_QUELLE]->(ext:ExternalLink)
RETURN a.id AS node_id,
       ext.url AS url,
       ext.url_status AS url_status,
       ext.url_wayback_snapshot AS wayback,
       ext.url_last_checked_at AS last_checked,
       r.verification_status AS vs,
       r.verification_score AS vscore

UNION ALL

MATCH (a:Akteur)-[r:ZITIERT_QUELLE]->(ext:ExternalLink)
RETURN a.id AS node_id,
       ext.url AS url,
       ext.url_status AS url_status,
       ext.url_wayback_snapshot AS wayback,
       ext.url_last_checked_at AS last_checked,
       r.verification_status AS vs,
       r.verification_score AS vscore
"""

# Fetch all node IDs for a given label (so nodes with zero sources get stamped too)
_ALL_NODES_Q = "MATCH (n:{label}) RETURN n.id AS id"

# Write back summaries
_SET_SUMMARIES_Q = """
UNWIND $rows AS row
MATCH (n {id: row.id})
SET n.source_urls              = row.source_urls,
    n.source_count             = row.source_count,
    n.source_quality_summary   = row.source_quality_summary,
    n.source_freshness_summary = row.source_freshness_summary,
    n.source_trust_score       = row.source_trust_score,
    n.source_urls_updated_at   = row.updated_at,
    n.migration_origin         = coalesce(n.migration_origin, '') + ' | mig_s5_visibility'
"""

_EXCESSIVE_SOURCES_Q = """
MATCH (n) WHERE (n:Projekt OR n:Bauwerk OR n:Akteur) AND n.source_count > 50
MERGE (i:DataIssue {id: 'di_excessive_sources__' + n.id})
ON CREATE SET
  i.kind            = 'excessive_sources_on_node',
  i.severity        = 'low',
  i.ref_label       = labels(n)[0],
  i.ref_id          = n.id,
  i.found_at        = date(),
  i.found_by        = 's5_visibility',
  i.status          = 'open',
  i.resolution_note = 'Node has ' + toString(n.source_count) +
                      ' source URLs. Review whether all are warranted.'
MERGE (i)-[:CONCERNS]->(n)
RETURN count(i) AS n_issues
"""

# ─── acceptance gates ─────────────────────────────────────────────────────────

GATES = [
    ("Every :Projekt has source_urls",
     "MATCH (p:Projekt) WHERE p.source_urls IS NULL RETURN count(p) AS n",
     0),
    ("Every :Projekt has source_quality_summary",
     "MATCH (p:Projekt) WHERE p.source_quality_summary IS NULL RETURN count(p) AS n",
     0),
    ("Every :Projekt has source_freshness_summary",
     "MATCH (p:Projekt) WHERE p.source_freshness_summary IS NULL RETURN count(p) AS n",
     0),
    ("Every :Bauwerk has source_urls",
     "MATCH (b:Bauwerk) WHERE b.source_urls IS NULL RETURN count(b) AS n",
     0),
    ("Every :Akteur has source_urls",
     "MATCH (a:Akteur) WHERE a.source_urls IS NULL RETURN count(a) AS n",
     0),
]

SPOT_CHECKS = [
    ("Stuttgart 210",
     "MATCH (p:Projekt {id:'p_stuttgart_210'}) RETURN p.source_count AS sc, p.source_trust_score AS ts"),
    ("Holbein Gardens",
     "MATCH (p:Projekt {id:'p_holbein_gardens_london'}) RETURN p.source_count AS sc, p.source_trust_score AS ts"),
]


# ─── helpers ──────────────────────────────────────────────────────────────────

def _date_to_str(val) -> str | None:
    """Convert neo4j Date / datetime / str to ISO string, or None."""
    if val is None:
        return None
    if hasattr(val, "iso_format"):       # neo4j.time.Date or DateTime
        return val.iso_format()
    if isinstance(val, (date, datetime)):
        return val.isoformat()
    return str(val)


def _url_reachability(url_status: str | None, wayback: str | None) -> float:
    if url_status == "reachable_2xx":
        return 1.0
    if url_status == "reachable_3xx_to_4xx":
        return 0.7
    if url_status and url_status.startswith("dead_") and wayback:
        return 0.5
    return 0.0


_VERIF_GRADES: dict[str, float] = {
    "verbatim_match": 1.0,
    "paraphrase_match": 0.85,
    "token_match": 0.75,
    "target_page_dead": 0.5,
    "no_text_match": 0.0,
    "cookie_wall_detected": 0.0,
    "unsupported_javascript_required": 0.4,
    "language_mismatch": 0.0,
}


def _verif_grade(vs: str | None, vscore: float | None) -> float:
    if vs in _VERIF_GRADES:
        return _VERIF_GRADES[vs]
    return float(vscore) if vscore is not None else 0.0


def _aggregate(paths: list[dict]) -> dict:
    """
    Aggregate a list of path records for one node into S5 summary fields.
    Each path record has: url, url_status, wayback, last_checked, vs, vscore.
    """
    # Build per-URL dedup map for freshness
    url_status_map: dict[str, str | None] = {}
    url_wayback_map: dict[str, str | None] = {}
    url_checked_map: dict[str, str | None] = {}

    for p in paths:
        url = p.get("url")
        if not url:
            continue
        if url not in url_status_map:
            url_status_map[url] = p.get("url_status")
            url_wayback_map[url] = p.get("wayback")
        lc = _date_to_str(p.get("last_checked"))
        if lc and (url not in url_checked_map
                   or url_checked_map[url] is None
                   or lc > url_checked_map[url]):
            url_checked_map[url] = lc

    unique_urls = sorted(url_status_map.keys())

    # Freshness (per unique URL)
    n_reachable    = sum(1 for s in url_status_map.values() if s == "reachable_2xx")
    n_reachable_3xx = sum(1 for s in url_status_map.values() if s == "reachable_3xx_to_4xx")
    n_dead         = sum(1 for s in url_status_map.values()
                         if s and s.startswith("dead_"))
    n_unchecked    = sum(1 for s in url_status_map.values()
                         if s is None or s == "unchecked")
    n_wayback      = sum(1 for u, s in url_status_map.items()
                         if s and s.startswith("dead_") and url_wayback_map.get(u))

    latest_check: str | None = None
    for lc in url_checked_map.values():
        if lc and (latest_check is None or lc > latest_check):
            latest_check = lc

    # Quality (per citation edge — all paths, not deduplicated)
    valid_paths = [p for p in paths if p.get("url")]
    n_verbatim  = sum(1 for p in valid_paths if p.get("vs") == "verbatim_match")
    n_para      = sum(1 for p in valid_paths
                      if p.get("vs") in ("paraphrase_match", "token_match"))
    n_nomatch   = sum(1 for p in valid_paths
                      if p.get("vs") in ("no_text_match", "cookie_wall_detected",
                                          "unsupported_javascript_required", "language_mismatch"))
    n_v_dead    = sum(1 for p in valid_paths if p.get("vs") == "target_page_dead")
    n_v_unchk   = sum(1 for p in valid_paths
                      if p.get("vs") is None
                      or p.get("vs") == "unchecked"
                      or (p.get("vs") or "").startswith("skipped_"))

    # Trust score (mean of path_score = url_reachability × verif_grade over all paths)
    if not valid_paths:
        trust_score = None
    else:
        total = sum(
            _url_reachability(p.get("url_status"), p.get("wayback"))
            * _verif_grade(p.get("vs"), p.get("vscore"))
            for p in valid_paths
        )
        trust_score = round(total / len(valid_paths), 4)

    # Neo4j does not support map-typed properties — store summaries as JSON strings.
    return {
        "source_urls":    unique_urls[:100],
        "source_count":   len(unique_urls),
        "source_quality_summary": json.dumps({
            "n_verbatim":   n_verbatim,
            "n_paraphrase": n_para,
            "n_no_match":   n_nomatch,
            "n_dead":       n_v_dead,
            "n_unchecked":  n_v_unchk,
        }),
        "source_freshness_summary": json.dumps({
            "n_reachable":         n_reachable,
            "n_reachable_via_3xx": n_reachable_3xx,
            "n_dead":              n_dead,
            "n_unchecked":         n_unchecked,
            "n_wayback_fallback":  n_wayback,
            "latest_check_date":   latest_check,
        }),
        "source_trust_score": trust_score,
        "updated_at": str(date.today()),
    }


def _process_label(session, label: str, paths_query: str, stats: dict) -> list[dict]:
    """Fetch all citation paths for `label`, aggregate, return rows for UNWIND."""
    print(f"  [{label}] Fetching citation paths…")
    all_rows = session.run(paths_query).data()
    print(f"  [{label}] {len(all_rows):,} path rows fetched")

    # Group by node_id
    by_node: dict[str, list[dict]] = defaultdict(list)
    for row in all_rows:
        by_node[row["node_id"]].append(row)

    # Ensure every node (even those with zero paths) gets a record
    all_ids = [r["id"] for r in session.run(_ALL_NODES_Q.format(label=label)).data()]
    print(f"  [{label}] {len(all_ids)} nodes total")

    write_rows = []
    for node_id in all_ids:
        agg = _aggregate(by_node.get(node_id, []))
        row = {"id": node_id, **agg}
        write_rows.append(row)

    stats[label] = {
        "total": len(all_ids),
        "with_sources": sum(1 for r in write_rows if r["source_count"] > 0),
        "avg_source_count": (
            round(sum(r["source_count"] for r in write_rows) / len(write_rows), 2)
            if write_rows else 0
        ),
        "avg_trust_score": (
            round(
                sum(r["source_trust_score"] for r in write_rows
                    if r["source_trust_score"] is not None)
                / max(1, sum(1 for r in write_rows if r["source_trust_score"] is not None)),
                4,
            )
            if write_rows else None
        ),
        "trust_null": sum(1 for r in write_rows if r["source_trust_score"] is None),
    }

    return write_rows


def main() -> None:
    # ── pre-flight ─────────────────────────────────────────────────────────
    if not S3_FLAG.exists():
        print("[ABORT] PHASE_S3_DONE.flag missing — run S3 first.")
        sys.exit(1)
    if not S4_FLAG.exists():
        print("[ABORT] PHASE_S4_DONE.flag missing — run S4 first.")
        sys.exit(1)

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    print(f"[INFO] Connected to Neo4j at {uri}, database={database}")

    stats: dict = {}
    audit_log = []

    with driver.session(database=database) as session:

        # ── S5.A  Projekt ───────────────────────────────────────────────
        print("\n[Stage 1] Processing :Projekt…")
        rows = _process_label(session, "Projekt", _PROJEKT_PATHS_Q, stats)
        print(f"  Writing {len(rows)} :Projekt summaries…")
        session.run(_SET_SUMMARIES_Q, rows=rows)
        audit_log.extend({"label": "Projekt", "id": r["id"],
                           "source_count": r["source_count"],
                           "source_trust_score": r["source_trust_score"]}
                          for r in rows)

        # ── S5.B  Bauwerk ───────────────────────────────────────────────
        print("\n[Stage 2] Processing :Bauwerk…")
        rows = _process_label(session, "Bauwerk", _BAUWERK_PATHS_Q, stats)
        print(f"  Writing {len(rows)} :Bauwerk summaries…")
        session.run(_SET_SUMMARIES_Q, rows=rows)
        audit_log.extend({"label": "Bauwerk", "id": r["id"],
                           "source_count": r["source_count"],
                           "source_trust_score": r["source_trust_score"]}
                          for r in rows)

        # ── S5.C  Akteur ────────────────────────────────────────────────
        print("\n[Stage 3] Processing :Akteur…")
        rows = _process_label(session, "Akteur", _AKTEUR_PATHS_Q, stats)
        print(f"  Writing {len(rows)} :Akteur summaries…")
        session.run(_SET_SUMMARIES_Q, rows=rows)
        audit_log.extend({"label": "Akteur", "id": r["id"],
                           "source_count": r["source_count"],
                           "source_trust_score": r["source_trust_score"]}
                          for r in rows)

        # ── S5.D  DataIssue for > 50 URLs ───────────────────────────────
        print("\n[Stage 4] Seeding DataIssue for nodes with > 50 source URLs…")
        r = session.run(_EXCESSIVE_SOURCES_Q).single()
        n_issues = r["n_issues"] if r else 0
        stats["excessive_sources_issues"] = n_issues
        print(f"  {n_issues} DataIssue(s) created/merged")

        # ── acceptance gates ────────────────────────────────────────────
        print("\n[Stage 5] Running acceptance gates…")
        gate_results = []
        all_passed = True
        for desc, cypher, expected in GATES:
            val = session.run(cypher).single()["n"]
            passed = val == expected
            if not passed:
                all_passed = False
            status = "PASS" if passed else "FAIL"
            print(f"  [{status}] {desc}: {val} (expected {expected})")
            gate_results.append({"gate": desc, "result": val,
                                  "expected": expected, "pass": passed})

        print("\n[Stage 6] Spot-checks…")
        spot_results = []
        for name, cypher in SPOT_CHECKS:
            rec = session.run(cypher).single()
            if rec:
                sc = rec["sc"]
                ts = rec["ts"]
                print(f"  {name}: source_count={sc}, trust_score={ts}")
                spot_results.append({"name": name, "source_count": sc,
                                      "source_trust_score": ts})
            else:
                print(f"  {name}: node not found")
                spot_results.append({"name": name, "error": "node_not_found"})

        # ── top / bottom 10 by trust score (Projekt) ───────────────────
        top10 = session.run(
            "MATCH (p:Projekt) WHERE p.source_trust_score IS NOT NULL "
            "RETURN p.id AS id, p.source_trust_score AS ts "
            "ORDER BY ts DESC LIMIT 10"
        ).data()
        bottom10 = session.run(
            "MATCH (p:Projekt) WHERE p.source_trust_score IS NOT NULL "
            "RETURN p.id AS id, p.source_trust_score AS ts "
            "ORDER BY ts ASC LIMIT 10"
        ).data()

    driver.close()

    # ── write logs & reports ────────────────────────────────────────────────
    audit_path = LOG_DIR / "s5_audit.jsonl"
    with audit_path.open("w", encoding="utf-8") as fh:
        for row in audit_log:
            fh.write(json.dumps(row, default=str) + "\n")
    print(f"\n[INFO] Audit log: {audit_path}")

    report = {
        "completed_utc": datetime.now(timezone.utc).isoformat(),
        "database": database,
        "verified": all_passed,
        "stats": stats,
        "gate_results": gate_results,
        "spot_checks": spot_results,
        "top10_by_trust": top10,
        "bottom10_by_trust": bottom10,
    }
    report_json = REPORT_DIR / "S5_REPORT.json"
    report_json.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(f"[INFO] Report: {report_json}")

    report_md = REPORT_DIR / "agent_s5_report.md"
    p_stats = stats.get("Projekt", {})
    b_stats = stats.get("Bauwerk", {})
    a_stats = stats.get("Akteur", {})

    top10_lines = "\n".join(f"  {i+1}. {r['id']}  ts={r['ts']}" for i, r in enumerate(top10))
    bot10_lines = "\n".join(f"  {i+1}. {r['id']}  ts={r['ts']}" for i, r in enumerate(bottom10))
    spot_lines  = "\n".join(
        f"  {r['name']}: source_count={r.get('source_count','?')}, "
        f"trust_score={r.get('source_trust_score','?')}"
        for r in spot_results
    )
    gate_lines  = "\n".join(
        f"  [{'PASS' if g['pass'] else 'FAIL'}] {g['gate']}: {g['result']}"
        for g in gate_results
    )

    report_md.write_text(f"""# Agent S5 visibility report

Completed UTC: {report['completed_utc']}
Database: {database}
Verified: {all_passed}

## Summary

| Label   | Total | With sources | Avg source count | Avg trust score | Trust=NULL |
|---------|------:|-------------:|-----------------:|----------------:|-----------:|
| Projekt | {p_stats.get('total',0)} | {p_stats.get('with_sources',0)} | {p_stats.get('avg_source_count',0)} | {p_stats.get('avg_trust_score','n/a')} | {p_stats.get('trust_null',0)} |
| Bauwerk | {b_stats.get('total',0)} | {b_stats.get('with_sources',0)} | {b_stats.get('avg_source_count',0)} | {b_stats.get('avg_trust_score','n/a')} | {b_stats.get('trust_null',0)} |
| Akteur  | {a_stats.get('total',0)} | {a_stats.get('with_sources',0)} | {a_stats.get('avg_source_count',0)} | {a_stats.get('avg_trust_score','n/a')} | {a_stats.get('trust_null',0)} |

Excessive-sources DataIssues: {stats.get('excessive_sources_issues', 0)}

## Acceptance gates
{gate_lines}

## Spot-checks
{spot_lines}

## Top 10 Projekt by trust score
{top10_lines}

## Bottom 10 Projekt by trust score
{bot10_lines}

## Logs
- {audit_path}
- {report_json}
""", encoding="utf-8")
    print(f"[INFO] Report MD: {report_md}")

    # ── HANDOFF_LOG ────────────────────────────────────────────────────────
    handoff_path = S5_DIR / "HANDOFF_LOG.md"
    handoff_path.write_text(f"""# S5 Handoff Log

Completed: {report['completed_utc']}

## Averages (Projekt)
- avg source_count : {p_stats.get('avg_source_count', '?')}
- avg trust_score  : {p_stats.get('avg_trust_score', '?')}
- trust=NULL (no sources): {p_stats.get('trust_null', '?')} / {p_stats.get('total', '?')}

## Top 10 by trust score
{top10_lines}

## Bottom 10 by trust score
{bot10_lines}

## Next step
Run Agent S6 (audit + sign-off).
""", encoding="utf-8")

    # ── done flag ──────────────────────────────────────────────────────────
    verdict = "PASS" if all_passed else "FAIL"
    FLAG_FILE.write_text(
        f"PHASE_S5_DONE\n"
        f"verified_at: {date.today()}\n"
        f"verdict: {verdict}\n"
        f"projekt_total: {p_stats.get('total', 0)}\n"
        f"projekt_with_sources: {p_stats.get('with_sources', 0)}\n"
        f"projekt_avg_trust: {p_stats.get('avg_trust_score', 'n/a')}\n"
        f"bauwerk_total: {b_stats.get('total', 0)}\n"
        f"bauwerk_with_sources: {b_stats.get('with_sources', 0)}\n"
        f"akteur_total: {a_stats.get('total', 0)}\n"
        f"akteur_with_sources: {a_stats.get('with_sources', 0)}\n"
        f"excessive_sources_issues: {stats.get('excessive_sources_issues', 0)}\n",
        encoding="utf-8",
    )
    print(f"\n[{verdict}] PHASE_S5_DONE flag written: {FLAG_FILE}")

    if not all_passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
