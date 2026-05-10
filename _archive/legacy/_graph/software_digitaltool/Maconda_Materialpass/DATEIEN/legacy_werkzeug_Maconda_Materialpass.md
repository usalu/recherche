---
type: Werkzeug
dokument: ["[[dokument/Materialinventar]]"]
verwandt: ["[[werkzeug/DGNB_Gebaeuderessourcenpass]]", "[[werkzeug/Maconda_ROMULUS]]", "[[werkzeug/Madaster_Plattform]]", "[[werkzeug/Pre_Demolition_Audit_Tools]]", "[[werkzeug/QR_RFID_Materialtracking]]", "[[werkzeug/Upcyclea]]"]
---

## Verknüpfungen

- **Übergeordnete Themen:** digitale Materialpässe, digitale Produktpässe, Gebäuderessourcenpässe, Circular Economy, Urban Mining, Rückbauinventar, Wiederverwendungsnachweis.
- **Verwandte Dateien:** `werkzeug/Maconda_ROMULUS.md`, `werkzeug/Upcyclea.md`, `werkzeug/Madaster_Plattform.md`, `werkzeug/DGNB_Gebaeuderessourcenpass.md`, `werkzeug/Pre_Demolition_Audit_Tools.md`, `datenmodell/Materialpass.md`, `dokument/Materialinventar.md`, `methode/Bauteilkartierung.md`, `methode/Selektiver_Rueckbau.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Maconda Solutions, ROMULUS Initiative, Mace / Waterman / BRE / City of London Material-Passport-Pilot, Upcyclea, BAMB Materials Passports, DGNB Gebäuderessourcenpass, Londoner Circular-Economy-Planungsanforderungen, Pre-Demolition Audit, Reclamation Audit.

## Kurzdefinition

**Maconda Material Passports** sind digitale Material- bzw. Produktpässe für Bauprojekte und Bestände. Maconda beschreibt den Materialpass als digitale Identitätskarte für Bauprodukte und Materialien, die Informationen erfasst, die deren künftige Wiederverwendung oder Rückgewinnung vorbereiten. Dazu gehören u. a. CO₂-Fußabdruck, Zirkularität, Materialgesundheit, Dokumentation und finanzieller Wert.

Die Datei ist von `werkzeug/Maconda_ROMULUS.md` zu unterscheiden: `Maconda_ROMULUS.md` behandelt die kollaborative Reuse-Initiative und Community-Logik; diese Datei behandelt den **Materialpass als Datenobjekt, Werkzeug und Nachweisstruktur**.

## Relevanz für Wiederverwendung im Bauwesen

Für Wiederverwendung reicht es nicht aus, Bauteile physisch zu erhalten. Sie müssen auch **identifizierbar, bewertbar, beschreibbar, rechtlich nachvollziehbar und in späteren Projekten auffindbar** bleiben. Materialpässe sind deshalb eine Schlüsseltechnologie für Reuse, weil sie Materialwissen von der Planung über Bau, Betrieb, Umbau, Rückbau, Lagerung und Wiedereinbau transportieren.

Maconda ist besonders relevant, weil der Ansatz nicht nur auf ökologische Kennzahlen zielt, sondern auf eine Verbindung von:

- Material- und Produktidentität,
- CO₂- und Zirkularitätsdaten,
- Materialgesundheit und Dokumentation,
- wirtschaftlichem Restwert,
- projekt- und portfolioübergreifender Berichterstattung,
- Anschlussfähigkeit an Audits und Reuse-Netzwerke.

Damit liegt der Schwerpunkt nicht nur auf „Dokumentation“, sondern auf **Wiederverwendungsfähigkeit als Datenzustand**.

## Fachinhalt

### Funktion im Reuse-Prozess

Maconda-Materialpässe können in mehreren Phasen eingesetzt werden:

1. **Planung / Neubau:** Produkte und Materialien werden mit technischen, ökologischen und wirtschaftlichen Daten angelegt. Ziel ist, künftigen Rückbau und Wiederverwendung bereits mitzudenken.
2. **Bestandsaufnahme:** Vorhandene Bauteile werden inventarisiert; verfügbare Dokumente, Fotos, Mengen, Zustände und Schadstoffhinweise werden ergänzt.
3. **Audit / Rückbau:** Passdaten unterstützen Entscheidungen, welche Produkte direkt wiederverwendet, geprüft, aufbereitet, gelagert, verkauft oder recycelt werden können.
4. **Portfolioebene:** Materialpässe werden über mehrere Projekte vergleichbar, etwa für CO₂-Reporting, ESG, Taxonomie- oder Circular-Economy-Ziele.
5. **Reuse-Community / Matching:** In Verbindung mit ROMULUS können gemeinsame Auditdaten und Materialpässe genutzt werden, um Transparenz über verfügbare Ressourcen zu schaffen.

### Typische Datenfelder

Belastbare Materialpässe sollten mindestens folgende Felder enthalten:

- eindeutige Bauteil- oder Produkt-ID,
- Produktname, Hersteller, Typ, Seriennummer, Baujahr,
- Geometrie, Maße, Masse, Anzahl, Lage im Gebäude,
- Materialzusammensetzung und Schichtenaufbau,
- technische Leistung: Tragfähigkeit, Brandschutz, Akustik, U-Wert, Oberflächenqualität, Verschleiß,
- Dokumentation: Datenblätter, EPDs, Prüfzeugnisse, Zulassungen, Wartungshistorie,
- Schadstoff- und Materialgesundheitsinformationen,
- CO₂- und Umweltkennwerte,
- Zirkularitätsinformationen: recycled content, Demontierbarkeit, Wiederverwendbarkeit, Recyclingfähigkeit,
- Rückbauhinweise: Verbindungsmittel, Demontagereihenfolge, Werkzeuge, Schutzmaßnahmen,
- finanzieller Wert bzw. Wiederverwendungs-/Restwert,
- Verfügbarkeit: Zeitpunkt, Eigentümer, Lagerort, reserviert/frei.

### Schnittstellen

Die wichtigsten Schnittstellen sind:

- **BIM / IFC:** Mengen, Bauteilklassen, Objekt-IDs und Lageinformationen können aus Modellen übernommen werden, sofern sie sauber modelliert sind.
- **Pre-Demolition Audit:** Auditdaten können Materialpässe initial befüllen oder aktualisieren.
- **Materialdatenbanken / EPD-Datenbanken:** Umwelt- und Produktdaten ergänzen die bauteilbezogene Erfassung.
- **Reuse-Marktplätze / Netzwerke:** Passdaten liefern die Mindestinformationen, um Bauteile verlässlich anzubieten.
- **Portfolio-Reporting:** Daten werden für ESG, Taxonomie, CO₂-Bilanzierung und zirkuläres Controlling aggregiert.

### Abgrenzung

Ein Materialpass ist **kein Marktplatz** und ersetzt weder Prüfung, Gewährleistung noch Logistik. Er ist ein strukturierter Datensatz. Sein Nutzen entsteht erst, wenn Daten aktuell, prüfbar, maschinenlesbar und mit Entscheidungsprozessen verbunden sind.

## Praxisbezug / Beispiele

- **ROMULUS Initiative:** Maconda beschreibt ROMULUS als Ressource für die gebaute Umwelt mit exklusivem Reuse-Netzwerk, geteilten Auditdaten und Materialpässen. Der Ansatz zeigt, dass Materialpässe nicht nur projektintern, sondern als kollaborative Infrastruktur für Angebot und Nachfrage genutzt werden können.
- **One Nine Elms / Upcyclea-Maconda-Bezug:** Berichte zu Materialpässen bei großen Londoner Projekten zeigen, dass Materialpässe zunehmend als Schnittstelle zwischen Nachhaltigkeitsbericht, Rückbaupotenzial und Beschaffungsstrategie eingesetzt werden.
- **Mace Material-Passport-Pilot:** Die britische Praxisdiskussion ordnet Materialpässe als Weg ein, um Theorie und reale Projektabwicklung im zirkulären Bauen zu verbinden.
- **Bestandsprojekte:** Besonders geeignet sind Innenausbau, Fassaden, technische Anlagen, Systemtrennwände, Türen, Bodenbeläge, Leuchten, Decken, Doppelböden und Stahl-/Holzelemente, weil hier Produktidentität und Ausbaupotenzial vergleichsweise gut dokumentierbar sind.

## Herausforderungen / offene Fragen

- **Datenqualität:** Materialpässe sind nur so belastbar wie ihre Eingabedaten. Fehlende Herstellerdaten, unklare Umbauhistorien und unvollständige BIM-Modelle reduzieren den Nutzen.
- **Pflege über Jahrzehnte:** Ein Pass muss bei Umbauten, Reparaturen, Austausch und Schadensfällen aktualisiert werden. Ohne Betreiberprozess wird er schnell historisch.
- **Standardisierung:** Noch bestehen Unterschiede zwischen BAMB, DGNB, Madaster, Maconda, Upcyclea und projektspezifischen Anforderungen.
- **Recht und Haftung:** Dokumentierte Wiederverwendungsfähigkeit ersetzt nicht den Nachweis der tatsächlichen Gebrauchstauglichkeit im neuen Kontext.
- **Datentiefe vs. Aufwand:** Für viele Bauteile lohnt keine sehr tiefe Erfassung. Entscheidend ist eine abgestufte Methodik nach Wert, Risiko und Wiederverwendungschance.
- **Interoperabilität:** Passdaten sollten exportierbar sein; reine Plattformbindung kann spätere Nutzung erschweren.

## Quellen

- Maconda Solutions: **Material Passports**. https://www.macondasolutions.com/materialpassports. Zugriff: 2026-04-27.
- Maconda Solutions: **ROMULUS**. https://www.macondasolutions.com/romulus. Zugriff: 2026-04-27.
- Maconda Solutions: **Circular Construction / company overview**. https://www.macondasolutions.com/. Zugriff: 2026-04-27.
- Multiplex: **Multiplex joins ROMULUS initiative aimed at spearheading a circular built environment**, 29.11.2024. https://www.multiplex.global/news/multiplex-joins-romulus-initiative-aimed-at-spearheading-a-circular-built-environment/. Zugriff: 2026-04-27.
- Mace: **Material Passports**, 12.02.2025. https://www.macegroup.com/case-studies/material-passports/. Zugriff: 2026-04-27.
- Lancaster University: **Material Passports – policy paper**, 2024. https://www.lancaster.ac.uk/media/lancaster-university/content-assets/images/lica/MaterialPassportsPolicyPaper%281%29.pdf. Zugriff: 2026-04-27.
