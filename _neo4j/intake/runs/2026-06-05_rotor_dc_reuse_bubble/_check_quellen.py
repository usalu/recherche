import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

ids = [
    "q_url_150bfa71ec64ea9192c5252bb7453284",
    "q_url_4a94cddf6628f350b982c97040dce9fd",
    "q_url_714d4c31c9d811b5269f20eaf16bb43f",
    "q_chiro_d_itterbeek_dilbeek_s5",
    "q_multi_brussels_reuse_in_multi_s5",
]
uri, u, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, pw))
with driver.session(database=db) as s:
    for i in ids:
        r = s.run("MATCH (n {id: $id}) RETURN n.id AS id", id=i).single()
        print(i, "OK" if r else "MISSING")
driver.close()
