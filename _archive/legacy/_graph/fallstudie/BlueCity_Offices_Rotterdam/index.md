---
id: "BlueCity_Offices_Rotterdam"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "BlueCity Offices Rotterdam – Fallstudie Direct Reuse / zirkuläres Bauen"
bauobjekt:
  - "BlueCity_Offices_Rotterdam"
legacy_paths:
  - "Gebäude\\BlueCity_Offices_Rotterdam.md"
projekt:
  - "BlueCity_Offices_Rotterdam"
reuse_chain_detected: "True"
---
# BlueCity Offices Rotterdam – Fallstudie Direct Reuse / zirkuläres Bauen

## Migration

- Fallstudie ID: BlueCity_Offices_Rotterdam
- Legacy source count: 1
- Generated project: BlueCity_Offices_Rotterdam
- Generated bauobjekt: BlueCity_Offices_Rotterdam
- Extracted reuse_einsatz rows: 7
- Extracted datenpunkt rows: 9
- Extracted entity mapping rows: 17
- Reuse chain detected: True

## Legacy Content

### Legacy Source: Gebäude\BlueCity_Offices_Rotterdam.md

- Map action: split_into_case_graph
- Primary target: fallstudie/BlueCity_Offices_Rotterdam
- Secondary targets: projekt/BlueCity_Offices_Rotterdam; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# BlueCity Offices Rotterdam – Fallstudie Direct Reuse / zirkuläres Bauen

**Projekt:** BlueCity Offices / Blue City 010 Offices, Rotterdam  
**Bearbeitung:** Deutsch, kompakt, quellenbasiert  
**Grundregel:** Gezählt werden nur wiederverwendete Bau-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Bestandserhalt und lose Möbel werden nicht als Direct Reuse gewertet.

---

## 1. EINORDNUNG

- **Entscheidung:** VERGLEICHSFALL
- **Bewertung:** ★★★☆☆
- **Begründung:** BlueCity Offices ist ein gebauter Innenausbau-/Transformationsfall mit stark belegter Wiederverwendung von festen räumlichen Bauteilen, vor allem geernteten Fensterrahmen als Trennwände bzw. innere Fassade. Die Wiederverwendung ist räumlich und hüllenartig wirksam, aber nicht tragwerkszentral.
- **Vertrauensgrad:** belegt
- **Warnung Bestandserhalt:** ja
- **Warnung Möbel/Dekoration:** ja
- **Projektstatus:** gebaut

---

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | BlueCity Offices / Blue City 010 Offices | Reuse-Fall für Büroflügel im ehemaligen Tropicana | S1–S4 | belegt | Teil der Gesamttransformation BlueCity |
| Gebäude | ehemaliges subtropisches Schwimmbad Tropicana / Club Tropicana | Bestandsgebäude und Einbauort | S1, S3 | belegt | Bestandserhalt nicht als Direct Reuse gewertet |
| Ort | Rotterdam, Maasboulevard | Standort | S1, S3 | belegt | genaue Adresse über BlueCity bekannt, hier nicht vertieft |
| Projekt | Büroflügel im ehemaligen Discobereich | neue Arbeitsplätze für Circular-Economy-Unternehmen | S1, S2 | belegt | 1.300 m² / 100 Arbeitsplätze |
| People | BlueCity, Superuse Studios, COUP, Workspot, Floris Schiferli | Auftraggeber, Architektur/Design/Partner | S1, S2, S5 | belegt | Bauunternehmen Bik Bouw laut Rotterdam Architekturprijs |
| Bauteil | Red-cedar-Fensterrahmen / geerntete Fensterrahmen | wichtigste Reuse-Bauteile, als Trennwände/Innenfassade | S1–S4 | belegt | feste räumliche Bauteile |
| Bauteil | wiederverwendeter Stahl | zweiter Materialinput nach Fensterrahmen | S1 | teilweise belegt | Bauteilrolle/Menge unbekannt |
| Bauteil | Betonblöcke | laut Circle Economy als Trennwände wiederverwendet | S6 | teilweise belegt | Sekundärquelle, Details unbekannt |
| Material | europäisches Konstruktionsholz | neu, erneuerbar, nicht Reuse | S1 | belegt | nicht als Direct Reuse zählen |
| Verbindung | geneigte Fensterrahmen / Trennwandsystem | räumliche und akustisch/klimatische Wirkung | S3 | belegt | Anschlussdetails unbekannt |
| Methode | harvesting / Oogstkaart-Logik | Materialsuche aus Abbruch-/Restströmen | S1, S7 | belegt | konkrete Harvest Map nicht vollständig öffentlich |
| Kennwert | 1.300 m² | Fläche erster Büroflügel | S1, S2 | belegt | 10.500 m² Gesamtgebäude bei Superuse-alt |
| Kennwert | 100 Arbeitsplätze | Nutzung | S1, S2 | belegt | nicht Reuse-Kennwert |
| Kennwert | 90 % circular / 90 % reused | Material-/Circularity-Anteil | S1, S3 | teilweise belegt | Quellen differieren in Begrifflichkeit |
| Kennwert | 68 % CO₂-Reduktion | Vergleich mit konventionellem Büroausbau | S1, S2 | belegt | Methode nicht öffentlich vollständig |
| Kennwert | 60 t CO₂ Einsparung | laut Rotterdam Architekturprijs / BlueCity | S5, S8 | belegt | Bilanzgrenze unbekannt |
| Hürde | Passung geernteter Fensterrahmen | Entwurf aus vorgegebenen Abmessungen | S1, S3 | belegt | materialgetriebenes Design |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Harvest Map / Oogstkaart | bildet Herkunft und Verfügbarkeit von Reuse-Material ab | Superuse-Harvesting | Tool, Methode, Bauteilbörse |
| Materialgetriebener Entwurf | Bauteilmaße bestimmen räumliches Konzept | Fensterrahmen als geneigte Trennwände | Methode, Bauteil, Gestaltung |
| Circular Workplace | Nutzungstyp kombiniert Reuse-Innenausbau und zirkuläre Unternehmen | 100 circular workplaces | Projekt, Wirtschaft, sozialer Wert |

---

## 3. FALLSTUDIE

- **Name:** BlueCity Offices / Blue City 010 Offices
- **Ort:** Rotterdam, Niederlande
- **Gebäude:** ehemaliges Tropicana / Club Tropicana
- **Projekt:** Büroflügel in ehemaliger Discothek als erster Transformationsabschnitt von BlueCity
- **Beteiligte People / Akteure:** BlueCity, Superuse Studios, COUP, Workspot, Bik Bouw laut Rotterdam Architekturpreis; weitere Akteure unbekannt
- **Architekt:** Superuse Studios / Floris Schiferli
- **Tragwerksplaner:** unbekannt
- **Bauherr:** BlueCity / Blue City 010 BV
- **Zeitraum:** eröffnet 31.03.2017; Fertigstellung März 2017
- **Ursprüngliche Nutzung:** subtropisches Schwimmbad / Discothek Club Tropicana
- **Neue Nutzung:** Büro- und Arbeitsplätze für zirkuläre Unternehmen, Coworking, private und flexible Offices
- **Fläche / Maßstab:** 1.300 m², 100 Arbeitsplätze; Gesamtgebäude ca. 10.500 m² laut älterer Superuse-Projektseite
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** gut für Konzept, Fläche, Hauptbauteil und CO₂-Angaben; schwächer für Mengen, technische Prüfungen und Kosten

---

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; feste räumliche Innenbauteile; adaptive reuse
- **Hauptniveau:** räumlicher Innenausbau / innere Hülle; teilweise Material
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Der Erhalt des Tropicana-Bestands zählt nicht als Direct Reuse. Bewertet werden die geernteten Fensterrahmen als neue Trennwände/Innenfassade und weitere feste wiederverwendete Bauteile.
- **Warum ist der Fall relevant?** Sehr anschauliches Beispiel für Material-Driven Design: Abmessungen vorhandener Fensterrahmen prägen Grundriss, Trennung, Licht, Sichtschutz und Atmosphäre.

---

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Fensterrahmen / Red-Cedar-Rahmen | Holz, Glas teils ersetzt | Abbruchgebäude / geerntete Rahmen; Sekundärquelle nennt Krankenhausfenster | Außenfenster | Trennwände / innere Fassade zwischen Büros und Gemeinschaftsbereichen | Menge unbekannt | nein | ja | innen hüllenartig | nein | Ernte, Auswahl, Montage; gebrochenes Glas ersetzt | geneigt / flach montiert, Details unbekannt | unbekannt | Sichtschutz, Akustik, Klima, Brandschutz unbekannt | unbekannt | Maße vorgegeben, Glaszustand | S1–S4, S6 | Anzahl, Prüfwerte |
| wiederverwendeter Stahl | Stahl | unbekannt | unbekannt | unbekannte Bauteile im Büroausbau | unbekannt | unbekannt | unbekannt | unbekannt | nein | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Rolle/Menge nicht belegt | S1 | fast alles |
| Betonblöcke | Beton | ursprüngliches Tropicana / laut Sekundärquelle | Bestandsmaterial | Trennwände | unbekannt | nein / unbekannt | ja | nein | nein | unbekannt | unbekannt | unbekannt | Schallschutz/Brandschutz unbekannt | unbekannt | nur Sekundärquelle | S6 | Menge, genaue Lage |
| Balustraden | Metall / unbekannt | laut Sekundärquelle dekommissionierte Ölplattform | Balustraden / Offshore-Bauteil | unbekannt | unbekannt | nein | ja | nein | nein | unbekannt | unbekannt | unbekannt | Absturzsicherung falls verwendet | unbekannt | Quelle sekundär | S6 | genaue Einbauorte |
| Türen | unbekannt | unbekannt | unbekannt | Büros | unbekannt | nein | ja | nein | nein | unbekannt | unbekannt | unbekannt | Brandschutz unbekannt | unbekannt | keine Reuse-Belege | unbekannt | alles |
| Beleuchtung | unbekannt | unbekannt | unbekannt | Beleuchtung | unbekannt | nein | nein | nein | ja | unbekannt | unbekannt | unbekannt | Elektrosicherheit | unbekannt | nicht belegt als Reuse | unbekannt | alles |
| feste Einbauten | Holz/sonstige | unbekannt | unbekannt | Büroeinbauten | unbekannt | nein | ja | nein | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Quellenfokus auf Fensterrahmen | unbekannt | alles |

---

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Transformationspotenzial ehemaliger Discothek erfassen | BlueCity, Superuse, COUP, Workspot | adaptive reuse | unbekannt | nicht zutreffend | unbekannt | unbekannt | im Bestandsgebäude | unkonventioneller Ort | Nutzung im Bestand | S1 |
| Bauteilinventar | geerntete Fensterrahmen identifizieren | Superuse | harvesting / material-driven design | Oogstkaart/Harvest-Map-Logik | unbekannt | Auswahl, Glasersatz | unbekannt | lokale / projektbezogene Quellen | Maße und Zustand variieren | Entwurf an Materialmaße angepasst | S1, S7 |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Altbau/Schwimmbad möglich | unbekannt | unbekannt |
| Rückbau | Fensterrahmen aus Donor-Kontext gewinnen | unbekannt | selektive Ernte | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Beschädigungsrisiko | unbekannt | S1 |
| Ausbau | Innenausbau der Büroflächen | COUP, Superuse, Workspot, Bauunternehmen | trockener / anpassender Ausbau vermutlich | unbekannt | nicht zutreffend | unbekannt | unbekannt | Arbeiten im Bestand | Passung, Bauzeit | Puzzeln mit Rahmen | S1, S3 |
| Transport | Reuse-Bauteile zum Standort | unbekannt | unbekannt | unbekannt | nicht zutreffend | unbekannt | unbekannt | lokal, soweit möglich | unbekannt | unbekannt | S3 |
| Lagerung | unbekannt | unbekannt | unbekannt | unbekannt | nicht zutreffend | unbekannt | unbekannt | unbekannt | Materialverfügbarkeit | unbekannt | unbekannt |
| Aufbereitung | beschädigtes Glas ersetzen, Rahmen ggf. reinigen/anpassen | unbekannt | Reparatur / Ersatz | unbekannt | nicht zutreffend | Glasersatz | unbekannt | Werkstatt/Baustelle unbekannt | unterschiedliche Zustände | Ersatzglas | S1 |
| Planung | Fensterrahmen als räumliche Ordnung einsetzen | Superuse | Materialgetriebener Entwurf | unbekannt | nicht zutreffend | nicht zutreffend | unbekannt | Entwurf folgt Fundstücken | keine Standardmodule | geneigte und flache Komposition | S1, S3 |
| Genehmigung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Brandschutz/Nutzung | unbekannt | unbekannt |
| Wiedereinbau | Fensterrahmen als Trennwände montieren | Projektteam | feste Innenfassade | unbekannt | nicht zutreffend | Montage | unbekannt | 1.300 m² Innenausbau | Maße/Anschlüsse | Komposition aus Rahmen | S1–S3 |
| Monitoring | CO₂-/Circularity-Angaben | Superuse / unbekannt | Vergleich zu konventionellem Büroausbau | unbekannt | nicht zutreffend | nicht zutreffend | unbekannt | unbekannt | Methode nicht öffentlich | Kennwert publiziert | S1, S5 |

---

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Reuse nicht tragwerkszentral | Standsicherheit Bestand | unbekannt | unbekannt | kein tragender Reuse-Fall | Bewertung als Vergleichsfall | S1 |
| Lastabtragung | Fensterrahmen nicht tragend | Eigenlast, Befestigung | unbekannt | unbekannt | Stabilität als Trennwand | unbekannt | S1 |
| Verbindung | Rahmen flach und geneigt zusammengesetzt | Befestigung, Stabilität | unbekannt | unbekannt | verschiedene Abmessungen | materialgetriebene Komposition | S1, S3 |
| Brandschutz | unbekannt | Büro- und Fluchtweganforderungen | unbekannt | unbekannt | gebrauchte Holz-/Glasrahmen | unbekannt | unbekannt |
| Schallschutz | geneigte Rahmen sollen akustische Wirkung unterstützen | Bürotrennung / Akustik | unbekannt | unbekannt | gebrauchte Fenster als Innenwand | geneigte Montage laut DutchArchitects | S3 |
| Feuchte | innen, ehemaliges Schwimmbad | Raumklima | unbekannt | unbekannt | Bestand mit Schwimmbadgeschichte | unbekannt | unbekannt |
| Wärmeschutz | Innenbauteile; externe Hülle nicht Kern des Falls | unbekannt | unbekannt | unbekannt | nicht primär energetische Hülle | unbekannt | S1 |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Luftdichtheit | unbekannt | unbekannt | unbekannt | unbekannt | Innenwände, nicht Außenhülle | unbekannt | unbekannt |
| TGA-Integration | Installationen reduziert laut Architekturpreis durch Klimaeigenschaften | Komfort, Klima | unbekannt | unbekannt | unkonventioneller Bestand | Minimierung Installationen | S5 |
| Barrierefreiheit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Dauerhaftigkeit | Red Cedar als langlebiges Holz | Innenraumdauerhaftigkeit | unbekannt | unbekannt | gebrauchte Rahmen | Reinigung/Ersatzglas | S1 |
| Wartung | unbekannt | Austauschbarkeit | unbekannt | unbekannt | gebrauchte Komponenten | unbekannt | unbekannt |
| Zulassung | unbekannt | Büroausbau | unbekannt | unbekannt | Reuse-Bauteile ohne Standarddaten | unbekannt | unbekannt |
| Haftung | unbekannt | unbekannt | unbekannt | unbekannt | gebrauchte Fensterrahmen | unbekannt | unbekannt |

---

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Fläche Büroflügel | 1.300 | m² | Projektangabe | erster Büroabschnitt | S1, S2 | belegt |
| Arbeitsplätze | 100 | Stück | Projektangabe | Nutzung | S1, S2 | belegt |
| Circularity / Reuse-Anteil | 90 | % | unbekannt | erster Transformationsabschnitt / Büros | S1, S3 | teilweise belegt |
| CO₂-Reduktion | 68 | % | Vergleich konventioneller Büroausbau | Büroausbau | S1, S2 | belegt, Methode unbekannt |
| CO₂-Einsparung | 60 | t CO₂ | Architekturpreis/BlueCity-Angabe | Bauprozess unbekannt | S5, S8 | teilweise belegt |
| wiederverwendete Masse | unbekannt | t | unbekannt | unbekannt | unbekannt | unbekannt |
| Anzahl Fensterrahmen | unbekannt | Stück | unbekannt | unbekannt | unbekannt | unbekannt |
| Kosten | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Bauzeit | innerhalb eines Jahres transformiert | Zeitraum | Projektangabe | Büroflügel | S1 | teilweise belegt |

---

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Unterschiedliche Rahmenmaße | technisch/gestalterisch | geerntete Fenster sind nicht standardisiert | Entwurf muss passen | Bauteil, Methode | Komposition aus flachen/geneigten Rahmen | Reuse-Material bestimmt Gestaltung | S1, S3 |
| Zustand von Glas | technisch | Bruch / Altzustand | Ersatz einzelner Scheiben | Bauteil | gebrochenes Glas ersetzt | Prüf-/Reparaturpuffer einplanen | S1 |
| Bestandserhalt vs Direct Reuse | methodisch | Transformation eines großen Bestandsgebäudes | Gefahr der Überwertung | Bewertung | Bestand separat führen | nur neue Bauteilfunktion zählen | S1 |
| Unbekannte Prüfungen | rechtlich/technisch | Quellen nennen keine Normen | Forschungsdatenlücke | Prüfung, Norm | unbekannt | Prüfprotokolle früh dokumentieren | unbekannt |
| Lose Möbel / flexible Arbeitsplätze | methodisch | Coworking enthält Möbel | nicht bewertungsrelevant | Bauteil, Möbelwarnung | Möbel ignorieren | nur feste Trennwände/Einbauten zählen | S1 |

---

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** Harvesting / lokale und projektnahe Materialsuche nach Superuse-Methodik.
- **Bauteilbörse / Quelle:** Oogstkaart-Logik / Superuse-Harvest Map; konkrete Bauteilbörse für jedes Element unbekannt.
- **Kostenwirkung:** unbekannt.
- **Zeitwirkung:** Büroflügel wurde innerhalb eines Jahres umgesetzt; Reuse-spezifische Mehrzeit unbekannt.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** hoch durch Auswahl, Puzzeln, Glasersatz, Montage; Stunden unbekannt.
- **Lagerung:** unbekannt.
- **Marktbarrieren:** Verfügbarkeit passender Bauteile, Qualität, Brandschutz/Schallschutz-Nachweise, Planungsflexibilität.

---

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** sehr hoch; Fensterrahmen sind prägendes Raumelement.
- **räumliche Transformation:** ehemalige Discothek wird zu Büro- und Coworking-Umgebung.
- **Atmosphäre / Ausdruck:** Collage aus roten/holzfarbenen Rahmen, Materialgeschichte sichtbar.
- **Umgang mit Spuren:** vorhandene Maße und Materialspuren bestimmen Gestaltung; beschädigtes Glas wurde ersetzt.
- **sozialer Wert:** Arbeitsplatz für Circular-Economy-Unternehmen und Innovationsnetzwerk.
- **Denkmal- oder Bestandswert:** ehemaliges Tropicana als ikonischer Bestandsort; Schutzstatus unbekannt.
- **Kritik / Grenzen:** kein tragender Reuse-Fall; genaue Mengen und Prüfungen öffentlich unvollständig.

---

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** Tragwerksplaner, Norm, Recht, Prüfung, detailliertes Bauteilinventar, Schadstoffprüfung, Kosten, Gewährleistung.
- **Welche neuen Entitäten wären sinnvoll?** Harvest Map / Oogstkaart; Materialgetriebener Entwurf; Circular Workplace.
- **Welche Daten fehlen?** Anzahl/Masse Fensterrahmen, Herkunftsliste, Befestigungsdetails, Brandschutz-/Schallschutzprüfung, Kosten, genaue CO₂-Methode.
- **Welche Quellen müssten geprüft werden?** vollständige Harvest Map, Bauunterlagen, CO₂-Berechnung, Ausschreibung/Bauteilliste, Genehmigungsunterlagen.

---

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja, aber nur als Vergleichsfall.
- **5 wichtigste Fakten:**
  1. 1.300 m² ehemaliger Discobereich wurden zu 100 Arbeitsplätzen transformiert.
  2. Fensterrahmen sind das zentrale wiederverwendete feste Raumelement.
  3. Quellen nennen 90 % circular/reused und 68 % CO₂-Reduktion.
  4. Das Projekt ist gebaut und 2017 eröffnet.
  5. Der Fall ist nicht tragwerkszentral.
- **5 wichtigste Bauteile:**
  1. Fensterrahmen / Red-Cedar-Rahmen.
  2. Glasflächen in den Rahmen.
  3. wiederverwendeter Stahl, Details unbekannt.
  4. Betonblöcke als Trennwände laut Sekundärquelle.
  5. mögliche Balustraden / weitere Reuse-Elemente, Details unbekannt.
- **5 wichtigste Hürden:**
  1. unterschiedliche Bauteilmaße.
  2. Glaszustand und Ersatz.
  3. Brandschutz/Schallschutz unbekannt.
  4. Trennung von Möbeln und festen Bauteilen.
  5. unvollständige Mengenangaben.
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Reuse kann die Raumatmosphäre prägen.
  2. Geerntete Bauteile sollten früh den Entwurf steuern.
  3. Kleine, sichtbare Reuse-Bauteile können große didaktische Wirkung haben.
  4. Kennwerte brauchen offene Methodik.
  5. Feste Innenwände zählen, Coworking-Möbel nicht.
- **5 offene Fragen:**
  1. Wie viele Fensterrahmen wurden eingebaut?
  2. Welche Prüfungen wurden dokumentiert?
  3. Welche Kostenwirkung hatte der Reuse-Ansatz?
  4. Welche Bauteile außer Rahmen und Stahl waren tatsächlich Reuse?
  5. Wie ist die 68-%-CO₂-Reduktion berechnet?

---

## Quellen und Links

- **S1** Superuse Studios, „BlueCity Offices“ – https://www.superuse-studios.com/projectplus/bluecity-offices/
- **S2** ältere Superuse-Projektseite, „BlueCity Offices“ – https://projects.superuse-studios.com/projects/blue-city/
- **S3** DutchArchitects, „BLUECITY, Rotterdam“ – https://dutcharchitects.org/projects/bluecity
- **S4** RE-USE.EU / Projektseite Blue City – https://www.re-use.eu/superuse-projects-blue-city
- **S5** Rotterdam Architectuurprijs, „Blue City 010 Offices“ – https://www.rotterdamarchitectuurprijs.nl/index.php?architect=Superuse+Studios%2C+Floris+Schiferli&item=blue-city-010-offices&lang=nl
- **S6** Circle Economy Foundation Knowledge Hub, „BlueCity: Repurposing a water park into a circular model city“ – https://knowledge-hub.circle-economy.com/article/30011
- **S7** Superuse Studios, „Harvest! Collect! Re-use!“ – https://www.superuse-studios.com/publication/harvest-collect-re-use/
- **S8** BlueCity, „Van beautycentrum tot 100% HACCP-proof FoodHub“ – https://www.bluecity.nl/en/nieuws/van-beautycentrum-tot-100-haccp-proof-foodhub
