import json, os, csv
from collections import defaultdict
from urllib.parse import urlparse

WORK = r"e:\recherche\_neo4j\review\2026-06-06_full_graph_verification\_agent06b_work"

with open(os.path.join(WORK, "gap_edges.json"), encoding="utf-8") as f:
    edges = json.load(f)
with open(os.path.join(WORK, "gap_nodes.json"), encoding="utf-8") as f:
    nodes = json.load(f)

node_ids = {n["id"] for n in nodes}            # sourced gap-node ids
sourced_ids = set(node_ids)

# Load ALL sourced akteur (220) to know which endpoints are "sourced real" even if not gap
with open(os.path.join(WORK, "sourced_akteur_nodes.json"), encoding="utf-8") as f:
    all_sourced = json.load(f)
all_sourced_ids = {n["id"] for n in all_sourced}

# --- Edge structure analysis ---
pair_set = {(e["from_id"], e["to_id"]) for e in edges}
# also need full graph pairs to detect reverse existing even if covered
with open(os.path.join(WORK, "all_verbunden_edges.json"), encoding="utf-8") as f:
    all_edges = json.load(f)
all_pairs = {(e["from_id"], e["to_id"]) for e in all_edges}

self_loops = []
bidir = []
classified = []
for e in edges:
    a, b = e["from_id"], e["to_id"]
    rev_exists = (b, a) in all_pairs
    is_self = (a == b)
    if is_self:
        verdict, action = "SCHEMA_VIOLATION", "DELETE"
        cat = "self_loop"
    elif rev_exists:
        # bidirectional pair: keep canonical (a<b) as ADD_SOURCE, other as MERGE_DUPLICATE
        if a < b:
            verdict, action, cat = "MISSING_EVIDENCE", "ADD_SOURCE", "bidir_canonical"
        else:
            verdict, action, cat = "SCHEMA_VIOLATION", "MERGE_DUPLICATE", "bidir_reverse"
    else:
        verdict, action, cat = "MISSING_EVIDENCE", "ADD_SOURCE", "unsourced_affiliation"
    classified.append({**e, "verdict": verdict, "action": action, "cat": cat,
                       "from_sourced": a in all_sourced_ids, "to_sourced": b in all_sourced_ids})

from collections import Counter
print("EDGE categories:", Counter(c["cat"] for c in classified))
print("EDGE connection_kind:", Counter((e.get("connection_kind") or "(null)") for e in edges))
print("self loops:", [ (c["from_id"],c["to_id"]) for c in classified if c["cat"]=="self_loop"])

# endpoints that are low-quality stubs (short ids / not sourced)
def is_stub(nid):
    return (len(nid) <= 3) or (nid in {"tomas","rau","2hs","gxn","3xn"})
stub_edges = [c for c in classified if is_stub(c["from_id"]) or is_stub(c["to_id"])]
print("\nedges touching stub ids:", len(stub_edges))
for c in stub_edges:
    print("   ", c["from_id"], "->", c["to_id"])

with open(os.path.join(WORK, "edges_classified.json"), "w", encoding="utf-8") as f:
    json.dump(classified, f, ensure_ascii=False, indent=2)

# --- Node clustering by shared source URLs ---
url_to_nodes = defaultdict(list)
for n in nodes:
    urls = n.get("source_urls") or []
    if n.get("primary_source_url"):
        urls = [n["primary_source_url"]] + urls
    for u in urls:
        url_to_nodes[u].append(n["id"])

# pick a representative authoritative URL per node: prefer first-party domain match
def domain(u):
    try:
        return urlparse(u).netloc.lower().replace("www.","")
    except Exception:
        return ""

# shared pages covering multiple nodes
shared = {u: ids for u, ids in url_to_nodes.items() if len(ids) > 1}
print("\nShared source pages covering >1 node:", len(shared))
for u, ids in sorted(shared.items(), key=lambda kv: -len(kv[1])):
    print(f"  [{len(ids)}] {u} -> {ids}")

print("\nTotal gap nodes:", len(nodes))
