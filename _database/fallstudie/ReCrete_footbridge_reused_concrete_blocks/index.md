---
entity: "fallstudie"
id: "ReCrete_footbridge_reused_concrete_blocks"
title: "Re:Crete footbridge — Fallstudie Direct Reuse"
build_status: "promoted_phase42"
legacy_paths:
  - "Gebäude\\ReCrete_footbridge_reused_concrete_blocks.md"
node_kind: "core"
bauobjekt:
  - "ReCrete_footbridge_reused_concrete_blocks"
projekt:
  - "ReCrete_footbridge_reused_concrete_blocks"
---

# Re:Crete footbridge — Fallstudie Direct Reuse

## Legacy Content

### Legacy Source: Gebäude\ReCrete_footbridge_reused_concrete_blocks.md

- Map action: split_into_case_graph
- Primary target: fallstudie/ReCrete_footbridge_reused_concrete_blocks
- Secondary targets: projekt/ReCrete_footbridge_reused_concrete_blocks; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Re:Crete footbridge — Fallstudie Direct Reuse

**Arbeitsregel:** Als Wiederverwendung gezählt werden nur wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Lose Möbel, Dekoration, reine DfD-Strategien ohne tatsächlichen Wiedereinbau sowie reiner Bestandserhalt werden nicht als Direct Reuse gewertet.

**Hinweis zur Quellenlage:** Nicht belegte Angaben sind als **unbekannt** markiert. Normnummern, Kosten, Mengen und CO₂-Werte werden nur genannt, wenn sie in den angegebenen Quellen belastbar auftauchen.

## 1. EINORDNUNG

- **Entscheidung:** ANHANG / Forschungsprototyp
- **Bewertung:** ★★☆☆☆
- **Begründung:** Technisch sehr starker Direct-Reuse-Prototyp: 25 aus Ortbeton-Kellerwänden gesägte Betonblöcke werden als tragende Segmente eines 10-m-Fußgängerbrückenbogens wiederverwendet. Wegen Infrastruktur-/Prototypcharakter und fehlendem Gebäudebezug nicht als Hauptgebäude-Fall.
- **Vertrauensgrad:** belegt
- **Warnung Bestandserhalt:** nein
- **Warnung Möbel/Dekoration:** nein
- **Projektstatus:** Prototyp / Forschungsdemonstrator

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
| --- | --- | --- | --- | --- | --- |
| Fallstudie | Re:Crete footbridge | untersuchte Prototyp-Fallstudie | S1, S2, S3 | belegt | Infrastruktur-/Forschungsprototyp, kein Gebäude |
| Bauteil | 25 Betonblöcke aus Ortbeton-Kellerwänden | Haupttragwerk des neuen Fußgängerbrückenbogens | S1, S2 | belegt | gesägt aus einem Gebäude unter Transformation |
| Material | Stahlbeton / Ortbeton | wiederverwendetes Material/Bauteil | S1 | belegt | nicht zu RC-Zuschlag recycelt |
| Tragwerkssystem | 10-m-spannender, nachgespannter segmentierter Bogen | neue tragende Konstruktion | S1, S2 | belegt | Spannweite 10 m, Stich 1,20 m, Breite 1,20 m |
| Verbindung | Nachspannung / post-tensioning | verbindet Betonsegmente zu tragfähigem Bogen | S1, S2 | belegt | Details der Anker/Kabel: teilweise unbekannt |
| Prüfung | Finite-Elemente-Modell, Lastversuch, nicht-destruktive Untersuchung | Validierung des Tragverhaltens | S1, S2, S5 | belegt | Lasttest und NDT ausdrücklich genannt |
| Kennwert | −71 % Global Warming Potential gegenüber Recyclingbeton-Alternative; −74 % gegenüber Stahl-Alternative; +9 % gegenüber Holz-Alternative | LCA-Ergebnis des Prototyps | S1 | belegt | Bilanzgrenze nach Studie; nicht verallgemeinern |
| Methode | Betonsägen, Heben, Transport, Reassemblage | Prozess zur Gewinnung und Nutzung von Ortbetonbauteilen | S1 | belegt | Donorgebäude nicht benannt |
| People | Julie Devènes, Jan Brütting, Célia Küpfer, Maléna Bastien-Masse, Corentin Fivet | Autor:innen / Projektteam im Forschungskontext | S1, S3 | belegt | genaue Rollen siehe Publikation |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
| --- | --- | --- | --- |
| Infrastruktur-Prototyp | Der Fall ist keine Gebäude-Fallstudie, zeigt aber tragende Direct-Reuse-Technik. | Fußgängerbrücke aus wiederverwendeten Betonblöcken | verknüpft Fallstudie, Projektstatus, Tragwerkssystem |
| Ortbeton-Bauteilernte | Reuse stammt nicht aus Fertigteilen, sondern aus gesägten Ortbetonwänden. | Blöcke aus Kellerwänden eines umzubauenden Gebäudes | verknüpft Abbruchmethode, Methode, Bauteil, Prüfung |

## 3. FALLSTUDIE

- **Name:** Re:Crete / Re:Crete footbridge
- **Ort:** Schweiz/EPFL-Kontext; genauer Montageort des Prototyps unbekannt
- **Gebäude:** kein Gebäude; Fußgängerbrücken-Prototyp
- **Projekt:** Reuse of concrete blocks from cast-in-place building to arch footbridge
- **Beteiligte People / Akteure:** Julie Devènes, Jan Brütting, Célia Küpfer, Maléna Bastien-Masse, Corentin Fivet; EPFL Structural Xploration Lab
- **Architekt:** unbekannt
- **Tragwerksplaner:** Forschungsteam EPFL/SXL; genaue professionelle Rollen unbekannt
- **Bauherr:** unbekannt; Forschungsförderung/Unterstützung u. a. EPFL ENAC Innovation Seed grant in Publikation genannt
- **Zeitraum:** 2022 publiziert; Bauzeitpunkt unbekannt
- **Ursprüngliche Nutzung:** Kellerwände eines Gebäudes unter Transformation
- **Neue Nutzung:** tragender Fußgängerbrückenbogen
- **Fläche / Maßstab:** 10 m Spannweite; 1,20 m Stich; 1,20 m Breite
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** sehr gut für Tragwerksprinzip, Menge, Prüfung und LCA; schwach für Donorgebäude, Kosten, Genehmigung und Langzeitnutzung

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** ex-situ / Bauteilwiederverwendung / struktureller Direct Reuse / Prototyp
- **Hauptniveau:** Tragwerk
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Kein Bestandserhalt. Die Betonblöcke werden nicht gebrochen und als Zuschlag recycelt, sondern als tragende Blöcke in einer neuen Konstruktion eingesetzt.
- **Warum ist der Fall relevant?** Er belegt eine seltene Methode der Wiederverwendung von Ortbetonbauteilen, inklusive Betonsägen, Nachspannung, FE-Modell, Lasttest und LCA.

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Betonblöcke / Bogensegmente | Stahlbeton/Ortbeton | Kellerwände eines Gebäudes unter größerer Transformation; genauer Standort unbekannt | Kellerwand / vertikales Trag- oder Abschlussbauteil | Segmente eines nachgespannten Bogen-Fußstegs | 25 Blöcke | ja | nein | nein | nein | Sägen aus Bestandswand, Vorbereitung, Montage | Nachspannung; Fugen/Details laut Studie | FE-Modell, Lastversuch, NDT | Drucktragfähigkeit, Bogenwirkung, Gebrauchstauglichkeit | unbekannt | Materialeigenschaften, Geometrievarianz, sichere Verbindung | S1, S2 | nein |
| Nachspannkabel / Verbindungssystem | Stahl; genaue Spezifikation unbekannt | neu oder wiederverwendet: unbekannt | nicht zutreffend/unbekannt | post-tensioning des Bogens | unbekannt | ja | nein | nein | nein | Einbau in Bogenkonstruktion | Nachspannung | Lastversuch der Gesamtstruktur | Vorspannkraft, Dauerhaftigkeit, Sicherung der Segmente | unbekannt | Nachweis der Verbindung mit variablen Altbetonblöcken | S1, S2 | teilweise |
| Widerlager / Auflager | unbekannt | unbekannt | unbekannt | Auflager des Brückenbogens | unbekannt | ja | nein | nein | nein | unbekannt | unbekannt | im Gesamtlasttest enthalten | Ableitung der Horizontalkräfte | unbekannt | Auflagergeometrie und Lastabtragung | S1 | ja |
| Geländer, Belag, Beleuchtung, TGA, Sanitär | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | nein | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine belastbare Quelle gefunden | ja |

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bestandsaufnahme | Betonwände eines umzubauenden Gebäudes als potenzieller Elementvorrat identifiziert | EPFL/SXL-Forschungsteam; genaue Donorakteure unbekannt | Sourcing von Ortbetonbauteilen | unbekannt | kein konventioneller Abbruch; selektives Ausschneiden | Sägen in Blöcke | Materialeigenschaften als Forschungsfrage | Ausschneiden, Heben, Transport | geeigneter Bestand in passender Menge/Geometrie | Prototyp auf verfügbaren Blöcken entwerfen | S1 |
| Bauteilinventar | 25 Blöcke für den Bogen definiert | Forschungsteam | Bauteilernte und Zuordnung im Entwurf | FE-Modell für Tragverhalten | Betonsägen | geometrische Vorbereitung | NDT, Lastversuch | unbekannt | Geometrische Varianz | segmentierter Bogen als toleranter Tragwerkstyp | S1, S2 |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | potenzielle Altbeton-/Bewehrungsrisiken | unbekannt | keine belastbare Quelle gefunden |
| Rückbau/Ausbau | Blöcke aus Ortbeton-Kellerwänden gesägt | Forschungsteam; Diamcoupe SA wird in Danksagung als Unterstützung für Prototypbau genannt | mobile Betonsägen / sawing | mobile sawing machines; genaue Geräte unbekannt | selektives Sägen | Schneiden statt Brechen | unbekannt | Heben/Transport zu Montageort | Zerstörungsarmes Gewinnen von Elementen | Sägen statt Recycling/Abbruch | S1 |
| Transport | Blöcke zum Prototyp-Montageort bewegt | unbekannt | Heben/Transport | unbekannt | nicht relevant | unbekannt | unbekannt | Transportdistanz unbekannt | Gewicht und Terminierung | unbekannt | S1 |
| Lagerung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Betonblocklagerung | unbekannt | keine belastbare Quelle gefunden |
| Aufbereitung | Geometrie/Segmente vorbereitet | Forschungsteam | Zuschnitt und Fugen-/Montageplanung | FE-Modell für Tragwerk | nicht relevant | Sägen, ggf. Bohren/Anpassen; Details unbekannt | NDT | unbekannt | Toleranzen und Bewehrungslage | Segmentbogen + Nachspannung | S1, S2 |
| Planung | Bogenform entworfen, um Druckfestigkeit von Altbeton zu nutzen | EPFL/SXL-Team | Bogen als druckdominantes System; FE-Modell | Finite-Elemente-Modell; Software unbekannt | unbekannt | unbekannt | Lasttest zur Validierung | unbekannt | Zuverlässigkeit wiederverwendeter Betonblöcke | Modell + Lastversuch | S1 |
| Genehmigung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Infrastrukturzulassung für Altbeton | unbekannt | keine belastbare Quelle gefunden |
| Wiedereinbau | 25 Blöcke als 10-m-Bogen montiert und nachgespannt | EPFL/SXL-Team; Unterstützer laut Danksagung | Segmentbogenmontage | unbekannt | nicht relevant | Nachspannung | Lasttest | Montageort unbekannt | Montagefolge und Vorspannung | post-tensioned segmented arch | S1, S2 |
| Monitoring | Tragverhalten und Umweltwirkung ausgewertet | Forschungsteam | Load testing, LCA | LCA-Methode/FE-Modell; Software unbekannt | unbekannt | unbekannt | Lastversuch, NDT | unbekannt | Vergleichbarkeit mit Alternativen | vergleichende LCA | S1 |

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Tragwerkssystem | nachgespannter segmentierter Bogen aus 25 Betonblöcken | Drucktragfähigkeit, Stabilität, Gebrauchstauglichkeit | unbekannt | FE-Modell, Lastversuch, NDT | Altbetonsegmente aus Ortbeton statt normierter Fertigteile | Bogenform nutzt Druckfestigkeit; Nachspannung hält Segmente zusammen | S1, S2 |
| Lastabtragung | Lastabtrag über Bogenkompression zu Auflagern; Horizontalkräfte am Widerlager | sichere Abtragung Fußgängerlasten im Prototyp | unbekannt | Load testing | Segmentfugen und Auflagerkräfte | post-tensioning + FE-Validierung | S1 |
| Verbindung | Nachspannung als Hauptverbindung; Fugen zwischen Blöcken | Vorspannkraft, Schub-/Druckübertragung, Dauerhaftigkeit | unbekannt | Lasttest der Gesamtstruktur | keine Standardverbindung für gesägte Altbetonblöcke | segmentierter nachgespannter Bogen | S1, S2 |
| Brandschutz | für Brückenprototyp nicht öffentlich behandelt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine belastbare Quelle gefunden |
| Schallschutz | nicht relevant / unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine belastbare Quelle gefunden |
| Feuchte/Wärmeschutz/Wärmebrücken/Luftdichtheit | für Fußbrückenprototyp nicht relevant bzw. unbekannt | Dauerhaftigkeit gegen Bewitterung wäre relevant, aber nicht öffentlich belegt | unbekannt | NDT; Langzeit-Monitoring unbekannt | Altbeton-Dauerhaftigkeit bei Exposition | unbekannt | S1 |
| TGA-Integration | nicht relevant | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine belastbare Quelle gefunden |
| Barrierefreiheit | unbekannt | Fußgängerbrücke/Prototyp; Anforderungen nicht belegt | unbekannt | unbekannt | unbekannt | unbekannt | keine belastbare Quelle gefunden |
| Dauerhaftigkeit/Wartung | Dauerhaftigkeit als Thema der Altbetonqualität relevant; Langzeitdaten unbekannt | unbekannt | unbekannt | NDT erwähnt | Zustand/Restlebensdauer der Blöcke | nicht-destruktive Untersuchung | S1, S2 |
| Zulassung/Haftung | nicht öffentlich belegt | unbekannt | unbekannt | Lasttest/FE-Modell als technische Plausibilisierung | fehlende Routine für wiederverwendeten Ortbeton | Proof-of-concept statt Regelanwendung | S1 |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
| --- | --- | --- | --- | --- | --- | --- |
| Anzahl Betonblöcke | 25 | Stück | Publikationsangabe | Bogenstruktur | S1, S2 | belegt |
| Spannweite | 10 | m | Publikationsangabe | Fußbrückenbogen | S1, S2 | belegt |
| Stich / rise | 1,20 | m | Publikationsangabe | Bogenstruktur | S1 | belegt |
| Breite | 1,20 | m | Publikationsangabe | Bogenstruktur | S1 | belegt |
| Öffnungswinkel | 26 | Grad | Publikationsangabe | Bogenstruktur | S1 | belegt |
| Global Warming Potential gegenüber Recyclingbeton-Alternative | −71 | % | vergleichende LCA | Studienbilanz des Brückenprototyps | S1 | belegt |
| Global Warming Potential gegenüber Stahl-Alternative | −74 | % | vergleichende LCA | Studienbilanz des Brückenprototyps | S1 | belegt |
| Global Warming Potential gegenüber Holz-Alternative | +9 | % | vergleichende LCA | Studienbilanz des Brückenprototyps | S1 | belegt |
| Kosten | unbekannt | CHF/EUR | unbekannt | unbekannt | keine belastbare Quelle gefunden | unbekannt |

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie: technisch/rechtlich/wirtschaftlich/logistisch/gestalterisch/sozial | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Geeignete Ortbetonbauteile finden | logistisch/technisch | Bestand muss passende Abmessungen und Qualität liefern | Entwurf abhängig vom verfügbaren Bestand | Bauteil, Material, Logistik | Sourcing vor Detailentwurf | Entwurf folgt Bauteilernte | S1 |
| Mechanische Eigenschaften unbekannt | technisch | Altbeton aus bestehendem Gebäude, nicht neues Produkt | Unsicherheit bei Tragfähigkeit | Prüfung, Tragwerkssystem | FE-Modell, NDT, Lasttest | Prüfung ist integraler Teil des Reuse-Prozesses | S1, S2 |
| Geometrische Varianz der gesägten Blöcke | technisch/gestalterisch | Ausschneiden aus vorhandenen Wänden | Fugen/Passgenauigkeit anspruchsvoll | Bauteil, Verbindung | segmentierter Bogen mit Nachspannung | Tragwerkstypen wählen, die Varianz tolerieren | S1 |
| Zulassung und Haftung | rechtlich | keine etablierte Normkette für wiederverwendeten Ortbeton | Prototyp statt Regelbau | Recht, Norm, Prüfung | Proof-of-concept und belastbare Tests | Vorzeigeprojekte brauchen Prüf- und Genehmigungsstrategie | S1 |
| Logistik schwerer Betonsegmente | logistisch | schwere Blöcke, Transport, Montagefolge | Planungsaufwand; Kosten unbekannt | Logistik, Wirtschaft, Bauteil | unbekannt | Transportdistanz und Kraneinsatz müssen früh bewertet werden | S1 |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** Forschungsbasiertes Sourcing von Betonblöcken aus einem Transformationsgebäude; kommerzielles Modell unbekannt.
- **Bauteilbörse / Quelle:** keine Bauteilbörse belegt.
- **Kostenwirkung:** unbekannt.
- **Zeitwirkung:** unbekannt.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt; im Prototyp über Tests plausibilisiert, aber kein Regelmodell belegt.
- **Arbeitsaufwand:** hoch für Sägen, Heben, Transport, Nachspannung und Tests; quantitative Arbeitsdaten unbekannt.
- **Lagerung:** unbekannt.
- **Marktbarrieren:** fehlende Routine für Ortbeton-Elementernte, Prüf-/Zulassungsfragen, schwere Logistik.

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** hoch; Blockfugen und Materialherkunft sind Teil des Forschungsnarrativs.
- **räumliche Transformation:** Kellerwand wird Brückenbogen.
- **Atmosphäre / Ausdruck:** technische Demonstration von Massivität, Segmentierung und Nachspannung.
- **Umgang mit Spuren:** Textur/Blockcharakter des Altbetons sichtbar; Details unbekannt.
- **sozialer Wert:** Wissens- und Machbarkeitsnachweis für kreislauffähige Tragwerke.
- **Denkmal- oder Bestandswert:** unbekannt.
- **Kritik / Grenzen:** nicht Gebäude, nicht kommerzieller Regelbau, nicht als dauerhaft öffentlicher Brückenbetrieb belegt.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** Norm, Recht, Kosten, Bauherr, Genehmigung, Transportdistanz, Donorgebäude, Langzeitmonitoring.
- **Sinnvolle neue Entitäten:** Infrastruktur-Prototyp; Ortbeton-Bauteilernte.
- **Fehlende Daten:** Bewehrungsdaten, konkrete NDT-Protokolle, Verbindungsdetails, Auflagerdetails, Kosten, Transport.
- **Zu prüfende Quellen:** Volltext der Structures-Publikation, supplementary data, EPFL/SXL-Projektarchiv.

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** Anhang
- **5 wichtigste Fakten:**
  1. 25 Betonblöcke aus Ortbeton-Kellerwänden.
  2. 10 m langer nachgespannter segmentierter Bogen.
  3. FE-Modell und Lasttest validieren Tragverhalten.
  4. LCA zeigt −71 % GWP gegenüber Recyclingbeton-Alternative.
  5. Kein Gebäude, sondern Infrastruktur-Prototyp.
- **5 wichtigste Bauteile:**
  1. Betonblöcke.
  2. Nachspannkabel.
  3. Fugen zwischen Segmenten.
  4. Auflager/Widerlager.
  5. Bewehrung im Altbeton: Lage/Umfang unbekannt.
- **5 wichtigste Hürden:**
  1. Ortbeton zerstörungsarm gewinnen.
  2. Materialeigenschaften nachweisen.
  3. Geometrische Varianz beherrschen.
  4. Zulassung/Haftung.
  5. Schwerlastlogistik.
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Ortbeton kann strukturell wiederverwendet werden.
  2. Druckdominante Tragwerke passen gut zu Beton-Reuse.
  3. Nachspannung kann heterogene Segmente aktivieren.
  4. Prüf- und Modellierungsstrategie ist unverzichtbar.
  5. LCA muss konkrete Alternativen vergleichen.
- **5 offene Fragen:**
  1. Wo stand das Donorgebäude?
  2. Welche Kosten entstanden?
  3. Welche Norm-/Genehmigungslogik wurde angewandt?
  4. Wie dauerhaft ist die Konstruktion im Außenraum?
  5. Kann das Verfahren auf echte Gebäude- oder Brückenprojekte skaliert werden?

## Quellen und Links

- **S1**: Structures / ScienceDirect: Re:Crete – Reuse of concrete blocks from cast-in-place building to arch footbridge — https://www.sciencedirect.com/science/article/pii/S2352012422005720
- **S2**: Structurae: Re:crete – a Footbridge Made of Reused Concrete Blocks — https://structurae.net/en/literature/conference-paper/re-crete-a-footbridge-made-of-reused-concrete-blocks
- **S3**: EPFL Graph Search: Re:Crete – reuse of concrete elements in new structures — https://graphsearch.epfl.ch/en/publication/2539acac-140d-4914-8306-c1f540294152
- **S4**: UPM SciMarina publication record — https://upm.scimarina.org/en/ipublic/item/10424106
- **S5**: ResearchGate record / full-text mirror — https://www.researchgate.net/publication/362652352_ReCrete_-_Reuse_of_concrete_blocks_from_cast-in-place_building_to_arch_footbridge
