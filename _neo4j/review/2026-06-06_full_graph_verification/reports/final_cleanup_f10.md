# Final Cleanup Agent F10 — Report

**Date:** 2026-06-06 · **Mode:** read-only Neo4j · **Database:** `mit-bestand`

## Summary

F10 cross-walked F09-merged `VERIFICATION_LEDGER_ELEMENT.csv` against live `elementId` export.

| Check | Result |
|---|---|
| Live elements | **17,323** (2,263 nodes + 15,060 rels) |
| Ledger rows | **17,323** |
| Uncovered nodes | **0** |
| Uncovered rels | **0** |
| Stale-only keys | **0** |
| PROVEN % | **89.36%** (15,479/17,323) |
| Evidence Gate violations (empty-quote PROVEN/PARTIAL) | **12** |
| Malformed `verdict=200` rows (http_status leak) | **17** |
| **Coverage (D1–D3)** | **PASS** |
| **Evidence Gate (D4)** | **PARTIAL** (12 residual P6-new synthetics) |

## Outputs

- `FINAL_COVERAGE_PROOF.md`
- `CAMPAIGN_CLOSEOUT_REPORT.md`
- `_f10_work/coverage.json`
- `_f10_work/synthesis.json`
- `AGENTS.md` §Aktueller Stand updated

## Notes

- No graph mutations performed.
- P6 baseline: 89.27% PROVEN on 17,327 rows.
- Delta: **+11** PROVEN rows, **+0.09** percentage points.
