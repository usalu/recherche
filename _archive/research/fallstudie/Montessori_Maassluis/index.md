---
entity: "fallstudie"
id: "Montessori_Maassluis"
title: "Montessori Maassluis — Fallstudie Direct Reuse / zirkuläres Bauen"
build_status: "promoted_phase42"
legacy_paths:
  - "Gebäude\\Montessori_Maassluis.md"
node_kind: "core"
bauobjekt:
  - "Montessori_Maassluis"
projekt:
  - "Montessori_Maassluis"
---

# Montessori Maassluis — Fallstudie Direct Reuse / zirkuläres Bauen

## Legacy Content

### Legacy Source: Gebäude\Montessori_Maassluis.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Montessori_Maassluis
- Secondary targets: projekt/Montessori_Maassluis; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Montessori Maassluis — Fallstudie Direct Reuse / zirkuläres Bauen

**Stand:** 2026-05-07  
**Sprache:** Deutsch  
**Arbeitsregel:** Gewertet werden nur tatsächlich eingebaute wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Da das Projekt nach aktuellem Quellenstand im Bau/noch nicht fertiggestellt ist, werden die wiederverwendeten Hohlkörperdecken als geplant bzw. projektseitig angekündigt markiert, bis der Einbau as-built belegt ist.

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Montessori Maassluis / Montessorischool Maassluis | untersuchter Fall | Kraaijvanger | belegt | Schulneubau |
| Gebäude | Montessorischool Maassluis | Ersatzneubau für bestehende Schule | Kraaijvanger news | belegt | bestehende Schule erfüllt Anforderungen nicht mehr |
| Projekt | new construction of Montessori School Maassluis | Neubauprojekt | Kraaijvanger news | belegt | Vertrag 02.02.2026 unterzeichnet |
| Ort | Maassluis, Zuid-Holland, Niederlande | Standort | Kraaijvanger; Schulwebsite | belegt | genaue Bauadresse der neuen Schule nicht eindeutig genannt; bestehende Schule Seringenstraat 110 |
| People | Kraaijvanger Architects | Architektur | Kraaijvanger | belegt | Entwurf 2024 |
| Projekt | Stichting Montessorischolen Monton / Stichting Montessorischolen Midden-Nederland (Monton) | Auftraggeber/Schulträger | Kraaijvanger | belegt | Quellen variieren in Langbezeichnung |
| Projekt | Anculus B.V. | Auftraggeber/Projektpartner | Kraaijvanger | belegt | |
| People | IMd Raadgevende Ingenieurs | Design team / Tragwerksbezug | Kraaijvanger | belegt | genaue Rolle als Tragwerksplaner naheliegend, aber in Quelle „design team“ |
| People | Vintis installatieadviseurs | TGA/Installationsberatung | Kraaijvanger | belegt | |
| People | VIA Landscape | Landschaftsplanung | Kraaijvanger | belegt | |
| People | Van Dijk Maasland B.V. | Bauunternehmen / Partner | Kraaijvanger news | belegt | |
| People | A. de Jong Groep | Projektpartner | Kraaijvanger news | belegt | |
| Bauteil | reused hollow core slabs | geplante/wahrscheinliche wiederverwendete Deckenbauteile | Kraaijvanger project page | belegt als Entwurfsangabe | Einbau as-built noch zu prüfen |
| Material | Beton / Spannbeton vermutlich | Material der Hohlkörperdecken | aus Bauteiltyp abgeleitet, nicht projektspezifisch genannt | unklar | Material nicht ausdrücklich in Quelle; nicht weiter quantifiziert |
| Tragwerkssystem | Hybrid aus Holzstützen und reused hollow core slabs | tragende Strategie | Kraaijvanger project page | belegt | große flexible Klassenräume |
| Reuse-Strategie | ex-situ Bauteilwiederverwendung / strukturelle Wiederverwendung geplant | Kern der Fallstudie | Kraaijvanger | teilweise belegt | noch nicht fertig |
| Kennwert | ca. 1.508 m² | Projektgröße laut News | Kraaijvanger news | belegt | BVO |
| Kennwert | 1.534 m² | GFA laut Projektseite | Kraaijvanger project page | belegt | Quellenabweichung |
| Kennwert | 10 educational groups + BSO | Programm | Kraaijvanger news | belegt | |
| Kennwert | mindestens 50 Jahre Nutzungsdauer | Entwurfsziel | Kraaijvanger project page | belegt | |
| Prozessphase | Bauvertrag unterzeichnet | Bau-/Vergabestand | Kraaijvanger news | belegt | 02.02.2026 |
| Projektstatus | completion scheduled end 2026; use early 2027 | Zeitplan | Kraaijvanger news | belegt | |
| Prüfung | unbekannt | Hohlkörperdeckenprüfung | unbekannt | unbekannt | keine Prüfdetails öffentlich |
| Norm | unbekannt | Schulbau/Tragwerk | unbekannt | unbekannt | keine Normnummern |
| Schadstoff | unbekannt | Donor-Decken | unbekannt | unbekannt | keine Herkunftsdaten |
| Bauteilbörse | unbekannt | Quelle der Hohlkörperdecken | unbekannt | unbekannt | Donor Building nicht genannt |
| Software/Tool | unbekannt | Material-/Bauteilmanagement | unbekannt | unbekannt | keine Angabe |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Geplanter Reuse-Einbau | Im Bau befindliche Projekte dürfen nicht wie gebaute Direct-Reuse-Fälle behandelt werden. | reused hollow core slabs sind im Entwurf genannt, aber as-built noch offen. | Projektstatus, Bauteil, Prüfung |
| Donor Building unbekannt | Für strukturelle Hohlkörperdecken ist die Herkunft entscheidend. | Herkunft der reused slabs ist öffentlich nicht genannt. | Gebäude, Bauteil, Logistik |
| As-built-Verifikation | Die Bewertung muss nach Fertigstellung überprüft werden. | Fertigstellung Ende 2026 / Nutzung Anfang 2027 geplant. | Prozessphase, Kennwert, Fallstudie |

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** geplant/angekündigt; partiell; ex-situ; Bauteilwiederverwendung; strukturelle Wiederverwendung von Hohlkörperdecken
- **Hauptniveau:** Tragwerk
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Der Ersatzneubau selbst ist keine Sanierung. Bewertbar wäre nur der tatsächliche Einbau wiederverwendeter Hohlkörperdecken. Neue Holzstützen, flexible Grundrisse, vorbereitete Erweiterbarkeit und 50-Jahre-Ziel zählen nicht als Direct Reuse, sondern als Neubau-/Anpassungsstrategie.
- **Warum ist der Fall relevant?** Wenn der Einbau as-built bestätigt wird, wäre das Projekt ein aktueller Schulbau mit tragender Wiederverwendung von Betonfertigteilen — besonders relevant, weil Schulbauten hohe Anforderungen an Tragwerk, Schall, Brandschutz und Nutzungssicherheit haben.

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | bestehende Schule bewertet als unzureichend | Monton/Gemeinde/Projektteam | Bedarfsermittlung | unbekannt | nicht relevant | nicht relevant | unbekannt | aktueller Standort | Bestand erfüllt Anforderungen nicht | Ersatzneubau | Kraaijvanger news |
| Bauteilinventar | Quelle der Hohlkörperdecken unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Donor Building nicht genannt | unbekannt | unbekannt |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | reused Betonfertigteile können Prüfung erfordern | unbekannt | unbekannt |
| Rückbau | Gewinnung der Hohlkörperdecken geplant/erfolgt unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | zerstörungsarme Demontage | unbekannt | unbekannt |
| Ausbau | Hohlkörperdecken aus Donor-Gebäude ausbauen | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Beschädigung, Vorspannung, Anschlussreste | unbekannt | unbekannt |
| Transport | Transport nach Maassluis | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | schwere Betonfertigteile | unbekannt | unbekannt |
| Lagerung | Zwischenlagerung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Timing mit Neubau | unbekannt | unbekannt |
| Aufbereitung | Zuschneiden/Prüfen/Anpassen der Hohlkörperdecken | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Tragfähigkeit und Anschlüsse | unbekannt | unbekannt |
| Planung | Hybridstruktur aus Holzstützen und reused hollow core slabs | Kraaijvanger; IMd; Team | Entwurf für flexible Räume | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Integration alter Decken | Tragwerk mit Holzstützen | Kraaijvanger |
| Genehmigung | unbekannt | Gemeinde/Planer | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Schulbau + Reuse | unbekannt | unbekannt |
| Wiedereinbau | Einbau der Hohlkörperdecken | Bauunternehmen/Tragwerksplaner | geplant | unbekannt | unbekannt | unbekannt | unbekannt | Baustelle | as-built noch offen | nach Fertigstellung prüfen | Kraaijvanger |
| Monitoring | nach Nutzung ab 2027 möglich | Schule/Bauherr | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Betriebserfahrung fehlt | später prüfen | unbekannt |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Entwurf | 2024 | Jahr | unbekannt | Projekt | Kraaijvanger project page | belegt |
| Bauvertrag unterzeichnet | 02.02.2026 | Datum | unbekannt | Projekt | Kraaijvanger news | belegt |
| geplante Fertigstellung | Ende 2026 | Zeitraum | unbekannt | Projekt | Kraaijvanger news | belegt |
| geplante Nutzung | Anfang 2027 | Zeitraum | unbekannt | Projekt | Kraaijvanger news | belegt |
| Fläche laut News | ca. 1.508 | m² BVO | unbekannt | Gebäude | Kraaijvanger news | belegt |
| Fläche laut Projektseite | 1.534 | m² GFA | unbekannt | Gebäude | Kraaijvanger project page | belegt; Quellenabweichung |
| Unterrichtsgruppen | 10 | Anzahl | unbekannt | Programm | Kraaijvanger news | belegt |
| geplante Lebensdauer | mindestens 50 | Jahre | unbekannt | Gebäude | Kraaijvanger project page | belegt |
| Anzahl reused hollow core slabs | unbekannt | Anzahl | unbekannt | Tragwerk | unbekannt | unbekannt |
| Masse reused hollow core slabs | unbekannt | t | unbekannt | Tragwerk | unbekannt | unbekannt |
| CO₂-Einsparung | unbekannt | kg CO₂e | unbekannt | unbekannt | unbekannt | unbekannt |
| Kosten | unbekannt | EUR | unbekannt | Projekt | unbekannt | unbekannt |
| U-Wert | unbekannt | W/m²K | unbekannt | Gebäudehülle | unbekannt | unbekannt |
| Zirkularitätskennwert | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** unbekannt; offizielle Quellen nennen reused hollow core slabs, aber nicht die Quelle, Bauteilbörse oder den Beschaffungsprozess.
- **Bauteilbörse / Quelle:** unbekannt.
- **Kostenwirkung:** Kraaijvanger beschreibt die Konstruktion als cost-efficient; konkrete Kosten oder Vergleichswerte unbekannt.
- **Zeitwirkung:** unbekannt; Bauvertrag unterzeichnet Februar 2026, Fertigstellung geplant Ende 2026.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** unbekannt; wahrscheinlich erhöht durch Prüfung/Anpassung der Hohlkörperdecken, aber nicht belegt.
- **Lagerung:** unbekannt.
- **Marktbarrieren:** fehlende Herkunftsdaten, Prüfbedarf, Genehmigung, Beschaffungslogistik, as-built-Verifikation.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** Donor Building, Anzahl/Masse der Hohlkörperdecken, Materialgüte, Prüfprotokolle, Normen, CO₂, Kosten, Bauablauf, Lagerung, Versicherungsmodell.
- **Sinnvolle neue Entitäten:** Geplanter Reuse-Einbau; Donor Building unbekannt; As-built-Verifikation.
- **Fehlende Daten:** Herkunft, Menge, Einbauorte, Anschlussdetails, Lastannahmen, Brandschutz-/Schallnachweise.
- **Zu prüfende Quellen:** Bau-/Werkpläne, Tragwerksbericht IMd, Bauteilpass, Ausschreibung, Baustellenfotos 2026, Abnahme-/As-built-Unterlagen Ende 2026/Anfang 2027.

## Quellen und Links

- Kraaijvanger – Montessori Maassluis project: https://www.kraaijvanger.nl/en/projects/montessori-maassluis
- Kraaijvanger – Construction contract signed: https://www.kraaijvanger.nl/en/news/de-handtekeningen-zijn-gezet-montessorischool-maassluis
- Montessorischool Maassluis – school website: https://www.montessorischoolmaassluis.nl/
- Kraaijvanger – Dutch news page: https://www.kraaijvanger.nl/nl/nieuws/de-handtekeningen-zijn-gezet-montessorischool-maassluis
