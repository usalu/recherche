"""Centrality analysis for Rotor DC reuse bubble vs live mit-bestand."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

OUT = Path(__file__).resolve().parent

CENTRAL_FROM_DOC = [
    "rotordc",
    "Rotor",
    "opalis",
    "bellastock",
    "prog_fcrbe",
    "p_multi_brussels_reuse_in_multi",
    "p_chiro_d_itterbeek_dilbeek",
]

uri, user, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(user, pw))
try:
    with driver.session(database=db) as s:
        report = {"seeds": {}, "rankings": {}, "gaps": []}

        # existence + verbunden degree
        for sid in CENTRAL_FROM_DOC + ["prog_preuse"]:
            row = s.run(
                """
                MATCH (n {id: $id})
                OPTIONAL MATCH (n)-[r:VERBUNDEN_MIT_AKTEUR]-(a)
                OPTIONAL MATCH (n)-[r2:BETEILIGT_AN]->(p)
                RETURN n.id AS id, labels(n) AS labels, n.name AS name,
                       count(DISTINCT a) AS verbunden_degree,
                       collect(DISTINCT a.id)[..20] AS verbunden_neighbors,
                       count(DISTINCT p) AS beteiligt_count,
                       collect(DISTINCT p.id)[..10] AS projects
                """,
                id=sid,
            ).single()
            report["seeds"][sid] = dict(row) if row and row["id"] else {"id": sid, "missing": True}

        # total rel counts for rotor stack
        for sid in ["rotordc", "Rotor", "opalis", "bellastock"]:
            rows = s.run(
                """
                MATCH (n {id: $id})-[r]-()
                RETURN type(r) AS typ, count(r) AS c
                ORDER BY c DESC LIMIT 15
                """,
                id=sid,
            )
            report["rankings"][sid] = [dict(x) for x in rows]

        # rotor stack internal mesh
        stack = s.run(
            """
            UNWIND ['rotordc','Rotor','opalis','bellastock','prog_fcrbe'] AS sid
            MATCH (n {id: sid})
            WITH collect(n) AS nodes
            UNWIND nodes AS a
            UNWIND nodes AS b
            WITH a, b WHERE elementId(a) < elementId(b)
            OPTIONAL MATCH (a)-[r]-(b)
            RETURN a.id AS from_id, b.id AS to_id, type(r) AS typ, r.id AS rid
            """
        )
        report["stack_edges"] = [dict(x) for x in stack if x["typ"]]

        # preuse in graph?
        preuse = s.run(
            """
            MATCH (n)
            WHERE toLower(n.id) CONTAINS 'preuse' OR toLower(coalesce(n.name,'')) CONTAINS 'preuse'
            RETURN n.id AS id, labels(n) AS labels, n.name AS name LIMIT 10
            """
        )
        report["preuse_nodes"] = [dict(x) for x in preuse]

        # opalis neighbors
        opalis_n = s.run(
            """
            MATCH (o:Akteur {id:'opalis'})-[r:VERBUNDEN_MIT_AKTEUR]-(a)
            RETURN a.id AS id, r.evidence_confidence AS conf
            ORDER BY a.id
            """
        )
        report["opalis_verbunden"] = [dict(x) for x in opalis_n]

        # rotordc-rotor link
        rr = s.run(
            """
            MATCH (d:Akteur {id:'rotordc'})-[r]-(v:Akteur {id:'Rotor'})
            RETURN type(r) AS typ, r.id AS rid, properties(r) AS props
            """
        )
        report["rotordc_rotor_links"] = [dict(x) for x in rr]

finally:
    driver.close()

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "centrality_report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))
