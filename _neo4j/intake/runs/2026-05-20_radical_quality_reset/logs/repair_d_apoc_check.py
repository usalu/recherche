from neo4j import GraphDatabase
d = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "ENTWERFENMITBESTAND"))
with d.session(database="mit-bestand", default_access_mode="READ") as s:
    rows = list(s.run("SHOW PROCEDURES YIELD name WHERE name STARTS WITH 'apoc' RETURN count(name) AS c"))
    print("APOC procedures count:", rows[0]["c"] if rows else 0)
    rows = list(s.run("SHOW FUNCTIONS YIELD name WHERE name STARTS WITH 'apoc' RETURN name ORDER BY name LIMIT 100"))
    print("Sample APOC functions:")
    for r in rows:
        print(" ", r["name"])
d.close()
