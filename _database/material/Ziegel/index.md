---
id: "Ziegel"
entity: "material"
build_status: "clean_phase20"
title: "Dachziegel"
---
# Dachziegel

## Clean Node

- Final path: _database/material/Ziegel
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/bauteiltyp/Dachziegel
  - Action: split_to_clean_targets
  - Status: CONFIDENT
  - Reason: Roof tile is roof component plus brick/clay material.

- Source: _graph/bauteiltyp/Ziegel
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Ziegel is primarily what something is made of; component cases use `bauteiltyp/Mauerstein_Block` plus raw label.

