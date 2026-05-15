---
entity: "fallstudie"
id: "BedZED_London_Hackbridge"
title: "BedZED, London / Hackbridge — Fallstudie Direct Reuse / Bauteilwiederverwendung"
build_status: "promoted_phase42"
legacy_paths:
  - "Gebäude\\BedZED_London_Hackbridge.md"
node_kind: "core"
bauobjekt:
  - "BedZED_London_Hackbridge"
projekt:
  - "BedZED_London_Hackbridge"
---

# BedZED, London / Hackbridge — Fallstudie Direct Reuse / Bauteilwiederverwendung

## Legacy Content

### Legacy Source: Gebäude\BedZED_London_Hackbridge.md

- Map action: split_into_case_graph
- Primary target: fallstudie/BedZED_London_Hackbridge
- Secondary targets: projekt/BedZED_London_Hackbridge; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# BedZED, London / Hackbridge — Fallstudie Direct Reuse / Bauteilwiederverwendung

**Arbeitsstand:** 2026-05-06  
**Sprache:** Deutsch  
**Grundregel:** Gewertet werden nur wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Lose Möbel/Dekoration werden nicht für die Bewertung herangezogen.

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | BedZED / Beddington Zero Energy Development | Untersuchter Wiederverwendungsfall | S1, S2, S4 | belegt | Gemischt genutztes Ökoquartier |
| Gebäude | Wohn- und Arbeitsquartier | Neubau mit Direct Reuse | S1, S5 | belegt | 82 Wohnungen; Arbeitsflächenangaben variieren |
| Ort | Hackbridge / Wallington, London Borough of Sutton, UK | Standort | S1, S5, S6 | belegt | Quellen nutzen teils Wallington, teils Hackbridge |
| Projekt | Beddington Zero Energy Development | Projektname | S1, S2 | belegt | 2000–2002 gebaut |
| People | Bill Dunster / ZEDfactory; BioRegional; Peabody Trust; Arup; Ellis & Moore; Gardiner & Theobald | Planung, Entwicklung, Beratung | S1, S6 | belegt | Rollen je Quelle unterschiedlich detailliert |
| Bauherr | Peabody Trust | Auftraggeber/Entwickler | S1, S6 | belegt | Partnerschaft mit BioRegional |
| Bauteil | Wiederverwendeter Baustahl | Hauptbauteil der Bewertung | S4 | belegt | 98 t; 95 % des tragenden Stahls |
| Bauteil | Holzständer / softwood walling studs | Feste Innen-/Wandkonstruktion | S3, S5 | belegt | 54 km Hölzer laut BAZED |
| Bauteil | Türen, Bordsteine, Natursteinplatten, Gerüstrohre als Geländer/Balustraden | Feste Raum-/Hüll-/Außenbauteile | S5 | teilweise belegt | Umfang je Bauteil unbekannt |
| Material | Stahl, Holz, Stein, Glas, Recyclingmaterialien | Wiederverwendete/recycelte Materialströme | S2, S3, S4, S5 | belegt | Direkt wiederverwendet und recycelt unterscheiden |
| Reuse-Strategie | Ex-situ Bauteilwiederverwendung | Tragende Stahlprofile aus Rückbauquellen neu eingebaut | S4 | belegt | Kern des Falls |
| Aufbereitungsmethode | Sandstrahlen, Fertigung, Beschichtung mit zinkreicher Beschichtung | Vorbereitung wiederverwendeter Stahlprofile | S4 | belegt | Zusätzliches Sandstrahlen dokumentiert |
| Prüfung | Sichtprüfung, Herstellungsdatum, Zustand, vorhandene Verbindungen, Fabrikationseignung | Qualitätskontrolle Stahl | S4 | belegt | Historische Profile über Historic Sections Book bemessen |
| Verbindung | Anschlussdetails mit Toleranzen für verschiedene Profile | Design für verfügbare Profile | S4 | belegt | Erhöhte Beschaffungsflexibilität |
| Logistik | Beschaffung in 35-mile-Radius; lokale Materialstrategie | Lokale Rückbau-/Reclaim-Quellen | S2, S3, S4 | belegt | Durchschnittliche Bezugsdistanz 66,5 miles laut BioRegional |
| Kennwert | 98 t wiederverwendeter Stahl | Tragender Direct-Reuse-Kennwert | S4 | belegt | Wichtigster Kennwert |
| Kennwert | 3.404 t wiederverwendete/recycelte Materialien, 15 % | Gesamtmaterialkennwert, nicht alles Direct Reuse | S3 | belegt | Enthält recyceltes Material und Unterbau/Füllmaterial |
| Wirtschaft | Reclaimed steel ca. 4 % günstiger; mit Zusatzaufwand effektiv kostenneutral | Kostenwirkung Stahlwiederverwendung | S4 | belegt | £300/t vs £313/t; Zusatzaufwand ca. £1.000 |
| Hürde | Verfügbarkeit passender Profile; lange Vorlaufzeiten; gebogene Profile nicht reused | Prozess- und Fertigungshürden | S4 | belegt | Lokaler Biegebetrieb wollte reclaimed steel nicht biegen |
| Norm | Historic Sections Book | Bemessung historischer Stahlprofile | S4 | belegt | Konkrete Normnummern unbekannt |
| Schadstoff | Rost/Scaling/Materialzustand geprüft | Qualitäts-/Schadensprüfung | S4 | teilweise belegt | Keine konkreten Schadstoffe genannt |
| Software | unbekannt | Keine Software publiziert | - | unbekannt | - |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Reclaim-Manager / Materialbeschaffer | Direct Reuse erforderte aktive Suche, Fristen und Beschaffungskoordination | BioRegional Reclaimed / Construction Manager beschafft Stahl | verbindet Logistik, Bauteilbörse, Wirtschaft |
| Historische Profilbemessung | Wiederverwendeter Stahl hat oft andere historische Profileigenschaften | Historic Sections Book | verbindet Prüfung, Norm, Tragwerkssystem |
| Free-Issue-Material | Wiederverwendete Bauteile wurden vom Construction Manager im Auftrag des Clients beschafft | Client trägt Risiko wie bei free-issue materials | verbindet Recht, Wirtschaft, Haftung |

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; Materialwiederverwendung/Recycling zusätzlich vorhanden
- **Hauptniveau:** Tragwerk, räumlicher Innenausbau, Hülle/Innenbauteile
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die 98 t Stahlprofile wurden aus anderen Rückbauquellen entnommen, geprüft, aufbereitet und als tragende Bauteile neu eingebaut. Das ist Direct Reuse. Recycelte Zuschläge, Glasgranulat oder Recyclingkunststoffe zählen nur als Materialrecycling und nicht als Direct Reuse im engeren Sinn.
- **Warum ist der Fall relevant?** Sehr früher, dokumentierter, gebauter Fall mit belastbaren Mengen-, Kosten-, Prüf- und Beschaffungsinformationen für tragende Stahlwiederverwendung.

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Suche lokaler Materialquellen | BioRegional Reclaimed, Construction Manager, Planungsteam | aktive Quellenrecherche | unbekannt | unbekannt | unbekannt | Sichtprüfung bei Stahl | 35-mile-Zielradius | kein standardisierter Markt | frühe Planung und flexible Spezifikation | S2, S3, S4 |
| Bauteilinventar | Stahlprofile mit variierenden Abmessungen erfassen | Tragwerksplaner, Beschaffer | Profilvarianten statt exakt gleicher Profile | Historic Sections Book | unbekannt | unbekannt | Herstellungsdatum, Zustand, Verbindungen | Reclaim-Quellen statt Lagerware | passende Mengen/Querschnitte selten | Design mit toleranten Anschlussdetails | S4 |
| Schadstoffprüfung | Prüfung von Rost/Scaling/Zustand | Tragwerksplaner | visuelle Kontrolle | unbekannt | unbekannt | unbekannt | ja | vor Bestellung | Materialqualität unklar | Ausschluss ungeeigneter Profile | S4 |
| Rückbau | Gewinnung aus lokalen Abbruchstellen | Rückbauunternehmen unbekannt | sorgfältiger Ausbau ideal | unbekannt | selektiver Rückbau vermutet, nicht belegt | unbekannt | unbekannt | Quelle vor Abriss identifizieren | Reclamation yards haben geringe Mengen | direkt aus Abbruchgebäuden suchen | S4 |
| Ausbau | Stahlprofile demontieren | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Transport | Material zur Werkstatt/Baustelle | Construction Manager, Stahlbauer | lokale Beschaffung | unbekannt | - | - | unbekannt | 35-mile-Ziel; Durchschnitt 66,5 miles für Gesamtmaterial | Verfügbarkeit nicht immer lokal | flexible Quellen und lange Vorlaufzeit | S3, S4 |
| Lagerung | Lagern bis Einbau | Construction Manager | unbekannt | unbekannt | - | - | unbekannt | Lagerfläche nötig | Platzbedarf | lange Vorlaufzeiten/Lager berücksichtigen | S3 |
| Aufbereitung | Sandstrahlen, Fertigen, Beschichten | Stahlbauer | Werkstattaufbereitung | unbekannt | - | Sandstrahlen, zinkreiche Beschichtung, Lack | visuelle Kontrolle | Werkstatt | zusätzlicher Prozessgang | Aufbereitung im Stahlbauvertrag | S4 |
| Planung | Querschnittsvarianten und Anschlüsse planen | Ellis & Moore, Bill Dunster Architects | flexible Spezifikation | Historic Sections Book | - | - | Bemessung zulässiger Spannungen | Beschaffung parallel Planung | Bestand passt nicht 1:1 | Anschlüsse auf Größenbereich ausgelegt | S4 |
| Genehmigung | Baurechtliche Zulassung | unbekannt | unbekannt | unbekannt | - | - | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Wiedereinbau | Stahlrahmen in Workspaces | Stahlbauer, Construction Manager | konventionelle Montage mit reclaimed steel | unbekannt | - | aufbereitete Profile | unbekannt | Lieferung auf Bauprogramm | Zeitdruck bei gebogenen Profilen | für curved sections neuer Stahl | S4 |
| Monitoring | Material-/Umweltwirkung ausgewertet | BioRegional / BRE | embodied impact analysis | unbekannt | - | - | Vergleich neu vs reclaimed | Kennwerte dokumentiert | Systemgrenzen komplex | Toolkit/Report veröffentlicht | S3, S4 |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Wiederverwendeter struktureller Stahl | 98 | t | Materialreport / Fallstudie | Stahltragwerk BedZED | S4 | belegt |
| Anteil reclaimed steel am tragenden Stahl | 95 | % | Materialreport | Tragender Stahl | S4 | belegt |
| Kosten reclaimed steel | 300 | £/t | Kostenvergleich | Stahlbeschaffung | S4 | belegt |
| Vergleichspreis neuer Stahl | 313 | £/t | Kostenvergleich | Stahlbeschaffung | S4 | belegt |
| Zusatzaufwand Sourcing/Prüfung Stahl | ca. 1.000 | £ | Schätzung | Stahlwiederverwendung | S4 | belegt |
| Gesamte wiederverwendete/recycelte Materialien | 3.404 | t | BioRegional Materials Report | Gesamtprojekt; enthält Reuse + Recycling + subgrade fill | S3 | belegt |
| Anteil reclaimed/recycled materials | 15 | % Gewicht | BioRegional Materials Report | Gesamtmaterial | S3 | belegt |
| Baustoffe aus 35-mile-Zielradius | 52 | % Gewicht | BioRegional | Gesamtmaterial | S3 | belegt |
| Durchschnittliche Bezugsdistanz | 66,5 | miles | BioRegional | Gesamtmaterial | S3 | belegt |
| Transportbedingte CO₂-Einsparung durch lokale Beschaffung | 120 | t CO₂ | Vergleich zu Durchschnittsdistanzen | Transport / Materialien | S3 | belegt |
| Wohnungsanzahl | 82 | Stück | Projektbeschreibung | Gesamtprojekt | S5, S6 | belegt |
| Arbeits-/Gewerbefläche | 1.405–2.500 | m² | Quellenvergleich | Gesamtprojekt | S5, S6 | teilweise belegt | Quellen widersprechen sich |
| Lebensdauer | unbekannt | - | - | - | - | unbekannt |
| U-Wert | unbekannt | - | - | - | - | unbekannt |
| Zirkularitätskennwert | unbekannt | - | - | - | - | unbekannt |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** Reclaimed steel wurde durch den Construction Manager im Auftrag des Client beschafft; Stahlbaupaket zunächst auf Basis neuen Stahls ausgeschrieben, dann Preisreduktion bei free-issue reclaimed steel vereinbart.
- **Bauteilbörse / Quelle:** keine klassische Bauteilbörse belegt; lokale Abbruch-/Refurbishment-Quellen und aktive Materialsuche; Brighton Railway Station als wichtige Stahlquelle laut BioRegional.
- **Kostenwirkung:** Reclaimed steel ca. 4 % günstiger als neuer Stahl; mit Zusatzaufwand für Sourcing/Inspektion effektiv kostenneutral.
- **Zeitwirkung:** lange Vorlaufzeiten hilfreich; gebogene Profile wurden wegen Programm-/Lieferkettenrisiko neu ausgeführt.
- **Versicherung / Haftung:** Client trägt free-issue-Material-Risiko; Engineer Ellis & Moore trug Risiko der strukturellen Integrität laut Toolkit.
- **Gewährleistung:** unbekannt
- **Arbeitsaufwand:** zusätzlicher Aufwand für Sourcing, Sichtprüfung, Sandstrahlen, Beschichtung, Koordination.
- **Lagerung:** explizit als hilfreich/notwendig benannt; konkrete Fläche unbekannt.
- **Marktbarrieren:** keine off-the-shelf-Produkte; geringe Lagerbestände passender Strukturprofile; fehlende Bereitschaft einzelner Verarbeiter.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** konkrete Normnummern, genaue Profiltypen, Brandschutz-/Schallschutzdetails, Genehmigungsakten, exakte Einbaupläne, Wartungsdaten, Lebensdauerprognose.
- **Sinnvolle neue Entitäten:** Reclaim-Manager, historische Profilbemessung, free-issue-Material, Rückbauquelle.
- **Fehlende Daten:** genaue Herkunft jedes Stahlprofils, Umfang der Türen/Pflaster/Geländer, Prüfprotokolle, tatsächliche Lagerflächen, Versicherungs-/Gewährleistungsdokumente.
- **Zu prüfende Quellen:** originale BedZED Materials Reports, Ellis & Moore Statikunterlagen, Bauakten London Borough of Sutton, BioRegional Archiv, BRE-Vergleichsstudien.

## Quellen und Links

- **S1 – ZEDfactory: BedZED.** https://www.zedfactory.com/bedzed
- **S2 – BioRegional: BedZED case study.** https://www.bioregional.com/projects-and-services/case-studies/bedzed-the-uks-first-large-scale-eco-village
- **S3 – BioRegional: Using sustainable building materials – lessons from BedZED.** https://www.bioregional.com/resources/using-sustainable-building-materials-lessons-from-bedzed
- **S4 – BioRegional: BedZED Toolkit Part I / Materials Report PDF.** https://www.bioregional.com/uploads/downloads/BedZED-Toolkit-Part-I_Bioregional_2002_sustainable-building-materials.pdf
- **S5 – BAZED: BedZED project sheet.** https://www.bazed.fr/projet-exemplaire/bedzed-2
- **S6 – Structurae: BedZED.** https://structurae.net/en/structures/bedzed
- **S7 – BioRegional: The BedZED Story PDF.** https://www.bioregional.com/uploads/downloads/The-BedZED-Story_Bioregional_2017.pdf
