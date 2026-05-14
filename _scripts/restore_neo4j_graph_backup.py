"""Restore a logical Neo4j backup created by backup_neo4j_graph.py.

Default mode is non-destructive validation. A destructive restore requires the
exact confirmation phrase stored in `backup_manifest.json`.

Usage:
  python _scripts/restore_neo4j_graph_backup.py _neo4j/review/backups/<backup>
  python _scripts/restore_neo4j_graph_backup.py _neo4j/review/backups/<backup> \
    --confirm "RESTORE mit-bestand FROM <backup>"
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402


LABEL_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
REL_TYPE_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
TEMP_KEY = "__restore_backup_key"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_backup(backup_dir: Path) -> tuple[dict, list[dict], list[dict]]:
    manifest = load_json(backup_dir / "backup_manifest.json")
    graph_path = backup_dir / manifest["files"]["graph"]

    checksums = manifest.get("checksums_sha256") or {}
    for name, expected in checksums.items():
        if name == "checksums.sha256":
            continue
        path = backup_dir / name
        if path.exists() and sha256_file(path) != expected:
            raise SystemExit(f"Checksum mismatch: {path}")

    nodes: list[dict] = []
    rels: list[dict] = []
    with graph_path.open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            record_type = record.get("record_type")
            if record_type == "node":
                labels = record.get("labels") or []
                if not labels or any(not LABEL_RE.match(label) for label in labels):
                    raise SystemExit(f"Unsafe/missing labels at {graph_path}:{lineno}")
                nodes.append(record)
            elif record_type == "rel":
                rel_type = record.get("type") or ""
                if not REL_TYPE_RE.match(rel_type):
                    raise SystemExit(f"Unsafe relationship type at {graph_path}:{lineno}")
                rels.append(record)
            else:
                raise SystemExit(f"Unknown record_type at {graph_path}:{lineno}")
    return manifest, nodes, rels


def validate_only(backup_dir: Path) -> dict:
    manifest, nodes, rels = load_backup(backup_dir)
    expected = manifest.get("counts") or {}
    result = {
        "backup_dir": str(backup_dir),
        "database": manifest.get("database"),
        "nodes_in_backup": len(nodes),
        "relationships_in_backup": len(rels),
        "expected_nodes": expected.get("nodes"),
        "expected_relationships": expected.get("relationships"),
        "valid": len(nodes) == expected.get("nodes")
        and len(rels) == expected.get("relationships"),
        "restore_confirmation": manifest.get("restore_confirmation"),
    }
    return result


def label_clause(labels: list[str]) -> str:
    return "".join(f":`{label}`" for label in labels)


def restore(backup_dir: Path, confirm: str) -> dict:
    try:
        from neo4j import GraphDatabase
    except ImportError as exc:
        raise SystemExit("Install: pip install -r requirements-neo4j.txt") from exc

    manifest, nodes, rels = load_backup(backup_dir)
    expected_confirm = manifest.get("restore_confirmation")
    if confirm != expected_confirm:
        raise SystemExit(
            "Refusing destructive restore. Confirmation must exactly equal: "
            f"{expected_confirm!r}"
        )

    uri, user, password, database = resolve_connection()
    if database != manifest.get("database"):
        raise SystemExit(
            f"Configured database {database!r} does not match backup database "
            f"{manifest.get('database')!r}."
        )

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            session.run("MATCH (n) DETACH DELETE n").consume()

            for record in nodes:
                props = dict(record.get("properties") or {})
                props[TEMP_KEY] = record["backup_key"]
                cypher = f"CREATE (n{label_clause(record['labels'])}) SET n = $props"
                session.run(cypher, props=props).consume()

            for record in rels:
                cypher = (
                    f"MATCH (a {{{TEMP_KEY}: $from_key}}) "
                    f"MATCH (b {{{TEMP_KEY}: $to_key}}) "
                    f"CREATE (a)-[r:`{record['type']}`]->(b) SET r = $props"
                )
                session.run(
                    cypher,
                    from_key=record["from_backup_key"],
                    to_key=record["to_backup_key"],
                    props=record.get("properties") or {},
                ).consume()

            session.run(f"MATCH (n) REMOVE n.{TEMP_KEY}").consume()
            counts = session.run(
                "MATCH (n) WITH count(n) AS nodes "
                "MATCH ()-[r]->() RETURN nodes, count(r) AS relationships"
            ).single()
            return {
                "database": database,
                "nodes": int(counts["nodes"]),
                "relationships": int(counts["relationships"]),
            }
    finally:
        driver.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("backup_dir", type=Path)
    parser.add_argument(
        "--confirm",
        default="",
        help="Exact destructive restore confirmation phrase from backup_manifest.json.",
    )
    args = parser.parse_args()

    if args.confirm:
        result = restore(args.backup_dir, args.confirm)
    else:
        result = validate_only(args.backup_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
