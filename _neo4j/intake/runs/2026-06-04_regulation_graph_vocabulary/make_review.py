import csv, json
from collections import defaultdict, Counter
from neo4j import GraphDatabase
from build_vocabulary_graph import REGULIERUNGSFRAGE, NACHWEISFORDERUNG, REGELWERK

vocab={}
for l in open("vocab_nodes.jsonl",encoding="utf-8"):
    if l.strip(): d=json.loads(l); vocab[d["id"]]=d
def vn(i): return vocab.get(i,{}).get("name",i)
anchor=list(csv.DictReader(open("anchor_edges.csv",encoding="utf-8")))
by=defaultdict(lambda:defaultdict(list))
for r in anchor: by[r["from_node_id"]][r["edge_type"]].append(r)

# live names + pick 2 clean examples
s=GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","ENTWERFENMITBESTAND")).session(database="mit-bestand")
names={r["id"]:r["n"] for r in s.run("MATCH (n) WHERE n.id IN $i RETURN n.id AS id, coalesce(n.name,n.titel,'') AS n", i=[r["from_node_id"] for r in anchor])}
s.close()

L=[]
L.append("# REVIEW — Regulation vocabulary overlay for `mit-bestand`")
L.append("\n**Run:** `regulation_graph_vocab_2026_06_04`  ·  **Status:** awaiting your approval  ·  **Nothing is written yet.**\n")
L.append("This overlay adds a regulation/proof layer on top of the existing graph and connects it to your\n"
         "Projekte, Materialien, Bauteilgruppen and Bauteiltypen — every connection backed by a real\n"
         "source URL + quote, derived from facts already in the graph (material, country, load-bearing,\n"
         "intervention, building era). **No existing nodes or edges are changed or deleted.**\n")

L.append("## 1. What gets added\n")
L.append("**3 new node types** (the vocabulary):\n")
L.append(f"- **Regulierungsfrage** ({len(REGULIERUNGSFRAGE)}) — the regulatory questions a reuse project raises")
L.append(f"- **Nachweisforderung** ({len(NACHWEISFORDERUNG)}) — the concrete proofs/checks required")
L.append(f"- **Regelwerk** ({len(REGELWERK)}) — the actual laws/standards (each web-researched, with URL)\n")
L.append("**New connections (edges), all carrying `source_url`, `source_quote`, `confidence`, `review_run`):**\n")
ec=Counter(r["edge_type"] for r in anchor)
L.append("| Edge | Meaning | Count |")
L.append("|---|---|---:|")
L.append(f"| anchor → Regulierungsfrage | which questions apply | {ec['TRIGGERS_REGULIERUNGSFRAGE']} |")
L.append(f"| anchor → Nachweisforderung | which proofs are required | {ec['ERFORDERT_NACHWEIS']} |")
L.append(f"| anchor → Regelwerk | which laws govern | {ec['UNTERLIEGT_REGELWERK']} |")
L.append(f"| + vocabulary backbone (Frage→Nachweis→Regelwerk→Land/Material/Bauteiltyp) | | 552 |")
L.append(f"\n**Total: 128 new nodes + ~4 158 new edges**, across {len({r['from_node_id'] for r in anchor})} of your existing anchors.\n")

L.append("## 2. The 11 Regulierungsfragen (questions)\n")
for i,n in REGULIERUNGSFRAGE.items(): L.append(f"- {n}")
L.append("\n## 3. The 33 Nachweisforderungen (proofs)\n")
L.append(", ".join(NACHWEISFORDERUNG.values()))

L.append("\n\n## 4. The 84 Regelwerke (laws/standards), by domain\n")
dom={"Reuse/Rückbau & Abfall":["rw_din_spec_91484","rw_din_spec_91525","rw_vdi_6210","rw_krwg","rw_gewabfv","rw_eu_wfd_2008_98","rw_eu_cdw_protocol","rw_iso_20887","rw_oenorm_b3151","rw_fr_pemd","rw_fr_rep_pmcb","rw_no_tek17","rw_be_tracimat_regional","rw_fcrbe_reuse_toolkit","rw_vob_c_din_18459"],
"Tragwerk & Material-Prüfung":["rw_cen_ts_1090_201","rw_sci_p427","rw_nta_8713","rw_en_1090","rw_en_1090_2_bolts_reuse","rw_eurocodes_en_1990_1999","rw_en_iso_6892","rw_din_4074_en_14081","rw_en_408","rw_en_13791_12504","rw_sia_269","rw_sia_269_2","rw_dafstb_rc_beton","rw_fib_precast_reuse","rw_en_1168","rw_en_1992_4","rw_nen_8700","rw_en_771_reclaimed","rw_naturstein_reuse"],
"Bauproduktstatus & Bauteilnormen":["rw_eu_cpr_2024_3110","rw_eu_cpr_305_2011","rw_dibt_zie_abz","rw_mvv_tb","rw_mbo_lbo","rw_ukca_ce","rw_en_14351","rw_en_13830","rw_din_18065","rw_espr_dpp"],
"Schadstoffe":["rw_trgs_519","rw_trgs_521","rw_trgs_524","rw_gefstoffv","rw_reach_annex_xvii","rw_pop_2019_1021","rw_vdi_6202","rw_pcb_richtlinie","rw_din_68800_altholzv","rw_agbb_voc","rw_vdi_3492","rw_uba_schimmelleitfaden","rw_strlschg_radon","rw_ebv"],
"Brandschutz":["rw_din_en_13501","rw_din_4102","rw_vkf_bsv","rw_uk_adb","rw_oib_richtlinien","rw_din_18008"],
"Bauphysik/Energie & Ökobilanz":["rw_geg","rw_sia_380_1","rw_sia_2032","rw_ch_muken","rw_fr_re2020","rw_nl_mpg","rw_uk_pas2080","rw_en_15804_15978","rw_eu_taxonomy","rw_eu_levels","rw_madaster_grp","rw_qng_dgnb","rw_glas_reuse_igu"],
"Genehmigung/Recht & Funktion":["rw_nl_bbl","rw_dk_br18","rw_prodhaftg_bgb","rw_dguv_v3_vde","rw_vdi_6023_6022","rw_din_18040"]}
for d,ids in dom.items():
    nm=[vn(i) for i in ids if i in vocab]
    L.append(f"**{d}** ({len(nm)}): "+", ".join(nm))
    L.append("")

def example(aid,title):
    L.append(f"\n### {title}: `{aid}` — {names.get(aid,'')}")
    for et,lab in [("TRIGGERS_REGULIERUNGSFRAGE","Questions"),("ERFORDERT_NACHWEIS","Required proofs"),("UNTERLIEGT_REGELWERK","Governing laws")]:
        items=sorted(set(vn(r["to_node_id"]) for r in by[aid][et]))
        L.append(f"- **{lab}:** "+", ".join(items))
    ex=sorted(by[aid]["UNTERLIEGT_REGELWERK"],key=lambda r:-float(r["confidence"]))[0]
    L.append(f"- *example evidence:* {ex['applicability_reason']}")
    L.append(f"  → {ex['source_url']}")

L.append("\n## 5. Worked examples (how to read a connection)\n")
# pick a steel structural group, a project, a material
steel=next((r["from_node_id"] for r in anchor if r["from_label"]=="Bauteilgruppe" and any('1090' in x["to_node_id"] for x in by[r["from_node_id"]]["UNTERLIEGT_REGELWERK"])),None)
proj=next((r["from_node_id"] for r in anchor if r["from_label"]=="Projekt"),None)
example("mat_stahl","MATERIAL")
if steel: example(steel,"BAUTEILGRUPPE")
if proj: example(proj,"PROJEKT")

L.append("\n## 6. Deliberately NOT connected (honest gaps)\n")
L.append("- Materials with no researched rule: Kunststoff, Dämmstoff, Bitumen, Lehm, Stroh, Textil, Kupfer/Messing, PCM.")
L.append("- `mat_faserzement` (Eternit): left unmapped — old fibre-cement is often asbestos, modern is not; needs your call.")
L.append("- Non-load-bearing steel railings in non-DE projects (no EU-wide non-structural steel reuse rule).")
L.append("- The old `HAT_HUERDE` / `REFERENZIERT_NORM` edges were **not** used (you flagged them as inaccurate).")

L.append("\n## 7. Quality checks already run\n")
L.append("- `audit_edges.py`: **0** jurisdiction mismatches, **0** structural rules on non-load-bearing parts, **0** bad targets, confidence all in (0,1].")
L.append("- `apply_to_graph.py` dry-run: **all 128 nodes + edges resolve** against the live graph (validated, no writes).")

L.append("\n## 8. To import (only after you approve)\n")
L.append("```powershell\npython apply_to_graph.py            # dry-run, no writes (re-check)\npython apply_to_graph.py --commit   # writes the overlay\n```")
L.append("**Full rollback (one step, removes everything this run added):**")
L.append("```cypher\nMATCH ()-[r {review_run:'regulation_graph_vocab_2026_06_04'}]->() DELETE r;\nMATCH (n {source_scope:'regulation_graph_vocab_2026_06_04'}) DETACH DELETE n;\n```")

L.append("\n## 9. Sign-off checklist\n")
for c in ["Vocabulary (questions / proofs / laws) makes sense","Domain coverage is right for your scope",
          "Worked examples look correct","Gaps in §6 are acceptable (or tell me to research them)",
          "OK that national rules apply only in their country","Approve commit"]:
    L.append(f"- [ ] {c}")

open("REVIEW.md","w",encoding="utf-8").write("\n".join(L))
print("wrote REVIEW.md  (",len(L),"lines )")
