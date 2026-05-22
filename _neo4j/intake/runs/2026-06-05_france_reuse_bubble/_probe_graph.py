"""Probe live graph for France reuse bubble actors."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

OUT = Path(__file__).resolve().parent / "graph_probe.json"
SEEDS = [
    "bellastock", "Rotor", "rotordc", "opalis", "prog_fcrbe", "prog_preuse",
    "cycle_up", "backacia", "mobius_reemploi", "mineka", "raedificare", "reavie",
    "booster_du_reemploi", "a4mt", "ademe", "cstb", "qualiconsult",
    "maarten_gielen", "brussels_environment", "city_of_utrecht",
]
PROJECTS = [
    "p_actlab", "p_fabrique_du_clos", "p_maison_des_canaux", "p_pavillon_circulaire",
    "p_pavillon_keller", "prog_life_waste2build", "prog_repar", "prog_spirou",
]
uri, u, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, pw))
out: dict = {"database": db, "nodes": {}, "seed_rels": [], "bellastock_neighborhood": []}
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
        bn = s.run(
            """
            MATCH (b:Akteur {id:'bellastock'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
            RETURN collect(DISTINCT a.id) AS neighbors, count(DISTINCT a) AS degree
            """
        ).single()
        out["bellastock_verbunden"] = dict(bn) if bn else {}
        on = s.run(
            """
            MATCH (o:Akteur {id:'opalis'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
            RETURN collect(DISTINCT a.id) AS neighbors, count(DISTINCT a) AS degree
            """
        ).single()
        out["opalis_verbunden"] = dict(on) if on else {}
        fuzzy = s.run(
            """
            MATCH (n:Akteur)
            WHERE toLower(n.name) CONTAINS 'cycle'
               OR toLower(n.name) CONTAINS 'backacia'
               OR toLower(n.name) CONTAINS 'mobius'
               OR toLower(n.name) CONTAINS 'mineka'
               OR toLower(n.name) CONTAINS 'raedific'
               OR toLower(n.name) CONTAINS 'réavie'
               OR toLower(n.name) CONTAINS 'reavie'
               OR toLower(n.name) CONTAINS 'bellastock'
               OR n.id CONTAINS 'booster'
            RETURN n.id AS id, n.name AS name
            ORDER BY id LIMIT 30
            """
        )
        out["fuzzy_actors"] = [dict(x) for x in fuzzy]
finally:
    driver.close()
OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(OUT)
