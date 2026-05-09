---
id: "Dachtragwerk"
entity: "tragwerkstyp"
build_status: "clean_phase20"
title: "Dachtragwerk"
---
# Dachtragwerk

## Clean Node

- Final path: _database/tragwerkstyp/Dachtragwerk
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/bauteiltyp/Dachtragwerk
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: A roof structure is a structural type/system, not a simple component type.

- Source: _graph/tragwerkstyp/Dachtragwerk
  - Action: keep_or_merge
  - Status: CONFIDENT
  - Reason: Correct strongest type. Merge bauteiltyp content here.

