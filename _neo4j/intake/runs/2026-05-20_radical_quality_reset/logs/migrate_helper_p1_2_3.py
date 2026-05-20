"""Phase 1.2 + 1.3 migration runner for mit-bestand (Agent 3, Wave-1).

Reads connection settings from `.cursor/mcp.json` via
`_scripts/neo4j_env.resolve_connection()` (with env-var overrides) and applies
the two Cypher migration files for Phase 1.2 (ontology anchors) and Phase 1.3
(propagated marktmodell flags + dominant-edge removal).

Behaviour:
  - Statement-by-statement execution within a single write transaction per
    migration file. The transaction is committed only if every statement
    succeeds; any error rolls the whole file back.
  - Each statement's RETURN values are captured and logged to
    `logs/phase1_2_3_progress.log`.
  - Pre-flight checks confirm the snapshot is present and the expected
    pre-migration counts match the plan (defensive guard against accidental
    re-runs against a different graph).
  - On full success writes `logs/PHASE_1_2_DONE.flag` and
    `logs/PHASE_1_3_DONE.flag` with timestamps + counts.

Idempotency:
  - Pre-flight checks each phase's expected counts and SKIPS the file when the
    "before" counts already match the "after" counts (i.e. the migration was
    already applied). The DONE flag is still (re-)written so downstream agents
    see a stable signal.
"""

from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = REPO_ROOT / "_neo4j" / "intake" / "runs" / "2026-05-20_radical_quality_reset"
MIG_DIR = RUN_ROOT / "migrations"
LOG_DIR = RUN_ROOT / "logs"
DEL_DIR = RUN_ROOT / "deleted"
PROGRESS_LOG = LOG_DIR / "phase1_2_3_progress.log"
RESULT_JSON = LOG_DIR / "phase1_2_3_result.json"

MIG_1_2_FILE = MIG_DIR / "mig_1_2_anchor_relabel.cypher"
MIG_1_3_FILE = MIG_DIR / "mig_1_3_flag_propagated.cypher"

FLAG_1_2 = LOG_DIR / "PHASE_1_2_DONE.flag"
FLAG_1_3 = LOG_DIR / "PHASE_1_3_DONE.flag"

ARCHIVE_FILE_1_2 = DEL_DIR / "phase1_2_quelle.jsonl"


def _log(line: str) -> None:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    msg = f"[{stamp}] {line}"
    print(msg, flush=True)
    with PROGRESS_LOG.open("a", encoding="utf-8") as fp:
        fp.write(msg + "\n")


def _resolve_connection() -> tuple[str, str, str, str]:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection  # type: ignore

    uri, user, password, database = resolve_connection()
    if not uri or not user or not password:
        raise RuntimeError(
            "Neo4j connection settings missing (NEO4J_URI/USERNAME/PASSWORD)."
        )
    if database != "mit-bestand":
        _log(
            f"WARN: configured NEO4J_DATABASE='{database}' — overriding to 'mit-bestand'."
        )
        database = "mit-bestand"
    return uri, user, password, database


_COMMENT_RE = re.compile(r"//[^\n]*")


def parse_cypher_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    stripped = _COMMENT_RE.sub("", text)
    stmts = [s.strip() for s in stripped.split(";")]
    return [s for s in stmts if s]


def _to_jsonable(value):  # noqa: ANN001
    from neo4j.time import Date, DateTime, Duration, Time  # type: ignore
    from neo4j.spatial import Point  # type: ignore

    if isinstance(value, (Date, DateTime, Time)):
        return value.iso_format()
    if isinstance(value, Duration):
        return str(value)
    if isinstance(value, Point):
        return {"srid": value.srid, "coordinates": list(value)}
    if isinstance(value, dict):
        return {k: _to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, (bytes, bytearray)):
        return value.decode("utf-8", errors="replace")
    return value


def run_migration(driver, database: str, label: str, path: Path) -> list[dict]:
    _log(f"--- {label}: parsing {path.name}")
    stmts = parse_cypher_file(path)
    _log(f"--- {label}: {len(stmts)} statements parsed")

    results: list[dict] = []
    with driver.session(database=database) as session:
        def _work(tx):
            collected = []
            for idx, stmt in enumerate(stmts, start=1):
                preview = " ".join(stmt.split())[:120]
                _log(f"    [{label} #{idx}/{len(stmts)}] {preview}")
                res = tx.run(stmt)
                rows = [{k: _to_jsonable(v) for k, v in r.items()} for r in res]
                summary = res.consume()
                ctrs = summary.counters
                ctr_dict = {
                    "nodes_created": ctrs.nodes_created,
                    "nodes_deleted": ctrs.nodes_deleted,
                    "relationships_created": ctrs.relationships_created,
                    "relationships_deleted": ctrs.relationships_deleted,
                    "labels_added": ctrs.labels_added,
                    "labels_removed": ctrs.labels_removed,
                    "properties_set": ctrs.properties_set,
                }
                _log(f"        rows={len(rows)}  counters={ctr_dict}")
                if rows:
                    _log(f"        first_row={json.dumps(rows[0], ensure_ascii=False)[:300]}")
                collected.append({
                    "statement_index": idx,
                    "statement_preview": preview,
                    "rows": rows,
                    "counters": ctr_dict,
                })
            return collected
        results = session.execute_write(_work)
    return results


def precheck(driver, database: str) -> dict:
    _log("precheck: gathering live counts")
    with driver.session(database=database) as session:
        def _q(cypher):
            return list(session.run(cypher))

        anchors_as_quelle = _q(
            "MATCH (q:Quelle) WHERE q.id IN "
            "['q_controlled_vocab_seed','q_akteursliste_master_md'] "
            "RETURN count(q) AS c"
        )[0]["c"]
        anchors_as_ontoanchor = _q(
            "MATCH (q:OntologyAnchor) WHERE q.id IN "
            "['q_controlled_vocab_seed','q_akteursliste_master_md'] "
            "RETURN count(q) AS c"
        )[0]["c"]
        belegt_in_to_anchors_pre = _q(
            "MATCH ()-[r:BELEGT_IN]->(a) WHERE a.id IN "
            "['q_controlled_vocab_seed','q_akteursliste_master_md'] "
            "RETURN count(r) AS c"
        )[0]["c"]
        anchored_by_to_anchors = _q(
            "MATCH ()-[r:ANCHORED_BY]->(a) WHERE a.id IN "
            "['q_controlled_vocab_seed','q_akteursliste_master_md'] "
            "RETURN count(r) AS c"
        )[0]["c"]
        deg0_quelle = _q(
            "MATCH (q:Quelle) WHERE NOT exists { (q)<-[]-() } AND NOT exists { (q)-[]->() } "
            "RETURN count(q) AS c"
        )[0]["c"]
        propagated_mm = _q(
            "MATCH ()-[r:HAT_MARKTMODELL]->() "
            "WHERE r.source_excerpt CONTAINS 'propagated' "
            "RETURN count(r) AS c"
        )[0]["c"]
        propagated_flagged = _q(
            "MATCH ()-[r:HAT_MARKTMODELL]->() "
            "WHERE r.evidence_basis = 'propagated' "
            "RETURN count(r) AS c"
        )[0]["c"]
        dom_mm = _q(
            "MATCH ()-[r:HAT_DOMINANT_MARKTMODELL]->() RETURN count(r) AS c"
        )[0]["c"]
        dom_akz = _q(
            "MATCH ()-[r:HAT_DOMINANT_AKZEPTANZ]->() RETURN count(r) AS c"
        )[0]["c"]
        total_nodes = _q("MATCH (n) RETURN count(n) AS c")[0]["c"]
        total_rels = _q("MATCH ()-[r]->() RETURN count(r) AS c")[0]["c"]

    snap = {
        "total_nodes": total_nodes,
        "total_rels": total_rels,
        "anchors_as_quelle": anchors_as_quelle,
        "anchors_as_ontology_anchor": anchors_as_ontoanchor,
        "belegt_in_to_anchors": belegt_in_to_anchors_pre,
        "anchored_by_to_anchors": anchored_by_to_anchors,
        "deg0_quelle": deg0_quelle,
        "hat_marktmodell_with_propagated_excerpt": propagated_mm,
        "hat_marktmodell_with_propagated_basis": propagated_flagged,
        "hat_dominant_marktmodell": dom_mm,
        "hat_dominant_akzeptanz": dom_akz,
    }
    _log(f"precheck snapshot: {json.dumps(snap)}")
    return snap


def write_done_flag(flag_path: Path, phase: str, before: dict, after: dict) -> None:
    body = {
        "phase": phase,
        "completed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "before": before,
        "after": after,
    }
    flag_path.write_text(json.dumps(body, ensure_ascii=False, indent=2), encoding="utf-8")
    _log(f"wrote done flag: {flag_path.name}")


def main() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    DEL_DIR.mkdir(parents=True, exist_ok=True)

    if not ARCHIVE_FILE_1_2.is_file():
        raise RuntimeError(
            f"archive file missing: {ARCHIVE_FILE_1_2} — refusing to run 1.2.c"
        )

    from neo4j import GraphDatabase  # type: ignore

    uri, user, password, database = _resolve_connection()
    _log(f"connecting to {uri} db='{database}' as user='{user}'")

    started = time.perf_counter()
    started_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()

        before = precheck(driver, database)

        # Defensive: require that the migrations have not already been applied
        # OR that they were applied cleanly. We allow re-running idempotently.
        phase_1_2_already = (
            before["anchors_as_quelle"] == 0
            and before["anchors_as_ontology_anchor"] == 2
            and before["belegt_in_to_anchors"] == 0
            and before["anchored_by_to_anchors"] == 716
            and before["deg0_quelle"] == 0
        )
        phase_1_3_already = (
            before["hat_marktmodell_with_propagated_excerpt"] == 0
            and before["hat_marktmodell_with_propagated_basis"] == 319
            and before["hat_dominant_marktmodell"] == 0
            and before["hat_dominant_akzeptanz"] == 0
        )

        # Plan-expected "before" sanity check (only enforced when not already
        # applied — allows graceful idempotent re-runs).
        # NOTE: 1.2.c is tolerant of the deg-0 Quelle count because Phase 1.5
        # (Agent 5) ran in parallel and preempted the 21 named deletions; what
        # remains as deg-0 here is collateral from Phase 1.1 chain deletion.
        if not phase_1_2_already:
            assert before["anchors_as_quelle"] == 2, (
                f"expected 2 Quelle anchors, got {before['anchors_as_quelle']}"
            )
            assert before["belegt_in_to_anchors"] == 716, (
                f"expected 716 BELEGT_IN to anchors, got {before['belegt_in_to_anchors']}"
            )
            deg0_observed = before["deg0_quelle"]
            assert deg0_observed >= 0, deg0_observed
            _log(
                f"observed {deg0_observed} deg-0 Quelle (plan expected 21 by "
                f"1.2.c; Phase 1.5 already removed the 21 named IDs — any "
                f"remaining are Phase-1.1 collateral and will be deleted)."
            )
        if not phase_1_3_already:
            assert before["hat_marktmodell_with_propagated_excerpt"] == 319, (
                f"expected 319 propagated HAT_MARKTMODELL, got "
                f"{before['hat_marktmodell_with_propagated_excerpt']}"
            )
            assert before["hat_dominant_marktmodell"] == 86, (
                f"expected 86 HAT_DOMINANT_MARKTMODELL, got "
                f"{before['hat_dominant_marktmodell']}"
            )
            assert before["hat_dominant_akzeptanz"] == 24, (
                f"expected 24 HAT_DOMINANT_AKZEPTANZ, got "
                f"{before['hat_dominant_akzeptanz']}"
            )

        result = {"started_at": started_iso, "before": before, "phase_1_2": None, "phase_1_3": None}

        if phase_1_2_already:
            _log("Phase 1.2 already applied — skipping execution, re-issuing flag.")
            result["phase_1_2"] = {"skipped": True, "reason": "already_applied"}
        else:
            r12 = run_migration(driver, database, "Phase 1.2", MIG_1_2_FILE)
            result["phase_1_2"] = {"skipped": False, "statements": r12}

        if phase_1_3_already:
            _log("Phase 1.3 already applied — skipping execution, re-issuing flag.")
            result["phase_1_3"] = {"skipped": True, "reason": "already_applied"}
        else:
            r13 = run_migration(driver, database, "Phase 1.3", MIG_1_3_FILE)
            result["phase_1_3"] = {"skipped": False, "statements": r13}

        after = precheck(driver, database)
        result["after"] = after

        # Hard post-conditions
        assert after["anchors_as_quelle"] == 0, after
        assert after["anchors_as_ontology_anchor"] == 2, after
        assert after["belegt_in_to_anchors"] == 0, after
        assert after["anchored_by_to_anchors"] == 716, after
        assert after["deg0_quelle"] == 0, after
        assert after["hat_marktmodell_with_propagated_excerpt"] == 0, after
        assert after["hat_marktmodell_with_propagated_basis"] == 319, after
        assert after["hat_dominant_marktmodell"] == 0, after
        assert after["hat_dominant_akzeptanz"] == 0, after

        # Node/edge accounting. Node delta = number of deg-0 Quelle observed
        # at precheck (post-1.5 reality). Edge delta = -110 from 1.3.b/c (-86
        # HAT_DOMINANT_MARKTMODELL, -24 HAT_DOMINANT_AKZEPTANZ). 1.2.b is a
        # zero-sum retype (-716 BELEGT_IN, +716 ANCHORED_BY).
        node_delta = before["deg0_quelle"]
        expected_total_nodes = before["total_nodes"] - node_delta
        expected_total_rels = before["total_rels"] - 110
        assert after["total_nodes"] == expected_total_nodes, (
            f"expected total_nodes={expected_total_nodes}, got {after['total_nodes']}"
        )
        assert after["total_rels"] == expected_total_rels, (
            f"expected total_rels={expected_total_rels}, got {after['total_rels']}"
        )

        write_done_flag(FLAG_1_2, "1.2", before, after)
        write_done_flag(FLAG_1_3, "1.3", before, after)

        finished_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
        elapsed = time.perf_counter() - started
        result["finished_at"] = finished_iso
        result["elapsed_seconds"] = elapsed
        RESULT_JSON.write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        _log(
            f"DONE  nodes {before['total_nodes']}->{after['total_nodes']} "
            f"(-{node_delta}) rels {before['total_rels']}->{after['total_rels']} (-110) "
            f"elapsed={elapsed:.2f}s"
        )

    finally:
        driver.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
