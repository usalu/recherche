---
id: "Brent_Cross_Town_Primary_Substation_London"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "Brent Cross Town Primary Substation, London — Fallstudie Direct Reuse / zirkuläres Bauen"
bauobjekt:
  - "Brent_Cross_Town_Primary_Substation_London"
legacy_paths:
  - "Gebäude\\Brent_Cross_Town_Primary_Substation_London.md"
projekt:
  - "Brent_Cross_Town_Primary_Substation_London"
reuse_chain_detected: "True"
---
# Brent Cross Town Primary Substation, London — Fallstudie Direct Reuse / zirkuläres Bauen

## Migration

- Fallstudie ID: Brent_Cross_Town_Primary_Substation_London
- Legacy source count: 1
- Generated project: Brent_Cross_Town_Primary_Substation_London
- Generated bauobjekt: Brent_Cross_Town_Primary_Substation_London
- Extracted reuse_einsatz rows: 6
- Extracted datenpunkt rows: 17
- Extracted entity mapping rows: 30
- Reuse chain detected: True

## Legacy Content

### Legacy Source: Gebäude\Brent_Cross_Town_Primary_Substation_London.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Brent_Cross_Town_Primary_Substation_London
- Secondary targets: projekt/Brent_Cross_Town_Primary_Substation_London; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Brent Cross Town Primary Substation, London — Fallstudie Direct Reuse / zirkuläres Bauen

**Stand:** 2026-05-07  
**Hinweis zum Namen:** Die Prioritätenliste nennt „Brent Cross Town Primary / Electrical Substation“. Die belastbaren Quellen sprechen von **Brent Cross Town Primary Substation** bzw. **Brent Cross Town Substation**. Es handelt sich nicht um eine Schule.  
**Regel:** Gezählt werden nur wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente.

---

## 1. EINORDNUNG

- **Entscheidung:** HAUPTFALL / VERGLEICHSFALL Infrastruktur
- **Bewertung:** ★★★★☆
- **Begründung:** Die tragende Stahlstruktur der Substation-Screen nutzt wiederverwendete bzw. überschüssige Stahlrohre aus Öl-/Gas-Pipeline-Projekten als lange Stützen und Aussteifungselemente. Der Reuse-Anteil ist hoch und tragwerksrelevant, aber das Projekt ist eher Infrastruktur-/Screen-Bauwerk als klassisches Hochbaugebäude.
- **Vertrauensgrad:** belegt
- **Warnung Bestandserhalt:** nein
- **Warnung Möbel/Dekoration:** nein
- **Projektstatus:** gebaut; Stahlbauarbeiten laut ASBP Juli–November 2022 abgeschlossen; Arup beschreibt realisiertes Projekt.

---

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Brent Cross Town Primary Substation | Reuse-Tragwerk einer technischen Infrastrukturhülle | ASBP, Arup | belegt | High-profile substation screen |
| Projekt | 80 MVA Substation für Brent Cross Town | Versorgung für neues Quartier | ASBP, Arup | belegt | Strom für 6,700 homes + offices etc. |
| Gebäude | Substation screen / oval steel structure | Tragende Hülle / Kunstwerk / Infrastruktur | ASBP, Arup | belegt | 21 m hoch, 115 m Umfang; Arup nennt 52 m lang, 21 m hoch |
| Ort | Brent Cross, London, UK | Standort | ASBP, Arup | belegt | Am North Circular / M1-Kontext |
| People | Brent Cross South Limited Partnership | Client / Joint venture Related Argent + London Borough of Barnet | ASBP | belegt | Bauherr |
| People | Related Argent | Client / development partner | Arup, ASBP | belegt | Carbon-neutrality goal 2030 |
| People | London Borough of Barnet | Joint venture partner | ASBP, Arup | belegt | öffentlicher Partner |
| People | IF_DO | Architekt | ASBP, Arup, Bourne | belegt | Entwurf Screen / Artwork integration |
| People | Arup | Concept structural engineer / design lead | ASBP, Arup | belegt | Reuse-Idee und Designteam |
| People | Whitby Wood | Structural engineer | ASBP | belegt | Detailtragwerk laut ASBP |
| People | Bourne Special Projects / Bourne Group | steel structure designer, fabricator, erector / wrap contractor | ASBP, Bourne | belegt | Stahlbau |
| People | Galldris / Galldris Group | main contractor | ASBP, Arup | belegt | Schreibweise in Quellen variiert |
| People | Cleveland Steel and Tubes | reclaimed steel stockholder / supplier | ASBP, Arup | belegt | Quelle der reclaimed tubulars |
| Bauteil | Reclaimed tubular steel columns | tragende Stützen / Aussteifungen | ASBP, Arup | belegt | aus surplus/cancelled oil and gas pipeline projects |
| Material | Stahlrohre | wiederverwendete / überschüssige Rohrprofile | ASBP, Arup | belegt | nicht aus Hochbauabbruch |
| Reuse-Strategie | Reuse von Stahlrohren / stockholder procurement | Ex-situ Bauteil-/Produktwiederverwendung | ASBP, Arup | belegt | Stützen und Bracing |
| Kennwert | 33.46 t reused steel | Menge reused steel | ASBP | belegt | ASBP-Wert |
| Kennwert | 42.5 % / around 45 % reused steel | Anteil am Stahltragwerk | Arup / ASBP | teilweise belegt | Quellenabweichung |
| Kennwert | 66 t / 99.2 t CO₂e saving | CO₂e-Einsparung | ASBP / Arup | teilweise belegt | Quellenkonflikt wegen Bilanzmethode/Bezugsrahmen |
| Prüfung | Independent testing + weld inspection | Freigabe Tubulars | ASBP | belegt | SCI P427 protocol genannt |
| Norm | SCI P427 protocol | Prüfprotokoll reclaimed steel | ASBP | belegt | Keine weiteren Normen erfinden |
| Recht | CE/UKCA marked | Warranty / Konformität | ASBP | belegt | Details unbekannt |
| Aufbereitungsmethode | surface preparation, testing, weld inspection | Reuse-fähig machen | ASBP | belegt | Tubulars in excellent „as new“ condition |
| Abbruchmethode | keine Gebäudedemontage | Herkunft aus surplus/cancelled oil & gas pipeline projects | ASBP, Arup | belegt | Donor-Gebäude nicht vorhanden |
| Hürde | Reservation mismatch / design changes | Reuse-Material passte nach Änderungen nicht vollständig | ASBP | belegt | verpasste zusätzliche 22 t CO₂e saving laut ASBP |
| Logistik | early engagement with Cleveland Steel | Auswahl geeigneter Rohre | ASBP, Arup | belegt | ohne enge Koordination schwierig |
| Tool | digitale Tools / BIM | Arup nennt digital tools und BIM services | Arup | teilweise belegt | konkrete Software unbekannt |
| Software | unbekannt | keine spezifische Software genannt | — | unklar |  |
| Schadstoff | unbekannt | keine Angaben | — | unklar |  |
| Förderprogramm | DISRUPT case study | Forschungskontext der ASBP-Fallstudie | ASBP | belegt | nicht zwingend Projektförderung |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Surplus-Industriebauteil | Herkunft ist kein Gebäudeabbruch, sondern ungenutzte Pipeline-Projekte | Stahlrohre aus oil and gas industry | Bauteil, Material, Logistik |
| Reuse-Screen | Bauwerkstyp zwischen Hülle, Tragwerk und technischer Infrastruktur | 21 m hoher ovaler Substation-Screen | Gebäude, Tragwerkssystem, TGA |
| Reuse-Quote mit Quellenkonflikt | Unterschiedliche Quellen nennen 42.5 %, 45 % und ca. 50 % | Arup vs. ASBP vs. Bourne | Kennwert, Bericht |
| Verpasste Reuse-Chance | Dokumentiert nicht nur Erfolg, sondern nicht realisierte Einsparung | 22 t embodied carbon saving missed | Hürde, Logistik, Prozessphase |

---

## 3. FALLSTUDIE

- **Name:** Brent Cross Town Primary Substation / Brent Cross Town Substation
- **Ort:** Brent Cross, London, Vereinigtes Königreich
- **Gebäude:** elektrische Primär-Substation mit ovalem Stahl-Screen / Kunstwerk-Hülle
- **Projekt:** Substation und öffentliche Landmarke für Brent Cross Town
- **Beteiligte People / Akteure:** Brent Cross South Limited Partnership; Related Argent; London Borough of Barnet; IF_DO; Arup; Whitby Wood; Bourne Special Projects / Bourne Group; Galldris Group; Cleveland Steel and Tubes; Gillespies; Power On; Lakwena
- **Architekt:** IF_DO
- **Tragwerksplaner:** Arup als concept structural engineer; Whitby Wood als structural engineer; Bourne als steel structure designer/fabricator
- **Bauherr:** Brent Cross South Limited Partnership / Related Argent + London Borough of Barnet
- **Zeitraum:** Stahlbau Juli–November 2022; weitere Projektdaten unbekannt
- **Ursprüngliche Nutzung:** Stahlrohre: ungenutzte/überschüssige oil-and-gas pipeline projects; Grundstück: brownfield/ex-industrial land laut Arup
- **Neue Nutzung:** tragende Stützen und Aussteifungen des Substation-Screens
- **Fläche / Maßstab:** 21 m hoch; 115 m Umfang laut ASBP; Arup beschreibt 52 m lang und 21 m hoch; 80 MVA Substation
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** sehr gut für Stahlreuse, Akteure, Mengen, Prüfprotokoll und Hürden; eingeschränkt für genaue Verbindung, Brandschutz, detaillierte Statik, Wartung

---

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteil-/Produktwiederverwendung; Reuse über Stockholder; keine Gebäudeversetzung; keine adaptive reuse
- **Hauptniveau:** Tragwerk / technische Gebäudeinfrastruktur / Screen-Hülle
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die Rohre bleiben als Stahlrohrprofile erhalten und werden als Stützen/Bracing genutzt; sie werden nicht eingeschmolzen. Da die Herkunft überschüssige Pipeline-Projekte sind, ist es eher Produkt-/Bauteilwiederverwendung als Hochbau-Urban-Mining.
- **Warum ist der Fall relevant?** Er zeigt, dass Reuse-Stahl in Infrastrukturprojekten tragend und sichtbar eingesetzt werden kann, wenn Bauherr, Ingenieure und Stockholder früh zusammenarbeiten. Zusätzlich ist der Fall wichtig, weil die Quellen auch eine verpasste Reuse-Chance durch unzureichende Änderungskoordination dokumentieren.

---

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Lange Stützen aus reclaimed tubulars | Stahlrohre | surplus/cancelled oil and gas pipeline projects via Cleveland Steel and Tubes | Pipeline-/Industrieprodukt; teils ungenutzt | tragende Stützen des Substation-Screens | Anteil in 33.46 t enthalten | ja | ja | ja, Screen-Struktur | ja, Infrastrukturhülle | Auswahl, Test, ggf. Vorbereitung | unbekannt | unabhängig getestet; weld inspected | Tragfähigkeit, Dauerhaftigkeit, Montage | SCI P427; CE/UKCA | Profilverfügbarkeit, Verbindungseffizienz | ASBP, Arup | genaue Rohrmaße |
| Aussteifung / bracing members | Stahlrohre | wie oben | Pipeline-/Industrieprodukt | Aussteifung Stahlrahmen | Anteil in 33.46 t enthalten | ja | ja | ja | ja | wie oben | unbekannt | wie oben | Stabilität / Windlasten | SCI P427; CE/UKCA | geänderte Designs / reserved steel mismatch | Arup, ASBP | Verbindungsdetails |
| Façade support members | Stahl, überwiegend neu | nicht reused | keine | Träger der farbigen Hülle / artwork | unbekannt | teilweise | ja | ja | ja | neu | unbekannt | unbekannt | effiziente Anschlüsse | unbekannt | Reused tubes wären hier laut Arup weniger effizient | ASBP, Arup | Menge |
| Ovaler Substation-Screen | Stahl + Hülle/Artwork | Mischsystem | keine | technische Einhausung / öffentl. Kunstwerk | 21 m hoch, 115 m Umfang / 52 m lang laut Arup | ja | ja | ja | ja | Montage | unbekannt | unbekannt | Wind, Dauerhaftigkeit, Zugang | unbekannt | große Landmarke an Verkehrsraum | ASBP, Arup | genaue Systemdetails |
| Earth Friendly Concrete / low-cement concrete | Beton | neu / zementreduziert | keine | Fundamente/Bauteile unbekannt | unbekannt | ja/unklar | nein | nein | ja | nicht Reuse | — | unbekannt | Tragfähigkeit, Dauerhaftigkeit | unbekannt | nicht als Direct Reuse zählen | Arup | Menge |
| Elektrotechnische Anlagen | unbekannt | neu | keine | 80 MVA Substation | unbekannt | nein | nein | nein | ja | unbekannt | unbekannt | unbekannt | Betriebssicherheit | unbekannt | außerhalb Reuse-Fokus | ASBP, Arup | Details |

---

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Reuse-Potenzial im größten Materialposten Stahl erkannt | Arup, Related Argent, IF_DO | circular economy inception | digitale Tools / BIM allgemein | — | — | — | frühes Teamgespräch | Stahl ist Hauptcarbon-Treiber | Reuse als Entwurfsziel | ASBP, Arup |
| Bauteilinventar | Verfügbare Rohre bei Cleveland geprüft | Arup, Cleveland, Bourne | stockholder inventory matching | unbekannt | keine | Auswahl geeigneter tubular sections | Vorprüfung | early engagement | begrenzte Profilauswahl | Design auf verfügbare Rohre | ASBP, Arup |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | — | unbekannt | unbekannt | unbekannt | keine Daten | unbekannt | — |
| Rückbau | nicht zutreffend | — | surplus material sourcing | — | keine Gebäudedemontage | — | — | — | Herkunft aus oil/gas surplus | Stockholder supply | ASBP |
| Ausbau | nicht zutreffend / surplus procurement | Cleveland | Bestand aus cancelled projects | unbekannt | — | surface preparation unbekannt | Sicht-/Qualitätsprüfung | Lagerbestand | Dokumentation Herkunft | Stockholder-Daten | ASBP |
| Transport | Lieferung von Cleveland zur Baustelle | Cleveland, Galldris/Bourne | just supply chain | unbekannt | — | — | — | genaue Distanz unbekannt | unbekannt | frühe Beschaffung | ASBP |
| Lagerung | Stockholder hält Rohre verfügbar | Cleveland | Reuse stockholding | unbekannt | — | ggf. Vorbereitung | Nachweisführung | Lager bei supplier | reservierter Stahl passte später teils nicht | bessere Change-Kommunikation nötig | ASBP |
| Aufbereitung | Testen, weld inspection, ggf. Oberflächenvorbereitung | Cleveland, Bourne, Prüflabore | SCI P427 | unbekannt | — | testing / weld inspection | unabhängig getestet | unbekannt | Verwendbarkeit muss belegt werden | CE/UKCA marking | ASBP |
| Planung | Einbau als Stützen und Bracing | Arup, Whitby Wood, Bourne, IF_DO | lean design / efficient use | BIM genannt, Details unbekannt | — | — | Design check | koordinierte Auswahl | Tubes nicht für alle Funktionen optimal | virgin steel für façade support | Arup, ASBP |
| Genehmigung | technische Infrastruktur geplant | Related Argent, Barnet, Arup | unbekannt | unbekannt | — | — | unbekannt | unbekannt | öffentliche Landmarke / Verkehrssichtbarkeit | Integration von Kunstwerk und Technik | Arup |
| Wiedereinbau | Stahlbau Juli–November 2022 | Bourne, Galldris | Stahlbau-Montage | unbekannt | — | vorbereitete Tubulars | CE/UKCA | Baustelle ohne erwähnte Platzprobleme | supplier/design mismatch | teilweise neue Stahlbeschaffung | ASBP |
| Monitoring | CO₂e-saving und Reuse-Anteil dokumentiert | ASBP/DISRUPT, Arup, Related Argent | case study / embodied carbon reporting | unbekannt | — | — | unbekannt | — | Quellenwerte weichen ab | Werte getrennt dokumentieren | ASBP, Arup |

---

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Ovale Screen-Struktur mit reused tubular columns und bracing | Tragfähigkeit, Wind, Steifigkeit | unbekannt | SCI P427 testing / weld inspection | vorhandene Rohre müssen effizient passen | Wiederverwendung nur dort, wo effizient | ASBP, Arup |
| Lastabtragung | Reused tubes als lange Stützen / Bracing | Vertikale und horizontale Lasten | unbekannt | Material- und Schweißprüfung | Profilverfügbarkeit | frühe Abstimmung mit Cleveland | ASBP |
| Verbindung | Anschlussdetails nicht veröffentlicht | sichere Stahlbauanschlüsse | unbekannt | weld inspection | Rohre können für façade support klobig/ineffizient sein | virgin steel für façade support | ASBP, Arup |
| Brandschutz | unbekannt | unbekannt | unbekannt | unbekannt | technische Infrastruktur | unbekannt | — |
| Schallschutz | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Feuchte | unbekannt | Witterungsbeständigkeit | unbekannt | unbekannt | Open-air substation / Wetter | natürliche Ventilation laut Arup | Arup |
| Wärmeschutz | nicht zentral | Substation operational carbon | unbekannt | unbekannt | nicht klassisches beheiztes Gebäude | open-air / natürliche Ventilation | Arup |
| Wärmebrücken | nicht relevant / unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | — |
| Luftdichtheit | nicht relevant / unbekannt | unbekannt | unbekannt | unbekannt | open-air | unbekannt | — |
| TGA-Integration | Energieinfrastruktur für Quartier | 80 MVA Versorgung, saubere Energie | unbekannt | unbekannt | funktionales Bauwerk + Landmarke | Screen statt geschlossener Box | ASBP, Arup |
| Barrierefreiheit | nicht belegt | unbekannt | unbekannt | unbekannt | technisches Bauwerk | unbekannt | — |
| Dauerhaftigkeit | Tubulars „excellent as new“ | Langzeitverwendung außen | CE/UKCA | independent testing | Materialnachweis | Test + Marking | ASBP |
| Wartung | unbekannt | Zugänglichkeit Substation | unbekannt | unbekannt | Screen/Artwork um Technik | unbekannt | — |
| Zulassung | Reused steel CE/UKCA marked | Gewährleistung / Konformität | SCI P427; CE/UKCA | testing / weld inspection | Reuse-Nachweis | Prüfroutine | ASBP |
| Haftung | keine warranty issues genannt | Nachweisfähigkeit | CE/UKCA | Prüflabore | Reuse-Material muss akzeptiert werden | CE/UKCA marking | ASBP |

---

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| wiederverwendete Stahlmenge | 33.46 | t | ASBP/DISRUPT case study | Stahlstruktur Screen | ASBP | belegt |
| Anteil reused steel | around 45 | % | Projektangabe | total designed steelwork | ASBP | belegt |
| Anteil salvaged structural steel | 42.5 | % | Projektangabe | structural steel | Arup | belegt |
| weiterer Anteil laut Bourne | approx. 50 | % | Projektangabe | steel frame | Bourne | teilweise belegt |
| CO₂e-Einsparung | 66 | t CO₂e | ASBP | embodied carbon steel reuse | ASBP | belegt |
| CO₂e-Einsparung | 99.2 | t CO₂e | Arup | steel frame / Projektangabe | Arup | belegt, aber Quellenkonflikt |
| verpasste zusätzliche Einsparung | 22 | t embodied carbon | ASBP | nicht realisierte reuse steel substitution | ASBP | teilweise belegt |
| Höhe | 21 | m | Projektangabe | Screen | ASBP, Arup | belegt |
| Umfang | 115 | m | Projektangabe | ovaler Screen | ASBP | belegt |
| Länge Artwork | 52 | m | Projektangabe | Kunstwerk / Screen | Arup | belegt |
| Substation capacity | 80 | MVA | Projektangabe | elektrische Infrastruktur | ASBP | belegt |
| Stahlbauzeit | Juli–November 2022 | Zeitraum | Projektangabe | steel works | ASBP | belegt |
| Kostenwirkung | 25 % lower than new steel inkl. Zusatzkosten / 50 % lower material per tonne | % | 2021 cost analysis | Reclaimed steel vs new | ASBP | teilweise belegt |
| Terminwirkung | keine | qualitativ | Interview / case study | project timeline | ASBP | teilweise belegt |
| U-Wert | unbekannt | — | — | — | — | unklar |
| Lebensdauer | unbekannt | — | — | — | — | unklar |
| Zirkularitätskennwert | unbekannt | — | — | — | — | unklar |

---

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Begrenzte Profilverfügbarkeit | technisch/logistisch | stockholder hat nur bestimmte Rohrdimensionen | nicht jedes Bauteil sinnvoll mit reused steel | Bauteil, Planung, Logistik | Einsatz nur als columns/bracing | Reuse dort einsetzen, wo Profile effizient sind | ASBP, Arup |
| Designänderungen nicht an supplier kommuniziert | logistisch/technisch | reserved steel passte später nicht zum aktualisierten Design | virgin steel musste genutzt werden; 22 t potenzielle Einsparung verpasst | Prozessphase, Logistik | Change-Kommunikation verbessern | Reuse braucht Material- und Designkontrolle in Echtzeit | ASBP |
| Buyer inertia / business as usual | sozial/wirtschaftlich | Fabricator und supply chain müssen überzeugt werden | Reuse könnte aus Bequemlichkeit entfallen | Wirtschaft, People | Specifying and championing reuse | Bauherr/Ingenieur muss Reuse aktiv durchsetzen | ASBP |
| Reused tubes nicht für alle Details optimal | technisch/gestalterisch | Runde Tubes können bei Anschlüssen klobig sein | für façade support wurde neuer Stahl gewählt | Verbindung, Bauteil | Design efficiency über Reuse um jeden Preis | Nicht jedes Bauteil sollte reused sein | ASBP, Arup |
| Unterschiedliche Kennwerte | methodisch | ASBP und Arup nennen verschiedene CO₂e-Werte | Vergleichbarkeit erschwert | Kennwert | Werte getrennt angeben | Bilanzgrenzen immer dokumentieren | ASBP, Arup |
| Kein Hochbau-Donor | methodisch | Herkunft aus oil/gas surplus | Einordnung als Bauteilreuse vs. Materialproduktreuse | Reuse-Strategie | klar benennen | Herkunftstyp muss als Entität erfasst werden | eigene Bewertung |

---

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** Stockholder-Beschaffung über Cleveland Steel and Tubes; frühe Abstimmung zwischen Arup, Bourne, Client und Contractor.
- **Bauteilbörse / Quelle:** keine klassische Bauteilbörse; reclaimed steel stockholder.
- **Kostenwirkung:** ASBP nennt 50 % niedrigere Materialkosten pro Tonne gegenüber neuem Stahl; inkl. Test, Oberflächenbehandlung und Transport 25 % niedriger als neu.
- **Zeitwirkung:** ASBP nennt keine Auswirkungen auf den Projektzeitplan; Stahl wurde früh beschafft.
- **Versicherung / Haftung:** keine warranty issues laut ASBP, weil CE/UKCA marked.
- **Gewährleistung:** Details unbekannt.
- **Arbeitsaufwand:** erhöht durch Koordination, Testing, Design-Change-Management und Überzeugungsarbeit.
- **Lagerung:** über Cleveland Steel and Tubes; genaue Lagerdauer unbekannt.
- **Marktbarrieren:** begrenzte Reuse-Verfügbarkeit, fehlende Routine bei Fabricators, Designänderungen, unklare Bilanzierung.

---

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** Die Stahlstruktur ist Teil einer öffentlich sichtbaren Landmarke; ob einzelne Reuse-Spuren sichtbar sind, ist unbekannt.
- **räumliche Transformation:** Ein technisches Bauwerk wird durch Screen, Kunstwerk und Landschaft zu öffentlicher Stadtinfrastruktur.
- **Atmosphäre / Ausdruck:** farbige Hülle / Kunstwerk von Lakwena und IF_DO transformiert eine Substation in ein Landmark-Objekt.
- **Umgang mit Spuren:** Reuse-Herkunft der Stahlrohre ist eher dokumentarisch als materiell sichtbar.
- **sozialer Wert:** Arup nennt jährliche Sichtbarkeit für bis zu sechs Millionen Menschen von Straße und Bahn; öffentlicher Kunst-/Place-making-Wert.
- **Denkmal- oder Bestandswert:** unbekannt.
- **Kritik / Grenzen:** Reuse ist technisch stark, aber die Herkunft als surplus oil/gas pipelines ist methodisch anders als Wiederverwendung aus Gebäuderückbau.

---

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** Schadstoff, konkrete Software, detaillierte Verbindung, detaillierte Brandschutz-/Zulassungstexte, Wartung, Lebensdauer, U-Wert.
- **Welche neuen Entitäten wären sinnvoll?** Surplus-Industriebauteil, Reuse-Screen, verpasste Reuse-Chance, Reuse-Kennwertkonflikt.
- **Welche Daten fehlen?** exakte Rohrmaße; Lagerdauer; Oberflächen-/Korrosionsschutz; Anschlussdetails; Brandschutz; Wartung; genaue Bilanzgrenzen der CO₂e-Werte; Kostenbasis.
- **Welche Quellen müssten geprüft werden?** Arup project files; Whitby Wood/Bourne steel drawings; Cleveland certificates; SCI P427 test reports; Galldris/Bourne construction records.

---

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja, aber als Infrastruktur-/Vergleichsfall und mit korrigiertem Namen „Primary Substation“.
- **5 wichtigste Fakten:**
  1. Reused tubular steel wurde als Stützen und Bracing genutzt.
  2. ASBP nennt 33.46 t reused steel.
  3. ASBP nennt around 45 % reused steel; Arup nennt 42.5 %.
  4. Herkunft: surplus/cancelled oil-and-gas pipeline projects via Cleveland Steel.
  5. Testing erfolgte unabhängig nach SCI P427, CE/UKCA marking wurde erreicht.
- **5 wichtigste Bauteile:**
  1. reused tubular columns
  2. reused bracing members
  3. ovaler Substation-Screen
  4. neue façade support members, nicht reused
  5. technische Substation, Reuse-Anteil unbekannt
- **5 wichtigste Hürden:**
  1. begrenzte Profilverfügbarkeit
  2. Designänderungen und supplier coordination
  3. Reuse vs. effiziente Detailausbildung
  4. Buyer inertia in supply chain
  5. Kennwert-/Bilanzgrenzenkonflikte
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Reuse-Stahl kann in Infrastrukturtragwerken sinnvoll sein.
  2. Frühzeitiger Kontakt zu Stockholdern ist entscheidend.
  3. Reuse sollte nicht ineffiziente Bauteile erzwingen.
  4. Change Management muss Materialreservierungen synchron halten.
  5. Dokumentation von verpassten Reuse-Chancen ist wertvoll.
- **5 offene Fragen:**
  1. Welche Rohrdimensionen wurden eingebaut?
  2. Welche Anschlussdetails und Korrosionsschutzsysteme wurden genutzt?
  3. Warum unterscheiden sich 66 t und 99.2 t CO₂e?
  4. Welche Lebensdauerannahme gilt für die reused tubes?
  5. Welche Wartungsstrategie gilt für Screen und Stahlrohre?

---

## Quellen / Links

1. ASBP — Brent Cross Town Primary Substation: https://asbp.org.uk/case-studies/brent-cross-town-primary-substation  
2. Arup — Brent Cross Town Substation: https://www.arup.com/projects/brent-cross-town-substation/  
3. Arup insight — Recover, reuse, reimagine: https://www.arup.com/insights/recover-reuse-reimagine-how-we-can-reduce-steel-waste-at-scale/  
4. Bourne Group — Brent Cross Wrap Substation: https://www.bournegroup.ltd/bourne-special-projects/bourne-group-brent-cross-wrap-substation-at-brent-cross-town-developmemt/  
5. Domus — London power station becomes local icon: https://www.domusweb.it/en/speciali/domus-air/2023/energia-caleidoscopica.html  
6. ASBP — DISRUPT project context: https://asbp.org.uk/disrupt
