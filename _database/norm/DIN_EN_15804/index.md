---
id: "DIN_EN_15804"
entity: "norm"
build_status: "clean_phase20"
title: "DIN EN 15804"
---
# DIN EN 15804

## Clean Node

- Final path: _database/norm/DIN_EN_15804
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/norm/DIN_EN_15804
  - Action: keep_or_merge
  - Status: CONFIDENT
  - Reason: Actual named standard.

- Source: _graph/norm/EN_15804
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Duplicate standard family in this German-context dataset; keep as alias.

