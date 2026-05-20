"""Phase 1.1 — Wiederverwendungskette demote-not-delete runner (Agent 2, Wave 1).

Applies migration `mig_1_1_demote_chains.cypher` against the `mit-bestand`
database, but in a guarded Python wrapper that:

  1. Re-counts the unwired chains and refuses to run if the number is not 98.
  2. Writes a complete pre-delete snapshot of every unwired chain (id + all
     properties + every incident edge with payload) to
     `deleted/phase1_1_chains.jsonl`.
  3. Demotes outgoing HAT_STATUS / HAT_WIEDERVERWENDUNGSART / HAT_HUERDE /
     HAT_LOGISTIK / HAT_PROZESSPHASE / HAT_METHODE payload onto every
     :Bauteilgruppe connected via :TEIL_VON_KETTE, stamping provenance.
  4. DETACH DELETEs the 98 unwired chains.
  5. Verifies that exactly 14 fully-wired :Wiederverwendungskette remain
     and that each one has BOTH outgoing :AUS_BAUWERK and outgoing
     :EINGEBAUT_IN.
  6. Writes `logs/PHASE_1_1_DONE.flag` and progress to
     `logs/mig_1_1_progress.log`.

Read-only Cypher and write Cypher are isolated in dedicated transactions
so a failure in the write step cannot corrupt the snapshot file on disk.

Connection settings: re-uses `_scripts/neo4j_env.resolve_connection()`. The
NEO4J_DATABASE for this run is forced to `mit-bestand` even if the .cursor/
mcp.json points elsewhere, because the task spec requires it.
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = REPO_ROOT / "_neo4j" / "intake" / "runs" / "2026-05-20_radical_quality_reset"
LOG_DIR = RUN_ROOT / "logs"
DELETED_DIR = RUN_ROOT / "deleted"
MIGRATIONS_DIR = RUN_ROOT / "migrations"
REPORTS_DIR = RUN_ROOT / "reports"

DELETED_JSONL = DELETED_DIR / "phase1_1_chains.jsonl"
PROGRESS_LOG = LOG_DIR / "mig_1_1_progress.log"
DONE_FLAG = LOG_DIR / "PHASE_1_1_DONE.flag"
COUNTS_JSON = LOG_DIR / "mig_1_1_counts.json"

TARGET_DATABASE = "mit-bestand"
EXPECTED_TOTAL = 112
EXPECTED_UNWIRED = 98
EXPECTED_KEEP = 14

DEMOTABLE_TYPES = (
    "HAT_STATUS",
    "HAT_WIEDERVERWENDUNGSART",
    "HAT_HUERDE",
    "HAT_LOGISTIK",
    "HAT_PROZESSPHASE",
    "HAT_METHODE",
)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _log(line: str) -> None:
    stamp = _now_iso()
    msg = f"[{stamp}] {line}"
    print(msg, flush=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with PROGRESS_LOG.open("a", encoding="utf-8") as fp:
        fp.write(msg + "\n")


def _to_jsonable(value: Any) -> Any:
    """Convert Neo4j temporal / spatial primitives to JSON-safe Python."""
    from neo4j.spatial import Point  # type: ignore
    from neo4j.time import Date, DateTime, Duration, Time  # type: ignore

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


def _resolve_connection() -> tuple[str, str, str]:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection  # type: ignore

    uri, user, password, database = resolve_connection()
    if not uri or not user or not password:
        raise RuntimeError(
            "Neo4j connection settings missing (NEO4J_URI/USERNAME/PASSWORD)."
        )
    if database != TARGET_DATABASE:
        _log(
            f"WARN: resolved database='{database}', forcing '{TARGET_DATABASE}' "
            "for Phase 1.1 (task spec)."
        )
    return uri, user, password


def snapshot_unwired_chains(session) -> list[dict]:
    """Pull full payload (props + every incident edge) for the 98 unwired chains."""
    cypher = """
        MATCH (k:Wiederverwendungskette)
        WHERE NOT (exists{(k)-[:AUS_BAUWERK]->()} AND exists{(k)-[:EINGEBAUT_IN]->()})
        OPTIONAL MATCH (k)-[r_out]->(t_out)
        WITH k,
             collect(DISTINCT {
                 direction: 'out',
                 type: type(r_out),
                 rel_internal_id: id(r_out),
                 target_internal_id: id(t_out),
                 target_id: t_out.id,
                 target_labels: labels(t_out),
                 properties: properties(r_out)
             }) AS out_edges
        OPTIONAL MATCH (s_in)-[r_in]->(k)
        WITH k, out_edges,
             collect(DISTINCT {
                 direction: 'in',
                 type: type(r_in),
                 rel_internal_id: id(r_in),
                 source_internal_id: id(s_in),
                 source_id: s_in.id,
                 source_labels: labels(s_in),
                 properties: properties(r_in)
             }) AS in_edges
        RETURN id(k) AS internal_id,
               k.id AS id,
               labels(k) AS labels,
               properties(k) AS properties,
               [e IN out_edges WHERE e.type IS NOT NULL] AS out_edges,
               [e IN in_edges  WHERE e.type IS NOT NULL] AS in_edges
        ORDER BY k.id
    """
    rows = list(session.run(cypher))
    snapshot = []
    for r in rows:
        snapshot.append(
            {
                "neo4j_internal_id": r["internal_id"],
                "id": r["id"],
                "labels": list(r["labels"]),
                "properties": _to_jsonable(dict(r["properties"])),
                "out_edges": [
                    _to_jsonable(dict(e)) for e in r["out_edges"]
                ],
                "in_edges": [
                    _to_jsonable(dict(e)) for e in r["in_edges"]
                ],
            }
        )
    return snapshot


def count_chains(session) -> dict[str, int]:
    cypher = """
        MATCH (k:Wiederverwendungskette)
        WITH collect(k) AS all_chains
        UNWIND all_chains AS k
        WITH all_chains,
             sum(CASE WHEN exists{(k)-[:AUS_BAUWERK]->()} AND exists{(k)-[:EINGEBAUT_IN]->()}
                      THEN 1 ELSE 0 END) AS wired
        RETURN size(all_chains) AS total, wired
    """
    row = session.run(cypher).single()
    if row is None:
        return {"total": 0, "wired": 0, "unwired": 0}
    total = int(row["total"])
    wired = int(row["wired"])
    return {"total": total, "wired": wired, "unwired": total - wired}


def demote_payload(session) -> dict[str, int]:
    """Copy outgoing HAT_* edges from unwired chains onto connected BGs."""
    cypher = """
        MATCH (bg:Bauteilgruppe)-[:TEIL_VON_KETTE]->(k:Wiederverwendungskette)
        WHERE NOT (exists{(k)-[:AUS_BAUWERK]->()} AND exists{(k)-[:EINGEBAUT_IN]->()})
        MATCH (k)-[r]->(target)
        WHERE type(r) IN $types
        WITH bg, k, r, target,
             {
               migration_origin:     'mig_1_1_demote_chains',
               evidence_basis:       'demoted_from_kette',
               evidence_origin:      'derived',
               evidence_source_id:   k.id,
               evidence_confidence:  coalesce(r.evidence_confidence, 'unklar'),
               demoted_at:           datetime()
             } AS shape
        CALL apoc.merge.relationship(
                bg,
                type(r),
                {evidence_source_id: k.id},
                shape,
                target,
                shape
        ) YIELD rel
        RETURN type(rel) AS rel_type, count(rel) AS n
    """
    rows = list(session.run(cypher, types=list(DEMOTABLE_TYPES)))
    out = {}
    total = 0
    for r in rows:
        out[r["rel_type"]] = int(r["n"])
        total += int(r["n"])
    out["__total__"] = total
    return out


def delete_unwired_chains(session) -> int:
    cypher = """
        MATCH (k:Wiederverwendungskette)
        WHERE NOT (exists{(k)-[:AUS_BAUWERK]->()} AND exists{(k)-[:EINGEBAUT_IN]->()})
        WITH collect(k) AS to_delete
        UNWIND to_delete AS k
        DETACH DELETE k
        RETURN size(to_delete) AS n
    """
    row = session.run(cypher).single()
    return int(row["n"]) if row else 0


def verify_acceptance(session) -> dict[str, Any]:
    cypher = """
        MATCH (k:Wiederverwendungskette)
        WITH collect(k) AS chains
        UNWIND chains AS k
        WITH chains, k,
             exists{(k)-[:AUS_BAUWERK]->()}  AS has_ab,
             exists{(k)-[:EINGEBAUT_IN]->()} AS has_ei
        WITH chains,
             collect({
                id: k.id,
                has_ab: has_ab,
                has_ei: has_ei,
                wired: (has_ab AND has_ei)
             }) AS details
        RETURN size(chains) AS total,
               size([d IN details WHERE d.wired]) AS wired,
               [d IN details WHERE NOT d.wired] AS unwired_remaining
    """
    row = session.run(cypher).single()
    if row is None:
        return {"total": 0, "wired": 0, "unwired_remaining": []}
    return {
        "total": int(row["total"]),
        "wired": int(row["wired"]),
        "unwired_remaining": [dict(d) for d in row["unwired_remaining"]],
    }


def write_jsonl(snapshot: list[dict], path: Path) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fp:
        for rec in snapshot:
            fp.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return len(snapshot)


def main() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    DELETED_DIR.mkdir(parents=True, exist_ok=True)
    MIGRATIONS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    from neo4j import GraphDatabase  # type: ignore

    uri, user, password = _resolve_connection()
    _log(f"connecting to {uri} db='{TARGET_DATABASE}' as user='{user}'")

    started_iso = _now_iso()
    t0 = time.perf_counter()

    driver = GraphDatabase.driver(uri, auth=(user, password))
    counts: dict[str, Any] = {
        "started_at": started_iso,
        "target_database": TARGET_DATABASE,
    }
    try:
        driver.verify_connectivity()

        with driver.session(database=TARGET_DATABASE) as session:
            pre = count_chains(session)
            _log(f"PRE-COUNT: total={pre['total']} wired={pre['wired']} unwired={pre['unwired']}")
            counts["chains_before"] = pre["total"]
            counts["wired_before"] = pre["wired"]
            counts["unwired_before"] = pre["unwired"]

            if pre["total"] != EXPECTED_TOTAL:
                _log(f"ABORT: total {pre['total']} != expected {EXPECTED_TOTAL}")
                return 2
            if pre["unwired"] != EXPECTED_UNWIRED:
                _log(f"ABORT: unwired {pre['unwired']} != expected {EXPECTED_UNWIRED}")
                return 2

            _log("snapshotting 98 unwired chains (props + all edges)...")
            snap = snapshot_unwired_chains(session)
            if len(snap) != EXPECTED_UNWIRED:
                _log(f"ABORT: snapshot rows {len(snap)} != expected {EXPECTED_UNWIRED}")
                return 2
            n_written = write_jsonl(snap, DELETED_JSONL)
            _log(f"wrote {n_written} chains to {DELETED_JSONL}")
            counts["chains_snapshotted"] = n_written
            counts["edges_in_snapshot"] = sum(
                len(s["out_edges"]) + len(s["in_edges"]) for s in snap
            )

        with driver.session(database=TARGET_DATABASE) as session:
            _log("demoting outgoing HAT_* payload onto connected Bauteilgruppen...")
            demote_result = session.execute_write(
                lambda tx: list(
                    tx.run(
                        """
                        MATCH (bg:Bauteilgruppe)-[:TEIL_VON_KETTE]->(k:Wiederverwendungskette)
                        WHERE NOT (exists{(k)-[:AUS_BAUWERK]->()} AND exists{(k)-[:EINGEBAUT_IN]->()})
                        MATCH (k)-[r]->(target)
                        WHERE type(r) IN $types
                        WITH bg, k, r, target,
                             {
                               migration_origin:     'mig_1_1_demote_chains',
                               evidence_basis:       'demoted_from_kette',
                               evidence_origin:      'derived',
                               evidence_source_id:   k.id,
                               evidence_confidence:  coalesce(r.evidence_confidence, 'unklar'),
                               demoted_at:           datetime()
                             } AS shape
                        CALL apoc.merge.relationship(
                                bg,
                                type(r),
                                {evidence_source_id: k.id},
                                shape,
                                target,
                                shape
                        ) YIELD rel
                        RETURN type(rel) AS rel_type, count(rel) AS n
                        """,
                        types=list(DEMOTABLE_TYPES),
                    )
                )
            )
            demote_counts = {row["rel_type"]: int(row["n"]) for row in demote_result}
            edges_demoted = sum(demote_counts.values())
            _log(f"edges_demoted_total={edges_demoted} breakdown={demote_counts}")
            counts["edges_demoted_by_type"] = demote_counts
            counts["edges_demoted"] = edges_demoted

        with driver.session(database=TARGET_DATABASE) as session:
            _log("DETACH DELETE 98 unwired chains...")
            n_deleted = session.execute_write(
                lambda tx: tx.run(
                    """
                    MATCH (k:Wiederverwendungskette)
                    WHERE NOT (exists{(k)-[:AUS_BAUWERK]->()} AND exists{(k)-[:EINGEBAUT_IN]->()})
                    WITH collect(k) AS to_delete
                    UNWIND to_delete AS k
                    DETACH DELETE k
                    RETURN size(to_delete) AS n
                    """
                ).single()["n"]
            )
            _log(f"chains_deleted={n_deleted}")
            counts["chains_deleted"] = n_deleted

        with driver.session(database=TARGET_DATABASE) as session:
            acc = verify_acceptance(session)
            _log(
                f"POST-COUNT: total={acc['total']} wired={acc['wired']} "
                f"unwired_remaining={len(acc['unwired_remaining'])}"
            )
            counts["chains_after"] = acc["total"]
            counts["wired_after"] = acc["wired"]
            counts["unwired_remaining"] = acc["unwired_remaining"]

    finally:
        driver.close()

    ok = (
        counts.get("chains_after") == EXPECTED_KEEP
        and counts.get("wired_after") == EXPECTED_KEEP
        and counts.get("chains_deleted") == EXPECTED_UNWIRED
        and len(counts.get("unwired_remaining", [])) == 0
    )

    finished_iso = _now_iso()
    elapsed = time.perf_counter() - t0
    counts["finished_at"] = finished_iso
    counts["elapsed_seconds"] = round(elapsed, 2)
    counts["ok"] = ok

    COUNTS_JSON.write_text(
        json.dumps(counts, ensure_ascii=False, indent=2, sort_keys=True, default=str),
        encoding="utf-8",
    )

    flag_text = (
        f"phase: 1.1\n"
        f"agent: 2\n"
        f"target_database: {TARGET_DATABASE}\n"
        f"started_at: {started_iso}\n"
        f"finished_at: {finished_iso}\n"
        f"elapsed_seconds: {elapsed:.2f}\n"
        f"chains_before: {counts.get('chains_before')}\n"
        f"chains_after: {counts.get('chains_after')}\n"
        f"edges_demoted: {counts.get('edges_demoted')}\n"
        f"chains_deleted: {counts.get('chains_deleted')}\n"
        f"unwired_remaining: {len(counts.get('unwired_remaining', []))}\n"
        f"ok: {'true' if ok else 'false'}\n"
    )
    DONE_FLAG.write_text(flag_text, encoding="utf-8")
    _log(f"wrote {DONE_FLAG} ok={ok}")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
