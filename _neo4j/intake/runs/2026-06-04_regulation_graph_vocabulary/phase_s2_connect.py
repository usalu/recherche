# coding: utf-8
"""S2 — connect material-bearing unconnected Bauteilgruppen with EXPLICIT correct sources (no mis-attribution)."""
import sys
from datetime import datetime, timezone
from neo4j import GraphDatabase
RUN="regulation_graph_vocab_2026_06_04"; NOW=datetime.now(timezone.utc).isoformat()
S=GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","ENTWERFENMITBESTAND")).session(database="mit-bestand")
commit="--commit" in sys.argv
def cnt(q,**k): return S.run(q,**k).single()[0]

# Universal reuse proofs (material-agnostic, correct for ANY reclaimed component)
UNIV={
 "nf_herkunfts_und_rueckbaudokumentation":("https://www.gesetze-im-internet.de/krwg/__6.html","KrWG §6: Vorbereitung zur Wiederverwendung; Herkunfts-/Rueckbaudokumentation.","rule_documented",0.7),
 "nf_produktstatus_und_leistungserklaerung":("https://www.ressource-deutschland.de/service/rechtlicher-rahmen-zur-ressourceneffizienz/eu-bauprodukte-verordnung-2024/3110/","EU-Bauprodukteverordnung 2024/3110: erfasst gebrauchte Produkte; Produktstatus/Leistungserklaerung.","rule_documented",0.7),
}
RF=("rf_reusedokumentationfrage","https://din.one/pages/viewpage.action?pageId=160465716","DIN SPEC 91484: Erfassung von Bauprodukten (Pre-Demolition-Audit).","rule_documented",0.7)
# materialpruefung ONLY where the material has a real test standard
MAT_TEST={
 "mat_stahl":("https://www.iso.org/standard/78322.html","EN ISO 6892-1: Zugversuch metallischer Werkstoffe."),
 "mat_aluminium":("https://www.iso.org/standard/78322.html","EN ISO 6892-1: Zugversuch Metalle (Aluminium)."),
 "mat_gusseisen":("https://www.iso.org/standard/78322.html","EN ISO 6892-1: Zugversuch Metalle (Gusseisen)."),
 "mat_beton":("https://standards.iteh.ai/catalog/standards/cen/3209bcc7-df9a-4eb2-904d-e690e79b7452/en-13791-2019","EN 13791/12504: In-situ-Druckfestigkeit Beton."),
 "mat_stahlbeton":("https://standards.iteh.ai/catalog/standards/cen/3209bcc7-df9a-4eb2-904d-e690e79b7452/en-13791-2019","EN 13791/12504: In-situ-Druckfestigkeit Beton."),
 "mat_holz":("https://www.dinmedia.de/en/standard/din-en-408/126881788","EN 408: mechanische Eigenschaften Holz."),
 "mat_holz_clt":("https://www.dinmedia.de/en/standard/din-en-408/126881788","EN 408: mechanische Eigenschaften Holz (CLT)."),
}
# material-intrinsic pollutant checks
INTRINSIC={"mat_holz":[("nf_holzschutzmittel_check","https://www.gesetze-im-internet.de/altholzv/BJNR330210002.html","AltholzV/DIN 68800: Holzschutzmittel in behandeltem Holz.","rule_documented",0.7)],
           "mat_holz_clt":[("nf_holzschutzmittel_check","https://www.gesetze-im-internet.de/altholzv/BJNR330210002.html","AltholzV/DIN 68800: Holzschutzmittel.","rule_documented",0.7)],
           "mat_mdf":[("nf_formaldehyd_oder_emissionsnachweis","https://www.umweltbundesamt.de/system/files/medien/4031/dokumente/agbb_bewertungsschema_2024.pdf","AgBB/REACH: Formaldehyd aus Holzwerkstoffen.","rule_documented",0.7)]}

targets=[(r["bg"],r["mats"]) for r in S.run("""MATCH (b:Bauteilgruppe) WHERE NOT (b)-[:ERFORDERT_NACHWEIS|TRIGGERS_REGULIERUNGSFRAGE]->()
   AND (b)-[:NUTZT_MATERIAL]->() RETURN b.id AS bg, [(b)-[:NUTZT_MATERIAL]->(m)|m.id] AS mats""")]
plan=[]
for bg,mats in targets:
    for nf,(u,q,st,c) in UNIV.items(): plan.append((bg,"Nachweisforderung","ERFORDERT_NACHWEIS",nf,u,q,st,c))
    plan.append((bg,"Regulierungsfrage","TRIGGERS_REGULIERUNGSFRAGE",RF[0],RF[1],RF[2],RF[3],RF[4]))
    done_mp=False
    for m in mats:
        if m in MAT_TEST and not done_mp:
            u,q=MAT_TEST[m]; plan.append((bg,"Nachweisforderung","ERFORDERT_NACHWEIS","nf_materialpruefung",u,q,"rule_documented",0.7)); done_mp=True
        for it in INTRINSIC.get(m,[]):
            plan.append((bg,"Nachweisforderung","ERFORDERT_NACHWEIS",it[0],it[1],it[2],it[3],it[4]))
from collections import Counter
print(f"targets={len(targets)} planned={len(plan)}  by nf:",dict(Counter(p[3] for p in plan)))
print("components getting materialpruefung (have a test standard):",len(set(p[0] for p in plan if p[3]=='nf_materialpruefung')),"/30 (rest: plastic/textile/messing have no test standard -> only universal proofs)")
if commit:
    for bg,lbl,rel,tid,u,q,st,c in plan:
        S.run(f"MATCH (b:Bauteilgruppe {{id:$bg}}) MATCH (t:`{lbl}` {{id:$tid}}) MERGE (b)-[r:`{rel}`]->(t) "
              "SET r.source_url=$u,r.source_quote=$q,r.evidence_status=$st,r.confidence=$c,r.basis='material_derived_S2',r.review_run=$run,r.created_at_utc=$now",
              bg=bg,tid=tid,u=u,q=q,st=st,c=c,run=RUN,now=NOW)
    print("\nCOMMITTED. BTG reaching reg layer:",cnt("MATCH (b:Bauteilgruppe)-[:ERFORDERT_NACHWEIS|TRIGGERS_REGULIERUNGSFRAGE]->() RETURN count(DISTINCT b)"),"/364",
          "| material-bearing unconnected left:",cnt("MATCH (b:Bauteilgruppe) WHERE NOT (b)-[:ERFORDERT_NACHWEIS|TRIGGERS_REGULIERUNGSFRAGE]->() AND (b)-[:NUTZT_MATERIAL]->() RETURN count(b)"))
else:
    print("DRY-RUN (no writes).")
S.close()
