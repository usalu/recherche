---
id: "Big_Dig_Building_Boston"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "Big Dig Building, Boston/Cambridge — Fallstudie Direct Reuse / zirkuläres Bauen"
bauobjekt:
  - "Big_Dig_Building_Boston"
legacy_paths:
  - "Gebäude\\Big_Dig_Building_Boston.md"
projekt:
  - "Big_Dig_Building_Boston"
reuse_chain_detected: "True"
---
# Big Dig Building, Boston/Cambridge — Fallstudie Direct Reuse / zirkuläres Bauen

## Migration

- Fallstudie ID: Big_Dig_Building_Boston
- Legacy source count: 1
- Generated project: Big_Dig_Building_Boston
- Generated bauobjekt: Big_Dig_Building_Boston
- Extracted reuse_einsatz rows: 5
- Extracted datenpunkt rows: 11
- Extracted entity mapping rows: 14
- Reuse chain detected: True

## Legacy Content

### Legacy Source: Gebäude\Big_Dig_Building_Boston.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Big_Dig_Building_Boston
- Secondary targets: projekt/Big_Dig_Building_Boston; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Big Dig Building, Boston/Cambridge — Fallstudie Direct Reuse / zirkuläres Bauen

**Bearbeitungsstand:** 2026-05-06  
**Sprache:** Deutsch  
**Regelprüfung:** Gewertet werden nur tatsächlich wiederverwendete Bau-/Konstruktionselemente. Da dieser Fall als Vorschlag/abgebrochenes Projekt belegt ist, wird er nicht als gebauter Direct-Reuse-Hauptfall gewertet.

---

## 1. EINORDNUNG

- **Entscheidung:** ANHANG / NICHT ALS GEBAUTEN HAUPTFALL WERTEN  
- **Bewertung:** ★★☆☆☆  
- **Begründung:** Das Big Dig Building ist ein prämierter, aber nach Quellenlage nicht gebauter Vorschlag von Single Speed Design, der Infrastrukturbauteile aus Bostons Big Dig als Tragwerk, Fassade und Landschafts-/Gebäudeelemente nutzen sollte. Die Idee ist methodisch relevant, aber ohne tatsächlich realisierten Wiedereinbau darf sie nicht als gebauter Direct-Reuse-Fall in die Hauptliste.  
- **Vertrauensgrad:** teilweise belegt  
- **Warnung Bestandserhalt:** nein  
- **Warnung Möbel/Dekoration:** nein  
- **Projektstatus:** Proposal / aborted / ungebaut

---

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Big Dig Building | untersuchter Vorschlag | SsD / ArchDaily / Holcim Foundation | belegt | nicht Big Dig House verwechseln |
| Ort | Boston / Cambridge / North Cambridge, MA, USA | Standort/Projektkontext | SsD, ArchDaily, Holcim | teilweise belegt | Quellen nennen Boston bzw. Cambridge/North Cambridge |
| Projekt | Wiederverwendung von Big-Dig-Infrastrukturmaterialien | Kernidee | SsD / Holcim | belegt | als Bauteile von Tragwerk bis Fassade geplant |
| Gebäude | Big Dig Building | geplantes Wohn-/Gewerbeprojekt | ArchDaily | belegt | Programm: Housing, Commercial |
| People | Single Speed Design / SsD | Architektur | SsD / ArchDaily / Holcim | belegt | John Hong und Jinhee Park genannt |
| People | John Hong, Jinhee Park, Paul Pedini | Projektteam / Autoren | Holcim / New Yorker / SsD | teilweise belegt | Paul Pedini als Ingenieur/Initiator aus Big-Dig-Kontext belegt |
| Bauteil | Infrastrukturträger, Boxbeams, temporäre Straßen-/Rampenteile, Fassaden-/Strukturelemente | geplante Reuse-Bauteile | SsD / Holcim / ArchDaily | teilweise belegt | keine gebaute Bauteilliste |
| Material | Stahl und Beton | geplante Materialien | SsD / JCP/PRECS | teilweise belegt | Big Dig House später mit Stahl/Beton realisiert, hier Vorschlag |
| Reuse-Strategie | ex-situ; Infrastruktur-zu-Gebäude; Bauteilwiederverwendung | geplante Strategie | SsD / Holcim | belegt | ungebaut |
| Tragwerkssystem | Infrastrukturbauteile als hoch belastbare Gebäudestruktur | geplantes Tragwerksprinzip | SsD / Holcim | teilweise belegt | keine Nachweise für realisierten Bau |
| Kennwert | 2.335 m² site area; 2.936 m² constructed area | Planungskennwerte | ArchDaily | belegt | projektbezogene Entwurfsdaten |
| Förderprogramm | Holcim Awards Encouragement Prize 2005–2006 North America | Auszeichnung | Holcim Foundation | belegt | Preis, kein Förderprogramm im engeren Sinn |
| Hürde | Projektabbruch / nicht gebaut | Haupteinschränkung | JCP/PRECS | teilweise belegt | JCP: Projekt gestoppt; Grund in Quelle: Verlust des Hauptarchitekten |
| Methode | Relocate and reuse/recycle infrastructural materials as building components | Konzeptmethode | SsD | belegt | nicht als ausgeführte Methode nachgewiesen |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Nicht gebauter Reuse-Vorschlag | direkte Wiederverwendung wurde geplant, aber nicht realisiert | Big Dig Building | ergänzt Fallstudie, Projektstatus, Vertrauensgrad |
| Infrastruktur-Donor | Donor ist kein Gebäude, sondern Straßen-/Brücken-/Tunnelbau | Big Dig / Central Artery/Tunnel Project | verbindet Ort, Bauteil, Material, Logistik |
| Konzeptkennwert | Entwurfswerte sind nicht gebaute Betriebs-/Realisierungswerte | ArchDaily-Flächen | verbindet Kennwert und Projektstatus |

---

## 3. FALLSTUDIE

- **Name:** Big Dig Building  
- **Ort:** Boston / Cambridge / North Cambridge, Massachusetts, USA  
- **Gebäude:** geplantes Housing-/Commercial-Projekt  
- **Projekt:** Umnutzung von Big-Dig-Infrastrukturkomponenten als Gebäudestruktur und Fassaden-/Raumelemente  
- **Beteiligte People / Akteure:** Single Speed Design; John Hong; Jinhee Park; Paul Pedini als Initiator/Ingenieur im Big-Dig-Materialkontext  
- **Architekt:** Single Speed Design  
- **Tragwerksplaner:** unbekannt; Paul Pedini als structural engineer/Initiator im Umfeld belegt, genaue Rolle im Big Dig Building unbekannt  
- **Bauherr:** unbekannt  
- **Zeitraum:** Holcim Project Entry 2005; ArchDaily Project year 2008  
- **Ursprüngliche Nutzung:** temporäre/obsolete Infrastrukturbauteile aus Bostons Big Dig, z. B. erhöhte Straßen-/Rampenbauteile  
- **Neue Nutzung:** geplant als Gebäudestruktur, Fassade, Freiraum-/Landschaftselemente; nicht gebaut  
- **Fläche / Maßstab:** Site Area 2.335 m²; Constructed Area 2.936 m² laut ArchDaily  
- **Schutzstatus / Denkmalstatus:** unbekannt  
- **Quellenlage:** gut für Konzept und Auszeichnungen, unzureichend für gebaute Ausführung, Mengen und Prüfungen

---

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** geplant: ex-situ; Bauteilwiederverwendung; Infrastruktur-zu-Gebäude; partiell bis systembildend  
- **Hauptniveau:** geplant: Tragwerk, Gebäudehülle, räumliche Struktur, Außenraum  
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Der Vorschlag zielte nicht auf Bestandserhalt, sondern auf Überführung von Infrastrukturbauteilen in ein Gebäude. Da kein realer Wiedereinbau belegt ist, bleibt es jedoch Konzept/Anhang.  
- **Warum ist der Fall relevant?** Frühes, prämiertes Beispiel für Urban Mining großer Infrastrukturbauteile; zeigt Potenzial hoher Tragreserven und großer Spannweiten, aber auch das Risiko, dass ambitionierte Reuse-Konzepte nicht in gebaute Praxis übergehen.

---

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Boxbeams / Infrastrukturträger | Beton/Stahl, genau unbekannt | Big Dig temporäre/obsolete Straßeninfrastruktur | Brücken-/Rampen-/Straßentragwerk | geplant als Tragwerk | unbekannt | ja, geplant | ja | nein | nein | Demontage/Transport/Anpassung geplant | unbekannt | unbekannt | hohe Lasten, Gebäudenutzung | unbekannt | ungebaut | SsD / Holcim | Anzahl, Maße, Gewicht |
| Straßen-/Rampenelemente | Beton/Stahl | Big Dig | temporäre Fahrbahn/Rampe | geplant als Decken/Wände/Struktur | unbekannt | ja, geplant | ja | möglich | nein | unbekannt | unbekannt | unbekannt | Tragfähigkeit, Gebrauchstauglichkeit | unbekannt | ungebaut | SsD / Holcim | alle Ausführungsdaten |
| Fassaden-/Cladding-Elemente | unbekannt | Big Dig-Materialstrom | Infrastrukturmaterial | geplant als Hülle/Cladding | unbekannt | nein/teilweise | ja | ja | nein | Anpassung geplant | unbekannt | unbekannt | Wetterdichtheit, Befestigung | unbekannt | ungebaut | SsD | Material, Menge |
| Landscape / elevated landscape elements | Beton/Stahl/Erde unbekannt | Big Dig-Infrastruktur | Infrastruktur | geplant als begehbare/lastfähige Landschaft | unbekannt | ja/teilweise, geplant | ja | nein | nein | unbekannt | unbekannt | unbekannt | Nutzlasten, Abdichtung | unbekannt | ungebaut | Holcim | Details |
| TGA, Fenster, Türen, Dach | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | nicht belegt | — | alle Details |

---

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Big-Dig-Materialströme als Ressource erkannt | Single Speed Design, Paul Pedini | Urban-Mining-Konzept | unbekannt | — | — | unbekannt | Materiallager im Big-Dig-Kontext | riesige Materialmengen, Entsorgungsdruck | Entwurf aus vorhandenen Infrastrukturteilen | SsD / New Yorker |
| Bauteilinventar | Typologien und Lastpotenziale untersucht | Projektteam | Entwurfsstudie | unbekannt | — | — | unbekannt | unbekannt | keine veröffentlichte Bauteilliste | Konzeptgrafiken | Holcim / ArchDaily |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | — | — | unbekannt | unbekannt | Infrastrukturaltmaterialien | unbekannt | — |
| Rückbau | Big-Dig-Elemente verfügbar aus Abbau temporärer Straßen/Rampen | Big-Dig-Akteure, genaue Rolle unbekannt | Infrastrukturabbruch | unbekannt | Demontage/Abbruch | unbekannt | unbekannt | unbekannt | nicht projektspezifisch belegt | unbekannt | SsD / JCP |
| Ausbau | geplant, nicht ausgeführt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | ungebaut | — | — |
| Transport | geplant | unbekannt | Schwertransport wahrscheinlich, nicht belegt | unbekannt | — | unbekannt | unbekannt | unbekannt | große Bauteile | unbekannt | — |
| Lagerung | Big-Dig-Komponenten wurden gelagert; projektspezifisch unbekannt | unbekannt | Lagerdepot | unbekannt | — | unbekannt | unbekannt | unbekannt | Fläche/Kosten | Wiederverwendung als Alternative | Resource Salvation / New Yorker |
| Aufbereitung | geplant | unbekannt | Anpassung an Gebäudefunktion | unbekannt | — | unbekannt | unbekannt | unbekannt | Geometrie/Normen | unbekannt | SsD |
| Planung | Entwurf für Housing/Commercial | Single Speed Design | Material-driven Design | unbekannt | — | — | unbekannt | unbekannt | Abhängigkeit von Bauteilgeometrien | Entwurfsfreiheit durch hohe Lastreserven | SsD / Holcim |
| Genehmigung | unbekannt | unbekannt | unbekannt | unbekannt | — | — | unbekannt | unbekannt | ungebaut | — | — |
| Wiedereinbau | nicht erfolgt | — | — | — | — | — | — | — | Projekt nicht realisiert | — | JCP/PRECS |
| Monitoring | nicht möglich | — | — | — | — | — | — | — | ungebaut | — | — |

---

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | geplante Verwendung hoch belastbarer Infrastrukturbauteile | Tragfähigkeit für Wohn-/Gewerbenutzung | unbekannt | unbekannt | Umwidmung von Verkehrs- zu Gebäudelasten | hohe Tragreserven als Entwurfsargument | SsD / Holcim |
| Lastabtragung | geplant über Boxbeams/Träger/Paneele | unbekannt | unbekannt | unbekannt | Geometrie und Auflager | unbekannt | SsD |
| Verbindung | unbekannt | Kraftübertragung | unbekannt | unbekannt | Anschluss alter Infrastrukturteile an Neubau | unbekannt | — |
| Brandschutz | unbekannt | Feuerwiderstand | unbekannt | unbekannt | Umnutzung | unbekannt | — |
| Schallschutz | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Feuchte | unbekannt | Abdichtung bei Landschaft/Dach/Fassade | unbekannt | unbekannt | Infrastrukturbauteile nicht für Gebäudehülle entwickelt | unbekannt | Holcim |
| Wärmeschutz | unbekannt | Energie/Nutzung | unbekannt | unbekannt | massive Infrastrukturteile | unbekannt | — |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | Stahl-/Beton-Massivbauteile | unbekannt | — |
| Luftdichtheit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| TGA-Integration | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Barrierefreiheit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Dauerhaftigkeit | Big-Dig-Infrastrukturbauteile hoch belastbar | Dauerhaftigkeit | unbekannt | unbekannt | Bestandszustand | unbekannt | SsD |
| Wartung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Zulassung | keine gebaute Zulassung belegt | Nachweis in Gebäudeprojekt | unbekannt | unbekannt | Reuse von Infrastrukturbauteilen außerhalb Standards | unbekannt | eigene Einordnung |
| Haftung | unbekannt | Verantwortlichkeiten | unbekannt | unbekannt | nicht gebaut | — | — |

---

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Projektjahr | 2008 | Jahr | ArchDaily-Projektdaten | Entwurf | ArchDaily | belegt |
| Site Area | 2.335 | m² | ArchDaily-Projektdaten | Entwurf | ArchDaily | belegt |
| Constructed Area | 2.936 | m² | ArchDaily-Projektdaten | Entwurf | ArchDaily | belegt |
| Auszeichnung | Holcim Awards Encouragement Prize 2005–2006 North America | — | Holcim Foundation | Wettbewerb | Holcim | belegt |
| Metropolis Next Generation Prize | belegt | — | SsD | Wettbewerb | SsD | belegt |
| wiederverwendete Masse | unbekannt | t | — | geplantes Big Dig Building | — | unklar |
| Anzahl Bauteile | unbekannt | Stück | — | geplantes Big Dig Building | — | unklar |
| CO₂-Einsparung | unbekannt | kg CO₂e | — | — | — | unklar |
| Kosten | unbekannt | USD | — | — | — | unklar |
| Bauzeit | nicht gebaut | — | Projektstatus | — | JCP/PRECS | teilweise belegt |
| Realisierter Wiedereinbau | nein / unbekannt | — | Quellenlage | — | JCP/PRECS | teilweise belegt |

---

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Nicht gebaut / Projektabbruch | sozial / wirtschaftlich / organisatorisch | laut JCP gestoppt | keine reale Direct-Reuse-Fallstudie | Projektstatus, Fallstudie | als Konzeptanhang führen | gebaute Umsetzung zählt, nicht nur Idee | JCP/PRECS |
| Große Infrastrukturbauteile | logistisch/technisch | Gewicht, Größe, Geometrie | Transport-/Montage-/Planungsaufwand | Bauteil, Logistik, Werkzeug | unbekannt | Reuse braucht früh verfügbare Geometrie- und Zustandsdaten | SsD/Holcim |
| Norm- und Zulassungsfragen | rechtlich/technisch | Bauteile aus Verkehrsinfrastruktur in Gebäude | Nachweis unklar | Norm, Prüfung, Haftung | unbekannt | Cross-sector reuse benötigt neue Nachweisketten | eigene Ableitung |
| Nutzungskonflikt schwerer Bauteile | gestalterisch/technisch | massive Bauteile im Wohn-/Gewerbebau | Lastreserven, aber atypische Räume | Tragwerkssystem, Gestaltung | Entwurfsstrategie „heavy dwelling“ | technische Überdimensionierung kann Entwurfswert werden | SsD |
| Quellenverwechslung mit Big Dig House | methodisch | ähnliches Team/Thema, aber anderes gebautes Projekt | falsche Bewertung möglich | Fallstudie, Gebäude | klare Trennung | Donor- und Receiverprojekt exakt benennen | Recherchebefund |

---

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** geplant: Direktbeschaffung/Übernahme von Infrastrukturbauteilen aus Big-Dig-Materialstrom; nicht realisiert.  
- **Bauteilbörse / Quelle:** keine Bauteilbörse; Donorquelle war Big Dig / temporäre und obsolete Straßenelemente.  
- **Kostenwirkung:** unbekannt; Holcim würdigte nachhaltiges Potenzial, keine realen Baukosten öffentlich belegt.  
- **Zeitwirkung:** SsD argumentierte mit möglicher schneller Montage durch erprobte Highway-Fabrication-Technologien; nicht realisiert.  
- **Versicherung / Haftung:** unbekannt.  
- **Gewährleistung:** unbekannt.  
- **Arbeitsaufwand:** unbekannt; voraussichtlich hoch durch Prüfung, Transport, neue Anschlüsse.  
- **Lagerung:** Big-Dig-Materiallager als Kontext belegt; projektbezogene Lagerdauer unbekannt.  
- **Marktbarrieren:** ungebautes Konzept, fehlende Routine bei Infrastruktur-zu-Gebäude-Reuse, große Bauteile, Genehmigung, Haftung.

---

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** im Konzept hoch; Infrastruktur als Architektur sollte sichtbar werden.  
- **räumliche Transformation:** geplante Übersetzung von Highway-Elementen in Wohn-/Gewerberaum.  
- **Atmosphäre / Ausdruck:** „heavy“/massive Infrastrukturteile als neue Wohnlogik; nicht gebaut.  
- **Umgang mit Spuren:** unbekannt.  
- **sozialer Wert:** Kritik an urbanem Infrastrukturabfall und an Folgen großer Stadtautobahnprojekte.  
- **Denkmal- oder Bestandswert:** unbekannt.  
- **Kritik / Grenzen:** keine realisierte Direct-Reuse-Evidenz; nur als konzeptueller Anhang.

---

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** Bauherr, Genehmigung, Ausführungsplanung, Prüfberichte, genaue Bauteile, Kosten, CO₂, Versicherungs-/Haftungsmodell, endgültiger Projektstatus in Primärquelle.  
- **Sinnvolle neue Entitäten:** Infrastruktur-Donor; nicht gebauter Reuse-Vorschlag; Konzeptkennwert; Projektabbruch.  
- **Fehlende Daten:** exakte Materialmengen, Stückzahlen, Bauteilgeometrien, Prüfmethoden, Anschlussdetails, Gründe des Abbruchs.  
- **Zu prüfende Quellen:** Gorgolewski 2017; Holcim Jury Report; SsD-Archiv; Metropolis Next Generation Prize Unterlagen; Big-Dig-Materiallager-/Verwertungsakten.

---

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** nein; Anhang/Konzeptliste  
- **5 wichtigste Fakten:**  
  1. prämiertes Reuse-Konzept von Single Speed Design  
  2. geplant war die Wiederverwendung von Big-Dig-Infrastrukturteilen  
  3. Nutzung: Housing/Commercial  
  4. ArchDaily nennt 2.335 m² Site Area und 2.936 m² Constructed Area  
  5. nicht als gebauter Direct-Reuse-Fall belegt  
- **5 wichtigste Bauteile:**  
  1. geplante Boxbeams  
  2. geplante Fahrbahn-/Rampenelemente  
  3. geplante Strukturträger  
  4. geplante Cladding-Elemente  
  5. geplante Landschafts-/Dachelemente  
- **5 wichtigste Hürden:**  
  1. Projekt nicht gebaut  
  2. Transport/Logistik großer Infrastrukturteile  
  3. Norm-/Zulassungsfragen  
  4. Anschlussdetails  
  5. Verwechslung mit Big Dig House  
- **5 wichtigste übertragbare Erkenntnisse:**  
  1. Infrastrukturabbruch kann als Bauteilquelle gedacht werden.  
  2. Hohe Tragreserven können neue Programme erlauben.  
  3. Konzeptpreise ersetzen keine gebaute Evidenz.  
  4. Cross-sector reuse braucht Norm- und Haftungsmodelle.  
  5. Donor-/Receiverketten müssen früh organisatorisch gesichert sein.  
- **5 offene Fragen:**  
  1. Warum wurde das Big Dig Building genau nicht gebaut?  
  2. Welche Bauteile waren tatsächlich verfügbar?  
  3. Welche Prüfungen wären notwendig gewesen?  
  4. Gab es eine Bauherrschaft oder Finanzierung?  
  5. Welche Lehren gingen konkret in das Big Dig House über?

---

## QUELLEN UND LINKS

1. SsD Architecture: Big Dig Building. https://www.ssdarchitecture.com/works/residential/big-dig-building/  
2. ArchDaily: Big Dig Building / Single Speed Design. https://www.archdaily.com/30050/big-dig-building-single-speed-design  
3. Holcim Foundation: Big Dig Building. https://www.holcimfoundation.org/projects/big-dig-building-boston-massachusetts-usa  
4. Küpfer, C. et al.: *Reuse of concrete components in new construction projects*, Journal of Cleaner Production 383, 2023. https://www.sciencedirect.com/science/article/pii/S0959652622048090  
5. The New Yorker: Salvage Artists. https://www.newyorker.com/magazine/2007/03/19/salvage-artists  
6. FHWA: Big Lessons from the Big Dig. https://www.fhwa.dot.gov/publications/focus/01jul/index.cfm
