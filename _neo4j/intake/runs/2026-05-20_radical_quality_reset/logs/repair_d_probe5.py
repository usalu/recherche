"""Probe 5 — confirm HAT_BAUTEILGRUPPE promotion candidates with current dossier wiring."""
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

# 1. How many (p)-[HAT_BAUTEILGRUPPE]->(bg) where bg has BOTH FROM_DONOR and INTO_RECEIVER?
out["hbg_with_full_topology"] = q(
    """
    MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
    WHERE exists{(bg)-[:FROM_DONOR]->()} AND exists{(bg)-[:INTO_RECEIVER]->()}
    RETURN count(r) AS c
    """
)[0]["c"]

# 2. Same, but also require p to have a case_markdown anchor (BELEGT_IN, any evidence_origin)
out["hbg_full_topology_with_md_anchor"] = q(
    """
    MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
    WHERE exists{(bg)-[:FROM_DONOR]->()}
      AND exists{(bg)-[:INTO_RECEIVER]->()}
      AND exists{(p)-[:BELEGT_IN]->(:Quelle {quelltyp:'case_markdown'})}
    RETURN count(r) AS c
    """
)[0]["c"]

# 3. Without md anchor requirement: how many distinct projects?
out["projects_with_full_topology_bg"] = q(
    """
    MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
    WHERE exists{(bg)-[:FROM_DONOR]->()} AND exists{(bg)-[:INTO_RECEIVER]->()}
    RETURN count(DISTINCT p) AS c
    """
)[0]["c"]

# 4. Counted by md anchor presence
out["projects_full_topology_by_md_anchor"] = q(
    """
    MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
    WHERE exists{(bg)-[:FROM_DONOR]->()} AND exists{(bg)-[:INTO_RECEIVER]->()}
    WITH DISTINCT p
    RETURN
      sum(CASE WHEN exists{(p)-[:BELEGT_IN]->(:Quelle {quelltyp:'case_markdown'})} THEN 1 ELSE 0 END) AS with_md_anchor,
      sum(CASE WHEN exists{(p)-[:BELEGT_IN]->(:Quelle {quelltyp:'case_markdown'})} THEN 0 ELSE 1 END) AS without_md_anchor
    """
)

# 5. Show sample of HBG without md anchor — to understand what alternatives we have
out["hbg_full_topology_without_md_anchor_sample"] = q(
    """
    MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
    WHERE exists{(bg)-[:FROM_DONOR]->()}
      AND exists{(bg)-[:INTO_RECEIVER]->()}
      AND NOT exists{(p)-[:BELEGT_IN]->(:Quelle {quelltyp:'case_markdown'})}
    OPTIONAL MATCH (p)-[bel:BELEGT_IN]->(qany:Quelle)
    RETURN p.id AS p_id, bg.id AS bg_id, collect(DISTINCT qany.id) AS belegt_quellen
    LIMIT 10
    """
)

# 6. For each project with full-topology BG: list canonical (single) case_markdown anchor id
out["project_md_anchor_map_sample"] = q(
    """
    MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
    WHERE exists{(bg)-[:FROM_DONOR]->()} AND exists{(bg)-[:INTO_RECEIVER]->()}
    OPTIONAL MATCH (p)-[:BELEGT_IN]->(qmd:Quelle {quelltyp:'case_markdown'})
    WITH p.id AS p_id, collect(DISTINCT qmd.id) AS qmd_ids
    RETURN p_id, qmd_ids, size(qmd_ids) AS n_anchors
    ORDER BY p_id
    """
)

# 7. Recount the master-sourced curated_no_excerpt explicitly per rel type
out["master_sourced_breakdown"] = q(
    """
    MATCH ()-[r]->()
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
      AND r.evidence_source_id='q_akteursliste_master_md'
    RETURN type(r) AS t, r.evidence_basis AS basis, count(*) AS c
    ORDER BY c DESC
    """
)

# 8. Actor S-ref bucket: confirm
out["actor_sref_curated_no_excerpt"] = q(
    """
    MATCH ()-[r:BELEGT_IN]->()
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
      AND r.evidence_source_id STARTS WITH 'q_actor_'
    RETURN count(r) AS c
    """
)[0]["c"]

# 9. Confirm the precise breakdown
out["total_curated_no_excerpt"] = q(
    """
    MATCH ()-[r]->()
    WHERE r.evidence_origin='curated'
      AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
    RETURN count(r) AS c
    """
)[0]["c"]

# 10. HAT_BAUTEILGRUPPE curated now
out["hat_bg_curated_now"] = q(
    """
    MATCH ()-[r:HAT_BAUTEILGRUPPE]->()
    WHERE r.evidence_origin='curated'
    RETURN count(r) AS c
    """
)[0]["c"]

print(json.dumps(out, indent=2, ensure_ascii=False, default=str))
(RUN_DIR / "logs/repair_d_probe5.json").write_text(
    json.dumps(out, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
)
driver.close()
