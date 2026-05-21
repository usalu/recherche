"""Probe 7 — examine the structure of array-valued (dedup-merged) edges."""
from __future__ import annotations
import json, sys
from pathlib import Path
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "ENTWERFENMITBESTAND")
DB = "mit-bestand"
RUN_DIR = Path(r"E:/recherche/_neo4j/intake/runs/2026-05-20_radical_quality_reset")
driver = GraphDatabase.driver(URI, auth=AUTH)
sys.stdout.reconfigure(encoding="utf-8")


def q(query, **params):
    with driver.session(database=DB, default_access_mode="READ") as s:
        return [dict(r) for r in s.run(query, **params)]


out: dict = {}

# Edges where evidence_origin is a list (size > 1 implies list of size > 1)
out["array_origin_edges_count"] = q(
    """
    MATCH ()-[r]->()
    WHERE r.evidence_origin IS NOT NULL
      AND NOT r.evidence_origin IN ['curated','inferred','derived']
    RETURN count(r) AS c
    """
)
out["array_origin_edges_count_size"] = q(
    """
    MATCH ()-[r]->()
    WHERE r.evidence_origin IS NOT NULL
      AND size(r.evidence_origin) > 1
    RETURN count(r) AS c
    """
)

# Sample with detailed property breakdown
out["array_edge_samples_full"] = q(
    """
    MATCH (a)-[r]->(b)
    WHERE r.evidence_origin IS NOT NULL
      AND size(r.evidence_origin) > 1
    RETURN type(r) AS t, labels(a) AS a_labels, a.id AS a_id,
           labels(b) AS b_labels, b.id AS b_id,
           properties(r) AS props
    LIMIT 25
    """
)

# Group by rel type
out["array_edges_by_type"] = q(
    """
    MATCH ()-[r]->()
    WHERE r.evidence_origin IS NOT NULL
      AND size(r.evidence_origin) > 1
    RETURN type(r) AS t, count(*) AS c
    ORDER BY c DESC
    """
)

# Skip APOC-only diagnostic (we have the samples to enumerate keys manually)

# Find BELEGT_IN with basis='research_file_row'
out["belegt_in_research_basis_total"] = q(
    """
    MATCH ()-[r:BELEGT_IN]->()
    WHERE r.evidence_basis='research_file_row'
    RETURN count(r) AS c
    """
)[0]["c"]
out["belegt_in_research_basis_by_origin"] = q(
    """
    MATCH ()-[r:BELEGT_IN]->()
    WHERE r.evidence_basis='research_file_row'
    RETURN r.evidence_origin AS origin, r.evidence_confidence AS conf, count(*) AS c
    ORDER BY c DESC
    """
)

# Find ASSOZIIERT_MIT_PROJEKT going to Programm specifically
out["assoz_to_programm"] = q(
    """
    MATCH (a)-[r:ASSOZIIERT_MIT_PROJEKT]->(b:Programm)
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
    RETURN count(r) AS c
    """
)[0]["c"]

# Pre-migration: were these edges array-typed before? Check if any LIST_origin edge is NOT curated_no_excerpt
out["list_origin_curated_no_excerpt"] = q(
    """
    MATCH ()-[r]->()
    WHERE size(coalesce(r.evidence_origin,[])) > 1
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
    RETURN count(r) AS c
    """
)[0]["c"]

print(json.dumps(out, indent=2, ensure_ascii=False, default=str))
(RUN_DIR / "logs/repair_d_probe7.json").write_text(
    json.dumps(out, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
)
driver.close()
