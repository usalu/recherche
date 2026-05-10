---
id: "gjG_House_Gentbrugge"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "gjG House, Gentbrugge / Ghent — Fallstudie Direct Reuse / zirkuläres Bauen"
bauobjekt:
  - "gjG_House_Gentbrugge"
legacy_paths:
  - "Gebäude\\gjG_House_Gentbrugge.md"
projekt:
  - "gjG_House_Gentbrugge"
reuse_chain_detected: "False"
---
# gjG House, Gentbrugge / Ghent — Fallstudie Direct Reuse / zirkuläres Bauen

## Migration

- Fallstudie ID: gjG_House_Gentbrugge
- Legacy source count: 1
- Generated project: gjG_House_Gentbrugge
- Generated bauobjekt: gjG_House_Gentbrugge
- Extracted reuse_einsatz rows: 11
- Extracted datenpunkt rows: 12
- Extracted entity mapping rows: 20
- Reuse chain detected: False

## Legacy Content

### Legacy Source: Gebäude\gjG_House_Gentbrugge.md

- Map action: split_into_case_graph
- Primary target: fallstudie/gjG_House_Gentbrugge
- Secondary targets: projekt/gjG_House_Gentbrugge; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# gjG House, Gentbrugge / Ghent — Fallstudie Direct Reuse / zirkuläres Bauen

## 1. EINORDNUNG
- **Entscheidung:** VERGLEICHSFALL
- **Bewertung:** ★★★★☆
- **Begründung:** Wiederverwendete Ziegel bilden eine gekrümmte, strukturell autonome äußere Schale, die das Dach trägt und den Raum prägt. Der Fall ist tragwerks- und hüllenrelevant, aber ein Einfamilienhaus ohne öffentlich belegte Mengen-, Kosten- oder Prüfkennwerte.
- **Vertrauensgrad:** belegt für Prinzip; teilweise belegt für technische Details
- **Warnung Bestandserhalt:** nein
- **Warnung Möbel/Dekoration:** nein
- **Projektstatus:** gebaut

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | gjG House | untersuchtes Projekt | [S1], [S2], [S3] | belegt | experimentelles Haus aus BLAFs „Brick Wall City“-Forschung |
| Gebäude | Einfamilienhaus | neues Wohngebäude | [S1], [S2] | belegt | private single family house |
| Ort | Gentbrugge / Ghent, Belgien | Projektstandort | [S1], [S2], [S3] | belegt | nahe E17, ehemaliger Garten einer Villa des 19. Jh. |
| Projekt | gekrümmte Ziegelschale mit Innenstruktur | Reuse-Trag-/Hüllsystem | [S1], [S2] | belegt | Schale formt sich um vorhandene Bäume |
| People | BLAF Architecten | Architekt | [S1], [S2] | belegt | Designteam |
| People | Tecclem | Stabilität / Tragwerk | [S1], [S2] | belegt | als „Stability“ genannt |
| People | G-build | Structural work | [S1], [S2] | belegt | Ausführung Rohbau |
| People | Vlieghe | Carpentry | [S1], [S2] | belegt | Holzbau / Carpentry |
| People | Barbara Oelbrandt | EPB | [S1], [S2] | belegt | Energieperformance-Beteiligte |
| Bauteil | gekrümmte Außenmauer / Schale | wiederverwendete Ziegel als tragende Schale | [S1], [S2], [S3] | belegt | Schale ist strukturell autonom und trägt Dach |
| Material | wiederverwendete Ziegel | Haupt-Reuse-Material | [S1], [S2] | belegt | Herkunft/Menge unbekannt |
| Tragwerkssystem | formaktive, gekrümmte Ziegelschale + Stahl-/Holz-Infill | Hauptsystem | [S1], [S2] | belegt | Stabilität über Form und Ziegelverband, nicht über Querwände/Stützen/Träger |
| Reuse-Strategie | Bauteilwiederverwendung / Materialwiederverwendung | Reuse-Ziegel als Schale | [S1], [S2] | belegt | keine Recycling-Strategie |
| Methode | Brick Wall City / Big Brick | Forschungs-/Entwurfsrahmen | [S1] | belegt | Kritik an geklebten Fassadenschichten/End-of-life-Problemen |
| Leistungsanforderung | Strukturautonomie, Akustik, Dachauflager | Leistung der Schale | [S1], [S2] | belegt | massive Schale trägt auch zur Akustik bei |
| Kennwert | 190 m² | Bruttofläche | [S1], [S2] | belegt | 2045 ft² / 190 m² |
| Recht | EPB | Energieperformance-Bezug | [S1], [S2] | teilweise belegt | konkrete Norm-/Rechtsnummer unbekannt |
| Prüfung | unbekannt | Materialprüfung / Statik | keine Quelle | unbekannt | keine Prüfberichte gefunden |
| Hürde | Bäume / Lage / Lärm | gestalterisch, sozial, technisch | [S1], [S2] | belegt | Form folgt Bäumen; massive Schale verbessert akustischen Komfort |
| Wirtschaft | unbekannt | Kosten/Beschaffung | keine Quelle | unbekannt | keine belastbaren Daten gefunden |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Formaktive Reuse-Schale | erklärt, dass Stabilität durch Geometrie entsteht | gekrümmte Ziegelschale aus Reuse-Ziegeln | verbindet Tragwerkssystem, Verbindung, Reuse-Strategie |
| Reuse-Forschungsreihe | mehrere BLAF-Häuser untersuchen Ziegelreuse | Brick Wall City / Big Brick | verbindet Methode, Fallstudie, Material |

## 3. FALLSTUDIE
- **Name:** gjG House
- **Ort:** Gentbrugge / Ghent, Belgien
- **Gebäude:** Einfamilienhaus
- **Projekt:** Neubau mit gekrümmter strukturell autonomer Ziegelschale aus wiederverwendeten Ziegeln und innerem Stahl-/Holz-Infill
- **Beteiligte People / Akteure:** BLAF Architecten; Tecclem; G-build; Vlieghe; Barbara Oelbrandt; privater Bauherr
- **Architekt:** BLAF Architecten
- **Tragwerksplaner:** Tecclem / Stability
- **Bauherr:** privat / unbekannt
- **Zeitraum:** 2015 nach ArchDaily/Designboom; eine Sekundärquelle nennt 2017, daher 2015 priorisiert
- **Ursprüngliche Nutzung:** Ziegel aus unbekannter Herkunft; alte Funktion unbekannt
- **Neue Nutzung:** tragende, räumliche und hüllende Ziegelschale; Dachauflager
- **Fläche / Maßstab:** 190 m² / 2045 ft²
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** sehr gut für Konzept, Beteiligte und Traglogik; schwach für Materialherkunft, Mengen, Prüfungen, Kosten, Normen

## 4. REUSE-STRATEGIE
- **Art der Wiederverwendung:** partiell; ex-situ; Bauteil-/Materialwiederverwendung; keine Gebäudeversetzung; keine adaptive reuse.
- **Hauptniveau:** Tragwerk / Gebäudehülle / räumliche Struktur.
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die Ziegel werden als Ziegel in einer neuen tragenden Schale weiterverwendet; kein Bestandserhalt, keine reine Fassadenbekleidung, kein Recycling zu Zuschlagstoff.
- **Warum relevant:** Das Projekt zeigt, dass wiederverwendete Ziegel durch Form und Verband eine strukturell autonome Außenhülle bilden können; die reuse-relevante Leistung ist nicht dekorativ, sondern tragend und raumbildend.

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| gekrümmte Außenwand / Schale | wiederverwendete Ziegel | unbekannt | unbekannt | strukturell autonome Hülle; Dachauflager | unbekannt | ja | ja | ja | nein | Reinigung/Aufbereitung unbekannt | Ziegelverband; Mörtel unbekannt | unbekannt | Stabilität, Dachauflager, Akustik, Witterung | unbekannt | Altziegelqualität, Formgenauigkeit | [S1], [S2], [S3] | Menge, Herkunft, Prüfung |
| Dach | Material unbekannt | unbekannt | unbekannt | Abschluss; wird von Schale getragen | unbekannt | ja | nein | ja | nein | unbekannt | Auflager auf Schale | unbekannt | Lastabtragung/Witterung | unbekannt | Anschlussdetails | [S1], [S2] | Material, Reuse-Status |
| Infill-Struktur | Stahl und Holzrahmen | neu / unbekannt | nicht zutreffend | innere Wohnstruktur, 3 Geschosse in einem Bereich | unbekannt | ja | ja | nein | nein | nicht als Reuse belegt | unbekannt | unbekannt | Wohnnutzung | unbekannt | Einpassung in Schale | [S1], [S2] | genaue Konstruktion |
| Innenoberflächen der Schale | gleiche wiederverwendete Ziegel | unbekannt | unbekannt | Innenraumoberfläche / Außenraumgefühl | unbekannt | nein/Teil der Schale | ja | nein | nein | unbekannt | Mauerwerk | unbekannt | Raumwirkung | unbekannt | unbekannt | [S1], [S2] | Details |
| Fenster / Öffnungen | unbekannt | unbekannt | unbekannt | Belichtung | unbekannt | nein | ja | ja | nein | unbekannt | unbekannt | unbekannt | Wärme/Licht | unbekannt | Öffnungen in Schale | Fotos/Pläne, keine Detailquelle | alles |
| Türen | unbekannt | unbekannt | unbekannt | Zugang | unbekannt | nein | ja | ja | nein | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle | ja |
| Treppen | unbekannt | unbekannt | unbekannt | Erschließung | unbekannt | unbekannt | ja | nein | nein | unbekannt | unbekannt | unbekannt | Wohnnutzung | unbekannt | unbekannt | keine Quelle | ja |
| Geländer | unbekannt | unbekannt | unbekannt | Absturzsicherung | unbekannt | nein | ja | nein | nein | unbekannt | unbekannt | unbekannt | Sicherheit | unbekannt | unbekannt | keine Quelle | ja |
| Innenwände | Stahl-/Holzrahmen / unbekannt | neu / unbekannt | nicht zutreffend | Räume / Infill | unbekannt | teilweise | ja | nein | nein | nicht Reuse belegt | unbekannt | unbekannt | Wohnnutzung | unbekannt | unbekannt | [S1] | Reuse-Status |
| Dämmung | unbekannt | unbekannt | unbekannt | Energieperformance | unbekannt | nein | nein | nein | nein | unbekannt | unbekannt | unbekannt | EPB | EPB ohne Nummer | unbekannt | [S1] nur Kontext | Material/Werte |
| TGA | unbekannt | unbekannt | unbekannt | Gebäudetechnik | unbekannt | nein | nein | nein | ja | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle | ja |

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Grundstück mit Bäumen und Nähe zur E17 analysiert | BLAF | Entwurf um Bäume, Schale als Lärmpuffer | unbekannt | nicht relevant | nicht relevant | unbekannt | nicht relevant | Bäume, Lärm | gekrümmte Schale | [S1], [S2] |
| Bauteilinventar | wiederverwendete Ziegel als Schalenmaterial | BLAF / unbekannt | Material-/Formstrategie | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Qualität und Menge unbekannt | unbekannt | [S1] |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Altziegelrisiken | unbekannt | keine Quelle |
| Rückbau | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle |
| Ausbau | Ziegelbergung | unbekannt | unbekannt | unbekannt | selektiv vermutlich, aber unbelegt | unbekannt | unbekannt | unbekannt | Bruch/Qualität | unbekannt | keine Quelle |
| Transport | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Transportdistanz unbekannt | unbekannt | keine Quelle |
| Lagerung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle |
| Aufbereitung | Reuse-Ziegel in neuer Schale vermauern | G-build / unbekannt | Mauerwerk | unbekannt | nicht relevant | Reinigung/Sichtung unbekannt | unbekannt | Baustelle | gekrümmte Geometrie | Form und Verband sichern Stabilität | [S1], [S2] |
| Planung | autonome Schale und Infill entwickeln | BLAF, Tecclem | formaktive Tragwerksstrategie | unbekannt | nicht relevant | nicht relevant | statische Prüfung unbekannt | digital/analog unbekannt | Stabilität ohne Querwände/Stützen/Träger | gekrümmte Form + Ziegelverband | [S1], [S2] |
| Genehmigung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Reuse-Mauerwerk-Nachweis | unbekannt | keine Quelle |
| Wiedereinbau | Ziegel als tragende Schale | G-build, Tecclem, BLAF | Mauerwerk | unbekannt | nicht relevant | unbekannt | unbekannt | Baustelle | Formgenauigkeit | kurvige Schale | [S1], [S2] |
| Monitoring | unbekannt | unbekannt | unbekannt | unbekannt | nicht relevant | nicht relevant | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle |

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | gekrümmte wiederverwendete Ziegelschale; Infill aus Stahl/Holz | Schale stabil ohne Querwände/Stützen/Träger | unbekannt | unbekannt | Reuse-Ziegel in gekrümmter Schale | Stabilität durch Form und Mauerverband | [S1], [S2], [S3] |
| Lastabtragung | Schale trägt das Dach und bildet mit ihm eine „bell“ | Dachlasten, Wind, Eigenlast | unbekannt | unbekannt | Dachauflager in Altziegelschale | formaktive Hülle | [S1], [S2] |
| Verbindung | Ziegelverband; Dachanschluss unbekannt | Kraftschluss Schale/Dach | unbekannt | unbekannt | Mörtel/Verband/Altziegel | unbekannt | [S1] nur Prinzip |
| Brandschutz | unbekannt | unbekannt | unbekannt | unbekannt | Wohnhaus | unbekannt | keine Quelle |
| Schallschutz | massive Schale trägt zum akustischen Komfort bei | Lärm von E17 / Wohnkomfort | unbekannt | unbekannt | Autobahnnähe | massive Ziegelschale | [S1], [S2] |
| Feuchte | unbekannt | Witterung/Dauerhaftigkeit | unbekannt | unbekannt | Altziegel außen | unbekannt | keine Quelle |
| Wärmeschutz | EPB-Kontext; Details unbekannt | Energieperformance | EPB ohne Nummer | unbekannt | Ziegelhülle + Dämmung | hybrid mit Infill | [S1] |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | Dach-/Fensteranschlüsse | unbekannt | keine Quelle |
| Luftdichtheit | unbekannt | EPB | EPB ohne Nummer | unbekannt | gekrümmte Schale | unbekannt | keine Quelle |
| TGA-Integration | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle |
| Barrierefreiheit | unbekannt | unbekannt | unbekannt | unbekannt | mehrgeschossiges Wohnhaus | unbekannt | keine Quelle |
| Dauerhaftigkeit | massive Schale als dauerhafte Hülle | Dauerhaftigkeit/Akustik | unbekannt | unbekannt | Altziegelqualität | Mauerverband/Schale | [S1], [S2] |
| Wartung | unbekannt | unbekannt | unbekannt | unbekannt | Fassade/Feuchte | unbekannt | keine Quelle |
| Zulassung | unbekannt | unbekannt | unbekannt | unbekannt | wiederverwendete Ziegel als tragende Schale | unbekannt | keine Quelle |
| Haftung | unbekannt | unbekannt | unbekannt | unbekannt | Materialnachweis | unbekannt | keine Quelle |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| wiederverwendete Masse | unbekannt | t | unbekannt | Reuse-Ziegel | keine Quelle | unbekannt |
| Anzahl Bauteile | unbekannt | Stück | unbekannt | Reuse-Ziegel | keine Quelle | unbekannt |
| Fläche | 190 | m² | Projektdaten | Gebäude | [S1], [S2] | belegt |
| CO₂-Einsparung | unbekannt | kg/t CO₂e | unbekannt | Reuse-Ziegel | keine Quelle | unbekannt |
| Abfallvermeidung | unbekannt | kg/t | unbekannt | Reuse-Ziegel | keine Quelle | unbekannt |
| Transportdistanz | unbekannt | km | unbekannt | Ziegel | keine Quelle | unbekannt |
| Kosten | unbekannt | EUR | unbekannt | Projekt | keine Quelle | unbekannt |
| Bauzeit | unbekannt | Monate | unbekannt | Projekt | keine Quelle | unbekannt |
| Energiebedarf | unbekannt | kWh/m²a | unbekannt | Gebäude | keine Quelle | unbekannt |
| U-Wert | unbekannt | W/m²K | unbekannt | Hülle | keine Quelle | unbekannt |
| Lebensdauer | unbekannt | Jahre | unbekannt | Ziegelschale | keine Quelle | unbekannt |
| Zirkularitätskennwert | unbekannt | - | unbekannt | Projekt | keine Quelle | unbekannt |

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Stabilität ohne Querwände/Stützen/Träger | technisch/gestalterisch | Ziel einer freien Innenstruktur | Ziegelschale muss autonom wirken | Tragwerkssystem, Bauteil | gekrümmte Form + Mauerverband | Geometrie kann Reuse-Material leistungsfähiger machen | [S1], [S2] |
| Lärmbelastung durch E17 | technisch/sozial | Lage neben Autobahn | akustischer Komfort kritisch | Ort, Leistungsanforderung | massive Schale | Reuse-Masse kann akustischen Mehrwert liefern | [S1], [S2] |
| Baumerhalt | gestalterisch/sozial | bestehende Bäume auf Grundstück | Grundriss/Schale muss ausweichen | Ort, Methode | Hausform zwischen Bäumen | Reuse-Entwurf kann lokale Natur integrieren | [S1], [S2] |
| fehlende Materialdaten | rechtlich/technisch | Herkunft/Menge/Prüfung nicht publiziert | Forschungsbewertung lückenhaft | Prüfung, Material, Kennwert | unbekannt | Materialpässe wären nötig | keine Quelle |
| energetische Schichten | technisch | massive Ziegelhülle + EPB-Kontext | Details öffentlich nicht nachvollziehbar | Leistungsanforderung, Norm | hybrides Infill | Reuse-Hülle braucht klares Energiesystem | [S1] |

## 10. WIRTSCHAFT UND BESCHAFFUNG
- **Beschaffungsmodell:** unbekannt.
- **Bauteilbörse / Quelle:** unbekannt; keine Bauteilbörse belegt.
- **Kostenwirkung:** unbekannt.
- **Zeitwirkung:** unbekannt.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** gekrümmtes Mauerwerk und Reuse-Ziegel-Sortierung vermutlich arbeitsintensiv, aber öffentlich nicht quantifiziert.
- **Lagerung:** unbekannt.
- **Marktbarrieren:** fehlende Material-/Prüfdaten; Planungsaufwand; Mauerwerkskompetenz; Zulassung/Nachweise.

## 11. GESTALTUNG UND KULTURELLER WERT
- **Sichtbarkeit der Wiederverwendung:** hoch; Ziegel bleiben innen und außen sichtbar.
- **räumliche Transformation:** Reuse-Ziegel werden von Einzelsteinen zu einer autonomen räumlichen Schale.
- **Atmosphäre / Ausdruck:** robuste, monolithisch wirkende, kurvige Ziegelhülle; Innenraum wirkt wie Außenraum zwischen Bäumen.
- **Umgang mit Spuren:** wiederverwendete Ziegel erzeugen generische, zeitlose Materialität; konkrete Patinaselektion unbekannt.
- **sozialer Wert:** Erhalt vorhandener Bäume; akustischer Schutz im Wohnumfeld nahe Autobahn.
- **Denkmal- oder Bestandswert:** Grundstück war Teil eines Villengartens; Denkmalstatus unbekannt.
- **Kritik / Grenzen:** kleine Fallgröße; zu wenig belastbare Kennwerte; Herkunft und Prüfung der Ziegel unklar.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN
- **Welche bestehenden Entitäten wurden nicht gefunden?** Bauteilbörse, Abbruchmethode, Aufbereitungsmethode, Schadstoff, detaillierte Prüfung, Norm/Recht, Wirtschaft, Logistik, Software.
- **Welche neuen Entitäten wären sinnvoll?** Formaktive Reuse-Schale; Reuse-Forschungsreihe; akustischer Reuse-Mehrwert.
- **Welche Daten fehlen?** Herkunft, Anzahl, Masse, Prüfungen, Mörtel, Verbindung, CO₂, Kosten, Transportdistanz.
- **Welche Quellen müssten geprüft werden?** BLAF-Projektdossier; Tecclem-Statik; G-build-Ausführungsunterlagen; Bauakte; Materiallieferant.

## 13. ABSCHLUSS
- **Soll der Fall in die Hauptliste?** ja, als Vergleichsfall.
- **5 wichtigste Fakten:**
  1. Die Schale besteht aus wiederverwendeten Ziegeln.
  2. Die Schale ist strukturell autonom.
  3. Die Stabilität hängt von Form und Ziegelverband ab, nicht von Querwänden/Stützen/Trägern.
  4. Die Schale trägt das Dach.
  5. Das Haus hat 190 m² und wurde 2015 fertiggestellt.
- **5 wichtigste Bauteile:** Ziegelschale; Dach; Stahl-/Holz-Infill; Fensteröffnungen; Innenflächen der Schale.
- **5 wichtigste Hürden:** Altziegelprüfung; gekrümmtes tragendes Mauerwerk; akustische Anforderungen; Energieleistung; fehlende Kennwerte.
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Form kann die strukturelle Leistung von Reuse-Mauerwerk erhöhen.
  2. Reuse-Ziegel können tragend und raumbildend sein, nicht nur Fassade.
  3. Reuse-Masse kann akustischen Komfort unterstützen.
  4. Lokale Randbedingungen können Form und Kreislaufstrategie verbinden.
  5. Gute Projektdokumentation müsste Materialherkunft und Prüfung ergänzen.
- **5 offene Fragen:**
  1. Woher kamen die Ziegel?
  2. Welche Prüfungen wurden durchgeführt?
  3. Welche Mörtel-/Verbindungsdetails wurden verwendet?
  4. Wie hoch sind Masse und CO₂-Effekt?
  5. Wie wurden Wärme-/Feuchteanschlüsse gelöst?

## Quellen / Links
- [S1] ArchDaily — gjG House / BLAF Architecten: https://www.archdaily.com/951845/gjg-house-blaf-architecten
- [S2] Designboom — reused bricks / gjG House: https://www.designboom.com/architecture/blaf-architects-reused-bricks-gjg-house-belgium-10-30-2020/
- [S3] Archisearch — gjG House in Gentbrugge: https://www.archisearch.gr/architecture/gjg-house-in-gentbrugge-belgium-by-blaf-architects/
- [S4] Platform Architecture — gjG House: https://www.platformarchitecture.it/gjg-house/?lang=en
