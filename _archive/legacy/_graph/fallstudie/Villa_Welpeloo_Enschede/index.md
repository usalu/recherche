---
id: "Villa_Welpeloo_Enschede"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "Villa Welpeloo, Enschede — Fallstudie Direct Reuse / Bauteilwiederverwendung"
bauobjekt:
  - "Villa_Welpeloo_Enschede"
legacy_paths:
  - "Gebäude\\Villa_Welpeloo_Enschede.md"
projekt:
  - "Villa_Welpeloo_Enschede"
reuse_chain_detected: "False"
---
# Villa Welpeloo, Enschede — Fallstudie Direct Reuse / Bauteilwiederverwendung

## Migration

- Fallstudie ID: Villa_Welpeloo_Enschede
- Legacy source count: 1
- Generated project: Villa_Welpeloo_Enschede
- Generated bauobjekt: Villa_Welpeloo_Enschede
- Extracted reuse_einsatz rows: 11
- Extracted datenpunkt rows: 14
- Extracted entity mapping rows: 22
- Reuse chain detected: False

## Legacy Content

### Legacy Source: Gebäude\Villa_Welpeloo_Enschede.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Villa_Welpeloo_Enschede
- Secondary targets: projekt/Villa_Welpeloo_Enschede; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Villa Welpeloo, Enschede — Fallstudie Direct Reuse / Bauteilwiederverwendung

**Arbeitsstand:** 2026-05-06  
**Sprache:** Deutsch  
**Grundregel:** Gewertet werden nur wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Lose Möbel/Dekoration werden nicht für die Bewertung herangezogen.

---

## 1. EINORDNUNG

- **Entscheidung:** HAUPTFALL
- **Bewertung:** ★★★★★
- **Begründung:** Die Villa Welpeloo wurde von verfügbaren Materialströmen aus der Umgebung her entworfen. Die tragende Konstruktion besteht aus wiederverwendeten Stahlträgern einer Paternoster-/Textilindustriemaschine; eine einzige Maschine lieferte laut Superuse genug Stahl für die gesamte Villa. Zusätzlich besteht die Fassadenbekleidung aus Holz von überzähligen/beschädigten Kabeltrommeln. Die Bewertung stützt sich auf die tragende Stahlwiederverwendung.
- **Vertrauensgrad:** belegt
- **Warnung Bestandserhalt:** nein
- **Warnung Möbel/Dekoration:** ja; Lichtobjekte aus Regenschirmrippen, Kaffee-Becher-Wandbekleidungen oder Möbel werden nur erwähnt, aber nicht für die Bewertung gewertet, sofern sie nicht fest eingebaut und bautechnisch relevant sind.
- **Projektstatus:** gebaut

---

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Villa Welpeloo | Untersuchter Direct-Reuse-Fall | S1, S2 | belegt | Wohnhaus/Kunsthaus in Enschede |
| Gebäude | Wohnhaus mit Ausstellungs-/Kunstlagerfunktion | Neubau mit hohem Anteil geborgener Materialien | S1, S4 | belegt | Nutzung als Wohnhaus und Kunstraum |
| Ort | Roombeek, Enschede, Niederlande | Standort | S1, S4 | belegt | ehemals industriell geprägte Region |
| Projekt | Villa Welpeloo | Projektname | S1 | belegt | Fertigstellung 2009 laut Superuse |
| People | Jan Jongert, Jeroen Bergsma, Team Superuse/2012Architecten | Entwurf und Materialstrategie | S4, S7 | belegt | Büro firmierte auch als 2012Architecten |
| Architekt | Superuse Studios / 2012Architecten | Entwurfsverantwortung | S1, S4 | belegt | heutige Quelle: Superuse |
| Tragwerksplaner | Nico Plukkel | Tragwerksplanung | S4 | teilweise belegt | Quelle Architectuurgids |
| Bauherr | privat; Tjibbe Knol / Ingrid Blans in Architectuurgids genannt | Auftraggeber | S4 | teilweise belegt | private Bauherrschaft |
| Reuse-Strategie | Materialgetriebener Entwurf / Superuse | Entwurf nach verfügbaren Bauteilen | S1, S2 | belegt | „scouts“ suchten Materialflüsse |
| Bauteil | Stahlträger aus Paternoster/Textilmaschine | Tragende Hauptstruktur | S1, S2, S3 | belegt | Eine Maschine ausreichend für gesamte Villa |
| Bauteil | Holz aus Kabeltrommeln | Fassadenbekleidung | S1, S2, S5 | belegt | Kabeltrommeln der Twentse/Twente cable factory |
| Bauteil | Bau-/Montagelift, später Innenlift | fest eingebautes technisches/raumbezogenes Element | S1 | teilweise belegt | Nicht tragende Hauptbewertung |
| Material | Stahl, Holz, Polystyrol, Werbetafeln, weitere lokale Reststoffe | Materialpalette | S1, S2, S5 | teilweise belegt | Nicht alles zählt als Direct Reuse |
| Methode | Harvest Map / Materialscouting | Identifikation verfügbarer Materialströme | S1, S2 | belegt | Google Earth und lokale Kontakte laut EMF |
| Tool | Harvestmap / Oogstkaart | Folge-/Konzeptwerkzeug für Materialquellen | S2, S6 | teilweise belegt | Für Villa als methodische Vorläuferin genannt |
| Prüfung | Tragwerksberechnung mit schlechtester Stahlqualität aus Baujahr der Maschine | Nachweis für reused steel | S3 | belegt | konkrete Prüfprotokolle unbekannt |
| Aufbereitungsmethode | geringe Veränderung / Anpassung; Fassadenreserve angelegt | Reparatur-/Wartungsstrategie | S3 | teilweise belegt | Details unbekannt |
| Schadstoff | toxische Bahnschwellen/-platten als verworfene Option | Hürde in Materialwahl | S6 | teilweise belegt | genaue Stoffe unbekannt |
| Kennwert | ca. 60 % salvaged materials | Gesamtmaterialkennwert | S2, S6, S7 | teilweise belegt | Quellen teils 60 % Gesamt, teils 60 % außen / 90 % innen |
| Kennwert | 90 % CO₂-Reduktion für Konstruktion und Fassade | Umweltkennwert | S1, S6 | teilweise belegt | Methodik/Bilanzgrenze nicht vollständig publiziert |
| Wirtschaft | unbekannt | Kostenwirkung Reuse nicht belastbar | - | unbekannt | Einzelne Baukostenquelle vorhanden, aber nicht reuse-spezifisch |
| Norm | unbekannt | keine Normnummer publiziert | - | unbekannt | - |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Materialscout | Das Projekt begann mit aktiver Suche nach Bauteilen, nicht mit konventioneller Spezifikation | Scouts untersuchten verfügbare Materialien in der Umgebung | verbindet Methode, Logistik, Bauteil |
| Materialgetriebener Entwurf | Der Entwurf folgt vorhandenen Querschnitten/Materialien | Stahl aus einer Textilmaschine prägt Tragwerk | verbindet Reuse-Strategie, Tragwerkssystem |
| Reserve-/Ersatzteillager | Bei Sonder-Bauteilen ist spätere Wartung problematisch | zusätzliche Fassadenleisten wurden beschafft | verbindet Wartung, Wirtschaft, Logistik |
| Verworfenes Reuse-Bauteil | Für Forschung wichtig, weil nicht jedes gefundene Bauteil nutzbar ist | toxische Railway Slabs wurden verworfen | verbindet Schadstoff, Prüfung, Hürde |

---

## 3. FALLSTUDIE

- **Name:** Villa Welpeloo
- **Ort:** Roombeek, Enschede, Niederlande
- **Gebäude:** freistehendes Wohnhaus mit Kunstlager-/Ausstellungsfunktion
- **Projekt:** Neubau eines materialgetriebenen, zirkulären Wohnhauses
- **Beteiligte People / Akteure:** Superuse Studios / 2012Architecten; Jan Jongert; Jeroen Bergsma; private Bauherrschaft; Nico Plukkel laut Architectuurgids; TKF/Twente cable factory als Materialquelle für Kabeltrommelholz
- **Architekt:** Superuse Studios / 2012Architecten
- **Tragwerksplaner:** Nico Plukkel laut Architectuurgids
- **Bauherr:** privat; Namen öffentlich in Architectuurgids genannt
- **Zeitraum:** Entwurf ab ca. 2005; Fertigstellung 2009 laut Superuse/Architectuurgids
- **Ursprüngliche Nutzung:** Stahl aus Paternoster/Textilindustriemaschine; Holz aus Kabeltrommeln; weitere Reststoffe aus lokaler Industrie
- **Neue Nutzung:** Wohnen, Kunstlager, Ausstellung, Studio
- **Fläche / Maßstab:** uneinheitlich: Architectuurgids nennt 250 m² BGF; andere Sekundärquellen nennen 312 m² oder 400 m²; belastbare genaue Fläche daher unbekannt
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** sehr gut für Hauptbauteile und Strategie; mittel für Mengen/Fläche; schwach für Normen, Prüfprotokolle und Kosten

---

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; materialgetriebener Entwurf; ergänzend Upcycling
- **Hauptniveau:** Tragwerk und Gebäudehülle
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die Villa ist ein Neubau. Die Stahlträger und Fassadenhölzer behalten als Bauteile eine neue Funktion und werden nicht nur stofflich recycelt. Daher Direct Reuse. Kleinteilige Objekte wie Schirmrippen sind gestalterisch interessant, aber nicht ausschlaggebend für die Bewertung.
- **Warum ist der Fall relevant?** Das Projekt zeigt früh und gut dokumentiert, dass Tragwerksentwurf aus lokal verfügbaren Reuse-Bauteilen entstehen kann, inklusive Verantwortungs- und Prüfstrategien.

---

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Stahlträger / Stahlrahmen | Stahl | Paternoster/Textilindustriemaschine aus Region Enschede | Maschinentragstruktur / textile Produktion | Tragende Konstruktion der Villa | eine Maschine ausreichend; genaue t unbekannt | ja | nein | nein | nein | Demontage, Zuschnitt/Anpassung unbekannt | unbekannt | Tragwerksberechnung mit schlechtester Stahlqualität aus Maschinenjahr | Tragfähigkeit Wohnhaus | Normnummer unbekannt | Materialnachweis/Verantwortung | S1, S2, S3 | Gewicht, Profiltypen |
| Holzfassade | Holz | beschädigte/überzählige Kabeltrommeln von Twente/Twentse cable factory | Kabeltrommelkern/-slats | Fassadenbekleidung | genaue Menge unklar; eine Quelle nennt 1.000 reels, andere 200 reels; daher unbekannt | nein | nein | ja | nein | Auswahl, Zuschnitt, Montage; Zusatzleisten für Wartung | unbekannt | unbekannt | Witterung, Dauerhaftigkeit | unbekannt | Sondermaße/Wartung | S1, S3, S5 | korrekte Stückzahl |
| Bau-/Montagelift als Innenlift | Stahl/Technik | Baugerät für Montage der Stahlstruktur | Baustellenlift | fester Innen-/Lastenlift für Kunsttransport | 1 | nein | ja | nein | ja | Weiterverwendung im Innenraum | unbekannt | unbekannt | Betriebssicherheit | unbekannt | Zulassung unbekannt | S1 | genaue technische Zulassung |
| Polystyrol-Dämmplatten | Polystyrol | Restplatten eines Caravan-Herstellers laut Sekundärquellen | Produktionsrest | Dämmung | unbekannt | nein | nein | ja | nein | Zuschnitt | unbekannt | unbekannt | Wärmeschutz/Brandschutz | unbekannt | Brand-/Zulassungsfragen unbekannt | S5, S6 | Einbauumfang |
| Alte Werbetafeln / billboard boards | Kunststoff/Verbund unbekannt | alte Werbetafeln | Werbung | Schränke/feste Einbauten laut Sekundärquellen | unbekannt | nein | ja | nein | nein | Zuschnitt | unbekannt | unbekannt | Innenausbau | unbekannt | Oberflächenqualität | S5, S6 | fest eingebauter Umfang |
| Regenschirmrippen-Leuchten | Metall/Kunststoff | gebrauchte Regenschirme | Schirmrippen | Leuchten | unbekannt | nein | nein | nein | ja | künstlerische Umnutzung | unbekannt | unbekannt | Elektrosicherheit | unbekannt | zählt nicht für Hauptbewertung | S1 | fest/lose Einordnung |
| Innenwände | unbekannt | unbekannt | unbekannt | Raumtrennung | unbekannt | nein | ja | nein | nein | unbekannt | unbekannt | unbekannt | Schall/Brand | unbekannt | unbekannt | - | alles |
| Fenster | unbekannt | unbekannt | unbekannt | Fenster | unbekannt | nein | nein | ja | nein | unbekannt | unbekannt | unbekannt | Wärmeschutz/Luftdichtheit | unbekannt | unbekannt | - | alles |
| Türen | unbekannt | unbekannt | unbekannt | Türen | unbekannt | nein | ja | nein | nein | unbekannt | unbekannt | unbekannt | Brand/Schall | unbekannt | unbekannt | - | alles |
| Dach | unbekannt | unbekannt | unbekannt | Dach | unbekannt | teilweise | nein | ja | nein | unbekannt | unbekannt | unbekannt | Tragwerk/Feuchte | unbekannt | unbekannt | - | alles |
| Sanitär | unbekannt | unbekannt | unbekannt | Sanitär | unbekannt | nein | ja | nein | ja | unbekannt | unbekannt | unbekannt | Hygiene | unbekannt | unbekannt | - | alles |

---

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Lokale Materialflüsse suchen | Superuse/2012Architecten, Materialscouts | Materialscouting in Umgebung | Google Earth laut EMF; Harvest Map/Oogstkaart als spätere Methode | unbekannt | unbekannt | erste Eignungsprüfung | lokale Industriequellen | Material ist verfügbar, aber nicht katalogisiert | aktive Suche und Netzwerke | S1, S2 |
| Bauteilinventar | Stahlmaschine und Kabeltrommeln als Ausgangsmaterial erfassen | Architekten, Tragwerksplaner | Entwurf aus gefundenen Bauteilen | Harvest Map visuell dokumentiert | selektiver Ausbau unbekannt | unbekannt | Tragwerksberechnung | Nähe zur Baustelle | Dimensionen vorgegeben | Design an Bauteile angepasst | S1, S3 |
| Schadstoffprüfung | Verwerfen ungeeigneter Materialien | Planungsteam | Materialtests und Beratung | unbekannt | - | - | Tests laut Circle Economy | lokale Quellen | toxische Railway Slabs als Problem | Umplanung / Material nicht genutzt | S6 |
| Rückbau | Demontage Paternoster/Textilmaschine | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | regional | unbekannt | unbekannt | S1 |
| Ausbau | Gewinnung von Holzleisten aus Kabeltrommeln | unbekannt | Zerlegung der Kabeltrommeln | unbekannt | - | Auswahl/Zuschnitt | unbekannt | Transport vom Kabelwerk | beschädigte Trommeln, Sortierung | Nutzung standardisierter Leisten | S1, S5 |
| Transport | Transport lokaler Materialien zur Baustelle | unbekannt | lokal/regional | unbekannt | - | - | unbekannt | Radius 15 km/9 miles in Sekundärquellen, nicht in Primärquelle belegt | unbekannt | lokale Beschaffung | S2, S5 |
| Lagerung | Material bis Einbau vorhalten | Bau-/Planungsteam | unbekannt | unbekannt | - | - | unbekannt | unbekannt | Sonderbauteile für Reparatur schwer verfügbar | zusätzliche Fassadenleisten beschafft | S3 |
| Aufbereitung | Stahl und Holz anpassen | Stahlbauer/Schreiner unbekannt | minimalinvasive Anpassung | unbekannt | - | Zuschnitt, Montage | unbekannt | Werkstatt/Baustelle | nicht standardisierte Bauteile | materialgetriebene Detaillierung | S1 |
| Planung | Dynamischer Entwurf nach Materialverfügbarkeit | Architekten, Engineer, Bauherr | Superuse-Methode | Harvest Map/Google Earth als Suchhilfe | - | - | Engineer-Kalkulation | Entwurf und Beschaffung parallel | Entwurf nicht vollständig vorab fixierbar | flexible/dynamische Planung | S1, S2, S6 |
| Genehmigung | Nachweis reused steel | Engineer, Behörden unbekannt | Berechnung mit konservativer Stahlqualität | unbekannt | - | - | Tragwerksberechnung | unbekannt | Garantien für Reuse-Bauteile selten | Verantwortung teilen / externe Prüfung möglich | S3 |
| Wiedereinbau | Stahlrahmen und Holzfassade montieren | Bauunternehmen unbekannt | Neubau mit wiederverwendeten Bauteilen | unbekannt | - | vorbereitetes Material | unbekannt | unbekannt | Passungen/Unikate | handwerkliche Anpassung | S1 |
| Monitoring | CO₂-/Materialwirkung kommuniziert | Superuse, spätere Plattformen | Impact-Kommunikation | unbekannt | - | - | unbekannt | - | Methodik nicht offen | Angabe als Projektimpact | S1, S6 |

---

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Stahlrahmen aus Paternoster-/Textilmaschinenstahl | Tragfähigkeit Wohnhaus | unbekannt | Engineer-Berechnung | unbekannte Stahlqualität | konservativ schlechteste Stahlqualität aus Baujahr angenommen | S3 |
| Lastabtragung | Reused steel bildet tragende Hauptstruktur | vertikale/horizontale Lasten | unbekannt | statische Berechnung | Profilgeometrie aus Maschine | Entwurf an vorhandene Stahlprofile angepasst | S1, S3 |
| Verbindung | unbekannt | Tragfähigkeit, Montage | unbekannt | unbekannt | vorhandene Profile nicht Normstandard | unbekannt | - |
| Brandschutz | für Stahl/Dämmung/Fassade unbekannt | Brandschutz Wohnhaus | unbekannt | unbekannt | reused + Polystyrol möglich kritisch | unbekannt | - |
| Schallschutz | unbekannt | Wohnkomfort | unbekannt | unbekannt | unbekannt | unbekannt | - |
| Feuchte | Holzfassade aus Kabeltrommelholz | Witterungsbeständigkeit | unbekannt | unbekannt | Wiederverwendetes Holz im Außenraum | Ersatzleisten/Stockpiling | S3 |
| Wärmeschutz | Rest-Polystyrol als Dämmung laut Sekundärquellen | Wärmeschutz | unbekannt | unbekannt | Brandschutz/Zulassung unbekannt | unbekannt | S5, S6 |
| Wärmebrücken | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | - |
| Luftdichtheit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | - |
| TGA-Integration | Installationsleitungen in Wänden integriert; Bau-/Lastenlift als Innenfunktion | Betrieb Kunsthaus/Wohnen | unbekannt | unbekannt | Reuse-Lift-Zulassung unbekannt | unbekannt | S1 |
| Barrierefreiheit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | - |
| Dauerhaftigkeit | Holzfassade als Sonderbauteil mit Reserveleisten | Wartbarkeit | unbekannt | unbekannt | Ersatz schwer erhältlich | zusätzliche Leisten gekauft | S3 |
| Wartung | Reserve für Fassadenmaterial | Reparaturfähigkeit | unbekannt | unbekannt | Sonderquelle versiegt | Stockpiling | S3 |
| Zulassung | keine allgemeinen Garantien für Reuse-Materialien | Nachweisfähigkeit | unbekannt | Engineer/ggf. externe Prüfung | fehlende Lieferantengarantien | Verantwortung teilen / externe Beurteilung / Stockpiling | S3 |
| Haftung | Team-/Bauherrnverantwortung statt Standardgarantie | Sicherheit/Gewährleistung | unbekannt | Engineer-Berechnung | geringe Reuse-Garantien | Rollenklärung | S3 |

---

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Anteil salvaged/reused materials | ca. 60 | % | Projektbericht/Sekundärdarstellung | Gesamtmaterial, genaue Methode unbekannt | S2, S6, S7 | teilweise belegt |
| Anteil Innenausbau reused | ca. 90 | % | Sekundärquelle | Innenausbau | S5, S7 | teilweise belegt |
| CO₂-Reduktion Struktur und Fassade | ca. 90 | % | nicht offengelegte Methodik | Konstruktion und Fassade | S1, S6 | teilweise belegt |
| Fertigstellung | 2009 | Jahr | Projektseite | Projekt | S1, S4 | belegt |
| Entwurfsbeginn | 2005 | Jahr | Architectuurgids / DASH | Projekt | S4, S8 | teilweise belegt |
| Fläche | 250 / 312 / 400 | m² | widersprüchliche Quellen | Gebäudefläche | S4, S9, S5 | unklar |
| Wiederverwendeter Stahl | unbekannt | t | - | Tragwerk | - | unbekannt |
| Anzahl Kabeltrommeln | unbekannt | Stück | Quellen widersprechen: 200 bzw. 1.000 | Fassade | S5, S10 | unklar |
| Kosten | unbekannt reuse-spezifisch | - | - | Reuse | - | unbekannt |
| Bauzeit | unbekannt | - | - | Projekt | - | unbekannt |
| Energiebedarf | unbekannt | - | - | Betrieb | - | unbekannt |
| U-Wert | unbekannt | - | - | Fassade | - | unbekannt |
| Lebensdauer | unbekannt | - | - | Bauteile | - | unbekannt |
| Zirkularitätskennwert | unbekannt | - | - | - | - | unbekannt |

---

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Materialsuche vor Entwurf | logistisch/gestalterisch | Kein Standardmarkt für passende Reuse-Bauteile | längere und dynamische Planung | Methode, Logistik, Bauteil | Materialscouting, lokale Industriekontakte | Entwurf muss auf Fundmaterial reagieren | S1, S2 |
| Stahlqualität nachweisen | technisch/rechtlich | gebrauchte Maschinenstahlprofile ohne Standardgarantie | Risiko für Tragwerk | Prüfung, Norm, Recht | konservative Engineer-Berechnung | Reuse braucht belastbare Nachweisstrategie | S3 |
| Schadstoffe / ungeeignete Materialien | technisch/rechtlich | zuerst erwogene Materialien können toxisch sein | Umplanung | Schadstoff, Prüfung, Bauteil | Materialtests und Ausschluss | Nicht jedes gefundene Material ist nutzbar | S6 |
| Wartung von Unikat-Fassade | technisch/logistisch | Sonderbauteile später schwer beschaffbar | Instandhaltungsrisiko | Fassade, Wirtschaft | Reserveleisten beschaffen | Ersatzteillogik bei Reuse mitplanen | S3 |
| Verantwortungs-/Garantiefrage | rechtlich/wirtschaftlich | Reuse-Lieferanten bieten selten Garantien | Unsicherheit für Bauherr/Planer | Recht, Wirtschaft | Verantwortung teilen oder externe Prüfung | Vertragliche Rollen früh klären | S3 |
| Quellen widersprechen bei Mengen/Flächen | methodisch | Sekundärquellen variieren | Unsicherheit in Datenbank | Kennwert | Primärquellen bevorzugen; unbekannt markieren | Datenqualität getrennt bewerten | eigene Auswertung |

---

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** direkte lokale Materialsuche / Materialscouting; kein konventioneller Katalogprozess.
- **Bauteilbörse / Quelle:** Harvestmap/Oogstkaart ist als Methode/Tool mit Superuse verbunden; für die Villa selbst sind lokale Industriequellen belegt, keine konkrete Bauteilbörse als Transaktionsplattform.
- **Kostenwirkung:** unbekannt; eine Quelle nennt Baukosten, aber nicht reuse-spezifisch und daher nicht als Kostenwirkung verwertbar.
- **Zeitwirkung:** verlängerte bzw. dynamische frühe Planungsphase durch Materialsuche und Tests; konkrete Zeitkosten unbekannt.
- **Versicherung / Haftung:** Superuse beschreibt geteilte Verantwortung, externe Prüfung und Stockpiling als Strategien; konkrete Vertrags-/Versicherungsdetails unbekannt.
- **Gewährleistung:** unbekannt
- **Arbeitsaufwand:** erhöhter Aufwand für Materialsuche, Prüfung, Detaillierung und Anpassung.
- **Lagerung:** Reserve für Fassadenleisten belegt; Lagerort/-menge unbekannt.
- **Marktbarrieren:** fehlende Garantien, fehlende Standardisierung, Schadstoffrisiko, unklare Qualität gebrauchter Bauteile.

---

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** sehr hoch; Holzfassade aus Kabeltrommeln und industrielle Stahlgeschichte sind Teil der architektonischen Identität.
- **räumliche Transformation:** Industriebauteile werden in ein Wohn-/Kunsthaus überführt; der Innenraum ist als Ausstellungsraum organisiert.
- **Atmosphäre / Ausdruck:** zurückhaltendes Interieur für Kunst, zugleich sichtbar industrielle Materialgeschichte.
- **Umgang mit Spuren:** Materialspuren werden nicht vollständig verborgen; Fassade zeigt variierende Texturen/Farbigkeit.
- **sozialer Wert:** Referenzprojekt für Superuse-Methode und materialgetriebenen Entwurf; didaktischer Wert hoch.
- **Denkmal- oder Bestandswert:** kein Denkmalstatus bekannt; kultureller Wert liegt in regionaler Industriegeschichte der Bauteile.
- **Kritik / Grenzen:** geringe Größe, Einfamilienhausmaßstab, viele Kennwerte nicht transparent; einige Elemente sind eher Upcycling/Designobjekte und dürfen nicht ratingrelevant sein.

---

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** Normnummern, Brandschutzdetails, Stahlprüfprotokolle, genaue Profil-/Gewichtslisten, komplette Bauteilherkunft, detaillierte Kosten, Genehmigungsunterlagen.
- **Sinnvolle neue Entitäten:** Materialscout, materialgetriebener Entwurf, Ersatzteillager, verworfenes Reuse-Bauteil.
- **Fehlende Daten:** Menge der Stahlprofile, korrekte Anzahl Kabeltrommeln, tatsächlicher Reuse-Anteil nach Bauteilgruppen, U-Werte, Lebensdauer, Haftungsmodell.
- **Zu prüfende Quellen:** Superuse-Projektarchiv, Bauantrag Enschede, Statik Nico Plukkel, Werkstatt-/Montagepläne, Oogstkaart/Harvestmap-Archive.

---

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja

### 5 wichtigste Fakten

1. Die tragende Struktur besteht aus Stahlträgern einer früheren Textil-/Paternostermaschine.
2. Eine einzige Maschine lieferte laut Superuse genug Stahl für die gesamte Villa.
3. Die Fassadenbekleidung besteht aus Holz überzähliger/beschädigter Kabeltrommeln.
4. Das Projekt wurde materialgetrieben entworfen; Materialscouts suchten Quellen in der Umgebung.
5. Superuse nennt eine 90-%-CO₂-Reduktion für Konstruktion und Fassade, Methodik nicht vollständig öffentlich.

### 5 wichtigste Bauteile

1. Wiederverwendete Stahlträger
2. Wiederverwendete Holzleisten aus Kabeltrommeln
3. Wiederverwendeter Bau-/Lastenlift als Innenfunktion
4. Rest-/Reuse-Dämmplatten, soweit eingebaut
5. Feste Einbauten aus Werbetafeln/Restmaterialien, soweit tatsächlich fest eingebaut

### 5 wichtigste Hürden

1. Materialsuche und Verfügbarkeit
2. Tragwerksnachweis für gebrauchten Maschinenstahl
3. Schadstoff-/Materialeignung
4. Wartung und Ersatzteilversorgung bei Sonderbauteilen
5. Fehlende Garantien und klare Haftungsmodelle

### 5 wichtigste übertragbare Erkenntnisse

1. Ein Gebäude kann aus verfügbaren Bauteilen heraus entworfen werden.
2. Tragwerksreuse braucht frühe Einbindung von Engineer und Bauherr.
3. Lokale industrielle Restströme können hochwertige Bauteile liefern.
4. Stockpiling/Ersatzteile sind Teil der Dauerhaftigkeitsstrategie.
5. Nicht jedes gestalterische Upcycling-Element sollte als bautechnischer Direct Reuse gewertet werden.

### 5 offene Fragen

1. Wie viele Tonnen Stahl wurden genau eingebaut?
2. Welche Prüfungen und Nachweise liegen für den Stahl vor?
3. Welche Fläche ist für die Fallstudie verbindlich?
4. Welche konkreten Kosten-/Zeitwirkungen hatte die Materialsuche?
5. Welche Reuse-Bauteile sind nach Jahren Betrieb wartungsintensiv?

---

## Quellen und Links

- **S1 – Superuse Studios: Villa Welpeloo.** https://www.superuse-studios.com/projectplus/villa-welpeloo/
- **S2 – Ellen MacArthur Foundation: Finding and utilising waste materials for construction purposes.** https://www.ellenmacarthurfoundation.org/circular-examples/finding-and-utilising-waste-materials-for-construction-purposes
- **S3 – Superuse Studios: About / Permits and Warranties; Villa Welpeloo reference.** https://www.superuse-studios.com/about-us/
- **S4 – Architectuurgids: Villa Welpeloo.** https://www.architectuur.org/bouwwerk/42/Villa_Welpeloo.html
- **S5 – Construção Sustentável: Villa Welpeloo.** https://csustentavel.com/en/villa-welpeloo-i-salveged-house/
- **S6 – Circle Economy Knowledge Hub: Villa Welpeloo.** https://knowledge-hub.circle-economy.com/article/30046
- **S7 – e-genius: Villa Welpeloo.** https://www.e-genius.at/lernfelder/energieeffiziente-gebaeudekonzepte/innovative-baukonzepte/innovative-beispiele-fuer-bauen-mit-recyclingmaterialien/villa-welpeloo
- **S8 – DASH / TU Delft: Villa Welpeloo Enschede.** https://journals.open.tudelft.nl/dash/article/view/4751
- **S9 – Circular Material Systems: Villa Welpeloo.** https://circularmaterialsystems.com/en/case/villa-welpeloo/
- **S10 – Tea After Twelve: Villa Welpeloo constructed from waste materials.** https://www.tea-after-twelve.com/all-issues/issue-03/issue-03-overview/chapter1/villa-welpeloo-constructed-from-waste-materials/
