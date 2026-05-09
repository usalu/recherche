---
id: "Moebel_Dekoration_Nicht_Direct_Reuse"
entity: "bewertungslogik_abgrenzung"
build_status: "clean_phase20"
title: "Moebel"
---
# Moebel

## Clean Node

- Final path: _database/bewertungslogik_abgrenzung/Moebel_Dekoration_Nicht_Direct_Reuse
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/bauteiltyp/Moebel
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Furniture should not be counted as construction-component direct reuse unless explicitly scoped.

- Source: _graph/bewertungslogik_abgrenzung/Moebel_Dekoration_Nicht_Direct_Reuse
  - Action: keep_default
  - Status: CONFIDENT
  - Reason: Folder is included in clean ontology and node has no conflict-specific normalization rule.

