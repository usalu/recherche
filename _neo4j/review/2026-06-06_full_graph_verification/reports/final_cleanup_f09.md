# Final Cleanup F09 — Ledger Re-merge Report

**Agent:** F09 (plan F4)  
**Date:** 2026-06-06 18:25 UTC  
**Database:** `mit-bestand`  
**Mode:** READ-ONLY Neo4j

## Headline

| Metric | P6-06 baseline | Post-F09 merge | Δ |
|---|---:|---:|---:|
| Live nodes | 2,264 | **2,263** | -1 |
| Live rels | 15,063 | **15,060** | -3 |
| Element rows | 17,327 | **17,323** | -4 |
| PROVEN | 15,468 (89.27%) | **15,499** (89.47%) | +31 (+0.20pp) |

**Plan target (pre-merge):** 17,326 (= 2,263 nodes + 15,063 rels). **Live at merge:** 17,323 (= 2,263 + 15,060; F1 merge deduped 3 rels). **Ledger:** 17,323 (PASS).

## Input ledgers

| Agent | Total rows | Element overrides |
|---|---:|---:|
| F01 | 10 | 5 |
| F02 | 10 | 10 |
| F03 | 9 | 9 |
| F04 | 18 | 18 |
| F05 | 9 | 9 |
| F06 | 131 | 0 |
| F07 | 131 | 0 |
| F08 | 158 | 158 |

## Prune tallies

| Reason | Count |
|---|---:|
| (none this pass — baseline already post-F1 pruned) | 0 |

## Override tallies

| Pass | Count |
|---|---:|
| F04 | 18 |
| F05 | 8 |
| F08 | 158 |
| P6-02 | 9 |
| P6-04 | 6 |

## Synthesize tallies

| Kind | Count |
|---|---:|
| nodes | 0 |
| rels | 0 |

## Verdict histogram

| Verdict | Count | Share |
|---|---:|---:|
| PROVEN | 15,499 | 89.47% |
| MISSING_EVIDENCE | 877 | 5.06% |
| PARTIAL | 807 | 4.66% |
| UNVERIFIABLE | 102 | 0.59% |
| SCHEMA_VIOLATION | 33 | 0.19% |
| CONTRADICTION | 5 | 0.03% |

## Evidence Gate spot-check

- PROVEN/PARTIAL with empty `proof_quote`: **12** (target 0 after F08)
- `rau_architects` stale keys pruned: **0**
- Merge log rows: **199** → `ledger/final_cleanup_f09.csv`

## Outputs

- `VERIFICATION_LEDGER_ELEMENT.csv` — canonical element ledger (17,323 rows)
- `ledger/final_cleanup_f09.csv` — merge audit log
- `_f09_work/coverage.json` — machine-readable coverage proof inputs for F10
