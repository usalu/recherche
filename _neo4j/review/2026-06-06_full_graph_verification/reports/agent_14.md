# Verifier Agent 14 — Global Hygiene & Schema Conformance

**Campaign:** Full-Graph Verification (15-agent proof campaign)
**Database:** `mit-bestand` (READ-ONLY; only `read-cypher` + `get-schema` used)
**Date:** 2026-06-06
**Ledger:** [`ledger/agent_14.csv`](../ledger/agent_14.csv) — 112 claim rows (24 invariant/violation summary rows + 88 bidirectional-pair rows)

## Scope recap

Agent 14 is the graph-wide meta layer. It owns no shard exclusively; it runs pure Cypher invariants over the entire graph and emits a violations ledger. All eight mandated checks from `VERIFICATION_PLAN_15_AGENTS.md` §4 (Agent 14) were executed: orphans, duplicates/parallel/bidirectional, DEPRECATED isolation, forbidden properties, property-key schema drift, id/label/type legality, evidence-schema consistency, and the `needs_source_url_review.csv` recovery backlog.

## Baseline (live, scanned today)

| Surface | Live | Plan baseline | Note |
|---|---:|---:|---|
| Nodes | 2,304 | 2,304 | matches |
| Relationships | 15,457 | 15,457 | matches |
| Labels | 55 | 54 active | +1 = `DEPRECATED` meta-label (reconciles) |
| Relationship types | 51 | 50 active | +1 = `NUTZT_BAUWERK` singleton (flagged, A14-RELTYPE-001) |
| Distinct node property keys | **83** | 57 approved | **+26 drift** (A14-DRIFT-001) |
| Distinct rel property keys | **51** | 22 approved | **+29 drift** (A14-DRIFT-002) |

## Counts by verdict

| Verdict | Rows | Meaning |
|---|---:|---|
| PROVEN (invariant pass) | 12 | invariants that hold cleanly |
| SCHEMA_VIOLATION | 96 | 88 bidirectional pairs + 3 orphans + 5 structural/key/drift |
| PARTIAL | 1 | redundant `land` scalar (low severity) |
| MISSING_EVIDENCE | 1 | 353-row recovery backlog |
| **Total** | **112** | |

## Invariants that PASS (clean)

1. **Forbidden properties: 0.** No node or relationship carries `q_url_*`, `evidence_source_id`, `archive_source_id`, `evidence_claim_ids`, or any `legacy_*` / `phase*` key. The 2026-06-05 property cleanup holds; the legacy keys still listed in `node_property_matrix.csv` are fully gone from the live graph.
2. **Forbidden labels/types: 0.** No `:Quelle` / `:Regelwerk` / `:ExternalLink` / `:ResearchDocument` nodes; `BELEGT_IN` is absent from the 51 relationship types. Evidence lives only on properties, per `AGENTS.md`.
3. **Node id legality: clean.** All 2,304 nodes have a non-null `id`; zero duplicate ids.
4. **No parallel same-direction edges.** Zero `(type, from, to)` groups with count > 1.
5. **No duplicate normalized names** within any label.
6. **DEPRECATED isolation holds.** All 16 `DEPRECATED` nodes (8 `Architekturergebnis`, 8 `Entwurfsmethodik`) are degree-0 — never wired into the active subgraph.
7. **Evidence schema consistent.** No relationship carries both `source_url` and `evidence_url`; 72/72 `evidence_url` rels also have `evidence_confidence`; 3,691/3,691 `source_url` rels have `source_quote` or `confidence`; all `review_run` rels (49 VERBUNDEN_MIT_AKTEUR + others, 72 total) carry `evidence_url`.
8. **Confidence values in range.** Zero rel or node `confidence` outside [0, 1].

> Note on relationship `id`: 4,977 relationships lack an `id` property, but this is **by design** for the regulation/process layer (`ERFORDERT_NACHWEIS`, `TRIGGERS_REGULIERUNGSFRAGE`, `GILT_IN_LAND`, `GESTUETZT_AUF_REGELWERK`, `ERFUELLT_NACHWEIS`, geo/spender edges, …). The Agent-14 invariant only requires unique **node** ids, so this is recorded as an observation, not a violation.

## The 10 worst findings

### 1. 88 bidirectional `VERBUNDEN_MIT_AKTEUR` pairs — dedup regression (HIGH)
Of 341 `VERBUNDEN_MIT_AKTEUR` edges, **88 endpoint pairs carry edges in both directions** (≈176 edges). The earlier dedup was supposed to collapse these to one canonical direction; the invariant does **not** hold. Examples: `eth_zuerich ↔ matthias_kohler`, `Rotor ↔ opalis`, `madaster ↔ rau`, `gramazio_kohler_research ↔ matthias_kohler`, `materiuum ↔ materiuum_geneve_ressourcerie`. Full enumeration: ledger rows `A14-BIDIR-001..088`. Proposed action: `MERGE_DUPLICATE` (keep one direction).

### 2. 3 orphan `Akteur` nodes — non-vocab, zero edges (HIGH)
`c33_circular_construction_catalyst`, `circular_economy_switzerland` (CH, Agent 01 scope), and `repurpose` (NL, Agent 05 scope) have **no relationships at all**. These are named organisations expected to participate in the reuse network. Proposed action: `ESCALATE_HUMAN` (connect with sourced edges or deprecate).

### 3. Node property-key drift 57 → 83 (HIGH, re-baseline)
Live graph has 83 distinct node keys vs the 57 approved on 2026-06-05. Most additions are legitimate June intakes (geo: `latitude`/`longitude`/`geo_*`/`adresse`; entwurfsqualitaet: `entwurfsbeschreibung*`/`entwurfsqualitaet_*`; vocab: `name_de`/`literature_ref`/`vokabular_version`/`intake_run`/`deprecated_*`). The approved-key ledger and `AGENTS.md` "Aktueller Stand" are stale and must be re-baselined. (`A14-DRIFT-001`)

### 4. Relationship property-key drift 22 → 51 (HIGH, re-baseline)
51 distinct rel keys vs 22 approved. Additions stem from entwurfsqualitaet edges (`begruendung`, `belegkonfidenz`, `extraktionsstatus`, `integration_layer/phase`, `kandidatentext`, `quell_urls`, `vokabular_version`, `zuordnung_*`) and reuse-bubble edges (`evidence_*`, `connection_kind`, `dossier_section`, `fact_label`, `inference_basis`, `source_scope`, `dedup_run`). (`A14-DRIFT-002`)

### 5. `NUTZT_BAUWERK` singleton relationship type (MEDIUM)
A single `NUTZT_BAUWERK` edge (`rotordc → bw_generale_de_banque_brussels`, `nutzung_role='salvage_source'`) is the 51st relationship type, outside the canonical 50. The same donor building is also reached by a canonical `HAT_BAUWERK`. Proposed action: normalize to `HAT_BAUWERK{role:'salvage_source'}` or `AUS_SPENDER`. (`A14-RELTYPE-001`, `A14-RELKEY-001`)

### 6. `bauwerk_role` singleton property (LOW)
`HAT_BAUWERK` edge `p_multi_brussels_reuse_in_multi → bw_generale_de_banque_brussels` uses `bauwerk_role='donor_source'` (occ 1) instead of the canonical `role` (occ 166). Proposed action: `FIX_PROPERTY` rename. (`A14-RELKEY-002`)

### 7. Stray node keys on `enviromate` (LOW)
`additional_marktmodelle` (occ 1) — leftover enrichment key, not in the `Akteur` canonical schema. (`A14-NODEKEY-001`)

### 8. Stray node keys on `mobius_reemploi` (LOW)
`needs_evidence_urls` + `evidence_urls_target` (occ 1 each) — TODO-marker leftovers from an enrichment run. Resolve evidence, then drop. (`A14-NODEKEY-002`)

### 9. Redundant `land` scalar on 6 `Akteur` (LOW)
`bauteilboerse_hannover`, `circular_berlin`, `haus_der_materialisierung`, `material_mafia`, `mineka`, `repurpose` carry a scalar `land` property that duplicates the canonical `LIEGT_IN_LAND` edge. In-schema but redundant; verify the edge exists then drop the scalar. (`A14-LAND-001`)

### 10. Recovery backlog — 353 unsourced relationship claims (MEDIUM)
`needs_source_url_review.csv` lists 353 claims still without on-graph URL evidence: `HAT_BAUTEILTYP` 142, `NUTZT_MATERIAL` 103, `BETEILIGT_AN` 63, `HAT_AKTEURROLLE` 15, `HAT_GESCHAEFTSMODELL` 12, `LIEGT_IN_LAND` 9, `NUTZT_SOFTWARE` 3, `BETRIEBEN_VON` 3, `HAT_BESCHAFFUNGSWEG` 3. On-graph confirmation: `BETEILIGT_AN` carries no URL on 578/599 edges (21 `evidence_url`, 0 `source_url`). These types use `evidence_url`, not `source_url`. Proposed action: `RESOURCE` via the Tier-A web-evidence agents. (`A14-BACKLOG-001`)

## Items escalated to human

- 3 orphan `Akteur` nodes (`A14-ORPH-001..003`) — connect-or-deprecate.
- Node & rel key re-baseline (`A14-DRIFT-001/002`) — update the approved-key ledger + `AGENTS.md` to reflect June intakes.
- `NUTZT_BAUWERK` singleton type (`A14-RELTYPE-001`) — modelling decision.

## Anomalies / notes for the Aggregator

- Casing inconsistency in some `VERBUNDEN_MIT_AKTEUR` rel ids (e.g. `..._verbunden_mit_akteur_...` lowercase vs `...VERBUNDEN_MIT_AKTEUR...`); 6 `VERBUNDEN_MIT_AKTEUR` edges have null `id`. Cosmetic; bundle with the bidirectional dedup.
- All schema-drift findings are **additive growth from approved June intakes**, not forbidden-property reintroductions — the cleanup invariants themselves are intact.

## Summary

Across 12 graph-wide invariants the core hygiene is strong: **zero forbidden properties, zero forbidden labels/types, zero duplicate or missing node ids, zero parallel edges, zero name collisions, DEPRECATED fully isolated, and a fully consistent evidence schema** (no dual-URL rels; every `evidence_url`/`source_url`/`review_run` rel is schema-complete; all confidences in range). The two material violations are (a) **88 bidirectional `VERBUNDEN_MIT_AKTEUR` pairs** that the earlier dedup failed to collapse, and (b) **3 non-vocab orphan `Akteur` nodes**. Secondary issues are property-key drift (node 57→83, rel 22→51 — legitimate June-intake growth needing a re-baseline), a `NUTZT_BAUWERK` singleton type with off-canonical role properties, a handful of stray Akteur keys, and a 353-claim source-URL recovery backlog routed to the Tier-A agents. **Single most important finding: the 88 bidirectional `VERBUNDEN_MIT_AKTEUR` pairs — a dedup regression to be remediated by `MERGE_DUPLICATE`.**
