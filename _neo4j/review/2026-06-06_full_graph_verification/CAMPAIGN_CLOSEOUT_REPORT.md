# Campaign Closeout Report — Final Cleanup Wave (F1–F10)

**Agent:** F10 (Final Aggregator) · **Date:** 2026-06-06 · **Database:** `mit-bestand`
**Merged ledger:** `VERIFICATION_LEDGER_ELEMENT.csv` — **17,323 rows**
**Coverage proof:** `FINAL_COVERAGE_PROOF.md`
**Supersedes:** `POST_QUALITY_CAMPAIGN_REPORT.md` (P6-06)

---

## 1. Campaign outcome

| Criterion | Status |
|---|---|
| D1 — every live node has one element row | ✅ |
| D2 — every live rel has one element row | ✅ |
| D3 — coverage diff = 0 uncovered, 0 stale-only | ✅ |
| D4 — no empty-quote PROVEN/PARTIAL | ⚠️ (12 residual P6-new synthetics) |
| D5 — PROVEN% recomputed | **15,479 / 17,323 = 89.36%** |
| D6 — no graph mutation in F10 | ✅ (read-only) |

## 2. Live graph (post final-cleanup patches)

| Surface | Count |
|---|---:|
| Nodes | **2,263** |
| Relationships | **15,060** |
| Σ elements | **17,323** |

## 3. VMA backbone (live)

| Metric | Count |
|---|---:|
| `VERBUNDEN_MIT_AKTEUR` (undirected) | **496** |
| With `review_run` | **132** |
| With `evidence_confidence='belegt'` | **114** |
| With `evidence_url` | **132** |

## 4. Verdict distribution (17,323 element rows)

| Verdict | Count | Share |
|---|---:|---:|
| PROVEN | 15,479 | 89.4% |
| MISSING_EVIDENCE | 877 | 5.1% |
| PARTIAL | 805 | 4.6% |
| UNVERIFIABLE | 107 | 0.6% |
| SCHEMA_VIOLATION | 33 | 0.2% |
| CONTRADICTION | 5 | 0.0% |

*17 legacy rows have malformed `verdict=200` (http_status leak); not counted above.*

## 5. Baseline → final delta

| Metric | P6-06 | Final (F10) | Δ |
|---|---:|---:|---:|
| Element rows | 17,327 | 17,323 | **-4** |
| PROVEN | 15,468 | 15,479 | **+11** |
| PROVEN % | 89.27% | 89.36% | **+0.09 pp** |
| Nodes (live) | 2,264 | 2,263 | -1 |
| Rels (live) | 15,063 | 15,060 | -3 |

## 6. Final-cleanup agent inputs

| Agent | Scope |
|---|---|
| F1 | `rau_architects` → `rau` merge + dry-run audit |
| F2 | 19 merge-redirect relationship re-proofs |
| F3 | 27 UNVERIFIABLE/PARTIAL externals |
| F4–F8 | (parallel doc/schema sync per plan) |
| F9 | Ledger re-merge → `VERIFICATION_LEDGER_ELEMENT.csv` |
| F10 | Coverage proof + closeout (this report) |

## 7. Evidence Gate residual

- Empty-quote PROVEN/PARTIAL rows: **12**
- Duplicate element keys: **0**

---

*Final attestation for `mit-bestand` after Final Cleanup wave. Graph mutations only via prior human-gated patch batches (F1).*
