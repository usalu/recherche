---
entity: "fallstudie"
id: "Ferme_du_Rail_Paris"
title: "La Ferme du Rail, Paris — Fallstudie Direct Reuse / zirkuläres Bauen"
build_status: "promoted_phase42"
legacy_paths:
  - "Gebäude\\Ferme_du_Rail_Paris.md"
node_kind: "core"
bauobjekt:
  - "Ferme_du_Rail_Paris"
projekt:
  - "Ferme_du_Rail_Paris"
---

# La Ferme du Rail, Paris — Fallstudie Direct Reuse / zirkuläres Bauen

## Legacy Content

### Legacy Source: Gebäude\Ferme_du_Rail_Paris.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Ferme_du_Rail_Paris
- Secondary targets: projekt/Ferme_du_Rail_Paris; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# La Ferme du Rail, Paris — Fallstudie Direct Reuse / zirkuläres Bauen

**Stand:** 2026-05-06  
**Arbeitsregel:** Bio-basierte Baustoffe, Kreislaufnutzung organischer Abfälle und Sozialprogramm sind wichtig, zählen aber nur dann als Direct Reuse, wenn tatsächlich Bau-/Hüll-/Raum-/Technikbauteile wiederverwendet wurden.

## 1. EINORDNUNG

- **Entscheidung:** VERGLEICHSFALL
- **Bewertung:** ★★★☆☆
- **Begründung:** Gebautes Projekt mit belegter Wiederverwendung fester Bau- und Ausbauelemente: Granitbordsteine/-steine, bituminöse und Betonblöcke für Außenflächen, Stein-/Dachterrassenplatten, Fliesen/Fayencen aus Restbeständen, Holzfensterrahmen als Dachterrassen-Akroterien/Pflanztröge/Geländer und als Holzpflaster/Parkett, Holz für feste Schränke, textile/rezyklierte Fasern als Sonnenschutz. Tragende Reuse wurde im Prozess untersucht, aber mehrere Optionen wurden als zu schwierig bzw. nicht umgesetzt beschrieben.
- **Vertrauensgrad:** belegt
- **Warnung Bestandserhalt:** nein — Neubau auf schwierigem Grundstück; kein Bestandstragwerk als Bewertungsbasis.
- **Warnung Möbel/Dekoration:** ja — lose Möbel nicht zählen; feste Schränke / bauliche Einbauten zählen nur soweit fest eingebaut.
- **Projektstatus:** gebaut

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | La Ferme du Rail | untersuchtes Projekt | [S1], [S2], [S3], [S4] | belegt | urbane Landwirtschaft + Wohnen + Restaurant |
| Ort | 2 bis rue de l’Ourcq, 75019 Paris | Standort | [S2], [S4] | belegt | an der Petite Ceinture |
| Gebäude | Neubauensemble | Bauwerk | [S2], [S4] | belegt | Wohngebäude R+3 und Serre/Restaurant |
| Projekt | Réinventer Paris 1 / Ourcq-Jaurès | Entstehungskontext | [S2], [S3], [S4] | belegt | Wettbewerb / urbane Innovation |
| People | Grand Huit | Architekt | [S2], [S3], [S4] | belegt | Clara Simay / Grand Huit in Quellen |
| People | Bellastock | AMO / Reuse-Logistik | [S1], [S3] | belegt | Prospektion, Logistikkette, Plananpassung |
| People | Travail & Vie | Betreiber / soziale Integration | [S2], [S4] | belegt | Integration durch Arbeit |
| People | Réhabail | Bauherr / privater Auftraggeber | [S2] | belegt | Quelle Ekopolis |
| People | Albert & Compagnie | Nachhaltigkeitsberatung | [S1], [S3] | belegt | Nachhaltigkeit / Reuse-Beteiligung |
| People | Pouget Consultants | Thermik | [S1], [S3] | belegt | Ingenieur Thermik |
| People | Scoping | BE TCE | [S1] | belegt | Gesamttechnik |
| People | Mélanie Devret | Landschaftsplanung | [S1], [S3] | belegt | Landschaft |
| People | Philippe Peiger | urbaner Agro-Ökologe | [S1], [S3] | belegt | Landwirtschaft |
| Reuse-Strategie | Material- und Bauteilwiederverwendung | zentraler Ansatz | [S1], [S2], [S3] | belegt | v.a. Ausbau/Außenraum/Hülle |
| Bauteil | Holzfensterrahmen | wiederverwendet als Akroterie/Pflanztröge/Geländer und Holzpflaster | [S2] | belegt | neue Funktionen |
| Bauteil | Granitbordsteine | wiederverwendet als Stützmauer | [S2] | belegt | Außenraum |
| Bauteil | Bitumen-/Betonblöcke | Außenwege | [S2] | belegt | aus Rückbauten |
| Bauteil | Fliesen/Fayence | Badwände / Beläge | [S2] | belegt | teils aus Restbeständen |
| Kennwert | 90 % biosourced und/oder reused, Trockenbauweise | Projektkennwert | [S2] | belegt | nicht reiner Reuse-Anteil |
| Kennwert | 2.300 m² / 1.000 m² gebaut | Maßstab | [S3] | belegt | CMS-Quelle |
| Kennwert | 830 m² SDP + 1.466 m² nicht spezifiziert | Fläche | [S2] | teilweise | Ekopolis differenziert |
| Hürde | geringe Grundstücksgröße / keine Lagerfläche | Logistik | [S2] | belegt | Gisements verpasst |
| Methode | LEAN-Planung | Projektsteuerung | [S2] | belegt | Förderung Gewerkeabstimmung |
| Prüfung | visuelle Analyse, Risikobewertung durch Bureau de contrôle | Bauteilfreigabe | [S2] | belegt | kein Permis d’expérimenter nötig |
| Norm | unbekannt | keine Normnummer belastbar | — | unbekannt | — |
| Software | Entscheidungshilfe-Tool | Auswahl bei kurzfristigen Gisements | [S2] | teilweise | Name unbekannt |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Opportunitäts-Gisement | Materialverfügbarkeit war kurzfristig und ortsabhängig. | Entscheidung, ob ein Gisement bis zum Folgetag geborgen wird | Bauteilbörse, Logistik, Prozessphase |
| Risikobasierte Freigabe | Viele Bauteile wurden nicht über ATEx, sondern über Einzelfallrisiko bewertet. | visuelle Prüfung + Risikoeinschätzung Büro de contrôle | Prüfung, Norm, Recht |
| Sozialer Baustellenprozess | Reuse und Low-Tech wurden mit Eingliederungsarbeit verbunden. | Unternehmen / Vereine mit Personen in Wiedereingliederung | People, Wirtschaft, Prozessphase |

## 3. FALLSTUDIE

- **Name:** La Ferme du Rail.
- **Ort:** 2 bis rue de l’Ourcq, Paris 19e, Frankreich.
- **Gebäude:** Neubauensemble mit Wohngebäude, Restaurant, Gewächshaus, urbaner Landwirtschaft.
- **Projekt:** Gewinner Réinventer Paris; sozial-ökologisches Agri-urbanes Projekt an der Petite Ceinture.
- **Beteiligte People / Akteure:** Grand Huit, Réhabail, Travail & Vie, Bail pour tous, APIJ, Ferme de Jade, Bellastock, Albert & Compagnie, Pouget Consultants, Scoping, Mélanie Devret, Philippe Peiger, BTP Consultants, Toerana Habitat, Gamba, R-are.
- **Architekt:** Grand Huit; Quellen nennen Clara Simay / Grand Huit.
- **Tragwerksplaner:** Julien Virgili laut Circular Material Systems; weitere Tragwerksdetails unbekannt.
- **Bauherr:** Réhabail laut Ekopolis; City of Paris / Grand Paris in CMS als Client-Kontext genannt.
- **Zeitraum:** 2014–2019 laut Circular Material Systems; Lieferung 2019.
- **Ursprüngliche Nutzung:** Grundstück auf / bei ehemaliger Bahntrasse; zuvor SNCF-Remblai und informelle Garage laut Ekopolis.
- **Neue Nutzung:** urbane Landwirtschaft, Restaurant, Wohnen für 15 Personen in Reintegration und 5 Horticulture-Studierende, Ausbildung/soziale Integration.
- **Fläche / Maßstab:** 2.300 m² Gesamt / 1.000 m² gebaut nach CMS; Ekopolis nennt 830 m² SDP und 1.466 m² nicht näher spezifiziert.
- **Schutzstatus / Denkmalstatus:** unbekannt.
- **Quellenlage:** gut für Reuse-Elemente, Logistik und Nutzung; begrenzt für Mengen vieler Bauteile, Prüfprotokolle, Verbindungstechnik.

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; Materialwiederverwendung; Umnutzung von Bauteilen mit Funktionswechsel.
- **Hauptniveau:** Außenraum, Hülle/Absturzsicherung/Akroterie, räumlicher Innenausbau, Beläge, Material.
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Es handelt sich um Neubau. Bio-basierte Holz-/Strohbauweise und Recycling zählen nicht automatisch als Direct Reuse. Direct Reuse sind konkret wiederverwendete Fensterrahmen, Steine/Bordsteine, Platten, Fliesen, Holz und feste Einbauten.
- **Warum ist der Fall relevant?** Der Fall zeigt Reuse trotz Neubau, engem Grundstück, kurzfristigen Gisements und sozialem Bauprozess. Besonders interessant sind Bauteile mit neuer Funktion: Fenster werden Akroterie/Pflanztröge/Geländer und Holzpflaster.

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Holzfensterrahmen / Châssis bois | Holz/Glas | Pariser Sozial-/Bestandsfenster, genaue Quelle unbekannt | Fenster | Akroterie, Pflanztröge, Geländer der Dachterrasse | unbekannt | nein | ja | teils | nein | Vorbereitung, Zuschnitt/Anpassung | unbekannt | Bureau de contrôle beteiligt | Absturzsicherung, Abdichtung, Nutzbarkeit Dach | unbekannt | Mehrfachfunktion / Abdichtung | [S2] | teilweise |
| Holzfensterrahmen | Holz | s.o. | Fenster | Holzpflaster / Parkett bois de bout in Gemeinschaftsraum | unbekannt | nein | ja | nein | nein | Feuillures nicht abgeschnitten; puzzleartige Montage | Bodenverlegung | Bureau de contrôle akzeptierte geringes Risiko | Ebenheit, Abrieb, Brandschutz | unbekannt | hoher Arbeitsaufwand | [S2] | teilweise |
| Granitbordsteine | Granit | Pariser öffentliche Raum-/Straßenbau-Baustellen | Bordstein | Stützmauer am Gemüsegarten | unbekannt | teils als Stützmauer | ja | außen | nein | Wiederverwendung ohne Bindemittel als „pierre sèche“ | Trockenmauer | unbekannt | Stabilität, Dauerhaftigkeit | unbekannt | Logistik / Gewicht | [S2] | teilweise |
| Bitumen-/Betonblöcke | Bitumen/Beton | Rückbauten | Abbruchmaterial | Außenwege / Zirkulationen | unbekannt | nein | ja | außen | nein | Auswahl / Einbau | unbekannt | unbekannt | Trittsicherheit, Entwässerung | unbekannt | Heterogenität | [S2] | teilweise |
| Steinplatten von Dachterrassen / Büro-Fußbodenplatten | Stein | Renovierung Bürogebäude La Défense / Büro-Fußböden | Dach-/Bodenplatten | geplant Dachterrasse; teilweise Boden-/Füllplatten | unbekannt | nein | ja | außen/innen | nein | Lagerung, Einbauversuch | unbekannt | unbekannt | Frost-/Feuchteresistenz, Bruchfestigkeit | unbekannt | Feuchte/Frost führte zu Rissen; Einsatz geändert | [S2] | teilweise |
| Fliesen / Fayence | Keramik | Restbestand eines Handwerkers | Fliesen | Badwandbelag | unbekannt | nein | ja | nein | nein | Calepinage, Umnutzung von Boden zu Wand | Kleber/Untergrund unbekannt | PV und Produktdaten vorhanden | Feuchte, Haftung, ggf. Rutsch bei Boden | unbekannt | Bodenanwendung zu komplex wegen Abdichtung | [S2] | teilweise |
| Holz für Schränke | Holz | wiederverwendet, Herkunft unbekannt | unbekannt | feste Schränke in CHRS und Studierendenwohnungen | unbekannt | nein | ja | nein | nein | unbekannt | eingebaut | unbekannt | Gebrauch, Brandschutz | unbekannt | Möbelgrenze: nur fest eingebaute Schränke zählen | [S2] | teilweise |
| textile / rezyklierte Fasern | Fasern | recycelt / reused nach Tissage | unbekannt | Sonnenschutzstores Restaurant | unbekannt | nein | nein | Hülle/Sonnenschutz | nein | Weben / Herstellung | unbekannt | unbekannt | UV, Brandschutz, Bedienung | unbekannt | eher Recycling/Reusing, genaue Herkunft unklar | [S2] | teilweise |
| Metallteile | Metall | unbekannt | Metallbauteile | untersucht als Jardinière/Garde-corps | unbekannt | unbekannt | ja | außen | nein | Transformation | unbekannt | unbekannt | Absturzsicherung | unbekannt | Umsetzung unklar / kompliziert | [S1] | ja |
| Dallettes préfabriquées | Beton | unbekannt | Betonplatten | untersucht als tragender Boden | unbekannt | potenziell | ja | nein | nein | unbekannt | unbekannt | unbekannt | Tragfähigkeit | unbekannt | Kosten der Transformation, Deponiemethode | [S1] | ja / nicht als umgesetzt werten |
| Holz-/Strohbau | Holz/Stroh | regionale Bio-Materialien | neu | Tragwerk / Dämmung | Hauptkonstruktion | ja | ja | ja | nein | Neubau | Holzbau | unbekannt | Tragwerk, Wärmeschutz, Brandschutz | unbekannt | kein Direct Reuse | [S3], [S4] | nicht Reuse |

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Grundstück und Nutzungskonflikte analysieren | Grand Huit, Projektteam | holistische Planung | LEAN-Planung | — | — | Bodenuntersuchung / Verschmutzung belegt | enger Ort | belastete Böden, Zugang | SNCF-Gleis temporär für Baustelle genutzt | [S2] |
| Bauteilinventar | Bedarf und mögliche Reuse-Gisements suchen | Bellastock, MOA, Unternehmen | Prospektionsbilanz | Entscheidungshilfe-Tool, Name unbekannt | selektive Demontage bei Spendern | unbekannt | visuell | kurzfristige Gisements | wenig Lagerfläche | schnelle Entscheidungen | [S1], [S2] |
| Schadstoffprüfung | Bodenverschmutzung festgestellt | unbekannt | Bodenanalyse | unbekannt | — | — | belegt allgemein | — | Altlasten / Hydrokarbonabfälle | Phyto-Sanierung nicht möglich; andere Maßnahmen | [S2] |
| Rückbau / Ausbau | Gisements bei Spendern sichern | Bellastock / MOA / Unternehmen | selektiv | unbekannt | selektiv | unbekannt | unbekannt | dezentral | Gisements können schnell verloren gehen | MOA sammelte Gisements | [S2] |
| Transport | Material aus Paris/Region/Normandie/Bretagne | MOA, Unternehmen | lokale/regionale Beschaffung | unbekannt | — | — | unbekannt | Radius teils 65 km für Hauptmaterialien | begrenzte Lagerfläche | Material möglichst roh und wenig transformiert | [S3] |
| Lagerung | Zwischenlagerung | MOA / Unternehmen | unbekannt | unbekannt | — | — | unbekannt | wenig Platz | Dachplatten nahmen Feuchte/Frost auf | Einsatzänderung | [S2] |
| Aufbereitung | Fenster als Boden/Akroterie; Fliesen kalepinieren | R-are, Unternehmen | handwerkliche Anpassung | unbekannt | — | Schneiden/Sortieren/Montage | Bureau de contrôle | vor Ort | zeitintensiv | Eingliederungs-/Fachakteure | [S2] |
| Planung | Reuse spät in Studienphase integriert | Grand Huit, Albert & Co, Bellastock | dynamische Planung | Entscheidungshilfe | — | — | visuell + Risiko | Entwurf passt sich Material an | späte Integration | flexible Anpassung grafischer Unterlagen | [S1], [S2] |
| Genehmigung | kein „Permis d’expérimenter“ nötig laut Ekopolis | Projektteam, Kontrollbüro | Einzelfallauswahl | unbekannt | — | — | visuell + Risikobewertung | — | ATEx vermeiden | traditionelle Einbautechniken | [S2] |
| Wiedereinbau | Reuse-Bauteile als feste Elemente montieren | Unternehmen, R-are, Travail & Vie u.a. | klassische Technikähnlichkeit | unbekannt | — | vorbereitet | Kontrollbüro | Baustelle eng | Koordination | LEAN / gewerkeübergreifende Abstimmung | [S2] |
| Monitoring | Rückmeldungen / Erfahrungsberichte | Ekopolis, Bellastock | Fallstudie | unbekannt | — | — | — | — | Wissenstransfer | publizierte Projektblätter | [S1], [S2], [S3] |

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Haupttragwerk neu aus Holz/Stroh; Reuse-Tragwerksideen untersucht, aber Umsetzung unklar | Tragfähigkeit | unbekannt | unbekannt | Betonplatten als tragender Boden kompliziert | nicht als zentraler Reuse-Fall werten | [S1], [S3] |
| Lastabtragung | Granit-Stützmauer und ggf. Außenraumelemente | lokale Stabilität | unbekannt | unbekannt | Gewicht / Trockenmauer | Montage ohne Bindemittel | [S2] |
| Verbindung | Fensterrahmen als Akroterie/Geländer und Holzpflaster | sichere Befestigung, Abdichtung | unbekannt | Kontrollbüro | neue Funktionen mit mehreren Anforderungen | feine Abstimmung Entwurf + Büro de contrôle | [S2] |
| Brandschutz | Holz/Stroh/Reuse-Innenausbau relevant | Brandverhalten, Flucht | unbekannt | unbekannt | Holzfenster als Boden / Schränke | Risiko gering bei Bodenverwendung laut Quelle | [S2] |
| Schallschutz | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Feuchte | Dachplatten wurden durch Feuchte/Frost geschädigt | Frostbeständigkeit, Feuchte | unbekannt | Einbaubeobachtung | Lagerung schadete Platten | anderer Einsatz als Füll-/Bodenplatten | [S2] |
| Wärmeschutz | Bio-basierte Gebäudehülle, Gewächshaus separat | thermische Trennung | unbekannt | unbekannt | Gewächshaus und Restaurant verschiedene Anforderungen | Räume getrennt | [S3] |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Luftdichtheit | Stroh-/Holzbau, nicht Reuse-Schwerpunkt | Luftdichtheit | unbekannt | unbekannt | unbekannt | Frédéric Cousin als Stroh-/Luftdichtheitssystem-Partner in CMS | [S3] |
| TGA-Integration | kein zentrales Reuse-TGA belegt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Barrierefreiheit | Aufzug/Betonkern nötig | PMR-Zugang | unbekannt | unbekannt | Kosten/Betonanteil | Betonkern für Aufzug/Lasten | [S2] |
| Dauerhaftigkeit | Außenreuse stark exponiert | Frost, Wasser, Verschleiß | unbekannt | Kontrollbüro / visuell | Plattenbruch, Holz außen | Einzelfallrisiko und Funktionsänderung | [S2] |
| Wartung | Garten-/Dachterrassenelemente | Wartung Pflanztröge/Geländer | unbekannt | unbekannt | Mehrfachnutzung | unbekannt | [S2] |
| Zulassung | kein Permis d’expérimenter; keine ATEx nötig laut Quelle | Versicherbarkeit | unbekannt | Kontrollbüro | Nachweisaufwand | traditionelle Einbaulogiken | [S2] |
| Haftung | Materials durch pose-Los versichert | Verantwortlichkeit Fachunternehmen | unbekannt | Risikoanalyse | Haftung bei alten Materialien | Materialien durch ausführendes Los versichert | [S2] |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Gesamtfläche | 2.300 | m² | unbekannt | Projekt | [S3] | belegt |
| gebaute Fläche | 1.000 | m² | unbekannt | Built | [S3] | belegt |
| SDP | 830 | m² | unbekannt | Surface de plancher | [S2] | belegt |
| weitere Fläche | 1.466 | m² | unbekannt | Quelle „Non précisé“ | [S2] | teilweise |
| Baukosten | 3,3 | Mio. € HT | unbekannt | travaux | [S2] | belegt |
| Anteil biosourcé und/oder réemployé | 90 | % | unbekannt | Materialien in Trockenbauweise | [S2] | belegt, aber kein reiner Reuse-Anteil |
| Personen in Wiedereingliederung | 15 | Personen | Programm | Nutzung | [S2], [S3] | belegt |
| Studierende | 5 | Personen | Programm | Nutzung | [S2], [S3] | belegt |
| Transport-/Sourcing-Radius Hauptmaterialien | 65 | km | unbekannt | Hauptmaterialien laut CMS | [S3] | belegt |
| Menge Holzfenster reused | unbekannt | — | — | — | [S2] | nicht quantifiziert |
| CO₂-Einsparung | unbekannt | — | — | — | — | unbekannt |
| Abfallvermeidung | unbekannt | — | — | — | — | unbekannt |
| Kostenwirkung Reuse | ohne Mehrkosten insgesamt behauptet | — | unbekannt | Reuse vs. neu | [S2] | teilweise; keine Zahl |
| Bauzeit | unbekannt | — | — | — | — | unbekannt |
| U-Wert | unbekannt | — | — | — | — | unbekannt |

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Reuse spät in Studienphase | prozessual | Materialreuse nicht von Anfang an voll integriert | Zeitdruck, Opportunitätsentscheidungen | Prozessphase, Methode | Entscheidungshilfe, flexible Pläne | Reuse früh starten | [S2] |
| Kein Lagerplatz | logistisch | kleines Grundstück | Gisements verpasst, Schäden möglich | Logistik, Bauteil | schnelle Entscheidungen; MOA sammelte Material | Lagerstrategie ist zentral | [S2] |
| Platten durch Feuchte/Frost beschädigt | technisch/logistisch | Lagerung | geplanter Einsatz scheiterte; Kranmehrkosten | Bauteil, Lagerung | Einsatzänderung / neues Material | Witterungsschutz beim Lagern | [S2] |
| Bodenfliesen in Nassräumen | technisch/rechtlich | Abdichtung und Klassifizierung anspruchsvoll | Bodenanwendung verworfen | Fliesen, Prüfung | Verwendung als Wandbelag | Leistungsanforderung durch neuen Einsatz reduzieren | [S2] |
| Hoher Arbeitsaufwand Holzfenster-Boden | wirtschaftlich/sozial | puzzleartige Verlegung ohne Materialverlust | zeitintensiv | Aufbereitung, People | R-are / Eingliederungsakteur | Arbeitsintensive Reuse braucht passende Organisation | [S2] |
| Tragwerksreuse schwer umsetzbar | technisch/wirtschaftlich | Kosten der Transformation, Demontagemethode | geplante Beton-/Metalloptionen nicht gesichert | Tragwerkssystem, Bauteil | Fokus auf weniger kritische Anwendungen | nicht jede Reuse-Idee ist wirtschaftlich | [S1] |
| Altlasten am Grundstück | technisch/wirtschaftlich | Hydrokarbonabfälle, frühere Nutzung | hoher Aufwand für Boden/VRD | Ort, Prozessphase | alternative Baustellenlogistik | Reuse-Projekt kann durch Standortlasten überlagert werden | [S2] |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** privater/partnerschaftlicher Projektkontext; Réhabail als MOA laut Ekopolis; Réinventer Paris als Rahmen.
- **Bauteilbörse / Quelle:** kein einzelner Marktplatz; Bellastock/Projektteam suchte Gisements in Paris/Region, Normandie und Bretagne; MOA sammelte Gisements.
- **Kostenwirkung:** Ekopolis berichtet, dass das Ziel „kein Mehrpreis gegenüber neuen Materialien“ insgesamt gehalten wurde; keine belastbare absolute Kostenzahl für Reuse.
- **Zeitwirkung:** erhöht durch kurzfristige Gisements, Lagerung und Aufbereitung; keine Zahl.
- **Versicherung / Haftung:** Materialien wurden laut Ekopolis durch das Los versichert, das sie einbaute; keine ATEx, weil traditionelle Einbautechniken und Risikobewertung.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** bei Holzfenster-Boden hoch; keine Stundenzahl.
- **Lagerung:** kritische Hürde; Frost-/Feuchteschaden bei Platten.
- **Marktbarrieren:** kurzfristige Verfügbarkeit, fehlender Lagerplatz, Prüf-/Klassifizierungsanforderungen, fehlende Standardisierung.

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** hoch in Dachterrassen-Akroterien/Pflanztrögen/Geländern und Holzpflaster aus Fenstern; Außenmauern und Beläge sichtbar.
- **räumliche Transformation:** Neubau als mikro-dörflicher Landwirtschafts-, Wohn- und Lernort.
- **Atmosphäre / Ausdruck:** Low-tech, bioklimatisch, landwirtschaftlich; Materialspuren unterstützen soziale und ökologische Erzählung.
- **Umgang mit Spuren:** eher sichtbar und didaktisch; Details zu Erhalt der Patina unbekannt.
- **sozialer Wert:** sehr hoch durch Wiedereingliederung, Ausbildung, Restaurant und Quartiersbezug.
- **Denkmal- oder Bestandswert:** Bezug zur Petite Ceinture; formaler Denkmalschutz unbekannt.
- **Kritik / Grenzen:** Reuse-Anteil nicht als reine Zahl belegt; 90 %-Wert umfasst auch biosourcierte Materialien. Tragwerksreuse blieb begrenzt.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** exakte Mengen der reused Fenster, Steine, Platten, Fliesen; konkrete Normen; vollständige Prüfberichte; CO₂-Bilanz; Gewährleistung.
- **Neue Entitäten:** Opportunitäts-Gisement; risikobasierte Freigabe; Sozialer Baustellenprozess.
- **Fehlende Daten:** Massen, Transportdistanzen je Gisement, Kosten je Bauteil, Lagerort/-dauer, Prüfprotokolle, Lebensdauerannahmen.
- **Zu prüfende Quellen:** vollständige Ekopolis-Unterlagen, Grand Huit-Projektbericht, Bellastock-Projektakten, Kontrollbüroberichte.

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja, als Vergleichsfall.
- **5 wichtigste Fakten:**
  1. Neubau mit urbaner Landwirtschaft, Wohnen und Restaurant.
  2. 90 % der Materialien werden als biosourciert und/oder wiederverwendet beschrieben, aber kein reiner Reuse-Wert.
  3. Fensterrahmen wurden zu Akroterien/Pflanztrögen/Geländern und Holzpflaster umgenutzt.
  4. Reuse wurde spät integriert und erforderte schnelle Entscheidungen.
  5. Das Projekt verzichtete laut Ekopolis auf ATEx und nutzte traditionelle Einbaulogiken mit Risikobewertung.
- **5 wichtigste Bauteile:**
  1. Holzfensterrahmen.
  2. Granitbordsteine.
  3. Stein-/Bodenplatten.
  4. Fliesen/Fayence.
  5. Holz für feste Schränke / Innenausbau.
- **5 wichtigste Hürden:**
  1. kleines Grundstück / Lagerknappheit.
  2. Feuchte-/Frostschäden.
  3. hohe Arbeitszeit bei Umnutzung.
  4. technische Grenzen bei Nassräumen.
  5. nicht umgesetzte Tragwerksreuse-Ideen.
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Funktionswechsel kann Leistungsanforderungen entschärfen.
  2. Kontrollbüro früh einbeziehen.
  3. Reuse braucht Lager- und Wetterschutz.
  4. Sozialwirtschaftliche Akteure können arbeitsintensive Reuse tragen.
  5. Reuse im Neubau funktioniert auch ohne Bestand, wenn Gisements aktiv gesucht werden.
- **5 offene Fragen:**
  1. Welche genaue Menge an Fenstern wurde wiederverwendet?
  2. Welche CO₂-Effekte wurden bilanziert?
  3. Welche Bauteile wurden nach Prüfprotokoll freigegeben?
  4. Wie wurde die Absturzsicherung der Fenster-Akroterien detailliert nachgewiesen?
  5. Welche Kosten entstanden je Reuse-Bauteil?

## Quellen und Links

- [S1] Bellastock — „La Ferme du Rail“: https://www.bellastock.com/projets/la-ferme-du-rail/
- [S2] Ekopolis — „La Ferme du Rail“: https://www.ekopolis.fr/operations-batiment/la-ferme-du-rail
- [S3] Circular Material Systems — „Ferme du Rail“: https://circularmaterialsystems.com/en/case/05_ferme-du-rail/
- [S4] Grand Huit — „Ferme du Rail“: https://grandhuit.eu/projet/ferme-du-rail/
- [S5] ESBA / European Straw Building Association — „Ferme du rail“: https://strawbuilding.eu/ferme-du-rail/
- [S6] Batiactu — „La ferme du rail cultive l’économie circulaire“: https://www.batiactu.com/edito/ferme-rail-56126.php
