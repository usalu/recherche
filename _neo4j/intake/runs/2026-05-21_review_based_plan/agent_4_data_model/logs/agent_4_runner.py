"""Agent 4 runner - R4 Kennwert lift.

Usage:
    python agent_4_runner.py preflight
    python agent_4_runner.py r4
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any

from neo4j import GraphDatabase

THIS_FILE = Path(__file__).resolve()
RUN_DIR = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[6]
PLAN_RUN_DIR = RUN_DIR.parent
sys.path.insert(0, str(REPO_ROOT / "_scripts"))

from neo4j_env import resolve_connection  # noqa: E402

AGENT = "agent_4_data_model"
DATABASE = "mit-bestand"
MIG_DIR = RUN_DIR / "migrations"
LOG_DIR = RUN_DIR / "logs"
REPORT_DIR = RUN_DIR / "reports"
FLAG_PATH = RUN_DIR / "PHASE_R4_DONE.flag"

FACT_PROPS = {
    "reuse_share_facts": {
        "category": "reuse_share",
        "source_scope": "r4_reuse_share",
        "node_migration_origin": "mig_r4_a_lift_reuse_share_facts",
        "default_unit": "%",
    },
    "co2_facts": {
        "category": "co2_saving",
        "source_scope": "r4_co2_saving",
        "node_migration_origin": "mig_r4_b_lift_co2_facts",
        "default_unit": "t_co2",
    },
    "cost_facts": {
        "category": "cost",
        "source_scope": "r4_cost",
        "node_migration_origin": "mig_r4_c_lift_cost_facts",
        "default_unit": "EUR",
    },
}

ORIGIN_ENUM = {
    "source_curated",
    "topology_synthesized",
    "registry_derived",
    "inferred",
    "external_unfolded",
}
CONFIDENCE_ENUM = {"belegt", "teilweise_belegt", "unklar", "inferiert"}
NUMBER_RE = re.compile(r"-?\d+(?:[.,]\d+)?")
RANGE_RE = re.compile(r"(-?\d+(?:[.,]\d+)?)\s*(?:-|\u2013|\u2014)\s*(-?\d+(?:[.,]\d+)?)")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_driver():
    uri, user, password, _database = resolve_connection()
    if not uri or not user:
        raise SystemExit("Missing Neo4j connection. Check .cursor/mcp.json or NEO4J_* env vars.")
    return GraphDatabase.driver(uri, auth=(user, password))


def log(message: str) -> None:
    line = f"[{utc_now()}] {message}"
    print(line)
    with (LOG_DIR / "agent_4_progress.log").open("a", encoding="utf-8") as fp:
        fp.write(line + "\n")


def dependency_status() -> dict:
    r1_flag = PLAN_RUN_DIR / "agent_1_evidence_honesty" / "PHASE_R1_DONE.flag"
    return {
        "phase": "R4",
        "r1_done": r1_flag.is_file(),
        "can_run": r1_flag.is_file(),
        "missing": [] if r1_flag.is_file() else [str(r1_flag.relative_to(PLAN_RUN_DIR))],
    }


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


def scalar(session, cypher: str, key: str = "c") -> int:
    row = session.run(cypher).single()
    return 0 if row is None else int(row[key])


def collect_rows(session, cypher: str, **params) -> list[dict]:
    return [dict(row) for row in session.run(cypher, **params)]


def probe(session) -> dict:
    counts = {
        "captured_at_utc": utc_now(),
        "total_nodes": scalar(session, "MATCH (n) RETURN count(n) AS c"),
        "total_rels": scalar(session, "MATCH ()-[r]->() RETURN count(r) AS c"),
        "kennwert_total": scalar(session, "MATCH (kw:Kennwert) RETURN count(kw) AS c"),
        "hat_kennwert_total": scalar(session, "MATCH ()-[r:HAT_KENNWERT]->() RETURN count(r) AS c"),
        "quality_tier_facts_present": scalar(
            session,
            "MATCH (p:Projekt) WHERE p.quality_tier_facts IS NOT NULL RETURN count(p) AS c",
        ),
        "kennwert_by_category": collect_rows(
            session,
            "MATCH (kw:Kennwert) RETURN kw.category AS category, count(kw) AS c ORDER BY category",
        ),
    }
    for prop, meta in FACT_PROPS.items():
        category = meta["category"]
        counts[f"projects_with_{prop}"] = scalar(
            session,
            f"MATCH (p:Projekt) WHERE p.{prop} IS NOT NULL AND size(p.{prop}) > 0 RETURN count(p) AS c",
        )
        counts[f"{prop}_entries"] = scalar(
            session,
            f"MATCH (p:Projekt) RETURN sum(CASE WHEN p.{prop} IS NULL THEN 0 ELSE size(p.{prop}) END) AS c",
        )
        counts[f"kennwert_{category}"] = scalar(
            session,
            f"MATCH (kw:Kennwert {{category:'{category}'}}) RETURN count(kw) AS c",
        )
    return counts


def normalize_number_token(token: str) -> float | None:
    value = token.strip()
    if "," in value and "." in value:
        if value.rfind(",") > value.rfind("."):
            value = value.replace(".", "").replace(",", ".")
        else:
            value = value.replace(",", "")
    elif "," in value:
        before, after = value.split(",", 1)
        if len(after) == 3 and len(before.replace("-", "")) <= 3:
            value = before + after
        else:
            value = before + "." + after
    elif "." in value:
        before, after = value.split(".", 1)
        if len(after) == 3 and len(before.replace("-", "")) <= 3:
            value = before + after
    try:
        return float(value)
    except ValueError:
        return None


def parse_value(raw_value: Any) -> tuple[float | None, str | None, float | None, float | None]:
    if raw_value is None:
        return None, None, None, None
    text = str(raw_value).strip()
    if not text:
        return None, None, None, None
    range_match = RANGE_RE.search(text)
    if range_match:
        low = normalize_number_token(range_match.group(1))
        high = normalize_number_token(range_match.group(2))
        if low is not None and high is not None:
            return None, text, low, high
    number_match = NUMBER_RE.search(text)
    if not number_match:
        return None, text, None, None
    return normalize_number_token(number_match.group(0)), text, None, None


def evidence_origin(confidence: str, source_id: str | None) -> str:
    if confidence == "inferiert":
        return "inferred"
    if source_id:
        return "source_curated"
    return "topology_synthesized"


def normalize_confidence(raw: Any) -> str:
    confidence = str(raw or "unklar").strip()
    return confidence if confidence in CONFIDENCE_ENUM else "unklar"


def load_fact_rows(session) -> tuple[list[dict], list[dict]]:
    projects = collect_rows(
        session,
        "MATCH (p:Projekt) "
        "WHERE p.reuse_share_facts IS NOT NULL OR p.co2_facts IS NOT NULL OR p.cost_facts IS NOT NULL "
        "RETURN p.id AS project_id, p.reuse_share_facts AS reuse_share_facts, "
        "p.co2_facts AS co2_facts, p.cost_facts AS cost_facts ORDER BY p.id",
    )
    rows: list[dict] = []
    errors: list[dict] = []
    for project in projects:
        project_id = project["project_id"]
        for prop, meta in FACT_PROPS.items():
            entries = project.get(prop) or []
            for index, raw in enumerate(entries):
                try:
                    fact = json.loads(raw) if isinstance(raw, str) else dict(raw)
                except Exception as exc:
                    errors.append(
                        {
                            "project_id": project_id,
                            "property": prop,
                            "index": index,
                            "error": str(exc),
                            "raw": raw,
                        }
                    )
                    continue
                raw_value = fact.get("wert", fact.get("value"))
                wert, wert_text, wert_min, wert_max = parse_value(raw_value)
                confidence = normalize_confidence(fact.get("confidence"))
                source_id = fact.get("source_id")
                if source_id == "":
                    source_id = None
                origin = evidence_origin(confidence, source_id)
                if origin not in ORIGIN_ENUM:
                    origin = "topology_synthesized"
                kennwert = fact.get("kennwert") or fact.get("basis") or f"{meta['category']}_{index}"
                unit = fact.get("einheit") or fact.get("unit") or meta["default_unit"]
                rows.append(
                    {
                        "id": f"kw_{project_id}_{meta['category']}_{index}",
                        "project_id": project_id,
                        "category": meta["category"],
                        "kennwert": str(kennwert) if kennwert is not None else None,
                        "wert": wert,
                        "wert_text": wert_text,
                        "wert_min": wert_min,
                        "wert_max": wert_max,
                        "einheit": str(unit) if unit is not None else None,
                        "method": fact.get("method"),
                        "bilanzgrenze": fact.get("bilanzgrenze"),
                        "loader": fact.get("loader") or "unknown",
                        "source_id": source_id,
                        "fact_index": index,
                        "raw_property": prop,
                        "source_scope": meta["source_scope"],
                        "node_migration_origin": meta["node_migration_origin"],
                        "evidence_origin": origin,
                        "evidence_basis": "cell_citation" if source_id else "legacy_fact_property",
                        "evidence_confidence": confidence,
                        "evidence_excerpt": None,
                    }
                )
    return rows, errors


def execute_migration(driver, rows: list[dict]) -> list[dict]:
    statements = split_statements((MIG_DIR / "mig_r4_kennwert_lift.cypher").read_text(encoding="utf-8"))
    audit_entries: list[dict] = []
    with driver.session(database=DATABASE, default_access_mode="WRITE") as session, (
        LOG_DIR / "agent_4_audit.jsonl"
    ).open("w", encoding="utf-8") as audit_fp:
        for index, stmt in enumerate(statements):
            started = utc_now()
            t0 = perf_counter()
            result = session.run(stmt, rows=rows)
            records = [row.data() for row in result]
            summary = result.consume()
            entry = {
                "statement_index": index,
                "started_utc": started,
                "elapsed_ms": round((perf_counter() - t0) * 1000, 1),
                "records": records,
                "counters": {
                    name: getattr(summary.counters, name)
                    for name in [
                        "nodes_created",
                        "relationships_created",
                        "properties_set",
                        "labels_added",
                    ]
                    if getattr(summary.counters, name)
                },
            }
            audit_entries.append(entry)
            audit_fp.write(json.dumps(entry, ensure_ascii=True) + "\n")
    return audit_entries


def run_gates(session) -> tuple[dict, bool]:
    gates = {
        "kennwert_total": {
            "cypher": "MATCH (kw:Kennwert) RETURN count(kw) AS c",
            "expect": ">= 12",
            "ok": lambda v: v["c"] >= 12,
        },
        "reuse_share_count": {
            "cypher": "MATCH (kw:Kennwert {category:'reuse_share'}) RETURN count(kw) AS c",
            "expect": ">= 4",
            "ok": lambda v: v["c"] >= 4,
        },
        "co2_saving_count": {
            "cypher": "MATCH (kw:Kennwert {category:'co2_saving'}) RETURN count(kw) AS c",
            "expect": ">= 5",
            "ok": lambda v: v["c"] >= 5,
        },
        "cost_count": {
            "cypher": "MATCH (kw:Kennwert {category:'cost'}) RETURN count(kw) AS c",
            "expect": ">= 5",
            "ok": lambda v: v["c"] >= 5,
        },
        "kennwert_orphan": {
            "cypher": "MATCH (kw:Kennwert) WHERE NOT exists{()-[:HAT_KENNWERT]->(kw)} RETURN count(kw) AS violations",
            "expect": "0",
            "ok": lambda v: v["violations"] == 0,
        },
        "reuse_share_count_mismatch": {
            "cypher": (
                "MATCH (p:Projekt) WHERE p.reuse_share_facts IS NOT NULL AND size(p.reuse_share_facts) > 0 "
                "OPTIONAL MATCH (p)-[:HAT_KENNWERT]->(kw:Kennwert {category:'reuse_share'}) "
                "WITH p, count(kw) AS kw_count, size(p.reuse_share_facts) AS expected "
                "WHERE kw_count <> expected RETURN count(p) AS violations"
            ),
            "expect": "0",
            "ok": lambda v: v["violations"] == 0,
        },
        "co2_count_mismatch": {
            "cypher": (
                "MATCH (p:Projekt) WHERE p.co2_facts IS NOT NULL AND size(p.co2_facts) > 0 "
                "OPTIONAL MATCH (p)-[:HAT_KENNWERT]->(kw:Kennwert {category:'co2_saving'}) "
                "WITH p, count(kw) AS kw_count, size(p.co2_facts) AS expected "
                "WHERE kw_count <> expected RETURN count(p) AS violations"
            ),
            "expect": "0",
            "ok": lambda v: v["violations"] == 0,
        },
        "cost_count_mismatch": {
            "cypher": (
                "MATCH (p:Projekt) WHERE p.cost_facts IS NOT NULL AND size(p.cost_facts) > 0 "
                "OPTIONAL MATCH (p)-[:HAT_KENNWERT]->(kw:Kennwert {category:'cost'}) "
                "WITH p, count(kw) AS kw_count, size(p.cost_facts) AS expected "
                "WHERE kw_count <> expected RETURN count(p) AS violations"
            ),
            "expect": "0",
            "ok": lambda v: v["violations"] == 0,
        },
        "hat_kennwert_origin_enum": {
            "cypher": (
                "MATCH ()-[r:HAT_KENNWERT]->() "
                "WHERE NOT r.evidence_origin IN "
                "['source_curated','topology_synthesized','registry_derived','inferred','external_unfolded'] "
                "RETURN count(r) AS violations"
            ),
            "expect": "0",
            "ok": lambda v: v["violations"] == 0,
        },
        "q3_tier1_reuse_projects": {
            "cypher": (
                "MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})-[:HAT_KENNWERT]->"
                "(:Kennwert {category:'reuse_share'}) RETURN count(DISTINCT p) AS c"
            ),
            "expect": ">= 3",
            "ok": lambda v: v["c"] >= 3,
        },
        "holbein_steel_34": {
            "cypher": (
                "MATCH (:Projekt {id:'p_holbein_gardens_london'})-[:HAT_KENNWERT]->(kw:Kennwert) "
                "WHERE toLower(kw.kennwert) CONTAINS 'steel' RETURN count(kw) AS hits, max(kw.wert) AS wert"
            ),
            "expect": "hits >= 1 and wert = 34",
            "ok": lambda v: v["hits"] >= 1 and abs(float(v["wert"]) - 34.0) < 0.0001,
        },
        "jeugdkliniek_range": {
            "cypher": (
                "MATCH (:Projekt {id:'p_jeugdkliniek_ithaka_emergis_kloetinge'})-[:HAT_KENNWERT]->(kw:Kennwert) "
                "WHERE kw.wert_text CONTAINS '30' AND kw.wert_text CONTAINS '40' "
                "RETURN count(kw) AS hits, min(kw.wert_min) AS wert_min, max(kw.wert_max) AS wert_max"
            ),
            "expect": "hits >= 1 and range 30..40",
            "ok": lambda v: v["hits"] >= 1
            and abs(float(v["wert_min"]) - 30.0) < 0.0001
            and abs(float(v["wert_max"]) - 40.0) < 0.0001,
        },
        "quality_tier_facts_untouched": {
            "cypher": "MATCH (p:Projekt) WHERE p.quality_tier_facts IS NOT NULL RETURN count(p) AS c",
            "expect": "> 0",
            "ok": lambda v: v["c"] > 0,
        },
    }
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


def extra_metrics(session) -> dict:
    return {
        "kennwert_by_category": collect_rows(
            session,
            "MATCH (kw:Kennwert) RETURN kw.category AS category, count(kw) AS c ORDER BY category",
        ),
        "tier1_kennwerte": collect_rows(
            session,
            "MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})-[:HAT_KENNWERT]->(kw:Kennwert) "
            "RETURN p.id AS projekt_id, kw.category AS category, kw.kennwert AS kennwert, "
            "kw.wert AS wert, kw.wert_text AS wert_text, kw.wert_min AS wert_min, "
            "kw.wert_max AS wert_max, kw.einheit AS einheit, kw.source_id AS source_id "
            "ORDER BY p.id, kw.category, kw.fact_index",
        ),
        "hat_kennwert_origin_distribution": collect_rows(
            session,
            "MATCH ()-[r:HAT_KENNWERT]->() RETURN r.evidence_origin AS origin, "
            "r.evidence_confidence AS confidence, count(r) AS c ORDER BY origin, confidence",
        ),
    }


def artifact_block() -> str:
    files = sorted(path for path in RUN_DIR.rglob("*") if path.is_file())
    return "\n".join(str(path.relative_to(REPO_ROOT)).replace("\\", "/") for path in files)


def write_report(verdict: str, pre: dict, post: dict | None, gates: dict | None, deps: dict, metrics: dict | None, errors: list[dict]) -> None:
    after = post or pre
    gate_rows = "| _not run_ | _dependency/preflight_ | _not run_ | BLOCKED |"
    if gates:
        gate_rows = "\n".join(
            f"| {name} | {value.get('_expect', '')} | {json.dumps({k: v for k, v in value.items() if not k.startswith('_')}, ensure_ascii=True)} | {'PASS' if value.get('_pass') else 'FAIL'} |"
            for name, value in gates.items()
        )
    report = f"""# Agent 4 - Phase R4 Report

- **Agent:** {AGENT}
- **Database:** {DATABASE}
- **Branch:** wip/kinan2 working tree
- **Completed (UTC):** {utc_now()}
- **Verdict:** {verdict}

## Executive summary

R4 lifts `reuse_share_facts`, `co2_facts`, and `cost_facts` from JSON-string arrays on `:Projekt` into first-class `:Kennwert` nodes. The JSON mirrors remain untouched; `quality_tier_facts` remains untouched by design. `:HAT_KENNWERT` edges carry the canonical R1 evidence fields.

## Before / after counts

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Total nodes | {pre['total_nodes']} | {after['total_nodes']} | {after['total_nodes'] - pre['total_nodes']} |
| Total relationships | {pre['total_rels']} | {after['total_rels']} | {after['total_rels'] - pre['total_rels']} |
| Kennwert total | {pre['kennwert_total']} | {after['kennwert_total']} | {after['kennwert_total'] - pre['kennwert_total']} |
| HAT_KENNWERT total | {pre['hat_kennwert_total']} | {after['hat_kennwert_total']} | {after['hat_kennwert_total'] - pre['hat_kennwert_total']} |
| reuse_share Kennwert | {pre['kennwert_reuse_share']} | {after['kennwert_reuse_share']} | {after['kennwert_reuse_share'] - pre['kennwert_reuse_share']} |
| co2_saving Kennwert | {pre['kennwert_co2_saving']} | {after['kennwert_co2_saving']} | {after['kennwert_co2_saving'] - pre['kennwert_co2_saving']} |
| cost Kennwert | {pre['kennwert_cost']} | {after['kennwert_cost']} | {after['kennwert_cost'] - pre['kennwert_cost']} |
| quality_tier_facts present | {pre['quality_tier_facts_present']} | {after['quality_tier_facts_present']} | {after['quality_tier_facts_present'] - pre['quality_tier_facts_present']} |

## Acceptance gates

| Gate | Expected | Live | Verdict |
|---|---|---|---|
{gate_rows}

## Issues raised

- Dependency status: `{json.dumps(deps, ensure_ascii=True)}`.
- Parse errors: `{len(errors)}`.
- D4 resolved YES: `:Kennwert.category` is written.
- D5 resolved NO: `quality_tier_facts` was not lifted.
- JSON-string source properties were not stripped; that remains orchestrator-gated after Stage 4.

## Metrics

```json
{json.dumps(metrics or {}, indent=2, ensure_ascii=True)}
```

## Parse Errors

```json
{json.dumps(errors, indent=2, ensure_ascii=True)}
```

## Artefacts

```
{artifact_block()}
```

## Handoff

Agent 5 R7.c can use this schema after `PHASE_R4_DONE.flag` is present. The runner is idempotent; rerunning R4 rewrites the same deterministic `kw_<projekt>_<category>_<i>` nodes and `:HAT_KENNWERT` edges.
"""
    (REPORT_DIR / "agent_4_report.md").write_text(report, encoding="utf-8")


def run_preflight() -> None:
    deps = dependency_status()
    driver = get_driver()
    try:
        with driver.session(database=DATABASE, default_access_mode="READ") as session:
            pre = probe(session)
            rows, errors = load_fact_rows(session)
        (LOG_DIR / "agent_4_probe_pre.json").write_text(json.dumps(pre, indent=2, ensure_ascii=True), encoding="utf-8")
        (LOG_DIR / "agent_4_normalized_rows.json").write_text(json.dumps(rows, indent=2, ensure_ascii=True), encoding="utf-8")
        (LOG_DIR / "agent_4_parse_errors.json").write_text(json.dumps(errors, indent=2, ensure_ascii=True), encoding="utf-8")
        metrics = {
            "normalized_rows": len(rows),
            "rows_by_category": {
                category: sum(1 for row in rows if row["category"] == category)
                for category in ["reuse_share", "co2_saving", "cost"]
            },
        }
        write_report("READY" if deps["can_run"] else "BLOCKED", pre, None, None, deps, metrics, errors)
        log(f"Preflight complete. can_run={deps['can_run']} normalized_rows={len(rows)} errors={len(errors)}")
    finally:
        driver.close()


def run_r4() -> None:
    deps = dependency_status()
    if not deps["can_run"]:
        run_preflight()
        raise SystemExit(f"R4 blocked; missing dependency flags: {', '.join(deps['missing'])}")
    driver = get_driver()
    try:
        with driver.session(database=DATABASE, default_access_mode="READ") as session:
            pre = probe(session)
            rows, errors = load_fact_rows(session)
        (LOG_DIR / "agent_4_probe_pre.json").write_text(json.dumps(pre, indent=2, ensure_ascii=True), encoding="utf-8")
        (LOG_DIR / "agent_4_normalized_rows.json").write_text(json.dumps(rows, indent=2, ensure_ascii=True), encoding="utf-8")
        (LOG_DIR / "agent_4_parse_errors.json").write_text(json.dumps(errors, indent=2, ensure_ascii=True), encoding="utf-8")
        if errors:
            write_report("FAIL", pre, None, None, deps, {"normalized_rows": len(rows)}, errors)
            raise SystemExit("R4 parse errors found; see logs/agent_4_parse_errors.json")
        audit_entries = execute_migration(driver, rows)
        with driver.session(database=DATABASE, default_access_mode="READ") as session:
            post = probe(session)
            gates, verified = run_gates(session)
            metrics = extra_metrics(session)
        (LOG_DIR / "agent_4_probe_post.json").write_text(json.dumps(post, indent=2, ensure_ascii=True), encoding="utf-8")
        (LOG_DIR / "agent_4_gates.json").write_text(json.dumps(gates, indent=2, ensure_ascii=True), encoding="utf-8")
        (LOG_DIR / "agent_4_metrics.json").write_text(json.dumps(metrics, indent=2, ensure_ascii=True), encoding="utf-8")
        (LOG_DIR / "agent_4_audit_summary.json").write_text(json.dumps(audit_entries, indent=2, ensure_ascii=True), encoding="utf-8")
        flag = {
            "phase": "R4",
            "agent": AGENT,
            "completed_at_utc": utc_now(),
            "verified": verified,
            "verification_query_results": gates,
            "extra": {
                "kennwert_by_category": post["kennwert_by_category"],
                "normalized_rows": len(rows),
                "parse_errors": len(errors),
            },
        }
        FLAG_PATH.write_text(json.dumps(flag, indent=2, ensure_ascii=True), encoding="utf-8")
        write_report("PASS" if verified else "FAIL", pre, post, gates, deps, metrics, errors)
        if not verified:
            raise SystemExit("R4 verification failed; see logs/agent_4_gates.json")
        log("R4 complete. PASS.")
    finally:
        driver.close()


def main() -> None:
    command = sys.argv[1].lower() if len(sys.argv) > 1 else "preflight"
    if command == "preflight":
        run_preflight()
    elif command == "r4":
        run_r4()
    else:
        raise SystemExit("Usage: python agent_4_runner.py [preflight|r4]")


if __name__ == "__main__":
    main()
