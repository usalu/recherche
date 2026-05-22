from __future__ import annotations
import json, sys
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
uri, u, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, pw))
with driver.session(database=db) as s:
    rows = list(s.run(
        """
        MATCH (n)-[r]->()
        WHERE r.review_run IN $runs
        WITH DISTINCT n
        WHERE n.primary_source_url IS NULL AND n.source_urls IS NULL
        RETURN n.id AS id, labels(n) AS labels, n.name AS name
        ORDER BY n.id
        """,
        runs=RUNS,
    ))
driver.close()
print(json.dumps([dict(r) for r in rows], indent=2))
