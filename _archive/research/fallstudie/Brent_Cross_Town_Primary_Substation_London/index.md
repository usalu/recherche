---
entity: "fallstudie"
id: "Brent_Cross_Town_Primary_Substation_London"
title: "Brent Cross Town Primary Substation, London — Fallstudie Direct Reuse / zirkuläres Bauen"
build_status: "promoted_phase42"
legacy_paths:
  - "Gebäude\\Brent_Cross_Town_Primary_Substation_London.md"
node_kind: "core"
bauobjekt:
  - "Brent_Cross_Town_Primary_Substation_London"
projekt:
  - "Brent_Cross_Town_Primary_Substation_London"
---

# Brent Cross Town Primary Substation, London — Fallstudie Direct Reuse / zirkuläres Bauen

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

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteil-/Produktwiederverwendung; Reuse über Stockholder; keine Gebäudeversetzung; keine adaptive reuse
- **Hauptniveau:** Tragwerk / technische Gebäudeinfrastruktur / Screen-Hülle
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die Rohre bleiben als Stahlrohrprofile erhalten und werden als Stützen/Bracing genutzt; sie werden nicht eingeschmolzen. Da die Herkunft überschüssige Pipeline-Projekte sind, ist es eher Produkt-/Bauteilwiederverwendung als Hochbau-Urban-Mining.
- **Warum ist der Fall relevant?** Er zeigt, dass Reuse-Stahl in Infrastrukturprojekten tragend und sichtbar eingesetzt werden kann, wenn Bauherr, Ingenieure und Stockholder früh zusammenarbeiten. Zusätzlich ist der Fall wichtig, weil die Quellen auch eine verpasste Reuse-Chance durch unzureichende Änderungskoordination dokumentieren.

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

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** Schadstoff, konkrete Software, detaillierte Verbindung, detaillierte Brandschutz-/Zulassungstexte, Wartung, Lebensdauer, U-Wert.
- **Welche neuen Entitäten wären sinnvoll?** Surplus-Industriebauteil, Reuse-Screen, verpasste Reuse-Chance, Reuse-Kennwertkonflikt.
- **Welche Daten fehlen?** exakte Rohrmaße; Lagerdauer; Oberflächen-/Korrosionsschutz; Anschlussdetails; Brandschutz; Wartung; genaue Bilanzgrenzen der CO₂e-Werte; Kostenbasis.
- **Welche Quellen müssten geprüft werden?** Arup project files; Whitby Wood/Bourne steel drawings; Cleveland certificates; SCI P427 test reports; Galldris/Bourne construction records.

## Quellen / Links

1. ASBP — Brent Cross Town Primary Substation: https://asbp.org.uk/case-studies/brent-cross-town-primary-substation  
2. Arup — Brent Cross Town Substation: https://www.arup.com/projects/brent-cross-town-substation/  
3. Arup insight — Recover, reuse, reimagine: https://www.arup.com/insights/recover-reuse-reimagine-how-we-can-reduce-steel-waste-at-scale/  
4. Bourne Group — Brent Cross Wrap Substation: https://www.bournegroup.ltd/bourne-special-projects/bourne-group-brent-cross-wrap-substation-at-brent-cross-town-developmemt/  
5. Domus — London power station becomes local icon: https://www.domusweb.it/en/speciali/domus-air/2023/energia-caleidoscopica.html  
6. ASBP — DISRUPT project context: https://asbp.org.uk/disrupt
