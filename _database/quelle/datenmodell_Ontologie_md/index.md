---
entity: "quelle"
id: "datenmodell_Ontologie_md"
title: "datenmodell_Ontologie_md"
build_status: "promoted_phase42"
source_filename: "Ontologie.md"
legacy_type: "Datenmodell"
---

# datenmodell_Ontologie_md

## Verknüpfungen

**Übergeordnete Themen**
- Semantische Datenmodellierung, Linked Data, Wissensgraphen, digitale Gebäudemodelle
- Integration von BIM, Materialpässen, Dokumenten, Kennwerten, Rückbau- und Logistikdaten
- Maschinenlesbare Bedeutung von Klassen, Eigenschaften, Beziehungen und Regeln

**Verwandte Dateien**
- `datenmodell/Taxonomie.md`
- `datenmodell/Klassifikation.md`
- `datenmodell/IFC.md`
- `datenmodell/Bauteil_ID.md`
- `datenmodell/Materialpass_Schema.md`
- `werkzeug/BIM.md`, `werkzeug/IFC_Viewer.md`, `werkzeug/Materialdatenbank.md`, `werkzeug/Dataview.md`, `werkzeug/Obsidian.md`
- `dokument/`: Nachweise, Prüfdokumente, Herkunft, EPDs, Rückbauanleitungen, Fotos
- `logistik/`: Ausbauprozess, Lagerorte, Transporte, Packeinheiten, Statusereignisse
- `kennwert/`: LCA-Werte, Masse, Zustand, Restwert, Risiko, Verfügbarkeit
- `meta/`: kontrollierte Begriffe, Datenqualität, Mapping, SHACL-Regeln, Governance

**Relevante Akteure / Fallstudien / Materialien / Standards / Methoden**
- W3C RDF, OWL, SHACL, SKOS, JSON-LD
- BOT (Building Topology Ontology), ifcOWL, Brick Schema, SAREF, schema.org als mögliche Bezugspunkte
- buildingSMART, bSDD, IFC, IDS, ISO 12006-3, ISO 23386/23387
- Datenarchitektur, BIM-Management, Forschungsprojekte zu Linked Building Data und Urban Mining

## Kurzdefinition

Eine **Ontologie** ist ein formales, maschinenlesbares Modell von Begriffen und Beziehungen in einem Wissensbereich. Sie beschreibt nicht nur Klassen wie „Bauteil“, „Material“ oder „Gebäude“, sondern auch Eigenschaften und Relationen: Ein Bauteil *besteht aus* Material, *befindet sich in* einem Raum, *hat* einen Zustand, *wurde ausgebaut aus* einem Gebäude, *besitzt* einen Prüfbericht und *ist geeignet für* eine Anschlussnutzung.

Im ReUse-Kontext ist eine Ontologie die semantische Integrationsschicht zwischen heterogenen Datenquellen. Sie kann erklären, welche Begriffe gleich, ähnlich, enger oder weiter gefasst sind, und sie kann Beziehungen auswertbar machen, die in Tabellen oder IFC-Properties allein schwer konsistent abzubilden sind.

## Relevanz für Wiederverwendung im Bauwesen

Wiederverwendung ist ein Beziehungsproblem: Ein Bauteil ist nur dann wiederverwendbar, wenn Material, Zustand, Maße, technische Leistung, Schadstoffstatus, Demontage, Verfügbarkeit, Transport, Recht und Nachfrage zusammenpassen. Diese Zusammenhänge sind oft über verschiedene Dateien, Tools und Akteure verteilt.

Eine Ontologie hilft, solche verteilten Informationen zu verbinden:

- **Semantische Integration**: IFC, Materialpass, Bauteil_ID, Klassifikation, Fotos, Prüfberichte und Logistikereignisse können in einem gemeinsamen Graphen referenziert werden.
- **Abfragen über Beziehungen**: „Zeige alle Holzfenster im Gebäude A, Zustand A/B, demontierbar, mit Foto, ohne Schadstoffverdacht und verfügbar vor Juni.“
- **Mapping zwischen Begriffen**: Lokale Begriffe, IFC-Klassen, Plattformkategorien und Klassifikationscodes werden als Beziehungen modelliert.
- **Regelprüfung**: SHACL- oder IDS-nahe Regeln können Pflichtfelder, Wertbereiche und Beziehungen prüfen.
- **Nachvollziehbarkeit**: Provenienz, Datenqualität und Konflikte können feld- oder aussagenbezogen gespeichert werden.
- **Wissensaufbau**: ReUse-Erfahrungen aus Projekten können als wiederverwendbares Wissensnetz dokumentiert werden.

## Fachinhalt

### Abgrenzung zu Taxonomie und Klassifikation

| Konzept | Kernfrage | Beispiel | ReUse-Rolle |
|---|---|---|---|
| Taxonomie | Wie ordnen wir Begriffe hierarchisch? | `Ausbau > Türen > Innentüren` | Navigation, Tag-Struktur, einfache Suche. |
| Klassifikation | Welcher Klasse gehört dieses Objekt an? | Bauteil `btl:123` ist `IfcDoor` und `Innentür` | Filter, Listen, Auswertung, Datenaustausch. |
| Ontologie | Welche Dinge stehen wie in Beziehung? | Tür `btl:123` befindet sich in Raum X, besteht aus Holz, hat Prüfung Y | Integration, Abfragen, Regeln, Schlussfolgerungen. |

### Grundbausteine einer ReUse-Ontologie

#### Klassen / Entitäten

- `Building`, `Site`, `Storey`, `Space`, `Zone`
- `Component`, `Assembly`, `Product`, `Material`, `MaterialFraction`
- `Connection`, `Fastener`, `Layer`, `Finish`
- `ConditionAssessment`, `Damage`, `Test`, `HazardAssessment`
- `Document`, `Photo`, `EPD`, `Certificate`, `InspectionReport`
- `ReuseScenario`, `ReuseOption`, `DismantlingMethod`, `TreatmentProcess`
- `StorageLocation`, `Transport`, `PackagingUnit`, `LogisticsEvent`
- `Actor`, `Organization`, `Role`, `Owner`, `Custodian`
- `Indicator`, `Quantity`, `LCAIndicator`, `CostIndicator`, `RiskIndicator`

#### Beziehungen

- `hasPart` / `isPartOf`
- `locatedIn` / `originatedFrom`
- `madeOf` / `hasMaterialFraction`
- `hasClassification` / `mappedToClass`
- `hasPassport` / `documentedBy`
- `hasConditionAssessment` / `hasDamage`
- `hasTestResult` / `hasHazardStatus`
- `canBeDismantledBy` / `requiresTool`
- `storedAt` / `transportedBy` / `reservedFor`
- `hasReuseOption` / `compatibleWith`
- `hasQuantity` / `hasGWP` / `hasResidualValue`
- `assertedBy` / `derivedFrom` / `validUntil`

#### Eigenschaften

- Identifikatoren: Bauteil_ID, Passport_ID, IFC_GUID, Dokument-ID
- Datumswerte: Erfassung, Prüfung, Ausbau, Lagerung, Verfügbarkeit
- Einheiten: mm, kg, m², m³, kgCO₂e, Euro
- Qualitätswerte: Datenqualität, Konfidenz, Quelle, Methode
- Statuswerte: geprüft, freigegeben, reserviert, verkauft, wiederverbaut

### Beispielhafte Aussagen als Wissensgraph

```text
btl:000314 rdf:type reuse:Door .
btl:000314 reuse:locatedIn space:A-EG-012 .
btl:000314 reuse:madeOf material:woodBasedPanel .
btl:000314 reuse:hasClassification ifc:IfcDoor .
btl:000314 reuse:hasConditionAssessment assessment:000314-2026-04 .
assessment:000314-2026-04 reuse:conditionGrade "B" .
btl:000314 reuse:documentedBy photo:000314-front .
btl:000314 reuse:hasReuseOption reuse:DirectReuseInterior .
btl:000314 reuse:storedAt storage:Lager2-RegalT04 .
```

Solche Aussagen können über RDF/OWL, JSON-LD oder eine Graphdatenbank gespeichert werden. Für kleinere Repos kann auch eine vereinfachte Tabellen- oder YAML-Struktur sinnvoll sein, solange Relationen explizit geführt werden.

### Beziehung zu IFC und ifcOWL

IFC ist ein reiches objektorientiertes Datenmodell. ifcOWL bildet IFC-Strukturen in OWL/RDF ab und ermöglicht die Nutzung im Linked-Data-Kontext. Für ReUse bedeutet das:

- IFC kann als Quelle für räumliche Struktur, Objekte, Materialien und Mengen dienen.
- ifcOWL kann IFC-Daten mit anderen Linked-Data-Quellen verbinden.
- Eine ReUse-Ontologie sollte IFC nicht komplett nachbauen, sondern IFC-Objekte referenzieren und um ReUse-spezifische Konzepte ergänzen.
- Praktisch ist oft eine schlanke Kernontologie sinnvoller als eine vollständige ifcOWL-Datenkopie.

### Beziehung zu bSDD und Data Templates

bSDD stellt Definitionen von Klassen und Eigenschaften bereit, die in IFC-Modellen und IDS-Anforderungen referenziert werden können. ISO 23386 beschreibt die Methodik zur Definition und Pflege von Eigenschaften in vernetzten Data Dictionaries; ISO 23387 beschreibt Data Templates für Bauobjekte.

Für die Ontologie bedeutet das:

- Begriffe sollten nicht isoliert im Repo definiert werden, wenn es etablierte Definitionen gibt.
- Eigenschaften können auf bSDD-/Data-Dictionary-Definitionen verweisen.
- Data Templates können als strukturierte Mindestanforderungen für bestimmte Klassen dienen.
- Die Ontologie kann Mappings zwischen lokalen Begriffen, IFC, bSDD und Materialpassfeldern speichern.

### Validierung mit SHACL / IDS

Ontologien beschreiben Bedeutung; Validierungsregeln prüfen Daten. Für ReUse sind beide Ebenen nötig.

Beispiele für Regeln:

- Jedes wiederverwendbare Einzelbauteil muss eine Bauteil_ID haben.
- Jedes angebotene Bauteil muss mindestens Zustand, Menge, Foto, Standort und Verfügbarkeit besitzen.
- Ein Bauteil mit Status „freigegeben“ muss eine Prüfaussage oder Freigabequelle besitzen.
- Ein Schadstoffstatus „unbekannt“ darf nicht automatisch als „unbedenklich“ interpretiert werden.
- GWP-Werte müssen Einheit, Quelle, Systemgrenze und Szenario enthalten.

IDS ist näher an IFC-Modellanforderungen; SHACL ist stärker für RDF/Linked-Data-Graphen. Beide können sich ergänzen.

## Praxisbezug / Beispiele

### Beispiel 1: Semantische Suche im Bauteilkatalog

Eine einfache Liste findet nur Objekte mit exakt dem Wort „Fenster“. Eine Ontologie kann auch Elemente finden, die als `IfcWindow`, „Holzfenster“, „Kastenfenster“, „window unit“ oder lokale Kategorie `fassade.oeffnung.fenster` eingetragen sind, wenn diese Begriffe gemappt sind.

### Beispiel 2: ReUse-Matching

Ein Entwurfsprojekt sucht 30 m² Innenwandbekleidung mit Holzoberfläche, Zustand A/B, verfügbar innerhalb von 40 km, ohne Schadstoffverdacht. Die Ontologie kann Bauteile, Materialien, Lagerorte, Prüfergebnisse und Mengenbeziehungen zusammen auswerten.

### Beispiel 3: Konfliktmanagement

Ein BIM-Modell nennt ein Bauteil „Aluminiumfenster“, ein Prüfbericht nennt Holz-Aluminium-Verbund, ein Foto zeigt Holzrahmen. Eine Ontologie kann mehrere Aussagen mit Quelle, Datum und Konfidenz speichern, statt eine unsichere Wahrheit zu erzwingen.

### Beispiel 4: Rückbau- und Logistikereignisse

Ein Bauteil kann Ereignisse haben: erfasst, markiert, ausgebaut, gereinigt, geprüft, gelagert, reserviert, transportiert, eingebaut. Als Ontologie oder Wissensgraph lassen sich Ereignisse zeitlich, räumlich und organisatorisch mit dem Objekt verbinden.

## Herausforderungen / offene Fragen

- **Komplexität**: Eine vollständige Ontologie kann mehr Aufwand erzeugen als ein kleines Projekt tragen kann.
- **Tool-Reife**: Viele Planungs- und Rückbauprozesse arbeiten noch mit Tabellen, PDFs und proprietären Plattformen.
- **Governance**: Begriffe, Relationen und Regeln müssen gepflegt, versioniert und dokumentiert werden.
- **Mappingqualität**: Falsche Gleichsetzungen zwischen Klassen sind gefährlicher als fehlende Mappings.
- **Unsicherheit**: Bestandsdaten sind oft lückenhaft; Ontologien müssen Unsicherheit, Quelle und Konfidenz ausdrücken können.
- **Performance und Nutzbarkeit**: Graphmodelle sind mächtig, aber für Baustellen- und Marktplatzprozesse müssen sie einfache Oberflächen speisen.
- **Keine Ersatzprüfung**: Semantische Schlussfolgerungen ersetzen keine technische, rechtliche oder schadstoffbezogene Prüfung.
- **Balance**: Für das Repo ist eine pragmatische Kernontologie mit wenigen stabilen Relationen oft sinnvoller als eine akademisch vollständige Modellwelt.

## Quellen

- W3C: RDF 1.1 Concepts and Abstract Syntax. https://www.w3.org/TR/rdf11-concepts/
- W3C: OWL 2 Web Ontology Language Document Overview. https://www.w3.org/TR/owl2-overview/
- W3C: SHACL – Shapes Constraint Language. https://www.w3.org/TR/shacl/
- W3C: SKOS Simple Knowledge Organization System Reference. https://www.w3.org/TR/skos-reference/
- W3C Linked Building Data Community Group: Building Topology Ontology (BOT). https://w3c-lbd-cg.github.io/bot/
- buildingSMART Technical: IFC Schema Specifications, including OWL/RDF/TTL resources. https://technical.buildingsmart.org/standards/ifc/ifc-schema-specifications/
- buildingSMART: buildingSMART Data Dictionary (bSDD). https://www.buildingsmart.org/users/services/buildingsmart-data-dictionary/
- ISO 12006-3:2022, Framework for object-oriented information. https://www.iso.org/standard/74932.html
- ISO 23386:2020, Methodology to describe, author and maintain properties in interconnected data dictionaries. https://www.iso.org/standard/75401.html
- ISO 23387:2020, Data templates for construction objects used in the life cycle of built assets. https://www.iso.org/standard/75403.html
- Brick Schema. https://brickschema.org/
- SAREF: Smart Applications REFerence ontology. https://saref.etsi.org/
