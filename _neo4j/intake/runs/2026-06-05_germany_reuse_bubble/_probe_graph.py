"""Probe live graph for Germany reuse bubble actors."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

OUT = Path(__file__).resolve().parent / "graph_probe.json"
SEEDS = [
    "concular", "restado", "circular_structural_design", "haus_der_materialisierung",
    "material_mafia", "bauteilboerse_bremen", "bauteilboerse_hannover", "circular_berlin",
    "madaster", "madaster_epea", "madaster_context", "dgnb", "resource_stiftung",
    "software_concular", "software_restado", "tool_rcmi", "dominik_campanella",
    "p_multi_brussels_reuse_in_multi", "p_thoravej_29_copenhagen",
    "prog_din_spec_91484", "prog_din_spec_91525", "tool_urban_mining_index",
]
PROJECTS = [
    "p_berlin_txl", "p_rathaus_korbach", "p_crclr_house_berlin", "p_ice_city_erfurt",
    "p_leipzig_airport_modular", "p_forum_koenigsbrunn", "p_huthmacher_haus_berlin",
    "p_heidelberg_circular_city", "p_mint_zentrum_bensheim",
]
uri, u, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, pw))
out: dict = {"database": db, "nodes": {}, "seed_rels": [], "concular_neighborhood": []}
try:
    with driver.session(database=db) as s:
        for nid in SEEDS + PROJECTS:
            r = s.run(
                "MATCH (n {id: $id}) RETURN labels(n) AS l, n.name AS name",
                id=nid,
            ).single()
            out["nodes"][nid] = {
                "exists": r is not None,
                "labels": list(r["l"]) if r else None,
                "name": r["name"] if r else None,
            }
        rels = s.run(
            """
            MATCH (a)-[r]-(b)
            WHERE a.id IN $ids AND b.id IN $ids
            RETURN a.id AS from_id, type(r) AS typ, b.id AS to_id, r.id AS rid,
                   r.evidence_confidence AS conf
            ORDER BY a.id, typ, to_id
            """,
            ids=SEEDS,
        )
        out["seed_rels"] = [dict(x) for x in rels]
        cn = s.run(
            """
            MATCH (c:Akteur {id:'concular'})-[r]-(n)
            RETURN type(r) AS typ, startNode(r).id AS from_id, endNode(r).id AS to_id,
                   labels(startNode(r)) AS fl, labels(endNode(r)) AS tl, r.id AS rid
            LIMIT 40
            """
        )
        out["concular_neighborhood"] = [dict(x) for x in cn]
        # fuzzy search for germany actors by name
        fuzzy = s.run(
            """
            MATCH (n:Akteur)
            WHERE toLower(n.name) CONTAINS 'concular'
               OR toLower(n.name) CONTAINS 'restado'
               OR toLower(n.name) CONTAINS 'materialisierung'
               OR toLower(n.name) CONTAINS 'bauteilbörse'
               OR toLower(n.name) CONTAINS 'bauteilboerse'
               OR n.id CONTAINS 'haus_der_material'
               OR n.id CONTAINS 'circular_berlin'
               OR n.id CONTAINS 'resource'
            RETURN n.id AS id, n.name AS name, labels(n) AS labels
            ORDER BY id LIMIT 30
            """
        )
        out["fuzzy_actors"] = [dict(x) for x in fuzzy]
finally:
    driver.close()
OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(OUT.read_text(encoding="utf-8"))
