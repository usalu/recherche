---
entity: "fallstudie"
id: "Superlocal_Expogebouw_Bleijerheide"
title: "SUPERLOCAL Expogebouw, Bleijerheide/Kerkrade — Fallstudie Direct Reuse / zirkuläres Bauen"
build_status: "promoted_phase42"
legacy_paths:
  - "Gebäude\\Superlocal_Expogebouw_Bleijerheide.md"
node_kind: "core"
bauobjekt:
  - "Superlocal_Expogebouw_Bleijerheide"
projekt:
  - "Superlocal_Expogebouw_Bleijerheide"
---

# SUPERLOCAL Expogebouw, Bleijerheide/Kerkrade — Fallstudie Direct Reuse / zirkuläres Bauen

## Legacy Content

### Legacy Source: Gebäude\Superlocal_Expogebouw_Bleijerheide.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Superlocal_Expogebouw_Bleijerheide
- Secondary targets: projekt/Superlocal_Expogebouw_Bleijerheide; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# SUPERLOCAL Expogebouw, Bleijerheide/Kerkrade — Fallstudie Direct Reuse / zirkuläres Bauen

**Bearbeitungsstand:** 2026-05-06  
**Sprache:** Deutsch  
**Regelprüfung:** Gewertet werden nur wiederverwendete Bau-/Konstruktionselemente. Lose Möbel, reine Sanierung und unverifizierte Circularity-Claims werden nicht als Wiederverwendung gezählt.

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | SUPERLOCAL Expogebouw | untersuchtes Info-/Testgebäude | SUPERLOCAL-Projektseite | belegt | Teilprojekt der Super Circular Estate Entwicklung |
| Ort | Bleijerheide, Kerkrade, Niederlande | Standort | SUPERLOCAL / Kerkrade | belegt | Projektgebiet Bleijerheide |
| Projekt | SUPERLOCAL – Super Circular Estate | übergeordnete Quartiersentwicklung | SUPERLOCAL / Gemeinde Kerkrade | belegt | Wiederverwendung von Materialien aus Hochhausflats |
| Gebäude | Expogebouw / Superlocal Pavilion | Empfängerbau | SUPERLOCAL / Maurer United | belegt | Infogebäude / Pavillon |
| Gebäude | Hochhausflat Ursulastraat | Donorgebäude | SUPERLOCAL | belegt | 50 Jahre alte Flat; Teile aus Wohnung herausgesägt |
| Bauteil | drei Wohnungsteile / Betonunits | Hauptreuse-Bauteile | SUPERLOCAL | belegt | je ca. 45 t laut Projektseite; andere Projektmeldung ca. 40 t |
| Bauteil | Aluminiumrohre, Heizkörper, Plattenmaterial, Fensterrahmen, Haustüren, Geländer, Brüstungen, Küche | weitere wiederverwendete Bauteile | SUPERLOCAL | belegt | feste Bauteile / technische Teile / feste Einbauten |
| Material | Beton, Aluminium, Holz/Fensterrahmen, Metall, Plattenmaterial | wiederverwendete Materialien | SUPERLOCAL | teilweise belegt | genaue Materialqualitäten unbekannt |
| People | Maurer United | Architekt / Entwurf | Maurer United | belegt | Designteam: Marc Maurer, Nicole Maurer, Alan Frijns, Annika Frencken |
| People | HEEMwonen | Auftraggeber / Partner | SUPERLOCAL / Maurer United | belegt | Wohnungsbaugesellschaft |
| People | Gemeinde Kerkrade, IBA Parkstad | Partner / Koordination | SUPERLOCAL | belegt | Ambitionen und Koordination |
| People | Volantis | Konstrukteur | SUPERLOCAL | belegt | bestimmte wiederverwendbare Materialien/Elemente |
| People | Dusseldorp | Rückbauunternehmen / Materiallieferant | SUPERLOCAL / Maurer United | belegt | erntete Materialien beim Rückbau |
| People | Bouwbedrijven Jongen | Bauunternehmen | SUPERLOCAL / Maurer United | belegt | Realisierung |
| Abbruchmethode | selektive Demontage / Heraussägen / Herausheben | gewann große Reuse-Elemente | SUPERLOCAL | belegt | 52-m-Kran; Trailertransport |
| Aufbereitungsmethode | möglichst ohne Bearbeitung; Repair/Remanufacturing als Lehre | Strategie und spätere Lehre | SUPERLOCAL | belegt | bei Fenstern wegen Asbest kostspielige Bearbeitung |
| Prüfung | unabhängiges Bauadviesbureau prüfte technische/finanzielle/prozessuale Machbarkeit | Evaluations- und Machbarkeitsprüfung | SUPERLOCAL | belegt | genaue Prüfnormen unbekannt |
| Schadstoff | Asbest in Fensterrahmen | Hürde | SUPERLOCAL | belegt | künftige Strategie: gutes Holz trennen, kontaminiertes Holz separieren |
| Logistik | 52-m-Kran, Trailer, lokale Umsetzung | bauteilbezogene Logistik | SUPERLOCAL | belegt | Teile aus oberem Geschoss herausgehoben |
| Kennwert | 95 % wiederverwendete Materialien; Maurer United nennt 100 % Material aus Abriss | Reuse-Anteil | SUPERLOCAL / Maurer United | teilweise belegt | Quellenkonflikt; offizielle Projektseite: 95 % |
| Förderprogramm | Urban Innovative Actions / IBA Parkstad | Kontextförderung | Kerkrade / SUPERLOCAL | belegt | € 5 Mio. EU-Förderung für Gesamtprojekt laut Gemeinde Kerkrade |
| Tool | Track-and-trace / Materialdatenbank / QR-Code / STABU-Code | im Gesamtprojekt genutzt | SUPERLOCAL | belegt | nicht sicher spezifisch für Expogebouw-Elemente |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Donor-/Empfängerquartier | Materialströme bleiben im Quartier und sind nicht nur objektbezogen | Bleijerheide / Ursulastraat → Expogebouw und spätere Wohnungen | verbindet Ort, Logistik, Projekt, Material |
| Bauteil-Ernte | „Harvesting“ ist hier operativ zentral | Dusseldorp erntet Bauteile beim Rückbau | verknüpft Abbruchmethode, Bauteil, Logistik |
| Quellenkonflikt Kennwert | Reuse-Anteile werden unterschiedlich angegeben | 95 % vs. 96 % vs. 100 % | verbindet Kennwert, Bericht, Vertrauensgrad |

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; Materialwiederverwendung; Demonstrator  
- **Hauptniveau:** Tragwerk/Raum durch große Beton-Wohnungsteile; zusätzlich Hülle, Innenausbau, TGA, feste Einbauten und Außenraum  
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Das Expogebouw wurde aus ausgebauten Wohnungsteilen und geernteten Bauteilen eines anderen Gebäudes erstellt. Es ist kein bloßer Bestandserhalt. Recycling in kleinere Rohstofffraktionen ist nur ein Teil des Gesamtprogramms, nicht der Kern dieses Demonstrators.  
- **Warum ist der Fall relevant?** Er testet 1:1-Hochwertreuse großer Beton-/Wohnungseinheiten aus einem Wohnhochhaus und dokumentiert reale Prozess-, Logistik-, Schadstoff- und Koordinationshürden.

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Wiederverwendbare Elemente aus Flat identifiziert | Volantis, Dusseldorp, Maurer United, HEEMwonen | Bauteilbewertung | unbekannt | — | — | Bewehrungsuntersuchung genannt | lokal im Projektgebiet | vorhandene Qualität unklar | frühe Bau-Team-Kooperation | SUPERLOCAL |
| Bauteilinventar | Materialien/Elemente aus Flat bestimmt | Dusseldorp, Volantis, Maurer United | Ernteplanung | später Track-and-trace im Gesamtprojekt | — | — | unbekannt | unbekannt | Architekt an verfügbare Elemente gebunden | integraler Bauprozess | SUPERLOCAL |
| Schadstoffprüfung | Asbest in Fensterrahmen als Problem erkannt | unbekannt | Schadstoffbewertung | unbekannt | — | Trennung kontaminierter/guter Teile als Lehre | unbekannt | unbekannt | teure Bearbeitung | künftige Trennung von gutem Holz und Asbestanteilen | SUPERLOCAL |
| Rückbau | Hochhausflat demontiert/gestrippt | Dusseldorp | selektive Demontage | 52-m-Kran bei Großteilen | Sägen und Herausheben | möglichst wenig Bearbeitung | Riss-/Maßprüfung als Frage | Trailertransport | Beschädigungsrisiko | große Elemente statt viele kleine diskutiert | SUPERLOCAL |
| Ausbau | drei Wohnungsteile aus oberem Geschoss entnommen | Dusseldorp | Heraussägen, Ausheben | 52-m-Kran | selektiv | unbekannt | Risse/Maßhaltigkeit beobachtet/geprüft | in Projektgebiet transportiert | Gewicht 40–45 t je Teil | Kran + Trailer | SUPERLOCAL |
| Transport | Bauteile in Projektgebiet bewegt | Dusseldorp | Trailer | Kran/Trailer | — | — | unbekannt | lokal | schwere Elemente | kurze lokale Wege | SUPERLOCAL |
| Lagerung | Bauteile/Materialien zwischengelagert | Dusseldorp/Projektteam | Container/Depot im Gesamtprojekt | Track-and-trace im Gesamtprojekt | — | — | unbekannt | lokale Materiallager | Zeitpunkt der Verfügbarkeit | frühere Ketteneinbindung empfohlen | SUPERLOCAL |
| Aufbereitung | Teile wiederverwendet, teils Bearbeitung | Bauunternehmen/Handwerker | Repair/Remanufacturing als Lehre | unbekannt | — | möglichst ohne Bearbeitung; teils Repair | unbekannt | unbekannt | Qualität, Asbest | Repair/Remanufacturing für weitere Wohnungen | SUPERLOCAL |
| Planung | Entwurf an geerntete Elemente angepasst | Maurer United, Volantis | Material-driven Design | unbekannt | — | — | statische Randbedingungen | Planungs-/Bauprozess verschoben | Reihenfolge ungewohnt | frühe Integration aller Beteiligten | SUPERLOCAL |
| Genehmigung | experimentelles Gebäude | HEEMwonen, Gemeinde, IBA, Bauaufsicht unbekannt | unbekannt | unbekannt | — | — | unabhängiges Bauadviesbureau | — | Gesetzgebung als Herausforderung | Evaluation | SUPERLOCAL |
| Wiedereinbau | Erstellung Expogebouw | Bouwbedrijven Jongen, Dusseldorp | Montage geernteter Bauteile | unbekannt | — | Wiedereinbau | Machbarkeitsprüfung | lokale Baustelle | Lieferzeitpunkte | Bauketten früher einbinden | SUPERLOCAL |
| Monitoring | Evaluation erste Phase | HEEMwonen, IBA, UIA | Evaluationsbericht | unbekannt | — | — | technische/finanzielle/prozessuale Evaluation | — | Übertragbarkeit | Erkenntnisse für zirkuläre Wohnungen | SUPERLOCAL |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Reuse-Anteil | 95 | % | Projektangabe | Expogebouw | SUPERLOCAL | belegt |
| Reuse-Anteil alternative Quelle | 100 | % | Projektangabe | „Material harvested from demolition of four gallery flats“ | Maurer United | teilweise belegt; Quellenkonflikt |
| Fertigstellung/Lieferung | 22.02.2018 | Datum | Projektangabe | Expogebouw | SUPERLOCAL | belegt |
| Große Betonunits | 3 | Stück | Projektangabe | Grundstruktur | SUPERLOCAL | belegt |
| Gewicht Betonunits | ca. 45 / ca. 40 | t je Element | Projektmeldungen | Großbauteile | SUPERLOCAL | teilweise belegt; Quellenkonflikt |
| Kranhöhe | 52 | m | Projektangabe | Ausbau/Heben | SUPERLOCAL | belegt |
| Donor-Alter | ca. 50 | Jahre | Projektangabe | Hochhausflat | SUPERLOCAL | belegt |
| CO₂-Einsparung | unbekannt | kg CO₂e | — | Expogebouw | — | unklar |
| Kosten | unbekannt | EUR | unabhängige Evaluation erwähnt, Werte nicht öffentlich in Recherche | Expogebouw | — | unklar |
| Bauzeit | unbekannt | — | — | Expogebouw | — | unklar |
| Transportdistanz | lokal, genaue km unbekannt | km | — | Projektgebiet | SUPERLOCAL | teilweise belegt |
| Materialdatenmodell | Track-and-trace, STABU-/QR-Code, Materialpass | — | Tool im Gesamtprojekt | Gesamtprojekt | SUPERLOCAL | belegt, spezifische Anwendung auf Expogebouw unklar |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** lokale Bauteilernte aus Donorhochhaus durch Rückbauunternehmen Dusseldorp; kein klassischer Produktkauf.  
- **Bauteilbörse / Quelle:** keine externe Bauteilbörse; Quelle war die Hochhausflat an der Ursulastraat und weiteres Material aus dem Projektgebiet.  
- **Kostenwirkung:** unbekannt; ein unabhängiges Bauadviesbureau prüfte finanzielle, wirtschaftliche und gesellschaftliche Machbarkeit, aber konkrete Kostenwerte wurden in den gefundenen Quellen nicht veröffentlicht.  
- **Zeitwirkung:** Logistik und Verfügbarkeit der Bauteile waren unerwartet große Herausforderungen.  
- **Versicherung / Haftung:** unbekannt.  
- **Gewährleistung:** unbekannt.  
- **Arbeitsaufwand:** hoch gegenüber Regelbau, weil Rückbau, Ernte, Prüfung, Transport und Entwurfsanpassung zusammenfallen.  
- **Lagerung:** Materialien im Gesamtprojekt in Containern/Depots gelagert; konkrete Lagerdauer Expogebouw unbekannt.  
- **Marktbarrieren:** Qualität, Schadstoffe, Timing, fehlende Standardprozesse, Bauordnungs-/Nachweisfragen.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** konkrete Normen, detaillierte Prüfprotokolle, genaue Kosten, CO₂-Bilanz Expogebouw, exakte Bauteilmaße, bauteilweise Massen, Genehmigungsdokumente, Versicherungs-/Gewährleistungsmodell.  
- **Sinnvolle neue Entitäten:** Bauteil-Ernte; Donor-/Empfängerquartier; Quellenkonflikt Kennwert; Materialpass.  
- **Fehlende Daten:** Flächen, U-Werte, Bewehrungsdaten, Anschlussdetails, Schadstoffbericht, technische Zeichnungen, Evaluationsergebnisse mit Zahlen.  
- **Zu prüfende Quellen:** Evaluatierapport Eerste Fase; UIA-Dokumente; Volantis-/Dusseldorp-Projektdaten; kommunale Genehmigungsunterlagen.

## QUELLEN UND LINKS

1. SUPERLOCAL: Expogebouw. https://www.superlocal.eu/superlocal/expogebouw/  
2. Maurer United: Superlocal Pavilion. https://maurerunited.com/projecten/superlocal-pavilion/  
3. Maurer United Deutsch: Superlocal Pavilion. https://maurerunited.com/de/projecten/superlocal-pavilion/  
4. SUPERLOCAL: Update realisatie expogebouw. https://www.superlocal.eu/update-realisatie-expogebouw-superlocal/  
5. Gemeinde Kerkrade: SUPERLOCAL. https://www.kerkrade.nl/superlocal  
6. SUPERLOCAL: Track and trace materialen SUPERLOCAL flat. https://www.superlocal.eu/track-and-trace-materialen-superlocal-flat/  
7. Jongen: SUPERLOCAL. https://www.jongen.com/nl/sterk-ons-werk/superlocal
