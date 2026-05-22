# Coverage Proof — Full-Graph Verification Campaign

**Agent:** 15b (Aggregator re-run incl. Agent 06b)
**Date:** 2026-06-06
**Database:** `mit-bestand` (graph id export read-only; Agent 15 node-source patch **applied** — see apply report)
**Inputs:** `ledger/agent_01.csv` … `ledger/agent_14.csv` + `ledger/agent_06b.csv` (**8,284 rows**) + live graph id inventory.

> **Headline:** Actor-network **element gaps are closed** after Agent 06b merge. Element-level proof exists for
> **6,365 / 15,457 relationships (41.2 %)** and **1,264 / 2,304 nodes (54.9 %)**. Another **9,092 relationships**
> and **1,040 nodes** are verified **only at aggregate type/structural level** (Agents 12 & 13 group rows).
> **0 relationships** and **0 sourced `Akteur` nodes** remain outside the ledger. The remaining 1,040 uncovered
> nodes are **Tier-C vocab/process labels only** (no genuine Akteur gap).

---

## 1. Live graph baseline (read-only)

| Surface | Live count | Plan expectation | Match |
|---|---:|---:|:--:|
| Nodes | **2,304** | 2,304 | ✅ |
| Relationships | **15,457** | 15,457 | ✅ |
| Relationship types | 50 active (+`NUTZT_BAUWERK` singleton = 51) | 50 | ✅ (see Agent 14 `A14-RELTYPE-001`) |

Counts pulled via `MATCH (n) RETURN count(n)` and `MATCH ()-[r]->() RETURN count(r)`; the full id inventory
was exported read-only (`default_access_mode="READ"`) by `_agent15_export_graph_ids.py` into
`_agent15_work/graph_nodes.json` (2,304) and `_agent15_work/graph_rels.json` (15,457). All 2,304 nodes carry a
non-null `id` property.

## 2. How ledger rows were matched to graph elements

Shard ledgers use **heterogeneous identifiers**; the aggregator resolves each row in this order:

- **Relationships** — (1) real `elementId` `5:<uuid>:<n>` (Agents 02, 04, 06, 07, 09); (2) `(from_id, type, to_id)`
  triple (Agents 01, 03, 05); (3) **aggregate / type-level** rows — `agg:<TYPE>` (Agent 12) or bare `<TYPE>`
  (Agent 13) → expanded to that whole relationship class as **type-level coverage, not element-level**.
- **Nodes** — real `elementId`, else node `id` property (e.g. `concular`); `_*_GROUP` summary rows are treated
  as type-level.
- **Invariants** — Agent 14's 15 graph-wide scans (own no individual element).

Match outcome was written back into the merged `VERIFICATION_LEDGER.csv` as `coverage_level`
(`element` | `type` | `invariant` | `unmatched`) + `graph_element_id`.

## 3. Relationship coverage (Σ = 15,457)

| Coverage class | Rels | % |
|---|---:|---:|
| **Element-level** (per-edge evidence or per-edge logic, real id or triple match) | **6,365** | 41.2 % |
| **Type-level only** (Agents 12/13 aggregate domain/range proof — not per edge) | **9,092** | 58.8 % |
| **Uncovered** (no shard, no aggregate) | **0** | 0 % |

Element-level coverage is **complete (100 %)** for every Tier-A/Tier-B URL or factual class, e.g.:

| Relationship type | Total | Element-covered | Owner |
|---|---:|---:|---|
| `ERFORDERT_NACHWEIS` | 1,578 | 1,578 | 07 |
| `TRIGGERS_REGULIERUNGSFRAGE` | 1,130 | 1,130 | 07 |
| `LIEGT_IN_LAND` | 651 | 651 | 09 |
| `BETEILIGT_AN` | 599 | 599 | 09 |
| `GILT_IN_LAND` | 281 | 281 | 07 |
| `LIEGT_IN_STADT` | 252 | 252 | 09 |
| `AUS_SPENDER` | 245 | 245 | 09 |
| `HAT_BAUWERK` | 194 | 194 | 09 |
| `GESTUETZT_AUF_REGELWERK` | 167 | 167 | 07 |
| `NUTZT_SOFTWARE` | 54 | 54 | 10 |
| `TEIL_VON_PROGRAMM` | 35 | 35 | 10 |
| `BETRIEBEN_VON` | 9 | 9 | 10 |

The **9,092 type-level-only** edges are the controlled-vocabulary / process-classification classes owned by
Agents 12 and 13 (`HAT_AKTEURROLLE` 1,493, `HAT_BAUTEILTYP` 871, `HAT_AKTEURTYP` 700, `NUTZT_MATERIAL` 633,
`HAT_PROZESSPHASE` 679, `HAT_BESCHAFFUNGSWEG` 592, `HAT_LOGISTIK` 434, `HAT_MATERIALGRUPPE` 403, …). For these
classes the shards **did** prove, with Cypher, that **100 % of endpoints conform to the schema range and that
every source label is in the allowed domain set**, and they individually flagged each violation (see §6). What
they did **not** produce is one ledger row per edge. This is a legitimate Tier-C method but it means a per-edge
audit trail does not exist for these 9,092 edges.

### 3.1 `VERBUNDEN_MIT_AKTEUR` — **100 % element-covered after Agent 06b**

All **341** `VERBUNDEN_MIT_AKTEUR` edges now have per-element ledger rows (189 from Agents 01–06 + **218** from
Agent 06b re-dispatch; 66 reverse legs overlap canonical directions in the ledger but de-duplicate to unique
graph elements). Agent 06b finding: **0 / 218** gap edges carried on-graph `evidence_url` at audit time — the
class is adjudicated but largely **sourceless on-graph**; remediation patches drafted (see `REMEDIATION_PLAN.md` §8).

## 4. Node coverage (Σ = 2,304)

| Coverage class | Nodes | % |
|---|---:|---:|
| **Element-level** | **1,264** | 54.9 % |
| **Type/group-level only** (vocab + process nodes via Agents 12/13 aggregate rows) | **1,040** | 45.1 % |
| **Uncovered — genuine gap** | **0** | 0 % |

- **Element-level (1,264):** adds **168** sourced `Akteur` nodes from Agent 06b to the prior 1,097 (actors,
  buildings/projects/places, software/depots, law nodes, violation nodes from 12/13/14).
- **Type/group-level (1,040):** unchanged — controlled-vocabulary and process nodes covered only by Agents 12/13
  aggregate rows (`Bauteilgruppe` 364, `Kennwert` 255, `PruefungNachweis` 118, …).
- **No uncovered `Akteur` nodes remain.** Agent 06b closed the sourced-actor gap; unsourced actors were already
  covered by Agent 08.

## 5. Overlap reconciliation

- **No element-id was double-counted.** Coverage sets are de-duplicated by resolved graph `element_id`; rows
  that map to the same edge/node (e.g. an edge web-checked by Agent 01 *and* structurally owned elsewhere)
  collapse to one covered element.
- Agent 14 is an intentional **meta-layer** (overlap allowed); its 91 element rows (88 bidirectional pairs +
  3 orphans) and 15 invariants are recorded but do not contribute to MECE element counts.

## 6. Limitations (explicit — not papered over)

1. **Tier-C is aggregate, not per-element.** Agents 12 (vocab) and 13 (process/requirement) returned
   **type/group ledgers** (32 and 47 rows) instead of the ~6,900 + ~6,435 per-edge rows the plan's §5.1 implies.
   Their structural conclusions (range/domain conformance, satisfiability) are sound and reproducible by Cypher,
   but **9,092 edges and 1,040 nodes have no per-element proof row.** If per-edge attestation is a hard
   acceptance requirement, Agents 12 & 13 must be re-run in enumerate-every-row mode.
2. **Actor-network element coverage is complete** (Agent 06b, §3.1/§4). Remaining risk is **on-graph provenance**:
   218 gap edges had zero `evidence_url` at audit; 06b remediation patches are drafted but not yet applied
   (except 17 Agent-15 node sources applied 2026-06-06).
3. **Source-ledger CSV hygiene:** 2 rows arrived column-shifted by an unescaped comma — Agent 13
   `A13-node-pn-0001` (verdict blank; a notes fragment landed in `proposed_action`) and Agent 14 `A14-INV` row
   (verdict `false`). Both are cosmetic parse artifacts in the *source* shards; the underlying findings are
   intact in their `notes`. Counted as `(blank)`/`false` in raw verdict tallies and excluded from action logic.
4. **Tier-A "PROVEN" trust** rests on each web agent's quoted snippet; the aggregator did not re-fetch all
   3,542 Agent-07 PROVEN URLs. Spot regression checks should sample these in a later pass.

## 7. Required re-dispatches (to reach true 100 %)

| # | Shard | Work-set | Status |
|---|---|---|---|
| R1 | **Agent 06b — non-bubble actor networks** | 218 edges + 168 sourced `Akteur` nodes (386 claims) | ✅ **merged** (`agent_15b`) |
| R2 | **Agent 12-full** (optional, if per-edge proof required) | enumerate every vocab classification edge/node | open |
| R3 | **Agent 13-full** (optional, if per-edge proof required) | enumerate every process/requirement edge/node | open |

Definition-of-Done item *"actor-network element coverage / ∅ Akteur+VERBUNDEN gaps"* is **met at ledger level**.
Per-edge attestation for the 9,092 Tier-C edges remains optional (R2/R3).
