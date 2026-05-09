---
id: "Stuetze"
entity: "bauteiltyp"
build_status: "clean_phase20"
title: "Brettschichtholzstuetze"
---
# Brettschichtholzstuetze

## Clean Node

- Final path: _database/bauteiltyp/Stuetze
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/bauteiltyp/Brettschichtholzstuetze
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Component type is column; `Brettschichtholz` is material.

- Source: _graph/bauteiltyp/Stuetze
  - Action: keep_default
  - Status: CONFIDENT
  - Reason: Folder is included in clean ontology and node has no conflict-specific normalization rule.

