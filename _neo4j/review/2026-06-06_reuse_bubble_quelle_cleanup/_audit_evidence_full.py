"""Full evidence property audit for bubble runs."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

RUNS = [
    "swiss_reuse_bubble_2026_06_05",
    "germany_reuse_bubble_2026_06_05",
    "france_reuse_bubble_2026_06_05",
    "netherlands_reuse_bubble_2026_06_05",
    "rotor_dc_reuse_bubble_2026_06_05",
]

uri, u, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, pw))
out: dict = {"database": db}
try:
    with driver.session(database=db) as s:
        rel_gaps = [
            dict(r)
            for r in s.run(
                """
                MATCH ()-[r]->()
                WHERE r.review_run IN $runs
                RETURN r.id AS id, type(r) AS typ, r.review_run AS run,
                       r.evidence_url IS NULL AS no_url,
                       r.evidence_quote IS NULL AS no_quote,
                       r.evidence_confidence IS NULL AS no_conf,
                       r.evidence_basis IS NULL AS no_basis,
                       r.evidence_source_id IS NOT NULL AS has_source_id,
                       r.metadata_sidecar_key IS NOT NULL AS has_sidecar
                """,
                runs=RUNS,
            )
            if r["no_url"] or r["no_quote"] or r["no_conf"] or r["no_basis"]
            or r["has_source_id"] or r["has_sidecar"]
        ]
        nodes_from_rels = [
            dict(r)
            for r in s.run(
                """
                MATCH (n)-[r]->()
                WHERE r.review_run IN $runs
                WITH DISTINCT n
                RETURN n.id AS id, labels(n) AS labels,
                       n.primary_source_url AS primary_source_url,
                       n.source_urls AS source_urls,
                       n.primary_source_url IS NULL AS no_primary,
                       n.source_urls IS NULL AS no_list
                ORDER BY n.id
                """
            )
        ]
        nodes_from_rels_in = [
            dict(r)
            for r in s.run(
                """
                MATCH ()-[r]->(n)
                WHERE r.review_run IN $runs
                WITH DISTINCT n
                RETURN n.id AS id, labels(n) AS labels,
                       n.primary_source_url AS primary_source_url,
                       n.source_urls AS source_urls
                ORDER BY n.id
                """
            )
        ]
        new_swiss = [
            dict(r)
            for r in s.run(
                """
                MATCH (n)
                WHERE n.id IN [
                  'software_planular','tool_swiss_inv','software_cirkla_scan',
                  'prog_swircular','prog_innosuisse_reuse_legal_framework_ch',
                  'c33_circular_construction_catalyst','circular_hub_zurich',
                  'circular_economy_switzerland','sumami','repurpose'
                ]
                RETURN n.id AS id, labels(n) AS labels,
                       n.primary_source_url AS primary_source_url, n.source_urls AS source_urls
                ORDER BY n.id
                """
            )
        ]
        out["rel_gaps"] = rel_gaps
        out["nodes_without_urls"] = [
            n for n in nodes_from_rels if n["no_primary"] and n["no_list"]
        ]
        out["nodes_partial_urls"] = [
            n for n in nodes_from_rels if not (n["no_primary"] and n["no_list"])
            and (n["no_primary"] or n["no_list"])
        ]
        out["new_or_bubble_nodes"] = new_swiss
        out["counts"] = {
            "bubble_rels": s.run(
                "MATCH ()-[r]->() WHERE r.review_run IN $runs RETURN count(r) AS c",
                runs=RUNS,
            ).single()["c"],
            "rel_gaps": len(rel_gaps),
            "nodes_without_urls": len(out["nodes_without_urls"]),
        }
finally:
    driver.close()

path = Path(__file__).resolve().parent / "evidence_full_audit.json"
path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(path)
print(json.dumps(out["counts"], indent=2))
if out["nodes_without_urls"]:
    print("no urls:", [n["id"] for n in out["nodes_without_urls"][:20]])
