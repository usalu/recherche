"""
Export Neo4j graph schema (labels, relationship types, constraints, indexes) to JSON.

Uses the same connection env vars as import_database_folder_to_neo4j.py:
  NEO4J_URI, NEO4J_USER, NEO4J_DATABASE, NEO4J_PASSWORD
  or --password-file <path> (first non-empty, non-# line).

Example:
  python _scripts/export_neo4j_schema.py --password-file .neo4j_password
  python _scripts/export_neo4j_schema.py --out _neo4j/review/neo4j_schema_export.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Repo root on sys.path for importer constants
_REPO = Path(__file__).resolve().parents[1]
_scripts = _REPO / "_scripts"
if str(_scripts) not in sys.path:
    sys.path.insert(0, str(_scripts))

from import_database_folder_to_neo4j import ENTITY_LABEL  # noqa: E402
from neo4j_relation_fold import NEO4J_REL_TYPES  # noqa: E402


def _json_safe(obj):
    """Convert Neo4j driver / temporal types to JSON-serializable values."""
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, dict):
        return {str(k): _json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_json_safe(v) for v in obj]
    if isinstance(obj, (frozenset, set)):
        return sorted(_json_safe(v) for v in obj)
    return str(obj)


def _read_password(password_file: Path | None) -> str:
    password = (os.environ.get("NEO4J_PASSWORD") or "").strip()
    if password or password_file is None:
        return password
    if not password_file.is_file():
        raise FileNotFoundError(f"--password-file not found: {password_file}")
    for line in password_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    return ""


def _rows(session, cypher: str) -> list[dict]:
    result = session.run(cypher)
    keys = result.keys()
    out: list[dict] = []
    for record in result:
        out.append(_json_safe({k: record[k] for k in keys}))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Export Neo4j schema metadata to JSON.")
    ap.add_argument(
        "--out",
        type=Path,
        default=_REPO / "_neo4j" / "review" / "neo4j_schema_export.json",
        help="Output JSON path (default: _neo4j/review/neo4j_schema_export.json)",
    )
    ap.add_argument(
        "--password-file",
        type=Path,
        default=None,
        help="Read Neo4j password from first non-empty line (UTF-8).",
    )
    args = ap.parse_args()

    password = _read_password(args.password_file)
    if not password:
        print(
            "NEO4J_PASSWORD is not set. Export it or pass --password-file <path>.",
            file=sys.stderr,
        )
        return 1

    try:
        from neo4j import GraphDatabase
    except ImportError:
        print("Install: pip install -r requirements-neo4j.txt", file=sys.stderr)
        return 1

    uri = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687").strip()
    user = os.environ.get("NEO4J_USER", "neo4j").strip()
    database = (os.environ.get("NEO4J_DATABASE") or "neo4j").strip() or "neo4j"

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as sess:
            labels = [r["label"] for r in _rows(sess, "CALL db.labels() YIELD label RETURN label ORDER BY label")]
            rel_types = [
                r["relationshipType"]
                for r in _rows(
                    sess,
                    "CALL db.relationshipTypes() YIELD relationshipType AS relationshipType "
                    "RETURN relationshipType ORDER BY relationshipType",
                )
            ]
            constraints: list[dict] = []
            indexes: list[dict] = []
            try:
                constraints = _rows(sess, "SHOW CONSTRAINTS")
            except Exception as e:  # noqa: BLE001
                constraints = [{"error": str(e)}]
            try:
                indexes = _rows(sess, "SHOW INDEXES")
            except Exception as e:  # noqa: BLE001
                indexes = [{"error": str(e)}]

            node_counts = _rows(
                sess,
                "MATCH (n) UNWIND labels(n) AS label RETURN label, count(*) AS node_count ORDER BY label",
            )
    finally:
        driver.close()

    payload = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "connection": {"uri": uri, "user": user, "database": database},
        "normative_plan": ".cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md",
        "inventory_entity_to_neo4j_label": dict(sorted(ENTITY_LABEL.items())),
        "folded_relationship_types": sorted(NEO4J_REL_TYPES),
        "live_graph": {
            "node_labels": labels,
            "relationship_types": rel_types,
            "constraints": constraints,
            "indexes": indexes,
            "node_counts_by_label": node_counts,
        },
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
