---
id: "Upcycle_Studios_Copenhagen"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "Upcycle Studios, Copenhagen — Fallstudie Bauteilwiederverwendung / Direct Reuse"
bauobjekt:
  - "Upcycle_Studios_Copenhagen"
legacy_paths:
  - "Gebäude\\Upcycle_Studios_Copenhagen.md"
projekt:
  - "Upcycle_Studios_Copenhagen"
reuse_chain_detected: "False"
---
# Upcycle Studios, Copenhagen — Fallstudie Bauteilwiederverwendung / Direct Reuse

## Migration

- Fallstudie ID: Upcycle_Studios_Copenhagen
- Legacy source count: 1
- Generated project: Upcycle_Studios_Copenhagen
- Generated bauobjekt: Upcycle_Studios_Copenhagen
- Extracted reuse_einsatz rows: 9
- Extracted datenpunkt rows: 17
- Extracted entity mapping rows: 20
- Reuse chain detected: False

## Legacy Content

### Legacy Source: Gebäude\Upcycle_Studios_Copenhagen.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Upcycle_Studios_Copenhagen
- Secondary targets: projekt/Upcycle_Studios_Copenhagen; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Upcycle Studios, Copenhagen — Fallstudie Bauteilwiederverwendung / Direct Reuse

## 1. EINORDNUNG

- **Entscheidung:** VERGLEICHSFALL
- **Bewertung:** ★★★☆☆
- **Begründung:** Gebautes Wohnprojekt mit nachweislich wiederverwendeten Fenstern und wiederverwendeten / upgecycelten Holzbauteilen sowie recyceltem Beton. Als Direct Reuse zählen vor allem die fest eingebauten Fenster und Holzbauteile; Beton aus Metroabbruch ist eher Materialrecycling / Materialwiederverwendung und nicht Bauteilwiederverwendung im engeren Sinn.
- **Vertrauensgrad:** teilweise belegt
- **Warnung Bestandserhalt:** nein
- **Warnung Möbel/Dekoration:** nein
- **Projektstatus:** gebaut / fertiggestellt 2018 nach NREP; a:gain nennt 2019 als „year finished“

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Upcycle Studios | untersuchter Fall | NREP; Lendager; a:gain | belegt | 20 Reihenhäuser in Ørestad |
| Ort | Ørestad, Copenhagen, DK | Standort | NREP; Ellen MacArthur Foundation | belegt | Schreibweisen: Ørestad / Orestad / Oerestad |
| Projekt | 20 row houses / terraced houses | Bauprogramm | NREP; a:gain | belegt | Wohnen + Arbeiten |
| Gebäude | Reihenhausensemble | Zielgebäude | NREP | belegt | 3.440 m² laut NREP; 3.909 m² laut Lendager |
| People | NREP, AG Gruppen, Lendager, MOE, Artelia, BOGL | Beteiligte | NREP; Lendager; a:gain | teilweise belegt | Rollen variieren je Quelle |
| Architekt | Lendager / Lendager Group | Entwurf | NREP; a:gain; Lendager | belegt |  |
| Bauherr | NREP / AG Gruppen | Entwickler / Eigentümer | NREP; a:gain | belegt |  |
| Tragwerksplaner | MOE | beratender Ingenieur | NREP | teilweise belegt | konkrete Tragwerksrolle unbekannt |
| Reuse-Strategie | Upcycling / reuse of existing materials | zentrale Strategie | Lendager; NREP; EMF | belegt | Materialentwicklung und Remanufacturing |
| Bauteil | Double-glazed windows | wiederverwendete Hüllenbauteile | a:gain; EMF; Lendager | belegt | 75 % der Fenster aus öffentlichen Wohnbauten Nordjütlands laut a:gain/EMF |
| Bauteil | discarded floorboards / Dinesen offcuts | Boden/Wand/Fassade | Lendager; a:gain; EMF | teilweise belegt | teils Reststrom statt gebrauchtes Bauteil |
| Material | recycled/upcycled concrete from Copenhagen Metro | Beton / Materialrecycling | NREP; EMF; a:gain | belegt, aber Mengenkonflikt | 904 t, 1000 t oder 1400 tons je Quelle |
| Kennwert | 32 % CO₂-Reduktion bei Materialien | LCA-Kennwert | NREP | teilweise belegt | Methode nicht im Detail geprüft |
| Kennwert | 45 % CO₂-Einsparung über 50 Jahre inkl. Betrieb | LCA-Kennwert | NREP; Lendager | teilweise belegt | Vergleichsszenario laut Quelle, Details offen |
| Kennwert | 914.000 kg waste saved | Abfallvermeidung | a:gain | teilweise belegt | interne Berechnung |
| Hürde | Remanufacturing auf Neubaustandard | technische/wirtschaftliche Hürde | Lendager | teilweise belegt | Qualität, Funktion, Ästhetik wie neu |
| Prüfung | unbekannt | technische Zulassung/Tests | keine spezifische Quelle gefunden | unklar | besonders Fenster relevant |
| Norm | unbekannt | bauordnungsrechtliche Anforderungen | keine spezifische Quelle gefunden | unklar | keine Normnummern erfinden |
| Recht | unbekannt | Haftung/Gewährleistung | keine spezifische Quelle gefunden | unklar |  |
| Software | unbekannt | LCA / Materialerfassung | NREP erwähnt LCA, Tool unbekannt | unklar |  |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Remanufacturing | Upcycle Studios nutzt gebrauchte/restliche Produkte, die für Neubaustandard aufbereitet werden | gebrauchte Fenster „processed before use“ | Aufbereitungsmethode, Prüfung, Leistungsanforderung |
| Upcycled product stream | mehrere Bauteile sind nicht direkt aus einem Gebäude übernommen, sondern industriell aufbereitet | Dinesen-Offcuts als Boden/Wand/Fassade | Material, Bauteil, Wirtschaft |
| Quellenkonflikt Kennwert | zentrale Mengen variieren zwischen 904 t, 1000 t und 1400 tons | Metro-Beton | Kennwert, Datenmodell |

## 3. FALLSTUDIE

- **Name:** Upcycle Studios
- **Ort:** Ørestad / Orestad, Copenhagen, Denmark
- **Gebäude:** Reihenhausensemble / 20 terraced houses
- **Projekt:** kommerziell skaliertes zirkuläres Wohnprojekt mit Wohn-/Arbeitsnutzung
- **Beteiligte People / Akteure:** NREP, AG Gruppen, Lendager, MOE, Artelia, BOGL; a:gain/Lendager UP als Materialakteur in späterer Referenzkommunikation
- **Architekt:** Lendager / Lendager Group
- **Tragwerksplaner:** MOE laut NREP; konkrete Prüf-/Tragwerksdetails unbekannt
- **Bauherr:** NREP / AG Gruppen
- **Zeitraum:** 2015–2018 laut Lendager; Fertigstellung 2018 laut NREP; a:gain nennt 2019
- **Ursprüngliche Nutzung:** nicht zutreffend als Neubauprojekt; Spenderquellen u. a. öffentliche Wohnbauten in Nordjütland, Copenhagen Metro, Dinesen-Produktionsreste
- **Neue Nutzung:** Wohnen mit Möglichkeit zur Arbeit im Haus
- **Fläche / Maßstab:** 3.440 m² laut NREP; 3.909 m² laut Lendager; Quellenkonflikt
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** gut für Projektbasis und Hauptmaterialien; mittel für technische Nachweise und genaue Mengen

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung für Fenster; Materialwiederverwendung / Upcycling für Holz und Beton; Recyclinganteile vorhanden
- **Hauptniveau:** Gebäudehülle / räumlicher Innenausbau / Material
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Das Projekt ist Neubau. Wiederverwendung zählt für Fenster und fest verbaute Holzbauteile. Der Beton aus Metroabfällen ist eher recycelter Zuschlag / Materialrecycling und wird nicht als Direct Reuse von Bauteilen gewertet.
- **Warum ist der Fall relevant?** Upcycle Studios ist ein frühes, kommerziell realisiertes Wohnprojekt, das Wiederverwendung in Wohnungsbau und LCA-Kommunikation überführt, aber unter der strengen Direct-Reuse-Regel nur mittel zu bewerten ist.

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fenster / Doppelverglasung | Glas, Rahmen unbekannt | öffentliche Wohnbauten in Nordjütland | Fenster | Fenster / Gebäudehülle | 75 % der Fenster laut a:gain/EMF | nein | nein | ja | nein | Aufbereitung, Remanufacturing | unbekannt | unbekannt | Wärme, Dichtheit, Windlast, Bedienbarkeit | unbekannt | Produktdaten, Maße, Gewährleistung | a:gain; EMF; Lendager | U-Wert, Anzahl |
| Bodenbretter / Dinesen-Restholz | Holz | Dinesen floor production offcuts / surplus wood | Produktionsrest / Bodenholz | Böden, Wände, Fassaden | unbekannt | nein/teilweise unbekannt | ja | teilweise | nein | Remanufacturing / Zuschnitt | unbekannt | unbekannt | Dauerhaftigkeit, Brandschutz, Feuchte | unbekannt | Reststrom statt direct reuse | Lendager; a:gain; EMF | Mengen, Schichten |
| Fassadenholz | Holz | Dinesen-Offcuts / discarded wood | Produktionsrest | Fassade / Verkleidung | unbekannt | nein | nein | ja | nein | Aufbereitung | unbekannt | unbekannt | Witterung, Brandschutz | unbekannt | Dauerhaftigkeit | a:gain; EMF | Befestigung |
| Beton | recycelter Beton / Zuschlag | Copenhagen Metro construction waste | Betonabfall | Beton in Neubau | 904 t laut NREP; 1000 t laut a:gain; 1400 tons laut EMF/Circulary | ja, aber als Recyclingmaterial | nein | nein | nein | Zerkleinern, neues Betonieren | neu | unbekannt | Tragfähigkeit, Rezeptur | unbekannt | nicht Direct Reuse; Mengenkonflikt | NREP; a:gain; EMF | Methode |
| Solarzellen | unbekannt | neu oder unbekannt | - | Energieerzeugung | vorhanden, Menge unbekannt | nein | nein | nein | ja | unbekannt | unbekannt | unbekannt | elektrische Leistung | unbekannt | kein Reuse-Beleg | NREP/EMF | Reuse nein |
| Wärmepumpen | unbekannt | unbekannt | - | Energieversorgung | vorhanden | nein | nein | nein | ja | unbekannt | unbekannt | unbekannt | Betrieb/Effizienz | unbekannt | kein Reuse-Beleg | NREP | Reuse nein |
| Türen | unbekannt | unbekannt | unbekannt | Türen | unbekannt | nein | ja | teilweise | nein | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine Belege | - | alles |
| Treppen | unbekannt | unbekannt | unbekannt | Erschließung | unbekannt | unbekannt | ja | nein | nein | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine Reuse-Belege | - | alles |
| Sanitär / Beleuchtung / TGA | unbekannt | unbekannt | unbekannt | Technik | unbekannt | nein | nein | nein | ja | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine Reuse-Belege | - | alles |

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | potenzielle Materialströme identifizieren | Lendager, NREP, AG Gruppen | Materialmapping | unbekannt | unbekannt | unbekannt | unbekannt | lokal/regional | ausreichende Menge in Wohnungsbau | mehrere Stoffströme kombinieren | Lendager; EMF |
| Bauteilinventar | Fenster, Holzreste, Betonabfälle bewerten | Lendager / Materialpartner | Upcycling-Analyse | unbekannt | selektiver Ausbau bei Spenderfenstern unbekannt | Remanufacturing | unbekannt | Quellen Nordjütland/Kopenhagen | Maße und Qualität | Aufbereitung auf Neubaustandard | a:gain; Lendager |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine öffentlichen Angaben | unbekannt | unbekannt |
| Rückbau | Fenster aus Wohnbauten und Beton aus Metrobaustelle gewinnen | Spender-/Rückbauakteure unbekannt | selektive Materialgewinnung | unbekannt | unbekannt | unbekannt | unbekannt | Transport nach Ørestad | Timing / Qualität | unbekannt | EMF; a:gain |
| Ausbau | Fenster demontieren | unbekannt | Demontage | unbekannt | unbekannt | unbekannt | unbekannt | Nordjütland → Copenhagen | Bruchrisiko | unbekannt | EMF |
| Transport | Fenster/Holz/Beton zum Projekt | unbekannt | unbekannt | unbekannt | - | - | - | Dänemark | Transportbilanz unbekannt | unbekannt | Quellen nennen Herkunft |
| Lagerung | Zwischenlagerung vor Aufbereitung | unbekannt | unbekannt | unbekannt | - | - | - | unbekannt | unbekannt | unbekannt | unbekannt |
| Aufbereitung | Fenster/Holz so aufbereiten, dass sie wie neu funktionieren | Materialpartner / Lendager | Remanufacturing | unbekannt | - | Reinigen, Reparieren, Zuschnitt | unbekannt | Werkstatt unbekannt | technische Performance | Qualitätsangleichung an Neuware | Lendager |
| Planung | Reihenhäuser auf verfügbare Bauteile abstimmen | Lendager, NREP, AG Gruppen | zirkulärer Materialentwurf | LCA, Tool unbekannt | - | - | LCA | - | Skalierung in kommerziellem Projekt | Materialinnovationen | NREP; Lendager |
| Genehmigung | unbekannt | unbekannt | regulär | unbekannt | - | - | unbekannt | - | gebrauchte Bauteile | unbekannt | unbekannt |
| Wiedereinbau | Fenster, Holzbauteile, Beton einbauen | AG Gruppen, Fachunternehmen | Neumontage | unbekannt | - | - | unbekannt | Baustelle Ørestad | Gewährleistung | unbekannt | NREP |
| Monitoring | LCA und CO₂-Kennwerte ausweisen | NREP / Projektteam | LCA / LCC | Tool unbekannt | - | - | LCA | - | Bilanzgrenze verstehen | 32 % / 45 % Kennwerte | NREP |

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Beton wird mit recyceltem Zuschlag hergestellt; kein Direct-Reuse-Tragwerk belegt | Tragfähigkeit | unbekannt | unbekannt | recyceltes Material im Beton | neues Betonieren nach Rezeptur; Details unbekannt | NREP |
| Lastabtragung | Lastpfade unbekannt | statischer Nachweis | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Verbindung | Fenster-/Fassadenanschlüsse unbekannt | Dichtheit, Windlast | unbekannt | unbekannt | gebrauchte Fenstermaße | Remanufacturing | Lendager |
| Brandschutz | Holz in Böden/Wänden/Fassaden relevant | Brandschutz | unbekannt | unbekannt | Holzreststoffe in Neubau | unbekannt | unbekannt |
| Schallschutz | keine Daten | Wohnstandard | unbekannt | unbekannt | gebrauchte Fenster/Bauteile | unbekannt | unbekannt |
| Feuchte | Fenster/Fassadenholz relevant | Feuchte- und Wetterschutz | unbekannt | unbekannt | gebrauchte Fenster und Holz | Aufbereitung | Lendager |
| Wärmeschutz | Fenster und Gebäudehülle entscheidend; keine U-Werte gefunden | Energieeffizienz | unbekannt | unbekannt | alte Fensterqualität | aufbereitet, Performance unbekannt | Lendager |
| Wärmebrücken | unbekannt | vermeiden | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Luftdichtheit | unbekannt | Wohnkomfort/Energie | unbekannt | unbekannt | gebrauchte Fensteranschlüsse | unbekannt | unbekannt |
| TGA-Integration | Solarzellen und Wärmepumpen genannt | Energieversorgung | unbekannt | unbekannt | Integration in Reihenhäuser | Neubau-TGA | NREP |
| Barrierefreiheit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Dauerhaftigkeit | Remanufacturing soll Qualität wie neu sichern | Nutzungsdauer | unbekannt | unbekannt | gebrauchte Fenster/Holz | Aufarbeitung | Lendager |
| Wartung | keine Details | Instandhaltung | unbekannt | unbekannt | gemischte Materialquellen | unbekannt | unbekannt |
| Zulassung | keine Details | Konformität | unbekannt | unbekannt | sekundäre Bauteile | unbekannt | unbekannt |
| Haftung | keine Details | Gewährleistung | unbekannt | unbekannt | gebrauchte Bauteile im kommerziellen Projekt | unbekannt | unbekannt |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Reihenhäuser | 20 | Stück | Projektangabe | Projekt | NREP; a:gain; EMF | belegt |
| Fläche | 3.440 | m² | Projektangabe | Projekt | NREP | belegt |
| Fläche | 3.909 | m² | Projektangabe | Projekt | Lendager | belegt, aber Konflikt |
| Fertigstellung | 2018 | Jahr | Projektangabe | Projekt | NREP; EMF | belegt |
| Fertigstellung | 2019 | Jahr | Projektangabe | Projekt | a:gain | Konflikt |
| Fenster wiederverwendet | 75 | % der Fenster | unbekannt | Fenster | a:gain; EMF | belegt |
| Upcycled/recycled Anteil | > 2/3 | Anteil Gebäude | Projektangabe | Gesamtgebäude | NREP | teilweise belegt |
| Beton aus Metro-Abfall | 904 | t | unbekannt | Betonmaterial | NREP | belegt |
| Beton aus Metro-Abfall | 1000 | t | interne Berechnung | Betonmaterial | a:gain | Konflikt |
| Beton aus Metro-Abfall | 1400 tons / ca. 1270 t | tons/t | unbekannt | Betonmaterial | EMF | Konflikt |
| Abfall vermieden | 914.000 | kg | interne Berechnung | Projekt | a:gain | teilweise belegt |
| CO₂-Reduktion Materialien | 32 | % | LCA | Materialphase | NREP | teilweise belegt |
| CO₂-Einsparung über 50 Jahre | 45 | % | LCA/LCC | embodied + operation, 50 Jahre | NREP; Lendager | teilweise belegt |
| CO₂-Footprint | 53.182 | kg CO₂e | interne Berechnung | unbekannt | a:gain | unklar |
| Kosten | unbekannt | - | - | - | - | unklar |
| U-Wert | unbekannt | W/m²K | - | Fenster/Fassade | - | unklar |
| Lebensdauer | 50 | Jahre | LCA-Annahme | Betrachtungszeitraum | NREP | teilweise belegt |

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Technische Performance gebrauchter Fenster | technisch | gebrauchte Fenster müssen Neubaustandard erreichen | Aufbereitung und Nachweis nötig | Bauteil, Prüfung, Leistungsanforderung | Remanufacturing | Bauteile brauchen industriell skalierbare Aufbereitung | Lendager |
| Mengenkonflikte / Dateninkonsistenz | datenbezogen | verschiedene Quellen nennen 904 t, 1000 t, 1400 tons Beton | erschwert Bewertung | Kennwert, Datenmodell | Werte getrennt dokumentieren | Quellenkonflikte nicht glätten | NREP; a:gain; EMF |
| Beton ist Recycling, nicht Direct Reuse | methodisch | Material wird neu verarbeitet | kann Fall überbewerten | Material, Reuse-Strategie | getrennte Bewertung | Bauteilreuse und Materialrecycling trennen | eigene Bewertung nach Grundregel |
| Skalierung im Wohnungsbau | wirtschaftlich/logistisch | 20 Reihenhäuser brauchen verlässliche Serien | Materialquellen und Standardisierung nötig | Wirtschaft, Logistik | Kombination mehrerer Stoffströme | kommerzieller Reuse braucht Produktisierung | NREP; Lendager |
| Gewährleistung | rechtlich/wirtschaftlich | gebrauchte Komponenten | Risiko für Bauherr und Nutzer | Recht, Wirtschaft | unbekannt | fehlende Haftungsdaten als Datenlücke markieren | keine Quelle |
| Wärme-/Schallschutz | technisch | gebrauchte Fenster und Holzbauteile | Nachweise nötig | Leistungsanforderung | unbekannt | technische Daten müssen offengelegt werden | keine Quelle |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** projektbezogene Beschaffung von gebrauchten und Restmaterialien; Kooperation mit Material-/Produktionsquellen; Remanufacturing.
- **Bauteilbörse / Quelle:** keine klassische Börse belegt; Quellen: öffentliche Wohnbauten Nordjütlands, Copenhagen Metro, Dinesen-Produktion.
- **Kostenwirkung:** NREP nennt LCA/LCC und positive Umwelt- sowie Finanzwirkungen; konkrete Kostenwerte unbekannt.
- **Zeitwirkung:** unbekannt.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** vermutlich erhöht durch Suche/Aufbereitung; konkret unbekannt.
- **Lagerung:** unbekannt.
- **Marktbarrieren:** Skalierung, Qualitätsnachweise, Produktdaten, remanufacturing, klare Abgrenzung von Recycling.

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** mittel; Projektkommunikation zeigt Materialgeschichten, Bauteile sollen aber „wie neu“ wirken.
- **räumliche Transformation:** Neubau mit flexibler Wohn-/Arbeitsnutzung; keine Bestandstransformation.
- **Atmosphäre / Ausdruck:** zeitgenössische Reihenhäuser; Reuse eher industriell veredelt als roh sichtbar.
- **Umgang mit Spuren:** Lendager betont, dass aufbereitete Materialien Qualität/Funktion/Ästhetik von Neuware erreichen.
- **sozialer Wert:** Beitrag zu urbanem Wohnmodell; konkrete soziale Programme unbekannt.
- **Denkmal- oder Bestandswert:** unbekannt.
- **Kritik / Grenzen:** hoher Anteil Recycling/Upcycling, aber weniger klare Direct-Reuse-Bauteile; widersprüchliche Mengen und Flächenangaben.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** Prüfung, Norm, Recht, Schadstoff, Verbindung, genaue Aufbereitungsmethode, detailliertes Tragwerkssystem.
- **Welche neuen Entitäten wären sinnvoll?** Remanufacturing, Upcycled product stream, Quellenkonflikt Kennwert.
- **Welche Daten fehlen?** genaue Anzahl und Maße der Fenster, U-Werte, Prüfberichte, technische Zulassungen, LCA-Bericht, Transportdistanzen, Baukosten, Bauteilpass.
- **Welche Quellen müssten geprüft werden?** NREP LCA/LCC-Vollbericht, Materialdatenblätter von Lendager/a:gain, Genehmigungs-/Ausschreibungsunterlagen, Fensterprüfungen.

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja, als Vergleichsfall / mittlere Priorität
- **5 wichtigste Fakten:**
  1. 20 Reihenhäuser in Ørestad, fertiggestellt 2018 nach NREP.
  2. 75 % der Fenster stammen laut a:gain/EMF aus öffentlichen Wohnbauten in Nordjütland.
  3. Beton aus der Copenhagen Metro wurde als recyceltes Material eingesetzt; Mengenangaben widersprechen sich.
  4. Holzreste / Dinesen-Offcuts wurden für Böden, Wände und Fassaden genutzt.
  5. NREP nennt 32 % CO₂-Reduktion bei Materialien und 45 % über 50 Jahre inkl. Betrieb.
- **5 wichtigste Bauteile:** wiederverwendete Fenster, Holzböden, Holz-Wand-/Fassadenelemente, recycelter Beton, Solartechnik nicht als Reuse.
- **5 wichtigste Hürden:** Performance gebrauchter Fenster, Gewährleistung, Mengen-/Datenkonflikte, Skalierung, Abgrenzung Recycling vs. Reuse.
- **5 wichtigste übertragbare Erkenntnisse:** Reuse kann kommerziellen Wohnbau erreichen; Fenster sind ein skalierbarer Hüllenstrom; Remanufacturing erhöht Akzeptanz; LCA braucht transparente Bilanzgrenzen; Materialrecycling nicht mit Bauteilreuse verwechseln.
- **5 offene Fragen:** Welche Fensterprüfungen wurden durchgeführt? Welche U-Werte wurden erreicht? Wie viel Beton wurde tatsächlich eingesetzt? Welche Holzbauteile sind gebrauchte Bauteile vs. Produktionsreste? Wie wurden Gewährleistung und Haftung geregelt?

## Quellen / Links

- NREP — Upcycle Studios: https://nrep.com/project/upcycle-studios/
- Lendager — Upcycle Studios: https://lendager.com/project/upcycle-studios/
- a:gain — Upcycle Studios project reference: https://www.again.dk/project-references/upcycle-studios
- Ellen MacArthur Foundation — Upcycled Studios: https://www.ellenmacarthurfoundation.org/circular-examples/reusing-construction-materials-to-limit-biodiversity-impacts-upcycles
- AG Gruppen / MyNewsdesk — 20 rækkehuse: https://www.mynewsdesk.com/dk/ag-gruppen/pressreleases/20-raekkehuse-bygget-af-upcyclede-materialer-paa-vej-i-oerestad-syd-2380409
- Circulary — Lendager / Upcycle Studios: https://www.circulary.eu/project/lendager/
