---
id: "Mauerstein_Block"
entity: "bauteiltyp"
build_status: "clean_phase20"
title: "Betonblock"
---
# Betonblock

## Clean Node

- Final path: _database/bauteiltyp/Mauerstein_Block
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/bauteiltyp/Betonblock
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: A concrete block is a block component; keep `material/Beton` as separate fact.

- Source: _graph/bauteiltyp/Mauerstein_Block
  - Action: keep_or_merge
  - Status: CONFIDENT
  - Reason: Correct component family for brick/block units; material is linked separately.

