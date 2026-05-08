---
id: "55_Great_Suffolk_Street_London"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "55 Great Suffolk Street, London — Fallstudie Direct Reuse / zirkuläres Bauen"
bauobjekt:
  - "55_Great_Suffolk_Street_London"
legacy_paths:
  - "Gebäude\\55_Great_Suffolk_Street_London.md"
projekt:
  - "55_Great_Suffolk_Street_London"
reuse_chain_detected: "True"
---
# 55 Great Suffolk Street, London — Fallstudie Direct Reuse / zirkuläres Bauen

## Migration

- Fallstudie ID: 55_Great_Suffolk_Street_London
- Legacy source count: 1
- Generated project: 55_Great_Suffolk_Street_London
- Generated bauobjekt: 55_Great_Suffolk_Street_London
- Extracted reuse_einsatz rows: 6
- Extracted datenpunkt rows: 17
- Extracted entity mapping rows: 36
- Reuse chain detected: True

## Legacy Content

### Legacy Source: Gebäude\55_Great_Suffolk_Street_London.md

- Map action: split_into_case_graph
- Primary target: fallstudie/55_Great_Suffolk_Street_London
- Secondary targets: projekt/55_Great_Suffolk_Street_London; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# 55 Great Suffolk Street, London — Fallstudie Direct Reuse / zirkuläres Bauen

**Stand:** 2026-05-07  
**Sprache:** Deutsch  
**Regel:** Gezählt werden nur wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Bestandserhalt wird nicht als Wiederverwendung gezählt, wenn Bauteile am Ort bleiben und dieselbe Funktion behalten.

---

## 1. EINORDNUNG

- **Entscheidung:** HAUPTFALL
- **Bewertung:** ★★★★☆
- **Begründung:** Das Projekt nutzt wiederverwendeten Baustahl für einen neuen außenliegenden Erschließungs- und Servicekern. Der Reuse-Anteil am Stahl dieses neuen Kerns ist sehr hoch und tragwerksrelevant. Nicht fünf Sterne, weil der Fall ein partieller Eingriff an einem Bestandsgebäude ist und der erhaltene denkmalgeschützte Lagerhausbestand selbst nicht als Direct Reuse gewertet wird.
- **Vertrauensgrad:** belegt
- **Warnung Bestandserhalt:** ja
- **Warnung Möbel/Dekoration:** nein
- **Projektstatus:** unklar / Live-Projekt; Quellen nennen „Expected in 2024“, „Estimated completion September 2024“ und Hawkins\Brown führt den Status weiterhin als „Live“. Eine belastbare öffentliche Fertigstellungsmeldung wurde nicht gefunden.

---

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | 55 Great Suffolk Street | Reuse-Fall eines denkmalgeschützten Lagerhauses mit neuem Stahlkern | ASBP, NLA, Hawkins\Brown | belegt | In Southwark, London |
| Gebäude | Grade II Listed Victorian warehouse | Bestandsgebäude; Retention ist nicht der Reuse-Score | ASBP, NLA, Hawkins\Brown | belegt | Heritage at Risk / lange ungenutzt laut Quellen |
| Projekt | Retrofit + Extension zu Arbeitsplatznutzung | Neuer externer Kern mit wiederverwendetem Stahl | ASBP, NLA | belegt | 15,000 sq ft / 1412 m² genannt |
| Ort | Southwark, London, UK | Standort | ASBP, NLA | belegt | Adresse: 55 Great Suffolk St, London SE1 |
| People | Fabrix | Developer / Bauherr | ASBP, NLA, Hawkins\Brown | belegt | Client / developer |
| People | Hawkins\Brown | Architekt | ASBP, NLA, Hawkins\Brown | belegt | Schreibweise in Quellen Hawkins Brown / Hawkins\Brown |
| People | Symmetrys | Structural engineer | ASBP, NLA | belegt | Tragwerksplanung |
| People | AKT II | Engineering consultant / Mitwirkung Reuse-Initiative | ASBP, Architects’ Journal | belegt | Nicht als Haupttragwerksplaner des Projekts eindeutig |
| People | CBRE | Sustainability consultant | ASBP, NLA, UKGBC | belegt | Embodied-carbon framework |
| People | Opera | Project manager | ASBP, Opera | belegt | Project management / contract administration |
| People | Gardiner & Theobald | Project manager reclaimed steel initiative | ASBP | belegt | Reuse-Beschaffung |
| People | Cantillon | Demolition contractor donor site 1 Broadgate | ASBP, Architects’ Journal | belegt | Lieferkette donor steel |
| People | Cleveland Steel and Tubes | Reclaimed steel stockholder / supplier | ASBP, NLA | belegt | Lagerung, Aufbereitung, Testkoordination |
| Bauteil | Wiederverwendete Stahlprofile | Tragender neuer externer Kern | ASBP, NLA | belegt | 20.35 t intended reused |
| Material | Baustahl | Reuse-Material | ASBP, NLA | belegt | Teilweise aus 1 Broadgate, teilweise Cleveland stock |
| Bauteilbörse | keine klassische Bauteilbörse | Direkte Beschaffung + Stockholder-Modell | ASBP, RIBA Journal | teilweise belegt | Kein offener Marktplatz genannt |
| Bericht | ASBP DISRUPT case study | Zentrale technische Quelle | ASBP | belegt | Interviewbasiert |
| Kennwert | 20.35 t reused steel | Menge wiederverwendeter Stahl im neuen Kern | ASBP, NLA | belegt | 97 % des Stahlwerks am neuen Kern |
| Kennwert | ca. 50 t CO₂ | Embodied carbon saving | ASBP, NLA | belegt | Quelle nennt „around“ / approximately |
| Kennwert | 386 kgCO₂e/m² A1-A5 | Upfront embodied carbon | ASBP, NLA | belegt | Nicht nur Stahlreuse, auch Retention |
| Prüfung | Testing + CE marking | Materialfreigabe wiederverwendeter Stahl | ASBP | belegt | EN 1090 genannt |
| Norm | EN 1090 | Konformität / CE marking der Stahlprofile | ASBP | belegt | Keine weiteren Normnummern erfinden |
| Recht | Grade II listing / Heritage at Risk | Denkmal-/Schutzkontext | NLA, Hawkins\Brown | teilweise belegt | Exakte Listen-ID unbekannt |
| Reuse-Strategie | Ex-situ Bauteilwiederverwendung | Stahl aus donor site / stockholder in neuer Funktion | ASBP, NLA | belegt | Tragende Konstruktion |
| Abbruchmethode | Deconstruction / Demolition donor site 1 Broadgate | Gewinnung von Stahl aus 1 Broadgate | ASBP, Architects’ Journal | teilweise belegt | Details der Demontage nur teilweise |
| Aufbereitungsmethode | Entfernen von Anbauteilen, Löcher füllen, Testen, CE marking | Reuse-fähig machen | ASBP | belegt | Hot-cut ends am donor steel erwähnt |
| Verbindung | Stahlbauverbindungen | Neue Konstruktion des externen Kerns | ASBP | unklar | Konkrete Verbindungstypen unbekannt |
| Hürde | Profilverfügbarkeit, Services, Profilhöhen, Zertifizierung | Planerische/technische Reuse-Hürden | ASBP | belegt | Tiefe Profile behinderten Services |
| Leistungsanforderung | Tragfähigkeit, Zertifizierung, Brandschutz, Erschließung | Neubau-/Umbauanforderungen | ASBP, Planungspapiere teilweise | teilweise belegt | Details Brandschutz öffentlich unvollständig |
| Wirtschaft | Materialkosten niedriger, aber keine Gesamteinsparung | Business case | ASBP, RIBA Journal | belegt | Aufwand für Aufbereitung/Erstfall |
| Logistik | Vorausbeschaffung, Lagerung bei Cleveland | Termin-/Supply-Chain-Strategie | ASBP, RIBA Journal | belegt | Kein Zeitverzug laut ASBP |
| Software | unbekannt | Keine projektspezifische Software belastbar gefunden | — | unklar |  |
| Tool | unbekannt | Keine projektspezifischen Reuse-Tools belastbar gefunden | — | unklar |  |
| Schadstoff | unbekannt | Keine belegten Schadstoffangaben zum Stahl | — | unklar | Paint/shear studs erwähnt, Schadstoff nicht |
| Förderprogramm | DISRUPT | Forschungs-/Case-Study-Kontext | ASBP | belegt | Nicht zwingend Projektförderung |
| Methode | Circular economy / urban mining | Beschaffung und Entwurf nach verfügbaren Profilen | ASBP, NLA, RIBA Journal | belegt |  |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Donor-Gebäude | Reuse braucht Herkunftsobjekt als eigene Entität | 1 Broadgate als donor site | Gebäude, Bauteil, Logistik, Prüfung |
| Reuse-Stockholder | Spezifischer Akteur zwischen Rückbau und Wiedereinbau | Cleveland Steel and Tubes | Bauteilbörse, Logistik, Prüfung, Wirtschaft |
| Reuse-Kette | Verknüpft Rückbauprojekt, Lagerung, Prüfung, neues Projekt | 1 Broadgate → Cleveland → 55 Great Suffolk Street | Prozessphase, Logistik, Bauteil |
| Reuse-Konformität | Zertifizierungsstatus wiederverwendeter Profile | CE marking / EN 1090 | Prüfung, Norm, Recht, Leistungsanforderung |

---

## 3. FALLSTUDIE

- **Name:** 55 Great Suffolk Street
- **Ort:** Southwark, London, Vereinigtes Königreich
- **Gebäude:** denkmalgeschütztes viktorianisches Lagerhaus, Grade II Listed
- **Projekt:** Retrofit / Conservation / Extension mit neuem außenliegendem Stahlkern
- **Beteiligte People / Akteure:** Fabrix; Hawkins\Brown; Symmetrys; AKT II; CBRE; Opera; Exigere; Gardiner & Theobald; Cantillon; Cleveland Steel and Tubes; Sir Robert McAlpine am donor site 1 Broadgate
- **Architekt:** Hawkins\Brown
- **Tragwerksplaner:** Symmetrys; AKT II als Engineering Consultant in Reuse-Initiative genannt
- **Bauherr:** Fabrix
- **Zeitraum:** Opera nennt 2021–2023; ASBP/NLA nennen erwartete Fertigstellung 2024; aktueller belastbarer Fertigstellungsstatus unbekannt
- **Ursprüngliche Nutzung:** Papierwaren-/Lagerhaus, u. a. Spicer Bros paper merchants
- **Neue Nutzung:** flexible Büro-/Arbeitsplatzflächen, Retail am Erdgeschoss / amenity facilities
- **Fläche / Maßstab:** 1412 m² / 15,000 sq ft genannt; NLA nennt auch 10,000 sq ft workspace in einem Textabschnitt; konsolidierter Wert: unbekannt mit Quellenkonflikt
- **Schutzstatus / Denkmalstatus:** Grade II Listed; Heritage at Risk wird in NLA/Hawkins\Brown-Kontext genannt
- **Quellenlage:** gut für Stahlreuse, Akteure, Mengen, CO₂- und Prozessangaben; unvollständig für endgültige Fertigstellung, detaillierte Verbindungstechnik, Brandschutz, konkrete Lagerdauer

---

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; Urban Mining; Reuse-Stockholder-Modell
- **Hauptniveau:** Tragwerk und räumlicher Erschließungskern
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Das erhaltene Lagerhaus ist Bestandserhalt und zählt nicht als Reuse-Score. Bewertungsrelevant ist der neue externe Stahlkern aus wiederverwendeten Profilen. Anders als Recycling bleibt der Stahl als Profil / Bauteil erhalten und wird nicht eingeschmolzen.
- **Warum ist der Fall relevant?** Er zeigt ein frühes UK-Beispiel, bei dem ein Entwickler Stahl aus einem Abbruchprojekt im Voraus kauft, prüfen lässt und in ein neues tragendes Bauteilsystem integriert. Der Fall ist besonders relevant für Beschaffung, Zertifizierung und Kosten-/Zeitlogik von wiederverwendetem Baustahl.

---

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Stahlprofile für neuen externen Kern | Baustahl | 1 Broadgate + Cleveland Steel and Tubes | Tragwerk eines donor building / reclaimed stock | Tragstruktur externer Service- und Erschließungskern | 20.35 t; 97 % von 20.98 t Stahlwerk | ja | ja | nein | indirekt, als Träger von Servicekern | Anbauteile entfernt, Löcher gefüllt, getestet, CE markiert | unbekannt | Testing centres; CE marking | Tragfähigkeit, Schweißbarkeit, Nachweisbarkeit | EN 1090 genannt | Profilgrößen, Services, Aufbereitung, Zertifizierung | ASBP, NLA | Verbindungstypen |
| Stahl aus 1 Broadgate | Baustahl | donor site 1 Broadgate, City of London | Stahlrahmen eines abgebrochenen Bürogebäudes | Teil des neuen Kerntragwerks | 8.3 t / ca. 43 % des reused steel | ja | ja | nein | nein | Concrete casings entfernt, hot-cut ends; Weiterbearbeitung | unbekannt | getestet / CE | strukturelle Verwendung | EN 1090 | timing donor/receiver, Profilverfügbarkeit | ASBP, Architects’ Journal | exakte Profile |
| Reclaimed stock von Cleveland | Baustahl | Cleveland Steel and Tubes | reclaimed stock / surplus | Teil des neuen Kerntragwerks | 11.1 t / ca. 57 % des reused steel | ja | ja | nein | nein | Lagerung, Restaurierung, Rezertifizierung | unbekannt | testing / CE | strukturelle Verwendung | EN 1090 | Marktliquidität | ASBP | ursprüngliche Herkunft |
| Bestandslagerhaus | Mauerwerk, Gusseisen, Holz, Stahlfenster u. a. | am Ort vorhanden | Lagerhaus | Büro-/Arbeitsplatzbestand | unbekannt | ja, aber nicht als Reuse gezählt | ja | ja | nein | Restaurierung / Erhalt | Bestand | denkmal-/bauaufsichtlich unbekannt | Denkmalschutz, Nutzungsänderung | Grade II | Bestandserhalt darf nicht als Direct Reuse gezählt werden | NLA, Hawkins\Brown, Opera | Mengen |
| Brückenlinks zum Kern | unbekannt / vermutlich Stahl | neues Projekt | keine | Verbindung Kern–Bestand | unbekannt | unbekannt | ja | nein | ja | unbekannt | unbekannt | unbekannt | Barrierefreiheit, Erschließung | unbekannt | Schnittstelle Alt/Neu | NLA | Material und Reuse-Anteil |
| Fassadenbekleidung externer Kern | unbekannt / corrugated cladding | neu, nicht als reuse belegt | keine | Hülle / Ausdruck | unbekannt | nein | nein | ja | nein | unbekannt | unbekannt | unbekannt | Witterung, Gestaltung | unbekannt | kein Reuse-Nachweis | NLA, Hawkins\Brown | Reuse-Anteil |

---

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Bedarf an Stahlprofilen für externen Kern identifiziert | Fabrix, Hawkins\Brown, Symmetrys, CBRE | Circular economy briefing | unbekannt | — | — | — | frühzeitige Integration in RIBA Stage 2/3 | Reuse zu spät im Briefing möglich | frühe Bauherrenvorgabe | ASBP, RIBA Journal |
| Bauteilinventar | Geeignete Profile aus 1 Broadgate gesucht | Fabrix, AKT II, Cantillon, Cleveland | Urban Mining nach Profilgrößen | unbekannt | donor building in Demolition/Deconstruction | Concrete casing ab, hot cuts | Vorprüfung | direkter Deal mit demolition contractor | Donor-Receiver timing | Vorabkauf von 139 t Stahl durch Fabrix | ASBP, Architects’ Journal |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine Daten | unbekannt | — |
| Rückbau | Stahl am donor site ausgebaut | Cantillon, Sir Robert McAlpine | deconstruction for reuse / demolition | unbekannt | Demolition donor site | hot-cut ends | unbekannt | Transport zu Cleveland | Stahl war ursprünglich fürs Einschmelzen vorgesehen | Deal auf Reuse umgestellt | ASBP, RIBA Journal |
| Ausbau | Stahlprofile getrennt und übernommen | Cantillon, Fabrix | Selektive Gewinnung | unbekannt | teilweise unbekannt | Anbauteile entfernt | unbekannt | Cleveland als Stockholder | Zusatzaufwand | Reuse-spezifische Prozesskette | ASBP |
| Transport | Donor → Stockholder → Baustelle | Cantillon, Cleveland, Fabrix | Reuse logistics | unbekannt | — | — | — | unbekannt | Transportemissionen und Timing | lokale London/UK-Kette, aber Distanz unbekannt | ASBP |
| Lagerung | Lagerung und Bereitstellung | Cleveland Steel and Tubes | Stockholder model | unbekannt | — | Lagerung, Restaurierung | Nachweisverwaltung | Stahl vor Produktion verfügbar | Markt illiquide | Stockholder als Puffer | ASBP, RIBA Journal |
| Aufbereitung | Attachments entfernt, Löcher gefüllt, Profile getestet | Cleveland | Restoration / recertification | unbekannt | — | Entfernen, Füllen, Testen, CE marking | Testing centres | unbekannt | Aufwand / Kosten | spezialisierter Reuse-Stockholder | ASBP |
| Planung | Entwurf an verfügbare Stahlgrößen angepasst | Hawkins\Brown, Symmetrys | Design from availability | unbekannt | — | — | Ingenieurprüfung | Beschaffung vor Produktion | tiefere Profile, Services-Kollision | Iterationen und Koordination | ASBP |
| Genehmigung | Denkmal-/Planungskontext mit Southwark | Planungsteam, Borough | Conservation + retrofit | unbekannt | — | — | bauaufsichtlich unbekannt | unbekannt | Denkmalschutz und Erschließung | externer Kern erhält Bestandsoffenheit | NLA, Opera |
| Wiedereinbau | Montage neuer Kern aus reused steel | Bau-/Stahlbauakteure unbekannt | Stahlbau | unbekannt | — | vorbereitete Profile | CE/EN 1090 | keine Zeitwirkung laut ASBP | unbekannte Montage-Details | Stahl im Voraus beschafft | ASBP |
| Monitoring | Carbon und Projektziele dokumentiert | CBRE, Fabrix | embodied-carbon assessment | unbekannt | — | — | unbekannt | unbekannt | Bilanzgrenzen | A1-A5 Kennwert dokumentiert | ASBP, NLA |

---

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Neuer externer Stahlkern aus überwiegend reused steel | Vertikale/horizontale Lasten des Kerns | EN 1090 für CE marking genannt | Testing centres | Profilverfügbarkeit | Entwurf auf verfügbare Profile | ASBP |
| Lastabtragung | Tragende Stahlprofile im Kern | Tragfähigkeit | unbekannt | unbekannt außer Materialprüfung | Details nicht öffentlich | unbekannt | ASBP |
| Verbindung | Stahlbauverbindungen nicht detailliert veröffentlicht | Anschlussfähigkeit, Montage | unbekannt | unbekannt | Profilunterschiede und vorhandene Löcher | Löcher gefüllt, Koordination | ASBP |
| Brandschutz | Fire strategy nicht projektspezifisch vollständig öffentlich | Building Regulations / Fire Safety Order relevant | Building Regulations 2010 / Regulatory Reform Fire Safety Order 2005 in Planungsdokument genannt | Construction monitoring / Regulation-38-Handover in Planungsdokument | unbekannt | Fire engineer / final fire strategy laut Planungserfordernis | Southwark planning PDF |
| Schallschutz | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Feuchte | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Wärmeschutz | Ziel Net Zero / BREEAM Excellent genannt | Energie-/Carbon Performance | unbekannt | unbekannt | Denkmalbestand | Retrofit statt Neubau | NLA |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | Alt-Neu-Schnittstelle wahrscheinlich | unbekannt | — |
| Luftdichtheit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| TGA-Integration | Externer Kern enthält WCs, Lift, Bike store, showers; Services-Koordination mit Profilhöhen | moderne Erschließung und Amenities | Barrierefreiheit rechtlich relevant, konkrete Norm unbekannt | unbekannt | tiefere Stahlprofile erschweren Services | Layout- und Koordinationsänderungen | ASBP, NLA |
| Barrierefreiheit | Externer Kern ermöglicht step-free access / new lift | Zugang zu allen Ebenen | unbekannt | unbekannt | denkmalgeschützter Bestand | neuer externer Kern | Hawkins\Brown, NLA |
| Dauerhaftigkeit | CE/UKCA/EN 1090-Konformität als Nachweis | langfristige Nutzbarkeit | EN 1090 | Testing centres | Alter/Qualität variiert | Aufbereitung und Marking | ASBP |
| Wartung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Zulassung | Kein Warranty-Problem, weil CE/UKCA markiert | Zulassungs-/Versicherungsfähigkeit | EN 1090 | CE marking | Reuse-Stahl muss konform nachgewiesen werden | Cleveland / testing centres | ASBP |
| Haftung | No warranty issues reported | Nachweisbarkeit | EN 1090 | CE/UKCA | Unsicherheit Reuse-Material | Zertifizierung | ASBP |

---

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Reused steel intended | 20.35 | t | Projekt-/ASBP-Daten | Neuer externer Kern | ASBP, NLA | belegt |
| Gesamtstahlwerk am Kern | 20.98 | t | Projekt-/ASBP-Daten | Neuer externer Kern | ASBP | belegt |
| Anteil reused steel am Kernstahl | 97 | % | 20.35/20.98 t | Neuer externer Kern | ASBP | belegt |
| Stahl aus donor site 1 Broadgate | 8.3 | t | Projekt-/ASBP-Daten | Anteil reused steel | ASBP | belegt |
| Reclaimed stock Cleveland | 11.1 | t | Projekt-/ASBP-Daten | Anteil reused steel | ASBP | belegt |
| Gesamtstahlkauf Fabrix | 139 | t | Urban-mining purchase | mehrere Fabrix-Projekte | NLA, Architects’ Journal | belegt |
| CO₂-Einsparung Stahlreuse | ca. 50 | t CO₂ / CO₂e | Vergleich zu A1-A3 2.5 kgCO₂e/kg steel | Stahl des externen Kerns | ASBP, NLA | teilweise belegt |
| Upfront embodied carbon | 386 | kgCO₂e/m² | embodied-carbon assessment | A1-A5 | ASBP, NLA | belegt |
| Frühere RIBA Stage 2 Schätzung | 406 | kgCO₂/m² | embodied-carbon estimation | A1-A5 | UKGBC | belegt |
| Reduktion ggü. LETI 2020 target | 36 | % | Vergleich zu 600 kgCO₂e/m² | A1-A5 | ASBP, NLA | belegt |
| Fläche | 1412 | m² | Projektdaten | Gebäude/Projekt | ASBP, NLA | belegt |
| Workspace-Fläche | 10,000 / 15,000 | sq ft | Quellenkonflikt | Projekt | NLA / ASBP | teilweise belegt |
| Kosten | unbekannt | — | — | — | — | unklar |
| Bauzeit | unbekannt | — | — | — | — | unklar |
| U-Wert | unbekannt | — | — | — | — | unklar |
| Lebensdauer | unbekannt | — | — | — | — | unklar |
| Zirkularitätskennwert | unbekannt | — | — | — | — | unklar |

---

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Kein liquider Reuse-Stahlmarkt | wirtschaftlich/logistisch | Fehlende zentrale Register und Timing-Probleme | Reuse hängt von Donor-Receiver-Zufall ab | Bauteilbörse, Logistik, Wirtschaft | Direktdeal + Stockholder | Materialpools würden Skalierung erleichtern | ASBP, RIBA Journal |
| Zertifizierung von Reuse-Stahl | rechtlich/technisch | Materialhistorie muss nachgewiesen werden | Zusatzprüfung und Aufbereitung | Prüfung, Norm, Recht | Testing + CE marking nach EN 1090 | Zertifizierungsroute früh klären | ASBP |
| Profilgrößen passen nicht perfekt | technisch/gestalterisch | Entwurf muss mit vorhandenen Profilen arbeiten | Services-Kollisionen, Layoutänderungen | Bauteil, TGA, Verbindung | Iterative Koordination | Reuse muss ab Briefing/Stage 0–1 starten | ASBP |
| Materialqualität variiert | technisch | Lack, shear studs, Zuschnitte, Löcher | Aufbereitung nötig | Bauteil, Aufbereitungsmethode | Entfernen/Füllen/Testen | Visuelle und technische Audits einplanen | ASBP |
| Keine Gesamtkosteneinsparung | wirtschaftlich | Erstfall, manuelle Prozesse, Reprocessing | Reuse nicht automatisch billiger | Wirtschaft, Aufbereitung | Bauherr hält an Carbon-Ziel fest | Business case nicht nur über Materialpreis bewerten | ASBP, RIBA Journal |
| Bestandsschutz / Denkmalschutz | rechtlich/gestalterisch | Grade II Listed warehouse | Eingriffe begrenzt | Recht, Gebäude, Projekt | Externer Kern erhält offene Bestandsgrundrisse | Reuse kann Bestand entlasten | NLA, Opera |
| Verwechslung Retention vs Reuse | methodisch | Bestandsgebäude bleibt erhalten | Risiko zu hoher Bewertung | Fallstudie, Reuse-Strategie | Score nur für neuen reused-steel core | Bestandserhalt separat bilanzieren | eigene Bewertung nach Grundregel |

---

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** Direkter Ankauf von reclaimed steel durch Fabrix aus donor site 1 Broadgate; Ergänzung über Cleveland Steel and Tubes als Stockholder.
- **Bauteilbörse / Quelle:** Keine klassische Bauteilbörse; donor site 1 Broadgate + Cleveland Steel and Tubes.
- **Kostenwirkung:** Reclaimed material war niedriger im Materialpreis bzw. marginally cheaper; laut ASBP keine echte Gesamteinsparung wegen Aufbereitung, Ästhetik und Erstfall-Aufwand.
- **Zeitwirkung:** ASBP nennt keine negativen Auswirkungen auf den Projektzeitplan, da Material früh beschafft wurde.
- **Versicherung / Haftung:** Keine Warranty-Probleme laut ASBP, weil CE/UKCA marked.
- **Gewährleistung:** belegt nur als „no warranty issues“; Details unbekannt.
- **Arbeitsaufwand:** hoch / manuell im Erstfall; Prozesse mussten teilweise neu entwickelt werden.
- **Lagerung:** Cleveland Steel and Tubes übernahm Lagerung, Restaurierung und Zertifizierung.
- **Marktbarrieren:** illiquider Markt, fehlendes zentrales Register, Timing von Rückbau und Neubau, Zertifizierungsaufwand, Planungsgewohnheiten.

---

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** Der neue externe Kern ist architektonisch ablesbar; ob die Reuse-Stahlspuren sichtbar bleiben, ist unbekannt.
- **räumliche Transformation:** Der externe Kern nimmt WCs, Lift, Bike-store, showers und step-free access auf und lässt die offenen Bestandsgrundrisse weitgehend intakt.
- **Atmosphäre / Ausdruck:** Kontrast aus viktorianischem Lagerhaus und zeitgenössischem externem Kern; corrugated cladding referenziert historische Papier-/Wellpappen-Nutzung.
- **Umgang mit Spuren:** Historische trap doors und Bestandsmerkmale werden laut NLA/Hawkins\Brown sichtbar bzw. lesbar gehalten.
- **sozialer Wert:** Reaktivierung eines lange leerstehenden Gebäudes; lokaler Heritage-Wert.
- **Denkmal- oder Bestandswert:** hoher Bestandswert, Grade II Listed, Heritage at Risk genannt.
- **Kritik / Grenzen:** Der kulturelle Wert kommt stark aus Bestandserhalt; der Direct-Reuse-Wert liegt fast ausschließlich im neuen Stahlkern. Ohne klare Trennung droht Überbewertung.

---

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** Gastprofessur, Lehrstuhl, konkrete Software, Tool, detaillierte Normen jenseits EN 1090, Schadstoff, detaillierte Verbindung, detaillierte TGA.
- **Welche neuen Entitäten wären sinnvoll?** Donor-Gebäude, Reuse-Stockholder, Reuse-Kette, Reuse-Konformität, Materialpass/Traceability-ID.
- **Welche Daten fehlen?** endgültige Fertigstellung; exakte Stahlprofile; Verbindungstypen; Lagerdauer; Transportdistanz; Brandschutzdetails; Kostenaufschlüsselung; Wartungs-/Monitoringdaten; vollständige Zertifikatslogik.
- **Welche Quellen müssten geprüft werden?** Planungsunterlagen Southwark; Statik-/Steelwork drawings; CE/UKCA-Zertifikate; Cleveland testing reports; Projektabschlussmeldung von Fabrix/Hawkins\Brown/Symmetrys.

---

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja, aber mit Statushinweis „Fertigstellung unklar/Live“ und Warnung Bestandserhalt.
- **5 wichtigste Fakten:**
  1. Neuer externer Kern nutzt 20.35 t reused steel.
  2. 97 % des Stahlwerks des neuen Kerns sind reused steel.
  3. 8.3 t kamen aus 1 Broadgate; 11.1 t aus Cleveland stock.
  4. Embodied-carbon saving für Stahlreuse wird mit ca. 50 t CO₂ angegeben.
  5. Das denkmalgeschützte Lagerhaus bleibt erhalten, zählt aber nicht als Direct Reuse.
- **5 wichtigste Bauteile:**
  1. wiederverwendete Stahlprofile externer Kern
  2. Stahl aus donor site 1 Broadgate
  3. reclaimed steel stock von Cleveland
  4. externe Brückenlinks / Erschließungsanschlüsse, Reuse-Anteil unbekannt
  5. Bestandsstruktur, nur als Bestandserhalt, nicht als Reuse
- **5 wichtigste Hürden:**
  1. Zertifizierung / CE / EN 1090
  2. Marktliquidität und Timing donor–receiver
  3. Profilgrößen und Service-Koordination
  4. Aufbereitungskosten
  5. methodische Trennung von Retention und Direct Reuse
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Reuse-Stahl muss früh im Briefing und Entwurf verankert werden.
  2. Stockholder können Lagerung, Prüfung und Marktfähigkeit ermöglichen.
  3. Der niedrigere Materialpreis garantiert keine Gesamtkosteneinsparung.
  4. Zertifizierte Reuse-Profile können warranty barriers reduzieren.
  5. Bestandserhalt und Bauteilwiederverwendung müssen getrennt bilanziert werden.
- **5 offene Fragen:**
  1. Ist das Projekt praktisch fertiggestellt?
  2. Welche Profile wurden konkret eingebaut?
  3. Welche Verbindungsmittel wurden verwendet?
  4. Wie hoch waren tatsächliche Reuse-Mehrkosten?
  5. Welche Brandschutz-/Korrosionsschutzmaßnahmen wurden für reused steel eingesetzt?

---

## Quellen / Links

1. ASBP — 55 Great Suffolk Street case study: https://asbp.org.uk/case-studies/55-great-suffolk-street  
2. New London Architecture — 55 Great Suffolk Street: https://www.nla.london/projects/55-great-suffolk-street  
3. Hawkins\Brown — 55 Great Suffolk Street: https://www.hawkinsbrown.com/projects/55-great-suffolk-street/  
4. Opera PM — 55 Great Suffolk Street: https://www.operapm.co.uk/place/our-projects/55-great-suffolk-street  
5. UKGBC — 55 Great Suffolk Street: https://ukgbc.org/resources/55-great-suffolk-street/  
6. Architects’ Journal — Broadgate steel frame recycled for Southwark retrofits: https://www.architectsjournal.co.uk/news/developer-urban-mines-broadgate-steel-frame-for-southwark-retrofits  
7. RIBA Journal — Fabrix reused steel lessons: https://www.ribaj.com/intelligence/reusing-steel-fabrix-hawkins-brown-sheppard-robson-riba-exhibition/  
8. Planning document found online — fire safety / Regulation 38 context: https://docs.planning.org.uk/20250730/54/T0453VKBMST00/ujg7bk1ggx2tx844.pdf
