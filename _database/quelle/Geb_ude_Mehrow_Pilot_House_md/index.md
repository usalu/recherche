---
entity: "quelle"
id: "Geb_ude_Mehrow_Pilot_House_md"
title: "Geb_ude_Mehrow_Pilot_House_md"
build_status: "promoted_phase42"
source_filename: "Mehrow_Pilot_House.md"
---

# Geb_ude_Mehrow_Pilot_House_md

**Arbeitsstand:** 2026-05-07  
**Sprache:** Deutsch  
**Regel:** Es werden nur tatsächlich wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente gezählt. Lose Möbel, Dekoration, reine DfD-Strategien und bloßer Bestandserhalt zählen nicht.

## 1. EINORDNUNG

- **Entscheidung:** HAUPTFALL / kleiner tragwerksrelevanter Vergleichsfall
- **Bewertung:** ★★★★☆
- **Begründung:** Gebautes Pilotwohnhaus mit zentraler tragender Wiederverwendung von WBS70-Stahlbetonfertigteilen aus einem abgebrochenen Plattenbau. Die PRECS-Datenbank dokumentiert 22 Wandplatten und 27 Deckenplatten, zusammen 118 m³, als Wiederverwendung in einem Flachdachhaus. Presseberichte nennen zusätzlich ein ca. 200 m² großes Einfamilienhaus in Mehrow aus 27 Deckenplatten und 22 Innenwänden eines abgerissenen Marzahner Elfgeschossers. Der Fall ist klein, aber technisch wichtig.
- **Vertrauensgrad:** belegt / teilweise belegt bei Detailrollen
- **Warnung Bestandserhalt:** nein
- **Warnung Möbel/Dekoration:** nein
- **Projektstatus:** gebaut

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Mehrow 1st pilot house | Untersuchter Reuse-Fall | [S1], [S2], [S3] | belegt | In PRECS als C31 geführt. |
| Gebäude | Einfamilienhaus / Pilotwohnhaus | Empfängergebäude | [S1], [S3] | belegt | Presse nennt 200 m² und Bewohnerfamilie. |
| Ort | Mehrow, Brandenburg, Deutschland | Standort | [S1], [S3] | belegt | Berliner Umland. |
| Projekt | Wiederverwendung von WBS70-Platten im Wohnhaus | Kernprojekt | [S1], [S3] | belegt | Flachdachhaus laut PRECS. |
| People | Hervé Biele / Conclus | Architekt/Planung im Pressekontext | [S3] | teilweise belegt | Presse nennt ihn als Architekt/Wirtschaftsingenieur im Konzept. |
| People | Claus Asam / IEMB | Bauingenieur/Forschung im Pressekontext | [S3] | teilweise belegt | Mit Biele im Testbau-Kontext genannt. |
| Material | WBS70-Stahlbetonfertigteile | wiederverwendetes Material | [S1], [S3] | belegt | DDR-Plattenbausystem. |
| Bauteil | 22 Wandplatten, 27 Deckenplatten | Hauptreuse | [S1], [S2], [S3] | belegt | 118 m³ laut PRECS; taz nennt gleiche Stückzahlen in umgekehrter Alltagssprache. |
| Gebäude | Spender: abgerissener Marzahner Elfgeschosser | Herkunft der Platten | [S3] | teilweise belegt | genaue Adresse unbekannt. |
| Reuse-Strategie | ex-situ Bauteilwiederverwendung | Entnahme und Wiedereinbau | [S1], [S3] | belegt | Keine Zerkleinerung zu Recyclingmaterial. |
| Aufbereitungsmethode | Demontage, Reinigung, ggf. Zuschnitt | Anpassung an Neubau | [S1], [S3] | teilweise belegt | Zuschnitt für Mehrow nicht in allen Details belegt. |
| Abbruchmethode | selektive Demontage / schonender Rückbau | Bauteilgewinnung | [S3] | teilweise belegt | Presse beschreibt allgemeinen Vorgang im Pilotkontext. |
| Logistik | 8 oder 17 km Distanz laut PRECS | Transport | [S1] | teilweise belegt | Unsicherheit in PRECS-Tabelle übernommen. |
| Wirtschaft | 840 EUR/m² berichtet; ca. 1.100 EUR/m² Vergleich laut Biele | Kostenhinweis | [S3] | teilweise belegt | Pressewert, nicht geprüfte Kostenabrechnung. |
| Kennwert | 118 m³; 49 Bauteile; 2005; Bauteilalter ca. 21 Jahre | Fallwerte | [S1] | belegt | Weitere Kennwerte unbekannt. |
| Prüfung | unbekannt / IEMB-Forschungskontext | Eignungsnachweis | [S3] | teilweise belegt | Einzelprüfberichte nicht gefunden. |
| Norm | unbekannt | Bauordnungs-/Tragwerksnachweis | unbekannt | unklar | Keine Normnummern öffentlich belegt. |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Spendergebäude | Ohne Herkunft keine Wiederverwendungsbewertung | Marzahner Elfgeschosser | Gebäude, Bauteil, Logistik |
| Pilotserie | Mehrow und Schildow gehören zu einer frühen Pilotreihe | „1st pilot house“ | Fallstudie, Projekt, Forschung |
| Rohbaukostenvorteil | Wirtschaftlicher Nutzen ist Kernargument | 840 EUR/m² laut Presse | Wirtschaft, Kennwert |

## 3. FALLSTUDIE

- **Name:** Mehrow 1st pilot house / Mehrow Pilot House
- **Ort:** Mehrow, Brandenburg, Deutschland
- **Gebäude:** Einfamilienhaus / Pilotwohnhaus
- **Projekt:** Neubau eines Wohnhauses mit wiederverwendeten WBS70-Plattenbauteilen
- **Beteiligte People / Akteure:** Hervé Biele / Conclus; Claus Asam / IEMB; Bewohnerfamilie laut Presse; weitere Akteure unbekannt
- **Architekt:** Hervé Biele / Conclus laut Pressekontext; offizielle Projektunterlagen unbekannt
- **Tragwerksplaner:** unbekannt; Claus Asam / IEMB im Forschungs-/Ingenieurkontext genannt
- **Bauherr:** unbekannt; Presse erwähnt Familie, Name nicht angegeben
- **Zeitraum:** 2005; Presse 2005/2006
- **Ursprüngliche Nutzung:** WBS70-Plattenbau / Elfgeschosser in Berlin-Marzahn
- **Neue Nutzung:** Einfamilienhaus für eine dreiköpfige Familie
- **Fläche / Maßstab:** ca. 200 m² laut taz; 49 Fertigteile / 118 m³ laut PRECS
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** Wissenschaftlich dokumentierter PRECS-Fall plus zeitgenössische Presse; technische Detailpläne und Genehmigungsunterlagen nicht öffentlich gefunden

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; tragende Wiederverwendung von Fertigteilen; adaptive Bauteiltransformation
- **Hauptniveau:** Tragwerk / Raumstruktur / Gebäudehülle teilweise
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die Bauteile stammen aus einem anderen Gebäude und werden als Bauteile weitergenutzt. Sie bleiben nicht im Bestand und werden nicht zu Recyclingzuschlag oder Schotter verarbeitet.
- **Warum ist der Fall relevant?** Mehrow ist ein früher, gebauter Nachweis, dass großformatige DDR-Plattenbauelemente im Einfamilienhausbau tragend wiederverwendet werden können.

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Wandplatten | Stahlbetonfertigteil / WBS70 | Marzahner Plattenbau | Innen-/Wandbauteile | Wände / Raumstruktur | 22 Stück | ja | ja | teilweise | nein | Demontage, Reinigung, ggf. Anpassung | unbekannt | unbekannt | Tragfähigkeit, Schallschutz, Brandschutz | unbekannt | Anschlüsse, bauaufsichtlicher Nachweis | [S1], [S3] | Lage/Abmessungen |
| Deckenplatten | Stahlbetonfertigteil / WBS70 | Marzahner Plattenbau | Geschossdecke | Decke / Dach? | 27 Stück | ja | ja | teilweise | nein | Demontage, Reinigung | unbekannt | unbekannt | Biegung, Durchbiegung, Brandschutz | unbekannt | Transportgewicht, Montage | [S1], [S3] | genaue Einbaulage |
| Betonvolumen gesamt | Stahlbeton | WBS70 | Wand/Decke | Tragwerk Neubau | 118 m³ | ja | ja | teilweise | nein | unbekannt | unbekannt | unbekannt | Tragfähigkeit | unbekannt | Materialnachweis | [S1] | Einzelwerte |
| Fenster | unbekannt | unbekannt | unbekannt | Fenster | unbekannt | nein | nein | ja | nein | unbekannt | unbekannt | unbekannt | Wärmeschutz | unbekannt | unbekannt | unbekannt | alle Daten |
| Türen | unbekannt | unbekannt | unbekannt | Türen | unbekannt | nein | ja | teilweise | nein | unbekannt | unbekannt | unbekannt | Schall-/Brandschutz | unbekannt | unbekannt | unbekannt | alle Daten |
| Dach | unbekannt; Flachdachhaus laut PRECS | unbekannt | unbekannt | Dach | unbekannt | unbekannt | ja | ja | nein | unbekannt | unbekannt | unbekannt | Feuchte/Wärme/Last | unbekannt | unbekannt | [S1] | Aufbau |
| Treppe | unbekannt | unbekannt | unbekannt | Treppe | unbekannt | ja | ja | nein | nein | unbekannt | unbekannt | unbekannt | Tragfähigkeit | unbekannt | unbekannt | unbekannt | alle Daten |
| TGA | unbekannt | unbekannt | unbekannt | Haustechnik | unbekannt | nein | nein | nein | ja | unbekannt | unbekannt | unbekannt | Energie/Wartung | unbekannt | unbekannt | [S3] | konkrete Systeme |
| Dämmung | unbekannt / hochwertig laut Pressekontext allgemein | unbekannt | unbekannt | Wärmeschutz | unbekannt | nein | nein | ja | nein | unbekannt | unbekannt | unbekannt | Wärmeschutz | unbekannt | Altbeton braucht Dämmkonzept | [S3] | Material und U-Werte |

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | passende WBS70-Bauteile identifizieren | Planung/Forschung | Bauteilaufnahme | unbekannt | unbekannt | unbekannt | unbekannt | Spenderort Nähe Berlin | passende Bauteilgeometrie | Entwurf an Bestand anpassen | [S1], [S3] |
| Bauteilinventar | 22 Wand- und 27 Deckenplatten erfassen | Planungsteam | Inventarliste | unbekannt | selektive Demontage | Reinigung | unbekannt | 8/17 km laut PRECS | unklare Distanz | lokale Beschaffung | [S1] |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Schadstoffe im Bestand möglich | unbekannt | unbekannt |
| Rückbau/Ausbau | Platten aus Marzahner Elfgeschosser lösen | Abbruch-/Baufirma, Forschungskontext | schonender Rückbau | Kran, Schneid-/Trenntechnik unbekannt | selektiver Rückbau | unbekannt | unbekannt | schwere Platten | Beschädigungsrisiko | kontrollierte Demontage | [S3] |
| Transport | Platten nach Mehrow transportieren | Logistik | Schwertransport | Tieflader/Kran wahrscheinlich | entfällt | entfällt | Sichtprüfung unbekannt | 8 oder 17 km | Transportgewicht | kurze Distanz | [S1] |
| Lagerung | Zwischenlagerung | Bauunternehmen/Bauherr | unbekannt | unbekannt | entfällt | unbekannt | unbekannt | unbekannt | Platzbedarf | unbekannt | unbekannt |
| Aufbereitung | Reinigung / mögliche Anpassung | Baufirma | unbekannt | unbekannt | entfällt | Reinigung/Zuschnitt? | unbekannt | unbekannt | Oberflächen und Anschlüsse | unbekannt | [S1], [S3] |
| Planung | Einfamilienhaus aus Platten entwickeln | Biele/Asam-Kontext | stockbasierter Entwurf | unbekannt | entfällt | unbekannt | statische Nachweise unbekannt | unbekannt | Raster vs. Wohnwünsche | Entwurf innerhalb Bauteillogik | [S3] |
| Genehmigung | unbekannt | Behörden/Planer | unbekannt | unbekannt | entfällt | entfällt | unbekannt | unbekannt | Reuse-Nachweise | unbekannt | unbekannt |
| Wiedereinbau | Montage der Platten | Bauunternehmen | Kranmontage | Kran | entfällt | Remontage | unbekannt | Baustellenkoordination | schwere Elemente | Kranmontage | [S3] |
| Monitoring | unbekannt | unbekannt | unbekannt | unbekannt | entfällt | entfällt | unbekannt | unbekannt | Langzeitdaten fehlen | unbekannt | unbekannt |

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Wiederverwendete WBS70-Wand- und Deckenplatten bilden Haupttragwerk | Tragfähigkeit, Gebrauchstauglichkeit | unbekannt | unbekannt | Bauteile aus anderem Gebäude | statische Nachweise erforderlich | [S1] |
| Lastabtragung | Wand-/Deckensystem im Flachdachhaus | Vertikal- und Horizontallasten | unbekannt | unbekannt | neue Lagerung/Fugen | unbekannt | [S1] |
| Verbindung | Anschlussdetails unbekannt | kraftschlüssige Fügung | unbekannt | unbekannt | alte Verbindungsstellen | unbekannt | unbekannt |
| Brandschutz | Stahlbetonbauteile mit unbekannter Betondeckung | Feuerwiderstand Wohnhaus | unbekannt | unbekannt | Schnittkanten/Fugen | unbekannt | unbekannt |
| Schallschutz | unbekannt | Wohnkomfort | unbekannt | unbekannt | Plattenfugen | unbekannt | unbekannt |
| Feuchte | unbekannt | Feuchteschutz Dach/Wand | unbekannt | unbekannt | Bestandplatten + neue Dämmung | unbekannt | unbekannt |
| Wärmeschutz | Presse nennt Möglichkeit, Rohbauersparnis in Haustechnik/Dämmung zu investieren | Energieanforderungen | unbekannt | unbekannt | Betonplatten thermisch schwach | Dämmung/Technik unbekannt | [S3] |
| TGA-Integration | unbekannt | Leitungsführung | unbekannt | unbekannt | Bohrungen/Schlitze in Altplatten | unbekannt | unbekannt |
| Barrierefreiheit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Dauerhaftigkeit | Bauteile ca. 21 Jahre alt bei Wiederverwendung | Restlebensdauer | unbekannt | unbekannt | Alterung, Bewehrungskorrosion | Prüfung nötig | [S1] |
| Zulassung/Haftung | nicht öffentlich dokumentiert | Bauaufsicht, Haftung | unbekannt | unbekannt | gebrauchte tragende Bauteile | unbekannt | unbekannt |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Wandplatten wiederverwendet | 22 | Stück | PRECS-Falldatenbank | Empfängerhaus | [S1] | belegt |
| Deckenplatten wiederverwendet | 27 | Stück | PRECS-Falldatenbank | Empfängerhaus | [S1] | belegt |
| Bauteile gesamt | 49 | Stück | Summe aus PRECS-Angaben | Empfängerhaus | [S1] | belegt |
| Betonvolumen | 118 | m³ | PRECS-Falldatenbank | wiederverwendete Fertigteile | [S1] | belegt |
| Fläche | ca. 200 | m² | Presseangabe | Einfamilienhaus | [S3] | teilweise belegt |
| Distanz Spender–Empfänger | 8 oder 17 | km | PRECS-Falldatenbank | Transport | [S1] | teilweise belegt |
| Bauteilalter | ca. 21 | Jahre | PRECS-Falldatenbank | Plattenbauteile | [S1] | belegt |
| Baujahr / Start | 2005 | Jahr | PRECS-Falldatenbank | Empfängerprojekt | [S1] | belegt |
| Baukosten | 840 | EUR/m² | Presseangabe nach Biele | Gesamtbaukosten? unklar | [S3] | teilweise belegt |
| Vergleichswert Baukosten | 1.100 | EUR/m² | Presseangabe nach Biele | Vergleich Deutschland, unklar | [S3] | teilweise belegt |
| Kostenwirkung PRECS | -15 | % | JCP Appendix, Quelle Heyn et al. | Vergleich zu konventioneller Bauweise | [S1] | teilweise belegt |
| CO₂-Einsparung | unbekannt | t CO₂e | unbekannt | unbekannt | unbekannt | unklar |
| Abfallvermeidung | unbekannt | t / m³ | unbekannt | unbekannt | unbekannt | unklar |
| Energiebedarf | unbekannt | kWh/m²a | unbekannt | Betrieb | unbekannt | unklar |
| U-Wert | unbekannt | W/m²K | unbekannt | Bauteil | unbekannt | unklar |

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Akzeptanz alter Platten | sozial/wirtschaftlich | DDR-Plattenbauteile gelten als belastetes Image | Bauherren müssen überzeugt werden | Wirtschaft, Material | Kostenvorteil und Qualität kommunizieren | Reuse braucht Narrative plus Zahlen | [S3] |
| Tragfähigkeitsnachweis | technisch/rechtlich | gebrauchte tragende Fertigteile | Genehmigungs-/Haftungsrisiko | Prüfung, Norm, Recht | Prüf- und Nachweiskonzept | Alte Bauteile brauchen neue Dokumentation | unbekannt |
| Bauteilraster | gestalterisch/technisch | WBS70-Standardabmessungen | Entwurfsfreiheit begrenzt | Bauteil, Methode | Entwurf aus Bestand / ggf. Zuschnitt | stockbasierter Entwurf ist zentral | [S1], [S3] |
| Logistik | logistisch | schwere großformatige Elemente | Transport- und Kranbedarf | Logistik | kurze Distanzen nutzen | Nähe zum Spendergebäude ist entscheidend | [S1] |
| Dokumentationslücken | dokumentarisch | frühe Pilotprojekte, verstreute Quellen | viele Detailfelder unbekannt | Dokument, Bericht | Primärberichte nachrecherchieren | Forschungsfälle brauchen offene Daten | [S1] |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** projektbezogene Gewinnung aus einem rückgebauten Marzahner Plattenbau; keine Bauteilbörse belegt.
- **Bauteilbörse / Quelle:** Spendergebäude Marzahner Elfgeschosser / WBS70-Plattenbau; genaue Adresse unbekannt.
- **Kostenwirkung:** Presse nennt 840 EUR/m² und einen Vergleichswert von 1.100 EUR/m²; die PRECS-Auswertung nennt für C31 eine Kostenreduktion von -15 % gegenüber konventioneller Bauweise. Beide Werte sind quellenabhängig und nicht als geprüfte Abrechnung interpretieren.
- **Zeitwirkung:** unbekannt.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** erhöht für Demontage, Sortierung, Transport und Nachweis; genaue Stunden unbekannt.
- **Lagerung:** unbekannt.
- **Marktbarrieren:** Akzeptanz, Nachweis, Koordination, fehlende Bauteilpässe.

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** laut Presse von außen nicht mehr erkennbar; genaue Fassadengestaltung unbekannt.
- **räumliche Transformation:** hoch; Platten aus industriellem Großwohnungsbau werden zu einem individuellen Einfamilienhaus.
- **Atmosphäre / Ausdruck:** unbekannt.
- **Umgang mit Spuren:** Spuren der Platten wahrscheinlich durch neue Hülle/Oberflächen überformt; nicht belegt.
- **sozialer Wert:** Demonstration, dass rückgebaute DDR-Platten nicht nur Abfall sind, sondern tragende Ressourcen.
- **Denkmal- oder Bestandswert:** unbekannt.
- **Kritik / Grenzen:** kleiner Maßstab; geringe Sichtbarkeit; unvollständige technische Dokumentation öffentlich.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** Bauakten, Detailstatik, Anschlussdetails, Norm-/Genehmigungsgrundlage, Schadstoffprüfung, genaue Dämmung/TGA, Langzeitmonitoring.
- **Neue Entitäten sinnvoll:** Spendergebäude, Pilotserie, Rohbaukostenvorteil, Bauteilalter.
- **Fehlende Daten:** genaue Adresse des Spendergebäudes, tatsächliche Bauteillage, Bauteilqualitäten, Prüfprotokolle, CO₂-/Abfallbilanz.
- **Zu prüfende Quellen:** Heyn et al. 2008b, Mettke 2008/2010, Asam 2007a/b, IEMB/TU Berlin, Conclus-Projektarchiv, Bauakten Mehrow.

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja, aber als kleiner Haupt-/Vergleichsfall; nicht mit Schildow doppelt vermischen.
- **5 wichtigste Fakten:**
  1. Mehrow ist ein gebautes Pilotwohnhaus von 2005.
  2. Wiederverwendet wurden 22 Wandplatten und 27 Deckenplatten des WBS70-Systems.
  3. Das wiederverwendete Betonvolumen beträgt 118 m³.
  4. Presse nennt ca. 200 m² Wohnfläche und 840 EUR/m² Baukosten.
  5. Der Fall belegt tragende Wiederverwendung im Wohnhausmaßstab.
- **5 wichtigste Bauteile:** WBS70-Wandplatten; WBS70-Deckenplatten; Betonfertigteilfugen; Dach/Deckenaufbau; Hülle/Dämmung als nicht dokumentierte Schnittstelle.
- **5 wichtigste Hürden:** Nachweis, Logistik, Akzeptanz, Bauteilraster, Dokumentationslücken.
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Kurze Transportdistanzen machen schwere Betonbauteile plausibler.
  2. Fertigteilsysteme mit standardisierten Geometrien können Reuse erleichtern.
  3. Kostenargumente sind für Bauherren zentral.
  4. Sichtbare Reuse-Ästhetik ist nicht zwingend; der Wert kann im Tragwerk liegen.
  5. Frühzeitige Forschung/Planung ersetzt fehlende Marktstrukturen teilweise.
- **5 offene Fragen:** Prüfberichte; genaue Bauteilpositionen; Anschlussdetails; CO₂-Bilanz; langfristiges Verhalten.

## Quellen und Links

- [S0] Ausgangsliste des Nutzers: `gebäude4_wiederverwendung_direct_reuse_examples.md`, Eintrag 18.
- [S1] Küpfer, C.; Bastien-Masse, M.; Fivet, C. (2023): *Reuse of concrete components in new construction projects: Critical review of 77 circular precedents*, Journal of Cleaner Production. https://www.sciencedirect.com/science/article/pii/S0959652622048090
- [S2] ScienceDirect Topics / Appendix-B-Auszug zur PRECS-Fallliste. https://www.sciencedirect.com/topics/engineering/inverset
- [S3] taz (2006): *Die Wiedergeburt der Platte*. https://taz.de/Die-Wiedergeburt-der-Platte/!493469/
- [S4] Deutschlandfunk Kultur (2005): *Abbruch und Aufbau*. https://www.deutschlandfunkkultur.de/abbruch-und-aufbau-100.html
