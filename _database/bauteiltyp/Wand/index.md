---
id: "Wand"
entity: "bauteiltyp"
build_status: "clean_phase20"
title: "Innenwand"
---
# Innenwand

## Clean Node

- Final path: _database/bauteiltyp/Wand
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/bauteiltyp/Innenwand
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Interior wall is a wall subtype; keep interior use as raw label.

- Source: _graph/bauteiltyp/Tragende_Wand
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Component type is wall; add `tragwerksprinzip/Wandtragwerk` when structural role matters.

- Source: _graph/bauteiltyp/Wand
  - Action: keep_default
  - Status: CONFIDENT
  - Reason: Folder is included in clean ontology and node has no conflict-specific normalization rule.

