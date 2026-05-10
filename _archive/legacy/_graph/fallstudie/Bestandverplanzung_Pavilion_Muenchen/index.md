---
id: "Bestandverplanzung_Pavilion_Muenchen"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "Bestandverplanzung Pavilion, München — Fallstudie Direct Reuse / zirkuläres Bauen"
bauobjekt:
  - "Bestandverplanzung_Pavilion_Muenchen"
legacy_paths:
  - "Gebäude\\Bestandverplanzung_Pavilion_Muenchen.md"
projekt:
  - "Bestandverplanzung_Pavilion_Muenchen"
reuse_chain_detected: "True"
---
# Bestandverplanzung Pavilion, München — Fallstudie Direct Reuse / zirkuläres Bauen

## Migration

- Fallstudie ID: Bestandverplanzung_Pavilion_Muenchen
- Legacy source count: 1
- Generated project: Bestandverplanzung_Pavilion_Muenchen
- Generated bauobjekt: Bestandverplanzung_Pavilion_Muenchen
- Extracted reuse_einsatz rows: 6
- Extracted datenpunkt rows: 12
- Extracted entity mapping rows: 12
- Reuse chain detected: True

## Legacy Content

### Legacy Source: Gebäude\Bestandverplanzung_Pavilion_Muenchen.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Bestandverplanzung_Pavilion_Muenchen
- Secondary targets: projekt/Bestandverplanzung_Pavilion_Muenchen; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Bestandverplanzung Pavilion, München — Fallstudie Direct Reuse / zirkuläres Bauen

**Bearbeitungsstand:** 2026-05-06  
**Sprache:** Deutsch  
**Regelprüfung:** Gewertet werden nur wiederverwendete Bau-/Konstruktionselemente. Lose Möbel, reine Denkmal-/Bestandserhaltung und unverifizierte Circularity-Claims werden nicht als Wiederverwendung gezählt.

---

## 1. EINORDNUNG

- **Entscheidung:** ANHANG  
- **Bewertung:** ★★☆☆☆  
- **Begründung:** Der Fall ist als gebauter Klein-/Pavillonfall in der PRECS-Fallstudiendatenbank belegt: Paneele aus drei Bungalows des Münchner Olympischen Dorfes wurden wiederverwendet. Tragende Betonfertigteile sind damit relevant, aber Maßstab, dauerhaftes Nutzungsprogramm, genaue Bauteilanzahl und technische Dokumentation sind öffentlich nur sehr knapp belegbar.  
- **Vertrauensgrad:** teilweise belegt  
- **Warnung Bestandserhalt:** nein  
- **Warnung Möbel/Dekoration:** nein  
- **Projektstatus:** gebaut / Pavillon bzw. kleiner Demonstrator

---

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Bestandverplanzung Pavilion / Bestandverpflanzung? | untersuchter Klein-/Pavillonfall | PRECS/JCP-Datenbank | teilweise belegt | Schreibweise in Quellen uneinheitlich bzw. Listeneintrag „Bestandverplanzung“ |
| Ort | München, Deutschland | Empfänger-/Projektort | PRECS/JCP-Datenbank | belegt | genaue Adresse unbekannt |
| Projekt | Wiederverwendung von Paneelen aus Olympiadorf-Bungalows | Kern des Falls | PRECS/JCP-Datenbank | belegt | drei Bungalows als Quelle |
| Gebäude | Olympisches Dorf / Bungalows | Donor-Bauten | München/Olympiapark-Quellen; PRECS | belegt | Bungalows des ehemaligen Olympischen Dorfes wurden 2007–2010/2011 weitgehend abgebrochen und denkmalgerecht neu aufgebaut |
| Bauteil | Betonfertigteil-Paneele | wiederverwendetes Bauteil | PRECS/JCP-Datenbank | belegt | genaue Bauteiltypen/Anzahl unbekannt |
| Material | Beton / Stahlbetonfertigteile | Material der Bauteile | PRECS/JCP-Datenbank | teilweise belegt | PRECS klassifiziert als „PC“ = precast concrete |
| Reuse-Strategie | ex-situ / Gebäudeversetzung / Bauteilwiederverwendung | Paneele aus Bungalows erneut verwendet | PRECS/JCP-Datenbank | teilweise belegt | kleine/prototypische Anwendung |
| Prozessphase | Rückbau, Transport, Wiedereinbau | notwendige Phasen | aus Reuse-Logik abgeleitet | unklar | Detailablauf unbekannt |
| Prüfung | unbekannt | Bauteilprüfung nicht öffentlich gefunden | — | unklar | keine Prüfprotokolle gefunden |
| Norm | unbekannt | Normen nicht öffentlich gefunden | — | unklar | keine Normnummern erfinden |
| Hürde | geringe Quellenlage | Bewertung erschwert | Recherchebefund | belegt | Hauptlücke des Falls |
| Kennwert | 2008; ca. 36 Jahre Bauteilalter | Jahr und Alter laut PRECS | PRECS/JCP-Datenbank | belegt | genaue Mengen/Massen unbekannt |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Donorgebäude-Serie | Serien-/Systembauten sind bei Fertigteil-Reuse zentral | Olympiadorf-Bungalows / OLY-72-Kontext | verbindet Gebäude, Bauteil, Tragwerkssystem, Ort |
| Quellenunsicherheit | viele ältere Kleinprojekte sind nur über Sekundärdatenbanken greifbar | fehlende Detailpublikation zum Bestandverplanzung-Pavillon | verbindet Fallstudie, Bericht, Vertrauensgrad |

---

## 3. FALLSTUDIE

- **Name:** Bestandverplanzung Pavilion, München  
- **Ort:** München, Deutschland  
- **Gebäude:** Pavillon / kleine wiederaufgebaute Bungalow-Struktur; genaue Gebäudebezeichnung unbekannt  
- **Projekt:** Wiederverwendung von Paneelen aus drei Bungalows des Münchner Olympischen Dorfes  
- **Beteiligte People / Akteure:** unbekannt; PRECS nennt als Literatur u. a. Huber und zukunftsgeraeusche, aber die konkrete Projektorganisation ist öffentlich nicht belastbar auffindbar  
- **Architekt:** unbekannt  
- **Tragwerksplaner:** unbekannt  
- **Bauherr:** unbekannt  
- **Zeitraum:** 2008 laut PRECS; Donor-Bungalows aus Olympiadorf-Kontext ca. 1972  
- **Ursprüngliche Nutzung:** Studentische bzw. olympische Bungalows im Olympischen Dorf München  
- **Neue Nutzung:** Pavillon / Demonstrator; genaue Nutzung unbekannt  
- **Fläche / Maßstab:** unbekannt; kleiner Pavillon/Demonstrator  
- **Schutzstatus / Denkmalstatus:** Olympisches Dorf München steht als Ensemble seit 1998 unter Schutz und seit 2018 als Einzeldenkmal; ob der Pavillon selbst Schutzstatus hat: unbekannt  
- **Quellenlage:** knapp; belastbar nur als Fall in PRECS/JCP-Datenbank plus allgemeine Quellen zum Olympischen Dorf

---

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; Gebäude-/Bungalow-Versetzungslogik  
- **Hauptniveau:** Tragwerk / Raum / Gebäudehülle, soweit Betonpaneele tragende bzw. raumbildende Teile waren  
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die Paneele blieben nicht einfach am Ort und wurden nicht nur recycelt; sie wurden aus Bungalows entnommen und in einer neuen/versetzten Struktur erneut verwendet.  
- **Warum ist der Fall relevant?** Früh belegter deutscher Kleinfall für Wiederverwendung von Fertigteil-Betonkomponenten aus einem ikonischen Nachkriegs-/Olympiabau-Bestand; relevant für Diskussion um Serienbauten, Demontagefähigkeit und Translozierung.

---

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Fertigteil-Paneele | Stahlbeton / Betonfertigteil | drei Bungalows des Olympischen Dorfes München | Wand-/Decken-/Raumelemente; genauer Typ unbekannt | Paneele in versetztem Pavillon / Bungalowstruktur | Paneele aus 3 Bungalows; Anzahl unbekannt | wahrscheinlich ja | ja | wahrscheinlich teilweise | nein | Demontage, Transport, Wiedereinbau; Details unbekannt | unbekannt | unbekannt | Tragfähigkeit, Gebrauchstauglichkeit, Dauerhaftigkeit | unbekannt | kaum technische Primärquellen | PRECS/JCP-Datenbank | Anzahl, Maße, Masse, genaue Position |
| Türen | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | nein | ja | ja/innen unbekannt | nein | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | nicht belegt | — | alle Details |
| Fenster/Fassade | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | nein | ja | ja | nein | unbekannt | unbekannt | unbekannt | Wärmeschutz, Dichtheit | unbekannt | nicht belegt | — | alle Details |
| Dach | unbekannt | unbekannt | unbekannt | Dach | unbekannt | unbekannt | ja | ja | nein | unbekannt | unbekannt | unbekannt | Feuchte, Lasten | unbekannt | nicht belegt | — | alle Details |
| Treppen/Geländer | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | ja | nein | nein | unbekannt | unbekannt | unbekannt | Absturzsicherung | unbekannt | nicht belegt | — | alle Details |
| TGA / Sanitär / Beleuchtung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | nein | nein | nein | ja | unbekannt | unbekannt | unbekannt | Betriebssicherheit | unbekannt | nicht belegt | — | alle Details |

---

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Identifikation wiederverwendbarer Bungalow-Paneele | unbekannt | unbekannt | unbekannt | — | — | unbekannt | unbekannt | geringe Quellenlage | unbekannt | PRECS/JCP |
| Bauteilinventar | Paneele aus drei Bungalows erfasst | unbekannt | unbekannt | unbekannt | — | — | unbekannt | unbekannt | keine öffentliche Liste | unbekannt | PRECS/JCP |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | — | — | unbekannt | unbekannt | Olympiadorf-Bungalows waren Altbestand | unbekannt | — |
| Rückbau | Demontage der Bungalow-Paneele | unbekannt | selektiver Rückbau anzunehmen | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Beschädigungsrisiko | unbekannt | PRECS/JCP |
| Ausbau | Entnahme der Paneele | unbekannt | unbekannt | Hebezeug vermutlich nötig, aber nicht belegt | unbekannt | unbekannt | unbekannt | unbekannt | Bauteilgewicht/Maße unbekannt | unbekannt | — |
| Transport | Verlagerung innerhalb/um München | unbekannt | unbekannt | unbekannt | — | unbekannt | unbekannt | unbekannt | Transportdetails unbekannt | unbekannt | — |
| Lagerung | unbekannt | unbekannt | unbekannt | unbekannt | — | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Aufbereitung | unbekannt | unbekannt | unbekannt | unbekannt | — | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Planung | Neu-/Versetzungsplanung für Pavillon | unbekannt | Anpassung an vorhandene Paneele | unbekannt | — | unbekannt | unbekannt | unbekannt | Maße und Anschlussdetails | unbekannt | PRECS/JCP |
| Genehmigung | unbekannt | unbekannt | unbekannt | unbekannt | — | — | unbekannt | unbekannt | Norm-/Haftungsfragen | unbekannt | — |
| Wiedereinbau | Paneele erneut montiert | unbekannt | Fertigteilmontage | unbekannt | — | unbekannt | unbekannt | unbekannt | Anschlussdetails unbekannt | unbekannt | PRECS/JCP |
| Monitoring | unbekannt | unbekannt | unbekannt | unbekannt | — | — | unbekannt | unbekannt | keine Folgedaten gefunden | unbekannt | — |

---

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | wiederverwendete Betonfertigteil-Paneele | Tragfähigkeit/Gebrauchstauglichkeit | unbekannt | unbekannt | Anschluss- und Nachweisführung | unbekannt | PRECS/JCP |
| Lastabtragung | wahrscheinlich über Paneele | unbekannt | unbekannt | unbekannt | alte Bauteile in neuer Lastsituation | unbekannt | abgeleitet, nicht einzeln belegt |
| Verbindung | unbekannt | Kraftübertragung, Dauerhaftigkeit | unbekannt | unbekannt | Originalanschlüsse evtl. verloren | unbekannt | — |
| Brandschutz | unbekannt | Feuerwiderstand | unbekannt | unbekannt | Nachweis alter Betonbauteile | unbekannt | — |
| Schallschutz | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Feuchte | unbekannt | Feuchte-/Frostschutz | unbekannt | unbekannt | alte Paneele / neue Hülle | unbekannt | — |
| Wärmeschutz | unbekannt | unbekannt | unbekannt | unbekannt | Altbauteile aus 1970er Jahren | unbekannt | — |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | alte Anschlussdetails | unbekannt | — |
| Luftdichtheit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| TGA-Integration | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Barrierefreiheit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Dauerhaftigkeit | PRECS listet Fall als gebaut | Dauerhafte Gebrauchstauglichkeit | unbekannt | unbekannt | Alter ca. 36 Jahre beim Wiedereinbau | unbekannt | PRECS/JCP |
| Wartung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Zulassung | unbekannt | unbekannt | unbekannt | unbekannt | experimenteller Kleinmaßstab | unbekannt | — |
| Haftung | unbekannt | unbekannt | unbekannt | unbekannt | unklare Verantwortlichkeiten | unbekannt | — |

---

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Jahr / Baubeginn Empfängerprojekt | 2008 | Jahr | PRECS-Fallstudiendatenbank | Projekt | PRECS/JCP | belegt |
| Alter der wiederverwendeten Komponenten | ca. 36 | Jahre | PRECS-Fallstudiendatenbank | Bauteile aus 1972-Kontext | PRECS/JCP | belegt |
| Donor-Umfang | 3 | Bungalows | PRECS-Fallstudiendatenbank | Donorgebäude | PRECS/JCP | belegt |
| wiederverwendete Masse | unbekannt | t | — | — | — | unklar |
| Anzahl Bauteile | unbekannt | Stück | — | — | — | unklar |
| Fläche | unbekannt | m² | — | — | — | unklar |
| CO₂-Einsparung | unbekannt | kg CO₂e | — | — | — | unklar |
| Abfallvermeidung | unbekannt | t | — | — | — | unklar |
| Transportdistanz | unbekannt | km | — | — | — | unklar |
| Kosten | unbekannt | EUR | — | — | — | unklar |
| Bauzeit | unbekannt | — | — | — | — | unklar |
| Zirkularitätskennwert | unbekannt | — | — | — | — | unklar |

---

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Sehr geringe Quellenlage | sozial / wissenschaftlich | Kleinprojekt, ältere Dokumentation schwer auffindbar | viele technische Details unbekannt | Bericht, Prüfung, Norm, Bauteil | Primärquellen suchen | Kleinprojekte brauchen systematische Dokumentation | Recherchebefund |
| Alte Fertigteile in neuer Funktion | technisch | Bauteile aus 1970er Jahren | Nachweise zu Tragfähigkeit, Anschlüssen, Dauerhaftigkeit nötig | Bauteil, Tragwerkssystem, Prüfung | unbekannt | Reuse braucht frühzeitige Prüfstrategie | PRECS/JCP + Ableitung |
| Anschlussdetails | technisch | ursprüngliche Verbindungen evtl. nicht wiederverwendbar | neue Verbindungsmittel nötig | Verbindung, Norm | unbekannt | Anschlussplanung ist Kernproblem bei Fertigteil-Reuse | PRECS/JCP + Ableitung |
| Denkmal-/Bestandskontext | rechtlich / kulturell | Olympiadorf ist geschützter Nachkriegsbestand | Rückbau/Umgang sensibel | Recht, Ort, Gebäude | denkmalgerechter Neubau/Sicherung im Gesamtprojekt | Reuse kann Konflikt zwischen Erhalt und Neubau sichtbar machen | München/Olympiapark-Quellen |
| Maßstab | methodisch | Pavillon statt Regelgebäude | begrenzte Übertragbarkeit | Fallstudie, Kennwert | als Anhang führen | Demonstratoren nicht mit Hauptfällen vermischen | eigene Einordnung |

---

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** unbekannt; vermutlich projektbezogene Bauteilgewinnung aus lokalem Donorbestand  
- **Bauteilbörse / Quelle:** keine Bauteilbörse belegt; Quelle waren Bungalows des Olympischen Dorfes München  
- **Kostenwirkung:** unbekannt  
- **Zeitwirkung:** unbekannt  
- **Versicherung / Haftung:** unbekannt  
- **Gewährleistung:** unbekannt  
- **Arbeitsaufwand:** unbekannt; aufgrund selektiver Demontage wahrscheinlich höher als Standardabbruch, aber nicht belegt  
- **Lagerung:** unbekannt  
- **Marktbarrieren:** fehlende Norm-/Prüf- und Beschaffungsroutine; geringe Dokumentation; begrenzter Maßstab

---

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** unbekannt; vermutlich über Bungalow-/Paneelcharakter sichtbar  
- **räumliche Transformation:** Paneele aus Bungalowbestand wurden in neuer/versetzter Pavillonstruktur weitergenutzt  
- **Atmosphäre / Ausdruck:** unbekannt  
- **Umgang mit Spuren:** unbekannt  
- **sozialer Wert:** Bezug zum Olympischen Dorf München und studentischem Wohnen; konkrete Beteiligung unbekannt  
- **Denkmal- oder Bestandswert:** hoher Kontextwert, da Olympisches Dorf München als Nachkriegs-/Olympia-Ensemble geschützt ist; Pavillon selbst unbekannt  
- **Kritik / Grenzen:** sehr geringe Detailquellen; kleiner Maßstab; daher nicht als Hauptfall führen

---

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** Abbruchmethode, Aufbereitungsmethode, Bauteilbörse, Förderprogramm, Interview, Software, Tool, Norm, Recht, Wirtschaft, genaue People/Akteure, Tragwerksplaner, Prüfung.  
- **Sinnvolle neue Entitäten:** Donorgebäude-Serie; Quellenunsicherheit; Translozierung.  
- **Fehlende Daten:** genaue Adresse, Pläne, Bauteilliste, Stückzahlen, Maße, Massen, Prüfberichte, Anschlussdetails, Kosten, CO₂, Genehmigung, heutiger Zustand.  
- **Zu prüfende Quellen:** Huber 2008/2013; zukunftsgeraeusche 2010; Münchner Archiv-/Studentenwerk-Unterlagen; Forschungsberichte zu OLY-72-Fertigteilreuse.

---

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** Anhang  
- **5 wichtigste Fakten:**  
  1. gebauter kleiner PRECS-Fall in München  
  2. Wiederverwendung von Paneelen aus drei Olympiadorf-Bungalows  
  3. Jahr 2008 laut PRECS  
  4. Bauteilalter ca. 36 Jahre laut PRECS  
  5. technische Detailquellen öffentlich kaum verfügbar  
- **5 wichtigste Bauteile:**  
  1. Betonfertigteil-Paneele  
  2. Wandpaneele: genauer Typ unbekannt  
  3. Decken-/Dachpaneele: unbekannt  
  4. Fenster/Türen: unbekannt  
  5. Anschlüsse: unbekannt  
- **5 wichtigste Hürden:**  
  1. Quellenlage  
  2. Tragfähigkeitsnachweis alter Paneele  
  3. Anschlussdetails  
  4. Denkmal-/Bestandskontext  
  5. geringe Skalierbarkeit  
- **5 wichtigste übertragbare Erkenntnisse:**  
  1. Fertigteilbestände können als Bauteilressource gelesen werden.  
  2. Kleinpavillons eignen sich als Testfeld, ersetzen aber keine Hauptfallstudie.  
  3. Historische und kulturelle Werte von Bauteilen können Reuse-Argumente stärken.  
  4. Ohne Prüf-/Bauteildokumentation bleibt die Übertragbarkeit begrenzt.  
  5. Serienbauteile brauchen standardisierte Demontage- und Anschlussstrategien.  
- **5 offene Fragen:**  
  1. Welche Paneeltypen wurden konkret verwendet?  
  2. Wer waren Architekt, Ingenieur, Bauherr?  
  3. Welche Prüfungen wurden durchgeführt?  
  4. Ist der Pavillon heute erhalten?  
  5. Welche Kosten-/CO₂-Wirkungen wurden ermittelt?

---

## QUELLEN UND LINKS

1. Küpfer, C. et al.: *Reuse of concrete components in new construction projects: Critical review of 77 circular precedents*, Journal of Cleaner Production 383, 2023. https://www.sciencedirect.com/science/article/pii/S0959652622048090  
2. EPFL open PDF / PRECS appendix mit Fall C52 „Bestandverplanzung Pavilion“. https://infoscience.epfl.ch/server/api/core/bitstreams/00948e56-68fd-4f05-9280-5e835b8d2570/content  
3. München/Olympiapark: Olympic Village. https://olympiapark.muenchen.de/en/olympiapark/olympisches-dorf.html  
4. Entdecken München: Bungalows in the Olympic Village. https://entdecken.muenchen.de/en/station/18-5/  
5. SOS Brutalism: Olympic Village Munich. https://www.sosbrutalism.org/cms/20147031
