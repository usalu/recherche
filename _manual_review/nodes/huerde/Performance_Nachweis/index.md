---
id: "Performance_Nachweis"
entity: "huerde"
build_status: "clean_phase20"
title: "Performance-Nachweis"
---
# Performance-Nachweis

## Clean Node

- Final path: _manual_review/nodes/huerde/Performance_Nachweis
- Build rule: typed path IDs only.

## Imported Staging Nodes

- Source: _graph/huerde/Performance_Nachweis
  - Action: manual_review
  - Status: REVIEW_REQUIRED
  - Reason: Barrier is missing/uncertain proof, not the proof type itself.

## Review Recommendation

- Recommendation: keep out of clean database until final manual approval.
- Reason: `Performance_Nachweis` mixes barrier, proof/check, and performance requirement levels.
- Clean mapping rule: split case by case into concrete targets such as `huerde/Gewaehrleistung`, `huerde/Technische_Freigabe`, `huerde/Datenluecke`, `huerde/Hygieneanforderung`, `leistungsanforderung/*`, or `pruefung_nachweis/*`.
- Edge review note: see `_migration/29_huerde_performance_nachweis_edge_review_decisions.csv`.
