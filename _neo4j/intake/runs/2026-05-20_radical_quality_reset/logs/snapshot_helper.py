"""Pre-migration snapshot exporter for mit-bestand (Agent 1, Wave-0).

Reads connection settings from `.cursor/mcp.json` via
`_scripts/neo4j_env.resolve_connection()` (with env-var overrides) and writes:

  snapshot/nodes.jsonl
  snapshot/relationships.jsonl
  snapshot/stats.json
  snapshot/label_counts.json
  snapshot/rel_type_counts.json

Pages through the graph in chunks of 1000 (per task spec). Read-only.
Counts are verified against `apoc.meta.stats()`; any mismatch is logged to
`logs/snapshot_warnings.txt` but does NOT abort.

Also emits `SNAPSHOT_DONE.flag` in the run root with summary metadata.
"""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = REPO_ROOT / "_neo4j" / "intake" / "runs" / "2026-05-20_radical_quality_reset"
SNAP_DIR = RUN_ROOT / "snapshot"
LOG_DIR = RUN_ROOT / "logs"
RUN_FLAG = RUN_ROOT / "SNAPSHOT_DONE.flag"
WARN_FILE = LOG_DIR / "snapshot_warnings.txt"
PROGRESS_LOG = LOG_DIR / "snapshot_progress.log"

PAGE_SIZE = 1000


def _log(line: str) -> None:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    msg = f"[{stamp}] {line}"
    print(msg, flush=True)
    with PROGRESS_LOG.open("a", encoding="utf-8") as fp:
        fp.write(msg + "\n")


def _warn(line: str) -> None:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    msg = f"[{stamp}] WARN: {line}"
    print(msg, flush=True)
    with WARN_FILE.open("a", encoding="utf-8") as fp:
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
        _warn(
            f"Configured NEO4J_DATABASE='{database}' but task expects 'mit-bestand'."
        )
    return uri, user, password, database


def _to_jsonable(value):  # noqa: ANN001
    """Convert Neo4j value graph primitives to JSON-serialisable Python."""
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


def export_nodes(driver, database: str, expected: int) -> int:
    out_path = SNAP_DIR / "nodes.jsonl"
    count = 0
    skip = 0
    cypher = (
        "MATCH (n) "
        "RETURN id(n) AS internal_id, labels(n) AS labels, properties(n) AS properties "
        "ORDER BY id(n) SKIP $skip LIMIT $limit"
    )
    with out_path.open("w", encoding="utf-8", newline="\n") as fp:
        while True:
            with driver.session(database=database) as session:
                result = session.run(cypher, skip=skip, limit=PAGE_SIZE)
                rows = list(result)
            if not rows:
                break
            for r in rows:
                props = _to_jsonable(dict(r["properties"]))
                rec = {
                    "id": props.get("id"),
                    "neo4j_internal_id": r["internal_id"],
                    "labels": list(r["labels"]),
                    "properties": props,
                }
                fp.write(json.dumps(rec, ensure_ascii=False) + "\n")
                count += 1
            _log(f"nodes paged: skip={skip}, fetched={len(rows)}, total={count}/{expected}")
            if len(rows) < PAGE_SIZE:
                break
            skip += PAGE_SIZE
    return count


def export_relationships(driver, database: str, expected: int) -> int:
    out_path = SNAP_DIR / "relationships.jsonl"
    count = 0
    skip = 0
    cypher = (
        "MATCH (a)-[r]->(b) "
        "RETURN id(r) AS internal_id, type(r) AS type, "
        "id(a) AS start_internal, id(b) AS end_internal, "
        "a.id AS start_id, b.id AS end_id, "
        "properties(r) AS properties "
        "ORDER BY id(r) SKIP $skip LIMIT $limit"
    )
    with out_path.open("w", encoding="utf-8", newline="\n") as fp:
        while True:
            with driver.session(database=database) as session:
                result = session.run(cypher, skip=skip, limit=PAGE_SIZE)
                rows = list(result)
            if not rows:
                break
            for r in rows:
                rec = {
                    "internal_id": r["internal_id"],
                    "type": r["type"],
                    "start_node_internal_id": r["start_internal"],
                    "end_node_internal_id": r["end_internal"],
                    "start_node_id_property": r["start_id"],
                    "end_node_id_property": r["end_id"],
                    "properties": _to_jsonable(dict(r["properties"])),
                }
                fp.write(json.dumps(rec, ensure_ascii=False) + "\n")
                count += 1
            _log(
                f"rels  paged: skip={skip}, fetched={len(rows)}, total={count}/{expected}"
            )
            if len(rows) < PAGE_SIZE:
                break
            skip += PAGE_SIZE
    return count


def fetch_stats(driver, database: str) -> dict:
    cypher = (
        "CALL apoc.meta.stats() YIELD labels, relTypes, nodeCount, relCount, "
        "propertyKeyCount "
        "RETURN labels, relTypes, nodeCount, relCount, propertyKeyCount"
    )
    with driver.session(database=database) as session:
        row = session.run(cypher).single()
    if not row:
        raise RuntimeError("apoc.meta.stats() returned no rows.")
    return {
        "labels": _to_jsonable(dict(row["labels"])),
        "relTypes": _to_jsonable(dict(row["relTypes"])),
        "nodeCount": row["nodeCount"],
        "relCount": row["relCount"],
        "propertyKeyCount": row["propertyKeyCount"],
    }


def fetch_label_counts(driver, database: str) -> list[dict]:
    cypher = "MATCH (n) UNWIND labels(n) AS l RETURN l, count(*) AS c ORDER BY c DESC"
    with driver.session(database=database) as session:
        rows = list(session.run(cypher))
    return [{"label": r["l"], "count": r["c"]} for r in rows]


def fetch_rel_type_counts(driver, database: str) -> list[dict]:
    cypher = (
        "MATCH ()-[r]->() RETURN type(r) AS t, count(*) AS c ORDER BY c DESC"
    )
    with driver.session(database=database) as session:
        rows = list(session.run(cypher))
    return [{"type": r["t"], "count": r["c"]} for r in rows]


def file_byte_size(path: Path) -> int:
    return path.stat().st_size if path.is_file() else 0


def file_line_count(path: Path) -> int:
    if not path.is_file():
        return 0
    n = 0
    with path.open("rb") as fp:
        for _ in fp:
            n += 1
    return n


def main() -> int:
    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    from neo4j import GraphDatabase  # type: ignore

    uri, user, password, database = _resolve_connection()
    _log(f"connecting to {uri} db='{database}' as user='{user}'")

    started = time.perf_counter()
    started_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()

        _log("fetching stats / label_counts / rel_type_counts")
        stats = fetch_stats(driver, database)
        label_counts = fetch_label_counts(driver, database)
        rel_type_counts = fetch_rel_type_counts(driver, database)

        (SNAP_DIR / "stats.json").write_text(
            json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        (SNAP_DIR / "label_counts.json").write_text(
            json.dumps(label_counts, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        (SNAP_DIR / "rel_type_counts.json").write_text(
            json.dumps(rel_type_counts, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        expected_nodes = int(stats["nodeCount"])
        expected_rels = int(stats["relCount"])
        label_count = len(stats["labels"])
        rel_type_count = sum(
            1 for k in stats["relTypes"] if k.startswith("()-[:") and k.endswith("]->()")
        )

        _log(
            f"expected counts from apoc.meta.stats: nodes={expected_nodes}, "
            f"rels={expected_rels}, labels={label_count}, rel_types={rel_type_count}"
        )

        _log("exporting nodes...")
        n_written = export_nodes(driver, database, expected_nodes)
        _log(f"nodes export done: wrote {n_written} lines")

        _log("exporting relationships...")
        r_written = export_relationships(driver, database, expected_rels)
        _log(f"relationships export done: wrote {r_written} lines")
    finally:
        driver.close()

    nodes_path = SNAP_DIR / "nodes.jsonl"
    rels_path = SNAP_DIR / "relationships.jsonl"
    n_lines = file_line_count(nodes_path)
    r_lines = file_line_count(rels_path)
    n_bytes = file_byte_size(nodes_path)
    r_bytes = file_byte_size(rels_path)

    verified = True
    if n_lines != expected_nodes:
        _warn(
            f"nodes.jsonl line count {n_lines} != stats.nodeCount {expected_nodes}"
        )
        verified = False
    if r_lines != expected_rels:
        _warn(
            f"relationships.jsonl line count {r_lines} != stats.relCount {expected_rels}"
        )
        verified = False

    finished_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
    elapsed = time.perf_counter() - started

    flag_text = (
        f"snapshot_completed_at: {finished_iso}\n"
        f"snapshot_started_at: {started_iso}\n"
        f"elapsed_seconds: {elapsed:.2f}\n"
        f"node_count: {n_lines}\n"
        f"relationship_count: {r_lines}\n"
        f"nodes_jsonl_bytes: {n_bytes}\n"
        f"relationships_jsonl_bytes: {r_bytes}\n"
        f"label_count: {label_count}\n"
        f"rel_type_count: {rel_type_count}\n"
        f"verified: {'true' if verified else 'false'}\n"
    )
    RUN_FLAG.write_text(flag_text, encoding="utf-8")

    _log(
        f"SNAPSHOT_DONE: nodes={n_lines}/{expected_nodes} "
        f"rels={r_lines}/{expected_rels} verified={verified} "
        f"elapsed={elapsed:.1f}s"
    )

    return 0 if verified else 2


if __name__ == "__main__":
    sys.exit(main())
