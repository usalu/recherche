from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

IDS = [
    "baubuero_in_situ","brussels_environment","city_of_utrecht","eth_zuerich",
    "immobel","madaster_epea","whitewood","zirkular",
]
RUNS = [
    "swiss_reuse_bubble_2026_06_05","germany_reuse_bubble_2026_06_05",
    "france_reuse_bubble_2026_06_05","netherlands_reuse_bubble_2026_06_05",
    "rotor_dc_reuse_bubble_2026_06_05",
]
uri, u, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, pw))
with driver.session(database=db) as s:
    for nid in IDS:
        rows = list(s.run(
            """
            MATCH (n {id:$id})-[r]-()
            WHERE r.review_run IN $runs AND r.evidence_url IS NOT NULL
            RETURN DISTINCT r.evidence_url AS url, type(r) AS typ
            ORDER BY url
            """,
            id=nid, runs=RUNS,
        ))
        print(nid, [dict(r) for r in rows])
driver.close()
