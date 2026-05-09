---
id: "Klimaschutz_Konfigurator"
entity: "software_digitaltool"
node_kind: "core"
migration_status: "migrated_phase3_core_entities"
title: "Klimaschutz Konfigurator"
source_count: 2
legacy_paths:
  - "software\\klimaschutz-konfigurator\\index.md"
  - "werkzeug\\Klimaschutz_Konfigurator.md"
raw_targets:
  - "software_digitaltool/klimaschutz_konfigurator"
migration_actions:
  - "move_as_core"
  - "semantic_move"
risk_flags:
  - "may_duplicate_bauteilboerse_or_akteur"
  - "nested_index_is_content_node_not_category_index"
---
# Klimaschutz Konfigurator

## Migration

- Canonical target: software_digitaltool/Klimaschutz_Konfigurator
- Legacy source count: 2
- Semantic note: Digitales Werkzeug oder Plattform. Bauteilboersen werden hier als Plattformprofile gefuehrt, nicht als eigene Entitaet.

## Legacy Content

### Legacy Source: werkzeug\Klimaschutz_Konfigurator.md

- Map action: semantic_move
- Target role in map: primary
- Raw mapped target: software_digitaltool/Klimaschutz_Konfigurator
- Original primary target: software_digitaltool/Klimaschutz_Konfigurator
- Original secondary targets: 

---
type: Werkzeug
name: Klimaschutz-Konfigurator
homepage: https://www.nachhaltig-bauen-mit-beton.de/klimaschutz-konfigurator
---

### Legacy Source: software\klimaschutz-konfigurator\index.md

- Map action: move_as_core
- Target role in map: primary
- Raw mapped target: software_digitaltool/klimaschutz_konfigurator
- Original primary target: software_digitaltool/klimaschutz_konfigurator
- Original secondary targets: 

---
type: Software
name: Klimaschutz-Konfigurator
homepage: https://www.nachhaltig-bauen-mit-beton.de/klimaschutz-konfigurator
---
