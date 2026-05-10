---
id: "Jeugdkliniek_Ithaka_Emergis_Kloetinge"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "Jeugdkliniek Ithaka / Emergis, Kloetinge"
bauobjekt:
  - "Jeugdkliniek_Ithaka_Emergis_Kloetinge"
legacy_paths:
  - "Gebäude\\Jeugdkliniek_Ithaka_Emergis_Kloetinge.md"
projekt:
  - "Jeugdkliniek_Ithaka_Emergis_Kloetinge"
reuse_chain_detected: "True"
---
# Jeugdkliniek Ithaka / Emergis, Kloetinge

## Migration

- Fallstudie ID: Jeugdkliniek_Ithaka_Emergis_Kloetinge
- Legacy source count: 1
- Generated project: Jeugdkliniek_Ithaka_Emergis_Kloetinge
- Generated bauobjekt: Jeugdkliniek_Ithaka_Emergis_Kloetinge
- Extracted reuse_einsatz rows: 14
- Extracted datenpunkt rows: 10
- Extracted entity mapping rows: 19
- Reuse chain detected: True

## Legacy Content

### Legacy Source: Gebäude\Jeugdkliniek_Ithaka_Emergis_Kloetinge.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Jeugdkliniek_Ithaka_Emergis_Kloetinge
- Secondary targets: projekt/Jeugdkliniek_Ithaka_Emergis_Kloetinge; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Jeugdkliniek Ithaka / Emergis, Kloetinge

## 1. EINORDNUNG
- **Entscheidung:** HAUPTFALL mit Vorbehalt / starker VERGLEICHSFALL
- **Bewertung:** ★★★★☆
- **Begründung:** Die Kinder- und Jugendpsychiatrie-Klinik Ithaka verwendet umfangreich feste Bauteile aus dem ehemaligen Rijkswaterstaat-Districtskantoor in Terneuzen: Außenfenster/-rahmen, Innentüren, Fassadenbekleidung, Holzfußböden, Straßenklinker, Holzträger/-balken, HSB-Innenblätter, Vordächer/Sonnenschutz und teils Installationen. Die Holztragwerk-/Balkenrolle ist belegt, aber Mengen und vollständige statische Nachweise sind öffentlich nicht detailliert.
- **Vertrauensgrad:** teilweise belegt
- **Warnung Bestandserhalt:** ja
- **Warnung Möbel/Dekoration:** nein
- **Projektstatus:** gebaut / eröffnet 2019

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Kinder- en jeugdkliniek Ithaka / Emergis | Empfängergebäude für Bauteile aus RWS-Terneuzen | [S1], [S2], [S3] | belegt | erste zirkuläre GGZ-Klinik laut Quellen |
| Gebäude | ehemaliges Districtskantoor Rijkswaterstaat Terneuzen | Donorgebäude | [S1], [S2], [S4] | belegt | 2000 fertiggestellt, wegen Nieuwe Sluis abgebrochen |
| Gebäude | bestehender Emergis-Bestand Kloetinge | teilweise erhalten/renoviert | [S5] | belegt | Bestandserhalt nicht als Direct Reuse zählen |
| Ort | Kloetinge, Zeeland, Niederlande | Projektstandort | [S1], [S3], [S6] | belegt | Oostmolenweg 79/83 nach Emergis |
| People | Rothuizen Architecten / Taco Tuinhof | Architekt | [S2], [S5], [S7] | belegt | Entwurf aus verfügbaren Materialien |
| People | Burobas | Innenarchitektur / feste Einrichtung | [S1], [S8] | belegt | Möbel nur zählen, wenn feste Einrichtung |
| People | ABT + Adviesbureau Lüning | Holz-/Tragwerksberatung | [S4] | belegt | Holzstruktur spielt wichtige Rolle |
| Bauherr | Emergis | Auftraggeber / Betreiber | [S2], [S3], [S6] | belegt | Klinik für Kinder- und Jugendpsychiatrie |
| Bauteil | Außenkozijnen / Fensterrahmen | Hülle | [S2], [S9], [S10] | belegt | in ganzer Einheit mit Stahlrahmen/Sonnenschutz wiederverwendet |
| Bauteil | HSB-binnenbladen | wiederverwendete Holzständer-/Innenblätter der Fassade | [S4] | teilweise belegt | genaue Rolle/Menge unbekannt |
| Bauteil | Holzträger / houten balken | tragende oder konstruktive Holzbauteile | [S4], [S5], [S8] | teilweise belegt | „timber structure plays important role“; Detailnachweis begrenzt |
| Bauteil | Azobé-hardwood shingles | Fassadenbekleidung, drittes Leben | [S4], [S8] | belegt | ursprünglich Meerpfähle, dann RWS-Fassade, dann Klinik |
| Bauteil | Innentüren / Hang- und Schließwerk | fester Innenausbau | [S2], [S5], [S11] | belegt | Mengen unbekannt |
| Bauteil | Holzfußböden | fester Innenausbau | [S2], [S5], [S11] | belegt | Mengen unbekannt |
| Bauteil | Straßenklinker | befestigte Außenflächen | [S2], [S5], [S11] | belegt | fixed construction layer |
| Bauteil | Armaturen / Beleuchtung / Installationen | technische Wiederverwendung möglich | [S11], [S12] | teilweise belegt | exakte installierte Menge unbekannt |
| Methode | Materialenpaspoort | Dokumentation der eingesetzten Materialien | [S5] | belegt | wichtig für spätere Wiederverwendung |
| Förderprogramm | Provinz Zeeland / Rabobank Groenprojecten | Entwicklungs-/Finanzierungsunterstützung | [S13] | teilweise belegt | genaue Summen unbekannt |
| Wirtschaft | Circulair bouwen nicht unbedingt billiger | Kostenwirkung | [S5] | belegt | konkrete Kosten unbekannt |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Donorgebäude | Das Projekt hängt stark von einem konkreten Spendergebäude ab. | RWS-Districtskantoor Terneuzen. | Gebäude, Bauteil, Logistik |
| Materialpass | Eigene Dokumentationsform für zukünftige Reuse-Fähigkeit. | Emergis-Materialenpaspoort. | Dokument, Datenmodell, Methode |
| Mehrfachleben | Einige Bauteile haben schon drittes Leben. | Azobé-Shingles: Meerpfahl → RWS → Klinik. | Bauteil, Material, kultureller Wert |

## 3. FALLSTUDIE
- **Name:** Kinder- en jeugdkliniek Ithaka / Emergis Kloetinge
- **Ort:** Kloetinge, Zeeland, Niederlande
- **Gebäude:** teils Neubau, teils Renovierung einer Kinder- und Jugendpsychiatrie-Klinik
- **Projekt:** zirkulär gebaute/umgebaute Klinik mit Donorbauteilen aus dem Rijkswaterstaat-Districtskantoor Terneuzen
- **Beteiligte People / Akteure:** Emergis, Rothuizen Architecten, Taco Tuinhof, Burobas, ABT, Adviesbureau Lüning, Paree, DWT Groep, LuxImprove, Rijkswaterstaat, Impuls Zeeland, Rabobank, Provinz Zeeland
- **Architekt:** Rothuizen Architecten / Taco Tuinhof
- **Tragwerksplaner:** ABT zusammen mit Adviesbureau Lüning für Holzstruktur nach Quelle; weitere unbekannt
- **Bauherr:** Emergis
- **Zeitraum:** Planung/Bau 2017–2019; Eröffnung/Inbetriebnahme 2019
- **Ursprüngliche Nutzung:** Donor: Rijkswaterstaat-Districtskantoor in Terneuzen; Empfängerbestand: bestehende Klinik/GGZ-Gebäude
- **Neue Nutzung:** Kinder- und Jugendpsychiatrie / GGZ-Klinik, 24–28 flexible Betten laut Emergis
- **Fläche / Maßstab:** ca. 1.400 m² Bestand erhalten + ca. 2.000 m² Neubau laut Duurzaamdoor; weitere Flächen unbekannt
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** gute Projektquellen für Bauteilarten; unvollständig für Mengen, Prüfungen, Normen und Kosten

## 4. REUSE-STRATEGIE
- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; in-situ Bestandserhalt/renovatie; Materialwiederverwendung; adaptive reuse des Klinikbestands
- **Hauptniveau:** Gebäudehülle / räumlicher Innenausbau / teilweise Tragwerk / Außenraum / technische Gebäudeausrüstung
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die 70% erhaltenen Bestandsflächen in Kloetinge zählen nicht als Direct Reuse. Gezählt werden nur die aus Terneuzen oder anderen Gebäuden ausgebauten und neu eingebauten festen Bauteile. Granulat aus abgebrochenen Wänden zählt als Recycling, nicht Direct Reuse.
- **Warum ist der Fall relevant?** Real gebauter Healthcare-Fall mit Donorgebäude, materialgetriebenem Entwurf, Mehrfachleben von Holzbauteilen und Materialpass.

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Holzträger / houten balken | Holz | RWS-Districtskantoor Terneuzen | Trag-/Konstruktionsbauteile | Holzstruktur / sichtbare Konstruktion | unbekannt | ja, teilweise belegt | ja | nein | nein | Enden ursprünglich zum Kürzen diskutiert; „Narben“ sichtbar belassen | vorhandene Verbindungsspuren; neue Verbindung unbekannt | unbekannt | Tragfähigkeit, Brandschutz | unbekannt | Löcher/alte Verbindungsmittel | [S4], [S5], [S8] | teilweise |
| Außenkozijnen / Fensterrahmen | Kiefernholz, Stahlrahmen, Isolierglas | RWS Terneuzen | Außenfenster/Fassade | Außenfenster/Fassade Klinik | unbekannt | nein | ja | ja | nein | Farbe erneuert wegen Blasen; Einheit beibehalten | inkl. Stahlrahmen und horizontaler Stahlsonnenschutz | Zustand „prima“; Glas beibehalten | U-Wert, Dichtheit, Sicherheit | unbekannt | Entwurf an verfügbare Maße angepasst | [S9], [S10] | teilweise |
| HSB-binnenbladen | Holzständerbau / Holz | RWS Terneuzen | Fassadeninnenblätter | Fassadenaufbau Klinik | unbekannt | möglich/unklar | ja | ja | nein | Demontage und Wiedereinbau | unbekannt | unbekannt | Wärme, Feuchte, Brand | unbekannt | Passung/Qualität | [S4] | ja |
| Vordächer / luifels | Stahl/Holz unbekannt | RWS Terneuzen | Vordach/Sonnenschutz | Vordach/Sonnenschutz Klinik | unbekannt | nein | ja | ja | nein | Demontage, Montage | unbekannt | unbekannt | Windlast, Dauerhaftigkeit | unbekannt | unbekannt | [S4] | ja |
| horizontale Stahlroste / Sonnenschutz | Stahl | RWS Terneuzen | Sonnenschutz über Fenstern | Sonnenschutz Klinik | unbekannt | nein | nein | ja | nein | Wiederverwendung mit Fenstereinheit | unbekannt | unbekannt | Korrosion, Windlast | unbekannt | Lack/Korrosion unbekannt | [S9] | teilweise |
| Azobé-Shingles | Hartholz Azobé | RWS-Fassade; davor Meerpfähle | Fassadenbekleidung / davor Wasserbau | Fassadenbekleidung Klinik | unbekannt | nein | nein | ja | nein | Ausbau, Wiederbefestigung | unbekannt | unbekannt | Witterung, Brandschutz | unbekannt | Restlebensdauer | [S4], [S8] | teilweise |
| Innentüren | Holz/Metall unbekannt | RWS Terneuzen | Innentüren | Innentüren Klinik | unbekannt | nein | ja | nein | nein | Demontage, Anpassung | Beschläge teils mitverwendet | unbekannt | Brand-/Schallschutz, Hygiene | unbekannt | Gesundheitsbau-Anforderungen | [S2], [S5], [S11] | ja |
| Hang- und Schließwerk | Metall | RWS Terneuzen | Türbeschläge | Türbeschläge Klinik | unbekannt | nein | ja | nein | technisch: ja | Wiederverwendung | Schraub-/Beschlagverbindung | unbekannt | Funktion, Sicherheit | unbekannt | Kompatibilität | [S11] | ja |
| Holzfußböden / vloerdelen | Holz | RWS Terneuzen | Bodenbelag | Bodenbelag Klinik | unbekannt | nein | ja | nein | nein | Ausbau, ggf. Aufbereitung | unbekannt | unbekannt | Abrieb, Hygiene, Brand | unbekannt | Healthcare-Nutzung | [S2], [S5], [S11] | ja |
| Straßenklinker | gebrannter Stein/Beton unbekannt | RWS Terneuzen | Außenpflaster | Außenpflaster Klinik | unbekannt | nein | ja | nein | nein | Ausbau, Reinigung, Neuverlegung | Sandbett/Mörtel unbekannt | unbekannt | Rutschfestigkeit, Frost | unbekannt | Reinigung/Sortierung | [S2], [S5], [S11] | ja |
| Fassadenbekleidung allgemein | Holz / unbekannt | RWS Terneuzen | Fassade | Fassade Klinik | unbekannt | nein | nein | ja | nein | Wiederverwendung | unbekannt | unbekannt | Witterung, Brand | unbekannt | unbekannt | [S2], [S3] | teilweise |
| Beleuchtungsarmaturen | unbekannt | RWS / andere Quellen | Beleuchtung | Innenbeleuchtung | 30–40% Donorgebäude möglich; genaue Menge unbekannt | nein | ja | nein | technisch: ja | prüfen, ggf. anpassen | Elektroanschluss | Elektroprüfung unbekannt | Sicherheit, Effizienz | NEN unbekannt | alte Technik vs. Energieziel | [S11], [S13] | ja |
| Elektroinstallationen / Rohre | unbekannt | andere Sloop-Panden / Bestand | Elektro | Elektro/Kommunikation/Sicherheit | unbekannt | nein | nein | nein | technisch: ja | Wiederverwendung/Neumontage unbekannt | unbekannt | Elektroprüfung | Sicherheit, Brandschutz | unbekannt | Energieziel vs. Reuse | [S12], [S13] | ja |
| Sanitär, TGA, feste Einbauten | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | nein | ja | nein | technisch: ja | unbekannt | unbekannt | unbekannt | Hygiene/Healthcare | unbekannt | nicht belegt | unbekannt | ja |

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Donorgebäude mit Logbuch/Bestekken durchgehen und Bauteile auswählen | Emergis, Rothuizen, Rijkswaterstaat | materialgetriebenes Design | Logbuch/Bestekken | vor Rückbau | Auswahl verwertbarer Bauteile | Sicht-/Zustandsprüfung | Terneuzen → Kloetinge | Material bestimmt Entwurf | Entwurf nach verfügbaren Bauteilen | [S5], [S13] |
| Bauteilinventar | Materialien dokumentieren | Emergis, Projektteam | Materialenpaspoort | Materialpass mit Fotos | unbekannt | Katalogisierung | Wert/Lebensdauer abschätzen | unbekannt | Datenaufwand | Materialpass | [S5], [S14] |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine öffentlichen Daten | unbekannt | unbekannt |
| Rückbau | RWS-Gebäude nicht klassisch gesloopt, sondern ontmanteld | Rijkswaterstaat / Rückbauakteure | selektive Demontage | unbekannt | Ontmanteling | Sortierung | Zustand prüfen | Bauteile aus Terneuzen | Zeitfenster durch Neue Sluis | Donorgebäude parallel nutzbar | [S11], [S13] |
| Ausbau | Fenster, Türen, Balken, Shingles, Böden, Klinker ausbauen | Rückbauakteure | Bauteilernte | unbekannt | selektiv | schonender Ausbau | Sichtprüfung | Zwischenlager unbekannt | Schäden | Demontage statt Abbruch | [S2], [S4], [S5] |
| Transport | Bauteile nach Kloetinge transportieren | unbekannt | lokale/regionale Logistik | unbekannt | entfällt | Verpackung unbekannt | unbekannt | Terneuzen–Kloetinge | Distanz über Schelde / Timing | unbekannt | [S13] |
| Lagerung | unbekannt | unbekannt | unbekannt | unbekannt | entfällt | Schutz vor Wetter | unbekannt | Lagerfläche unbekannt | Feuchte/Verzug | unbekannt | unbekannt |
| Aufbereitung | Fensterfarbe ersetzen; Holzspuren belassen; reinigen/anpassen | Architekt, Ausführende | minimal reparieren / Spuren zeigen | unbekannt | entfällt | Schleifen, streichen, ggf. zuschneiden | Zustand prüfen | Werkstatt/Baustelle | Restzustand, Maße | Entwurf an Bauteile | [S4], [S9] |
| Planung | Design hängt von verfügbaren Materialien ab | Rothuizen/Taco Tuinhof | „koken met restjes“ / Design from availability | Materialpass/Logbuch | entfällt | unbekannt | unbekannt | Koordination | mehr Organisation nötig | früh Partner einbinden | [S5], [S7] |
| Genehmigung | Healthcare-Neubau/Renovierung | Emergis, Behörden | unbekannt | unbekannt | entfällt | unbekannt | unbekannt | unbekannt | Hygiene/Brandschutz/Energie | unbekannt | unbekannt |
| Wiedereinbau | Bauteile in Neubau/Renovierung integrieren | Bauunternehmen unbekannt, Paree, DWT, Burobas | Wiederverwendung | unbekannt | entfällt | Anpassung | unbekannt | Baustellenkoordination | Kompatibilität mit Energieziel | flexible Details | [S1], [S2], [S12] |
| Monitoring | Energie-/Nutzungsziele | Emergis | unbekannt | unbekannt | entfällt | entfällt | Energieneutralität/Label A genannt | unbekannt | Reuse vs. Energieambition | Gaslos/energieneutraler Neubau | [S3], [S6] |

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Holzstruktur mit wiederverwendeten Holzbauteilen spielt Rolle; genaue Statik unbekannt | Tragfähigkeit, Brandschutz | niederländisches Baurecht/NEN unbekannt | unbekannt | alte Löcher/Verbindungen | Spuren sichtbar belassen, Details angepasst | [S4] |
| Lastabtragung | Neubau + renovierter Bestand | Standsicherheit | unbekannt | unbekannt | Kombination Bestand/Reuse/Neubau | ABT/Lüning-Beratung | [S4], [S5] |
| Verbindung | alte Verbindungslöcher in Holz sichtbar | neue Anschlüsse sicher ausführen | unbekannt | unbekannt | vorhandene Bohrungen | ursprünglich Kürzen erwogen, dann sichtbar belassen | [S4] |
| Brandschutz | Klinik, Türen, Holz, Fassade | Brandabschnitte/Fluchtwege | unbekannt | unbekannt | gebrauchte Türen/Holz | unbekannt | unbekannt |
| Schallschutz | Kliniknutzung mit Patientenzimmern | Privatsphäre/Komfort | unbekannt | unbekannt | wiederverwendete Türen/Böden | unbekannt | unbekannt |
| Feuchte | Außenhülle mit Reuse-Holz | Witterungsschutz | unbekannt | unbekannt | Restlebensdauer Azobé/Fenster | Farbe erneuert, harte Holzart | [S4], [S9] |
| Wärmeschutz | energieneutraler Neubau, Renovierung Label A | Energiebedarf | unbekannt | Energielabel A genannt | alte Fenster/Gläser vs. Energieziel | vorhandenes Isolierglas beibehalten, Energieplanung | [S3], [S6], [S9] |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | vorhandene Fensterrahmen | unbekannt | unbekannt |
| Luftdichtheit | unbekannt | Hülle kliniktauglich | unbekannt | unbekannt | alte Fenster | Farbe/Überarbeitung | [S9] |
| TGA-Integration | Paree: Elektro/Kommunikation/Sicherheit; DWT: W-Installationen | Healthcare, Sicherheit, Energie | unbekannt | Elektro-/Installationsprüfung unbekannt | Reuse vs. moderne Technik | Installationsteams | [S12], [S15] |
| Barrierefreiheit | unbekannt | Klinikzugänglichkeit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Dauerhaftigkeit | RWS-Bauteile von 2000, Azobé teils drittes Leben | Restlebensdauer | unbekannt | Sichtprüfung | Alter, Gebrauchsspuren | Materialauswahl + Materialpass | [S4], [S5] |
| Wartung | Holzfassade/Fenster | Instandhaltung | unbekannt | unbekannt | gebrauchte Oberfläche | Pflege/Anstrich | [S9] |
| Zulassung | gebrauchte Bauteile in Healthcare | öffentlich nicht erläutert | unbekannt | unbekannt | rechtliche Unsicherheit | Anwalt/Partner für neue Verträge laut RVO/Skipr | [S13] |
| Haftung | Produkt-as-a-service für feste Bestandteile rechtlich schwierig | Eigentum/Gewährleistung | niederländisches Recht unbekannt | unbekannt | attached-to-land-Komponenten | unbekannt | [S14] |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| erhaltener Bestand | ca. 70% / 1.400 | % / m² | Projektbericht | Bestand Kloetinge; zählt nicht Direct Reuse | [S5] | teilweise belegt |
| Neubau | ca. 2.000 | m² | Projektbericht | neues Klinikteil | [S5] | teilweise belegt |
| Materialanteil aus RWS | 30–40 | % | Emergis/Medienangabe | Materialien/Grundstoffe aus Donorgebäude | [S6], [S11] | teilweise belegt |
| Ziel Reuse-Anteil Neubau | 50 | % | Planungsziel | neues Gebäude | [S13] | teilweise belegt |
| Betten | 24–28 | Anzahl | Emergis | Klinik | [S6] | belegt |
| Eröffnung / Nutzung | 2019 | Jahr | Emergis/Skipr | Projekt | [S3], [S6] | belegt |
| CO₂-Einsparung | unbekannt | t CO₂e | unbekannt | unbekannt | unbekannt | unbekannt |
| Kosten | unbekannt | EUR | unbekannt | unbekannt | unbekannt | unbekannt |
| Energie | Neubau energieneutral; Renovation Energielabel A | qualitativ | Projektangabe | Betrieb, nicht Direct Reuse | [S3], [S6] | teilweise belegt |
| Materialpass | vorhanden | ja/nein | Materialenpaspoort mit Fotos | Dokumentation für zukünftige Reuse | [S5], [S14] | belegt |

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie: technisch/rechtlich/wirtschaftlich/logistisch/gestalterisch/sozial | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Entwurf hängt von verfügbaren Bauteilen ab | gestalterisch/logistisch | Donormaterial bestimmt Raster/Maße | mehr Kreativität/Organisation | Methode, Bauteil | „koken met restjes“, Materialpass | Reuse früh als Entwurfsgrundlage setzen | [S5], [S7] |
| Energieziel vs. Reuse alter Komponenten | technisch | alte Fenster/Installationen vs. energieneutral | Zielkonflikte | Hülle, TGA | Energieplanung, Neubau gaslos | Reuse und Energie gemeinsam optimieren | [S3], [S15] |
| Gebrauchte Fensteroberflächen | technisch | Farbe mit Blasen | Aufarbeitung nötig | Fenster | Farbe ersetzen, Glas beibehalten | Reparatur statt Austausch | [S9] |
| Alte Verbindungslöcher in Holz | technisch/gestalterisch | Verbindungsmittel aus vorheriger Nutzung | Trag-/Ästhetikfrage | Holzträger | Spuren sichtbar belassen | Gebrauchsspuren können Wert schaffen | [S4] |
| Rechtliche Eigentums-/Servicefragen | rechtlich/wirtschaftlich | feste Bauteile sind mit Grundstück verbunden | Product-as-service erschwert | Recht, Wirtschaft | unbekannt | Recht früh klären | [S14] |
| Circulair bouwen nicht billiger | wirtschaftlich | zusätzlicher Koordinationsaufwand | Kosten können steigen | Wirtschaft | Förder-/Finanzierungspartner | Reuse nicht nur als Sparmodell planen | [S5], [S13] |

## 10. WIRTSCHAFT UND BESCHAFFUNG
- **Beschaffungsmodell:** Donorgebäude Rijkswaterstaat Terneuzen; zusätzliche Materialien aus anderen Sloop-Panden und bestehendem Emergis-Gebäude.
- **Bauteilbörse / Quelle:** keine öffentliche Bauteilbörse; direkte Donorbeziehung mit Rijkswaterstaat.
- **Kostenwirkung:** konkrete Kosten unbekannt; Quelle betont, zirkuläres Bauen sei nicht zwingend billiger.
- **Zeitwirkung:** hoher Planungs- und Organisationsaufwand; genaue Bauzeitwirkung unbekannt.
- **Versicherung / Haftung:** unbekannt; rechtliche Beratung zu neuen Verträgen erwähnt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** hoch durch Ausbau, Materialpass, Designanpassung, Aufarbeitung.
- **Lagerung:** unbekannt.
- **Marktbarrieren:** fehlende Routine, Produkt-as-service-Rechtsfragen, Energie-/Hygieneanforderungen im Gesundheitsbau.

## 11. GESTALTUNG UND KULTURELLER WERT
- **Sichtbarkeit der Wiederverwendung:** hoch; Holzspuren/Löcher und Azobé-Shingles bleiben sichtbar.
- **räumliche Transformation:** Kombination aus renoviertem Bestand und Neubau; „healing environment“ statt klinischer Atmosphäre.
- **Atmosphäre / Ausdruck:** warme, häusliche Räume durch Holz und wiederverwendete Materialien.
- **Umgang mit Spuren:** bewusstes Zeigen von „Narben“ im Holz; drittes Leben der Shingles wird erzählt.
- **sozialer Wert:** Klinik für Kinder/Jugendliche; Zusammenarbeit mit sozialer Werkstatt bei fester Einrichtung laut Burobas.
- **Denkmal- oder Bestandswert:** RWS-Gebäude war frühes nachhaltiges Büro, aber wegen Nieuwe Sluis abgebrochen; Denkmalstatus unbekannt.
- **Kritik / Grenzen:** 70% Bestandserhalt nicht als Direct Reuse zählen; genaue Mengen, Prüfungen und CO₂-Daten fehlen.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN
- **Nicht gefunden:** vollständige Bauteilliste mit Mengen; statische Berechnung der Holzreuse; Norm-/Prüfdetails; Kosten; Transportdistanz; Lagerung.
- **Sinnvolle neue Entitäten:** Donorgebäude, Materialpass, Mehrfachleben, Healthcare-Anforderung.
- **Fehlende Daten:** Anteil der Bauteile, die direkt wiederverwendet wurden vs. recycelt; genaue Bauteilprüfungen; Rückbauvertrag.
- **Zu prüfende Quellen:** Lernbundel zum Projekt, Materialenpaspoort, ABT/Lüning-Unterlagen, Rothuizen-Ausführungsplanung, Emergis-Bauakten.

## 13. ABSCHLUSS
- **Soll der Fall in die Hauptliste?** ja, mit Vorbehalt; als starker Healthcare-/Donorgebäude-Fall, nicht als gesicherter ★★★★★-Tragwerksfall.
- **5 wichtigste Fakten:**
  1. Die Klinik wurde 2019 in Kloetinge in Betrieb genommen/eröffnet.
  2. Große Teile stammen aus dem RWS-Districtskantoor Terneuzen.
  3. Außenfenster, Türen, Fassadenbekleidung, Holzfußböden, Klinker und Holzbauteile wurden wiederverwendet.
  4. Etwa 70% / 1.400 m² des vorhandenen Emergis-Gebäudes blieben erhalten; ca. 2.000 m² Neubau kamen hinzu.
  5. Ein Materialpass dokumentiert die verwendeten Materialien für zukünftige Wiederverwendung.
- **5 wichtigste Bauteile:** Holzträger/-balken; Außenfenster/-rahmen mit Stahlsonnenschutz; Azobé-Shingles; Innentüren/Beschläge; Holzfußböden/Straßenklinker.
- **5 wichtigste Hürden:** Materialbestimmter Entwurf; Energieziel vs. alte Bauteile; rechtliche/vertragliche Unsicherheit; Aufarbeitung Fenster/Holz; Daten-/Mengenlücken.
- **5 wichtigste übertragbare Erkenntnisse:** Donorgebäude früh sichern; Bauteile als Entwurfsparameter nutzen; Materialpass erstellen; Spuren als Qualität nutzen; Bestandserhalt getrennt bewerten.
- **5 offene Fragen:** Welche Mengen jeder Bauteilkategorie wurden eingebaut? Welche Holzbauteile sind wirklich tragend? Welche Prüfungen wurden durchgeführt? Welche Kosten-/CO₂-Wirkung entstand? Wie wurden Gewährleistung und Haftung geregelt?

## Quellen und Links
- [S1] Burobas: Kinder- en jeugdkliniek mooiste gebouw van Zeeland — https://www.burobas.nl/nieuws/kinder-en-jeugdkliniek-van-emergis-volgens-jury-mooiste-gebouw-van-zeeland/
- [S2] INNAX: Emergis opent eerste circulaire zorgkliniek van Nederland — https://www.innax.nl/kennisbank/toekomstvast-bouwen/emergis
- [S3] Skipr: Circulair herbouwde kliniek Emergis geopend — https://www.skipr.nl/nieuws/circulair-herbouwde-kliniek-emergis-geopend/
- [S4] Adviesbureau Lüning/Galleo: Zorgkliniek Emergis te Kloetinge — https://galleo.co/project/zorgkliniek-emergis-te-kloetinge
- [S5] Duurzaamdoor: Circulair gebouw voor kinder- en jeugdkliniek Emergis — https://www.duurzaamdoor.nl/circulair-gebouw-voor-kinder-en-jeugdkliniek-emergis
- [S6] Emergis Kind & Jeugd: Nieuwe kliniek Kind & Jeugd in gebruik — https://emergiskindenjeugd.nl/wie-zijn-we/nieuws/2019-08/nieuwe-kliniek-kind-jeugd-gebruik
- [S7] BouwTotaal: Circulair project kinder- en jeugdkliniek in Kloetinge — https://www.bouwtotaal.nl/2019/07/circulair-project-kinder-en-jeugdkliniek-in-kloetinge/
- [S8] Burobas Portfolio: Emergis Ithaka — https://www.burobas.nl/project/emergis-ithaka-circulariteit-duurzaamheid-healing-environment-ontwerp/
- [S9] Bouwwereld: Hergebruikte kozijnen — https://www.bouwwereld.nl/bouwdelen/gevels/hergebruikte-kozijnen/
- [S10] PL: Construction details in NL — https://www.pl-pr-architects.nl/nl/construction-and-material-specification-details/
- [S11] Architectuur.nl: Symposium in circulaire kinder-en jeugdkliniek Emergis — https://www.architectuur.nl/nieuws/evenementen/symposium-in-circulaire-kinder-en-jeugdkliniek-emergis/
- [S12] Paree: Ithaka Emergis Kloetinge — https://www.paree.nl/project/ithaka-emergis-kloetinge/
- [S13] Skipr: Emergis bouwt kliniek met hergebruikt materiaal — https://www.skipr.nl/nieuws/emergis-bouwt-kliniek-met-hergebruikt-materiaal/
- [S14] Scribd/Circular Buildings case-study excerpt — https://www.scribd.com/document/960365903/Circular-Buildings-Strategies-and-Case-Studies-2021
- [S15] DWT Groep: Kinder- en jeugdkliniek Emergis – Kloetinge — https://dwtgroep.nl/projecten/kinder-en-jeugdkliniek-emergis-kloetinge/
