---
entity: "quelle"
id: "Geb_ude_K118_Kopfbau_Halle_118_Winterthur_md"
title: "Geb_ude_K118_Kopfbau_Halle_118_Winterthur_md"
build_status: "promoted_phase42"
source_filename: "K118_Kopfbau_Halle_118_Winterthur.md"
---

# Geb_ude_K118_Kopfbau_Halle_118_Winterthur_md

**Sprache:** Deutsch  
**Arbeitsregel:** Gezählt werden nur wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Bestandserhalt der Halle allein wird nicht als Direct Reuse gewertet.  
**Kurzurteil:** sehr starker Hauptfall, weil die Aufstockung ein wiederverwendetes Stahltragwerk und viele weitere feste Bauteile aus Rückbauprojekten nutzt.

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | K.118 / Kopfbau Halle 118 | Untersuchter Fall | [S1], [S2], [S3] | belegt | Pionierprojekt zirkulären Bauens |
| Gebäude | bestehende Industriehalle Halle 118 | Bestandsgebäude / Sockel | [S1], [S4] | belegt | Bestandserhalt zählt nicht allein |
| Projekt | Aufstockung um 3 Etagen | Empfängerprojekt | [S1], [S2] | belegt | Studios, Werkstätten, Denk-/Arbeitsräume |
| Ort | Lagerplatz / Winterthur, Schweiz | Standort | [S2], [S4] | belegt | ehemaliges Sulzer-Areal |
| People | Stiftung Abendrot / Vorsorgestiftung Abendrot | Bauherr / Eigentümer | [S1], [S5] | belegt | Auftraggeberin |
| People | baubüro in situ | Architektur | [S1], [S2], [S4] | belegt | zentrale Planende |
| People | Zirkular GmbH | Fachplanung Bauteilwiederverwendung / spätere Gründung | [S1], [S5] | belegt | Projekt war Auslöser der Zirkular-Gründung |
| People | ZHAW IKE | Forschung / Dokumentation | [S5], [S6] | belegt | Kompendium / Case Study |
| People | Oberli Ingenieurbau AG | Bauingenieur / Civil engineer | [S4] | teilweise belegt | Quelle Arch2O |
| People | Josef Kolb AG | Holzbauingenieur | [S2], [S4] | teilweise belegt | Quelle ArchDaily/Arch2O |
| People | Wetter AG | Stahlbau | [S4] | teilweise belegt | Quelle Arch2O |
| Bauteil | Stahlträger / Stützen / Profilbleche Verbunddecken | tragende Wiederverwendung | [S1], [S6] | belegt | zentraler ★★★★★-Grund |
| Bauteil | externe Stahltreppe | Zugang / Fluchtweg / räumliches Bauteil | [S3], [S7] | belegt | 22 m hoch; ehem. Orion-Bürogebäude Zürich |
| Bauteil | Fenster | Hülle | [S3], [S6] | belegt | wiederverwendet |
| Bauteil | Metallblech / Profilblech / Fassadenblech | Hülle / Bekleidung | [S3], [S7] | belegt | rotes wiederverwendetes Blech als Ausdruck |
| Bauteil | EPS-Dämmung | Hülle / Wärmeschutz | [S3], [S7] | belegt | Leistung im Detail unbekannt |
| Bauteil | Naturstein-/Granitplatten | Boden/Belag | [S3], [S7] | belegt | feste Bauteile |
| Bauteil | Klinker / Backstein | Wand/Belag | [S3], [S7] | belegt | Umfang unbekannt |
| Bauteil | Holzdachelemente / Holzwerkstoffe / Türen / Dreischichtplatten | Ausbau / Hülle / Innenräume | [S6], [S8] | teilweise belegt | Einzeldetails unbekannt |
| Reuse-Strategie | Bauteilsuche + Entwurf aus Verfügbarkeit | Prozessstrategie | [S1], [S3], [S5] | belegt | „Catch of the day“ / reversed planning |
| Methode | Katalogisieren, Prüfen, Lagermanagement | Bauteilprozess | [S1], [S3] | belegt | detaillierte Prozesse im Kompendium |
| Kennwert | 14 % Wiederverwendungsrate nach Gewicht | quantitativ | [S6] | belegt | wegen neuer schwerer Beton-/Fundamentteile |
| Kennwert | 41 % Wiederverwendungsrate nach Volumen | quantitativ | [S6] | belegt | hohe Leichtbauteilquote |
| Kennwert | 59 % CO₂-Reduktion / 494 t CO₂ | Klimawirkung | [S3], [S7] | belegt | gegenüber Neubaukomponenten / Vergleichsmodell |
| Kennwert | ca. 500 t Primärmaterial eingespart | Ressourceneffekt | [S3], [S4] | teilweise belegt | Quelle EGGA/Arch2O |
| Norm/Recht | keine konkrete Normnummer öffentlich | — | — | unklar | Projektnachweise nicht vollständig offen |
| Hürde | heutige Bauprozesse, Kosten-/Verfahrenslogik | Wirtschaft/Prozess | [S5], [S6] | belegt | Case Study benennt Hindernisse |
| Wirtschaft | Kosten etwa vergleichbar mit ähnlichem Neubau | Kostenwirkung | [S3], [S8] | teilweise belegt | genaue Kosten unbekannt |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Bauteiljäger / component hunting | beschreibt aktive Suche nach verfügbaren Bauteilen | Zirkular/baubüro in situ Bauteilsuche | Methode, Prozessphase, Tool |
| Materialdepot / Lagerverwaltung | Lagerung ist planungsrelevant | Verwaltung und Lagerung wiederverwendeter Bauteile | Logistik, Bauteil, Werkzeug |
| Reuse-Rate nach Gewicht/Volumen | klassische Massenbilanz unterschätzt Leichtbauteile | 14 % Gewicht, 41 % Volumen | Kennwert, Datenmodell |
| Umgekehrter Entwurfsprozess | Entwurf folgt Bauteilfund, nicht umgekehrt | Treppenpodeste bestimmen Geschosshöhen | Methode, Gestaltung, Tragwerk |

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; Bestandstransformation; adaptive reuse des Bestands als Kontext, aber nicht Score-Grundlage
- **Hauptniveau:** Tragwerk plus Gebäudehülle und räumlicher Innenausbau
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Der Bestandsbau wurde aufgestockt, aber die Direct-Reuse-Bewertung kommt aus Bauteilen, die aus anderen Rückbauprojekten in K.118 neu eingesetzt wurden. Das bloße Weiterbenutzen der bestehenden Halle wird nicht als Direct Reuse gezählt.
- **Warum ist der Fall relevant?** K.118 zeigt einen dokumentierten Prozess vom Bauteilsuchen über Lagerung, Planung, Prüfung, Kosten- und CO₂-Auswertung bis zur Ausführung. Besonders relevant ist, dass tragende Stahlbauteile wiederverwendet wurden.

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Suche nach geeigneten Rückbauteilen | baubüro in situ, Zirkular | component hunting | unbekannt | — | — | Vorbewertung | verschiedene Quellen | Bauteile nicht planbar wie Neuwaren | Entwurf parallel zur Bauteilsuche | [S1], [S3], [S5] |
| Bauteilinventar | Katalogisierung der gefundenen Bauteile | Zirkular/Planungsteam | Katalogisieren, Anforderungen zuordnen | unbekannt | — | — | Zustand/Geometrie | Lagerverwaltung | Informationslücken | Reuse-Planung | [S1], [S3] |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Altstoffe möglich | unbekannt | — |
| Rückbau | Bauteile aus ELYS/Orion/weiteren Quellen entnommen | Donorgebäude-Akteure | selektiver Rückbau | unbekannt | Teilrückbau | schonende Demontage | unbekannt | Transport nach Winterthur | Beschädigungsrisiko | zerstörungsarme Demontage | [S1], [S3], [S7] |
| Ausbau | Treppe, Stahl, Fenster, Platten ausgebaut | Rückbau-/Fachfirmen | Demontage | unbekannt | selektiv | Reinigung/Anpassung | unbekannt | Zwischenlager | Maße und Zustand | Bauteilwahl nach Passung | [S3], [S7] |
| Transport | Bauteile aus Basel/Zürich/anderen Quellen nach Winterthur | Fachfirmen | Bauteillogistik | unbekannt | — | — | unbekannt | regionale Transporte | Timing/Lager | Lager- und Prozessmanagement | [S1] |
| Lagerung | Bauteile bis Einbau gelagert | Zirkular/Team | Lagerverwaltung | unbekannt | — | Schutz vor Schäden | unbekannt | Lagerflächen | Platzbedarf | frühzeitige Lagerplanung | [S1] |
| Aufbereitung | Reinigung, Anpassung, Ergänzungen | Handwerker/Fachplaner | handwerkliche Aufarbeitung | unbekannt | — | Zuschnitt, Geländerfüllungen, Montagevorbereitung | unbekannt | Werkstatt/Baustelle | Arbeitsaufwand | lokales Handwerk | [S3], [S7] |
| Planung | Entwurf folgt verfügbaren Bauteilen | baubüro in situ | umgekehrter Entwurf | CAD/BIM unbekannt | — | — | Planungsabgleich | — | Bauteile geben Maße vor | iterative Planung | [S3], [S7] |
| Genehmigung | unbekannt | unbekannt | unbekannt | unbekannt | — | — | unbekannt | — | Reuse in Standardprozessen schwer | unbekannt | [S6] |
| Wiedereinbau | Aufstockung aus Reuse-/Bio-/Neumaterialien errichtet | Ausführungsteam | Montage | unbekannt | — | — | unbekannt | Baustelle | Koordination vieler Einzelquellen | integrierte Bauleitung | [S2], [S3] |
| Monitoring | wissenschaftliche Auswertung | ZHAW, baubüro in situ, Zirkular | Case Study / Kompendium | unbekannt | — | — | CO₂-/Ressourcenbilanz | — | Datenverfügbarkeit | publizierte Fallstudie | [S5], [S6] |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Fläche | 1.100 | m² | Projektangabe | Aufstockung | [S2], [S4] | belegt |
| Geschosse Aufstockung | 3 | Geschosse | Projektangabe | Erweiterung | [S1] | belegt |
| Wiederverwendungsrate Gewicht | 14 | % | Case Study K.118 | Bauteilgewicht | [S6] | belegt |
| Wiederverwendungsrate Volumen | 41 | % | Case Study K.118 | Bauteilvolumen | [S6] | belegt |
| CO₂-Reduktion | 59 | % | Vergleich mit neuen Bauteilen | Erstellungsphase / Bauteile | [S3], [S7] | belegt |
| CO₂-Reduktion absolut | 494 | t CO₂ | Vergleichsmodell | Erstellungsphase / Bauteile | [S3], [S7] | belegt |
| Primärmaterial eingespart | ca. 500 | t | Vergleichsmodell | Bauteile / Primärmaterial | [S3], [S4] | teilweise belegt |
| CO₂-Beitrag Stahlreuse | ca. 80 | t CO₂ / 16 % | Vergleichsmodell | Stahl | [S3], [S7] | teilweise belegt |
| Kostenwirkung | vergleichbar mit ähnlichem Neubau | qualitativ | Projektbericht/Artikel | Gesamtkosten | [S3], [S8] | teilweise belegt |
| Bauzeit | unbekannt | — | — | — | — | unklar |
| U-Wert | unbekannt | — | — | — | — | unklar |
| Lebensdauer | unbekannt | — | — | — | — | unklar |
| Zirkularitätskennwert | unbekannt | — | — | — | — | unklar |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** aktive Bauteilsuche in Rückbauprojekten; projektbezogene Sicherung, Lagerung und Wiedereinbau.
- **Bauteilbörse / Quelle:** keine klassische Bauteilbörse belegt; Quellen sind konkrete Rückbauprojekte wie ELYS Basel und Orion Zürich.
- **Kostenwirkung:** Quellen beschreiben Kosten im Rahmen eines vergleichbaren Neubaus; eingesparte Materialkosten verschieben sich zu höherem Arbeits-/Handwerksaufwand.
- **Zeitwirkung:** unbekannt; Prozess offensichtlich länger/iterativer wegen Suche, Lagerung, Anpassung.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** erhöht durch Suche, Katalogisierung, Prüfung, Anpassung und handwerkliche Aufbereitung.
- **Lagerung:** Teil des dokumentierten Prozesses; genaue Lagerkosten unbekannt.
- **Marktbarrieren:** heutige Bauwirtschaft ist auf Neuprodukte, feste Ausschreibungen und klare Produktgarantien ausgelegt.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** konkrete Normnummern, Bauteilbörse, Software, genaue Prüfberichte, Versicherung, Gewährleistung.
- **Welche neuen Entitäten wären sinnvoll?** Bauteiljäger; Materialdepot; Reuse-Rate nach Gewicht/Volumen; umgekehrter Entwurfsprozess.
- **Welche Daten fehlen?** vollständiges Bauteilinventar mit Mengen; Stahlprofil- und Prüfdetails; detaillierte Kosten; Lagerdauer; Brandschutz- und Schallschutzdetails.
- **Welche Quellen müssten geprüft werden?** Buch „Bauteile wiederverwenden“; Journal-of-Physics-Case-Study-Volltext; Ausführungspläne; Ausschreibungsunterlagen; Bauteilkatalog.

## Quellen und Links

[S1] Zirkular — K.118 / Kopfbau Halle 118: https://zirkular.net/de/projekt/k-118-kopfbau-halle-118/  
[S2] ArchDaily — K118 Kopfbau Halle 118 / baubüro in situ: https://www.archdaily.com/968958/k118-kopfbau-halle-118-hauburo-in-situ  
[S3] EGGA — K.118 from former factory to beacon of sustainable building: https://www.galvanizingeurope.org/case_studies/k-118-from-former-factory-to-beacon-of-sustainable-building/  
[S4] Arch2O — K118 Kopfbau Halle 118: https://www.arch2o.com/k118-kopfbau-halle-118-bauburo-in-situ/  
[S5] Zirkular — Reuse in Construction / Kompendium: https://zirkular.net/en/project/reuse-in-construction-a-compendium-of-circular-architecture/  
[S6] ResearchGate — Case Study K.118, Journal of Physics Conference Series: https://www.researchgate.net/publication/376148869_Case_Study_K118_-_The_Reuse_of_Building_Components_in_Winterthur_Switzerland  
[S7] Intergalva — K.118 Kopfbau Halle 118: https://intergalva.com/awards/global-galvanizing-awards-2024/k-118-kopfbau-halle-118/  
[S8] ArchDaily text excerpt / project description: https://www.archdaily.com/968958/k118-kopfbau-halle-118-hauburo-in-situ  
[S9] ZHAW sustainable blog — Bauteile wiederverwenden und CO₂-Emissionen reduzieren: https://blog.zhaw.ch/sustainable/2022/06/28/bauteile-wiederverwenden-und-co2-emissionen-reduzieren/
