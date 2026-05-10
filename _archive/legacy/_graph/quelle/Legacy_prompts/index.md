---
id: "Legacy_prompts."
entity: "quelle"
node_kind: "source"
migration_status: "migrated_phase5_legacy_source"
title: "Prompts"
legacy_path: "prompts.md"
migration_action: "archive_as_source"
legacy_type: ""
target_primary: "meta_or_90_import_rohdaten/prompts"
target_secondary: ""
risk_flags: ""
---
# Prompts

## Migration

- Legacy path: prompts.md
- Action in migration map: archive_as_source
- Reason: not already consumed by phase 1-4, so preserved as source/meta node.
- Original primary target: meta_or_90_import_rohdaten/prompts
- Original secondary targets: 

## Legacy Content

# Prompts

---

Erstellen Sie einen Baum von Themen, nur Namen keine Beschreibung zu allen themen die das Notebook umfasst.

---

Welche konstruktiven Verbindungen gibt es, um wiederverwendete Stahlbetonteile zu fügen?

---

Erstellen Sie einen Baum von Themen, nur Namen keine Beschreibung zu allen themen die das Notebook umfasst.

---

```
1.

Analysieren Sie das Software-Ecosystem SOFTWARE (LINK).

2.

Finden Sie alle Quellen zu Features, Handbücher, Tutorials, Videos, Beispiele, etc.

3.

Finden Sie alle Architektur und Ingenieurbüros, welche dieses Tool verwenden und welche Gebäude mit diesem Tool nachweislich verwendet wurde.
```

---

```
1.

Analysieren Sie die NORM (LINK) im Detail.

2.

Finden Sie alle Quellen zu Features, Handbücher, Tutorials, Videos, Beispiele, etc.

3.

Finden Sie alle Architektur und Ingenieurbüros, welche dieses Tool verwenden und welche Gebäude mit diesem Tool nachweislich verwendet wurde.
```

---

Erstellen Sie einen Bericht mit den

---

resource
bericht
abschlussbericht
paper
aufbereitungsmethode
gebäude
fallstudie
element
pavillon
hürde

material
verbindung

gebäude -- bericht
gebäude -- aufbereitungsmethode
aufbereitungsmethode -- elementart

thema
berichte
material
organization - buro - institute - research
aufbereitungsmethode
prüfverfahren
büro

organization
projects and case study
platforms and tools
guidelines and standards
methods
workflow steps
challenges and bottlenecks
metadata fields and data requirements
actor roles

source Layer : websites
project pages
reports
PDFs
slide decks
funding applications
internal project documents
guidelines
case study pages
later : interview transcripts and workshop material

```mermaid
erDiagram
resource ||--o{ bericht : places
bericht ||--|{ paper : contains
paper ||--o{ paper_item : includes
resource {
    string id
    string name
    string email
}
ORDER {
    string id
    date orderDate
    string status
}
PRODUCT {
    string id
    string name
    float price
}
ORDER_ITEM {
    int quantity
    float price
}
```
