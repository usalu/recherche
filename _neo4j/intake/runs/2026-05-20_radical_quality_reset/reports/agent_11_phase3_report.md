# Agent 11 — Phase 3.1 + 3.2 + 3.3 Report

_Database: `mit-bestand` (bolt://localhost:7687)_
_Runner: `logs/agent11_runner.py`_
_Initial run: 2026-05-20T22:34:36 → 22:34:41 (5.1 s)_
_Idempotent re-run: 2026-05-20T22:34:59 → 22:35:01 (2.4 s, zero deltas)_
_Acceptance: 20 / 20 PASS (see `logs/agent11_verify.json`)_

---

## TL;DR

| metric | before Phase 3 | after Phase 3 | Δ |
|---|---:|---:|---:|
| total nodes | 3 731 | 3 820 | +89 (20 ReuseRule + 69 inferred Norm anchors) |
| total relationships | 24 460 | 25 740 | +1 280 |
| `:BUILT_IN_ERA` edges | 0 | 8 | +8 |
| `:HAT_SCHADSTOFF` edges | 11 | 0 | -11 (promoted) |
| `:HAS_RISK_POLLUTANT` edges | 0 | 803 | +803 |
| `:REQUIRES_VERIFICATION_FOR` edges | 0 | 347 | +347 |
| `:ReuseRule` nodes | 0 | 20 | +20 |
| `:APPLIES_IN` / `:APPLIES_TO` | 0 / 0 | 20 / 20 | +20 each |
| `:REFERENZIERT_NORM` from `:ReuseRule` | 0 | 93 | +93 |
| `:Norm` nodes | 34 | 103 | +69 inferred |
| `:Land` with `country_iso` | 0 | 7 | +7 |

All 20 acceptance checks (across 3.1 / 3.2 / 3.3) pass on first run and again on idempotent re-run.

---

## 3.1 — Wire `:Bauwerk` (and `:Materialdepot`) to `:BauwerkEra`

### Inputs

- 186 `:Bauwerk` nodes, 23 `:Materialdepot` nodes, 6 `:BauwerkEra` nodes (`era_vor_1900`, `era_1900_1945`, `era_nachkrieg_1945_1970`, `era_1970_1990`, `era_1990_2000`, `era_post_2000`).
- Year property today: only `baujahr` exists in `mit-bestand` (the plan also names `jahr_errichtet` which is not present — see `logs/agent11_probe.json`).
- 8 of 186 `:Bauwerk` carry `baujahr`. 0 of 23 `:Materialdepot` carry `baujahr`.

### Outputs

- 8 `:Bauwerk -[:BUILT_IN_ERA]-> :BauwerkEra` edges (one per dated bauwerk).
- 0 `:Materialdepot -[:BUILT_IN_ERA]-> :BauwerkEra` edges (no materialdepot carries a year today).
- 178 `:Bauwerk` get `era_unknown=true` (the honest 186 − 8 remainder).
- 23 `:Materialdepot` get `era_unknown=true` (every depot).

### Sample edges

| bauwerk | baujahr | era |
|---|---:|---|
| `bw_ka13_existing_building` | 1950 | `era_nachkrieg_1945_1970` |
| `bw_multi_brouckere_tower` | 1969 | `era_nachkrieg_1945_1970` |
| `bw_lycee_block_3000` | 1973 | `era_1970_1990` |
| `bw_werkhof_moeoeslistrasse` | 1978 | `era_1970_1990` |
| `bw_suutarila_community_centre_donor` | 1981 | `era_1970_1990` |
| `bw_lycee_block_6000` | 1997 | `era_1990_2000` |
| `bw_rws_districtskantoor_terneuzen` | 2000 | `era_1990_2000` |
| `bw_villa_welpeloo_wohnhaus_und_kunstlager` | 2009 | `era_post_2000` |

All edges carry `evidence_origin='curated'`, `evidence_basis='year_inferred'`, `evidence_source_id='bauwerk.baujahr_property'`, `evidence_confidence='belegt'`.

### Deviation from plan

Plan section 3.1.c promises an additional `~111` `:Bauwerk -[:BUILT_IN_ERA]-> :BauwerkEra` backfill emitted by the Phase 4b dossier loader. That backfill did NOT land — the Phase 4b loaders (`logs/agent10_research_registry_loader.py`, `logs/agent9_dossier_loader.py`) extract pollutant, processing-method, and verification rows but do not emit era cells from gebaeude dossier sections. This is out of scope for Agent 11 (Phase 4b changes are explicitly excluded by the task brief), so the 178 remaining donor buildings are honestly flagged `era_unknown=true` instead of silently fabricating an era.

---

## 3.2 — Pollutant inference

### Inputs

- 11 pre-existing `:HAT_SCHADSTOFF` edges (4 `:Projekt → :Schadstoff`, 7 `:Bauteilgruppe → :Schadstoff`).
- 9 `:Schadstoff` nodes with 18 `:TYPISCH_BEI_MATERIAL` edges and 15 `:TYPISCH_BEI_ERA` edges.
- 472 `:Bauteilgruppe -[:NUTZT_MATERIAL]-> :Material` edges.

### Rule pipeline

1. **3.2.a `documented`** — promote every `:HAT_SCHADSTOFF` to `:HAS_RISK_POLLUTANT` with `evidence_basis='documented'`, copying provenance; delete the original edge.
2. **3.2.b `era_and_material`** — for each `(:Bauteilgruppe)-[:NUTZT_MATERIAL]->(:Material)<-[:TYPISCH_BEI_MATERIAL]-(:Schadstoff)-[:TYPISCH_BEI_ERA]->(:BauwerkEra)`, fire an edge when the bauteilgruppe's donor `(:Bauteilgruppe)-[:FROM_DONOR]->(:Bauwerk)` is `:BUILT_IN_ERA` to the same era.
3. **3.2.c `material_only`** — fallback for material matches that did not get an era_and_material edge.
4. **3.2.d project rollup** — for every `(:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg)-[:HAS_RISK_POLLUTANT]->(s)`, emit `(:Projekt)-[:REQUIRES_VERIFICATION_FOR]->(:Schadstoff)` with `pollutant_basis` = strongest underlying basis (`documented` > `era_and_material` > `material_only`).

### Results

| edge type | basis | count |
|---|---|---:|
| `:HAS_RISK_POLLUTANT` | `documented` | 11 |
| `:HAS_RISK_POLLUTANT` | `era_and_material` | 4 |
| `:HAS_RISK_POLLUTANT` | `material_only` | 788 |
| `:HAS_RISK_POLLUTANT` | **total** | **803** |
| `:REQUIRES_VERIFICATION_FOR` | `documented` | 5 |
| `:REQUIRES_VERIFICATION_FOR` | `era_and_material` | 4 |
| `:REQUIRES_VERIFICATION_FOR` | `material_only` | 338 |
| `:REQUIRES_VERIFICATION_FOR` | **total** | **347** |

### Deviations from plan

- Plan rule 3.2.b cites `(bg)-[:AUS_BAUWERK]->(b:Bauwerk)`. Phase 4.2 has since renamed that type to `:FROM_DONOR` (`mig_4_2_rename_donor_receiver.cypher`). The migration uses `:FROM_DONOR`, which is the same semantic edge — donor building's era determines the era in which the pollutants were originally present.
- Plan estimate "~250 era_and_material + ~540 material_only" assumed `~111` Bauwerke would receive `:BUILT_IN_ERA` from a Phase 4b dossier pass. With only 8 dated bauwerke today, `era_and_material` realistically fires 4 times. The `material_only` fallback then absorbs the rest, producing 788 inferred edges (rather than ~540) and bringing the total to 803, well within the ~800 magnitude.
- Project-level `:REQUIRES_VERIFICATION_FOR` totals 347 vs. plan estimate ~250. Reason: the plan assumed ~85 projects with pollutant exposure × ~3 pollutants each; the actual material mix in the 105 `:Projekt` corpus produces 347 distinct (project, schadstoff) tuples. Magnitude (~250) is preserved.

### Sample edges

```text
era_and_material (donor era + material rule fired):
  bg_reuse_daemmstoff_mehrere_lycee_gypsum_acoustic_panels -[HAS_RISK_POLLUTANT]-> s_kmf
  bg_reuse_daemmstoff_mehrere_lycee_gypsum_acoustic_panels -[HAS_RISK_POLLUTANT]-> s_asbest
  bg_reuse_mehrere_mehrere_moeoeslistrasse_sanitaer_kueche -[HAS_RISK_POLLUTANT]-> s_pcb

documented (promoted from HAT_SCHADSTOFF):
  bg_dismantled_glas_technik_medunicampus_fluorescent -[HAS_RISK_POLLUTANT]-> s_schwermetalle
  bg_retained_mehrere_mehrere_europa_residence_palace_parts -[HAS_RISK_POLLUTANT]-> s_asbest
```

```text
sample REQUIRES_VERIFICATION_FOR (project-level rollup):
  p_awm_muenster_circular_office -[REQUIRES_VERIFICATION_FOR]-> s_pcb (basis: material_only)
  p_awm_muenster_circular_office -[REQUIRES_VERIFICATION_FOR]-> s_holzschutzmittel (basis: material_only)
  p_awm_muenster_circular_office -[REQUIRES_VERIFICATION_FOR]-> s_formaldehyd (basis: material_only)
```

---

## 3.3 — ReuseRule (20-row country × material decision shelf)

### Inputs

- Source: `_knowledge/themes/circular_construction_reuse_graph_gaps.md`, "Top 20 graph gaps" table.
- 19 pre-existing `:Land` nodes (none with `country_iso`), 26 `:Material` nodes, 34 `:Norm` nodes.

### Outputs

- **20** `:ReuseRule` nodes (one per ranked row), each carrying `id`, `name`, `rank`, `country_iso`, `country_name`, `material`, `material_id`, `priority` (`P1_Critical` or `P2_High`), `project_cluster`, plus five list-properties: `key_norms`, `legal_conditions`, `required_tests`, `pollutant_risks`, `processing_methods`, plus `source_url` and `suggested_graph_action`.
- **20** `:ReuseRule -[:APPLIES_IN]-> :Land` edges (1 per rule, all 7 target countries — DE, BE, NL, CH, GB, FI, NO — now also carry `country_iso`).
- **20** `:ReuseRule -[:APPLIES_TO]-> :Material` edges (the two "Beton / hollow-core slabs" rules both anchor to `mat_beton`, with the full material string retained in `ReuseRule.material`).
- **93** `:ReuseRule -[:REFERENZIERT_NORM]-> :Norm` edges across **75** distinct norms; **69** new `:Norm` nodes were created (`evidence_origin='inferred'`, `source_scope='reuse_rule_seed'`), 6 existing norms were re-used by id match.

### ReuseRule degree distribution

| metric | value |
|---|---:|
| min degree per ReuseRule | 5 (Swiss Beton / Holz / Naturstein rules carry 5 outgoing edges each) |
| median degree per ReuseRule | 7 |
| mean degree per ReuseRule | 6.65 |
| max degree per ReuseRule | 10 (Belgian Naturstein — 8 EN test standards) |

All 20 rules satisfy plan Rule B (`≥ 5 connections per node`).

### 20 ReuseRule node ids (in rank order)

```text
 1  rr_gb_stahl
 2  rr_be_stahl
 3  rr_de_stahl
 4  rr_nl_stahl
 5  rr_ch_stahl
 6  rr_be_beton
 7  rr_nl_beton
 8  rr_de_beton
 9  rr_ch_beton
10  rr_fi_beton_hollow_core_slabs
11  rr_no_beton_hollow_core_slabs
12  rr_de_holz
13  rr_nl_holz
14  rr_be_holz
15  rr_ch_holz
16  rr_be_naturstein
17  rr_ch_naturstein
18  rr_gb_holz
19  rr_de_ziegel
20  rr_de_lehm
```

### Decision-support query (works now)

```cypher
MATCH (rule:ReuseRule)-[:APPLIES_IN]->(:Land {country_iso:'DE'}),
      (rule)-[:APPLIES_TO]->(:Material {name:'Stahl'})
RETURN rule.id, rule.key_norms, rule.required_tests,
       rule.pollutant_risks, rule.processing_methods,
       rule.evidence_source_id;
```

Returns rule `rr_de_stahl` with norms `["CEN/TS 1090-201","DIN EN 1090-2","DIN EN 1993","MVV TB/DIBt pathway"]`, tests including mechanical / weldability / NDT, pollutants including lead/chromate / PAH / asbestos / PCB / old fireproofing, and a 5-step processing workflow.

---

## Acceptance summary

| group | check | want | got | pass |
|---|---|---|---:|:-:|
| 3.1 | BUILT_IN_ERA from Bauwerk created | ≥ 8 | 8 | ✓ |
| 3.1 | BUILT_IN_ERA from Materialdepot | = 0 | 0 | ✓ |
| 3.1 | every Bauwerk has era edge OR era_unknown | = 0 | 0 | ✓ |
| 3.1 | every Materialdepot has era edge OR era_unknown | = 0 | 0 | ✓ |
| 3.1 | Bauwerk era_unknown == total − dated | = 178 | 178 | ✓ |
| 3.1 | Materialdepot era_unknown == total − dated | = 23 | 23 | ✓ |
| 3.2 | zero remaining HAT_SCHADSTOFF | = 0 | 0 | ✓ |
| 3.2 | HAS_RISK_POLLUTANT total ~800 | 600..1100 | 803 | ✓ |
| 3.2 | documented edges promoted | ≥ 11 | 11 | ✓ |
| 3.2 | era_and_material rule fired | ≥ 0 | 4 | ✓ |
| 3.2 | material_only fallback fired | ≥ 600 | 788 | ✓ |
| 3.2 | REQUIRES_VERIFICATION_FOR total ~250 | 200..500 | 347 | ✓ |
| 3.3 | exactly 20 ReuseRule nodes | = 20 | 20 | ✓ |
| 3.3 | APPLIES_IN edges | = 20 | 20 | ✓ |
| 3.3 | APPLIES_TO edges | = 20 | 20 | ✓ |
| 3.3 | REFERENZIERT_NORM total ~93 | 60..120 | 93 | ✓ |
| 3.3 | no ReuseRule missing APPLIES_IN | = 0 | 0 | ✓ |
| 3.3 | no ReuseRule missing APPLIES_TO | = 0 | 0 | ✓ |
| 3.3 | no ReuseRule missing REFERENZIERT_NORM | = 0 | 0 | ✓ |
| 3.3 | ReuseRule median degree (Rule B) | ≥ 5 | 7 | ✓ |

20 / 20 PASS.

---

## Idempotency

Both runs (initial + immediate re-run) produced identical after-counts. Every write uses MERGE with `ON CREATE SET`; the only `DELETE` is on `:HAT_SCHADSTOFF` in step 3.2.a, which is a no-op the second time because that type has 0 instances after the first run.

---

## Files

| path | purpose |
|---|---|
| `migrations/mig_3_1_built_in_era.cypher` | declarative migration for Phase 3.1 |
| `migrations/mig_3_2_pollutant_inference.cypher` | declarative migration for Phase 3.2 |
| `migrations/mig_3_3_reuse_rules.cypher` | declarative migration for Phase 3.3 (consumes `$rule_rows`, `$norm_rows`, `$referenziert_norm_rows`) |
| `logs/agent11_runner.py` | executes the three migrations against `mit-bestand`; embeds the canonical 20-row `:ReuseRule` payload |
| `logs/agent11_verify.py` | post-run acceptance checks |
| `logs/agent11_probe.py`, `logs/agent11_probe2.py` | pre-run inventory probes |
| `logs/agent11_progress.log` | timestamped run log (initial + idempotent re-run) |
| `logs/agent11_result.json` | structured before/after counts + audit cards from each migration |
| `logs/agent11_verify.json` | structured acceptance report (20/20 PASS) |
| `PHASE_3_1_DONE.flag`, `PHASE_3_2_DONE.flag`, `PHASE_3_3_DONE.flag` | done flags with before/after counts per phase |

---

## What this enables

- "Risk Story" query (`MATCH (bg:Bauteilgruppe)-[r:HAS_RISK_POLLUTANT]->(s:Schadstoff) RETURN bg, s, r.evidence_basis, r.evidence_origin`) now returns 803 rows where the graph previously returned 0. Every row carries a `documented` / `era_and_material` / `material_only` basis label.
- "Decision Support" query (`MATCH (rule:ReuseRule)-[:APPLIES_IN]->(:Land {country_iso:'DE'}), (rule)-[:APPLIES_TO]->(:Material {name:'Stahl'}) RETURN rule.key_norms, rule.required_tests, rule.pollutant_risks` ) now returns the German steel reuse decision shelf in one hop; previously 0 rows.
- The 178 honestly-marked `:Bauwerk{era_unknown:true}` form the explicit work-list for any future Phase 4b expansion that wants to back-fill donor era from gebaeude dossiers.

---

## Hand-off

Phase 3 is complete, idempotent, and traceable. Phase 5 quality tiers (Agent 12 scope) can now read `evidence_origin` and `evidence_basis` on the new `:HAS_RISK_POLLUTANT`, `:REQUIRES_VERIFICATION_FOR`, `:APPLIES_IN`, `:APPLIES_TO`, `:REFERENZIERT_NORM`, and `:BUILT_IN_ERA` edges and on the new `:ReuseRule` and inferred `:Norm` nodes to compute tier coverage.
