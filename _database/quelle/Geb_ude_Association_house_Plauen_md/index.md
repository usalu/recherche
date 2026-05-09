---
entity: "quelle"
id: "Geb_ude_Association_house_Plauen_md"
title: "Geb_ude_Association_house_Plauen_md"
build_status: "promoted_phase42"
source_filename: "Association_house_Plauen.md"
---

# Geb_ude_Association_house_Plauen_md

**Arbeitsstand:** 2026-05-07  
**Sprache:** Deutsch  
**Regel:** Es werden nur tatsächlich wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente gezählt. Lose Möbel, Dekoration, reine DfD-Strategien und bloßer Bestandserhalt zählen nicht.

## 1. EINORDNUNG

- **Entscheidung:** HAUPTFALL
- **Bewertung:** ★★★★☆
- **Begründung:** Der Fall ist ein gebautes Sport-/Vereinshaus mit tragwerksrelevanter Wiederverwendung von Betonfertigteilen. In der wissenschaftlichen Fallstudienübersicht wird die Wiederverwendung von 145 Decken-/Bodenplatten, 19 Außenwandelementen, 14 Innenwandelementen und 11 Kellerwandelementen aus dem Fertigteilsystem IW73/6 beschrieben. Damit handelt es sich nicht um Möbel, Dekoration oder bloßen Bestandserhalt, sondern um ex-situ Bauteilwiederverwendung in einem neuen Gebäude.
- **Vertrauensgrad:** teilweise belegt
- **Warnung Bestandserhalt:** nein
- **Warnung Möbel/Dekoration:** nein
- **Projektstatus:** gebaut

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Association house, Plauen / Plauen association house | Untersuchter Reuse-Fall | [S0], [S1] | teilweise belegt | In Quellen auf Englisch geführt. Deutsche genaue Projektbezeichnung unbekannt. |
| Gebäude | Sport-/Vereinshaus | Empfängergebäude | [S1] | teilweise belegt | „sport-association house“; spezifischer Verein unbekannt. |
| Ort | Plauen, Deutschland | Standort Empfängerprojekt | [S1] | belegt | Distanz zum Spendergebäude ca. 7 km laut PRECS-Datenbank. |
| Projekt | Neubau mit gebrauchten Betonfertigteilen | Reuse-Projekt | [S1] | belegt | Start/Jahr der Fallstudie: 2007. |
| Bauteil | 145 Decken-/Bodenplatten, 19 Außenwandelemente, 14 Innenwände, 11 Kellerwände | Direkt wiederverwendete tragende/raum- und hüllenbildende Bauteile | [S1], [S3] | belegt | Summe: 189 dokumentierte Fertigteile. |
| Material | Stahlbetonfertigteile / precast concrete | Hauptmaterial | [S1] | belegt | System IW73/6. |
| Tragwerkssystem | Plattenbau-/Wandbau-System mit Fertigteilplatten | Reuse-Tragwerk | [S1] | teilweise belegt | Exakte neue Lastabtragung nicht veröffentlicht. |
| Reuse-Strategie | ex-situ Bauteilwiederverwendung | Bauteile aus Spendergebäude in neues Gebäude | [S1] | belegt | Kein Recycling zu Zuschlagstoff. |
| Abbruchmethode | selektiver Rückbau / Demontage | Erforderlich für Fertigteilgewinnung | [S1], [S6] | teilweise belegt | Projektspezifische Methode unbekannt; allgemeine Methode für solche Fälle belegt. |
| Aufbereitungsmethode | unbekannt | Vor Wiedereinbau | unbekannt | unklar | Keine projektbezogenen Angaben zu Reinigung, Zuschnitt, Reparatur. |
| Prüfung | unbekannt | Tragfähigkeit/Schadstoffe/Geometrie | unbekannt | unklar | Keine projektspezifischen Prüfdaten öffentlich gefunden. |
| Logistik | ca. 7 km Transportdistanz | Spender- zu Empfängerstandort | [S1] | belegt | Sonstige Lagerung unbekannt. |
| Hürde | Gewährleistung, Prüfung, Logistik, Toleranzen | Typische Hürden bei Fertigteil-Reuse | [S1], [S4], [S5] | teilweise belegt | Allgemeine, nicht vollständig projektspezifische Einordnung. |
| Kennwert | 189 Fertigteile; ca. 7 km Distanz; 2007; gebaut | Dokumentierte Fallwerte | [S1], [S3] | belegt | Fläche, CO₂, Kosten unbekannt. |
| People | Angelika Mettke / Heyn et al. / Dechantsreiter et al. / Fischer et al. | Literatur- und Forschungsbezug | [S1] | teilweise belegt | Beteiligung am konkreten Projekt nicht vollständig belegbar; in Referenzen genannt. |
| Norm | Eurocode 2, DIN EN 206-1, DIN 1045-2 | Allgemeiner heutiger Bewertungsrahmen für Stahlbetonbauteile | [S4] | teilweise belegt | Nicht als projektspezifische Genehmigungsgrundlage belegt. |
| Recht | unbekannt | Genehmigung/Haftung | unbekannt | unklar | Keine Projektakten gefunden. |
| Wirtschaft | unbekannt | Kostenwirkung | unbekannt | unklar | Keine Kostenwerte gefunden. |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Spendergebäude | Reuse-Fälle brauchen die Trennung zwischen Herkunfts- und Empfängergebäude | IW73/6-Wohnungsbau als Herkunft der Platten | verknüpft Gebäude, Bauteil, Logistik, Schadstoff, Prüfung |
| Empfängergebäude | Erlaubt klare Zuordnung der neuen Nutzung und Anforderungen | Sport-/Vereinshaus Plauen | verknüpft Fallstudie, Projekt, Leistungsanforderung |
| Fertigteilsystem | Plattenbautyp bestimmt Geometrie, Verbindung und Wiederverwendbarkeit | IW73/6 | verknüpft Bauteil, Tragwerkssystem, Verbindung, Norm |

## 3. FALLSTUDIE

- **Name:** Association house, Plauen / Plauen association house
- **Ort:** Plauen, Deutschland
- **Gebäude:** Sport-/Vereinshaus
- **Projekt:** Neubau eines Sport-/Vereinshauses aus wiederverwendeten Stahlbetonfertigteilen
- **Beteiligte People / Akteure:** unbekannt; in der Sekundärliteratur werden u. a. Dechantsreiter et al., Fischer et al., Heyn et al. und Mettke als Quellen genannt
- **Architekt:** unbekannt
- **Tragwerksplaner:** unbekannt
- **Bauherr:** unbekannt
- **Zeitraum:** 2007 laut PRECS-Fallstudienliste
- **Ursprüngliche Nutzung:** Spendergebäude: industrieller Wohnungsbau / mass housing, Fertigteilsystem IW73/6
- **Neue Nutzung:** Sport-/Vereinshaus
- **Fläche / Maßstab:** Fläche unbekannt; dokumentiert sind 189 wiederverwendete Fertigteile
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** Sekundärwissenschaftlich gut als Fall identifizierbar; projektspezifische Primärquellen, Pläne und Genehmigungsunterlagen nicht gefunden

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; Materialwiederverwendung nur im Sinne von Bauteilen, nicht als Recycling
- **Hauptniveau:** Tragwerk / räumlicher Ausbau / Gebäudehülle
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die Fertigteile wurden aus einem anderen Gebäude entnommen und in einem neuen Gebäude wieder montiert. Sie wurden nicht nur im Bestand belassen und nicht zu Recyclingzuschlag zerkleinert.
- **Warum ist der Fall relevant?** Der Fall zeigt, dass DDR-/ostdeutsche Wohnungsbau-Fertigteile nicht nur für Wohnhäuser, sondern auch für Vereins-/Sportbauten wiederverwendet werden konnten.

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Decken-/Bodenplatten | Stahlbetonfertigteil | IW73/6-Wohnungsbau | Decke/Boden | Decke/Boden oder tragendes Bauteil im Vereinshaus | 145 | ja | ja | nein | nein | unbekannt | unbekannt | unbekannt | Tragfähigkeit, Gebrauchstauglichkeit, Brandschutz | projektspezifisch unbekannt | Geometrie, Nachweis, Anschlüsse | [S1], [S3] | Detailabmessungen, Bewehrung, Prüfwerte |
| Außenwandelemente | Stahlbetonfertigteil | IW73/6-Wohnungsbau | Außenwand | Wand/Hülle | 19 | wahrscheinlich ja | ja | ja | nein | unbekannt | unbekannt | unbekannt | Tragfähigkeit, Wärmeschutz, Feuchte, Brandschutz | unbekannt | Hülle/Anschluss/Wärmebrücken | [S1] | Aufbau, Dämmung |
| Innenwandelemente | Stahlbetonfertigteil | IW73/6-Wohnungsbau | Innenwand | Innen-/Tragwand | 14 | wahrscheinlich ja | ja | nein | nein | unbekannt | unbekannt | unbekannt | Tragfähigkeit, Schallschutz, Brandschutz | unbekannt | Grundrissbindung | [S1] | Bewehrung/Lasten |
| Kellerwandelemente | Stahlbetonfertigteil | IW73/6-Wohnungsbau | Kellerwand | Wand/Sockel/Kellerbereich | 11 | wahrscheinlich ja | ja | teilweise | nein | unbekannt | unbekannt | unbekannt | Feuchte, Druck, Dauerhaftigkeit | unbekannt | Feuchteschutz | [S1] | genaue Lage |
| Träger | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | nein | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle | ja |
| Stützen | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | nein | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle | ja |
| Fenster/Türen/Dach/Treppen/Geländer/TGA/Dämmung/Sanitär/Beleuchtung/feste Einbauten | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle | ja |

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Auswahl geeigneter IW73/6-Fertigteile | unbekannt | Bauteilidentifikation | unbekannt | selektiver Rückbau erforderlich | unbekannt | unbekannt | Spendergebäude ca. 7 km entfernt | passende Geometrien finden | Nutzung standardisierter Platten | [S1] |
| Bauteilinventar | Mengen dokumentiert | unbekannt | Bauteilliste | unbekannt | unbekannt | unbekannt | unbekannt | 189 Bauteile | Datenverfügbarkeit | wissenschaftliche Falllistung | [S1], [S3] |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | mögliche Schadstoffe in Plattenbau-Fugen/Dämmungen | unbekannt | [S5] allgemein |
| Rückbau/Ausbau | schonende Demontage statt Zerkleinerung | unbekannt | selektive Demontage | Kran/Schneidtechnik unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Beschädigungsrisiko | unbekannt | [S1], [S6] allgemein |
| Transport | Transport zum Neubauort | unbekannt | Tieflader wahrscheinlich, aber nicht belegt | unbekannt | unbekannt | unbekannt | unbekannt | ca. 7 km | Kosten/Koordination | kurze Distanz | [S1] |
| Lagerung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Lagerflächen | unbekannt | keine Quelle |
| Aufbereitung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Toleranzen/Anpassung | unbekannt | keine Quelle |
| Planung | Entwurf um vorhandene Fertigteile | unbekannt | Bauteilgerechte Planung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | eingeschränkte Entwurfsfreiheit | Standardraster nutzen | [S1] allgemein |
| Genehmigung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Nachweis/Gewährleistung | unbekannt | [S4], [S5] allgemein |
| Wiedereinbau | Remontage im Sport-/Vereinshaus | unbekannt | Montage von Betonfertigteilen | Kran vermutlich, aber nicht belegt | unbekannt | unbekannt | unbekannt | Neubau Plauen | Anschlüsse | unbekannt | [S1] |
| Monitoring | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Langzeitdaten fehlen | unbekannt | keine Quelle |

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Wiederverwendete IW73/6-Fertigteilplatten | Tragfähigkeit/Gebrauchstauglichkeit | projektspezifisch unbekannt | unbekannt | Anschluss- und Lastnachweise | unbekannt | [S1] |
| Lastabtragung | Platten übernehmen voraussichtlich tragende Wand-/Deckaufgaben | Standsicherheit | unbekannt | unbekannt | Lastumlagerung im neuen Gebäude | unbekannt | [S1] |
| Verbindung | unbekannt | kraftschlüssige Montage | unbekannt | unbekannt | alte Verbindungspunkte/Toleranzen | unbekannt | keine Quelle |
| Brandschutz | unbekannt | Feuerwiderstand nach Nutzung/Gebäudeklasse | unbekannt; heutige WBS70-Diskussion nennt F30/F60/F90-Probleme | unbekannt | Betondeckung/Feuerwiderstand | unbekannt | [S5] allgemein |
| Schallschutz | unbekannt | nutzungsabhängig | unbekannt | unbekannt | alte Platten/Anschlüsse | unbekannt | keine Quelle |
| Feuchte | Außen-/Kellerwände betroffen | Feuchte- und Dauerhaftigkeitsschutz | unbekannt | unbekannt | alte Bauteile in neuer Hülle | unbekannt | keine Quelle |
| Wärmeschutz | Außenwände betroffen | Dämmstandard 2007 | unbekannt | unbekannt | Wärmebrücken/alte Wandaufbauten | unbekannt | keine Quelle |
| TGA-Integration | unbekannt | Leitungsführung | unbekannt | unbekannt | Öffnungen/Durchbrüche | unbekannt | keine Quelle |
| Barrierefreiheit | unbekannt | nutzungsabhängig | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle |
| Zulassung/Haftung | nicht öffentlich dokumentiert | Nachweis wie neues Tragwerk | allgemeine heutige Einordnung: Eurocode 2, DIN EN 206-1, DIN 1045-2 | unbekannt | Rechts-/Gewährleistungsunsicherheit | unbekannt | [S4] allgemein |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| wiederverwendete Fertigteile gesamt | 189 | Stück | PRECS-Fallstudienliste | Empfängergebäude | [S1], [S3] | belegt |
| Decken-/Bodenplatten | 145 | Stück | PRECS-Fallstudienliste | Bauteile | [S1] | belegt |
| Außenwände | 19 | Stück | PRECS-Fallstudienliste | Bauteile | [S1] | belegt |
| Innenwände | 14 | Stück | PRECS-Fallstudienliste | Bauteile | [S1] | belegt |
| Kellerwände | 11 | Stück | PRECS-Fallstudienliste | Bauteile | [S1] | belegt |
| Transportdistanz | ca. 7 | km | PRECS-Fallstudienliste | Spender- zu Empfängerstandort | [S1] | belegt |
| Jahr/Fallstudienstart | 2007 | Jahr | PRECS-Fallstudienliste | Projekt | [S1] | belegt |
| Fläche | unbekannt | m² | unbekannt | unbekannt | keine Quelle | unklar |
| CO₂-Einsparung | unbekannt | kg CO₂e | unbekannt | unbekannt | keine Quelle | unklar |
| Kosten | unbekannt | EUR | unbekannt | unbekannt | keine Quelle | unklar |
| U-Wert/Energiebedarf | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle | unklar |

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Fehlende Primärdaten | technisch/rechtlich | wenig veröffentlichte Projektunterlagen | unsichere Detailbewertung | Dokument, Prüfung, Norm | Archiv-/Planrecherche nötig | Reuse-Fälle brauchen offene Bauteildokumentation | eigene Bewertung, [S1] |
| Bauteilgeometrie/Raster | gestalterisch/technisch | vorhandene IW73/6-Formate | Entwurf wird durch Bestandsteile begrenzt | Bauteil, Tragwerkssystem | Entwurf an Raster anpassen | Früh Bauteilbestand inventarisieren | [S1] allgemein |
| Nachweisfähigkeit | rechtlich/technisch | gebrauchte tragende Bauteile | Genehmigung/Haftung komplex | Prüfung, Norm, Recht | Material- und Tragfähigkeitsprüfung | Reuse braucht Prüfpfad | [S4], [S5] |
| Anschlüsse/Toleranzen | technisch | Demontage und Remontage | Montage- und Tragwerksrisiken | Verbindung, Werkzeug | robuste Anschlussdetails | Anschlussplanung ist Kernaufgabe | [S1] allgemein |
| Logistik | logistisch/wirtschaftlich | schweres Bauteil, kurze Zeitfenster | Kostenrisiko | Logistik, Wirtschaft | kurze Distanz hilft | lokale Materialkreisläufe bevorzugen | [S1] |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** unbekannt; wahrscheinlich direkte Projektbeschaffung aus Rückbau, aber nicht belegt
- **Bauteilbörse / Quelle:** keine Bauteilbörse belegt
- **Kostenwirkung:** unbekannt
- **Zeitwirkung:** unbekannt
- **Versicherung / Haftung:** unbekannt
- **Gewährleistung:** unbekannt
- **Arbeitsaufwand:** unbekannt; bei Fertigteilreuse allgemein erhöht durch Auswahl, Prüfung, Logistik und Anschlussplanung
- **Lagerung:** unbekannt
- **Marktbarrieren:** fehlende Regelprozesse, Gewährleistung, Prüfaufwand, Logistik, Datenmangel

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** unbekannt
- **räumliche Transformation:** Wohnungsbau-Fertigteile werden in ein Vereins-/Sportgebäude übertragen
- **Atmosphäre / Ausdruck:** unbekannt
- **Umgang mit Spuren:** unbekannt
- **sozialer Wert:** Vereins-/Sportnutzung deutet öffentlichen oder gemeinschaftlichen Nutzen an; Details unbekannt
- **Denkmal- oder Bestandswert:** unbekannt
- **Kritik / Grenzen:** Datenlage schwach; kaum öffentlich sichtbare technische Dokumentation

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** Architekt, Tragwerksplaner, Bauherr, Schadstoff, Software, Werkzeug, detaillierte Verbindung, konkrete Norm-/Genehmigungsnachweise, Kosten, CO₂, Monitoring.
- **Welche neuen Entitäten wären sinnvoll?** Spendergebäude, Empfängergebäude, Fertigteilsystem, Bauteilzustand, Reuse-Prüfpfad.
- **Welche Daten fehlen?** Pläne, Fotos, Bauteilabmessungen, Tragwerksnachweise, Prüfberichte, Schadstoffgutachten, Kosten- und CO₂-Bilanzen.
- **Welche Quellen müssten geprüft werden?** Mettke 2008/2010, Heyn et al. 2008b, Dechantsreiter et al. 2015, lokale Bauakten Plauen, Vereins-/Sportstättenunterlagen.

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja
- **5 wichtigste Fakten:**
  1. Gebauter Reuse-Fall in Plauen.
  2. Neues Sport-/Vereinshaus.
  3. 189 dokumentierte wiederverwendete Stahlbetonfertigteile.
  4. Herkunft aus IW73/6-Mass-Housing-Kontext.
  5. Transportdistanz ca. 7 km.
- **5 wichtigste Bauteile:**
  1. 145 Decken-/Bodenplatten.
  2. 19 Außenwandelemente.
  3. 14 Innenwandelemente.
  4. 11 Kellerwandelemente.
  5. Anschlüsse/Verbindungen: relevant, aber unbekannt.
- **5 wichtigste Hürden:**
  1. Nachweis der Tragfähigkeit.
  2. Anschlussdetails.
  3. Geometrie/Rasterbindung.
  4. Schadstoff- und Materialprüfung.
  5. Fehlende öffentliche Primärdaten.
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Fertigteile aus seriellen Wohnbauten können in Nichtwohngebäuden weitergenutzt werden.
  2. Kurze Transportdistanz verbessert die Plausibilität.
  3. Bauteilkataloge sind für Planung entscheidend.
  4. Tragende Reuse-Fälle brauchen Prüf- und Haftungsstrategien.
  5. Dokumentation sollte systematisch veröffentlicht werden.
- **5 offene Fragen:**
  1. Wer waren Architekt, Tragwerksplaner und Bauherr?
  2. Welche Prüfungen wurden durchgeführt?
  3. Wie wurden die Platten verbunden?
  4. Welche Kosten- oder CO₂-Effekte wurden erreicht?
  5. Ist das Gebäude heute unverändert in Nutzung?

## Quellen und Links

- [S0] Hochgeladene Prioritätenliste: gebäude4_wiederverwendung_direct_reuse_examples.md
- [S1] Küpfer, C.; Bastien-Masse, M.; Fivet, C. (2023): Reuse of concrete components in new construction projects: Critical review of 77 circular precedents, Journal of Cleaner Production 383, 135235. DOI: https://doi.org/10.1016/j.jclepro.2022.135235
- [S2] ScienceDirect / Journal of Cleaner Production article page: https://www.sciencedirect.com/science/article/pii/S0959652622048090
- [S3] ResearchGate PDF/record for the same article: https://www.researchgate.net/publication/365763750_Reuse_of_concrete_components_in_new_construction_projectscritical_review_of_77_circular_precedents
- [S4] BauStatik-Wiki, Wiederverwendung von Stahlbetonbauteilen: https://baustatik-wiki.fiw.hs-wismar.de/mediawiki/index.php/Wiederverwendung_von_Stahlbetonbauteilen
- [S5] InNoWest Brandenburg, Bachelorarbeit zur Wiederverwendung von WBS70-Fertigteilen: https://innowest-brandenburg.de/beitraege/Bachelorarbeit-plattenbautyp-wbs-70
- [S6] BFT International, Wiederverwendung von Betonfertigteilplatten: https://www.bft-international.com/de/artikel/wiederverwendung-von-betonfertigteilplatten-4095412.html
