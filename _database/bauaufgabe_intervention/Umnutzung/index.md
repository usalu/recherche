---
id: "Umnutzung"
entity: "bauaufgabe_intervention"
build_status: "clean_phase20"
title: "Umnutzung"
---
# Umnutzung

## Clean Node

- Final path: _database/bauaufgabe_intervention/Umnutzung
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/bauaufgabe_intervention/Umnutzung
  - Action: keep_or_merge
  - Status: CONFIDENT
  - Reason: Correct strongest type. Merge strategy content here.

- Source: _graph/reuse_strategie/Umnutzung
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Umnutzung is a building intervention/use change, not component-level reuse strategy.

