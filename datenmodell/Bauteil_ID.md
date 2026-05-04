# Bauteil_ID

## Verknüpfungen

**Übergeordnete Themen**
- Datenmodellierung für Wiederverwendung, Urban Mining, Bauteilkataloge und Materialpässe
- Digitale Bestandsaufnahme, Pre-Demolition-Audit, Rückbauplanung, Lager- und Marktplatzprozesse
- Interoperabilität zwischen BIM/IFC, Materialdatenbank, Dokumentation, Kennwerten und Logistik

**Verwandte Dateien**
- `datenmodell/IFC.md`
- `datenmodell/Klassifikation.md`
- `datenmodell/Materialpass_Schema.md`
- `datenmodell/Ontologie.md`
- `datenmodell/Taxonomie.md`
- `werkzeug/BIM.md`, `werkzeug/IFC_Viewer.md`, `werkzeug/Dataview.md`, `werkzeug/Materialdatenbank.md`, `werkzeug/Madaster_Plattform.md`, `werkzeug/Concular_Plattform.md`
- `dokument/`: Rückbauaudit, Materialpass, Prüfberichte, Fotos, Herkunftsnachweise, EPDs
- `logistik/`: Ausbau, Verpackung, Lager, Transport, Übergabe, Wiedereinbau
- `kennwert/`: Masse, Stückzahl, Abmessungen, CO₂-/GWP-Werte, Restwert, Zustands- und Qualitätskennwerte
- `meta/`: Namenskonventionen, Datenqualität, Quellenkritik, Versionierung, Rollen/Rechte

**Relevante Akteure / Fallstudien / Materialien / Standards / Methoden**
- Bestandserfasser:innen, Planer:innen, Rückbauunternehmen, Prüfstellen, Plattformbetreiber, Lagerlogistik, Bauherrschaft, Behörden
- DIN SPEC 91484 als Verfahren zur Erfassung von Bauprodukten vor Abbruch- und Renovierungsarbeiten
- IFC / buildingSMART, IDS, bSDD, ISO 12006, ISO 23386/23387, ISO 19650, GS1 Digital Link, EU-Digital-Product-Passport-Ansätze

## Kurzdefinition

Eine **Bauteil_ID** ist ein dauerhaftes, eindeutiges Identifikationsmerkmal für ein reales Bauteil, eine Bauteilgruppe, eine Charge oder einen wiederverwendbaren Materialstrom. Im ReUse-Kontext ist sie der Primärschlüssel, mit dem Informationen aus Bestandsaufnahme, BIM/IFC-Modell, Materialpass, Fotos, Prüfungen, Rückbau, Lagerung, Marktplatz, Transport und Wiedereinbau zuverlässig zusammengeführt werden.

Die Bauteil_ID ist **keine Klassifikation**. Sie sagt nicht primär, *was* ein Bauteil ist, sondern *welches konkrete Objekt* gemeint ist. Ein Türblatt kann z. B. die Klasse „Innentür“ tragen, aber zusätzlich eine eigene Bauteil_ID erhalten, damit sein Zustand, seine Maße, sein Ausbauort und seine zukünftige Verwendung eindeutig nachvollziehbar bleiben.

## Relevanz für Wiederverwendung im Bauwesen

Wiederverwendung scheitert in der Praxis häufig nicht an der Existenz verwertbarer Bauteile, sondern an der fehlenden Verknüpfbarkeit von Informationen: Ein Element wird im Aufmaß erfasst, in Fotos dokumentiert, im Rückbau gelagert, später auf einer Plattform angeboten und noch später in ein neues Projekt integriert. Ohne stabile ID entstehen Medienbrüche, Dubletten, verlorene Nachweise und falsche Zuordnungen.

Die Bauteil_ID ermöglicht:
- **Rückverfolgbarkeit** von der Quelle bis zum Wiedereinbau.
- **Datenintegration** zwischen `werkzeug/`, `dokument/`, `logistik/` und `kennwert/`.
- **Qualitätssicherung** durch eindeutige Verknüpfung von Prüfprotokollen, Fotos, Messwerten und Freigaben.
- **Mengensicherheit** für Inventarlisten, CO₂-Bilanzen, Restwertberechnungen und Lagerbestände.
- **Revisionssicherheit** bei Änderungen, Zerlegung, Bündelung, Reparatur, Verkauf oder Verlust.
- **Marktplatzfähigkeit**, weil ein Angebot nicht nur eine Kategorie, sondern ein konkretes Objekt mit dokumentierter Historie adressiert.

## Fachinhalt

### Abgrenzung zu verwandten Identifikatoren

| Identifikator | Hauptzweck | Risiko im ReUse-Kontext |
|---|---|---|
| `IfcRoot.GlobalId` | Eindeutige ID eines Objekts in einem IFC-Modell | Kann beim Export, Remodellieren oder Zusammenführen verändert werden; nicht automatisch physische Objektidentität. |
| Bauteil_ID | Persistente ID eines realen Bauteils oder Bauteilbestands | Muss aktiv verwaltet werden; braucht Regeln für Splits, Merges und Ersatzobjekte. |
| Klassifikationscode | Einordnung nach System, Funktion, Produktgruppe oder Kostenstruktur | Nicht eindeutig für einzelne Objekte. |
| Produkt-ID / GTIN / Hersteller-ID | Serienprodukt oder Produktvariante | Reicht nicht für gebrauchte Einzelstücke mit individueller Nutzungsgeschichte. |
| Chargen-/Losnummer | Produktions- oder Liefercharge | Hilfreich für Herkunft, aber meist nicht ausreichend für einzelne Bauteile. |
| Materialpass-ID | Dokument- oder Datensatz-ID eines Passes | Kann mehrere Bauteile aggregieren; ist nicht zwingend identisch mit Bauteil_ID. |
| Lager-ID / Standortcode | Logistische Position | Ändert sich während Ausbau, Transport und Lagerung. |

### Empfohlene Granularität

Die Granularität wird nach ReUse-Ziel gewählt, nicht nach Modellierungsgewohnheit. Sinnvolle Ebenen sind:

1. **Einzelbauteil**: z. B. Fensterflügel, Stahlträger, Türblatt, Sanitärobjekt.
2. **Bauteilgruppe / Assembly**: z. B. Fensterelement inklusive Rahmen, Beschläge und Glas.
3. **Charge / Set**: z. B. 120 identische Bodenplatten, Leuchtenserie, Fassadenpaneele gleicher Ausführung.
4. **Materialstrom**: z. B. sortenreiner Ziegelbruch, Altholz, Natursteinplatten.
5. **Dokumentationsobjekt**: z. B. ein Bauteilkatalogeintrag, der mehrere gleichartige physische Objekte zusammenfasst.

Für Wiederverwendung mit hoher Qualität ist die Einzelbauteil- oder Set-Ebene meist sinnvoller als eine reine Materialstrom-Ebene. Für Recycling, Verwertung oder frühe Potenzialabschätzungen kann eine gröbere Ebene genügen.

### Grundprinzipien eines robusten ID-Schemas

- **Persistenz**: Die ID bleibt über Erfassung, Ausbau, Lagerung, Verkauf und Wiedereinbau stabil.
- **Eindeutigkeit**: Eine ID bezeichnet genau ein Objekt oder genau einen definierten Bestand.
- **Nicht zu viel Bedeutung codieren**: Standort, Zustand oder Besitzer können sich ändern; sie gehören als Felder in den Datensatz, nicht zwingend in die ID.
- **Maschinenlesbarkeit**: UUID, URI, QR-Code, NFC/RFID oder GS1-Digital-Link können eingesetzt werden.
- **Menschenlesbare Kurzform**: Ergänzend zur technischen ID ist ein kurzer Label-Code im Baustellenalltag hilfreich.
- **Versionierung**: Änderungen am Datensatz werden versioniert, ohne die physische Objektidentität zu verlieren.
- **Provenienz**: Es muss erkennbar sein, wer wann mit welcher Methode welche Information erzeugt hat.
- **Split/Merge-Regeln**: Wenn eine Baugruppe zerlegt oder mehrere Objekte gebündelt werden, müssen Eltern-Kind-Beziehungen gespeichert werden.

### Minimaler Datensatz zur Bauteil_ID

```yaml
bauteil_id: "btl:projekt-abc:000123"
id_schema: "repo-bauteil-id-v1"
id_issuer: "Organisation / Projekt / Plattform"
id_created: "YYYY-MM-DD"
id_status: "aktiv | reserviert | ausgebaut | gelagert | angeboten | verkauft | wiederverbaut | ausgeschieden"
object_granularity: "Einzelbauteil | Set | Baugruppe | Materialstrom"
label_human_readable: "ABC-TUER-000123"
parent_id: null
child_ids: []
related_ifc_global_ids: []
related_materialpass_ids: []
classification:
  - system: "IFC"
    code: "IfcDoor"
  - system: "lokale Taxonomie"
    code: "ausbau.tuer.innentuer"
current_location: "Gebäude A / EG / Raum 0.12"
source_location: "Gebäude A / EG / Raum 0.12"
owner_or_custodian: "optional / datenschutzsensibel"
data_quality: "hoch | mittel | niedrig | unbekannt"
last_verified: "YYYY-MM-DD"
```

### Operative Einbindung im Repo

Eine Bauteil_ID sollte in allen Dateien wiederkehren, die dasselbe physische Objekt betreffen:

- In `dokument/`: als Referenz in Fotos, Prüfberichten, Rückbauaudit, Materialpass und Freigaben.
- In `werkzeug/`: als Import-/Export-Schlüssel für BIM, Datenbanken, Marktplätze, Obsidian/Dataview und Materialpass-Plattformen.
- In `logistik/`: als Packstück-, Lager- und Übergabereferenz.
- In `kennwert/`: als Bezugsschlüssel für Masse, Stückzahl, Abmessung, GWP, Restwert und Zustandsnote.
- In `meta/`: als Gegenstand von Namensregeln, Rollen, Qualitätssicherungsprozessen und Änderungsprotokollen.

### Beziehung zu IFC

IFC-Objekte besitzen eigene GUIDs. Diese sind für den Modellaustausch wichtig, reichen aber für physische ReUse-Prozesse oft nicht aus. Empfehlenswert ist:

- IFC-GUID als **Modellobjekt-ID** behalten.
- Bauteil_ID als **persistente reale Objekt-ID** zusätzlich führen.
- Zuordnung über Property Set, externe Referenz oder separate Mapping-Tabelle dokumentieren.
- Bei Scan-to-BIM oder Modellneuaufbau prüfen, ob IFC-GUIDs erhalten, neu erzeugt oder gemappt wurden.
- Bauteil_ID nicht aus IFC-GUID allein ableiten, wenn physische Rückverfolgbarkeit über Modellversionen hinweg gebraucht wird.

### Datenqualitätsstufen

Für Bestandsdaten ist eine ID nur so belastbar wie ihre Zuordnung. Sinnvoll sind Qualitätsstufen:

- **A – geprüft**: Objekt vor Ort markiert, gemessen, fotografiert, ID physisch angebracht, Dokumente verknüpft.
- **B – plausibel**: Objekt modelliert und fotografisch belegt, aber keine vollständige Prüfung.
- **C – geschätzt**: Aus Plan, Scan oder Mengenmodell abgeleitet, noch nicht verifiziert.
- **D – unklar**: Dublette, Konflikt, fehlender Standort oder unsichere Objektgrenze.

## Praxisbezug / Beispiele

### Beispiel 1: Türen aus einem Bürogebäude

Ein Rückbauaudit erfasst 86 Innentüren. Jede Tür erhält eine Bauteil_ID. Gleichartige Türen werden zusätzlich als Set gruppiert. Fotos, Maße, Brandschutzangaben, Beschlagtyp, Zustand und Ausbauort werden an der ID gespeichert. Beim Ausbau wird jede Tür mit QR-Code versehen. Im Lager werden Lagerplatz, Packeinheit und Schäden aktualisiert. Wird eine Tür später verkauft, bleibt die Bauteil_ID bestehen und erhält eine neue Phase „wiederverbaut“.

### Beispiel 2: Stahlträger

Stahlträger erfordern neben Maßen und Profiltyp auch Angaben zu Stahlgüte, Anschlüssen, Korrosion, Brandschutzbeschichtung und Prüfstatus. Die Bauteil_ID verknüpft Geometrie, Laborprüfung, statische Wiederverwendbarkeit, Lagerort und CO₂-Kennwert. Wenn ein langer Träger zugeschnitten wird, entstehen neue Kind-IDs; die ursprüngliche ID bleibt als Herkunftsobjekt erhalten.

### Beispiel 3: IFC-Modell und Materialpass

Ein Bestandsmodell enthält `IfcWindow`-Objekte. Die Bauteil_ID wird zusätzlich in einem ReUse-Property-Set oder in einer externen Mapping-Tabelle geführt. Der Materialpass verweist über dieselbe ID auf Verglasung, Rahmenmaterial, U-Wert, Zustand und Ausbauhinweise. Das IFC-Modell dient der räumlichen Lokalisierung; der Materialpass enthält die zirkulären Zusatzdaten.

## Herausforderungen / offene Fragen

- **Physische Markierung**: QR-Codes, Etiketten und RFID müssen Rückbau, Staub, Feuchte, Stapelung und Transport überstehen.
- **Dubletten und Objektgrenzen**: Bei Bestandsaufnahme durch mehrere Teams entstehen leicht doppelte oder widersprüchliche IDs.
- **Modellwechsel**: IFC-Exports, Scan-to-BIM-Neumodellierung oder Plattformmigration können technische IDs verändern.
- **Granularität**: Zu feine IDs erzeugen Aufwand; zu grobe IDs verhindern gezielte Wiederverwendung.
- **Eigentum und Datenschutz**: Herkunfts-, Eigentums- und Standortdaten können vertraulich sein.
- **Rechtsstatus**: Eine ID ersetzt keine Zulassung, Gewährleistung, CE-Konformität, Prüfbescheinigung oder Freigabe.
- **Dauerhafte Auflösung von Links**: QR/URI-Systeme müssen auch nach Projektende erreichbar bleiben oder archiviert werden.
- **Verhältnis zum EU-Digital-Product-Passport**: Produktpässe adressieren vor allem Produktinformationen; gebrauchte Einzelbauteile benötigen zusätzlich zustands- und objektspezifische ReUse-Daten.

## Quellen

- DIN Media: DIN SPEC 91484:2023-09, Verfahren zur Erfassung von Bauprodukten als Grundlage für Bewertungen des Anschlussnutzungspotentials vor Abbruch- und Renovierungsarbeiten. https://www.dinmedia.de/de/technische-regel/din-spec-91484/371235753
- buildingSMART Technical: Industry Foundation Classes (IFC) – open international standard, ISO 16739-1:2024. https://technical.buildingsmart.org/standards/ifc/
- buildingSMART: Information Delivery Specification (IDS). https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids/
- buildingSMART: buildingSMART Data Dictionary (bSDD), Referenzierbarkeit von Definitionen in IFC und IDS. https://www.buildingsmart.org/users/services/buildingsmart-data-dictionary/
- ISO 12006-2:2015, Building construction — Organization of information about construction works — Part 2: Framework for classification. https://www.iso.org/standard/61753.html
- ISO 23386:2020, Methodology to describe, author and maintain properties in interconnected data dictionaries. https://www.iso.org/standard/75401.html
- ISO 23387:2020, Data templates for construction objects used in the life cycle of built assets. https://www.iso.org/standard/75403.html
- GS1: GS1 Digital Link Standard. https://ref.gs1.org/standards/digital-link/
- EUR-Lex: Regulation (EU) 2024/3110 on construction products. https://eur-lex.europa.eu/eli/reg/2024/3110/oj/eng
