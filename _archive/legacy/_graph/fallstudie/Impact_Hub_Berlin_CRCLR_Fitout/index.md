---
id: "Impact_Hub_Berlin_CRCLR_Fitout"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "Impact Hub Berlin Interior / CRCLR Fit-out – Fallstudie Direct Reuse / zirkuläres Bauen"
bauobjekt:
  - "Impact_Hub_Berlin_CRCLR_Fitout"
legacy_paths:
  - "Gebäude\\Impact_Hub_Berlin_CRCLR_Fitout.md"
projekt:
  - "Impact_Hub_Berlin_CRCLR_Fitout"
reuse_chain_detected: "False"
---
# Impact Hub Berlin Interior / CRCLR Fit-out – Fallstudie Direct Reuse / zirkuläres Bauen

## Migration

- Fallstudie ID: Impact_Hub_Berlin_CRCLR_Fitout
- Legacy source count: 1
- Generated project: Impact_Hub_Berlin_CRCLR_Fitout
- Generated bauobjekt: Impact_Hub_Berlin_CRCLR_Fitout
- Extracted reuse_einsatz rows: 8
- Extracted datenpunkt rows: 9
- Extracted entity mapping rows: 17
- Reuse chain detected: False

## Legacy Content

### Legacy Source: Gebäude\Impact_Hub_Berlin_CRCLR_Fitout.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Impact_Hub_Berlin_CRCLR_Fitout
- Secondary targets: projekt/Impact_Hub_Berlin_CRCLR_Fitout; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Impact Hub Berlin Interior / CRCLR Fit-out – Fallstudie Direct Reuse / zirkuläres Bauen

**Projekt:** Impact Hub Berlin at CRCLR House, Innenausbau / Fit-out  
**Bearbeitung:** Deutsch, kompakt, quellenbasiert  
**Grundregel:** Gezählt werden nur wiederverwendete Bau-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Bestandserhalt und lose Möbel werden nicht als Direct Reuse gewertet.

---

## 1. EINORDNUNG

- **Entscheidung:** ANHANG / niedriger VERGLEICHSFALL
- **Bewertung:** ★★☆☆☆
- **Begründung:** Der Innenausbau des Impact Hub Berlin ist ein belegter zirkulärer Fit-out mit wiederverwendeten und recycelten Materialien, Produkt-/Materialpässen und demontierbaren Strukturen. Für Direct Reuse zählen hier nur feste Einbauten wie Wandpaneele, Schrank-/Wandflächen, Telefonboxen/Booth-Elemente und andere räumliche Bauteile. Viele publizierte Beispiele sind Möbel oder Recycling/Upcycling und werden nicht gewertet. Der tragende CRCLR-House-Reuse-Kern wurde bereits als eigener Fall behandelt; dieser Eintrag ist daher ein ergänzender Innenausbau-Fall.
- **Vertrauensgrad:** teilweise belegt
- **Warnung Bestandserhalt:** ja
- **Warnung Möbel/Dekoration:** ja
- **Projektstatus:** gebaut

---

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Impact Hub Berlin Interior / CRCLR fit-out | Innenausbau im CRCLR House | S1–S4 | belegt | Abgrenzung zu CRCLR-Hauptgebäude nötig |
| Gebäude | CRCLR House, ehemalige Kindl-Brauerei | Einbauort / Transformation | S1, S3 | belegt | Bestandserhalt nicht zählen |
| Ort | Berlin-Neukölln | Standort | S1–S4 | belegt | auf Kindl-Areal |
| Projekt | Coworking- und Community-Space | neue Nutzung | S1, S3, S4 | belegt | 3.500 m² oder 4.871 m² je Betrachtung |
| People | Impact Hub Berlin, LXSY Architektur, TRNSFRM eG, Die Zusammenarbeiter, ZRS Ingenieure | Nutzer, Innenarchitektur, Projektentwicklung/Architektur, Tragwerksplanung im Gesamtprojekt | S1, S2 | belegt | Fit-out-Fokus auf LXSY |
| Bauteil | red MDF boards und Ziegel aus anderer Baustelle | feste Rezeption / Treffpunkte laut UBM | S3 | teilweise belegt | direkte Bauteilfunktion nur teilweise klar |
| Bauteil | schwarze MDF-Platten | Schranktüren und Wandpaneele | S3 | belegt | aus Boros/Berghain-Ausstellung |
| Bauteil | Holzlatten aus Tischlereiresten | Telefonboxen | S3 | teilweise belegt | Offcuts; zählt als festes räumliches Element, wenn eingebaut |
| Bauteil | Filzpaneele | Schallschutz in Telefonboxen | S3 | teilweise belegt | recycelt, nicht zwingend direct reuse |
| Bauteil | Holzgalerie | Raumteilung / zweite Ebene | S2 | teilweise belegt | Wiederverwendung nicht belegt; daher nicht als Reuse gezählt |
| Methode | Design for Disassembly | demontierbarer Innenausbau | S2, S4 | belegt | nur ergänzend, zählt ohne Reuse nicht allein |
| Datenmodell | Produkt- und Materialpässe | spätere Wiederverwendung | S2 | belegt | Details unbekannt |
| Software | Concular / Restado | Materialsuche im Gesamtprojekt CRCLR | S1 | teilweise belegt | betrifft Gesamtprojekt, nicht jedes Interior-Element |
| Kennwert | ca. 70 % recycled or sustainable | Material-/Produktanteil nach LXSY/UBM | S2, S3 | belegt | nicht gleich 70 % Direct Reuse |
| Kennwert | 80 % sustainable/recycled/upcycled | Impact Hub-eigene Darstellung | S4 | teilweise belegt | abweichende Quote |
| Hürde | Zulassung / Brandschutz / Anforderungen | Türen, Öffnungen, Reuse-Komponenten im Gesamtprojekt | S1 | belegt | überwiegend Gesamtprojekt |
| Prüfung | Zugversuche / chemische Analysen für Stahl | Gesamtprojekt CRCLR, nicht Fit-out | S1 | belegt | hier nur Kontext |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Fit-out-Reuse | Innenausbau hat eigene Logik zwischen Möbel und Bauwerk | feste Wandpaneele, Telefonboxen, Rezeption | Bauteil, Reuse-Strategie, Gestaltung |
| Offcut-Verwertung | Reststücke sind keine klassischen Bauteile, können aber feste Bauteile bilden | Holzlatten aus Tischlereien | Material, Aufbereitungsmethode |
| Produktpass | Objektbezogene Dokumentation für Innenausbau | Produkt- und Materialpässe | Datenmodell, Dokument, Bauteil |

---

## 3. FALLSTUDIE

- **Name:** Impact Hub Berlin at CRCLR-House / Interior Fit-out
- **Ort:** Berlin-Neukölln, Deutschland
- **Gebäude:** CRCLR House auf dem ehemaligen Kindl-Brauereigelände
- **Projekt:** Coworking-, Community-, Event- und Arbeitsflächen mit zirkulärem Innenausbau
- **Beteiligte People / Akteure:** Impact Hub Berlin, LXSY Architektur, TRNSFRM eG, Die Zusammenarbeiter, ZRS Ingenieure; weitere Handwerksbetriebe/Community unbekannt
- **Architekt:** LXSY Architektur für Innenausbau; TRNSFRM eG / Die Zusammenarbeiter für Gesamtprojekt
- **Tragwerksplaner:** ZRS Ingenieure im Gesamtprojekt; für Fit-out unbekannt
- **Bauherr:** TRNSFRM eG / Nutzer Impact Hub Berlin; genaue Vertragsstruktur unbekannt
- **Zeitraum:** Bauzeit CRCLR 2019–2024; Impact Hub eröffnete am Standort 2022
- **Ursprüngliche Nutzung:** Lager-/Industriegebäude der ehemaligen Kindl-Brauerei
- **Neue Nutzung:** Coworking, Team Offices, Eventflächen, Labs, Maker Space
- **Fläche / Maßstab:** 3.500 m² Impact Hub nach eigener Quelle; 4.871 m² CRCLR-Gesamtfall nach Circular Material Systems
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** gut für Gestaltungskonzept und einige Materialien; unklar für genaue Mengen, Prüfungen und Direct-Reuse-Anteile im Fit-out

---

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; fester Innenausbau; Bauteilwiederverwendung; Materialwiederverwendung; Upcycling; Design for Disassembly
- **Hauptniveau:** räumlicher Innenausbau
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Der Erhalt des Brauereibestands und der tragende Reuse im CRCLR House werden nicht hier bewertet. Recycelte Materialien und Möbel werden separat geführt. Direct Reuse zählt nur bei festen, wieder eingebauten Raum- oder Konstruktionselementen.
- **Warum ist der Fall relevant?** Er zeigt die Grauzone zwischen zirkulärem Interior, Möbel, Upcycling und baulichem Reuse. Für diese Liste ist er nur relevant, wenn feste räumliche Elemente betrachtet werden.

---

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Schwarze MDF-Platten | MDF | Boros Foundation Ausstellung im Berghain-Kontext | Ausstellungsbau / Platten | Schranktüren und Wandpaneele | unbekannt | nein | ja | nein | nein | Zuschnitt, Montage | geschraubt/vermutlich trocken, Details unbekannt | unbekannt | Brandschutz, Oberflächen, Stabilität | unbekannt | Brandschutz nicht dokumentiert | S3 | Menge, Plattentyp |
| Red MDF boards | MDF | andere Baustelle | unbekannt | Rezeption / Treffpunktzone | unbekannt | nein | ja | nein | nein | unbekannt | unbekannt | unbekannt | Oberflächen/Brandschutz | unbekannt | Funktion nicht vollständig klar | S3 | Menge |
| Ziegel im Empfang | Ziegel | andere Baustelle | unbekannt | Empfangs-/Treffpunktgestaltung | unbekannt | nein | ja | nein | nein | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | bauliche Funktion unklar | S3 | Menge |
| Holzlatten | Holz-Offcuts | verschiedene Tischlereien | Produktionsrest | Telefonboxen | unbekannt | nein | ja | nein | nein | Zuschnitt / Montage | unbekannt | unbekannt | Akustik, Stabilität | unbekannt | Offcuts statt Bauteilreuse | S3 | Menge |
| Filzpaneele | recycelter Filz | unbekannt | unbekannt | Schallabsorption Telefonboxen | unbekannt | nein | ja | nein | nein | Recycling/Einbau | unbekannt | unbekannt | Akustik, Brandschutz | unbekannt | nicht direct reuse, eher Recycling | S3 | Herkunft |
| Holzgalerie | Holz | unbekannt | unbekannt | zweite Ebene / Raumstruktur | unbekannt | ja / räumlich tragend im Innenausbau | ja | nein | nein | unbekannt | unbekannt | unbekannt | Standsicherheit | unbekannt | Wiederverwendung nicht belegt | S2 | ob reused |
| Türen/Fenster/Sanitär | diverse | Gesamtprojekt CRCLR, Quellen nennen reused doors/windows/sanitary | Altbauteile | neue Gebäude-/Innenbauteile | unbekannt | nein | ja/technisch | ja/innen | ja | refurbishment | unbekannt | teils schwierig wegen Brandschutz/Energie | Brandschutz/Energie | unbekannt | Reuse-Bauteile im Gesamtprojekt, Fit-out-Zuordnung unscharf | S1 | Einbauorte |
| Möbel | diverse | Clearance / reuse | Möbel | Möbel | unbekannt | nein | nein | nein | nein | aufgearbeitet | nicht relevant | nicht relevant | nicht relevant | nicht relevant | zählt nicht | S3, S4 | nicht bewertet |

---

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Nutzungsanforderungen und Bestand prüfen | Impact Hub, LXSY, TRNSFRM | partizipatives Design | unbekannt | nicht zutreffend | unbekannt | unbekannt | im Bestandsgebäude | Bestand und Fluchtwege | flexible Raumgrößen | S2 |
| Bauteilinventar | Material- und Produktpässe anlegen | LXSY / Projektteam | Dokumentation | Produkt-/Materialpässe | nicht zutreffend | nicht zutreffend | unbekannt | digital | spätere Wiederverwendung | Pässe | S2 |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Altindustriegebäude möglich | unbekannt | unbekannt |
| Rückbau | Material von anderen Baustellen/Ausstellungen übernehmen | unbekannt | Materialsuche | Concular/Restado im Gesamtprojekt | selektiv / unbekannt | unbekannt | unbekannt | Berlin / informelle Kontakte | Verfügbarkeit | materialbasierte Planung | S1, S3 |
| Ausbau | Innenausbau aus wiederverwendeten/recycelten/sustainable Materialien | LXSY, Handwerk, Nutzer | demontierbar, sortenrein | Produktpässe | nicht zutreffend | Zuschnitt, Upcycling | unbekannt | Baustellenkoordination | Material passt nicht exakt | 62,5-cm-Raster für Reststücke | S2, S3 |
| Transport | Materialien aus Berlin/Umfeld anliefern | Projektteam | Einzellogistik | unbekannt | nicht zutreffend | unbekannt | unbekannt | einzelne Lieferungen | komplex | detaillierte Anweisungen / Lagerung im Gesamtprojekt | S1 |
| Lagerung | Reuse-Komponenten trocken und geschützt lagern | Projektteam | temporäre Lagerung | unbekannt | nicht zutreffend | unbekannt | unbekannt | Lager nahe Baustelle wichtig | Beschädigung / Timing | Lagerflächen sichern | S1 |
| Aufbereitung | Platten, Offcuts, Möbel / Paneele anpassen | LXSY/Handwerk | Upcycling, Reparatur | Werkstatt | nicht zutreffend | Zuschnitt, Montage | unbekannt | unbekannt | heterogene Qualität | Gestaltung nutzt Materialgeschichte | S3 |
| Planung | Entwurf nach Flexibilität und verfügbaren Materialien | LXSY | material-as-found, upcycling | unbekannt | nicht zutreffend | nicht zutreffend | unbekannt | unbekannt | feste Raster, Fluchtwege | flexible Raumgrößen | S2, S3 |
| Genehmigung | Brandschutz/Energie/Barrierefreiheit berücksichtigen | Projektteam | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Türen/Öffnungen im Gesamtprojekt | teils neue Bauteile nötig | S1 |
| Wiedereinbau | Paneele, Schranktüren, Telefonboxen, Innenwände montieren | LXSY/Handwerk | trockene / reversible Montage | unbekannt | nicht zutreffend | Montage | unbekannt | Innenausbau | Gewährleistung | unbekannt | S2, S3 |
| Monitoring | Räume als Circular Space Tours zeigen | Impact Hub Berlin | didaktische Vermittlung | unbekannt | nicht zutreffend | nicht zutreffend | unbekannt | Betrieb | Wissensvermittlung | Führungen | S4 |

---

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Interior-Fall nicht tragwerkszentral | unbekannt | unbekannt | unbekannt | tragender Reuse separat im CRCLR-Gesamtfall | Abgrenzung | S1 |
| Lastabtragung | Holzgalerie als Innenstruktur erwähnt, Reuse unklar | Standsicherheit | unbekannt | unbekannt | keine Reuse-Belege | nicht als Reuse zählen | S2 |
| Verbindung | demontierbare, sortenreine Konstruktionen | Rückbaubarkeit | unbekannt | unbekannt | Reuse + spätere Demontage | Produkt-/Materialpässe | S2 |
| Brandschutz | CRCLR-Quelle nennt Türen/Öffnungen als Brandschutzhürde | Brandschutz | unbekannt | unbekannt | gebrauchte Türen teils problematisch | teilweise neue Bauteile / Anpassung | S1 |
| Schallschutz | Telefonboxen mit recycelten Filzpaneelen | Akustik | unbekannt | unbekannt | Materialheterogenität | Filzpaneele | S3 |
| Feuchte | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Wärmeschutz | Innenausbau, nicht Hauptthema | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Luftdichtheit | unbekannt | unbekannt | unbekannt | unbekannt | Innenausbau | unbekannt | unbekannt |
| TGA-Integration | Maker Space / Labs, Details unbekannt | Betriebssicherheit | unbekannt | unbekannt | unbekannt | unbekannt | S4 |
| Barrierefreiheit | LXSY nennt Zugänglichkeit als Entwicklungsaspekt | Barrierefreiheit | unbekannt | unbekannt | Bestand / Galerie | unbekannt | S2 |
| Dauerhaftigkeit | wiederverwendete Platten und Einbauten | Nutzung im Büro | unbekannt | unbekannt | Patina und Gebrauchsspuren | gestalterisch integriert | S3 |
| Wartung | Innenausbau demontierbar | Austauschbarkeit | unbekannt | unbekannt | keine zerstörungsfreie Wartung? | demontierbare Details | S2, S4 |
| Zulassung | unbekannt | unbekannt | unbekannt | unbekannt | gebrauchte Bauteile | unbekannt | S1 |
| Haftung | Gesamtprojekt nennt Gewährleistung als Thema | unbekannt | unbekannt | unbekannt | wenige Firmen übernehmen Haftung | unbekannt | S1 |

---

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Impact Hub Fläche | 3.500 | m² | Eigenangabe Impact Hub | Coworking-Space | S4 | belegt |
| CRCLR-Gesamtfläche | 4.871 | m² | Case-Study-Angabe | Gesamtgebäude | S1 | belegt |
| Arbeitsplätze | 100+ | Stück | Case-Study-Angabe | Nutzung | S1 | belegt |
| Materialanteil recycled/sustainable | ca. 70 | % | LXSY/UBM-Angabe | Innenausbau | S2, S3 | belegt, nicht Direct Reuse |
| Materialanteil sustainable/recycled/upcycled | 80 | % | Impact-Hub-Angabe | Impact Hub / CRCLR Space | S4 | teilweise belegt |
| Direct-Reuse-Masse | unbekannt | t | unbekannt | Fit-out | unbekannt | unbekannt |
| CO₂-Einsparung | unbekannt | unbekannt | unbekannt | Fit-out | unbekannt | unbekannt |
| Kosten | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Bauzeit Interior | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |

---

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Möbel vs feste Bauteile | methodisch | viele publizierte Beispiele sind Möbel | Überbewertung möglich | Bauteil, Bewertung | nur Wandpaneele, Trenn-/Raumelemente zählen | Interior-Reuse sauber abgrenzen | S3, S4 |
| Unklare Direct-Reuse-Quote | wissenschaftlich | 70/80 % umfassen recycelt/sustainable/upcycled | kein Reuse-Kennwert | Kennwert | als „nicht Direct Reuse“ markieren | Kennwerte genau definieren | S2–S4 |
| Brandschutz | technisch/rechtlich | gebrauchte Türen/Öffnungen im Gesamtprojekt | Bauteile konnten nicht immer wiederverwendet werden | Recht, Prüfung | teilweise neue Bauteile | Brandschutz früh prüfen | S1 |
| Materialverfügbarkeit | logistisch | Baustellenquellen und Reststücke | Entwurf abhängig vom Fund | Bauteil, Methode | 62,5-cm-Raster / flexible Planung | Raster an Reststücke anpassen | S3 |
| Haftung | rechtlich/wirtschaftlich | gebrauchte Bauteile ohne Standardgarantie | Firmen schwer zu finden | Prüfung, Wirtschaft | Expert*innenpool | Haftungsketten aufbauen | S1 |
| Lagerung/Timing | logistisch | Materialien verfügbar, bevor sie eingebaut werden | Lagerkosten und Beschädigungsrisiko | Logistik | trockene Lagerung nahe Baustelle | Logistik als Entwurfsparameter | S1 |

---

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** Materialsuche über Baustellen, informelle Kontakte, Plattformen im Gesamtprojekt; Nutzung vorhandener Reststücke und gebrauchter Materialien.
- **Bauteilbörse / Quelle:** Concular / Restado im CRCLR-Gesamtprojekt; konkrete Interior-Bauteilbörse pro Bauteil unbekannt.
- **Kostenwirkung:** Gesamtprojekt versuchte, gebrauchte Materialien deutlich günstiger als neue zu beziehen; Mehrkosten durch Logistik und Vorbereitung werden genannt, aber keine Zahlen für Fit-out.
- **Zeitwirkung:** unbekannt.
- **Versicherung / Haftung:** Haftung bei wiederverwendeten Komponenten öffentlich als Herausforderung genannt, konkrete Lösung unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** hoch durch Suche, Zuschnitt, Prototyping und Einbau; genaue Stunden unbekannt.
- **Lagerung:** trocken und baustellennah wichtig; konkrete Fit-out-Lagerung unbekannt.
- **Marktbarrieren:** Brandschutz, Gewährleistung, Verfügbarkeit, Planungsänderungen, Unschärfe zwischen Reuse/Recycling/Möbel.

---

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** hoch bei MDF-/Wandpaneelen, Rezeption, Telefonboxen und Materialcollagen.
- **räumliche Transformation:** ehemaliges Lager/Industriegebäude wird Coworking- und Community-Space.
- **Atmosphäre / Ausdruck:** zirkuläre Ästhetik soll nicht „second-hand minderwertig“ wirken, sondern hochwertig und offen.
- **Umgang mit Spuren:** Materialgeschichte wird sichtbar gemacht; „as found“ und Upcycling sind Teil des Konzepts.
- **sozialer Wert:** Coworking-Community für Circular Economy, Social Impact und Green Tech.
- **Denkmal- oder Bestandswert:** ehemaliges Kindl-Areal; Schutzstatus unbekannt.
- **Kritik / Grenzen:** als Direct-Reuse-Fall nur eingeschränkt belastbar, da viele Bauteile recycelt, neu nachhaltig oder Möbel sind.

---

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** genaue Normen, Prüfberichte, Mengen je Bauteil, Gewährleistung, Kosten, detailliertes Bauteilinventar.
- **Welche neuen Entitäten wären sinnvoll?** Fit-out-Reuse; Offcut-Verwertung; Produktpass.
- **Welche Daten fehlen?** Masse/Anzahl der wiederverwendeten festen Bauteile, Einbauorte, Brandschutzklassen, Schallschutzwerte, Montage-/Verbindungssysteme.
- **Welche Quellen müssten geprüft werden?** LXSY-Ausführungspläne, Materialpässe, Impact-Hub-Tourmaterialien, Bauteillisten, Brandschutzkonzept.

---

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** Anhang oder niedriger Vergleichsfall; nicht als eigenständiger Hauptfall neben CRCLR House.
- **5 wichtigste Fakten:**
  1. Der Impact Hub Berlin eröffnete 2022 im CRCLR House.
  2. Der Innenausbau wurde von LXSY als zirkulärer Fit-out beschrieben.
  3. Rund 70 % der Materialien/Produkte werden als recycled oder sustainable angegeben.
  4. Feste wiederverwendete Wand-/Schrank-/Telefonboxelemente sind relevant, Möbel nicht.
  5. Der Fall überschneidet sich mit dem CRCLR-House-Gesamtfall.
- **5 wichtigste Bauteile:**
  1. schwarze MDF-Platten als Schranktüren/Wandpaneele.
  2. red MDF boards / Empfangselemente.
  3. Holzlatten aus Offcuts für Telefonboxen.
  4. Filzpaneele für Akustik, eher Recycling.
  5. Türen/Fenster/Sanitär im Gesamtprojekt, Fit-out-Zuordnung unklar.
- **5 wichtigste Hürden:**
  1. Abgrenzung Möbel vs feste Bauteile.
  2. Brandschutz und Öffnungsmaße.
  3. Verfügbarkeit passender Materialien.
  4. Haftung/Gewährleistung.
  5. Kennwertunschärfe.
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Interior-Reuse braucht eigene Bewertungsregeln.
  2. Materialpässe sind auch im Innenausbau sinnvoll.
  3. Rasterplanung kann Reststücke nutzbar machen.
  4. Sichtbare Patina kann hochwertig gestaltet werden.
  5. Reuse, Recycling und nachhaltige Neumaterialien müssen getrennt bilanziert werden.
- **5 offene Fragen:**
  1. Welche Bauteile sind tatsächlich Direct Reuse und fest eingebaut?
  2. Welche Brandschutzklassen wurden erreicht?
  3. Wie viele Bauteile/Massen wurden wiederverwendet?
  4. Welche Kosten entstanden durch Logistik und Aufbereitung?
  5. Welche Daten stehen in den Produkt-/Materialpässen?

---

## Quellen und Links

- **S1** Circular Material Systems, „CRCLR / Impact Hub Berlin CRCLR House“ – https://circularmaterialsystems.com/en/case/impact-hub-berlin-crclr-house/
- **S2** LXSY Architektur, „Impact Hub Berlin at CRCLR-House“ – https://lxsy.de/en/projects/impact-hub-berlin-at-crclr-house
- **S3** UBM / Timber Peak, „The circular office“ – https://www.timber-peak.de/en/the-circular-office/ ; https://www.ubm-development.com/magazin/en/impact-hub-berlin/
- **S4** Impact Hub Berlin, „Circular space / tours“ und „Celebrating One Year Of CRCLR House“ – https://berlin.impacthub.net/about-us/circular-space/ ; https://berlin.impacthub.net/celebrating-one-year-of-crclr-house/
- **S5** Building Social Ecology, „CRCLR House Berlin“ – https://www.buildingsocialecology.org/projects/crclr-house-berlin/
