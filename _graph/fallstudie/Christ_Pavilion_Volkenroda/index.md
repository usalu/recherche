---
id: "Christ_Pavilion_Volkenroda"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "Christus-Pavillon / Christ Pavilion, Volkenroda — Fallstudie Direct Reuse / zirkuläres Bauen"
bauobjekt:
  - "Christ_Pavilion_Volkenroda"
legacy_paths:
  - "Gebäude\\Christ_Pavilion_Volkenroda.md"
projekt:
  - "Christ_Pavilion_Volkenroda"
reuse_chain_detected: "True"
---
# Christus-Pavillon / Christ Pavilion, Volkenroda — Fallstudie Direct Reuse / zirkuläres Bauen

## Migration

- Fallstudie ID: Christ_Pavilion_Volkenroda
- Legacy source count: 1
- Generated project: Christ_Pavilion_Volkenroda
- Generated bauobjekt: Christ_Pavilion_Volkenroda
- Extracted reuse_einsatz rows: 8
- Extracted datenpunkt rows: 13
- Extracted entity mapping rows: 18
- Reuse chain detected: True

## Legacy Content

### Legacy Source: Gebäude\Christ_Pavilion_Volkenroda.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Christ_Pavilion_Volkenroda
- Secondary targets: projekt/Christ_Pavilion_Volkenroda; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Christus-Pavillon / Christ Pavilion, Volkenroda — Fallstudie Direct Reuse / zirkuläres Bauen

**Bearbeitungsstand:** 2026-05-06  
**Sprache:** Deutsch  
**Regelprüfung:** Gewertet werden nur wiederverwendete Bau-/Konstruktionselemente. Hier zählt die Translozierung des gesamten Pavillonensembles: demontiert nach EXPO 2000 und am Kloster Volkenroda wiederaufgebaut.

---

## 1. EINORDNUNG

- **Entscheidung:** VERGLEICHSFALL / ANHANG  
- **Bewertung:** ★★☆☆☆  
- **Begründung:** Der Christus-Pavillon ist ein klar belegter Fall von Gebäude-/Pavillonversetzung: Das auf der EXPO 2000 errichtete Ensemble wurde nach der Weltausstellung abgebaut und in gleicher Fügung am Kloster Volkenroda wieder aufgebaut. Die Reuse-Strategie ist stark und baulich real, aber wegen Pavillon-/Expo-Logik und ursprünglich geplanter Demontierbarkeit kein Hauptfall für dauerhafte Gebäudereuse im Regelbau.  
- **Vertrauensgrad:** belegt  
- **Warnung Bestandserhalt:** nein  
- **Warnung Möbel/Dekoration:** nein; Kunst-/Vitrinenfüllungen werden nicht als Reuse-Bauteile gewertet  
- **Projektstatus:** gebaut / transloziert / in Nutzung

---

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Christus-Pavillon / Christ Pavilion | untersuchter Fall | gmp / Kloster Volkenroda / Structurae | belegt | EXPO 2000 → Volkenroda |
| Ort | Hannover EXPO 2000; Kloster Volkenroda, Thüringen | Donor-/erster Standort und Empfängerort | gmp / Kloster | belegt | Standortwechsel nach Expo |
| Gebäude | Christus-Pavillon | Pavillon / Kirche / Kulturgebäude | gmp | belegt | ursprüngliche Nutzung Ausstellung/Kirche, heute Kirche/Klosterensemble |
| Projekt | Demontage und Wiederaufbau des gesamten Ensembles | Kern der Wiederverwendung | gmp | belegt | „in gleicher Fügung“ wiederaufgebaut |
| People | gmp · Architekten von Gerkan, Marg und Partner | Architekt | gmp / Structurae | belegt | Entwurf Meinhard von Gerkan, Joachim Zais |
| People | Evangelisches Büro für die Weltausstellung Expo 2000 | Auftraggeber | gmp | belegt | Kirchenprojekt |
| People | Kloster Volkenroda / Jesus-Bruderschaft | heutiger Betreiber/Kontext | Kloster / Bauhaus Uni | teilweise belegt | Betreiberkontext genannt |
| Bauteil | Stahltragwerk / neun kreuzförmige Stützen | Tragwerk des Christusraums | gmp | belegt | Dach wird von neun schlanken kreuzförmigen Stützen getragen |
| Bauteil | Marmor-Glas-Hülle | Hülle des Christusraums | gmp | belegt | transluzente, einschalige Fläche |
| Bauteil | Glasfassade / Kreuzgang / Vitrinen | Hülle und Raumstruktur | gmp / Bauhaus Uni | belegt | doppelwandige Stahl-Glas-Konstruktion mit quadratischen Ausfachungen |
| Material | Stahl, Sichtbeton, Glas, Marmor | Hauptmaterialien | gmp | belegt | coated steel / fair-faced concrete / glass / marble |
| Tragwerkssystem | modulares, demontier- und wieder zusammensetzbares System | Grundlage der Translozierung | gmp | belegt | modulare Konstruktion |
| Verbindung | demontierbare/modulare Fügung | Wiederaufbau möglich | gmp | teilweise belegt | genaue Verbindungsmittel unbekannt |
| Reuse-Strategie | Gebäudeversetzung / komplett / ex-situ | ganze Pavillonstruktur wiederverwendet | gmp / Kloster | belegt | gesamtes Ensemble; gmp: Ausnahme Krypta, Kolonnade, Wasserbecken in deutscher Quelle |
| Kennwert | BGF 2.004 m²; BRI 18.548 m³ | Maßstab | gmp / Structurae | belegt | Projektkennwerte |
| Kennwert | Wiederaufbau August 2001 | Zeitraum | gmp | belegt | gmp englisch: August 2001; deutsch: Fertigstellung Wiederaufbau August 2001 |
| Leistungsanforderung | Kirche / öffentlicher Versammlungsraum | neue Nutzung | Structurae / Kloster | belegt | heutige Nutzung Kirche |
| Hürde | Instandhaltung der Fenstervitrinen | spätere technische Hürde | Bauhaus-Universität Weimar | belegt | Schäden nach 20 Jahren Witterung |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Translozierung | Wiederverwendung des ganzen Gebäudes durch Ortsversetzung | Hannover → Volkenroda | verbindet Gebäude, Ort, Logistik, Reuse-Strategie |
| Wiederaufbau in gleicher Fügung | wichtig für Direct Reuse kompletter Gebäude | demontiert und in gleicher Ordnung reassembled | verbindet Verbindung, Prozessphase, Bauteil |
| Temporärer Erstnutzer | Expo-Pavillon war von Beginn an für spätere Versetzung gedacht | EXPO 2000 | verbindet Projektstatus, Reuse-Strategie |

---

## 3. FALLSTUDIE

- **Name:** Christus-Pavillon / Christ Pavilion, EXPO 2000  
- **Ort:** ursprünglich Hannover EXPO 2000; wiederaufgebaut im Kloster Volkenroda, Körner/Thüringen  
- **Gebäude:** ökumenischer Pavillon / Kirche / Kreuzgangensemble  
- **Projekt:** Abbau nach EXPO 2000 und Wiederaufbau in Volkenroda  
- **Beteiligte People / Akteure:** gmp Architekten; Meinhard von Gerkan; Joachim Zais; Evangelisches Büro für die Weltausstellung Expo 2000; Evangelisch-Lutherische Landeskirche Hannover; Kloster Volkenroda / Jesus-Bruderschaft; Andreas Felger für spätere künstlerische Kammern  
- **Architekt:** gmp · Architekten von Gerkan, Marg und Partner; Entwurf Meinhard von Gerkan und Joachim Zais  
- **Tragwerksplaner:** unbekannt; Structurae nennt Teilnehmerbereich, aber in den gefundenen Ausschnitten ist kein Tragwerksplaner belastbar sichtbar  
- **Bauherr:** Evangelisches Büro für die Weltausstellung Expo 2000; genaue Rechtsform unbekannt  
- **Zeitraum:** Wettbewerb 1997; Bauzeit 1999–April/2000; Wiederaufbau in Volkenroda Februar–August 2001 bzw. Fertigstellung August 2001  
- **Ursprüngliche Nutzung:** EXPO-Pavillon / ökumenische Kirche für Weltausstellung  
- **Neue Nutzung:** Kirche / Bestandteil des Klosters Volkenroda  
- **Fläche / Maßstab:** BGF 2.004 m²; BRI 18.548 m³; Christusraum ca. 24 × 24 m und 18 m Höhe; große Kammer bei Felger-Quelle 25 × 25 × 18 m; Kreuzgang ca. 70 × 30 × 6,8 m laut Felger-Quelle  
- **Schutzstatus / Denkmalstatus:** Bauhaus-Universität behandelt Frage „vom EXPO 2000 zum Denkmal 2000?“; formaler Denkmalstatus unbekannt  
- **Quellenlage:** sehr gut für Architektur, Material, Translozierung und Kennwerte; begrenzt für Montage-/Prüfdetails und Kosten

---

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** komplett; ex-situ; Gebäudeversetzung; direkte Wiederverwendung eines demontierten Pavillonensembles  
- **Hauptniveau:** Gesamtgebäude / Tragwerk / Gebäudehülle / räumliche Struktur  
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Der Pavillon blieb nicht am Ort und wurde nicht stofflich recycelt; er wurde abgebaut und an einem neuen Ort wieder zusammengesetzt.  
- **Warum ist der Fall relevant?** Seltener, gut belegter Fall einer vollständigen, geplanten Translozierung eines modularen Stahl-Glas-Marmor-Pavillons. Wichtig für Demontierbarkeit, Wiederaufbau in gleicher Fügung und zweite Nutzung von Expo-Architektur.

---

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| gesamtes Pavillonensemble | Stahl, Sichtbeton, Glas, Marmor | EXPO 2000 Hannover | Pavillon / Ausstellungskirche | Kirche / Klosterensemble | BGF 2.004 m²; BRI 18.548 m³ | ja/teilweise | ja | ja | nein | demontiert und in Volkenroda wiederaufgebaut | modular; Details unbekannt | unbekannt | Standsicherheit, Wetter, Nutzung | unbekannt | Transport/Montage | gmp | Kosten, Montageplan |
| Dachtragwerk Christusraum | beschichteter Stahl | EXPO 2000 | Dachtragwerk | Dachtragwerk Kirche | Dach über ca. 24×24 m Raum | ja | ja | ja | nein | Abbau/Wiederaufbau | unbekannt | unbekannt | Tragfähigkeit | unbekannt | Fügung/Transport | gmp | Profilgrößen |
| neun kreuzförmige Stützen | Stahl | EXPO 2000 | tragende Stützen | tragende Stützen | 9 Stück | ja | ja | nein | nein | Abbau/Wiederaufbau | unbekannt | unbekannt | Lastabtragung Dach | unbekannt | Anschlüsse | gmp | Querschnitte |
| Marmor-Glas-Wand Christusraum | Marmor + Glas | EXPO 2000 | transluzente Hülle | Hülle/Raumstimmung | einschalige Fläche; genaue Anzahl Tafeln unbekannt | nein/teilweise | ja | ja | nein | Abbau/Wiederaufbau | unbekannt | unbekannt | Witterung, Befestigung, Sicherheit | unbekannt | Bruch/Transport | gmp | Tafelmaße |
| Kreuzgang | Stahl-Glas-Konstruktion | EXPO 2000 | umlaufender Pavillon-/Ausstellungsraum | Kloster-Kreuzgang | ca. 70×30×6,8 m laut Felger-Quelle | teilweise | ja | ja | nein | Abbau/Wiederaufbau | modular | unbekannt | Witterung, Nutzung | unbekannt | Fenstervitrinen später beschädigt | gmp / Bauhaus Uni / Felger | genaue Module |
| Glasfassade/Vitrinen | Glas, Stahl, Füllungen verschiedener Herkunft | EXPO 2000 | Ausstellungsfassade | Kreuzgangfassade | großformatige Vitrinen; genaue Anzahl unbekannt | nein | ja | ja | nein | wiederaufgebaut | unbekannt | unbekannt | Witterung, Sicherheit | unbekannt | Witterungsschäden nach 20 Jahren | gmp / Bauhaus Uni | Anzahl/Füllungen |
| Sichtbetonteile | Beton | EXPO 2000 | Sockel/Raumteile | Raum-/Bauwerksteile | unbekannt | teilweise | ja | teilweise | nein | Abbau/Wiederaufbau, soweit Teil des translozierten Ensembles | unbekannt | unbekannt | Dauerhaftigkeit | unbekannt | unbekannt | gmp | genaue Bauteile |
| Krypta, Kolonnade, Wasserbecken | unbekannt | EXPO 2000 | Teil des Expo-Komplexes | laut gmp-de nicht mit transloziert | nicht wiederverwendet als Teil des Volkenroda-Komplexes | nein | ja | teils | nein | nicht gewertet | — | — | — | — | nicht Teil der Reuse-Bewertung | gmp-de | Details |

---

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Pavillon als demontierbares modulares System geplant | gmp, Auftraggeber | Design for disassembly mit realem Wiedereinbau | unbekannt | — | — | unbekannt | späterer Standort von Anfang an vorgesehen | Expo-Temporarität | Translozierungskonzept | gmp / Kloster |
| Bauteilinventar | Ensemble/Module für Abbau und Wiederaufbau identifiziert | unbekannt | modulare Fügung | unbekannt | — | — | unbekannt | Wiederaufbau in gleicher Fügung | genaue Modulnummerierung unbekannt | gleiche Reihenfolge/Fügung | gmp |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | — | — | unbekannt | — | unbekannt | unbekannt | — |
| Rückbau | Abbau nach EXPO 2000 | unbekannt | Demontage statt Abriss | unbekannt | Demontage | unbekannt | unbekannt | Verpackung/Transport nach Thüringen | Bruch/Schäden | modulare Konstruktion | gmp / Kloster |
| Ausbau | Entnahme der Bauteile/Module | unbekannt | unbekannt | unbekannt | demontierbar | unbekannt | unbekannt | unbekannt | Marmor/Glas empfindlich | unbekannt | gmp |
| Transport | Hannover → Volkenroda | unbekannt | Schwer-/Bauteiltransport | unbekannt | — | — | unbekannt | ex-situ Verlagerung | Entfernung und Schutz der Bauteile | unbekannt | gmp / Kloster |
| Lagerung | unbekannt | unbekannt | unbekannt | unbekannt | — | — | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Aufbereitung | unbekannt | unbekannt | Reinigung/Reparatur anzunehmen, nicht belegt | unbekannt | — | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Planung | Integration in Kloster Volkenroda | gmp / Klosterakteure | Anpassung des Ensembles an Kloster | unbekannt | — | — | unbekannt | Standortplanung | historischer Kontext | moderner Kreuzgang ergänzt Kloster | gmp / Felger / Kloster |
| Genehmigung | unbekannt | unbekannt | unbekannt | unbekannt | — | — | unbekannt | — | Kirchen-/Versammlungsnutzung | unbekannt | — |
| Wiedereinbau | Wiederaufbau in gleicher Fügung | unbekannt | modulare Reassemblierung | unbekannt | — | Wiedermontage | unbekannt | Baustelle Volkenroda | genaue Montage unbekannt | Fertigstellung August 2001 | gmp |
| Monitoring | spätere Untersuchung von Fensterschäden | Bauhaus-Uni, EKD Institut, Jesus-Bruderschaft | Quellenrecherche/Bestandsdokumentation | unbekannt | — | Instandsetzungsansätze | Bestandsdokumentation | — | Witterungsschäden | Neugestaltung/Instandsetzung diskutiert | Bauhaus Uni |

---

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | modularer Stahlbau mit neun Stützen im Christusraum | Standsicherheit, Dachlasten | unbekannt | unbekannt | Demontage-/Wiederaufbauanschlüsse | modulares System | gmp |
| Lastabtragung | Dach über Christusraum durch neun schlanke kreuzförmige Stützen | Dach-/Wind-/Nutzlasten | unbekannt | unbekannt | Wiederherstellung gleicher Lastpfade | Wiederaufbau in gleicher Fügung | gmp |
| Verbindung | modular, demontier- und wieder zusammensetzbar | lösbare und erneut tragfähige Verbindungen | unbekannt | unbekannt | genaue Verbindungsmittel unbekannt | modulare Fügung | gmp |
| Brandschutz | unbekannt | Kirchen-/Versammlungsraum | unbekannt | unbekannt | Stahl-/Glasbau | unbekannt | — |
| Schallschutz | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Feuchte | Glas-/Marmorhülle und Fenstervitrinen witterungsausgesetzt | Witterungsschutz | unbekannt | Bauhaus-Uni thematisiert Schäden | Schäden nach 20 Jahren | Instandsetzungs-/Neugestaltungsansätze | Bauhaus Uni |
| Wärmeschutz | unbekannt | Nutzung als Kirche/Kulturort | unbekannt | unbekannt | Glas-/Stahlhülle | unbekannt | — |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | Stahl-Glas-Konstruktion | unbekannt | — |
| Luftdichtheit | unbekannt | unbekannt | unbekannt | unbekannt | modulare Fugen | unbekannt | — |
| TGA-Integration | unbekannt | Kirchenbetrieb | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Barrierefreiheit | unbekannt | öffentlicher Zugang | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Dauerhaftigkeit | seit 2001 in Volkenroda in Nutzung | Dauerhafte Nutzung | unbekannt | Bestands-/Denkmalpflegearbeiten | Fenstervitrinen geschädigt | Instandsetzung/Neugestaltung | Kloster / Bauhaus Uni |
| Wartung | Fenstervitrinen müssen nach 20 Jahren betrachtet werden | Wartbarkeit | unbekannt | Bestandsdokumentation | Witterung | Kooperation EKD/Bauhaus/Jesus-Bruderschaft | Bauhaus Uni |
| Zulassung | unbekannt | Wiedererrichtung und Nutzung | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Haftung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |

---

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Wettbewerb | 1997 | Jahr | Projektdaten | Entwurf | gmp | belegt |
| Bauzeit EXPO | 1999–April 2000 / 1999–2000 | Zeitraum | Projektdaten | Ersterrichtung Hannover | gmp | belegt |
| Wiederaufbau | Februar–August 2001 / Fertigstellung August 2001 | Zeitraum | Projektdaten | Volkenroda | gmp | belegt |
| BGF | 2.004 | m² | Projektdaten | Pavillon | gmp / Structurae | belegt |
| BRI / Volumen | 18.548 | m³ | Projektdaten | Pavillon | gmp / Structurae | belegt |
| Christusraum | ca. 24 × 24 × 18 | m | Projektdaten | Hauptkirchenraum | gmp | belegt |
| Tragstützen Christusraum | 9 | Stück | Projektbeschreibung | Dachtragwerk | gmp | belegt |
| Besucher Expo | 1,8 Mio. | Personen | ntv/dpa-Bericht | Expo-Nutzung | ntv | teilweise belegt |
| Gewicht | 800 | t | ntv/dpa-Bericht | Pavillon | ntv | teilweise belegt |
| wiederverwendete Masse | unbekannt | t | — | Direct-Reuse-Bauteile | — | unklar |
| CO₂-Einsparung | unbekannt | kg CO₂e | — | — | — | unklar |
| Kosten | unbekannt | EUR | — | — | — | unklar |
| Zirkularitätskennwert | unbekannt | — | — | — | — | unklar |

---

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Translozierung eines kompletten Pavillons | logistisch/technisch | großes, empfindliches Stahl-Glas-Marmor-Ensemble | hohe Anforderungen an Demontage, Transport, Wiederaufbau | Bauteil, Logistik, Verbindung | modularer Entwurf, Wiederaufbau in gleicher Fügung | DfD zählt erst als Reuse, wenn Wiedereinbau tatsächlich erfolgt | gmp |
| Empfindliche Hülle | technisch | Marmor-/Glasflächen, Vitrinen | Bruch-/Witterungsrisiken | Hülle, Material, Dauerhaftigkeit | unbekannt; spätere Instandsetzungsansätze | Hüllenreuse braucht Wartungsstrategie | gmp / Bauhaus Uni |
| Nachnutzung nach Expo | organisatorisch/sozial | temporäre Bauaufgabe braucht zweiten Standort | Risiko temporärer Abfallarchitektur | Projekt, Ort, Wirtschaft | Standort Volkenroda von Anfang an geplant | Nachnutzung muss vor Errichtung geklärt sein | Kloster / gmp |
| Instandhaltung nach 20 Jahren | technisch/kulturell | Witterungsschäden an Fenstervitrinen | Sanierungsbedarf | Wartung, Denkmalwert | Kooperation für Neugestaltung/Untersuchung | Reuse endet nicht beim Wiedereinbau | Bauhaus Uni |
| Bewertung als Hauptfall | methodisch | Pavillon/Expo-Logik statt Regelbau | nicht mit dauerhaften Wohn-/Gewerbebauten gleichsetzen | Fallstudie, Projektstatus | Anhang/Vergleichsfall | Kategorien nach Maßstab trennen | eigene Einordnung |

---

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** Auftrag für EXPO-Pavillon mit geplanter Nachnutzung; kein Bauteilbörsenmodell.  
- **Bauteilbörse / Quelle:** keine; Quelle war das gesamte vorhandene Pavillonensemble aus Hannover.  
- **Kostenwirkung:** unbekannt.  
- **Zeitwirkung:** Wiederaufbau 2001 innerhalb weniger Monate laut gmp-Zeitraum; genaue Demontage-/Transportzeit unbekannt.  
- **Versicherung / Haftung:** unbekannt.  
- **Gewährleistung:** unbekannt.  
- **Arbeitsaufwand:** hoch, da kompletter Abbau und Wiederaufbau eines empfindlichen Pavillons; genaue Werte unbekannt.  
- **Lagerung:** unbekannt.  
- **Marktbarrieren:** seltene Gelegenheit, hoher Planungsaufwand, transport- und montageabhängige Risiken, Nachnutzung muss gesichert sein.

---

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** hoch im Sinne der vollständigen Translozierung; am neuen Ort ist die Expo-Herkunft Teil der Identität.  
- **räumliche Transformation:** temporärer Expo-Pavillon wird dauerhafter Teil eines ehemaligen Zisterzienserklosters.  
- **Atmosphäre / Ausdruck:** reduziertes modulares System aus Stahl, Sichtbeton, Glas und transluzentem Marmor; kontemplativer Christusraum.  
- **Umgang mit Spuren:** EXPO-Identität bleibt als Erinnerung an die Weltausstellung erhalten.  
- **sozialer Wert:** kirchlicher, kultureller und touristischer Ort; laut Kloster Bestandteil des wiedererstandenen Klosters.  
- **Denkmal- oder Bestandswert:** Denkmalwert wird universitär untersucht; formaler Status unbekannt.  
- **Kritik / Grenzen:** DfD war Teil des Ursprungskonzepts; als Direct Reuse zählt hier nur, dass der Wiederaufbau tatsächlich erfolgte. Kein Regelbau-Hauptfall.

---

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** Tragwerksplaner, statische Prüfberichte, Montage-/Demontageplan, Transportdetails, Verbindungsmittel, Kosten, CO₂-Bilanz, Gewährleistung, formaler Denkmalstatus.  
- **Sinnvolle neue Entitäten:** Translozierung; Wiederaufbau in gleicher Fügung; temporärer Erstnutzer; Nachnutzungsort.  
- **Fehlende Daten:** Bauteilanzahl, Masse nach Material, konkrete wiederverwendete vs. neu ergänzte Bauteile, Instandsetzungskosten, heutiger Zustand aller Bauteile.  
- **Zu prüfende Quellen:** gmp-Archiv, Bauakten Volkenroda, Kirchenbauinstitut Marburg, Bauhaus-Uni-Dokumentation, Expo-2000-Projektunterlagen.

---

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** Anhang / Vergleichsfall  
- **5 wichtigste Fakten:**  
  1. EXPO-2000-Pavillon wurde in Volkenroda wiederaufgebaut.  
  2. gmp beschreibt Abbau und Wiederaufbau in gleicher Fügung.  
  3. BGF 2.004 m², BRI 18.548 m³.  
  4. Hauptmaterialien: Stahl, Sichtbeton, Glas, Marmor.  
  5. Dach des Christusraums wird von neun kreuzförmigen Stützen getragen.  
- **5 wichtigste Bauteile:**  
  1. Stahltragwerk  
  2. neun kreuzförmige Stützen  
  3. Marmor-Glas-Hülle  
  4. Kreuzgang/Stahl-Glas-Fassade  
  5. Sichtbetonteile  
- **5 wichtigste Hürden:**  
  1. vollständige Demontage und Wiederaufbau  
  2. empfindliche Glas-/Marmorbauteile  
  3. Transportlogistik Hannover–Volkenroda  
  4. spätere Witterungsschäden an Vitrinen  
  5. klare Abgrenzung von DfD zu tatsächlichem Reuse  
- **5 wichtigste übertragbare Erkenntnisse:**  
  1. Temporäre Architektur kann durch geplante Zweitnutzung Abfall vermeiden.  
  2. Modulare Fügung ist wertvoll, wenn sie wirklich zum Wiederaufbau führt.  
  3. Gesamtgebäude-Translozierung ist eine eigene Reuse-Kategorie.  
  4. Hüllen-/Fensterbauteile brauchen langfristige Wartungsstrategien.  
  5. Kultureller Wert kann die Akzeptanz von Reuse erhöhen.  
- **5 offene Fragen:**  
  1. Welche Verbindungsmittel wurden wiederverwendet oder ersetzt?  
  2. Welche Bauteile wurden neu ergänzt?  
  3. Welche Kosten hatte der Wiederaufbau?  
  4. Welche Prüfungen/Genehmigungen waren nötig?  
  5. Wie ist der aktuelle Sanierungsstand der Fenstervitrinen?

---

## QUELLEN UND LINKS

1. gmp Architekten: Christ Pavilion, Expo 2000. https://www.gmp.de/en/projects/415/christ-pavilion-expo-2000  
2. gmp Architekten Deutsch: Christus-Pavillon, Expo 2000. https://www.gmp.de/de/projekte/415/christus-pavillon-expo-2000  
3. Kloster Volkenroda: Christus-Pavillon. https://www.kloster-volkenroda.de/christus-pavillon/  
4. Structurae: Christus-Pavillon. https://structurae.net/de/bauwerke/christus-pavillon  
5. Bauhaus-Universität Weimar: Christus-Pavillon Volkenroda. https://www.uni-weimar.de/de/architektur-und-urbanistik/professuren/denkmalpflege-und-baugeschichte/lehre/vergangene-semester/winter-201920/thesisarbeiten/christus-pavillon/  
6. Bauhaus-Universität Weimar: Zukunftsvisionen zur Fenstergestaltung. https://www.uni-weimar.de/de/architektur-und-urbanistik/aktuell/publikationen/zukunftsvisionen/  
7. Andreas Felger Kulturstiftung: Kammern EXPO 2000 Christus Pavillon. https://www.af-kulturstiftung.de/werkzyklen/kammern-expo-2000-christus-pavillon/  
8. ntv/dpa: Expo-Kirche ist Christus-Pavillon. https://www.n-tv.de/reise/Expo-Kirche-ist-Christus-Pavillon-article4050336.html
