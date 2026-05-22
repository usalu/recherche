"""Review Swiss phase1 edges currently in mit-bestand."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

RUN = "swiss_reuse_bubble_2026_06_05"
PHASE1_IDS = [
    "r_cirkla__belegt_in__q_url_0f6a8243ac5d1567100a3117bc4594e6",
    "r_cirkla__belegt_in__q_actor_benjamin_poignon_03",
    "r_cirkla__belegt_in__q_url_72047630eba27e60c1f672463457463e",
    "r_cirkla__belegt_in__q_url_83aa2d2f1524132cce8dcbac4e8fb774",
    "r_cirkla__verbunden_mit_akteur__useagain_bauteilclick",
    "r_useagain_bauteilclick__verbunden_mit_akteur__cirkla",
    "r_cirkla__verbunden_mit_akteur__materiuum",
    "r_materiuum__verbunden_mit_akteur__cirkla",
    "r_cirkla__verbunden_mit_akteur__wick_reuse_roto_baumarkt",
    "r_wick_reuse_roto_baumarkt__verbunden_mit_akteur__cirkla",
    "r_cirkla__verbunden_mit_akteur__bauteilladen_winterthur",
    "r_bauteilladen_winterthur__verbunden_mit_akteur__cirkla",
    "r_cirkla__verbunden_mit_akteur__reuzi_ch",
    "r_reuzi_ch__verbunden_mit_akteur__cirkla",
    "r_cirkla__verbunden_mit_akteur__gruner_reuse_platform",
    "r_gruner_reuse_platform__verbunden_mit_akteur__cirkla",
    "r_cirkla__verbunden_mit_akteur__baubuero_in_situ",
    "r_baubuero_in_situ__verbunden_mit_akteur__cirkla",
    "r_cirkla__verbunden_mit_akteur__salza",
    "r_salza__verbunden_mit_akteur__cirkla",
    "r_cirkla__verbunden_mit_akteur__zirkular",
    "r_zirkular__verbunden_mit_akteur__cirkla",
    "r_baubuero_in_situ__beteiligt_an__p_k118_kopfbau_halle_118_winterthur",
    "r_zirkular__beteiligt_an__p_k118_kopfbau_halle_118_winterthur",
    "r_zirkular__beteiligt_an__p_elys_kultur_gewerbehaus_basel",
    "r_madaster__belegt_in__q_url_c19e3aef6ee77ca6de0e75bf46654fb0",
    "r_useagain_bauteilclick__belegt_in__q_url_82ad61e4b3672c05a8fedf46e57faee6",
    "r_useagain_bauteilclick__belegt_in__q_url_9fce1894aaa7455c757369850397e39f",
    "r_salza__belegt_in__q_url_45d7c6380377a9cec952dbf6c3f2ba8c",
    "r_materiuum__belegt_in__q_url_56649f37d5b1ee18d083da852797c756",
    "r_bauteilladen_winterthur__belegt_in__q_url_48e67450f81ae55a6012813987faf31e",
    "r_wick_reuse_roto_baumarkt__belegt_in__q_url_161aca331467d6b5bd144e83b6837af4",
]

uri, u, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, pw))
out: dict = {"database": db, "review_run": RUN, "phase1_edges": [], "summary": {}}
try:
    with driver.session(database=db) as s:
        for rid in PHASE1_IDS:
            row = s.run(
                """
                MATCH ()-[r]->()
                WHERE r.id = $id
                RETURN r.id AS id, type(r) AS typ, startNode(r).id AS from_id,
                       endNode(r).id AS to_id, r.evidence_confidence AS conf,
                       r.review_run AS review_run, r.connection_kind AS kind
                """,
                id=rid,
            ).single()
            out["phase1_edges"].append(
                {"id": rid, "exists": row is not None, **(dict(row) if row else {})}
            )
        cirkla = s.run(
            """
            MATCH (c:Akteur {id:'cirkla'})-[r:VERBUNDEN_MIT_AKTEUR]-(n:Akteur)
            WHERE r.review_run = $run
            RETURN collect(DISTINCT n.id) AS neighbors, count(DISTINCT n) AS degree
            """,
            run=RUN,
        ).single()
        phase1_count = s.run(
            """
            MATCH ()-[r]->()
            WHERE r.id IN $ids
            RETURN count(r) AS c
            """,
            ids=PHASE1_IDS,
        ).single()["c"]
        bubble_count = s.run(
            """
            MATCH ()-[r]->()
            WHERE r.review_run = $run
            RETURN count(r) AS c
            """,
            run=RUN,
        ).single()["c"]
        stub = s.run(
            """
            MATCH ()-[r:ASSOZIIERT_MIT_PROJEKT]->()
            WHERE r.id IN [
              'r_zirkular__assoziiert_mit_projekt__p_k118_kopfbau_halle_118_winterthur',
              'r_zirkular__assoziiert_mit_projekt__p_elys_kultur_gewerbehaus_basel'
            ]
            RETURN count(r) AS c
            """
        ).single()["c"]
        out["summary"] = {
            "phase1_edges_present": phase1_count,
            "phase1_edges_expected": len(PHASE1_IDS),
            "bubble_edges_total": bubble_count,
            "cirkla_verbunden_neighbors": list(cirkla["neighbors"]),
            "cirkla_verbunden_degree": cirkla["degree"],
            "stub_assoziiert_remaining": stub,
        }
finally:
    driver.close()

out_path = Path(__file__).resolve().parent / "phase1_live_review.json"
out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(out_path)
print(json.dumps(out["summary"], indent=2))
