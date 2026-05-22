import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

TARGETS = [
    "sumami", "eth_zuerich", "c33_circular_construction_catalyst", "circular_hub_zurich",
    "circular_economy_switzerland", "useagain_bauteilclick", "wick_reuse_roto_baumarkt",
    "city_of_utrecht", "immobel", "whitewood", "brussels_environment",
    "new_horizon_urban_mining", "superuse_studios_2012architecten", "repurpose",
    "kunst_stoffe_ev", "circular_structural_design",
]

uri,u,pw,db=resolve_connection()
d=GraphDatabase.driver(uri,auth=(u,pw))
out={}
with d.session(database=db) as s:
    for tid in TARGETS:
        r=s.run("MATCH (n {id:$id}) RETURN labels(n) AS l, n.name AS name, n.primary_source_url AS url", id=tid).single()
        if not r:
            out[tid]={"exists":False}; continue
        rels=[dict(x) for x in s.run("""
            MATCH (n {id:$id})-[r]-(m)
            RETURN type(r) AS t, m.id AS other, r.evidence_confidence AS conf, r.review_run AS run
            ORDER BY t, other LIMIT 20
        """, id=tid)]
        out[tid]={"exists":True,"labels":list(r["l"]),"name":r["name"],"url":r["url"],"rels":rels}
d.close()
p=Path(__file__).resolve().parent/"isolated_probe.json"
p.write_text(json.dumps(out,indent=2),encoding="utf-8")
print(p)
