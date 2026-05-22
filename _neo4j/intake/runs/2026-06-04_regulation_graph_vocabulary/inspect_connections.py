import csv, json
from collections import defaultdict, Counter
from pathlib import Path
from neo4j import GraphDatabase

OUT=Path(".")
rows=list(csv.DictReader(open("anchor_edges.csv",encoding="utf-8")))
vocab={json.loads(l)["id"]:json.loads(l) for l in open("vocab_nodes.jsonl",encoding="utf-8") if l.strip()}
def vname(i): return vocab.get(i,{}).get("name",i)

# live names for anchors
ids=sorted({r["from_node_id"] for r in rows})
drv=GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","ENTWERFENMITBESTAND"))
names={}
with drv.session(database="mit-bestand") as s:
    for r in s.run("MATCH (n) WHERE n.id IN $ids RETURN n.id AS id, coalesce(n.name,n.titel,'') AS n", ids=ids):
        names[r["id"]]=r["n"]
drv.close()

byanchor=defaultdict(lambda:defaultdict(list))
for r in rows:
    byanchor[r["from_node_id"]][r["edge_type"]].append(r)

# pick representative anchors: most-connected per label
best_per_label={}
cnt=Counter(r["from_node_id"] for r in rows)
lbl={r["from_node_id"]:r["from_label"] for r in rows}
for aid,c in cnt.most_common():
    L=lbl[aid]
    if L not in best_per_label:
        best_per_label[L]=aid

out=[]
out.append("# Dry-run detail — anchor connections with evidence\n")
out.append(f"Total anchor edges: {len(rows)} across {len(ids)} anchors. Below: the most-connected anchor of each type, full evidence.\n")
ET=["TRIGGERS_REGULIERUNGSFRAGE","ERFORDERT_NACHWEIS","UNTERLIEGT_REGELWERK"]
for L in ["Material","Bauteilgruppe","Bauteiltyp","Projekt","Bauwerk"]:
    aid=best_per_label.get(L)
    if not aid: continue
    out.append(f"\n## [{L}] `{aid}` — {names.get(aid,'')}\n")
    for et in ET:
        es=byanchor[aid][et]
        if not es: continue
        out.append(f"### {et} ({len(es)})")
        for e in sorted(es,key=lambda x:-float(x["confidence"]))[:8]:
            tgt=e["to_node_id"]
            out.append(f"- **{vname(tgt)}** (`{tgt}`) · conf {e['confidence']} · {e['support_rules']} rule(s)")
            out.append(f"  - why: {e['applicability_reason']}")
            out.append(f"  - src: {e['source_url']}")
        if len(es)>8: out.append(f"  …(+{len(es)-8} more)")
        out.append("")

# distributions
out.append("\n## Distributions\n")
out.append("### Edges per Projekt (top 10)")
proj=[(a,sum(len(v) for v in byanchor[a].values())) for a in byanchor if lbl[a]=="Projekt"]
for a,c in sorted(proj,key=lambda x:-x[1])[:10]:
    out.append(f"- {a} ({names.get(a,'')}): {c} edges")
out.append("\n### TRIGGERS_REGULIERUNGSFRAGE by question")
q=Counter(r["to_node_id"] for r in rows if r["edge_type"]=="TRIGGERS_REGULIERUNGSFRAGE")
for k,c in q.most_common(): out.append(f"- {vname(k)} ({k}): {c}")
out.append("\n### ERFORDERT_NACHWEIS by proof (top 15)")
n=Counter(r["to_node_id"] for r in rows if r["edge_type"]=="ERFORDERT_NACHWEIS")
for k,c in n.most_common(15): out.append(f"- {vname(k)} ({k}): {c}")
out.append("\n### UNTERLIEGT_REGELWERK by law (top 15)")
w=Counter(r["to_node_id"] for r in rows if r["edge_type"]=="UNTERLIEGT_REGELWERK")
for k,c in w.most_common(15): out.append(f"- {vname(k)} ({k}): {c}")

Path("DRY_RUN_DETAIL.md").write_text("\n".join(out),encoding="utf-8")
print("wrote DRY_RUN_DETAIL.md")
print(f"anchors with names resolved: {sum(1 for i in ids if names.get(i))}/{len(ids)}")
