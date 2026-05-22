"""Audit parallel / duplicate semantic edges in mit-bestand."""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

SEMANTIC_TYPES = [
    "VERBUNDEN_MIT_AKTEUR",
    "BETEILIGT_AN",
    "BETRIEBEN_VON",
    "GESTUETZT_AUF_REGELWERK",
    "GILT_IN_LAND",
]

uri, u, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, pw))
out: dict = {
    "database": db,
    "same_type_duplicates": [],
    "parallel_semantic_pairs": [],
    "restado_neighborhood": [],
    "bubble_tagged_parallel": [],
    "nodes_missing_evidence": {"rels": [], "actors_no_url": []},
}

try:
    with driver.session(database=db) as s:
        # Exact duplicate rels (same from, to, type) — multiple edges
        rows = s.run(
            """
            MATCH (a)-[r]->(b)
            WHERE type(r) IN $types
            WITH a.id AS from_id, b.id AS to_id, type(r) AS t, collect(r) AS rels
            WHERE size(rels) > 1
            RETURN from_id, to_id, t,
                   [x IN rels | {id: x.id, review_run: x.review_run, conf: x.evidence_confidence}] AS edges
            ORDER BY size(rels) DESC, from_id, to_id
            """
            ,
            types=SEMANTIC_TYPES,
        )
        out["same_type_duplicates"] = [dict(x) for x in rows]

        # Parallel different types between same directed pair (e.g. BETRIEBEN_VON + VERBUNDEN)
        rows = s.run(
            """
            MATCH (a)-[r]->(b)
            WHERE type(r) IN $types
            WITH a.id AS from_id, b.id AS to_id, collect(DISTINCT type(r)) AS types, count(r) AS c
            WHERE size(types) > 1
            RETURN from_id, to_id, types, c
            ORDER BY c DESC, from_id, to_id
            """
            ,
            types=SEMANTIC_TYPES,
        )
        out["parallel_semantic_pairs"] = [dict(x) for x in rows]

        # Undirected parallel: A->B and B->A both VERBUNDEN is OK; flag if >2 total same type
        rows = s.run(
            """
            MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]-(b)
            WHERE id(a) < id(b)
            WITH a.id AS a_id, b.id AS b_id, collect(r) AS rels
            WHERE size(rels) > 2
            RETURN a_id, b_id, size(rels) AS rel_count,
                   [x IN rels | {id: x.id, from: startNode(x).id, to: endNode(x).id,
                                 review_run: x.review_run, conf: x.evidence_confidence,
                                 url: x.evidence_url}] AS edges
            ORDER BY rel_count DESC
            """
        )
        out["undirected_verbunden_gt2"] = [dict(x) for x in rows]

        # software_restado / concular neighborhood
        rows = s.run(
            """
            MATCH (n)-[r]-(m)
            WHERE n.id IN ['software_restado','concular','superuse_studios_2012architecten']
            RETURN n.id AS node, type(r) AS rel_type, m.id AS other,
                   r.id AS rid, r.review_run AS run, r.evidence_confidence AS conf,
                   r.evidence_url AS url
            ORDER BY node, rel_type, other
            """
        )
        out["restado_neighborhood"] = [dict(x) for x in rows]

        # Bubble-tagged rels missing evidence fields
        rows = s.run(
            """
            MATCH ()-[r]->()
            WHERE r.review_run CONTAINS 'reuse_bubble' OR r.review_run CONTAINS 'cross_bubble'
            AND (r.evidence_url IS NULL OR r.evidence_confidence IS NULL)
            RETURN r.id AS id, type(r) AS t, r.review_run AS run
            LIMIT 50
            """
        )
        out["bubble_missing_evidence"] = [dict(x) for x in rows]

        # Akteur hubs in bubbles without primary_source_url
        rows = s.run(
            """
            MATCH (n:Akteur)-[r]-()
            WHERE r.review_run CONTAINS 'reuse_bubble' OR r.review_run CONTAINS 'cross_bubble'
            WITH DISTINCT n
            WHERE n.primary_source_url IS NULL
            RETURN n.id AS id, n.name AS name
            ORDER BY id
            LIMIT 40
            """
        )
        out["actors_missing_url"] = [dict(x) for x in rows]

        row = s.run(
            "MATCH (n) WITH count(n) AS nodes MATCH ()-[r]->() RETURN nodes, count(r) AS rels"
        ).single()
        out["counts"] = {"nodes": row["nodes"], "relationships": row["rels"]}
finally:
    driver.close()

p = Path(__file__).resolve().parent / "duplicate_edge_audit.json"
p.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps({
    "counts": out["counts"],
    "same_type_duplicates": len(out["same_type_duplicates"]),
    "parallel_semantic_pairs": len(out["parallel_semantic_pairs"]),
    "undirected_verbunden_gt2": len(out.get("undirected_verbunden_gt2", [])),
    "restado_rows": len(out["restado_neighborhood"]),
    "missing_evidence": len(out["bubble_missing_evidence"]),
}, indent=2))
