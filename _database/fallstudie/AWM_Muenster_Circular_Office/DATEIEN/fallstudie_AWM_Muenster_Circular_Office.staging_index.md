---
id: "AWM_Muenster_Circular_Office"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "AWM Münster – Zirkulärer Büroausbau 3. OG – Fallstudie Direct Reuse / zirkuläres Bauen"
bauobjekt:
  - "AWM_Muenster_Circular_Office"
legacy_paths:
  - "Gebäude\\AWM_Muenster_Circular_Office.md"
projekt:
  - "AWM_Muenster_Circular_Office"
reuse_chain_detected: "True"
---
# AWM Münster – Zirkulärer Büroausbau 3. OG – Fallstudie Direct Reuse / zirkuläres Bauen

## Migration

- Fallstudie ID: AWM_Muenster_Circular_Office
- Legacy source count: 1
- Generated project: AWM_Muenster_Circular_Office
- Generated bauobjekt: AWM_Muenster_Circular_Office
- Extracted reuse_einsatz rows: 10
- Extracted datenpunkt rows: 13
- Extracted entity mapping rows: 18
- Reuse chain detected: True

## Legacy Content

### Legacy Source: Gebäude\AWM_Muenster_Circular_Office.md

- Map action: split_into_case_graph
- Primary target: fallstudie/AWM_Muenster_Circular_Office
- Secondary targets: projekt/AWM_Muenster_Circular_Office; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# AWM Münster – Zirkulärer Büroausbau 3. OG – Fallstudie Direct Reuse / zirkuläres Bauen

**Projekt:** Abfallwirtschaftsbetriebe Münster, Büroetage Rösnerstraße / 3. OG  
**Bearbeitung:** Deutsch, kompakt, quellenbasiert  
**Grundregel:** Gezählt werden nur wiederverwendete Bau-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Bestandserhalt und lose Möbel werden nicht als Direct Reuse gewertet.

---

## 1. EINORDNUNG

- **Entscheidung:** VERGLEICHSFALL / ANHANG
- **Bewertung:** ★★☆☆☆
- **Begründung:** AWM Münster ist ein kleiner, aber gut dokumentierter zirkulärer Innenausbau mit wiedergewonnenen Glastrennwänden/-türen, Reuse-WC-Trennwänden, Kabeltrassen als Regale/Leuchten, Wandverkleidung aus alten Schul-/Theaterstühlen und wiederverwendetem Holz. Er ist relevant, weil mehrere Elemente fest eingebaut sind. Er ist aber kein Tragwerks-, Hüllen- oder Großmaßstabsfall; Möbel und Bestandserhalt werden nicht gewertet.
- **Vertrauensgrad:** belegt
- **Warnung Bestandserhalt:** ja
- **Warnung Möbel/Dekoration:** ja
- **Projektstatus:** gebaut

---

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | AWM Münster, 3. OG Rösnerstraße | zirkulärer Büroinnenausbau | S1–S5 | belegt | kleines Interior-Projekt |
| Gebäude | altes Verwaltungsgebäude der awm | Bestand, umgebautes 3. Obergeschoss | S2, S5 | belegt | Bestandserhalt nicht als Direct Reuse |
| Ort | Münster, Rösnerstraße | Standort | S2, S5 | belegt | genaue Hausnummer unbekannt |
| Projekt | moderne Arbeitswelt aus gebrauchten Materialien | neue Büro-/Workshop-/Küchen-/Besprechungsflächen | S2, S5 | belegt | 250 m² nach urselmann/AWM, 200 m² in Portfolio Dritter |
| People | Abfallwirtschaftsbetriebe Münster, urselmann interior, Concular, Petra Jablonická, Sven Urselmann | Bauherr/Nutzer, Entwurf/Innenausbau, Materialplattform/Ökobilanz | S1–S5 | belegt | genaue Vertragsrollen nicht vollständig |
| Bauteil | Glastrennwände und Türen | Reuse-Bauteile aus Behrensbau Düsseldorf | S4, S6 | belegt | fest eingebaut, zählt |
| Bauteil | WC-Trennwände | Reuse aus Behrensbau Düsseldorf | S4 | belegt | fest eingebaut, zählt |
| Bauteil | Kabeltrassen | als Regale und Allgemeinbeleuchtung genutzt | S1, S4 | belegt | fest eingebaut/technisch, zählt teilweise |
| Bauteil | Wandverkleidung aus alten Holzstühlen | feste Wandbekleidung | S1, S4 | belegt | Stühle als Möbel alt, neue Funktion feste Wandverkleidung; zählt als festes Bauteil mit Warnung |
| Bauteil | Holz aus Deckenkonstruktion/Supermarkt/Discounter | Sideboard, Küche, Wand-/Unterkonstruktion | S1, S4, S6 | belegt/teilweise | feste Einbauten zählen, lose Möbel nicht |
| Material | Hanfkalksteine, Lehm, Akustikbaffeln, Teppich | teils C2C/recycelt/biobasiert, nicht Direct Reuse | S1, S4 | belegt | separat führen |
| Bauteilbörse | Concular | Materialbeschaffung und Ökobilanzierung | S3, S6 | belegt | Glastrennwände aus Behrensbau |
| Kennwert | 6,9 t wiedergewonnene Materialien | Reuse-/Materialkennwert | S1, S3 | belegt | Bilanzgrenze Büroausbau |
| Kennwert | 13,32 t CO₂e / 82 % | Einsparung gegenüber konventionell | S1–S3, S5 | belegt | Methode nicht vollständig öffentlich |
| Kennwert | 95,6 % c2c-inspiriert oder ReUse | Produktanteil | S1–S3 | belegt | nicht alles Direct Reuse |
| Kennwert | 250 m² / 200 m² | Fläche | S1, S2 | teilweise belegt | Quellenkonflikt |
| Logistik | Urban Mining aus öffentlichen Gebäuden | Beschaffung gebrauchter Baumaterialien | S1, S3, S6 | belegt | detaillierte Distanzen unbekannt |
| Methode | ReUse first / Design follows availability | Entwurfsprinzip | S1, S3 | belegt | gutes Beispiel für Innenausbau |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| ReUse-Interior | feste Innenausbau-Bauteile zwischen Möbel und Bauwerk | Glastrennwände, WC-Trennwände, Wandverkleidung | Bauteil, Reuse-Strategie |
| Materialherkunftsseite / QR-Materialatlas | projektspezifische Material-Herkunftsdokumentation | AWM-Materialseite | Dokument, Datenmodell, Bauteil |
| Reaktivierung | technische/gestalterische Wiederinbetriebnahme gebrauchter Elemente | Reuse-LED-Leuchten, Sattler-Leuchten | Aufbereitungsmethode, TGA |

---

## 3. FALLSTUDIE

- **Name:** AWM Münster, zirkulärer Büroausbau 3. OG
- **Ort:** Münster, Deutschland
- **Gebäude:** altes Verwaltungsgebäude der Abfallwirtschaftsbetriebe Münster
- **Projekt:** Umbau des bis dahin nicht mehr nutzbaren dritten Obergeschosses zu Büro-, Workshop-, Besprechungs-, Küchen- und Coworking-Flächen
- **Beteiligte People / Akteure:** Abfallwirtschaftsbetriebe Münster, urselmann interior, Concular, Petra Jablonická, Sven Urselmann, Patrick Hasenkamp; weitere Handwerksbetriebe unbekannt
- **Architekt:** urselmann interior / Petra Jablonická im Portfolio genannt
- **Tragwerksplaner:** unbekannt
- **Bauherr:** Abfallwirtschaftsbetriebe Münster
- **Zeitraum:** Fertigstellung 2023; öffentliche Vorstellung / Meldung Januar 2024
- **Ursprüngliche Nutzung:** Verwaltungsgebäude / nicht mehr nutzbares 3. OG
- **Neue Nutzung:** moderne Arbeitswelt mit Büros, festen/mobilen Arbeitsplätzen, Workshop- und Besprechungsräumen, Küche
- **Fläche / Maßstab:** 250 m² nach urselmann interior/AWM; 200 m² nach Drittportfolio; Quellenkonflikt
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** sehr gut für Materialbeispiele und Kennwerte; schwach für Normen, Prüfungen, Kostenaufschlüsselung und Verbindungsdetails

---

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; fester Innenausbau; technische Gebäude-/Elektroelemente; Bauteilwiederverwendung; Materialwiederverwendung; adaptive reuse
- **Hauptniveau:** räumlicher Innenausbau / technische Ausstattung / feste Einbauten
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Der Umbau des bestehenden Gebäudes und die Reparatur von Möbeln werden nicht als Direct Reuse gezählt. Gezählt werden feste, neu eingebaute Bauteile wie Glastrennwände, WC-Trennwände, Kabeltrassen-Regale/Leuchten, Wandverkleidung und feste Holzeinbauten.
- **Warum ist der Fall relevant?** AWM ist ein sehr gut dokumentierter Innenausbau mit Materialherkünften, Kennwerten und öffentlich zugänglicher Materialliste. Er eignet sich als Referenz für ReUse-Interior, nicht für tragende Reuse-Fälle.

---

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Glastrennwände und Türen | Glas, Metallprofile | Behrensbau, Düsseldorf, über Concular | Büro-/Gebäudetrennwände | Trennwände und Türen im AWM-Office | 4,39 t CO₂ durch Wiederverwendung eingespart; Stückzahl unbekannt | nein | ja | nein | nein | Rückgewinnung, Transport, Montage | unbekannt | unbekannt | Brandschutz/Schallschutz/Sicherheit | unbekannt | Passung, Transport, Glaszustand | S4, S6 | Anzahl, Abmessungen |
| WC-Trennwände | unbekannt | Behrensbau, Düsseldorf | Sanitärtrennwände | WC-Trennwände | unbekannt | nein | ja | nein | nein | Rückgewinnung, Montage | unbekannt | unbekannt | Hygiene, Feuchte, Stabilität | unbekannt | Zustand/Passung | S4 | Menge |
| Kabeltrassen als Regale | Metall | ReUse-Kabeltrassen | Kabeltrassen | Regale / Ablage | unbekannt | nein | ja | nein | nein | Umnutzung, Halterungen 3D-Druck | Spezialhalterungen | unbekannt | Tragfähigkeit für Regalnutzung | unbekannt | neue Lastfunktion | S1, S4 | Menge |
| Kabeltrassen und LED-Leuchten | Metall, Elektrokomponenten | ReUse-Kabeltrassen und ReUse-LED-Leuchten | Elektroleitung/Leuchten | Allgemeinbeleuchtung | unbekannt | nein | nein | nein | ja | Reaktivierung, Montage | unbekannt | Elektrosicherheitsprüfung unbekannt | Elektrosicherheit | unbekannt | Zulassung/Haftung | S4 | Menge, Prüfungen |
| Wandverkleidung aus Stuhllehnen/-sitzen | Holz | alte Schul- und Theaterstühle | Möbel | feste Wandverkleidung | mehr als 500 alte Holzstühle bzw. 550 Sitze/Rücken nach Drittquelle | nein | ja | nein | nein | Demontage, Zuschnitt, Wandmontage | unbekannt | unbekannt | Brandschutz/Oberfläche | unbekannt | Grenzfall Möbel -> festes Bauteil | S1, S4 | genaue Fläche |
| Sideboard / Holzeinbauten | Holz | Deckenkonstruktion eines Supermarkts / Discounter-Auflösung | konstruktives Holz / Ladenbau | Sideboard, Küche, Unterkonstruktion, Einbauten | unbekannt | nein | ja | nein | nein | Rückbau, Zuschnitt, Tischlerei | unbekannt | unbekannt | Stabilität, Hygiene bei Küche | unbekannt | Herkunft und Sortierung | S1, S4, S6 | genaue Menge |
| Hanfkalksteine | Hanf, Kalk, Mineralien, Wasser | neu/biobasiert | nicht zutreffend | Wände / Bauteil | 1,7 t CO₂e Einsparung gegenüber Kalksandstein | nein | ja | nein | nein | Neubauprodukt | unbekannt | unbekannt | Raumklima/Brandschutz unbekannt | unbekannt | zählt nicht als Direct Reuse | S4 | Menge |
| Lehmbauwände | Holz, Lehmbauplatten, Lehmspachtel | teils regional/neu, Holz ggf. reuse unklar | unbekannt | Wände | unbekannt | nein | ja | nein | nein | Montage | unbekannt | unbekannt | Innenwand | unbekannt | Reuse-Anteil unklar | S4 | Reuse-Anteil |
| Akustik-Baffeln | PET-Recycling | recycelte PET-Flaschen | Recyclingrohstoff | Akustikelement | unbekannt | nein | ja | nein | nein | Recycling/Produktion | unbekannt | unbekannt | Akustik, Brandschutz | unbekannt | kein Direct Reuse | S4 | Menge |
| Möbel | diverse | aufgearbeitet / reused | Möbel | Möbel | unbekannt | nein | nein | nein | nein | Reparatur | nicht relevant | nicht relevant | nicht relevant | nicht relevant | zählt nicht | S1, S4 | nicht bewertet |

---

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Entscheidung Umbau statt Rückbau | AWM, urselmann interior | ReUse first / Umbau vor Neubau | unbekannt | nicht zutreffend | unbekannt | unbekannt | im Bestand | ungenutztes 3. OG | Umbau | S2, S5 |
| Bauteilinventar | Materialien und Herkunft dokumentieren | AWM, urselmann interior, Concular | Materialliste / QR-Seiten | Materialherkunftsseite | nicht zutreffend | nicht zutreffend | unbekannt | digital | Transparenz | öffentliche Materialseite | S4 |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Altbau | unbekannt | unbekannt |
| Rückbau | Glastrennwände aus Behrensbau zurückgewinnen | Concular / Partner | Urban Mining | Concular-Plattform | selektiver Ausbau | unbekannt | unbekannt | Düsseldorf -> Münster | Transport/Glasbruch | Plattformbeschaffung | S4, S6 |
| Ausbau | 3. OG umbauen | urselmann interior, Handwerk | zirkulärer Innenausbau | unbekannt | nicht zutreffend | Montage / Reparatur | unbekannt | Baustelle im Bestand | Koordination verschiedener Reuse-Materialien | Design follows availability | S1, S3 |
| Transport | Materialien aus unterschiedlichen öffentlichen Gebäuden | urselmann, Concular, Lieferanten | Einzelbeschaffung | Concular | nicht zutreffend | unbekannt | unbekannt | mehrere Quellen in Deutschland | Logistikaufwand | direkte Beschaffung | S1, S3 |
| Lagerung | unbekannt | unbekannt | unbekannt | unbekannt | nicht zutreffend | unbekannt | unbekannt | unbekannt | wechselnde Verfügbarkeit | unbekannt | unbekannt |
| Aufbereitung | Holz, Kabeltrassen, Stühle, Leuchten anpassen | urselmann interior / Handwerk | Reparatur, Upcycling, Reaktivierung | 3D-Druck für Halterungen | nicht zutreffend | Zuschnitt, Reparatur, Montage | unbekannt | Werkstatt/baustelle | nicht standardisierte Bauteile | handwerkliche Details | S1, S4 |
| Planung | Entwurf nach verfügbaren Bauteilen | urselmann interior | Design follows availability | unbekannt | nicht zutreffend | nicht zutreffend | unbekannt | Materialsuche parallel | Verfügbarkeit statt Katalog | kreatives Handwerk | S1, S3 |
| Genehmigung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Brandschutz/Arbeitsstätten möglich | unbekannt | unbekannt |
| Wiedereinbau | Glastrennwände, Regale, Leuchten, Wandverkleidung montieren | urselmann / Handwerk | feste Montage, demontierbare Details | unbekannt | nicht zutreffend | Wiedereinbau | unbekannt | Baustelle | Passung | Anpassung | S1, S4 |
| Monitoring | zirkuläre Ökobilanzierung | Concular, urselmann | LCA / Vergleich konventionell | Concular | nicht zutreffend | nicht zutreffend | unbekannt | digital | Bilanzgrenzen nicht vollständig offen | Kennwerte publiziert | S3 |

---

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | kein tragender Reuse-Fall | unbekannt | unbekannt | unbekannt | nicht relevant | Bewertung niedrig | S1 |
| Lastabtragung | Kabeltrassen als Regale müssen neue Lasten tragen | Regaltragfähigkeit | unbekannt | unbekannt | alte Kabeltrasse in neuer Funktion | 3D-gedruckte Halterungen | S4 |
| Verbindung | sichtbar/demontierbar, Aufputz-Elektro | Demontierbarkeit, Wartung | unbekannt | unbekannt | Wiederverwendbarkeit | trockenere/zugängliche Details | S1, S4 |
| Brandschutz | Holz-Wandverkleidung, Glaswände, Innenausbau | Brandschutz Arbeitsstätte | unbekannt | unbekannt | keine öffentlichen Nachweise | unbekannt | unbekannt |
| Schallschutz | Glastrennwände und Akustikbaffeln | Büroakustik | unbekannt | unbekannt | gebrauchte Glaswände | Akustikelemente aus PET | S4 |
| Feuchte | WC-Trennwände / Küche | Hygiene/Feuchte | unbekannt | unbekannt | gebrauchte Sanitärtrennwände | unbekannt | S4 |
| Wärmeschutz | nicht Hauptthema | unbekannt | unbekannt | unbekannt | Innenausbau | nicht relevant | unbekannt |
| Wärmebrücken | nicht Hauptthema | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Luftdichtheit | nicht Hauptthema | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| TGA-Integration | Kabeltrassen und ReUse-LED-Leuchten | Elektrosicherheit | unbekannt | unbekannt | gebrauchte technische Bauteile | Reaktivierung / Aufputzführung | S4 |
| Barrierefreiheit | unbekannt | Arbeitsstättenanforderungen | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Dauerhaftigkeit | gebrauchte feste Bauteile im Büroalltag | Robustheit | unbekannt | unbekannt | Gebrauchsspuren | kulturell/gestalterisch genutzt | S1 |
| Wartung | Aufputz, sichtbare und zugängliche Systeme | Wartbarkeit | unbekannt | unbekannt | Umbauflexibilität | demontierbare Details | S1 |
| Zulassung | unbekannt | unbekannt | unbekannt | unbekannt | gebrauchte Bauteile | unbekannt | unbekannt |
| Haftung | unbekannt | unbekannt | unbekannt | unbekannt | Reuse-Bauteile im Innenausbau | unbekannt | unbekannt |

---

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Fläche | 250 | m² | Projektangabe urselmann/AWM | Büroetage | S2, S4 | belegt |
| Fläche | 200 | m² | Drittportfolio | Büroetage | S1 | teilweise belegt / Konflikt |
| wiedergewonnene Materialien | 6,9 | t | Concular zirkuläre Ökobilanzierung | Bauprojekt Büroetage | S1, S3 | belegt |
| Abfallvermeidung | 6,9 | t | Concular | Büroetage | S1, S3 | belegt |
| CO₂-Einsparung | 13,32 | t CO₂e | zirkuläre Ökobilanzierung | gegenüber konventioneller Bauweise | S1–S3 | belegt |
| CO₂-Reduktion | 82 | % | zirkuläre Ökobilanzierung | gegenüber konventioneller Bauweise | S1–S3, S5 | belegt |
| Wassereinsparung | 32 | % | AWM-Angabe | gegenüber konventioneller Bauweise | S5 | belegt |
| c2c-inspiriert oder ReUse | 95,6 | % Produkte | Concular/urselmann | alle Produkte im Ausbau | S1–S3 | belegt, nicht Direct-Reuse-Anteil |
| CO₂-Einsparung Glastrennwände | 4,39 | t CO₂ | AWM Materialseite | Glastrennwände | S4 | belegt |
| CO₂-Einsparung Hanfkalk | 1,7 | t CO₂e | AWM Materialseite | Vergleich zu Kalksandstein | S4 | belegt, nicht Reuse |
| alte Holzstühle für Wandverkleidung | >500 / 550 | Stück | AWM / Drittportfolio | Wandverkleidung | S1, S4 | teilweise belegt |
| Kostenwirkung | vergleichbare Kosten | qualitativ | AWM-Zitat | Gesamtprojekt | S5 | teilweise belegt |
| Bauzeit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |

---

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Interior-Grenzfall | methodisch | Mischung aus Möbel, Bauteilen und Recycling | Gefahr der Überbewertung | Bewertung, Bauteil | feste Bauteile separat werten | Möbel konsequent ausklammern | S1, S4 |
| Beschaffung vieler Einzelquellen | logistisch | Urban Mining aus verschiedenen Gebäuden | Planungs- und Lieferaufwand | Logistik, Bauteilbörse | Concular / Design follows availability | Beschaffung als Entwurfsphase verstehen | S1, S3 |
| Technische Reaktivierung | technisch/rechtlich | gebrauchte Leuchten/Kabeltrassen | Elektrosicherheits- und Tragfähigkeitsfragen | TGA, Prüfung | Aufputz, Spezialhalterungen, Reaktivierung | Wiederverwendung technischer Bauteile braucht Prüfpfad | S4 |
| Brandschutz nicht öffentlich | rechtlich/technisch | Holzverkleidung und gebrauchte Trennwände | unklare Übertragbarkeit | Norm, Prüfung | unbekannt | Prüfberichte veröffentlichen | unbekannt |
| Flächenkonflikt | wissenschaftlich | 200 vs 250 m² in Quellen | unscharfer Maßstab | Kennwert | beide Werte dokumentieren | Primärquelle priorisieren | S1, S2 |
| Qualitätserwartung | sozial/gestalterisch | Gebrauchsspuren werden oft als Mangel gesehen | Abnahme-/Akzeptanzhürde | Gestaltung, Wirtschaft | Spuren als Geschichte und Designwert | Akzeptanz aktiv gestalten | S1 |

---

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** ReUse first, Urban Mining über Concular und direkte Materialsuche; Design & Build durch urselmann interior.
- **Bauteilbörse / Quelle:** Concular für Glastrennwände aus Behrensbau Düsseldorf; weitere Quellen: öffentliche Gebäude, Supermarkt-/Discounter-Auflösung, Schul-/Theaterstühle, AWM-Lager.
- **Kostenwirkung:** AWM nennt vergleichbare Kosten gegenüber konventioneller Bauweise; genaue Kostentabelle unbekannt.
- **Zeitwirkung:** unbekannt.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** hoch durch Suche, Demontage, Aufbereitung, handwerkliche Anpassungen; genaue Stunden unbekannt.
- **Lagerung:** unbekannt.
- **Marktbarrieren:** Abnahmequalität, Norm-/Prüfnachweise, Logistik, unklare Haftung, höhere Planungsflexibilität.

---

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** sehr hoch, besonders Wandverkleidung aus Stuhlteilen, Kabeltrassen-Regale und Glastrennwände.
- **räumliche Transformation:** ungenutztes Verwaltungs-OG wird moderne Arbeitswelt.
- **Atmosphäre / Ausdruck:** Gebrauchsspuren und Materialgeschichten werden zum Gestaltungsthema.
- **Umgang mit Spuren:** ausdrücklich positiv; Spuren gelten nicht als Mangel, sondern als Erzählung.
- **sozialer Wert:** AWM als kommunaler Akteur zeigt Reuse öffentlich und didaktisch.
- **Denkmal- oder Bestandswert:** unbekannt.
- **Kritik / Grenzen:** kleiner Maßstab, überwiegend Innenausbau; Kennwert 95,6 % umfasst auch C2C-/Recyclingprodukte, nicht nur Direct Reuse.

---

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** Normen, Prüfberichte, Tragwerksplanung, Brandschutzdetails, Gewährleistung, detaillierte Kosten.
- **Welche neuen Entitäten wären sinnvoll?** ReUse-Interior; Materialherkunftsseite/QR-Materialatlas; Reaktivierung.
- **Welche Daten fehlen?** Mengen je Bauteil, Prüfungen für Glas und Elektro, konkrete Befestigungen, Arbeitsstunden, Lagerzeiten, CO₂-Methode im Detail.
- **Welche Quellen müssten geprüft werden?** Concular-LCA-Bericht, urselmann-Ausführungspläne, Brandschutzkonzept, Elektroabnahme, Materialpässe/QR-Daten komplett.

---

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** Anhang / niedriger Vergleichsfall; nicht als Hauptfall.
- **5 wichtigste Fakten:**
  1. Das 3. OG des AWM-Verwaltungsgebäudes wurde 2023 zirkulär umgebaut.
  2. 6,9 t wiedergewonnene Materialien und 13,32 t CO₂e Einsparung sind angegeben.
  3. Glastrennwände aus Behrensbau Düsseldorf sind zentrale feste Reuse-Bauteile.
  4. Mehr als 500 alte Stühle wurden als Wandverkleidung umgenutzt.
  5. 95,6 % bezieht sich auf c2c-inspirierte oder ReUse-Produkte, nicht allein Direct Reuse.
- **5 wichtigste Bauteile:**
  1. Glastrennwände und Türen.
  2. WC-Trennwände.
  3. Kabeltrassen als Regale und Leuchtenträger.
  4. Wandverkleidung aus Stuhlteilen.
  5. wiederverwendetes Holz aus Supermarkt-/Discounterkontext.
- **5 wichtigste Hürden:**
  1. Abgrenzung zu Möbeln.
  2. Elektro-/TGA-Prüfung.
  3. Brandschutz für Holz und Glas.
  4. Materialbeschaffung und Passung.
  5. Nachweisführung für Kennwerte.
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Innenausbau ist ein guter Einstieg in Direct Reuse.
  2. Kommunale Bauherrschaft kann als Reuse-Vorbild wirken.
  3. Materialherkunft sollte öffentlich dokumentiert werden.
  4. Gebrauchsspuren brauchen kulturelle Akzeptanz.
  5. Kennwerte müssen ReUse, Recycling und C2C getrennt ausweisen.
- **5 offene Fragen:**
  1. Welche Prüfungen gab es für Glastrennwände und Türen?
  2. Welche Elektroprüfungen wurden für ReUse-Leuchten durchgeführt?
  3. Welche konkreten Kostenpositionen änderten sich?
  4. Wie viel der 95,6 % ist wirklich Direct Reuse?
  5. Sind alle festen Bauteile sortenrein demontierbar dokumentiert?

---

## Quellen und Links

- **S1** Petra Jablonická Portfolio, „95,6% circular reconstruction of offices for AWM Münster“ – https://www.jablonicka.com/work/95%2C6%25-circular-reconstruction-of-offices-for-awm-m%C3%BCnster-
- **S2** urselmann interior, „AWM“ – https://www.urselmann-interior.de/awm-office
- **S3** Concular, „Zirkuläres Bauen funktioniert: 95,6% zirkuläre Beschaffung für Bauprojekt in Münster“ – https://concular.de/bueroetage-muenster/
- **S4** AWM Münster, „Material“ – https://awm.stadt-muenster.de/gemeinsam-nachhaltig/klima-technik-innovation/kreislauffaehiges-bauen/material
- **S5** AWM Münster, „Moderne Arbeitswelt aus gebrauchten Materialien“ – https://awm.stadt-muenster.de/aktuelles/newsdetail/moderne-arbeitswelt-aus-gebrauchten-materialien
- **S6** AWM Münster, „Küche“ – https://awm.stadt-muenster.de/gemeinsam-nachhaltig/klima-technik-innovation/kreislauffaehiges-bauen/kueche
