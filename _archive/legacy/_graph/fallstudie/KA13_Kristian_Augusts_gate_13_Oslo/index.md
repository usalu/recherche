---
id: "KA13_Kristian_Augusts_gate_13_Oslo"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "KA13 / Kristian Augusts gate 13, Oslo — Fallstudie Direct Reuse / Bauteilwiederverwendung"
bauobjekt:
  - "KA13_Kristian_Augusts_gate_13_Oslo"
legacy_paths:
  - "Gebäude\\KA13_Kristian_Augusts_gate_13_Oslo.md"
projekt:
  - "KA13_Kristian_Augusts_gate_13_Oslo"
reuse_chain_detected: "True"
---
# KA13 / Kristian Augusts gate 13, Oslo — Fallstudie Direct Reuse / Bauteilwiederverwendung

## Migration

- Fallstudie ID: KA13_Kristian_Augusts_gate_13_Oslo
- Legacy source count: 1
- Generated project: KA13_Kristian_Augusts_gate_13_Oslo
- Generated bauobjekt: KA13_Kristian_Augusts_gate_13_Oslo
- Extracted reuse_einsatz rows: 12
- Extracted datenpunkt rows: 18
- Extracted entity mapping rows: 25
- Reuse chain detected: True

## Legacy Content

### Legacy Source: Gebäude\KA13_Kristian_Augusts_gate_13_Oslo.md

- Map action: split_into_case_graph
- Primary target: fallstudie/KA13_Kristian_Augusts_gate_13_Oslo
- Secondary targets: projekt/KA13_Kristian_Augusts_gate_13_Oslo; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# KA13 / Kristian Augusts gate 13, Oslo — Fallstudie Direct Reuse / Bauteilwiederverwendung

**Arbeitsstand:** 2026-05-06  
**Sprache:** Deutsch  
**Grundregel:** Gewertet werden nur wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Reiner Bestandserhalt wird nicht als Direct Reuse gewertet, wenn Bauteile am Ort bleiben und dieselbe Funktion behalten.

---

## 1. EINORDNUNG

- **Entscheidung:** HAUPTFALL
- **Bewertung:** ★★★★★
- **Begründung:** KA13 ist ein gebautes großmaßstäbliches Wiederverwendungsprojekt mit tragenden ex-situ-Donor-Bauteilen: wiederverwendete Hohlkörperdecken aus Regjeringsbygg R4 und wiederverwendeter Stahl in der Erweiterung sowie viele weitere wiederverwendete Hüll-, Raum- und Technikbauteile. Wichtig: Das erhaltene Bestandstragwerk und die Außenwände zählen nach der Grundregel nicht als Direct Reuse, sondern als Bestandserhalt; bewertungsrelevant sind die umgesetzten donor-basierten und transformierten Bauteilwiederverwendungen.
- **Vertrauensgrad:** belegt
- **Warnung Bestandserhalt:** ja
- **Warnung Möbel/Dekoration:** ja; lose Ausstattung wird nicht gewertet. Feste Bürofronten, Türen, Radiatoren, Sanitär und Lüftung können zählen.
- **Projektstatus:** gebaut

---

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | KA13 / Kristian Augusts gate 13 | Untersuchter Direct-Reuse-Fall | S1, S2 | belegt | FutureBuilt-Pilot |
| Gebäude | Bürogebäude mit Umbau und Erweiterung | Bestand + neues Annex/Erweiterung | S1 | belegt | Originalgebäude 1950er |
| Ort | Kristian Augusts gate 13, Oslo, Norwegen | Standort | S1, S2 | belegt | Tullinløkka |
| Projekt | Reuse and transformation / KA13 | Projektname/Ansatz | S1, S5 | belegt | Zirkulärer Umbau |
| Bauherr | Entra AS | Developer | S1, S4 | belegt | rechtliche Verantwortung laut Sekundärquellen bei Client stark |
| Architekt | MAD arkitekter / Mad as | Architektur | S1 | belegt | FutureBuilt nennt Mad/Mad as |
| Tragwerksplaner | unbekannt | Nicht eindeutig in verfügbaren Quellen | - | unbekannt | Rådgiver ombruk: Asplan Viak / Insenti |
| People | Entra, MAD, FutureBuilt, Asplan Viak, Insenti, Scenario Interiørarkitekter, IWG/Spaces | Beteiligte Akteure | S1 | belegt | Rollen teils klar |
| Reuse-Strategie | Großmaßstäbliche Bauteilwiederverwendung + Transformation | zentrale Projektstrategie | S1, S2 | belegt | bis/nahe 80 % Wiederverwendung nach Gewicht |
| Bauteil | Hohlkörperdecken / hollow-core slabs | Donor-Tragwerk in Erweiterung | S2, S3, S6 | belegt | 21 Elemente, ca. 160 m² laut Sekundär-/Thesisquelle |
| Bauteil | Stahl | tragende Bauteile, ca. 75 % reused laut Norden | S2 | teilweise belegt | genaue Bauteilliste unbekannt |
| Bauteil | Radiatoren | wiederverwendete technische Bauteile | S1, S2 | belegt | teils aus Bestand und/oder Donor |
| Bauteil | Fassadenbekleidung | Hüllbauteil-Wiederverwendung | S2 | teilweise belegt | genaue Komponenten/Mengen unbekannt |
| Bauteil | Sanitär, ducts, pipes, office fronts, doors | feste Technik-/Innenbauteile | S2 | teilweise belegt | zählt, sofern fest eingebaut |
| Tragwerkssystem | bestehendes Stahlstützensystem + donor HCS/Steel | Bestand + Erweiterung | S2 | teilweise belegt | Bestand nicht als Direct Reuse zählen |
| Prozessphase | Umbau, Rückbau, Aufbereitung, Wiedereinbau | Circular pilot process | S1, S5 | belegt | 25 donor buildings laut Sekundärquellen |
| Prüfung | Dokumentation nach TEK; Tests/SINTEF für HCS laut Thesisquellen | Nachweis reused hollow-core slabs | S3, S7 | teilweise belegt | genaue Prüfberichte unbekannt |
| Norm | NS 3682 für reuse of hollow-core slabs | nach/aus Erfahrungen relevant | S3 | teilweise belegt | Standard wurde nach solchen Erfahrungen eingeführt; Anwendung im Projekt wegen Fertigstellung 2021 unklar |
| Recht | Regelwerksarbeit / regulatorische Anpassung | KA13 beeinflusste Regelwerksdiskussion | S1, S4 | belegt | genaue Paragraphen unbekannt |
| Kennwert | Gesamtfläche 4.297 m² | Projektmaßstab | S1 | belegt | Original 2.734 m²; Basement 708 m²; Extension 855 m² |
| Kennwert | nahezu/bis 80 % Wiederverwendung | Materialwiederverwendung | S1, S2, S4 | belegt | Methodik FutureBuilt |
| Kennwert | 70 % Treibhausgasreduktion | Klimawirkung | S1, S4 | teilweise belegt | Vergleich Neubau; Methodik nicht im Detail in Kurzquellen |
| Kennwert | ca. 160 m² HCS, 21 Elemente | Tragwerksbauteile | S6 | teilweise belegt | Thesisquelle |
| Wirtschaft | HCS 5–6× teurer als neue HCS laut Thesis | Kostenhürde | S6, S8 | teilweise belegt | Pilot-/Erstaufwand; nicht Gesamtprojektkosten |
| Hürde | Regelwerk, Dokumentation, Marktverfügbarkeit, Rückbaukosten | zentrale Barrieren | S1, S2, S6, S8 | belegt | - |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Donor Building | Mehrere externe Gebäude liefern Bauteile | Regjeringsbygg R4; weitere ca. 25 donor projects/buildings | verbindet Ort, Bauteil, Logistik |
| Reuse-Koordinator | Koordination zwischen Rückbau, Planung, Markt und Genehmigung | Insenti als Koordinator laut FutureBuilt | verbindet Prozessphase, People, Logistik |
| Regelwerks-Pilot | Projekt erzeugt Lernwissen für neue Norm-/Regelarbeit | Erfahrungen flossen in norwegische Diskussionen und HCS-Standard ein | verbindet Recht, Norm, Bericht |
| Ombruksgrad / Reuse-by-weight | Wiederverwendungsanteil als norwegischer Kennwert | ca. 80 Gewichts-% nach FutureBuilt-Methodik | verbindet Kennwert, Datenmodell |

---

## 3. FALLSTUDIE

- **Name:** KA13 / Kristian Augusts gate 13
- **Ort:** Kristian Augusts gate 13, Oslo, Norwegen
- **Gebäude:** Bürogebäude aus den 1950er-Jahren, saniert/transformiert und erweitert
- **Projekt:** FutureBuilt-Pilot für zirkuläres Bauen und großmaßstäbliche Bauteilwiederverwendung
- **Beteiligte People / Akteure:** Entra AS, MAD arkitekter, FutureBuilt, Asplan Viak, Insenti, Scenario Interiørarkitekter, IWG Group / Spaces
- **Architekt:** MAD arkitekter / Mad as
- **Tragwerksplaner:** unbekannt in den gesichteten Kurzquellen
- **Bauherr:** Entra AS
- **Zeitraum:** Fertigstellung 2021; Öffnung/Eröffnung 2021
- **Ursprüngliche Nutzung:** Bürogebäude der 1950er; donor materials aus anderen Abriss-/Umbauprojekten, u. a. Regjeringsbygg R4
- **Neue Nutzung:** Büro / flexible Arbeitsflächen, Spaces-Konzept
- **Fläche / Maßstab:** 4.297 m² total; 2.734 m² Originalgebäude; 708 m² Basement; 855 m² Extension
- **Schutzstatus / Denkmalstatus:** „vernestatus“ / Schutzstatus wird in norwegischer Quelle genannt; exakte Kategorie unbekannt
- **Quellenlage:** gut für Projektakteure, Flächen, reuse targets, HCS-Grunddaten; mittel für exakte Bauteillisten; schwach für Norm-/Prüfprotokolle und Detailstatik

---

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; in-situ transformiert; Bauteilwiederverwendung; adaptive reuse; Design-for-future-disassembly ergänzend
- **Hauptniveau:** Tragwerk, Gebäudehülle, räumlicher Innenausbau, technische Gebäudeausrüstung
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Erhaltene Bestandsstützen/Außenwände sind Bestandserhalt und werden nicht als Direct Reuse gewertet. Die donor-basierten Hohlkörperdecken, reused steel und weitere neu eingesetzte gebrauchte Bauteile zählen als Direct Reuse.
- **Warum ist der Fall relevant?** KA13 verbindet großmaßstäbliches Bauen, tragende concrete/steel component reuse, regulatorische Lernprozesse und viele fixed technical/spatial components.

---

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Hohlkörperdecken / hollow-core slabs | Stahlbeton/Spannbeton | Regjeringsbygg R4 / government quarter Oslo | Geschossdecken | Deckenelemente / floor separators in oberen Geschossen der Erweiterung | 21 Elemente; ca. 160 m²; 6,5 m Länge, 1,2 m Breite laut Thesis | ja | nein | nein | nein | Demontage, Reinigung, Tests, Zuschnitt | Auflager/Anschluss unbekannt | Site investigations/lab tests; SINTEF laut Thesis | Tragfähigkeit, Gebrauchstauglichkeit | TEK dokumentiert; NS 3682 später relevant | Demontage, Tests, Transport, Kosten | S3, S6, S7, S8 | genaue Prüfprotokolle |
| Stahlträger/-stützen reused | Stahl | teils Bestand, teils donor/surplus; genaue Quellen unbekannt | Tragwerk | Tragwerk/Erweiterung | ca. 75 % Stahl reused laut Norden | ja | nein | nein | nein | unbekannt | Bolting als future reuse strategy genannt | unbekannt | Tragfähigkeit | unbekannt | Dokumentation/Regelwerk | S2, S1 | genaue Tonnen/Profile |
| Bestehendes Tragwerk | Stahl/Beton unbekannt | Bestandsgebäude KA13 | Tragwerk | weiterhin Tragwerk | großer Teil erhalten | ja | nein | nein | nein | Verstärkung/Öffnungen teils | unbekannt | unbekannt | Tragfähigkeit Bestand | unbekannt | zählt nicht als Direct Reuse nach Grundregel | S2 | Eingriffe |
| Außenwände Bestand | Beton/Backstein laut Norden | Bestandsgebäude KA13 | Außenwand | weiterhin Außenwand | erhalten, mit Ausnahmen | nein/teilweise | nein | ja | nein | Öffnungen/Reparaturen | unbekannt | unbekannt | Hülle | unbekannt | Bestandserhalt nicht zählen | S2 | genaue Bauteile |
| Fassadenbekleidung / concrete plates and brick | Beton/Backstein | donor oder Bestand, genaue Herkunft unbekannt | Fassade | Fassade | unbekannt | nein | nein | ja | nein | unbekannt | unbekannt | unbekannt | Witterung, Brandschutz | unbekannt | passende Mengen/Qualität | S2 | Menge |
| Radiatoren | Metall | Bestand und/oder donor buildings | Heizung | Heizung | unbekannt | nein | nein | nein | ja | Ausbau, Wiedereinbau unbekannt | Rohranschlüsse | unbekannt | Heizleistung/Dichtheit | unbekannt | technische Gewährleistung | S1, S2 | Menge |
| Sanitär: Waschbecken, Toiletten | Keramik/Metall | donor/Bestand unbekannt | Sanitär | Sanitär | unbekannt | nein | ja | nein | ja | Reinigung, Ausbau, Wiedereinbau | Wasser/Abwasser | unbekannt | Hygiene, Dichtheit | unbekannt | Hygiene/Gewährleistung | S2, S5 | Menge |
| Lüftungskanäle / ducts and pipes | Metall/Kunststoff | donor/Bestand unbekannt | TGA | TGA | unbekannt | nein | nein | nein | ja | Reinigung/Anpassung unbekannt | Flansche/Verbindungen | unbekannt | Luftmenge, Hygiene | unbekannt | Passgenauigkeit | S2 | Menge |
| Office fronts / Innenverglasung | Glas/Alu/Stahl unbekannt | donor/Bestand | Bürofront | Bürofront/Innenraumtrennung | unbekannt | nein | ja | nein | nein | Anpassung | unbekannt | unbekannt | Schall/Brand unbekannt | unbekannt | Maße/Performance | S2 | Details |
| Türen | Holz/Metall/Glas unbekannt | donor/Bestand | Türen | Türen | unbekannt | nein | ja | teilweise | nein | Anpassung | Beschläge | unbekannt | Brandschutz/Schall/Fluchtweg | unbekannt | Nachweis | S2, S5 | Menge |
| Innere Oberflächen: Mosaikfliesen/Terrazzo | Stein/Keramik | Bestandsgebäude | Oberfläche/Treppe | erhaltene Oberfläche/Treppe | unbekannt | nein | ja | nein | nein | Restaurierung | - | unbekannt | Nutzung/Dauerhaftigkeit | Schutzstatus unbekannt | zählt als Bestandserhalt, nicht Direct Reuse | S2 | Umfang |
| Dachbegrünung / blau-grüne Lösungen | Substrat/Pflanzen | neu/vermutlich nicht reused | Dachökologie | Regenwasser/Biodiversität | über 50 norwegisch produzierte Arten laut FutureBuilt | nein | nein | ja | technisch | neu | - | unbekannt | Regenwasser/Biodiversität | unbekannt | nicht Direct Reuse | S1 | Details |

---

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Bestandsgebäude analysieren, wiederverwendbare Bauteile identifizieren | Entra, MAD, Asplan Viak, Insenti | circular building criteria | unbekannt | - | - | unbekannt | Bestand vor Ort | Bestandserhalt vs Reuse abgrenzen | getrennte Bewertung | S1 |
| Bauteilinventar | Donor-Bauteile aus Osloer Projekten suchen | Entra, Insenti, Rückbauakteure | donor building sourcing | unbekannt | selektiver Rückbau | unbekannt | Dokumentation | ca. 25 donor buildings/projects laut Sekundärquellen | Markt nicht etabliert | breite Suche und Koordination | S1, S9 |
| Schadstoffprüfung | HCS und andere Bauteile prüfen | unbekannt / SINTEF laut Thesis | technische Tests | unbekannt | - | Reinigung | site/lab tests | Transport ggf. zu Testort | Aufwand und Zusatztransport | Prüfung vor Wiedereinbau | S6, S7 |
| Rückbau | Hohlkörperdecken aus R4 demontieren | Rückbauunternehmen unbekannt | vorsichtiger Ausbau | unbekannt | selektiver Rückbau | Entfernen, Sichern | Zustand prüfen | kurze Osloer Wege möglich | Demontage anspruchsvoll | Bracing, drilling, cutting, hoisting laut Sekundärliteratur | S8 |
| Ausbau | Ausbau Radiatoren, Sanitär, Office fronts, Türen | unbekannt | selektiver Ausbau | unbekannt | selektiv | Reinigung/Anpassung | unbekannt | Donor-to-recipient | viele Einzelteile | Koordination durch reuse team | S1, S2 |
| Transport | HCS und andere Bauteile transportieren | unbekannt | Bauteiltransport | unbekannt | - | - | vor/nach Transport | donor sites in Oslo/Norwegen | Kosten/Emissionen/Bruchrisiko | lokale Quellen bevorzugt | S6, S8 |
| Lagerung | Zwischenlagerung von Bauteilen | unbekannt | unbekannt | unbekannt | - | - | unbekannt | unbekannt | Timing donor/recipient passt selten | unbekannt | - |
| Aufbereitung | HCS schneiden/reinigen; andere Bauteile anpassen | unbekannt | Verarbeitung gebrauchter Bauteile | unbekannt | - | cleaning, cutting, preparation | Tests | Werkstatt/Baustelle | Kosten 5–6× bei HCS | Pilotlernen, Standardisierung | S6, S8 |
| Planung | Entwurf und Nachweis für donor components | MAD, Engineers unbekannt, Asplan Viak, Entra | material-adaptive planning | unbekannt | - | - | TEK-Dokumentation | Planen mit vorhandenen Abmessungen | Regeln unklar | Workshops, rechtliche Beratung | S1, S2 |
| Genehmigung | Wiederverwendete Bauprodukte dokumentieren | Entra, Behörden, Berater | Nachweis nach Bauvorschriften | unbekannt | - | - | Dokumentation | - | Regelwerkslücke | Rechts-/Behördenkontakt, FutureBuilt-Pilot | S1, S2 |
| Wiedereinbau | HCS in oberen Geschossen, TGA/Innenbauteile montieren | Bauunternehmen unbekannt | konventionelle Montage mit Reuse-Bauteilen | unbekannt | - | vorbereitet | Abnahme unbekannt | Baustellenkoordination | Passgenauigkeit | Zuschnitt/Anpassung | S6 |
| Monitoring | Erfahrungen und Emissionswirkung dokumentieren | Entra, FutureBuilt, Asplan Viak | Erfahrungsbericht / LCA | LCA-Tools unbekannt | - | - | Kennwertprüfung | - | Datenqualität | Findings report | S1, S5 |

---

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Bestandstragwerk + Erweiterung mit reused HCS und steel | Tragfähigkeit, Nutzlasten Büro | TEK; genaue Normen unbekannt | Dokumentation und Tests | Bestand + donor-Komponenten | angepasste Planung | S2, S6 |
| Lastabtragung | HCS als Geschossdecken der oberen Geschosse | Biegung, Schub, Durchbiegung, Risse | TEK; NS 3682 später relevant | site/lab tests, crack/load tests laut Thesiskontext | gebrauchte HCS beschädigungsanfällig | Tests, Zuschnitt, neue Auflager | S3, S6 |
| Verbindung | Bolting steel als spätere Wiederverwendbarkeit genannt | Demontierbarkeit und Tragfähigkeit | unbekannt | unbekannt | geschweißte/alte Verbindungen | Schraubverbindungen wo möglich | S1, S5 |
| Brandschutz | unbekannt | Bürogebäude | unbekannt | unbekannt | reused doors/fronts können Nachweis brauchen | unbekannt | - |
| Schallschutz | Office fronts/doors und HCS relevant | Schallanforderungen Büro | unbekannt | unbekannt | gebrauchte Bauteile haben unbekannte Performance | unbekannt | - |
| Feuchte | Dachbegrünung/blue-green roof | Feuchte-/Wassermanagement | unbekannt | unbekannt | nicht Direct Reuse | innovative Regenwasserlösung | S1 |
| Wärmeschutz | Fassade/Bestand saniert; reused cladding teils | Energieanforderung | unbekannt | unbekannt | Bestand + reused Teile | unbekannt | S2 |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | - |
| Luftdichtheit | unbekannt | unbekannt | unbekannt | unbekannt | alte Fassaden-/Türteile | unbekannt | - |
| TGA-Integration | Reused radiators, ducts, pipes, sanitary equipment | Leistung, Hygiene, Dichtheit | unbekannt | unbekannt | Kompatibilität | Anpassung/Wiedereinbau | S2 |
| Barrierefreiheit | unbekannt | aktuelle Bauanforderungen | unbekannt | unbekannt | Bestandsgebäude | unbekannt | - |
| Dauerhaftigkeit | HCS reuse möglich, aber Demontage anspruchsvoll | Restlebensdauer | NS 3682 später relevant | tests/documentation | Schäden beim Ausbau | Standardisierung und Prüfungen | S3 |
| Wartung | circular maintenance angekündigt | zukünftiger Wiedergebrauch | unbekannt | Dokumentation/Traceability | Bauteiltracking | Dokumentation und demontierbare Details | S1 |
| Zulassung | Regelwerk damals unsicher | Bauproduktnachweis | TEK; regulatorische Diskussion | Dokumentation | keine Routine für Reuse-Bauprodukte | FutureBuilt-Pilot, Behörden-/Rechtsexpertise | S1, S2 |
| Haftung | Client/Projektteam musste Verantwortung klären | Haftung für wiederverwendete Produkte | unbekannt | Nachweise | fehlende Marktakteure/Garantien | Entra engagierte Rechts-/Regelwerksakteure laut Norden | S2 |

---

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Gesamtfläche | 4.297 | m² | Projektangabe FutureBuilt | Gesamtgebäude | S1 | belegt |
| Originalgebäude | 2.734 | m² | Projektangabe FutureBuilt | Bestand | S1 | belegt |
| Basement | 708 | m² | Projektangabe FutureBuilt | Untergeschoss | S1 | belegt |
| Extension | 855 | m² | Projektangabe FutureBuilt | Erweiterung | S1 | belegt |
| Ziel Reuse-Anteil | mindestens 50 | % | FutureBuilt-Kriterium/Ziel | Materialien | S1 | belegt |
| Erreichter Reuse-Anteil | bis/nahe 80 | % | FutureBuilt/Entra/Norden; vermutlich Gewicht | Gesamtmaterial | S1, S2, S4 | belegt |
| Treibhausgasreduktion | 70 | % | Vergleich Neubau; Methode im Kurztext nicht vollständig | Materialien/Gebäude | S1, S4 | teilweise belegt |
| Hohlkörperdecken | 21 | Stück | Thesis-/Sekundärquelle | HCS aus R4 | S6 | teilweise belegt |
| Hohlkörperdeckenfläche | ca. 160 | m² | Thesis-/Sekundärquelle | HCS aus R4 | S6 | teilweise belegt |
| HCS-Abmessung | 6,5 × 1,2 | m | Thesis-/Sekundärquelle | HCS | S6 | teilweise belegt |
| CO₂-Reduktion HCS gegenüber neu | 89 | % | Umweltanalyse laut Thesis | Hohlkörperdecken | S6 | teilweise belegt |
| Kosten HCS gegenüber neu | 5–6× | Faktor | Thesis/Sekundärliteratur | Hohlkörperdecken | S6, S8 | teilweise belegt |
| Stahl reused | ca. 75 | % | Norden case | Stahl | S2 | teilweise belegt |
| Abfallmaximum Ziel | 20 | kg/m² | FutureBuilt | Baustellenabfall exkl. demolition | S1 | belegt |
| Anzahl donor buildings/projects | ca. 25 | Stück | Sekundärquellen | Materialherkunft | S9 | teilweise belegt |
| U-Wert | unbekannt | - | - | - | - | unbekannt |
| Lebensdauer | unbekannt | - | - | - | - | unbekannt |
| Kosten Gesamtprojekt | unbekannt | - | - | - | - | unbekannt |

---

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Regelwerksunsicherheit | rechtlich | Reuse-Bauprodukte nicht Routine | Genehmigungs- und Haftungsrisiko | Recht, Norm, Prüfung | FutureBuilt-Pilot, Dokumentation, Workshops | frühe Behörden- und Rechtsklärung nötig | S1, S2 |
| HCS-Demontage anspruchsvoll | technisch/logistisch | vorgespannte Fertigteile nicht für Ausbau geplant | Kosten, Bruchrisiko, Zeitaufwand | Bauteil, Abbruchmethode, Prüfung | vorsichtiger Rückbau, Tests, Standardentwicklung | Design for disassembly für künftige HCS wichtig | S3, S8 |
| HCS-Kosten höher | wirtschaftlich | Pilotprozess, Tests, Transport, Zuschnitt, Design | 5–6× gegenüber neu laut Thesis | Wirtschaft, Bauteil | Lernen, Standardisierung, lokale Quellen | Pilotkosten nicht mit Serienkosten gleichsetzen | S6, S8 |
| Marktverfügbarkeit | logistisch/wirtschaftlich | kein ausgereifter Reuse-Markt | Materialsuche aus ca. 25 Quellen | Bauteilbörse, Logistik | breites donor sourcing | Reuse braucht Plattformen und Koordinatoren | S1, S9 |
| Dokumentation | rechtlich/technisch | Herkunft, Leistung, Produktdaten fehlen | Nachweise aufwendig | Prüfung, Datenmodell | Traceability/Dokumentation | Materialpässe erleichtern Reuse | S1 |
| Bestandserhalt vs Direct Reuse | methodisch | Bestand bleibt vor Ort | Bewertungsrisiko | Reuse-Strategie, Gebäude | donor-Bauteile separat ausweisen | retained structure nicht als Direct Reuse zählen | eigene Bewertung nach S2 |
| TGA-Kompatibilität | technisch | alte Radiatoren/ducts/pipes müssen passen | Anpassungsaufwand | TGA, Verbindung | Reinigung/Anpassung | technische Reuse-Bauteile früh prüfen | S2 |

---

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** breit angelegte Suche nach donor materials aus eigenen und fremden Projekten; Koordination über Entra, Insenti/Reuse-Beratung und Projektteam.
- **Bauteilbörse / Quelle:** keine einzelne Bauteilbörse als Hauptquelle belegt; donor buildings/projects, recycling centres und surplus/new-old-stock von Herstellern werden in Sekundärquellen genannt.
- **Kostenwirkung:** HCS-Pilot laut Thesis 5–6× teurer als neue HCS; Gesamtprojektkosten und Wirtschaftlichkeit unbekannt.
- **Zeitwirkung:** erhöhter Planungs-, Rückbau-, Prüf- und Koordinationsaufwand; genaue Zeitwerte unbekannt.
- **Versicherung / Haftung:** konkrete Versicherungen unbekannt; regulatorische/haftungsbezogene Klärung war eine zentrale Hürde.
- **Gewährleistung:** unbekannt
- **Arbeitsaufwand:** sehr hoch durch Suche, Dokumentation, Tests, Umbau, Anpassung und Genehmigung.
- **Lagerung:** Zwischenlagerung wahrscheinlich, aber Ort/Umfang unbekannt.
- **Marktbarrieren:** fehlende standardisierte Produktnachweise, geringe Marktreife, ungesicherte Gewährleistung, hohe Pilotkosten.

---

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** mittel bis hoch; historische Oberflächen wie Mosaikfliesen/Terrazzo und verschiedene reused components tragen zur Identität bei; technische/strukturelle Reuse teils nicht direkt sichtbar.
- **räumliche Transformation:** Bürogebäude aus den 1950er-Jahren wird in ein modernes Arbeitsgebäude mit Erweiterung überführt.
- **Atmosphäre / Ausdruck:** Mischung aus vorhandener 1950er-Jahre-Substanz, wiederverwendeten Bauteilen und neuer Erweiterung.
- **Umgang mit Spuren:** Bestandsspuren werden laut Norden sichtbar erhalten; donor Bauteilspuren im Detail unbekannt.
- **sozialer Wert:** Pilotprojekt mit Branchenwirkung und Regelwerksimpuls in Norwegen.
- **Denkmal- oder Bestandswert:** Schutz-/Vernestatus genannt; exakte Kategorie unbekannt.
- **Kritik / Grenzen:** Hoher Anteil Bestandserhalt darf nicht mit Direct Reuse verwechselt werden; HCS-Kosten zeigen Pilotcharakter; einige Daten bleiben sekundär.

---

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** exakter Tragwerksplaner, Prüfberichte der HCS, Brandschutz-/Schallschutznachweise, genaue Bauteilliste aller donor components, Vertrags-/Haftungsmodell, Lagerlogistik.
- **Sinnvolle neue Entitäten:** Donor Building, Reuse-Koordinator, Regelwerks-Pilot, Ombruksgrad/Reuse-by-weight.
- **Fehlende Daten:** vollständige Materialdatenbank, Bauteilherkunft je Element, Rückbauprotokolle, Kostenaufschlüsselung, Nachweise für TGA und Türen, Langzeitmonitoring.
- **Zu prüfende Quellen:** FutureBuilt Findings Report, Entra experience report, Asplan Viak LCA, Bauaufsicht Oslo, SINTEF-Prüfunterlagen, NS 3682 Hintergrunddokumente.

---

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja

### 5 wichtigste Fakten

1. KA13 wurde 2021 fertiggestellt und gilt als norwegischer Großmaßstab-Pilot für Reuse.
2. Gesamtfläche: 4.297 m².
3. Bis/nahe 80 % Wiederverwendung und 70 % Emissionsreduktion werden publiziert.
4. 21 Hohlkörperdecken aus Regjeringsbygg R4 wurden als tragende Bauteile wiederverwendet.
5. Bestandserhalt ist wichtig, aber für diese Bewertung nur donor-/transformierte Bauteile zählen.

### 5 wichtigste Bauteile

1. Wiederverwendete Hohlkörperdecken
2. Wiederverwendeter Stahl
3. Wiederverwendete Radiatoren
4. Wiederverwendete Sanitär- und Lüftungselemente
5. Wiederverwendete Bürofronten/Türen/Fassadenbekleidung

### 5 wichtigste Hürden

1. Regelwerks- und Dokumentationsunsicherheit
2. Demontage und Prüfung vorgespannter Hohlkörperdecken
3. Hohe Pilotkosten für HCS-Reuse
4. Marktverfügbarkeit und donor sourcing
5. Trennung von Bestandserhalt und echter Bauteilwiederverwendung

### 5 wichtigste übertragbare Erkenntnisse

1. Hohlkörperdecken können als tragende Bauteile wiederverwendet werden.
2. Reuse-Koordination ist eine eigene Projektleistung.
3. Rechtliche und technische Dokumentation muss Teil des Entwurfsprozesses sein.
4. Pilotprojekte können Standards und Regeländerungen anstoßen.
5. Bestandserhalt und Direct Reuse müssen methodisch getrennt bilanziert werden.

### 5 offene Fragen

1. Welche exakten Prüfergebnisse liegen für jedes HCS-Element vor?
2. Welche Profile/Mengen umfasst der wiederverwendete Stahl?
3. Welche Bauteile stammen aus welchen 25 donor buildings/projects?
4. Wie wurden Haftung und Gewährleistung vertraglich verteilt?
5. Wie entwickeln sich Betrieb, Wartung und Rückbaubarkeit nach mehreren Jahren?

---

## Quellen und Links

- **S1 – FutureBuilt: Kristian Augusts gate 13, Oslo.** https://www.futurebuilt.no/forbildeprosjekter/kristian-augusts-gate-13-oslo
- **S2 – Nordic Council of Ministers / Norden: Best Practice Catalogue, Kristian August gate 13.** https://pub.norden.org/us2024-461/25-kristian-august-gate-13.html
- **S3 – NMBU thesis: Muligheter med ombruk av prefabrikkerte betongelementer.** https://nmbu.brage.unit.no/nmbu-xmlui/handle/11250/3079873
- **S4 – Entra press release via NTB: Öffnung KA13.** https://kommunikasjon.ntb.no/pressemelding/17906148/kommunalministeren-apnet-norges-forste-storskala-ombruksbygg?publisherId=16126567
- **S5 – FutureBuilt Findings Report PDF: Reuse and transformation / KA13.** https://www.futurebuilt.no/assets/originals/download/75a48b7634efe5970abe0f09403f3e45.pdf
- **S6 – University thesis excerpt on reused HCS in KA13.** https://uis.brage.unit.no/uis-xmlui/bitstream/handle/11250/3136867/no.uis%3Ainspera%3A232787794%3A233624667.pdf
- **S7 – UiT thesis / HCS tests and reuse context.** https://munin.uit.no/bitstream/handle/10037/23335/thesis.pdf
- **S8 – ResearchGate: The Renaissance of Reuse in Norway.** https://www.researchgate.net/publication/387845453_The_Renaissance_of_Reuse_in_Norway_The_Future_Is_Back
- **S9 – CIRCON examples: KA13.** https://circon.graennibyggd.is/en/examples/
