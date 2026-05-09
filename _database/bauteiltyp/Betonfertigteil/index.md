---
id: "Betonfertigteil"
entity: "bauteiltyp"
build_status: "clean_phase20"
title: "Betonfertigteil"
---
# Betonfertigteil

## Clean Node

- Final path: _database/bauteiltyp/Betonfertigteil
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/bauteiltyp/Betonfertigteil
  - Action: keep_default
  - Status: CONFIDENT
  - Reason: Folder is included in clean ontology and node has no conflict-specific normalization rule.

- Source: _graph/material/Beton_Fertigteile
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Betonfertigteile are component/product types, not material; material stays `Beton` or `Stahlbeton`.

