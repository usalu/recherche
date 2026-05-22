import sys, json
sys.path.insert(0, r'e:\recherche\_scripts')
from neo4j import GraphDatabase
from neo4j_env import resolve_connection
uri, u, p, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, p))
out = {}
with driver.session(database=db) as s:
    for aid in ['cycle_up', 'backacia', 'mobius_reemploi', 'raedificare', 'association_reavie', 'bellastock']:
        rows = s.run(
            """
            MATCH (a {id: $id})-[r]-(n)
            RETURN type(r) AS typ, n.id AS nid
            ORDER BY typ, nid
            """,
            id=aid,
        ).data()
        out[aid] = rows
driver.close()
print(json.dumps(out, indent=2))
