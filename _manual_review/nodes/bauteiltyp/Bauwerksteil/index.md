---
id: "Bauwerksteil"
entity: "bauteiltyp"
build_status: "clean_phase20"
title: "Bauwerksteil"
---
# Bauwerksteil

## Clean Node

- Final path: _manual_review/nodes/bauteiltyp/Bauwerksteil
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/bauteiltyp/Bauwerksteil
  - Action: manual_review
  - Status: REVIEW_REQUIRED
  - Reason: Whole building parts are object scale, not component type; create bauobjekt/beteiligung if concrete.

## Review Recommendation

- Recommendation: keep out of clean database until final manual approval.
- Reason: `Bauwerksteil` is too broad and often object-scale or system-scale.
- Clean mapping rule: resolve each case to `bauobjekt/*`, `bauobjekt_beteiligung/*`, `tragwerkstyp/*`, `tragwerksprinzip/*`, or a precise `bauteiltyp/*`.
- Edge review note: see `_migration/31_bauteiltyp_bauwerksteil_edge_review_decisions.csv`.
