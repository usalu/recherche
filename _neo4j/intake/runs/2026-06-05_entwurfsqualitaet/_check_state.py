import sys
from pathlib import Path
sys.path.insert(0, str(Path(r"e:\recherche\_scripts")))
from neo4j_env import resolve_connection
from neo4j import GraphDatabase
uri,user,pw,db=resolve_connection()
d=GraphDatabase.driver(uri,auth=(user,pw))
with d.session(database=db) as s:
    print("nodes", s.run("MATCH (n) RETURN count(n)").single()[0])
    print("em active", s.run("MATCH (em:Entwurfsmethodik) WHERE NOT em:DEPRECATED RETURN count(em)").single()[0])
    print("em v2", s.run("MATCH (em:Entwurfsmethodik) WHERE em.vokabular_version = $v RETURN count(em)", v="v2").single()[0])
    for r in s.run("MATCH (em:Entwurfsmethodik) RETURN em.id AS id, em.name AS name, em.vokabular_version AS v ORDER BY id"):
        print(dict(r))
    print("edges em", s.run("MATCH ()-[r:HAT_ENTWURFSMETHODIK]->() RETURN count(r)").single()[0])
    row=s.run("MATCH (em:Entwurfsmethodik {id: $id}) RETURN em.beschreibung AS b", id="em_design_with_stock").single()
    b=row["b"] if row else None
    print("sample beschreibung", (b[:80]+"...") if b else None)
d.close()
