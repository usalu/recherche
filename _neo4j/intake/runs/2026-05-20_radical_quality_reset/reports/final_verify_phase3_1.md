# Final Verification — Phase 3.1 BUILT_IN_ERA

**Verifier:** Final Verifier 7 of 12 (read-only)
**Date:** 2026-05-21
**Database:** `mit-bestand`
**Plan reference:** `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md` §3.1
**Run dir:** `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\`

## Verdict

**STATUS: PASS** — all 7 checks pass against the live `mit-bestand` graph. Phase 3.1 is correctly applied and idempotent.

## Check results

| # | Check | Expected | Got | Result |
|---|---|---|---|---|
| 1 | `migrations/mig_3_1_built_in_era.cypher` exists | present | present | PASS |
| 2 | `PHASE_3_1_DONE.flag` present in run dir | present | present (1 848 B, 2026-05-21 00:36) | PASS |
| 3 | `MATCH ()-[r:BUILT_IN_ERA]->() RETURN count(r)` | ≥ 5 (target ~8) | 8 | PASS |
| 4 | Bauwerk `era_unknown = true` count | ≥ 150 (target ~178) | 178 | PASS |
| 5 | Materialdepot `era_unknown = true` count | ≥ 20 (target 23) | 23 | PASS |
| 6 | Bauwerk neither `BUILT_IN_ERA` nor `era_unknown` | == 0 | 0 | PASS |
| 7 | Sample BUILT_IN_ERA edges have evidence_origin set, evidence_basis ∈ {`year_inferred`, `cell_citation`} | yes | 8/8 sampled edges have `evidence_origin='curated'`, `evidence_basis='year_inferred'` | PASS |

## Coverage reconciliation

- `MATCH (b:Bauwerk) RETURN count(b)` → **186**
- `MATCH (b:Bauwerk)-[:BUILT_IN_ERA]->() RETURN count(b)` → **8**
- `MATCH (b:Bauwerk) WHERE b.era_unknown = true RETURN count(b)` → **178**
- 8 + 178 = 186 ✓ (every `:Bauwerk` either has `BUILT_IN_ERA` or `era_unknown=true`; the two sets are disjoint per check 6)

- `MATCH (m:Materialdepot) RETURN count(m)` → **23**
- `MATCH (m:Materialdepot)-[:BUILT_IN_ERA]->() RETURN count(m)` → **0**
- `MATCH (m:Materialdepot) WHERE m.era_unknown = true RETURN count(m)` → **23**
- 0 + 23 = 23 ✓

## Sampled BUILT_IN_ERA edges (all 8, sorted by source id)

| source id | era id | evidence_origin | evidence_basis | evidence_confidence | evidence_source_id |
|---|---|---|---|---|---|
| `bw_ka13_existing_building` | `era_nachkrieg_1945_1970` | curated | year_inferred | belegt | `bauwerk.baujahr_property` |
| `bw_lycee_block_3000` | `era_1970_1990` | curated | year_inferred | belegt | `bauwerk.baujahr_property` |
| `bw_lycee_block_6000` | `era_1990_2000` | curated | year_inferred | belegt | `bauwerk.baujahr_property` |
| `bw_multi_brouckere_tower` | `era_nachkrieg_1945_1970` | curated | year_inferred | belegt | `bauwerk.baujahr_property` |
| `bw_rws_districtskantoor_terneuzen` | `era_1990_2000` | curated | year_inferred | belegt | `bauwerk.baujahr_property` |
| `bw_suutarila_community_centre_donor` | `era_1970_1990` | curated | year_inferred | belegt | `bauwerk.baujahr_property` |
| `bw_villa_welpeloo_wohnhaus_und_kunstlager` | `era_post_2000` | curated | year_inferred | belegt | `bauwerk.baujahr_property` |
| `bw_werkhof_moeoeslistrasse` | `era_1970_1990` | curated | year_inferred | belegt | `bauwerk.baujahr_property` |

All 8 edges have `evidence_origin` set (`curated`) and `evidence_basis='year_inferred'` (the second permitted value `cell_citation` was not used by Phase 3.1 because the Phase 4b dossier-emitted per-row era backfill in plan §3.1.c was intentionally not applied; this is documented in the PHASE_3_1_DONE.flag note 3 and is consistent with the agent 11 brief). Check 7 only requires that `evidence_basis ∈ {'year_inferred','cell_citation'}` — `year_inferred` satisfies the disjunction.

## Live cypher used

```cypher
// Check 3
MATCH ()-[r:BUILT_IN_ERA]->() RETURN count(r) AS c;  // 8

// Check 4
MATCH (b:Bauwerk) WHERE b.era_unknown = true RETURN count(b) AS c;  // 178

// Check 5
MATCH (m:Materialdepot) WHERE m.era_unknown = true RETURN count(m) AS c;  // 23

// Check 6
MATCH (b:Bauwerk)
WHERE NOT exists{(b)-[:BUILT_IN_ERA]->()}
  AND (b.era_unknown IS NULL OR b.era_unknown = false)
RETURN count(b) AS c;  // 0

// Check 7 (sample, all 8 returned)
MATCH (b)-[r:BUILT_IN_ERA]->(e:BauwerkEra)
RETURN b.id AS source_id, labels(b) AS source_labels, e.id AS era_id,
       r.evidence_origin, r.evidence_basis,
       r.evidence_confidence, r.evidence_source_id
ORDER BY source_id LIMIT 8;
```

## Notes (informational, not blocking)

- All 8 BUILT_IN_ERA edges originate from `:Bauwerk`; no `:Materialdepot` carries `baujahr`, so the entire 23-node depot population is honestly flagged `era_unknown=true`. This matches the PHASE_3_1_DONE.flag `after.built_in_era_from_materialdepot=0` and is acceptable per plan §3.1.d ("any Bauwerk without BUILT_IN_ERA gets explicit era_unknown").
- The remaining 178 Bauwerke are flagged `era_unknown=true` rather than receiving `cell_citation` edges from dossier markdown (plan §3.1.c). Per the PHASE_3_1_DONE.flag note 3, this is intentional: Phase 4b loaders did not emit donor-era metadata into a queryable form, so the §3.1.c path is a no-op until Phase 4b is expanded. The current state is honest (`era_unknown=true`) and satisfies §3.1.d.
- Migration is idempotent: re-runnable via `MERGE` on the edge with `ON CREATE` / `ON MATCH SET coalesce(...)`.
