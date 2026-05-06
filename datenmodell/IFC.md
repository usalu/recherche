---
type: Datenmodell
---

# IFC

## Verknüpfungen

**Übergeordnete Themen**
- openBIM, Interoperabilität, Bestandsmodellierung, digitale Bauwerksdokumentation
- Datenaustausch zwischen Planung, Bestandserfassung, Rückbau, Materialpass, LCA, Facility Management und ReUse-Marktplätzen
- Objektorientierte Modellierung von Gebäuden und Infrastrukturen

**Verwandte Dateien**
- `datenmodell/Bauteil_ID.md`
- `datenmodell/Klassifikation.md`
- `datenmodell/Materialpass_Schema.md`
- `datenmodell/Ontologie.md`
- `datenmodell/Taxonomie.md`
- `werkzeug/BIM.md`, `werkzeug/IFC_Viewer.md`, `werkzeug/Rhino.md`, `werkzeug/Materialdatenbank.md`, `werkzeug/Madaster_Plattform.md`, `werkzeug/Concular_Plattform.md`
- `dokument/`: Bestandsmodell, Rückbauaudit, Prüfberichte, Modellvalidierung, Materialpass
- `logistik/`: räumliche Verortung, Ausbauabschnitte, Mengenexporte, Packlisten
- `kennwert/`: Mengen, Massen, Flächen, Volumen, GWP-/LCA-Werte, Zustandskennwerte
- `meta/`: Informationsanforderungen, Datenqualitätsregeln, IDS, CDE, Versionierung

**Relevante Akteure / Fallstudien / Materialien / Standards / Methoden**
- buildingSMART International, Softwarehersteller, BIM-Koordination, Bestandserfassung, Fachplanung, Rückbau- und ReUse-Plattformen
- IFC 2x3, IFC 4, IFC 4.3 / ISO 16739-1:2024, MVD, IDS, bSDD, ifcOWL, IFC-STEP, IFC-XML, IFC-JSON, IFC-RDF/TTL

## Kurzdefinition

**IFC** steht für **Industry Foundation Classes**. Es ist ein offener, herstellerneutraler Datenstandard zur digitalen Beschreibung der gebauten Umwelt, einschließlich Gebäuden, Bauteilen, technischen Anlagen, räumlichen Strukturen, Eigenschaften, Beziehungen, Mengen und teilweise Prozessen. IFC wird von buildingSMART International entwickelt und ist als ISO 16739 standardisiert.

Im ReUse-Kontext ist IFC vor allem ein **Austausch- und Strukturmodell**: Es hilft, Bauteile räumlich und objektorientiert zu beschreiben, Mengen zu exportieren, Klassifikationen und Eigenschaften zu transportieren und Materialpassdaten oder Bauteil_IDs mit BIM-Objekten zu verknüpfen. IFC ist jedoch kein vollständiger Materialpass, kein Prüfbericht, kein Lagerverwaltungssystem und keine Garantie für tatsächliche Wiederverwendbarkeit.

## Relevanz für Wiederverwendung im Bauwesen

IFC ist relevant, weil Wiederverwendung auf verlässliche Objektinformationen angewiesen ist. Ein Bauteil muss nicht nur als geometrisches Element sichtbar sein, sondern mit Herkunft, Material, Zustand, Abmessungen, Verbindungen, Mengen, Dokumenten und potenzieller Anschlussnutzung verknüpfbar werden.

IFC kann im ReUse-Prozess folgende Rollen übernehmen:

- **Objektstruktur**: Bauteile werden als Objekte statt nur als Linien, Flächen oder Mengen geführt.
- **Räumliche Verortung**: Gebäude, Geschosse, Räume und Zonen können die Quelle eines Bauteils beschreiben.
- **Mengenbasis**: Flächen, Volumen, Stückzahlen und Geometrien können für Inventar, CO₂-Bilanz und Logistik exportiert werden.
- **Interoperabilität**: Verschiedene BIM- und Analysewerkzeuge können auf einem gemeinsamen Austauschformat arbeiten.
- **Verknüpfung**: Bauteil_IDs, Klassifikationen, Materialangaben und externe Dokumente können referenziert werden.
- **Validierung**: Informationsanforderungen können über IDS und Modellprüfungen maschinenlesbar formuliert werden.

## Fachinhalt

### Grundstruktur von IFC

IFC beschreibt Bauwerksinformationen objektorientiert. Zentrale Ebenen sind:

- **Projektstruktur**: `IfcProject`, `IfcSite`, `IfcBuilding`, `IfcBuildingStorey`, `IfcSpace`, Zonen und räumliche Container.
- **Physische Objekte**: z. B. `IfcWall`, `IfcSlab`, `IfcBeam`, `IfcColumn`, `IfcDoor`, `IfcWindow`, `IfcRoof`, `IfcStair`, `IfcCurtainWall`, MEP-Objekte.
- **Typen und Vorkommen**: Ein Objekttyp beschreibt wiederkehrende Eigenschaften; einzelne Instanzen beschreiben konkrete Vorkommen.
- **Beziehungen**: räumliche Zuordnung, Aggregation, Materialzuweisung, Öffnungen, Anschlüsse, Klassifikationen, Dokumentreferenzen.
- **Eigenschaften**: Attribute, Property Sets (`Pset_*`), benutzerdefinierte Property Sets, Mengen (`Qto_*`).
- **Materialien**: einzelne Materialien, Materialschichten, Materialprofile, Materiallisten und Relationen zu Objekten.
- **Repräsentationen**: Geometrie, vereinfachte Körper, BRep, Extrusionen, Achsen, 2D/3D-Repräsentationen.

### IFC und ReUse-Daten

Für Wiederverwendung sind insbesondere folgende Informationsgruppen wichtig:

| ReUse-Information | IFC-Abbildung | Bewertung |
|---|---|---|
| Objektklasse | IFC-Entität, z. B. `IfcDoor` | Gut geeignet, aber manchmal zu grob oder exportabhängig. |
| Räumliche Herkunft | räumliche IFC-Hierarchie und `IfcRelContainedInSpatialStructure` | Sehr nützlich für Rückbauabschnitte und Inventar. |
| Bauteil_ID | eigenes Property Set, externe Referenz oder Mapping-Tabelle | Muss projektspezifisch geregelt werden. |
| Material | `IfcMaterial`, Schicht-/Profilsets | Geeignet für bekannte Schichten; Bestandsunsicherheiten müssen ergänzt werden. |
| Mengen | Quantity Sets, Geometrieauswertung | Nützlich, aber abhängig von Modellqualität. |
| Zustand | meist benutzerdefinierte Properties | Kein einheitlich durchgesetztes IFC-Kernthema. |
| Schadstoffe | benutzerdefinierte Properties oder externe Dokumente | Nur mit Prüf- und Quellenbezug belastbar. |
| Demontierbarkeit | benutzerdefinierte Properties, Beziehungen, Dokumente | In IFC nicht hinreichend standardisiert. |
| Prüfberichte / Fotos | `IfcDocumentReference` oder externe Links | Gut als Referenz, nicht als vollständiges DMS. |
| Logistikstatus | externe Datenbank, Property oder Prozessmodell | IFC allein ist dafür meist unpraktisch. |

### Empfohlene ReUse-Property-Set-Struktur

Für ein Repo-nahes IFC-ReUse-Modell kann ein eigenes Property Set genutzt werden, solange es klar dokumentiert und validierbar ist. Beispiel:

```text
Pset_ReUseIdentity
- ReUse_Bauteil_ID
- ReUse_Passport_ID
- ReUse_Source_Building
- ReUse_Source_Room
- ReUse_Data_Quality
- ReUse_Inventory_Date

Pset_ReUseCondition
- Condition_Grade
- Condition_Description
- Damage_Observed
- Test_Status
- Hazard_Status
- Reuse_Clearance

Pset_ReUseLogistics
- Dismantling_Status
- Dismantling_Method
- Storage_Location
- Packaging_Unit
- Availability_Date
```

Wichtig: Solche Properties sollten nicht isoliert erfunden werden. Besser ist, sie mit `datenmodell/Klassifikation.md`, `datenmodell/Materialpass_Schema.md`, `datenmodell/Ontologie.md`, bSDD, ISO 23386/23387 und IDS abzugleichen.

### IFC als Austauschschicht, nicht als alleinige Datenbank

IFC eignet sich besonders für Austausch, Archivierung und Koordination. Für ein ReUse-Repository sollte IFC jedoch nicht die einzige Datenquelle sein. Ein belastbares Datenmodell trennt:

- **IFC-Modell**: Geometrie, räumliche Struktur, Objektbeziehungen, Basismengen.
- **Bauteil_ID-Tabelle**: stabile Identität, Mapping, Status, Historie.
- **Materialpass-Schema**: zirkuläre, ökologische, technische und rechtliche Zusatzdaten.
- **Dokumentenablage**: Fotos, Prüfberichte, EPDs, Zulassungen, Rückbauanleitungen.
- **Logistiksystem**: Lagerorte, Packeinheiten, Transporte, Reservierungen.
- **Kennwerttabellen**: Massen, GWP, Restwerte, Zustandsgrade, Wiederverwendungspotenziale.

### IDS und Validierung

Die buildingSMART Information Delivery Specification (IDS) kann definieren, welche Informationen ein IFC-Modell für einen ReUse-Anwendungsfall enthalten muss. Beispiele:

- Alle `IfcDoor`-Objekte müssen eine `ReUse_Bauteil_ID` besitzen.
- Alle wiederverwendbaren Fenster müssen Material, Abmessungen, Zustand und Prüfstatus enthalten.
- Bauteile mit ReUse-Status „angeboten“ müssen eine Klassifikation, Menge und Lager-/Verfügbarkeitsangabe haben.
- Werte müssen definierte Einheiten, Vokabulare und zulässige Wertbereiche nutzen.

Damit wird IFC von einem bloßen Austauschformat zu einem überprüfbaren Liefergegenstand.

### IFC, Klassifikation und bSDD

IFC-Klassen reichen nicht aus, um alle ReUse-Fragen zu beantworten. Ein Objekt kann gleichzeitig folgende Einordnungen brauchen:

- IFC-Entität: technische Modellklasse, z. B. `IfcWindow`.
- Produkt-/Bauteilklassifikation: z. B. Uniclass, OmniClass, eClass, DIN-Systematik oder lokale Taxonomie.
- Materialklassifikation: z. B. Holz, Aluminium, Verbundglas, mineralisch.
- ReUse-Taxonomie: Zustand, Demontierbarkeit, Verfügbarkeit, Anschlussnutzung.
- bSDD-Definitionen: semantisch definierte Eigenschaften und Klassen, die in IFC oder IDS referenziert werden können.

## Praxisbezug / Beispiele

### Beispiel 1: Scan-to-BIM für Rückbauaudit

Ein Bestandsgebäude wird gescannt und modelliert. IFC exportiert Wände, Türen, Fenster, Decken und Träger mit räumlicher Struktur. Für ReUse werden zusätzlich Bauteil_ID, Zustand, Demontagehinweise und Schadstoffstatus ergänzt. Unsichere Bauteile erhalten Datenqualitätsstufe „geschätzt“ und werden nach Vor-Ort-Prüfung aktualisiert.

### Beispiel 2: Materialpass-Plattform

Ein IFC-Modell liefert Mengen und Bauteilstruktur an eine Materialpass-Plattform. Die Plattform ergänzt material- und zirkularitätsbezogene Daten, etwa GWP, Recyclinganteil, Schadstoffhinweise, Restwert oder Wiederverwendungspotenzial. Die Verbindung erfolgt über Bauteil_ID und IFC-GUID-Mapping.

### Beispiel 3: Marktplatzexport

Aus einem IFC-Modell werden Fensterobjekte mit Maßen, Material, Lage und Fotos selektiert. Ein separater ReUse-Datensatz enthält Preis, Verfügbarkeit, Ausbauzeitpunkt, Prüfstatus und Lagerort. Das Marktplatzangebot referenziert die Bauteil_ID, nicht nur die IFC-GUID.

## Herausforderungen / offene Fragen

- **Modellqualität im Bestand**: Bestandsmodelle sind oft unvollständig, approximiert oder nicht as-built-validiert.
- **Exportverluste**: Property Sets, Klassifikationen, Materialien und GUIDs können je nach Software unterschiedlich exportiert werden.
- **Zustandsdaten**: IFC standardisiert nicht hinreichend, wie Verschleiß, Schadstoffrisiko, Restlebensdauer oder Prüfstatus zu führen sind.
- **Verbindungen und Demontage**: Für Wiederverwendung sind Anschlüsse, Fügetechniken und zerstörungsarme Ausbaupfade entscheidend; sie werden selten ausreichend modelliert.
- **Datenüberfrachtung**: IFC-Dateien können unübersichtlich werden, wenn alle ReUse-Informationen als freie Properties abgelegt werden.
- **Versionsmanagement**: Ein Modell kann viele Stände haben; Bauteil_IDs und Passdaten müssen unabhängig davon konsistent bleiben.
- **Rechts- und Qualitätsnachweise**: IFC transportiert Referenzen, ersetzt aber keine Prüfungen, Zulassungen oder Haftungsentscheidungen.
- **Semantische Harmonisierung**: Ohne kontrollierte Vokabulare, bSDD oder Data Templates bleiben gleich benannte Properties oft unterschiedlich gemeint.

## Quellen

- buildingSMART Technical: Industry Foundation Classes (IFC) – Introduction. https://technical.buildingsmart.org/standards/ifc/
- buildingSMART Technical: IFC Schema Specifications Database, IFC 4.3 ADD2 / ISO 16739-1:2024. https://technical.buildingsmart.org/standards/ifc/ifc-schema-specifications/
- buildingSMART Technical: IFC Formats. https://technical.buildingsmart.org/standards/ifc/ifc-formats/
- buildingSMART: Information Delivery Specification (IDS). https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids/
- buildingSMART: IFC Validation Service. https://www.buildingsmart.org/users/services/validation-service/
- buildingSMART: buildingSMART Data Dictionary (bSDD). https://www.buildingsmart.org/users/services/buildingsmart-data-dictionary/
- ISO 16739-1:2024, Industry Foundation Classes (IFC) for data sharing in the construction and facility management industries. https://www.iso.org/standard/84123.html
- ISO 12006-2:2015, Framework for classification. https://www.iso.org/standard/61753.html
- ISO 23386:2020, Methodology to describe, author and maintain properties in interconnected data dictionaries. https://www.iso.org/standard/75401.html
- ISO 23387:2020, Data templates for construction objects used in the life cycle of built assets. https://www.iso.org/standard/75403.html
