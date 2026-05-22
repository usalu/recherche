"""Probe live graph for Netherlands reuse bubble actors."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

OUT = Path(__file__).resolve().parent / "graph_probe.json"
SEEDS = [
    "superuse_studios_2012architecten",
    "superuse_on_site",
    "new_horizon_urban_mining",
    "new_horizon",
    "madaster",
    "madaster_epea",
    "madaster_context",
    "insert_marketplace",
    "repurpose",
    "madopt",
    "cirkelstad",
    "platform_cb23",
    "city_of_utrecht",
    "Rotor",
    "rotordc",
    "opalis",
    "bellastock",
    "prog_fcrbe",
    "prog_preuse",
    "concular",
]
PROJECTS = [
    "p_villa_welpeloo",
    "p_wikado",
    "p_bluecity_offices",
    "p_buitenplaats_brienenoord",
    "p_de_ceuvel",
    "p_circl",
    "p_peoples_pavilion",
    "p_biopartner_5",
]
uri, u, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, pw))
out: dict = {"database": db, "nodes": {}, "seed_rels": []}
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
        for hub, q in [
            ("superuse_studios_2012architecten", "superuse"),
            ("new_horizon_urban_mining", "new_horizon"),
            ("madaster", "madaster"),
            ("insert_marketplace", "insert"),
        ]:
            row = s.run(
                f"""
                MATCH (h:Akteur {{id: $id}})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
                RETURN collect(DISTINCT a.id) AS neighbors, count(DISTINCT a) AS degree
                """,
                id=hub,
            ).single()
            out[f"{q}_verbunden"] = dict(row) if row else {}
        fuzzy = s.run(
            """
            MATCH (n:Akteur)
            WHERE toLower(n.name) CONTAINS 'superuse'
               OR toLower(n.name) CONTAINS 'horizon'
               OR toLower(n.name) CONTAINS 'madaster'
               OR toLower(n.name) CONTAINS 'insert'
               OR toLower(n.name) CONTAINS 'madopt'
               OR toLower(n.name) CONTAINS 'repurpose'
               OR toLower(n.name) CONTAINS 'cirkel'
               OR n.id CONTAINS 'oogst'
            RETURN n.id AS id, n.name AS name
            ORDER BY id LIMIT 40
            """
        )
        out["fuzzy_actors"] = [dict(x) for x in fuzzy]
finally:
    driver.close()
OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(OUT)
