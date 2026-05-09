---
entity: "fallstudie"
id: "Timber_Square_London"
title: "Timber Square, London — Fallstudie Direct Reuse / Bauteilwiederverwendung"
build_status: "promoted_phase42"
legacy_paths:
  - "Gebäude\\Timber_Square_London.md"
node_kind: "core"
bauobjekt:
  - "Timber_Square_London"
projekt:
  - "Timber_Square_London"
---

# Timber Square, London — Fallstudie Direct Reuse / Bauteilwiederverwendung

## Legacy Content

### Legacy Source: Gebäude\Timber_Square_London.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Timber_Square_London
- Secondary targets: projekt/Timber_Square_London; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Timber Square, London — Fallstudie Direct Reuse / Bauteilwiederverwendung

**Arbeitsstand:** 2026-05-06  
**Sprache:** Deutsch  
**Grundregel:** Gewertet werden nur wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Retained existing structure wird nicht als Direct Reuse gezählt, wenn sie am Ort bleibt und dieselbe Funktion behält.

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Timber Square | Untersuchter Direct-Reuse-Fall | S1, S2, S3 | belegt | Büro-/Mixed-use-Campus |
| Gebäude | Print Building und Ink Building | Zwei Gebäudeteile: Umbau/Erweiterung + Neubau | S1, S2, S5 | belegt | Print: ehemaliges 1950s printworks; Ink: 15-storey Neubau |
| Ort | 25 Lavington Street / Bankside, Southwark, London SE1 | Standort | S1, S5 | belegt | London Borough of Southwark |
| Projekt | Net-zero / hybrid timber office redevelopment | Projektkontext | S1, S2, S4, S5 | belegt | Direct Reuse ist Teil eines größeren Low-carbon-Konzepts |
| Bauherr | Landsec | Client/Developer | S1, S2, S4, S5 | belegt | - |
| Architekt | Bennetts Associates | Architektur | S1, S4 | belegt | - |
| Tragwerksplaner | Heyne Tillett Steel / HTS | Structural Engineer | S1, S2 | belegt | entwickelte/benutzte Stockmatcher |
| People/Akteure | Landsec, Bennetts Associates, HTS, Mace, Hoare Lea, Alinea/T+T Alinea, Opera, Stora Enso, Hybrid Structures, Cleveland Steel & Tubes | Projektteam / Lieferkette | S1, S4, S8, S10 | belegt/teilweise | Rollen je Quelle |
| Reuse-Strategie | ex-situ Bauteilwiederverwendung von Stahl + Bestandserhalt + DfD | Reuse-Bewertung | S2, S3, S8 | belegt | Nur Stahlreuse und einzelne wiederverwendete Bauteile zählen als Direct Reuse |
| Bauteil | wiederverwendete Stahlträger | Hauptbauteil Direct Reuse | S2, S3, S7, S8 | belegt | Mengenangaben 115, 116 oder 125 t je Quelle |
| Bauteil | großer Stahlträger als Empfangstresen | fester Einbau aus vor Ort entnommenem Stahlträger | S3 | belegt | nicht für Tragwerksrating relevant |
| Bauteil | bestehende Struktur Print Building | Bestandserhalt | S1, S2, S4 | belegt | ca. 80 % erhalten; nicht als Direct Reuse zählen |
| Material | CLT und Stahl | Hybridtragwerk | S1, S2, S4, S8 | belegt | CLT nicht reused, aber kohlenstoffarme Strategie |
| Tool | HTS Reused Steel Stockmatcher | Matching von wiederverwendeten Stahlträgern | S2, S9 | belegt | Python-basiertes Tool |
| Datenmodell | Stock list / design list matching | Vergleich Bestandsstahl mit Designanforderungen | S9 | belegt | Materialmatching |
| Verbindung | reversible joints / non-composite structural design | DfD/Future Reuse | S3, S4 | belegt | Nicht selbst Direct Reuse, aber relevant |
| Prüfung | fire testing, acoustics, insurance, vibration performance at scale | Leistungsnachweise Hybrid-CLT/Stahl | S2 | belegt | spezifisch für Hybridbau; reused steel Prüfdetails unbekannt |
| Logistik | reused steel sourced from Cleveland Steel & Tubes laut Timber Development UK | Lieferkette Stahlreuse | S8 | teilweise belegt | genaue donor source unbekannt |
| Kennwert | >500 beams; ca. 115–125 t reused steel | tragender Direct-Reuse-Kennwert | S2, S3, S7, S8 | belegt/unklar | Quellen variieren |
| Kennwert | CO₂-Einsparung reused steel 216 oder 276 tCO₂e | Umweltkennwert | S1, S2, S3, S7 | unklar | Werte widersprechen sich |
| Hürde | fire, acoustics, insurance, vibration | technische Hürden des Hybridtragwerks | S2 | belegt | nicht nur Reuse |
| Norm/Recht | UKGBC Net Zero Carbon Buildings Framework; BREEAM Outstanding, WELL Platinum, NABERS 5 target | Projektbenchmarks | S2, S3, S4 | belegt | Normnummern/Regelwerke für Stahlreuse unbekannt |
| Wirtschaft | unbekannt | Kostenwirkung reused steel nicht publiziert | - | unbekannt | - |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Matching-Algorithmus | Reuse-Stahl wurde digital mit Designanforderungen abgeglichen | HTS Stockmatcher | verbindet Tool, Datenmodell, Bauteil |
| Stockholder / Reuse-Lieferant | Stahlreuse hängt an konkreten Lager-/Lieferantenbeständen | Cleveland Steel & Tubes | verbindet Bauteilbörse, Logistik, Wirtschaft |
| Retained-Structure-Anteil | Methodisch abgrenzen von Direct Reuse | 80 % Print Building retained | verbindet Gebäude, Kennwert, Warnung Bestandserhalt |
| Embodied-Carbon-Wertekonflikt | Quellen nennen 216 und 276 tCO₂e Einsparung | reused-steel carbon saving | verbindet Kennwert, Bericht, Datenqualität |

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ Bauteilwiederverwendung von Stahl; in-situ Bestandserhalt als Kontext; DfD/Future Reuse ergänzend
- **Hauptniveau:** Tragwerk; ergänzend feste Einbauten
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die über 500 reused steel beams / ca. 115–125 t steel sind Direct Reuse. Das Erhalten von ca. 80 % des Print Building ist wichtig für Low Carbon, zählt hier aber als Bestandserhalt und nicht als Direct Reuse. EAF-/scrap steel oder CLT sind nicht Direct Reuse.
- **Warum ist der Fall relevant?** Großmaßstäblicher kommerzieller Nachweis, dass digitale Bestands-/Designabgleiche reused steel in einem hochregulierten Büroprojekt ermöglichen können.

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Print Building analysieren und zu erhaltende Struktur bestimmen | Landsec, Bennetts, HTS, Mace | retention/cut-and-carve | unbekannt | selektive Demolition | unbekannt | Bestandsanalyse | onsite | zusätzliche Lasten auf Bestand | Transferstrukturen, foundation pads | S2, S10 |
| Bauteilinventar | Design list und stock list für reused steel erstellen | HTS | reused steel matching | HTS Stockmatcher, Python | - | - | Abgleich Section/Length/Weight | Stockholder-Bestände | passende Träger finden | Algorithmisches Matching inkl. Offcuts | S9 |
| Schadstoffprüfung | unbekannt für reused steel | unbekannt | unbekannt | unbekannt | - | - | unbekannt | unbekannt | unbekannt | unbekannt | - |
| Rückbau | Demolition der westlichen Bestandsstruktur / Entnahme vor Ort für Empfangsträger | Mace/Abbruchteam unbekannt | cut-and-carve/demolition | unbekannt | selektiv | reconditioned girder | unbekannt | onsite | Wertstoffe sichern | Wiederverwendung im Empfang | S3, S10 |
| Ausbau | Reused steel aus externer Lieferkette | Cleveland Steel & Tubes / HTS / Contractor | Stockholder procurement | Stockmatcher | unbekannt | unbekannt | unbekannt | Lieferkette zu Baustelle | Timing/Verfügbarkeit | matched procurement | S8, S9 |
| Transport | Lieferung reused beams | Lieferant/Contractor | konventionelle Stahl-Logistik | unbekannt | - | - | unbekannt | UK supply chain | unbekannt | unbekannt | S8 |
| Lagerung | Stockholder-Bestand / Baustellenkoordination | Cleveland Steel & Tubes, Mace | Lager-/Abruflogik | Stockmatcher-Daten | - | unbekannt | unbekannt | stock beams/offcuts | Lager- und Zuordnungskomplexität | digitaler Abgleich | S9 |
| Aufbereitung | Recondition/fabrication | Stahlbauer unbekannt | unbekannt | unbekannt | - | Reconditioning belegt nur für Empfangsgirder; Stahlträger unbekannt | unbekannt | Werkstatt | unbekannt | unbekannt | S3 |
| Planung | Hybrid-CLT/Stahl + reused steel integrieren | Bennetts, HTS, Landsec | hybrid structural design, DfMA | Stockmatcher | - | - | fire/acoustic/vibration tests | Materialverfügbarkeit im Entwurf | Großmaßstab/Versicherung/Brand | rigorous testing, non-composite design | S2, S3 |
| Genehmigung | Planung nach UKGBC/NABERS/BREEAM/WELL und Baurecht | Landsec, Planer, Behörden | Zertifizierungs-/Regelwerksprozess | unbekannt | - | - | NABERS Independent Design Review | - | Mass timber acceptance | Tests/Reviews | S2, S4 |
| Wiedereinbau | Montage reused steel in Struktur | Mace, Stahlbauer unbekannt | Stahlmontage | unbekannt | - | - | Abnahmen unbekannt | Baustelle | Schnittstellen CLT/Stahl | standardisierte/reversible Verbindungen | S2, S3 |
| Monitoring | Carbon Declaration / embodied carbon tracking | Bennetts, HTS, Landsec | upfront carbon reporting | unbekannt | - | - | LCA/Carbon data | - | Werte variieren | Quellenvergleich nötig | S1, S4 |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Wiederverwendete Stahlträger | >500 | Stück | UKGBC / TDUK | Projekt / Struktur | S3, S8 | belegt |
| Wiederverwendeter Stahl | 115 | t | HTS Stockmatcher | reused steel | S2, S7 | belegt |
| Wiederverwendeter Stahl | 116 | t | Mace | reused steel | S7 | belegt |
| Wiederverwendeter Stahl | 125 | t | Timber Development UK | reused steel | S8 | teilweise belegt |
| CO₂-Einsparung reused steel | 216 | tCO₂e | HTS project page | reused steel | S1, S2 | belegt, aber Konflikt |
| CO₂-Einsparung reused steel | 276 | tCO₂e | UKGBC / HTS topping out / Mace | reused steel | S3, S7 | belegt, aber Konflikt |
| Retained Print Building structure | ca. 80 | % | HTS/Bennetts/Mace | Bestandserhalt Print Building | S1, S2, S4 | belegt |
| GIA | 52.026 | m² | HTS | Gesamtprojekt | S1, S2 | belegt |
| Area | 33.910 | m² | Bennetts | Projektfläche, genaue Definition unklar | S4 | belegt |
| Workspace | 365.000 | sq ft | Landsec | vermietbare/Arbeitsflächen | S5 | belegt |
| Gesamtgröße | 380.000 | sq ft | Mace/Medien | Büro/Retail/Public Space | S7, S10 | teilweise belegt |
| Upfront carbon total | 510 | kgCO₂e/m² | Bennetts carbon data | A1-A5 total | S4 | belegt |
| Upfront carbon Stage 4 | <550 / 550 | kgCO₂e/m² | Bennetts older/newer pages | A1-A5 | S4 | teilweise belegt |
| Structural embodied carbon | 205 | kgCO₂e/m² | HTS | Struktur | S1 | belegt |
| Carbon stored by timber | 5.300 oder 4.999 | tCO₂e | HTS | timber storage | S1, S7 | unklar |
| Bauzeit/Completion | Q4 2025 / 2026 | Jahr/Quartal | Quellenvergleich | Projektstatus | S4, S7, S10 | unklar |
| U-Wert | unbekannt | - | - | - | - | unbekannt |
| Kosten | unbekannt reuse-spezifisch | - | - | - | - | unbekannt |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** wiederverwendeter Stahl wurde über HTS Stockmatcher gegen Designanforderungen gematcht und aus Stockholder-Beständen beschafft; Cleveland Steel & Tubes wird als Quelle/Lieferant genannt.
- **Bauteilbörse / Quelle:** keine offene Bauteilbörse belegt; eher professioneller Stahl-Stockholder + digitales Matching.
- **Kostenwirkung:** unbekannt; keine belastbaren Kostenangaben für reused steel gefunden.
- **Zeitwirkung:** unklar; Matching und procurement als spezifischer Zusatzprozess belegt, konkrete Dauer unbekannt.
- **Versicherung / Haftung:** Mass timber/Hybridstruktur mit insurance considerations belegt; spezifische Haftung für reused steel unbekannt.
- **Gewährleistung:** unbekannt
- **Arbeitsaufwand:** erhöhter Aufwand für Datenabgleich, Beschaffung, Koordination und Leistungsnachweise.
- **Lagerung:** Stahlstock beim Stockholder; Baustellenlagerung unbekannt.
- **Marktbarrieren:** Datenqualität, Verfügbarkeit passender Stahlträger, Zertifizierung/Prüfung, Terminplan, Versicherbarkeit im Hybridhochbau.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** donor sources der Stahlträger, genaue Profile/Längen, Prüf-/Zertifizierungsunterlagen für reused steel, Kosten, Gewährleistung, Handoverstatus, detailliertes Bauteilinventar für Nicht-Stahl-Elemente.
- **Sinnvolle neue Entitäten:** Matching-Algorithmus, Stockholder/Reuse-Lieferant, Retained-Structure-Anteil, Embodied-Carbon-Wertekonflikt.
- **Fehlende Daten:** eindeutige Stahlmenge, eindeutiger CO₂-Saving-Wert, genaue Einbauorte, Prüfverfahren, Vertragsmodell, Wartungsdaten.
- **Zu prüfende Quellen:** HTS Stockmatcher-Projektdaten, Landsec carbon reports, Mace procurement records, Cleveland Steel & Tubes Lieferlisten, BREEAM/WELL/NABERS Dokumente, Bauakten Southwark.

## Quellen und Links

- **S1 – Heyne Tillett Steel: Timber Square project.** https://hts.uk.com/project/timber-square/
- **S2 – Heyne Tillett Steel: How we made it: Timber Square.** https://hts.uk.com/news-views/how-we-made-it-timber-square/
- **S3 – UKGBC: Timber Square.** https://ukgbc.org/resources/timber-square/
- **S4 – Bennetts Associates: Timber Square.** https://www.bennettsassociates.com/projects/timber-square/
- **S5 – Landsec: Timber Square, Bankside.** https://www.landsec.com/en/workplace/our-properties/timber-square-london-se1
- **S6 – Landsec press release 2023.** https://landsec.com/media/press-releases/2023/landsec-signals-confidence-london-office-market-commitment-deliver-timber
- **S7 – Heyne Tillett Steel: Topping out at Timber Square.** https://hts.uk.com/news-views/topping-out-at-timber-square/
- **S8 – Timber Development UK: Print and Ink buildings, Timber Square.** https://timberdevelopment.uk/print-and-ink-buildings-timber-square/
- **S9 – Heyne Tillett Steel: Stockmatcher.** https://hts.uk.com/research-innovation/stockmatcher/
- **S10 – Mace Group: Timber Square.** https://www.macegroup.com/projects/timber-square/
