---
entity: "fallstudie"
id: "BlueCity_Offices_Rotterdam"
title: "BlueCity Offices Rotterdam – Fallstudie Direct Reuse / zirkuläres Bauen"
build_status: "promoted_phase42"
legacy_paths:
  - "Gebäude\\BlueCity_Offices_Rotterdam.md"
node_kind: "core"
bauobjekt:
  - "BlueCity_Offices_Rotterdam"
projekt:
  - "BlueCity_Offices_Rotterdam"
---

# BlueCity Offices Rotterdam – Fallstudie Direct Reuse / zirkuläres Bauen

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

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; feste räumliche Innenbauteile; adaptive reuse
- **Hauptniveau:** räumlicher Innenausbau / innere Hülle; teilweise Material
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Der Erhalt des Tropicana-Bestands zählt nicht als Direct Reuse. Bewertet werden die geernteten Fensterrahmen als neue Trennwände/Innenfassade und weitere feste wiederverwendete Bauteile.
- **Warum ist der Fall relevant?** Sehr anschauliches Beispiel für Material-Driven Design: Abmessungen vorhandener Fensterrahmen prägen Grundriss, Trennung, Licht, Sichtschutz und Atmosphäre.

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

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** Tragwerksplaner, Norm, Recht, Prüfung, detailliertes Bauteilinventar, Schadstoffprüfung, Kosten, Gewährleistung.
- **Welche neuen Entitäten wären sinnvoll?** Harvest Map / Oogstkaart; Materialgetriebener Entwurf; Circular Workplace.
- **Welche Daten fehlen?** Anzahl/Masse Fensterrahmen, Herkunftsliste, Befestigungsdetails, Brandschutz-/Schallschutzprüfung, Kosten, genaue CO₂-Methode.
- **Welche Quellen müssten geprüft werden?** vollständige Harvest Map, Bauunterlagen, CO₂-Berechnung, Ausschreibung/Bauteilliste, Genehmigungsunterlagen.

## Quellen und Links

- **S1** Superuse Studios, „BlueCity Offices“ – https://www.superuse-studios.com/projectplus/bluecity-offices/
- **S2** ältere Superuse-Projektseite, „BlueCity Offices“ – https://projects.superuse-studios.com/projects/blue-city/
- **S3** DutchArchitects, „BLUECITY, Rotterdam“ – https://dutcharchitects.org/projects/bluecity
- **S4** RE-USE.EU / Projektseite Blue City – https://www.re-use.eu/superuse-projects-blue-city
- **S5** Rotterdam Architectuurprijs, „Blue City 010 Offices“ – https://www.rotterdamarchitectuurprijs.nl/index.php?architect=Superuse+Studios%2C+Floris+Schiferli&item=blue-city-010-offices&lang=nl
- **S6** Circle Economy Foundation Knowledge Hub, „BlueCity: Repurposing a water park into a circular model city“ – https://knowledge-hub.circle-economy.com/article/30011
- **S7** Superuse Studios, „Harvest! Collect! Re-use!“ – https://www.superuse-studios.com/publication/harvest-collect-re-use/
- **S8** BlueCity, „Van beautycentrum tot 100% HACCP-proof FoodHub“ – https://www.bluecity.nl/en/nieuws/van-beautycentrum-tot-100-haccp-proof-foodhub
