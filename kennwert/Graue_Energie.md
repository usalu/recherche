---
type: Kennwert
---

# Graue Energie

## Verknüpfungen

- **Übergeordnete Themen:** Kennwerte; Ökobilanzierung; Ressourcenschonung; Bestandserhalt; Entwerfen mit Bestand; zirkuläres Bauen; Lebenszyklusplanung.
- **Verwandte Dateien:** `kennwert/CO2_Einsparung.md`; `kennwert/Wiederverwendungsquote.md`; `kennwert/Demontagegrad.md`; `kennwert/Materialwert.md`; `dokument/LCA.md`; `methode/ReUse_Assessment.md`; `datenmodell/`; `wirtschaft/`; `standard/`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** DIN EN 15978; DIN EN 15804+A2; ISO 14040/14044; ISO 21930; SIA 2032; KBOB Ökobilanzdaten; ÖKOBAUDAT; eLCA; BNB; DGNB; Level(s); K.118 Winterthur; Stadt Zürich Studien zu Grauer Energie und Treibhausgasen; Umbau-vor-Neubau-Analysen; Materialpass; Gebäuderessourcenpass; Primärenergieindikatoren PENRT/PERT; kumulierter Energieaufwand.

## Kurzdefinition

**Graue Energie** bezeichnet die Energie, die für Gewinnung, Herstellung, Transport, Einbau, Instandhaltung, Rückbau und Entsorgung von Baustoffen, Bauteilen oder Gebäuden aufgewendet wird, bevor oder außerhalb des eigentlichen Gebäudebetriebs. Sie wird meist als **Primärenergie** in MJ, kWh oder kWh/m² angegeben.

Im engeren Sinn wird Graue Energie häufig auf die **Herstellungsphase** von Baustoffen und Bauteilen bezogen. In vollständigen Lebenszyklusbetrachtungen können zusätzlich Transport, Baustelle, Ersatz, Instandsetzung und End-of-Life einbezogen werden. Deshalb muss der Bilanzrahmen immer genannt werden.

Wichtig: Graue Energie ist nicht identisch mit CO2-Emissionen. Sie beschreibt Energieaufwand, nicht direkt Klimawirkung.

## Relevanz für Wiederverwendung im Bauwesen

Bestandsgebäude und vorhandene Bauteile speichern bereits aufgewendete Energie. Bei Abriss oder Austausch wird diese investierte Energie nicht physisch zurückgewonnen; sie bleibt historisch verbraucht. Wiederverwendung kann aber verhindern, dass für eine gleiche Funktion erneut Primärenergie für Neuherstellung aufgewendet wird. Deshalb ist Graue Energie ein Schlüsselbegriff für die Argumentation „Bestand ist Ressource“.

Im ReUse-Kontext hilft der Kennwert:

- Eingriffe in den Bestand energetisch zu gewichten;
- Bauteile mit hohem Herstellungsenergieaufwand zu priorisieren;
- Umbau- und Neubauvarianten zu vergleichen;
- Rückbauentscheidungen nicht nur nach Betriebsenergie zu treffen;
- ReUse mit LCA, CO2-Bilanz und Materialwert zu koppeln;
- den Zielkonflikt zwischen energetischer Sanierung und Substanzerhalt sichtbar zu machen.

Gerade bei Gebäuden mit sinkender Betriebsenergie gewinnt die Graue Energie der Erstellung, Sanierung und Bauteilersatzzyklen an Bedeutung. Bei sehr effizienten Neubauten kann ein erheblicher Anteil der Lebenszykluswirkungen bereits vor der Nutzung entstehen.

## Fachinhalt

### Abgrenzung zu CO2-Einsparung

- **Graue Energie:** kumulierter Primärenergieaufwand, meist MJ oder kWh.
- **CO2-Einsparung:** vermiedene Treibhausgaswirkung, kg CO2e.
- Ein energieintensiver Prozess kann niedrige CO2-Emissionen haben, wenn erneuerbare Energie genutzt wird.
- Ein Prozess mit moderatem Energieeinsatz kann hohe CO2-Emissionen haben, wenn prozessbedingte Emissionen entstehen, z. B. bei mineralischen Bindemitteln.
- Graue Energie zeigt Ressourcen- und Energiebedarf, CO2 zeigt Klimawirkung. Beide sollten im ReUse Assessment getrennt ausgewiesen werden.

### Indikatoren und Begriffe

In Normen und Datenbanken wird der Begriff „Graue Energie“ nicht immer identisch verwendet. Häufige technische Indikatoren sind:

- **PENRT:** nicht erneuerbare Primärenergie, total.
- **PERT:** erneuerbare Primärenergie, total.
- **PE gesamt:** Summe erneuerbarer und nicht erneuerbarer Primärenergie.
- **KEA:** kumulierter Energieaufwand.
- **Embodied Energy:** englischer Sammelbegriff für eingebaute / verkörperte Energie.

Für wissenschaftliche und planerische Vergleiche sollte angegeben werden, ob nur nicht erneuerbare Primärenergie oder die gesamte Primärenergie betrachtet wird. In vielen Nachhaltigkeitsbewertungen ist insbesondere nicht erneuerbare Primärenergie relevant, während Klimabilanzen GWP separat ausweisen.

### Berechnungslogik

Bauteilbezogen:

```text
Graue Energie_Bauteil = Menge × Primärenergiekennwert + Transporte + Einbau + Aufbereitung + anteilige Ersatz-/End-of-Life-Prozesse
```

Gebäudebezogen:

```text
Graue Energie_Gebäude = Summe(Graue Energie aller Bauteile und Prozesse innerhalb der Systemgrenze)
```

ReUse-Vergleich:

```text
Vermiedene Graue Energie = Graue Energie_Neuherstellung_Referenz - Graue Energie_ReUse-Prozesse
```

Im Wiederverwendungsszenario wird die historische Herstellungsenergie des bestehenden Bauteils in der Regel nicht noch einmal als Aufwand des neuen Projekts gebucht. Erfasst werden die zusätzlich nötigen Prozesse: Ausbau, Transport, Lagerung, Reinigung, Prüfung, Reparatur, Anpassung, Montage und späteres End-of-Life.

### Lebenszyklusmodule

Eine saubere Gliederung folgt analog EN 15978 / EN 15804:

- **A1-A3:** Herstellungsenergie der Baustoffe und Bauteile.
- **A4-A5:** Transport zur Baustelle und Einbau.
- **B2-B5:** Wartung, Reparatur, Ersatz, Umbau.
- **C1-C4:** Rückbau, Transport, Abfallbehandlung, Entsorgung.
- **D:** potenzielle Gutschriften aus Wiederverwendung, Recycling oder Energierückgewinnung außerhalb der Systemgrenze.

Bei Bestands- und ReUse-Projekten sind besonders A1-A3 und B4/B5 relevant, weil vermiedene Neuherstellung und vermiedener Ersatz die größten Effekte haben können.

### Typische Datenquellen

- **ÖKOBAUDAT:** Primärenergie- und Umweltindikatoren für Baustoffe, Bauteile, Transporte, Energie und Entsorgung.
- **EPDs nach EN 15804:** produktbezogene Primärenergie- und Umweltindikatoren.
- **eLCA / BNB:** Gebäudebilanzierung mit deutschen Datensätzen.
- **KBOB Ökobilanzdaten im Baubereich:** in der Schweiz häufig genutzte Grundlage für Primärenergie und Treibhausgasemissionen.
- **SIA 2032:** Schweizer Merkblatt zur Grauen Energie von Gebäuden.
- **Level(s):** EU-Rahmen für Lebenszyklusdenken und Materialmengen; GWP wird explizit, Energiekennwerte werden in vollständigen LCA-Kontexten ergänzend genutzt.
- **Materialpässe / Gebäuderessourcenpässe:** Mengen, Materialien, Bauteilschichten und Wiederverwendungspotenzial.
- **Kosten- und Mengenermittlung:** Bauteilflächen, Massen, Stückzahlen, Kostengruppen.
- **Rückbauinventare:** real verfügbare Bauteile, Zustand, Demontierbarkeit, Schadstoffe.

### Typische Bewertungsfragen

1. Wie viel Graue Energie ist im Bestand bereits gebunden?
2. Welche Eingriffe verursachen neue Graue Energie?
3. Welche Bauteile sollten wegen hoher Herstellungsenergie möglichst erhalten oder wiederverwendet werden?
4. Wie viel Betriebsenergie wird durch Austausch eingespart, und nach welcher Zeit amortisiert sich die zusätzliche Graue Energie?
5. Wird ein ReUse-Bauteil mit kurzer Restlebensdauer bald erneut ersetzt?
6. Werden Aufbereitungsprozesse so intensiv, dass der Vorteil gegenüber Neuware schrumpft?

### Anwendung im ReUse Assessment

Für `methode/ReUse_Assessment.md` sollte Graue Energie mindestens auf drei Arten genutzt werden:

- **Priorisierung:** Bauteile mit hohem Primärenergieaufwand und guter Demontierbarkeit zuerst untersuchen.
- **Variantenvergleich:** Erhalt, Reparatur, ReUse, Recycling und Neuware getrennt bilanzieren.
- **Hotspotanalyse:** Nicht nur Gesamtmengen betrachten, sondern Bauteilschichten, Ersatzzyklen und technische Systeme identifizieren.

Bei Bestandsgebäuden ist besonders relevant, ob ein Bauteil **weitergenutzt im Bestand**, **vor Ort wiederverwendet**, **extern wiederverwendet** oder **stofflich recycelt** wird. Jede Option hat eine andere Bilanzlogik.

## Praxisbezug / Beispiele

- **Erhalt der Tragstruktur:** Tragwerke enthalten große Massen und hohe Herstellungsaufwendungen. Selbst wenn ihre CO2-Intensität je kg niedriger ist als bei Aluminium oder Edelstahl, kann der absolute Effekt wegen der Masse sehr groß sein.
- **K.118 Winterthur:** Die Fallstudien zur Wiederverwendung von Bauteilen zeigen, dass die Bilanzierung der Grauen Energie stark vom methodischen Ansatz abhängt. Diskutiert werden u. a. tatsächliche Aufwendungen für Demontage, Transport und Montage, Neuwertvergleich und Amortisationslogiken.
- **Fassaden und Fenster:** Ersetzen alter Fenster kann Betriebsenergie reduzieren, verursacht aber neue Graue Energie. Die Bewertung muss Restlebensdauer, energetischen Standard, Reparaturfähigkeit und Nutzungskontext berücksichtigen.
- **Innenausbau:** Bodenbeläge, Decken, Trennwände und Möbel haben kürzere Austauschzyklen. Obwohl sie leichter sind als Rohbau, kann ihre häufige Erneuerung über den Lebenszyklus hohe kumulierte Graue Energie erzeugen.
- **Technische Anlagen:** Gebäudetechnik hat oft hohe Materialkomplexität und kurze Zyklen. ReUse ist technisch und haftungsseitig schwieriger, aber Reparatur und längere Nutzung können graue Energie reduzieren.

## Herausforderungen / offene Fragen

- **Begriffsunschärfe:** „Graue Energie“, „embodied energy“, „Primärenergie“ und „KEA“ werden in Praxis und Literatur nicht immer gleich verwendet.
- **Systemgrenzen:** Ergebnisse ändern sich stark, wenn nur A1-A3 oder der gesamte Lebenszyklus betrachtet wird.
- **Erneuerbare vs. nicht erneuerbare Primärenergie:** Die Summe kann andere Schlussfolgerungen erzeugen als nur nicht erneuerbare Energie.
- **Alte Bauteile ohne Daten:** Für historische Bauteile fehlen oft Herstellungsdaten. Referenzwerte müssen transparent gewählt werden.
- **Ersatzzyklen:** Kurzlebige Komponenten können über den Lebenszyklus wichtiger sein als ihre Anfangsmasse vermuten lässt.
- **Energetische Sanierung:** Mehr Dämmung oder neue Fenster reduzieren Betriebsenergie, erhöhen aber Graue Energie. Der ökologische Break-even hängt von Nutzung, Klima, Energieversorgung und Bauteillebensdauer ab.
- **Doppelte Anrechnung:** Die historische Graue Energie eines Bauteils sollte nicht gleichzeitig als Belastung im neuen Projekt und als Einsparung gegenüber Neuware gebucht werden.
- **Kommunikation:** Graue Energie ist für Laien weniger intuitiv als CO2e. Für Entscheidungen sollte sie mit CO2, Kosten und Demontagegrad zusammengeführt werden.

## Quellen

- DIN EN 15978: Nachhaltigkeit von Bauwerken – Bewertung der umweltbezogenen Qualität von Gebäuden – Berechnungsmethode.
- DIN EN 15804+A2: Nachhaltigkeit von Bauwerken – Umweltproduktdeklarationen – Grundregeln für die Produktkategorie Bauprodukte.
- ISO 14040 und ISO 14044: Life cycle assessment – Principles, framework, requirements and guidelines.
- ISO 21930: Core rules for environmental product declarations of construction products and services.
- SIA 2032: Graue Energie von Gebäuden.
- KBOB / ecobau / IPB: Ökobilanzdaten im Baubereich.
- ÖKOBAUDAT: Plattform für ökologische Gebäudebewertungen. https://www.oekobaudat.de/en.html
- BBSR / BMWSB: eLCA für Gebäudebilanzierung. https://www.oekobaudat.de/en/home/assessment-system-for-sustainable-building-bnb.html
- European Commission / Joint Research Centre: Level(s) documentation. https://green-forum.ec.europa.eu/green-business/levels_en
- European Commission / Joint Research Centre: Level(s) indicator 1.2, Life cycle Global Warming Potential. https://susproc.jrc.ec.europa.eu/product-bureau/sites/default/files/2020-10/20201013%20New%20Level%28s%29%20documentation_Indicator%201.2_Publication%20v1.0.pdf
- DGNB: Building Resource Passport. https://www.dgnb.de/en/sustainable-building/circular-building/building-resource-passport
- Stadt Zürich: Graue Energie und Treibhausgasemissionen von wiederverwendeten Bauteilen, Studie zu K.118. https://www.stadt-zuerich.ch/content/dam/web/de/aktuell/publikationen/2022/studien-netto-null/graue-energie-bauteile-studie.pdf
- baubüro in situ: K.118 – Kopfbau Halle 118, Winterthur. https://www.insitu.ch/projekte/196-k118-kopfbau-halle-118
- RICS: Whole Life Carbon Assessment for the Built Environment, 2nd edition.
