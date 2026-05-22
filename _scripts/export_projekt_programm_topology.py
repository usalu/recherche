"""Export the direct topology around :Projekt|:Programm anchors.

Scope: every node carrying label :Projekt or :Programm, every directly-adjacent
node, and every relationship incident to an anchor. No property bags are
exported. Nodes contain only elementId and labels; edges contain only
elementId, type, source elementId, and target elementId.

Replaces the 2026-05-31 :Projekt-only export at
_neo4j/review/2026-05-31_project_direct_topology_export_mit-bestand/.
Anchor scope widened on 2026-06-01 to include :Programm because the 6
canonicals stripped from :Projekt → :Programm on 2026-05-31 would otherwise
fall out of the export.

Example:
  python _scripts/export_projekt_programm_topology.py \
    --out _neo4j/review/2026-06-01_projekt_programm_topology_export_mit-bestand/topology.nodes_edges_only.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "_scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    if not all([uri, user, password, database]):
        print("Missing Neo4j connection settings.", file=sys.stderr)
        return 1

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database, default_access_mode="READ") as sess:
            anchors = list(sess.run(
                "MATCH (p) WHERE p:Projekt OR p:Programm "
                "RETURN elementId(p) AS id, labels(p) AS labels"
            ))
            anchor_ids = [r["id"] for r in anchors]

            neighbour_rows = list(sess.run(
                "MATCH (p)-[r]-(n) WHERE elementId(p) IN $aids AND NOT elementId(n) IN $aids "
                "RETURN DISTINCT elementId(n) AS id, labels(n) AS labels",
                aids=anchor_ids,
            ))

            edge_rows = list(sess.run(
                "MATCH (a)-[r]->(b) WHERE elementId(a) IN $aids OR elementId(b) IN $aids "
                "RETURN elementId(r) AS id, type(r) AS type, "
                "elementId(a) AS source, elementId(b) AS target",
                aids=anchor_ids,
            ))
    finally:
        driver.close()

    # Build the JSON shape that mirrors the 2026-05-31 export
    nodes = []
    for r in anchors:
        nodes.append({"elementId": r["id"], "labels": list(r["labels"])})
    for r in neighbour_rows:
        nodes.append({"elementId": r["id"], "labels": list(r["labels"])})
    edges = [
        {"elementId": r["id"], "type": r["type"], "source": r["source"], "target": r["target"]}
        for r in edge_rows
    ]

    payload = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "database": database,
        "scope": "all :Projekt + :Programm anchors, directly adjacent nodes, and all relationships incident to anchors",
        "counts": {
            "anchors": len(anchors),
            "neighbours": len(neighbour_rows),
            "nodes_total": len(nodes),
            "edges": len(edges),
        },
        "nodes": nodes,
        "edges": edges,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.out}")
    print(f"  anchors:    {len(anchors)}")
    print(f"  neighbours: {len(neighbour_rows)}")
    print(f"  edges:      {len(edges)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
