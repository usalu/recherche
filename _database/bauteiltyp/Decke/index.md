---
id: "Decke"
entity: "bauteiltyp"
build_status: "clean_phase20"
title: "Brettsperrholzdecke"
---
# Brettsperrholzdecke

## Clean Node

- Final path: _database/bauteiltyp/Decke
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/bauteiltyp/Brettsperrholzdecke
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Component type is slab/floor/ceiling; `Brettsperrholz` is material.

- Source: _graph/bauteiltyp/Deckenplatte
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Deckenplatte is a specific slab/floor element; broad component type is Decke.

