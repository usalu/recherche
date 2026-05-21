"""Pass-2 Q4 supplementary — list the tier-1 actors with >=2 tier-1 projects.

Reported via BETEILIGT_AN (canonical) and ASSOZIIERT_MIT_PROJEKT for cross-check.
"""
from __future__ import annotations

import json
from pathlib import Path

from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "ENTWERFENMITBESTAND")
DB = "mit-bestand"

RUN_DIR = Path(r"E:/recherche/_neo4j/intake/runs/2026-05-20_radical_quality_reset")

driver = GraphDatabase.driver(URI, auth=AUTH)


def q(query, **params):
    with driver.session(database=DB, default_access_mode="READ") as s:
        return [dict(r) for r in s.run(query, **params)]


out = {}

out["via_BETEILIGT_AN"] = q(
    """
    MATCH (a:Akteur)-[:BETEILIGT_AN]->(p:Projekt {quality_tier:'tier_1_decision_grade'})
    WITH a, count(DISTINCT p) AS c, collect(DISTINCT p.id) AS project_ids
    WHERE c >= 2
    RETURN a.id AS actor_id,
           a.name AS actor_name,
           c AS tier1_project_count,
           project_ids
    ORDER BY tier1_project_count DESC, actor_id
    """
)

out["via_ASSOZIIERT_MIT_PROJEKT"] = q(
    """
    MATCH (a:Akteur)-[:ASSOZIIERT_MIT_PROJEKT]->(p:Projekt {quality_tier:'tier_1_decision_grade'})
    WITH a, count(DISTINCT p) AS c, collect(DISTINCT p.id) AS project_ids
    WHERE c >= 2
    RETURN a.id AS actor_id,
           a.name AS actor_name,
           c AS tier1_project_count,
           project_ids
    ORDER BY tier1_project_count DESC, actor_id
    """
)

out["union_any_edge"] = q(
    """
    MATCH (a:Akteur)-[:BETEILIGT_AN|ASSOZIIERT_MIT_PROJEKT|HAT_AKTEURROLLE]-(p:Projekt {quality_tier:'tier_1_decision_grade'})
    WITH a, count(DISTINCT p) AS c, collect(DISTINCT p.id) AS project_ids
    WHERE c >= 2
    RETURN a.id AS actor_id,
           a.name AS actor_name,
           c AS tier1_project_count,
           project_ids
    ORDER BY tier1_project_count DESC, actor_id
    """
)

print(json.dumps(out, indent=2, ensure_ascii=False, default=str))
(RUN_DIR / "logs/pass2_q4_actor_list.json").write_text(
    json.dumps(out, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
)
driver.close()
