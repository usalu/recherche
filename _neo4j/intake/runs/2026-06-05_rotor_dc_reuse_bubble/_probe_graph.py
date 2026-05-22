"""Probe live graph state for patch building."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

OUT = Path(__file__).resolve().parent / "graph_probe.json"
ids = [
    "Rotor", "rotordc", "opalis", "bellastock", "prog_fcrbe", "brussels_environment",
    "p_multi_brussels_reuse_in_multi", "p_architecture_of_reuse_brussels",
    "whitewood", "immobel", "bw_generale_de_banque_brussels", "city_of_utrecht",
    "prog_preuse", "p_oxy_centre_monnaie",
]
uri, u, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, pw))
out: dict = {"database": db, "nodes": {}, "rels": [], "generale_neighborhood": []}
try:
    with driver.session(database=db) as s:
        for nid in ids:
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
                   r.evidence_confidence AS conf, startNode(r).id AS start_id
            ORDER BY a.id, typ, to_id
            """,
            ids=ids,
        )
        out["rels"] = [dict(x) for x in rels]
        gm = s.run(
            """
            MATCH (bw:Bauwerk {id:'bw_generale_de_banque_brussels'})-[r]-(n)
            RETURN type(r) AS typ, startNode(r).id AS from_id, endNode(r).id AS to_id, r.id AS rid
            LIMIT 30
            """
        )
        out["generale_neighborhood"] = [dict(x) for x in gm]
        multi = s.run(
            """
            MATCH (p:Projekt {id:'p_multi_brussels_reuse_in_multi'})<-[r:BETEILIGT_AN]-(a)
            RETURN a.id AS actor, r.id AS rid, r.evidence_confidence AS conf, r.evidence AS ev
            """
        )
        out["multi_beteiligt"] = [dict(x) for x in multi]
finally:
    driver.close()
OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(OUT.read_text(encoding="utf-8"))
