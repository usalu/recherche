import json, os, csv, re
from collections import defaultdict, OrderedDict
from urllib.parse import urlparse

WORK = r"e:\recherche\_neo4j\review\2026-06-06_full_graph_verification\_agent06b_work"
LEDGER_DIR = r"e:\recherche\_neo4j\review\2026-06-06_full_graph_verification\ledger"

with open(os.path.join(WORK, "gap_nodes.json"), encoding="utf-8") as f:
    nodes = json.load(f)
with open(os.path.join(WORK, "edges_classified.json"), encoding="utf-8") as f:
    edges = json.load(f)

def dom(u):
    try: return urlparse(u).netloc.lower().replace("www.","")
    except: return ""

WEAK = ("play.google.com","apps.apple.com","instagram.com","facebook.com")

def tokset(s):
    return set(re.findall(r"[a-z0-9]+", s.lower()))

# choose best fetch url per node: prefer first-party (domain tokens overlap id/name), skip weak
node_plan = {}
for n in nodes:
    nid = n["id"]; nm = n.get("name") or ""
    urls = []
    if n.get("primary_source_url"): urls.append(n["primary_source_url"])
    urls += (n.get("source_urls") or [])
    # dedupe keep order
    urls = list(OrderedDict.fromkeys(urls))
    idtok = tokset(nid) | tokset(nm)
    best = None; best_score=-1
    for u in urls:
        d = dom(u)
        if any(w in d for w in WEAK):
            continue
        dtok = tokset(d.split(".")[0])
        score = len(idtok & dtok)
        # first-party homepage-ish bonus (short path)
        path = urlparse(u).path.strip("/")
        if score>0 and path.count("/")<=1:
            score += 1
        if score > best_score:
            best_score=score; best=u
    if best is None:
        # all weak or none
        best = urls[0] if urls else None
    firstparty = best_score>0
    node_plan[nid] = {"fetch_url": best, "firstparty": firstparty,
                      "all_urls": urls, "name": nm}

# dedupe fetch urls
fetch_map = defaultdict(list)
for nid,p in node_plan.items():
    if p["fetch_url"]:
        fetch_map[p["fetch_url"]].append(nid)

print("unique fetch urls:", len(fetch_map))
print("nodes with firstparty source:", sum(1 for p in node_plan.values() if p["firstparty"]))
print("nodes WITHOUT firstparty (weak/third-party only):")
for nid,p in node_plan.items():
    if not p["firstparty"]:
        print("   ", nid, "|", p["name"], "|", p["all_urls"])

with open(os.path.join(WORK,"node_plan.json"),"w",encoding="utf-8") as f:
    json.dump(node_plan,f,ensure_ascii=False,indent=2)
with open(os.path.join(WORK,"fetch_map.json"),"w",encoding="utf-8") as f:
    json.dump(fetch_map,f,ensure_ascii=False,indent=2)

# ---- Auto-generate EDGE ledger rows (218) ----
HEADER = ["claim_id","claim_kind","element_id","from_id","to_id","rel_type_or_label",
          "asserted_claim","basis_type","basis_ref","fetched","http_status","verdict",
          "confidence","proof_quote","proposed_action","agent_id","notes"]

rows = []
i=0
for e in sorted(edges, key=lambda x:(x["from_id"],x["to_id"])):
    i+=1
    a,b=e["from_id"],e["to_id"]; cat=e["cat"]
    ck = e.get("connection_kind") or ""
    asserted = f"actor-network link {a} -> {b}" + (f" ({ck})" if ck else "") + " (no evidence_url/source_url on edge)"
    if cat=="self_loop":
        verdict="SCHEMA_VIOLATION"; action="DELETE"
        note="self-loop VERBUNDEN_MIT_AKTEUR (a==a); structurally invalid; delete"
    elif cat=="bidir_reverse":
        verdict="SCHEMA_VIOLATION"; action="MERGE_DUPLICATE"
        note=f"bidirectional duplicate of {b}->{a}; collapse to one canonical direction (Agent 14 dedup class)"
    elif cat=="bidir_canonical":
        verdict="MISSING_EVIDENCE"; action="ADD_SOURCE"
        note=f"unsourced; bidirectional pair with {b}->{a} (that reverse = MERGE_DUPLICATE). Needs a source naming both endpoints before KEEP"
    else:
        verdict="MISSING_EVIDENCE"; action="ADD_SOURCE"
        note="legacy untagged edge, zero on-graph evidence (no evidence_url/source_url). Needs a fetched source naming both endpoints; until then unproven"
    # stub endpoints -> escalate
    def stub(x): return len(x)<=3 or x in {"tomas","rau","2hs","gxn","3xn"}
    if stub(a) or stub(b):
        if action=="ADD_SOURCE":
            action="ESCALATE_HUMAN"
            note="LOW-QUALITY/STUB endpoint id; "+note
    rows.append([f"A06B-rel-{i:04d}","rel",e["eid"],a,b,"VERBUNDEN_MIT_AKTEUR",
                 asserted,"none","",("false"),"","",verdict,"",
                 # placeholder; will reorder below
                 ])
    rows[-1] = [f"A06B-rel-{i:04d}","rel",e["eid"],a,b,"VERBUNDEN_MIT_AKTEUR",
                asserted,"none","","false","",verdict,"0.0","",action,"06b",note]

with open(os.path.join(WORK,"edge_rows.json"),"w",encoding="utf-8") as f:
    json.dump(rows,f,ensure_ascii=False)
print("\nedge rows generated:", len(rows))
from collections import Counter
print("edge actions:", Counter(r[14] for r in rows))
print("edge verdicts:", Counter(r[11] for r in rows))
