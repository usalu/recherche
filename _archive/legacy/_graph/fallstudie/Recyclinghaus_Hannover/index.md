---
id: "Recyclinghaus_Hannover"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "Recyclinghaus Hannover — Fallstudie Direct Reuse / zirkuläres Bauen"
bauobjekt:
  - "Recyclinghaus_Hannover"
legacy_paths:
  - "Gebäude\\Recyclinghaus_Hannover.md"
projekt:
  - "Recyclinghaus_Hannover"
reuse_chain_detected: "False"
---
# Recyclinghaus Hannover — Fallstudie Direct Reuse / zirkuläres Bauen

## Migration

- Fallstudie ID: Recyclinghaus_Hannover
- Legacy source count: 1
- Generated project: Recyclinghaus_Hannover
- Generated bauobjekt: Recyclinghaus_Hannover
- Extracted reuse_einsatz rows: 14
- Extracted datenpunkt rows: 13
- Extracted entity mapping rows: 33
- Reuse chain detected: False

## Legacy Content

### Legacy Source: Gebäude\Recyclinghaus_Hannover.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Recyclinghaus_Hannover
- Secondary targets: projekt/Recyclinghaus_Hannover; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Recyclinghaus Hannover — Fallstudie Direct Reuse / zirkuläres Bauen

**Stand:** 2026-05-07  
**Sprache:** Deutsch  
**Arbeitsregel:** Gewertet werden nur wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Recyclingmaterialien, neue recyclingfähige Konstruktionen, lose Möbel und reine Design-for-Disassembly-Strategien werden separat markiert.

---

## 1. EINORDNUNG

- **Entscheidung:** VERGLEICHSFALL
- **Bewertung:** ★★★★☆
- **Begründung:** Das Recyclinghaus Hannover ist ein gebauter Prototyp mit vielen wiederverwendeten festen Bauteilen, besonders in der Fassade und im Innenausbau: Aluminiumfenster, Faserzement-/Eternitplatten, Profilbauglas, Wellblech, Saunabank-Holz, Abbruchziegel, historische Türen, Waschbecken/Fliesen und eingebaute Messebauplatten. Das Haupttragwerk ist jedoch ein neuer, leimfreier Massivholzbau; geplante Wiederverwendung einer alten Stahlkonstruktion wurde laut Deutschem Architektenblatt nicht umgesetzt. Daher stark, aber nicht ★★★★★.
- **Vertrauensgrad:** belegt
- **Warnung Bestandserhalt:** nein — Neubau/Prototyp; keine Hauptbewertung aus Bestandserhalt.
- **Warnung Möbel/Dekoration:** ja — Einbaumöbel/feste Einbauten zählen nur, wenn fest eingebaut; lose Möbel und dekorative Objekte werden ignoriert.
- **Projektstatus:** gebaut / bezogen 2019

---

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Recyclinghaus Hannover | untersuchter Fall | CITYFÖRSTER; ZAB; DAB | belegt | experimentelles Wohnhaus/Prototyp |
| Gebäude | Einfamilienhaus / Wohnhaus | neues Wohngebäude | DAB; ZAB | belegt | 3 Etagen / Wohnnutzung |
| Projekt | Recyclinghaus Hanover/Hannover | Pilot- und Forschungsprojekt | CITYFÖRSTER; BauNetz Wissen | belegt | Reallabor für Recycling, Reuse, DfD |
| Ort | Hannover-Kronsberg / ehemaliges Expo-Areal | Standort | DAB; BauNetz Wissen | belegt | Deutschland |
| People | Nils Nolting / CITYFÖRSTER | Architektur/Projektkommunikation | DAB; ELEMENTE | teilweise belegt | weitere Teamdetails unbekannt |
| Projekt | Gundlach GmbH & Co. KG Wohnungsunternehmen | Bauherrschaft | ZAB; DAB | belegt | auch Quelle gebrauchte Bauteile aus eigenem Bestand |
| Architekt | CITYFÖRSTER architecture + urbanism | Planung | ZAB; CITYFÖRSTER | belegt | |
| Tragwerksplaner | DREWES + SPETH Beratende Ingenieure | Statik | ZAB; db | belegt | |
| Reuse-Strategie | Bauteilwiederverwendung + Recyclingmaterial + recyclinggerechte Konstruktion | zentrale Strategie | CITYFÖRSTER | belegt | Direct Reuse separat von Recycling bewerten |
| Bauteil | Aluminiumfenster | wiederverwendete Hüllbauteile | db; Architekturvideo; RE.MATERIAL | belegt | teils mit neuer 3-fach-Verglasung/thermischer Ertüchtigung |
| Bauteil | Faserzement-/Eternitplatten | wiederverwendete Fassadenbekleidung | Detail; ZAB; db | belegt | ehemaliges Jugendzentrum/Haus der Jugend |
| Bauteil | Profilbauglas | wiederverwendete Fassaden-/Hüllbauteile | Detail; db; Bauhandwerk | belegt | aus alter Lackiererei |
| Bauteil | Wellblech | wiederverwendete Fassadenkomponente | ZAB; db | belegt | genaue Herkunft unbekannt |
| Bauteil | Saunabänke / Holzleisten | Fassadenholz | Detail; ZAB | belegt | aus Sportzentrum/Sauna |
| Bauteil | Abbruchziegel | nichttragende Innenwände / Terrazzo-Splitt teilweise | db; DAB | belegt | bei Terrazzo eher Materialrecycling, nicht Direct Reuse |
| Bauteil | historische Bauernhaustür | feste Türen zu Technik/Gäste-WC | db; DAB | belegt | Raumabschluss zählt |
| Bauteil | Messebauplatten | Wandverkleidung, Türen, Einbauschränke, feste Einbauten | DAB; db | belegt | nur fest eingebaute Verwendung zählt |
| Bauteil | Waschbecken / Sanitär | feste Sanitäreinbauten | Architekturvideo; db | teilweise belegt | genaue Herkunft/Anzahl unbekannt |
| Material | Recyclingbeton | Fundament/Bodenplatte | ZAB; 3N; Bauhandwerk | belegt | Recycling, nicht Direct Reuse |
| Material | Jutedämmung aus Kakaosäcken | Dämmung | DAB; ZAB; RE.MATERIAL | belegt | Upcycling/Materialverwendung, nicht Bauteil-Direktreuse |
| Methode | Bauteilernte | regionale Beschaffung | Detail; DAB | belegt | kurze Transportwege |
| Methode | recyclinggerechte Bauweise | spätere Demontierbarkeit | CITYFÖRSTER; 3N | belegt | DfD zählt nicht als Direct Reuse, aber relevant |
| Abbruchmethode | selektive Bauteilernte aus Region | Herkunft der Fassaden-/Innenbauteile | Detail | teilweise belegt | konkrete Rückbauprozesse unbekannt |
| Aufbereitungsmethode | Fensterglas ersetzt, Rahmen ertüchtigt | technische Anpassung der Reuse-Fenster | RE.MATERIAL | belegt | altes Glas wurde separat in einem Pavillon weitergenutzt |
| Prüfung | unbekannt | technische Nachweise | unbekannt | unbekannt | keine Prüfprotokolle öffentlich |
| Kennwert | 285 m² BGF | Größe | ZAB | belegt | BGF |
| Kennwert | 160 m² Wohnfläche | Nutzung / bewohnte Fläche | DAB | belegt | abweichende Flächengrenze |
| Kennwert | 90 % Fassadenmaterial wiederverwendet | Reuse-Anteil Fassade | ZAB; BauNetz Wissen; ELEMENTE | belegt | Fassade, nicht Gesamtgebäude |
| Kennwert | 42 % Altmaterial im Recyclingbeton | Recyclinganteil Fundament | ZAB | belegt | Recyclingkennwert, nicht Direct Reuse |
| Kennwert | ca. 100 t CO₂ gebunden | gespeicherter Kohlenstoff/Material | ZAB | teilweise belegt | nicht als Direct-Reuse-Einsparung interpretieren |
| Recht | Bauordnung/Zulassung | Hürde im Projekt | ImmobilienScout24; Bauhandwerk | teilweise belegt | keine Normnummern |
| Schadstoff | Faserzement/Eternit potenziell relevant | mögliche Prüfung erforderlich | keine spezifische Angabe | unbekannt | Asbeststatus nicht belegt; keine Annahme |
| Software/Tool | unbekannt | Bauteilkatalog/Planung | unbekannt | unbekannt | keine konkrete Software genannt |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Bauteilernte | Beschreibt aktive Gewinnung gebrauchter Bauteile aus der Region. | Karte/regionale Herkunft in Hannover; Detail nennt „Bauteilernte“. | Methode, Logistik, Bauteil |
| Reuse-vs-Recycling-Abgrenzung | Das Projekt mischt Direct Reuse, Recyclingmaterial und DfD. | Faserzementplatten = Direct Reuse; Recyclingbeton = Recycling. | Material, Kennwert, Reuse-Strategie |
| Fest eingebauter Innenausbau | Notwendig zur Abgrenzung gegenüber Möbel/Deko. | eingebaute Messebauplatten, raumhohe Türen, Einbauschränke. | Bauteil, räumlicher Innenausbau |

---

## 3. FALLSTUDIE

- **Name:** Recyclinghaus Hannover / Recyclinghouse Hanover
- **Ort:** Hannover-Kronsberg, Deutschland
- **Gebäude:** experimentelles Wohnhaus / Einfamilienhaus
- **Projekt:** Prototyp für Reuse, Recyclingmaterialien und recyclinggerechte Bauweise
- **Beteiligte People / Akteure:** CITYFÖRSTER architecture + urbanism; Gundlach GmbH & Co. KG; DREWES + SPETH; H2A; weitere unbekannt
- **Architekt:** CITYFÖRSTER architecture + urbanism
- **Tragwerksplaner:** DREWES + SPETH Beratende Ingenieure
- **Bauherr:** Gundlach GmbH & Co. KG Wohnungsunternehmen, Hannover
- **Zeitraum:** Fertigstellung/Bezug 2019; Veröffentlichungen 2020–2022
- **Ursprüngliche Nutzung:** nicht anwendbar für Neubau; einzelne Bauteile stammen aus Jugendzentrum, Lackiererei, Sportzentrum/Sauna, Messebau u. a.
- **Neue Nutzung:** Wohnen
- **Fläche / Maßstab:** 285 m² BGF laut ZAB; 160 m² Wohnfläche laut DAB
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** gut für Bauteilarten, Fläche, Akteure und Fassadenanteil; mittel/schwach für Normen, Kosten, Mengen, Prüfungen und CO₂-Methode

---

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ Bauteilwiederverwendung; Materialwiederverwendung/Recycling separat; recyclinggerechte Bauweise
- **Hauptniveau:** Gebäudehülle; räumlicher Innenausbau; technische/feste Einbauten; Material
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Das Haupttragwerk aus leimfreien Massivholzelementen ist neu und zählt nicht als Direct Reuse. Recyclingbeton, Schaumglasschotter, Jutedämmung und DfD zählen als zirkuläre Strategien, aber nicht als Bauteil-Direktreuse. Bewertet werden vor allem wiederverwendete Fenster, Fassadenplatten, Profilglas, Wellblech, Holzleisten, Türen, Sanitär und feste Innenausbauten.
- **Warum ist der Fall relevant?** Der Fall zeigt eine konsequente Kombination aus regionaler Bauteilernte, sichtbarer Reuse-Fassade, festem Innenausbau aus Gebrauchtmaterial und späterer Demontierbarkeit in einem real bewohnten Wohnhaus.

---

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Aluminiumfenster | Aluminium/Glas | u. a. ehemaliges Jugendzentrum / Bauherrbestand | Fenster | Fassadenfenster | alle Fenster laut ELEMENTE; genaue Anzahl unbekannt | nein | ja | ja | nein | Rahmen thermisch ertüchtigt, Glas ersetzt | unbekannt | unbekannt | U-Wert, Luftdichtheit, Schlagregen | unbekannt | energetische Anforderungen | RE.MATERIAL; ELEMENTE; db | Anzahl |
| alte Glasscheiben aus Fenstern | Glas | Reuse-Fenster | Fensterglas | in anderem Pavillon weitergenutzt | unbekannt | nein | nein | ja | nein | Ausbau beim Glastausch | unbekannt | unbekannt | geringere Anforderungen im Pavillon | unbekannt | Kaskadennutzung | RE.MATERIAL | Pavillon |
| Faserzement-/Eternitplatten | Faserzement | ehemaliges evangelisches Haus der Jugend / Jugendzentrum | Fassaden-/Plattenmaterial | VHF-Fassadenbekleidung | Teil der 90-%-Reuse-Fassade | nein | ja | ja | nein | Demontage, Zuschnitt unbekannt | VHF mechanisch | unbekannt | Witterung, Brandschutz | unbekannt | Schadstoff-/Zustandsnachweis | Detail; BauNetz Wissen; db | Asbeststatus, Menge |
| Profilbauglas | Glas | alte/stillgelegte Lackiererei | Industrieglas/Fassade | Fassadenbekleidung/Belichtung | unbekannt | nein | ja | ja | nein | Demontage/Anpassung | unbekannt | unbekannt | Witterung, Bruch, Wärmeschutz | unbekannt | Maße, U-Wert | Detail; Bauhandwerk; db | Menge |
| Wellblech | Metall | unbekannt | unbekannt | Fassadenbekleidung | unbekannt | nein | ja | ja | nein | unbekannt | unbekannt | unbekannt | Witterung/Korrosion | unbekannt | Herkunft | ZAB; db | Herkunft, Menge |
| Holzleisten / alte Saunabänke | Holz | Sportzentrum/Sauna | Sitzbänke | Fassadenholz / Bekleidung | unbekannt | nein | ja | ja | nein | Demontage, Zuschnitt | unbekannt | unbekannt | Witterung, Dauerhaftigkeit | unbekannt | Holzschutz | Detail; ZAB | genaue Behandlung |
| historische Bauernhaustür | Holz/Metall unbekannt | unbekannt | Haustür | Türen Technikraum/Gäste-WC | einzelne Türflügel | nein | ja | nein | nein | aufgearbeitet | unbekannt | unbekannt | Raumabschluss, ggf. Brandschutz | unbekannt | Passmaß | db; DAB | Herkunft |
| Messebauplatten | Holzwerkstoff/Plattenmaterial | Messebauer in Hannover | Messestand/Lagerplatten | Wandverkleidung, Einbauten, Türen, Schränke | mehr als Hälfte Innenmaterialien laut DAB; genaue Menge unbekannt | nein | ja | nein | teilweise | Zuschnitt | verschraubt/vermutet | unbekannt | Innenraum, Emissionen, Brandschutz | unbekannt | Materialdaten | DAB; db | Menge |
| Abbruchziegel | Ziegel | Abbruch | Mauerwerk | nichttragende Innenwände / Zuschlag für Terrazzo | unbekannt | nein | ja | nein | nein | Reinigung/Zuschnitt unbekannt | Mörtel unbekannt | unbekannt | Schallschutz/Brandschutz | unbekannt | Sortierung | db; DAB | Menge |
| Waschbecken / Sanitär | Keramik/Metall | unbekannt | Sanitär | Sanitärinstallation | unbekannt | nein | nein | nein | ja | Reinigung/Anpassung | unbekannt | unbekannt | Hygiene, Dichtheit | unbekannt | Gewährleistung | Architekturvideo; db | Anzahl |
| Fliesen / Kronkorken-Mosaik | Keramik/Metall | gebraucht/Restmaterial | Oberfläche/Verpackung | Fliesenspiegel/Oberfläche | unbekannt | nein | ja | nein | nein | unbekannt | unbekannt | unbekannt | Hygiene/Reinigung | unbekannt | Oberfläche vs. Dekoration | db; Architekturvideo | Anteil Direct Reuse |
| alter vor Ort gefundener Beton / Gehwegplatten / Blockstufen / Pflaster | Beton/Stein | Außenraum/Bestand | Außenbeläge/Bauteile | Außenanlagen | unbekannt | nein | ja | nein | nein | Verlegung | unbekannt | unbekannt | Tragfähigkeit/Frost | unbekannt | lokale Wiederverwendung | db | Menge |
| Rohbau | leimfreies Massivholz | neu | nicht vorhanden | Tragwerk | 285 m² BGF-Projekt | ja | ja | nein | nein | neu, recyclingfähig | Holzschrauben/Buchenholzdübel je Quelle | unbekannt | Tragfähigkeit | unbekannt | nicht Direct Reuse | ZAB; 3N; dach+holzbau | technische Details |
| Fundament/Bodenplatte | Recyclingbeton | Recyclingmaterial | gebrochene mineralische Stoffe | Fundament | 42 % Altmaterial im Beton | ja | nein | nein | nein | Betonherstellung | monolithisch | zugelassen laut Bauhandwerk | Tragfähigkeit | keine Normnummer | Recycling, nicht Reuse | ZAB; Bauhandwerk | genaue Rezeptur |

---

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | regionale Bauteilquellen suchen | CITYFÖRSTER, Gundlach | Bauteilernte | Karte/Inventar, Software unbekannt | unbekannt | unbekannt | unbekannt | Region Hannover | passende Quellen finden | lokale Netzwerke/Bauherrbestand | Detail; DAB |
| Bauteilinventar | gebrauchte Komponenten erfassen | Planer/Bauherr | Design by Availability | unbekannt | unbekannt | unbekannt | unbekannt | lokaler Suchradius | variable Bauteile | Entwurf mit verfügbaren Teilen | CITYFÖRSTER; DAB |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Faserzement/Eternit potenziell relevant | unbekannt | unbekannt |
| Rückbau | Bauteile aus Jugendzentrum, Lackiererei, Sportzentrum, Messebau sichern | Rückbau-/Quellakteure unbekannt | selektive Demontage vermutet | unbekannt | unbekannt | unbekannt | unbekannt | lokal/regional | beschädigungsarme Entnahme | Bauteilernte | Detail |
| Ausbau | Fenster/Platten/Profilglas/Saunabänke ausbauen | unbekannt | unbekannt | unbekannt | selektiv vermutet | unbekannt | unbekannt | unbekannt | Bruch/Schäden | unbekannt | Detail; DAB |
| Transport | kurze Transportwege | Bauherr/Planer/Lieferanten | regionale Beschaffung | unbekannt | unbekannt | unbekannt | unbekannt | Region Hannover | Logistik heterogener Teile | lokale Herkunft | ZAB; Detail |
| Lagerung | Materiallager/Messebauplatten | Messebauer/Bauherr | Lagerauflösung | unbekannt | unbekannt | unbekannt | unbekannt | Hannover Messeumfeld | Timing | Lagerverkleinerung als Quelle | DAB |
| Aufbereitung | Fenster ertüchtigen; Glas ersetzen; Platten zuschneiden | Handwerker/Planer | Anpassung | unbekannt | unbekannt | thermische Ertüchtigung | unbekannt | Baustelle/Werkstatt | U-Wert | neue 3-fach-Verglasung, alte Gläser weitergenutzt | RE.MATERIAL |
| Planung | Reuse + Recycling + DfD integrieren | CITYFÖRSTER, Tragwerksplanung | recyclinggerechte Planung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Bauordnung, heterogene Bauteile | lösbare Konstruktionen | CITYFÖRSTER; ImmobilienScout24 |
| Genehmigung | Zulassung für RC-Beton/gebrauchte Bauteile | Bauherr/Planer/Behörden | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Bauordnung komplex | Einzelfall-/Genehmigungsprozess unbekannt | Bauhandwerk; ImmobilienScout24 |
| Wiedereinbau | Fassaden-/Innenbauteile fest einbauen | Handwerker | VHF, Innenausbau, Holzbau | unbekannt | unbekannt | unbekannt | unbekannt | Baustelle | Passmaß | handwerkliche Anpassung | db; DAB |
| Monitoring | Nutzung als Prototyp/Reallabor | Bauherr/Planer | Lernen am gebauten Objekt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Übertragbarkeit | Publikationen/Führungen | CITYFÖRSTER; 3N |

---

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | neuer leimfreier Massivholzbau; nicht reused | Tragfähigkeit, sortenreiner Rückbau | unbekannt | unbekannt | geplante Stahlreuse nicht umgesetzt | neuer Holzrohbau | DAB; 3N |
| Lastabtragung | Massivholz + RC-Fundament | Tragfähigkeit | unbekannt | unbekannt | Direct-Reuse-Tragwerk fehlt | Massivholzsystem | ZAB; 3N |
| Verbindung | recyclinggerechte, trennbare Bauweise | demontierbar, sortenrein | unbekannt | unbekannt | spätere Wiederverwendung | lösbare Verbindungen | CITYFÖRSTER; 3N |
| Brandschutz | VHF und Faserzement/EQUITONE teils nicht brennbar genannt | Brandschutz Fassade/Innenraum | unbekannt | unbekannt | heterogene gebrauchte Materialien | Materialauswahl/VHF | dach+holzbau; BauNetz Wissen |
| Schallschutz | unbekannt | Wohnstandard | unbekannt | unbekannt | gebrauchte Innenbauteile | unbekannt | unbekannt |
| Feuchte | Fassade/VHF; Jutedämmung | Feuchte-/Witterungsschutz | unbekannt | unbekannt | gebrauchte Fassadelemente | VHF-System | BauNetz Wissen |
| Wärmeschutz | alte Fensterrahmen ertüchtigt, Glas auf 3-fach ersetzt | U-Wert/EnEV/GEG unbekannt | unbekannt | unbekannt | alte Fenster erreichen Anforderungen nicht | neue Verglasung, Rahmen ertüchtigt | RE.MATERIAL |
| Wärmebrücken | unbekannt | Wärmebrückenminimierung | unbekannt | unbekannt | gebrauchte Fensteranschlüsse | unbekannt | unbekannt |
| Luftdichtheit | unbekannt | Luftdichtheit | unbekannt | unbekannt | gebrauchte Fenster/Türen | unbekannt | unbekannt |
| TGA-Integration | Sanitärreuse teilweise belegt | Hygiene, Dichtheit, Wartung | unbekannt | unbekannt | Gewährleistung | unbekannt | Architekturvideo; db |
| Barrierefreiheit | unbekannt | unbekannt | unbekannt | unbekannt | Einfamilienhaus | unbekannt | unbekannt |
| Dauerhaftigkeit | Fassadenmaterialien mit zweitem Leben | Witterung/Dauerhaftigkeit | unbekannt | unbekannt | gebrauchte Oberflächen | sichtbare Patina / VHF | Detail; db |
| Wartung | unbekannt | Wartbarkeit | unbekannt | unbekannt | heterogene Materialien | unbekannt | unbekannt |
| Zulassung | Bauordnung komplex; RC-Beton erstmalig/neu zugelassen laut Berichten | Genehmigungsfähigkeit | keine Normnummer | unbekannt | ungewöhnliche Materialien | Projekt als Einzelfall/Prototyp | ImmobilienScout24; Bauhandwerk |
| Haftung | unbekannt | Gewährleistung | unbekannt | unbekannt | gebrauchte Bauteile | unbekannt | unbekannt |

---

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Fertigstellung/Bezug | 2019 | Jahr | unbekannt | Gebäude | ZAB; DAB | belegt |
| BGF | 285 | m² | unbekannt | Gebäude | ZAB | belegt |
| Wohnfläche | 160 | m² | unbekannt | Wohnnutzung | DAB | belegt |
| Anteil wiederverwendeter Fassadenmaterialien | 90 | % | unbekannt | Fassade | ZAB; BauNetz Wissen; ELEMENTE | belegt |
| Anteil Altmaterial im Recyclingbeton | 42 | % | unbekannt | Fundament/Bodenplatte | ZAB | belegt, aber Recycling, nicht Reuse |
| gebundener CO₂-Anteil | ca. 100 | t CO₂ | unbekannt | Gebäude / Materialbindung | ZAB | teilweise belegt; nicht Direct-Reuse-Einsparung |
| Anteil Innenmaterialien aus recycelten/gebrauchten Beständen | >50 | % | unbekannt | Innenausbau | DAB | teilweise belegt; Abgrenzung Reuse/Recycling unklar |
| Anzahl Bauteile | unbekannt | Anzahl | unbekannt | Gebäude | unbekannt | unbekannt |
| wiederverwendete Masse | unbekannt | t | unbekannt | Direct-Reuse-Bauteile | unbekannt | unbekannt |
| Kosten | unbekannt | EUR | unbekannt | Projekt | unbekannt | unbekannt |
| Bauzeit | unbekannt | Monate | unbekannt | Projekt | unbekannt | unbekannt |
| U-Wert | unbekannt | W/m²K | unbekannt | Fenster/Wand/Dach | unbekannt | unbekannt |
| Zirkularitätskennwert | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |

---

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| tragende Stahlreuse nicht umgesetzt | technisch/wirtschaftlich | alte Lagerhallenstahlteile passten/Prozess unbekannt | Haupttragwerk wurde neu in Holz gebaut | Tragwerkssystem, Bauteil | Massivholzbau statt Stahlreuse | frühe Verfügbarkeit/Passung tragender Bauteile klären | DAB |
| Bauordnung komplex | rechtlich | ungewohnte gebrauchte/recycelte Baustoffe | Genehmigungsaufwand | Recht, Prüfung | Projekt als Prototyp | rechtliche Klärung früh starten | ImmobilienScout24 |
| energetische Anforderungen an gebrauchte Fenster | technisch | alte Verglasung erfüllt U-Wert nicht | Glas musste ersetzt werden | Fenster, Wärmeschutz | Rahmen ertüchtigt, 3-fach-Glas; altes Glas in Pavillon | Bauteil und Teilbauteil kaskadieren | RE.MATERIAL |
| Schadstoff-/Materialnachweis Faserzement | technisch/rechtlich | Faserzement/Eternit kann kritisch sein | Prüfung nötig, aber öffentlich unbekannt | Fassade, Schadstoff | unbekannt | keine Annahmen ohne Prüfbeleg | unbekannt |
| heterogene Bauteile und Handwerk | logistisch/gestalterisch | unterschiedliche Herkunft und Maße | mehr Planungs-/Montageaufwand | Bauteil, Methode | Bauteilernte und Anpassung | Reuse braucht handwerkliche Flexibilität | Detail; DAB |
| Abgrenzung Reuse/Recycling/DfD | methodisch | Projekt mischt mehrere Kreislaufstrategien | Gefahr der Überbewertung | Kennwert, Reuse-Strategie | getrennte Bewertung | Direct Reuse nur für feste Bauteile zählen | CITYFÖRSTER; ZAB |

---

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** regionale Bauteilernte; Teile aus Bauherrbestand/Gundlach, regionalen Rückbauquellen, Messebau-Lagerauflösung und lokalen Gebäuden.
- **Bauteilbörse / Quelle:** keine konkrete Bauteilbörse belegt; Quellen u. a. ehemaliges Jugendzentrum/Haus der Jugend, Lackiererei, Sportzentrum/Sauna, Messebauunternehmen.
- **Kostenwirkung:** unbekannt.
- **Zeitwirkung:** unbekannt; Beschaffung war timingabhängig, z. B. Lagerverkleinerung des Messebauers.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** vermutlich erhöht durch Suche, Ausbau, Aufbereitung, Fensterertüchtigung und handwerkliche Anpassung; konkrete Werte unbekannt.
- **Lagerung:** Messebauplatten stammten aus Lagerauflösung; eigenes Zwischenlager unbekannt.
- **Marktbarrieren:** Bauordnung, Leistungsnachweise, Schadstofffragen, Passgenauigkeit, fehlende Standardprozesse.

---

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** sehr hoch; Fassade macht Faserzement, Profilglas, Wellblech und Holzleisten sichtbar.
- **räumliche Transformation:** Neubau, aber mit Bauteilbiografien aus Hannover in Hülle und Innenausbau.
- **Atmosphäre / Ausdruck:** experimentell, patchworkartig, ressourcenbewusst.
- **Umgang mit Spuren:** ehemalige Aufdrucke auf Messebauplatten und historische Türen werden gestalterisch sichtbar.
- **sozialer Wert:** Demonstrator/Reallabor; Wohnhaus einer Familie; Bildungs- und Vorbildfunktion.
- **Denkmal- oder Bestandswert:** kein Gebäudedenkmal; kultureller Wert liegt in der Materialgeschichte und regionalen Bauteilernte.
- **Kritik / Grenzen:** Haupttragwerk nicht reused; viele Kennwerte fehlen; einige Elemente sind Recycling/Upcycling, nicht Direct Reuse.

---

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** konkrete Prüfprotokolle, Schadstoffnachweise, Norm-/Zulassungsdetails, Kosten, tatsächliche wiederverwendete Masse, Anzahl einzelner Bauteile.
- **Sinnvolle neue Entitäten:** Bauteilernte; Reuse-vs-Recycling-Abgrenzung; fest eingebauter Innenausbau; Kaskadenreuse.
- **Fehlende Daten:** Anzahl Fenster, m² Fassadenplatten/Profilglas, Masse einzelner Bauteilgruppen, CO₂-Methode, Lager- und Transportdistanzen.
- **Zu prüfende Quellen:** Bauteilkatalog des Projekts, Genehmigungsunterlagen, Brandschutzkonzept, Schadstoffgutachten, Detailpläne VHF, Fensterprüfungen.

---

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja, als Vergleichsfall / starker Hüllen- und Innenausbau-Reuse-Fall.
- **5 wichtigste Fakten:**
  1. Fertigstellung/Bezug 2019.
  2. 285 m² BGF laut ZAB; 160 m² Wohnfläche laut DAB.
  3. Die Fassade besteht zu ca. 90 % aus wiederverwendetem Material.
  4. Haupttragwerk ist neuer leimfreier Massivholzbau, nicht wiederverwendeter Stahl.
  5. Fenster wurden wiederverwendet, aber energetisch ertüchtigt und neu verglast.
- **5 wichtigste Bauteile:**
  1. Aluminiumfenster
  2. Faserzement-/Eternitplatten
  3. Profilbauglas
  4. Holzleisten aus Saunabänken
  5. Messebauplatten / feste Innenausbauten
- **5 wichtigste Hürden:**
  1. Bauordnung/Zulassung
  2. energetische Leistungsanforderungen an Fenster
  3. Schadstoff-/Materialnachweis
  4. Beschaffung passender Bauteile
  5. Abgrenzung von Recycling und Direct Reuse
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Regionale Bauteilernte kann Transport und Beschaffung plausibel machen.
  2. Reuse-Fenster benötigen oft technische Aufbereitung.
  3. Reuse muss pro Bauteilgruppe getrennt von Recycling bewertet werden.
  4. Fest eingebaute Innenbauteile zählen; lose Möbel nicht.
  5. Ein starker Reuse-Fall kann trotz neuem Tragwerk relevant sein, wenn Hülle und Innenausbau substanziell sind.
- **5 offene Fragen:**
  1. Welche Schadstoffprüfungen gab es für Faserzement/Eternit?
  2. Wie hoch ist die Masse der wiederverwendeten Bauteile?
  3. Welche Kosten entstanden durch Bauteilernte und Aufbereitung?
  4. Welche Norm-/Einzelfallnachweise wurden verlangt?
  5. Wie dauerhaft funktionieren die reused Fassadenelemente im Betrieb?

---

## Quellen und Links

- CITYFÖRSTER – Recyclinghaus Hanover: https://www.cityfoerster.net/projects/recyclinghaus_hanover-218-2.html
- Zukunftsagentur Bau – Recyclinghouse Hannover: https://www.zukunft-bau.at/en/project/office-industry/recyclinghouse-hannover
- Deutsches Architektenblatt – Recyclinghaus in Hannover: https://www.dabonline.de/architektur/recyclinghaus-in-hannover-von-cityfoerster-baustoffe-baumaterialien/
- Detail – Bauteilernte aus der Region: https://www.detail.de/de_de/bauteilernte-aus-der-region-recyclinghaus-in-hannover
- db deutsche bauzeitung – Recyclinghaus Hannover: https://www.db-bauzeitung.de/architektur/wohnungsbau/recyclinghaus-hannover-cityfoerster/
- RE.MATERIAL – Zu Besuch im Recyclinghaus Hannover: https://re-material.de/?p=315
- BauNetz Wissen – Fassade aus recycelten Faserzementplatten: https://www.baunetzwissen.de/fassade/tipps/forschung/fassade-aus-recycelten-faserzementplatten-7437980
- ELEMENTE MaterialForum – Recycling House lecture: https://www.elemente-material.de/en/materials-online/materialien/sustainable-materials/cityfoerster1.html
- Bauhandwerk – Einfamilienhaus aus recycelten Baustoffen in Hannover: https://www.bauhandwerk.de/artikel/bhw_Einfamilienhaus_aus_recycelten_Baustoffen_in_Hannover-3591655.html
- dach+holzbau – Massivholzbau trifft Recycling: https://www.dach-holzbau.de/artikel/massivholzbau-trifft-recycling-3592766.html
- 3N Kompetenzzentrum – Recyclinghaus: https://www.3-n.info/themenfelder/praxisbeispiele/holzbau-in-niedersachsen/wohnungsbau/recyclinghaus.html
- Architekturvideo – Kreislaufwirtschaft beim Bauen: https://architekturvideo.de/kreislaufwirtschaft-bauen-recyclinghaus-cityfoerster-hannover/
- ImmobilienScout24 – Das Recycling-Haus kommt: https://www.immobilienscout24.de/neubau/ratgeber/aktuelle-neubau-themen/recycling-haus.html
