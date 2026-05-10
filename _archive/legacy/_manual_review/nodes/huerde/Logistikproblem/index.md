---
id: "Logistikproblem"
entity: "huerde"
build_status: "clean_phase20"
title: "Logistikproblem"
---
# Logistikproblem

## Clean Node

- Final path: _manual_review/nodes/huerde/Logistikproblem
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/huerde/Logistikproblem
  - Action: manual_review
  - Status: REVIEW_REQUIRED
  - Reason: Correct broad barrier when exact logistics issue is unknown.

## Review Recommendation

- Recommendation: keep out of clean database until final manual approval.
- Reason: `Logistikproblem` is a broad fallback, not a clean analytical hurdle.
- Clean mapping rule: split case by case into concrete barriers such as `huerde/Fehlende_Lagerflaeche`, `huerde/Verfuegbarkeitsproblem`, `huerde/Terminunsicherheit`, `huerde/Toleranzen`, `huerde/Kompatibilitaetsproblem`, or `huerde/Bruch_Beschaedigungsrisiko`.
- Edge review note: see `_migration/32_huerde_logistikproblem_edge_review_decisions.csv`.
