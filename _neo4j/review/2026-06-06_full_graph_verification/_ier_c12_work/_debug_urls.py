import sys
sys.path.insert(0, r"e:\recherche\_neo4j\review\2026-06-06_full_graph_verification\_ier_c12_work")
import build_ier_c12 as m
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

scope = m.load_scope()[:1]
row = scope[0]
aid = row["element_id"]
uri, u, p, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, p))
live = m.query_actors(driver, db, [aid])
driver.close()
actor = live[aid]
actor["asserted_claim"] = row.get("asserted_claim", "")
cands = []
for q in (f'"{actor["name"]}" official site',):
    cands += [(u, "ddg") for u in m.ddg_search(q, {}, 4)]
cands += [(u, "guess") for u in m.guess_domains(aid, actor["name"], None)]
for u, s in cands[:20]:
    print(s, m.is_valid_http_url(u), u[:120])
