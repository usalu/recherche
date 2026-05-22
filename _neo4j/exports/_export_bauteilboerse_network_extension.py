"""Extend the enriched Bauteilboerse network JSON with broader live coverage.

Starts from the existing enriched export file and preserves everything already in
it, then adds:

- all live Akteur nodes
- all live Projekt nodes
- all live Bauteilgruppe nodes
- all live Bauwerk nodes
- donor-related live nodes modeled via Bauwerk / Materialdepot /
  Ressourcenquelle / Bauobjektrolle / Wiederverwendungskette / Programm /
  Software
- all direct 1-hop neighbours and incident edges of those force-included nodes
- all internal edges between the collected nodes

There is no dedicated :Donor label in the live graph. Donor semantics are
captured through FROM_DONOR edges and donor-side Bauwerk / Materialdepot /
Ressourcenquelle / Bauobjektrolle nodes.
"""
from __future__ import annotations

import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase

URI = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687").strip()
USER = (os.environ.get("NEO4J_USER") or os.environ.get("NEO4J_USERNAME") or "neo4j").strip()
DATABASE = os.environ.get("NEO4J_DATABASE", "mit-bestand").strip()
PWPATH = Path(".neo4j_password")

SOURCE = Path(
    "_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json"
)
OUT = Path(
    "_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges_extended.json"
)

FORCE_INCLUDE_LABELS = {
    "Akteur",
    "Projekt",
    "Bauteilgruppe",
    "Bauwerk",
    "Materialdepot",
    "Programm",
    "Software",
    "Ressourcenquelle",
    "Bauobjektrolle",
    "Wiederverwendungskette",
}


def read_password() -> str:
    env_password = (os.environ.get("NEO4J_PASSWORD") or "").strip()
    if env_password:
        return env_password

    for line in PWPATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    raise RuntimeError("No password found in NEO4J_PASSWORD or .neo4j_password")


def to_jsonable(value):
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    if hasattr(value, "iso_format"):
        return value.iso_format()
    return str(value)


def is_live_element_id(element_id: str | None) -> bool:
    return bool(element_id) and not str(element_id).startswith("synthetic:")


def add_node(nodes_by_eid: dict[str, dict], node) -> None:
    if node is None:
        return
    nodes_by_eid[node.element_id] = {
        "elementId": node.element_id,
        "labels": list(node.labels),
        "properties": {key: to_jsonable(value) for key, value in dict(node).items()},
    }


def add_edge(edges_by_eid: dict[str, dict], rel) -> None:
    if rel is None:
        return
    edges_by_eid[rel.element_id] = {
        "elementId": rel.element_id,
        "type": rel.type,
        "source": rel.start_node.element_id,
        "target": rel.end_node.element_id,
        "properties": {key: to_jsonable(value) for key, value in dict(rel).items()},
    }


def load_base_doc() -> tuple[dict, dict[str, dict], dict[str, dict], dict[str, str]]:
    doc = json.loads(SOURCE.read_text(encoding="utf-8"))
    nodes_by_eid = {node["elementId"]: node for node in doc.get("nodes", [])}
    edges_by_eid = {edge["elementId"]: edge for edge in doc.get("edges", [])}
    descriptions = {item["label"]: item.get("description", "") for item in doc.get("nodetypes", [])}
    return doc, nodes_by_eid, edges_by_eid, descriptions


def batched(items: list[str], size: int) -> list[list[str]]:
    return [items[index:index + size] for index in range(0, len(items), size)]


def main() -> None:
    base_doc, nodes_by_eid, edges_by_eid, nt_descriptions = load_base_doc()
    password = read_password()
    driver = GraphDatabase.driver(URI, auth=(USER, password))

    forced_label_counts: dict[str, int] = {}

    with driver.session(database=DATABASE) as session:
        rows = list(
            session.run(
                """
                MATCH (n)
                WHERE any(label IN labels(n) WHERE label IN $labels)
                RETURN n
                """,
                labels=sorted(FORCE_INCLUDE_LABELS),
            )
        )

        force_eids: list[str] = []
        for record in rows:
            node = record["n"]
            add_node(nodes_by_eid, node)
            force_eids.append(node.element_id)

        for label in sorted(FORCE_INCLUDE_LABELS):
            forced_label_counts[label] = sum(
                1 for record in rows if label in list(record["n"].labels)
            )

        print(f"Loaded {len(force_eids)} live nodes across force labels.")

        print("Pulling 1-hop neighbours and incident edges of force-included nodes...")
        for chunk in batched(force_eids, 250):
            for record in session.run(
                """
                UNWIND $eids AS eid
                MATCH (n) WHERE elementId(n) = eid
                OPTIONAL MATCH (n)-[r_out]->(m_out)
                WITH n, collect(DISTINCT {r: r_out, other: m_out}) AS out_pairs
                OPTIONAL MATCH (m_in)-[r_in]->(n)
                RETURN n, out_pairs, collect(DISTINCT {r: r_in, other: m_in}) AS in_pairs
                """,
                eids=chunk,
            ):
                add_node(nodes_by_eid, record["n"])
                for bucket in (record["out_pairs"], record["in_pairs"]):
                    for item in bucket:
                        rel = item["r"]
                        other = item["other"]
                        if rel is None or other is None:
                            continue
                        add_edge(edges_by_eid, rel)
                        add_node(nodes_by_eid, other)

        print("Densifying internal edges between collected live nodes...")
        live_eids = [eid for eid in nodes_by_eid.keys() if is_live_element_id(eid)]
        for chunk in batched(live_eids, 300):
            for record in session.run(
                """
                UNWIND $eids AS eid
                MATCH (a) WHERE elementId(a) = eid
                MATCH (a)-[r]->(b)
                WHERE elementId(b) IN $all_eids
                RETURN r
                LIMIT 200000
                """,
                eids=chunk,
                all_eids=live_eids,
            ):
                add_edge(edges_by_eid, record["r"])

    driver.close()

    nt_descriptions.update(
        {
            "Akteur": "Operator / company (Bauteilboerse anchor or related actor)",
            "Projekt": "Reuse project anchor",
            "Bauteilgruppe": "Component group / batch / project-side reuse group",
            "Bauwerk": "Building / donor / receiver / source structure",
            "Materialdepot": "Material depot / stockholder / aggregated donor stock",
            "Ressourcenquelle": "Resource-source vocabulary",
            "Bauobjektrolle": "Building-object role vocabulary",
            "Wiederverwendungskette": "Reuse-chain node",
            "Programm": "Programme node",
            "Software": "Software product node",
        }
    )

    nt_counter: Counter = Counter()
    for node in nodes_by_eid.values():
        for label in node.get("labels", []):
            nt_counter[label] += 1

    et_counter: Counter = Counter()
    et_endpoints: dict[str, dict] = defaultdict(lambda: {"from_labels": set(), "to_labels": set()})
    for edge in edges_by_eid.values():
        et_counter[edge["type"]] += 1
        source_labels = tuple(nodes_by_eid.get(edge["source"], {}).get("labels", []))
        target_labels = tuple(nodes_by_eid.get(edge["target"], {}).get("labels", []))
        et_endpoints[edge["type"]]["from_labels"].update(source_labels)
        et_endpoints[edge["type"]]["to_labels"].update(target_labels)

    metadata = dict(base_doc.get("metadata", {}))
    metadata.update(
        {
            "extended_generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "extended_from_file": SOURCE.name,
            "extended_output_file": OUT.name,
            "extended_force_included_labels": sorted(FORCE_INCLUDE_LABELS),
            "extended_force_included_live_counts": forced_label_counts,
            "extended_policy": (
                "Preserve the existing enriched JSON exactly, then top it up with all live "
                "Akteur/Projekt/Bauteilgruppe/Bauwerk plus donor-related nodes modeled via "
                "Bauwerk/Materialdepot/Ressourcenquelle/Bauobjektrolle/Wiederverwendungskette, "
                "plus all direct 1-hop neighbours and internal edges."
            ),
            "extended_donor_model_note": (
                "There is no dedicated Donor label in the live graph; donor semantics are "
                "captured by FROM_DONOR edges and donor-side Bauwerk / Materialdepot / "
                "Ressourcenquelle / Bauobjektrolle nodes."
            ),
            "scope": (
                str(base_doc.get("metadata", {}).get("scope", "Bauteilboerse network"))
                + " + extension: all live Akteur/Projekt/Bauteilgruppe/Bauwerk and donor-related nodes"
            ),
            "node_count": len(nodes_by_eid),
            "edge_count": len(edges_by_eid),
        }
    )

    doc = {
        "metadata": metadata,
        "nodetypes": [
            {
                "label": label,
                "count": count,
                "description": nt_descriptions.get(label, ""),
            }
            for label, count in sorted(nt_counter.items(), key=lambda item: (-item[1], item[0]))
        ],
        "edgetypes": [
            {
                "type": edge_type,
                "count": et_counter[edge_type],
                "from_labels": sorted(et_endpoints[edge_type]["from_labels"]),
                "to_labels": sorted(et_endpoints[edge_type]["to_labels"]),
            }
            for edge_type in sorted(et_counter.keys(), key=lambda item: (-et_counter[item], item))
        ],
        "nodes": sorted(
            nodes_by_eid.values(),
            key=lambda node: (
                node["labels"][0] if node.get("labels") else "",
                (node.get("properties") or {}).get("id") or node.get("elementId"),
            ),
        ),
        "edges": sorted(
            edges_by_eid.values(),
            key=lambda edge: (edge.get("type"), edge.get("source"), edge.get("target")),
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Written {OUT}")
    print(f"  nodes: {len(nodes_by_eid)}")
    print(f"  edges: {len(edges_by_eid)}")
    print("  requested label coverage:")
    for label in ("Akteur", "Projekt", "Bauteilgruppe", "Bauwerk"):
        print(f"    {label}: {nt_counter.get(label, 0)}")


if __name__ == "__main__":
    main()