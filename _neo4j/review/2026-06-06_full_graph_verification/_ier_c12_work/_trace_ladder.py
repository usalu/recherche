import sys
sys.path.insert(0, r"e:\recherche\_neo4j\review\2026-06-06_full_graph_verification\_ier_c12_work")
import build_ier_c12 as m
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

scope = m.load_scope()
row = scope[0]
aid = row["element_id"]
print("row element_id", aid, "claim", row.get("claim_id"))
uri, u, p, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, p))
live = m.query_actors(driver, db, [aid])
driver.close()
actor = live.get(aid, {"id": aid, "name": aid})
actor["asserted_claim"] = row.get("asserted_claim", "")
print("actor", actor)

cache = {}
name = actor["name"]
candidates = []
for q in (f'"{name}" official site', f'"{name}" site officiel', f'"{name}" offizielle website'):
    for u in m.ddg_search(q, cache, 4):
        candidates.append((u, "search_official"))
for u in m.guess_domains(aid, name, None):
    candidates.append((u, "domain_guess"))

print("candidates", len(candidates))
for url, step in candidates:
    if not m.is_valid_http_url(url):
        print("INVALID", step, url)
        continue
    print("try", step, url[:90])
    entry = m.fetch_url(url, cache)
    if entry.get("error") and "4777" in str(entry.get("error")):
        print("BAD ERROR", url, entry["error"])
