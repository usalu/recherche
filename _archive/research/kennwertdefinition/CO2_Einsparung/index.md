---
entity: "kennwertdefinition"
id: "CO2_Einsparung"
title: "CO2-Einsparung"
build_status: "promoted_phase42"
legacy_paths:
  - "kennwert\CO2_Einsparung.md"
node_kind: "knot"
legacy_type: "Kennwert"
---

# CO2-Einsparung

# CO2-Einsparung

## Verknüpfungen

- **Übergeordnete Themen:** Kennwerte; Ökobilanzierung / Life Cycle Assessment; Klimaschutz im Gebäudesektor; zirkuläres Bauen; Entwerfen mit Bestand; Urban Mining.
- **Verwandte Dateien:** `kennwert/Graue_Energie.md`; `kennwert/Demontagegrad.md`; `kennwert/Wiederverwendungsquote.md`; `kennwert/Materialwert.md`; `dokument/LCA.md`; `methode/ReUse_Assessment.md`; `datenmodell/`; `wirtschaft/`; `standard/`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** DIN EN 15978; DIN EN 15804+A2; ISO 14040/14044; ISO 21930; Level(s) Indikator 1.2 „Life cycle Global Warming Potential“; ÖKOBAUDAT; eLCA; EPD nach EN 15804; DGNB Building Resource Passport; BNB; RICS Whole Life Carbon Assessment; K.118 Kopfbau Halle 118 Winterthur; ReUse-Pilotprojekte Stadt Zürich; Rotor / Rotor DC; Concular; Madaster; selektiver Rückbau; Pre-demolition Audit; vergleichende Szenariobilanz; Modul-D-Bilanzierung.

## Kurzdefinition

**CO2-Einsparung** bezeichnet im ReUse-Kontext die Differenz der Treibhausgasemissionen zwischen einem Wiederverwendungsszenario und einem definierten Referenzszenario, meist einem Szenario mit neu produzierten Bauteilen gleicher Funktion. Der Kennwert wird in der Regel als **kg CO2-Äquivalente** oder **t CO2e** angegeben; gebäudebezogen auch als **kg CO2e/m²**, **kg CO2e/m²a** oder als prozentuale Reduktion gegenüber einem Referenzfall.

Der Kennwert ist kein Materialkennwert an sich. Er ist ein **Vergleichsergebnis** und hängt von Systemgrenze, Referenzprodukt, Transport, Aufbereitung, Nutzungsdauer, Allokation und End-of-Life-Annahmen ab.

Kernformel:

```text
CO2-Einsparung = GWP_Referenzszenario - GWP_Wiederverwendungsszenario
```

Bei positiver Differenz spart Wiederverwendung Treibhausgasemissionen gegenüber der Referenz. Bei negativer Differenz ist das ReUse-Szenario klimawirksam schlechter, etwa durch sehr weite Transporte, intensive Aufbereitung, kurze Restnutzungsdauer oder ungeeignete Substitution.

## Relevanz für Wiederverwendung im Bauwesen

CO2-Einsparung ist einer der wichtigsten Wirkungskennwerte zur Begründung von Bauteilwiederverwendung. Viele Wiederverwendungsentscheidungen werden nicht primär über Masse, Stückzahl oder Kosten, sondern über vermiedene **Herstellungs- und Beschaffungsemissionen** plausibel. Die größte Hebelwirkung liegt häufig bei emissionsintensiven Bauteilen und Materialien wie Stahl, Aluminium, Glas, Betonfertigteilen, Naturstein, Ziegeln, technischen Anlagen und Innenausbausystemen mit hohem Herstellungsaufwand.

Für die Forschung zu „Entwerfen mit Bestand“ ist der Kennwert besonders relevant, weil er drei Ebenen verbindet:

1. **Entwurfsentscheidung:** Erhalt, Umnutzung, Erweiterung, Rückbau oder Ersatz.
2. **Bauteilentscheidung:** Wiederverwenden, reparieren, aufbereiten, recyceln oder neu beschaffen.
3. **Projekt- und Politikbewertung:** Klimabilanz, Taxonomie-/ESG-Berichterstattung, Zertifizierung, Förderlogik, Beschaffungsanforderungen.

CO2-Einsparung ist jedoch nur belastbar, wenn der Vergleich funktional äquivalent ist. Ein wiederverwendetes Fenster darf nicht allein mit einem neuen Fenster verglichen werden, wenn U-Wert, Luftdichtheit, Restlebensdauer, Wartungsbedarf, Brandschutz oder Schallschutz deutlich abweichen. Der Kennwert muss deshalb immer zusammen mit Funktionseinheit, technischer Gleichwertigkeit und Datenqualität dokumentiert werden.

## Fachinhalt

### Abgrenzung zu Grauer Energie

CO2-Einsparung und Graue Energie sind verwandt, aber nicht identisch:

- **CO2-Einsparung** misst Klimawirkung in kg CO2e. Sie umfasst Kohlendioxid, Methan, Lachgas und weitere Treibhausgase über Charakterisierungsfaktoren.
- **Graue Energie** misst den kumulierten Primärenergieaufwand, meist in MJ oder kWh. Sie sagt zunächst nichts direkt über CO2e aus, weil der gleiche Energieaufwand je nach Energieträger, Strommix und Prozess sehr unterschiedliche Emissionen verursachen kann.
- Prozessbedingte Emissionen, etwa bei Zementklinker, Kalk oder Metallurgie, können auch dann hoch sein, wenn der reine Energieindikator nicht proportional ansteigt.
- Wiederverwendung kann sowohl Primärenergie als auch CO2e senken, aber die Rangfolge von Maßnahmen kann je nach Indikator verschieden sein.

### Übliche Einheit und Bezugsgrößen

- **Bauteilbezogen:** kg CO2e je Bauteil, je m² Bauteilfläche, je kg Material, je Stück.
- **Gebäudebezogen:** kg CO2e/m² Nutzfläche, Bruttogrundfläche oder Energiebezugsfläche.
- **Lebenszyklusbezogen:** kg CO2e/m²a über einen Referenzbetrachtungszeitraum, häufig 50 Jahre in europäischen Bewertungsrahmen.
- **Portfolio- oder Beschaffungsbezogen:** t CO2e vermieden je Projekt, Los, Rückbauinventar oder Beschaffungsprogramm.
- **Prozentual:** Reduktion gegenüber Neubau-/Neuware-Referenz.

Die Bezugsgröße muss explizit genannt werden. Eine Angabe „60 % CO2-Einsparung“ ist ohne Systemgrenze, Baseline und Funktionsgleichheit nicht interpretierbar.

### Berechnungslogik

Eine belastbare ReUse-Bilanz besteht aus mindestens zwei Szenarien:

1. **Referenzszenario:** Beschaffung eines neuen Bauteils oder Neubauvariante gleicher Funktion.
2. **Wiederverwendungsszenario:** Demontage, Prüfung, Transport, Lagerung, Aufbereitung und Wiedereinbau eines vorhandenen Bauteils.

Vereinfacht:

```text
GWP_Referenz = GWP_Herstellung_neu + GWP_Transport_neu + GWP_Einbau_neu + GWP_Nutzung/Wartung_neu + GWP_End_of_Life_neu

GWP_ReUse = GWP_Demontage + GWP_Prüfung + GWP_Transport + GWP_Lagerung + GWP_Aufbereitung + GWP_Wiedereinbau + GWP_Nutzung/Wartung_ReUse + GWP_End_of_Life_ReUse

CO2-Einsparung = GWP_Referenz - GWP_ReUse
```

Wichtig ist, dass die **bereits historisch entstandenen Emissionen** eines bestehenden Bauteils nicht erneut als Herstellungsaufwand des neuen Projekts gebucht werden, wenn attributional bilanziert wird. Sie sind „sunk emissions“ des ersten Lebenszyklus. Zusätzlich anfallen können aber Rückbau, Transport, Reinigung, Zuschnitt, Verstärkung, neue Beschichtungen, Prüfungen und Montage.

### Lebenszyklusmodule

Nach EN 15978 und EN 15804 werden Gebäude- und Produktbilanzen in Module gegliedert:

- **A1-A3:** Rohstoffbereitstellung, Transport zur Herstellung, Herstellung.
- **A4-A5:** Transport zur Baustelle und Bau-/Einbauprozess.
- **B1-B7:** Nutzungsphase, Wartung, Reparatur, Austausch, Energie- und Wasserverbrauch.
- **C1-C4:** Rückbau, Transport, Abfallbehandlung, Entsorgung.
- **D:** Potenzielle Nutzen und Lasten außerhalb der Systemgrenze, z. B. durch Wiederverwendung, Recycling oder Energierückgewinnung.

Für ReUse ist Modul D methodisch besonders sensibel. Wird eine Gutschrift für vermiedene Neuherstellung vergeben, muss klar sein, ob diese Gutschrift dem abgebenden Gebäude, dem aufnehmenden Gebäude oder nur informativ außerhalb des Gebäudebilanzrahmens zugeordnet wird. Andernfalls droht Doppelzählung.

### Typische Datenquellen

- **EPD-Daten** nach EN 15804: produktspezifische Umweltproduktdeklarationen, besonders für Neuware-Referenzen.
- **ÖKOBAUDAT:** generische und spezifische Datensätze für Baustoffe, Bauteile, Transport, Energie und Entsorgung; geeignet für frühe Projektphasen und BNB/eLCA-Anwendungen.
- **eLCA / BNB:** Gebäudebilanzierung im deutschen Bewertungskontext.
- **Level(s):** EU-Rahmen für Lebenszyklus-GWP und Materialmengen.
- **Materialpässe / Gebäuderessourcenpässe:** Bauteilidentität, Menge, Zustand, Herkunft, Schadstoffe, Demontagehinweise, potenzielle künftige Nutzung.
- **Rückbau- und Bauteilgutachten:** reale Demontierbarkeit, Schadstoffbefund, Sortenreinheit, technische Restqualität.
- **Logistikdaten:** Entfernungen, Transportmittel, Lagerdauer, Hubtechnik, Verpackung.
- **Aufbereitungsdaten:** Reinigung, Reparatur, Zuschnitt, Oberflächenbehandlung, Ersatzteile, Nachweise.
- **Projektabrechnung und Mengenermittlung:** tatsächlich wiederverwendete Mengen, nicht nur geplante Mengen.

### Mindestangaben für eine belastbare Kennwertangabe

Jede Angabe zur CO2-Einsparung sollte mindestens dokumentieren:

- Funktionseinheit und Bezugsgröße.
- Referenzprodukt oder Referenzgebäude.
- Betrachtungszeitraum und Restnutzungsdauer.
- Lebenszyklusmodule, die einbezogen wurden.
- Datenquellen und Datenqualität.
- Umgang mit Modul D und Gutschriften.
- Annahmen zu Transport, Lagerung, Aufbereitung und Ausschuss.
- Technische Gleichwertigkeit oder Abweichungen.
- Ob es sich um geplante, prognostizierte oder nachgewiesene Einsparung handelt.

### Interpretationsprobleme

- **Referenzfall bestimmt das Ergebnis:** Gegenüber einem emissionsintensiven Neuprodukt wirkt ReUse deutlich besser; gegenüber einem sehr emissionsarmen Produkt kann die Einsparung kleiner sein.
- **Restnutzungsdauer:** Ein Bauteil mit kurzer Restlebensdauer kann rechnerisch schlechter abschneiden, wenn bald Ersatz nötig wird.
- **Datenlücken:** Bestandsbauteile haben oft keine EPD, kein Baujahr, keine Materialrezeptur oder keine Wartungshistorie.
- **Qualitätsrisiko:** Prüf- und Nachweisaufwand ist klimatisch meist klein, kann aber wirtschaftlich entscheidend sein.
- **Transportmythos:** Transport ist oft weniger relevant als vermiedene Herstellung, kann aber bei schweren, niedrig emittierenden oder weit transportierten Bauteilen relevant werden.
- **Biogener Kohlenstoff:** Holzbauteile erfordern getrennte Betrachtung von biogenem Kohlenstoff, Speicherwirkung, End-of-Life und Substitution.
- **Doppelzählung:** Die gleiche vermiedene Neuherstellung darf nicht gleichzeitig dem Rückbauprojekt, dem Neubauprojekt und einer Plattformbilanz gutgeschrieben werden.
- **Downcycling vs. ReUse:** Recyclinggutschriften dürfen nicht als Wiederverwendung ausgegeben werden.

### Anwendung im ReUse-Kontext

CO2-Einsparung eignet sich für:

- Variantenvergleich zwischen Erhalt, Umbau, Rückbau und Neubau.
- Priorisierung von Bauteilen im Rückbauinventar.
- Beschaffungskriterien für ReUse-Bauteile.
- Klimabudgetierung von Gebäuden.
- Kommunikation gegenüber Bauherrschaft, Behörden und Öffentlichkeit.
- Nachweis in Zertifizierungssystemen und Förderprogrammen.
- Portfolioentscheidungen, etwa welche Bestandsgebäude als urbane Materiallager besonders relevant sind.

Ein robustes ReUse Assessment sollte CO2-Einsparung immer mit Demontagegrad, Schadstoffrisiko, Materialwert, Verfügbarkeit, Zeitplan, Haftungsrisiken und funktionaler Eignung kombinieren.

## Praxisbezug / Beispiele

- **K.118 Kopfbau Halle 118, Winterthur:** Das Projekt von baubüro in situ nutzt u. a. wiederverwendete Stahltragwerke, Fenster, Außentreppen und Granitplatten. Projektangaben berichten rund 60 % weniger Treibhausgase und rund 500 t eingesparte Primärmaterialien gegenüber einer Neubau-/Neuware-Referenz. Die Fallstudie zeigt, dass große CO2-Hebel vor allem dort entstehen, wo emissionsintensive Primärproduktion ersetzt wird.
- **ReUse-Pilotprojekte Stadt Zürich:** Untersuchungen zu wiederverwendeten Bauteilen zeigen, dass die Bilanzierung stark von der gewählten Methode abhängt: Neuwertvergleich, Anrechnung nicht amortisierter Grauer Energie oder tatsächliche ReUse-Aufwendungen führen zu unterschiedlichen Ergebnissen.
- **Stahlbauteile:** Wiederverwendeter Baustahl kann hohe CO2-Einsparungen erzielen, weil Primär- und Sekundärstahlherstellung energie- und emissionsintensiv sind. Voraussetzung sind Nachweise zu Stahlgüte, Tragfähigkeit, Verbindungsmitteln, Korrosion und Geometrie.
- **Fenster:** Einsparungen aus vermiedener Herstellung müssen gegen energetische Qualität, Restlebensdauer, Dichtheit, Glasaufbau und mögliche Anpassungskosten abgewogen werden. ReUse ist besonders plausibel bei kurzer Zweitnutzung, Innenanwendung, unbeheizten Bereichen oder hochwertigen Sonderbauteilen.
- **Naturstein und Keramik:** Bauteile wie Natursteinplatten, Klinker oder Fliesen können hohe Aufbereitungsarbeit verursachen, aber sehr lange Nutzungsdauern erreichen. Klimatisch relevant sind Demontageverluste, Reinigung, Zuschnitt und die Substitution hochwertiger Neuware.

## Herausforderungen / offene Fragen

- **Keine einheitliche ReUse-Allokation:** Europäische Normen strukturieren Lebenszyklusmodule, aber die projektpraktische Zuordnung von ReUse-Gutschriften bleibt interpretationsoffen.
- **Unklare Baselines:** Der Vergleich gegen „Neubau“ oder „Neuware“ kann strategisch gewählt werden. Für Forschung und Planung braucht es transparente, konservative Referenzen.
- **Mangel an bauteilspezifischen ReUse-Datensätzen:** Datenbanken sind auf neue Baustoffe und Standardprozesse ausgerichtet. Demontage, Prüfung, Reparatur und Lagerung sind oft nur näherungsweise vorhanden.
- **Qualität und Haftung:** Technisch nicht gleichwertige ReUse-Bauteile dürfen nicht rein nach CO2 bewertet werden.
- **Zeitliche Dynamik:** Sinkt die CO2-Intensität der Neuherstellung in Zukunft, ändern sich Substitutionsgutschriften; historische Bauteile behalten aber ihre bereits entstandenen Emissionen.
- **Skalierung:** Einzelprojekt-Einsparungen lassen sich nicht linear auf den Markt übertragen, weil Angebot, Nachfrage, Normung, Lagerflächen und Planungsvorlauf begrenzend wirken.
- **Kommunikation:** „Eingesparte Tonnen CO2“ sind leicht verständlich, aber methodisch anfällig. Der Kennwert sollte als Bandbreite oder Szenarioergebnis statt als absolute Wahrheit kommuniziert werden.

## Quellen

- DIN EN 15978: Nachhaltigkeit von Bauwerken – Bewertung der umweltbezogenen Qualität von Gebäuden – Berechnungsmethode.
- DIN EN 15804+A2: Nachhaltigkeit von Bauwerken – Umweltproduktdeklarationen – Grundregeln für die Produktkategorie Bauprodukte.
- ISO 14040 und ISO 14044: Environmental management – Life cycle assessment – Principles, framework, requirements and guidelines.
- ISO 21930: Sustainability in buildings and civil engineering works – Core rules for environmental product declarations of construction products and services.
- European Commission / Joint Research Centre: Level(s) indicator 1.2, Life cycle Global Warming Potential (GWP), User manual. https://susproc.jrc.ec.europa.eu/product-bureau/sites/default/files/2020-10/20201013%20New%20Level%28s%29%20documentation_Indicator%201.2_Publication%20v1.0.pdf
- European Commission: Level(s), EU framework for sustainable buildings. https://green-forum.ec.europa.eu/green-business/levels_en
- ÖKOBAUDAT: Plattform und Datenbank für ökologische Gebäudebewertungen. https://www.oekobaudat.de/en.html
- BBSR / BMWSB: eLCA und BNB-konforme Gebäudebilanzierung. https://www.oekobaudat.de/en/home/assessment-system-for-sustainable-building-bnb.html
- DGNB: Building Resource Passport. https://www.dgnb.de/en/sustainable-building/circular-building/building-resource-passport
- European Commission: EU construction & demolition waste management protocol including guidelines for pre-demolition and pre-renovation audits of construction works, updated edition 2024. https://op.europa.eu/en/publication-detail/-/publication/d63d5a8f-64e8-11ef-a8ba-01aa75ed71a1/language-en
- baubüro in situ: K.118 – Kopfbau Halle 118, Winterthur. https://www.insitu.ch/projekte/196-k118-kopfbau-halle-118
- Stadt Zürich: Graue Energie und Treibhausgasemissionen von wiederverwendeten Bauteilen, Studie zu K.118. https://www.stadt-zuerich.ch/content/dam/web/de/aktuell/publikationen/2022/studien-netto-null/graue-energie-bauteile-studie.pdf
- Stricker, E. et al.: Case Study K.118 – The Reuse of Building Components in Winterthur, Switzerland, Journal of Physics: Conference Series 2600, 2023.
- RICS: Whole Life Carbon Assessment for the Built Environment, 2nd edition.
