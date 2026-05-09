---
id: "Traeger"
entity: "bauteiltyp"
build_status: "clean_phase20"
title: "Fachwerktraeger"
---
# Fachwerktraeger

## Clean Node

- Final path: _database/bauteiltyp/Traeger
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/bauteiltyp/Fachwerktraeger
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Component type is beam/girder; `Fachwerk` belongs to structural principle/raw label.

- Source: _graph/bauteiltyp/Pfette
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: A purlin is a beam/member subtype; keep `Pfette` as raw label.

- Source: _graph/bauteiltyp/Traeger
  - Action: keep_default
  - Status: CONFIDENT
  - Reason: Folder is included in clean ontology and node has no conflict-specific normalization rule.

