"""Orchestrator R5 runner — Bauteilgruppe disambiguation.

Reads creds from .cursor/mcp.json via _scripts.neo4j_env.resolve_connection().
Runs mig_r5_bg_disambiguation.cypher against the live mit-bestand graph.
Verifies acceptance gates, writes PHASE_R5_DONE.flag and a report.

Idempotent. Safe to re-run.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase

THIS_FILE = Path(__file__).resolve()
RUN_DIR = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
sys.path.insert(0, str(REPO_ROOT / "_scripts"))

# noinspection PyUnresolvedReferences
from neo4j_env import resolve_connection  # type: ignore

MIG_DIR = RUN_DIR / "migrations"
LOG_DIR = RUN_DIR / "logs"
REPORT_DIR = RUN_DIR / "reports"
FLAG_PATH = RUN_DIR / "PHASE_R5_DONE.flag"


def split_statements(cypher_text: str) -> list[str]:
    """Split a Cypher file into statements at top-level semicolons.

    Ignores comments and empty lines. Does NOT handle semicolons inside
    string literals (none in this migration).
    """
    statements: list[str] = []
    current: list[str] = []
    for raw_line in cypher_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            current.append(line)
            continue
        if stripped.startswith("//"):
            current.append(line)
            continue
        current.append(line)
        if stripped.endswith(";"):
            stmt = "\n".join(current).strip()
            # Strip line-comments and trailing semicolon
            cleaned = "\n".join(
                ln for ln in stmt.splitlines() if not ln.strip().startswith("//")
            ).strip()
            if cleaned.endswith(";"):
                cleaned = cleaned[:-1].rstrip()
            if cleaned:
                statements.append(cleaned)
            current = []
    return statements


def probe_distribution(session) -> dict:
    """Read the current :Bauteilgruppe bg_kind distribution + edge counts."""
    result = {}
    result["total_bg"] = session.run(
        "MATCH (bg:Bauteilgruppe) RETURN count(bg) AS c"
    ).single()["c"]
    result["bg_with_kind"] = session.run(
        "MATCH (bg:Bauteilgruppe) WHERE bg.bg_kind IS NOT NULL RETURN count(bg) AS c"
    ).single()["c"]
    result["distribution"] = {
        row["kind"]: row["c"]
        for row in session.run(
            "MATCH (bg:Bauteilgruppe) "
            "RETURN coalesce(bg.bg_kind, '<null>') AS kind, count(bg) AS c "
            "ORDER BY c DESC"
        )
    }
    result["from_donor_edges"] = session.run(
        "MATCH ()-[r:FROM_DONOR]->() RETURN count(r) AS c"
    ).single()["c"]
    result["into_receiver_edges"] = session.run(
        "MATCH ()-[r:INTO_RECEIVER]->() RETURN count(r) AS c"
    ).single()["c"]
    result["bg_with_donor_and_receiver"] = session.run(
        "MATCH (bg:Bauteilgruppe) "
        "WHERE exists{(bg)-[:FROM_DONOR]->()} AND exists{(bg)-[:INTO_RECEIVER]->()} "
        "RETURN count(bg) AS c"
    ).single()["c"]
    return result


def run_audits(session) -> tuple[bool, dict]:
    """Run the 5 audit gates from the migration. Returns (passed, details)."""
    gates = {
        "a1_bg_without_kind": (
            "MATCH (bg:Bauteilgruppe) WHERE bg.bg_kind IS NULL RETURN count(bg) AS v",
            "expect_zero",
        ),
        "a2_bg_kind_enum_violation": (
            "MATCH (bg:Bauteilgruppe) WHERE bg.bg_kind IS NOT NULL "
            "AND NOT bg.bg_kind IN ['batch','partial_batch','category'] "
            "RETURN count(bg) AS v",
            "expect_zero",
        ),
        "a3_category_with_donor_or_receiver": (
            "MATCH (bg:Bauteilgruppe {bg_kind:'category'}) "
            "WHERE exists{(bg)-[:FROM_DONOR]->()} OR exists{(bg)-[:INTO_RECEIVER]->()} "
            "RETURN count(bg) AS v",
            "expect_zero",
        ),
        "a4_batch_missing_topology": (
            "MATCH (bg:Bauteilgruppe {bg_kind:'batch'}) "
            "WHERE NOT exists{(bg)-[:FROM_DONOR]->()} OR NOT exists{(bg)-[:INTO_RECEIVER]->()} "
            "RETURN count(bg) AS v",
            "expect_zero",
        ),
        "a5_partial_batch_misclassified": (
            "MATCH (bg:Bauteilgruppe {bg_kind:'partial_batch'}) "
            "WITH bg, exists{(bg)-[:FROM_DONOR]->()} AS d, exists{(bg)-[:INTO_RECEIVER]->()} AS r "
            "WHERE (d AND r) OR (NOT d AND NOT r) "
            "RETURN count(bg) AS v",
            "expect_zero",
        ),
        "q1_canonical_batches_distinct": (
            "MATCH (d)<-[:FROM_DONOR]-(bg:Bauteilgruppe {bg_kind:'batch'})-[:INTO_RECEIVER]->(r) "
            "RETURN count(DISTINCT bg) AS v",
            "expect_at_least_254",
        ),
    }
    results = {}
    passed = True
    for name, (cypher, expectation) in gates.items():
        v = session.run(cypher).single()["v"]
        results[name] = {"value": v, "expectation": expectation}
        if expectation == "expect_zero" and v != 0:
            passed = False
        if expectation == "expect_at_least_254" and v < 254:
            passed = False
    return passed, results


def run_migration():
    conn = resolve_connection()
    driver = GraphDatabase.driver(conn["uri"], auth=(conn["user"], conn["password"]))

    migration_path = MIG_DIR / "mig_r5_bg_disambiguation.cypher"
    migration_text = migration_path.read_text(encoding="utf-8")
    statements = split_statements(migration_text)

    progress_log = LOG_DIR / "orchestrator_r5_progress.log"
    audit_jsonl = LOG_DIR / "orchestrator_r5_audit.jsonl"

    def log(msg: str) -> None:
        line = f"[{datetime.now(timezone.utc).isoformat()}] {msg}"
        print(line)
        with progress_log.open("a", encoding="utf-8") as fp:
            fp.write(line + "\n")

    log(f"Starting R5 migration ({len(statements)} statements)")
    log(f"Database: {conn.get('database', 'mit-bestand')}; URI: {conn['uri']}")

    # Pre-probe (read-only)
    with driver.session(
        database=conn.get("database", "mit-bestand"),
        default_access_mode="READ",
    ) as session:
        pre = probe_distribution(session)
    (LOG_DIR / "orchestrator_r5_probe_pre.json").write_text(
        json.dumps(pre, indent=2), encoding="utf-8"
    )
    log(f"Pre-probe: total :Bauteilgruppe = {pre['total_bg']}; "
        f"already-tagged = {pre['bg_with_kind']}; "
        f"FROM_DONOR edges = {pre['from_donor_edges']}; "
        f"INTO_RECEIVER edges = {pre['into_receiver_edges']}")

    # Execute migration statements
    with driver.session(
        database=conn.get("database", "mit-bestand"),
        default_access_mode="WRITE",
    ) as session, audit_jsonl.open("w", encoding="utf-8") as audit_fp:
        for i, stmt in enumerate(statements):
            t0 = datetime.now(timezone.utc)
            try:
                result = session.run(stmt)
                records = [dict(r) for r in result]
                summary = result.consume()
                entry = {
                    "statement_index": i,
                    "started_utc": t0.isoformat(),
                    "elapsed_ms": (
                        datetime.now(timezone.utc) - t0
                    ).total_seconds()
                    * 1000.0,
                    "records": records[:5],
                    "records_total": len(records),
                    "counters": dict(summary.counters.__dict__),
                }
                audit_fp.write(json.dumps(entry, default=str) + "\n")
                preview = stmt.splitlines()[0][:80]
                log(
                    f"  [{i+1}/{len(statements)}] OK ({entry['elapsed_ms']:.1f} ms): "
                    f"{preview}…"
                )
            except Exception as exc:
                audit_fp.write(
                    json.dumps(
                        {
                            "statement_index": i,
                            "error": str(exc),
                            "statement_preview": stmt[:200],
                        }
                    )
                    + "\n"
                )
                log(f"  [{i+1}/{len(statements)}] ERROR: {exc}")
                raise

    # Post-probe + audits
    with driver.session(
        database=conn.get("database", "mit-bestand"),
        default_access_mode="READ",
    ) as session:
        post = probe_distribution(session)
        gates_passed, gate_results = run_audits(session)
    (LOG_DIR / "orchestrator_r5_probe_post.json").write_text(
        json.dumps(post, indent=2), encoding="utf-8"
    )
    log(f"Post-probe distribution: {post['distribution']}")
    log(f"Audit gates passed: {gates_passed}")

    # Done flag
    flag_payload = {
        "phase": "R5",
        "agent": "orchestrator",
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "verified": gates_passed,
        "verification_query_results": gate_results,
        "extra": {
            "pre_distribution": pre["distribution"],
            "post_distribution": post["distribution"],
            "total_bauteilgruppe": post["total_bg"],
            "from_donor_edges": post["from_donor_edges"],
            "into_receiver_edges": post["into_receiver_edges"],
        },
    }
    FLAG_PATH.write_text(json.dumps(flag_payload, indent=2), encoding="utf-8")
    log(f"Wrote flag: {FLAG_PATH}")

    # Report skeleton (the orchestrator fills the narrative after the run)
    report_path = REPORT_DIR / "orchestrator_r5_report.md"
    if not report_path.exists():
        report_path.write_text(
            _report_template(pre, post, gate_results, gates_passed),
            encoding="utf-8",
        )
        log(f"Wrote report template: {report_path}")

    driver.close()

    if not gates_passed:
        raise SystemExit(
            "R5 verification FAILED. See logs/orchestrator_r5_audit.jsonl"
        )
    log("R5 complete. PASS.")


def _report_template(pre, post, gates, passed: bool) -> str:
    verdict = "PASS" if passed else "FAIL"
    return f"""# Orchestrator — Phase R5 Report

- **Agent:** orchestrator
- **Phase:** R5 (Bauteilgruppe disambiguation)
- **Database:** mit-bestand
- **Completed (UTC):** {datetime.now(timezone.utc).isoformat()}
- **Verdict:** {verdict}

## Executive summary

R5 tagged every `:Bauteilgruppe` with a `bg_kind` property classifying it as
`batch`, `partial_batch`, or `category` based on its FROM_DONOR / INTO_RECEIVER
edge topology.

## Before / after counts

| Metric | Before | After |
|---|---:|---:|
| Total `:Bauteilgruppe` | {pre['total_bg']} | {post['total_bg']} |
| With `bg_kind` set | {pre['bg_with_kind']} | {post['bg_with_kind']} |
| `FROM_DONOR` edges | {pre['from_donor_edges']} | {post['from_donor_edges']} |
| `INTO_RECEIVER` edges | {pre['into_receiver_edges']} | {post['into_receiver_edges']} |
| BG with both donor and receiver | {pre['bg_with_donor_and_receiver']} | {post['bg_with_donor_and_receiver']} |

## bg_kind distribution

| kind | count |
|---|---:|
{chr(10).join(f'| {k} | {v} |' for k, v in post['distribution'].items())}

## Acceptance gates

| Gate | Value | Expectation |
|---|---:|---|
{chr(10).join(f"| {name} | {res['value']} | {res['expectation']} |" for name, res in gates.items())}

## Risks / follow-ups

- BGs tagged `partial_batch` are pending dossier follow-up (donor or receiver
  identified but not both). Recommend a future ingestion pass to complete
  the topology.
- BGs tagged `category` that nonetheless carry a `menge_*` property are a
  data-quality issue: a category should not have mass. Agent 1's R8 seed pass
  should pick these up.

## Open questions

- D6 was decided property-only (no secondary labels). If queries become
  noisy, revisit.

## Artefacts

```
_neo4j/intake/runs/2026-05-21_review_based_plan/orchestrator_r5/
├── PHASE_R5_DONE.flag
├── migrations/mig_r5_bg_disambiguation.cypher
├── logs/
│   ├── orchestrator_r5_runner.py
│   ├── orchestrator_r5_progress.log
│   ├── orchestrator_r5_audit.jsonl
│   ├── orchestrator_r5_probe_pre.json
│   └── orchestrator_r5_probe_post.json
└── reports/orchestrator_r5_report.md
```

## Handoff

R5 is independent and standalone. No downstream agent waits on it specifically,
but Stage 4 integration audit will consume `bg_kind` when running honest
aggregation queries.

The completion of R5 also validates the integration pipeline (snapshot →
branch → migration → flag → log) for the heavier phases that follow.
"""


if __name__ == "__main__":
    run_migration()
