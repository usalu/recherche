import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

HUBS = ["madaster","madaster_epea","opalis","Rotor","rotordc","concular","cirkla","insert_marketplace","bellastock","city_of_utrecht","restado","kunst_stoffe_ev","material_mafia","haus_der_materialisierung","useagain_bauteilclick","new_horizon_urban_mining"]
uri,u,pw,db=resolve_connection()
d=GraphDatabase.driver(uri,auth=(u,pw))
out={}
with d.session(database=db) as s:
    for hid in HUBS:
        r=s.run("MATCH (n {id:$id}) RETURN labels(n) AS l, n.name AS name, n.primary_source_url AS url", id=hid).single()
        if not r:
            out[hid]={"exists":False}; continue
        deg=s.run("MATCH (n {id:$id})-[r:VERBUNDEN_MIT_AKTEUR]-(a) RETURN count(DISTINCT a) AS c", id=hid).single()["c"]
        runs=[x["run"] for x in s.run("MATCH (n {id:$id})-[r]-() WHERE r.review_run IS NOT NULL RETURN DISTINCT r.review_run AS run", id=hid)]
        out[hid]={"exists":True,"labels":list(r["l"]),"name":r["name"],"url":r["url"],"verbunden_degree":deg,"bubble_runs":runs}
    pairs=[("insert_marketplace","madaster"),("concular","restado"),("concular","madaster_epea"),("Rotor","opalis"),("bellastock","opalis"),("madaster","madaster_epea"),("kunst_stoffe_ev","haus_der_materialisierung"),("useagain_bauteilclick","restado")]
    out["paths"]=[]
    for a,b in pairs:
        row=s.run("MATCH (x {id:$a}),(y {id:$b}) OPTIONAL MATCH p=shortestPath((x)-[*..8]-(y)) RETURN length(p) AS len, [n IN nodes(p)|n.id] AS path", a=a,b=b).single()
        out["paths"].append({"from":a,"to":b,"len":row["len"] if row else None,"path":row["path"] if row else None})
d.close()
p=Path(__file__).resolve().parent/"hub_probe.json"
p.write_text(json.dumps(out,indent=2),encoding="utf-8")
print(p)
