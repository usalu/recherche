---
id: "BedZED_London_Hackbridge"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "BedZED, London / Hackbridge — Fallstudie Direct Reuse / Bauteilwiederverwendung"
bauobjekt:
  - "BedZED_London_Hackbridge"
legacy_paths:
  - "Gebäude\\BedZED_London_Hackbridge.md"
projekt:
  - "BedZED_London_Hackbridge"
reuse_chain_detected: "True"
---
# BedZED, London / Hackbridge — Fallstudie Direct Reuse / Bauteilwiederverwendung

## Migration

- Fallstudie ID: BedZED_London_Hackbridge
- Legacy source count: 1
- Generated project: BedZED_London_Hackbridge
- Generated bauobjekt: BedZED_London_Hackbridge
- Extracted reuse_einsatz rows: 12
- Extracted datenpunkt rows: 15
- Extracted entity mapping rows: 22
- Reuse chain detected: True

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

---

## 1. EINORDNUNG

- **Entscheidung:** HAUPTFALL
- **Bewertung:** ★★★★★
- **Begründung:** BedZED ist ein früher gebauter Referenzfall für tragende Wiederverwendung: 98 t wiederverwendeter Baustahl, ca. 95 % des tragenden Stahls des Projekts, wurden vor allem in den Stahlrahmen der Arbeits-/Gewerbeflächen eingesetzt. Zusätzlich sind wiederverwendete Holzständer, Türen, Bordsteine, Natursteinplatten und weitere feste Bauteile dokumentiert. Gewertet wird primär die tragende Stahlwiederverwendung, nicht der allgemeine Ökoquartier-Anspruch.
- **Vertrauensgrad:** belegt
- **Warnung Bestandserhalt:** nein
- **Warnung Möbel/Dekoration:** nein; dekorative oder lose Elemente sind nicht bewertungsrelevant.
- **Projektstatus:** gebaut

---

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

---

## 3. FALLSTUDIE

- **Name:** BedZED / Beddington Zero Energy Development
- **Ort:** Hackbridge / Wallington, London Borough of Sutton, UK
- **Gebäude:** Gemischt genutztes Quartier mit Wohnungen, Arbeits-/Gewerbeflächen und Gemeinschaftseinrichtungen
- **Projekt:** Neubau eines Nullenergie-/Ökoquartiers mit Direct Reuse einzelner Bauteile
- **Beteiligte People / Akteure:** Peabody Trust, Bill Dunster / ZEDfactory bzw. Bill Dunster Architects, BioRegional, Arup, Ellis & Moore Consulting Engineers, Gardiner & Theobald
- **Architekt:** Bill Dunster / ZEDfactory bzw. Bill Dunster Architects
- **Tragwerksplaner:** Ellis & Moore Consulting Engineers
- **Bauherr:** Peabody Trust
- **Zeitraum:** gebaut 2000–2002; Eröffnung/Nutzung ab 2002
- **Ursprüngliche Nutzung:** Brownfield / ehemals für Klärschlamm bzw. sewage works genutzt; genaue Vornutzung der Bauteilquellen: lokale Abbruch-/Refurbishment-Standorte, u. a. Brighton Railway Station für Stahl laut BioRegional
- **Neue Nutzung:** Wohnen, Arbeiten, Gemeinschaftsnutzung
- **Fläche / Maßstab:** 82 Wohnungen; Arbeitsflächenangaben uneinheitlich: 1.405 m² bis 2.500 m² je Quelle; Maßstab Quartier / gemischt genutzt
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** gut für Stahl, Materialmengen, Kosten-/Prozesshinweise; mittel für genaue Einbaupositionen einzelner Nebenbauteile; Norm-/Genehmigungsdetails unbekannt

---

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; Materialwiederverwendung/Recycling zusätzlich vorhanden
- **Hauptniveau:** Tragwerk, räumlicher Innenausbau, Hülle/Innenbauteile
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die 98 t Stahlprofile wurden aus anderen Rückbauquellen entnommen, geprüft, aufbereitet und als tragende Bauteile neu eingebaut. Das ist Direct Reuse. Recycelte Zuschläge, Glasgranulat oder Recyclingkunststoffe zählen nur als Materialrecycling und nicht als Direct Reuse im engeren Sinn.
- **Warum ist der Fall relevant?** Sehr früher, dokumentierter, gebauter Fall mit belastbaren Mengen-, Kosten-, Prüf- und Beschaffungsinformationen für tragende Stahlwiederverwendung.

---

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Stahlrahmen / Stahlprofile | Stahl | Lokale Abbruchstandorte im 35-mile-Radius; teilweise Brighton Railway Station | Tragende Stahlbauteile in früheren Gebäuden | Tragende Stahlrahmen, v. a. Workspaces | 98 t; 95 % des tragenden Stahls | ja | nein | nein | nein | Sandstrahlen, Fertigung, Lackierung, zinkreiche Beschichtung | Anschlussdetails für Profilvarianten | Sichtprüfung; Herstellungsdatum; Rost/Scaling; vorhandene Verbindungen; Fabrikationseignung | Tragfähigkeit als Stahlrahmen | Historic Sections Book; sonst unbekannt | Profilverfügbarkeit; gebogene Profile nicht verfügbar/akzeptiert | S4, S2 | genaue Profiltypen, alte Gebäude je Profil |
| Curved steel sections | Stahl | geplant als wiederverwendet, tatsächlich neu | unbekannt | gebogene Stahlteile | unbekannt | ja | nein | nein | nein | neu statt wiederverwendet | unbekannt | unbekannt | Biegbarkeit | unbekannt | Biegebetrieb wollte reclaimed steel nicht biegen; Zeitdruck | S4 | Umfang |
| Holzständer / Wandständer | Nadelholz | lokale Rückbau-/Reclaim-Quellen | unbekannt | Unterkonstruktion für Gipskartonwände | 54 km laut BAZED | teilweise / nicht primär | ja | nein | nein | Instandsetzung, Behandlung, Zuschneiden in Sägewerk | Schrauben/Nägel unbekannt | unbekannt | Wand-/Innenausbauleistung | unbekannt | Aufbereitung und Zuschnitt nötig | S5 | genaue Holzqualitäten |
| Türen | Holz/Metall/Glas unbekannt | wiederverwendet, Quelle unbekannt | Tür | Tür | unbekannt | nein | ja | teilweise | nein | unbekannt | Beschläge unbekannt | unbekannt | Nutzbarkeit/Brandschutz unbekannt | unbekannt | Programm-/Lieferkettenprobleme bei reclaimed doors | S5, S3 | Menge, Brandschutz |
| Gerüstrohre als Rampen/Geländer/Balustraden | Stahl | Gerüstmaterial | Gerüstrohr | Geländer/Balustrade | unbekannt | nein | ja | nein | nein | unbekannt | unbekannt | unbekannt | Absturzsicherung | unbekannt | unbekannt | S5 | Details |
| Bordsteine | Stein/Beton | wiederverwendet | Straßen-/Außenraumkante | Außenraumkante | unbekannt | nein | ja | nein | nein | unbekannt | unbekannt | unbekannt | Außenraumtauglichkeit | unbekannt | unbekannt | S5 | Details |
| Natursteinplatten / paving slabs | Stein | wiederverwendet geplant/teilweise unklar | Bodenbelag | Boden-/Außenbelag | unbekannt | nein | ja | nein | nein | unbekannt | unbekannt | unbekannt | Rutschfestigkeit/Frost unbekannt | unbekannt | Reclaimed paving slabs funktionierten nicht vollständig im Programm | S3, S5 | tatsächlicher Einbauumfang |
| Recycling-Glas-Sand unter Pflaster | Glasgranulat | recycelt | Glas | Unterbau | 1.000 t laut BedZED Story | nein | nein | nein | nein | Recycling, Körnung | lose Schüttung | unbekannt | Unterbau | unbekannt | zählt als Recycling, nicht Direct Reuse | S7 | technische Kennwerte |
| Feste Einbauten/Küchenteile | Recyclingkunststoff, unbekannt | recycelt | unbekannt | Küchenfronten/Arbeitsplatten | unbekannt | nein | ja | nein | nein | Recyclingprodukt | unbekannt | unbekannt | Innenausbau | unbekannt | zählt eher Recycling als Direct Reuse | S5 | Menge |
| Dämmung | unbekannt | unbekannt | unbekannt | Dämmung | unbekannt | nein | nein | ja | nein | unbekannt | unbekannt | unbekannt | Wärmeschutz | unbekannt | unbekannt | - | alles |
| Sanitär | unbekannt | unbekannt | unbekannt | Sanitär | unbekannt | nein | ja | nein | ja | unbekannt | unbekannt | unbekannt | Hygiene | unbekannt | unbekannt | - | alles |
| Beleuchtung | unbekannt | unbekannt | unbekannt | Beleuchtung | unbekannt | nein | ja | nein | ja | unbekannt | unbekannt | unbekannt | Elektrosicherheit | unbekannt | unbekannt | - | alles |

---

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

---

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Stahlrahmen in Workspaces mit 98 t reclaimed steel | Tragfähigkeit, Stabilität | Historic Sections Book; sonst unbekannt | Sichtprüfung und Bemessung | unterschiedliche Profile | Spezifikation mehrerer zulässiger Querschnitte | S4 |
| Lastabtragung | Reused steel hauptsächlich in Stahlrahmen der Arbeitsbereiche | unbekannt | unbekannt | Tragwerksplanung | Materialhistorie | zulässige Spannungen historischer Profile ermittelt | S4 |
| Verbindung | Anschlüsse auf unterschiedliche Querschnitte ausgelegt | Montierbarkeit, Tragfähigkeit | unbekannt | unbekannt | verfügbare Profile nicht exakt planbar | flexible Anschlussdetails | S4 |
| Brandschutz | unbekannt | Brandschutzanforderungen UK | unbekannt | unbekannt | unbekannt | unbekannt | - |
| Schallschutz | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | - |
| Feuchte | Stahlkorrosion/Scaling visuell geprüft | Korrosionsschutz | unbekannt | Sichtprüfung | Rost/Scaling möglich | Sandstrahlen und zinkreiche Beschichtung | S4 |
| Wärmeschutz | Superisolierte Gebäudehülle, aber Direct-Reuse-Detail unbekannt | Energieperformance | unbekannt | unbekannt | unbekannt | unbekannt | S1 |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | - |
| Luftdichtheit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | - |
| TGA-Integration | On-site Wasser-/CHP-Systeme im Gesamtprojekt; keine Direct-Reuse-Information | Betrieb | unbekannt | unbekannt | Nicht Bestandteil Direct Reuse | unbekannt | S1 |
| Barrierefreiheit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | - |
| Dauerhaftigkeit | Reclaimed steel in gutem Zustand; zusätzliche Beschichtung | Langzeittragfähigkeit | unbekannt | Sichtprüfung | unbekannte Vorgeschichte | Prüfung + Aufbereitung | S4 |
| Wartung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | - |
| Zulassung | Verantwortung geteilt zwischen Client und Engineer | Nachweisführung | UK-Baurecht unbekannt | Engineer übernimmt Strukturintegritätsrisiko | Verantwortungszuordnung | free-issue Material mit definierter Risikoverteilung | S4 |
| Haftung | Construction Manager kauft im Auftrag des Clients; Engineer trägt Integritätsrisiko | Gewährleistung/Haftung | unbekannt | visuelle Prüfung | Risiko beim Client wie bei free-issue | Rollenklärung | S4 |

---

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

---

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Passende Stahlprofile schwer verfügbar | logistisch/technisch | Reclamation yards haben geringe Mengen guter Strukturprofile | Sourcing-Risiko und Zeitbedarf | Bauteil, Logistik, Tragwerkssystem | flexible Querschnittslisten, lange Vorlaufzeiten | Reuse früh in Entwurf integrieren | S4 |
| Qualitätsnachweis historischer Profile | technisch/rechtlich | unbekannte Materialgeschichte | Engineer muss Risiko tragen | Prüfung, Recht, Norm | Sichtprüfung, Historic Sections Book, konservative Bemessung | Rollen und Nachweise vor Ausschreibung definieren | S4 |
| Zusatzaufbereitung | technisch/wirtschaftlich | Korrosion/alte Beschichtungen | zusätzlicher Werkstattaufwand | Aufbereitungsmethode, Wirtschaft | Sandstrahlen, Beschichtung | Reuse spart Material, braucht aber Bearbeitungsbudget | S4 |
| Gebogene Profile nicht wiederverwendet | technisch/logistisch | lokaler Biegebetrieb akzeptierte reclaimed steel nicht | Neumaterial für curved sections | Bauteil, Hürde | Neuer Stahl wegen Zeitdruck | Lieferkette muss Reuse akzeptieren und testen | S4 |
| Komplexe Lieferketten bei Türen/Pflaster | logistisch | nicht off-the-shelf | Programmrisiko | Bauteil, Logistik | teilweise nicht umgesetzt | Bauteile mit kritischem Programm früh sichern | S3 |
| Lagerfläche nötig | logistisch/wirtschaftlich | Material wird vor Bedarf gefunden | zusätzlicher Platzbedarf | Logistik, Wirtschaft | Lagerung einplanen | Direct Reuse braucht Pufferfläche | S3 |
| Reuse vs Recycling unscharf | methodisch | Projekt nutzt beides | Bewertungsrisiko | Reuse-Strategie, Kennwert | Direct-Reuse-Bauteile separat inventarisieren | Nur Bauteile zählen, nicht allgemeines Recycling | eigene Auswertung nach S3/S4 |

---

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

---

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** Stahl in Workspaces wahrscheinlich baulich relevant, Sichtbarkeit im Detail unbekannt; BedZED wird stärker als Ökoquartier denn als Reuse-Ästhetik wahrgenommen.
- **räumliche Transformation:** Wiederverwendeter Stahl ermöglicht Arbeits-/Gewerberahmen innerhalb eines gemischt genutzten Quartiers.
- **Atmosphäre / Ausdruck:** markante Low-energy-Architektur; Reuse ist Teil des Materialkonzepts, nicht alleiniger Ausdrucksträger.
- **Umgang mit Spuren:** unbekannt; Stahl wurde sandgestrahlt und beschichtet, also Spuren vermutlich reduziert.
- **sozialer Wert:** gemischt genutztes Quartier mit Wohnen/Arbeiten und nachhaltigem Lebensstil; sozialer Reuse-Wert indirekt.
- **Denkmal- oder Bestandswert:** unbekannt
- **Kritik / Grenzen:** Viele Kennwerte beziehen sich auf Recycling und lokale Beschaffung; die Bewertung darf nicht durch Energie-/Mobilitätsstrategien oder Recycling aufgebläht werden.

---

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** konkrete Normnummern, genaue Profiltypen, Brandschutz-/Schallschutzdetails, Genehmigungsakten, exakte Einbaupläne, Wartungsdaten, Lebensdauerprognose.
- **Sinnvolle neue Entitäten:** Reclaim-Manager, historische Profilbemessung, free-issue-Material, Rückbauquelle.
- **Fehlende Daten:** genaue Herkunft jedes Stahlprofils, Umfang der Türen/Pflaster/Geländer, Prüfprotokolle, tatsächliche Lagerflächen, Versicherungs-/Gewährleistungsdokumente.
- **Zu prüfende Quellen:** originale BedZED Materials Reports, Ellis & Moore Statikunterlagen, Bauakten London Borough of Sutton, BioRegional Archiv, BRE-Vergleichsstudien.

---

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja

### 5 wichtigste Fakten

1. 98 t wiederverwendeter Baustahl wurden eingebaut.
2. Dieser Stahl entspricht ca. 95 % des tragenden Stahls des Projekts.
3. Der Stahl wurde hauptsächlich in den Stahlrahmen der Workspaces genutzt.
4. Die Stahlwiederverwendung war nach Zusatzaufwand effektiv kostenneutral.
5. Das Projekt dokumentiert frühe Strategien für lokale Beschaffung, flexible Anschlüsse und Qualitätsprüfung.

### 5 wichtigste Bauteile

1. Wiederverwendete Stahlprofile / Stahlrahmen
2. Wiederverwendete Holzständer für Wände
3. Gerüstrohre als feste Geländer/Balustraden
4. Wiederverwendete Türen / Innenbauteile
5. Wiederverwendete Bordsteine/Natursteinplatten, soweit tatsächlich eingebaut

### 5 wichtigste Hürden

1. Verfügbarkeit passender Stahlprofile
2. Nachweis der Materialqualität
3. Zusatzaufbereitung und Korrosionsschutz
4. Akzeptanz der Verarbeiter, z. B. beim Biegen
5. Programmrisiko und Lager-/Lieferkettenkoordination

### 5 wichtigste übertragbare Erkenntnisse

1. Tragende Stahlwiederverwendung ist machbar, wenn Profile früh flexibel spezifiziert werden.
2. Anschlüsse sollten Varianz in Querschnitt und Länge aufnehmen können.
3. Prüf- und Haftungsrollen müssen vor Beschaffung geklärt sein.
4. Direct Reuse braucht Zeit- und Lagerpuffer.
5. Reuse-Kennwerte müssen von Recycling- und Ökoquartierkennwerten getrennt ausgewiesen werden.

### 5 offene Fragen

1. Welche exakten Stahlprofile wurden aus welchen Donor-Bauten übernommen?
2. Welche Brandschutz- und Schallschutzprüfungen waren für wiederverwendete Bauteile erforderlich?
3. Welche Türen, Platten und Geländer wurden tatsächlich eingebaut und in welchem Umfang?
4. Wie wurde die Gewährleistung zwischen Client, Engineer und Contractor vertraglich geregelt?
5. Welche Langzeiterfahrungen liegen nach über 20 Jahren Betrieb vor?

---

## Quellen und Links

- **S1 – ZEDfactory: BedZED.** https://www.zedfactory.com/bedzed
- **S2 – BioRegional: BedZED case study.** https://www.bioregional.com/projects-and-services/case-studies/bedzed-the-uks-first-large-scale-eco-village
- **S3 – BioRegional: Using sustainable building materials – lessons from BedZED.** https://www.bioregional.com/resources/using-sustainable-building-materials-lessons-from-bedzed
- **S4 – BioRegional: BedZED Toolkit Part I / Materials Report PDF.** https://www.bioregional.com/uploads/downloads/BedZED-Toolkit-Part-I_Bioregional_2002_sustainable-building-materials.pdf
- **S5 – BAZED: BedZED project sheet.** https://www.bazed.fr/projet-exemplaire/bedzed-2
- **S6 – Structurae: BedZED.** https://structurae.net/en/structures/bedzed
- **S7 – BioRegional: The BedZED Story PDF.** https://www.bioregional.com/uploads/downloads/The-BedZED-Story_Bioregional_2017.pdf
