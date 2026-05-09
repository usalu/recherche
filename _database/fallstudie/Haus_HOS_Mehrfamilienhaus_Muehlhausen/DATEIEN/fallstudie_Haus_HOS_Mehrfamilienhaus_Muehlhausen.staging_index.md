---
id: "Haus_HOS_Mehrfamilienhaus_Muehlhausen"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "Haus HOS / Mehrfamilienhaus Mühlhausen — Fallstudie Direct Reuse / Wiederverwendung von WBS70-Plattenbauteilen"
bauobjekt:
  - "Haus_HOS_Mehrfamilienhaus_Muehlhausen"
legacy_paths:
  - "Gebäude\\Haus_HOS_Mehrfamilienhaus_Muehlhausen.md"
projekt:
  - "Haus_HOS_Mehrfamilienhaus_Muehlhausen"
reuse_chain_detected: "False"
---
# Haus HOS / Mehrfamilienhaus Mühlhausen — Fallstudie Direct Reuse / Wiederverwendung von WBS70-Plattenbauteilen

## Migration

- Fallstudie ID: Haus_HOS_Mehrfamilienhaus_Muehlhausen
- Legacy source count: 1
- Generated project: Haus_HOS_Mehrfamilienhaus_Muehlhausen
- Generated bauobjekt: Haus_HOS_Mehrfamilienhaus_Muehlhausen
- Extracted reuse_einsatz rows: 6
- Extracted datenpunkt rows: 14
- Extracted entity mapping rows: 17
- Reuse chain detected: False

## Legacy Content

### Legacy Source: Gebäude\Haus_HOS_Mehrfamilienhaus_Muehlhausen.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Haus_HOS_Mehrfamilienhaus_Muehlhausen
- Secondary targets: projekt/Haus_HOS_Mehrfamilienhaus_Muehlhausen; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Haus HOS / Mehrfamilienhaus Mühlhausen — Fallstudie Direct Reuse / Wiederverwendung von WBS70-Plattenbauteilen

**Arbeitsstand:** 2026-05-07  
**Sprache:** Deutsch  
**Regel:** Es werden nur tatsächlich wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente gezählt. Lose Möbel, Dekoration, reine DfD-Strategien und bloßer Bestandserhalt zählen nicht.


## 1. EINORDNUNG

- **Entscheidung:** HAUPTFALL
- **Bewertung:** ★★★★☆
- **Begründung:** Gebautes Mehrfamilienhaus aus demontierten Plattenbauteilen mit tragender Wiederverwendung. Primärquelle der Architekten nennt 58 Stahlbeton-Wand- und Deckenelemente mit ca. 190 t Gesamtgewicht, Transport aus Leinefelde nach Mühlhausen und Remontage zu einem Mehrfamilienhaus. Die PRECS-Datenbank gliedert die 58 Elemente in 28 Wand-, 23 Deckenelemente und 7 Treppen.
- **Vertrauensgrad:** belegt
- **Warnung Bestandserhalt:** nein
- **Warnung Möbel/Dekoration:** nein
- **Projektstatus:** gebaut

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Haus HOS / Mühlhausen 2-story multi-housing building | Untersuchter Reuse-Fall | [S1], [S7], [S8] | belegt | Seidl+Seidl nennt „HAUS HOS“. |
| Gebäude | Mehrfamilienhaus | Empfängergebäude | [S7], [S8] | belegt | Neubau aus demontierten Plattenbauteilen. |
| Ort | Mühlhausen, Thüringen, Deutschland | Standort Empfängerprojekt | [S7] | belegt | Spenderstandort Leinefelde. |
| Projekt | Neubau eines Mehrfamilienhauses aus demontierten Plattenbauteilen | Reuse-Projekt | [S7], [S8] | belegt | Pilotprojekt. |
| Bauteil | 58 Stahlbeton-Wand- und Deckenelemente; nach PRECS: 28 Wände, 23 Decken, 7 Treppen | direkt wiederverwendete Bauteile | [S1], [S7], [S8] | belegt | 58 Elemente = 28+23+7. |
| Material | Stahlbetonfertigteile / WBS70-Plattenbauteile | Hauptmaterial | [S1], [S7] | belegt | Quelle nennt WBS70-Kontext. |
| Gebäude | Spender: Rückbaustelle Leinefelde | Herkunft | [S7] | belegt | Entfernung 30 km laut Architektenquelle; PRECS nennt 28 km. |
| People | Seidl + Seidl Architekten; Architekturbüro Hose; Dr. Angelika Mettke / BTU Cottbus | Planung und Forschungsbegleitung | [S7], [S8] | belegt | Seidl+Seidl Lph 1–8 in Zusammenarbeit mit Architekturbüro Hose; BTU-Forschungsbegleitung. |
| Bauherr | Privat | Bauherrschaft | [S7], [S8] | belegt | Name unbekannt. |
| Reuse-Strategie | ex-situ Remontage | Bauteile von Leinefelde nach Mühlhausen | [S7] | belegt | Direkte Bauteilwiederverwendung. |
| Kennwert | ca. 250 m² Nutzfläche; ca. 300.000 EUR Herstellungskosten; 2008 Fertigstellung | Projektdaten | [S7], [S8] | belegt | Kostenangabe aus Architektenquelle. |
| Kennwert | ca. 190 t wiederverwendete Elemente | Masse | [S7], [S8] | belegt | Gesamtgewicht der ausgewählten Elemente. |
| Kennwert | ca. 75 % Wiederverwendungsgrad Rohbau-Substanz; ca. 25 % Kosteneinsparung | Wirtschaft/Reuse | [S7], [S8] | belegt | Quelle: Architektenangabe. |
| Logistik | Tieflader; 30 km von Leinefelde nach Mühlhausen | Transport | [S7], [S8] | belegt | Schwertransport. |
| Abbruchmethode | Rückbau/Demontage | Voraussetzung | [S7], [S9] | teilweise belegt | Stern beschreibt Auswahl von Wand-/Deckenelementen, Podesten und Treppenläufen beim Rückbau in Leinefelde. |
| Prüfung | Auswahl gemeinsam mit Statiker | Bauteilprüfung/Auswahl | [S9] | teilweise belegt | Konkrete Prüfwerte unbekannt. |
| Norm | unbekannt | Projektgenehmigung | unbekannt | unklar | Keine projektbezogenen Normangaben. |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Spendergebäude | Herkunft der Bauteile muss dokumentiert werden | Rückbaustelle Leinefelde | Gebäude, Logistik, Prüfung |
| Remontage | Wiederaufbauprozess ist nicht nur „Einbau“ | Remontage in Mühlhausen | Prozessphase, Methode |
| Wiederverwendungsgrad Rohbau | Quantifiziert Anteil wiederverwendeter Rohbausubstanz | ca. 75 % | Kennwert, Wirtschaft |
| Reuse-Pilotprojekt | markiert Forschungs-/Demonstratorrolle eines gebauten Falls | Haus HOS | Fallstudie, Förderprogramm, Bericht |

## 3. FALLSTUDIE

- **Name:** „HAUS HOS“ / Neubau eines Mehrfamilienhauses aus demontierten Plattenbauteilen, Mühlhausen
- **Ort:** Mühlhausen, Thüringen, Deutschland
- **Gebäude:** Mehrfamilienhaus
- **Projekt:** Neubau mit 58 demontierten Stahlbeton-Wand- und Deckenelementen aus Leinefelde
- **Beteiligte People / Akteure:** Seidl + Seidl Architekten; Architekturbüro Hose, Mühlhausen; BTU Cottbus, Lehrstuhl Altlasten / Dr. Angelika Mettke
- **Architekt:** Seidl + Seidl Architekten, in Zusammenarbeit mit Architekturbüro Hose
- **Tragwerksplaner:** unbekannt; Auswahl mit Statiker laut Stern-Bericht, Name unbekannt
- **Bauherr:** Privat
- **Zeitraum:** PRECS-Fallstudie 2007; Fertigstellung 2008 laut Architektenquelle
- **Ursprüngliche Nutzung:** Plattenbau-/Wohnungsbaukontext in Leinefelde; genaue Spendergebäudeadresse unbekannt
- **Neue Nutzung:** Mehrfamilienhaus
- **Fläche / Maßstab:** ca. 250 m² Nutzfläche
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** relativ gut: Architektenseite/PDF plus wissenschaftliche PRECS-Datenbank und Presseberichte

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; Remontage; adaptive Nutzung vorhandener Plattenbauteile
- **Hauptniveau:** Tragwerk / räumliche Struktur / Erschließung
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die Elemente blieben nicht im Bestand, sondern wurden von einer Rückbaustelle abgebaut, transportiert und in einem neuen Mehrfamilienhaus wieder montiert. Es handelt sich nicht um Zerkleinerung zu Recyclingmaterial.
- **Warum ist der Fall relevant?** Erstmals wurden laut Architektenquelle gebrauchte Plattenbauteile dreigeschossig für den Neubau eines Gebäudes wiederverwendet. Der Fall dokumentiert Masse, Transport, Kosten, Wiederverwendungsgrad und Forschungsbegleitung.

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Wandelemente | Stahlbetonfertigteil / WBS70-Kontext | Leinefelde | Wand im Plattenbau | Wand/Trag-/Raumstruktur | 28 | ja | ja | teilweise | nein | Auswahl; ggf. Anpassung unbekannt | Laschen/Ösen-Schweißverbindungen allgemein für Plattenbau im Stern-Bericht beschrieben | Auswahl mit Statiker; Detailprüfung unbekannt | Tragfähigkeit, Schall, Brand, Wärme bei Außenwand | projektspezifisch unbekannt | Nachweis, Anschlüsse, Dämmung | [S1], [S7], [S9] | Abmessungen, Prüfwerte |
| Deckenelemente | Stahlbetonfertigteil / WBS70-Kontext | Leinefelde | Decke/Boden | Decke/Boden | 23 | ja | ja | nein | nein | Auswahl; unbekannte Aufbereitung | unbekannt | Auswahl mit Statiker; Detailprüfung unbekannt | Tragfähigkeit, Brandschutz, Gebrauchstauglichkeit | unbekannt | Betondeckung/Feuerwiderstand | [S1], [S7], [S9] | Bewehrung, Spannweite |
| Treppen | Stahlbetonfertigteil | Leinefelde | Treppenläufe/Podeste | Erschließung | 7 | ja | ja | nein | nein | unbekannt | unbekannt | unbekannt | Tragfähigkeit, Brandschutz, Schallschutz, Barrierefreiheit | unbekannt | Schall/Brand | [S1], [S9] | genaue Art |
| Gesamtbauteile | Stahlbetonfertigteile | Leinefelde | Wand/Decke/Treppe | Rohbau Mehrfamilienhaus | 58 / ca. 190 t | ja | ja | teilweise | nein | Remontage | unbekannt | teilweise belegt | Rohbau | unbekannt | Logistik | [S7], [S8] | Detailqualitäten |
| Fassaden | unbekannt | unbekannt | unbekannt | Hülle | unbekannt | unbekannt | unbekannt | ja | nein | unbekannt | unbekannt | unbekannt | Wärmeschutz/Feuchte | unbekannt | unbekannt | keine Quelle | ja |
| Fenster/Türen/Dach/Geländer/Bodenaufbauten/Innenwände/TGA/Dämmung/Sanitär/Beleuchtung/feste Einbauten | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle | ja |

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Auswahl geeigneter Wand-, Decken-, Treppen-/Podestelemente | Architekt Hose, Statiker; genaue Namen unbekannt | Sichtung/Auswahl | unbekannt | Rückbau Leinefelde | unbekannt | Auswahl mit Statiker | Spenderort Leinefelde | Bauteile müssen passen | gezielte Auswahl | [S9] |
| Bauteilinventar | 58 Elemente dokumentiert | Seidl+Seidl / Architekturbüro Hose / BTU | Bauteilliste | unbekannt | unbekannt | unbekannt | unbekannt | 30 km | Bestand genau erfassen | ausgewählte Bauteile | [S7], [S8] |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | mögliche Schadstoffe/Dämmungen/Fugen | unbekannt | [S5] allgemein |
| Rückbau | Elemente demontieren statt zerstören | Rückbauunternehmen unbekannt | selektiver Rückbau | Kran/Tieflader; Details unbekannt | Rückbau von 5 auf 3 Geschosse im Pressekontext erwähnt | unbekannt | unbekannt | direkte Auskopplung | Beschädigungsrisiko | demontierbare Platten wählen | [S9] |
| Ausbau | Wand- und Deckenteile, Podeste, Treppenläufe entnehmen | unbekannt | Demontage | Kran wahrscheinlich | unbekannt | unbekannt | unbekannt | unbekannt | Knotenpunkte/Verbindungen | unbekannt | [S9] |
| Transport | Transport per Tieflader | unbekannt | Schwertransport | Tieflader | unbekannt | unbekannt | unbekannt | 30 km Leinefelde–Mühlhausen | Kosten/Timing | regionale Nähe | [S7], [S8] |
| Lagerung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Lagerfläche | unbekannt | keine Quelle |
| Aufbereitung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Maß-/Öffnungsanpassung | unbekannt | keine Quelle |
| Planung | Entwurf und Lph 1–8 | Seidl+Seidl, Architekturbüro Hose | Planung mit vorhandenen Platten | unbekannt | unbekannt | unbekannt | statische Auswahl | unbekannt | Rasterbindung | Gebäude aus Plattenbauteilen planen | [S7] |
| Genehmigung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Bauaufsicht/Gewährleistung | unbekannt | keine Quelle |
| Wiedereinbau | Remontage zum Mehrfamilienhaus | Bau-/Montageteam unbekannt | Fertigteilmontage | Kran wahrscheinlich | unbekannt | unbekannt | unbekannt | Mühlhausen | Kranstandzeit/Just-in-time | Remontage | [S7], [S8] |
| Monitoring | Prämierung/Präsentation, aber kein technisches Monitoring gefunden | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Langzeitdaten | unbekannt | [S7] |

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Wiederverwendete Wand-, Decken- und Treppenelemente bilden ca. 75 % der Rohbau-Substanz | Standsicherheit/Gebrauchstauglichkeit | projektspezifisch unbekannt | Auswahl mit Statiker; Detailwerte unbekannt | Nachweis alter Bauteile | gezielte Auswahl | [S7], [S9] |
| Lastabtragung | dreigeschossige Verwendung laut Architektenquelle | Tragfähigkeit über mehrere Geschosse | unbekannt | unbekannt | höhere Anforderungen als Einfamilienhaus | unbekannt | [S7] |
| Verbindung | Plattenbauknoten/Laschen/Ösen im allgemeinen Pressebericht beschrieben | kraftschlüssige Verbindung | unbekannt | unbekannt | alte Anschlusslogik | Schweißverbindungen im Plattenbaukontext erwähnt | [S9] |
| Brandschutz | projektspezifisch unbekannt | Mehrfamilienhaus-Anforderungen | unbekannt | unbekannt | alte Deckenelemente können in aktuellen Diskussionen brandschutztechnische Defizite haben | unbekannt | [S5] allgemein |
| Schallschutz | Treppen und Decken relevant | Wohnnutzung | unbekannt | unbekannt | Körperschall/alte Elemente | unbekannt | [S5] allgemein |
| Feuchte | unbekannt | Feuchte- und Dauerhaftigkeitsschutz | unbekannt | unbekannt | Außenwandaufbau | unbekannt | keine Quelle |
| Wärmeschutz | „Effizienzhaus“ in Architektenquelle erwähnt; genaue Klasse unbekannt | energetischer Standard | unbekannt | unbekannt | Dämmung alter Wände | unbekannt | [S7] |
| Wärmebrücken | unbekannt | Hülle | unbekannt | unbekannt | Fugen/Anschlüsse | unbekannt | keine Quelle |
| Luftdichtheit | unbekannt | Wohngebäude | unbekannt | unbekannt | Fugen | unbekannt | keine Quelle |
| TGA-Integration | unbekannt | Wohnnutzung | unbekannt | unbekannt | Leitungsführung in alten Platten | unbekannt | keine Quelle |
| Barrierefreiheit | unbekannt | Wohnnutzung | unbekannt | unbekannt | Treppen/Grundriss | unbekannt | keine Quelle |
| Zulassung/Haftung | unbekannt | Neubaunachweis | allgemeine heutige Einordnung: Eurocode 2, DIN EN 206-1, DIN 1045-2 | unbekannt | Gewährleistung | unbekannt | [S4] allgemein |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| wiederverwendete Elemente gesamt | 58 | Stück | Architektenquelle / PRECS | Rohbau | [S1], [S7], [S8] | belegt |
| Wandteile | 28 | Stück | PRECS-Datenbank | Bauteile | [S1], [S3] | belegt |
| Deckenteile | 23 | Stück | PRECS-Datenbank | Bauteile | [S1], [S3] | belegt |
| Treppen | 7 | Stück | PRECS-Datenbank | Bauteile | [S1], [S3] | belegt |
| Gesamtgewicht | ca. 190 | t | Architektenquelle | 58 Elemente | [S7], [S8] | belegt |
| Nutzfläche | ca. 250 | m² | Architektenquelle | Gebäude | [S7], [S8] | belegt |
| Herstellungskosten | ca. 300.000 | EUR | Architektenquelle | Gebäude | [S7], [S8] | belegt |
| Wiederverwendungsgrad Rohbau-Substanz | ca. 75 | % | Architektenquelle | Rohbau | [S7], [S8] | belegt |
| Kosteneinsparung | ca. 25 | % | Architektenquelle | nicht näher definierte Kostenbasis | [S7], [S8] | teilweise belegt |
| Transportdistanz | ca. 30 / 28 | km | Architektenquelle / PRECS | Leinefelde–Mühlhausen | [S7], [S1] | belegt |
| Fertigstellung | 2008 | Jahr | Architektenquelle | Projekt | [S7], [S8] | belegt |
| Fallstudienstart | 2007 | Jahr | PRECS | Projekt | [S1] | belegt |
| CO₂-Einsparung | unbekannt | kg CO₂e | unbekannt | unbekannt | keine Quelle | unklar |
| U-Wert/Energiebedarf | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle | unklar |

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Logistik | logistisch/wirtschaftlich | 190 t schwere Bauteile, Kran/Tieflader | Kosten- und Terminrisiko | Logistik, Wirtschaft | 30-km-regionale Quelle | regionale Rückbau-/Neubaukopplung ist wichtig | [S7], [S8] |
| Tragfähigkeitsnachweis | technisch/rechtlich | gebrauchte tragende Bauteile | Prüf- und Haftungsaufwand | Prüfung, Norm, Recht | Auswahl mit Statiker | Statiker früh einbinden | [S9] |
| Entwurfsbindung | gestalterisch | WBS70-Formate | Grundriss und Öffnungen begrenzt | Bauteil, Tragwerkssystem | Gebäude an Bauteile anpassen | Design-from-availability | [S7] |
| Brandschutz/Schallschutz | technisch/rechtlich | alte Decken/Treppen | Zusatzmaßnahmen möglich | Leistungsanforderung | unbekannt | aktuelle Anforderungen früh prüfen | [S5] allgemein |
| Marktbarriere | sozial/wirtschaftlich | Image „Platte“, Gewährleistung, Logistik | geringe Skalierung | Wirtschaft, Recht | Pilotprojekt/Prämierung | Demonstratoren schaffen Vertrauen | [S7], [S9] |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** direkte Beschaffung/Auswahl aus Rückbaustelle Leinefelde; Details vertraglich unbekannt
- **Bauteilbörse / Quelle:** keine Bauteilbörse belegt; Quelle war Rückbaustelle Leinefelde
- **Kostenwirkung:** ca. 25 % Kosteneinsparung laut Architektenquelle; Bezugsgröße nicht näher differenziert
- **Zeitwirkung:** unbekannt; Presseberichte nennen allgemein Verkürzung der Bauzeit als Ziel, projektspezifisch nicht belastbar quantifiziert
- **Versicherung / Haftung:** unbekannt
- **Gewährleistung:** unbekannt
- **Arbeitsaufwand:** erhöht durch Auswahl, Transport, Remontage, Planung
- **Lagerung:** unbekannt
- **Marktbarrieren:** Logistik, fehlende Bauteilbörse, Gewährleistung, Akzeptanz, Prüfaufwand

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** unbekannt; Architekten-/Pressekontext betont, dass der Neubau nicht bloß „Platte“ wirken soll
- **räumliche Transformation:** Plattenbau-Elemente aus Leinefelde werden zu einem neuen Mehrfamilienhaus in Mühlhausen
- **Atmosphäre / Ausdruck:** unbekannt
- **Umgang mit Spuren:** unbekannt
- **sozialer Wert:** Schaffung von Wohnraum mit Ressourcenschonung; privater Bauherr
- **Denkmal- oder Bestandswert:** unbekannt
- **Kritik / Grenzen:** Wiederverwendung ist technisch plausibel, aber abhängig von Statik, Logistik, Akzeptanz und Genehmigung

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** genaue Tragwerksplanung, Prüfberichte, Schadstoffbefunde, Norm-/Genehmigungsnachweise, U-Werte, CO₂-Bilanz, Monitoring.
- **Welche neuen Entitäten wären sinnvoll?** Remontage, Wiederverwendungsgrad Rohbau, Spendergebäude, Reuse-Pilotprojekt.
- **Welche Daten fehlen?** Spenderadresse, Bauteilabmessungen, Verbindungstypen, Prüfwerte, Energiekonzept, heutiger Nutzungszustand.
- **Welche Quellen müssten geprüft werden?** BTU-Cottbus-Berichte, Bauakte Mühlhausen, Statikunterlagen, Architekturbüro Hose/Seidl+Seidl Archiv.

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja
- **5 wichtigste Fakten:**
  1. Gebautes Pilot-Mehrfamilienhaus in Mühlhausen.
  2. 58 wiederverwendete Stahlbeton-Wand-/Deckenelemente bzw. 28 Wände, 23 Decken, 7 Treppen.
  3. Gesamtgewicht ca. 190 t.
  4. Transport per Tieflader aus ca. 30 km entferntem Leinefelde.
  5. Ca. 75 % Wiederverwendungsgrad der Rohbau-Substanz und ca. 25 % Kosteneinsparung laut Architektenquelle.
- **5 wichtigste Bauteile:**
  1. Wandelemente.
  2. Deckenelemente.
  3. Treppen.
  4. Podeste, falls in Projekt enthalten; nur im Pressekontext erwähnt.
  5. Verbindungen/Knoten, Details unbekannt.
- **5 wichtigste Hürden:**
  1. Logistik.
  2. Tragfähigkeitsnachweis.
  3. Anschlussdetails.
  4. Brandschutz/Schallschutz.
  5. Marktakzeptanz und Gewährleistung.
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Auch dreigeschossiger Neubau mit gebrauchten Plattenbauteilen ist möglich.
  2. Regionale Spendergebäude senken Logistikrisiken.
  3. Statiker und Architekt müssen schon bei der Bauteilauswahl beteiligt sein.
  4. Wiederverwendung kann Kosten im Rohbau beeinflussen.
  5. Forschung und Demonstratoren helfen bei Akzeptanz.
- **5 offene Fragen:**
  1. Welche konkreten Prüfberichte gibt es?
  2. Welche Norm-/Genehmigungsstrategie wurde angewandt?
  3. Wie wurden Fugen und Anschlüsse ausgeführt?
  4. Welche CO₂-Einsparung ergab sich?
  5. Wie ist der aktuelle Zustand des Gebäudes?

## Quellen und Links

- [S0] Hochgeladene Prioritätenliste: gebäude4_wiederverwendung_direct_reuse_examples.md
- [S1] Küpfer, C.; Bastien-Masse, M.; Fivet, C. (2023): Reuse of concrete components in new construction projects: Critical review of 77 circular precedents, Journal of Cleaner Production 383, 135235. DOI: https://doi.org/10.1016/j.jclepro.2022.135235
- [S2] ScienceDirect / Journal of Cleaner Production article page: https://www.sciencedirect.com/science/article/pii/S0959652622048090
- [S3] ResearchGate PDF/record for the same article: https://www.researchgate.net/publication/365763750_Reuse_of_concrete_components_in_new_construction_projectscritical_review_of_77_circular_precedents
- [S4] BauStatik-Wiki, Wiederverwendung von Stahlbetonbauteilen: https://baustatik-wiki.fiw.hs-wismar.de/mediawiki/index.php/Wiederverwendung_von_Stahlbetonbauteilen
- [S5] InNoWest Brandenburg, Bachelorarbeit zur Wiederverwendung von WBS70-Fertigteilen: https://innowest-brandenburg.de/beitraege/Bachelorarbeit-plattenbautyp-wbs-70
- [S6] BFT International, Wiederverwendung von Betonfertigteilplatten: https://www.bft-international.com/de/artikel/wiederverwendung-von-betonfertigteilplatten-4095412.html
- [S7] Seidl+Seidl Architekten, HAUS HOS Mühlhausen: https://www.seidlarchitekten.de/haus-hos-muehlhausen/
- [S8] Seidl+Seidl PDF, HAUS HOS Mühlhausen: https://www.seidlarchitekten.de/wp-content/uploads/2022/10/SeidlSeidl-Architekten_Haus-Hos_Muehlhausen.pdf
- [S9] Stern, Vorzeigeimmobilien: Recycling der Platte: https://www.stern.de/wirtschaft/immobilien/vorzeigeimmobilien-recycling-der-platte-3300150.html
