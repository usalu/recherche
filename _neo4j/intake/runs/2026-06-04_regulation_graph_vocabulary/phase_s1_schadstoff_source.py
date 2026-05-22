# coding: utf-8
"""S1 — attach web-researched evidence to the unsourced Schadstoff edges. Dry-run default; --commit writes."""
import sys
from datetime import datetime, timezone
from neo4j import GraphDatabase
RUN="regulation_graph_vocab_2026_06_04"; NOW=datetime.now(timezone.utc).isoformat()
S=GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","ENTWERFENMITBESTAND")).session(database="mit-bestand")
POLL={
 "s_asbest":("https://www.baua.de/DE/Angebote/Regelwerk/TRGS/TRGS-519","TRGS 519: Gebaeude vor 1993 asbestverdaechtig; Erkundung vor Abbruch-/Sanierungsarbeiten."),
 "s_kmf":("https://www.baua.de/DE/Angebote/Regelwerk/TRGS/pdf/TRGS-521.pdf","TRGS 521: alte Mineralwolle vor 1996/2000, krebserzeugend Kat. 2."),
 "s_pcb":("https://gewerbeaufsicht.baden-wuerttemberg.de/documents/20121/49165/6_1.pdf","PCB-Richtlinie: PCB in Fugendichtmassen/Beschichtungen 1955-1975; Sanierung ab 3000 ng/m3."),
 "s_pak":("https://www.arguk.de/leistung/innenraum/Sanierung-von-teerpechhaltigen-Parkettklebern.htm","PAK in Teerprodukten (Parkettkleber/Dachpappe/Abdichtung) bis ~1970er, bis 60.000 mg/kg."),
 "s_schwermetalle":("https://www.schadstoff-kompass.de/grenzwerte-fuer-schadstoffbelastungen/","Schwermetalle (Pb/Cd/Hg/Cr) in Beschichtungen/Laborbauten; REACH-beschraenkt."),
 "s_bleifarbe":("https://www.schadstoff-kompass.de/grenzwerte-fuer-schadstoffbelastungen/","Bleifarbe in Anstrichen v.a. vor 1960."),
 "s_formaldehyd":("https://www.umweltbundesamt.de/system/files/medien/4031/dokumente/agbb_bewertungsschema_2024.pdf","AgBB/REACH: Formaldehyd aus Holzwerkstoffen (Span/MDF)."),
 "s_holzschutzmittel":("https://www.gesetze-im-internet.de/altholzv/BJNR330210002.html","Holzschutzmittel (PCP/Lindan) in behandeltem Holz bis 1989; AltholzV-Kategorien."),
 "s_schimmel":("https://www.umweltbundesamt.de/themen/gesundheit/umwelteinfluesse-auf-den-menschen/schimmel/aktueller-uba-schimmelleitfaden","UBA-Schimmelleitfaden: mikrobieller Befall bei Feuchteschaeden."),
 "s_chlorid":("https://www.abt-w.de/messungen/salzbestimmung.html","Bauschaedliche Salze (Chloride/Sulfate/Nitrate); Bewertung nach WTA-Merkblatt 4-5."),
 "s_salze":("https://www.abt-w.de/messungen/salzbestimmung.html","Bauschaedliche Salze im Mauerwerk; WTA-Merkblatt 4-5 Schwellenwerte."),
 "s_mineraloel":("https://www.labo-deutschland.de/documents/LABO_MKW-Bewertung_2017_12.pdf","MKW/Oelkontamination (z.B. oelverschmierte Betonboeden); LABO-Bewertung, relevant bei Rueckbau/Entsorgung."),
 "s_radon":("https://www.bfs.de/DE/themen/ion/umwelt/radon/regelungen/referenzwert.html","Radon: Referenzwert 300 Bq/m3 (StrlSchG); geologie-/standortabhaengig."),
}
commit="--commit" in sys.argv
def run(q,**k): return S.run(q,**k)
def cnt(q,**k): return run(q,**k).single()[0]
# pre-counts
print("BEFORE unsourced: HAT_SCHADSTOFFRISIKO",cnt("MATCH ()-[r:HAT_SCHADSTOFFRISIKO]->() WHERE r.source_url IS NULL RETURN count(r)"),
      "| ERFORDERT_SCHADSTOFFPRUEFUNG",cnt("MATCH ()-[r:ERFORDERT_SCHADSTOFFPRUEFUNG]->() WHERE r.source_url IS NULL RETURN count(r)"),
      "| TYPISCH_BEI_MATERIAL",cnt("MATCH (:Schadstoff)-[r:TYPISCH_BEI_MATERIAL]->() WHERE r.source_url IS NULL RETURN count(r)"))
if not commit:
    print("\nDRY-RUN. Would set source on edges per pollutant:")
    for p in POLL:
        n=cnt("MATCH ()-[r:HAT_SCHADSTOFFRISIKO|ERFORDERT_SCHADSTOFFPRUEFUNG]->(s:Schadstoff {id:$p}) WHERE r.source_url IS NULL RETURN count(r)",p=p)
        m=cnt("MATCH (s:Schadstoff {id:$p})-[r:TYPISCH_BEI_MATERIAL]->() WHERE r.source_url IS NULL RETURN count(r)",p=p)
        print(f"  {p:20} risk/pruef={n}  typisch_mat={m}")
    print("\n(s_radon node gets source_url property; left as location-based reference, no component edges.)")
else:
    for p,(url,q) in POLL.items():
        run("""MATCH (a)-[r:HAT_SCHADSTOFFRISIKO|ERFORDERT_SCHADSTOFFPRUEFUNG]->(s:Schadstoff {id:$p}) WHERE r.source_url IS NULL
               SET r.source_url=$url, r.source_quote=$qt, r.evidence_status='screening_documented',
                   r.confidence=coalesce(r.confidence,0.5), r.review_run=$run, r.updated_at_utc=$now""",p=p,url=url,qt=q,run=RUN,now=NOW)
        run("""MATCH (s:Schadstoff {id:$p})-[r:TYPISCH_BEI_MATERIAL]->() WHERE r.source_url IS NULL
               SET r.source_url=$url, r.source_quote=$qt, r.evidence_status='rule_documented',
                   r.confidence=coalesce(r.confidence,0.6), r.review_run=$run, r.updated_at_utc=$now""",p=p,url=url,qt=q,run=RUN,now=NOW)
        run("MATCH (s:Schadstoff {id:$p}) SET s.source_url=coalesce(s.source_url,$url)",p=p,url=url)
    print("\nAFTER unsourced: HAT_SCHADSTOFFRISIKO",cnt("MATCH ()-[r:HAT_SCHADSTOFFRISIKO]->() WHERE r.source_url IS NULL RETURN count(r)"),
          "| ERFORDERT_SCHADSTOFFPRUEFUNG",cnt("MATCH ()-[r:ERFORDERT_SCHADSTOFFPRUEFUNG]->() WHERE r.source_url IS NULL RETURN count(r)"),
          "| TYPISCH_BEI_MATERIAL",cnt("MATCH (:Schadstoff)-[r:TYPISCH_BEI_MATERIAL]->() WHERE r.source_url IS NULL RETURN count(r)"))
    print("COMMITTED.")
S.close()
