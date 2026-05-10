---
id: "Metall"
entity: "material"
build_status: "clean_phase20"
title: "Metall"
---
# Metall

## Clean Node

- Final path: _manual_review/nodes/material/Metall
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/material/Metall
  - Action: manual_review
  - Status: REVIEW_REQUIRED
  - Reason: Broad fallback when exact metal is unknown; prefer Stahl/Aluminium when known.

## Review Recommendation

- Recommendation: keep out of clean database until final manual approval.
- Reason: `Metall` is too broad as a clean material knot.
- Clean mapping rule: use exact known materials such as `material/Stahl`, `material/Aluminium`, `material/Glas`, `material/Holz`, `material/Keramik`, or `material/Kunststoff`.
- Edge review note: see `_migration/28_material_metall_edge_review_decisions.csv`.
