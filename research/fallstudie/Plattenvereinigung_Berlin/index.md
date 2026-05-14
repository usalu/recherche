---
entity: "fallstudie"
id: "Plattenvereinigung_Berlin"
title: "Plattenvereinigung Berlin — Fallstudie Direct Reuse"
build_status: "promoted_phase42"
legacy_paths:
  - "Gebäude\\Plattenvereinigung_Berlin.md"
node_kind: "core"
bauobjekt:
  - "Plattenvereinigung_Berlin"
projekt:
  - "Plattenvereinigung_Berlin"
---

# Plattenvereinigung Berlin — Fallstudie Direct Reuse

## Legacy Content

### Legacy Source: Gebäude\Plattenvereinigung_Berlin.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Plattenvereinigung_Berlin
- Secondary targets: projekt/Plattenvereinigung_Berlin; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Plattenvereinigung Berlin — Fallstudie Direct Reuse

**Arbeitsregel:** Als Wiederverwendung gezählt werden nur wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Lose Möbel, Dekoration, reine DfD-Strategien ohne tatsächlichen Wiedereinbau sowie reiner Bestandserhalt werden nicht als Direct Reuse gewertet.

**Hinweis zur Quellenlage:** Nicht belegte Angaben sind als **unbekannt** markiert. Normnummern, Kosten, Mengen und CO₂-Werte werden nur genannt, wenn sie in den angegebenen Quellen belastbar auftauchen.

## 1. EINORDNUNG

- **Entscheidung:** ANHANG / temporäres Recyclinggebäude und Bildungsprototyp
- **Bewertung:** ★★☆☆☆
- **Begründung:** Tatsächliche Wiederverwendung von ost- und westdeutschen Betonfertigteilen ist belegt. Wegen temporärem/mobilen Charakter, Bildungsfokus, fehlenden Mengen/Normdaten und begrenzter technischer Detailtiefe nicht Hauptfall.
- **Vertrauensgrad:** belegt für Projekt, Herkunft der Bauteile und De-/Remontierbarkeit; teilweise belegt für konkrete Bauteilliste und technische Prüfungen
- **Warnung Bestandserhalt:** nein
- **Warnung Möbel/Dekoration:** nein
- **Projektstatus:** gebaut / temporär / mobil / weitergenutzt als Projektraum

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Plattenvereinigung Berlin | untersuchte Fallstudie / temporäres Recyclinggebäude | S1, S2, S4 | belegt | Forschungs-, Bildungs- und Begegnungsraum |
| Gebäude | vollständig de- und remontierbares Recycling-Gebäude | zentrales Objekt | S1, S2, S4 | belegt | mobil/temporär, mehrere Standorte |
| Ort | Peter-Behrens-Halle TU Berlin; Tempelhofer Feld Berlin | Entwicklungs- und Nutzungsorte | S3, S4 | belegt | Jan 2010–Mai 2011 Halle; ab Mai 2011 Tempelhofer Feld |
| Material | wiederverwendete ost- und westdeutsche Plattenbauteile / Fertigbetonteile | Hauptmaterial des Gebäudes | S1, S2, S4 | belegt | genaue Mengen unbekannt |
| Bauteil | Fertigbetonteile aus Olympischem Dorf München und PH12-Punkthochhaus Frankfurt/Oder | Herkunft der wiederverwendeten Bauteile | S3, S4 | belegt | Ost-/West-Herkunft ist Teil des Konzepts |
| Bauteil | Treppenelemente | im Abschlussbericht als montiert erwähnt | S5 | teilweise belegt | Menge und genaue Herkunft unbekannt |
| Projekt | Forschungs- und Bildungsprojekt zur Recyclingkultur | programmatischer Rahmen | S1, S2, S4 | belegt | nicht nur Architektur-, auch Vermittlungsprojekt |
| Förderprogramm | DBU-Förderung; bpb-Förderung für Programm am Tempelhofer Feld | Förder-/Bildungskontext | S4 | belegt | Beträge unbekannt |
| Lehrstuhl | TU Berlin Fachgebiet Bauphysik und Baukonstruktionen | wissenschaftlicher Partner | S1, S4 | belegt | Lehrbaustellen mit Auszubildenden und Studierenden |
| Hürde | Reinigung ölhaltiger Außenfarbe auf Olympiaplatten | Aufbereitungshürde | S6 | teilweise belegt | aus PDF-Auszug; Vollbericht prüfen |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Mobiles Recyclinggebäude | Der Fall ist weder Dauergebäude noch reine Baustelle; Mobilität ist zentral. | De-/Remontage zwischen Peter-Behrens-Halle und Tempelhofer Feld | verknüpft Gebäude, Ort, Logistik, Reuse-Strategie |
| Bildungs-/Lehrbaustelle | Der Prozess war ausdrücklich als Ausbildung und Öffentlichkeit organisiert. | Lehrbaustellen mit Auszubildenden und Studierenden | verknüpft People, Methode, Prozessphase, sozialer Wert |

## 3. FALLSTUDIE

- **Name:** Plattenvereinigung
- **Ort:** Berlin; Entwicklung in Peter-Behrens-Halle der TU Berlin; Umsetzung auf Tempelhofer Feld
- **Gebäude:** temporäres, vollständig de- und remontierbares Recyclinggebäude / Begegnungsraum
- **Projekt:** Forschungs- und Bildungsprojekt zur Recyclingkultur und nachhaltigen Stadtentwicklung
- **Beteiligte People / Akteure:** zukunftsgeraeusche GbR; TU Berlin Fachgebiet Bauphysik und Baukonstruktionen; Auszubildende/Studierende; DBU; bpb im Programmkontakt
- **Architekt:** unbekannt / Projektteam nicht eindeutig als Architekturbüro belegt
- **Tragwerksplaner:** unbekannt
- **Bauherr:** unbekannt; Projektträger zukunftsgeraeusche GbR
- **Zeitraum:** Jan 2010–Mai 2011 Peter-Behrens-Halle; Mai 2011 Umsetzung Tempelhofer Feld; danach weitere Nutzung als Projektraum belegt
- **Ursprüngliche Nutzung:** Fertigbetonteile aus Olympischem Dorf München und einem PH12-Punkthochhaus in Frankfurt/Oder
- **Neue Nutzung:** temporäres Recyclinggebäude, Werkstatt, Studienobjekt, Kultur-/Bildungsraum
- **Fläche / Maßstab:** unbekannt
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** gut für Programmatik, Orte und Herkunft; schwach für Bauteilmengen, Verbindungen, Normen, Kosten, CO₂

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** ex-situ / Bauteilwiederverwendung / Gebäudeversetzung / partiell bis gesamt als mobiles Reuse-Gebäude
- **Hauptniveau:** Tragwerk + Hülle + räumliches Gefüge, genaue Rollen der Bauteile teilweise unbekannt
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Bauteile wurden aus entfernten Beständen entnommen und in einem neuen mobilen Gebäude zusammengesetzt. Das ist kein reiner Bestandserhalt und kein Betonrecycling zu Zuschlag.
- **Warum ist der Fall relevant?** Er kombiniert technische Bauteilwiederverwendung, Mobilität/De- und Remontage, Lehrbaustelle und kulturelle Vermittlung.

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ost- und westdeutsche Plattenbauteile | Betonfertigteile | Olympisches Dorf München und PH12-Hochhaus Frankfurt/Oder | Wohn-/Olympia-/Hochhaus-Fertigteile; genaue Funktion je Bauteil unbekannt | mobiles Recyclinggebäude / Begegnungsraum | unbekannt | teilweise/unbekannt | ja | ja/teilweise | nein | Reinigung, Betonarbeiten, Montage | unbekannt | unbekannt | Standsicherheit, Demontierbarkeit | unbekannt | heterogene Bauteile | S1–S4 | teilweise |
| Wand-/Fassadenelemente | Betonfertigteile | München / Frankfurt-Oder; genaue Zuordnung unbekannt | Wand/Fassade; unbekannt | Raumabschluss/Fassade | unbekannt | teilweise/unbekannt | ja | ja | nein | Reinigung, Anpassung | unbekannt | unbekannt | Witterung, Standsicherheit | unbekannt | Oberfläche, Anschlüsse | S3, S4 | ja |
| Deckenelemente / Zwischendecke | Betonfertigteile; genaue Art unbekannt | unbekannt innerhalb der genannten Quellen | Decke; unbekannt | Zwischendecke/Deckenelement | unbekannt | ja/teilweise | ja | nein/teilweise | nein | Auflagerung der Zwischendecke erwähnt | unbekannt | unbekannt | Lastabtragung | unbekannt | Auflagerung, Gewicht | S5 | ja |
| Treppenelemente | Betonfertigteile; genaue Art unbekannt | unbekannt innerhalb der genannten Quellen | Treppe; unbekannt | Erschließung | unbekannt | ja/teilweise | ja | nein | nein | Montage der Treppenelemente erwähnt | unbekannt | unbekannt | Tragfähigkeit, Nutzungssicherheit | unbekannt | Montage und Anschlüsse | S5 | ja |
| Primärtragwerk / Aussteifung | unbekannt | unbekannt | unbekannt | tragender Rahmen/Aussteifung | unbekannt | ja | ja | nein | nein | unbekannt | unbekannt | unbekannt | Standsicherheit, Demontierbarkeit | unbekannt | technische Detaildaten fehlen | S6 | ja |
| Fenster/Türen/Dach/TGA/Sanitär/Beleuchtung/feste Einbauten | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine belastbare Quelle gefunden | ja |

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Bauteile aus Ost- und West-Beständen als Ressource identifiziert | zukunftsgeraeusche GbR; TU Berlin | Ressourcenschutz + Geschichtsvermittlung | unbekannt | unbekannt | unbekannt | unbekannt | München, Frankfurt/Oder, Berlin | verschiedene Bauteilsysteme | gemeinsame Architektur aus heterogenen Teilen | S1–S4 |
| Bauteilinventar | Fertigbetonteile für mobiles Gebäude zusammengestellt | Projektteam; TU Berlin; Auszubildende/Studierende | Lehrbaustelle | unbekannt | unbekannt | Reinigung/Betonarbeiten | unbekannt | Peter-Behrens-Halle | Mengen/Dokumentation unbekannt | experimentelle Umgebung | S4, S6 |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Reinigung ölhaltiger Farbe bei Olympiaplatten erwähnt | unbekannt | unbekannt | ölhaltige Außenfarbe | zeitaufwändige Reinigung | S6 |
| Rückbau/Ausbau | Fertigbetonteile aus München und Frankfurt/Oder gewonnen | unbekannt | selektiver Rückbau unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Transport nach Berlin | Herkunft weit verteilt | unbekannt | S3, S4 |
| Transport | Bauteile nach Berlin und später Tempelhofer Feld bewegt | unbekannt | Schwertransport/Kran wahrscheinlich | unbekannt | nicht relevant | unbekannt | unbekannt | München, Frankfurt/Oder, Berlin | Gewicht und Distanz | unbekannt | S3, S4 |
| Lagerung | Aufbau/Entwicklung in Peter-Behrens-Halle | TU Berlin; Lehrbaustellen | Haus-im-Haus / experimentelle Umgebung | unbekannt | nicht relevant | unbekannt | unbekannt | Halle als Werkstatt | Koordination Ausbildung und Bau | Lehrbaustelle | S4 |
| Aufbereitung | Reinigung, Betonarbeiten, Montagevorbereitung | Auszubildende/Studierende; Projektteam | Lehrbaustelle | unbekannt | nicht relevant | Reinigung/Betonarbeiten | unbekannt | Halle | ölhaltige Farbe/Bauteilzustand | Reinigung | S5, S6 |
| Planung | vollständig de- und remontierbares Gebäude geplant | zukunftsgeraeusche; TU Berlin; Partner | mobiles Recyclinggebäude | unbekannt | unbekannt | unbekannt | unbekannt | mehrere Standorte | temporäre Nutzung + Reuse-Bauteile | demontierbarer Aufbau | S1, S2, S4 |
| Genehmigung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Tempelhofer Feld als öffentlicher Ort | temporäres Gebäude im Park | unbekannt | keine belastbare Quelle gefunden |
| Wiedereinbau | Umsetzung auf Tempelhofer Feld im Mai 2011 | Projektteam | De- und Remontage | unbekannt | nicht relevant | Montage der Fertigteile | unbekannt | Standortwechsel | Remontage schwerer Fertigteile | demontierbares Konzept | S3, S4 |
| Monitoring | Nutzung als Studienobjekt, Werkstatt, Projektraum und Kulturplattform | zukunftsgeraeusche; Nutzer:innen | Workshops, Vorträge, Theater/Kunst | unbekannt | nicht relevant | unbekannt | unbekannt | laufende Programmnutzung | Langzeitdaten unbekannt | öffentlicher Bildungsbetrieb | S4 |

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Recyclinggebäude aus wiederverwendeten Betonfertigteilen; genaue Statik unbekannt | Standsicherheit, Demontierbarkeit | unbekannt | unbekannt | heterogene Fertigteile aus mehreren Systemen | vollständig de- und remontierbares Gebäude | S1–S4 |
| Lastabtragung | unbekannt; Berichtsauszug erwähnt Zwischendecke und Treppenelemente | unbekannt | unbekannt | unbekannt | alte Fertigteile + neue Nutzung | unbekannt | S5, S6 |
| Verbindung | demontierbar/remontierbar belegt; konkrete Verbindung unbekannt | lösbar, tragfähig, wiederholbar | unbekannt | unbekannt | Verbindung heterogener Fertigteile | demontierbares Gesamtkonzept | S1, S2 |
| Brandschutz | unbekannt | unbekannt | unbekannt | unbekannt | temporäre öffentliche Nutzung | unbekannt | keine belastbare Quelle gefunden |
| Schallschutz | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine belastbare Quelle gefunden |
| Feuchte/Wärmeschutz/Luftdichtheit | unbekannt; temporäres Recyclinggebäude | unbekannt | unbekannt | unbekannt | Fugen und Bestandsoberflächen | unbekannt | keine belastbare Quelle gefunden |
| TGA-Integration | unbekannt | unbekannt | unbekannt | unbekannt | temporäre Nutzung | unbekannt | keine belastbare Quelle gefunden |
| Barrierefreiheit | unbekannt | unbekannt | unbekannt | unbekannt | Treppen/temporärer Pavillon | unbekannt | keine belastbare Quelle gefunden |
| Dauerhaftigkeit/Wartung | Gebäude wurde umgesetzt und weitergenutzt; technische Langzeitdaten unbekannt | wiederholte De-/Remontage | unbekannt | unbekannt | Oberflächenreinigung, Bauteilverschleiß | Reinigung und Lehrbaustellenbetrieb | S4, S6 |
| Zulassung/Haftung | unbekannt | öffentliche Nutzung / temporäres Gebäude | unbekannt | unbekannt | Reuse-Betonfertigteile im mobilen Gebäude | unbekannt | keine belastbare Quelle gefunden |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---|---|---|---|---|---|
| Bauteilherkünfte | Olympisches Dorf München; PH12-Punkthochhaus Frankfurt/Oder | Orte/Donorquellen | Projektangabe | Fertigbetonteile | S3, S4 | belegt |
| Entwicklung in Peter-Behrens-Halle | Jan 2010–Mai 2011 | Zeitraum | Projektangabe | Projektphase | S4 | belegt |
| Umsetzung Tempelhofer Feld | Mai 2011 | Datum/Monat | Projektangabe | Standortwechsel | S3, S4 | belegt |
| Anzahl Bauteile | unbekannt | Stück | unbekannt | Gesamtgebäude | keine belastbare Quelle gefunden | unbekannt |
| Fläche | unbekannt | m² | unbekannt | Gesamtgebäude | keine belastbare Quelle gefunden | unbekannt |
| wiederverwendete Masse | unbekannt | t | unbekannt | Betonfertigteile | keine belastbare Quelle gefunden | unbekannt |
| CO₂-Einsparung | unbekannt | kg CO₂e | unbekannt | unbekannt | keine belastbare Quelle gefunden | unbekannt |
| DBU/bpb-Förderbetrag | unbekannt | EUR | Förderung belegt, Betrag nicht gefunden | Projektförderung | S4 | teilweise belegt |

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie: technisch/rechtlich/wirtschaftlich/logistisch/gestalterisch/sozial | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Heterogene Bauteilherkünfte | technisch/gestalterisch | Ost- und West-Fertigteile aus unterschiedlichen Systemen | Planung und Verbindungen komplex | Bauteil, Tragwerkssystem, Verbindung | gemeinsame Architektur und Demontierbarkeit | Heterogenität kann technische und kulturelle Ressource sein | S1–S4 |
| Schwerlastlogistik über große Distanzen | logistisch | Betonfertigteile aus München und Frankfurt/Oder nach Berlin | Transportaufwand; Kosten/CO₂ unbekannt | Logistik, Wirtschaft, Kennwert | unbekannt | Transportbilanz früh klären | S3, S4 |
| Oberflächenreinigung | technisch/wirtschaftlich | ölhaltige Außenfarbe auf Olympiaplatten | zeitaufwändige Reinigung | Aufbereitungsmethode, Schadstoff, Wirtschaft | Reinigung vor Wiederverwendung | Oberflächen können Hauptaufwand werden | S6 |
| Temporäre öffentliche Nutzung | rechtlich/sozial | mobiles Gebäude auf Tempelhofer Feld | Genehmigungs-/Betriebsdetails nötig | Recht, Ort, Prozessphase | Projektpartnerschaften/Förderung; Details unbekannt | Reuse-Pavillons brauchen Betreiber- und Genehmigungsmodell | S4 |
| Datenlücken | methodisch | öffentliche Quellen nennen wenig Mengen/Normen/Kosten | Bewertung nur teilweise möglich | Kennwert, Norm, Wirtschaft | Abschlussbericht/Genehmigung prüfen | Reuse-Projekte sollten Bauteilpässe veröffentlichen | S1–S6 |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** Projektbasierte Beschaffung/Ernte von Fertigbetonteilen aus zwei Beständen; Verträge unbekannt.
- **Bauteilbörse / Quelle:** keine Bauteilbörse belegt; direkte Herkunft aus Olympischem Dorf München und PH12-Hochhaus Frankfurt/Oder.
- **Kostenwirkung:** unbekannt.
- **Zeitwirkung:** Entwicklung/Aufbau über Jan 2010–Mai 2011; konkrete Montagezeiten unbekannt.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** Lehrbaustelle mit Auszubildenden/Studierenden; quantitative Arbeitsstunden unbekannt.
- **Lagerung:** Peter-Behrens-Halle als Werkstatt-/Entwicklungs- und Zwischenstandort belegt.
- **Marktbarrieren:** Heterogene Bauteile, schwere Logistik, Oberflächenreinigung, Genehmigung temporärer öffentlicher Nutzung, fehlende Kennwerte.

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** sehr hoch; das Gebäude dient als Medium, Begegnungsraum und Diskursobjekt.
- **räumliche Transformation:** Bauteile aus ehemaligen visionären Ost-/West-Beständen werden in einer gemeinsamen Architektur zusammengesetzt.
- **Atmosphäre / Ausdruck:** experimentell, didaktisch und kulturpolitisch aufgeladen.
- **Umgang mit Spuren:** Geschichte und Geschichten der Bauteile sind ausdrücklich Teil des Konzepts.
- **sozialer Wert:** Lehrbaustelle, Workshops, Kunst-/Theaterprojekte, öffentliche Information.
- **Denkmal- oder Bestandswert:** kulturhistorischer Wert der Herkunftsorte; formaler Denkmalstatus der verwendeten Bauteile unbekannt.
- **Kritik / Grenzen:** technischer Datensatz ist lückenhaft; temporärer Bildungsfokus erschwert Vergleich mit regulären Gebäuden.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** exakte Bauteilanzahl, Fläche, Tragwerksplaner, Verbindungstypen, Prüfungen, Normen, Kosten, CO₂, Transportdistanzen.
- **Sinnvolle neue Entitäten:** Mobiles Recyclinggebäude; Bildungs-/Lehrbaustelle.
- **Fehlende Daten:** Bauteilpass, Donorbauteilliste, Statik, Genehmigung, Materialprüfungen, TGA.
- **Zu prüfende Quellen:** kompletter Abschlussbericht, Projektpartnerlisten, TU-Berlin-Archiv, Genehmigungsunterlagen Tempelhofer Feld.

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** Anhang
- **5 wichtigste Fakten:**
  1. Wiederverwendete Ost- und Westdeutsche Fertigbetonteile.
  2. Herkunft aus Olympischem Dorf München und PH12-Hochhaus Frankfurt/Oder.
  3. Vollständig de- und remontierbares Recyclinggebäude.
  4. Entwicklung in Peter-Behrens-Halle, Umsetzung auf Tempelhofer Feld 2011.
  5. Starkes Bildungs-/Kulturprojekt, wenige technische Kennwerte öffentlich.
- **5 wichtigste Bauteile:**
  1. Betonfertigteil-Platten.
  2. Wand-/Fassadenelemente.
  3. Deckenelemente/Zwischendecke.
  4. Treppenelemente.
  5. Verbindungssysteme: unbekannt.
- **5 wichtigste Hürden:**
  1. Heterogene Bauteilherkünfte.
  2. Schwerlastlogistik.
  3. Oberflächenreinigung/Altbeschichtungen.
  4. Temporäre öffentliche Nutzung und Genehmigung.
  5. Datenlücken bei Kennwerten und Normen.
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Reuse kann Bildungs- und Baupraxis verbinden.
  2. Mobilität/De- und Remontage kann Reuse sichtbar machen.
  3. Bauteilgeschichte kann kultureller Mehrwert sein.
  4. Oberflächenzustand ist oft genauso wichtig wie Tragfähigkeit.
  5. Ohne veröffentlichte Bauteilpässe bleibt Bewertung begrenzt.
- **5 offene Fragen:**
  1. Wie viele Bauteile wurden tatsächlich eingebaut?
  2. Welche Verbindungen wurden verwendet?
  3. Welche Genehmigungslogik galt für das Tempelhofer Feld?
  4. Welche Kosten und Transportemissionen entstanden?
  5. Wie wurde die Resttragfähigkeit nachgewiesen?

## Quellen und Links

- **S1**: TU Berlin, FG Bauphysik: Projekt Plattenvereinigung — https://www.tu.berlin/bauphysik/forschung/abgeschlossene-projekte/projekt-plattenvereinigung
- **S2**: Plattenvereinigung Projektseite — https://www.plattenvereinigung.de/project/
- **S3**: Plattenvereinigung Orte — https://www.plattenvereinigung.de/project/orte/
- **S4**: Tempelhofer Feld: Plattenvereinigung — https://www.tempelhoferfeld.de/entdecken-erleben/projekte-buergerschaftlichen-engagements/plattenvereinigung/
- **S5**: Plattenvereinigung Abschlussbericht PDF, Einzelseiten — https://www.plattenvereinigung.de/wp-content/uploads/2023/03/plv_abschlussbericht_web_einzelseiten.pdf
- **S6**: Plattenvereinigung Abschlussbericht PDF, Doppelseiten — https://www.plattenvereinigung.de/wp-content/uploads/2023/03/plv_abschlussbericht_web_doppelseiten.pdf
