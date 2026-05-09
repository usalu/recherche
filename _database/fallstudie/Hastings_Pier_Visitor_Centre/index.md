---
entity: "fallstudie"
id: "Hastings_Pier_Visitor_Centre"
title: "Hastings Pier Visitor Centre / Pavilion Cladding, Hastings"
build_status: "promoted_phase42"
legacy_paths:
  - "Gebäude\\Hastings_Pier_Visitor_Centre.md"
node_kind: "core"
bauobjekt:
  - "Hastings_Pier_Visitor_Centre"
projekt:
  - "Hastings_Pier_Visitor_Centre"
---

# Hastings Pier Visitor Centre / Pavilion Cladding, Hastings

## Legacy Content

### Legacy Source: Gebäude\Hastings_Pier_Visitor_Centre.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Hastings_Pier_Visitor_Centre
- Secondary targets: projekt/Hastings_Pier_Visitor_Centre; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Hastings Pier Visitor Centre / Pavilion Cladding, Hastings

**Fallstudie zur Wiederverwendung von Bauteilen / Direct Reuse / zirkulärem Bauen**  
**Stand:** 2026-05-06  
**Bearbeitungssprache:** Deutsch  
**Kurzregel für diese Auswertung:** Gezählt werden nur fest verbaute wiederverwendete Bauteile. Möbel aus wiederverwendetem Holz sind dokumentiert, werden aber nicht als Bauteil-Reuse gewertet.

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Hastings Pier Visitor Centre / Pavilion Cladding | Untersuchter Reuse-Fall | Q1, Q2, Q3 | belegt | Fokus auf fest verbaute Altholzbekleidung |
| Gebäude | Hastings Pier / Visitor Centre | Pier mit neuem Besucherzentrum | Q1, Q3 | belegt | Gesamtfläche bezieht sich auf Pier, nicht nur Visitor Centre |
| Projekt | Hastings Pier Regeneration | Wiederaufbau/Regeneration nach Brand 2010 | Q1, Q4 | belegt | Großes Restaurierungsprojekt |
| Ort | Hastings, United Kingdom | Standort | Q1, Q3, Q4 | belegt | South Coast / Hastings |
| People | dRMM Architects | Architektur | Q1, Q3 | belegt | Principal architect |
| People | Hastings Pier Charity | Bauherr / Projektträger | Q1, Q4, Q6 | belegt | Charity ging später in Administration; nicht reuse-relevant |
| People | Ramboll | Tragwerks-/Multidisciplinary Engineering | Q1, Q3, Q6 | belegt | Marine, Struktur, Building Services |
| Bauteil | tropische Hartholz-Deckbohlen | wiederverwendet als feste Außenbekleidung | Q1, Q2, Q5 | belegt | Kernbauteil des Reuse-Falls |
| Material | Holz, tropisches Hartholz / Pier decking | Material der wiederverwendeten Bretter | Q2 | belegt | genaue Holzart unbekannt |
| Reuse-Strategie | Ex-situ auf demselben Standort / Bauteilwiederverwendung | Holz von alter Pier-Deckfläche zu Fassadenbekleidung | Q1, Q2 | belegt | Funktionswechsel Deck → Hülle |
| Tragwerkssystem | neues CLT-Besucherzentrum | neues Tragwerk, nicht Reuse | Q1, Q3 | belegt | CLT von KLH |
| Abbruchmethode | Bergung aus Brandruine | Holz aus charred remains gerettet | Q2 | teilweise belegt | Detailmethodik unbekannt |
| Aufbereitungsmethode | Zuschneiden / Spalten längerer Stücke | Anpassung der Bretter für Bekleidung | Q2 | belegt | exakte Oberflächenbehandlung unbekannt |
| Verbindung | Holzbekleidung auf neuem Visitor Centre | Befestigungssystem unbekannt | Q1, Q2 | teilweise belegt | Schrauben/Unterkonstruktion nicht belegt |
| Prüfung | Materialzustand / Eignung für Außenbekleidung | keine konkreten Prüfungen genannt | Q2 | unklar | unbekannt |
| Leistungsanforderung | Marine Außenklima, Dauerhaftigkeit, Brandschutz | aus Nutzung ableitbar, aber nicht quantifiziert | Q1, Q2 | unklar | Normen unbekannt |
| Norm | Grade-II-Listed Pier / Heritage-Kontext | Denkmal-/Heritage-Rahmen | Q4; Q6 abweichend | teilweise belegt | Q4 nennt Grade II; Q6 nennt Grade 1 – prüfen |
| Förderprogramm | Heritage Lottery Fund / National Lottery Heritage Fund | Finanzierung der Reparatur/Regeneration | Q1, Q4 | belegt | Förderbetrag ist kein Reuse-Kennwert |
| Hürde | begrenzte Längen und Mengen | Gestaltung der Bekleidung durch kurze Stücke | Q2 | belegt | Chevron-Muster nutzt Restlängen |
| Hürde | Budgetverschiebung nach Sturmschäden | ursprüngliche Spiegel-Fassade wurde aufgegeben | Q2 | belegt | führte zur Altholzlösung |
| Logistik | lokale Holzrettung und Holzverwertung | Hastings & Bexhill Wood Recycling bei Möbeln beteiligt | Q1, Q5 | teilweise belegt | Möbel ignoriert; Logistikkette für Bekleidung nicht vollständig belegt |
| Wirtschaft | £12.6 Mio. / £11.4 Mio. HLF-Förderung | Projektfinanzierung | Q1, Q4 | belegt | nicht Reuse-Kosten |
| Bericht | dRMM Insight „Building with reclaimed timber“ | Quelle zu Materialentscheidung und Aufbereitung | Q2 | belegt | wichtigste Detailquelle |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Heritage-Konflikt / Schutzstatuskonflikt | Quellen nennen unterschiedlich Grade II bzw. Grade 1 | National Lottery Heritage Fund vs. PT Projects | verbindet Norm/Recht, Hürde, Prüfung |
| Brandereignis | Direkter Auslöser und Materialquelle | Brand 2010 zerstörte Pier, einige Holzbohlen überlebten | verbindet Abbruchmethode, Material, Projektphase |
| Marine Exposition | Spezifische Leistungsumgebung für wiederverwendetes Holz | Fassadenbekleidung auf Pier über Meerwasser | verbindet Leistungsanforderung, Dauerhaftigkeit, Verbindung |

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ auf demselben Gesamtstandort; Bauteilwiederverwendung; Funktionswechsel von Deckbohle zu Fassadenbekleidung.
- **Hauptniveau:** Gebäudehülle / feste Außenbekleidung; Nebenfall Möbel wird nicht gezählt.
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die Pier-Instandsetzung und der erhaltene viktorianische Pavillon sind Bestandserhalt. Als Reuse zählt hier nur das entnommene und neu eingesetzte Holz der Brandruine, weil es in neuer Funktion als feste Hüllbekleidung verbaut wurde.
- **Warum ist der Fall relevant?** Der Fall zeigt eine opportunistische Reuse-Entscheidung: Ein ursprünglich geplantes teureres Bekleidungskonzept wurde nach Budgetänderung verworfen; die Restlängen geretteter Holzbohlen wurden gestalterisch in ein Chevron-Muster übersetzt.

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Zustand der brandgeschädigten Pier und überlebender Hölzer erkannt | dRMM, Hastings Pier Charity, Ingenieure | visuelle/site-basierte Einschätzung | unbekannt | Brandschaden / Räumung | unbekannt | unbekannt | vor Ort | Holzreste unregelmäßig | Potenzial der alten Deckbohlen erkannt | Q2 |
| Bauteilinventar | Auswahl brauchbarer Hartholzstücke | dRMM | Materialboard / Auswahl nach Längen | unbekannt | Rettung aus Ruine | Sortieren nach Länge/Qualität | unbekannt | wahrscheinlich vor Ort | begrenzte Menge | Fassadenmuster auf kurze Längen ausgelegt | Q2 |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | mögliche Brandrückstände | unbekannt | unbekannt |
| Rückbau | Abtrag von Brandresten und Reparatur unter Deck | Projektteam | Reparatur / Wiederaufbau | unbekannt | Brandruine geräumt | unbekannt | unbekannt | Meer-/Pier-Baustelle | laufende Seeerosion und Sturmschäden | Strukturelle Reparaturen | Q4, Q6 |
| Ausbau | Holzbohlen aus Brandresten geborgen | unbekannt | selektive Bergung | unbekannt | unbekannt | unbekannt | unbekannt | vor Ort | Qualität ungleichmäßig | nur verwertbare Stücke genutzt | Q2 |
| Transport | vermutlich innerhalb Baustelle / lokal | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | kurze Wege wahrscheinlich, nicht belegt | unbekannt | unbekannt | unbekannt |
| Lagerung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Witterung / Feuchte | unbekannt | unbekannt |
| Aufbereitung | längere Stücke gespalten; kurze Stücke für Chevron-Fassade | dRMM / Holzbauunternehmen | Zuschnitt / Profilierung | unbekannt | n/a | Spalten, Zuschneiden | unbekannt | Baustellen-/Werkstattlogistik unbekannt | Restlängen | Muster nutzt kurze Reststücke | Q2 |
| Planung | Umplanung von Spiegel-/Reflexionsfassade zu Altholzfassade | dRMM | Entwurfsänderung | unbekannt | n/a | n/a | unbekannt | Materialverfügbarkeit beeinflusst Entwurf | Budget nach Sturmschaden | Materialgerechte Gestaltung | Q2 |
| Genehmigung | Heritage-/Bauordnungsabstimmung | Bauherr, Behörden, Planer | unbekannt | unbekannt | n/a | n/a | unbekannt | unbekannt | Denkmal-/Brandschutzkontext | unbekannt | Q4 |
| Wiedereinbau | Montage als Bekleidung auf CLT-Gebäude | dRMM, Contractor | Fassadenbekleidung | unbekannt | n/a | zugeschnittene Holzprofile | unbekannt | Pier-Baustelle | Marine Außenklima | feste Bekleidung, Chevron-Muster | Q1, Q2 |
| Monitoring | unbekannt | unbekannt | unbekannt | unbekannt | n/a | n/a | unbekannt | unbekannt | Dauerhaftigkeit | unbekannt | unbekannt |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| wiederverwendete Masse | unbekannt | kg/t | unbekannt | nur Altholzbekleidung | unbekannt | unklar |
| Anzahl wiederverwendeter Bauteile | unbekannt | Stück | unbekannt | geborgene Holzbohlen | Q2 | unklar |
| wiederverwendete Fassadenfläche | unbekannt | m² | unbekannt | Visitor Centre / Nebenbekleidungen | Q1, Q2 | unklar |
| Fläche Gesamtprojekt | 11.720 | m² | Projektangabe | Pier/Gesamtprojekt, nicht Reuse-Fläche | Q3 | belegt |
| Pierlänge | 280 | m | Projektbeschreibung | Gesamtpier | Q5 | belegt |
| CO₂-Einsparung | unbekannt | kg CO₂e | unbekannt | unbekannt | unbekannt | unklar |
| Abfallvermeidung | unbekannt | kg/t | unbekannt | geborgene Holzbohlen | unbekannt | unklar |
| Transportdistanz | unbekannt | km | unbekannt | unbekannt | unbekannt | unklar |
| Kosten | £12.6 Mio. Förder-/Projektbetrag; £11.4 Mio. HLF-Anteil laut dRMM | GBP | Projektfinanzierung | Gesamtregeneration, nicht Reuse-Kosten | Q1, Q4 | belegt, aber nicht reuse-spezifisch |
| Bauzeit | unbekannt | Monate | unbekannt | unbekannt | unbekannt | unklar |
| Energiebedarf | unbekannt | kWh | unbekannt | unbekannt | unbekannt | unklar |
| U-Wert | unbekannt | W/m²K | unbekannt | Visitor Centre-Hülle | unbekannt | unklar |
| Lebensdauer | unbekannt | Jahre | unbekannt | Altholzbekleidung | unbekannt | unklar |
| Zirkularitätskennwert | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unklar |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** opportunistische Eigenbeschaffung aus der vorhandenen Brandruine / Pier-Baustelle; genaue Vertragsstruktur unbekannt.
- **Bauteilbörse / Quelle:** keine externe Bauteilbörse belegt; Quelle sind überlebende Deckbohlen des alten Piers.
- **Kostenwirkung:** Budgetverschiebung durch Sturmschäden machte ursprüngliche Spiegel-Fassade zu teuer; Reuse-Holz wurde alternative Bekleidung. Quantifizierte Einsparung: unbekannt.
- **Zeitwirkung:** unbekannt.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** zusätzliche Sortierung, Zuschnitt, Spalten und Planung mit Restlängen; Stunden unbekannt.
- **Lagerung:** unbekannt.
- **Marktbarrieren:** keine Marktquelle; projektinterne Bergung. Übertragbarkeit hängt von Materialqualität, Brandschadensprüfung und Außenraumtauglichkeit ab.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** Bauteilbörse, Software, Datenmodell, genaue Normen, detaillierte Prüfprotokolle, genaue Verbindungsmittel, Schadstoffgutachten, Monitoring.
- **Welche neuen Entitäten wären sinnvoll?** Brandereignis; Marine Exposition; Heritage-Konflikt; Restlängen-Entwurfsstrategie.
- **Welche Daten fehlen?** Holzart, Stückzahl, m² Bekleidung, Masse, Feuchte-/Brand-/Dauerhaftigkeitsprüfung, Befestigungsdetails, CO₂-Werte, Reuse-Kosten, Wartungsdaten.
- **Welche Quellen müssten geprüft werden?** Ausschreibungsunterlagen, Fassadendetails, Ramboll-/dRMM-Ausführungsdetails, Bauantrag, Heritage-Unterlagen, Holzschutz-/Brandschutzgutachten.

## Quellen / Links

- **Q1 – dRMM Architects, „Hastings Pier“:** https://drmmstudio.com/project/hastings-pier/  
- **Q2 – dRMM Architects, „Building with reclaimed timber“:** https://drmmstudio.com/insight/reclaimed-timber-at-hastings-pier/  
- **Q3 – ArchDaily, „Hastings Pier / dRMM“:** https://www.archdaily.com/876788/hastings-pier-drmm  
- **Q4 – National Lottery Heritage Fund, „Hastings Pier“:** https://www.heritagefund.org.uk/projects/hastings-pier  
- **Q5 – Archilovers, „HASTINGS PIER REGENERATION“:** https://www.archilovers.com/projects/211599/hastings-pier-regeneration.html  
- **Q6 – PT Projects, „Hastings Pier Redevelopment“:** https://www.ptprojects.co.uk/projects/hastings-pier-redevelopment  
- **Q7 – proHolz Austria, „Besucherzentrum Seebrücke von Hastings“:** https://www.proholz.at/holzbauten/architektur/seebruecke-von-hastings
