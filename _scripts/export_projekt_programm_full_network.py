"""Export :Projekt + :Programm anchors with their full 2-hop neighbourhood.

Scope:
  - Anchors: every node carrying label :Projekt or :Programm.
  - 1-hop: every node directly adjacent to an anchor, every edge incident to
    an anchor (either direction).
  - 2-hop: through middle nodes carrying :Bauteilgruppe, :Bauwerk, :Akteur,
    :Software, :Projekt, or :Programm, pull their outgoing neighbours. This
    surfaces :Schadstoff, :Huerde, :Kennwert, :Stadt, :WiederverwendungsArt,
    :MatchingQualitaet, etc. — vocabularies that hang off project-side
    middle nodes.
  - Densify: every edge that connects two already-collected nodes is
    included, so the subgraph is closed under containment.

Detail level: nodes carry elementId + labels + full property bag, edges
carry elementId + type + source + target (no edge property bag). Result
is written as a single JSON document.

Example:
  python _scripts/export_projekt_programm_full_network.py \
    --out _neo4j/review/2026-06-02_projekt_programm_full_network_export_mit-bestand/topology.json
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


MIDDLE_LABELS = ("Bauteilgruppe", "Bauwerk", "Akteur", "Software", "Projekt", "Programm")


def to_jsonable(v):
    if v is None or isinstance(v, (str, int, float, bool)):
        return v
    if isinstance(v, (list, tuple)):
        return [to_jsonable(x) for x in v]
    if hasattr(v, "iso_format"):
        return v.iso_format()
    return str(v)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True, type=Path,
                    help="Path to write the single combined JSON file.")
    args = ap.parse_args()

    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    if not all([uri, user, password, database]):
        print("Missing Neo4j connection settings.", file=sys.stderr)
        return 1

    nodes: dict[str, dict] = {}
    edges: dict[str, dict] = {}

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database, default_access_mode="READ") as s:
            # ---------- anchors ----------
            anchor_rows = list(s.run(
                "MATCH (p) WHERE p:Projekt OR p:Programm "
                "RETURN elementId(p) AS id, labels(p) AS labels, properties(p) AS props"
            ))
            anchor_ids = [r["id"] for r in anchor_rows]
            for r in anchor_rows:
                nodes[r["id"]] = {
                    "elementId": r["id"],
                    "labels": list(r["labels"]),
                    "properties": {k: to_jsonable(v) for k, v in dict(r["props"]).items()},
                }
            print(f"anchors: {len(anchor_ids)}")

            # ---------- 1-hop neighbours (with properties) ----------
            n1_rows = list(s.run(
                "MATCH (p)-[r]-(n) WHERE elementId(p) IN $aids "
                "RETURN DISTINCT elementId(n) AS id, labels(n) AS labels, "
                "properties(n) AS props",
                aids=anchor_ids,
            ))
            for r in n1_rows:
                if r["id"] not in nodes:
                    nodes[r["id"]] = {
                        "elementId": r["id"],
                        "labels": list(r["labels"]),
                        "properties": {k: to_jsonable(v) for k, v in dict(r["props"]).items()},
                    }
            print(f"  +1-hop neighbours: {len(n1_rows)} (nodes total: {len(nodes)})")

            # ---------- 1-hop edges (incident to any anchor) ----------
            e1_rows = list(s.run(
                "MATCH (a)-[r]->(b) "
                "WHERE elementId(a) IN $aids OR elementId(b) IN $aids "
                "RETURN elementId(r) AS id, type(r) AS type, "
                "elementId(a) AS source, elementId(b) AS target",
                aids=anchor_ids,
            ))
            for r in e1_rows:
                edges.setdefault(r["id"], {
                    "elementId": r["id"], "type": r["type"],
                    "source": r["source"], "target": r["target"],
                })
            print(f"  1-hop edges: {len(e1_rows)} (edges total: {len(edges)})")

            # ---------- 2-hop via middle labels ----------
            middle_ids = [
                eid for eid, node in nodes.items()
                if any(lbl in MIDDLE_LABELS for lbl in node["labels"])
            ]
            print(f"  middle nodes (2-hop sources): {len(middle_ids)}")

            n2_rows = list(s.run(
                "MATCH (m)-[r]-(t) WHERE elementId(m) IN $mids "
                "RETURN elementId(r) AS rid, type(r) AS rtype, "
                "elementId(startNode(r)) AS source, elementId(endNode(r)) AS target, "
                "elementId(t) AS nid, labels(t) AS nlabels, properties(t) AS nprops",
                mids=middle_ids,
            ))
            added_n2 = added_e2 = 0
            for r in n2_rows:
                if r["nid"] not in nodes:
                    nodes[r["nid"]] = {
                        "elementId": r["nid"],
                        "labels": list(r["nlabels"]),
                        "properties": {k: to_jsonable(v) for k, v in dict(r["nprops"]).items()},
                    }
                    added_n2 += 1
                if r["rid"] not in edges:
                    edges[r["rid"]] = {
                        "elementId": r["rid"], "type": r["rtype"],
                        "source": r["source"], "target": r["target"],
                    }
                    added_e2 += 1
            print(f"  +2-hop: {added_n2} nodes / {added_e2} edges")

            # ---------- densify: edges between collected nodes ----------
            all_ids = list(nodes.keys())
            added_e3 = 0
            BATCH = 1000
            for i in range(0, len(all_ids), BATCH):
                chunk = all_ids[i:i + BATCH]
                rows = list(s.run(
                    "MATCH (a)-[r]->(b) "
                    "WHERE elementId(a) IN $chunk AND elementId(b) IN $all_ids "
                    "RETURN elementId(r) AS id, type(r) AS type, "
                    "elementId(a) AS source, elementId(b) AS target",
                    chunk=chunk, all_ids=all_ids,
                ))
                for r in rows:
                    if r["id"] not in edges:
                        edges[r["id"]] = {
                            "elementId": r["id"], "type": r["type"],
                            "source": r["source"], "target": r["target"],
                        }
                        added_e3 += 1
            print(f"  +densify: {added_e3} internal edges")
    finally:
        driver.close()

    # ---------- aggregate counts ----------
    nt_counter: Counter = Counter()
    for n in nodes.values():
        for lbl in n["labels"]:
            nt_counter[lbl] += 1
    et_counter: Counter = Counter()
    for e in edges.values():
        et_counter[e["type"]] += 1

    metadata = {
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "database": database,
        "scope": (
            "Anchors :Projekt + :Programm, all 1-hop neighbours, "
            "2-hop via Bauteilgruppe/Bauwerk/Akteur/Software/Projekt/Programm, "
            "densified with all edges between collected nodes. "
            "Nodes carry full property bag; edges carry topology only."
        ),
        "counts": {
            "anchors": len(anchor_ids),
            "nodes_total": len(nodes),
            "edges_total": len(edges),
            "nodetypes": len(nt_counter),
            "edgetypes": len(et_counter),
        },
        "nodetypes": [
            {"label": lbl, "count": cnt}
            for lbl, cnt in sorted(nt_counter.items(), key=lambda kv: (-kv[1], kv[0]))
        ],
        "edgetypes": [
            {"type": t, "count": cnt}
            for t, cnt in sorted(et_counter.items(), key=lambda kv: (-kv[1], kv[0]))
        ],
    }

    sorted_nodes = sorted(
        nodes.values(),
        key=lambda n: (n["labels"][0] if n["labels"] else "",
                       n["properties"].get("id") or n["elementId"]),
    )
    sorted_edges = sorted(
        edges.values(),
        key=lambda e: (e["type"], e["source"], e["target"]),
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps({**metadata, "nodes": sorted_nodes, "edges": sorted_edges},
                   ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    size_mb = args.out.stat().st_size / (1024 * 1024)
    print()
    print(f"Wrote {args.out}  ({size_mb:.2f} MB)")
    print(f"  nodes:     {len(nodes)}")
    print(f"  edges:     {len(edges)}")
    print(f"  anchors:   {len(anchor_ids)}")
    print(f"  nodetypes: {len(nt_counter)}")
    print(f"  edgetypes: {len(et_counter)}")
    print("Top nodetypes:")
    for lbl, n in nt_counter.most_common(10):
        print(f"    {lbl:25s} {n}")
    print("Top edgetypes:")
    for t, n in et_counter.most_common(10):
        print(f"    {t:25s} {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
