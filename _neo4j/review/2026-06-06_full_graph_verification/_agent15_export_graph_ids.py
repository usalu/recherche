"""Agent 15 (Aggregator) — READ-ONLY graph id inventory export.

Strictly read-only: opens a Neo4j session with default_access_mode="READ" and
runs only MATCH ... RETURN queries. No writes, no patches. Used to build the
coverage proof for the full-graph verification campaign.

Outputs (under this review folder, _agent15_work/):
- graph_nodes.json : [{"id","element_id","labels"}]
- graph_rels.json  : [{"element_id","type","from_id","to_id","from_eid","to_eid"}]
- graph_counts.json: summary counts
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402

OUT = HERE / "_agent15_work"


def main() -> int:
    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    if not all([uri, user, password, database]):
        raise RuntimeError("Missing Neo4j connection settings.")

    OUT.mkdir(parents=True, exist_ok=True)
    nodes: list[dict] = []
    rels: list[dict] = []

    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        driver.verify_connectivity()
        with driver.session(database=database, default_access_mode="READ") as s:
            for row in s.run(
                "MATCH (n) RETURN n.id AS id, elementId(n) AS eid, labels(n) AS labels"
            ):
                nodes.append(
                    {"id": row["id"], "element_id": row["eid"], "labels": row["labels"]}
                )
            for row in s.run(
                "MATCH (a)-[r]->(b) "
                "RETURN elementId(r) AS eid, type(r) AS t, "
                "a.id AS from_id, b.id AS to_id, "
                "elementId(a) AS from_eid, elementId(b) AS to_eid"
            ):
                rels.append(
                    {
                        "element_id": row["eid"],
                        "type": row["t"],
                        "from_id": row["from_id"],
                        "to_id": row["to_id"],
                        "from_eid": row["from_eid"],
                        "to_eid": row["to_eid"],
                    }
                )

    (OUT / "graph_nodes.json").write_text(
        json.dumps(nodes, ensure_ascii=False), encoding="utf-8"
    )
    (OUT / "graph_rels.json").write_text(
        json.dumps(rels, ensure_ascii=False), encoding="utf-8"
    )
    counts = {
        "database": database,
        "nodes": len(nodes),
        "rels": len(rels),
        "nodes_without_id_prop": sum(1 for n in nodes if not n["id"]),
    }
    (OUT / "graph_counts.json").write_text(
        json.dumps(counts, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(counts, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
