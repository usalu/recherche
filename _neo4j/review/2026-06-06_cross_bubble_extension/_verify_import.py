import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

CHECKS = [
    ("phase1", "MATCH (a {id:'madaster'})-[r:VERBUNDEN_MIT_AKTEUR]-(b {id:'madaster_epea'}) RETURN r.evidence_confidence AS c"),
    ("phase1", "MATCH (a {id:'opalis'})-[r:BETEILIGT_AN]->(b {id:'prog_preuse'}) RETURN r.evidence_confidence AS c"),
    ("phase2", "MATCH (a {id:'sumami'})-[r:VERBUNDEN_MIT_AKTEUR]-(b {id:'cirkla'}) RETURN r.evidence_confidence AS c"),
    ("phase2", "MATCH (a {id:'useagain_bauteilclick'})-[r:VERBUNDEN_MIT_AKTEUR]-(b {id:'software_restado'}) RETURN r.evidence_confidence AS c"),
    ("totals", "MATCH (n) WITH count(n) AS nodes MATCH ()-[r]->() RETURN nodes, count(r) AS rels"),
]

uri,u,pw,db=resolve_connection()
d=GraphDatabase.driver(uri,auth=(u,pw))
out={}
with d.session(database=db) as s:
    for phase,q in CHECKS:
        rows=[dict(x) for x in s.run(q)]
        out.setdefault(phase,[]).extend(rows)
d.close()
print(json.dumps(out,indent=2))
