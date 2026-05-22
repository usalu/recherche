# Element-Proof Agent EP-09 — Residuals & Wave-2 Backlog

**Database:** `mit-bestand` (READ-ONLY)
**Date:** 2026-06-06
**Ledger:** [`ledger/element_proof_agent_09.csv`](../ledger/element_proof_agent_09.csv) — **58** rows (41 rels + 17 nodes)
**Builder:** [`_agent_ep09_build.py`](../_agent_ep09_build.py)
**Plan:** [`VERIFICATION_PLAN_10_AGENTS_ELEMENT_PROOF.md`](../VERIFICATION_PLAN_10_AGENTS_ELEMENT_PROOF.md) §Agent 09
**Wave-2 context:** [`WAVE2_SUMMARY.md`](../WAVE2_SUMMARY.md)

---

## 1. Scope & pre-flight

| Surface | Planned | Live gap |
|---|---:|---:|
| `BETEILIGT_AN` | 15 | 15 |
| `ERFUELLT_NACHWEIS` | 10 | 10 |
| `VERBUNDEN_MIT_AKTEUR` | 10 | 10 |
| `LIEGT_IN_LAND` | 5 | 5 |
| `NUTZT_SOFTWARE` | 1 | 1 |
| Unsourced `Materialdepot` | 17 | 17 |
| **Total** | **58** | **58** |

Pre-flight subtracted `VERIFICATION_LEDGER.csv` rows with `coverage_level=element` (matched on `graph_element_id` or rel triple / node id). Did **not** re-prove the 583 already-covered `BETEILIGT_AN` edges from Agent 09.

---

## 2. Verdict summary

| Verdict | Count |
|---|---:|
| MISSING_EVIDENCE | 26 |
| PARTIAL | 7 |
| PROVEN | 25 |

| Proposed action | Count |
|---|---:|
| ADD_SOURCE | 7 |
| ESCALATE_HUMAN | 19 |
| KEEP | 27 |
| RESOURCE | 5 |

---

## 3. Shard notes

### R07 / post-R03 `BETEILIGT_AN` (15 gap edges)

The 15 gap edges are **post-R03 merge survivors** (canonical actor ids like `btu_cottbus`, `tampere_university`, `CITYFOERSTER`) whose prior Agent 09 element rows pointed at stale `elementId`s. Re-attestation inherits dossier corroboration from `akteur_typ_projekt_geo.json` where the project target matches. R07 overlap-derived `BETEILIGT_AN` (actor→Bauteilgruppe) are a disjoint set absorbed by Agents 03/04.

### R02 — 10 new `ERFUELLT_NACHWEIS` edges

Wave-2 `remediation_r02_erfuellt_nachweis.patch.jsonl` added 10 high-confidence satisfaction edges. Each row attests the specific `PruefungNachweis`→`Nachweisforderung` pair via logic + R02 rewire_map (11 dangling NF remain for Agent EP-08).

### R05 — 5 `LIEGT_IN_LAND` orphan-connect deltas

Three R05 orphan `Akteur` nodes (`c33_circular_construction_catalyst`, `circular_economy_switzerland`, `repurpose`) gained `LIEGT_IN_LAND` edges post-Wave-2; element rows were missing until this shard.

### Stale `VERBUNDEN_MIT_AKTEUR` (10)

Re-attestation after Wave-2 dedup/merge changed live `elementId`s; prior element ledger keys were stale. Rows inherit Agent 06b / prior web adjudication where available.

### R01 — 17 unsourced `Materialdepot`

All 17 carry `MISSING_EVIDENCE` + `ESCALATE_HUMAN` (aggregate/unknown-source placeholders per R01). Five sibling depots were sourced in R01 patch; these 17 remain structural cleanup.

---

## 4. R03/R04 deferred merges (document only — not in 58-row scope)

Per plan §2.4, **17 deferred node-duplicate pairs** from R03 + `rau`↔`rau_architects` (R04) require human gate — **no auto-merge**. See [`ledger/remediation_r03.csv`](../ledger/remediation_r03.csv) rows with `ESCALATE_HUMAN` / `DEFER` / `REFERENCE_R04` and [`reports/remediation_r04.md`](remediation_r04.md).

---

## 5. Limits

- READ-ONLY: no graph mutation.
- R07 PARTIAL/RESOURCE BETEILIGT_AN rows: `fetched=true` where R07 fetched, but component proof weak — verdict capped at PARTIAL.
- R03/R04 merge pairs documented in §4; not duplicated as element rows (disjoint from 58-item scope).

---

## 6. One-paragraph summary

EP-09 closes the **58-element** residual shard: **41** relationship gaps (15 `BETEILIGT_AN` R07 residuals, 10 R02 `ERFUELLT_NACHWEIS`, 10 stale `VERBUNDEN_MIT_AKTEUR`, 5 R05 `LIEGT_IN_LAND`, 1 `NUTZT_SOFTWARE`) plus **17** unsourced `Materialdepot` nodes escalated from R01. Strict web gate applied to actor-participation edges; logic/dossier proof used for regulation satisfaction edges. All rows use `coverage_level=element` with live `graph_element_id`.
