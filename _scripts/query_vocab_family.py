"""Helper for the round_002 family re-verification.

Queries the live mit-bestand graph for a vocab family and emits:
  - hub snapshot table (id, name, inbound count, sample inbound labels)
  - same-name duplicates
  - orphans (no inbound link)
  - missing parent links (for hierarchical families)

Result is printed to stdout as JSON.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402


def query_family(labels: list[str], parent: tuple[str, str, str] | None = None) -> dict:
    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    out: dict = {"labels": labels, "snapshots": {}, "same_name_duplicates": [], "orphans": []}

    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            for label in labels:
                rows = list(
                    session.run(
                        f"MATCH (n:`{label}`) "
                        "OPTIONAL MATCH (n)<-[r]-(x) "
                        "RETURN n.id AS id, n.name AS name, "
                        "count(DISTINCT r) AS inbound, "
                        "collect(DISTINCT labels(x)[0])[..5] AS sample_in_labels "
                        "ORDER BY inbound DESC, name"
                    )
                )
                out["snapshots"][label] = [dict(r) for r in rows]
            for label in labels:
                rows = list(
                    session.run(
                        f"MATCH (n:`{label}`) WHERE n.name IS NOT NULL "
                        "WITH toLower(toString(n.name)) AS k, collect(n) AS nodes "
                        "WHERE size(nodes) > 1 "
                        "RETURN k AS name_key, [x IN nodes | x.id] AS ids, size(nodes) AS count"
                    )
                )
                for r in rows:
                    out["same_name_duplicates"].append({"label": label, **dict(r)})
            for label in labels:
                rows = list(
                    session.run(
                        f"MATCH (n:`{label}`) WHERE NOT (n)<-[]-() RETURN n.id AS id, n.name AS name"
                    )
                )
                for r in rows:
                    out["orphans"].append({"label": label, **dict(r)})
            if parent:
                child_label, rel_type, parent_label = parent
                rows = list(
                    session.run(
                        f"MATCH (child:`{child_label}`) "
                        f"WHERE NOT (child)-[:`{rel_type}`]->(:`{parent_label}`) "
                        "RETURN child.id AS id, child.name AS name"
                    )
                )
                out["missing_parent"] = [dict(r) for r in rows]
    finally:
        driver.close()
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--labels", required=True, help="comma-separated label list")
    parser.add_argument("--parent", help="child_label:REL_TYPE:parent_label")
    args = parser.parse_args()
    labels = [s.strip() for s in args.labels.split(",") if s.strip()]
    parent = None
    if args.parent:
        parts = args.parent.split(":")
        if len(parts) == 3:
            parent = (parts[0], parts[1], parts[2])
    result = query_family(labels, parent)
    sys.stdout.write(json.dumps(result, ensure_ascii=False, indent=2))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
