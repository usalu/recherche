# Campaign Report — 10-Agent ELEMENT-PROOF Campaign

**Agent:** EP-10 (Aggregator) · **Date:** 2026-06-06 · **Database:** `mit-bestand`
**Merged ledger:** `VERIFICATION_LEDGER_ELEMENT.csv` — **17,596 rows** (all `coverage_level=element`)
**Coverage proof:** `ELEMENT_COVERAGE_PROOF.md` — **2,284/2,284 nodes + 15,312/15,312 rels** (0 uncovered)

---

## 1. Campaign outcome

| Criterion | Status |
|---|---|
| D1 — every live node has one element row | ✅ |
| D2 — every live rel has one element row | ✅ |
| D3 — zero aggregate/type rows | ✅ |
| D4 — coverage diff = 0 uncovered | ✅ |
| D7 — 17,596 / 17,596 elements | ✅ |
| D8 — no graph mutation | ✅ |

## 2. Verdict distribution (17,596 element rows)

| Verdict | Count | Share |
|---|---:|---:|
| PROVEN | 15,453 | 87.8% |
| PARTIAL | 1,017 | 5.8% |
| MISSING_EVIDENCE | 887 | 5.0% |
| UNVERIFIABLE | 124 | 0.7% |
| SCHEMA_VIOLATION | 63 | 0.4% |
| DEAD_LINK | 35 | 0.2% |
| CONTRADICTION | 16 | 0.1% |
| UNSUPPORTED | 1 | 0.0% |

## 3. Proposed-action distribution

| Action | Count |
|---|---:|
| KEEP | 15,862 |
| ADD_SOURCE | 856 |
| RESOURCE | 571 |
| ESCALATE_HUMAN | 206 |
| RELABEL | 65 |
| MERGE_DUPLICATE | 22 |
| DEPRECATE_NODE | 8 |
| FIX_PROPERTY | 6 |

## 4. Wave-1 shard heatmap (EP-01 … EP-09)

| Agent | Rows | PROVEN | PARTIAL | SCHEMA | CONTRA | MISSING |
|---|---:|---:|---:|---:|---:|---:|
| EP-01 | 1,459 | 1459 | 0 | 0 | 0 | 0 |
| EP-02 | 1,239 | 1238 | 0 | 1 | 0 | 0 |
| EP-03 | 1,504 | 1358 | 143 | 0 | 0 | 3 |
| EP-04 | 1,104 | 1104 | 0 | 0 | 0 | 0 |
| EP-05 | 1,270 | 1270 | 0 | 0 | 0 | 0 |
| EP-06 | 1,303 | 1303 | 0 | 0 | 0 | 0 |
| EP-07 | 1,159 | 1159 | 0 | 0 | 0 | 0 |
| EP-08 | 1,066 | 1047 | 0 | 8 | 11 | 0 |
| EP-09 | 58 | 25 | 7 | 0 | 0 | 26 |

## 5. R07 / Wave-2 residual status

- **R07 `RESOURCE` edges:** 145 `HAT_BAUTEILTYP`/`NUTZT_MATERIAL` re-adjudicated in EP-03 shard; 25 residual `BETEILIGT_AN` in EP-09.
- **R01 unsourced `Materialdepot`:** 17 nodes in EP-09 (`ADD_SOURCE` / `ESCALATE_HUMAN`).
- **R02 dangling `Nachweisforderung`:** 11 `CONTRADICTION` in EP-08; 10 `ERFUELLT_NACHWEIS` gaps in EP-09.
- **R03/R04 deferred merges:** documented in EP-09 report; not auto-merged.

**Findings requiring action:** 2,260 rows (non-KEEP or negative verdict).

## 6. Proposed patches (human-gated)

9 new `UNSUPPORTED`/`SCHEMA_VIOLATION` rows from EP shards → `patches/element_proof_remediation_proposed.jsonl`. **Not applied.**

---

*Prior 15-agent aggregate coverage (41.2 % rel / 54.9 % node element-level) is superseded by this campaign's 100 % element attestation.*
