---
id: "Keramik"
entity: "material"
build_status: "clean_phase20"
title: "Keramik"
---
# Keramik

## Clean Node

- Final path: _database/material/Keramik
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/material/Keramik
  - Action: keep_or_merge
  - Status: CONFIDENT
  - Reason: Correct material class.

- Source: _graph/material/Sanitarkeramik
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Sanitary ceramic is material subtype; component should be `bauteiltyp/Sanitaerobjekt`.

