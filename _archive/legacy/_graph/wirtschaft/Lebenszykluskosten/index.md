---
id: "Lebenszykluskosten"
entity: "wirtschaft"
node_kind: "knot"
migration_status: "migrated_phase1_stable_knots"
migration_action: "move_as_knot"
title: "Lebenszykluskosten"
legacy_type: "Wirtschaft"
legacy_paths:
  - "wirtschaft\Lebenszykluskosten.md"
target_primary: "wirtschaft/Lebenszykluskosten"
target_secondary: ""
risk_flags: ""
---
# Lebenszykluskosten

## Migration

- Target: wirtschaft/Lebenszykluskosten
- Legacy source count: 1
- Legacy types: Wirtschaft
- Migration actions: move_as_knot
- Secondary targets: 
- Risk flags: 

## Legacy Content: wirtschaft\Lebenszykluskosten.md

---
type: Wirtschaft
huerde: ["[[huerde/Haftung]]"]
prozessphase: ["[[prozessphase/Betrieb_und_Rueckbauplanung]]", "[[prozessphase/Entwurf]]"]
recht: ["[[recht/Vergaberecht]]"]
verwandt: ["[[wirtschaft/Finanzierung]]", "[[wirtschaft/Kostenvergleich]]", "[[wirtschaft/Preisbildung]]", "[[wirtschaft/Restwert]]"]
---

## Verknüpfungen

### Übergeordnete Themen
- Wirtschaftlichkeit über den gesamten Gebäudelebenszyklus
- Zirkuläres Planen, Betreiben, Umbauen und Rückbauen
- Verhältnis von Investitionskosten, Nutzungskosten, Instandhaltung, Ersatz und Restwert
- Integration von Wiederverwendung in langfristige Immobilien- und Portfoliostrategien

### Verwandte Dateien
- `wirtschaft/Kostenvergleich.md`
- `wirtschaft/Finanzierung.md`
- `wirtschaft/Restwert.md`
- `wirtschaft/Preisbildung.md`
- `kennwert/Lebensdauer.md`
- `kennwert/Wartungskosten.md`
- `kennwert/CO2_Kennwerte.md`
- `logistik/Zeitplanung.md`
- `akteur/Bauherr.md`
- `akteur/Investor.md`
- `akteur/Facility_Management.md`
- `akteur/Planer.md`
- `werkzeug/LCA_LCC.md`
- `werkzeug/Materialpass.md`
- `werkzeug/Gebaeuderessourcenpass.md`
- `huerde/Datenunsicherheit.md`
- `huerde/Normen.md`
- `huerde/Haftung.md`

### Relevante Akteure / Fallstudien / Materialien / Standards / Methoden
- Akteure: Bauherrschaft, Investoren, Bestandshalter, Facility Management, Kostenplaner, Nachhaltigkeitsberater, Planer, Betreiber, Versicherer, öffentliche Auftraggeber
- Standards / Rahmen: ISO 15686-5, DIN 276, DIN 18960, Level(s), BNB, DGNB, EN 15804, EN 15978, EU-Taxonomie, Materialpass, Gebäuderessourcenpass
- Methoden: Lebenszykluskostenrechnung, Kapitalwertmethode, Barwert, Diskontierung, Betrachtungszeitraum, Ersatzzyklus, Szenarioanalyse, Sensitivitätsanalyse, Restwertberechnung, Whole-Life-Costing, Whole-Life-Carbon in paralleler Bewertung
- Fallstudien / Konzepte: BAMB – Buildings as Material Banks, Madaster, CCBuild, zirkuläre Büroausbauten, reversible Konstruktionen, Materialpässe

## Kurzdefinition

Lebenszykluskosten (Life Cycle Costing, LCC) bezeichnen die Summe aller relevanten Kosten eines Gebäudes, Bauteils oder Systems über einen definierten Betrachtungszeitraum. Dazu gehören Anschaffung, Planung, Bau, Betrieb, Wartung, Inspektion, Instandsetzung, Ersatz, Umbau, Rückbau, Entsorgung sowie mögliche Restwerte oder Erlöse.

Für Wiederverwendung ist LCC besonders wichtig, weil wiederverwendete Bauteile nicht nur über ihren Anschaffungspreis bewertet werden dürfen. Ihre ökonomische Wirkung hängt von Nutzungsdauer, Wartung, Anpassbarkeit, Ersatzbedarf, Rückbaubarkeit und zukünftigem Restwert ab.

## Relevanz für Wiederverwendung im Bauwesen

Wiederverwendung verändert die Kostenstruktur eines Gebäudes:
- Investitionskosten können steigen oder sinken;
- technische Prüfung und Aufbereitung fallen früh an;
- Betriebs- und Wartungskosten können je nach Zustand höher oder niedriger sein;
- Ersatzzyklen können unsicherer sein;
- reversible Konstruktionen können spätere Umbaukosten senken;
- dokumentierte Bauteile können am Lebensende einen Restwert behalten;
- Materialpässe können zukünftige Rückgewinnungskosten reduzieren;
- CO₂- und Ressourcenkennwerte werden für Finanzierung, Regulierung und ESG-Berichte wichtiger.

LCC hilft, kurzfristige Mehrkosten gegen langfristige Vorteile abzuwägen. Besonders bei Bestandshaltern, öffentlichen Bauherren und Portfolioeigentümern ist LCC aussagekräftiger als ein reiner Investitionskostenvergleich.

## Fachinhalt

### 1. Abgrenzung zu Kostenvergleich

**Kostenvergleich** betrachtet konkrete Varianten in einer Projektphase: neu kaufen oder wiederverwenden, Händlerware oder Same-site reuse, selektiv rückbauen oder konventionell abbrechen.

**Lebenszykluskosten** betrachten die Kosten über die Nutzungszeit. Sie fragen:
- Wie lange bleibt ein Bauteil funktional?
- Welche Wartung ist erforderlich?
- Wann muss es ersetzt werden?
- Wie teuer sind Anpassung, Umbau und Rückbau?
- Hat es einen Restwert?
- Welche Kosten entstehen durch Dokumentation oder fehlende Dokumentation?
- Wie wirken Zinssatz, Inflation und Preissteigerungen?

Ein wiederverwendetes Bauteil kann im Kostenvergleich teurer sein, aber in der LCC günstiger, wenn es langlebig, reparierbar und erneut demontierbar ist. Umgekehrt kann ein günstiges gebrauchtes Bauteil über den Lebenszyklus teuer werden, wenn es früh ausfällt oder hohe Wartung verursacht.

### 2. Systemgrenzen

Eine belastbare LCC muss klar festlegen:
- Betrachtungsobjekt: Bauteil, Gebäudesystem, Gebäude, Portfolio;
- Betrachtungszeitraum: z. B. 20, 30, 50 oder 80 Jahre;
- Preisbasis: nominal oder real;
- Diskontierungszinssatz;
- enthaltene Kostenarten;
- enthaltene Restwerte;
- Umgang mit Steuern, Fördermitteln und Finanzierungskosten;
- Szenarien für Nutzung, Umbau und Rückbau;
- Qualitäts- und Leistungsannahmen wiederverwendeter Bauteile.

Unsicher / regional unterschiedlich: Öffentliche Bewertungsrahmen, Zinssätze, Preisindizes und anerkannte Kostenarten unterscheiden sich nach Land, Auftraggeber und Zertifizierungssystem.

### 3. Kostenarten

#### 3.1 Investitionskosten
- Planung;
- Ausschreibung;
- Bauteilerfassung;
- Erwerb;
- Rückbau und Aufbereitung;
- Transport;
- Lagerung;
- technische Prüfung;
- Montage;
- Anpassungsdetails;
- Dokumentation.

#### 3.2 Nutzungskosten
- Reinigung;
- Wartung;
- Inspektion;
- Energieverbrauch;
- Wasserverbrauch;
- Betriebsstoffe;
- Instandhaltung;
- Ersatzteile;
- Versicherungs- und Prüfkosten.

#### 3.3 Instandsetzungs- und Ersatzkosten
- Reparatur;
- Austausch einzelner Komponenten;
- Modernisierung;
- Funktionsanpassung;
- Normenanpassung;
- Ersatz bei Ausfall;
- Wiederbeschaffung aus ReUse-Märkten oder Neuprodukten.

#### 3.4 Umbaukosten
- Demontage bei Nutzungsänderung;
- Zwischenlagerung;
- Wiedermontage;
- Anpassung von Anschlüssen;
- Dokumentationsaktualisierung;
- Restmengenverwertung.

#### 3.5 End-of-Life-Kosten und Restwerte
- Rückbau;
- selektive Demontage;
- Prüfung für erneute Nutzung;
- Verkauf oder interne Wiederverwendung;
- Recycling;
- Entsorgung;
- Schadstoffsanierung;
- Restwert oder negativer Restwert.

### 4. ReUse-spezifische LCC-Faktoren

#### Technische Restlebensdauer
Die ökonomische Bewertung hängt davon ab, wie lange ein Bauteil noch nutzbar ist. Die Restlebensdauer ist unsicherer als bei Neuprodukten, kann aber bei langlebigen Materialien wie Naturstein, Stahl, Holz oder Ziegeln hoch sein, wenn Zustand und Belastung bekannt sind.

#### Wartungs- und Instandhaltungsbedarf
Gebrauchte Bauteile können höhere Wartungskosten haben, wenn sie verschlissen sind oder Ersatzteile fehlen. Sie können aber auch robust und reparaturfähig sein, besonders bei älteren, einfachen Konstruktionen.

#### Anpassbarkeit
Bauteile mit modularen Maßen, lösbaren Verbindungen und dokumentierten Anschlüssen senken spätere Umbaukosten. Design for Disassembly ist daher eine LCC-Strategie, nicht nur eine ökologische Maßnahme.

#### Dokumentation
Materialpässe, Produktdaten und Wartungshistorien senken zukünftige Such-, Prüf- und Rückbaukosten. Fehlende Dokumentation erhöht Risikoaufschläge und kann Wiederverwendung verhindern.

#### Restwert
Ein Bauteil mit realistischer Wiederverwendungsperspektive kann am Ende des Betrachtungszeitraums einen positiven Restwert haben. Dieser Restwert muss konservativ angesetzt und um Rückgewinnungs-, Prüf- und Vermarktungskosten reduziert werden.

#### Risiko und Unsicherheit
LCC für Wiederverwendung sollte mit Szenarien arbeiten:
- optimistisch: hohe Nutzungsdauer, niedrige Wartung, positiver Restwert;
- konservativ: mittlere Nutzungsdauer, zusätzliche Prüfung, niedriger Restwert;
- negativ: frühzeitiger Ersatz, keine Wiederverwendung, Entsorgungskosten.

### 5. Methodischer Ablauf

1. **Ziel und Entscheidung definieren**
   - Bauteil behalten, ersetzen, wiederverwenden oder neu kaufen?
   - Betrachtung für Bauherr, Nutzer, Investor oder Gesellschaft?

2. **Varianten festlegen**
   - Neuprodukt;
   - wiederverwendetes Bauteil;
   - Erhalt im Bestand;
   - aufbereitetes Produkt;
   - modularer Neubau mit späterem Restwert.

3. **Systemgrenzen festlegen**
   - Betrachtungszeitraum;
   - Kostenarten;
   - Diskontierung;
   - Restwertannahmen.

4. **Daten erheben**
   - Anschaffungskosten;
   - Prüf- und Aufbereitungskosten;
   - Wartung;
   - Ersatzzyklen;
   - Energie- und Betriebskosten;
   - Rückbaukosten;
   - Restwertdaten.

5. **Barwerte berechnen**
   - zukünftige Kosten werden auf den Bewertungszeitpunkt abgezinst;
   - regelmäßige Kosten und Einmalzahlungen getrennt erfassen.

6. **Szenarien und Sensitivitäten prüfen**
   - Nutzungsdauer;
   - Zinssatz;
   - Energiepreise;
   - Ersatzteilverfügbarkeit;
   - Restwert;
   - CO₂-Preis, falls monetarisiert.

7. **Ergebnis interpretieren**
   - nicht nur niedrigster Barwert zählt;
   - technische, ökologische, soziale und gestalterische Ziele dokumentieren.

### 6. LCC und CO₂

Lebenszykluskosten sind eine ökonomische Methode. Sie dürfen nicht mit Lebenszyklusanalyse (LCA) verwechselt werden. Für ReUse ist jedoch eine parallele Betrachtung sinnvoll:
- LCC bewertet Geldströme;
- LCA bewertet Umweltwirkungen;
- Whole-Life-Carbon bewertet Treibhausgasemissionen über Herstellung, Betrieb und End-of-Life;
- CO₂ kann über interne Schattenpreise in LCC integriert werden, wenn die Organisation dies festlegt.

Wichtig: Die Monetarisierung von CO₂ ist keine neutrale technische Wahrheit, sondern abhängig von Preisannahmen, Regulierung und internen Zielsystemen.

### 7. Lebenszykluskosten in Standards und Bewertungssystemen

#### ISO 15686-5
ISO 15686-5 ist ein zentraler internationaler Standard für Life-Cycle Costing bei Gebäuden und baulichen Anlagen. Er strukturiert die Kostenbetrachtung über Zeit, Szenarien und Barwertmethodik.

#### DIN 276 und DIN 18960
DIN 276 ordnet Baukosten; DIN 18960 ordnet Nutzungskosten im Hochbau. Zusammen können sie als Grundlage dienen, um Investitions- und Nutzungskosten getrennt, aber anschlussfähig zu erfassen.

#### Level(s)
Level(s) ist der europäische Rahmen für nachhaltige Gebäude. Es integriert Lebenszyklusdenken, Ressourcen, Kreislauffähigkeit und ökonomische Aspekte in eine gemeinsame Struktur.

#### BNB / DGNB
Nachhaltigkeitsbewertungssysteme im deutschsprachigen Raum berücksichtigen Lebenszykluskosten und ökologische Wirkung. Wiederverwendung kann dort über Ressourcenschonung, Rückbaubarkeit, Dokumentation und LCC-Performance relevant werden.

### 8. ReUse in der LCC-Bewertung nach Bauteilgruppen

| Bauteilgruppe | LCC-Chancen | LCC-Risiken |
|---|---|---|
| Tragende Stahlbauteile | hoher Restwert, lange Lebensdauer, Wiederverwendbarkeit | Nachweise, Brandschutz, Korrosion |
| Holzbauteile | Reparierbarkeit, CO₂-Speicher, geringe Bearbeitungskosten | Feuchte, biologische Schäden, Holzschutzmittel |
| Naturstein | sehr lange Lebensdauer, hoher Restwert | Gewicht, Ausbaukosten, Bruch |
| Ziegel | langlebig, lokale Kreisläufe | Reinigung, Bruch, unsichere Festigkeit |
| Fassaden | hoher Materialwert, Restwert bei modularen Systemen | Energieanforderungen, Dichtungen, Normenwandel |
| Innenausbau | häufige Umbauten, hohes Wiederverwendungspotenzial | Abnutzung, Brandschutz, Akustik, Modezyklen |
| Haustechnik | Refurbishment möglich | Effizienz, Ersatzteile, technische Obsoleszenz |

### 9. Restwert in LCC

Restwert sollte nicht mit Neupreis oder Materialschrottwert gleichgesetzt werden. Er ergibt sich aus:
- erwartbarem Marktpreis;
- verbleibender technischer Nutzbarkeit;
- Demontagekosten;
- Prüf- und Aufbereitungskosten;
- Transport und Lagerung;
- rechtlicher Wiederverwendbarkeit;
- Dokumentationsqualität;
- Nachfrage zum Bewertungszeitpunkt.

Konservativ sollte der Restwert als Bandbreite angesetzt werden. Bei unsicherer Marktlage ist ein Szenario mit Restwert Null erforderlich.

## Praxisbezug / Beispiele

### BAMB – Buildings as Material Banks
BAMB formuliert Gebäude als temporäre Materiallager. Für LCC bedeutet dies, dass Bauteile nicht nur als Kosten, sondern als potenzielle zukünftige Ressourcen betrachtet werden. Materialpässe und reversible Verbindungen sollen den späteren Wertverlust reduzieren.

### Madaster
Madaster operationalisiert die Idee des Materialkatasters: Materialien und Produkte im Gebäude werden dokumentiert, um Kreislaufpotenziale und teilweise auch finanzielle Materialwerte sichtbar zu machen. Für LCC ist relevant, dass Datenqualität den künftigen Rückgewinnungsaufwand beeinflusst.

### Büroausbau mit internen Materialpools
Bei Unternehmen mit häufigen Umbauten können Trennwände, Doppelböden, Türen und Leuchten mehrfach genutzt werden. Die Investition in modulare Systeme und Lager-/Inventarprozesse kann sich über mehrere Umbauzyklen rechnen.

### Öffentliche Gebäude
Öffentliche Bauherren haben oft lange Nutzungszeiträume. LCC kann hier ReUse-Maßnahmen rechtfertigen, die im Investitionsbudget teurer erscheinen, aber langfristig Wartung, Ersatz und Rückbaukosten senken.

## Herausforderungen / offene Fragen

- **Datenunsicherheit:** Restlebensdauer, Wartung und Restwert gebrauchter Bauteile sind schwer zu prognostizieren.
- **Marktentwicklung:** Zukünftige Nachfrage nach bestimmten Bauteilen ist unsicher.
- **Normenwandel:** Bauteile können technisch intakt sein, aber zukünftige Anforderungen nicht erfüllen.
- **Diskontierung:** Hohe Diskontierungszinssätze entwerten zukünftige Restwerte und ökologische Vorteile.
- **Getrennte Budgets:** Investitions- und Betriebskosten werden organisatorisch oft getrennt, obwohl LCC sie zusammen betrachten muss.
- **Nichtmonetäre Werte:** CO₂, Ressourcenschonung, kultureller Wert und Resilienz werden nicht immer in LCC abgebildet.
- **Bilanzielle Anerkennung:** Materialpässe zeigen Werte, aber diese werden in Immobilienbewertungen und Bilanzen noch nicht konsistent berücksichtigt.
- **Haftung und Gewährleistung:** Lebenszykluskosten hängen stark davon ab, wer langfristig Verantwortung übernimmt.
- **Unsicher / regional unterschiedlich:** Bewertungszeiträume, Zinssätze, Energiepreisannahmen und Förderbedingungen variieren stark.

## Quellen

- ISO 15686-5: *Buildings and constructed assets – Service life planning – Part 5: Life-cycle costing*. International Organization for Standardization.
- DIN 276: *Kosten im Bauwesen*. DIN.
- DIN 18960: *Nutzungskosten im Hochbau*. DIN.
- European Commission: *Level(s) – European framework for sustainable buildings*. https://environment.ec.europa.eu/topics/circular-economy/levels_en
- BNB – Bewertungssystem Nachhaltiges Bauen: Kriterien und Methodik zu Lebenszykluskosten. https://www.bnb-nachhaltigesbauen.de/
- DGNB: Kriterienkataloge und Systemgrundlagen. https://www.dgnb.de/
- BAMB – Buildings as Material Banks: *Materials Passports*. https://www.bamb2020.eu/topics/materials-passports/
- BAMB – Buildings as Material Banks: *Business Models*. https://www.bamb2020.eu/topics/business-models/
- European Commission / CORDIS: *Buildings as Material Banks: Integrating Materials Passports with Reversible Building Design*. https://cordis.europa.eu/project/id/642384
- FCRBE / Interreg NWE: *A guide for identifying the reuse potential of construction products*, 2020. https://vb.nweurope.eu/media/10132/en-fcrbe_wpt2_d12_a_guide_for_identifying_the_reuse_potential_of_construction_products.pdf
- EN 15804: *Sustainability of construction works – Environmental product declarations – Core rules for the product category of construction products*. CEN.
- EN 15978: *Sustainability of construction works – Assessment of environmental performance of buildings – Calculation method*. CEN.

