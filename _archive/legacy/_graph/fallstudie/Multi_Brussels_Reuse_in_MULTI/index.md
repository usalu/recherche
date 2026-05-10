---
id: "Multi_Brussels_Reuse_in_MULTI"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "Multi Brussels / Reuse in MULTI – Fallstudie Direct Reuse / zirkuläres Bauen"
bauobjekt:
  - "Multi_Brussels_Reuse_in_MULTI"
legacy_paths:
  - "Gebäude\\Multi_Brussels_Reuse_in_MULTI.md"
projekt:
  - "Multi_Brussels_Reuse_in_MULTI"
reuse_chain_detected: "False"
---
# Multi Brussels / Reuse in MULTI – Fallstudie Direct Reuse / zirkuläres Bauen

## Migration

- Fallstudie ID: Multi_Brussels_Reuse_in_MULTI
- Legacy source count: 1
- Generated project: Multi_Brussels_Reuse_in_MULTI
- Generated bauobjekt: Multi_Brussels_Reuse_in_MULTI
- Extracted reuse_einsatz rows: 7
- Extracted datenpunkt rows: 12
- Extracted entity mapping rows: 18
- Reuse chain detected: False

## Legacy Content

### Legacy Source: Gebäude\Multi_Brussels_Reuse_in_MULTI.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Multi_Brussels_Reuse_in_MULTI
- Secondary targets: projekt/Multi_Brussels_Reuse_in_MULTI; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Multi Brussels / Reuse in MULTI – Fallstudie Direct Reuse / zirkuläres Bauen

**Projekt:** MULTI / ehemaliger Philips- bzw. Brouckère Tower, Brüssel  
**Bearbeitung:** Deutsch, kompakt, quellenbasiert  
**Grundregel:** Gezählt werden nur wiederverwendete Bau-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Bestandserhalt und lose Möbel werden nicht als Direct Reuse gewertet.

---

## 1. EINORDNUNG

- **Entscheidung:** VERGLEICHSFALL
- **Bewertung:** ★★★☆☆
- **Begründung:** MULTI ist ein großmaßstäblicher Umbau mit gut dokumentierter Urban-Mining- und Materialpass-Logik. Für diese Liste zählt jedoch nicht der bloße Erhalt von 89 % des bestehenden Betons, sondern die tatsächlich transformierten oder extern wiederverwendeten Bauteile: Blaustein-Fassadenplatten, Granit-/Natursteinplatten, Aluminiumprofile, wieder eingebaute Aufzugstechnik und weitere feste Bauteile. Die Wiederverwendung ist bauteil- und hüll-/ausbaubezogen, nicht zentral tragend.
- **Vertrauensgrad:** belegt
- **Warnung Bestandserhalt:** ja
- **Warnung Möbel/Dekoration:** ja
- **Projektstatus:** gebaut / fertiggestellt

---

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | MULTI Brussels / Reuse in Multi | Umbau mit Reuse-/Urban-Mining-Strategie | S1, S2, S5 | belegt | ehem. Brouckère/Philips Tower |
| Gebäude | ehemaliger Philips Tower / Brouckère Tower | Bestandsgebäude, 1969 | S1, S5 | belegt | Bestandserhalt nur als Kontext |
| Ort | Boulevard Anspach / De Brouckère, Brüssel | Standort | S3, S5 | belegt | genaue Adresse teils Boulevard Anspachlaan |
| Projekt | großmaßstäbliche Büro-/Mixed-use-Rekonversion | Reuse-Fall im Hochhausumbau | S1, S3 | belegt | 44.200–45.800 m² je nach Quelle |
| People | Whitewood, Immobel, CONIX RDBM, Cordeel, Rotor, RotorDC, Madaster/EPEA | Bauherr/Entwickler, Architektur, Ausführung, Reuse-Beratung, Materialpass | S1–S6 | belegt | Rollen je Quelle |
| Bauteil | Blaustein-Fassadenblöcke/-platten | in situ bzw. transformierte Wiederverwendung | S2, S6 | belegt | Naturstein aus ursprünglicher Fassade |
| Bauteil | Granitplatten, Natursteinplatten | Boden/Terrasse/Treppenpodest | S3, S5 | belegt | teils externe Herkunft |
| Bauteil | Aluminiumprofile | Balustraden und Lichtarmaturen | S3, S4 | belegt | ca. 1.300 m |
| Bauteil | Aufzugsmotoren | demontiert und eine Etage höher wieder eingebaut | S5 | belegt | technisches Bauteil |
| Material | Betonbestand | 89 % bestehender Beton erhalten | S4, S7 | belegt | nach Grundregel überwiegend Bestandserhalt, nicht Direct Reuse |
| Datenmodell | Madaster Material Passport / Building Circularity Passport | Materialdokumentation | S4 | belegt | Digitaler Materialpass |
| Bauteilbörse | RotorDC | urban mining / Vermittlung / Wiederverwendung | S5, S8 | belegt | direkte Beschaffung nicht für jedes Bauteil einzeln belegbar |
| Prozessphase | Demontage / Remanufacturing / Wiedereinbau | Naturstein und weitere Bauteile | S2, S6 | belegt | technische Details begrenzt |
| Hürde | Großmaßstäblicher, hochkodifizierter Hochbau | Reuse-Integration in formalisierte Prozesse | S5 | belegt | Qualitäts-/Prozesshürden |
| Kennwert | 44.200 / 45.000 / 45.800 m² | Fläche je Quelle | S1, S4, S5 | teilweise belegt | Quellenkonflikt |
| Kennwert | 2 % bzw. 3 % Urban Mining / externe Reuse-Materialien | Anteil externer Reuse-Komponenten | S4, S7 | teilweise belegt | Quellenkonflikt |
| Recht | BREEAM Excellent | Nachhaltigkeitszertifizierung | S1, S3 | belegt | kein Reuse-Normnachweis |
| Software | Madaster | Materialpass | S4 | belegt | digitale Dokumentation |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Materialpass | trennt Datenmodell/Software von konkreter Gebäudedokumentation | Madaster / Building Circularity Passport | Datenmodell, Software, Kennwert, Bauteil |
| Reuse-Beratung | spezifische Planungsrolle zwischen Entwurf, Beschaffung und Prüfung | Rotor als Design-Assistance | People, Prozessphase, Methode |
| In-situ-Transformation | Bauteil bleibt aus demselben Gebäude, erhält aber neue Funktion | Blaustein-Fassade zu Terrasse/Wandbekleidung | Bauteil, Reuse-Strategie, Prozessphase |

---

## 3. FALLSTUDIE

- **Name:** MULTI Brussels / Reuse in Multi
- **Ort:** Brüssel, Belgien
- **Gebäude:** ehemaliger Philips Tower / Brouckère Tower
- **Projekt:** Renovierung / Rekonversion zu Büro-/Mixed-use-Gebäude mit Urban Platform
- **Beteiligte People / Akteure:** Whitewood, Immobel, CONIX RDBM, Cordeel, Rotor, RotorDC, Madaster, EPEA; weitere technische Partner unbekannt
- **Architekt:** CONIX RDBM Architects
- **Tragwerksplaner:** unbekannt
- **Bauherr:** Whitewood und Immobel / Entwicklungsstruktur je Quelle unterschiedlich beschrieben
- **Zeitraum:** 2015–2024 nach CONIX RDBM; Q1 2019–Q1 2022 nach Cordeel; 2018–2022 nach Whitewood; Quellenkonflikt
- **Ursprüngliche Nutzung:** Bürohochhaus der 1960er Jahre
- **Neue Nutzung:** flexible Büro-/Mixed-use-Flächen, öffentliche Durchwegung / Urban Platform
- **Fläche / Maßstab:** 44.200 m², 45.000 m² oder 45.800 m²; Quellenkonflikt
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** gut für Akteure, Zeitraum, Fläche, Materialpass und zentrale Reuse-Bauteile; unvollständig für technische Prüfungen, Normen, Kosten und Gewährleistung

---

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; in-situ transformiert; ex-situ; Bauteilwiederverwendung; Materialwiederverwendung; adaptive reuse
- **Hauptniveau:** Gebäudehülle; räumlicher Innenausbau; technische Gebäudeausrüstung; Material; nicht primär Tragwerk
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Der erhaltene Beton des Bestandsgebäudes zählt hier nicht als Direct Reuse, weil er überwiegend am Ort bleibt und dieselbe tragende Funktion behält. Gezählt werden transformierte und neu eingesetzte Reuse-Bauteile wie Blaustein, Granit, Aluminiumprofile und Aufzugstechnik.
- **Warum ist der Fall relevant?** Er zeigt, wie Reuse in einem großen kommerziellen Bürohochhaus mit Materialpass, Urban Mining und Reuse-Beratung versucht wurde, auch wenn der direkte Bauteilanteil relativ klein blieb.

---

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Blausteinblöcke / Fassadenplatten | Belgischer Blaustein | ursprüngliche Fassade MULTI | Fassadenbekleidung | Terrasse, Wandbekleidung, neue Plinthe / Innenraum | 82 Blöcke bzw. ca. 280 m² / 140 t in Salvage-Bericht | nein | ja | ja | nein | Demontage, Sägen, Remanufacturing, Wiederverlegung | unbekannt | unbekannt | Witterung, Rutschhemmung, Befestigung | unbekannt | Bruchrisiko, Bearbeitung | S2, S6 | Normen, genaue Prüfwerte |
| Blaustein-Flagstones | Naturstein | Platz in Brügge | Außenbelag | Atriumboden | unbekannt | nein | ja | nein | nein | Bergung, Zuschnitt/Dimensionierung | unbekannt | unbekannt | Bodenbelag | unbekannt | Passung, Muster | S5 | Menge |
| Granitboden | geflammter Granit | Générale de Banque | Bodenbelag | Treppenpodest / öffentlicher Bereich | unbekannt | nein | ja | nein | nein | Bergung und Wiedereinbau | unbekannt | unbekannt | Trittsicherheit | unbekannt | Logistik | S5 | Menge |
| Granitplatten Terrasse | Granit | Pariser Bürogebäude / extern | Bodenbelag | öffentliche Terrasse | unbekannt / Cordeel nennt 400 recovered granite tiles | nein | ja | nein | nein | Reinigung, Verlegung | unbekannt | unbekannt | Außenbelag | unbekannt | Verfügbarkeit | S3, S5 | genaue Herkunft je Platte |
| Aluminiumprofile | Aluminium | Brouckère Tower | Fassaden-/Gebäudeelemente unbekannt | Balustraden, Lichtarmaturen | ca. 1.300 m | nein | ja | nein | teilweise | Zuschnitt, Umnutzung | unbekannt | unbekannt | Absturzsicherung, Elektrointegration bei Leuchten | unbekannt | Zulassung / Anschlussdetails | S3, S4 | genaue alte Funktion |
| Aufzugsmotoren | Metall / Technik | Bestand MULTI | Aufzugstechnik | eine Etage höher wieder installiert | unbekannt | nein | nein | nein | ja | Demontage, Reinstallation | unbekannt | unbekannt | Betriebssicherheit | unbekannt | technische Freigabe | S5 | Typ, Leistung |
| Türen / Wände / Einbauten | Holz/Metall/sonstige | C-wood / Projektlieferungen | unbekannt | Türen, Wände, Postfächer, Schließfächer | unbekannt | nein | ja | nein | nein | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | nicht als Reuse belegbar | S3 | ob reused oder neu |

---

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Ermittlung nutzbarer Bauteile im Bestandsgebäude | Whitewood, Immobel, CONIX RDBM, Rotor | Reuse-Beratung, Materialanalyse | unbekannt | selektive Demontage geplant | unbekannt | unbekannt | unbekannt | Hochhaus mit formalen Prozessen | frühe Einbindung Reuse-Partner | S5 |
| Bauteilinventar | Materialpass für Gebäude | Madaster, EPEA, Projektteam | Digitaler Materialpass | Madaster, Building Circularity Passport | nicht zutreffend | nicht zutreffend | Datenprüfung unbekannt | digital | Langzeitdokumentation | Materialpass | S4 |
| Schadstoffprüfung | Altgebäude prüfen | Projektteam | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Quellen nennen Asbest als Renovierungshürde allgemein | unbekannt | S7 |
| Rückbau / Ausbau | Blaustein-Fassade demontieren | Cordeel, De Meuter, Rotor | selektiver Rückbau | unbekannt | schonende Demontage / Sägen | Palettierung, Lagerung | unbekannt | Lagerung bei RotorDC | Bruchrisiko | chirurgische Präzision, Sandbett, Paletten | S6 |
| Transport | Bauteile zu Werkstatt / Lager / Projekt | RotorDC, Carrière de Maffle, Projektteam | just-in-time / Materiallogistik | unbekannt | nicht zutreffend | unbekannt | unbekannt | enges innerstädtisches Baufeld | geringe Lagerfläche | just-in-time-Lieferungen | S3 |
| Aufbereitung | Blaustein remanufacturing | Carrière de Maffle | Sägen, Umformatieren | Steinwerkstatt | nicht zutreffend | Remanufacturing | unbekannt | Rücktransport | schwere 800-kg-Blöcke | Fachbetrieb | S2 |
| Planung | Design aus verfügbaren Reuse-Bauteilen | CONIX RDBM, Rotor | Design assistance | unbekannt | nicht zutreffend | nicht zutreffend | unbekannt | Materialverfügbarkeit | Reuse muss in High-End-Projekt passen | begrenzte Materialpalette | S5 |
| Genehmigung | Integration in BREEAM / Hochhausumbau | Projektteam | Zertifizierung | BREEAM | unbekannt | unbekannt | unbekannt | unbekannt | formale Anforderungen | BREEAM Excellent angestrebt/erreicht je Quelle | S1, S3 |
| Wiedereinbau | Naturstein, Aluminium, Aufzugsmotoren | Cordeel, Fachunternehmen | Wiedereinbau / Umnutzung | unbekannt | nicht zutreffend | je Bauteil | unbekannt | richtige Mengen je Geschoss | Puzzlearbeit | just-in-time und Etagenlogistik | S3 |
| Monitoring | Materialdaten dokumentieren | Madaster/EPEA | Materialpass | Madaster | nicht zutreffend | nicht zutreffend | unbekannt | digital | langfristige Aktualität | digitaler Gebäudepass | S4 |

---

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Bestandstragwerk weitgehend erhalten | Standsicherheit | unbekannt | unbekannt | zählt nicht als Direct Reuse, wenn gleiche Funktion | Bewertung getrennt | S4, S7 |
| Lastabtragung | keine zentrale wiederverwendete Tragwerkskomponente belegt | unbekannt | unbekannt | unbekannt | Reuse nicht tragwerksdominant | Einordnung als Vergleichsfall | S5 |
| Verbindung | Naturstein, Aluminiumprofile und Leuchten neu angeschlossen | Befestigung, Absturzsicherung, Elektrosicherheit | unbekannt | unbekannt | Anschluss an Bestands-/Neubausystem | unbekannt | S3, S5 |
| Brandschutz | Hochhausumbau, Anforderungen anzunehmen | Brandschutzkonzept | unbekannt | unbekannt | öffentlich nicht detailliert | unbekannt | unbekannt |
| Schallschutz | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Feuchte | Naturstein im Außen-/Terrassenbereich | Frost-/Feuchtebeständigkeit | unbekannt | unbekannt | wiederverwendeter Naturstein | Steinbearbeitung | S2 |
| Wärmeschutz | neue Fassade / Energieeffizienz | BREEAM, Energieeffizienz | unbekannt | unbekannt | Bestandshochhaus energetisch aufwerten | Dämmung, PV, Wärmepumpen | S3 |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Luftdichtheit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| TGA-Integration | Aufzugsmotoren reinstalled; neue TGA durch Imtech | Betriebssicherheit, Energieeffizienz | unbekannt | unbekannt | alte Technik weiterverwenden | Reinstallation / neue Systeme | S3, S5 |
| Barrierefreiheit | öffentlich zugängliche Durchwegung/Urban Platform; Details unbekannt | unbekannt | unbekannt | unbekannt | Hochhausumbau | unbekannt | S1 |
| Dauerhaftigkeit | Naturstein und Aluminium langlebig | Außen- und Innenbelag | unbekannt | unbekannt | Zustand/Patina | Aufbereitung | S2, S3 |
| Wartung | Materialpass ermöglicht künftige Identifikation | Rückbaubarkeit / Wissenserhalt | unbekannt | unbekannt | Materialdaten gehen sonst verloren | Madaster | S4 |
| Zulassung | unbekannt | unbekannt | unbekannt | unbekannt | Reuse in formalen Hochbauprozessen | Reuse-Beratung | S5 |
| Haftung | unbekannt | unbekannt | unbekannt | unbekannt | gebrauchte Bauteile in High-End-Projekt | unbekannt | S5 |

---

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Fläche | 44.200 | m² | Projektangabe Cordeel | Gebäude | S3 | belegt |
| Fläche | 45.000 | m² | Projektangabe CONIX/Rotor | Gebäude | S1, S5 | belegt |
| Fläche | 45.800 | m² | Immobel/Madaster-Angabe | Gebäude | S4 | belegt |
| vorhandener Beton erhalten | 89 | % | Building Circularity Passport / Projektangabe | Bestand | S4, S7 | belegt, aber Bestandserhalt |
| Abfall vermieden durch Betonerhalt | 20.000 | t | Projektangabe | Bestandserhalt | S7 | belegt, nicht Direct-Reuse-Kernwert |
| Embodied Carbon durch Betonerhalt | 3.259 | t CO₂e | Projektangabe | Bestandserhalt | S7 | belegt, nicht Direct-Reuse-Kernwert |
| Blaustein demontiert | ca. 280 / 140 | m² / t | Rotor Salvage-Bericht | Naturstein-Fassade | S6 | teilweise belegt |
| Blausteinblöcke | 82 | Stück | Rotor | Naturstein | S2 | belegt |
| Aluminiumprofile | 1.300 | m | Projektangabe | Reuse-Bauteile | S3, S4 | belegt |
| Granitfliesen Terrasse | 400 | Stück | Cordeel | Reuse-Bodenbelag | S3 | belegt |
| externer Reuse-/Urban-Mining-Anteil | 2 bzw. 3 | % | Materialpass/Projektangaben | neue Materialien / Gesamtprojekt | S4, S7 | Quellenkonflikt |
| Kosten | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |

---

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Reuse-Anteil im Großprojekt niedrig | wirtschaftlich/technisch | Hohe Anforderungen, große Mengen, Planungssicherheit | Zielwerte 2/3 % Urban Mining bleiben relativ klein | Material, Bauteil, Methode | Reuse-Beratung und Materialpass | In Großprojekten früh starten und realistische Quoten setzen | S4, S5 |
| Bestandserhalt vs Direct Reuse | methodisch | Erhaltener Beton dominiert Kennwerte | Gefahr der Überbewertung | Kennwert, Bewertung | separate Bilanzierung | Bestandserhalt nicht mit Bauteilwiederverwendung verwechseln | S4, S7 |
| Natursteinbruch bei Demontage | technisch/logistisch | schwere Platten, verdeckte Befestigungen | Verlust / Bruchrisiko | Bauteil, Abbruchmethode | präzises Sägen, Sandbett, Palettierung | Rückbau muss handwerklich geplant werden | S6 |
| Materiallogistik im Zentrum | logistisch | enges innerstädtisches Baufeld | Etagen- und Zeitdruck | Logistik, Prozessphase | just-in-time | Reuse braucht Baustellenlogistik wie TGA/Tragwerk | S3 |
| Norm-/Haftungsfragen | rechtlich/technisch | gebrauchte Bauteile im hochwertigen Bürobau | Freigabeaufwand | Recht, Prüfung | unbekannt | Prüfkette dokumentieren | S5 |
| Quellenkonflikte | wissenschaftlich | unterschiedliche Flächen-/Prozentangaben | unscharfe Kennwerte | Kennwert | Angaben nebeneinander führen | keine Glättung ohne Primärquelle | S1, S3, S4, S7 |

---

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** Urban Mining, in-situ Materialtransformation und externe Reuse-Materialien über Reuse-Netzwerke; Rotor/RotorDC als Reuse-Akteur.
- **Bauteilbörse / Quelle:** RotorDC / Reuse-Sektor; Madaster als Dokumentationsplattform, keine Bauteilbörse.
- **Kostenwirkung:** unbekannt.
- **Zeitwirkung:** Wiederverwendung erforderte sechsjährige Zusammenarbeit bzw. langen Prozess nach Rotor; konkrete Mehrzeit unbekannt.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** hoch bei Natursteinrückbau, Sortierung, Anpassung, Etagenlogistik; genaue Stunden unbekannt.
- **Lagerung:** Naturstein wurde gelagert / über RotorDC bzw. Werkstattprozesse geführt; Details unbekannt.
- **Marktbarrieren:** Formalisierte Hochbauprozesse, ausreichende Mengen, gleiche Qualität, Lieferzeiten, technische Freigaben.

---

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** hoch bei Blaustein und Natursteinoberflächen; Aluminiumprofile und Technik weniger offensichtlich.
- **räumliche Transformation:** ehemaliger monofunktionaler Büroblock wird zu öffentlicherem Urban Platform-Konzept.
- **Atmosphäre / Ausdruck:** heller, transparenter Umbau statt dunkler „black box“.
- **Umgang mit Spuren:** Natursteinpatina und vorhandene Materialgeschichte werden sichtbar bzw. weitergeführt.
- **sozialer Wert:** öffentliche Durchwegung, Stadtreparatur und Nutzungsaktivierung.
- **Denkmal- oder Bestandswert:** modernistischer/Brüsselisierung-Kontext, Schutzstatus unbekannt.
- **Kritik / Grenzen:** Direct-Reuse-Anteil bleibt gegenüber Bestandserhalt klein; Gefahr, große CO₂-Kennwerte aus Betonerhalt als Bauteilwiederverwendung zu missverstehen.

---

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** Tragwerksplaner, konkrete Prüfberichte, Normen, Versicherungsmodell, Gewährleistung, Kosten, detaillierte Leistungsanforderungen.
- **Welche neuen Entitäten wären sinnvoll?** Materialpass; Reuse-Beratung; In-situ-Transformation.
- **Welche Daten fehlen?** geprüfte Mengen je Reuse-Bauteil, Einbauorte, Befestigungsdetails, Prüfmethoden, CO₂ nur für Direct-Reuse-Bauteile, Kosten und Bauzeitwirkung.
- **Welche Quellen müssten geprüft werden?** Buch „Working with MULTI“, Madaster-/EPEA-Pass, Rotor-Projektunterlagen, Ausschreibungs-/Bauakten, technische Prüfberichte.

---

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** Anhang / Vergleichsfall, nicht als tragender Hauptfall.
- **5 wichtigste Fakten:**
  1. Großmaßstäbliche Rekonversion eines Brüsseler Bürohochhauses.
  2. Wiederverwendung von Blaustein, Granit/Naturstein, Aluminiumprofilen und Aufzugstechnik ist belegt.
  3. Der Erhalt von 89 % des Betons ist wichtig, zählt aber überwiegend als Bestandserhalt.
  4. Madaster-/Building-Circularity-Passport wurde eingesetzt.
  5. Quellen nennen unterschiedliche Flächen und Urban-Mining-Anteile.
- **5 wichtigste Bauteile:**
  1. Blaustein-Fassadenblöcke/-platten.
  2. Granit-/Natursteinplatten für Böden/Terrasse.
  3. Aluminiumprofile.
  4. Aufzugsmotoren.
  5. Wiederverwendete bzw. dokumentierte Materialpass-Bauteile unbekannter Detailtiefe.
- **5 wichtigste Hürden:**
  1. Großmaßstäbliche Qualitätssicherung.
  2. Natursteinbruch beim Rückbau.
  3. innerstädtische Just-in-time-Logistik.
  4. Norm-/Haftungsfragen.
  5. methodische Trennung Bestandserhalt vs Direct Reuse.
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Reuse-Beratung muss sehr früh eingebunden werden.
  2. Materialpass hilft für künftige Reuse-Zyklen.
  3. In-situ-Transformation von Hüllmaterialien kann architektonisch stark sein.
  4. Große Projekte brauchen realistische Reuse-Quoten.
  5. Kennwerte müssen nach Bilanzgrenzen getrennt werden.
- **5 offene Fragen:**
  1. Welche Norm-/Prüfverfahren wurden für Naturstein und Aluminium angewendet?
  2. Welche Bauteile kamen tatsächlich von externen Urban-Mining-Quellen?
  3. Welche Kostenmehr-/minderkosten entstanden?
  4. Welche Gewährleistungsregelung galt?
  5. Wie hoch war die CO₂-Wirkung nur der Direct-Reuse-Bauteile?

---

## Quellen und Links

- **S1** CONIX RDBM, „Multi“ – https://www.conixrdbm.com/project/multi/
- **S2** Rotor, „Reuse of blue limestone in Multi“ – https://rotordb.org/en/news/reuse-blue-limestone-multi
- **S3** Cordeel, „Multi - Brouckère“ – https://cordeel.eu/en/projects/multi-brouckere
- **S4** Immobel, „The materials passport used for the first time in a major renovation project“ – https://www.immobelgroup.com/en/news/the-materials-passport-used-for-the-first-time-in-a-major-renovation-project
- **S5** Rotor, „Reuse in the Multi project“ / „Multi - De Brouckère Tower“ – https://rotordb.org/en/projects/multi-de-brouckere-tower
- **S6** Rotor, „Reclaiming blue limestone slabs“ – https://rotordb.org/en/news/reclaiming-blue-limestone-slabs
- **S7** Whitewood / Drees & Sommer Projektangaben zu Multi – https://www.whitewood.eu/multibrussels ; https://www.dreso.com/de/en/company-2/press/press-releases/details/ressourcen-neu-gedacht-urban-mining-transformiert-bruessels-skyline
- **S8** RotorDC / circlemade Profil – https://circlemade.brussels/en/members/rotordc/
