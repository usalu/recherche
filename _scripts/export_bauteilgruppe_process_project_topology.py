"""Export the Bauteilgruppe process topology plus attached :Projekt nodes.

Scope:
  - every :Bauteilgruppe node;
  - (:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe);
  - (:Bauteilgruppe)-[:HAT_RUECKBAUVERFAHREN]->(:Rueckbauverfahren);
  - (:Bauteilgruppe)-[:HAT_AUFBEREITUNG]->(:Aufbereitungsverfahren);
  - (:Aufbereitungsverfahren)-[:IST_UNTERVERFAHREN_VON]->(:Aufbereitungsverfahren);
  - (:Bauteilgruppe)-[:HAT_WIEDERVERWENDUNGSART]->(:WiederverwendungsArt).

Nodes carry elementId + labels + full property bag. Edges carry elementId,
type, source, and target only.

Example:
  python _scripts/export_bauteilgruppe_process_project_topology.py \
    --out _neo4j/review/2026-06-02_bauteilgruppe_process_project_export_mit-bestand/topology.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "_scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402


NODE_QUERIES = [
    (
        "bauteilgruppen",
        "MATCH (bg:Bauteilgruppe) "
        "RETURN elementId(bg) AS id, labels(bg) AS labels, properties(bg) AS props",
    ),
    (
        "projects",
        "MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe) "
        "RETURN DISTINCT elementId(p) AS id, labels(p) AS labels, properties(p) AS props",
    ),
    (
        "rueckbauverfahren",
        "MATCH (:Bauteilgruppe)-[:HAT_RUECKBAUVERFAHREN]->(rv:Rueckbauverfahren) "
        "RETURN DISTINCT elementId(rv) AS id, labels(rv) AS labels, properties(rv) AS props",
    ),
    (
        "aufbereitungsverfahren",
        "MATCH (:Bauteilgruppe)-[:HAT_AUFBEREITUNG]->(av:Aufbereitungsverfahren) "
        "RETURN DISTINCT elementId(av) AS id, labels(av) AS labels, properties(av) AS props",
    ),
    (
        "parent_aufbereitungsverfahren",
        "MATCH (:Bauteilgruppe)-[:HAT_AUFBEREITUNG]->(:Aufbereitungsverfahren)"
        "-[:IST_UNTERVERFAHREN_VON]->(parent:Aufbereitungsverfahren) "
        "RETURN DISTINCT elementId(parent) AS id, labels(parent) AS labels, properties(parent) AS props",
    ),
    (
        "wiederverwendungsarten",
        "MATCH (:Bauteilgruppe)-[:HAT_WIEDERVERWENDUNGSART]->(wva:WiederverwendungsArt) "
        "RETURN DISTINCT elementId(wva) AS id, labels(wva) AS labels, properties(wva) AS props",
    ),
]


EDGE_QUERIES = [
    (
        "HAT_BAUTEILGRUPPE",
        "MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe) "
        "RETURN elementId(r) AS id, type(r) AS type, "
        "elementId(p) AS source, elementId(bg) AS target",
    ),
    (
        "HAT_RUECKBAUVERFAHREN",
        "MATCH (bg:Bauteilgruppe)-[r:HAT_RUECKBAUVERFAHREN]->(rv:Rueckbauverfahren) "
        "RETURN elementId(r) AS id, type(r) AS type, "
        "elementId(bg) AS source, elementId(rv) AS target",
    ),
    (
        "HAT_AUFBEREITUNG",
        "MATCH (bg:Bauteilgruppe)-[r:HAT_AUFBEREITUNG]->(av:Aufbereitungsverfahren) "
        "RETURN elementId(r) AS id, type(r) AS type, "
        "elementId(bg) AS source, elementId(av) AS target",
    ),
    (
        "IST_UNTERVERFAHREN_VON",
        "MATCH (:Bauteilgruppe)-[:HAT_AUFBEREITUNG]->(av:Aufbereitungsverfahren)"
        "-[r:IST_UNTERVERFAHREN_VON]->(parent:Aufbereitungsverfahren) "
        "RETURN DISTINCT elementId(r) AS id, type(r) AS type, "
        "elementId(av) AS source, elementId(parent) AS target",
    ),
    (
        "HAT_WIEDERVERWENDUNGSART",
        "MATCH (bg:Bauteilgruppe)-[r:HAT_WIEDERVERWENDUNGSART]->(wva:WiederverwendungsArt) "
        "RETURN elementId(r) AS id, type(r) AS type, "
        "elementId(bg) AS source, elementId(wva) AS target",
    ),
]


def to_jsonable(value):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    if hasattr(value, "iso_format"):
        return value.iso_format()
    return str(value)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True, type=Path,
                    help="Path to write the combined JSON file.")
    args = ap.parse_args()

    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    if not all([uri, user, password, database]):
        print("Missing Neo4j connection settings.", file=sys.stderr)
        return 1

    nodes: dict[str, dict] = {}
    edges: dict[str, dict] = {}
    node_scope_counts: dict[str, int] = {}
    edge_scope_counts: dict[str, int] = {}

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database, default_access_mode="READ") as session:
            for scope, query in NODE_QUERIES:
                rows = list(session.run(query))
                node_scope_counts[scope] = len(rows)
                for row in rows:
                    nodes[row["id"]] = {
                        "elementId": row["id"],
                        "labels": list(row["labels"]),
                        "properties": {k: to_jsonable(v) for k, v in dict(row["props"]).items()},
                    }
                print(f"{scope}: {len(rows)}")

            for scope, query in EDGE_QUERIES:
                rows = list(session.run(query))
                edge_scope_counts[scope] = len(rows)
                for row in rows:
                    edges[row["id"]] = {
                        "elementId": row["id"],
                        "type": row["type"],
                        "source": row["source"],
                        "target": row["target"],
                    }
                print(f"{scope}: {len(rows)}")
    finally:
        driver.close()

    node_type_counts: Counter = Counter()
    for node in nodes.values():
        for label in node["labels"]:
            node_type_counts[label] += 1

    edge_type_counts: Counter = Counter()
    for edge in edges.values():
        edge_type_counts[edge["type"]] += 1

    payload = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "database": database,
        "scope": (
            "All :Bauteilgruppe nodes plus direct :Projekt attachments and the "
            "Bauteilgruppe process vocabulary reachable through "
            "HAT_RUECKBAUVERFAHREN, HAT_AUFBEREITUNG, "
            "IST_UNTERVERFAHREN_VON, and HAT_WIEDERVERWENDUNGSART. "
            "Nodes carry full property bag; edges carry topology only."
        ),
        "query": (
            "MATCH (bg:Bauteilgruppe) "
            "OPTIONAL MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg) "
            "OPTIONAL MATCH (bg)-[:HAT_RUECKBAUVERFAHREN]->(:Rueckbauverfahren) "
            "OPTIONAL MATCH (bg)-[:HAT_AUFBEREITUNG]->(av:Aufbereitungsverfahren) "
            "OPTIONAL MATCH (av)-[:IST_UNTERVERFAHREN_VON]->(:Aufbereitungsverfahren) "
            "OPTIONAL MATCH (bg)-[:HAT_WIEDERVERWENDUNGSART]->(:WiederverwendungsArt)"
        ),
        "counts": {
            "nodes_total": len(nodes),
            "edges_total": len(edges),
            "nodetypes": len(node_type_counts),
            "edgetypes": len(edge_type_counts),
            "node_scope": node_scope_counts,
            "edge_scope": edge_scope_counts,
        },
        "nodetypes": [
            {"label": label, "count": count}
            for label, count in sorted(node_type_counts.items(), key=lambda kv: (-kv[1], kv[0]))
        ],
        "edgetypes": [
            {"type": rel_type, "count": count}
            for rel_type, count in sorted(edge_type_counts.items(), key=lambda kv: (-kv[1], kv[0]))
        ],
        "nodes": sorted(
            nodes.values(),
            key=lambda node: (
                node["labels"][0] if node["labels"] else "",
                node["properties"].get("id") or node["elementId"],
            ),
        ),
        "edges": sorted(
            edges.values(),
            key=lambda edge: (edge["type"], edge["source"], edge["target"]),
        ),
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    size_mb = args.out.stat().st_size / (1024 * 1024)
    print()
    print(f"Wrote {args.out} ({size_mb:.2f} MB)")
    print(f"  nodes:     {len(nodes)}")
    print(f"  edges:     {len(edges)}")
    print(f"  nodetypes: {len(node_type_counts)}")
    print(f"  edgetypes: {len(edge_type_counts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())