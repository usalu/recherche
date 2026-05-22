import csv, json
from collections import defaultdict, Counter
from neo4j import GraphDatabase
from build_vocabulary_graph import REGELWERK, expand_land

RW={rw["id"]:rw for rw in REGELWERK}
vocab={}
for l in open("vocab_nodes.jsonl",encoding="utf-8"):
    if l.strip(): d=json.loads(l); vocab[d["id"]]=d
rf_ids={i for i,d in vocab.items() if d["label"]=="Regulierungsfrage"}
nf_ids={i for i,d in vocab.items() if d["label"]=="Nachweisforderung"}
rw_ids={i for i,d in vocab.items() if d["label"]=="Regelwerk"}
anchor=list(csv.DictReader(open("anchor_edges.csv",encoding="utf-8")))
vedges=list(csv.DictReader(open("vocab_edges.csv",encoding="utf-8")))

problems=defaultdict(list)

# --- live context: bauteilgruppe -> countries (via project), tragend ---
s=GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","ENTWERFENMITBESTAND")).session(database="mit-bestand")
bg_land=defaultdict(set)
for r in s.run("MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(b:Bauteilgruppe) OPTIONAL MATCH (p)-[:LIEGT_IN_LAND]->(l:Land) OPTIONAL MATCH (p)-[:LIEGT_IN_STADT]->(:Stadt)-[:LIEGT_IN_LAND]->(l2:Land) RETURN b.id AS b, collect(DISTINCT l.id)+collect(DISTINCT l2.id) AS lands"):
    bg_land[r["b"]]|={x for x in r["lands"] if x}
bg_tragend={}
for r in s.run("MATCH (b:Bauteilgruppe) RETURN b.id AS b, b.tragend AS t"):
    bg_tragend[r["b"]]=r["t"] if isinstance(r["t"],bool) else None
s.close()

STRUCTURAL_RW={"rw_cen_ts_1090_201","rw_en_1090","rw_en_1090_2_bolts_reuse","rw_sci_p427","rw_nta_8713","rw_eurocodes_en_1990_1999","rw_en_iso_6892","rw_din_4074_en_14081","rw_en_408","rw_en_13791_12504","rw_sia_269","rw_sia_269_2","rw_dafstb_rc_beton","rw_fib_precast_reuse","rw_en_1168","rw_en_1992_4","rw_nen_8700"}

# rule id from edge: for UNTERLIEGT to_node is rw; for others, need source rule — not stored per edge. Use to_node for UNTERLIEGT.
# 1. confidence range, self-loop, target-label sanity
for r in anchor:
    c=float(r["confidence"])
    if not (0<c<=1): problems["confidence_out_of_range"].append(r)
    if r["from_node_id"]==r["to_node_id"]: problems["self_loop"].append(r)
    et,tgt=r["edge_type"],r["to_node_id"]
    if et=="TRIGGERS_REGULIERUNGSFRAGE" and tgt not in rf_ids: problems["triggers_bad_target"].append(r)
    if et=="ERFORDERT_NACHWEIS" and tgt not in nf_ids: problems["erfordert_bad_target"].append(r)
    if et=="UNTERLIEGT_REGELWERK" and tgt not in rw_ids: problems["unterliegt_bad_target"].append(r)

# 2. jurisdiction mismatch on Bauteilgruppe UNTERLIEGT_REGELWERK (national rule vs component country)
mismatch=Counter()
for r in anchor:
    if r["from_label"]!="Bauteilgruppe" or r["edge_type"]!="UNTERLIEGT_REGELWERK": continue
    rid=r["to_node_id"]; rw=RW.get(rid)
    if not rw: continue
    if "EU" in rw["land"]: continue  # EU-wide ok everywhere
    rule_lands=set(expand_land(rw["land"]))
    comp_lands=bg_land.get(r["from_node_id"],set())
    if comp_lands and not (comp_lands & rule_lands):
        mismatch[rid]+=1
        if len(problems["jurisdiction_mismatch_examples"])<12:
            problems["jurisdiction_mismatch_examples"].append(f"{r['from_node_id']} (in {sorted(comp_lands)}) -> {rid} (gilt {sorted(rule_lands)})")

# 3. structural rule reaching tragend=False component
for r in anchor:
    if r["from_label"]=="Bauteilgruppe" and r["edge_type"]=="UNTERLIEGT_REGELWERK" and r["to_node_id"] in STRUCTURAL_RW:
        if bg_tragend.get(r["from_node_id"]) is False:
            problems["structural_on_nonloadbearing"].append(f"{r['from_node_id']} -> {r['to_node_id']}")

# 4. vocab backbone sanity
for r in vedges:
    if r["edge_type"]=="GESTUETZT_AUF_REGELWERK" and (r["from_node_id"] not in nf_ids or r["to_node_id"] not in rw_ids): problems["gestuetzt_bad"].append(r)
    if r["edge_type"]=="ERFORDERT_NACHWEIS" and (r["from_node_id"] not in rf_ids or r["to_node_id"] not in nf_ids): problems["vocab_erfordert_bad"].append(r)

print("=== AUDIT RESULTS ===")
for k,v in problems.items():
    print(f"\n[{k}] count={len(v)}")
    for x in v[:12]:
        print("   ",x if isinstance(x,str) else {kk:x[kk] for kk in ('from_node_id','edge_type','to_node_id')})
print("\n=== jurisdiction mismatch by rule (national rule on foreign-country component) ===")
for rid,c in mismatch.most_common():
    print(f"  {rid:28} {c}  (gilt {expand_land(RW[rid]['land'])})")
print(f"\nTOTAL jurisdiction mismatches: {sum(mismatch.values())}")
