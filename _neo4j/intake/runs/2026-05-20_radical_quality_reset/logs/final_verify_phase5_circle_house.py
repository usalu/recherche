"""Diagnostic: why is p_circle_house tier_2, not tier_3?"""
import json
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "ENTWERFENMITBESTAND"))

def q(cy, **p):
    with driver.session(database="mit-bestand", default_access_mode="READ") as s:
        return [dict(r) for r in s.run(cy, **p)]

print(json.dumps(q(
    """
    MATCH (p:Projekt {id:'p_circle_house'})
    RETURN p.quality_tier AS tier,
           p.quality_tier_n_bg AS n_bg,
           p.quality_tier_n_bg_quantified AS n_bg_q,
           p.quality_tier_n_curated_evidence AS n_curated,
           p.quality_tier_has_year AS has_year,
           p.quality_tier_has_land AS has_land,
           p.quality_tier_has_components AS has_components,
           p.quality_tier_has_metric AS has_metric,
           p.quality_tier_has_evidence AS has_evidence,
           p.year_completed AS year_completed,
           p.jahr_fertigstellung AS jahr,
           p.import_status AS import_status
    """
), indent=2, ensure_ascii=False, default=str))

print(json.dumps(q(
    """
    MATCH (p:Projekt {quality_tier:'tier_3_stub'})
    RETURN p.id AS id ORDER BY id
    """
), indent=2, ensure_ascii=False, default=str))

driver.close()
