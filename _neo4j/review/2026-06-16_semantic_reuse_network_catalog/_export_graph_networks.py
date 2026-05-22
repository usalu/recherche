"""Validate and export all catalog graph networks to JSON (no row limits)."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from neo4j import GraphDatabase
from neo4j.graph import Node, Path as GraphPath, Relationship

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
sys.path.insert(0, str(REPO / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

from _graph_queries import GRAPH_NETWORKS  # noqa: E402

OUT_DIR = ROOT / "graph_networks"
MANIFEST = OUT_DIR / "manifest.json"


def write_manifest(database: str, networks: dict[str, dict]) -> None:
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "database": database,
        "network_count": len(networks),
        "networks": [
            {
                "id": net_id,
                "file": f"{net_id}.json",
                "section": payload["section"],
                "title": payload["title"],
                "node_count": payload["node_count"],
                "relationship_count": payload["relationship_count"],
                "row_count": payload["row_count"],
            }
            for net_id, payload in sorted(networks.items())
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [json_safe(v) for v in value]
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    return str(value)


def serialize_node(node: Node) -> dict[str, Any]:
    return {
        "element_id": node.element_id,
        "id": node.get("id"),
        "labels": list(node.labels),
        "properties": json_safe(dict(node)),
    }


def serialize_relationship(rel: Relationship) -> dict[str, Any]:
    return {
        "element_id": rel.element_id,
        "type": rel.type,
        "start_element_id": rel.start_node.element_id,
        "end_element_id": rel.end_node.element_id,
        "start_id": rel.start_node.get("id"),
        "end_id": rel.end_node.get("id"),
        "properties": json_safe(dict(rel)),
    }


def collect_graph(records: list[dict[str, Any]]) -> tuple[list[dict], list[dict], int]:
    nodes: dict[str, dict] = {}
    rels: dict[str, dict] = {}

    def add_node(n: Node) -> None:
        if n.element_id not in nodes:
            nodes[n.element_id] = serialize_node(n)

    def add_rel(r: Relationship) -> None:
        add_node(r.start_node)
        add_node(r.end_node)
        if r.element_id not in rels:
            rels[r.element_id] = serialize_relationship(r)

    for record in records:
        for value in record.values():
            if isinstance(value, Node):
                add_node(value)
            elif isinstance(value, Relationship):
                add_rel(value)
            elif isinstance(value, GraphPath):
                for n in value.nodes:
                    add_node(n)
                for r in value.relationships:
                    add_rel(r)

    return list(nodes.values()), list(rels.values()), len(records)


def run_network(session, spec: dict[str, str]) -> dict[str, Any]:
    cypher = spec["cypher"].strip()
    records = [dict(row) for row in session.run(cypher)]
    nodes, relationships, row_count = collect_graph(records)
    return {
        "id": spec["id"],
        "section": spec["section"],
        "title": spec["title"],
        "cypher": cypher,
        "status": "ok",
        "row_count": row_count,
        "node_count": len(nodes),
        "relationship_count": len(relationships),
        "nodes": nodes,
        "relationships": relationships,
    }


def main() -> None:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))

    networks: dict[str, dict] = {}
    failures: list[dict[str, str]] = []

    with driver.session(database=database) as session:
        for spec in GRAPH_NETWORKS:
            net_id = spec["id"]
            print(f"Running {net_id} ...", end=" ", flush=True)
            try:
                payload = run_network(session, spec)
                networks[net_id] = payload
                print(
                    f"OK rows={payload['row_count']} "
                    f"nodes={payload['node_count']} rels={payload['relationship_count']}"
                )
            except Exception as exc:
                failures.append({"id": net_id, "error": str(exc)})
                print(f"FAIL {exc}")

    driver.close()

    if failures:
        report = ROOT / "graph_networks_export_errors.json"
        report.write_text(json.dumps({"failures": failures}, indent=2), encoding="utf-8")
        raise SystemExit(
            f"{len(failures)} network(s) failed validation. See {report.name}"
        )

    OUT_DIR.mkdir(exist_ok=True)
    for net_id, payload in networks.items():
        path = OUT_DIR / f"{net_id}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    write_manifest(database, networks)
    print(f"Wrote {len(networks)} graph files + manifest under {OUT_DIR}/")


if __name__ == "__main__":
    main()
