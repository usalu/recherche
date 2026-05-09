---
id: "Berlin_Schildow_Pilot_House"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "Berlin-Schildow Pilot House — Fallstudie Direct Reuse / Wiederverwendung von WBS70-Plattenbauteilen"
bauobjekt:
  - "Berlin_Schildow_Pilot_House"
legacy_paths:
  - "Gebäude\\Berlin_Schildow_Pilot_House.md"
projekt:
  - "Berlin_Schildow_Pilot_House"
reuse_chain_detected: "False"
---
# Berlin-Schildow Pilot House — Fallstudie Direct Reuse / Wiederverwendung von WBS70-Plattenbauteilen

## Migration

- Fallstudie ID: Berlin_Schildow_Pilot_House
- Legacy source count: 1
- Generated project: Berlin_Schildow_Pilot_House
- Generated bauobjekt: Berlin_Schildow_Pilot_House
- Extracted reuse_einsatz rows: 6
- Extracted datenpunkt rows: 11
- Extracted entity mapping rows: 16
- Reuse chain detected: False

## Legacy Content

### Legacy Source: Gebäude\Berlin_Schildow_Pilot_House.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Berlin_Schildow_Pilot_House
- Secondary targets: projekt/Berlin_Schildow_Pilot_House; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Berlin-Schildow Pilot House — Fallstudie Direct Reuse / Wiederverwendung von WBS70-Plattenbauteilen

**Arbeitsstand:** 2026-05-07  
**Sprache:** Deutsch  
**Regel:** Es werden nur tatsächlich wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente gezählt. Lose Möbel, Dekoration, reine DfD-Strategien und bloßer Bestandserhalt zählen nicht.


## 1. EINORDNUNG

- **Entscheidung:** HAUPTFALL
- **Bewertung:** ★★★★☆
- **Begründung:** Gebautes Pilotwohnhaus im Berliner Umland/Schildow mit tragender Wiederverwendung von WBS70-Fertigteilen aus abgebrochenem Plattenbau. Die wissenschaftliche PRECS-Datenbank führt den Fall als „Berlin-Schildow 2nd pilot house“ mit 200 zugeschnittenen Teilen aus 60 Decken- und 50 Innenwandplatten, 245 m³ Beton, Satteldachhaus, zweigeschossigem Atrium und nur neuer Betontreppe. Deine Ausgangsliste nennt „Berlin-Schildow pilot house 1“; die Fallbezeichnung ist daher unsicher, der Schildow-Reuse-Fall selbst ist belegt.
- **Vertrauensgrad:** teilweise belegt
- **Warnung Bestandserhalt:** nein
- **Warnung Möbel/Dekoration:** nein
- **Projektstatus:** gebaut

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Berlin-Schildow Pilot House / Berlin-Schildow 2nd pilot house | Untersuchter Reuse-Fall | [S0], [S1], [S7], [S8] | teilweise belegt | Nummerierung weicht zwischen Ausgangsliste und PRECS/Presse ab. |
| Gebäude | Einfamilienhaus / Pilotwohnhaus | Empfängergebäude | [S1], [S7], [S8] | belegt | Haus in Schildow nördlich Berlins. |
| Ort | Schildow, Brandenburg/Berliner Umland, Deutschland | Standort | [S1], [S7] | belegt | In Presse als „nördlich Berlins“ / „Berliner Umland“ beschrieben. |
| Projekt | Pilotprojekt zur Wiederverwendung von WBS70-Platten | Reuse-Projekt | [S1], [S7], [S8] | belegt | Forschung TU Berlin/IEMB-Kontext. |
| People | Claus Asam, IEMB/TU Berlin; Architekturbüro Conclus / Hervé Biele bzw. Joel Biele | Forschung/Planung laut Presse | [S7], [S8] | teilweise belegt | Namensschreibweise in Presse uneinheitlich; konkrete Projektrollen prüfen. |
| Bauteil | 200 zugeschnittene Teile aus 60 Decken- und 50 Innenwandplatten | Hauptreuse | [S1], [S3] | belegt | Volumen 245 m³. |
| Material | Stahlbetonfertigteile / WBS70 | Hauptmaterial | [S1], [S7] | belegt | Platten aus Berlin-Marzahn laut Presse. |
| Gebäude | Spender: Berliner Elfgeschosser / Marzahn-Plattenbau | Herkunft | [S7], [S8] | teilweise belegt | genaue Adresse unbekannt. |
| Reuse-Strategie | ex-situ Bauteilwiederverwendung; Zuschnitt; Remontage | direkte Wiederverwendung | [S1], [S7] | belegt | Platten wurden zugeschnitten und wieder montiert. |
| Aufbereitungsmethode | Zuschnitt/Sägen von Platten | Anpassung an neues Haus | [S1], [S7] | belegt | „sawn from“ / „auf Maß zersägt“. |
| Prüfung | Festigkeitstests / Belastungs-, Schneid-, Bohrversuche im IEMB-Kontext | Wiederverwendungseignung | [S7], [S8] | teilweise belegt | Allgemeine Projekt-/Forschungsprüfung, nicht alle Einzelwerte öffentlich. |
| Logistik | ca. 33 km Distanz; Transport per Tieflader/Kran im Pressekontext | Transport/Montage | [S1], [S7] | belegt | PRECS nennt 33 km. |
| Abbruchmethode | leichte Geräte, Lösen von Knotenpunkten, Durchtrennen von Verbindungsstählen | schonende Demontage | [S7] | teilweise belegt | Presse beschreibt allgemeines Verfahren im Pilotkontext. |
| Verbindung | WBS70-Knoten / neue Anschlüsse unbekannt | Montage | [S7] | teilweise belegt | genaue Ausführung in Schildow unbekannt. |
| Kennwert | 245 m³; 200 Teile; 33 km; 2005; Bauteilalter ca. 18 Jahre | Fallwerte | [S1] | belegt | Baukosten im Schildow-Fall unbekannt. |
| Norm | unbekannt | Genehmigung | unbekannt | unklar | Keine projektbezogenen Normangaben. |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Spendergebäude | Herkunft der WBS70-Platten ist entscheidend | Berliner Elfgeschosser / Marzahn | Gebäude, Bauteil, Logistik |
| Bauteilzuschnitt | Wiederverwendung erfolgt nicht nur 1:1, sondern durch Maßanpassung | 200 Teile aus 60 Decken- und 50 Innenwandplatten | Aufbereitungsmethode, Werkzeug |
| Pilotnummerierung | Quellen widersprechen sich bei „1st/2nd“ | Ausgangsliste vs. PRECS | Fallstudie, Dokument |
| Reuse-Testbau | Forschung erzeugt Prototyp-/Pilotstatus | Schildow als zweites Pilotprojekt | Fallstudie, Prüfung |

## 3. FALLSTUDIE

- **Name:** Berlin-Schildow Pilot House / Berlin-Schildow 2nd pilot house; Ausgangslistename: Berlin-Schildow pilot house 1
- **Ort:** Schildow, nördlich von Berlin, Deutschland
- **Gebäude:** Einfamilienhaus / Pilotwohnhaus
- **Projekt:** Wiederverwendung von WBS70-Plattenbauteilen aus Berliner/Marzahner Plattenbau
- **Beteiligte People / Akteure:** Claus Asam, IEMB/TU Berlin; Architekturbüro Conclus; Hervé/Joel Biele laut Presse; Bauherr unbekannt
- **Architekt:** Architekturbüro Conclus laut Pressekontext; konkrete Projektverantwortung prüfen
- **Tragwerksplaner:** unbekannt
- **Bauherr:** unbekannt; Presse nennt Bauherr als Unternehmensberater aus Westdeutschland, Name unbekannt
- **Zeitraum:** 2005 laut PRECS; Presseberichte 2005/2006
- **Ursprüngliche Nutzung:** WBS70-Plattenbau / Elfgeschosser in Berlin-Marzahn
- **Neue Nutzung:** Einfamilienhaus
- **Fläche / Maßstab:** Fläche unbekannt; 200 zugeschnittene Teile / 245 m³ Beton
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** Wissenschaftliche Sekundärquelle plus zeitgenössische Presse; Nummerierung und Detailplanung müssen geprüft werden

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; Zuschnitt; Remontage; Wohnungsbau-Platten zu Einfamilienhaus
- **Hauptniveau:** Tragwerk / Raumstruktur / Dachform
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die Platten wurden aus einem anderen Gebäude entnommen, geprüft/zugeschnitten und im neuen Haus verwendet. Sie wurden nicht am Ort erhalten und nicht zu Schotter oder Recyclingbeton verarbeitet.
- **Warum ist der Fall relevant?** Der Fall demonstriert, dass standardisierte WBS70-Elemente auch für individuellere Einfamilienhaus-Typologien mit Satteldach eingesetzt werden können.

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| zugeschnittene Betonfertigteile | Stahlbeton / WBS70 | Berliner/Marzahner Plattenbau | Wand/Decke | Wand/Decke/Dach-/Raumteile | 200 Teile / 245 m³ | ja | ja | teilweise | nein | Zuschnitt/Sägen | unbekannt | Festigkeitstests allgemein belegt | Tragfähigkeit, Gebrauchstauglichkeit | unbekannt | Maßanpassung, Anschlüsse | [S1], [S7], [S8] | Einzelteilmaße |
| Deckenplatten | Stahlbetonfertigteil | WBS70 | Decke | Ausgangsmaterial für zugeschnittene Bauteile, teils Decke/Dach? | 60 Ursprungsplatten | ja | ja | teilweise | nein | in Stücke gesägt | unbekannt | belastet/gesägt/gebohrt im Forschungsumfeld | Tragfähigkeit, Brandschutz | unbekannt | Brandschutz/Betondeckung | [S1], [S8] | neue genaue Funktion |
| Innenwandplatten | Stahlbetonfertigteil | WBS70 | Innenwand | Wand/Tragstruktur | 50 Ursprungsplatten | ja | ja | nein | nein | in Stücke gesägt | unbekannt | Festigkeitstests allgemein | Tragfähigkeit | unbekannt | Anschlüsse | [S1], [S8] | neue genaue Funktion |
| Treppe | neuer Beton | Neubau | keine Wiederverwendung | Treppe | 1 / unbekannter Umfang | ja | ja | nein | nein | neu | neu | unbekannt | Tragfähigkeit, Brandschutz | unbekannt | zählt nicht als Reuse | [S1] | Detail |
| Dach/Satteldach | Stahlbetonfertigteile? | WBS70-Teile | Wand/Decke | Satteldachform | unbekannt | wahrscheinlich ja | ja | ja | nein | Zuschnitt | unbekannt | unbekannt | Dachlasten, Feuchte, Wärme | unbekannt | ungewöhnliche Geometrie | [S7] | genaue Bauteilrolle |
| Fenster/Türen/Fassade/Geländer/Bodenaufbauten/TGA/Dämmung/Sanitär/Beleuchtung/feste Einbauten | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle | ja |

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | WBS70-Platten aus Marzahn identifizieren | IEMB/TU Berlin, Architekturbüro | Forschungs-/Bauteilaufnahme | unbekannt | selektiver Rückbau | unbekannt | Tests im IEMB-Kontext | Spender zu Schildow ca. 33 km | geeignete Platten finden | standardisierte WBS70-Elemente | [S1], [S7], [S8] |
| Bauteilinventar | 60 Decken + 50 Innenwände als Ausgangsmaterial; 200 Stücke | Forschung/Planer | Bauteilliste | unbekannt | unbekannt | Zuschnitt | unbekannt | 245 m³ | Daten-/Schnittplanung | Stücke nach Entwurf schneiden | [S1] |
| Schadstoffprüfung | Außenwandplatten teils problematisch wegen Dämmstoffen im allgemeinen WBS70-Kontext | IEMB/TU Berlin allgemein | Schadstoffvermeidung | unbekannt | Außenwände weniger geeignet | unbekannt | unbekannt | unbekannt | Asbest/gesundheitsschädliche Dämmstoffe möglich | vorrangig Decken und Innenwände | [S7] |
| Rückbau | Knoten lösen, Verbindungsstähle trennen | Rückbauunternehmen unbekannt | schonende Demontage | leichtes Gerät, Kran; Details allgemein | leichtes Gerät, Durchtrennen von Verbindungsstählen | unbekannt | unbekannt | Just-in-time wichtig | Beschädigung/Kosten | sorgfältige Demontage | [S7] |
| Ausbau | Wandteile auf Maß zersägen und verladen | unbekannt | Sägen/Zuschnitt | Säge, Kran, Tieflader | unbekannt | Zuschnitt | unbekannt | Direktanlieferung | Kran-/Baggerstandzeiten | Just-in-time | [S7] |
| Transport | Transport zur Baustelle | unbekannt | Schwertransport | Tieflader | unbekannt | unbekannt | unbekannt | ca. 33 km | Kosten/Timing | kurze regionale Kette | [S1], [S7] |
| Lagerung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | fehlende Bauteilbörse/Lager | Bauteilbörse gefordert | [S7] |
| Aufbereitung | Sägen in passende Teile | unbekannt | Zuschnitt | Säge | unbekannt | Zuschnitt | unbekannt | unbekannt | Maßgenauigkeit | maßgerechte Stücke | [S1], [S7] |
| Planung | Haus mit Satteldach und Atrium aus vorhandenen Platten | Conclus/IEMB-Kontext | Design aus vorhandenen Teilen | unbekannt | unbekannt | Zuschnitt | unbekannt | unbekannt | Bauvorschriften Satteldach | Platten für Satteldach nutzen | [S1], [S7] |
| Genehmigung | örtliche Bauvorschriften forderten Satteldach | Gemeinde/Bauaufsicht unbekannt | Anpassung an Ortsrecht | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Dachform | Satteldach aus Platten | [S7] |
| Wiedereinbau | Remontage in Schildow | Bau-/Montageteam unbekannt | Fertigteilmontage | Kran | unbekannt | unbekannt | unbekannt | Baustelle Schildow | Montagepräzision | zugeschnittene Platten | [S1], [S7] |
| Monitoring | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Langzeitdaten | unbekannt | keine Quelle |

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | WBS70-Wand- und Deckenplatten als neues Haus | Standsicherheit | projektspezifisch unbekannt | Festigkeitstests im Forschungsumfeld | Eignung alter Platten | Tests und Auswahl | [S7], [S8] |
| Lastabtragung | Satteldach und zweigeschossiges Atrium aus Platten möglich | Dach- und Wandlasten | unbekannt | unbekannt | ungewöhnliche Geometrie | Zuschnitt/Entwurf | [S1], [S7] |
| Verbindung | Knotenpunkte und Verbindungsstähle im Rückbau relevant | Montageanschluss | unbekannt | unbekannt | alte Verbindungen lösen/neue schaffen | Durchtrennen/Lösen beim Rückbau | [S7] |
| Brandschutz | projektspezifisch unbekannt | Wohngebäude | unbekannt | unbekannt | alte Deckenplatten; heutige Diskussion sieht mögliche Feuerwiderstandsdefizite | unbekannt | [S5] allgemein |
| Schallschutz | unbekannt | Wohnnutzung | unbekannt | unbekannt | Platten/Fugen | unbekannt | keine Quelle |
| Feuchte | Dach/Hülle betroffen | Witterungsschutz | unbekannt | unbekannt | Satteldach aus/mit Betonplatten | gute Dämmung erwähnt | [S7] |
| Wärmeschutz | Presse nennt Niedrigenergiehaus mit guter Dämmung als möglich/angestrebt | energetischer Standard | unbekannt | unbekannt | alte Bauteile | zusätzliche Dämmung | [S7] |
| Wärmebrücken | unbekannt | Hülle | unbekannt | unbekannt | Fugen/Plattenanschlüsse | unbekannt | keine Quelle |
| Luftdichtheit | unbekannt | Wohnhaus | unbekannt | unbekannt | Fugen | unbekannt | keine Quelle |
| TGA-Integration | Solarzellen im Pressekontext erwähnt/geplant | Energieversorgung | unbekannt | unbekannt | Integration in Bestandsteile | unbekannt | [S8] |
| Barrierefreiheit | unbekannt | Einfamilienhaus | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle |
| Zulassung/Haftung | unbekannt | Neubaunachweis | allgemeine heutige Einordnung: Eurocode 2, DIN EN 206-1, DIN 1045-2 | unbekannt | Bauaufsicht/Gewährleistung | Pilot-/Forschungsnachweis | [S4] allgemein |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| zugeschnittene wiederverwendete Teile | 200 | Stück | PRECS-Fallstudienliste | Empfängergebäude | [S1] | belegt |
| Ursprungs-Deckenplatten | 60 | Stück | PRECS-Fallstudienliste | Ausgangsbauteile | [S1] | belegt |
| Ursprungs-Innenwandplatten | 50 | Stück | PRECS-Fallstudienliste | Ausgangsbauteile | [S1] | belegt |
| Betonvolumen | 245 | m³ | PRECS-Fallstudienliste | wiederverwendetes Betonvolumen | [S1] | belegt |
| Transportdistanz | 33 | km | PRECS-Fallstudienliste | Spender zu Empfänger | [S1] | belegt |
| Jahr/Fallstudienstart | 2005 | Jahr | PRECS-Fallstudienliste | Projekt | [S1] | belegt |
| Bauteilalter | ca. 18 | Jahre | PRECS-Fallstudienliste | Bauteile bei Wiederverwendung | [S1] | belegt |
| Kosten | unbekannt | EUR | unbekannt | Schildow-Projekt | keine Quelle | unklar |
| CO₂-Einsparung | unbekannt | kg CO₂e | unbekannt | unbekannt | keine Quelle | unklar |
| Fläche | unbekannt | m² | unbekannt | Gebäude | keine Quelle | unklar |
| Energiebedarf | unbekannt | unbekannt | unbekannt | Gebäude | keine Quelle | unklar |

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Logistik/Just-in-time | logistisch/wirtschaftlich | Kran- und Tiefladerstandzeiten teuer | Wirtschaftlichkeit gefährdet | Logistik, Wirtschaft | genaue Abstimmung von Rückbau, Transport, Montage | Reuse braucht Logistikkette | [S7] |
| Schadstoffe in Außenwandplatten | technisch/gesundheitlich | Fassadenteile mit problematischen Dämmstoffen/Asbest im allgemeinen WBS70-Kontext | Außenwände weniger geeignet | Schadstoff, Bauteil | Decken und Innenwände bevorzugen | Bauteilauswahl muss Schadstoffe berücksichtigen | [S7] |
| Öffentliche Akzeptanz/Image | sozial/gestalterisch | „Platte“ als negatives Image | Markthemmnis | People, Wirtschaft | architektonisch eigenständige Häuser | Gestaltung beeinflusst Akzeptanz | [S8] |
| Genehmigung/Dachform | rechtlich/gestalterisch | örtliche Bauvorschriften forderten Satteldach | Entwurf muss angepasst werden | Recht, Gebäudehülle | Satteldach mit Platten realisieren | Reuse muss lokale Vorschriften aufnehmen | [S7] |
| Gewährleistung | rechtlich | gebrauchte tragende Teile | Unsicherheit bei Bauaufsicht | Recht, Prüfung | unbekannt | Prüf- und Dokumentationspfad nötig | [S8], [S4] |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** Forschung/Pilotprojekt aus Rückbau eines Marzahner Plattenbaus; genaue vertragliche Beschaffung unbekannt
- **Bauteilbörse / Quelle:** keine bestehende Bauteilbörse; Presse nennt Bedarf nach einer Börse für Plattenbauteile
- **Kostenwirkung:** projektspezifisch Schildow unbekannt; Presse nennt allgemein mögliche Rohbauersparnis von 20–30 % für Plattenhäuser, nicht als gesicherter Schildow-Kennwert
- **Zeitwirkung:** unbekannt
- **Versicherung / Haftung:** unbekannt
- **Gewährleistung:** als allgemeines Hemmnis genannt; projektspezifisch unbekannt
- **Arbeitsaufwand:** hoch durch Demontage, Tests, Zuschnitt, Logistik und Montage
- **Lagerung:** unbekannt; fehlende Lager-/Börsenstruktur als Problem
- **Marktbarrieren:** Logistik, Image, Gewährleistung, Bauteilmarkt, Schadstoffprüfung

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** laut Presse bei ähnlichen Pilotbauten von außen nicht zwingend erkennbar; für Schildow genaue Sichtbarkeit unbekannt
- **räumliche Transformation:** Elfgeschosser-/WBS70-Bauteile werden zum Einfamilienhaus mit Satteldach und Atrium
- **Atmosphäre / Ausdruck:** unbekannt
- **Umgang mit Spuren:** Rohbau zeigte laut Presse Spuren der Vorgeschichte; fertiger Zustand unbekannt
- **sozialer Wert:** Demonstration einer Alternative zum Zerschreddern von Plattenbauteilen
- **Denkmal- oder Bestandswert:** kein Denkmalschutz belegt
- **Kritik / Grenzen:** Pilotcharakter, Logistik, Image und Gewährleistung verhinderten offenbar breite Skalierung

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** Bauherr, exakter Architekt/Tragwerksplaner, Bauakte, Prüfberichte, Normnachweise, Kosten, CO₂, fertige Fotos/Monitoring.
- **Welche neuen Entitäten wären sinnvoll?** Pilotnummerierung, Bauteilzuschnitt, Spendergebäude, Reuse-Testbau.
- **Welche Daten fehlen?** genaue Adresse, Spendergebäude, Pläne, Verbindungsdetails, Prüfwerte, Kosten, U-Werte, heutiger Zustand.
- **Welche Quellen müssten geprüft werden?** IEMB/TU-Berlin-Berichte von Claus Asam, Conclus-Archiv, Bauakte Schildow/Mühlenbecker Land, Mettke/Asam 2005/2007-Veröffentlichungen.

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja, aber mit Namens-/Nummerierungswarnung
- **5 wichtigste Fakten:**
  1. Gebautes Pilotwohnhaus in Schildow.
  2. Wiederverwendung von WBS70-Platten aus Berliner/Marzahner Plattenbaukontext.
  3. 200 zugeschnittene Teile aus 60 Decken- und 50 Innenwandplatten.
  4. 245 m³ wiederverwendetes Betonvolumen.
  5. Satteldach und zweigeschossiges Atrium zeigen gestalterische Anpassbarkeit.
- **5 wichtigste Bauteile:**
  1. Deckenplatten.
  2. Innenwandplatten.
  3. zugeschnittene Betonstücke.
  4. Dach-/Satteldachbauteile aus Platten, genaue Funktion unbekannt.
  5. neue Betontreppe zählt nicht als Reuse.
- **5 wichtigste Hürden:**
  1. Logistik/Just-in-time.
  2. Schadstoffe in ungeeigneten Außenwandplatten.
  3. Zuschnitt und Maßgenauigkeit.
  4. Gewährleistung/Bauaufsicht.
  5. Image der Plattenbauweise.
- **5 wichtigste übertragbare Erkenntnisse:**
  1. WBS70-Platten können in individuelle Hausformen transformiert werden.
  2. Außenwandplatten sind wegen Schadstoffen/Dämmung besonders kritisch.
  3. Bauteilprüfung und Forschung schaffen Vertrauen.
  4. Reuse muss lokale Bauvorschriften aufnehmen.
  5. Ohne Bauteilbörse/Logistiksystem bleibt Skalierung schwierig.
- **5 offene Fragen:**
  1. Ist die korrekte Bezeichnung „pilot house 1“ oder „2nd pilot house“?
  2. Welche Prüfwerte wurden gemessen?
  3. Welche Anschlüsse wurden neu hergestellt?
  4. Welche Kosten entstanden im Schildow-Projekt?
  5. Wie ist der aktuelle Zustand und Nutzungsstatus?

## Quellen und Links

- [S0] Hochgeladene Prioritätenliste: gebäude4_wiederverwendung_direct_reuse_examples.md
- [S1] Küpfer, C.; Bastien-Masse, M.; Fivet, C. (2023): Reuse of concrete components in new construction projects: Critical review of 77 circular precedents, Journal of Cleaner Production 383, 135235. DOI: https://doi.org/10.1016/j.jclepro.2022.135235
- [S2] ScienceDirect / Journal of Cleaner Production article page: https://www.sciencedirect.com/science/article/pii/S0959652622048090
- [S3] ResearchGate PDF/record for the same article: https://www.researchgate.net/publication/365763750_Reuse_of_concrete_components_in_new_construction_projectscritical_review_of_77_circular_precedents
- [S4] BauStatik-Wiki, Wiederverwendung von Stahlbetonbauteilen: https://baustatik-wiki.fiw.hs-wismar.de/mediawiki/index.php/Wiederverwendung_von_Stahlbetonbauteilen
- [S5] InNoWest Brandenburg, Bachelorarbeit zur Wiederverwendung von WBS70-Fertigteilen: https://innowest-brandenburg.de/beitraege/Bachelorarbeit-plattenbautyp-wbs-70
- [S6] BFT International, Wiederverwendung von Betonfertigteilplatten: https://www.bft-international.com/de/artikel/wiederverwendung-von-betonfertigteilplatten-4095412.html
- [S7] WELT, Wände mit Vorleben, 13.11.2005: https://www.welt.de/print-wams/article134693/Waende-mit-Vorleben.html
- [S8] taz, Die Wiedergeburt der Platte, 06.01.2006: https://taz.de/Die-Wiedergeburt-der-Platte/!493469/
- [S9] Stern, Vorzeigeimmobilien: Recycling der Platte: https://www.stern.de/wirtschaft/immobilien/vorzeigeimmobilien-recycling-der-platte-3300150.html
