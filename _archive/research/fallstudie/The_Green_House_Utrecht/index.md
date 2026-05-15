---
entity: "fallstudie"
id: "The_Green_House_Utrecht"
title: "The Green House, Utrecht"
build_status: "promoted_phase42"
legacy_paths:
  - "Gebäude\\The_Green_House_Utrecht.md"
node_kind: "core"
bauobjekt:
  - "The_Green_House_Utrecht"
projekt:
  - "The_Green_House_Utrecht"
---

# The Green House, Utrecht

## Legacy Content

### Legacy Source: Gebäude\The_Green_House_Utrecht.md

- Map action: split_into_case_graph
- Primary target: fallstudie/The_Green_House_Utrecht
- Secondary targets: projekt/The_Green_House_Utrecht; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# The Green House, Utrecht

**Fallstudie zur Wiederverwendung von Bauteilen / Direct Reuse / zirkulärem Bauen**  
**Stand:** 2026-05-06  
**Bearbeitungssprache:** Deutsch  
**Kurzregel für diese Auswertung:** Gezählt werden nur fest eingebaute wiederverwendete Bauteile/Materialien. Demontierbarkeit allein ist kein Reuse. Lose Möbel werden nicht gewertet.

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | The Green House Utrecht | Untersuchter Reuse-Fall | Q1, Q2 | belegt | temporärer zirkulärer Pavillon |
| Gebäude | The Green House | Restaurant, Meetingräume, Urban-Farming-Gewächshaus | Q1, Q3 | belegt | zweigeschossiger Pavillon |
| Projekt | temporärer Stopgap / circular pavilion | Zwischennutzung zwischen Knoopkazerne und Rabobank | Q1, Q2 | belegt | 15-Jahre-Horizont |
| Ort | Utrecht, Croeselaan / Knoopkazerne-Areal | Standort | Q1, Q5 | belegt | genaue Adresse in Q5 |
| People | cepezed | Architektur | Q1, Q2 | belegt | Entwurf |
| People | Rijksvastgoedbedrijf / Central Government Real Estate Agency | Primärer Auftraggeber | Q1, Q2 | belegt | Auftraggeber |
| People | R Creators | Konsortium / Vertragsauftraggeber | Q1, Q2, Q5 | belegt | Strukton, Ballast Nedam, Facilicom |
| People | Pieters Bouwtechniek | Tragwerksplanung | Q1, Q2, Q5 | belegt | Stability / Constructief ontwerp |
| People | Strukton Worksphere | Gebäudetechnik | Q1, Q2 | belegt | TGA |
| People | Ballast Nedam | Hauptauftragnehmer | Q1, Q2 | belegt | Main contractor |
| People | Kampstaal | Stahlbau | Q1, Q5 | belegt | neues demontables Stahltragwerk |
| People | De Groot & Visser | Fassaden | Q1 | belegt | Fassadenausführung |
| Bauteil | Rauchglas-Fassadenpaneele Knoopkazerne | wiederverwendet als zweite Haut und Gewächshausfassade | Q1, Q3, Q6 | belegt | Haupt-Reuse-Bauteil |
| Bauteil | Pflasterklinker aus alter Kade in Tiel | Boden Erdgeschoss | Q1, Q3 | belegt | Material/Bauteil-Reuse |
| Bauteil | vorkonsumiertes Holz / pre-used wood | Geschossdecke | Q1, Q3 | belegt | genaue Herkunft unbekannt |
| Bauteil | Innenwände / Holzfußboden-Bauteile / Dämmmaterialien | laut Dutch Architects wiederverwendet | Q3 | teilweise belegt | Details fehlen |
| Reuse-Strategie | Bauteil- und Materialwiederverwendung, temporärer demontabler Neubau | kombinierte Strategie | Q1, Q3 | belegt | Demontierbarkeit zusätzlich, nicht als Reuse gezählt |
| Tragwerkssystem | demontables Stahlrahmen-System aus galvanisierten Profilen | neues, wiederaufbaubares Tragwerk | Q1, Q2, Q5 | belegt | nicht Reuse, aber DfD |
| Verbindung | trockene / demontierbare Montage | Gebäude als Kit-of-parts | Q1, Q3 | teilweise belegt | Detailverbindungen unbekannt |
| Logistik | Urban Mining aus Knoopkazerne und alter Kade | Materialquellen | Q1, Q3 | belegt | Transportdistanz unbekannt |
| Software | Smart measuring system | im DutchArchitects-Text erwähnt | Q3 | unklar | keine Software genannt |
| Kennwert | 80 m² Vertical Farming Greenhouse | Nutzungs-/Flächenkennwert | Q1, Q2, Q4 | belegt | Teilfläche Gewächshaus |
| Kennwert | 15 Jahre temporäre Nutzung | Zeithorizont der Standortnutzung | Q1, Q4 | belegt | kein Lebensdauerwert für Bauteile |
| Förderprogramm | unbekannt | nicht gefunden | unbekannt | unklar | keine Förderquelle belegt |
| Wirtschaft | Miet-/Leasingmodelle für Licht/Möbel | Betriebscircularity | Q3 | teilweise belegt | Möbel nicht zählen |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Temporäre Wiederaufbaubarkeit | Das Gebäude ist auf Ortswechsel nach 15 Jahren ausgelegt | demontierbarer Pavillon inkl. Betonblock-Fundamente | verbindet Reuse-Strategie, Verbindung, Wirtschaft |
| Quellgebäude | Reuse-Material stammt gezielt aus benachbartem Umbau | ehemalige Knoopkazerne | verbindet Gebäude, Material, Logistik |
| Betriebszirkularität | Circularity umfasst Restaurantbetrieb, Leasing, Menü; nicht alles ist Bauteil-Reuse | Licht und Möbel geleast | trennt Wirtschaft von Bauteil-Reuse |

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; Materialwiederverwendung; temporär demontierbar.
- **Hauptniveau:** Gebäudehülle, Boden, Decke, Innenausbau; Tragwerk neu.
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Der Pavillon ist Neubau. Wiederverwendung betrifft entnommene Bauteile aus anderen Quellen. Die Demontierbarkeit des neuen Stahlrahmens ist eine zukünftige Reuse-Option und wird nur als Kontext gewertet.
- **Warum ist der Fall relevant?** Er zeigt, wie ein Entwurf aus konkreten verfügbaren Reuse-Bauteilen entwickelt wird: die Maße der wiederverwendeten Rauchglas-Paneele bestimmten die Dimensionierung der Gebäudehülle.

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Knoopkazerne-Fassadenpaneele als verfügbare Quelle erkannt | cepezed, Rijksvastgoedbedrijf | Urban Mining | unbekannt | Rückbau Knoopkazerne-Umbau | unbekannt | unbekannt | benachbarte Materialquelle | Maße fixieren Entwurf | Gebäudeproportionen ab Paneelen abgeleitet | Q1, Q6 |
| Bauteilinventar | Glasfassaden, Klinker, Holz, Innenbauteile identifiziert | cepezed / R Creators | Materialinventar unbekannt | smart measuring system erwähnt, nicht spezifiziert | unbekannt | Sortieren | unbekannt | mehrere Quellen | Daten fehlen | Kit-of-parts-Planung | Q1, Q3 |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Altbauteile | unbekannt | unbekannt |
| Rückbau | Rauchglas-Paneele aus Knoopkazerne entnommen | unbekannt | selektive Demontage anzunehmen | unbekannt | unbekannt | unbekannt | unbekannt | nahe Baustelle | Bruch/Schaden | Wiederverwendung in zweiter Haut | Q1 |
| Ausbau | Klinker aus alter Kade in Tiel und Holz aus Vorverwendung beschafft | unbekannt | Urban Mining / Beschaffung | unbekannt | unbekannt | Reinigung/Sortierung unbekannt | unbekannt | Transport nach Utrecht | Herkunft verstreut | Materialwahl nach Funktion | Q1, Q3 |
| Transport | Materialien nach Utrecht | unbekannt | unbekannt | unbekannt | n/a | n/a | unbekannt | Distanz unbekannt; Tiel–Utrecht ca. regionale Quelle, nicht als Kennwert nutzen | Transportbilanz fehlt | unbekannt | Q1 |
| Lagerung | unbekannt | unbekannt | unbekannt | unbekannt | n/a | n/a | unbekannt | unbekannt | Glasbruch, Sortierung | unbekannt | unbekannt |
| Aufbereitung | Klinker verlegt, Paneele montiert, Holz zu Elementen | R Creators / Ausführende | Vorfertigung / trockene Montage | unbekannt | n/a | unbekannt | unbekannt | Baustelle | Maß- und Qualitätssicherung | standardisierte Kit-of-parts-Struktur | Q1, Q3 |
| Planung | Pavillon als demontierbarer Bausatz | cepezed | Kit-of-parts, dry assembly | smart measuring system nicht genauer benannt | n/a | n/a | unbekannt | Material- und Entwurfskoordination | 15-Jahre-Zeithorizont | demontierbares Tragwerk und Fundamente | Q1, Q3 |
| Genehmigung | temporärer Pavillon | Bauherr, Behörden | unbekannt | unbekannt | n/a | n/a | unbekannt | unbekannt | temporäre Nutzung | unbekannt | Q1 |
| Wiedereinbau | Rauchglas als zweite Haut/Gewächshaus; Klinkerboden; Holzdecke | ausführende Firmen | Montage | unbekannt | n/a | Elemente eingebaut | unbekannt | Baustelle | technische Integration mit Heizung/TGA | EG-Klinker auf Sandbett mit Fußbodenheizung | Q1, Q3 |
| Monitoring | Gebäude nach 15 Jahren demontierbar; digitales/Monitoring unbekannt | Betreiber | unbekannt | unbekannt | n/a | n/a | unbekannt | potenzieller Rückbau | zukünftige Wiederverwendung ungeprüft | DfD-Konzept | Q1, Q4 |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| wiederverwendete Masse | unbekannt | kg/t | unbekannt | Bau-Reuse-Elemente | unbekannt | unklar |
| Anzahl Bauteile | unbekannt | Stück | unbekannt | Fassadenpaneele/Klinker/Holz | unbekannt | unklar |
| Fläche Gesamtgebäude | unbekannt | m² | unbekannt | Pavillon | unbekannt | unklar |
| Gewächshausfläche | 80 | m² | Projektangabe | Vertical Farming Greenhouse | Q1, Q2, Q4 | belegt |
| geplante Standortnutzungsdauer | 15 | Jahre | Projektangabe | temporäre Nutzung am Standort | Q1, Q4 | belegt |
| CO₂-Einsparung | unbekannt | kg CO₂e | unbekannt | unbekannt | unbekannt | unklar |
| Abfallvermeidung | unbekannt | kg/t | unbekannt | Reuse-Bauteile | unbekannt | unklar |
| Transportdistanz | unbekannt | km | unbekannt | Materialquellen Knoopkazerne/Tiel | unbekannt | unklar |
| Kosten | unbekannt | EUR | unbekannt | Reuse-Kosten | unbekannt | unklar |
| Bauzeit | 2016–2018 ungefähr | Jahre | Projekt-/News-Angaben | Planung/Bau gesamt | Q4, Q6 | teilweise belegt |
| Energiebedarf | unbekannt | kWh | unbekannt | Betrieb | unbekannt | unklar |
| U-Wert | unbekannt | W/m²K | unbekannt | Hülle | unbekannt | unklar |
| Lebensdauer | Standort 15; Bauteillebensdauer unbekannt | Jahre | Projektangabe | Gebäude/Standort | Q1 | teilweise belegt |
| Zirkularitätskennwert | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unklar |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** projektinterne/regionale Urban-Mining-Beschaffung aus Knoopkazerne und alter Kade; weitere Quellen für pre-used wood/Innenwände nicht vollständig belegt.
- **Bauteilbörse / Quelle:** keine klassische Bauteilbörse belegt; Knoopkazerne und Tiel-Kade als Quellen.
- **Kostenwirkung:** unbekannt; demontierbare Bauweise und temporärer Betrieb prägen die Wirtschaftlichkeit, aber keine Reuse-Kosten veröffentlicht.
- **Zeitwirkung:** unbekannt.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** zusätzliche Koordination von vorhandenen Glasmaßen, Klinkerboden und vorkonsumiertem Holz; nicht quantifiziert.
- **Lagerung:** unbekannt.
- **Marktbarrieren:** fehlende Mengen-/Prüfdaten; Integration von Altmaterial in öffentliche Gastronomie-/Versammlungsnutzung; Unterscheidung zwischen Reuse und zukünftiger Demontage.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** Normnummern, Prüfungen, Schadstoffgutachten, CO₂-Daten, Kosten, genaue Stücklisten, Software/Datenmodell, Bauteilbörse.
- **Welche neuen Entitäten wären sinnvoll?** Quellgebäude; temporäre Wiederaufbaubarkeit; Betriebszirkularität; Reuse-Maßraster.
- **Welche Daten fehlen?** Anzahl und Maße der Glas-Paneele, Masse der Klinker/Holzbauteile, Aufbereitungsaufwand, Brandschutz- und Bauphysiknachweise, Reuse-Kosten, Transportdaten, LCA.
- **Welche Quellen müssten geprüft werden?** Projektbrochure von cepezed; DGMR-Bericht; Bauphysik-/Brandschutzunterlagen; Materialpass; Ausführungsdetails von De Groot & Visser/Kampstaal/Strukton.

## Quellen / Links

- **Q1 – cepezed, „The Green House“:** https://www.cepezed.nl/en/project/the-green-house/22172/  
- **Q2 – cepezed.com, „The Green House“:** https://www.cepezed.com/projects/the-green-house/  
- **Q3 – Dutch Architects, „The Green House, Utrecht“:** https://www.dutcharchitects.org/projects/the-green-house-utrecht  
- **Q4 – cepezed, „circular pavilion the green house opened“:** https://www.cepezed.nl/en/news/circulair-paviljoen-the-green-house-geopend/25587/  
- **Q5 – Nationale Staalprijs, „The Green House“:** https://www.nationalestaalprijs.nl/project/green-house  
- **Q6 – cepezed, „kit of parts circulair“:** https://www.cepezed.nl/en/news/kit-of-parts-circulair/161018/  
- **Q7 – Archilovers, „The Green House“:** https://www.archilovers.com/projects/240181/the-green-house.html
