import json,os
from collections import Counter
WORK=r"e:\recherche\_neo4j\review\2026-06-06_full_graph_verification\_agent06b_work"
ed=json.load(open(os.path.join(WORK,"edges_classified.json"),encoding="utf-8"))
nd=json.load(open(os.path.join(WORK,"gap_nodes.json"),encoding="utf-8"))
allsrc={n["id"] for n in json.load(open(os.path.join(WORK,"sourced_akteur_nodes.json"),encoding="utf-8"))}

print("=== EDGES",len(ed),"===")
print("cat:",Counter(e["cat"] for e in ed))
print("ck:",Counter((e.get("connection_kind") or "(null)") for e in ed))
both_sourced=sum(1 for e in ed if e["from_id"] in allsrc and e["to_id"] in allsrc)
print("edges where BOTH endpoints are sourced actors:",both_sourced)
one=sum(1 for e in ed if (e["from_id"] in allsrc) ^ (e["to_id"] in allsrc))
print("edges where exactly ONE endpoint sourced:",one)
none=sum(1 for e in ed if e["from_id"] not in allsrc and e["to_id"] not in allsrc)
print("edges where NEITHER endpoint sourced:",none)
print("ALL edges have evidence_url/source_url? any:",any(e.get("evidence_url") or e.get("source_url") for e in ed))

# cluster hubs of interest
hubs=["akt_ii","symmetrys","cleveland_steel_tubes","gardiner_and_theobald","cantillon","heyne_tillett_steel","ellis_and_moore",
      "skanska_finland","consolis_parma","umacon","ramboll_finland","recreate_project","btu_cottbus",
      "baukarussell","bellastock","single_speed_design","john_hong","jinhee_park","paul_pedini","Lendager","anders_lendager","baticycle"]
print("\n=== edges touching named clusters in coverage proof ===")
for e in ed:
    if e["from_id"] in hubs or e["to_id"] in hubs:
        print(" ",e["from_id"],"->",e["to_id"])
