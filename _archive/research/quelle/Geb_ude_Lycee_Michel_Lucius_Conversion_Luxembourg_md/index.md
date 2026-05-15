---
entity: "quelle"
id: "Geb_ude_Lycee_Michel_Lucius_Conversion_Luxembourg_md"
title: "Geb_ude_Lycee_Michel_Lucius_Conversion_Luxembourg_md"
build_status: "promoted_phase42"
source_filename: "Lycee_Michel_Lucius_Conversion_Luxembourg.md"
---

# Geb_ude_Lycee_Michel_Lucius_Conversion_Luxembourg_md

## 1. EINORDNUNG
- **Entscheidung:** VERGLEICHSFALL
- **Bewertung:** ★★★★☆
- **Begründung:** Das Projekt enthält belegte direkte Wiederverwendung von tragenden Stahlprofilen als neuer Überdachung sowie weitere feste Bau-/Hüll-/Innenausbaukomponenten. Es ist kein Fünf-Sterne-Fall, weil ein großer Teil des Projekts aus Umbau/Bestandserhalt und Recycling besteht und die wiederverwendete Tragstruktur nicht das Haupttragwerk des gesamten Gebäudes bildet.
- **Vertrauensgrad:** belegt
- **Warnung Bestandserhalt:** ja
- **Warnung Möbel/Dekoration:** ja
- **Projektstatus:** gebaut

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Conversion of two wings of Lycée Michel Lucius | untersuchtes Projekt | [S1], [S2], [S3] | belegt | Kreislauf-Pilotprojekt in Luxemburg |
| Gebäude | Lycée Michel Lucius Campus, Flügel 3000 und 6000 | Schulcampus / Umbau | [S1], [S2] | belegt | Flügel 3000 von 1973, Flügel 6000 von 1997 |
| Ort | Luxembourg-Limpertsberg, Luxemburg | Standort | [S1], [S3] | belegt | Campus mit mehreren Gebäuden |
| Projekt | selektiver Rückbau Block 3000, Umbau Block 6000, Neugestaltung Außenanlagen | zirkulärer Umbau | [S1], [S2] | belegt | 2018–2021 / Bau 2020–2021 nach Daedalus |
| People | Administration des bâtiments publics | Bauherr / öffentlicher Auftraggeber | [S2], [S4] | belegt | Staat Luxemburg |
| People | Schmets architectes | Architekt | [S1], [S2] | belegt | Projektplaner Architektur |
| People | Daedalus Engineering | Ingenieur / Projektbeteiligter | [S2] | belegt | Quelle mit Projektkosten und Zeitraum |
| Bauteil | 11,8 t Stahlprofile | aus Block 3000, neu als Überdachung | [S1] | belegt | stärkster Direct-Reuse-Bauteilnachweis |
| Bauteil | 61 m² Blech | aus Böden Block 3000, neu als Fassadenbekleidung Block 6000 | [S1] | belegt | von Schülern künstlerisch bemalt |
| Bauteil | Stahlfassadenpaneele | neu als Geländer an Esplanade | [S1] | belegt | feste Außen-/Sicherheitsbauteile |
| Bauteil | 419 m² Gips-Akustikpaneele + 12 Metallpaneele/4,3 m² | wiederverwendete Decken-/Akustikelemente | [S1] | belegt | aus abgehängten Decken Block 3000 in Block 6000 |
| Bauteil | 135 m² Straßenpflasterplatten | wiederverwendet in Außenanlagen/Fahrradbereich | [S1] | belegt | feste Boden-/Außenbauteile |
| Bauteil | 38 Fertigbetonelemente als Rinnen | wiederverwendete Elemente in Außenanlagen | [S1] | belegt | feste Entwässerungs-/Außenraumelemente |
| Material | rezyklierter Beton-Zuschlag | Recycling, nicht Direct Reuse | [S1], [S2] | belegt | 60 % RC-Zuschlag in neuen Betonelementen; nicht als Bauteilwiederverwendung zählen |
| Reuse-Strategie | on-site selective deconstruction and reuse | Rückbau und Wiedereinbau auf Campus | [S1], [S2] | belegt | starker lokaler Kreislauf |
| Prozessphase | Materialinventar / selektiver Rückbau | Voraussetzung der Wiederverwendung | [S1], [S2], [S5] | belegt | neue luxemburgische Abfallgesetzgebung als Kontext |
| Leistungsanforderung | Bibliothek/Leseraum, Rauch-/Wärmespeicher, Akustik/Thermik | Umbau Block 6000 | [S1], [S5] | teilweise belegt | konkrete Normen unbekannt |
| Kennwert | 2.700 m² | Projektgröße/Volume laut Daedalus | [S2] | belegt | „Dimension / Volume“ |
| Kennwert | 6.500.000 EUR ohne MwSt | Gesamtauftragskosten | [S2] | belegt | nicht Reuse-Mehrkosten |
| Kennwert | 79 % weniger Abbruchabfall | Gebäudestrategie, nicht nur Reuse | [S6] | teilweise belegt | Quelle ist Sekundär-/Storyquelle |
| Kennwert | 458–792 t CO₂e Einsparung | Gebäudestrategie, nicht nur Reuse | [S6] | teilweise belegt | nicht Direct-Reuse-only |
| Förderprogramm | New European Bauhaus Prize 2024 | Auszeichnung | [S2], [S3] | belegt | kein klassisches Förderprogramm |
| Warnung Möbel | Bibliotheksmöbel aus gleichem Gebäude | nicht zählen, wenn lose Möbel | [S1] | belegt | nur feste Einbauten wären relevant; Quelle spricht furniture |
| Hürde | Normen/Altgebäude/Materialprüfung | Umbau bestehender Schulgebäude | [S1], [S5] | teilweise belegt | Details unbekannt |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Campus-interner Kreislauf | Reuse findet zwischen Gebäudeteilen desselben Campus statt | Stahl aus Flügel 3000 für Überdachung / Paneele in Flügel 6000 | verbindet Logistik, Ort, Bauteil, Reuse-Strategie |
| Reuse-vs-Recycling-Abgrenzung | Projekt kombiniert direkte Wiederverwendung und RC-Beton | Stahlprofile = Reuse; 60 % RC-Zuschlag = Recycling | verbindet Kennwert, Material, Methode |
| Bildungs-/Partizipationsbezug | Schüler gestalten Fassadenbleche künstlerisch | bemalte Blechfassade am Block 6000 | verbindet sozialer Wert, Gestaltung, People |

## 3. FALLSTUDIE
- **Name:** Lycée Michel Lucius Conversion / Revitalizing Lycée Michel Lucius
- **Ort:** Limpertsberg, Luxembourg, Luxemburg
- **Gebäude:** Schulcampus, besonders Block/Flügel 3000 und 6000
- **Projekt:** selektiver Rückbau des Flügels 3000, Umnutzung/Modernisierung des Flügels 6000 zur Bibliothek/Leseraum, neue Esplanade und Außenanlagen
- **Beteiligte People / Akteure:** Administration des bâtiments publics; Schmets architectes; Daedalus Engineering; Universität Luxemburg / Ponts et Chaussées / Beton- und Zementakteure für Recycling-Pilot nach Daedalus
- **Architekt:** Schmets architectes
- **Tragwerksplaner:** unbekannt; Daedalus Engineering als Ingenieurbeteiligter belegt
- **Bauherr:** Administration des bâtiments publics
- **Zeitraum:** Projekt 2018–2021; Planung 01.2018–12.2019; Bau 01.2020–09.2021
- **Ursprüngliche Nutzung:** Block 3000 = Schulflügel von 1973 mit Metallrahmen/Fillod-System; Block 6000 = Holzbau-/modulares Schulgebäude von 1997
- **Neue Nutzung:** Block 6000 als Bibliothek/Leseraum/Jugendzentrum; Block 3000-Untergeschoss als Werkstatt/Lager; Dach als Esplanade; Stahlprofile als Überdachung
- **Fläche / Maßstab:** 2.700 m² laut Daedalus; Campusmaßstab
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** gut für Reuse-Bauteile, Mengen, Zeitraum, Auftraggeber und Pilotcharakter; schwach für Prüfberichte, Normen, Haftung, Detailkosten der Wiederverwendung

## 4. REUSE-STRATEGIE
- **Art der Wiederverwendung:** partiell; in-situ und campus-intern; Bauteilwiederverwendung; adaptive reuse; Recyclinganteile separat.
- **Hauptniveau:** Tragwerk / Gebäudehülle / räumlicher Innenausbau / Außenraum; untergeordnet Material/Recycling.
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Bestandserhalt von Block 6000 ist wichtig, zählt aber nur als Kontext, nicht als Direct Reuse. Direct Reuse sind vor allem Stahlprofile, Blech, Geländer-/Fassadenpaneele, Akustikpaneele, Pflasterplatten und Fertigbetonteile, die in neuer Funktion eingebaut wurden. RC-Zuschlag zählt als Recycling, nicht Direct Reuse.
- **Warum relevant:** Der Fall zeigt, wie selektiver Rückbau, Materialinventar und campusinterne Logistik in einem öffentlichen Schulprojekt zu mehreren belegten Reuse-Strömen führen können.

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Stahlprofile | Stahl | Block 3000, Metallrahmen | Tragstruktur Schulflügel | Überdachung neben Esplanade | 11,8 t | ja | ja | ja/Überdachung | nein | selektiver Rückbau, Zuschnitt/Anpassung unbekannt | unbekannt | unbekannt | Tragfähigkeit, Witterung, Sicherheit | unbekannt | Nachweis Altstahl | [S1] | Prüfungen, Verbindungen |
| Blech aus Böden | Stahlblech / sheet metal | Böden Block 3000 | Boden-/Deckenelement | Fassadenbekleidung Block 6000 | 61 m² | nein | ja | ja | nein | Bergung; künstlerische Bemalung durch Schüler | unbekannt | unbekannt | Witterung, Befestigung | unbekannt | Oberflächen/Brandschutz | [S1] | Detailanschlüsse |
| Stahlfassadenpaneele | Stahl, teilweise grün lackiert | Fassade Block 3000 | Fassadenpaneel | Geländer an neuer Esplanade | Menge unbekannt | nein | ja | ja/Außenraum | nein | Demontage, Wiedereinbau | unbekannt | unbekannt | Absturzsicherung, Witterung | unbekannt | Zulassung als Geländer | [S1] | Menge, Prüfung |
| Akustikpaneele | Gips-Akustikpaneele | abgehängte Decken Block 3000 | Decken-/Akustikelement | Akustikelemente in Block 6000 | 419 m² | nein | ja | nein | nein | Demontage, Wiedereinbau | unbekannt | unbekannt | Akustik, Brandschutz | unbekannt | Zustand/Brandschutz | [S1] | genaue Position |
| Metall-Deckenpaneele | Metall | abgehängte Decken Block 3000 | Deckenpaneele | Wiedereinbau Block 6000 | 12 Stück / 4,3 m² | nein | ja | nein | nein | Demontage/Wiedereinbau | unbekannt | unbekannt | Akustik/Decke | unbekannt | unbekannt | [S1] | Details |
| Straßenpflasterplatten | Beton/Stein, unbekannt | unbekannt / geliefert von Landschaftsbaufirma | Straßenbelag | Außenanlagen und Fahrradbereich | 135 m² | nein | ja | nein | nein | Demontage, Verpackung, Lieferung, Wiedereinbau | lose/fest verlegt, Details unbekannt | unbekannt | Bodenbelastung, Rutschfestigkeit | unbekannt | Logistik | [S1] | Material |
| Fertigbetonelemente als Rinnen | Betonfertigteile | Bauarbeiten / Bestand | unbekannt | Kanäle/Rinnen | 38 Stück | nein/teilweise | ja | Außenraum | technisch/Entwässerung | Bergung/Wiedereinbau | unbekannt | unbekannt | Entwässerung, Dauerhaftigkeit | unbekannt | unbekannt | [S1] | Herkunft |
| Palettenholz-Bänke | Holz | Palettenholz | Verpackung/Transport | Außenbank | unbekannt | nein | ja | nein | nein | Oberflächenbehandlungen getestet: Flamme + Schutzschicht/Farbe | unbekannt | unbekannt | Dauerhaftigkeit außen | unbekannt | Witterung | [S1] | ob fest eingebaut |
| Bibliotheksmöbel | Möbel | gleiches Gebäude | Möbel | Bibliotheksmöbel | unbekannt | nein | nein/lose | nein | nein | Wiederverwendung | lose | unbekannt | Nutzung | unbekannt | nicht nach Grundregel zählen | [S1] | ob fest eingebaut |
| RC-Zuschläge | Betonbruch | Rückbau Block 3000 | Betonabbruch | Zuschlag in neuen Betonelementen | 60 % Anteil in Betonrezeptur | nein | nein | nein | nein | Brechen/Recycling | nicht zutreffend | Laborversuche | Betonqualität | unbekannt | Recycling, nicht Direct Reuse | [S1], [S2] | absolute Mengen |
| Bestand Block 6000 | Holzbau / Bestand | Block 6000 | Schulflügel | Bibliothek/Leseraum | Großteil erhalten | ja | ja | ja | teilweise | Umbau | Bestand | Machbarkeitsstudie | Wirtschaft/Umwelt | unbekannt | zählt als Bestandserhalt, nicht Direct Reuse | [S1] | genaue Mengen |

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Untersuchung Flügel 3000/6000 und Materialressourcen | ABP, Schmets, Daedalus | Machbarkeitsstudie / Materialressourcen nutzen | unbekannt | nicht relevant | nicht relevant | Feasibility Study für Block 6000 | Campus | unterschiedliche Bauweisen/Standards | differenzierte Strategie pro Flügel | [S1] |
| Bauteilinventar | Identifikation rückbaubarer Elemente | Projektteam | Materialinventar / reclaiming | unbekannt | nicht relevant | nicht relevant | unbekannt | campusintern | Bauteile müssen brauchbar sein | selektive Demontage | [S1], [S5] |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Altgebäude von 1973/1997 | unbekannt | keine Quelle |
| Rückbau | Block 3000 weitgehend demontiert; Untergeschoss erhalten | Projektteam / Bauunternehmen unbekannt | selektiver Rückbau | unbekannt | selektive Dekonstruktion | unbekannt | unbekannt | vor Ort | Materialtrennung | Bauteile separieren | [S1], [S2] |
| Ausbau | Stahlprofile, Bleche, Paneele, Deckenplatten bergen | Bauakteure | selektiver Ausbau | unbekannt | selektiv | unbekannt | unbekannt | zwischen Block 3000 und 6000/Esplanade | Beschädigung, Sortierung | campusinterne Verwendung | [S1] |
| Transport | kurze Wege auf Campus / externe Lieferung Pflasterplatten | Landschaftsbaufirma, Projektteam | Verpackung, Lieferung, Wiedereinbau | unbekannt | nicht relevant | unbekannt | unbekannt | campusintern + Lieferung | Koordination | Firma übernimmt Demontage, Verpackung, Lieferung, Wiedereinbau für Pflaster | [S1] |
| Lagerung | unbekannt | unbekannt | unbekannt | unbekannt | nicht relevant | unbekannt | unbekannt | unbekannt | Zwischenlagerung erforderlich | unbekannt | keine Quelle |
| Aufbereitung | Stahlprofile/Paneele/Bleche anpassen; Palettenholz behandeln | Projektteam, Handwerker, Schüler | Zuschnitt/Bemalung/Oberflächenbehandlung | unbekannt | nicht relevant | Flammenbehandlung + Schutz/Farbe bei Holz getestet | Laborversuche für RC-Beton | vor Ort/extern unbekannt | Witterung/Qualität | Tests und angepasste Verwendung | [S1] |
| Planung | Block 6000 zu Bibliothek, Block 3000 zu Esplanade/Überdachung | Schmets, ABP, Daedalus | adaptive reuse + direct reuse | unbekannt | nicht relevant | nicht relevant | Machbarkeit | Campus | Normen/Standards | Programm an Bestand angepasst | [S1], [S2] |
| Genehmigung | unbekannt | ABP / Behörden | öffentliches Bauprojekt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | reuse-rechtliche Anforderungen | unbekannt | keine Quelle |
| Wiedereinbau | Stahlprofile als Überdachung, Bleche als Fassade, Paneele als Geländer/Decken | Bauakteure | Reuse-Einbau | unbekannt | nicht relevant | Anpassung/Befestigung | unbekannt | Campus | neue Funktionen | passgenaue Wiederverwendung | [S1] |
| Monitoring | Projekt als Pilot und NEB-Preis dokumentiert | ABP, Ministerium, EU/NEB | Projektkommunikation | unbekannt | nicht relevant | nicht relevant | unbekannt | öffentlich | Übertragbarkeit | Pilotprojekt kommuniziert | [S2], [S3], [S4] |

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Stahlprofile aus Block 3000 als neue Überdachung; Block 6000 weitgehend erhalten | Tragfähigkeit Überdachung; Bestandserhalt | unbekannt | unbekannt | Altstahlprofile neu nachweisen | Wiederverwendung in überschaubarem Bauteil | [S1] |
| Lastabtragung | Überdachung trägt Außenraum-/Dachlasten; Details unbekannt | Wind, Eigenlast, Schnee unbekannt | unbekannt | unbekannt | Stahlprofile aus Bestand | unbekannt | [S1] |
| Verbindung | unbekannt | Kraftschluss Stahlüberdachung und Geländer | unbekannt | unbekannt | neue Anschlüsse an Altprofile | unbekannt | keine Quelle |
| Brandschutz | Doppelhöhen in Block 6000 wirken als Rauchpuffer im Brandfall | Rauchableitung / Nutzungssicherheit | unbekannt | unbekannt | Umbau Bibliothek in Bestandsbau | Doppelhöhen / Pufferzonen | [S1] |
| Schallschutz | technische Maßnahmen zu Akustik erwähnt; Akustikpaneele wiederverwendet | Bibliotheksakustik | unbekannt | unbekannt | Klassenräume zu Bibliothek | reuse von Akustikpaneelen | [S1], [S5] |
| Feuchte | unbekannt | Außenbauteile, Überdachung, Fassadenblech | unbekannt | unbekannt | Altblech außen | unbekannt | keine Quelle |
| Wärmeschutz | Block 6000 konvertiert; technische Maßnahmen gegen Überhitzung erwähnt | thermischer Komfort | unbekannt | unbekannt | Holz-/Modulbau, neue Nutzung | Doppelhöhen speichern warme Luft / Überhitzungsrisiko reduzieren | [S1] |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | Bestandsumbau | unbekannt | keine Quelle |
| Luftdichtheit | unbekannt | unbekannt | unbekannt | unbekannt | Bestand | unbekannt | keine Quelle |
| TGA-Integration | unbekannt | Bibliotheksbetrieb | unbekannt | unbekannt | Bestandstechnik | unbekannt | keine Quelle |
| Barrierefreiheit | Rampen/Accessibility in Außenanlagen sichtbar/beschrieben | Erschließung Campus | unbekannt | unbekannt | Hang/Bestand | neue Rampen/Außenanlagen | [S1] |
| Dauerhaftigkeit | Stahl/Bleche/Pflaster im Außenraum | Witterung/Dauerhaftigkeit | unbekannt | unbekannt | Altmaterial außen | unbekannt | [S1] |
| Wartung | unbekannt | Schulbetrieb | unbekannt | unbekannt | reuse Komponenten | unbekannt | keine Quelle |
| Zulassung | unbekannt | Schulgebäude öffentlich | unbekannt | unbekannt | Reuse-Komponenten im öffentlichen Bau | Pilotprojekt / staatlicher Auftraggeber | [S2], [S4] |
| Haftung | unbekannt | öffentliche Auftraggeberverantwortung | unbekannt | unbekannt | Gewährleistung reuse | unbekannt | keine Quelle |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| wiederverwendete Stahlprofile | 11,8 | t | Materialinventar / Opalis-Projektdaten | Stahlprofile aus Block 3000 für Überdachung | [S1] | belegt |
| wiederverwendetes Blech | 61 | m² | Materialinventar | Bodenblech Block 3000 zu Fassadenbekleidung Block 6000 | [S1] | belegt |
| wiederverwendete Akustikpaneele | 419 | m² | Materialinventar | abgehängte Decken Block 3000 zu Block 6000 | [S1] | belegt |
| wiederverwendete Metallpaneele | 12 / 4,3 | Stück / m² | Materialinventar | abgehängte Decken | [S1] | belegt |
| wiederverwendete Pflasterplatten | 135 | m² | Liefer-/Wiedereinbauprozess | Außenanlagen/Fahrradbereich | [S1] | belegt |
| wiederverwendete Fertigbetonelemente | 38 | Stück | Materialinventar | Rinnen/Kanäle | [S1] | belegt |
| Fläche / Projektgröße | 2.700 | m² | Daedalus-Projektdaten | Umbau/Rückbau/Außenanlagen | [S2] | belegt |
| Kosten | 6.500.000 | EUR ohne MwSt | Daedalus-Projektdaten | Gesamtauftragskosten, nicht Reuse-only | [S2] | belegt |
| Bauzeit | 01.2020–09.2021 | Zeitraum | Daedalus-Projektdaten | Bauphase | [S2] | belegt |
| Planungszeit | 01.2018–12.2019 | Zeitraum | Daedalus-Projektdaten | Planung | [S2] | belegt |
| CO₂-Einsparung | 458–792 | t CO₂e | Sekundärquelle; nicht Direct-Reuse-only | Umbau-/Strategievergleich | [S6] | teilweise belegt |
| Abfallvermeidung | 79 | % | Sekundärquelle; nicht Direct-Reuse-only | Abrissabfall/Strategievergleich | [S6] | teilweise belegt |
| RC-Zuschlag | 60 | % | Laborversuche/Betonrezeptur | Recyclingbeton; nicht Direct Reuse | [S1] | belegt |
| U-Wert | unbekannt | W/m²K | unbekannt | Hülle | keine Quelle | unbekannt |
| Lebensdauer | unbekannt | Jahre | unbekannt | Reuse-Bauteile | keine Quelle | unbekannt |
| Zirkularitätskennwert | unbekannt | - | unbekannt | Projekt | keine Quelle | unbekannt |

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Unterschiedliche Gebäudelogiken 1973/1997 | technisch/planerisch | Block 3000 Metallrahmen, Block 6000 Holzbau | unterschiedliche Umbaustrategien nötig | Gebäude, Tragwerkssystem | 3000 weitgehend zurückbauen, 6000 erhalten und umnutzen | Reuse-Strategie muss pro Bauabschnitt differenziert sein | [S1] |
| Norm-/Standarddefizite der Bestandsbauten | technisch/rechtlich | Gebäude erfüllten aktuelle Standards nicht | Umbau statt einfache Weiternutzung | Leistungsanforderung, Recht | Programm und Bauteile angepasst | Bestandserhalt braucht Leistungs-Upgrade | [S1] |
| Reuse vs. Recycling methodisch trennen | methodisch | Projekt kombiniert Wiederverwendung und RC-Beton | Gefahr, Kennwerte falsch zuzuordnen | Kennwert, Material | Direct Reuse separat erfassen | klare Bilanzgrenzen sind nötig | [S1], Bewertung |
| Öffentlicher Bau und Haftung | rechtlich/wirtschaftlich | Schule, öffentlicher Auftraggeber, gebrauchte Bauteile | Nachweise vermutlich anspruchsvoll | Recht, Prüfung, Wirtschaft | Pilotprojekt durch ABP | öffentliche Pilotprojekte können Markthürden reduzieren | [S2], [S4] |
| Logistik vieler kleiner Materialströme | logistisch | Stahl, Bleche, Paneele, Pflaster, Holz, Fertigteile | Koordination von Ausbau, Lagerung, Wiedereinbau | Logistik, Prozessphase | Materialinventar und campusnahe Verwendung | kurze Wege und klare Zielorte erleichtern Reuse | [S1] |
| Möbel/lose Elemente | methodisch | Möbel aus gleichem Gebäude wiederverwendet | nach Grundregel nicht als Bauteilreuse zählen | Bauteil, Warnung Möbel | nur feste Bauteile bewerten | Reuse-Inventar muss lose Möbel markieren | [S1], Grundregel |

## 10. WIRTSCHAFT UND BESCHAFFUNG
- **Beschaffungsmodell:** überwiegend campusinterner Urban-Mining-/Selbstbeschaffungsansatz; externe Landschaftsbaufirma lieferte/demontierte/verpackte/reinstallierte Pflasterplatten.
- **Bauteilbörse / Quelle:** keine Bauteilbörse; Quelle = eigene Bestandsgebäude Block 3000/6000 und externe Pflasterplattenquelle.
- **Kostenwirkung:** Gesamtauftragskosten 6.500.000 EUR ohne MwSt belegt; Reuse-spezifische Mehr-/Minderkosten unbekannt. Eine Quelle beschreibt die Umbaulösung als schneller und wirtschaftlich günstiger, aber ohne belastbare Kostenaufteilung.
- **Zeitwirkung:** Bau 01.2020–09.2021; Reuse-spezifischer Zeiteffekt unbekannt.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** Materialinventar, selektiver Rückbau, Aufbereitung und Wiedereinbau mehrerer Ströme; Aufwand nicht quantifiziert.
- **Lagerung:** unbekannt.
- **Marktbarrieren:** Prüf-/Haftungsfragen, fragmentierte Materialströme, öffentliche Vergabe, Normnachweise.

## 11. GESTALTUNG UND KULTURELLER WERT
- **Sichtbarkeit der Wiederverwendung:** hoch bei Stahlüberdachung, Geländern, Fassadenblechen und Außenanlagen; teils sichtbar-pädagogisch durch künstlerisch bemalte Blechfassade.
- **räumliche Transformation:** alter Schulflügel wird zur Esplanade/Untergeschossnutzung; anderer Flügel zur Bibliothek und Lesezone; Bauteile wandern zwischen Gebäudeteilen.
- **Atmosphäre / Ausdruck:** pragmatischer öffentlicher Circular-Economy-Pilot mit sichtbaren Materialspuren.
- **Umgang mit Spuren:** grün lackierte Fassadenpaneele und Blechmaterial bleiben als Herkunfts-/Schulkontext lesbar; Schülerbemalung erzeugt neue kulturelle Schicht.
- **sozialer Wert:** Bildungswert durch Schulcampus, Schülerbeteiligung und New-European-Bauhaus-Anerkennung.
- **Denkmal- oder Bestandswert:** kein Denkmalstatus belegt; Bestandswert liegt in Ressourcenerhalt.
- **Kritik / Grenzen:** starke Bestandserhalt- und Recyclinganteile dürfen nicht als Direct Reuse überbewertet werden; Möbel zählen nicht; technische Nachweise nicht öffentlich.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN
- **Welche bestehenden Entitäten wurden nicht gefunden?** konkrete Normen, Rechts-/Vergabeweg, Prüfberichte, Schadstoffe, Lagerung, detaillierte Verbindungen, Gewährleistung, Versicherung.
- **Welche neuen Entitäten wären sinnvoll?** Campus-interner Kreislauf; Reuse-vs-Recycling-Abgrenzung; Bildungs-/Partizipationsbezug.
- **Welche Daten fehlen?** Prüfungen Stahlprofile/Bleche/Paneele; Details der Überdachungsverbindungen; Lagerzeiten; Reuse-spezifische Kosten; CO₂-Aufteilung Direct Reuse vs. Recycling vs. Bestandserhalt.
- **Welche Quellen müssten geprüft werden?** ABP-Projektdossier; Schmets-Planunterlagen; Daedalus-Statik; Ausschreibung; Prüfberichte; Materialinventar; NEB-Bewerbungsunterlagen.

## 13. ABSCHLUSS
- **Soll der Fall in die Hauptliste?** ja, als Vergleichsfall.
- **5 wichtigste Fakten:**
  1. 11,8 t Stahlprofile aus Block 3000 wurden als neue Überdachung wiederverwendet.
  2. 61 m² Blech wurden als Fassadenbekleidung am Block 6000 wiederverwendet.
  3. 419 m² Akustikpaneele und 12 Metallpaneele wurden aus abgehängten Decken wiederverwendet.
  4. 135 m² Pflasterplatten und 38 Fertigbetonelemente wurden in den Außenanlagen wiederverwendet.
  5. Das Projekt ist ein öffentlich dokumentierter Circular-Economy-Pilot und NEB-Preisträger 2024.
- **5 wichtigste Bauteile:** Stahlprofile; Blechfassade; Stahlfassadenpaneele/Geländer; Akustikpaneele; Pflasterplatten/Fertigbetonrinnen.
- **5 wichtigste Hürden:** Leistungsnachweis Altstahl; Abgrenzung Bestand/Recycling/Reuse; Logistik vieler Materialströme; öffentliche Haftung/Gewährleistung; technische Standards bei Schulumbau.
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Campusinterne Kreisläufe reduzieren Transport- und Beschaffungsrisiken.
  2. Reuse gelingt besser, wenn Zielorte für Bauteile früh festgelegt sind.
  3. Direct Reuse und Recycling müssen getrennt bilanziert werden.
  4. Öffentliche Pilotprojekte können Lernmodelle für selektiven Rückbau liefern.
  5. Sichtbare Reuse-Bauteile können pädagogischen und kulturellen Wert erzeugen.
- **5 offene Fragen:**
  1. Welche Prüfungen der 11,8 t Stahlprofile wurden durchgeführt?
  2. Welche Norm-/Zulassungswege wurden genutzt?
  3. Wie hoch waren Reuse-spezifische Kosten und Zeitaufwände?
  4. Wie teilen sich die CO₂-Einsparungen auf Bestandserhalt, Direct Reuse und Recycling auf?
  5. Wie wurden Lagerung und Gewährleistung geregelt?

## Quellen / Links
- [S1] Opalis — Conversion of two wings of the Lycée Michel Lucius: https://opalis.eu/en/projects/conversion-two-wings-lycee-michel-lucius
- [S2] Daedalus Engineering — Neugestaltung des Geländes des Lycée Michel Lucius: https://www.daedalus.lu/projekte/neugestaltung-des-gelandes-des-lycee-michel-lucius/
- [S3] New European Bauhaus Prizes — A Sustainable Campus Transformation: https://prizes.new-european-bauhaus.europa.eu/application/sustainable-campus-transformation
- [S4] Administration des bâtiments publics — Présentation du projet pilote: https://abp.gouvernement.lu/en/actualites.gouvernement2024%2Bfr%2Bactualites%2Btoutes_actualites%2Bcommuniques%2B2023%2B09-septembre%2B12-bausch-lucius.html
- [S5] LUGA — Economie circulaire dans la construction: https://luga.lu/en/experience/economie-circulaire-dans-la-construction/
- [S6] Naturanal — Reusing materials to solve the crisis in the building sector: https://www.naturanal.com/story/reusing-materials-crisis-in-the-construction-sector/
