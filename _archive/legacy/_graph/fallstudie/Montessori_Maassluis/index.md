---
id: "Montessori_Maassluis"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "Montessori Maassluis — Fallstudie Direct Reuse / zirkuläres Bauen"
bauobjekt:
  - "Montessori_Maassluis"
legacy_paths:
  - "Gebäude\\Montessori_Maassluis.md"
projekt:
  - "Montessori_Maassluis"
reuse_chain_detected: "True"
---
# Montessori Maassluis — Fallstudie Direct Reuse / zirkuläres Bauen

## Migration

- Fallstudie ID: Montessori_Maassluis
- Legacy source count: 1
- Generated project: Montessori_Maassluis
- Generated bauobjekt: Montessori_Maassluis
- Extracted reuse_einsatz rows: 8
- Extracted datenpunkt rows: 14
- Extracted entity mapping rows: 27
- Reuse chain detected: True

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

---

## 1. EINORDNUNG

- **Entscheidung:** ANHANG / WATCHLIST, nach Fertigstellung erneut prüfen
- **Bewertung:** ★★☆☆☆ aktuell; potenziell ★★★★☆ nach belegtem Einbau der wiederverwendeten Hohlkörperdecken
- **Begründung:** Die offiziellen Kraaijvanger-Quellen nennen eine Hybridkonstruktion aus Holzstützen und wiederverwendeten Hohlkörperdecken, die große flexible Klassenräume ermöglicht. Gleichzeitig wurde der Bauvertrag erst im Februar 2026 unterzeichnet, die Fertigstellung ist für Ende 2026 und die Nutzung für Anfang 2027 angekündigt. Damit ist der Direct-Reuse-Einbau zum Stand Mai 2026 noch nicht als gebaut/as-built belegbar.
- **Vertrauensgrad:** teilweise belegt
- **Warnung Bestandserhalt:** nein — Ersatzneubau am bestehenden Schulstandort; der Bestand zählt nicht.
- **Warnung Möbel/Dekoration:** nein — relevante Information betrifft tragende Hohlkörperdecken, nicht Möbel.
- **Projektstatus:** im Bau / geplant; Fertigstellung geplant Ende 2026, Nutzung Anfang 2027

---

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

---

## 3. FALLSTUDIE

- **Name:** Montessori Maassluis / Montessorischool Maassluis
- **Ort:** Maassluis, Niederlande; bestehende Schule laut Schulwebsite Seringenstraat 110, 3142 NX Maassluis; ob gleiche Adresse für Ersatzneubau exakt gilt: teilweise belegt
- **Gebäude:** Schulneubau / Ersatzneubau
- **Projekt:** Neubau einer Montessori-Grundschule mit 10 Unterrichtsgruppen und BSO
- **Beteiligte People / Akteure:** Kraaijvanger Architects; Stichting Montessorischolen Monton; Anculus B.V.; A. de Jong Groep; Vintis installatieadviseurs; VIA Landscape; IMd Raadgevende Ingenieurs; Van Dijk Maasland B.V.; weitere unbekannt
- **Architekt:** Kraaijvanger Architects
- **Tragwerksplaner:** IMd Raadgevende Ingenieurs im Designteam genannt; genaue Vertragsrolle unbekannt
- **Bauherr:** Stichting Montessorischolen Monton / Stichting Montessorischolen Midden-Nederland (Monton) und Anculus B.V. laut Kraaijvanger; genaue Bauherrschaftsstruktur unbekannt
- **Zeitraum:** Design 2024; Bauvertrag unterschrieben 02.02.2026; Fertigstellung geplant Ende 2026; Nutzung geplant Anfang 2027
- **Ursprüngliche Nutzung:** bestehende Schule am Standort; Donor-Nutzung der Hohlkörperdecken unbekannt
- **Neue Nutzung:** Montessori-Schule mit Unterricht, Lernplätzen, Patio, BSO
- **Fläche / Maßstab:** ca. 1.508 m² BVO laut News; 1.534 m² GFA laut Projektseite
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** gut für Entwurf, Akteure, Status und Zeitplan; schwach für Herkunft, Menge, Prüfung, Normen, Kosten und Einbau der reused slabs

---

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** geplant/angekündigt; partiell; ex-situ; Bauteilwiederverwendung; strukturelle Wiederverwendung von Hohlkörperdecken
- **Hauptniveau:** Tragwerk
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Der Ersatzneubau selbst ist keine Sanierung. Bewertbar wäre nur der tatsächliche Einbau wiederverwendeter Hohlkörperdecken. Neue Holzstützen, flexible Grundrisse, vorbereitete Erweiterbarkeit und 50-Jahre-Ziel zählen nicht als Direct Reuse, sondern als Neubau-/Anpassungsstrategie.
- **Warum ist der Fall relevant?** Wenn der Einbau as-built bestätigt wird, wäre das Projekt ein aktueller Schulbau mit tragender Wiederverwendung von Betonfertigteilen — besonders relevant, weil Schulbauten hohe Anforderungen an Tragwerk, Schall, Brandschutz und Nutzungssicherheit haben.

---

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Hohlkörperdecken / hollow core slabs | Beton/Spannbeton vermutlich | unbekannt | Decken-/Bodenplatten in Donor-Gebäude unbekannt | tragende Decken im Schulneubau | unbekannt | ja | ja | nein | nein | unbekannt | unbekannt | unbekannt | Tragfähigkeit, Gebrauchstauglichkeit, Brandschutz, Schall, Durchbiegung | unbekannt | Herkunft, Qualität, Anschlussdetails | Kraaijvanger project page | Materialdaten, Menge, Donor |
| Holzstützen | Holz | neu/unbekannt | nicht anwendbar | Tragwerk | unbekannt | ja | ja | nein | nein | neu | unbekannt | unbekannt | Tragfähigkeit, Brandschutz | unbekannt | nicht Direct Reuse | Kraaijvanger | Menge |
| Dach mit vorbereitetem Ausbau/Gemüsegarten | unbekannt | neu/unbekannt | nicht anwendbar | Dach/Erweiterbarkeit | unbekannt | ja/teilweise | ja | ja | nein | neu | unbekannt | unbekannt | Tragfähigkeit für Erweiterung und Garten | unbekannt | nicht Direct Reuse | Kraaijvanger | System |
| Sonnenschutz / awnings | unbekannt | neu/unbekannt | nicht anwendbar | Sonnenschutz | unbekannt | nein | nein | Hülle | nein | unbekannt | unbekannt | unbekannt | Sonnenschutz, Komfort | unbekannt | nicht Reuse belegt | Kraaijvanger | Material |
| Fassade/Fenster | unbekannt | unbekannt | unbekannt | Hülle | unbekannt | nein | ja | ja | nein | unbekannt | unbekannt | unbekannt | Tageslicht, Wärmeschutz | unbekannt | keine Reuse-Angabe | Kraaijvanger | Details |
| Innenwände/Lernplätze | unbekannt | unbekannt | unbekannt | flexible Räume | unbekannt | nein | ja | nein | nein | unbekannt | unbekannt | unbekannt | Akustik, Nutzung | unbekannt | keine Reuse-Angabe | Kraaijvanger | Material |
| TGA | unbekannt | unbekannt | unbekannt | Schulbetrieb | unbekannt | nein | nein | nein | ja | unbekannt | unbekannt | unbekannt | Lüftung/Heizung/Komfort | unbekannt | keine Reuse-Angabe | Kraaijvanger | Details |
| Sanitär | unbekannt | unbekannt | unbekannt | Schulbetrieb | unbekannt | nein | nein | nein | ja | unbekannt | unbekannt | unbekannt | Hygiene/Barrierefreiheit | unbekannt | keine Reuse-Angabe | unbekannt | alles |

---

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

---

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Hybrid aus Holzstützen und wiederverwendeten Hohlkörperdecken | Tragfähigkeit, große flexible Klassenräume | unbekannt | unbekannt | gebrauchte Decken in Neubau | Hybridkonstruktion | Kraaijvanger |
| Lastabtragung | Hohlkörperdecken spannen vermutlich zwischen Holz-/Tragachsen; Details unbekannt | Lasten aus Schulnutzung | unbekannt | unbekannt | Anschluss Holz-Beton | unbekannt | Kraaijvanger |
| Verbindung | unbekannt | sichere Auflager/Verbindungen | unbekannt | unbekannt | alte Hohlkörperplattenanschlüsse | unbekannt | unbekannt |
| Brandschutz | Schulbau + Hohlkörperdecken/Holzstützen | Brandschutz/Rettung | unbekannt | unbekannt | Holz + reused Beton | unbekannt | unbekannt |
| Schallschutz | Schule/Lernräume | Akustik, Trittschall | unbekannt | unbekannt | Hohlkörperdecken aus anderem Kontext | unbekannt | unbekannt |
| Feuchte | unbekannt | Feuchteschutz | unbekannt | unbekannt | Betonfertigteile + Neubauanschlüsse | unbekannt | unbekannt |
| Wärmeschutz | Gebäude ökologisch/kosteneffizient genannt | Energie/Komfort | unbekannt | unbekannt | nicht Reuse-spezifisch | Sonnenschutz, Tageslicht, natürliche Lüftung | Kraaijvanger |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | Anschluss Decken/Fassade | unbekannt | unbekannt |
| Luftdichtheit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| TGA-Integration | natürliche Lüftung erwähnt; TGA-Details unbekannt | Komfort, Luftqualität | unbekannt | unbekannt | Schule | unbekannt | Kraaijvanger |
| Barrierefreiheit | unbekannt | Schulbau | unbekannt | unbekannt | zweigeschossig | unbekannt | unbekannt |
| Dauerhaftigkeit | auf mindestens 50 Jahre ausgelegt | Lebensdauer | unbekannt | unbekannt | alte Decken + Neubau | robuste, wartungsarme Konstruktion | Kraaijvanger |
| Wartung | robust/low-maintenance genannt | geringe Wartung | unbekannt | unbekannt | unbekannt | Materialwahl | Kraaijvanger |
| Zulassung | unbekannt | Bauzulassung reused structural concrete | unbekannt | unbekannt | keine as-built Details | unbekannt | unbekannt |
| Haftung | unbekannt | Verantwortlichkeit für reused slabs | unbekannt | unbekannt | Gewährleistung | unbekannt | unbekannt |

---

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

---

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| As-built nicht belegt | Daten/Projektstatus | Fertigstellung erst Ende 2026 geplant | keine endgültige Hauptfallwertung | Fallstudie, Bauteil | nach Fertigstellung prüfen | geplante Reuse-Fälle separat führen | Kraaijvanger news |
| Herkunft der Hohlkörperdecken unbekannt | logistisch/Daten | Donor Building nicht öffentlich genannt | fehlende Nachvollziehbarkeit | Donor Building, Bauteil | Donor-Dokumentation anfordern | Herkunft ist Kerninformation | unbekannt |
| Prüfung reused structural concrete | technisch/rechtlich | Hohlkörperdecken aus anderem Bauwerk | Tragfähigkeits-/Brandschutz-/Schallschutznachweise nötig | Prüfung, Recht, Leistungsanforderung | unbekannt | Prüfprotokolle vor Bewertung prüfen | unbekannt |
| Anschluss Holzstützen + Betonfertigteile | technisch | Hybridkonstruktion | Detailplanung erforderlich | Verbindung, Tragwerkssystem | unbekannt | Hybrid-Reuse braucht Anschlussstandard | Kraaijvanger |
| Schulbauanforderungen | technisch/rechtlich | Kinder, Brandschutz, Akustik, Barrierefreiheit | höhere Nachweisanforderungen | Leistungsanforderung, Recht | unbekannt | öffentliche Gebäude erhöhen Nachweislast | unbekannt |
| Quellenabweichung Fläche | Daten | 1.508 m² BVO vs. 1.534 m² GFA | Kennwert unscharf | Kennwert | beide Werte getrennt führen | Bilanzgrenze immer angeben | Kraaijvanger |

---

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

---

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** unbekannt; Kraaijvanger beschreibt die hybride Konstruktion, aber nicht, ob Hohlkörperdecken sichtbar bleiben.
- **räumliche Transformation:** Ersatzneubau als „mini-society“ mit Dorfplatz, grünem Patio, flexiblen Klassen und Lernplätzen.
- **Atmosphäre / Ausdruck:** ruhig, hell, grün, pädagogisch auf Montessori-Lernen ausgerichtet.
- **Umgang mit Spuren:** unbekannt; keine Angaben zu sichtbaren Gebrauchsspuren der Decken.
- **sozialer Wert:** Schulneubau für 10 Gruppen und BSO; Bildungsinfrastruktur.
- **Denkmal- oder Bestandswert:** unbekannt; bestehende Schule wird ersetzt, nicht als Denkmalfall belegt.
- **Kritik / Grenzen:** Stand Mai 2026 kein gebauter Direct-Reuse-Nachweis; viele technische Daten fehlen.

---

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** Donor Building, Anzahl/Masse der Hohlkörperdecken, Materialgüte, Prüfprotokolle, Normen, CO₂, Kosten, Bauablauf, Lagerung, Versicherungsmodell.
- **Sinnvolle neue Entitäten:** Geplanter Reuse-Einbau; Donor Building unbekannt; As-built-Verifikation.
- **Fehlende Daten:** Herkunft, Menge, Einbauorte, Anschlussdetails, Lastannahmen, Brandschutz-/Schallnachweise.
- **Zu prüfende Quellen:** Bau-/Werkpläne, Tragwerksbericht IMd, Bauteilpass, Ausschreibung, Baustellenfotos 2026, Abnahme-/As-built-Unterlagen Ende 2026/Anfang 2027.

---

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** derzeit **Anhang/Watchlist**; nach belegter Fertigstellung und eingebauten reused hollow core slabs erneut prüfen.
- **5 wichtigste Fakten:**
  1. Neubauvertrag wurde am 02.02.2026 unterzeichnet.
  2. Fertigstellung ist für Ende 2026 geplant.
  3. Nutzung ist für Anfang 2027 geplant.
  4. Offizielle Projektseite nennt eine Hybridkonstruktion aus Holzstützen und wiederverwendeten Hohlkörperdecken.
  5. Flächenangaben weichen zwischen ca. 1.508 m² BVO und 1.534 m² GFA ab.
- **5 wichtigste Bauteile:**
  1. geplante wiederverwendete Hohlkörperdecken
  2. Holzstützen
  3. Dach mit Erweiterungsvorbereitung
  4. Sonnenschutz/Awnings
  5. flexible Innenraum-/Lernzonen
- **5 wichtigste Hürden:**
  1. fehlender as-built-Nachweis
  2. unbekannte Herkunft der Hohlkörperdecken
  3. unbekannte Prüfungen
  4. Anschlussdetails Holz-Beton
  5. Schulbauanforderungen an Brandschutz, Schall und Sicherheit
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Im-Bau-Projekte als Watchlist führen, nicht wie gebaute Hauptfälle bewerten.
  2. Tragende Hohlkörperdecken können ein starker Reuse-Fall sein, wenn Herkunft und Einbau belegt sind.
  3. Flächenwerte müssen mit Bilanzgrenze geführt werden.
  4. Schulbauten verlangen besonders belastbare Nachweise.
  5. As-built-Verifikation ist entscheidend für Direct-Reuse-Rankings.
- **5 offene Fragen:**
  1. Von welchem Donor Building stammen die Hohlkörperdecken?
  2. Wie viele Hohlkörperdecken werden eingebaut?
  3. Welche Tragfähigkeits-/Brandschutz-/Schallschutzprüfungen wurden durchgeführt?
  4. Welche CO₂- und Kosteneffekte ergeben sich?
  5. Bleiben die reused slabs sichtbar oder werden sie verkleidet?

---

## Quellen und Links

- Kraaijvanger – Montessori Maassluis project: https://www.kraaijvanger.nl/en/projects/montessori-maassluis
- Kraaijvanger – Construction contract signed: https://www.kraaijvanger.nl/en/news/de-handtekeningen-zijn-gezet-montessorischool-maassluis
- Montessorischool Maassluis – school website: https://www.montessorischoolmaassluis.nl/
- Kraaijvanger – Dutch news page: https://www.kraaijvanger.nl/nl/nieuws/de-handtekeningen-zijn-gezet-montessorischool-maassluis
