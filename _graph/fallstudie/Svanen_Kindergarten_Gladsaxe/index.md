---
id: "Svanen_Kindergarten_Gladsaxe"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "Svanen / The Swan Kindergarten, Gladsaxe — Fallstudie Direct Reuse / Wiederverwendung"
bauobjekt:
  - "Svanen_Kindergarten_Gladsaxe"
legacy_paths:
  - "Gebäude\\Svanen_Kindergarten_Gladsaxe.md"
projekt:
  - "Svanen_Kindergarten_Gladsaxe"
reuse_chain_detected: "True"
---
# Svanen / The Swan Kindergarten, Gladsaxe — Fallstudie Direct Reuse / Wiederverwendung

## Migration

- Fallstudie ID: Svanen_Kindergarten_Gladsaxe
- Legacy source count: 1
- Generated project: Svanen_Kindergarten_Gladsaxe
- Generated bauobjekt: Svanen_Kindergarten_Gladsaxe
- Extracted reuse_einsatz rows: 12
- Extracted datenpunkt rows: 14
- Extracted entity mapping rows: 25
- Reuse chain detected: True

## Legacy Content

### Legacy Source: Gebäude\Svanen_Kindergarten_Gladsaxe.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Svanen_Kindergarten_Gladsaxe
- Secondary targets: projekt/Svanen_Kindergarten_Gladsaxe; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Svanen / The Swan Kindergarten, Gladsaxe — Fallstudie Direct Reuse / Wiederverwendung

**Sprache:** Deutsch  
**Arbeitsregel:** Gezählt werden nur wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Lose Möbel, Dekoration und reine Recyclingangaben werden nicht für die Direct-Reuse-Bewertung gezählt.  
**Kurzurteil:** Hauptfall, weil großformatige Holz-Dachbinder aus der ehemaligen Gladsaxe School die neuen Räume strukturieren; zusätzlich wurden Ziegel, Dachziegel und Stahlfassadenelemente direkt wiederverwendet.

---

## 1. EINORDNUNG

- **Entscheidung:** HAUPTFALL
- **Bewertung:** ★★★★★
- **Begründung:** Der Kindergarten nutzt Materialien vom Vorgängerbau auf demselben Grundstück. Entscheidend für die ★★★★★-Bewertung sind die **großen Holzträger/Dachbinder aus der ehemaligen Sporthalle**, die laut Lendager die neuen Räume strukturieren. Zudem wurden Ziegel, Dachziegel und Stahlfassadenelemente wiederverwendet. Angaben zu Lampen, Fahrradständern und Möbeln werden nicht oder nur bei fest eingebauten technischen Elementen vorsichtig berücksichtigt.
- **Vertrauensgrad:** belegt / teilweise belegt
- **Warnung Bestandserhalt:** nein — der alte Schulbau wurde abgebrochen; Bauteile wurden transformiert und in den Neubau integriert.
- **Warnung Möbel/Dekoration:** ja — Quellen nennen Lampen, Fahrradständer, Uhr, Observatoriumskuppel; diese erhöhen die Reuse-Bewertung nicht, wenn sie nicht festes Bau-/Technikelement sind.
- **Projektstatus:** gebaut

---

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Svanen / The Swan / Børnehuset Svanen | Untersuchter Fall | [S1], [S2], [S3] | belegt | kreislauforientierter Kindergarten |
| Ort | Gladsaxe, Dänemark | Standort | [S1], [S2], [S3] | belegt | auf dem Gelände der ehemaligen Gladsaxe School |
| Projekt | Circular daycare / kindergarten | Neubau | [S1], [S4], [S5] | belegt | kommunaler Kindergarten |
| Gebäude | ehemalige Gladsaxe School | Donorgebäude | [S1], [S2], [S6] | belegt | 2020 abgebrochen |
| People | Gladsaxe Municipality / Gladsaxe Kommune | Bauherr / Kommune | [S1], [S2], [S3] | belegt | kommunaler Auftraggeber |
| People | Lendager | Architekturberatung, Nachhaltigkeitsberatung, Demolition tender | [S1], [S2] | belegt | Design / circular process |
| People | Sweco / Sweco Architects | Kollaborateur / Architekt | [S1], [S3], [S5] | belegt | Quellen nennen Sweco/NIRAS bzw. Sweco Architects |
| People | NIRAS | Kollaborateur | [S1], [S2] | belegt | technische/planerische Rolle nicht vollständig detailliert |
| People | Tscherning, Ason A/S, Aksel V. Jensen | Projektteam laut Troldtekt | [S7] | teilweise belegt | Rollen nicht vollständig ausgeführt |
| Bauteil | Holz-Dachbinder / timber roof trusses / rafters | zentrale tragende Wiederverwendung | [S1], [S2], [S6] | belegt | aus ehemaliger Schule/Sporthalle |
| Bauteil | Ziegel / bricks | direkt wiederverwendete feste Bauteile | [S1], [S2], [S6] | belegt | Innen- und Außenflächen |
| Bauteil | Dachziegel / roof tiles / vingetegl | Hülle/Oberflächen | [S1], [S2], [S6] | belegt | Dach/Fassade/Oberflächen |
| Bauteil | Stahlfassadenelemente / façade panels | Hülle | [S1], [S6] | belegt | Direktreuse genannt |
| Bauteil | Beton | Recycling / Materialwiederverwertung, nicht Direct Reuse im engeren Sinn | [S6] | belegt | 6.000 t abgebrochen, 600 t als Zuschlag; nicht als Bauteil-Direct-Reuse zählen |
| Bauteil | Lampen / Fahrradständer / Uhr / Observatoriumskuppel | kulturelle/technische Einzelobjekte | [S1], [S2], [S6] | teilweise belegt | nur fest eingebaute technische Elemente ggf. zählen; Dekor/Furniture nicht |
| Reuse-Strategie | Circular building site / on-site depot | Prozessstrategie | [S1] | belegt | Demontage, Sortierung, Lagerung und Neubau integriert |
| Methode | Material mapping vor Abbruch | Bauteilidentifikation | [S1], [S8] | belegt | frühzeitige Erfassung |
| Logistik | on-site storage / temporäres Materialdepot | lokale Kreisläufe | [S1] | belegt | reduziert Transport |
| Kennwert | 1.436 m² | Fläche Lendager | [S1] | belegt | Sweco nennt 1.270 m²; Quellenabweichung |
| Kennwert | 1.270 m² | Fläche Sweco | [S5] | teilweise belegt | Abweichung zu Lendager |
| Kennwert | 6.278 t Materialeinsparung / 178 t CO₂ | Award-/Pressekennwerte | [S7], [S9], [S10] | teilweise belegt | Bilanzgrenze nicht auf Direct Reuse beschränkt |
| Förderprogramm | unbekannt | — | — | unklar | keine spezifische Förderung gefunden |
| Norm/Recht | Nordic Swan Ecolabel / Svanemærket | Zertifizierung | [S2], [S3], [S10] | belegt | keine Baunormnummer |
| Hürde | nachhaltiger Rückbau als neuer Ausschreibungsprozess | Prozess / Vergabe | [S9] | teilweise belegt | BygTek nennt neuen Prozess als branchestandard |
| Schadstoff | chemische Anforderungen des Nordic Swan Ecolabel | Material-/Innenraumprüfung | [S10] | teilweise belegt | keine spezifischen Schadstoffe genannt |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Circular building site | Prozess ist nicht linearer Abriss + Neubau | Demontage, Lagerung, Neubau am selben Ort | Methode, Logistik, Prozessphase |
| Same-site urban mining | Donor und Empfänger sind dasselbe Grundstück | Gladsaxe School → Svanen | Ort, Donorgebäude, Logistik |
| Erinnerungsbauteil | kultureller Wert zählt getrennt von technischer Reuse | Schuluhr, Observatoriumskuppel | Gestaltung, sozialer Wert, Bauteil |
| Reuse vs. Recycling-Bilanz | nötig zur sauberen Bewertung | Betonrecycling nicht als Direct Reuse | Kennwert, Material, Methode |

---

## 3. FALLSTUDIE

- **Name:** Svanen / The Swan / Børnehuset Svanen
- **Ort:** Gladsaxe, Dänemark
- **Gebäude:** Kindergarten / daycare centre / integriertes Kinderhaus
- **Projekt:** Neubau auf dem Gelände der ehemaligen Gladsaxe School aus Materialien des Vorgängerbaus
- **Beteiligte People / Akteure:** Gladsaxe Municipality; Lendager; Sweco/Sweco Architects; NIRAS; Tscherning; Ason A/S; Aksel V. Jensen A/S
- **Architekt:** Lendager; Sweco Architects wird ebenfalls als Architekt genannt
- **Tragwerksplaner:** unbekannt; Aksel V. Jensen A/S als beratende Ingenieure in Teamquelle genannt
- **Bauherr:** Gladsaxe Municipality / Gladsaxe Kommune
- **Zeitraum:** 2019–2022; alter Schulabbruch 2020; Öffnung April 2022 laut State of Green; abgeschlossen
- **Ursprüngliche Nutzung:** Gladsaxe School / Schule, inkl. Sporthalle
- **Neue Nutzung:** Kindergarten / daycare centre für Kinder, darunter Angebote für Kinder mit besonderen Bedürfnissen
- **Fläche / Maßstab:** 1.436 m² nach Lendager; 1.270 m² nach Sweco; Quellenabweichung, daher **1.270–1.436 m²**
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** gut für Prozess, Akteure, zentrale Bauteilgruppen; mittel für Prüfungen, Normen, Mengen einzelner Direct-Reuse-Bauteile

---

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; in-situ transformiert am selben Standort; Bauteilwiederverwendung; Materialwiederverwendung; Recycling ergänzend
- **Hauptniveau:** Tragwerk und Gebäudehülle; zusätzlich räumliche Innen-/Außenoberflächen
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Der alte Schulbau wurde nicht einfach weitergenutzt. Bauteile wurden demontiert, sortiert, gelagert und in neuer Funktion im Kindergarten eingesetzt. Zerkleinerter Beton als Zuschlag ist Recycling/Materialwiederverwertung und wird getrennt von Direct Reuse geführt.
- **Warum ist der Fall relevant?** Svanen zeigt kommunalen Same-site-Urban-Mining-Prozess mit frühzeitiger Materialkartierung, lokaler Lagerung und gestalterisch sichtbarer Wiederverwendung. Die tragenden Holzträger machen den Fall stärker als reine Hüllen- oder Ausbaubeispiele.

---

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Holz-Dachbinder / timber trusses | Holz | ehemalige Sporthalle / Schule | Dachtragwerk | Strukturierung / Tragwerk neuer Räume | unbekannt | ja | ja | evtl. | nein | Demontage, Sortierung, Lagerung, Wiedereinbau | unbekannt | unbekannt | Tragfähigkeit, Brandschutz, Dauerhaftigkeit | unbekannt | Nachweis Alt-Holz | [S1], [S2] | Anzahl, Querschnitte, Holzqualität |
| Holzrafters / træspær | Holz | Gladsaxe School | Dach/Tragwerk | Bauteil im neuen Kindergarten | unbekannt | wahrscheinlich ja | ja | evtl. | nein | Ausbau/Wiedereinbau | unbekannt | unbekannt | Tragfähigkeit | unbekannt | unbekannt | [S2], [S6] | exakte Funktion |
| Ziegel / bricks | Keramik | alte Schule | Mauerwerk/Oberflächen | Innen- und Außenflächen | unbekannt | unbekannt | ja | ja/teilweise | nein | schonender Rückbau, Reinigung, Wiedereinbau | Mörtel unbekannt | unbekannt | Dauerhaftigkeit, Frost, ggf. Tragfähigkeit | unbekannt | Bruch, Mörtelreste | [S1], [S2], [S6] | Menge |
| Dachziegel / roof tiles / vingetegl | Keramik | alte Schule | Dachdeckung | Dach/Fassade/Oberflächen | unbekannt | nein | ja | ja | nein | Demontage, Sortierung, Wiedereinbau | unbekannt | unbekannt | Witterung, Wasserführung, Frost | unbekannt | Qualität/Bruch | [S1], [S2], [S6] | Menge |
| Stahlfassadenelemente / facade panels | Stahl/Metall | alte Schule | Fassadenelemente | neue Fassaden-/Hüllenelemente | unbekannt | nein | ja | ja | nein | Demontage, Lagerung, Wiedereinbau | unbekannt | unbekannt | Korrosion, Wind, Witterung | unbekannt | Anpassung | [S1], [S6] | Anzahl |
| Beton | Beton | abgebrochene Schule | Tragwerk / Bauteil | Recycling-Zuschlag in Fundament/tragenden Konstruktionen | 6.000 t zerkleinert; 600 t als grober Zuschlag | als Bauteil: nein; als Recyclingmaterial in tragenden Bauteilen: ja | nein | nein | nein | Zerkleinerung, Recyclingzuschlag | monolithisch neu | Betonprüfung unbekannt | Betonqualität | unbekannt | zählt nicht als Direct-Reuse-Bauteil | [S6] | genaue Rezeptur |
| Schuluhr | unbekannt | Schulhof | Uhr | Orangery / Erinnerungselement | 1? | nein | ja/gestalterisch | nein | technisch? | Umsetzung | unbekannt | unbekannt | unbekannt | unbekannt | nicht als Score-Bauteil | [S1] | Einbauart |
| Observatoriumskuppel | unbekannt | alte Schule | Observatorium | Spielhaus | 1? | nein/unklar | ja | evtl. | nein | Umsetzung | unbekannt | unbekannt | Sicherheit | unbekannt | eher kulturelles Objekt | [S1] | Konstruktion |
| Lampen | unbekannt | alte Schule | Beleuchtung | evtl. Beleuchtung | unbekannt | nein | nein | nein | ja, falls fest installiert | Reinigung/Prüfung unbekannt | Elektroanschluss | unbekannt | Elektrosicherheit | unbekannt | nur zählen, wenn fest eingebaut und geprüft | [S2], [S6] | Einbau/Prüfung |
| Fahrradständer | Stahl | alte Schule | Fahrradparken | unbekannt / Außenraum | unbekannt | nein | nein | nein | nein | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | nicht Score-relevant | [S2], [S6] | Menge |
| Sanitär | unbekannt | unbekannt | unbekannt | Sanitär Kindergarten | unbekannt | nein | nein | nein | ja | unbekannt | unbekannt | unbekannt | Hygiene | unbekannt | nicht belegt | — | ja |
| Innenwände / Decken | Troldtekt acoustic panels neu? | Produktquelle | — | Akustikdecken/-wände | unbekannt | nein | ja | nein | nein | neu bzw. nicht als Reuse belegt | Schrauben | Produktzertifizierung | Akustik/Innenraum | Nordic Swan Kontext | nicht als reuse belegt | [S3] | Reuse-Anteil |

---

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Materialkartierung vor Abriss | Lendager, Gladsaxe Municipality, Team | early mapping | unbekannt | — | — | unbekannt | same-site | wissen, was verfügbar ist | Materialmapping | [S1], [S8] |
| Bauteilinventar | Ziegel, Dachziegel, Holzträger, Stahlfassade etc. ausgewählt | Lendager, Kommune | Auswahl und Zusammenstellung | unbekannt | — | — | unbekannt | Baustelle als Materialdepot | Bauteilqualität und Menge | Sortierung | [S1], [S2] |
| Schadstoffprüfung | im Kontext Nordic Swan strenge Chemikalienanforderungen; projektspezifisch unbekannt | Team / Zertifizierung | Materialanforderungen | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Altmaterial + Chemikalienkriterien | Auswahl geeigneter Materialien | [S10] |
| Rückbau | alte Gladsaxe School 2020 abgebrochen | Kommune, Rückbauunternehmen | nachhaltiger/schonender Rückbau | unbekannt | careful demolition | Sortierung | unbekannt | same-site | Materialerhalt | nachhaltiger Rückbauprozess | [S2], [S9] |
| Ausbau | wiederverwendbare Bauteile demontiert | Rückbau/Team | selektive Demontage | unbekannt | schonend | Reinigung/Sortierung | unbekannt | vor Ort | Bruch/Schäden | sortieren und lagern | [S1] |
| Transport | Material bleibt auf dem Gelände | Projektteam | minimierter Transport | unbekannt | — | — | — | on-site storage | Platz auf Baustelle | temporäres Depot | [S1] |
| Lagerung | Bauteile vor Ort gelagert | Projektteam | Baustelle als Materialdepot | unbekannt | — | Witterungsschutz unbekannt | unbekannt | same-site | Platz/Wetter | integrierter Bauablauf | [S1] |
| Aufbereitung | Reinigen, Sortieren, ggf. Zuschnitt | Fachfirmen | upcycling | unbekannt | — | Anpassung | unbekannt | Baustelle/Werkstatt | heterogene Bauteile | design follows availability | [S1] |
| Planung | Entwurf aus Materialflüssen entwickelt | Lendager, Sweco/NIRAS | form follows availability | unbekannt | — | — | unbekannt | — | verfügbare Mengen/Geometrien | flexible Gestaltung | [S1] |
| Genehmigung | Nordic Swan Ecolabel Zertifizierung | Kommune, Ecolabel, Team | Zertifizierung | unbekannt | — | — | Drittprüfung im Labelkontext genannt | — | strenge Anforderungen | Auswahl/Qualitätskontrolle | [S10] |
| Wiedereinbau | Träger, Ziegel, Dachziegel, Stahlfassade integriert | Ausführungsteam | Montage | unbekannt | — | — | unbekannt | Baustelle | Passung, Normen | integrierter Prozess | [S1], [S2] |
| Monitoring | Awards und Berichte | Danish Design Award, Building Awards, Medien | Auswertung/Kommunikation | unbekannt | — | — | — | — | Übertragbarkeit | öffentliche Dokumentation | [S3], [S7], [S9] |

---

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | große Holzträger aus ehemaliger Sporthalle strukturieren neue Räume | Tragfähigkeit, Brandschutz, Dauerhaftigkeit | konkrete Normen unbekannt | öffentlich unbekannt | Alt-Holz in Kita-Neubau | frühe Materialkartierung und Planung | [S1] |
| Lastabtragung | Holzträger/roof trusses tragend oder raumbildend; genaue Lastwege unbekannt | Lasten Kindergarten | unbekannt | unbekannt | Nutzung mit Kindern, Sicherheit | unbekannt | [S1], [S2] |
| Verbindung | unbekannt | Kraftübertragung und Montage | unbekannt | unbekannt | alte Bauteilgeometrie | unbekannt | — |
| Brandschutz | nicht detailliert | Kita/Kindergarten erhöhte Anforderungen | unbekannt | unbekannt | alte Holzbauteile + Kinderhaus | unbekannt | — |
| Schallschutz | Akustikdecken/-wandpaneele Troldtekt genannt, nicht als Reuse belegt | Akustik/Innenraum | Nordic Swan Kontext | Produkt-/Labelprüfung möglich, Details unbekannt | Kita-Akustik | Akustikpaneele | [S3] |
| Feuchte | Dachziegel und Fassadenelemente wiederverwendet | Witterungsschutz, Frost | unbekannt | unbekannt | gebrauchte Dachziegel | Sortierung/Einbau | [S1], [S6] |
| Wärmeschutz | Nordic Swan / energieeffiziente Kindergärten | geringer Energieverbrauch | Nordic Swan Ecolabel | Zertifizierung | Altmaterialien müssen Anforderungen erfüllen | Materialauswahl | [S10] |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Luftdichtheit | unbekannt | unbekannt | unbekannt | unbekannt | reused Hülle möglich | unbekannt | — |
| TGA-Integration | Lampen erwähnt, Details unbekannt | Elektrosicherheit / Energie | unbekannt | unbekannt | gebrauchte Leuchten? | unbekannt | [S2] |
| Barrierefreiheit | Kindergarten mit Kindern 0–6; Details unbekannt | Zugänglichkeit | unbekannt | unbekannt | unbekannt | unbekannt | [S4] |
| Dauerhaftigkeit | direkte Wiederverwendung plus Recycling soll neue Lebensdauer schaffen | 50–100 Jahre für Beton-Recycling in Synligbeton genannt | unbekannt | unbekannt | Betonrecycling nicht Direct Reuse | neue Betonrezeptur mit 600 t Zuschlag | [S6] |
| Wartung | unbekannt | unbekannt | unbekannt | unbekannt | heterogene reused Hülle | unbekannt | — |
| Zulassung | Nordic Swan Ecolabel als Zertifizierung | Material-, Chemikalien-, Qualitätssicherung | Svanemærket/Nordic Swan | Drittprüfung im Labelsystem | Reuse + strenge Materialanforderungen | Zertifizierungsprozess | [S10] |
| Haftung | unbekannt | unbekannt | unbekannt | unbekannt | Gebrauchtbauteile in öffentlichem Kita-Bau | unbekannt | — |

---

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Fläche Lendager | 1.436 | m² | Projektangabe | Gebäude | [S1] | belegt |
| Fläche Sweco | 1.270 | m² | Projektangabe | Gebäude | [S5] | teilweise belegt |
| Zeitraum | 2019–2022 | Jahre | Projektangabe | Planung/Bau | [S1] | belegt |
| Öffnung | April 2022 | Monat/Jahr | State of Green | Inbetriebnahme geplant/erfolgt | [S2] | teilweise belegt |
| Materialeinsparung | 6.278 | t | Award-/Presseangabe | Gesamtprojekt, nicht Direct-Reuse-only | [S7], [S9] | teilweise belegt |
| CO₂-Einsparung | 177.668 kg / ca. 178 t | kg / t CO₂ | Award-/Presseangabe | Gesamtprojekt; Bilanzgrenze unklar | [S7], [S9], [S10] | teilweise belegt |
| zerkleinerter Beton | 6.000 | t | Synligbeton | Betonrecycling alte Schule | [S6] | teilweise belegt |
| Recyclingbeton-Zuschlag | 600 | t | Synligbeton | grober Zuschlag in Fundament/tragenden Konstruktionen | [S6] | teilweise belegt |
| wiederverwendete Holzträger | unbekannt | Stück/t | — | Direct Reuse Tragwerk | [S1] | unklar |
| wiederverwendete Ziegel/Dachziegel | unbekannt | Stück/t | — | Direct Reuse Hülle/Oberfläche | [S1], [S2] | unklar |
| Transportdistanz | sehr gering / same-site, exakte Distanz unbekannt | — | Projektlogik | alte Schule → Neubau auf gleichem Gelände | [S1] | teilweise belegt |
| Kosten | unbekannt | — | — | — | — | unklar |
| U-Wert | unbekannt | — | — | — | — | unklar |
| Lebensdauer | unbekannt | — | — | — | — | unklar |

---

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Altmaterialien in zertifiziertem Kinderhaus | technisch/rechtlich | Nordic Swan hat strenge Material-/Chemikalienanforderungen | Auswahl und Prüfung nötig | Bauteil, Norm/Recht, Schadstoff | Materialkartierung und Zertifizierungsprozess | Reuse muss mit Gesundheits-/Innenraumzielen kompatibel sein | [S10] |
| Abbruch muss Bauteile erhalten | logistisch/technisch | normale Demolition zerstört Bauteile | zusätzlicher Planungsaufwand | Abbruchmethode, Bauteilinventar | nachhaltiger/schonender Rückbau | Rückbau ist Teil des Entwurfs | [S1], [S9] |
| Materialmengen und Geometrien vorgegeben | gestalterisch | Design folgt Verfügbarkeit | flexible Entwurfslogik nötig | Methode, Gestaltung, Bauteil | form follows availability | früh kartieren, flexibel entwerfen | [S1] |
| Abgrenzung Direct Reuse vs. Recycling | methodisch | Betonrecycling und Möbel werden mitgenannt | Bewertung könnte verfälscht werden | Kennwert, Bauteil, Material | getrennte Bilanz: Bauteilreuse vs Recycling | klare Definition im Datenmodell | [S6], [S9] |
| Öffentliche Beschaffung / neuer Rückbauprozess | wirtschaftlich/rechtlich | nachhaltige Demolition nicht Standard | neue Ausschreibungslogik | Wirtschaft, Recht, Prozessphase | Prozess wurde als branchestandard beschrieben | Kommunen können Standards setzen | [S9] |

---

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** same-site urban mining: Materialien stammen direkt aus dem Abbruch der alten Gladsaxe School.
- **Bauteilbörse / Quelle:** keine Bauteilbörse; Quelle ist der Vorgängerbau auf demselben Grundstück.
- **Kostenwirkung:** unbekannt.
- **Zeitwirkung:** integrierter Prozess aus Demontage, Lagerung und Neubau; konkrete Zeitwirkung unbekannt.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** erhöht durch Materialkartierung, schonenden Rückbau, Sortierung, Lagerung und Anpassung.
- **Lagerung:** on-site storage / Baustelle als temporäres Materialdepot belegt.
- **Marktbarrieren:** Zertifizierungsanforderungen, Qualitätssicherung von Altbauteilen, neue Vergabe-/Rückbauprozesse.

---

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** hoch — Ziegel, Dachziegel, Holzträger und Stahlfassadenelemente bleiben sichtbar.
- **räumliche Transformation:** Schule/Sporthalle wird in Kindergartenräume übertragen.
- **Atmosphäre / Ausdruck:** Materialspuren schaffen eine eigene Erzählung für Kinder, Eltern und lokale Gemeinschaft.
- **Umgang mit Spuren:** Materialien werden nicht verdeckt, sondern als Geschichte des Ortes ausgestellt.
- **sozialer Wert:** ehemalige Schüler/Eltern können Elemente wiedererkennen; der Bau unterstützt lokale Kontinuität.
- **Denkmal- oder Bestandswert:** kein formaler Denkmalstatus belegt; kultureller Wert als Erinnerung an die Schule.
- **Kritik / Grenzen:** viele veröffentlichte Kennwerte mischen Reuse, Recycling und Upcycling; Direct-Reuse-Mengen für einzelne Bauteile sind nicht ausreichend öffentlich dokumentiert.

---

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** konkrete Normnummern, detaillierte Tragwerksprüfung, Brandschutzprüfung, Bauteilbörse, Software, Versicherung, Gewährleistung, Kosten.
- **Welche neuen Entitäten wären sinnvoll?** Circular building site; same-site urban mining; Erinnerungsbauteil; Reuse-vs-Recycling-Bilanz.
- **Welche Daten fehlen?** Anzahl/Abmessungen der Holzträger; Mengen Ziegel/Dachziegel/Stahlfassadenelemente; Prüfungen; Brandschutz; Anschlussdetails; Kosten; Lager- und Rückbauaufwand.
- **Welche Quellen müssten geprüft werden?** Ausschreibungsunterlagen der Kommune; Lendager/NIRAS/Sweco Detailberichte; Nordic Swan Zertifizierungsunterlagen; LCA-Bilanz hinter den 178 t CO₂.

---

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja

### 5 wichtigste Fakten

1. Svanen wurde auf dem Gelände der ehemaligen Gladsaxe School gebaut.
2. Materialien aus dem Vorgängerbau wurden demontiert, sortiert, vor Ort gelagert und wiedereingebaut.
3. Große Holz-Dachbinder aus der früheren Sporthalle strukturieren die neuen Räume.
4. Ziegel, Dachziegel und Stahlfassadenelemente wurden direkt wiederverwendet.
5. Das Gebäude ist als Nordic-Swan-Ecolabel-Kindergarten dokumentiert und wurde 2022 ausgezeichnet.

### 5 wichtigste Bauteile

1. Holz-Dachbinder / timber roof trusses.
2. Holzrafters / træspær.
3. Wiederverwendete Ziegel.
4. Wiederverwendete Dachziegel.
5. Wiederverwendete Stahlfassadenelemente.

### 5 wichtigste Hürden

1. Tragwerks- und Sicherheitsnachweise für alte Holzbauteile.
2. Vereinbarkeit von Reuse mit Nordic-Swan-Chemikalien- und Qualitätsanforderungen.
3. Schonender Rückbau statt normaler Abriss.
4. Bauteillagerung auf der Baustelle.
5. Saubere Trennung von Direct Reuse, Recycling und nicht zählenden Objekten.

### 5 wichtigste übertragbare Erkenntnisse

1. Same-site urban mining reduziert Transport und bewahrt Ortsgeschichte.
2. Demolition tender und Materialmapping müssen vor dem Rückbau starten.
3. Wiederverwendung kann in kommunalen Kita-Projekten funktionieren.
4. Sichtbare Reuse-Bauteile stärken Identität und Akzeptanz.
5. Kennwerte müssen Direct Reuse und Recycling getrennt ausweisen.

### 5 offene Fragen

1. Wie viele Holzträger wurden exakt wiederverwendet?
2. Welche Prüfungen wurden für Holzträger, Ziegel und Dachziegel durchgeführt?
3. Welche Brandschutzlösung wurde für die Reuse-Holzbauteile gewählt?
4. Welche Kostenwirkung hatte der kreislauforientierte Rückbau?
5. Wie viel der angegebenen 6.278 t Materialeinsparung entfällt auf Direct Reuse statt Recycling?

---

## Quellen und Links

[S1] Lendager — The Swan: https://lendager.com/project/the-swan/  
[S2] State of Green — A Swan takes shape: https://stateofgreen.com/en/solutions/a-swan-takes-shape/  
[S3] Troldtekt — First circular daycare centre: https://www.troldtekt.com/references/children-and-youth/boernehuset-svanen/  
[S4] Gladsaxe Kommune — Børnehuset Svanen: https://gladsaxe.dk/svanen  
[S5] Sweco — The world’s first circular kindergarten: https://www.sweco.dk/en/showroom/boernehuset-svanen-the-worlds-first-circular-kindergarten/  
[S6] Synligbeton / Dansk Industri — Børnehuset Svanen: https://www.danskindustri.dk/synligbeton.dk/projekter/byggeri/bornehuset-svanen/  
[S7] Troldtekt — Danish Design Award 2022: https://www.troldtekt.dk/nyheder-og-presse/nyheder/2022/verdens-foerste-cirkulaere-boernehave-vinder-pris-ved-danish-design-award-2022/  
[S8] Hringvangur — Svanurinn: https://www.hringvangur.is/en/post/svanurinn-1  
[S9] BygTek — Svanemærket børnehus vinder designpris: https://bygtek.dk/artikel/byggeri/svanemrket-brnehus-i-gladsaxe-vinder-eftertragtet-designpris  
[S10] Dagens Byggeri — Børnehus af genbrugte materialer får Svanemærket: https://dagensbyggeri.dk/gronnere-byggeri/aldrig-set-for-bornehus-af-genbrugte-materialer-far-svanemaerket/
