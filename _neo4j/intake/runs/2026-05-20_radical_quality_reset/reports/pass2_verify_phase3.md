# Pass-2 Detailed Verification — Phase 3 (Enrichment)

- **Verifier:** Pass-2 Detailed Verifier 8 of 12 (read-only)
- **Date (UTC):** 2026-05-21
- **Database:** `mit-bestand` (`bolt://localhost:7687`)
- **Driver:** Neo4j MCP (`project-0-recherche-Neo4j-Official`, `NEO4J_READ_ONLY=true`)
- **Plan sections:** 3.1 (BUILT_IN_ERA), 3.2 (pollutant inference), 3.3 (ReuseRule)
- **Run dir:** `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\`
- **Source reports cross-checked:** `agent_11_phase3_report.md`, `final_verify_phase3_1.md`, `final_verify_phase3_2.md`, `final_verify_phase3_3.md`, `repair_phase4_1_q1.md`

## Verdict

**STATUS: PASS** — all 17 detailed checks pass live against `mit-bestand`. Phase 3.1 + 3.2 + 3.3 are fully complete.

A single intentional drift from the original Phase 3 outputs is documented:
`BUILT_IN_ERA.evidence_origin` was demoted from `curated` to `inferred` (and
`evidence_confidence` from `belegt` to `inferiert`) by the later
`mig_repair_4_1_curated_excerpts_and_q1.cypher` (repair step C). This still
satisfies check #6 because `evidence_origin` remains set and the requested
shape constraints (`evidence_basis ∈ {year_inferred, cell_citation}`,
`evidence_confidence` ∈ canonical enum) hold.

---

## Phase 3.1 — BUILT_IN_ERA

| # | Check | Expected | Got | Result |
|---|---|---|---|---|
| 1 | `migrations/mig_3_1_built_in_era.cypher` exists | present | present (4231 B, 2026-05-21 00:30) | PASS |
| 1 | `PHASE_3_1_DONE.flag` exists | present | present (1848 B, 2026-05-21 00:36) | PASS |
| 2 | `MATCH ()-[r:BUILT_IN_ERA]->() RETURN count(r)` | ≥ 5 | 8 | PASS |
| 2 | Breakdown by `era_id` | partition of 8 | `era_1970_1990`=3, `era_1990_2000`=2, `era_nachkrieg_1945_1970`=2, `era_post_2000`=1 (sum = 8) | PASS |
| 3 | `MATCH (b:Bauwerk) WHERE b.era_unknown=true RETURN count(b)` | (no hard target stated) | 178 | PASS |
| 4 | `MATCH (m:Materialdepot) WHERE m.era_unknown=true RETURN count(m)` | == 23 | 23 | PASS |
| 5 | `MATCH (b:Bauwerk) WHERE NOT exists{(b)-[:BUILT_IN_ERA]->()} AND coalesce(b.era_unknown,false)<>true RETURN count(b)` | == 0 | 0 | PASS |
| 6 | Sample 5 BUILT_IN_ERA: `evidence_origin` set, `evidence_basis ∈ {year_inferred, cell_citation}`, `evidence_confidence` valid | 5 / 5 | 5 / 5 (`origin=inferred`, `basis=year_inferred`, `confidence=inferiert`) | PASS |

### Coverage reconciliation

- `(:Bauwerk)` total = 186 → with `BUILT_IN_ERA` (8) + with `era_unknown=true` (178) = 186 ✓ (disjoint, per check 5)
- `(:Materialdepot)` total = 23 → with `BUILT_IN_ERA` (0) + with `era_unknown=true` (23) = 23 ✓

### Sample BUILT_IN_ERA edges (first 5 by `source_id`)

| source_id | era_id | evidence_origin | evidence_basis | evidence_confidence | evidence_source_id |
|---|---|---|---|---|---|
| `bw_ka13_existing_building` | `era_nachkrieg_1945_1970` | inferred | year_inferred | inferiert | `bauwerk.baujahr_property` |
| `bw_lycee_block_3000` | `era_1970_1990` | inferred | year_inferred | inferiert | `bauwerk.baujahr_property` |
| `bw_lycee_block_6000` | `era_1990_2000` | inferred | year_inferred | inferiert | `bauwerk.baujahr_property` |
| `bw_multi_brouckere_tower` | `era_nachkrieg_1945_1970` | inferred | year_inferred | inferiert | `bauwerk.baujahr_property` |
| `bw_rws_districtskantoor_terneuzen` | `era_1990_2000` | inferred | year_inferred | inferiert | `bauwerk.baujahr_property` |

`evidence_origin` was previously `curated` (per `final_verify_phase3_1.md`); it was demoted to `inferred` by `mig_repair_4_1_curated_excerpts_and_q1.cypher` step C ("year_inferred is a derivation, not a citation"). This is documented in `repair_phase4_1_q1.md` and is a strengthening of provenance honesty, not a regression of Phase 3.1 acceptance.

---

## Phase 3.2 — Pollutant inference

| # | Check | Expected | Got | Result |
|---|---|---|---|---|
| 7 | `migrations/mig_3_2_pollutant_inference.cypher` exists | present | present (7094 B, 2026-05-21 00:30) | PASS |
| 7 | `PHASE_3_2_DONE.flag` exists | present | present (2411 B, 2026-05-21 00:37) | PASS |
| 8 | `MATCH ()-[r:HAT_SCHADSTOFF]->() RETURN count(r)` | == 0 | 0 | PASS |
| 9 | `MATCH ()-[r:HAS_RISK_POLLUTANT]->() RETURN count(r)` | ≥ 700 | 803 | PASS |
| 9 | Breakdown by `evidence_basis` | partition of 803 | `material_only`=788, `documented`=11, `era_and_material`=4 (sum = 803) | PASS |
| 10 | `MATCH ()-[r:REQUIRES_VERIFICATION_FOR]->() RETURN count(r)` | ≥ 250 | 347 | PASS |
| 11 | Sample 5 HAS_RISK_POLLUTANT: canonical evidence shape, `evidence_source_id` non-null | 5 / 5 | 5 / 5 | PASS |
| 11 | Sample 5 REQUIRES_VERIFICATION_FOR: canonical evidence shape, `evidence_source_id` non-null | 5 / 5 | 5 / 5 | PASS |

### Sample HAS_RISK_POLLUTANT edges (first 5 by `src_id`)

| src_id | dst_id | evidence_origin | evidence_basis | evidence_source_id | evidence_confidence |
|---|---|---|---|---|---|
| `bg_dismantled_glas_technik_medunicampus_fluorescent` | `s_schwermetalle` | derived | documented | `batch2_v2_followup_2026-05-20` | unklar |
| `bg_dismantled_holz_mehrere_circl_larch_structure` | `s_holzschutzmittel` | inferred | material_only | `q_schadstoff_reuse_knowledge_graph_research_md` | inferiert |
| `bg_dismantled_holz_mehrere_circl_larch_structure` | `s_schwermetalle` | inferred | material_only | `q_schadstoff_reuse_knowledge_graph_research_md` | inferiert |
| `bg_dismantled_holz_mehrere_circl_larch_structure` | `s_formaldehyd` | inferred | material_only | `q_schadstoff_reuse_knowledge_graph_research_md` | inferiert |
| `bg_dismantled_holz_mehrere_circl_larch_structure` | `s_bleifarbe` | inferred | material_only | `q_schadstoff_reuse_knowledge_graph_research_md` | inferiert |

All 5 carry a non-null `evidence_source_id` and an `evidence_origin` / `evidence_basis` / `evidence_confidence` triple from the canonical enums.

### Sample REQUIRES_VERIFICATION_FOR edges (first 5 by `src_id`)

| src_id | dst_id | evidence_origin | evidence_basis | pollutant_basis | evidence_source_id | evidence_confidence |
|---|---|---|---|---|---|---|
| `p_55_great_suffolk_street_london` | `s_bleifarbe` | inferred | project_rollup | material_only | `q_schadstoff_reuse_knowledge_graph_research_md` | inferiert |
| `p_55_great_suffolk_street_london` | `s_schwermetalle` | inferred | project_rollup | material_only | `q_schadstoff_reuse_knowledge_graph_research_md` | inferiert |
| `p_association_house_groeditz` | `s_pcb` | inferred | project_rollup | material_only | `q_schadstoff_reuse_knowledge_graph_research_md` | inferiert |
| `p_association_house_plauen` | `s_pcb` | inferred | project_rollup | material_only | `q_schadstoff_reuse_knowledge_graph_research_md` | inferiert |
| `p_awm_muenster_circular_office` | `s_formaldehyd` | inferred | project_rollup | material_only | `q_schadstoff_reuse_knowledge_graph_research_md` | inferiert |

All 5 carry the project-rollup contract (`evidence_basis='project_rollup'`, `pollutant_basis ∈ {documented, era_and_material, material_only}`), with non-null `evidence_source_id`.

---

## Phase 3.3 — ReuseRule

| # | Check | Expected | Got | Result |
|---|---|---|---|---|
| 12 | `migrations/mig_3_3_reuse_rules.cypher` exists | present | present (6256 B, 2026-05-21 00:31) | PASS |
| 12 | `PHASE_3_3_DONE.flag` exists | present | present (2430 B, 2026-05-21 00:37) | PASS |
| 13 | `MATCH (r:ReuseRule) RETURN count(r)` | == 20 | 20 | PASS |
| 13 | All 5 list properties non-empty on all 20 rules (`key_norms`, `legal_conditions`, `required_tests`, `pollutant_risks`, `processing_methods`) | 20/20 each | 20/20 each | PASS |
| 14 | Every `:ReuseRule` wired to a `:Land` via `APPLIES_IN` | 20/20 | 20/20 | PASS |
| 14 | Every `:ReuseRule` wired to a `:Material` via `APPLIES_TO` | 20/20 | 20/20 | PASS |
| 15 | `MATCH (:ReuseRule)-[:REFERENZIERT_NORM]->(:Norm) RETURN count(*)` | ≥ 60 | 93 | PASS |
| 16 | All 20 `:ReuseRule` have `evidence_origin='inferred'` | 20/20 | 20/20 | PASS |
| 17 | `MATCH (rr:ReuseRule)-[:APPLIES_IN]->(:Land),(rr)-[:APPLIES_TO]->(:Material) RETURN count(*)` | == 20 | 20 | PASS |

### ReuseRule inventory (20 rows, ranked)

| rank | id | country_iso | material | priority | key_norms | legal | tests | pollutants | processing |
|---:|---|---|---|---|---:|---:|---:|---:|---:|
| 1 | `rr_gb_stahl` | GB | Stahl | P1_Critical | 5 | 4 | 9 | 5 | 7 |
| 2 | `rr_be_stahl` | BE | Stahl | P1_Critical | 4 | 4 | 2 | 3 | 4 |
| 3 | `rr_de_stahl` | DE | Stahl | P1_Critical | 4 | 3 | 7 | 5 | 5 |
| 4 | `rr_nl_stahl` | NL | Stahl | P1_Critical | 4 | 4 | 6 | 4 | 4 |
| 5 | `rr_ch_stahl` | CH | Stahl | P1_Critical | 4 | 3 | 6 | 5 | 5 |
| 6 | `rr_be_beton` | BE | Beton | P1_Critical | 6 | 3 | 10 | 6 | 7 |
| 7 | `rr_nl_beton` | NL | Beton | P1_Critical | 5 | 4 | 6 | 5 | 6 |
| 8 | `rr_de_beton` | DE | Beton | P1_Critical | 5 | 3 | 9 | 5 | 6 |
| 9 | `rr_ch_beton` | CH | Beton | P1_Critical | 3 | 3 | 7 | 5 | 5 |
| 10 | `rr_fi_beton_hollow_core_slabs` | FI | Beton / hollow-core slabs | P1_Critical | 4 | 2 | 8 | 6 | 6 |
| 11 | `rr_no_beton_hollow_core_slabs` | NO | Beton / hollow-core slabs | P1_Critical | 4 | 3 | 6 | 5 | 6 |
| 12 | `rr_de_holz` | DE | Holz | P2_High | 5 | 3 | 9 | 8 | 8 |
| 13 | `rr_nl_holz` | NL | Holz | P2_High | 5 | 3 | 6 | 5 | 7 |
| 14 | `rr_be_holz` | BE | Holz | P2_High | 4 | 3 | 6 | 5 | 6 |
| 15 | `rr_ch_holz` | CH | Holz | P2_High | 3 | 3 | 7 | 7 | 6 |
| 16 | `rr_be_naturstein` | BE | Naturstein | P2_High | 8 | 3 | 7 | 5 | 6 |
| 17 | `rr_ch_naturstein` | CH | Naturstein | P2_High | 3 | 4 | 7 | 5 | 6 |
| 18 | `rr_gb_holz` | GB | Holz | P2_High | 5 | 3 | 7 | 5 | 6 |
| 19 | `rr_de_ziegel` | DE | Ziegel | P2_High | 6 | 4 | 6 | 5 | 6 |
| 20 | `rr_de_lehm` | DE | Lehm | P2_High | 6 | 3 | 7 | 5 | 6 |

All 20 rows have every required list ≥ 2 entries; minimum required list size across all 20 nodes / all 5 lists is 2 (legal_conditions on `rr_fi_beton_hollow_core_slabs`); none are empty.

Country ISO codes represented: `BE`, `CH`, `DE`, `FI`, `GB`, `NL`, `NO` (7 distinct, matching plan §3.3.pre).

---

## Cypher used (read-only)

```cypher
// 3.1
MATCH ()-[r:BUILT_IN_ERA]->() RETURN count(r);                                                       // 8
MATCH ()-[r:BUILT_IN_ERA]->(e:BauwerkEra) RETURN e.id, count(r) ORDER BY e.id;                       // breakdown
MATCH (b:Bauwerk)       WHERE b.era_unknown=true       RETURN count(b);                              // 178
MATCH (m:Materialdepot) WHERE m.era_unknown=true       RETURN count(m);                              // 23
MATCH (b:Bauwerk)
WHERE NOT exists{(b)-[:BUILT_IN_ERA]->()}
  AND coalesce(b.era_unknown,false)<>true
RETURN count(b);                                                                                     // 0
MATCH (b)-[r:BUILT_IN_ERA]->(e:BauwerkEra)
RETURN b.id, e.id, r.evidence_origin, r.evidence_basis,
       r.evidence_confidence, r.evidence_source_id
ORDER BY b.id LIMIT 5;                                                                               // sample

// 3.2
MATCH ()-[r:HAT_SCHADSTOFF]->()               RETURN count(r);                                       // 0
MATCH ()-[r:HAS_RISK_POLLUTANT]->()           RETURN count(r);                                       // 803
MATCH ()-[r:HAS_RISK_POLLUTANT]->()           RETURN r.evidence_basis, count(r) ORDER BY 2 DESC;     // breakdown
MATCH ()-[r:REQUIRES_VERIFICATION_FOR]->()    RETURN count(r);                                       // 347
MATCH (a)-[r:HAS_RISK_POLLUTANT]->(b)
RETURN a.id, b.id, r.evidence_origin, r.evidence_basis,
       r.evidence_source_id, r.evidence_confidence
ORDER BY a.id LIMIT 5;                                                                               // sample
MATCH (a)-[r:REQUIRES_VERIFICATION_FOR]->(b)
RETURN a.id, b.id, r.evidence_origin, r.evidence_basis,
       r.evidence_source_id, r.evidence_confidence, r.pollutant_basis
ORDER BY a.id LIMIT 5;                                                                               // sample

// 3.3
MATCH (r:ReuseRule) RETURN count(r);                                                                 // 20
MATCH (r:ReuseRule)
WITH r,
     size(r.key_norms)          AS kn,
     size(r.legal_conditions)   AS lc,
     size(r.required_tests)     AS rt,
     size(r.pollutant_risks)    AS pr,
     size(r.processing_methods) AS pm
RETURN count(r) AS rules_total,
       sum(CASE WHEN kn>0 THEN 1 ELSE 0 END) AS key_norms_nonempty,
       sum(CASE WHEN lc>0 THEN 1 ELSE 0 END) AS legal_conditions_nonempty,
       sum(CASE WHEN rt>0 THEN 1 ELSE 0 END) AS required_tests_nonempty,
       sum(CASE WHEN pr>0 THEN 1 ELSE 0 END) AS pollutant_risks_nonempty,
       sum(CASE WHEN pm>0 THEN 1 ELSE 0 END) AS processing_methods_nonempty;                         // 20 / 20 each
MATCH (r:ReuseRule)
OPTIONAL MATCH (r)-[ai:APPLIES_IN]->(:Land)
OPTIONAL MATCH (r)-[at:APPLIES_TO]->(:Material)
WITH r, count(ai) AS n_in, count(at) AS n_to
RETURN count(r),
       sum(CASE WHEN n_in>0 THEN 1 ELSE 0 END),
       sum(CASE WHEN n_to>0 THEN 1 ELSE 0 END),
       sum(CASE WHEN n_in>0 AND n_to>0 THEN 1 ELSE 0 END);                                           // 20/20/20/20
MATCH (:ReuseRule)-[r:REFERENZIERT_NORM]->(:Norm) RETURN count(r);                                   // 93
MATCH (r:ReuseRule) RETURN r.evidence_origin, count(*);                                              // inferred: 20
MATCH (rr:ReuseRule)-[:APPLIES_IN]->(:Land),(rr)-[:APPLIES_TO]->(:Material) RETURN count(*);         // 20
```

---

## Cross-report consistency

| Source | Total checks declared | This Pass-2 result |
|---|---:|---|
| `agent_11_phase3_report.md` | 20 / 20 PASS | confirmed live |
| `final_verify_phase3_1.md` | 7 / 7 PASS | confirmed live (with documented evidence_origin demotion) |
| `final_verify_phase3_2.md` | 9 / 9 PASS | confirmed live |
| `final_verify_phase3_3.md` | 9 / 9 PASS | confirmed live |
| Pass-2 (this report) | 17 / 17 PASS | **PASS** |

---

## JSON verdict

```json
{
  "verifier": "pass2_detailed_verifier_8_of_12",
  "date": "2026-05-21",
  "database": "mit-bestand",
  "status": "pass",
  "phases": ["3.1", "3.2", "3.3"],
  "phase_3_1": {
    "migration_present": true,
    "phase_flag_present": true,
    "built_in_era_total": 8,
    "built_in_era_minimum_met_ge5": true,
    "built_in_era_breakdown_by_era_id": {
      "era_1970_1990": 3,
      "era_1990_2000": 2,
      "era_nachkrieg_1945_1970": 2,
      "era_post_2000": 1
    },
    "bauwerk_era_unknown": 178,
    "materialdepot_era_unknown": 23,
    "materialdepot_era_unknown_equals_23": true,
    "bauwerk_neither_era_nor_unknown": 0,
    "sample_built_in_era_shape_ok": true,
    "sample_built_in_era_notes": "evidence_origin='inferred', evidence_basis='year_inferred', evidence_confidence='inferiert' on all 5 sampled (and all 8 live) BUILT_IN_ERA edges; origin was demoted from 'curated' by mig_repair_4_1_curated_excerpts_and_q1.cypher step C — see repair_phase4_1_q1.md"
  },
  "phase_3_2": {
    "migration_present": true,
    "phase_flag_present": true,
    "hat_schadstoff_total": 0,
    "has_risk_pollutant_total": 803,
    "has_risk_pollutant_minimum_met_ge700": true,
    "has_risk_pollutant_breakdown_by_basis": {
      "documented": 11,
      "era_and_material": 4,
      "material_only": 788
    },
    "requires_verification_for_total": 347,
    "requires_verification_for_minimum_met_ge250": true,
    "sample_has_risk_pollutant_shape_ok": true,
    "sample_requires_verification_for_shape_ok": true
  },
  "phase_3_3": {
    "migration_present": true,
    "phase_flag_present": true,
    "reuse_rule_total": 20,
    "all_five_list_properties_nonempty_on_all_rules": true,
    "rules_with_applies_in_to_land": 20,
    "rules_with_applies_to_to_material": 20,
    "referenziert_norm_from_reuse_rule_total": 93,
    "referenziert_norm_minimum_met_ge60": true,
    "reuse_rule_evidence_origin_all_inferred": true,
    "decision_support_query_total_equals_20": true
  },
  "checks_total": 17,
  "checks_passed": 17,
  "checks_failed": 0
}
```
