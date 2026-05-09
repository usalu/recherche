---
id: "Betrieb"
entity: "prozessphase"
build_status: "clean_phase20"
title: "Betrieb und Rueckbauplanung"
---
# Betrieb und Rueckbauplanung

## Clean Node

- Final path: _database/prozessphase/Betrieb
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/prozessphase/Betrieb_und_Rueckbauplanung
  - Action: split_to_clean_targets
  - Status: CONFIDENT
  - Reason: Combines operation and future deconstruction planning; should not stay one phase.

