---
id: "Dach"
entity: "bauteiltyp"
build_status: "clean_phase20"
title: "Dach"
---
# Dach

## Clean Node

- Final path: _database/bauteiltyp/Dach
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/bauteiltyp/Dach
  - Action: keep_default
  - Status: CONFIDENT
  - Reason: Folder is included in clean ontology and node has no conflict-specific normalization rule.

- Source: _graph/bauteiltyp/Dachziegel
  - Action: split_to_clean_targets
  - Status: CONFIDENT
  - Reason: Roof tile is roof component plus brick/clay material.

- Source: _graph/bauteiltyp/Vordach_Ueberdachung
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Canopy/covering is roof-family component.

