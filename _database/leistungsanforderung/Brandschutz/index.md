---
id: "Brandschutz"
entity: "leistungsanforderung"
build_status: "clean_phase20"
title: "Feuerschuetztuer"
---
# Feuerschuetztuer

## Clean Node

- Final path: _database/leistungsanforderung/Brandschutz
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/bauteiltyp/Feuerschutztuer
  - Action: split_to_clean_targets
  - Status: CONFIDENT
  - Reason: It is a door with fire-safety requirement, not a separate top-level component family.

- Source: _graph/leistungsanforderung/Brandschutz
  - Action: keep_default
  - Status: CONFIDENT
  - Reason: Folder is included in clean ontology and node has no conflict-specific normalization rule.

