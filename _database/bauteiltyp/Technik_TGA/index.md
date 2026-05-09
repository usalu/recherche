---
id: "Technik_TGA"
entity: "bauteiltyp"
build_status: "clean_phase20"
title: "Heizkoerper"
---
# Heizkoerper

## Clean Node

- Final path: _database/bauteiltyp/Technik_TGA
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/bauteiltyp/Heizkoerper
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Radiator is TGA component; keep exact raw label.

- Source: _graph/bauteiltyp/Schacht
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: Shaft is service/technical infrastructure component in this schema.

- Source: _graph/bauteiltyp/TGA_Element
  - Action: move_to_clean_target
  - Status: CONFIDENT
  - Reason: TGA_Element is a generic technical-building-services component.

