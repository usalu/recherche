import sys
sys.path.insert(0, r"E:/recherche/_scripts")
from neo4j_env import resolve_connection
from neo4j import GraphDatabase

uri, user, pw, db = resolve_connection()
print(f"uri={uri} user={user} db_resolved={db}")
drv = GraphDatabase.driver(uri, auth=(user, pw))
drv.verify_connectivity()
with drv.session(database="mit-bestand") as s:
    r = s.run("CALL db.info() YIELD name RETURN name").single()
    print("connected to db:", r["name"])
    r = s.run("MATCH (k:Wiederverwendungskette) RETURN count(k) AS c").single()
    print("chain count:", r["c"])
    r = s.run(
        "MATCH (k:Wiederverwendungskette) "
        "WHERE NOT (exists{(k)-[:AUS_BAUWERK]->()} AND exists{(k)-[:EINGEBAUT_IN]->()}) "
        "RETURN count(k) AS unwired"
    ).single()
    print("unwired count:", r["unwired"])
    r = s.run("RETURN apoc.version() AS v").single()
    print("apoc version:", r["v"])
drv.close()
