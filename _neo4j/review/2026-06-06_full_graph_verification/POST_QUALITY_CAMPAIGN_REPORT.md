# Post Quality Campaign Report (P6)

**Agent:** P6-06 (Aggregator) · **Date:** 2026-06-06 · **Database:** `mit-bestand`
**Merged ledger:** `VERIFICATION_LEDGER_ELEMENT.csv` — **17,327 rows** (all `coverage_level=element`)
**Coverage proof:** `ELEMENT_COVERAGE_PROOF.md`
**Summary:** `QUALITY_PASS_SUMMARY.md`

---

## 1. Campaign outcome

| Criterion | Status |
|---|---|
| D1 — every live node has one element row | ✅ |
| D2 — every live rel has one element row | ✅ |
| D3 — ledger reconciled to post-patch graph | ✅ |
| D4 — coverage diff = 0 uncovered | ✅ |
| D5 — PROVEN% recomputed on live ledger | **15,468 / 17,327 = 89.27%** |
| D6 — no graph mutation in aggregator | ✅ (read-only) |

## 2. Live graph (post quality-pass patches)

| Surface | Count |
|---|---:|
| Nodes | **2,264** |
| Relationships | **15,063** |
| Σ elements | **17,327** |

Graph mutations were applied by P6-01…P6-05 patch batches before this aggregator run.

## 3. Verdict distribution (17,327 element rows)

| Verdict | Count | Share |
|---|---:|---:|
| PROVEN | 15,468 | 89.3% |
| MISSING_EVIDENCE | 867 | 5.0% |
| PARTIAL | 812 | 4.7% |
| UNVERIFIABLE | 124 | 0.7% |
| SCHEMA_VIOLATION | 51 | 0.3% |
| CONTRADICTION | 5 | 0.0% |

## 4. P6 pass ledger inputs

| Agent | Scope | Rows adjudicated |
|---|---|---:|
| P6-01 | Schema & structural | 15 |
| P6-02 | Materialdepots | 17 |
| P6-03 | Compliance graph | 11 |
| P6-04 | Catalogue edges | 146 |
| P6-05 | Actor/participation | 139 |

## 5. Baseline → post-merge delta

| Metric | EP-10 | Post P6 | Δ |
|---|---:|---:|---:|
| Element rows | 17,596 | 17,327 | **-269** |
| PROVEN | 15,457 | 15,468 | **+11** |
| PROVEN % | 87.84% | 89.27% | — |
| Nodes (live) | 2,284 | 2,264 | -20 |
| Rels (live) | 15,312 | 15,063 | -249 |

## 6. Prune & synthesize summary

- **Pruned from baseline:** 305 rows (deleted/deprecated/merged graph elements)
- **Synthesized for new graph elements:** 36 rows

---

*Supersedes EP-10 `CAMPAIGN_REPORT_ELEMENT.md` for live coverage attestation on current `mit-bestand`.*
