---
entity: "quelle"
id: "dokument_Rueckbaukataster_md"
title: "dokument_Rueckbaukataster_md"
build_status: "promoted_phase42"
source_filename: "Rueckbaukataster.md"
legacy_type: "Dokument"
---

# dokument_Rueckbaukataster_md

## Verknüpfungen

- **Übergeordnete Themen:** selektiver Rückbau, Urban Mining, Wiederverwendung, Rückbauplanung, Stoffstrommanagement, Kreislaufwirtschaft, Rückbau- und Entsorgungskonzept, Logistik, Bauteilvermittlung.
- **Verwandte Dateien:** `dokument/Pre_Demolition_Audit.md`, `dokument/Materialinventar.md`, `dokument/Materialpass.md`, `dokument/Bauwerksdiagnose.md`, `dokument/Bestandsaufnahme.md`, `dokument/Auditbericht.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Rückbauplanung, Abbruchunternehmen, Bauherrschaft, Entsorgungsfachbetriebe, Reuse-Händler, Bauteilbörsen, Logistikunternehmen, Schadstoffgutachter:innen, Behörden, Arbeitsschutz, BIM-Management; DIN SPEC 91484, EU Construction & Demolition Waste Management Protocol, FCRBE, KrWG, GewAbfV, AVV, VDI/GVSS 6202, DGNB Gebäuderessourcenpass, Materialkataster/Urban-Mining-Plattformen; `methode/` für selektiven Rückbau, Bauteil-Losbildung, Demontageplanung, Stoffstrombilanz; `prozessphase/` für Rückbauvorbereitung, Ausschreibung, Ausführung, Dokumentation; `pruefung/` für Schadstofffreigabe, Bauteilprüfung, Ausgangskontrolle; `datenmodell/` für Katasterstruktur, Bauteil-ID, Georeferenz, Raum-/Achsenbezug, AVV-Codes; `logistik/` für Ausbaufolge, Schutz, Verpackung, Zwischenlager, Transport, Marktplatz und Entsorgung.

## Kurzdefinition

Ein **Rückbaukataster** ist ein strukturiertes, positionsbezogenes Verzeichnis der Bauteile, Materialien, Schadstoffe, Rückbaufraktionen, Wiederverwendungslose und Entsorgungswege eines Gebäudes oder Areals. Es übersetzt Erkenntnisse aus Bestandsaufnahme, Bauwerksdiagnose, Materialinventar und Pre-Demolition Audit in eine arbeits- und logistikfähige Grundlage für selektiven Rückbau.

Der Begriff ist im deutschsprachigen Raum nicht überall einheitlich normiert. Er wird teils synonym oder überlappend mit Rückbaukonzept, Schadstoffkataster, Materialkataster, Bauteilkataster oder Rückbau- und Entsorgungskonzept verwendet. Für diese Datei wird Rückbaukataster als **dokumentarische Grundlage für selektiven Rückbau und Wiederverwendung** verstanden: Es sagt nicht nur, welche Materialien vorhanden sind, sondern wo sie liegen, wie sie auszubauen sind, welche Risiken bestehen und wohin sie gehen sollen.

## Relevanz für Wiederverwendung im Bauwesen

Wiederverwendung braucht operative Übersetzung. Ein Materialinventar kann zeigen, dass Bauteile vorhanden sind; ein Rückbaukataster macht daraus umsetzbare Rückbau-, Prüf-, Lager- und Vermarktungseinheiten. Es ist daher ein Schlüssel zwischen Planung und Baustelle.

Ein Rückbaukataster ist relevant, weil es:

- selektiven Rückbau strukturiert,
- wiederverwendungsfähige Bauteile vor Beschädigung schützt,
- Schadstoffe und Störstoffe getrennt führt,
- Ausbaufolgen, Verantwortlichkeiten und Logistik klärt,
- Reuse-Lose für Ausschreibung und Marktplätze vorbereitet,
- Material- und Abfallströme dokumentiert,
- Rückverfolgbarkeit vom eingebauten Zustand bis zum neuen Einsatz oder zur Entsorgung ermöglicht.

Ohne Rückbaukataster bleiben Audit- und Inventardaten häufig im Bericht stehen und erreichen die Baustellenlogik nicht.

## Fachinhalt

### Dokumenttyp

- **Zweck:** Operative, datenbasierte Grundlage für selektiven Rückbau, Wiederverwendung, Vorbereitung zur Wiederverwendung, Recycling und ordnungsgemäße Entsorgung.
- **Inhalt:** Bauteile, Materialfraktionen, Schadstoffe, Mengen, Orte, Ausbauverfahren, Reihenfolge, Verantwortlichkeiten, Schutzmaßnahmen, Lagerorte, Transportwege, Zielverwertung, Nachweise und Status.
- **Autorenschaft:** Rückbauplaner:innen, Pre-Demolition-Auditor:innen, Schadstoffgutachter:innen, Fachplanung, Bauherrschaft und ausführende Rückbauunternehmen; Fortschreibung während der Ausführung durch Baustellenleitung und Dokumentation.
- **Einsatzzeitpunkt:** Nach Bestandsaufnahme und Audit, vor Rückbauausschreibung; fortgeschrieben während Bauteilöffnungen, Demontage und Abtransport; abgeschlossen als Nachweis der ausgeführten Stoffströme.
- **Mindestinhalte:** Objekt- und Bauteil-ID, Ort, Material/Bauteiltyp, Menge, Zustand, Schadstoffstatus, Demontierbarkeit, Rückbauverfahren, Ausbaupriorität, Schutz- und Arbeitsschutzmaßnahmen, Zielweg, Lager- und Transportangaben, Nachweisstatus.
- **Datenlogik:** Ort/Bauteil → Rückbaulos → Menge → Risiko → Ausbauverfahren → Zielpfad → Status → Nachweis. Das Kataster muss auf der Baustelle nutzbar und zugleich digital auswertbar sein.
- **Anschlussfähigkeit:** Ausschreibung, Leistungsverzeichnis, Baustellenlogistik, Abfallbilanz, Materialmarktplatz, Materialpass, Rückbau- und Entsorgungskonzept, Behördennachweise, ESG-/Nachhaltigkeitsreporting.

### Mindeststruktur eines Rückbaukatasters

Ein praxisfähiges Rückbaukataster sollte mindestens folgende Register enthalten:

1. **Bauteil- und Materialregister:** ID, Position, Material, Menge, Einheit, Zustand, Datenquelle.
2. **Reuse-Register:** Bauteile mit Wiederverwendungspotenzial, Ausbauanforderungen, Prüfbedarf, Fotos, Vermarktungsstatus, Ziellager oder Käufer:in.
3. **Schadstoffregister:** Schadstoffverdacht, Probe, Laborwert, Lage, Ausbau-/Sanierungsverfahren, Entsorgungsweg.
4. **Fraktionenregister:** mineralisch, metallisch, Holz, Glas, Kunststoffe, Dämmstoffe, Gips, Bitumen, TGA, gefährliche Abfälle, sonstige Fraktionen.
5. **Rückbaufolgeplan:** Abhängigkeiten, Schutzmaßnahmen, vorgezogene Demontage, schwere Geräte, Kran- oder Transportbedarf.
6. **Logistikregister:** Verpackung, Zwischenlager, Paletten, Container, Witterungsschutz, Transport, Umschlag, externe Lager.
7. **Nachweisregister:** Fotos nach Ausbau, Wiegescheine, Übernahmescheine, Prüfzeugnisse, Verkaufsbelege, Entsorgungsnachweise, Abweichungen.

### Datenfelder für Wiederverwendung

Für Reuse-Lose sollten zusätzliche Felder geführt werden:

- Reuse-Losnummer,
- Bauteilgruppe und Produktbeschreibung,
- Anzahl, Maße, Gewicht,
- Zustand und Beschädigungen,
- Verbindungsart und Demontagewerkzeug,
- Schadstoffstatus,
- notwendige Reinigung, Reparatur oder Prüfung,
- Ausbauzeitfenster,
- Lageranforderung: trocken, frostfrei, stapelbar, palettiert, geschützt,
- potenzieller Zielmarkt oder internes Folgeprojekt,
- rechtlicher Status und Eigentumsübergang,
- Preisannahme oder Kostenvermeidung, falls erhoben,
- Status: identifiziert, geprüft, reserviert, ausgebaut, eingelagert, verkauft, wieder eingebaut, recycelt, entsorgt.

### Rückbaukataster vs. Materialinventar

Das Materialinventar ist die Ressourcensicht: Menge, Material, Ort, Datenqualität. Das Rückbaukataster ist die Handlungssicht: Was wird in welcher Reihenfolge durch wen wie ausgebaut, getrennt, geschützt, gelagert, transportiert oder entsorgt? Beide Dokumente müssen dieselben IDs verwenden, sonst geht die Rückverfolgbarkeit verloren.

### Rückbaukataster vs. Rückbau- und Entsorgungskonzept

Ein Rückbau- und Entsorgungskonzept beschreibt Strategie, Verfahren, Abfallfraktionen, Schadstoffe, Genehmigungs- und Entsorgungswege. Das Rückbaukataster kann als detaillierte Datenanlage dazu dienen. In Projekten mit Wiederverwendungsziel sollte das Kataster die Bauteil- und Materialebene genauer abbilden als ein rein entsorgungsorientiertes Konzept.

## Praxisbezug / Beispiele

- **Selektiver Rückbau eines Verwaltungsgebäudes:** Das Kataster teilt das Gebäude in Rückbaulose: Schadstoffsanierung, Reuse-Innenausbau, TGA-Demontage, mineralischer Rückbau, Metallfraktionen. Für jedes Los werden Räume, Mengen, Fotos und Zielpfade geführt.
- **Wiederverwendung von Türen:** Das Rückbaukataster enthält Türnummer, Raum, Maße, Brandschutzkennzeichnung, Beschlag, Zustand, Ausbauhinweis, Lagerplatz und Vermarktungsstatus. Schäden beim Ausbau werden nachgeführt.
- **Ziegel- oder Natursteinrückgewinnung:** Katastereinträge definieren Wand-/Flächenbereiche, Mörtelart, Ausbauverfahren, Reinigungsaufwand, Bruchquote und Lagerung.
- **Schadstoffhaltiger Bestand:** Asbesthaltige Bauteile werden vor Reuse- und Recyclingfraktionen separiert. Das Kataster verhindert, dass kontaminierte Stoffe in hochwertige Kreisläufe gelangen.
- **Digitales Kataster mit BIM-Bezug:** Bauteil-IDs im Modell verlinken Fotos, Proben, Rückbauanweisungen, Logistikstatus und Nachweise. Das erleichtert Bauleitung und Reporting.

## Herausforderungen / offene Fragen

- **Begriffliche Unschärfe:** Rückbaukataster ist nicht in jedem Rechtsraum ein standardisierter Dokumenttyp. Inhalt und Verbindlichkeit müssen im Projekt festgelegt werden.
- **Fortschreibung auf der Baustelle:** Rückbau erzeugt neue Erkenntnisse. Kataster müssen während der Ausführung aktualisiert werden, nicht nur vorab erstellt.
- **Bruch und Beschädigung:** Wiederverwendungspotenziale können beim Ausbau verloren gehen. Das Kataster muss Soll- und Ist-Mengen unterscheiden.
- **Schnittstelle zu Abfallrecht:** Sobald Bauteile ausgebaut werden, ist der rechtliche Status sorgfältig zu klären. Wiederverwendung, Vorbereitung zur Wiederverwendung und Abfallentsorgung haben unterschiedliche Anforderungen.
- **Logistik als Engpass:** Fehlender Lagerraum, kurze Bauzeiten oder unklare Abnehmer können technisch wiederverwendbare Bauteile in Recycling oder Entsorgung drängen.
- **Datendisziplin:** Ohne eindeutige IDs, Fotos und Statusfelder ist die Nachverfolgung vom Fundort bis zum Zielort kaum möglich.
- **Ausschreibungsintegration:** Das Rückbaukataster muss in Leistungsverzeichnisse und Vertragsbedingungen übersetzt werden, sonst bleibt es unverbindlich.
- **Regionale Verwertungswege:** Recycling-, Deponie- und Reuse-Infrastrukturen sind regional sehr unterschiedlich. Zielpfade müssen lokal geprüft werden.

## Quellen

- Europäische Kommission (2024): *EU Construction & Demolition Waste Management Protocol including guidelines for pre-demolition and pre-renovation audits*. Publications Office of the European Union. https://op.europa.eu/en/publication-detail/-/publication/d63d5a8f-64e8-11ef-a8ba-01aa75ed71a1/language-en
- Europäische Kommission (2018): *Guidelines for the waste audits before demolition and renovation works of buildings*. https://ec.europa.eu/docsroom/documents/31521
- DIN SPEC 91484:2023-09: *Verfahren zur Erfassung von Bauprodukten als Grundlage für Bewertungen des Anschlussnutzungspotentials vor Abbruch- und Renovierungsarbeiten*. https://www.dinmedia.de/de/technische-regel/din-spec-91484/371235753
- FCRBE / Interreg NWE: *A guide for identifying the reuse potential of construction products*. https://vb.nweurope.eu/media/10132/en-fcrbe_wpt2_d12_a_guide_for_identifying_the_reuse_potential_of_construction_products.pdf
- Land Berlin (2024): *Leitfaden zur Erstellung eines Rückbau- und Entsorgungskonzeptes*. https://www.berlin.de/nachhaltige-beschaffung/_assets/beschaffungshinweise/leitfaden_rueckbau.pdf
- Kreislaufwirtschaftsgesetz (KrWG), insbesondere § 6 Abfallhierarchie. https://www.gesetze-im-internet.de/krwg/
- Gewerbeabfallverordnung (GewAbfV). https://www.gesetze-im-internet.de/gewabfv_2017/
- Abfallverzeichnis-Verordnung (AVV). https://www.gesetze-im-internet.de/avv/
- VDI Zentrum Ressourceneffizienz: *Rückbau im Hochbau – Potenziale der Ressourcenschonung im Bauwesen*. https://www.ressource-deutschland.de
- Umweltbundesamt: Informationen zu Bauabfällen und Ressourcenschutz. https://www.umweltbundesamt.de/daten/ressourcen-abfall/verwertung-entsorgung-ausgewaehlter-abfallarten/bauabfaelle
- Leibniz-Institut für ökologische Raumentwicklung: *Materialkataster Deutschland / IÖR-Materialkataster*. https://www.ioer.de
- DGNB: *Gebäuderessourcenpass*. https://www.dgnb.de/de/nachhaltiges-bauen/zirkulaeres-bauen/gebaeuderessourcenpass
