---
id: "Boden"
entity: "bauteiltyp"
build_status: "clean_phase20"
title: "Bodenbelag"
---
# Bodenbelag

## Clean Node

- Final path: _database/bauteiltyp/Boden
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/bauteiltyp/Bodenbelag
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Floor finish is part of the Boden component family.

- Source: _graph/bauteiltyp/Bodenfliese
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Floor tile is Boden plus material/raw label.

- Source: _graph/bauteiltyp/Pflaster_Bodenplatte
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Paving/floor plates belong to Boden for this ontology; keep exact raw label.

