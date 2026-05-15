---
entity: "quelle"
id: "Geb_ude_Chiro_d_Itterbeek_Dilbeek_md"
title: "Geb_ude_Chiro_d_Itterbeek_Dilbeek_md"
build_status: "promoted_phase42"
source_filename: "Chiro_d_Itterbeek_Dilbeek.md"
---

# Geb_ude_Chiro_d_Itterbeek_Dilbeek_md

**Recherchezeitpunkt:** 2026-05-06  
**Sprache:** Deutsch  
**Grundregel angewandt:** Gezählt werden feste Bau-, Hüll-, Technik- und Innenausbauteile. Lose Möbel werden nicht bewertet. Bei diesem Fall zählen u. a. Fassadenziegel, Fenster/Türen, Fliesen, Sanitär, Leuchten und feste technische Bauteile; bloße „surplus“-Neumaterialien werden separat markiert.

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Sanitary block for the Itterbeek Chiro / Pavillon de sanitaires | Untersuchter Fall | [S1], [S2], [S3], [S4] | belegt | Ausgangsliste hatte „verify“; Quellen bestätigen Reuse umfassend. |
| Gebäude | Sanitärpavillon neben alter Farm | Zielgebäude | [S2], [S3] | belegt | Kleine Erweiterung für Jugendorganisation Chiro. |
| Projekt | Neubau/Extension + Renovation-Kontext | Projektart | [S2] | belegt | 2018 Baujahr, 2019 Lieferung. |
| Ort | Plankenstraat 23, 1701 Dilbeek, Belgien | Standort | [S2] | belegt | Itterbeek / Dilbeek. |
| People | Rotor asbl-vzw | Entwurf / Design-Build | [S2], [S3], [S4] | belegt | Designer-contractor laut Construction21. |
| Bauherr | Commune de Dilbeek | Eigentümer Sanitärblock / Auftraggeber | [S2], [S4] | belegt | Farm selbst Eigentum kirchlicher Verwaltung. |
| People | CC Autrement | Konstrukteur / Ausführung | [S2], [S4] | belegt | Partner im Design-Build. |
| Bauteilbörse | Franck, RotorDC, Gebruiktebouwmaterialen, Namur Croisade pauvreté, Bouwstocks, kleine Anzeigen | Lieferquellen | [S2], [S4], [S5], [S6] | belegt | Mischung Händler, Spende, Restposten, Kleinanzeigen. |
| Bauteil | Fassadenziegel | Reuse-Hülle | [S2], [S3], [S4] | belegt | 30 m². |
| Bauteil | Stahl-U-Profile als Außenstürze | Reuse-Konstruktion/Fassade | [S2], [S4] | belegt | 5 lfm / 2 U-Profile. |
| Bauteil | Dachziegel | Reuse/Restposten Dach | [S2], [S4] | belegt | 20 m², Rest einer Brüsseler Villa-Renovierung. |
| Bauteil | Außentüren und Holzfenster | Reuse-Hülle | [S2], [S4] | belegt | 2 Türen, 2 Holzfenster. |
| Bauteil | Boden- und Wandfliesen | Reuse-Innenausbau | [S2], [S4] | belegt | 14 m² Boden / 11 m² Wand. |
| Bauteil | Sanitär | Reuse-Technik | [S2], [S4] | belegt | 4 WCs, 2 Urinale, 3 Art-déco-Waschbecken, Urinaltrenner. |
| Bauteil | Leuchten | Reuse-Technik | [S2], [S4] | belegt | 5 Leuchten. |
| Material | Dämmung, Betonblöcke, Holzrahmen | Restposten / Produktionsüberschüsse | [S2], [S4] | belegt | Nicht immer Direct Reuse; als Surplus dokumentieren. |
| Kennwert | weniger als ein Drittel neue Materialien nach Masse | zirkulärer Gesamtanteil | [S2], [S3] | belegt | Wichtig, aber Mischung aus Reuse und Surplus. |
| Kennwert | 4.572,702786 kg CO₂ vermieden | Umweltkennwert | [S2], [S4] | belegt | Construction21-Rechner; Bilanzgrenze beachten. |
| Prozessphase | alle klassischen Neubauphasen durchgeführt | Übertragbarkeit | [S2], [S3] | belegt | Fundamente, Kanalisation, Rohbau, Sanitär, Elektro, Innenausbau. |
| Hürde | logistisch-organisatorische Hindernisse | Ziel des Projekts | [S2], [S3] | belegt | Pilot/learning experience. |
| Wirtschaft | 55.000 € Bau-/Renovierungskosten; 15 m² | Kennwert | [S2] | belegt | Kosten/m² angegeben. |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Surplus-/Restpostenmaterial | Viele eingesetzte Bauteile sind keine gebrauchten Bauteile, sondern Baustellen-/Produktionsüberschüsse. | Dämmung, Betonblöcke, Holzrahmen aus Restposten/End-of-stock. | Ergänzt Material, Bauteilbörse, Wirtschaft, Reuse-Strategie. |
| Design-Build-Reuse | Entwurf und Ausführung liegen bei einer reuse-erfahrenen Organisation; wichtig für Haftung/Koordination. | Rotor als concepteur-contractant mit CC Autrement. | Verknüpft Projekt, Prozessphase, Wirtschaft und Hürde. |

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; Materialwiederverwendung; Technik-/Sanitärreuse; Hüllenreuse; ergänzt durch Restposten-/Surplus-Materialien
- **Hauptniveau:** Gebäudehülle + räumlicher Innenausbau + technische Gebäudeausrüstung + Material
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Der Sanitärblock ist neu, aber verwendet wiederverwendete Bauteile und Restposten. Reuse ist nicht Recycling zu Granulat; Bauteile bleiben als Ziegel, Fliesen, Fenster, Sanitär, Leuchten usw. erhalten.
- **Warum ist der Fall relevant?** Trotz nur 15 m² zeigt der Fall sehr konkret, welche Bauteilgruppen in einem klassischen Neubauprozess mit Reuse/Surplus umgesetzt werden können und welche logistischen Hürden auftreten.

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Bedarf Sanitärblock + bestehender Farmkontext | Commune de Dilbeek, Rotor | Entwurfs-/Bedarfsanalyse | unbekannt | entfällt | entfällt | unbekannt | Standortanalyse | Integration in Backsteinumfeld | Fassadenmaterial Backstein | [S2], [S3] |
| Bauteilinventar | möglichst viele Reuse-/Surplus-Bauteile identifiziert | Rotor, Händler | Materialsuche nach Baulos | Opalis-Händlernetz / Marketplace | unbekannt | Sortierung/Reinigung | unbekannt | viele kleine Quellen | Koordination vieler Quellen | Design-Build mit reuse-erfahrenem Akteur | [S2], [S4] |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Sanitär/Fliesen/Leuchten gebraucht | unbekannt | keine Quelle |
| Rückbau | vorgelagert bei Lieferanten/Herkunftsorten | Händler | selektive Rückgewinnung unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | ex-situ | unbekannt | Nutzung etablierter Händler | [S2], [S4] |
| Ausbau | Entnahme von Ziegeln, Fliesen, Sanitär, Türen/Fenstern | Händler/Lieferanten | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Bruch/Kompatibilität | robuste Bauteile | [S2], [S4] |
| Transport | Lieferung mehrerer kleiner Lots | Rotor, Händler, Ausführende | Kleinmengenlogistik | unbekannt | entfällt | unbekannt | unbekannt | meist Region Brüssel laut Quelle | Transportaufwand beachten | regionale Quellen | [S2], [S4] |
| Lagerung | kurzzeitige Baustellen-/Materiallagerung | Rotor/CC Autrement | unbekannt | unbekannt | entfällt | unbekannt | unbekannt | Baustelle | Sortierung, Bruch | unbekannt | keine Quelle |
| Aufbereitung | Reinigung/Anpassung | Händler/CC Autrement | unbekannt | unbekannt | entfällt | unbekannt | unbekannt | unbekannt | Zeit/Arbeitsaufwand | Händler und kleine Chargen | [S2], [S4] |
| Planung | Entwurf auf verfügbare Komponenten abgestimmt | Rotor | Design-Build / reuse-led design | unbekannt | entfällt | Auswahl | unbekannt | Beschaffung parallel zu Planung | Bauteilverfügbarkeit | Materialmix aus Reuse, Surplus, neu | [S2], [S3] |
| Genehmigung | kommunales Bauprojekt | Commune de Dilbeek | unbekannt | unbekannt | entfällt | unbekannt | unbekannt | unbekannt | öffentliches kleines Projekt | Design-Build-Auftrag | [S2] |
| Wiedereinbau | Umsetzung aller Gewerke | Rotor, CC Autrement | klassischer Neubauprozess mit Reuse/Surplus | unbekannt | entfällt | Bauteile eingebaut | unbekannt | Baustelle | Passung, fehlende Dachziegel | zusätzliche Suche; keine monetäre Einbuße laut Quelle | [S2], [S4] |
| Monitoring | Umweltkennwerte berechnet / Nutzungsenergie nicht präzise | Construction21/Rotor | Impact-Rechner / Erfahrungsbericht | unbekannt | entfällt | entfällt | unbekannt | nach Projekt | Energieverbrauch unbekannt | Nutzung: Wochenende, geringe Verbraucher beschrieben | [S2], [S4] |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Nettofläche | 15 | m² | Construction21 | Gebäude | [S2] | belegt |
| Kosten Bau/Renovierung | 55.000 | € | Construction21 | Projekt | [S2] | belegt |
| Kosten/m² | 3.666,67 | €/m² | Construction21 | Projekt | [S2] | belegt |
| neue Materialien | weniger als 1/3 | % Masse | Projektangabe | gesamte Materialmasse | [S2], [S3] | belegt |
| Fassadenziegel Reuse | 30 | m² | Projektangabe | Fassade | [S2], [S4] | belegt |
| Außenstürze Reuse | 5 | lfm | Projektangabe | Fassade | [S2], [S4] | belegt |
| Dachziegel Reuse/Rest | 20 | m² | Projektangabe | Dach | [S2], [S4] | belegt |
| Außentüren/Fenster | 2 + 2 | Stück | Projektangabe | Hülle | [S2], [S4] | belegt |
| Bodenfliesen Reuse | 14 | m² | Projektangabe | Boden | [S2], [S4] | belegt |
| Wandfliesen Reuse | 11 | m² | Projektangabe | Wand | [S2], [S4] | belegt |
| Sanitär Reuse | 4 WCs, 2 Urinale, 3 Waschbecken, 1 Trenner | Stück | Projektangabe | Sanitär | [S2], [S4] | belegt |
| Leuchten Reuse | 5 | Stück | Projektangabe | Elektro/Beleuchtung | [S2], [S4] | belegt |
| Dämmung Boden/Wand Surplus | 43,3 | m² | Projektangabe | Dämmung | [S2], [S4] | belegt |
| Dämmung Decke Surplus | 18 | m² | Projektangabe | Dämmung | [S2], [S4] | belegt |
| Betonblöcke Surplus | 48 | m² | Projektangabe | Rohbau | [S2], [S4] | belegt |
| Holzrahmen Surplus | 49,2 | lfm | Projektangabe | Charpente | [S2], [S4] | belegt |
| vermiedenes CO₂ | 4.572,702786 | kg CO₂ | Construction21-Impactberechnung; PMR-Bars/Wickeltisch ausgenommen | Reuse-/Surplus-Materialeinsatz | [S2], [S4] | belegt |
| vermiedener Wasserverbrauch | 122,8623915 | m³ | Construction21-Impactberechnung | Reuse-/Surplus-Materialeinsatz | [S2], [S4] | belegt |
| vermiedene Abfälle | 5.400,626347 | kg | Construction21-Impactberechnung | Reuse-/Surplus-Materialeinsatz | [S2], [S4] | belegt |
| Energiebedarf Betrieb | unbekannt | kWh/m²a | Quelle sagt keine präzisen Informationen | Betrieb | [S2], [S4] | unbekannt |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** kommunaler Auftrag; Design-Build/Designer-Contractor Rotor mit CC Autrement.
- **Bauteilbörse / Quelle:** Franck für Ziegel; Gebruiktebouwmaterialen für Stahlprofile/Dämmung; RotorDC für Fliesen, Sanitär, Leuchten; Namur Croisade pauvreté für Türen/Fenster; Bouwstocks für Surplus-Dämmung/Betonblöcke/Holz; private Brüsseler Baustelle/Villa-Renovierung als Spende für Dachziegel.
- **Kostenwirkung:** Gesamt 55.000 € / 3.666,67 €/m² belegt; spezifische Mehr-/Minderkosten durch Reuse unbekannt. Dachziegellos: Quelle nennt keinen Geldverlust, aber Zeitverlust/Nachsuche.
- **Zeitwirkung:** kleine Zeitverluste bei fehlenden Dachziegeln belegt; sonst unbekannt.
- **Versicherung / Haftung:** unbekannt; Design-Build könnte Koordination vereinfachen, ist aber kein belegter Haftungsnachweis.
- **Gewährleistung:** unbekannt
- **Arbeitsaufwand:** erhöht durch Suche, Koordination, Anpassung und Wiedereinbau; nicht quantifiziert.
- **Lagerung:** unbekannt
- **Marktbarrieren:** Verfügbarkeit, Mengenunsicherheit, Prüfnachweise, elektrische/sanitäre Kompatibilität, Transportkosten auch bei Gratisware.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** Normnummern, detaillierte Prüfung, Schadstoffprüfung, Tragwerksplanung, Software/Datenmodell, Versicherung/Gewährleistung, Lagerung im Detail.
- **Welche neuen Entitäten wären sinnvoll?** Surplus-/Restpostenmaterial; Design-Build-Reuse; Kleinmengenlogistik; Gratis-/Spendenmaterial.
- **Welche Daten fehlen?** genaue Prüfungen von Leuchten/Sanitär/Fenstern/Stahlprofilen, Gewährleistungsmodell, exakte Transportdistanzen, Betriebsmessdaten, Lebensdauerannahmen.
- **Welche Quellen müssten geprüft werden?** Rotor-Projektdossier, Ausführungs-/Prüfunterlagen, Rechnungen/Liefernachweise, kommunale Ausschreibung, technische Details der Stürze und Anschlüsse.

## Quellen und Links

- [S1] Interne Ausgangsliste: `gebäude4_wiederverwendung_direct_reuse_examples.md`, Priorität 56.
- [S2] Construction21 France – Pavillon de sanitaires du Chiro d’Itterbeek: https://www.construction21.org/france/case-studies/h/pavillon-de-sanitaires-du-chiro-d-itterbeek.html
- [S3] Rotor – Sanitary block for the Itterbeek Chiro: https://rotordb.org/en/projects/sanitary-block-itterbeek-chiro
- [S4] Construction21 Belgique – Pavillon de sanitaires du Chiro d’Itterbeek (Dilbeek): https://www.construction21.org/belgique/case-studies/h/pavillon-de-sanitaires-du-chiro-d-itterbeek-dilbeek.html
- [S5] Opalis – Rotor Deconstruction: https://opalis.eu/en/dealers/rotor-deconstruction
- [S6] Opalis – Franck Bricks: https://opalis.eu/en/dealers/franck-bricks
- [S7] Adokin – Bricks / Chiro d’Itterbeek summary: https://adokin.eu/fr/tag/briques/
