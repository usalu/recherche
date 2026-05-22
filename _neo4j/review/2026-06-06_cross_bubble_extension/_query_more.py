import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

QUERIES = {
    "utrecht-insert": "MATCH (a {id:'city_of_utrecht'})-[r]-(b {id:'insert_marketplace'}) RETURN type(r) AS t, r.evidence_confidence AS c",
    "utrecht-madaster": "MATCH (a {id:'city_of_utrecht'})-[r:VERBUNDEN_MIT_AKTEUR]-(b {id:'madaster'}) RETURN r.evidence_confidence AS c",
    "opalis-preuse": "MATCH (a {id:'opalis'})-[r]-(b {id:'prog_preuse'}) RETURN type(r) AS t",
    "concular-software_restado": "MATCH (a {id:'concular'})-[r]-(b {id:'software_restado'}) RETURN type(r) AS t, properties(r) AS p",
    "shortest cirkla-opalis": "MATCH (a {id:'cirkla'}),(b {id:'opalis'}) OPTIONAL MATCH p=shortestPath((a)-[*..8]-(b)) RETURN length(p) AS len, [n IN nodes(p)|n.id] AS path",
    "shortest madaster-opalis": "MATCH (a {id:'madaster'}),(b {id:'opalis'}) OPTIONAL MATCH p=shortestPath((a)-[*..8]-(b)) RETURN length(p) AS len, [n IN nodes(p)|n.id] AS path",
    "shortest cirkla-madaster": "MATCH (a {id:'cirkla'}),(b {id:'madaster'}) OPTIONAL MATCH p=shortestPath((a)-[*..8]-(b)) RETURN length(p) AS len, [n IN nodes(p)|n.id] AS path",
    "graph totals": "MATCH (n) WITH count(n) AS nodes MATCH ()-[r]->() RETURN nodes, count(r) AS rels",
}

uri,u,pw,db=resolve_connection()
d=GraphDatabase.driver(uri,auth=(u,pw))
out={}
with d.session(database=db) as s:
    for k,q in QUERIES.items():
        out[k]=[dict(x) for x in s.run(q)]
d.close()
print(json.dumps(out,indent=2))
