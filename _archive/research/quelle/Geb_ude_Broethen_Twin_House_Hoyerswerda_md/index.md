---
entity: "quelle"
id: "Geb_ude_Broethen_Twin_House_Hoyerswerda_md"
title: "Geb_ude_Broethen_Twin_House_Hoyerswerda_md"
build_status: "promoted_phase42"
source_filename: "Broethen_Twin_House_Hoyerswerda.md"
---

# Geb_ude_Broethen_Twin_House_Hoyerswerda_md

**Arbeitsstand:** 2026-05-07  
**Sprache:** Deutsch  
**Regel:** Es werden nur tatsächlich wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente gezählt. Lose Möbel, Dekoration, reine DfD-Strategien und bloßer Bestandserhalt zählen nicht.

## 1. EINORDNUNG

- **Entscheidung:** VERGLEICHSFALL
- **Bewertung:** ★★★★☆
- **Begründung:** Gebauter Wohnhausfall mit tragender Wiederverwendung von großformatigen P2-Stahlbetonfertigteilen aus dem Plattenbau. Die wissenschaftliche PRECS-Datenbank nennt 26 Wand- und 50 Deckenplatten des P2-Systems aus dem Massenwohnungsbau, wiederverwendet in einem neuen Doppelhaus in Bröthen/Hoyerswerda. Die Quellenlage ist jedoch dünn und stark sekundär; deshalb Vergleichsfall statt Hauptfall.
- **Vertrauensgrad:** teilweise belegt
- **Warnung Bestandserhalt:** nein
- **Warnung Möbel/Dekoration:** nein
- **Projektstatus:** gebaut

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Bröthen twin-house | Untersuchter Reuse-Fall | [S1], [S2] | belegt | In PRECS als C23 geführt. |
| Ort | Bröthen / Hoyerswerda, Deutschland | Standort | [S1], [S2] | belegt | Bröthen ist Ortsteil/Teilraum von Hoyerswerda. |
| Gebäude | Doppelhaus / twin-house | Empfängergebäude | [S1], [S2] | belegt | Neue Wohnnutzung. |
| Projekt | Wiederverwendung von P2-Plattenbauteilen | Kernprojekt | [S1], [S2] | belegt | Wohnungsbau-Platten zu Doppelhaus. |
| Bauteil | 26 Wandplatten | tragende/räumliche Bauteile | [S1], [S2] | belegt | P2-System aus Massenwohnungsbau. |
| Bauteil | 50 Deckenplatten | tragende/räumliche Bauteile | [S1], [S2] | belegt | P2-System aus Massenwohnungsbau. |
| Material | Stahlbetonfertigteile / P2-PC-System | Hauptmaterial | [S1], [S2] | belegt | PC = precast concrete. |
| Gebäude | Spender: Massenwohnungsbau / Plattenbau | Herkunft | [S1], [S2] | teilweise belegt | genaue Adresse unbekannt. |
| Reuse-Strategie | ex-situ Bauteilwiederverwendung | Entnahme und Einbau in Neubau | [S1], [S2] | belegt | Kein Recycling. |
| Logistik | ca. 6 km Spender–Empfänger | Transport | [S1], [S2] | belegt | Kurze Distanz laut PRECS-Tabelle. |
| Kennwert | 76 Platten; 2001; ca. 32 Jahre Bauteilalter | Fallwerte | [S1], [S2] | belegt | Volumen/Fläche unbekannt. |
| People | unbekannt | Akteure | unbekannt | unklar | keine öffentlich verifizierte Projektliste gefunden. |
| Architekt | unbekannt | Planung | unbekannt | unklar | nicht belegt. |
| Tragwerksplaner | unbekannt | Nachweise | unbekannt | unklar | nicht belegt. |
| Bauherr | unbekannt | Auftraggeber | unbekannt | unklar | nicht belegt. |
| Prüfung | unbekannt | Eignungsnachweis | unbekannt | unklar | PRECS belegt Fall, aber nicht Prüfprotokolle. |
| Norm | unbekannt | Genehmigung | unbekannt | unklar | Keine Normnummern gefunden. |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Spendergebäude | Herkunft der Platten ist nicht ausreichend erfasst | mass-housing donor, 6 km entfernt | Gebäude, Logistik, Bauteil |
| Fertigteilsystem | P2-System ist für die Demontierbarkeit entscheidend | P2 PC system | Material, Bauteil, Tragwerkssystem |
| Quellenqualität | Fall ist hauptsächlich über Sekundärdatenbank belegt | PRECS/JCP statt Projektseite | Bericht, Dokument, Vertrauensgrad |

## 3. FALLSTUDIE

- **Name:** Bröthen twin-house / Bröthen twin-house, Hoyerswerda
- **Ort:** Bröthen / Hoyerswerda, Deutschland
- **Gebäude:** Doppelhaus / Wohnhaus
- **Projekt:** Wiederverwendung von P2-Fertigteilen aus Massenwohnungsbau
- **Beteiligte People / Akteure:** unbekannt
- **Architekt:** unbekannt
- **Tragwerksplaner:** unbekannt
- **Bauherr:** unbekannt
- **Zeitraum:** 2001 laut PRECS
- **Ursprüngliche Nutzung:** Massenwohnungsbau / Plattenbau im P2-System
- **Neue Nutzung:** Doppelhaus / Wohnnutzung
- **Fläche / Maßstab:** 76 wiederverwendete Platten; Fläche und Volumen unbekannt
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** hauptsächlich wissenschaftliche Sekundärquelle; Primärdokumente nicht öffentlich gefunden

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; tragende Wiederverwendung von Betonfertigteilen
- **Hauptniveau:** Tragwerk / Raumstruktur / Gebäudehülle teilweise
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die Platten wurden aus einem anderen Gebäude entnommen und als Wand-/Deckenelemente im Neubau wiederverwendet. Kein Verbleib am Ort, keine Zerkleinerung zu Recyclingmaterial.
- **Warum ist der Fall relevant?** Bröthen erweitert die Reihe ostdeutscher Plattenbau-Reuse-Fälle um das P2-System und zeigt den Einsatz im Doppelhausmaßstab mit kurzer Transportdistanz.

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Wandplatten | Stahlbetonfertigteil / P2 | Massenwohnungsbau | Wand | Wand / Trag- und Raumstruktur im Doppelhaus | 26 Stück | ja | ja | teilweise | nein | Demontage, Reinigung, ggf. Anpassung unbekannt | unbekannt | unbekannt | Tragfähigkeit, Brandschutz, Schallschutz | unbekannt | Anschlussdetails | [S1], [S2] | Maße, Lage |
| Deckenplatten | Stahlbetonfertigteil / P2 | Massenwohnungsbau | Geschossdecke | Decke / ggf. Dach oder Boden | 50 Stück | ja | ja | teilweise | nein | Demontage, Reinigung | unbekannt | unbekannt | Biegung, Durchbiegung, Feuerwiderstand | unbekannt | Transportgewicht | [S1], [S2] | Lage, Spannweiten |
| Fassaden-/Außenwandanteile | Stahlbetonfertigteil? | P2-Platten | Außenwand? | Hülle? | unbekannt | ja/teilweise | ja | ja | nein | unbekannt | unbekannt | unbekannt | Wärmeschutz, Feuchte | unbekannt | Dämmstandard | unbekannt | alle Details |
| Fenster | unbekannt | unbekannt | unbekannt | Fenster | unbekannt | nein | nein | ja | nein | unbekannt | unbekannt | unbekannt | Wärmeschutz | unbekannt | unbekannt | unbekannt | alle Daten |
| Türen | unbekannt | unbekannt | unbekannt | Türen | unbekannt | nein | ja | teilweise | nein | unbekannt | unbekannt | unbekannt | Brand/Schall | unbekannt | unbekannt | unbekannt | alle Daten |
| Dach | unbekannt | unbekannt | unbekannt | Dach | unbekannt | unbekannt | ja | ja | nein | unbekannt | unbekannt | unbekannt | Wetter, Last, Dämmung | unbekannt | unbekannt | unbekannt | alle Daten |
| Treppen | unbekannt | unbekannt | unbekannt | Erschließung | unbekannt | ja | ja | nein | nein | unbekannt | unbekannt | unbekannt | Tragfähigkeit | unbekannt | unbekannt | unbekannt | alle Daten |
| TGA | unbekannt | unbekannt | unbekannt | Haustechnik | unbekannt | nein | nein | nein | ja | unbekannt | unbekannt | unbekannt | Betrieb/Wartung | unbekannt | Integration in Platten | unbekannt | alle Daten |

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | P2-Platten aus Massenwohnungsbau auswählen | unbekannt | Bauteilaufnahme | unbekannt | unbekannt | unbekannt | unbekannt | Spender ca. 6 km entfernt | passende Plattenverfügbarkeit | lokale Ressource nutzen | [S1] |
| Bauteilinventar | 26 Wand- und 50 Deckenplatten erfassen | unbekannt | Inventarisierung | unbekannt | selektiver Rückbau wahrscheinlich | unbekannt | unbekannt | kurze Distanz | Dokumentation fehlt | unbekannt | [S1], [S2] |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Schadstoffe möglich | unbekannt | unbekannt |
| Rückbau | Bauteile aus Spenderbau demontieren | unbekannt | Demontage von Fertigteilen | Kran / Trenntechnik unbekannt | selektiv, nicht belegt im Detail | unbekannt | unbekannt | schwere Elemente | Beschädigung | unbekannt | [S1] |
| Transport | Platten nach Bröthen transportieren | unbekannt | Schwertransport | Tieflader/Kran wahrscheinlich | entfällt | entfällt | Sichtkontrolle unbekannt | ca. 6 km | Gewicht/Sequenz | kurze Distanz | [S1] |
| Lagerung | unbekannt | unbekannt | unbekannt | unbekannt | entfällt | unbekannt | unbekannt | unbekannt | Platzbedarf | unbekannt | unbekannt |
| Aufbereitung | Reinigung / Anpassung | unbekannt | unbekannt | unbekannt | entfällt | unbekannt | unbekannt | unbekannt | Detaildaten fehlen | unbekannt | unbekannt |
| Planung | Doppelhaus mit P2-Platten entwerfen | unbekannt | stockbasierter Entwurf | unbekannt | entfällt | unbekannt | statische Nachweise unbekannt | unbekannt | Rasterbindung | unbekannt | [S1] |
| Genehmigung | unbekannt | unbekannt | unbekannt | unbekannt | entfällt | entfällt | unbekannt | unbekannt | Zulassung | unbekannt | unbekannt |
| Wiedereinbau | Montage als neues Doppelhaus | unbekannt | Kranmontage wahrscheinlich | unbekannt | entfällt | Remontage | unbekannt | unbekannt | Fügung/Anschlüsse | unbekannt | [S1] |
| Monitoring | unbekannt | unbekannt | unbekannt | unbekannt | entfällt | entfällt | unbekannt | unbekannt | Langzeitdaten fehlen | unbekannt | unbekannt |

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | P2-Wand- und Deckenplatten in Doppelhaus | Tragfähigkeit / Gebrauchstauglichkeit | unbekannt | unbekannt | Platten aus anderer Typologie | statische Neuberechnung erforderlich | [S1] |
| Lastabtragung | wahrscheinlich Wand-/Deckensystem | Vertikal-/Horizontallasten | unbekannt | unbekannt | neue Anordnung | unbekannt | unbekannt |
| Verbindung | unbekannt | kraftschlüssige Anschlüsse | unbekannt | unbekannt | alte Plattenfugen | unbekannt | unbekannt |
| Brandschutz | unbekannt | Feuerwiderstand Wohnhaus | unbekannt | unbekannt | Betondeckung/Fugen | unbekannt | unbekannt |
| Schallschutz | unbekannt | Wohnnutzung | unbekannt | unbekannt | Fugen, neue Raumaufteilung | unbekannt | unbekannt |
| Feuchte | unbekannt | Außenwand/Dach | unbekannt | unbekannt | Plattenhülle | unbekannt | unbekannt |
| Wärmeschutz | unbekannt | zeitgenössischer Wärmeschutz | unbekannt | unbekannt | Altplatten brauchen Dämmung | unbekannt | unbekannt |
| Wärmebrücken | unbekannt | Minimierung | unbekannt | unbekannt | Plattenfugen | unbekannt | unbekannt |
| Luftdichtheit | unbekannt | Gebäudehülle | unbekannt | unbekannt | Fugen | unbekannt | unbekannt |
| TGA-Integration | unbekannt | Leitungsführung | unbekannt | unbekannt | Durchbrüche in Altplatten | unbekannt | unbekannt |
| Barrierefreiheit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Dauerhaftigkeit | Platten ca. 32 Jahre alt bei Wiederverwendung | Restlebensdauer | unbekannt | unbekannt | Alterung | Prüfung erforderlich | [S1] |
| Zulassung/Haftung | unbekannt | Bauordnungsrecht | unbekannt | unbekannt | wiederverwendete tragende Bauteile | unbekannt | unbekannt |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| wiederverwendete Wandplatten | 26 | Stück | PRECS-Falldatenbank | Empfänger-Doppelhaus | [S1] | belegt |
| wiederverwendete Deckenplatten | 50 | Stück | PRECS-Falldatenbank | Empfänger-Doppelhaus | [S1] | belegt |
| wiederverwendete Bauteile gesamt | 76 | Stück | Summe aus PRECS-Angaben | Empfänger-Doppelhaus | [S1] | belegt |
| Transportdistanz | 6 | km | PRECS-Falldatenbank | Spender–Empfänger | [S1] | belegt |
| Bauteilalter | 32 | Jahre | PRECS-Falldatenbank | Plattenbauteile | [S1] | belegt |
| Projektjahr | 2001 | Jahr | PRECS-Falldatenbank | Empfängerprojekt | [S1] | belegt |
| Fläche | unbekannt | m² | unbekannt | Empfängergebäude | unbekannt | unklar |
| Betonvolumen | unbekannt | m³ | unbekannt | wiederverwendete Platten | unbekannt | unklar |
| CO₂-Einsparung | unbekannt | t CO₂e | unbekannt | unbekannt | unbekannt | unklar |
| Kosten | unbekannt | EUR | unbekannt | unbekannt | unbekannt | unklar |
| Bauzeit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unklar |
| U-Wert | unbekannt | W/m²K | unbekannt | Gebäudehülle | unbekannt | unklar |
| Zirkularitätskennwert | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unklar |

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| dünne Quellenlage | dokumentarisch | alte Projektunterlagen nicht öffentlich | viele Felder unbekannt | Dokument, Bericht | Primärquellen prüfen | Sekundärdaten reichen nicht für Detailplanung | [S1] |
| Fertigteildemontage | technisch/logistisch | großformatige Platten müssen beschädigungsarm gelöst werden | Risiko von Ausschuss | Bauteil, Abbruchmethode | selektiver Rückbau | Demontierbarkeit des Systems ist zentral | [S1] |
| kurze Transportdistanz nötig | wirtschaftlich/logistisch | Beton ist schwer | Transporte können Umweltvorteil reduzieren | Logistik, Kennwert | lokale Spender nutzen | Nahbereich ist für Betonreuse entscheidend | [S1] |
| neue Anschlüsse | technisch/rechtlich | alte Platten in neuem System | Nachweis- und Haftungsfragen | Verbindung, Prüfung | unbekannt | Anschlussdetails dokumentieren | unbekannt |
| Wärmeschutz | technisch | alte Betonplatten allein erfüllen moderne Hüllenanforderungen nicht | Zusatzdämmung nötig | Leistungsanforderung, Material | unbekannt | Reuse-Tragwerk braucht neue Hüllschichten | unbekannt |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** lokale Entnahme aus Massenwohnungsbau / P2-Plattenbau; konkrete Verträge unbekannt.
- **Bauteilbörse / Quelle:** keine Bauteilbörse belegt; Spendergebäude im Umkreis von ca. 6 km laut PRECS.
- **Kostenwirkung:** unbekannt.
- **Zeitwirkung:** unbekannt.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** unbekannt; bei PRECS generell höher für Demontage, Sortierung und Nachweis.
- **Lagerung:** unbekannt.
- **Marktbarrieren:** fehlende Primärdaten, Nachweis gebrauchter Tragbauteile, Logistik schwerer Elemente.

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** unbekannt.
- **räumliche Transformation:** hoch; Platten aus Massenwohnungsbau werden zu einem Doppelhaus.
- **Atmosphäre / Ausdruck:** unbekannt.
- **Umgang mit Spuren:** unbekannt.
- **sozialer Wert:** Beleg für Weiterverwendung ostdeutscher Plattenbausubstanz im Wohnungsneubau kleiner Maßstäbe.
- **Denkmal- oder Bestandswert:** unbekannt.
- **Kritik / Grenzen:** starke Abhängigkeit von Sekundärquellen; keine detaillierten öffentlichen Projektinformationen.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** Akteure, Pläne, Fotos, Bauherr, Tragwerksnachweise, Baukosten, CO₂-Bilanz, Flächen, Verbindungsdetails, Dämm- und TGA-Konzept.
- **Neue Entitäten sinnvoll:** Spendergebäude, Fertigteilsystem, Quellenqualität.
- **Fehlende Daten:** genaue Herkunft der P2-Platten, Zuschnitt/Aufbereitung, Prüfmethoden, Abfallvermeidung in t.
- **Zu prüfende Quellen:** Dechantsreiter et al. 2015; Fischer et al. 2012; Heyn et al. 2008b; Mettke 2008/2010; lokale Bauakten Hoyerswerda/Bröthen.

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja, aber als Vergleichsfall mit Quellenhinweis.
- **5 wichtigste Fakten:**
  1. Gebauter PRECS-Fall, 2001.
  2. Standort Bröthen/Hoyerswerda.
  3. 26 Wandplatten und 50 Deckenplatten wurden wiederverwendet.
  4. Die Bauteile stammen aus dem P2-Plattenbausystem des Massenwohnungsbaus.
  5. Die Distanz zwischen Spender- und Empfängerprojekt betrug ca. 6 km.
- **5 wichtigste Bauteile:** P2-Wandplatten; P2-Deckenplatten; Verbindungen/Fugen; Gebäudehülle/Dämmung; Dach/Treppen unbekannt.
- **5 wichtigste Hürden:** Quellenlage; Demontage; Anschlüsse; Logistik; Wärmeschutz.
- **5 wichtigste übertragbare Erkenntnisse:**
  1. P2-Fertigteile können im kleinen Wohnhausmaßstab weitergenutzt werden.
  2. Kurze Distanzen sind besonders wichtig.
  3. Bauteildokumentation muss projektbegleitend entstehen.
  4. Ohne Primärquellen bleibt technische Übertragbarkeit begrenzt.
  5. Historische Plattenbau-Reuse-Fälle sind wichtige Präzedenzfälle, aber keine fertigen Leitfäden.
- **5 offene Fragen:** genaue Akteure; Plattenherkunft; Prüfprotokolle; Kosten; heutiger Gebäudezustand.

## Quellen und Links

- [S0] Ausgangsliste des Nutzers: `gebäude4_wiederverwendung_direct_reuse_examples.md`, Eintrag 19.
- [S1] Küpfer, C.; Bastien-Masse, M.; Fivet, C. (2023): *Reuse of concrete components in new construction projects: Critical review of 77 circular precedents*, Journal of Cleaner Production. https://www.sciencedirect.com/science/article/pii/S0959652622048090
- [S2] ScienceDirect Topics / Appendix-B-Auszug zur PRECS-Fallliste. https://www.sciencedirect.com/topics/engineering/inverset
