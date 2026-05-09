---
id: "Verbiest_Karreveld_Brussels"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "Verbiest + Karreveld, Brüssel / Molenbeek"
bauobjekt:
  - "Verbiest_Karreveld_Brussels"
legacy_paths:
  - "Gebäude\\Verbiest_Karreveld_Brussels.md"
projekt:
  - "Verbiest_Karreveld_Brussels"
reuse_chain_detected: "True"
---
# Verbiest + Karreveld, Brüssel / Molenbeek

## Migration

- Fallstudie ID: Verbiest_Karreveld_Brussels
- Legacy source count: 1
- Generated project: Verbiest_Karreveld_Brussels
- Generated bauobjekt: Verbiest_Karreveld_Brussels
- Extracted reuse_einsatz rows: 13
- Extracted datenpunkt rows: 15
- Extracted entity mapping rows: 30
- Reuse chain detected: True

## Legacy Content

### Legacy Source: Gebäude\Verbiest_Karreveld_Brussels.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Verbiest_Karreveld_Brussels
- Secondary targets: projekt/Verbiest_Karreveld_Brussels; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Verbiest + Karreveld, Brüssel / Molenbeek

**Fallstudie zur Wiederverwendung von Bauteilen / Direct Reuse / zirkulärem Bauen**  
**Stand:** 2026-05-06  
**Bearbeitungssprache:** Deutsch  
**Kurzregel für diese Auswertung:** Diese Datei behandelt zwei eng verwandte AgwA-Projekte als kombinierten Vergleichsfall: **Verbiest** und **Karreveld**. Gezählt werden nur tatsächlich neu eingesetzte oder umgesetzte feste Bauteile; bloßer Bestandserhalt zählt nicht, außer Bauteile werden in veränderter Funktion/Position wieder eingebaut.

---

## 1. EINORDNUNG

- **Entscheidung:** VERGLEICHSFALL  
- **Bewertung:** ★★★☆☆  
- **Begründung:** Beide Projekte belegen in-situ bzw. projektinterne Wiederverwendung fester Bauteile. Karreveld ist besonders relevant durch die dokumentierte Wiederverwendung von ca. 450 m² modularen Innenwänden und ca. 400 m² abgehängten Decken/Leuchten aus dem ehemaligen Bürogebäude. Verbiest belegt wiederverwendete Dach-/Terrassenfliesen, Geländer, Fliesen, Steine und dekorative Fliesen aus anderen Projekten. Gleichzeitig besteht hohe Warnung vor Verwechslung mit normalem Bestandserhalt.
- **Vertrauensgrad:** belegt für Kernbauteile und Flächen bei Karreveld; teilweise belegt für Verbiest-Mengen, Technik, Prüfungen und Rechtsfragen.
- **Warnung Bestandserhalt:** ja – beide sind Umbauten/Transformationen; erhaltene Treppen, Toiletten, technische Schächte und Tragwerke zählen nicht automatisch als Reuse.
- **Warnung Möbel/Dekoration:** nein für die Kernbewertung; dekorative Fliesen sind fest eingebaut und werden gezählt, lose Ausstattung nicht.
- **Projektstatus:** gebaut; Verbiest ca. 2020 abgeschlossen, Karreveld Phase 1 ca. 2019 und Phase 2 ca. 2022.

---

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Verbiest + Karreveld | kombinierter AgwA-Reuse-Vergleichsfall | Q1, Q2, Q3, Q4 | belegt | Opalis listet beide als „Conservation et réemploi (in situ)“ |
| Gebäude | Verbiest | Lagerhaus zu Einfamilienhaus und künstlerischem Atelier | Q1 | belegt | Molenbeek, Brüssel |
| Gebäude | Karreveld | ehemaliges Bürogebäude zu Sekundarschule und Sportzentrum | Q2, Q3, Q5 | belegt | Gentsesteenweg 615, Molenbeek |
| Projekt | Verbiest transformation | Umnutzung eines 1900–1970 errichteten Lagers | Q1 | belegt | fast 1000 m² Bestandsbau, 610 m² Projektfläche |
| Projekt | Karreveld 1/2 | Transformation und Erweiterung einer ehemaligen Büroanlage | Q2, Q3 | belegt | Schule in Phasen |
| Ort | Sint-Jans-Molenbeek / Brüssel | Standort beider Fälle | Q1, Q2, Q5 | belegt | Verbiest und Karreveld in Molenbeek |
| People | AgwA | Architektur beider Projekte | Q1, Q2, Q3 | belegt | Hauptakteur |
| People | Evelia Macal | Mitwirkend bei Verbiest | Q1 | belegt | AgwA + Evelia Macal |
| People | JZH & Partners | Tragwerksplanung / Subcontractor | Q1, Q2, Q3 | belegt | bei beiden Projekten |
| People | Daidalos Peutz, Sixco | Subcontractors Karreveld 1 | Q2 | belegt | genaue Rolle in Quelle nicht ausgeführt |
| People | Kahle Acoustics, Denis Dujardin | Subcontractors Karreveld 2 | Q3 | belegt | Akustik/Landschaft vermutlich, Details unbekannt |
| People | Pouvoir Organisateur Pluriel / POP | Schulträger / Bauherr-Kontext Karreveld | Q7 | belegt | BMA-Ausschreibung |
| Bauteil | modulare Innenwände Karreveld | in situ aus ehemaligem Büro entnommen, gelagert, wiedereingebaut | Q4, Q8 | belegt | ca. 450 m², Phase 1 |
| Bauteil | abgehängte Decke + Leuchten Karreveld | wiederverwendet in Phase 1 | Q4 | belegt | ca. 400 m² |
| Bauteil | bestehende Treppen, Toiletten, technische Schächte Karreveld | erhalten, nicht als Direct Reuse gewertet | Q5 | belegt | Bestandserhalt |
| Bauteil | Dach- und Terrassenfliesen Verbiest | wiederverwendet aus bestehender Konstruktion | Q1 | belegt | Menge unbekannt |
| Bauteil | Geländer, Fliesen, Steine Verbiest | wiederverwendet aus Palais des Expositions in Charleroi | Q1 | belegt | externe Projektquelle |
| Bauteil | dekorative Fliesen Verbiest | wiederverwendet aus altem Projekt in Hanzinelle | Q1 | belegt | teils Chimay-Produktion frühes 20. Jh. |
| Material | Holz, massive Holzbalken/Platten Verbiest | neue Verstärkung statt Beton/Stahl | Q1 | belegt | nicht als Reuse belegt |
| Reuse-Strategie | in-situ transformiert / Bauteilwiederverwendung | Karreveld: innerhalb Gebäude; Verbiest: innerhalb + externe Quellen | Q1, Q4 | belegt | wichtiger Unterschied zu Erhalt |
| Aufbereitungsmethode | Demontage, Zwischenlagerung, Wiedereinbau | Karreveld | Q4 | belegt | Materialien verließen Gebäude nicht |
| Abbruchmethode | sehr begrenzte Demolition / selective deconstruction | Verbiest/Karreveld | Q1, Q3 | teilweise belegt | Detailmethoden unbekannt |
| Prüfung | unbekannt | keine veröffentlichten Prüfprotokolle | unbekannt | unklar | Brandschutz/Schallschutz/Tragfähigkeit fehlen |
| Leistungsanforderung | Schule, Wohnhaus, Atelier | hohe Anforderungen an Brand, Akustik, Hygiene | Q1, Q3, Q5 | teilweise belegt | Normnummern unbekannt |
| Norm/Recht | Belgische / Brüsseler Bauvorschriften, Schulbau, Brandschutz | nicht genauer belegt | unbekannt | unklar | keine Normnummern erfinden |
| Kennwert | Verbiest 610 m² | Projektfläche | Q1 | belegt | Bestandslager fast 1000 m² |
| Kennwert | Karreveld 6.000.000 EUR exkl. MwSt. | Phase-2-Projektkosten, nicht Reuse-Kosten | Q3 | belegt | wirtschaftlicher Kontext |
| Hürde | laufender Schulbetrieb / Phasierung | Karreveld in Nutzung während Transformation | Q3, Q7 | belegt | Baustelle und Schule koexistieren |
| Hürde | Bestandserhalt vs. Direct Reuse | methodische Abgrenzung | Q1, Q5 | belegt | zentrale Warnung |
| Bericht | Verbiest. Approximations | Buch zum Prozess | Q9 | belegt | Quelle zur Prozessreflexion |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| In-situ-Reuse-Kette | Bauteile verlassen das Gebäude nicht, werden aber neu zugeordnet | Karreveld-Innenwände und Decken werden ausgebaut, gelagert, wiedereingebaut | verbindet Logistik, Prozessphase, Bauteil |
| Parallelbetrieb | Umbau bei laufender Nutzung beeinflusst Reuse und Phasing | Karreveld-Schule wächst während Bauphasen | verbindet Logistik, Hürde, Prozessphase |
| Projektübergreifender Materialtransfer | Bauteile stammen von anderer AgwA-/Baustelle | Verbiest nutzt Geländer/Steine vom Palais des Expositions Charleroi | verbindet Projekt, Logistik, Bauteil |

---

## 3. FALLSTUDIE

- **Name:** Verbiest + Karreveld
- **Ort:** Sint-Jans-Molenbeek / Brüssel, Belgien
- **Gebäude:**  
  - Verbiest: ehemaliges Lagerhaus, gebaut zwischen 1900 und 1970, zu Haus und künstlerischem Atelier.  
  - Karreveld: ehemalige Takeda-/Bürogebäude zu Sekundarschule, Sportzentrum und Kantine.
- **Projekt:** adaptive reuse mit dokumentierter Bauteilwiederverwendung
- **Beteiligte People / Akteure:** AgwA; Evelia Macal; JZH & Partners; Daidalos Peutz; Sixco; Kahle Acoustics; Denis Dujardin; POP / Pouvoir Organisateur Pluriel; zwei Nachbargemeinden als Erwerbskontext laut AgwA/WBA
- **Architekt:** AgwA; Verbiest zusätzlich mit Evelia Macal
- **Tragwerksplaner:** JZH & Partners
- **Bauherr:** Verbiest unbekannt; Karreveld: POP / Schulträgerkontext, zwei Nachbargemeinden als Erwerberkontext; genaue Bauherrschaft in Quellen nicht eindeutig
- **Zeitraum:** Verbiest 2018–2020 / Planning 2020; Karreveld Phase 1 2017–2019, Phase 2 bis 2022/2023 je Quelle; Phasierung prüfen
- **Ursprüngliche Nutzung:** Lagerhaus / Bürogebäude
- **Neue Nutzung:** Einfamilienhaus + Atelier / Sekundarschule + Sporthalle + Kantine
- **Fläche / Maßstab:** Verbiest 610 m² Projektfläche, Bestandslager fast 1000 m²; Karreveld-Fläche unbekannt; Phase-2-Kosten 6.000.000 EUR exkl. MwSt.
- **Schutzstatus / Denkmalstatus:** kein formaler Denkmalstatus belegt; AgwA betont nicht-kanonische Bestandswerte
- **Quellenlage:** gut für Projektbeschreibungen und Karreveld-Mengen; lückenhaft für technische Prüfungen, genaue Ausführungsdetails und Reuse-Kosten.

---

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:**  
  - Karreveld: in-situ transformiert, Bauteilwiederverwendung, interne Lagerung und Wiedereinbau.  
  - Verbiest: in-situ und ex-situ Bauteil-/Materialwiederverwendung, adaptive reuse.
- **Hauptniveau:** räumlicher Innenausbau, feste Oberflächen, Gebäudehülle/Boden/Fliesen; nicht primär Tragwerk.
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Erhaltene Tragwerke, Treppen, Toiletten oder technische Schächte zählen nicht, solange sie am Ort bleiben und gleiche Funktion behalten. Gezählt werden nur versetzte/neu integrierte Innenwände, Decken/Leuchten, Fliesen, Geländer, Steine usw.
- **Warum ist der Fall relevant?** Karreveld liefert selten konkrete m²-Angaben zu in-situ wiederverwendeten Ausbau-Bauteilen. Verbiest zeigt eine präzise, baustellennahe Reuse-Haltung mit Verzicht auf unnötige Eingriffe und projektübergreifenden Materialtransfer.

---

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Karreveld Innenwandsystem | Stahlstruktur, weiße Laminatpaneele, Akustikdämmung, Fenster, Innentüren | ehemaliges Bürogebäude Karreveld | Bürotrennwände | Klassenzimmer-/Schultrennwände | ca. 450 m² | nein | ja | nein | nein | ausgebaut, im Gebäude gelagert, wiedereingebaut/angepasst | modular, Details unbekannt | unbekannt | Brandschutz, Schallschutz, Robustheit Schule | belgisches Schul-/Baurecht unbekannt | Phasierung, Schulbetrieb | Q4, Q8 | Prüfungen, genaue Anordnung |
| Karreveld abgehängte Decken + Leuchten | perforiertes Metall, Steinwolle, Leuchten | ehemaliges Bürogebäude | Bürodecke/Beleuchtung | Decke/Beleuchtung in Schule | ca. 400 m² | nein | nein | nein | ja | ausgebaut, gelagert, wiedereingebaut | Deckenabhänger unbekannt | unbekannt | Akustik, Brand, Beleuchtungsniveau, Elektroprüfung | Elektro-/Brandschutzrecht unbekannt | CE/Elektroprüfung unbekannt | Q4 | Prüfungen |
| Karreveld bestehende Treppen | Bestand | Bürogebäude | Treppen | Treppen | unbekannt | ja | ja | nein | nein | erhalten | Bestand | unbekannt | Fluchtwege, Sicherheit | Schul-/Brandschutzrecht | Bestandserhalt, nicht Reuse | Q5 | nicht gezählt |
| Karreveld Toiletten | Bestand | Bürogebäude | Sanitär | Sanitär Schule | unbekannt | nein | ja | nein | ja | erhalten | Bestand | unbekannt | Hygiene, Barrierefreiheit | unbekannt | Bestandserhalt, Nutzungswechsel | Q5 | nicht als Reuse gezählt |
| Karreveld technische Schächte | Bestand | Bürogebäude | technische Versorgung | technische Versorgung | unbekannt | nein | ja | nein | ja | erhalten | Bestand | unbekannt | TGA, Brandschutz | unbekannt | Bestandserhalt | Q5 | nicht gezählt |
| Verbiest Dachfliesen | keramisch/unbekannt | vorhandene Konstruktion Verbiest | Dachdeckung | erneut als Dach-/Oberflächenmaterial | unbekannt | nein | nein | ja | nein | zurückgewonnen und wiederverwendet | unbekannt | unbekannt | Feuchte, Witterung | unbekannt | Zustand, Abdichtung | Q1 | Menge |
| Verbiest Terrassenfliesen | keramisch/Stein unbekannt | vorhandene Konstruktion Verbiest | Terrassenbelag | neuer/erneuerter Terrassenbelag | unbekannt | nein | nein | teils | nein | zurückgewonnen | unbekannt | unbekannt | Frost, Rutschhemmung, Abdichtung | unbekannt | Aufbereitung | Q1 | Menge |
| Verbiest Geländer | Metall/Holz unbekannt | Palais des Expositions Charleroi | Geländer | Geländer im Verbiest-Projekt | unbekannt | nein | ja | teils | nein | geborgen und eingebaut | unbekannt | unbekannt | Absturzsicherung | belgisches Recht unbekannt | Nachweis Trag-/Höhenanforderung | Q1 | Menge, Prüfung |
| Verbiest Fliesen | keramisch/Stein | Palais des Expositions Charleroi | Boden/Wand unbekannt | Boden/Wand/Oberfläche | unbekannt | nein | ja | teils | nein | geborgen und wiederverwendet | Mörtel/Kleber unbekannt | unbekannt | Rutsch, Abrieb, Reinigung | unbekannt | Heterogene Chargen | Q1 | Menge |
| Verbiest Steine | Natur-/Mauersteine unbekannt | Palais des Expositions Charleroi | unbekannt | Bauteil/Oberfläche im Projekt | unbekannt | unbekannt | ja | teils | nein | geborgen | unbekannt | unbekannt | Tragfähigkeit/Frost je Einsatz | unbekannt | Funktion unklar | Q1 | genaue Funktion |
| Verbiest dekorative Fliesen | Keramik, teils Chimay-Produktion frühes 20. Jh. | altes Projekt in Hanzinelle | dekorative Fliesen | feste dekorative Oberfläche | unbekannt | nein | ja | nein | nein | geborgen und eingebaut | unbekannt | unbekannt | Haftung, Reinigung | unbekannt | begrenzte Mengen | Q1 | Menge |
| Verbiest massive Holzplatten/-träger | Holz | neu/Materialquelle unbekannt | n/a | Verstärkung bestehender Betonstruktur | unbekannt | ja | ja | nein | nein | neue Holzverstärkung statt Beton/Stahl | Holzstützen auf bestehender Gründung | unbekannt | Tragfähigkeit, Brand | unbekannt | nicht Reuse, aber Low-carbon-Ersatz | Q1 | Materialherkunft |
| Verbiest Industriegewächshaus | Glas/Stahl unbekannt | unbekannt | unbekannt | Dachersatz / produktives Gewächshaus | unbekannt | teils | ja | ja | teils | Teil des Dachs ersetzt | unbekannt | unbekannt | Feuchte, Wärme, Tragfähigkeit | unbekannt | kein Reuse-Beleg | Q1 | Reuse-Anteil unbekannt |

---

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | vorhandene Büroausbauten und Strukturen analysiert | AgwA, POP, Ingenieure | Bestandsanalyse | unbekannt | n/a | n/a | unbekannt | im Gebäude | schnell wachsende Schule | Phasenplanung | Q2, Q7 |
| Bauteilinventar | Karreveld: Innenwände, Decken, Leuchten erfasst | AgwA / Team | internes Inventar | unbekannt | selektiver Ausbau | Sortierung | unbekannt | Lagerung im Gebäude | keine externen Wege | Materialien verließen das Gebäude nicht | Q4 |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Altbau-/Büroausbau | unbekannt | unbekannt |
| Rückbau | Karreveld: Ausbau von Innenwänden/Decken; Verbiest: sehr begrenzte Demolition | AgwA, Ausführende | selektive Demontage | unbekannt | limited demolition / selective dismantling | unbekannt | unbekannt | Baustelle | laufender Betrieb/Bestand | Interventionen begrenzt | Q1, Q4 |
| Ausbau | Modularwände, Decken, Leuchten aus Karreveld ausgebaut | Ausführende unbekannt | demontierbar/modular | unbekannt | manuell/selektiv | unbekannt | unbekannt | im Gebäude gelagert | Beschädigung vermeiden | Wiederverwendung durch gleiche Systemlogik | Q4 |
| Transport | Karreveld: kein externer Transport; Verbiest: Transfer aus Charleroi und Hanzinelle | unbekannt | interne/externe Logistik | unbekannt | n/a | n/a | unbekannt | Karreveld intern; Verbiest projektübergreifend | Transport- und Lagerdaten fehlen | Material aus laufenden Projekten | Q1, Q4 |
| Lagerung | Karreveld: Materialien im alten Bürogebäude gelagert | unbekannt | Zwischenlager im Gebäude | unbekannt | n/a | n/a | unbekannt | Lagerung vor Ort | Platzbedarf im Umbau | Gebäude als Depot | Q4 |
| Aufbereitung | Anpassung modularer Wände/Decken; Fliesen/Geländer/Steine vorbereitet | unbekannt | Reinigung/Zuschnitt unbekannt | unbekannt | n/a | unbekannt | unbekannt | intern/externe Baustellen | Zustand und Passung | schrittweiser Prozess | Q1, Q4 |
| Planung | flexible Klassenzimmer, minimale Eingriffe, projektübergreifender Materialeinsatz | AgwA, Evelia Macal, Ingenieure | Element- und Opportunitätsstrategie | unbekannt | n/a | n/a | unbekannt | phasenabhängig | Budget, Zeit, Bestand | einfache, robuste Eingriffe | Q1, Q2, Q3 |
| Genehmigung | Nutzungswechsel zu Schule / Wohnen+Atelier | Bauherr, Behörden | unbekannt | unbekannt | n/a | n/a | unbekannt | unbekannt | Schul- und Wohnanforderungen | unbekannt | Q3, Q7 |
| Wiedereinbau | Karreveld: Trennwände/Decken/Leuchten integriert; Verbiest: Fliesen/Geländer/Steine | Ausführende | Wiedermontage | unbekannt | n/a | angepasst | unbekannt | Baustelle | Norm-/Leistungsnachweis | vorhandene Systeme nutzen | Q1, Q4 |
| Monitoring | unbekannt | unbekannt | unbekannt | unbekannt | n/a | n/a | unbekannt | unbekannt | langfristige Flexibilität | flexible Elemente | Q2, Q8 |

---

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Verbiest: vorhandene Betonstruktur mit Holzstützen/-platten verstärkt; Karreveld: Bestand + neue Volumen | Tragfähigkeit, Nutzungswechsel | belgisches Baurecht unbekannt | unbekannt | vorhandene Struktur an neue Nutzung anpassen | Holzverstärkung / begrenzte Eingriffe | Q1, Q3 |
| Lastabtragung | Reuse-Innenwände nicht tragend; Holzverstärkung bei Verbiest nicht als Reuse belegt | Lasten Schule/Wohnen/Atelier | unbekannt | unbekannt | Bestandsreserven | minimale strukturelle Eingriffe | Q1, Q3 |
| Verbindung | modulare Karreveld-Wände; abgehängte Decken; Verbiest-Geländer/Fliesen | Standsicherheit, Reversibilität, Sicherheit | unbekannt | unbekannt | Altbauteile in neuer Nutzung | modulare Systeme wiederverwenden | Q4 |
| Brandschutz | Schule, Sporthalle, Wohnen/Atelier | Fluchtwege, Brandabschnitte, Materialklassen | unbekannt | unbekannt | Reuse-Decken mit Steinwolle/Metall, alte Wände | unbekannt | Q4 |
| Schallschutz | Karreveld-Wände enthalten Akustikdämmung; Kahle Acoustics in Phase 2 | Klassenräume, Sporthalle | unbekannt | unbekannt | Bürotrennwände für Schulakustik | Wiederverwendung vorhandener Akustikschichten | Q3, Q4 |
| Feuchte | Verbiest Dach-/Terrassenfliesen; Gewächshaus | Abdichtung, Frost, Kondensat | unbekannt | unbekannt | alte Fliesen in Außenbereichen | Wiederverwendung mit unbekannter Abdichtung | Q1 |
| Wärmeschutz | Verbiest reduziert beheizte Fläche um ca. Hälfte; Hanfdämmung lokal | Energiebedarf, Komfort | unbekannt | unbekannt | Dämm-Graue-Energie vs. Heizenergie | beheizte Zonen verkleinert | Q1 |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Luftdichtheit | unbekannt | Schule/Wohnen | unbekannt | unbekannt | Altbau, Reuse-Innenausbau | unbekannt | unbekannt |
| TGA-Integration | Karreveld technische Schächte erhalten; TGA-Details unbekannt | Hygiene, Lüftung, Schule | unbekannt | unbekannt | Bestandssysteme vs. neue Anforderungen | Erhalt technischer Schächte, nicht Reuse gezählt | Q5 |
| Barrierefreiheit | Schule/Sportzentrum öffentlich | Zugänglichkeit | unbekannt | unbekannt | Bestandsbüro | neue/angepasste Erschließung | Q3, Q5 |
| Dauerhaftigkeit | modulare Büroelemente in Schulnutzung | Robustheit gegen intensive Nutzung | unbekannt | unbekannt | Schulbetrieb belastet Oberflächen | flexible, ersetzbare Elemente | Q2, Q4 |
| Wartung | unbekannt | Schule und Wohnen | unbekannt | unbekannt | heterogene Wiederverwendung | unbekannt | unbekannt |
| Zulassung | keine Details | Nutzungswechsel Schule/Hotel? nein: Schule/Wohnen | unbekannt | unbekannt | Reuse-Komponenten | unbekannt | unbekannt |
| Haftung | unbekannt | Bauherr/Planer/Ausführende | unbekannt | unbekannt | Wiederverwendete Elektro-Leuchten | unbekannt | Q4 |

---

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Karreveld wiederverwendete Innenwände | ca. 450 | m² | Opalis-Projektangabe | Phase 1, in-situ | Q4 | belegt |
| Karreveld wiederverwendete abgehängte Decke + Leuchten | ca. 400 | m² | Opalis-Projektangabe | Phase 1, in-situ | Q4 | belegt |
| Verbiest Projektfläche | 610 | m² | AgwA-Projektangabe | Verbiest | Q1 | belegt |
| Verbiest Bestandslager | fast 1000 | m² | AgwA-Text | ursprüngliches Lagerhaus | Q1 | belegt |
| Karreveld Phase-2-Kosten | 6.000.000 | EUR exkl. MwSt. | AgwA-Projektangabe | Gesamtprojektphase, nicht Reuse-Kosten | Q3 | belegt, nicht reuse-spezifisch |
| wiederverwendete Masse | unbekannt | kg/t | unbekannt | beide Projekte | unbekannt | unklar |
| Anzahl Bauteile | unbekannt | Stück | unbekannt | beide Projekte | unbekannt | unklar |
| CO₂-Einsparung | unbekannt | kg CO₂e | unbekannt | unbekannt | unbekannt | unklar |
| Abfallvermeidung | unbekannt | kg/t | unbekannt | Reuse-Ausbau | unbekannt | unklar |
| Transportdistanz | unbekannt | km | unbekannt | Karreveld intern; Verbiest extern | unbekannt | unklar |
| Bauzeit | Verbiest bis 2020; Karreveld Phasen bis 2022/2023 | Jahre | Projektquellen | Projektstatus | Q1, Q3, Q5 | teilweise belegt |
| Energiebedarf | unbekannt | kWh | unbekannt | Betrieb | unbekannt | unklar |
| U-Wert | unbekannt | W/m²K | unbekannt | Hülle | unbekannt | unklar |
| Lebensdauer | unbekannt | Jahre | unbekannt | Reuse-Bauteile | unbekannt | unklar |
| Zirkularitätskennwert | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unklar |

---

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Abgrenzung Bestandserhalt/ReUse | methodisch | viele Bestandsbauteile bleiben am Ort | falsche Bewertung möglich | Gebäude, Bauteil, Reuse-Strategie | nur versetzte/neu integrierte Bauteile zählen | klare Inventarregeln sind entscheidend | Q1, Q5 |
| Schulbetrieb und Phasierung | logistisch/sozial | Karreveld musste schrittweise Schüler aufnehmen | Baustellenlogistik und Zeitdruck | Prozessphase, Logistik, Hürde | unabhängige, elementare Interventionen | Reuse-Systeme helfen bei schnellen Umbauten | Q2, Q7 |
| Akustik/Brandschutz von Bürotrennwänden | technisch/rechtlich | Büroelemente werden zu Schulwänden | Leistungsnachweise unklar | Prüfung, Leistungsanforderung | vorhandene Akustikdämmung nutzen; Prüfungen unbekannt | Nutzungssprung braucht systematische Tests | Q4 |
| Elektroprüfung alter Leuchten | technisch/rechtlich | Leuchten aus abgehängter Decke wiederverwendet | Haftung und Sicherheit unklar | Bauteil, Technik, Recht | unbekannt | Reuse-Leuchten brauchen klare Prüf-/CE-Strategie | Q4 |
| Außenfliesen/Abdichtung Verbiest | technisch | alte Dach-/Terrassenfliesen in Außenbereichen | Feuchte-/Frostrisiko | Bauteil, Feuchte | unbekannt | Reuse im Außenbereich braucht Detailnachweise | Q1 |
| Projektübergreifender Transfer | logistisch/wirtschaftlich | Verbiest nutzt Material aus Charleroi/Hanzinelle | Transport, Timing, Lagerung | Logistik, Bauteil | Material aus laufenden Projekten | Bürointerne/project network supply kann Bauteilquellen öffnen | Q1 |
| fehlende CO₂-/Massenwerte | datenbezogen | keine vollständigen Materialpässe veröffentlicht | Bilanz nicht möglich | Kennwert, Datenmodell | unbekannt markieren | m²-Angaben sind gut, aber Masse/LCA fehlt | Q4 |

---

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:**  
  - Karreveld: interne Wiederverwendung – Ausbau, Lagerung und Wiedereinbau im selben Gebäude; keine externe Bauteilbörse.  
  - Verbiest: Kombination aus Wiederverwendung aus eigener Konstruktion und projektübergreifender Beschaffung aus Charleroi/Hanzinelle.
- **Bauteilbörse / Quelle:** keine klassische Bauteilbörse belegt; Quellen sind eigenes Gebäude, Palais des Expositions Charleroi, altes Projekt in Hanzinelle.
- **Kostenwirkung:** Karreveld Phase 2: 6.000.000 EUR exkl. MwSt. als Gesamtprojektkosten; Reuse-spezifische Kosten unbekannt.
- **Zeitwirkung:** Karreveld musste schnell und phasenweise funktionieren; wiederverwendete modulare Wände erlaubten flexible Klassenzimmer, quantifizierte Zeitwirkung unbekannt.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** hoch durch Demontage, Lagerung, Anpassung, Wiedereinbau; nicht quantifiziert.
- **Lagerung:** Karreveld: im Gebäude selbst belegt; Verbiest: unbekannt.
- **Marktbarrieren:** Nachweis alter Büroelemente für Schulbetrieb; Elektroprüfung von Leuchten; fehlende Massen-/CO₂-Daten; Reuse außerhalb standardisierter Lieferketten.

---

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** mittel bis hoch; Karreveld nutzt Büro-Ausbau sichtbar in Schulräumen; Verbiest zeigt Fliesen, Steine und Materialspuren.
- **räumliche Transformation:** Büro → Schule; Lager → Haus/Atelier. Beide Projekte nutzen vorhandene großzügige Strukturen.
- **Atmosphäre / Ausdruck:** roh, direkt, nutzungsnah; bei Verbiest bewusster Widerstand gegen unnötige Veredelung.
- **Umgang mit Spuren:** Materialspuren werden nicht vollständig neutralisiert; besonders bei Verbiest als Teil der architektonischen Haltung.
- **sozialer Wert:** Karreveld schafft dringend benötigte Schulräume und öffnet Sporthalle auch für das Quartier.
- **Denkmal- oder Bestandswert:** kein formaler Denkmalwert belegt; Wert liegt in pragmatischer Nutzung vorhandener Strukturen.
- **Kritik / Grenzen:** weniger spektakulär als konstruktiver Tragwerks-Reuse; Gefahr, normalen Bestandserhalt zu überschätzen; technische Prüfungen nicht offen.

---

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** genaue Normen, Prüfprotokolle, Schadstoffprüfung, Software/Datenmodell, vollständige Materialpässe, Versicherung/Gewährleistung, CO₂-Daten.
- **Welche neuen Entitäten wären sinnvoll?** In-situ-Reuse-Kette; Parallelbetrieb; Projektübergreifender Materialtransfer; Bestandserhalt-Warnung.
- **Welche Daten fehlen?** Massen, Stückzahlen, Detailpläne, Wiederverwendungsquote, Kostenwirkung, Prüfungen für Akustik/Brand/Elektro, Wartungsdaten.
- **Welche Quellen müssten geprüft werden?** Opalis-Vollseite und Projektdossier; AgwA-Ausführungspläne; Buch „Verbiest. Approximations“; Ausschreibungen von POP/BMA; Brandschutz-/Akustikberichte; Elektroprüfprotokolle.

---

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** Anhang oder Vergleichsfall; Karreveld kann bei Fokus „in-situ reuse interior systems“ in eine Hauptliste-Unterkategorie.
- **5 wichtigste Fakten:**
  1. Karreveld verwendete ca. 450 m² modulare Innenwände wieder.
  2. Karreveld verwendete ca. 400 m² abgehängte Decken und Leuchten wieder.
  3. Diese Materialien wurden im Gebäude selbst gelagert und wieder eingebaut.
  4. Verbiest verwendete Dach-/Terrassenfliesen aus dem Bestand sowie Geländer, Fliesen und Steine aus anderen Projekten.
  5. Beide Projekte sind Umbauten; Bestandserhalt muss methodisch getrennt werden.
- **5 wichtigste Bauteile:**
  1. Karreveld: modulare Innenwände
  2. Karreveld: abgehängte Decken
  3. Karreveld: Leuchten
  4. Verbiest: Dach-/Terrassenfliesen
  5. Verbiest: Geländer, Steine und dekorative Fliesen
- **5 wichtigste Hürden:**
  1. Bestandserhalt vs. Direct Reuse
  2. Schulbetrieb und Bauphasierung
  3. Brandschutz/Schallschutz für wiederverwendete Innenbausysteme
  4. Elektroprüfung wiederverwendeter Leuchten
  5. fehlende Massen-, CO₂- und Kostendaten
- **5 wichtigste übertragbare Erkenntnisse:**
  1. In-situ-Lagerung kann Logistik stark vereinfachen.
  2. Modulare Bürotrennwände sind gute Kandidaten für schnelle Schulumbauten.
  3. Projektübergreifende Materialquellen können kleine, wertvolle Bauteilchargen liefern.
  4. Reuse wird stärker, wenn Phasing und Nutzung von Anfang an mitgedacht werden.
  5. Erhalt, Reuse und Neubau müssen separat inventarisiert werden.
- **5 offene Fragen:**
  1. Welche Prüfungen wurden für Trennwände, Decken und Leuchten durchgeführt?
  2. Wie hoch war die tatsächliche Abfall- oder CO₂-Einsparung?
  3. Wie viele Einzelbauteile entsprechen den angegebenen m²?
  4. Welche Gewährleistungsregelungen wurden vereinbart?
  5. Welche Bauteile aus späteren Karreveld-Phasen wurden zusätzlich wiederverwendet?

---

## Quellen / Links

- **Q1 – AgwA, „1718_VERBIEST“:** https://www.agwa.be/en/projects/1718_verbiest/201/  
- **Q2 – AgwA, „1619_KARREVELD 1“:** https://www.agwa.be/en/projects/1619_TAKEDA/185/  
- **Q3 – AgwA, „1811_KARREVELD 2“:** https://www.agwa.be/en/projects/1811_KARREVELD/212/  
- **Q4 – Opalis, „Reconversion d’un immeuble de bureau en une école“:** https://opalis.eu/fr/projets/reconversion-dun-immeuble-de-bureau-en-une-ecole  
- **Q5 – VAi, „Karreveld“:** https://www.vai.be/gebouwen/sportinfrastructuur/karreveld  
- **Q6 – Wallonie-Bruxelles Architectures, „Karreveld“:** https://wbarchitectures.be/en/architects/agwa/karreveld  
- **Q7 – bouwmeester maître architecte, „POP KARREVELD“:** https://bma.brussels/nl/oproep-pop-karreveld/  
- **Q8 – EN BLANCO / Polipapers, „2016–2022 KARREVELD“:** https://www.polipapers.upv.es/index.php/enblanco/user/setLocale/en_US?source=%2Findex.php%2Fenblanco%2Farticle%2Fview%2F21454  
- **Q9 – AgwA Books, „Verbiest. Approximations“:** https://www.agwa.be/en/books/
