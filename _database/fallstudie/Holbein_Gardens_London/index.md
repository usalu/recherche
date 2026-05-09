---
entity: "fallstudie"
id: "Holbein_Gardens_London"
title: "Holbein Gardens, London — Fallstudie Direct Reuse / Wiederverwendung von Tragwerksstahl"
build_status: "promoted_phase42"
legacy_paths:
  - "Gebäude\\Holbein_Gardens_London.md"
node_kind: "core"
bauobjekt:
  - "Holbein_Gardens_London"
projekt:
  - "Holbein_Gardens_London"
---

# Holbein Gardens, London — Fallstudie Direct Reuse / Wiederverwendung von Tragwerksstahl

## Legacy Content

### Legacy Source: Gebäude\Holbein_Gardens_London.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Holbein_Gardens_London
- Secondary targets: projekt/Holbein_Gardens_London; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Holbein Gardens, London — Fallstudie Direct Reuse / Wiederverwendung von Tragwerksstahl

**Arbeitsstand:** 2026-05-07  
**Sprache:** Deutsch  
**Regel:** Es werden nur tatsächlich wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente gezählt. Lose Möbel, Dekoration, reine DfD-Strategien und bloßer Bestandserhalt zählen nicht.

## 1. EINORDNUNG

- **Entscheidung:** HAUPTFALL
- **Bewertung:** ★★★★☆
- **Begründung:** Gebautes und gut dokumentiertes Londoner Büro-Refurbishment mit direkter Wiederverwendung von tragendem Stahl in einer vertikalen Erweiterung. Reused steel ist real, geprüft und eingebaut; die Mengen liegen je nach Quelle bei 24–25 t bzw. ca. 34 % / ein Drittel der Stahltonnage. Nicht auf ★★★★★, weil der Hauptanteil der Kreislaufleistung aus Bestandserhalt/Retrofit und nur ein Teil des neuen Tragwerks aus wiederverwendetem Stahl besteht.
- **Vertrauensgrad:** belegt, mit Kennwertabweichungen je Quelle
- **Warnung Bestandserhalt:** ja — 90/93 % Bestandserhalt ist wichtig, zählt nach Grundregel aber nicht als Bauteilwiederverwendung
- **Warnung Möbel/Dekoration:** nein
- **Projektstatus:** gebaut / fertiggestellt 2023

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Holbein Gardens | Untersuchter Reuse-Fall | [S1], [S2], [S3], [S4] | belegt | Büro-Refurbishment mit vertikaler Erweiterung. |
| Ort | Royal Borough of Kensington and Chelsea / Chelsea, London | Standort | [S2] | belegt | Grosvenor spricht auch von Belgravia-Kontext. |
| Gebäude | 1980er-Jahre Bürogebäude | Bestands- und Empfängergebäude | [S1], [S2], [S3] | belegt | Bestandserhalt separat von Reuse bewerten. |
| Projekt | Refurbishment plus 1-/2-geschossige Aufstockung | Bauprojekt | [S2], [S4], [S8] | belegt | Quellen unterscheiden 1-storey vs. 2-storey extension; Dachterrasse inklusive. |
| Bauherr | Grosvenor | Auftraggeber/Developer | [S1], [S2], [S4] | belegt | Grosvenor-Portfolio lieferte Teil des Stahls. |
| Architekt | Barr Gazetas | Architektur | [S2], [S4] | belegt | In Projektquellen und Awards genannt. |
| Tragwerksplaner | Heyne Tillett Steel / HTS | Tragwerk und Reuse-Nachweis | [S2], [S3], [S4] | belegt | Projektseite und IStructE. |
| Bauteilbörse | Cleveland Steel and Tubes / reclaimed stock | Quelle für Teil des Reuse-Stahls | [S1], [S5], [S9] | belegt | Stahlstockist und Contractor. |
| Bauteil | wiederverwendete Stahlträger/-stützen | zentrale Wiederverwendung | [S1], [S3], [S4], [S5] | belegt | Mengenabweichungen 24/25 t. |
| Material | Baustahl | Hauptreuse-Material | [S3], [S4], [S9] | belegt | geprüft und refabriziert. |
| Reuse-Strategie | ex-situ Bauteilwiederverwendung / salvaged structural steel | Kernstrategie | [S1], [S3], [S5] | belegt | Stahl aus Demolition Sites und reused stock. |
| Prüfung | CST testing nach SCI P427; zerstörende und zerstörungsfreie Prüfungen | Eignungsnachweis | [S5], [S9], [S10] | belegt | Bestimmung von Grade/Subgrade/Yield/Tensile laut Fachquelle. |
| Norm/Recht | SCI P427/P440; EN 1090 im allgemeinen Stahlreuse-Kontext | Prüf-/Ausführungsrahmen | [S5], [S9], [S10] | belegt/teilweise | Projektbezogen P427 belegt; EN 1090 als Kontextquelle. |
| Methode | frühe Reuse-Beschaffungsentscheidung | Projekterfolg | [S5] | belegt | Reuse wurde früh in der Low-Carbon-Strategie entschieden. |
| Logistik | Koordination Donor Site–Fabrication–Installation | Prozesshürde | [S5] | belegt | TERC beschreibt komplexe Koordination. |
| Hürde | Kosten, Programm, verfügbare Bestände | Markt-/Projektbarrieren | [S1], [S5] | belegt | Grosvenor/TERC nennen diese Punkte. |
| Kennwert | 24–25 t reused steel; 35/45/60 t CO₂-Einsparung je Quelle | Leistungsdaten | [S1], [S3], [S4], [S5], [S7] | belegt mit Abweichung | Werte nicht vermischen; Quellenkontext beachten. |
| Software | HTS Stockmatcher | mögliches/branchenbezogenes Tool, nicht eindeutig für Holbein als eingesetzt belegt | [S6] | unklar | Stockmatcher wurde 2023 veröffentlicht; für Holbein nicht sicher als Projekttool nennen. |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Donor-Site-Stahl | Stahlelemente stammen aus mehreren Quellen | 9 t Grosvenor-Projekte + 15/16 t Cleveland Steel | Bauteilbörse, Logistik, Prüfung |
| Kennwertkonflikt | Quellen nennen unterschiedliche CO₂-/Mengenwerte | 35, 45 oder 60 t CO₂ saved | Kennwert, Bericht |
| Reuse-Protokoll | Prüfpfad ist zentral und kein klassisches Normfeld | SCI P427/P440 | Prüfung, Norm, Recht |
| Bestandserhalt-Warnung | Retention darf nicht als Direct Reuse gezählt werden | 90/93 % retained | Gebäude, Reuse-Strategie |

## 3. FALLSTUDIE

- **Name:** Holbein Gardens
- **Ort:** London, Royal Borough of Kensington and Chelsea / Chelsea, UK
- **Gebäude:** 1980er-Jahre Büro-/Gewerbegebäude, transformiert zu modernem Workplace
- **Projekt:** Refurbishment mit vertikaler Erweiterung, CLT-Decken und wiederverwendetem Stahl
- **Beteiligte People / Akteure:** Grosvenor; Barr Gazetas; Heyne Tillett Steel; Cleveland Steel and Tubes; Eurban für CLT; weitere: TFT, Blenheim House, HDR/Leslie Clark je Quelle
- **Architekt:** Barr Gazetas
- **Tragwerksplaner:** Heyne Tillett Steel
- **Bauherr:** Grosvenor
- **Zeitraum:** Stahlrahmen 2022 fertig; Fertigstellung 2023 laut HTS; andere Quellen nennen Completion 2022 für Added area/Extension-Datensatz
- **Ursprüngliche Nutzung:** Büro-/Commercial Building aus den 1980er Jahren
- **Neue Nutzung:** nachhaltiger moderner Arbeitsplatz / Büro
- **Fläche / Maßstab:** GIA 3.536 m² laut HTS; added area 2.322 m² laut Optoppen; 25 % Flächenzuwachs laut Grosvenor/IOM3
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** gut für Stahlreuse, Akteure und Kennwerte; einzelne Kennwerte widersprechen sich zwischen Projektseite, Presse, Fallstudien und Fachartikel

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; tragender Stahl; Retrofit/adaptive reuse als Kontext, aber nicht vollständig als Wiederverwendung zählen
- **Hauptniveau:** Tragwerk / Aufstockung; zusätzlich geringe Materialreuse bei Stein/Ziegel laut TFT, Details unbekannt
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die Bewertung stützt sich auf aus anderen Projekten/Beständen entnommene und erneut tragend eingesetzte Stahlprofile. Die Beibehaltung des bestehenden Betonrahmens und der Fassade ist nachhaltiger Bestandserhalt, zählt hier aber nicht als Direct Reuse.
- **Warum ist der Fall relevant?** Holbein Gardens ist ein früher britischer Referenzfall für geprüfte, beschaffte und refabrizierte tragende Stahlwiederverwendung in einem marktfähigen Büroprojekt.

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Stahlträger/-stützen | Stahl | 9 t aus Grosvenor-Projekten / 15–16 t aus Cleveland-Steel-Bestand | Tragwerk / low-load applications, roofs oder temporäre Konstruktionen laut NLA | Stahlrahmen der Aufstockung / rooftop extension | 24–25 t | ja | ja | nein | nein | Rückbau, Prüfung, Primerentfernung, Refabrikation | neue Stahlanschlüsse | CST / P427; zerstörende und zerstörungsfreie Prüfungen | Tragfähigkeit, Stahlgüte, Duktilität, Ausführung | SCI P427/P440; EN 1090-Kontext | Beschaffung, Test, Programm, Kosten | [S1], [S3], [S4], [S5], [S8], [S9] | exakte Profilliste |
| Reclaimed stone / brickwork | Stein/Ziegel | unbekannt / andere Quellen | unbekannt | Bauteil-/Oberflächenreuse im Projekt | unbekannt | unbekannt | ja | teilweise | nein | unbekannt | unbekannt | unbekannt | Dauerhaftigkeit, Optik | unbekannt | unklare Menge | [S11] | genaue Herkunft und Rolle |
| bestehender Betonrahmen | Stahlbeton | Bestandsgebäude vor Ort | Tragwerk | bleibt Tragwerk | 90–93 % Bestand erhalten | ja | ja | nein | nein | untersucht / minimal verstärkt | bestehend | Bestandsuntersuchungen | Tragfähigkeit für Erweiterung | unbekannt | **zählt nicht als Direct Reuse** | [S2], [S4] | genaue Bauteilmenge |
| bestehende Fassade | unbekannt | Bestandsgebäude | Hülle | bleibt Hülle | Teil von 93 % Bestandserhalt | nein/teilweise | ja | ja | nein | Erhalt / Sanierung | bestehend | unbekannt | Wärme, Feuchte, Optik | unbekannt | Bestandserhalt, nicht Reuse | [S2], [S7] | Aufbau |
| CLT-Decken | Holz / CLT | neu / Eurban | keine | Decken in Erweiterung | unbekannt | ja | ja | nein | nein | neu | neue Stahl-Holz-Anschlüsse | unbekannt | Tragfähigkeit, Brand, Schwingung | unbekannt | nicht wiederverwendet | [S7], [S8] | Menge |
| Cemfree concrete | Beton/Bindemittel | neu | keine | Betonanteile | unbekannt | ja/teilweise | nein | nein | nein | neu | unbekannt | unbekannt | Tragfähigkeit | unbekannt | nicht wiederverwendet | [S2] | Menge |
| TGA | unbekannt | unbekannt | unbekannt | Büro-TGA | unbekannt | nein | nein | nein | ja | unbekannt | unbekannt | WELL/NABERS-Anforderungen | Betrieb, Luftqualität, Komfort | unbekannt | Energie-/Komfortanforderungen | [S7] | reused? nein/unbekannt |
| Geländer/Treppen/Fenster/Türen | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | teilweise | ja | teilweise | teils | unbekannt | unbekannt | unbekannt | Barrierefreiheit/Brandschutz | unbekannt | keine Reuse-Angaben | unbekannt | alle Details |

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Bestandsgebäude untersuchen und Retention maximieren | HTS, Projektteam | intrusive Untersuchungen / structural investigations | unbekannt | entfällt | minimale Verstärkung | Bestandsprüfung | komplexe Lage über Thames-Water-Sewer / Nähe Underground | Tragfähigkeit Bestand | Retention statt Abriss | [S2] |
| Bauteilinventar | geeigneten Reuse-Stahl identifizieren | Grosvenor, HTS, CST | Donor-Site-/Stock-Abgleich | Stockmatcher nicht sicher belegt | donor demolition | Sortierung | Vorprüfung | mehrere Quellen | verfügbare Profile passen nicht immer | frühzeitig Quellen sichern | [S1], [S5], [S6] |
| Schadstoffprüfung | unbekannt für Stahl; Primerentfernung erwähnt | CST/Contractors | unbekannt | unbekannt | Demontage aus donor sites | Primer entfernen | unbekannt | unbekannt | Beschichtungen / Fire protection können Aufwand erhöhen | low-load/roof/temporary steel bevorzugt | [S8] |
| Rückbau | Stahl aus Donor Site bergen | Donor-site contractor / CST | Demontage statt Schrott | Kran/Schneidtechnik unbekannt | selektiver Rückbau | unbekannt | Sichtprüfung | Koordination Donor–Fabricator | Programmrisiko | frühzeitige Vertrags-/Ablaufkopplung | [S5] |
| Ausbau | Stahl aus Grosvenor-Projekten und Stock entnehmen | Grosvenor, CST | Bauteilgewinnung | unbekannt | selektiv | Sortierung | CST testing | Transport zu Fertigung | Verfügbarkeit | CST als Stockist/Fabricator | [S1], [S5] |
| Transport | Stahl zu Fertigung und Baustelle | CST / Contractors | LKW-Transport | unbekannt | entfällt | entfällt | nach Testing | Koordinierter Lieferfluss | Zeit/Programm | direkte Zusammenarbeit | [S5] |
| Lagerung | Stahlbestand halten | Cleveland Steel and Tubes | reclaimed stock | Lagerbestand / Datenlisten | entfällt | Sortierung | Materialtests | Lagerflächen | Bestandsverfügbarkeit | professioneller Stockist | [S1], [S5] |
| Aufbereitung | Refabrikation für neue Struktur | CST | Zuschnitt, Bohrung, Primerentfernung | Werkstatttechnik | entfällt | Refabrication | P427-konform | Fertigung vor Einbau | unbekannte Materialeigenschaften | zerstörende/zerstörungsfreie Tests | [S5], [S9] |
| Planung | Stahlreuse früh in Low-Carbon-Strategie integrieren | Grosvenor, HTS, Barr Gazetas | Design mit available sections | Stockmatcher nicht sicher belegt | entfällt | Design substitution | engineering check | Programmeinbindung | floor-to-ceiling heights erforderten flache/schwere Profile | Reuse dort einsetzen, wo Profile passen | [S5] |
| Genehmigung | Tragwerksnachweise für Reuse-Stahl | HTS / Behörden | Design verification | unbekannt | entfällt | entfällt | Grade/Subgrade/Yield/Tensile | unbekannt | Versicherung/Haftung | P427/P440-Protokoll | [S3], [S9], [S10] |
| Wiedereinbau | Einbau im Stahlrahmen der Aufstockung | CST, Contractor | Stahlbau | Kran | entfällt | verschraubt/geschweißt unbekannt | Werk-/Baustellenkontrolle | zentrale Londoner Baustelle | enge Baustelle | koordinierte Lieferung | [S4], [S5] |
| Monitoring | Zertifizierungen / Carbon reporting | Projektteam | LCA / Embodied Carbon reporting | unbekannt | entfällt | entfällt | unbekannt | unbekannt | Kennwertabweichungen | transparente Quellenangaben | [S3], [S4], [S7] |

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | bestehender Betonrahmen plus neue Stahl-/CLT-Aufstockung | zusätzliche Geschosse / Dachterrasse | unbekannt | Bestandsuntersuchungen | Tragfähigkeit Bestand | minimale Verstärkung | [S2] |
| Lastabtragung | Reclaimed steel im neuen Rahmen | Stahlbaunachweise | SCI P427/P440; EN 1090-Kontext | engineering checks | unbekannte Stahlgüte | Materialprüfung | [S5], [S9], [S10] |
| Verbindung | neue Stahl- und Stahl/CLT-Verbindungen | Kraftübertragung, Montage | unbekannt | unbekannt | gebrauchte Profile mit neuen Anschlüssen | refabrication | [S5] |
| Brandschutz | Büro/Aufstockung; Schutzsysteme nicht detailliert | Feuerwiderstand | unbekannt | unbekannt | vorhandene Beschichtungen können Wiederverwendung erschweren | Profile aus low-load/roof/temporary applications bevorzugt | [S8] |
| Schallschutz | Bürostandard, unbekannt | Nutzerkomfort | unbekannt | unbekannt | CLT/Stahl-Hybrid | unbekannt | unbekannt |
| Feuchte | Dachterrasse/Aufstockung | Abdichtung | unbekannt | unbekannt | Schnittstelle Bestand/Neu | unbekannt | unbekannt |
| Wärmeschutz | Gesamtprojekt low carbon; operational carbon savings genannt | Energieeffizienz | BREEAM/WELL/NABERS-Ziele, keine Normnummern | Zertifizierung | Bestand + Neubau | Sanierung / elektrische Energie | [S7], [S8] |
| Wärmebrücken | unbekannt | Gebäudehülle | unbekannt | unbekannt | Stahl/Bestand-Anschlüsse | unbekannt | unbekannt |
| Luftdichtheit | unbekannt | Bürokomfort/Energie | unbekannt | unbekannt | Bestandssanierung | unbekannt | unbekannt |
| TGA-Integration | WELL/NABERS-Anforderungen relevant | Komfort, Luftfiltration, Energie | WELL, NABERS als Zertifizierung | Zertifizierungsprozess | Komfortanforderungen vs. Energieverbrauch | abgestimmtes Design | [S7] |
| Barrierefreiheit | unbekannt | UK building regulations | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Dauerhaftigkeit | wiederverwendeter Stahl nach Prüfung | erneute Nutzungsdauer | SCI P427/P440 | zerstörend/zerstörungsfrei | Herkunft/Alter | Test und Refabrikation | [S5], [S9], [S10] |
| Zulassung | Reuse-Stahl rechtlich/versicherungstechnisch anspruchsvoll | Nachweisfähigkeit | SCI P427/P440 | Testing | Versicherung/Haftung | evidence-based approach | [S3], [S5] |
| Haftung | Single-stage D&B erschwerte cost certainty | Risikoallokation | unbekannt | unbekannt | wenig Erfahrung mit Reuse-Stahl | frühe CST-Einbindung | [S5] |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| wiederverwendeter Stahl | 25 | t | IStructE / TERC | im Projekt verbaute reclaimed steel members | [S3], [S5] | belegt |
| wiederverwendeter Stahl | 24 | t | ASBP DISRUPT / Grosvenor-Angabe 9+15 t | rooftop extension | [S1], [S4] | belegt, abweichend |
| Stahl aus Grosvenor-Projekten | 9 | t | Projekt-/Fallstudienangabe | donor sites im Portfolio | [S1], [S5] | belegt |
| Stahl aus Cleveland Steel stock | 15–16 | t | Quellenvergleich | reclaimed stock | [S1], [S5], [S8] | belegt mit Abweichung |
| Gesamtstahlbedarf | ca. 70 | t | Grosvenor/IOM3 | Aufstockung / Stahlwork | [S1], [S12] | belegt |
| Anteil reused steel an Stahltonnage | 34 / ca. ein Drittel | % | Fach-/Projektquellen | Stahlstruktur | [S9], [S11] | belegt |
| GIA | 3.536 | m² | HTS Projektseite | Gebäude | [S2] | belegt |
| Added area | 2.322 | m² | Optoppen | Aufstockung/Erweiterung | [S8] | teilweise belegt |
| Bestandserhalt | 90–93 | % | HTS/NLA | bestehendes Gebäude/Struktur | [S2], [S8] | belegt, aber nicht als Direct Reuse zählen |
| CO₂-Einsparung Stahlreuse | 35 | t CO₂e | IStructE / ASBP DISRUPT | Vergleich zu neuem Stahl | [S3], [S5] | belegt |
| CO₂-Einsparung Stahlreuse | 45 | t CO₂e | HTS Projektseite | embodied carbon saved by reused steel | [S2] | belegt, abweichend |
| CO₂-Einsparung Stahlreuse | 60 | t CO₂e | Grosvenor/ASBP/IOM3 | beams and columns / total area | [S1], [S7], [S12] | belegt, abweichend |
| embodied carbon reused steel | 0,3 | kgCO₂e/kg | A1–A5 | wiederverwendeter Stahl nach Fabrication | [S3], [S5] | belegt |
| embodied carbon virgin steel Vergleich | 1,7 | kgCO₂e/kg | ASBP DISRUPT | virgin steel incl. fabrication | [S5] | belegt |
| structural embodied carbon | 62 / 65 / 67,5 | kgCO₂e/m² | HTS / IStructE / ASBP | Struktur, teilweise ohne Fassade | [S2], [S3], [S7] | belegt, abweichend |
| Gesamt embodied carbon | 267,9 / 300 | kgCO₂e/m² | Grosvenor/ASBP/TFT | Gesamtprojekt | [S1], [S7], [S11] | belegt, abweichend |
| operational carbon savings | 69 | % | ASBP | Betrieb | [S7] | belegt |
| site waste eliminated | 99 | % | TFT | Baustelle | [S11] | teilweise belegt |
| Zertifizierungen | BREEAM Outstanding, WELL Platinum, NABERS 5 star, WiredScore Gold | - | Projektangaben | Gebäude | [S7], [S8] | belegt |
| Kosten | unbekannt | GBP | unbekannt | Projekt / Reuse-Anteil | unbekannt | unklar |
| Transportdistanz | unbekannt | km | unbekannt | Stahlquellen | unbekannt | unklar |

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Verfügbarkeit passender Stahlprofile | logistisch/technisch | Reuse-Stahl kommt in vorhandenen Querschnitten und Längen | nicht alle Designpositionen ersetzbar | Bauteil, Bauteilbörse | frühe Suche, Stockist, Designanpassung | Reuse muss in Stage 2/3 starten | [S1], [S5] |
| Kosten-/Programmsicherheit | wirtschaftlich | wenig Erfahrung in D&B-Prozessen | Risikoaufschläge / Unsicherheit | Wirtschaft, Prozessphase | frühe CST-Einbindung | Lieferkette früh vertraglich einbinden | [S5] |
| Test- und Nachweisaufwand | technisch/rechtlich | unbekannte Stahlgüte und Herkunft | zusätzliche Prüfungen | Prüfung, Norm | P427-Tests, destructive/nondestructive testing | Reuse braucht standardisierte Prüfpfade | [S5], [S9], [S10] |
| Koordination Donor-Fabrication-Installation | logistisch | mehrere Baustellen und Akteure | Komplexer Ablauf | Logistik, Bauteilbörse | direkte Vertrags-/Kooperationslinien | Donor-Projekt ist Teil des Neubauprogramms | [S5] |
| Boden-/Geschosshöhenanforderungen | technisch/gestalterisch | flache schwere Profile erforderlich | bestimmter reused steel nicht nutzbar | Leistungsanforderung, Tragwerkssystem | gezielter Einsatz, wo Profile passen | Entwurf und Reuse-Bestand müssen iterieren | [S5] |
| Bestandserhalt vs. Reuse-Verwechslung | methodisch | 90/93 % retention ist sehr präsent | Rating könnte überschätzt werden | Fallstudie, Reuse-Strategie | Reuse strikt auf ex-situ Stahl begrenzen | saubere Bilanzgrenzen sind entscheidend | [S2], [S8] |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** Kombination aus interner Donor-Site-Beschaffung aus Grosvenor-Projekten und externem reclaimed stock über Cleveland Steel and Tubes; anschließend Prüfung und Refabrikation.
- **Bauteilbörse / Quelle:** Cleveland Steel and Tubes; zusätzlich Grosvenor-Portfolio, u. a. in ASBP/TERC mit Biscuit Factory Bermondsey und US Former Embassy genannt.
- **Kostenwirkung:** keine belastbaren Projektkosten öffentlich; TERC nennt cost certainty als Herausforderung im single-stage D&B-Prozess.
- **Zeitwirkung:** Programm- und Koordinationsrisiken belegt; genaue Mehr-/Minderzeit unbekannt.
- **Versicherung / Haftung:** Fachartikel/ISTructE nennt insurance als Thema; konkrete Police unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** erhöht für Sourcing, Testing, Refabrication, Koordination.
- **Lagerung:** über reclaimed steel stockist gelöst; konkrete Lagerdauer unbekannt.
- **Marktbarrieren:** verfügbare Stockprofile, Prüfkosten, Gewährleistung, Projektprogramm, fehlende Routine.

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** wahrscheinlich teilweise im Tragwerk sichtbar bzw. dokumentiert; genaue Oberflächenstrategie unbekannt. IStructE nennt aesthetics als Betrachtungspunkt.
- **räumliche Transformation:** Aufstockung und Retrofit machen ein 1980er-Bürogebäude zu einem modernen Arbeitsplatz.
- **Atmosphäre / Ausdruck:** Kombination aus Bestand, CLT und Stahl; genaue Innenraumwirkung unbekannt.
- **Umgang mit Spuren:** Primerentfernung und Refabrikation deuten auf technische Überformung; sichtbare Gebrauchsspuren unbekannt.
- **sozialer Wert:** Marktrelevanter Demonstrator für Reuse-Stahl in London; unterstützt Aufbau eines Second-hand-Stahlmarkts.
- **Denkmal- oder Bestandswert:** kein Denkmalstatus gefunden; Bestandserhalt und Fassade als nachhaltiger Wert.
- **Kritik / Grenzen:** teilweise Stahlreuse bei gleichzeitig großem Bestandserhalt; Kennwerte variieren; nicht alle Angaben zur Quelle und Bilanzgrenze sind konsistent.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** vollständige Profilliste, genaue Donor-Elemente, Transportdistanzen, Prüfprotokolle, Anschlussdetails, Kosten, Gewährleistungsmodell, genaue Rolle von Stockmatcher im Projekt.
- **Neue Entitäten sinnvoll:** Donor-Site-Stahl, Kennwertkonflikt, Reuse-Protokoll, Bestandserhalt-Warnung.
- **Fehlende Daten:** einheitliche CO₂-Bilanzgrenze; Mengen für reclaimed stone/brickwork; Transport und Lagerdauer; konkrete Versicherungs-/Haftungsvereinbarungen.
- **Zu prüfende Quellen:** vollständiger IStructE-Artikel von Robert Mills; TERC-PDF; Grosvenor-Projektunterlagen; Cleveland Steel Prüf-/Fabrication records; HTS Projektakte.

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja.
- **5 wichtigste Fakten:**
  1. Holbein Gardens ist 2023 fertiggestellt und nutzt wiederverwendeten Stahl in einer Aufstockung.
  2. Der Reuse-Stahl umfasst je nach Quelle 24–25 t bzw. ca. 34 % / ein Drittel der Stahltonnage.
  3. 9 t kamen aus Grosvenor-Projekten, 15–16 t aus Cleveland-Steel-Bestand.
  4. Stahl wurde geprüft, refabriziert und nach P427-Kontext eingesetzt.
  5. Der Fall ist wegen Bestandserhalt wichtig, aber die Direct-Reuse-Bewertung darf nur den eingebauten Reuse-Stahl und belegte weitere Reuse-Bauteile zählen.
- **5 wichtigste Bauteile:** wiederverwendete Stahlträger; wiederverwendete Stahlstützen; existing concrete frame als Nicht-Reuse-Bestand; CLT-Decken als neues Low-carbon-Bauteil; reclaimed stone/brickwork mit unklarer Menge.
- **5 wichtigste Hürden:** Profilverfügbarkeit; Test/Nachweis; Programm/Kosten; Koordination Donor–Fabricator–Baustelle; klare Bilanzgrenze zwischen Retention und Reuse.
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Stahlreuse braucht frühe Projektentscheidung und Lieferkettenintegration.
  2. Professionelle Stockists können Beschaffung und Qualitätssicherung ermöglichen.
  3. Prüfprotokolle wie SCI P427 schaffen Vertrauen für tragende Wiederverwendung.
  4. Reuse ist einfacher bei Profilen ohne komplizierte Beschichtungen, Einbetonierungen oder Studs.
  5. Kennwerte müssen mit Bilanzgrenze und Quelle dokumentiert werden.
- **5 offene Fragen:** genaue Profile; Transportdistanzen; Prüfberichte; Kosten-/Versicherungsmodell; tatsächlicher Umfang anderer wiederverwendeter Materialien.

## Quellen und Links

- [S0] Ausgangsliste des Nutzers: `gebäude4_wiederverwendung_direct_reuse_examples.md`, Eintrag 20.
- [S1] Grosvenor (2022): *Some of UK’s first salvaged steelwork reused in Holbein Gardens retrofit*. https://www.grosvenor.com/news-insights/some-of-uk%E2%80%99s-first-salvaged-steelwork-reused-in-holbein-gardens-retrofit
- [S2] Heyne Tillett Steel: *Holbein Gardens*. https://hts.uk.com/project/holbein-gardens/
- [S3] Institution of Structural Engineers / Robert Mills (2023): *Holbein Gardens: delivering a low-carbon structure with reclaimed steel*. https://www.istructe.org/journal/volumes/volume-101-%282023%29/issue-3/holbein-gardens-low-carbon-reclaimed-steel/
- [S4] New Steel Construction (2024): *MERIT – Holbein Gardens, London*. https://www.newsteelconstruction.com/wp/holbein-gardens-london/
- [S5] The Engineers Reuse Collective: *Case Study: Holbein Gardens*. https://terc.org.uk/54-2/
- [S6] UKGBC: *Reused Steel Stockmatcher*. https://ukgbc.org/resources/reused-steel-stockmatcher/
- [S7] ASBP: *Holbein Gardens*. https://asbp.org.uk/case-studies/holbein-gardens
- [S8] New London Architecture / Optoppen summaries. https://nla.london/projects/holbein-gardens-2 ; https://www.optoppen.org/projects/holbein-gardens
- [S9] Springer: *Reuse of Steel in the Construction Industry: Challenges and Opportunities*. https://link.springer.com/article/10.1007/s13296-023-00778-4
- [S10] SCI P427 reference record: *Structural Steel Reuse: assessment, testing and design principles*. https://www.researchgate.net/publication/339713300_SCI_P427_-_Structural_Steel_Reuse_assessment_testing_and_design_principles
- [S11] TFT Consultants: *Holbein Gardens, London*. https://www.tftconsultants.com/projects/holbein-gardens-london
- [S12] IOM3: *Steel from demolition site directly reused for construction*. https://www.iom3.org/resource/steel-reused-from-uk-s-first-steelworks.html
