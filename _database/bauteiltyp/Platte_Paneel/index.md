---
id: "Platte_Paneel"
entity: "bauteiltyp"
build_status: "clean_phase20"
title: "Blechpaneel"
---
# Blechpaneel

## Clean Node

- Final path: _database/bauteiltyp/Platte_Paneel
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/bauteiltyp/Blechpaneel
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Panel is component type; broad `Metall` should stay out unless the exact metal is known.

- Source: _graph/bauteiltyp/Platte_Paneel
  - Action: keep_default
  - Status: CONFIDENT
  - Reason: Folder is included in clean ontology and node has no conflict-specific normalization rule.

