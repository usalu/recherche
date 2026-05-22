# Element Coverage Proof — Post Quality Pass (P6)

**Agent:** P6-06 (Aggregator)
**Date:** 2026-06-06
**Database:** `mit-bestand` (read-only `elementId` export)
**Merged ledger:** `VERIFICATION_LEDGER_ELEMENT.csv` — **17,327 rows** (live target 17,327)

---

## 1. Live graph baseline (post Q01–Q05 patches)

| Surface | Live count | EP-10 baseline | Δ |
|---|---:|---:|---:|
| Nodes | **2,264** | 2,284 | **-20** |
| Relationships | **15,063** | 15,312 | **-249** |

Counts from read-only Neo4j export (`_p6_06_work/graph_nodes.json`, `graph_rels.json`).

## 2. Element-level coverage (Definition of Done)

| Surface | Live | Element-covered | Uncovered | Status |
|---|---:|---:|---:|:--:|
| **Nodes** | 2,264 | **2,264** | **0** | ✅ PASS |
| **Relationships** | 15,063 | **15,063** | **0** | ✅ PASS |
| **Σ elements** | **17,327** | **17,327** | **0** | ✅ PASS |

**Verdict:** **100 % element coverage** on current `mit-bestand` after quality-pass graph mutations.

## 3. PROVEN attestation

| Metric | EP-10 baseline | Post P6 merge | Δ |
|---|---:|---:|---:|
| PROVEN rows | 15,457 | **15,468** | **+11** |
| PROVEN % | 87.84% | **89.27%** | — |

## 4. Merge methodology

1. **Baseline:** `VERIFICATION_LEDGER_ELEMENT.csv` from EP-10 campaign (17,596 rows).
2. **Overrides:** P6-01…P6-05 quality-pass ledgers (`ledger/quality_pass_q01.csv` … `q05.csv`).
3. **Pruned:** rows for graph-deleted elements (Q01 merges/deletes, Q02 depot deprecations, Q04 catalogue deletes, Q05 self-loop delete) — `305` rows dropped.
4. **Synthesized:** 5 new nodes + 31 new rels (Q03 `PruefungNachweis` / `ERFUELLT_NACHWEIS` additions).
5. **Override priority:** P6-05 → P6-04 → P6-03 → P6-02 → P6-01 on matching `prior_claim_id` / `graph_element_id` / `ep08_claim_id` / `claim_id`.
6. **No graph mutation** in this aggregator (read-only export).

### P6 shard row counts

| Agent | Ledger rows |
|---|---:|
| P6-01 | 15 |
| P6-02 | 17 |
| P6-03 | 11 |
| P6-04 | 146 |
| P6-05 | 139 |

Prune stats: `{"stale_not_in_graph": 171, "q_pass_removed": 134}`
Override stats: `{"P6-05": 138, "P6-01": 6, "P6-03": 11, "P6-04": 39}`

## 5. Uncovered elements (must be ∅)

**None.** Live graph element set equals merged ledger key set.
