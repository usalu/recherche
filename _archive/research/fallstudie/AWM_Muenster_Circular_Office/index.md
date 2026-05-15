---
entity: "fallstudie"
id: "AWM_Muenster_Circular_Office"
title: "AWM Münster – Zirkulärer Büroausbau 3. OG – Fallstudie Direct Reuse / zirkuläres Bauen"
build_status: "promoted_phase42"
legacy_paths:
  - "Gebäude\\AWM_Muenster_Circular_Office.md"
node_kind: "core"
bauobjekt:
  - "AWM_Muenster_Circular_Office"
projekt:
  - "AWM_Muenster_Circular_Office"
---

# AWM Münster – Zirkulärer Büroausbau 3. OG – Fallstudie Direct Reuse / zirkuläres Bauen

## Legacy Content

### Legacy Source: Gebäude\AWM_Muenster_Circular_Office.md

- Map action: split_into_case_graph
- Primary target: fallstudie/AWM_Muenster_Circular_Office
- Secondary targets: projekt/AWM_Muenster_Circular_Office; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# AWM Münster – Zirkulärer Büroausbau 3. OG – Fallstudie Direct Reuse / zirkuläres Bauen

**Projekt:** Abfallwirtschaftsbetriebe Münster, Büroetage Rösnerstraße / 3. OG  
**Bearbeitung:** Deutsch, kompakt, quellenbasiert  
**Grundregel:** Gezählt werden nur wiederverwendete Bau-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Bestandserhalt und lose Möbel werden nicht als Direct Reuse gewertet.

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | AWM Münster, 3. OG Rösnerstraße | zirkulärer Büroinnenausbau | S1–S5 | belegt | kleines Interior-Projekt |
| Gebäude | altes Verwaltungsgebäude der awm | Bestand, umgebautes 3. Obergeschoss | S2, S5 | belegt | Bestandserhalt nicht als Direct Reuse |
| Ort | Münster, Rösnerstraße | Standort | S2, S5 | belegt | genaue Hausnummer unbekannt |
| Projekt | moderne Arbeitswelt aus gebrauchten Materialien | neue Büro-/Workshop-/Küchen-/Besprechungsflächen | S2, S5 | belegt | 250 m² nach urselmann/AWM, 200 m² in Portfolio Dritter |
| People | Abfallwirtschaftsbetriebe Münster, urselmann interior, Concular, Petra Jablonická, Sven Urselmann | Bauherr/Nutzer, Entwurf/Innenausbau, Materialplattform/Ökobilanz | S1–S5 | belegt | genaue Vertragsrollen nicht vollständig |
| Bauteil | Glastrennwände und Türen | Reuse-Bauteile aus Behrensbau Düsseldorf | S4, S6 | belegt | fest eingebaut, zählt |
| Bauteil | WC-Trennwände | Reuse aus Behrensbau Düsseldorf | S4 | belegt | fest eingebaut, zählt |
| Bauteil | Kabeltrassen | als Regale und Allgemeinbeleuchtung genutzt | S1, S4 | belegt | fest eingebaut/technisch, zählt teilweise |
| Bauteil | Wandverkleidung aus alten Holzstühlen | feste Wandbekleidung | S1, S4 | belegt | Stühle als Möbel alt, neue Funktion feste Wandverkleidung; zählt als festes Bauteil mit Warnung |
| Bauteil | Holz aus Deckenkonstruktion/Supermarkt/Discounter | Sideboard, Küche, Wand-/Unterkonstruktion | S1, S4, S6 | belegt/teilweise | feste Einbauten zählen, lose Möbel nicht |
| Material | Hanfkalksteine, Lehm, Akustikbaffeln, Teppich | teils C2C/recycelt/biobasiert, nicht Direct Reuse | S1, S4 | belegt | separat führen |
| Bauteilbörse | Concular | Materialbeschaffung und Ökobilanzierung | S3, S6 | belegt | Glastrennwände aus Behrensbau |
| Kennwert | 6,9 t wiedergewonnene Materialien | Reuse-/Materialkennwert | S1, S3 | belegt | Bilanzgrenze Büroausbau |
| Kennwert | 13,32 t CO₂e / 82 % | Einsparung gegenüber konventionell | S1–S3, S5 | belegt | Methode nicht vollständig öffentlich |
| Kennwert | 95,6 % c2c-inspiriert oder ReUse | Produktanteil | S1–S3 | belegt | nicht alles Direct Reuse |
| Kennwert | 250 m² / 200 m² | Fläche | S1, S2 | teilweise belegt | Quellenkonflikt |
| Logistik | Urban Mining aus öffentlichen Gebäuden | Beschaffung gebrauchter Baumaterialien | S1, S3, S6 | belegt | detaillierte Distanzen unbekannt |
| Methode | ReUse first / Design follows availability | Entwurfsprinzip | S1, S3 | belegt | gutes Beispiel für Innenausbau |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| ReUse-Interior | feste Innenausbau-Bauteile zwischen Möbel und Bauwerk | Glastrennwände, WC-Trennwände, Wandverkleidung | Bauteil, Reuse-Strategie |
| Materialherkunftsseite / QR-Materialatlas | projektspezifische Material-Herkunftsdokumentation | AWM-Materialseite | Dokument, Datenmodell, Bauteil |
| Reaktivierung | technische/gestalterische Wiederinbetriebnahme gebrauchter Elemente | Reuse-LED-Leuchten, Sattler-Leuchten | Aufbereitungsmethode, TGA |

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; fester Innenausbau; technische Gebäude-/Elektroelemente; Bauteilwiederverwendung; Materialwiederverwendung; adaptive reuse
- **Hauptniveau:** räumlicher Innenausbau / technische Ausstattung / feste Einbauten
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Der Umbau des bestehenden Gebäudes und die Reparatur von Möbeln werden nicht als Direct Reuse gezählt. Gezählt werden feste, neu eingebaute Bauteile wie Glastrennwände, WC-Trennwände, Kabeltrassen-Regale/Leuchten, Wandverkleidung und feste Holzeinbauten.
- **Warum ist der Fall relevant?** AWM ist ein sehr gut dokumentierter Innenausbau mit Materialherkünften, Kennwerten und öffentlich zugänglicher Materialliste. Er eignet sich als Referenz für ReUse-Interior, nicht für tragende Reuse-Fälle.

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Entscheidung Umbau statt Rückbau | AWM, urselmann interior | ReUse first / Umbau vor Neubau | unbekannt | nicht zutreffend | unbekannt | unbekannt | im Bestand | ungenutztes 3. OG | Umbau | S2, S5 |
| Bauteilinventar | Materialien und Herkunft dokumentieren | AWM, urselmann interior, Concular | Materialliste / QR-Seiten | Materialherkunftsseite | nicht zutreffend | nicht zutreffend | unbekannt | digital | Transparenz | öffentliche Materialseite | S4 |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Altbau | unbekannt | unbekannt |
| Rückbau | Glastrennwände aus Behrensbau zurückgewinnen | Concular / Partner | Urban Mining | Concular-Plattform | selektiver Ausbau | unbekannt | unbekannt | Düsseldorf -> Münster | Transport/Glasbruch | Plattformbeschaffung | S4, S6 |
| Ausbau | 3. OG umbauen | urselmann interior, Handwerk | zirkulärer Innenausbau | unbekannt | nicht zutreffend | Montage / Reparatur | unbekannt | Baustelle im Bestand | Koordination verschiedener Reuse-Materialien | Design follows availability | S1, S3 |
| Transport | Materialien aus unterschiedlichen öffentlichen Gebäuden | urselmann, Concular, Lieferanten | Einzelbeschaffung | Concular | nicht zutreffend | unbekannt | unbekannt | mehrere Quellen in Deutschland | Logistikaufwand | direkte Beschaffung | S1, S3 |
| Lagerung | unbekannt | unbekannt | unbekannt | unbekannt | nicht zutreffend | unbekannt | unbekannt | unbekannt | wechselnde Verfügbarkeit | unbekannt | unbekannt |
| Aufbereitung | Holz, Kabeltrassen, Stühle, Leuchten anpassen | urselmann interior / Handwerk | Reparatur, Upcycling, Reaktivierung | 3D-Druck für Halterungen | nicht zutreffend | Zuschnitt, Reparatur, Montage | unbekannt | Werkstatt/baustelle | nicht standardisierte Bauteile | handwerkliche Details | S1, S4 |
| Planung | Entwurf nach verfügbaren Bauteilen | urselmann interior | Design follows availability | unbekannt | nicht zutreffend | nicht zutreffend | unbekannt | Materialsuche parallel | Verfügbarkeit statt Katalog | kreatives Handwerk | S1, S3 |
| Genehmigung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Brandschutz/Arbeitsstätten möglich | unbekannt | unbekannt |
| Wiedereinbau | Glastrennwände, Regale, Leuchten, Wandverkleidung montieren | urselmann / Handwerk | feste Montage, demontierbare Details | unbekannt | nicht zutreffend | Wiedereinbau | unbekannt | Baustelle | Passung | Anpassung | S1, S4 |
| Monitoring | zirkuläre Ökobilanzierung | Concular, urselmann | LCA / Vergleich konventionell | Concular | nicht zutreffend | nicht zutreffend | unbekannt | digital | Bilanzgrenzen nicht vollständig offen | Kennwerte publiziert | S3 |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Fläche | 250 | m² | Projektangabe urselmann/AWM | Büroetage | S2, S4 | belegt |
| Fläche | 200 | m² | Drittportfolio | Büroetage | S1 | teilweise belegt / Konflikt |
| wiedergewonnene Materialien | 6,9 | t | Concular zirkuläre Ökobilanzierung | Bauprojekt Büroetage | S1, S3 | belegt |
| Abfallvermeidung | 6,9 | t | Concular | Büroetage | S1, S3 | belegt |
| CO₂-Einsparung | 13,32 | t CO₂e | zirkuläre Ökobilanzierung | gegenüber konventioneller Bauweise | S1–S3 | belegt |
| CO₂-Reduktion | 82 | % | zirkuläre Ökobilanzierung | gegenüber konventioneller Bauweise | S1–S3, S5 | belegt |
| Wassereinsparung | 32 | % | AWM-Angabe | gegenüber konventioneller Bauweise | S5 | belegt |
| c2c-inspiriert oder ReUse | 95,6 | % Produkte | Concular/urselmann | alle Produkte im Ausbau | S1–S3 | belegt, nicht Direct-Reuse-Anteil |
| CO₂-Einsparung Glastrennwände | 4,39 | t CO₂ | AWM Materialseite | Glastrennwände | S4 | belegt |
| CO₂-Einsparung Hanfkalk | 1,7 | t CO₂e | AWM Materialseite | Vergleich zu Kalksandstein | S4 | belegt, nicht Reuse |
| alte Holzstühle für Wandverkleidung | >500 / 550 | Stück | AWM / Drittportfolio | Wandverkleidung | S1, S4 | teilweise belegt |
| Kostenwirkung | vergleichbare Kosten | qualitativ | AWM-Zitat | Gesamtprojekt | S5 | teilweise belegt |
| Bauzeit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** ReUse first, Urban Mining über Concular und direkte Materialsuche; Design & Build durch urselmann interior.
- **Bauteilbörse / Quelle:** Concular für Glastrennwände aus Behrensbau Düsseldorf; weitere Quellen: öffentliche Gebäude, Supermarkt-/Discounter-Auflösung, Schul-/Theaterstühle, AWM-Lager.
- **Kostenwirkung:** AWM nennt vergleichbare Kosten gegenüber konventioneller Bauweise; genaue Kostentabelle unbekannt.
- **Zeitwirkung:** unbekannt.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** hoch durch Suche, Demontage, Aufbereitung, handwerkliche Anpassungen; genaue Stunden unbekannt.
- **Lagerung:** unbekannt.
- **Marktbarrieren:** Abnahmequalität, Norm-/Prüfnachweise, Logistik, unklare Haftung, höhere Planungsflexibilität.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** Normen, Prüfberichte, Tragwerksplanung, Brandschutzdetails, Gewährleistung, detaillierte Kosten.
- **Welche neuen Entitäten wären sinnvoll?** ReUse-Interior; Materialherkunftsseite/QR-Materialatlas; Reaktivierung.
- **Welche Daten fehlen?** Mengen je Bauteil, Prüfungen für Glas und Elektro, konkrete Befestigungen, Arbeitsstunden, Lagerzeiten, CO₂-Methode im Detail.
- **Welche Quellen müssten geprüft werden?** Concular-LCA-Bericht, urselmann-Ausführungspläne, Brandschutzkonzept, Elektroabnahme, Materialpässe/QR-Daten komplett.

## Quellen und Links

- **S1** Petra Jablonická Portfolio, „95,6% circular reconstruction of offices for AWM Münster“ – https://www.jablonicka.com/work/95%2C6%25-circular-reconstruction-of-offices-for-awm-m%C3%BCnster-
- **S2** urselmann interior, „AWM“ – https://www.urselmann-interior.de/awm-office
- **S3** Concular, „Zirkuläres Bauen funktioniert: 95,6% zirkuläre Beschaffung für Bauprojekt in Münster“ – https://concular.de/bueroetage-muenster/
- **S4** AWM Münster, „Material“ – https://awm.stadt-muenster.de/gemeinsam-nachhaltig/klima-technik-innovation/kreislauffaehiges-bauen/material
- **S5** AWM Münster, „Moderne Arbeitswelt aus gebrauchten Materialien“ – https://awm.stadt-muenster.de/aktuelles/newsdetail/moderne-arbeitswelt-aus-gebrauchten-materialien
- **S6** AWM Münster, „Küche“ – https://awm.stadt-muenster.de/gemeinsam-nachhaltig/klima-technik-innovation/kreislauffaehiges-bauen/kueche
