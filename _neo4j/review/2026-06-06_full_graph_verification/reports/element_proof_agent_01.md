# Element-Proof Agent EP-01 — HAT_AKTEURROLLE

**Database:** `mit-bestand` (READ-ONLY)
**Date:** 2026-06-06
**Scope:** 1,459 element rows (1,461 live minus 2 prior A12 element rows A12-EXC-001/002)

## 1. Scope recap

- Live `HAT_AKTEURROLLE` edges: **1461**
- Excluded (already element-covered by Agent 12): **2** (`stadt_zuerich` → 2 roles)
- This ledger rows: **1459**

### Domain breakdown (this ledger)

| Domain label | edges |
|---|---:|
| `Akteur` | 1433 |
| `Software` | 26 |

## 2. Method

Per-edge contract conformance (Tier C): domain label ∈ {`:Akteur`, `:Software`},
range label `:Akteurrolle` on live target node (seed file cross-check; seed drift noted).
`basis_type=contract`; no web fetch. Aligns with Agent 12 aggregate range/domain Cypher checks.

## 3. Verdict counts

| Verdict | Count |
|---|---:|
| PROVEN | 1459 |

## 4. Excluded prior element rows (A12-EXC-001/002)

| claim_id | from | to | verdict |
|---|---|---|---|
| A12-rel-0001 | stadt_zuerich | ar_bauherr_auftraggeber | SCHEMA_VIOLATION |
| A12-rel-0002 | stadt_zuerich | ar_oeffentliche_hand_foerderung | SCHEMA_VIOLATION |

Re-point to `:Akteur` `stadt_zuerich_amt_hochbauten` or remove (Agent 12 ESCALATE_HUMAN).

## 5. Anomalies in this shard

- None. All 1,459 edges: domain valid (`Akteur` or `Software`), range `:Akteurrolle`.
- **Seed drift (72 edges):** `ar_materialbroker` — live `:Akteurrolle` nodes absent from `controlled_vocabulary.seed.kg.jsonl`; edges still PROVEN on live label check (A12 method).

## 6. Summary

Emitted **1459** element-level ledger rows (`coverage_level=element`).
**1459** PROVEN via contract+live endpoint check;
**0** SCHEMA_VIOLATION.
No aggregate rows. Two legacy `Stadt`-domain edges remain in prior Agent 12 element ledger only.

**Output:** `_neo4j/review/2026-06-06_full_graph_verification/ledger/element_proof_agent_01.csv`
