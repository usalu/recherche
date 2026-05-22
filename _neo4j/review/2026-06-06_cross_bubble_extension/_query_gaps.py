import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

CHECKS = [
    ("software_restado exists", "MATCH (n {id:'software_restado'}) RETURN n.name AS name, n.primary_source_url AS url"),
    ("concular-restado rel", "MATCH (a {id:'concular'})-[r]-(b {id:'software_restado'}) RETURN type(r) AS t, r.evidence_confidence AS conf, r.review_run AS run"),
    ("madaster-insert rel", "MATCH (a {id:'madaster'})-[r:VERBUNDEN_MIT_AKTEUR]-(b {id:'insert_marketplace'}) RETURN r.evidence_confidence AS conf, r.evidence_url AS url"),
    ("madaster-madaster_epea direct", "MATCH (a {id:'madaster'})-[r:VERBUNDEN_MIT_AKTEUR]-(b {id:'madaster_epea'}) RETURN count(r) AS c"),
    ("useagain-cirkla", "MATCH (a {id:'useagain_bauteilclick'})-[r]-(b {id:'cirkla'}) RETURN type(r) AS t, r.evidence_confidence AS conf LIMIT 5"),
    ("software_restado-opalis path", "MATCH (a {id:'software_restado'}),(b {id:'opalis'}) OPTIONAL MATCH p=shortestPath((a)-[*..6]-(b)) RETURN length(p) AS len"),
    ("bubble component count", """
        MATCH (n)-[r]-()
        WHERE r.review_run IN $runs
        WITH r.review_run AS run, count(DISTINCT n) AS nodes
        RETURN run, nodes ORDER BY run
    """),
]

uri,u,pw,db=resolve_connection()
d=GraphDatabase.driver(uri,auth=(u,pw))
out={}
with d.session(database=db) as s:
    for label, q in CHECKS:
        params={"runs":["swiss_reuse_bubble_2026_06_05","germany_reuse_bubble_2026_06_05","france_reuse_bubble_2026_06_05","netherlands_reuse_bubble_2026_06_05","rotor_dc_reuse_bubble_2026_06_05"]}
        rows=[dict(x) for x in s.run(q, **{k:v for k,v in params.items() if k in q})]
        out[label]=rows
d.close()
p=Path(__file__).resolve().parent/"gap_query.json"
p.write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out,indent=2))
