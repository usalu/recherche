"""Create a rollback-safe logical backup of the configured Neo4j database.

The backup is intentionally plain JSONL so it can be inspected, checksummed,
and restored without APOC or neo4j-admin. Connection settings come from the
same `.cursor/mcp.json` / environment variables used by the import scripts.

Usage:
  python _scripts/backup_neo4j_graph.py
  python _scripts/backup_neo4j_graph.py --out-dir _neo4j/review/backups/manual
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import repo_root, resolve_connection  # noqa: E402


# Neo4j identifiers in this graph include German Unicode names such as
# ``GEHÖRT_ZU``.  ``[^\W\d]`` means "a Unicode word character that is not a
# digit", so this still rejects empty names and digit-prefixed identifiers
# while allowing valid non-ASCII labels / relationship types.
LABEL_RE = re.compile(r"^[^\W\d]\w*$", re.UNICODE)
REL_TYPE_RE = re.compile(r"^[^\W\d]\w*$", re.UNICODE)


def json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted(json_safe(v) for v in value)
    return str(value)


def write_json(path: Path, payload: dict) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rows(session, cypher: str) -> list[dict]:
    result = session.run(cypher)
    keys = result.keys()
    return [json_safe({k: record[k] for k in keys}) for record in result]


def snapshot_schema(session) -> dict:
    constraints: list[dict]
    indexes: list[dict]
    try:
        constraints = rows(session, "SHOW CONSTRAINTS")
    except Exception as exc:  # noqa: BLE001
        constraints = [{"error": str(exc)}]
    try:
        indexes = rows(session, "SHOW INDEXES")
    except Exception as exc:  # noqa: BLE001
        indexes = [{"error": str(exc)}]

    return {
        "labels": [
            r["label"]
            for r in rows(
                session, "CALL db.labels() YIELD label RETURN label ORDER BY label"
            )
        ],
        "relationship_types": [
            r["relationshipType"]
            for r in rows(
                session,
                "CALL db.relationshipTypes() YIELD relationshipType "
                "RETURN relationshipType ORDER BY relationshipType",
            )
        ],
        "constraints": constraints,
        "indexes": indexes,
        "node_counts_by_label": rows(
            session,
            "MATCH (n) UNWIND labels(n) AS label "
            "RETURN label, count(*) AS node_count ORDER BY label",
        ),
        "relationship_counts_by_type": rows(
            session,
            "MATCH ()-[r]->() RETURN type(r) AS type, count(*) AS rel_count "
            "ORDER BY type",
        ),
    }


def default_out_dir(database: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_db = re.sub(r"[^A-Za-z0-9_.-]+", "_", database or "neo4j")
    return repo_root() / "_neo4j" / "review" / "backups" / f"{stamp}-{safe_db}"


def export_backup(out_dir: Path) -> dict:
    try:
        from neo4j import GraphDatabase
    except ImportError as exc:
        raise SystemExit("Install: pip install -r requirements-neo4j.txt") from exc

    uri, user, password, database = resolve_connection()
    if not uri or not user or not password:
        raise SystemExit("Missing Neo4j connection settings.")

    out_dir.mkdir(parents=True, exist_ok=False)
    backup_path = out_dir / "live_graph.backup.jsonl"
    counts_path = out_dir / "counts.json"
    schema_path = out_dir / "schema_snapshot.json"
    manifest_path = out_dir / "backup_manifest.json"
    checksums_path = out_dir / "checksums.sha256"

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            counts = rows(
                session,
                "MATCH (n) WITH count(n) AS nodes "
                "MATCH ()-[r]->() RETURN nodes, count(r) AS relationships",
            )[0]
            schema = snapshot_schema(session)

            node_rows = rows(
                session,
                "MATCH (n) RETURN elementId(n) AS element_id, labels(n) AS labels, "
                "properties(n) AS properties ORDER BY elementId(n)",
            )
            element_to_key = {
                row["element_id"]: f"n{idx}" for idx, row in enumerate(node_rows)
            }

            rel_rows = rows(
                session,
                "MATCH (a)-[r]->(b) "
                "RETURN elementId(r) AS element_id, elementId(a) AS from_element_id, "
                "elementId(b) AS to_element_id, type(r) AS type, properties(r) AS properties "
                "ORDER BY elementId(r)",
            )

            with backup_path.open("w", encoding="utf-8", newline="\n") as f:
                for row in node_rows:
                    labels = row["labels"]
                    if any(not LABEL_RE.match(label) for label in labels):
                        raise ValueError(f"Unsafe Neo4j label in backup: {labels!r}")
                    record = {
                        "record_type": "node",
                        "backup_key": element_to_key[row["element_id"]],
                        "element_id": row["element_id"],
                        "labels": labels,
                        "properties": row["properties"],
                    }
                    f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

                for idx, row in enumerate(rel_rows):
                    rel_type = row["type"]
                    if not REL_TYPE_RE.match(rel_type):
                        raise ValueError(f"Unsafe relationship type in backup: {rel_type!r}")
                    record = {
                        "record_type": "rel",
                        "backup_key": f"r{idx}",
                        "element_id": row["element_id"],
                        "from_backup_key": element_to_key[row["from_element_id"]],
                        "to_backup_key": element_to_key[row["to_element_id"]],
                        "type": rel_type,
                        "properties": row["properties"],
                    }
                    f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

            write_json(counts_path, counts)
            write_json(schema_path, schema)

            files = [backup_path, counts_path, schema_path]
            checksums = {p.name: sha256_file(p) for p in files}
            checksums_path.write_text(
                "".join(f"{digest}  {name}\n" for name, digest in sorted(checksums.items())),
                encoding="utf-8",
            )
            checksums["checksums.sha256"] = sha256_file(checksums_path)

            manifest = {
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "database": database,
                "connection": {"uri": uri, "user": user},
                "backup_format": "neo4j-logical-jsonl-v1",
                "files": {
                    "graph": backup_path.name,
                    "counts": counts_path.name,
                    "schema": schema_path.name,
                    "checksums": checksums_path.name,
                },
                "counts": counts,
                "checksums_sha256": checksums,
                "restore_confirmation": (
                    f"RESTORE {database} FROM {out_dir.name}"
                ),
            }
            write_json(manifest_path, manifest)
    finally:
        driver.close()

    return {
        "out_dir": str(out_dir),
        "database": database,
        "nodes": counts["nodes"],
        "relationships": counts["relationships"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    _, _, _, database = resolve_connection()
    out_dir = args.out_dir or default_out_dir(database)
    result = export_backup(out_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
