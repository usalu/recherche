---
type: Werkzeug
---

## Verknüpfungen

- **Übergeordnete Themen:** Track & Trace, digitale Materialpässe, Bauteilidentifikation, QR-Code, RFID, NFC, Direct Product Marking, Lieferkette, Reuse-Logistik.
- **Verwandte Dateien:** `werkzeug/Loopfront.md`, `werkzeug/Upcyclea.md`, `werkzeug/Maconda_Materialpass.md`, `werkzeug/Qflow.md`, `werkzeug/Pre_Demolition_Audit_Tools.md`, `logistik/Lagerung.md`, `logistik/Transport.md`, `datenmodell/Materialpass.md`, `dokument/Bauteiletikett.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** QR-Codes, RFID-Tags, NFC-Chips, GS1 Digital Link, Direct Product Marking, Material Passport, Circular Construction Supply Chains, Bauteillogistik, Komponentenverfolgung.

## Kurzdefinition

**QR-, RFID- und NFC-Materialtracking** bezeichnet die digitale Kennzeichnung und Nachverfolgung von Bauprodukten und Bauteilen über ihren Lebenszyklus. Ein physischer Datenträger – etwa QR-Code, RFID-Tag, NFC-Chip oder direkte Markierung – verbindet ein Bauteil mit einem digitalen Datensatz wie Materialpass, Prüfprotokoll, Inventareintrag oder Marktplatzangebot.

Für Wiederverwendung ist diese Technik wichtig, weil Bauteile nach Ausbau, Lagerung, Transport und Wiedereinbau ihre Identität und Dokumentation behalten müssen.

## Relevanz für Wiederverwendung im Bauwesen

Reuse scheitert oft an Informationsverlust: Nach Jahrzehnten ist unklar, welches Produkt verbaut wurde, welche Leistung es hat, wie es ausgebaut wurde oder wem es gehört. Tracking-Technologien reduzieren diesen Informationsverlust.

Sie sind reuse-relevant, weil sie:

- Bauteile eindeutig identifizierbar machen,
- Materialpassdaten direkt am Objekt abrufbar halten,
- Lager- und Transportprozesse unterstützen,
- Prüf-, Wartungs- und Rückbauhistorien dokumentieren,
- Verwechslungen und Datenbrüche reduzieren,
- Bauteile in Marktplätzen und Inventaren referenzierbar machen.

## Fachinhalt

### Technologietypen

- **QR-Code:** günstig, druckbar, mit Smartphone lesbar; benötigt Sichtkontakt und kann beschädigt werden.
- **RFID:** drahtlose Identifikation ohne direkte Sicht; nützlich für Lager und große Mengen; benötigt Lesegerät und geeignete Frequenz.
- **NFC:** kurze Reichweite, mit vielen Smartphones lesbar; geeignet für wartungsnahe Interaktion am Bauteil.
- **Direct Product Marking (DPM):** dauerhafte Markierung direkt auf Material; robust, aber material- und oberflächenabhängig.
- **Barcode / Data Matrix:** industriell etabliert; oft weniger datenreich als QR/NFC-Verknüpfungen.

### Datenmodell

Der Datenträger sollte nicht alle Daten selbst enthalten. Sinnvoll ist meist eine eindeutige ID oder URL, die auf einen gepflegten Datensatz verweist:

- Objekt-ID,
- Materialpass-ID,
- Hersteller- oder Produktdaten,
- Einbauort und Ausbauort,
- Zustand und Prüfstatus,
- Wartungs- und Rückbauhistorie,
- Lagerort,
- Eigentümer / Verantwortliche,
- Wiederverwendungsfreigabe,
- Dokumente und Fotos.

### Einsatzszenarien

- **Neubau:** Bauteile werden beim Einbau markiert, um später identifizierbar zu bleiben.
- **Rückbau:** Auditierte Bauteile erhalten Tags, bevor sie ausgebaut werden.
- **Lager:** Bauteile können ein-, aus- und umgelagert werden, ohne Datenbezug zu verlieren.
- **Wiedereinbau:** Prüfstatus, Herkunft und Dokumentation bleiben nachvollziehbar.
- **Facility Management:** Wartung und Austausch werden bauteilbezogen dokumentiert.

### Schnittstellen

- Materialpass-Plattformen,
- Reuse-Marktplätze,
- Lagerverwaltungs- und Logistiksysteme,
- BIM / IFC über Objekt-GUIDs,
- Prüf- und Wartungsdatenbanken,
- QR/NFC-basierte mobile Apps.

## Praxisbezug / Beispiele

- **QR-basierte Materialpässe:** Forschung zu QR-Code-basierten Materialpässen zeigt, dass einfache Track-and-Trace-Systeme Wiederverwendung über mehrere Lebenszyklusphasen unterstützen können.
- **Circular Construction Supply Chains:** Neuere Studien vergleichen QR, NFC und Direct Product Marking für zirkuläre Lieferketten und zeigen, dass die Wahl des Datenträgers von Material, Umgebung, Lebensdauer und Prozess abhängt.
- **Bauteile mit hohem Reuse-Potenzial:** Besonders geeignet sind Türen, Leuchten, Trennwände, Fassadenelemente, Stahlbauteile, Holzmodule, Doppelböden, Möbel und technische Geräte.

## Herausforderungen / offene Fragen

- **Dauerhaftigkeit:** Tags müssen Reinigung, Witterung, UV, Brand, Feuchte, Ausbau und Transport überstehen.
- **Datenträgerposition:** Der Code muss zugänglich sein, darf aber Nutzung, Ästhetik und Brandschutz nicht beeinträchtigen.
- **Datenschutz und Eigentum:** Eigentümer-, Standort- und Gebäudedaten können sensibel sein.
- **Datenpflege:** Ein QR-Code nützt wenig, wenn der verlinkte Datensatz verschwindet oder veraltet.
- **Standardisierung:** Ohne gemeinsame ID- und Datenstruktur entstehen Insellösungen.
- **Kosten:** Bei sehr günstigen oder massenhaften Produkten kann Tagging unwirtschaftlich sein.
- **Verwechslungsrisiko:** Tags können entfernt, überklebt oder falsch zugeordnet werden; Auditprozesse müssen das berücksichtigen.

## Quellen

- Byers, B. S. u. a.: **QR Code-Based Material Passports for Component Reuse Across Life Cycle Stages in Small-Scale Construction**, Circular Economy and Sustainability, 2023. https://circulareconomyjournal.org/articles/qr-code-based-material-passports-for-component-reuse-across-life-cycle-stages-in-small-scale-construction/. Zugriff: 2026-04-27.
- ETH Research Collection: **QR Code-Based Material Passports**, 2023. https://www.research-collection.ethz.ch/bitstreams/5916fa9e-0491-4a2c-9bb3-6243e97e0891/download. Zugriff: 2026-04-27.
- Byers, B. S. u. a.: **Data carriers for circular construction supply chains**, Journal of Cleaner Production, 2025. https://www.sciencedirect.com/science/article/pii/S0959652625004032. Zugriff: 2026-04-27.
- Dervishaj, A. u. a.: **Enabling reuse of prefabricated concrete components through tracking technologies**, 2023. https://ec-3.org/publications/conferences/EC32023/papers/EC32023_220.pdf. Zugriff: 2026-04-27.
- GS1: **GS1 Digital Link**. https://www.gs1.org/standards/gs1-digital-link. Zugriff: 2026-04-27.
