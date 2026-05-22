# Final Coverage Proof — Final Cleanup Wave (F10)

**Agent:** F10 (Final Aggregator)
**Date:** 2026-06-06
**Database:** `mit-bestand` (read-only `elementId` export)
**Canonical ledger:** `VERIFICATION_LEDGER_ELEMENT.csv` — **17,323 rows** (live target **17,323**)
**Supersedes:** `ELEMENT_COVERAGE_PROOF.md` (P6-06 attestation)

---

## 1. Live graph baseline (post F1–F3 patches)

| Surface | Live count | P6-06 baseline | Δ |
|---|---:|---:|---:|
| Nodes | **2,263** | 2,264 | **-1** |
| Relationships | **15,060** | 15,063 | **-3** |
| Σ elements | **17,323** | 17,327 | **-4** |

Counts from read-only Neo4j export (`_f10_work/graph_nodes.json`, `graph_rels.json`).

## 2. Element-level coverage (Definition of Done D1–D3)

| Surface | Live | Ledger-covered | Uncovered | Stale-only | Status |
|---|---:|---:|---:|---:|:--:|
| **Nodes** | 2,263 | **2,263** | **0** | — | ✅ |
| **Relationships** | 15,060 | **15,060** | **0** | — | ✅ |
| **Σ elements** | **17,323** | **17,323** | **0** | **0** | ✅ PASS |

**Verdict:** **100 % element coverage** — every live node and relationship has exactly one `coverage_level=element` row; zero stale-only ledger keys.

## 3. PROVEN attestation

| Metric | P6-06 baseline | Post F09 merge | Δ |
|---|---:|---:|---:|
| Element rows | 17,327 | **17,323** | **-4** |
| PROVEN rows | 15,468 | **15,479** | **+11** |
| PROVEN % | 89.27% | **89.36%** | **+0.09 pp** |

## 4. Verdict distribution (17,323 element rows)

| Verdict | Count | Share |
|---|---:|---:|
| PROVEN | 15,479 | 89.4% |
| MISSING_EVIDENCE | 877 | 5.1% |
| PARTIAL | 805 | 4.6% |
| UNVERIFIABLE | 107 | 0.6% |
| SCHEMA_VIOLATION | 33 | 0.2% |
| CONTRADICTION | 5 | 0.0% |

Note: **17** rows carry `verdict=200` (http_status column leak in legacy rows) — excluded from PROVEN tally; human cleanup optional.

## 5. Evidence Gate audit (D4)

| Check | Count | Status |
|---|---:|:--:|
| PROVEN/PARTIAL with empty `proof_quote` | **12** | ❌ FAIL |
| Duplicate `graph_element_id` keys | **0** | ✅ PASS |
| Rows with `coverage_level=type` | **0** | ✅ |

## 6. Uncovered / stale elements (must be ∅)

**None.** Live graph element set equals merged ledger key set.

## 7. Methodology

1. **Input:** F09-merged `VERIFICATION_LEDGER_ELEMENT.csv`.
2. **Live export:** read-only Neo4j `elementId` for all nodes and relationships.
3. **Cross-walk:** match ledger rows via `graph_element_id` / `element_id` / `(from_id, rel_type, to_id)` triple.
4. **No graph mutation** in this aggregator.

---

*Attestation agent F10 — read-only Neo4j, no patch apply.*
