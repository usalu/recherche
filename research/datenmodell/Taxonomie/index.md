---
entity: "datenmodell"
id: "Taxonomie"
title: "Taxonomie"
build_status: "promoted_phase42"
legacy_paths:
  - "datenmodell\Taxonomie.md"
node_kind: "knot"
legacy_type: "Datenmodell"
---

# Taxonomie

# Taxonomie

## Verknüpfungen

**Übergeordnete Themen**
- Wissensordnung, Navigation, kontrollierte Vokabulare, Tags, Bauteilkataloge und Materialdatenbanken
- Grundlage für Klassifikation, Ontologie, Suchfilter, Dataview-Auswertungen und Marktplatzkategorien
- Strukturierung von ReUse-relevanten Begriffen entlang Gebäude, Bauteil, Material, Zustand, Logistik und Anschlussnutzung

**Verwandte Dateien**
- `datenmodell/Klassifikation.md`
- `datenmodell/Ontologie.md`
- `datenmodell/Bauteil_ID.md`
- `datenmodell/IFC.md`
- `datenmodell/Materialpass_Schema.md`
- `werkzeug/Obsidian.md`, `werkzeug/Dataview.md`, `werkzeug/Materialdatenbank.md`, `werkzeug/BIM.md`, `werkzeug/Concular_Plattform.md`, `werkzeug/Madaster_Plattform.md`
- `dokument/`: Bauteilkataloge, Materialpässe, Rückbauaudits, Fotos, Prüfberichte
- `logistik/`: Lagerzonen, Packeinheiten, Transportstatus, Demontagephasen
- `kennwert/`: Zustandsklassen, Materialfraktionen, CO₂-Kennwerte, Restwerte, Datenqualitätsstufen
- `meta/`: Tag-Regeln, Vokabularpflege, Synonyme, Versionierung, Mapping

**Relevante Akteure / Fallstudien / Materialien / Standards / Methoden**
- ReUse-Repo-Pflege, BIM-Koordination, Materialpass- und Marktplatzbetreiber, Rückbauteams, Forschungsteams
- SKOS, ISO 12006-2, bSDD, IFC, Uniclass, OmniClass, eClass, DGNB-Gebäuderessourcenpass, BAMB

## Kurzdefinition

Eine **Taxonomie** ist eine geordnete, meist hierarchische Struktur von Begriffen oder Kategorien. Sie beantwortet die Frage: „Wie sortieren wir unser Wissen, damit Menschen und Tools es wiederfinden?“ Im ReUse-Kontext kann eine Taxonomie Bauteile, Materialien, Zustände, Demontagearten, Logistikstatus oder Anschlussnutzungen ordnen.

Taxonomie ist nicht dasselbe wie Klassifikation oder Ontologie:
- **Taxonomie**: Hierarchie und Navigation von Begriffen.
- **Klassifikation**: Zuordnung konkreter Objekte zu Klassen eines Systems.
- **Ontologie**: formales Beziehungsmodell mit Semantik, Relationen und Regeln.

## Relevanz für Wiederverwendung im Bauwesen

Ein ReUse-Repo wächst schnell: Werkzeuge, Fallstudien, Materialien, Normen, Bauteile, Kennwerte, Prozesswissen und Dokumente kommen aus unterschiedlichen Quellen. Ohne Taxonomie entstehen unkontrollierte Tags, Synonyme, Mehrfachablagen und Suchverluste. Eine gute Taxonomie ist deshalb kein akademisches Ordnungsdetail, sondern operative Infrastruktur.

Sie unterstützt:

- **Auffindbarkeit**: Bauteile und Wissen werden über konsistente Kategorien gefunden.
- **Vergleichbarkeit**: Ähnliche Objekte werden unter denselben Begriffen abgelegt.
- **Dataview-/Datenbank-Auswertung**: Tags und Felder lassen sich zuverlässig aggregieren.
- **Marktplatzfähigkeit**: Angebote und Gesuche nutzen gleiche Suchachsen.
- **Lernfähigkeit des Repos**: Neue Quellen können in bestehende Strukturen eingeordnet werden.
- **Interoperabilität**: Lokale Begriffe lassen sich später auf IFC, bSDD oder externe Klassifikationen mappen.

## Fachinhalt

### Grundprinzipien einer guten ReUse-Taxonomie

- **Ein Zweck pro Taxonomiebaum**: Bauteiltyp, Material, Zustand und Logistikstatus nicht in eine einzige Hierarchie mischen.
- **Stabile IDs**: Begriffe brauchen stabile Codes, nicht nur sichtbare Labels.
- **Klare Definitionen**: Jede Kategorie sollte kurz definieren, was eingeschlossen und ausgeschlossen ist.
- **Synonyme verwalten**: „Wiederverwendung“, „Reuse“, „Re-Use“ und „Weiterverwendung“ sollten gemappt, aber nicht beliebig gemischt werden.
- **Mehrsprachigkeit vorbereiten**: Deutsch/Englisch ist im Bau- und Forschungsbereich häufig nötig.
- **Versionierung**: Änderungen an Kategorien müssen nachvollziehbar bleiben.
- **Nicht zu tief starten**: Eine Taxonomie darf wachsen; zu frühe Feingliederung führt zu Inkonsistenz.
- **Mappbar bleiben**: Lokale Kategorien sollten externe Systeme referenzieren können.
- **Unsicherheit zulassen**: „unbekannt“, „prüfen“, „nicht zugeordnet“ sind notwendige Kategorien im Bestand.

### Empfohlene Taxonomieachsen für ReUse

#### 1. Bauteil- und Gebäudebereich

```text
bauwerk
├── tragwerk
│   ├── stütze
│   ├── träger
│   ├── decke
│   └── wand_tragend
├── hülle
│   ├── fassade
│   ├── fenster
│   ├── dach
│   └── abdichtung
├── ausbau
│   ├── tür
│   ├── bodenbelag
│   ├── deckenbekleidung
│   ├── wandbekleidung
│   └── einbaumöbel
├── tga
│   ├── leuchte
│   ├── heizkörper
│   ├── lüftungskomponente
│   └── sanitärobjekt
└── außenraum
    ├── belag
    ├── einfassung
    └── ausstattung
```

#### 2. Materialfamilie

```text
material
├── mineralisch
│   ├── beton
│   ├── ziegel
│   ├── naturstein
│   └── keramik
├── metall
│   ├── stahl
│   ├── edelstahl
│   ├── aluminium
│   └── kupfer
├── biobasiert
│   ├── vollholz
│   ├── holzwerkstoff
│   └── kork
├── glas
├── kunststoff
├── gips
├── dämmstoff
└── verbundmaterial
```

#### 3. ReUse-Status

```text
reuse_status
├── potenzial_erfasst
├── zu_pruefen
├── technisch_geprueft
├── freigegeben
├── eingeschraenkt_nutzbar
├── reserviert
├── ausgebaut
├── gelagert
├── angeboten
├── verkauft
├── wiederverbaut
└── ausgeschieden
```

#### 4. Zustand

```text
zustand
├── A_neuwertig_sehr_gut
├── B_gebrauchsfähig_leicht_abgenutzt
├── C_reparatur_refurbishment_noetig
├── D_stark_beschaedigt_nur_materialnutzung
└── unbekannt_pruefen
```

#### 5. Demontierbarkeit

```text
demontierbarkeit
├── zerstoerungsfrei
├── zerstoerungsarm
├── teilweise_zerstoerend
├── zerstoerend
└── unbekannt
```

#### 6. Anschlussnutzung

```text
anschlussnutzung
├── direkte_wiederverwendung
├── wiederverwendung_nach_pruefung
├── reparatur_refurbishment
├── upcycling
├── ersatzteil
├── materialrecycling
├── energetische_verwertung
└── deponie_vermeiden
```

#### 7. Datenqualität

```text
datenqualitaet
├── gemessen_geprueft
├── gemessen_ungeprueft
├── aus_modell_abgeleitet
├── aus_plan_abgeleitet
├── geschaetzt
└── unbekannt
```

### Taxonomie im Repo

Für ein Obsidian-/Markdown-orientiertes Repo kann die Taxonomie in Frontmatter, Tags oder kontrollierten Feldern genutzt werden. Empfehlung:

```yaml
tags:
  - datenmodell
  - reuse
  - materialpass
reuse_taxonomy:
  bauteilbereich: "ausbau.tuer"
  materialfamilie: "biobasiert.holzwerkstoff"
  reuse_status: "freigegeben"
  zustand: "B_gebrauchsfähig_leicht_abgenutzt"
  demontierbarkeit: "zerstoerungsarm"
  datenqualitaet: "gemessen_geprueft"
```

Wichtig ist, freie Tags nicht mit kontrollierten Taxonomiefeldern zu verwechseln. Freie Tags sind gut für Notizen und Suchbarkeit; belastbare Auswertung braucht kontrollierte Werte.

### SKOS als Publikationsform

SKOS ist ein W3C-Standard zur Darstellung kontrollierter Vokabulare, Thesauri, Klassifikationsschemata und Taxonomien als Linked Data. Für ein ReUse-Repo kann SKOS später genutzt werden, um lokale Taxonomiebegriffe mit externen Begriffen zu verknüpfen:

- `skos:prefLabel`: bevorzugte Bezeichnung
- `skos:altLabel`: Synonyme
- `skos:broader` / `skos:narrower`: Ober-/Unterbegriffe
- `skos:exactMatch`, `skos:closeMatch`, `skos:broadMatch`: Mapping zu externen Systemen
- `skos:definition`: Definition

### Verhältnis zu Klassifikation

Eine Taxonomie kann intern wachsen und arbeitspraktisch sein. Eine Klassifikation ist stärker formalisiert, oft normiert oder extern veröffentlicht. Beispiel:

```yaml
local_taxonomy: "ausbau.tuer.innentuer"
classification:
  - system: "IFC"
    code: "IfcDoor"
  - system: "externe Klassifikation"
    code: "..."
```

Die lokale Taxonomie darf einfacher sein, sollte aber auf externe Systeme mappbar bleiben.

### Verhältnis zu Ontologie

Eine Taxonomie sagt: „Innentür ist engerer Begriff von Tür.“ Eine Ontologie kann zusätzlich sagen:

- Eine Innentür ist Teil eines Türsystems.
- Ein Türsystem kann Beschläge, Zarge, Türblatt und Dichtung enthalten.
- Eine Innentür kann einen Brandschutznachweis benötigen, wenn sie in bestimmter Nutzung eingesetzt wird.
- Eine Innentür mit Zustand C kann eine Reparaturmaßnahme erfordern.

Taxonomie ist daher ein guter Einstieg; Ontologie ist die Erweiterung für komplexe Beziehungen.

## Praxisbezug / Beispiele

### Beispiel 1: Bauteilkatalog in Obsidian

Alle Bauteile erhalten kontrollierte Felder für `bauteilbereich`, `materialfamilie`, `reuse_status`, `zustand` und `datenqualitaet`. Dataview-Abfragen können dann zeigen:

- alle freigegebenen Türen aus Holzwerkstoff,
- alle Bauteile mit unbekanntem Schadstoffstatus,
- alle Objekte mit Zustand A/B und Verfügbarkeit innerhalb eines Rückbauabschnitts,
- alle Datensätze mit geringer Datenqualität, die vor Marktplatzexport geprüft werden müssen.

### Beispiel 2: Marktplatzfilter

Ein ReUse-Marktplatz braucht einfache Suchfilter. Die Taxonomie liefert Kategorien wie „Fenster“, „Türen“, „Bodenbeläge“, „Sanitärobjekte“. Die Material- und Zustandsachsen liefern zusätzliche Filter. Ohne Taxonomie wird die Suche von Freitexten abhängig und verliert relevante Bauteile.

### Beispiel 3: Rückbauplanung

Für Rückbauabschnitte können Bauteile nach Demontierbarkeit, Schadstoffstatus und Lagerfähigkeit gruppiert werden. Eine Taxonomie unterstützt die Priorisierung: zuerst leicht demontierbare, hochwertige, schadstoffunkritische Bauteile sichern; später Materialströme bündeln.

### Beispiel 4: Wissenssammlung im Forschungsrepo

Nicht nur Bauteile, sondern auch Quellen, Methoden und Fallstudien können taxonomisch geordnet werden: `methode.bestandsaufnahme`, `werkzeug.materialpass`, `fallstudie.urban_mining`, `standard.ifc`, `kennwert.gwp`. Dadurch werden Rechercheergebnisse wiederauffindbar.

## Herausforderungen / offene Fragen

- **Überhierarchisierung**: Zu tiefe Bäume werden nicht konsistent benutzt.
- **Mehrfachzugehörigkeit**: Ein Objekt kann zu mehreren Kategorien passen; Taxonomien müssen Facetten statt nur einen Baum erlauben.
- **Lokale Begriffe**: Baustellen- und Plattformbegriffe unterscheiden sich von Normbegriffen.
- **Synonyme und Schreibweisen**: Unkontrollierte Tags erzeugen Varianten wie `reuse`, `re-use`, `wiederverwendung`, `Wiederverwendung`.
- **Grenze zu Klassifikation**: Eine Taxonomie kann informell bleiben; für Austausch und Nachweis braucht es oft formale Klassifikation.
- **Grenze zu Ontologie**: Hierarchien reichen nicht, um Materialzusammensetzung, Prüfstatus, Rechte, Logistik und Anschlussnutzung vollständig zu beschreiben.
- **Versionierung**: Wenn Kategorien umbenannt oder verschoben werden, dürfen alte Datensätze nicht unverständlich werden.
- **Pflegeverantwortung**: Ohne klare Rollen verwildert die Taxonomie schnell.

## Quellen

- W3C: SKOS Simple Knowledge Organization System Reference. https://www.w3.org/TR/skos-reference/
- ISO 12006-2:2015, Framework for classification. https://www.iso.org/standard/61753.html
- ISO 12006-3:2022, Framework for object-oriented information. https://www.iso.org/standard/74932.html
- buildingSMART: buildingSMART Data Dictionary (bSDD). https://www.buildingsmart.org/users/services/buildingsmart-data-dictionary/
- buildingSMART Technical: IFC. https://technical.buildingsmart.org/standards/ifc/
- BAMB: Framework for Materials Passports. https://www.bamb2020.eu/wp-content/uploads/2018/01/Framework-for-Materials-Passports-for-the-webb.pdf
- DGNB: Building Resource Passport / Gebäuderessourcenpass. https://www.dgnb.de/en/sustainable-building/circular-building/building-resource-passport
- NBS: Uniclass. https://www.thenbs.com/our-tools/uniclass
- Construction Specifications Institute: OmniClass. https://www.csiresources.org/standards/omniclass
- eClass Standard. https://eclass.eu/
