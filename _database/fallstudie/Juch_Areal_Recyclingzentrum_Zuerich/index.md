---
entity: "fallstudie"
id: "Juch_Areal_Recyclingzentrum_Zuerich"
title: "Juch-Areal Recyclingzentrum, Zürich-Altstetten"
build_status: "promoted_phase42"
legacy_paths:
  - "Gebäude\\Juch_Areal_Recyclingzentrum_Zuerich.md"
node_kind: "core"
bauobjekt:
  - "Juch_Areal_Recyclingzentrum_Zuerich"
projekt:
  - "Juch_Areal_Recyclingzentrum_Zuerich"
---

# Juch-Areal Recyclingzentrum, Zürich-Altstetten

## Legacy Content

### Legacy Source: Gebäude\Juch_Areal_Recyclingzentrum_Zuerich.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Juch_Areal_Recyclingzentrum_Zuerich
- Secondary targets: projekt/Juch_Areal_Recyclingzentrum_Zuerich; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Juch-Areal Recyclingzentrum, Zürich-Altstetten

## 1. EINORDNUNG
- **Entscheidung:** ANHANG / FUTURE CANDIDATE
- **Bewertung:** ★★★☆☆, mit Potenzial auf ★★★★★ nach Fertigstellung und Nachweis des tatsächlichen Wiedereinbaus
- **Begründung:** Das Projekt ist als öffentliches Reuse-Pilotprojekt mit starker geplanter Direct Reuse belegt: eine bestehende Hallenkonstruktion soll 1:1 mit kleinen Anpassungen versetzt werden; gebrauchte Stahlbetonplatten sollen Hallenboden und Betriebsgebäude bilden. Es ist jedoch nach Quellenlage noch nicht fertiggestellt.
- **Vertrauensgrad:** teilweise belegt
- **Warnung Bestandserhalt:** nein, aber Projekt ist noch nicht gebaut
- **Warnung Möbel/Dekoration:** nein
- **Projektstatus:** geplant / Ausführung vorgesehen; Bauzeit 2026–2027 laut Stadt Zürich, Ausführungskredit/Volksabstimmung Juni 2026

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Recyclingzentrum Juch-Areal | Öffentliches Reuse-Pilotprojekt | [S1], [S2], [S3] | belegt | noch nicht fertig |
| Ort | Zürich-Altstetten, Juch-Areal | Standort | [S1], [S2], [S4] | belegt | ERZ-Recyclingzentrum |
| Projekt | Neues Recyclingzentrum ERZ Juch-Areal | Empfängerprojekt | [S1], [S2], [S4] | belegt | Halle + Betriebs-/Personalbereich |
| Bauherr | Stadt Zürich / Amt für Hochbauten; ERZ als Eigentümervertretung/Betreiber | öffentliche Bauherrschaft | [S1], [S4] | belegt | Perita nennt Stadt Zürich / AHB |
| People | Graber Pulver Architekt:innen | Wettbewerbsgewinner / Architektur | [S1], [S2], [S4] | belegt | Umsetzungsteam |
| People | Zirkular GmbH | Fachplanung Re-Use / Bauteiljagd / BIM-Katalog | [S1], [S2] | belegt | zentrale Reuse-Rolle |
| People | manoa Landschaftsarchitekten | Landschaft | [S5] | belegt | nicht Direct Reuse |
| People | Weber + Brönnimann AG | Bauingenieurwesen | [S2] | belegt | Tragwerksplanung laut Stadt Zürich |
| People | EK Energiekonzepte | Bauphysik, Nachhaltigkeit und Haustechnik-Konzept im Wettbewerbsteam | [S9] | teilweise belegt | Rolle im Siegerteam-Kontext |
| Bauteil | Stahlstruktur der ehemaligen Recyclinghalle Hagenholz | wird sorgfältig demontiert, eingelagert und 1:1 wieder aufgebaut | [S1], [S2], [S3], [S4] | belegt für Planung | tragendes Haupt-Reuse-Bauteil |
| Bauteil | Betonplatten aus dem Kerenzerbergtunnel | Wiederverwendung für Fundationen und Bodenbeläge / Hallenboden | [S2], [S3], [S4] | belegt für Planung | genaue Menge unbekannt |
| Datenmodell | digitaler Bauteilkatalog | Wettbewerbsgrundlage mit Bauteilen aus städtischen Liegenschaften | [S1], [S2] | belegt | BIM-Methodik |
| Methode | Bauteiljagd / component hunting | Suche und Koordination reused Bauteile | [S1], [S2] | belegt | Zirkular-Mandat |
| Kennwert | fast 600 t CO₂ / gut 40% Reduktion | Treibhausgasvergleich Gewinnerprojekt vs. konventioneller Neubau | [S1], [S2], [S3], [S4] | teilweise belegt | genaue Bilanzgrenze unbekannt |
| Wirtschaft | CHF 33,1 Mio. Ausführungskredit / CHF 18 Mio. frühere Schätzung / CHF 25 Mio. Perita-Bausumme | Kostenangaben nach Quellenstand | [S1], [S2], [S3], [S6] | Quellenkonflikt | Stadt Zürich 2025/26 ist aktuellste öffentliche Kostenquelle |
| Projektstatus | Bauzeit 2026–2027, Fertigstellung Q4 2027 geplant | Zeitplan | [S2], [S3] | belegt für Planung | Zirkular ältere Quelle nennt Ende 2026 |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Bauteilpool öffentlicher Bestand | Der Wettbewerb nutzte städtische Bestandsbauteile als Ressource. | digitaler Bauteilkatalog aus städtischen Liegenschaften. | Datenmodell, Bauteilbörse, Logistik |
| Versetzte Hallenkonstruktion | Reuse betrifft ein ganzes Tragwerks-/Hallensystem, nicht nur Einzelbauteile. | bestehende Halle wird am neuen Standort 1:1 wieder aufgebaut. | Tragwerkssystem, Bauteil, Abbruchmethode |

## 3. FALLSTUDIE
- **Name:** Recyclingzentrum Juch-Areal / ERZ Juchareal
- **Ort:** Zürich-Altstetten, Schweiz
- **Gebäude:** neues Recyclingzentrum mit großer Anliefer-, Sortier- und Sammelhalle sowie Verwaltungs-/Personalbereich
- **Projekt:** öffentliches Pilotprojekt für Re-Use-Bauteile und BIM-Methodik
- **Beteiligte People / Akteure:** Stadt Zürich, Amt für Hochbauten, Entsorgung + Recycling Zürich (ERZ), Graber Pulver Architekt:innen, Weber + Brönnimann AG, Zirkular GmbH, manoa Landschaftsarchitekten, Perita AG, EK Energiekonzepte; weitere unbekannt
- **Architekt:** Graber Pulver Architekt:innen AG
- **Tragwerksplaner:** Weber + Brönnimann AG laut Stadt Zürich
- **Bauherr:** Stadt Zürich / Amt für Hochbauten; ERZ als Betreiber/Eigentümervertretung
- **Zeitraum:** Architekturwettbewerb 2023; Ausführungskredit/Volksabstimmung 2026; Bauzeit 2026–2027 geplant
- **Ursprüngliche Nutzung:** Donor-Halle: ehemalige städtische Recyclinghalle Hagenholz; Betonplatten: Kerenzerbergtunnel; weitere Beton-Pilzstützen/Deckenelemente: Schellinghalle Rümlang
- **Neue Nutzung:** Recyclingzentrum / Werkstoffsammelstelle / Betrieb und Verwaltung
- **Fläche / Maßstab:** unbekannt
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** sehr gute Projektquellen für Strategie, Hauptbauteile und frühe Prüf-/Beschaffungsprozesse; noch keine gebaute Schlussdokumentation nach Wiedereinbau

## 4. REUSE-STRATEGIE
- **Art der Wiederverwendung:** geplant: partiell; ex-situ; Bauteilwiederverwendung; Hallensystemversetzung; Stahl-/Betontragwerksreuse; digitales Bauteilinventar
- **Hauptniveau:** Tragwerk / Bodenplatten / Betriebsgebäude / Material
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die Hallenkonstruktion wird demontiert und am neuen Standort wieder aufgebaut; das zählt als Direct Reuse. Gebrauchte Stahlbetonplatten werden als Bauteile wieder eingesetzt; das zählt als Direct Reuse. Recycling von Wertstoffen durch die spätere Nutzung des Gebäudes zählt nicht als Bau-Reuse.
- **Warum ist der Fall relevant?** Öffentlicher Bauherr, Wettbewerb auf Reuse-Anteil, digitales Bauteilinventar, potenziell tragende 1:1-Versetzung einer Hallenkonstruktion.

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Stahlstruktur der Traghalle Hagenholz | Stahl | ehemalige städtische Recyclinghalle Hagenholz | Hallentragwerk / Dachtragwerk | Hallentragwerk Recyclingzentrum Juch | einzelne Hallenbauteile beschriftet, demontiert und eingelagert; genaue Masse unbekannt | ja | ja | teilweise | nein | Beschriften, sorgfältig demontieren, einlagern, 1:1 wieder aufbauen | vorhandene/neue Stahlanschlüsse unbekannt | Eignung durch Spezialisten geprüft | Tragfähigkeit, Robustheit, Brandschutz | Schweizer Baunormen / SIA, genaue Normen unbekannt | Resttragfähigkeit, Demontage, Lagerung | [S2], [S3], [S4], [S8] | teilweise |
| Betonplatten aus Kerenzerbergtunnel | Beton / Faserbeton nach Stadt-Studie | Sicherheitsstollen Kerenzerbergtunnel | Tunnel-/Stollenplatten | Fundationen, Bodenbeläge, Hallenboden | Menge unbekannt | ja/als Platte/Boden | ja | nein | nein | Ausbau, Prüfung, Transport, Neuverlegung | Fugen/Anschlüsse unbekannt | Eignung durch Spezialisten geprüft | Tragfähigkeit, Ebenheit, Dauerhaftigkeit, Frost/Tausalz ggf. | Schweizer Normen unbekannt | Gewicht, Transport, Plattenzustand | [S2], [S3], [S4] | teilweise |
| Beton-Pilzstützen mit Deckenelementen | Beton/Stahlbeton | Schellinghalle Rümlang | Tragstruktur | geplante Wiederverwendung im Projektkontext | unbekannt | ja | ja | nein | nein | Beschaffung, Prüfung, Vorbereitung zum Wiedereinbau | unbekannt | in Stadt-Studie als Fallbeispiel dokumentiert | Tragfähigkeit | Schweizer Normen unbekannt | Anschluss und Resttragfähigkeit | [S4] | teilweise |
| Stahlträger und Trapezbleche Dach | Stahl / Trapezblech | zurückgebaute Recyclinghalle Hagenholz | Dachtragwerk / Dachdeckung | Dach-/Hallenelemente im Neubau | unbekannt | Stahlträger: ja; Trapezblech: Hülle/Dach | ja | ja | nein | Demontage, Einlagerung, Wiedereinbau | unbekannt | Eignung geprüft | Tragfähigkeit, Witterung, Brand | unbekannt | Korrosion, Dichtheit | [S3] | teilweise |
| Bauteilkatalog-Elemente | verschiedene | städtische Liegenschaften | verschiedene | Wettbewerbs-/Planungsressource | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Erfassung/Katalogisierung | unbekannt | unbekannt | je Bauteil | unbekannt | Verfügbarkeit während Planung | [S1], [S2] | ja |
| Betriebsgebäude | neue + gebrauchte Elemente | Juch-Areal + Reuse-Bauteile | unbekannt | Verwaltungs-/Personalbereich | unbekannt | ja/unklar | ja | ja | technisch: ja | unbekannt | unbekannt | unbekannt | Wärme/Brand/Schall | unbekannt | beheizte Hülle aus Reuse-Bauteilen anspruchsvoll | [S1], [S5] | ja |
| Photovoltaik / Gründach | neu oder unbekannt | unbekannt | unbekannt | Energie/Ökologie | unbekannt | nein | nein | Dach | technisch: ja | unbekannt | unbekannt | unbekannt | Strom/Lasten | unbekannt | nicht als Direct Reuse belegt | [S6] | ja |
| vertikaler Pflanzenfilter / Bäume | Pflanzen | Baumschulware / „Ware“ | Bäume/Pflanzen | Biodiversität/Luftqualität | unbekannt | nein | räumlich | nein | technisch: teils | Umpflanzung | unbekannt | unbekannt | Pflege | unbekannt | zählt nicht als Bauteilreuse | [S5] | teilweise |
| Fenster, Türen, TGA, Sanitär, Beleuchtung, Dach, Treppen, Geländer | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | nicht öffentlich belegt | unbekannt | ja |

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | städtische und externe Bestandsbauteile identifizieren | Zirkular, Stadt Zürich AHB, ERZ | Bauteiljagd | digitaler Bauteilkatalog / BIM | unbekannt | Katalogisierung | Eignung durch Spezialisten geprüft | städtischer Bauteilpool | Verfügbarkeit | Wettbewerb mit Bauteilkatalog | [S1], [S2], [S4] |
| Bauteilinventar | Katalog als Wettbewerbsgrundlage | Zirkular, AHB, ERZ | digitale Bauteilerfassung | BIM-Methodik | unbekannt | Datenmodell | unbekannt | unbekannt | Datenqualität | Katalog aus städtischem Eigentum | [S1], [S2] |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | nicht publiziert | unbekannt | unbekannt |
| Rückbau | Stahlstruktur Hagenholz beschriften, sorgfältig demontieren und einlagern | ERZ/Stadt, Rückbauakteure unbekannt | selektiver Rückbau | BIM/Markierung unbekannt | Demontage statt Abbruch | bauteilschonend | Eignungsprüfung | Lagerung auf ERZ-Areal | Erhalt der Bauteilqualität | Beschriftung + Einlagerung bis Wiederaufbau | [S2], [S3], [S4] |
| Ausbau | Betonplatten aus Kerenzerbergtunnel und Beton-Pilzstützen/Deckenelemente beschaffen | Zirkular, Stadt, Donorakteure | Bauteilernte | digitaler Bauteilkatalog | Rückbau/Entnahme | Sortierung/Reinigung | Eignung geprüft | Schwertransport | Gewicht/Beschädigung | koordinierte Bauteiljagd | [S2], [S3], [S4] |
| Transport | Halle/Platten an neuen Standort | unbekannt | Schwer-/Bauteillogistik | unbekannt | entfällt | Schutz/Markierung | unbekannt | urbaner Transport | Größe/Gewicht | unbekannt | unbekannt |
| Lagerung | Zwischenlagerung möglich | unbekannt | unbekannt | unbekannt | entfällt | wettergeschützt | unbekannt | Lagerfläche | Timing | unbekannt | unbekannt |
| Aufbereitung | kleinere Anpassungen an Hallenkonstruktion | unbekannt | minimalinvasive Anpassung | unbekannt | entfällt | Reparatur/Anpassung | unbekannt | Werkstatt/Baustelle | Passgenauigkeit | kleine Anpassungen | [S1], [S2] |
| Planung | Siegerprojekt auf Reuse-Bauteile entwickeln | Graber Pulver, Zirkular | Reuse-Fachplanung | BIM | entfällt | unbekannt | unbekannt | Koordination | Bauteile ändern Planung | Fachplanung Re-Use | [S1], [S2] |
| Genehmigung | öffentlicher Neubau mit Ausführungskredit und Volksabstimmung | Stadt Zürich, Gemeinderat/Stimmbevölkerung | öffentliches Bauverfahren | unbekannt | entfällt | Rahmenbedingungen geklärt | behördliche Prüfung | unbekannt | Norm-/Haftungsfragen | rechtliche Rahmenbedingungen klären | [S2], [S3] |
| Wiedereinbau | geplant: Halle und Stahlbetonplatten montieren | Graber Pulver, Ausführung unbekannt | Wiedermontage | BIM | entfällt | Montage | unbekannt | Baustelle Juch | noch nicht nachgewiesen | Fertigstellung abwarten | [S1], [S2], [S5] |
| Monitoring | THG-Bilanzvergleich | Zirkular/Planer | LCA/THG-Bilanz | unbekannt | entfällt | entfällt | unbekannt | entfällt | Bilanzgrenzen unbekannt | Vergleich mit konventionellem Neubau | [S1], [S2], [S3] |

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Stahlstruktur der Recyclinghalle Hagenholz, Betonplatten Kerenzerbergtunnel und Beton-Pilzstützen/Deckenelemente Schellinghalle Rümlang als Reuse-Trag-/Bauteile | Standsicherheit, Nutzlasten | Schweizer Normen / SIA, genaue Normen unbekannt | Eignung durch Spezialisten geprüft | Resttragfähigkeit | Fachplanung Re-Use + Bauingenieurwesen | [S2], [S3], [S4] |
| Lastabtragung | Halle + Hallenboden + Betriebsgebäude | schwere Betriebs-/Verkehrslasten | unbekannt | unbekannt | gebrauchte Platten, neue Nutzung | statischer Nachweis erforderlich | [S1] |
| Verbindung | Hallenverbindungen und Plattenfugen unbekannt | Montage-/Lastübertragung | unbekannt | unbekannt | alte Anschlüsse | kleine Anpassungen | [S1] |
| Brandschutz | Recyclingzentrum mit Halle/Betriebsbereich | Brandschutz für Industrie/Verwaltung | unbekannt | unbekannt | gebrauchte Konstruktion | unbekannt | unbekannt |
| Schallschutz | Betriebsgebäude beheizt/Arbeitsplätze | Arbeits-/Bürostandard | unbekannt | unbekannt | Halle/Betriebslärm | unbekannt | unbekannt |
| Feuchte | Hallenboden und Hülle | Dauerhaftigkeit | unbekannt | unbekannt | gebrauchte Betonplatten | unbekannt | unbekannt |
| Wärmeschutz | nur Betriebsgebäude klimatisiert; Hallenbereich offen/groß | Energiebedarf | unbekannt | unbekannt | Reuse-Hülle vs. Wärmeschutz | kompakter Betriebsbau | [S5] |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Luftdichtheit | Betriebsgebäude unbekannt | beheizte Hülle | unbekannt | unbekannt | gebrauchte Bauteile | unbekannt | unbekannt |
| TGA-Integration | Betriebs-/Verwaltungsbereich benötigt TGA | Arbeitsplatzkomfort | unbekannt | unbekannt | Integration in Reuse-Struktur | unbekannt | [S5] |
| Barrierefreiheit | öffentliches Recyclingzentrum | Zugänglichkeit | Schweizer Recht unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Dauerhaftigkeit | Hallenstruktur mit Restlebensdauer | langfristiger Betrieb | unbekannt | unbekannt | Zustand gebrauchter Bauteile | Prüfung/Anpassung nötig | [S1] |
| Wartung | Hallen-/Betonplattenwartung | Reparierbarkeit | unbekannt | unbekannt | heterogene Bauteile | unbekannt | unbekannt |
| Zulassung | Reuse-Bauteile im öffentlichen Bau | Nachweisfähigkeit | unbekannt | unbekannt | fehlende Standards | Pilotprojekt/Fachplanung | [S1], [S4] |
| Haftung | unbekannt | Gewährleistung | unbekannt | unbekannt | gebrauchte Tragbauteile | unbekannt | unbekannt |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| CO₂-Einsparung gegenüber konventionellem Neubau | fast 600 | t CO₂ | Treibhausgasbilanzvergleich | Gewinnerprojekt vs. konventioneller Neubau; genaue Module unbekannt | [S1], [S2], [S3], [S4] | teilweise belegt |
| THG-Reduktion | gut 40 / über 40 | % | Treibhausgasbilanzvergleich | Gesamtprojekt | [S1], [S2], [S3] | teilweise belegt |
| Ausführungskredit / neue einmalige Ausgaben | 33,1 | Mio. CHF | Stadt Zürich | Projektierung + Erstellung + Grundstücksübertrag | [S2], [S3] | belegt für Planung |
| frühere Baukostenschätzung | ca. 18 | Mio. CHF | Zirkular-Angabe | Gewinnerprojekt | [S1] | veraltet/teilweise belegt |
| Bausumme Perita | 25 | Mio. CHF | Perita-Angabe | Projekt-/Baumanagement | [S6] | teilweise belegt / Quellenkonflikt |
| Fertigstellung | Q4 2027 | Jahr/Quartal | Stadt Zürich | Gesamtprojekt | [S3] | belegt für Planung |
| Bauzeit | 2026–2027 | Jahre | Stadt Zürich | Ausführung | [S2], [S3] | belegt für Planung |
| Fläche | unbekannt | m² | unbekannt | unbekannt | unbekannt | unbekannt |
| wiederverwendete Masse | unbekannt | t | unbekannt | Hallenkonstruktion + Betonplatten | unbekannt | unbekannt |
| Anzahl Bauteile | unbekannt | Anzahl | digitaler Bauteilkatalog | städtische Bauteile | [S1], [S2] | unbekannt |

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie: technisch/rechtlich/wirtschaftlich/logistisch/gestalterisch/sozial | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Projekt noch nicht fertig | methodisch | keine gebaute Schlussdokumentation | Bewertung begrenzt | Projektstatus, Kennwert | Watchlist bis Fertigstellung | Planungsfälle nicht zu hoch bewerten | [S1], [S5] |
| Schwerer Bauteiltransport | logistisch | Hallenstruktur und Betonplatten groß/schwer | Kosten/Zeit/Risiko | Bauteil, Logistik | 1:1-Wiederaufbau, BIM-Katalog | Großbauteile brauchen Logistikkonzept | [S1], [S2] |
| Nachweis Resttragfähigkeit | technisch/rechtlich | gebrauchte Tragbauteile | Prüf-/Haftungsaufwand | Prüfung, Recht | Fachplanung Re-Use | Tragende Reuse-Bauteile früh prüfen | [S1] |
| Verfügbarkeit städtischer Bauteile | logistisch/wirtschaftlich | Katalog aus städtischem Bestand | Entwurf muss sich anpassen | Datenmodell, Bauteil | digitaler Bauteilkatalog | öffentlicher Bauteilpool kann Wettbewerb steuern | [S1], [S2] |
| Kostenquellen widersprechen | wirtschaftlich | unterschiedliche Quellenstände und Projektphasen | unsichere Kostenbewertung | Wirtschaft | aktuelle Stadt-Zürich-Kreditangabe priorisieren, Konflikt offenlegen | keine Kosten glätten | [S1], [S2], [S3], [S6] |

## 10. WIRTSCHAFT UND BESCHAFFUNG
- **Beschaffungsmodell:** öffentlicher Wettbewerb mit digitalem Bauteilkatalog aus städtischen Liegenschaften; Zirkular als Re-Use-Fachplanung/Bauteiljagd.
- **Bauteilbörse / Quelle:** kein klassischer öffentlicher Marktplatz; städtischer Bauteilpool/Katalog.
- **Kostenwirkung:** Quellenkonflikt nach Projektphase: Zirkular nennt ca. CHF 18 Mio. als frühere Schätzung, Perita CHF 25 Mio. Bausumme, Stadt Zürich 2025/26 einen Ausführungskredit von CHF 33,1 Mio.; isolierte Reuse-Kostenwirkung unbekannt.
- **Zeitwirkung:** Bauzeit 2026–2027 geplant; Reuse-Komponenten erfordern frühe Beschaffung, Prüfung, Demontage, Lagerung und Koordination.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** hoch wegen Bauteiljagd, BIM-Katalog, Demontage und Wiedereinbau.
- **Lagerung:** unbekannt.
- **Marktbarrieren:** fehlende Routine im öffentlichen Beschaffungswesen, bauteilspezifische Nachweise, zeitliche Synchronisation von Donor- und Empfängerprojekt.

## 11. GESTALTUNG UND KULTURELLER WERT
- **Sichtbarkeit der Wiederverwendung:** voraussichtlich hoch: wiederverwendete Stahlstruktur, Betonplatten, Leitplanken/Fassadenelemente und Dachbauteile werden als konstruktives Prinzip kommuniziert; gebaute Wirkung noch nicht dokumentiert.
- **räumliche Transformation:** funktionaler Infrastrukturtyp wird zum Demonstrator für urban mining.
- **Atmosphäre / Ausdruck:** Ensemble aus Betriebsgebäude, Halle, Depot, Treppenturm; Reuse als sichtbare Tektonik nach Wettbewerbsbeitrag.
- **Umgang mit Spuren:** unbekannt.
- **sozialer Wert:** öffentliches Recyclingzentrum als Lern-/Vorbildfunktion; Beitrag zur Circular-Zürich-Strategie.
- **Denkmal- oder Bestandswert:** unbekannt.
- **Kritik / Grenzen:** noch nicht fertig; keine vollständigen Mengen/Prüfungen; aktuelle Kostendaten uneinheitlich.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN
- **Nicht gefunden:** genaue Mengen/Massen je Bauteil, vollständige Prüfberichte, Verbindungsmittel, Transportdistanzen, Lagerdauer, finale Ausführungsdetails.
- **Sinnvolle neue Entitäten:** öffentlicher Bauteilpool, versetzte Hallenkonstruktion, Reuse-Wettbewerbsprogramm.
- **Fehlende Daten:** echte eingebaute Masse, tatsächliche CO₂-Bilanz nach Ausführung, Transportdistanzen, Lagerdauer, Verbindungsmittel, Gewährleistung.
- **Zu prüfende Quellen:** Stadt-Zürich-Publikation Teil 2/3, Jurybericht, Bauprojekt-/Ausführungsunterlagen, BIM-Bauteilkatalog, spätere Schlussdokumentation 2027.

## 13. ABSCHLUSS
- **Soll der Fall in die Hauptliste?** Anhang/Watchlist; nach Fertigstellung neu bewerten.
- **5 wichtigste Fakten:**
  1. Öffentliches Pilotprojekt der Stadt Zürich/ERZ für Re-Use-Bauteile und BIM.
  2. Die Stahlstruktur der ehemaligen Recyclinghalle Hagenholz soll beschriftet, demontiert, eingelagert und 1:1 wieder aufgebaut werden.
  3. Betonplatten aus dem Kerenzerbergtunnel sowie Beton-Pilzstützen/Deckenelemente aus der Schellinghalle Rümlang sind als Reuse-Bauteile dokumentiert.
  4. Ein digitaler Bauteilkatalog aus städtischem Eigentum war Wettbewerbsgrundlage.
  5. Quellen nennen fast 600 t CO₂ bzw. gut/über 40% Einsparung gegenüber konventionellem Neubau.
- **5 wichtigste Bauteile:** Stahlstruktur Recyclinghalle Hagenholz; Betonplatten Kerenzerbergtunnel; Beton-Pilzstützen/Deckenelemente Schellinghalle Rümlang; Stahlträger/Trapezbleche Dach; Re-Use-Leitplanken/Fassadenelemente.
- **5 wichtigste Hürden:** Projekt noch nicht fertig; Resttragfähigkeitsnachweis; Schwertransport; Verfügbarkeit/Timing; Kostenquellenkonflikt.
- **5 wichtigste übertragbare Erkenntnisse:** Öffentliche Bauherren können Bauteilpools aktivieren; Wettbewerbe können Reuse erzwingen; Hallenversetzung ist starkes Direct Reuse; BIM-Kataloge helfen Beschaffung; Planungsfälle bis Fertigstellung niedrig halten.
- **5 offene Fragen:** Welche Mengen/Massen werden final eingebaut? Welche Prüfwerte/Resttragfähigkeiten wurden nachgewiesen? Welche Transport- und Lageremissionen entstehen? Wie werden Gewährleistung/Haftung geregelt? Welche CO₂-Bilanz ergibt sich nach Fertigstellung?

## Quellen und Links
- [S1] Zirkular: ERZ Juchareal — https://zirkular.net/de/projekt/erz-juchareal/
- [S2] Stadt Zürich: Neubau Recyclingzentrum Juch-Areal — https://www.stadt-zuerich.ch/de/planen-und-bauen/projekte-und-ausschreibungen/hochbauvorhaben/planung-ausfuehrung/recyclingzentrum-juch-areal.html
- [S3] Stadt Zürich: Neubau Recyclingzentrum Juch-Areal als Pionierprojekt der Kreislaufwirtschaft — https://www.stadt-zuerich.ch/de/aktuell/medienmitteilungen/2025/07/neubau-recyclingzentrum-juch-areal.html
- [S4] Stadt Zürich: Kreislauforientiertes Bauen mit wiederverwendeten Tragstrukturen aus Stahl und Beton, Teil 1 — https://www.stadt-zuerich.ch/de/aktuell/publikationen/2026/reuse-tragstrukturen-studie.html
- [S5] Cirkla: Recyclingzentrum Juch-Areal — https://www.cirkla.ch/de/le-reseau-du-reemploi/lannuaire/projets/recyclingzentrum-juch-areal/
- [S6] Perita: Recyclingzentrum Juch-Areal — https://www.perita.ch/de/projekt/recyclingzentrum-juch-areal/
- [S7] Fachbau: Neubau Recyclingzentrum Juch-Areal — https://www.fachbau.ch/de/intelligent-bauen/2025-07-02/neubau-recyclingzentrum-juch-areal/
- [S8] Studio Lɔkɔ: Recyclingzentrum Juch-Areal competition entry — https://www.studioloko.ch/en/projects/recyclingzentrum-juch-areal
- [S9] EK Energiekonzepte: Innovationsprojekt Recyclingzentrum Juch-Areal — https://www.energiekonzepte.ch/en/current/zirkularitaet-am-bau-innovationsprojekt-recyclingzentrum-juch-areal/
