import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

uri, user, password, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(user, password))
with driver.session(database=db) as s:
    out = {
        "nodes": s.run("MATCH (n) RETURN count(n) AS c").single()["c"],
        "rels": s.run("MATCH ()-[x]->() RETURN count(x) AS c").single()["c"],
        "mineka": (s.run("MATCH (a:Akteur {id:'mineka'}) RETURN a.id AS id").single() or {}).get("id"),
        "france_bubble_rels": s.run(
            "MATCH ()-[x]->() WHERE x.review_run = 'france_reuse_bubble_2026_06_05' RETURN count(x) AS c"
        ).single()["c"],
        "opalis_reavie": s.run(
            "MATCH (o:Akteur {id:'opalis'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur {id:'association_reavie'}) RETURN count(r) AS c"
        ).single()["c"],
    }
print(json.dumps(out, indent=2))
driver.close()
