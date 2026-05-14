# Phase 33 First Manual Batch Recommendation Summary

## Scope

Prepared the five highest-impact manual-review nodes.

No clean database nodes or clean edges were added. Final manual decisions are deferred until the full review package is ready.

## Node Recommendations

| node | recommendation | reason |
|---|---|---|
| `material/Metall` | keep in review until final approval | Too broad as a material knot; exact materials already cover known parts where possible. |
| `huerde/Performance_Nachweis` | keep in review until final approval | Mixes barrier, proof/check, and performance requirement levels. |
| `bauteiltyp/Tragstruktur` | keep in review until final approval | Not a true component type; derive to structural type/principle/component case by case. |
| `bauteiltyp/Bauwerksteil` | keep in review until final approval | Usually object-scale or system-scale, not a reusable component family. |
| `huerde/Logistikproblem` | keep in review until final approval | Too broad; needs concrete logistics barrier behind it. |

## Reviewed Held Edges

| review node | held edges reviewed | decision file |
|---|---:|---|
| `material/Metall` | 46 | `_migration/28_material_metall_edge_review_decisions.csv` |
| `huerde/Performance_Nachweis` | 33 | `_migration/29_huerde_performance_nachweis_edge_review_decisions.csv` |
| `bauteiltyp/Tragstruktur` | 28 | `_migration/30_bauteiltyp_tragstruktur_edge_review_decisions.csv` |
| `bauteiltyp/Bauwerksteil` | 27 | `_migration/31_bauteiltyp_bauwerksteil_edge_review_decisions.csv` |
| `huerde/Logistikproblem` | 20 | `_migration/32_huerde_logistikproblem_edge_review_decisions.csv` |

Total reviewed held edges: 154.

## Current Manual Decision State

```text
TODO: 27
validation issues: 0
```

## Important Outcome

This batch intentionally did not reduce the clean database purity to reduce the review queue. The five reviewed nodes remain outside `_database`; their reports explain how to resolve individual edges later when source context is strong enough.

Final decisions stay in `_migration/25_manual_review_decision_template.csv` and should be filled only after all review packages are prepared.

## Next Recommended Nodes

Continue with:

```text
bauteiltyp/Fliese
bauteiltyp/Kueche
bauteiltyp/Landschaftselement
bauteiltyp/Bruestung
bauteiltyp/Kern
```
