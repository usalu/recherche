"""Probe cross-bubble connectivity and isolation in mit-bestand."""
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
HUBS = [
    "madaster", "madaster_epea", "opalis", "Rotor", "rotordc", "concular",
    "cirkla", "useagain_bauteilclick", "insert_marketplace", "bellastock",
    "city_of_utrecht", "prog_preuse", "prog_fcrbe", "software_restado", "gruner_reuse_platform",
]

uri, u, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, pw))
out: dict = {"database": db, "hubs": {}, "cross_bubble_paths": [], "isolated_by_run": {}}
try:
    with driver.session(database=db) as s:
        for hid in HUBS:
            r = s.run(
                "MATCH (n {id: $id}) RETURN labels(n) AS l, n.name AS name",
                id=hid,
            ).single()
            if not r:
                out["hubs"][hid] = {"exists": False}
                continue
            runs = [
                x["run"]
                for x in s.run(
                    """
                    MATCH (n {id: $id})-[r]-()
                    WHERE r.review_run IS NOT NULL
                    RETURN DISTINCT r.review_run AS run
                    """,
                    id=hid,
                )
            ]
            neighbors = [
                dict(x)
                for x in s.run(
                    """
                    MATCH (n {id: $id})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
                    RETURN a.id AS id, collect(DISTINCT r.review_run) AS runs,
                           count(DISTINCT a) AS degree
                    ORDER BY a.id
                    """,
                    id=hid,
                )
            ]
            out["hubs"][hid] = {
                "exists": True,
                "labels": list(r["l"]),
                "name": r["name"],
                "bubble_runs": runs,
                "verbunden_neighbors": neighbors,
            }

        pairs = [
            ("madaster", "madaster_epea"),
            ("opalis", "bellastock"),
            ("Rotor", "rotordc"),
            ("Rotor", "opalis"),
            ("cirkla", "concular"),
            ("insert_marketplace", "madaster"),
            ("city_of_utrecht", "prog_preuse"),
            ("concular", "software_restado"),
            ("cirkla", "insert_marketplace"),
            ("opalis", "prog_preuse"),
        ]
        for a, b in pairs:
            row = s.run(
                """
                MATCH (x {id: $a}), (y {id: $b})
                OPTIONAL MATCH p = shortestPath((x)-[*..6]-(y))
                RETURN length(p) AS len, [n IN nodes(p) | n.id] AS path
                """,
                a=a,
                b=b,
            ).single()
            out["cross_bubble_paths"].append(
                {
                    "from": a,
                    "to": b,
                    "length": row["len"] if row else None,
                    "path": row["path"] if row else None,
                }
            )

        for run in RUNS:
            rows = s.run(
                """
                MATCH (a:Akteur)-[r]-()
                WHERE r.review_run = $run
                WITH a, count(DISTINCT r) AS deg
                WHERE deg <= 2
                RETURN a.id AS id, deg
                ORDER BY deg, id
                LIMIT 15
                """,
                run=run,
            )
            out["isolated_by_run"][run] = [dict(x) for x in rows]
finally:
    driver.close()

path = Path(__file__).resolve().parent / "cross_bubble_probe.json"
path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(path)
