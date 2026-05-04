# Demontagegrad

## Verknüpfungen

- **Übergeordnete Themen:** Kennwerte; Design for Disassembly; selektiver Rückbau; zirkuläres Bauen; Entwerfen mit Bestand; Bauteilprüfung; Rückbauplanung; Urban Mining.
- **Verwandte Dateien:** `kennwert/Wiederverwendungsquote.md`; `kennwert/CO2_Einsparung.md`; `kennwert/Materialwert.md`; `kennwert/Graue_Energie.md`; `methode/ReUse_Assessment.md`; `dokument/LCA.md`; `datenmodell/`; `wirtschaft/`; `standard/`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** ISO 20887; Level(s) Indikator 2.4 „Design for deconstruction“; DIN SPEC 91484; DGNB Building Resource Passport; EU Construction & Demolition Waste Management Protocol; BNB; UMAR / NEST Empa; K.118 Winterthur; Rotor; Concular; Madaster; Urban Mining Index; Bauteilkatalog; Rückbauaudit; Materialpass; BIM; reversible Verbindung; zerstörungsarme Demontage.

## Kurzdefinition

**Demontagegrad** beschreibt, in welchem Maß ein Bauteil, ein Bauteilsystem oder ein Gebäude so getrennt, ausgebaut und rückgeführt werden kann, dass Bauteile oder Materialien mit möglichst geringer Beschädigung, Sortenvermischung und Wertminderung erhalten bleiben. Im ReUse-Kontext ist der Demontagegrad ein planungs- und bewertungsrelevanter Kennwert für das **Wiederverwendungspotenzial**.

Es gibt keine allgemein verbindliche, in allen europäischen Bewertungsrahmen standardisierte Formel für den Demontagegrad. Deshalb muss jede Anwendung die Bewertungslogik offenlegen. Übliche Formen sind:

- qualitative Klassen, z. B. „nicht demontierbar“, „nur zerstörend trennbar“, „sortenrein trennbar“, „bauteilschonend demontierbar“, „direkt wiederverwendbar“;
- quantitative Quoten, z. B. Anteil der demontierbaren Masse, Fläche, Stückzahl oder des Materialwerts;
- gewichtete Indizes, z. B. aus Verbindungstyp, Zugänglichkeit, Trennbarkeit, Dokumentation, Schadstofffreiheit und Wiederverwendungsfähigkeit.

## Relevanz für Wiederverwendung im Bauwesen

Wiederverwendung scheitert häufig nicht am theoretischen Materialbestand, sondern an der **praktischen Trennbarkeit**. Verklebte, vergossene, verschweißte, verdeckte, schadstoffbelastete oder unzugängliche Bauteile können zwar stofflich vorhanden sein, aber nicht wirtschaftlich, sicher oder beschädigungsarm ausgebaut werden. Der Demontagegrad übersetzt diese praktische Realität in einen Kennwert.

Für Entwurf und Bestandserfassung ist der Demontagegrad zentral, weil er:

- früh zeigt, welche Bauteile realistisches ReUse-Potenzial haben;
- Rückbauzeit, Kosten, Arbeitssicherheit und Logistik beeinflusst;
- CO2-Einsparungen erst realisierbar macht;
- Materialwert und Wiederverwendungsquote begrenzt;
- Hinweise für reversible Neubaukonstruktionen gibt;
- Daten für Materialpässe, Gebäuderessourcenpässe und Rückbaukonzepte liefert.

Ein hoher Demontagegrad ist nicht automatisch gleich Wiederverwendung. Er bedeutet zunächst, dass Bauteile technisch erreichbar und trennbar sind. Ob sie tatsächlich wiederverwendet werden, hängt zusätzlich von Zustand, Nachfrage, Normkonformität, Maßtoleranzen, Schadstofffreiheit, Haftung, Zeitplan und Wirtschaftlichkeit ab.

## Fachinhalt

### Bewertungsdimensionen

Ein belastbarer Demontagegrad sollte mehrere Dimensionen erfassen:

1. **Zugänglichkeit:** Sind Verbindungspunkte sichtbar, erreichbar und ohne große Vorarbeiten zugänglich?
2. **Verbindungsart:** Ist die Verbindung reversibel, mechanisch lösbar, lösungsmittelfrei, zerstörungsarm oder irreversibel?
3. **Trennschärfe:** Können Materialien sortenrein voneinander getrennt werden?
4. **Beschädigungsrisiko:** Bleibt das Bauteil beim Ausbau geometrisch, statisch und oberflächlich verwendbar?
5. **Dokumentation:** Sind Pläne, Produktdaten, Einbaujahr, Materialqualität, Schadstoffinformationen und Verbindungsmittel bekannt?
6. **Arbeitssicherheit:** Kann die Demontage ohne unvertretbare Risiken für Personal, Bestand oder Umgebung erfolgen?
7. **Werkzeug- und Zeitaufwand:** Ist Spezialgerät erforderlich? Ist der Aufwand verhältnismäßig zum Bauteilwert?
8. **Prüfbarkeit:** Kann das Bauteil nach der Demontage zuverlässig geprüft und freigegeben werden?
9. **Lager- und Transportfähigkeit:** Kann das Bauteil ohne Funktionsverlust bewegt, gestapelt, geschützt und gelagert werden?
10. **Wiederverwendungsnähe:** Ist das Bauteil direkt einsetzbar, reparaturfähig, nur stofflich verwertbar oder entsorgungspflichtig?

### Beispielhafte Demontageklassen

Eine praktikable, projektspezifische Klassifizierung kann wie folgt aufgebaut werden:

| Klasse | Beschreibung | Typische Konsequenz |
|---|---|---|
| D0 | Nicht oder nur mit Totalzerstörung demontierbar | Entsorgung oder stoffliches Recycling nach Zerkleinerung |
| D1 | Zerstörend trennbar, Material bleibt teilweise sortierbar | Recycling möglich, Bauteil-ReUse unwahrscheinlich |
| D2 | Selektiv rückbaubar, Bauteil wird aber beschädigt oder stark aufbereitet | ReUse nur nach Reparatur oder als Sekundärmaterial |
| D3 | Bauteilschonend demontierbar, begrenzte Aufbereitung nötig | ReUse technisch plausibel |
| D4 | Reversibel lösbar, dokumentiert, prüfbar und transportfähig | Direktes oder hochwertiges ReUse-Potenzial |

Die Klassen sind als Arbeitsmodell zu verstehen. Sie ersetzen keine Norm und müssen je Projekt angepasst werden.

### Quantitative Berechnung

Ein einfacher massenbezogener Demontagegrad lautet:

```text
Demontagegrad_Masse = Masse bauteilschonend demontierbarer Komponenten / betrachtete Gesamtmasse
```

Für ReUse ist eine reine Massenquote oft irreführend. Ein schweres, aber nur recycelbares Betonbauteil kann eine hohe Massenrelevanz haben, während leichte, wertvolle, direkt wiederverwendbare Fassaden- oder Innenausbauteile kaum sichtbar werden. Deshalb sind gewichtete Varianten sinnvoll:

```text
Demontagegrad_gewichtet = Summe(Menge_i × Gewichtung_i × Demontagefaktor_i) / Summe(Menge_i × Gewichtung_i)
```

Mögliche Gewichtungen:

- Masse,
- Fläche,
- Stückzahl,
- Wiederbeschaffungswert,
- Materialwert,
- CO2-Intensität,
- Schadstoffrisiko,
- Kritikalität / Seltenheit,
- Priorität der Bauherrschaft.

### Demontagefaktoren für Verbindungen

Verbindungen sind oft der stärkste Treiber des Demontagegrades:

- **Hoher Demontagefaktor:** Schrauben, Bolzen, Klemmen, Stecksysteme, trockene Fügungen, Nut-Feder-Verbindungen, reversible Konsolen, zugängliche Montageschienen.
- **Mittlerer Demontagefaktor:** genagelte oder geklammerte Systeme, teilweise verdeckte Verschraubungen, lösbare Dichtungen, punktuelle Mörtel- oder Klebeverbindungen, modularer Trockenbau.
- **Niedriger Demontagefaktor:** vollflächige Verklebung, Verbundsysteme, Ortbetonverguss, verschweißte Anschlüsse ohne Trennstrategie, nicht zugängliche Einlagen, Brandschutzummantelungen ohne zerstörungsarme Öffnung.

### Planungsrelevanter Kennwert

Im Neubau oder Umbau kann der Demontagegrad als Entwurfsziel verwendet werden. Dann wird nicht nur bewertet, was im Bestand vorhanden ist, sondern wie neue Eingriffe künftige Wiederverwendung ermöglichen. Wichtige Planungsprinzipien sind:

- Schichten mit unterschiedlicher Lebensdauer trennen.
- Mechanische und zugängliche Verbindungen bevorzugen.
- Verklebungen, Nassverbund und irreversible Mischmaterialien minimieren.
- Bauteile maßlich standardisieren.
- Bauteile kennzeichnen und digital dokumentieren.
- Demontagereihenfolge und Werkzeuge festlegen.
- Reparatur, Austausch und Nachrüstung einplanen.
- Brand-, Schall-, Wärme- und Feuchteschutz so lösen, dass sie Reversibilität nicht vollständig blockieren.

ISO 20887 adressiert Design für Demontage und Anpassungsfähigkeit als Prinzip für Gebäude und Ingenieurbauwerke. Level(s) Indikator 2.4 macht Design for Deconstruction auf EU-Ebene bewertbar. Der DGNB Building Resource Passport kann Demontage, Separierbarkeit und künftige Nutzungswege dokumentieren.

### Typische Datenquellen

- Bestandspläne, Werk- und Detailplanung.
- BIM-Modelle, Bauteillisten und Leistungsverzeichnisse.
- Rückbau- und Schadstoffgutachten.
- Pre-demolition Audits und Vor-Ort-Bauteilaufnahmen.
- Produktdatenblätter, Zulassungen, EPDs, Wartungsunterlagen.
- Materialpässe und Gebäuderessourcenpässe.
- Fotodokumentation der Verbindungen.
- Probefreilegungen, Muster-Demontagen, Bauteilprüfungen.
- Erfahrungswerte von Rückbauunternehmen und ReUse-Plattformen.
- Kosten- und Zeitdaten aus selektivem Rückbau.

### Grenzen des Kennwerts

Der Demontagegrad misst nicht automatisch:

- Marktverfügbarkeit oder Nachfrage,
- rechtliche Zulässigkeit des Wiedereinbaus,
- gestalterische Passfähigkeit,
- normgerechte technische Leistung,
- tatsächliche Wiederverwendungsquote,
- CO2-Einsparung,
- wirtschaftlichen Gewinn.

Er ist daher ein **Potenzial- und Machbarkeitskennwert**, kein Wirkungsnachweis.

## Praxisbezug / Beispiele

- **UMAR / NEST Empa:** Die Urban Mining & Recycling Unit wurde als Materialdepot und Reallabor konzipiert. Mechanische, trockene und trennbare Verbindungen sollen spätere Rückführung ermöglichen. Das Projekt zeigt Demontagegrad als Entwurfsprinzip, nicht nur als Rückbaukennwert.
- **K.118 Winterthur:** Wiederverwendete Stahlbauteile, Fenster, Treppen und Natursteinplatten wurden aus verschiedenen Herkunftsgebäuden gewonnen. Das Beispiel zeigt, dass wiederverwendbare Bauteile oft aus Systemen stammen, deren Verbindungen ausreichend lösbar oder mit vertretbarem Aufwand trennbar waren.
- **Rotor / Rotor DC:** Praktische Bauteilgewinnung basiert auf frühem Zugang zu Rückbaugebäuden, detaillierter Sichtung, selektiver Demontage und Kenntnis marktgängiger Bauteile. Der tatsächliche Demontagegrad entscheidet darüber, ob theoretisch wertvolle Bauteile im Kreislauf bleiben.
- **Trockenbau und Systemböden:** Gipskarton-Verbund, Kleber und Verspachtelungen reduzieren Bauteil-ReUse häufig; demontierbare Systemböden, abgehängte Decken oder modulare Trennwände können dagegen relativ hohe Demontagegrade erreichen, sofern Maße und Zustand passen.
- **Fassaden:** Vorhangfassaden, Kassetten, Natursteinplatten oder Metallbekleidungen sind oft besser rückbaubar als Wärmedämmverbundsysteme. Vollflächig verklebte Dämm- und Putzsysteme haben meist niedrige Demontagegrade für Bauteil-ReUse.

## Herausforderungen / offene Fragen

- **Fehlende Standardformel:** Demontagegrad ist als Begriff verbreitet, aber nicht als einheitlicher Kennwert genormt. Vergleichbarkeit entsteht nur durch dokumentierte Methode.
- **Verdeckte Realität:** Pläne zeigen nicht immer tatsächliche Ausführung, spätere Umbauten, Korrosion, Schadstoffe oder nicht dokumentierte Verklebungen.
- **Kosten vs. Zirkularität:** Hoher Demontagegrad kann mehr Planungs- und Montageaufwand bedeuten. Ob dieser Aufwand wirtschaftlich ist, hängt von Materialwert und Nachfrage ab.
- **Technische Zielkonflikte:** Brandschutz, Schallschutz, Luftdichtheit, Feuchteschutz, Erdbebensicherheit und Tragwerksanschlüsse können reversible Lösungen erschweren.
- **Schadstoffe:** Auch gut demontierbare Bauteile können bei Asbest, PCB, PAK, Schwermetallen, KMF oder Holzschutzmitteln aus dem ReUse ausscheiden.
- **Bewertung von Verbundbauteilen:** Verbund kann technische Leistung verbessern, reduziert aber häufig Sortenreinheit und Demontagefähigkeit.
- **Zeitfenster:** Selbst demontierbare Bauteile gehen verloren, wenn Rückbauplanung, Nachfrage und Zwischenlagerung zeitlich nicht koordiniert sind.
- **Datenmodell:** Für digitale Bewertung fehlen oft strukturierte Felder zu Verbindung, Zugänglichkeit, Demontagereihenfolge, Werkzeugbedarf und Zustandsklasse.

## Quellen

- ISO 20887: Sustainability in buildings and civil engineering works – Design for disassembly and adaptability – Principles, requirements and guidance.
- European Commission / Joint Research Centre: Level(s) indicator 2.4, Design for deconstruction, User manual. https://susproc.jrc.ec.europa.eu/product-bureau/sites/default/files/2021-11/UM3_Indicator_2.4_v.2.0_clean_20.07.2021.pdf
- DIN SPEC 91484: Verfahren zur Erfassung von Bauprodukten als Grundlage für Bewertungen vor Abbruch- und Renovierungsarbeiten.
- European Commission: EU construction & demolition waste management protocol including guidelines for pre-demolition and pre-renovation audits of construction works, updated edition 2024. https://op.europa.eu/en/publication-detail/-/publication/d63d5a8f-64e8-11ef-a8ba-01aa75ed71a1/language-en
- DGNB: Building Resource Passport. https://www.dgnb.de/en/sustainable-building/circular-building/building-resource-passport
- Madaster: Material passport. https://madaster.com/material-passport/
- Werner Sobek: NEST Unit UMAR. https://www.wernersobek.com/projects/nest-unit-umar/
- Empa NEST: Urban Mining & Recycling. https://nest.empa.ch/urban-mining
- baubüro in situ: K.118 – Kopfbau Halle 118. https://www.insitu.ch/projekte/196-k118-kopfbau-halle-118
- Honic, M. et al.: Material Passports for the end-of-life stage of buildings, Journal of Cleaner Production, 2021.
- Heisel, F.; Rau-Oberhuber, S.: Calculation and evaluation of circularity indicators for the built environment using the case studies of UMAR and Madaster, Journal of Cleaner Production, 2020.
