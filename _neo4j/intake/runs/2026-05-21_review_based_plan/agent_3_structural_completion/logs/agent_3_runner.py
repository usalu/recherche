"""Agent 3 runner - R3 structural edges and R9 stub edge rename.

Usage:
    python agent_3_runner.py preflight
    python agent_3_runner.py r3
    python agent_3_runner.py r9
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

from neo4j import GraphDatabase

THIS_FILE = Path(__file__).resolve()
RUN_DIR = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[6]
PLAN_RUN_DIR = RUN_DIR.parent
sys.path.insert(0, str(REPO_ROOT / "_scripts"))

from neo4j_env import resolve_connection  # noqa: E402

AGENT = "agent_3_structural_completion"
DATABASE = "mit-bestand"
MIG_DIR = RUN_DIR / "migrations"
LOG_DIR = RUN_DIR / "logs"
REPORT_DIR = RUN_DIR / "reports"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_driver():
    uri, user, password, _database = resolve_connection()
    if not uri or not user:
        raise SystemExit("Missing Neo4j connection. Check .cursor/mcp.json or NEO4J_* env vars.")
    return GraphDatabase.driver(uri, auth=(user, password))


def split_statements(cypher_text: str) -> list[str]:
    statements: list[str] = []
    current: list[str] = []
    for raw_line in cypher_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            current.append(line)
            continue
        current.append(line)
        if stripped.endswith(";"):
            stmt = "\n".join(current).strip()
            cleaned = "\n".join(
                ln for ln in stmt.splitlines() if not ln.strip().startswith("//")
            ).strip()
            if cleaned.endswith(";"):
                cleaned = cleaned[:-1].rstrip()
            if cleaned:
                statements.append(cleaned)
            current = []
    trailing = "\n".join(current).strip()
    if trailing:
        cleaned = "\n".join(
            ln for ln in trailing.splitlines() if not ln.strip().startswith("//")
        ).strip()
        if cleaned:
            statements.append(cleaned)
    return statements


def flag_exists(*relative_parts: str) -> bool:
    return (PLAN_RUN_DIR.joinpath(*relative_parts)).is_file()


def dependency_status(phase: str) -> dict:
    r1 = flag_exists("agent_1_evidence_honesty", "PHASE_R1_DONE.flag")
    r7_done = flag_exists("agent_5_loader_hardening", "PHASE_R7_DONE.flag")
    r7_ab = flag_exists("agent_5_loader_hardening", "PHASE_R7_AB_DONE.flag")
    r3_done = (RUN_DIR / "PHASE_R3_DONE.flag").is_file()
    status = {
        "phase": phase.upper(),
        "r1_done": r1,
        "r7_done": r7_done,
        "r7_ab_done": r7_ab,
        "r3_done": r3_done,
        "can_run": False,
        "missing": [],
    }
    if phase == "r3":
        status["can_run"] = r1 and (r7_done or r7_ab)
        if not r1:
            status["missing"].append("agent_1_evidence_honesty/PHASE_R1_DONE.flag")
        if not (r7_done or r7_ab):
            status["missing"].append(
                "agent_5_loader_hardening/PHASE_R7_DONE.flag or PHASE_R7_AB_DONE.flag"
            )
    elif phase == "r9":
        status["can_run"] = r3_done
        if not r3_done:
            status["missing"].append("agent_3_structural_completion/PHASE_R3_DONE.flag")
    else:
        status["can_run"] = True
    return status


def scalar(session, cypher: str, key: str = "c") -> int:
    row = session.run(cypher).single()
    return 0 if row is None else int(row[key])


def collect_rows(session, cypher: str) -> list[dict]:
    return [dict(row) for row in session.run(cypher)]


def probe(session) -> dict:
    return {
        "captured_at_utc": utc_now(),
        "total_nodes": scalar(session, "MATCH (n) RETURN count(n) AS c"),
        "total_rels": scalar(session, "MATCH ()-[r]->() RETURN count(r) AS c"),
        "projekt": scalar(session, "MATCH (p:Projekt) RETURN count(p) AS c"),
        "bauwerk": scalar(session, "MATCH (b:Bauwerk) RETURN count(b) AS c"),
        "bauteilgruppe": scalar(session, "MATCH (bg:Bauteilgruppe) RETURN count(bg) AS c"),
        "reuse_rule": scalar(session, "MATCH (r:ReuseRule) RETURN count(r) AS c"),
        "hat_bauteilgruppe": scalar(session, "MATCH ()-[r:HAT_BAUTEILGRUPPE]->() RETURN count(r) AS c"),
        "from_donor": scalar(session, "MATCH ()-[r:FROM_DONOR]->() RETURN count(r) AS c"),
        "into_receiver": scalar(session, "MATCH ()-[r:INTO_RECEIVER]->() RETURN count(r) AS c"),
        "nutzt_material": scalar(session, "MATCH ()-[r:NUTZT_MATERIAL]->() RETURN count(r) AS c"),
        "liegt_in_land": scalar(session, "MATCH ()-[r:LIEGT_IN_LAND]->() RETURN count(r) AS c"),
        "applies_in": scalar(session, "MATCH ()-[r:APPLIES_IN]->() RETURN count(r) AS c"),
        "applies_to": scalar(session, "MATCH ()-[r:APPLIES_TO]->() RETURN count(r) AS c"),
        "has_bauwerk_total": scalar(session, "MATCH ()-[r:HAS_BAUWERK]->() RETURN count(r) AS c"),
        "has_bauwerk_donor": scalar(session, "MATCH ()-[r:HAS_BAUWERK {role:'donor'}]->() RETURN count(r) AS c"),
        "has_bauwerk_receiver": scalar(session, "MATCH ()-[r:HAS_BAUWERK {role:'receiver'}]->() RETURN count(r) AS c"),
        "relevant_for": scalar(session, "MATCH ()-[r:RELEVANT_FOR]->() RETURN count(r) AS c"),
        "assoziiert_mit_projekt": scalar(session, "MATCH ()-[r:ASSOZIIERT_MIT_PROJEKT]->() RETURN count(r) AS c"),
        "stub_project_link": scalar(session, "MATCH ()-[r:STUB_PROJECT_LINK]->() RETURN count(r) AS c"),
        "origin_distribution": collect_rows(
            session,
            "MATCH ()-[r]->() WHERE r.evidence_origin IS NOT NULL "
            "RETURN r.evidence_origin AS origin, count(r) AS c ORDER BY c DESC",
        ),
        "r1_origin_enum_violations": scalar(
            session,
            "MATCH ()-[r]->() WHERE r.evidence_origin IS NOT NULL "
            "AND NOT r.evidence_origin IN "
            "['source_curated','topology_synthesized','registry_derived','inferred','external_unfolded'] "
            "RETURN count(r) AS c",
        ),
    }


def counters_to_dict(counters) -> dict:
    names = [
        "nodes_created",
        "nodes_deleted",
        "relationships_created",
        "relationships_deleted",
        "properties_set",
        "labels_added",
        "labels_removed",
    ]
    return {name: getattr(counters, name) for name in names if getattr(counters, name)}


def execute_file(driver, migration_filename: str, phase: str, audit_fp) -> None:
    migration_path = MIG_DIR / migration_filename
    statements = split_statements(migration_path.read_text(encoding="utf-8"))
    log(f"{phase}: executing {migration_filename} ({len(statements)} statements)")
    with driver.session(database=DATABASE, default_access_mode="WRITE") as session:
        for index, stmt in enumerate(statements):
            started = utc_now()
            t0 = perf_counter()
            try:
                result = session.run(stmt)
                records = [row.data() for row in result]
                summary = result.consume()
                entry = {
                    "phase": phase,
                    "migration": migration_filename,
                    "statement_index": index,
                    "started_utc": started,
                    "elapsed_ms": round((perf_counter() - t0) * 1000, 1),
                    "records": records[:20],
                    "records_total": len(records),
                    "counters": counters_to_dict(summary.counters),
                }
                audit_fp.write(json.dumps(entry, ensure_ascii=True) + "\n")
                preview = stmt.splitlines()[0][:96]
                log(f"  OK {migration_filename} [{index + 1}/{len(statements)}]: {preview}")
            except Exception as exc:
                audit_fp.write(
                    json.dumps(
                        {
                            "phase": phase,
                            "migration": migration_filename,
                            "statement_index": index,
                            "started_utc": started,
                            "error": str(exc),
                            "statement_preview": stmt[:300],
                        },
                        ensure_ascii=True,
                    )
                    + "\n"
                )
                raise


def run_gates(session, phase: str) -> tuple[dict, bool]:
    if phase == "r3":
        gates = {
            "has_bauwerk_total": {
                "cypher": (
                    "MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:FROM_DONOR]->(b:Bauwerk) "
                    "WITH count(DISTINCT coalesce(p.id, elementId(p)) + '|' + coalesce(b.id, elementId(b))) AS donor_expected "
                    "MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:INTO_RECEIVER]->(b:Bauwerk) "
                    "WITH donor_expected, count(DISTINCT coalesce(p.id, elementId(p)) + '|' + coalesce(b.id, elementId(b))) AS receiver_expected "
                    "MATCH ()-[r:HAS_BAUWERK]->() "
                    "RETURN count(r) AS c, donor_expected + receiver_expected AS expected"
                ),
                "expect": "matches BG-derived topology count",
                "ok": lambda v: v["c"] == v["expected"] and v["c"] > 0,
            },
            "has_bauwerk_donor": {
                "cypher": "MATCH ()-[r:HAS_BAUWERK {role:'donor'}]->() RETURN count(r) AS c",
                "expect": ">= 80",
                "ok": lambda v: v["c"] >= 80,
            },
            "has_bauwerk_receiver": {
                "cypher": "MATCH ()-[r:HAS_BAUWERK {role:'receiver'}]->() RETURN count(r) AS c",
                "expect": ">= 80",
                "ok": lambda v: v["c"] >= 80,
            },
            "project_with_bg_path_no_has_bauwerk": {
                "cypher": (
                    "MATCH (p:Projekt) "
                    "WHERE exists{(p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:FROM_DONOR|INTO_RECEIVER]->(:Bauwerk)} "
                    "AND NOT exists{(p)-[:HAS_BAUWERK]->()} "
                    "RETURN count(p) AS violations"
                ),
                "expect": "0",
                "ok": lambda v: v["violations"] == 0,
            },
            "relevant_for_total": {
                "cypher": "MATCH ()-[r:RELEVANT_FOR]->() RETURN count(r) AS c",
                "expect": ">= 5",
                "ok": lambda v: v["c"] >= 5,
            },
            "holbein_rule_count": {
                "cypher": (
                    "MATCH (p:Projekt {id:'p_holbein_gardens_london'}) "
                    "OPTIONAL MATCH (:ReuseRule)-[r:RELEVANT_FOR]->(p) "
                    "RETURN count(r) AS c"
                ),
                "expect": ">= 1",
                "ok": lambda v: v["c"] >= 1,
            },
            "ferme_du_rail_rule_count": {
                "cypher": (
                    "MATCH (p:Projekt {id:'p_ferme_du_rail_paris'}) "
                    "OPTIONAL MATCH (:ReuseRule)-[r:RELEVANT_FOR]->(p) "
                    "RETURN count(r) AS c"
                ),
                "expect": "0",
                "ok": lambda v: v["c"] == 0,
            },
            "has_bauwerk_evidence": {
                "cypher": (
                    "MATCH ()-[r:HAS_BAUWERK]->() "
                    "WHERE r.evidence_origin <> 'topology_synthesized' "
                    "OR r.evidence_basis IS NULL OR r.evidence_confidence IS NULL "
                    "OR r.evidence_source_id IS NULL OR r.migration_origin IS NULL "
                    "RETURN count(r) AS violations"
                ),
                "expect": "0",
                "ok": lambda v: v["violations"] == 0,
            },
            "relevant_for_evidence": {
                "cypher": (
                    "MATCH ()-[r:RELEVANT_FOR]->() "
                    "WHERE r.evidence_origin <> 'topology_synthesized' "
                    "OR r.evidence_basis IS NULL OR r.evidence_confidence IS NULL "
                    "OR r.evidence_source_id IS NULL OR r.migration_origin IS NULL "
                    "RETURN count(r) AS violations"
                ),
                "expect": "0",
                "ok": lambda v: v["violations"] == 0,
            },
        }
    elif phase == "r9":
        gates = {
            "old_type_remaining": {
                "cypher": "MATCH ()-[r:ASSOZIIERT_MIT_PROJEKT]->() RETURN count(r) AS violations",
                "expect": "0",
                "ok": lambda v: v["violations"] == 0,
            },
            "new_type_count": {
                "cypher": "MATCH ()-[r:STUB_PROJECT_LINK]->() RETURN count(r) AS c",
                "expect": "200",
                "ok": lambda v: v["c"] == 200,
            },
            "needs_verification_preserved": {
                "cypher": (
                    "MATCH ()-[r:STUB_PROJECT_LINK]->() "
                    "WHERE r.needs_verification IS NULL OR r.needs_verification = false "
                    "RETURN count(r) AS violations"
                ),
                "expect": "0",
                "ok": lambda v: v["violations"] == 0,
            },
        }
    else:
        raise ValueError(f"Unknown phase: {phase}")

    results = {}
    passed = True
    for name, gate in gates.items():
        row = session.run(gate["cypher"]).single()
        value = dict(row) if row is not None else {}
        ok = bool(gate["ok"](value))
        value["_pass"] = ok
        value["_expect"] = gate["expect"]
        results[name] = value
        if not ok:
            passed = False
    return results, passed


def extra_metrics(session, include_residuals: bool = True) -> dict:
    metrics = {
        "has_bauwerk_top20": collect_rows(
            session,
            "MATCH (p:Projekt)-[r:HAS_BAUWERK]->(b:Bauwerk) "
            "RETURN p.id AS projekt_id, "
            "sum(CASE WHEN r.role='donor' THEN 1 ELSE 0 END) AS donor, "
            "sum(CASE WHEN r.role='receiver' THEN 1 ELSE 0 END) AS receiver, "
            "count(DISTINCT b) AS distinct_bauwerk "
            "ORDER BY donor + receiver DESC, projekt_id ASC LIMIT 20",
        ),
        "relevant_for_per_rule": collect_rows(
            session,
            "MATCH (rule:ReuseRule) "
            "OPTIONAL MATCH (rule)-[r:RELEVANT_FOR]->(:Projekt) "
            "RETURN rule.id AS rule_id, count(r) AS projekt_count "
            "ORDER BY projekt_count DESC, rule_id ASC",
        ),
    }
    if include_residuals:
        metrics["residual_project_no_building_path"] = collect_rows(
            session,
            "MATCH (p:Projekt) "
            "WHERE exists{(p)-[:BELEGT_IN]->(:Quelle {quelltyp:'case_markdown'})} "
            "AND NOT exists{(p)-[:HAS_BAUWERK]->()} "
            "RETURN p.id AS projekt_id ORDER BY projekt_id",
        )
    return metrics


def artifact_block() -> str:
    files = sorted(path for path in RUN_DIR.rglob("*") if path.is_file())
    if not files:
        return "_no files written_"
    return "\n".join(str(path.relative_to(REPO_ROOT)).replace("\\", "/") for path in files)


def write_report(phase: str, verdict: str, pre: dict, post: dict | None, gates: dict | None, deps: dict, metrics: dict | None) -> None:
    completed = utc_now()
    after = post or pre
    delta_has = after["has_bauwerk_total"] - pre["has_bauwerk_total"]
    delta_relevant = after["relevant_for"] - pre["relevant_for"]
    delta_stub = after["stub_project_link"] - pre["stub_project_link"]
    gate_rows = ""
    if gates:
        gate_rows = "\n".join(
            f"| {name} | {value.get('_expect', '')} | {json.dumps({k: v for k, v in value.items() if not k.startswith('_')}, ensure_ascii=True)} | {'PASS' if value.get('_pass') else 'FAIL'} |"
            for name, value in gates.items()
        )
    else:
        gate_rows = "| _not run_ | _dependency gate_ | _not run_ | BLOCKED |"

    report = f"""# Agent 3 - Phase {phase.upper()} Report

- **Agent:** {AGENT}
- **Database:** {DATABASE}
- **Branch:** wip/kinan2 working tree
- **Completed (UTC):** {completed}
- **Verdict:** {verdict}

## Executive summary

Agent 3 artefacts for R3/R9 are present under this run directory. R3 creates direct `:Projekt-[:HAS_BAUWERK]->:Bauwerk` edges from Bauteilgruppe topology and `:ReuseRule-[:RELEVANT_FOR]->:Projekt` edges from country/material topology. R9 renames `:ASSOZIIERT_MIT_PROJEKT` to `:STUB_PROJECT_LINK`, but is gated behind R3 completion.

## Before / after counts

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Total relationships | {pre['total_rels']} | {after['total_rels']} | {after['total_rels'] - pre['total_rels']} |
| HAS_BAUWERK total | {pre['has_bauwerk_total']} | {after['has_bauwerk_total']} | {delta_has} |
| HAS_BAUWERK donor | {pre['has_bauwerk_donor']} | {after['has_bauwerk_donor']} | {after['has_bauwerk_donor'] - pre['has_bauwerk_donor']} |
| HAS_BAUWERK receiver | {pre['has_bauwerk_receiver']} | {after['has_bauwerk_receiver']} | {after['has_bauwerk_receiver'] - pre['has_bauwerk_receiver']} |
| RELEVANT_FOR | {pre['relevant_for']} | {after['relevant_for']} | {delta_relevant} |
| ASSOZIIERT_MIT_PROJEKT | {pre['assoziiert_mit_projekt']} | {after['assoziiert_mit_projekt']} | {after['assoziiert_mit_projekt'] - pre['assoziiert_mit_projekt']} |
| STUB_PROJECT_LINK | {pre['stub_project_link']} | {after['stub_project_link']} | {delta_stub} |

## Acceptance gates

| Gate | Expected | Live | Verdict |
|---|---|---|---|
{gate_rows}

## Issues raised

- Dependency status: `{json.dumps(deps, ensure_ascii=True)}`.
- D3 is deferred: no `:Bauteilgruppe-[:DERIVED_FROM]->:Bauteilgruppe` edge added in this phase.

## Distribution snippets

```json
{json.dumps(metrics or {}, indent=2, ensure_ascii=True)}
```

## Artefacts

```
{artifact_block()}
```

## Handoff

Run `python _neo4j/intake/runs/2026-05-21_review_based_plan/agent_3_structural_completion/logs/agent_3_runner.py r3` after Agent 5 has written `PHASE_R7_DONE.flag` or `PHASE_R7_AB_DONE.flag`. Run R9 only after R3 is integrated and `PHASE_R3_DONE.flag` exists.
"""
    (REPORT_DIR / "agent_3_report.md").write_text(report, encoding="utf-8")


def log(message: str) -> None:
    line = f"[{utc_now()}] {message}"
    print(line)
    with (LOG_DIR / "agent_3_progress.log").open("a", encoding="utf-8") as fp:
        fp.write(line + "\n")


def run_preflight() -> None:
    deps = dependency_status("r3")
    driver = get_driver()
    try:
        with driver.session(database=DATABASE, default_access_mode="READ") as session:
            pre = probe(session)
            metrics = extra_metrics(session, include_residuals=False)
        (LOG_DIR / "agent_3_probe_pre.json").write_text(
            json.dumps(pre, indent=2, ensure_ascii=True), encoding="utf-8"
        )
        write_report("preflight", "BLOCKED" if not deps["can_run"] else "READY", pre, None, None, deps, metrics)
        log(f"Preflight complete. can_run={deps['can_run']} missing={deps['missing']}")
    finally:
        driver.close()


def run_phase(phase: str) -> None:
    deps = dependency_status(phase)
    if not deps["can_run"]:
        driver = get_driver()
        try:
            with driver.session(database=DATABASE, default_access_mode="READ") as session:
                pre = probe(session)
                metrics = extra_metrics(session, include_residuals=False)
            (LOG_DIR / "agent_3_probe_pre.json").write_text(
                json.dumps(pre, indent=2, ensure_ascii=True), encoding="utf-8"
            )
            write_report(phase, "BLOCKED", pre, None, None, deps, metrics)
        finally:
            driver.close()
        raise SystemExit(f"{phase.upper()} blocked; missing dependency flags: {', '.join(deps['missing'])}")

    migrations = {
        "r3": ["mig_r3_a_has_bauwerk.cypher", "mig_r3_b_reuse_rule_relevant_for.cypher"],
        "r9": ["mig_r9_stub_project_link_rename.cypher"],
    }[phase]
    driver = get_driver()
    try:
        with driver.session(database=DATABASE, default_access_mode="READ") as session:
            pre = probe(session)
        (LOG_DIR / "agent_3_probe_pre.json").write_text(
            json.dumps(pre, indent=2, ensure_ascii=True), encoding="utf-8"
        )

        with (LOG_DIR / "agent_3_audit.jsonl").open("w", encoding="utf-8") as audit_fp:
            for filename in migrations:
                execute_file(driver, filename, phase, audit_fp)

        with driver.session(database=DATABASE, default_access_mode="READ") as session:
            post = probe(session)
            gates, verified = run_gates(session, phase)
            metrics = extra_metrics(session)
        (LOG_DIR / "agent_3_probe_post.json").write_text(
            json.dumps(post, indent=2, ensure_ascii=True), encoding="utf-8"
        )
        (LOG_DIR / "agent_3_gates.json").write_text(
            json.dumps(gates, indent=2, ensure_ascii=True), encoding="utf-8"
        )
        (LOG_DIR / "agent_3_metrics.json").write_text(
            json.dumps(metrics, indent=2, ensure_ascii=True), encoding="utf-8"
        )
        flag_data = {
            "phase": phase.upper(),
            "agent": AGENT,
            "completed_at_utc": utc_now(),
            "verified": verified,
            "verification_query_results": gates,
            "extra": metrics,
        }
        (RUN_DIR / f"PHASE_{phase.upper()}_DONE.flag").write_text(
            json.dumps(flag_data, indent=2, ensure_ascii=True), encoding="utf-8"
        )
        write_report(phase, "PASS" if verified else "FAIL", pre, post, gates, deps, metrics)
        if not verified:
            raise SystemExit(f"{phase.upper()} verification failed.")
        log(f"{phase.upper()} complete. PASS.")
    finally:
        driver.close()


def main() -> None:
    command = sys.argv[1].lower() if len(sys.argv) > 1 else "preflight"
    if command == "preflight":
        run_preflight()
    elif command in {"r3", "r9"}:
        run_phase(command)
    else:
        raise SystemExit("Usage: python agent_3_runner.py [preflight|r3|r9]")


if __name__ == "__main__":
    main()
