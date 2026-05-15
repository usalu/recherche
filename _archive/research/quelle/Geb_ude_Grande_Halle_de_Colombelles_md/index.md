---
entity: "quelle"
id: "Geb_ude_Grande_Halle_de_Colombelles_md"
title: "Geb_ude_Grande_Halle_de_Colombelles_md"
build_status: "promoted_phase42"
source_filename: "Grande_Halle_de_Colombelles.md"
---

# Geb_ude_Grande_Halle_de_Colombelles_md

**Stand:** 2026-05-06  
**Arbeitsregel:** Bestandserhalt der Betonhalle wird separat markiert. Als Wiederverwendung zählen nur demontierte und neu eingebaute Bau-, Hüll-, Raum-, Technik- oder feste Konstruktionselemente.

## 1. EINORDNUNG

- **Entscheidung:** VERGLEICHSFALL
- **Bewertung:** ★★★☆☆
- **Begründung:** Sehr gut belegter französischer Reuse-Referenzfall mit eigenem „Lot 01 Réemploi“, CCTP-Variantenlogik und wiederverwendeten festen Bauteilen: Dämmung, Radiatoren, Sanitärobjekte, Türen/Brandschutztüren, Holzpfetten, Fliesen/Fayencen, Außenfenster/Schreinerei, teils Metallträger. Nicht fünf- oder viersternig, weil die Hauptstruktur der Halle überwiegend erhalten bleibt und die Reuse-Bauteile vor allem Ausbau, Hülle und Technik betreffen.
- **Vertrauensgrad:** belegt
- **Warnung Bestandserhalt:** ja — erhaltene Betonhalle / Betonstruktur nicht als Direct Reuse zählen.
- **Warnung Möbel/Dekoration:** ja — Bar-/Möbelbau aus Reuse nur als feste Einbauten vorsichtig werten; lose Möblierung nicht zählen.
- **Projektstatus:** gebaut

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Grande Halle de Colombelles / Le WIP | untersuchtes Projekt | [S1], [S2], [S3], [S4] | belegt | Tiers-lieu in ehemaliger SMN-Halle |
| Gebäude | ehemalige elektrische Werkstatt der Société Métallurgique de Normandie | Ausgangsbestand | [S2], [S4], [S6] | belegt | Industrieerbe / friche industrielle |
| Ort | Rue des Ateliers, 14460 Colombelles | Standort | [S2], [S4] | belegt | Nähe Caen |
| Projekt | Umwandlung in Tiers-lieu der Kreislaufwirtschaft | neue Nutzung | [S1], [S2], [S4] | belegt | Kultur, Coworking, Werkstätten, Events, Restaurant |
| People | Normandie Aménagement | Bauherr / Commanditaire | [S3], [S6] | belegt | SEM / öffentliche Auftraggeberrolle |
| People | Encore Heureux | Architekt | [S3], [S6] | belegt | zusammen mit Construire |
| People | Construire | Architekt | [S3], [S6] | belegt | mandataire in manchen Quellen |
| People | Le WIP | Betreiber und Inhaber Lot 01 Reuse | [S1], [S2] | belegt | Sourcing, Lagerung, Bereitstellung |
| People | Stéphanie Paly | Co-traitance Lot 1 | [S1] | belegt | Wiederverwendungsmission |
| People | Ligne B.E. | Tragwerksplanung | [S3], [S6] | belegt | Struktur |
| People | Albert & Co | Umwelt/HQE/technische Leitung | [S6] | belegt | Reuse-Lot-Konzeption / Carbon-Bilanz |
| Reuse-Strategie | Lot 01 „Réemploi“ | methodischer Kern | [S1], [S2], [S4] | belegt | eigenes Vergabelos |
| Methode | CCTP à variantes / „à trous“ | Beschaffungsinnovation | [S4] | belegt | erleichtert Reuse bei mehreren Gewerken |
| Bauteil | mineralische Dämmung / Steinwolle | wiederverwendet | [S2], [S3], [S5] | belegt | 430 m² oder 200 m² je Quelle; Differenz markieren |
| Bauteil | Radiatoren | wiederverwendet | [S1], [S2], [S3], [S5] | belegt | 49, 52 oder 59 je Quelle; Differenz |
| Bauteil | Sanitärobjekte | wiederverwendet | [S1], [S2], [S3] | belegt | WC, Urinale, Waschbecken |
| Bauteil | Türen / Brandschutztüren | wiederverwendet | [S1], [S2], [S3], [S5] | belegt | unterschiedliche Mengen je Quelle |
| Bauteil | Holzpfetten / Holzstücke | wiederverwendet | [S2], [S3], [S5] | belegt | Balkon / Treppe / Geländer je Quelle |
| Kennwert | 19 t Abfall vermieden und wiederverwendet | Umweltkennwert | [S2] | belegt | Quelle Ekopolis |
| Kennwert | Fläche ca. 3.700 m² / 3.080 m² / 3.000 m² | Maßstab | [S2], [S3], [S6], [S7] | teilweise | Quellen differieren |
| Hürde | Versicherung / assurabilité | technischer/rechtlicher Fokus | [S5] | belegt | FCRBE-Fall „Insurance and reuse“ |
| Software | unbekannt | keine belastbare Angabe | — | unbekannt | — |
| Norm | ERP / öffentlich zugängliches Gebäude | Gebäudetyp / Rechtsrahmen | [S4] | teilweise | keine konkreten Normnummern |
| Recht | öffentlicher Markt / public procurement | Reuse-Beschaffung | [S2], [S4] | belegt | CCTP, Varianten |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Reuse-Los / Lot réemploi | Klassische Entitäten erfassen nicht, dass Wiederverwendung als eigenes Bau-/Beschaffungslos organisiert wurde. | Lot 01 Réemploi | Prozessphase, Recht, Methode, Wirtschaft |
| CCTP-Variante / „CCTP à trous“ | Spezifische Ausschreibungstechnik für Reuse | Variantenpreise Basis/Reuse | Recht, Methode, Leistungsanforderung |
| Reuse-Werkstatt auf Baustelle | verbindet Logistik, Aufbereitung und Beschäftigung | Atelier réemploi auf dem Gelände | Logistik, Werkzeug, Aufbereitungsmethode |

## 3. FALLSTUDIE

- **Name:** Grande Halle de Colombelles / Le WIP
- **Ort:** Rue des Ateliers, 14460 Colombelles, Frankreich.
- **Gebäude:** ehemalige elektrische Werkstatt der Société Métallurgique de Normandie.
- **Projekt:** Sanierung / Umbau zu einem kreislauforientierten Kultur-, Arbeits- und Veranstaltungshaus.
- **Beteiligte People / Akteure:** Normandie Aménagement, Encore Heureux, Construire, Le WIP, Stéphanie Paly, Ligne B.E., T&E Ingénierie, Albert & Co, ECRH, Liliana Motta, ATEVE.
- **Architekt:** Encore Heureux + Construire.
- **Tragwerksplaner:** Ligne B.E.
- **Bauherr:** Normandie Aménagement.
- **Zeitraum:** Lieferung 2019; Le WIP nennt Lot-1-Mission 2018 und Abschluss September 2019.
- **Ursprüngliche Nutzung:** Industriehalle / elektrische Werkstatt der SMN.
- **Neue Nutzung:** Tiers-lieu: kollaborative Arbeitsräume, Werkstätten, Proben-/Veranstaltungsräume, Ausstellung, Café-Restaurant, Kultur- und Wirtschaftsnutzungen.
- **Fläche / Maßstab:** 3.700 m² Nutz-/Projektfläche bei Ekopolis/REMIX; Albert & Co nennt 3.080 m²; Kulturministerium nennt ca. 3.000 m² auf drei Ebenen.
- **Schutzstatus / Denkmalstatus:** Industriehistorisch relevant; formaler Denkmalstatus unbekannt.
- **Quellenlage:** sehr gut für Mengen, Prozess und Beschaffung; Detailprüfungen und Normen nur teilweise.

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ Bauteilwiederverwendung; Bauteil-/Produktwiederverwendung; adaptive reuse des Gebäudes.
- **Hauptniveau:** Gebäudetechnik, Sanitär, Innenausbau, Dämmung, Boden-/Wandbeläge, Hülle, begrenzt Holz-/Metallbauteile.
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die Betonsanierung und der Erhalt der Halle sind Bestandserhalt. Direct Reuse sind die aus anderen Rückbau-/Sanierungsbaustellen gesicherten und wieder eingebauten Materialien und Produkte.
- **Warum ist der Fall relevant?** Er gilt als früher, gut dokumentierter öffentlicher Reuse-Prozess mit eigenem Reuse-Los, Reuse-Werkstatt vor Ort und Beschaffungslogik, die für andere öffentliche Projekte übertragbar ist.

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Mineralwolle-Dämmung | Stein-/Mineralwolle | Rückbau-/Sanierungsbaustellen Region Caen | Dämmung | Dämmung | 430 m² nach Construction21/FCRBE; 200 m² nach WIP/Ekopolis | nein | nein | ja | nein | Identifizieren, sammeln, lagern, vorbereiten | unbekannt | Zustand sehr gut laut FCRBE | Wärmeschutz, Brandschutz, Feuchte | unbekannt | Menge differiert | [S1], [S2], [S3], [S5] | teilweise |
| Radiatoren | Guss/Stahl | regionale Rückbau-/Sanierungsbaustellen | Heizung | Heizung | 49 nach C21; 52 nach Ekopolis; 59 nach WIP | nein | nein | nein | ja | Reinigung, Hydraulik-Anschluss unbekannt | TGA-Anschluss | unbekannt | Dichtheit, Druck, Leistung | unbekannt | Prüfung / Kompatibilität | [S1], [S2], [S3] | teilweise |
| Waschbecken / Sanitär | Keramik/Metall | Rückbau | Sanitär | Sanitär | 20–30 Sanitärteile je Quelle | nein | nein | nein | ja | Reinigung, Aufbereitung | Sanitäranschluss | unbekannt | Hygiene, Dichtheit, Barrierefreiheit teils | unbekannt | Normgerechter Wiedereinbau | [S1], [S2], [S3], [S5] | teilweise |
| WC | Keramik | Rückbau | WC | WC | 11 oder 12; davon Quelle Ekopolis 7 PMR | nein | nein | nein | ja | Reinigung | Sanitäranschluss | unbekannt | Hygiene, Barrierefreiheit bei PMR | unbekannt | Zustand | [S2], [S3] | teilweise |
| Urinale | Keramik | Rückbau | Urinal | Urinal | 5 | nein | nein | nein | ja | Reinigung | Sanitäranschluss | unbekannt | Hygiene | unbekannt | Zustand | [S2], [S3] | teilweise |
| Türen massiv / Brandschutztüren | Holz, teils Brandschutz | Wohnungs-/Sanierungsbaustellen Region Caen | Tür | Innentür / WC-Tür / Brandschutztür | 10, 18, 33 oder 50 je Quelle; mind. teils 2 Brandschutztüren | nein | ja | nein | nein | Maßanpassung / Sonderzargen | Zargen auf Maß laut C21 | unbekannt | Gebrauchstauglichkeit, Brandschutz bei Feuerschutztüren | unbekannt | Brandschutznachweis | [S1], [S2], [S3], [S5] | teilweise |
| Außenfenster / Außenschreinerei | Aluminium/Glas nach C21 | Büroabbruch nahe Grande Halle | Fenster | Außenfenster | 1 eingebaut; 21 identifiziert, aber vor Reuse gestohlen | nein | nein | ja | nein | unbekannt | unbekannt | unbekannt | Witterung, Luftdichtheit, U-Wert | unbekannt | Diebstahl / Lagerung | [S2], [S3] | teilweise |
| Holzpfetten / Holzstücke | Holz | Rückbau | Pfette / Holzbauteil | Balkon-/Geländer-/Treppenbauteil | 21 Pfetten/63 ml nach C21; FCRBE nennt 21 Geländerstücke + 45 Treppenstücke | teils | ja | nein | nein | Zuschnitt / Umnutzung | unbekannt | unbekannt | Trag-/Nutzungslasten, Dauerhaftigkeit | unbekannt | Nachweis | [S3], [S5] | teilweise |
| Fliesen / Fayence | Keramik | Rückbau/Bestände | Wand-/Bodenbelag | Belag | 190–200 m² | nein | ja | nein | nein | Sortierung, Reinigung, Verlegung | Mörtel/Kleber unbekannt | unbekannt | Rutsch, Haftung, Feuchte | unbekannt | heterogene Chargen | [S1], [S3] | teilweise |
| Metallträger / Poutres métalliques | Stahl | unbekannt | Trag-/Metallbauteil | unbekannt | „des poutres métalliques“ | unbekannt | unbekannt | unbekannt | nein | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | zu wenig Detail | [S1] | ja |
| Bestand-Betonstruktur | Beton/Stahlbeton | in situ | Tragwerk/Hülle | Tragwerk/Hülle | Gebäudehauptstruktur | ja | ja | ja | nein | Reparatur, Ferroscan, Passivierung korrodierter Bewehrung | Bestand | Ferroscan belegt | Tragfähigkeit, Dauerhaftigkeit | unbekannt | zählt als Sanierung, nicht Reuse | [S4] | teilweise |

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Halle prüfen, Beton reparieren | Architekten, Ligne B.E., Unternehmen | Ferroscan, Sondagen, Piquetage | Ferroscan | — | Reparatur / Passivierung | Ferroscan | in situ | Betonschäden | schwere Betonsanierung | [S4] |
| Bauteilinventar | Gisements in Region identifizieren | Le WIP, Stéphanie Paly | Lot 01 Réemploi | unbekannt | selektiver Rückbau bei Spendern | Charakterisierung, Sammlung | unbekannt | regionale Baustellen | Verfügbarkeit | eigene Reuse-Mission | [S1], [S2] |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Datenlücke | prüfen | — |
| Rückbau | Materialien aus Nachbarbaustellen sichern | Le WIP / Partner | selektive Demontage | unbekannt | selektiv | unbekannt | unbekannt | aus CU Caen la Mer / Region | Timing | Koordination durch Lot 01 | [S1], [S2], [S3] |
| Ausbau | Radiatoren, Türen, Sanitär, Dämmung etc. ausbauen | unbekannt | sorgfältiger Ausbau | unbekannt | selektiv | Reinigung / Sortierung | unbekannt | unbekannt | Beschädigung | unbekannt | [S1], [S2] |
| Transport | zur Grande Halle | Le WIP / Partner | regionale Logistik | unbekannt | — | — | unbekannt | regionale Transporte | Transport-/Lagerbedarf | Baustellennahe Reuse-Werkstatt | [S1] |
| Lagerung | Zwischenlagern und sichern | Le WIP | Atelier auf Baustelle | Reuse-Werkstatt | — | Vorbereitung | unbekannt | auf dem Gelände | Diebstahl: 21 Fenster wurden gestohlen | Sicherung wichtig | [S1], [S2] |
| Aufbereitung | Materialien vorbereiten | Le WIP, ATIPIC, TMI | Werkstattarbeit | Atelier réemploi | — | reinigen, sortieren, vorbereiten | unbekannt | vor Ort | Arbeitszeit | lokale ESS/Arbeitsplätze | [S1], [S2] |
| Planung | Reuse in CCTP integrieren | Encore Heureux, Construire, Albert & Co, Le WIP | Lot 01 + Varianten | CCTP „à trous“ | — | — | technische Koordination | gewerkeübergreifend | klassische Ausschreibung passt schlecht | Reuse-Los und Variantenpreise | [S2], [S4] |
| Genehmigung | ERP / öffentliches Gebäude | Projektteam | unbekannt | unbekannt | — | — | unbekannt | — | Reuse in ERP-Kontext | unbekannt | [S4] |
| Wiedereinbau | Bauteile durch Fachlose einbauen | Unternehmen der Gewerke, Le WIP als Lieferant | Le WIP liefert, Fachunternehmen montieren | unbekannt | — | vorbereitet | unbekannt | Lieferlogistik auf Baustelle | Schnittstellen | klare Losgrenzen | [S2] |
| Monitoring | Rückmeldungen dokumentieren | Le WIP, FCRBE, Ekopolis | Retour d’expérience | Dokumente / Besichtigungen | — | — | unbekannt | — | Wissenstransfer | Dokumentation | [S1], [S2], [S5] |

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Bestandshalle Beton, neu Holzstruktur; wiederverwendete Holzpfetten/Geländer-/Treppenteile nur partiell | Tragfähigkeit, Dauerhaftigkeit | unbekannt | Ferroscan für Bestandsbeton | Reuse nicht Haupttragwerk | Punktuelle Integration | [S3], [S4] |
| Lastabtragung | Holzpfetten als Balkon-/Nave-Bauteile belegt, Details unklar | Nutzlasten | unbekannt | unbekannt | Nachweis alter Bauteile | unbekannt | [S3], [S5] |
| Verbindung | Sonderzargen bei Türen, Holz-/Geländerbauteile unbekannt | sichere Anschlüsse | unbekannt | unbekannt | Maßabweichungen | Maßfertigung / Werkstatt | [S3] |
| Brandschutz | Brandschutztüren re-used, Gebäude ERP | Feuerwiderstand, Fluchtwege | ERP-Kontext, keine Normnummer | unbekannt | Nachweis alter Feuerschutztüren | unbekannt | [S1], [S4], [S5] |
| Schallschutz | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Feuchte | Mineralwolle, Fliesen, Sanitär relevant | Feuchteschutz | unbekannt | Zustand laut FCRBE sehr gut für Dämmung | Lagerfeuchte / Hygiene | unbekannt | [S5] |
| Wärmeschutz | 430 m² Mineralwolle laut C21/FCRBE | Dämmleistung | unbekannt | Zustand / Qualität | fehlende Produktdaten | unbekannt | [S3], [S5] |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Luftdichtheit | eine Außenschreinerei / Fenster | Luftdichtheit / U-Wert | unbekannt | unbekannt | alte Fensterperformance | unbekannt | [S3] |
| TGA-Integration | Radiatoren reused; Biomasseheizung/Heizungssystem im Projekt | Dichtheit, Heizleistung, Hydraulik | unbekannt | unbekannt | Altgeräte in neues Netz | unbekannt | [S1], [S3], [S4] |
| Barrierefreiheit | PMR-WC laut Ekopolis | Zugänglichkeit | unbekannt | unbekannt | gebrauchte Sanitärobjekte | Auswahl geeigneter Objekte | [S2] |
| Dauerhaftigkeit | Türen, Fliesen, Radiatoren, Dämmung | Zustandsprüfung | unbekannt | visuell / unbekannt | heterogene Gisements | Charakterisierung durch Lot 01 | [S2], [S5] |
| Wartung | Radiatoren/Sanitär | Ersatzteile, Wartung | unbekannt | unbekannt | alte Produkte | unbekannt | [S1] |
| Zulassung | Reuse in öffentlichem ERP | Nachweisfähigkeit | öffentliches Vergaberecht, ERP | unbekannt | Versicherbarkeit | FCRBE-Fall zu Insurance | [S4], [S5] |
| Haftung | Le WIP liefert, Gewerke montieren | Verantwortungsgrenzen | unbekannt | unbekannt | Schnittstellen Lieferant/Montage | Lot 01 + Varianten | [S2], [S4] |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Projektfläche | 3.700 | m² | unbekannt | Surface utile / Projektfläche | [S2], [S3] | belegt |
| Projektfläche alternative | 3.080 | m² | unbekannt | Surface bei Albert & Co | [S6] | teilweise, abweichend |
| Baukosten | 5,8 | Mio. € | unbekannt | Gebäude gesamt | [S3] | belegt |
| Baukosten alternative | 5,5 | Mio. € HT | unbekannt | travaux | [S6] | belegt, abweichende Kostenbasis |
| Studienkosten | 320.000 | € | unbekannt | Studien | [S3] | belegt |
| Abfall vermieden / wiederverwendet | 19 | t | unbekannt | Reuse-Lot | [S2] | belegt |
| Dämmung | 430 / 200 | m² | unbekannt | reused insulation | [S1], [S2], [S3], [S5] | teilweise; Quellen differieren |
| Radiatoren | 49 / 52 / 59 | Stück | unbekannt | Guss + Stahl | [S1], [S2], [S3], [S5] | teilweise; Quellen differieren |
| Türen | 10 / 18 / 33 / 50 | Stück | unbekannt | Türen inkl. Brandschutztüren | [S1], [S2], [S3], [S5] | teilweise; Quellen differieren |
| Sanitärobjekte | 20 / 30 | Stück | unbekannt | WC, Urinale, Waschbecken | [S1], [S2], [S5] | teilweise |
| Fliesen/Fayence | 190 / 200 | m² | unbekannt | Beläge | [S1], [S3] | teilweise |
| Holzpfetten | 21 / 63 | Stück / ml | unbekannt | Balkon / große Nave | [S3] | belegt |
| Koordinations-/Valorisationszeit | 2.790 | Stunden | unbekannt | Reuse-Koordination | [S2] | belegt |
| Arbeitsplätze | 3 | dauerhaft geschaffen | unbekannt | Folge Le WIP / Reuse-Aktion | [S2] | belegt |
| CO₂-Einsparung | unbekannt | — | — | — | [S2] | Ekopolis nennt „580 m³ CO2“, Einheit fachlich unklar; nicht als t CO₂ übernommen |
| Wasserersparnis | 120.529 | Liter | unbekannt | Reuse-Effekt | [S2] | belegt nach Quelle |

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Reuse in öffentlichem Bauvertrag | rechtlich/wirtschaftlich | übliche CCTP passen nicht zu verfügbaren Gisements | Unsicherheit bei Preisen und Gewerkeschnittstellen | Recht, Methode, Wirtschaft | Lot 01 + Varianten-CCTP | Beschaffung muss Reuse als Prozess abbilden | [S2], [S4] |
| Versicherbarkeit | rechtlich/technisch | gebrauchte Produkte ohne Neuproduktnachweise | Risiko bei Einbau | Prüfung, Norm, Haftung | FCRBE-Auswertung; Losgrenzen | früh Versicherungs-/Kontrollfragen klären | [S5] |
| Lagerung / Diebstahl | logistisch | 21 Fenster identifiziert, vor Reuse gestohlen | Verlust geeigneter Bauteile | Logistik, Bauteil | sichere Lagerung nötig | Lagerung ist kritische Infrastruktur | [S2] |
| Mengenabweichungen / Quellenheterogenität | technisch/logistisch | verschiedene Gisements und Dokumentationen | unsichere Inventarisierung | Kennwert, Bauteil | Quellen transparent nebeneinanderstellen | keine Scheingenauigkeit | [S1], [S2], [S3], [S5] |
| Arbeitsintensive Aufbereitung | wirtschaftlich/sozial | Sammlung, Sortierung, Reinigung, Anpassung | hoher Stundenbedarf | Wirtschaft, Aufbereitung | Reuse-Werkstatt, lokale Beschäftigung | Reuse schafft Arbeit, braucht Budget/Zeit | [S1], [S2] |
| Bestandserhalt vs. Reuse | methodisch | Sanierung einer großen Halle | Überschätzung des Reuse-Anteils | Fallstudie, Kennwert | klare Abgrenzung | Bestandserhalt separat bewerten | [S4] |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** öffentlicher Bauauftrag mit eigenem Lot 01 „Réemploi“ und Reuse-Varianten in weiteren Losen.
- **Bauteilbörse / Quelle:** keine klassische Börse; Le WIP identifizierte, sammelte, lagerte und bereitete Materialien aus regionalen Demontage-/Sanierungs-/Abbruchbaustellen auf.
- **Kostenwirkung:** Gesamtkosten belegt; spezifische Mehr-/Minderkosten Reuse unbekannt.
- **Zeitwirkung:** 2.790 Stunden Koordination/Valorisation nach Ekopolis; Projekt insgesamt langlaufend.
- **Versicherung / Haftung:** wichtiges Thema; FCRBE behandelt den Fall unter „Insurance and reuse“, Details im Kurzbefund begrenzt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** hoch; 2.790 Stunden Koordination/Valorisation belegt.
- **Lagerung:** Reuse-Werkstatt vor Ort; Diebstahl eines identifizierten Fenster-Gisements belegt.
- **Marktbarrieren:** fehlende Routinen, Nachweise, Lagerflächen, klare Zuständigkeiten, Versicherbarkeit.

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** sichtbar in Türen, Sanitärobjekten, Radiatoren, Belägen, teils Holzbauteilen.
- **räumliche Transformation:** Industriehalle wird offenes kulturelles und wirtschaftliches Gemeingut / Tiers-lieu.
- **Atmosphäre / Ausdruck:** Reuse unterstützt Werkstatt- und Industriecharakter.
- **Umgang mit Spuren:** belegt als „rien ne se perd, tout se transforme“-Narrativ; Detailbewertung unbekannt.
- **sozialer Wert:** hoch; Le WIP verknüpft Reuse mit ESS, lokalen Arbeitsplätzen und öffentlicher Aneignung.
- **Denkmal- oder Bestandswert:** industrielle Erinnerung an SMN; formaler Schutz unbekannt.
- **Kritik / Grenzen:** Der Hauptscore darf nicht auf der erhaltenen Betonhalle beruhen; Mengenangaben variieren zwischen Quellen.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** Schadstoffdiagnostik, konkrete Normen, Prüfberichte für Radiatoren/Sanitär/Türen, Haftungsdetails, genaue vollständige Inventarliste.
- **Neue Entitäten:** Reuse-Los, CCTP-Variante, Reuse-Werkstatt, Versicherbarkeit.
- **Fehlende Daten:** belastbare einheitliche Mengenliste, CO₂ in üblichen Einheiten, Kostenmehr-/minderung, Transportdistanzen, technische Prüfprotokolle.
- **Zu prüfende Quellen:** vollständiges „Retour d’expérience Lot 01 Réemploi“, FCRBE-PDF, Ausschreibungsunterlagen, Kontrollbüroberichte.

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja, aber als Vergleichsfall / mittlere Priorität.
- **5 wichtigste Fakten:**
  1. Eigenes Lot 01 Réemploi wurde eingerichtet.
  2. Reuse-CCTP mit Variantenlogik wurde entwickelt.
  3. 19 t Abfall wurden laut Ekopolis vermieden und wiederverwendet.
  4. Reuse umfasst Dämmung, Radiatoren, Sanitär, Türen, Beläge und Holzbauteile.
  5. Die Halle ist ein starkes Prozess- und Beschaffungsbeispiel, nicht primär Tragwerksreuse.
- **5 wichtigste Bauteile:**
  1. Mineralwolle-Dämmung.
  2. Radiatoren.
  3. Sanitärobjekte.
  4. Türen / Brandschutztüren.
  5. Holzpfetten / Holzbauteile.
- **5 wichtigste Hürden:**
  1. Vergabelogik.
  2. Versicherbarkeit.
  3. Lagerung / Diebstahl.
  4. heterogene Mengen und Nachweise.
  5. hoher Koordinationsaufwand.
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Ein eigenes Reuse-Los kann Schnittstellen klären.
  2. Reuse braucht eine Logistik- und Aufbereitungsstelle.
  3. Öffentliche CCTP können Reuse-Varianten abbilden.
  4. Soziale Beschäftigung kann Reuse ökonomisch und lokal verankern.
  5. Mengen müssen transparent mit Quellenabweichungen dokumentiert werden.
- **5 offene Fragen:**
  1. Welche Menge ist die endgültige geprüfte Inventarzahl je Bauteil?
  2. Wie wurden Radiatoren hydraulisch geprüft?
  3. Welche Nachweise gab es für Brandschutztüren?
  4. Wie wurden Versicherungsrisiken vertraglich verteilt?
  5. Gibt es eine belastbare CO₂-Bilanz in kg/t CO₂e?

## Quellen und Links

- [S1] Le WIP — „Le réemploi de matériaux“: https://www.le-wip.com/le-reemploi-de-materiaux/
- [S2] Ekopolis — „Grande halle de Colombelles“: https://www.ekopolis.fr/operations-batiment/grande-halle-de-colombelles
- [S3] Construction21 — „La Grande Halle de Colombelles“: https://www.construction21.org/france/case-studies/h/la-grande-halle-de-colombelles.html
- [S4] Encore Heureux — „La Grande Halle“: https://encoreheureux.org/fr/projets/grande-halle
- [S5] FCRBE / Interreg NWE — „Insurance and reuse – The Grande Halle de Colombelles“: https://vb.nweurope.eu/media/21155/fcrbe_cashallecolombelle_final18oct2023_en.pdf
- [S6] Albert & Co — „La Grande Halle, à Caen“: https://albert-and-co.fr/2023/05/28/centre-culturel-grande-halle-caen/
- [S7] Ministère de la Culture — „Micro-Folie à la Grande Halle de Colombelles“: https://www.culture.gouv.fr/regions/drac-normandie/actualites/Micro-Folie-a-la-Grande-Halle-de-Colombelles
- [S8] REMIX — „Grande halle“: https://www.remixremix.fr/portfolio/grande-halle/
