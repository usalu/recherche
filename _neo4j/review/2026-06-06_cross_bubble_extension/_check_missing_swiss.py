import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

PAIRS = [
    ("cirkla","wick_reuse_roto_baumarkt"),
    ("cirkla","useagain_bauteilclick"),
    ("sumami","cirkla"),
    ("sumami","eth_zuerich"),
    ("sumami","prog_swircular"),
    ("circular_hub_zurich","sumami"),
    ("madaster","sumami"),
    ("rotordc","whitewood"),
    ("rotordc","immobel"),
    ("kunst_stoffe_ev","material_mafia"),
    ("kunst_stoffe_ev","circular_berlin"),
    ("city_of_utrecht","insert_marketplace"),
]

uri,u,pw,db=resolve_connection()
d=GraphDatabase.driver(uri,auth=(u,pw))
out=[]
with d.session(database=db) as s:
    for a,b in PAIRS:
        c=s.run("MATCH (x {id:$a})-[r]-(y {id:$b}) RETURN count(r) AS c, collect(DISTINCT type(r)) AS types",a=a,b=b).single()["c"]
        out.append({"pair":f"{a}↔{b}","count":c})
d.close()
print(json.dumps(out,indent=2))
