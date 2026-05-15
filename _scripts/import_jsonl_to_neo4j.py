"""
Import nodes and relationships from a JSONL file into Neo4j.

Each line must be valid JSON with one of two shapes:

  Node:
    {"record_type":"node","id":"<id>","labels":["Label",...],"properties":{...}}

  Relationship:
    {"record_type":"rel","id":"<id>","from":"<start_id>","type":"REL_TYPE","to":"<end_id>","properties":{...}}

All imports use MERGE keyed on `id` — safe to re-run (idempotent).
Nodes are processed before relationships in a two-pass approach.

Usage:
  python _scripts/import_jsonl_to_neo4j.py <path_to_file.kg.jsonl>
  python _scripts/import_jsonl_to_neo4j.py <path1.jsonl> <path2.jsonl> ...

Environment: reads connection from .cursor/mcp.json (same as other scripts),
overridable via NEO4J_URI, NEO4J_USERNAME / NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Allow running from any cwd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from neo4j_env import resolve_connection

from neo4j import GraphDatabase


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _merge_node(tx, record: dict) -> None:
    node_id: str = record["id"]
    labels: list[str] = record["labels"]
    props: dict = record.get("properties") or {}

    if not labels:
        raise ValueError(f"Node record missing labels: {record}")

    # Primary label drives the MERGE; additional labels are added via SET.
    primary = labels[0]
    extra = labels[1:]

    # Build properties to set (include id)
    all_props = {"id": node_id, **props}

    # Build label string for SET (e.g. SET n:LabelA:LabelB)
    extra_label_clause = ("SET n" + "".join(f":`{l}`" for l in extra)) if extra else ""

    cypher = (
        f"MERGE (n:`{primary}` {{id: $id}}) "
        f"SET n += $props "
        + (extra_label_clause + " " if extra_label_clause else "")
    )
    tx.run(cypher, id=node_id, props=all_props)


def _merge_rel(tx, record: dict) -> None:
    rel_id: str = record["id"]
    from_id: str = record["from"]
    to_id: str = record["to"]
    rel_type: str = record["type"]
    props: dict = record.get("properties") or {}

    all_props = {"id": rel_id, **props}

    # Relationship ids are globally unique in the live graph.  Imports may be
    # replayed after actor-id reconciliation has redirected an existing
    # relationship to canonical endpoints, so matching through the original
    # endpoints can incorrectly attempt to create a duplicate id.  Reuse an
    # existing relationship by id first; only create when the id is new.
    existing = tx.run(
        "MATCH ()-[r {id: $rel_id}]->() RETURN count(r) AS count",
        rel_id=rel_id,
    ).single()["count"]
    if existing:
        tx.run(
            "MATCH ()-[r {id: $rel_id}]->() SET r += $props",
            rel_id=rel_id,
            props=all_props,
        )
        return

    cypher = (
        f"MATCH (a {{id: $from_id}}) "
        f"MATCH (b {{id: $to_id}}) "
        f"MERGE (a)-[r:`{rel_type}` {{id: $rel_id}}]->(b) "
        f"SET r += $props"
    )
    tx.run(cypher, from_id=from_id, to_id=to_id, rel_id=rel_id, props=all_props)


# ---------------------------------------------------------------------------
# Main import logic
# ---------------------------------------------------------------------------

def import_file(driver, database: str, path: Path) -> tuple[int, int]:
    """Import a single JSONL file. Returns (nodes_merged, rels_merged)."""
    records = []
    with open(path, encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"  [WARN] Line {lineno} skipped (JSON error): {e}")

    nodes = [r for r in records if r.get("record_type") == "node"]
    rels  = [r for r in records if r.get("record_type") == "rel"]

    node_count = 0
    rel_count  = 0

    # Pass 1: nodes
    if nodes:
        with driver.session(database=database) as session:
            for record in nodes:
                session.execute_write(_merge_node, record)
                node_count += 1

    # Pass 2: relationships
    if rels:
        with driver.session(database=database) as session:
            for record in rels:
                session.execute_write(_merge_rel, record)
                rel_count += 1

    return node_count, rel_count


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python import_jsonl_to_neo4j.py <file.kg.jsonl> [file2.kg.jsonl ...]")
        sys.exit(1)

    uri, user, password, database = resolve_connection()
    if not uri or not password:
        print("ERROR: Neo4j connection not configured. Check .cursor/mcp.json or env vars.")
        sys.exit(1)

    driver = GraphDatabase.driver(uri, auth=(user, password))

    try:
        driver.verify_connectivity()
    except Exception as e:
        print(f"ERROR: Cannot connect to Neo4j at {uri}: {e}")
        sys.exit(1)

    total_nodes = 0
    total_rels  = 0

    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.is_file():
            print(f"  [SKIP] File not found: {path}")
            continue
        print(f"Importing {path.name} ...", end=" ", flush=True)
        n, r = import_file(driver, database, path)
        print(f"{n} nodes, {r} rels")
        total_nodes += n
        total_rels  += r

    driver.close()
    print(f"\nDone. Total: {total_nodes} nodes merged, {total_rels} relationships merged.")


if __name__ == "__main__":
    main()
