---
id: "Planung"
entity: "prozessphase"
build_status: "clean_phase20"
title: "Betrieb und Rueckbauplanung"
---
# Betrieb und Rueckbauplanung

## Clean Node

- Final path: _database/prozessphase/Planung
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/prozessphase/Betrieb_und_Rueckbauplanung
  - Action: split_to_clean_targets
  - Status: CONFIDENT
  - Reason: Combines operation and future deconstruction planning; should not stay one phase.

- Source: _graph/prozessphase/Entwurf
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Entwurf is planning/design phase in the canonical process vocabulary.

