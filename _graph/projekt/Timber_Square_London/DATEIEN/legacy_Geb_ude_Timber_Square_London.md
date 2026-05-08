# Timber Square, London — Fallstudie Direct Reuse / Bauteilwiederverwendung

**Arbeitsstand:** 2026-05-06  
**Sprache:** Deutsch  
**Grundregel:** Gewertet werden nur wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Retained existing structure wird nicht als Direct Reuse gezählt, wenn sie am Ort bleibt und dieselbe Funktion behält.

---

## 1. EINORDNUNG

- **Entscheidung:** HAUPTFALL
- **Bewertung:** ★★★★☆
- **Begründung:** Timber Square ist ein großmaßstäbliches Büroprojekt mit sehr relevantem tragendem Direct Reuse von wiederverwendetem Stahl: je nach Quelle über 500 Stahlträger bzw. ca. 115–125 t reused steel, ermittelt und beschafft mit dem HTS Stockmatcher. Gleichzeitig ist ein großer Teil der Klimastrategie Bestandserhalt des Print Building und CLT-Hybridbau; dieser Bestandserhalt zählt nach der Grundregel nicht als Direct Reuse. Daher stark, aber nicht als Fünf-Sterne-Hauptfall.
- **Vertrauensgrad:** teilweise belegt
- **Warnung Bestandserhalt:** ja
- **Warnung Möbel/Dekoration:** ja; Empfangstresen aus wiederverwendetem Stahlträger ist ein fester Einbau, aber nicht bewertungsrelevantes Tragwerk.
- **Projektstatus:** im Bau / nahe Fertigstellung; Quellen nennen Q4 2025, 2026 oder „on site“. Übergabe/Handover ist zu verifizieren.

---

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Timber Square | Untersuchter Direct-Reuse-Fall | S1, S2, S3 | belegt | Büro-/Mixed-use-Campus |
| Gebäude | Print Building und Ink Building | Zwei Gebäudeteile: Umbau/Erweiterung + Neubau | S1, S2, S5 | belegt | Print: ehemaliges 1950s printworks; Ink: 15-storey Neubau |
| Ort | 25 Lavington Street / Bankside, Southwark, London SE1 | Standort | S1, S5 | belegt | London Borough of Southwark |
| Projekt | Net-zero / hybrid timber office redevelopment | Projektkontext | S1, S2, S4, S5 | belegt | Direct Reuse ist Teil eines größeren Low-carbon-Konzepts |
| Bauherr | Landsec | Client/Developer | S1, S2, S4, S5 | belegt | - |
| Architekt | Bennetts Associates | Architektur | S1, S4 | belegt | - |
| Tragwerksplaner | Heyne Tillett Steel / HTS | Structural Engineer | S1, S2 | belegt | entwickelte/benutzte Stockmatcher |
| People/Akteure | Landsec, Bennetts Associates, HTS, Mace, Hoare Lea, Alinea/T+T Alinea, Opera, Stora Enso, Hybrid Structures, Cleveland Steel & Tubes | Projektteam / Lieferkette | S1, S4, S8, S10 | belegt/teilweise | Rollen je Quelle |
| Reuse-Strategie | ex-situ Bauteilwiederverwendung von Stahl + Bestandserhalt + DfD | Reuse-Bewertung | S2, S3, S8 | belegt | Nur Stahlreuse und einzelne wiederverwendete Bauteile zählen als Direct Reuse |
| Bauteil | wiederverwendete Stahlträger | Hauptbauteil Direct Reuse | S2, S3, S7, S8 | belegt | Mengenangaben 115, 116 oder 125 t je Quelle |
| Bauteil | großer Stahlträger als Empfangstresen | fester Einbau aus vor Ort entnommenem Stahlträger | S3 | belegt | nicht für Tragwerksrating relevant |
| Bauteil | bestehende Struktur Print Building | Bestandserhalt | S1, S2, S4 | belegt | ca. 80 % erhalten; nicht als Direct Reuse zählen |
| Material | CLT und Stahl | Hybridtragwerk | S1, S2, S4, S8 | belegt | CLT nicht reused, aber kohlenstoffarme Strategie |
| Tool | HTS Reused Steel Stockmatcher | Matching von wiederverwendeten Stahlträgern | S2, S9 | belegt | Python-basiertes Tool |
| Datenmodell | Stock list / design list matching | Vergleich Bestandsstahl mit Designanforderungen | S9 | belegt | Materialmatching |
| Verbindung | reversible joints / non-composite structural design | DfD/Future Reuse | S3, S4 | belegt | Nicht selbst Direct Reuse, aber relevant |
| Prüfung | fire testing, acoustics, insurance, vibration performance at scale | Leistungsnachweise Hybrid-CLT/Stahl | S2 | belegt | spezifisch für Hybridbau; reused steel Prüfdetails unbekannt |
| Logistik | reused steel sourced from Cleveland Steel & Tubes laut Timber Development UK | Lieferkette Stahlreuse | S8 | teilweise belegt | genaue donor source unbekannt |
| Kennwert | >500 beams; ca. 115–125 t reused steel | tragender Direct-Reuse-Kennwert | S2, S3, S7, S8 | belegt/unklar | Quellen variieren |
| Kennwert | CO₂-Einsparung reused steel 216 oder 276 tCO₂e | Umweltkennwert | S1, S2, S3, S7 | unklar | Werte widersprechen sich |
| Hürde | fire, acoustics, insurance, vibration | technische Hürden des Hybridtragwerks | S2 | belegt | nicht nur Reuse |
| Norm/Recht | UKGBC Net Zero Carbon Buildings Framework; BREEAM Outstanding, WELL Platinum, NABERS 5 target | Projektbenchmarks | S2, S3, S4 | belegt | Normnummern/Regelwerke für Stahlreuse unbekannt |
| Wirtschaft | unbekannt | Kostenwirkung reused steel nicht publiziert | - | unbekannt | - |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Matching-Algorithmus | Reuse-Stahl wurde digital mit Designanforderungen abgeglichen | HTS Stockmatcher | verbindet Tool, Datenmodell, Bauteil |
| Stockholder / Reuse-Lieferant | Stahlreuse hängt an konkreten Lager-/Lieferantenbeständen | Cleveland Steel & Tubes | verbindet Bauteilbörse, Logistik, Wirtschaft |
| Retained-Structure-Anteil | Methodisch abgrenzen von Direct Reuse | 80 % Print Building retained | verbindet Gebäude, Kennwert, Warnung Bestandserhalt |
| Embodied-Carbon-Wertekonflikt | Quellen nennen 216 und 276 tCO₂e Einsparung | reused-steel carbon saving | verbindet Kennwert, Bericht, Datenqualität |

---

## 3. FALLSTUDIE

- **Name:** Timber Square
- **Ort:** Bankside / Southwark, London, UK; 25 Lavington Street, London SE1 0NZ
- **Gebäude:** Büro-/Mixed-use-Campus aus Print Building und Ink Building
- **Projekt:** Low-carbon redevelopment mit retained printworks, hybrid steel/CLT structure und reused steel
- **Beteiligte People / Akteure:** Landsec, Bennetts Associates, Heyne Tillett Steel, Mace, Hoare Lea, Alinea/T+T Alinea, Opera, Cleveland Steel & Tubes, Stora Enso, Hybrid Structures
- **Architekt:** Bennetts Associates
- **Tragwerksplaner:** Heyne Tillett Steel
- **Bauherr:** Landsec
- **Zeitraum:** Planung ab ca. 2019; Baubeginn/On site nach Quellen 2022/2023; Completion/Handover je nach Quelle Q4 2025 oder 2026; zu verifizieren
- **Ursprüngliche Nutzung:** ehemaliges 1950er printworks / Druckerei-Gebäude auf dem Standort; donor source des reused steel unbekannt bzw. Lieferant Cleveland Steel & Tubes
- **Neue Nutzung:** Büro, Retail/öffentlicher Raum, Mixed-use Campus
- **Fläche / Maßstab:** Quellen variieren: 52.026 m² GIA (HTS), 33.910 m² area (Bennetts), 365.000 sq ft workspace und 380.000 sq ft Gesamt-/Office/Retail/Public Space in Landsec/Mace-Quellen
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** gut für Projektteam, Reuse-Stahl-Mengenbereich, Stockmatcher und carbon claims; unklar bei Handoverstatus, genauen Stahlquellen, Norm-/Prüfdetails und Kosten

---

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ Bauteilwiederverwendung von Stahl; in-situ Bestandserhalt als Kontext; DfD/Future Reuse ergänzend
- **Hauptniveau:** Tragwerk; ergänzend feste Einbauten
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die über 500 reused steel beams / ca. 115–125 t steel sind Direct Reuse. Das Erhalten von ca. 80 % des Print Building ist wichtig für Low Carbon, zählt hier aber als Bestandserhalt und nicht als Direct Reuse. EAF-/scrap steel oder CLT sind nicht Direct Reuse.
- **Warum ist der Fall relevant?** Großmaßstäblicher kommerzieller Nachweis, dass digitale Bestands-/Designabgleiche reused steel in einem hochregulierten Büroprojekt ermöglichen können.

---

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Wiederverwendete Stahlträger | Stahl | Stockholder / Cleveland Steel & Tubes laut TDUK; donor buildings unbekannt | tragende Stahlträger | tragende Stahlträger, vor allem in/um Cores laut TDUK | >500 beams; ca. 115–125 t | ja | nein | nein | nein | matching, Beschaffung, ggf. Recondition/Fabrication unbekannt | Stahlanschlüsse; Details unbekannt | spezifische reused-steel Prüfung unbekannt | Tragfähigkeit, Schwingung, Brandschutz | EN/UK steel standards unbekannt | Matching, Verfügbarkeit, Zulassung | S2, S3, S7, S8 | donor source, Profile |
| Stahlträger für Empfangstresen | Stahl | vor Ort bei Demolition entnommen | Stahlträger | fester Empfangstresen in beiden Gebäuden | 1 großer girder geteilt/reconditioned | nein | ja | nein | nein | geteilt und wiederaufbereitet | Einbau als Möbel/fester Einbau | unbekannt | Nutzung/Innenausbau | unbekannt | zählt nicht als Tragwerk | S3 | Maße |
| Retained Print Building structure | Stahl/Beton unbekannt | bestehendes 1950er printworks | Tragwerk | weiterhin Tragwerk, erweitert | ca. 80 % retained | ja | nein | nein | nein | Verstärkung, Transferstrukturen | Bestand + neue Anschlüsse | unbekannt | erhöhte Lasten, sechs zusätzliche Geschosse | unbekannt | Bestandserhalt, nicht Direct Reuse | S1, S2, S4 | genaue Materialarten |
| CLT floor panels | Holz/CLT | neu, Lieferant Stora Enso laut TDUK | neu | Decken in Hybridstruktur | unbekannt | ja | nein | nein | nein | neu gefertigt | CLT spannt 6 m auf Stahlträger | fire/acoustic/vibration tests | Brand, Akustik, Schwingung | UK fire/insurance requirements unbekannt | nicht reused | S2, S8 | Mengen |
| Neue/recycled-content Stahlbauteile | Stahl | EAF/scrap steel | neu/recycelt | Tragwerk | >50 % scrap-EAF optimiert laut HTS | ja | nein | nein | nein | neue Produktion | unbekannt | unbekannt | Tragfähigkeit | unbekannt | Recycling, nicht Direct Reuse | S7 | Mengen |
| Fassaden-/Curtain-wall modules | Glas/Alu unbekannt | neu/vermutlich nicht reused | neu | Fassade | unbekannt | nein | nein | ja | nein | standardisiert | modular | unbekannt | Witterung, Wärme, Luft | unbekannt | DfMA, nicht Direct Reuse | S3 | Details |
| Major plant | TGA | neu/vermutlich nicht reused | neu | TGA | unbekannt | nein | nein | nein | ja | demontierbar geplant | demontierbar | unbekannt | Wartung, Austausch | unbekannt | Future DfD, kein aktueller Direct Reuse | S3 | Details |
| Türen | unbekannt | unbekannt | unbekannt | Türen | unbekannt | nein | ja | teilweise | nein | unbekannt | unbekannt | unbekannt | Brand/Schall | unbekannt | unbekannt | - | alles |
| Bodenaufbauten | unbekannt | unbekannt | unbekannt | Boden | unbekannt | nein | ja | nein | nein | unbekannt | unbekannt | unbekannt | Akustik/Brand | unbekannt | unbekannt | - | alles |
| Sanitär | unbekannt | unbekannt | unbekannt | Sanitär | unbekannt | nein | ja | nein | ja | unbekannt | unbekannt | unbekannt | Hygiene | unbekannt | unbekannt | - | alles |

---

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Print Building analysieren und zu erhaltende Struktur bestimmen | Landsec, Bennetts, HTS, Mace | retention/cut-and-carve | unbekannt | selektive Demolition | unbekannt | Bestandsanalyse | onsite | zusätzliche Lasten auf Bestand | Transferstrukturen, foundation pads | S2, S10 |
| Bauteilinventar | Design list und stock list für reused steel erstellen | HTS | reused steel matching | HTS Stockmatcher, Python | - | - | Abgleich Section/Length/Weight | Stockholder-Bestände | passende Träger finden | Algorithmisches Matching inkl. Offcuts | S9 |
| Schadstoffprüfung | unbekannt für reused steel | unbekannt | unbekannt | unbekannt | - | - | unbekannt | unbekannt | unbekannt | unbekannt | - |
| Rückbau | Demolition der westlichen Bestandsstruktur / Entnahme vor Ort für Empfangsträger | Mace/Abbruchteam unbekannt | cut-and-carve/demolition | unbekannt | selektiv | reconditioned girder | unbekannt | onsite | Wertstoffe sichern | Wiederverwendung im Empfang | S3, S10 |
| Ausbau | Reused steel aus externer Lieferkette | Cleveland Steel & Tubes / HTS / Contractor | Stockholder procurement | Stockmatcher | unbekannt | unbekannt | unbekannt | Lieferkette zu Baustelle | Timing/Verfügbarkeit | matched procurement | S8, S9 |
| Transport | Lieferung reused beams | Lieferant/Contractor | konventionelle Stahl-Logistik | unbekannt | - | - | unbekannt | UK supply chain | unbekannt | unbekannt | S8 |
| Lagerung | Stockholder-Bestand / Baustellenkoordination | Cleveland Steel & Tubes, Mace | Lager-/Abruflogik | Stockmatcher-Daten | - | unbekannt | unbekannt | stock beams/offcuts | Lager- und Zuordnungskomplexität | digitaler Abgleich | S9 |
| Aufbereitung | Recondition/fabrication | Stahlbauer unbekannt | unbekannt | unbekannt | - | Reconditioning belegt nur für Empfangsgirder; Stahlträger unbekannt | unbekannt | Werkstatt | unbekannt | unbekannt | S3 |
| Planung | Hybrid-CLT/Stahl + reused steel integrieren | Bennetts, HTS, Landsec | hybrid structural design, DfMA | Stockmatcher | - | - | fire/acoustic/vibration tests | Materialverfügbarkeit im Entwurf | Großmaßstab/Versicherung/Brand | rigorous testing, non-composite design | S2, S3 |
| Genehmigung | Planung nach UKGBC/NABERS/BREEAM/WELL und Baurecht | Landsec, Planer, Behörden | Zertifizierungs-/Regelwerksprozess | unbekannt | - | - | NABERS Independent Design Review | - | Mass timber acceptance | Tests/Reviews | S2, S4 |
| Wiedereinbau | Montage reused steel in Struktur | Mace, Stahlbauer unbekannt | Stahlmontage | unbekannt | - | - | Abnahmen unbekannt | Baustelle | Schnittstellen CLT/Stahl | standardisierte/reversible Verbindungen | S2, S3 |
| Monitoring | Carbon Declaration / embodied carbon tracking | Bennetts, HTS, Landsec | upfront carbon reporting | unbekannt | - | - | LCA/Carbon data | - | Werte variieren | Quellenvergleich nötig | S1, S4 |

---

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Hybrid steel/CLT; reused steel integriert | Tragfähigkeit, Brand, Schwingung, Akustik | genaue Stahlreuse-Normen unbekannt | fire/acoustic/vibration performance at scale | Mass timber + reused steel + Bürohochhaus | Tests und hybrides System | S2 |
| Lastabtragung | CLT spannt 6 m auf Stahlträger | Büro-Nutzlast, Schwingung | unbekannt | Vibration performance | footfall vibrations governing | Stahl/CLT-System mit großzügigem Raster | S2, S8 |
| Verbindung | visible/reversible joints, non-composite structure | Demontierbarkeit, Tragfähigkeit | unbekannt | unbekannt | Future disassembly | reversible connections | S3, S4 |
| Brandschutz | rigorose fire testing für CLT/Hybridstruktur | Selbstverlöschen/Brandsicherheit | UK fire/insurance requirements unbekannt | extensive fire testing | Mass timber in 15-storey office | rigorous testing | S2 |
| Schallschutz | Acoustics als Designhürde genannt | Bürokomfort | unbekannt | akustische Prüfung/Design considerations | CLT/Hybriddecken | Detailplanung | S2 |
| Feuchte | Roofs/terraces mit concrete slabs auf 60 mm CLT permanent formwork gegen Leckagerisiko | Feuchteschutz | unbekannt | unbekannt | Dach-/Terrassenleckage | Betondecken auf CLT-Schalung | S2 |
| Wärmeschutz | unbekannt | Gebäudehülle | BREEAM/WELL/NABERS Zielwerte, genaue U-Werte unbekannt | unbekannt | unbekannt | unbekannt | S4, S5 |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | - |
| Luftdichtheit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | - |
| TGA-Integration | major plant demontierbar geplant | Wartung/Austausch | unbekannt | unbekannt | DfD | plant removal allowance | S3 |
| Barrierefreiheit | unbekannt | Büro/öffentlicher Raum | UK building regulations unbekannt | unbekannt | unbekannt | unbekannt | - |
| Dauerhaftigkeit | reused steel als strukturell integriert | Lebensdauer | unbekannt | unbekannt | gebrauchte Herkunft | Stockmatcher + Beschaffung; Prüfung unbekannt | S9 |
| Wartung | DfD und standardisierte Module | Austauschbarkeit | unbekannt | unbekannt | künftiger Rückbau | reversible/non-composite design | S3 |
| Zulassung | Großes CLT-Büroprojekt mit insurance/fire considerations | Genehmigung/Versicherung | UKGBC Framework, BREEAM/WELL/NABERS; Baurecht unbekannt | reviews/tests | Versicherbarkeit Mass Timber | Tests und Design Reviews | S2, S4 |
| Haftung | unbekannt | Gewährleistung reused steel | unbekannt | unbekannt | gebrauchte Bauteile | unbekannt | - |

---

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Wiederverwendete Stahlträger | >500 | Stück | UKGBC / TDUK | Projekt / Struktur | S3, S8 | belegt |
| Wiederverwendeter Stahl | 115 | t | HTS Stockmatcher | reused steel | S2, S7 | belegt |
| Wiederverwendeter Stahl | 116 | t | Mace | reused steel | S7 | belegt |
| Wiederverwendeter Stahl | 125 | t | Timber Development UK | reused steel | S8 | teilweise belegt |
| CO₂-Einsparung reused steel | 216 | tCO₂e | HTS project page | reused steel | S1, S2 | belegt, aber Konflikt |
| CO₂-Einsparung reused steel | 276 | tCO₂e | UKGBC / HTS topping out / Mace | reused steel | S3, S7 | belegt, aber Konflikt |
| Retained Print Building structure | ca. 80 | % | HTS/Bennetts/Mace | Bestandserhalt Print Building | S1, S2, S4 | belegt |
| GIA | 52.026 | m² | HTS | Gesamtprojekt | S1, S2 | belegt |
| Area | 33.910 | m² | Bennetts | Projektfläche, genaue Definition unklar | S4 | belegt |
| Workspace | 365.000 | sq ft | Landsec | vermietbare/Arbeitsflächen | S5 | belegt |
| Gesamtgröße | 380.000 | sq ft | Mace/Medien | Büro/Retail/Public Space | S7, S10 | teilweise belegt |
| Upfront carbon total | 510 | kgCO₂e/m² | Bennetts carbon data | A1-A5 total | S4 | belegt |
| Upfront carbon Stage 4 | <550 / 550 | kgCO₂e/m² | Bennetts older/newer pages | A1-A5 | S4 | teilweise belegt |
| Structural embodied carbon | 205 | kgCO₂e/m² | HTS | Struktur | S1 | belegt |
| Carbon stored by timber | 5.300 oder 4.999 | tCO₂e | HTS | timber storage | S1, S7 | unklar |
| Bauzeit/Completion | Q4 2025 / 2026 | Jahr/Quartal | Quellenvergleich | Projektstatus | S4, S7, S10 | unklar |
| U-Wert | unbekannt | - | - | - | - | unbekannt |
| Kosten | unbekannt reuse-spezifisch | - | - | - | - | unbekannt |

---

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Werte- und Quellenkonflikt bei reused steel | methodisch | verschiedene Projektkommunikationen | Unsicherheit in Datenbank | Kennwert, Bericht | Quellen getrennt ausweisen | Mengen und CO₂ nicht harmonisieren ohne Primärdaten | eigene Auswertung nach S1/S3/S7/S8 |
| Matching passender Stahlträger | technisch/logistisch | vorhandene Längen/Querschnitte müssen Design treffen | Beschaffungsaufwand | Tool, Bauteil, Datenmodell | HTS Stockmatcher | Digitales Matching erleichtert strukturellen Reuse | S9 |
| Reuse-Stahl im Großprojekt beschaffen | logistisch/wirtschaftlich | hohe Mengen, Terminplan, Lieferantendaten | Risiko für Bauablauf | Logistik, Wirtschaft | Stockholder + Algorithmus | Reuse braucht Lieferkettenpartner | S8, S9 |
| Brand/Versicherung bei Hybrid-CLT | technisch/rechtlich | Mass timber im Hochhausmaßstab | Genehmigungs-/Versicherungsrisiko | Prüfung, Recht, Tragwerk | rigorous fire testing | Performance-Fragen früh testen | S2 |
| Schwingung/Akustik | technisch | CLT/Stahl-Hybriddecken | Komfort-/Nutzungsrisiko | Leistungsanforderung | Detailplanung/Tests | Hybriddecken brauchen performance-led design | S2, S8 |
| Bestandserhalt vs Direct Reuse | methodisch | 80 % Print retained | Rating könnte überschätzt werden | Reuse-Strategie, Gebäude | retained structure separat ausweisen | Bestandserhalt ist Low Carbon, aber kein Direct Reuse | eigene Bewertung |
| Status/Handover unklar | organisatorisch | Quellen nennen on site, 2025, 2026 | Projektstatus unsicher | Projektstatus | Handover verifizieren | aktuelle Projektquellen prüfen | S1, S4, S7 |

---

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** wiederverwendeter Stahl wurde über HTS Stockmatcher gegen Designanforderungen gematcht und aus Stockholder-Beständen beschafft; Cleveland Steel & Tubes wird als Quelle/Lieferant genannt.
- **Bauteilbörse / Quelle:** keine offene Bauteilbörse belegt; eher professioneller Stahl-Stockholder + digitales Matching.
- **Kostenwirkung:** unbekannt; keine belastbaren Kostenangaben für reused steel gefunden.
- **Zeitwirkung:** unklar; Matching und procurement als spezifischer Zusatzprozess belegt, konkrete Dauer unbekannt.
- **Versicherung / Haftung:** Mass timber/Hybridstruktur mit insurance considerations belegt; spezifische Haftung für reused steel unbekannt.
- **Gewährleistung:** unbekannt
- **Arbeitsaufwand:** erhöhter Aufwand für Datenabgleich, Beschaffung, Koordination und Leistungsnachweise.
- **Lagerung:** Stahlstock beim Stockholder; Baustellenlagerung unbekannt.
- **Marktbarrieren:** Datenqualität, Verfügbarkeit passender Stahlträger, Zertifizierung/Prüfung, Terminplan, Versicherbarkeit im Hybridhochbau.

---

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** mittel; reused steel als Tragwerk vermutlich sichtbar/integriert, aber Hauptästhetik ist hybrid timber/industrial retention. Empfangstresen aus wiederverwendetem Stahlträger macht Reuse symbolisch sichtbar.
- **räumliche Transformation:** ehemaliges Printworks wird zum Bürocampus transformiert; Neubau Ink ergänzt den Bestand.
- **Atmosphäre / Ausdruck:** industrielle Vergangenheit, offengelegte Struktur, minimale Oberflächen, sichtbare/reversible Fügungen.
- **Umgang mit Spuren:** Bestandsspuren der Druckerei werden bewahrt; Spuren der reused beams unbekannt.
- **sozialer Wert:** neuer öffentlicher Square und Retail/urban realm; Reuse dient als Mainstream-Beispiel für kommerzielle Büroentwicklung.
- **Denkmal- oder Bestandswert:** kein formaler Denkmalstatus gefunden; industrieller Charakter wird gestalterisch genutzt.
- **Kritik / Grenzen:** Projekt ist stark in Low Carbon und DfD, aber nicht alles ist Direct Reuse. Retention, CLT und recycled-content steel müssen methodisch von echter Bauteilwiederverwendung getrennt werden.

---

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** donor sources der Stahlträger, genaue Profile/Längen, Prüf-/Zertifizierungsunterlagen für reused steel, Kosten, Gewährleistung, Handoverstatus, detailliertes Bauteilinventar für Nicht-Stahl-Elemente.
- **Sinnvolle neue Entitäten:** Matching-Algorithmus, Stockholder/Reuse-Lieferant, Retained-Structure-Anteil, Embodied-Carbon-Wertekonflikt.
- **Fehlende Daten:** eindeutige Stahlmenge, eindeutiger CO₂-Saving-Wert, genaue Einbauorte, Prüfverfahren, Vertragsmodell, Wartungsdaten.
- **Zu prüfende Quellen:** HTS Stockmatcher-Projektdaten, Landsec carbon reports, Mace procurement records, Cleveland Steel & Tubes Lieferlisten, BREEAM/WELL/NABERS Dokumente, Bauakten Southwark.

---

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja

### 5 wichtigste Fakten

1. Timber Square integriert über 500 wiederverwendete Stahlträger.
2. Die publizierte reused-steel-Menge liegt je nach Quelle bei ca. 115–125 t.
3. HTS nutzte den Python-basierten Stockmatcher zum Abgleich von Stahlbeständen und Designanforderungen.
4. Das Print Building behält ca. 80 % seiner Struktur, zählt hier aber als Bestandserhalt.
5. Die CO₂-Einsparung durch reused steel wird widersprüchlich mit 216 oder 276 tCO₂e angegeben.

### 5 wichtigste Bauteile

1. Wiederverwendete Stahlträger
2. Wiederverwendeter Stahlträger als fester Empfangstresen
3. Bestehende Struktur des Print Building als Bestandserhalt, nicht Direct Reuse
4. CLT-Decken als Kontextbauteil, nicht reused
5. Demontierbare TGA-/Plant-Komponenten als Future-Reuse-Strategie, nicht aktueller Direct Reuse

### 5 wichtigste Hürden

1. Matching geeigneter Stahlprofile
2. Datenqualität und Nachweis reused steel
3. Brand-, Versicherungs-, Akustik- und Schwingungsanforderungen im Hybridbau
4. Abgrenzung von Bestandserhalt und Direct Reuse
5. Uneinheitliche publizierte Kennwerte

### 5 wichtigste übertragbare Erkenntnisse

1. Digitale Matching-Tools können reused steel im Großprojekt skalieren.
2. Reuse-Stahl braucht professionelle Stockholder und frühe Designintegration.
3. Klimaberichte müssen Retention, Reuse, Recycling und biogene Speicherung trennen.
4. Reversible/non-composite details unterstützen zukünftige Wiederverwendung.
5. Große kommerzielle Projekte können Direct Reuse aus der Nische holen, sofern Lieferketten stabil sind.

### 5 offene Fragen

1. Woher stammen die über 500 wiederverwendeten Stahlträger genau?
2. Welche Prüfungen/Zertifikate wurden für die reused beams angewandt?
3. Warum unterscheiden sich die Werte 115/116/125 t und 216/276 tCO₂e?
4. Welche Kosten- und Terminwirkungen hatte Stockmatcher-gestützte Beschaffung?
5. Ist das Projekt vollständig fertiggestellt/übergeben oder noch im Handover?

---

## Quellen und Links

- **S1 – Heyne Tillett Steel: Timber Square project.** https://hts.uk.com/project/timber-square/
- **S2 – Heyne Tillett Steel: How we made it: Timber Square.** https://hts.uk.com/news-views/how-we-made-it-timber-square/
- **S3 – UKGBC: Timber Square.** https://ukgbc.org/resources/timber-square/
- **S4 – Bennetts Associates: Timber Square.** https://www.bennettsassociates.com/projects/timber-square/
- **S5 – Landsec: Timber Square, Bankside.** https://www.landsec.com/en/workplace/our-properties/timber-square-london-se1
- **S6 – Landsec press release 2023.** https://landsec.com/media/press-releases/2023/landsec-signals-confidence-london-office-market-commitment-deliver-timber
- **S7 – Heyne Tillett Steel: Topping out at Timber Square.** https://hts.uk.com/news-views/topping-out-at-timber-square/
- **S8 – Timber Development UK: Print and Ink buildings, Timber Square.** https://timberdevelopment.uk/print-and-ink-buildings-timber-square/
- **S9 – Heyne Tillett Steel: Stockmatcher.** https://hts.uk.com/research-innovation/stockmatcher/
- **S10 – Mace Group: Timber Square.** https://www.macegroup.com/projects/timber-square/
