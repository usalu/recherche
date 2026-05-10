---
id: "Tragstruktur"
entity: "bauteiltyp"
build_status: "clean_phase20"
title: "Tragstruktur"
---
# Tragstruktur

## Clean Node

- Final path: _manual_review/nodes/bauteiltyp/Tragstruktur
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/bauteiltyp/Tragstruktur
  - Action: manual_review
  - Status: REVIEW_REQUIRED
  - Reason: Use only when the source names a structural assembly without precise component or system.

## Review Recommendation

- Recommendation: keep out of clean database until final manual approval.
- Reason: `Tragstruktur` is too broad and not a true `bauteiltyp`.
- Clean mapping rule: derive each case to `tragwerkstyp/*`, `tragwerksprinzip/*`, or a precise component such as `bauteiltyp/Traeger` or `bauteiltyp/Stuetze`.
- Ontology gap note: several rows suggest a possible future clean knot `tragwerkstyp/Stahltragwerk`.
- Edge review note: see `_migration/30_bauteiltyp_tragstruktur_edge_review_decisions.csv`.
