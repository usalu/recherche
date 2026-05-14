---
entity: "quelle"
id: "Geb_ude_KA13_Kristian_Augusts_gate_13_Oslo_md"
title: "Geb_ude_KA13_Kristian_Augusts_gate_13_Oslo_md"
build_status: "promoted_phase42"
source_filename: "KA13_Kristian_Augusts_gate_13_Oslo.md"
---

# Geb_ude_KA13_Kristian_Augusts_gate_13_Oslo_md

**Arbeitsstand:** 2026-05-06  
**Sprache:** Deutsch  
**Grundregel:** Gewertet werden nur wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Reiner Bestandserhalt wird nicht als Direct Reuse gewertet, wenn Bauteile am Ort bleiben und dieselbe Funktion behalten.

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

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; in-situ transformiert; Bauteilwiederverwendung; adaptive reuse; Design-for-future-disassembly ergänzend
- **Hauptniveau:** Tragwerk, Gebäudehülle, räumlicher Innenausbau, technische Gebäudeausrüstung
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Erhaltene Bestandsstützen/Außenwände sind Bestandserhalt und werden nicht als Direct Reuse gewertet. Die donor-basierten Hohlkörperdecken, reused steel und weitere neu eingesetzte gebrauchte Bauteile zählen als Direct Reuse.
- **Warum ist der Fall relevant?** KA13 verbindet großmaßstäbliches Bauen, tragende concrete/steel component reuse, regulatorische Lernprozesse und viele fixed technical/spatial components.

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

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** exakter Tragwerksplaner, Prüfberichte der HCS, Brandschutz-/Schallschutznachweise, genaue Bauteilliste aller donor components, Vertrags-/Haftungsmodell, Lagerlogistik.
- **Sinnvolle neue Entitäten:** Donor Building, Reuse-Koordinator, Regelwerks-Pilot, Ombruksgrad/Reuse-by-weight.
- **Fehlende Daten:** vollständige Materialdatenbank, Bauteilherkunft je Element, Rückbauprotokolle, Kostenaufschlüsselung, Nachweise für TGA und Türen, Langzeitmonitoring.
- **Zu prüfende Quellen:** FutureBuilt Findings Report, Entra experience report, Asplan Viak LCA, Bauaufsicht Oslo, SINTEF-Prüfunterlagen, NS 3682 Hintergrunddokumente.

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
