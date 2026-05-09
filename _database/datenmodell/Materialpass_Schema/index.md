---
id: "Materialpass_Schema"
entity: "datenmodell"
build_status: "clean_phase20"
title: "Madaster â€” vertieftes Forschungsdossier"
---
# Madaster â€” vertieftes Forschungsdossier

## Clean Node

- Final path: _database/datenmodell/Materialpass_Schema
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/datenmodell/Materialpass
  - Action: merge_to_clean_target
  - Status: CONFIDENT
  - Reason: `Materialpass` alone should be document; data-model node should be the schema.

- Source: _graph/datenmodell/Materialpass_Schema
  - Action: keep_or_merge
  - Status: CONFIDENT
  - Reason: Correct data model/schema node.

