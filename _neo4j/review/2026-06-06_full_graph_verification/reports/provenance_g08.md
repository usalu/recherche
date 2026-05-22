# Agent G8 — Git Provenance: 17 deleted Materialdepot placeholders

**Date:** 2026-06-06  
**Scope:** 17 `:Materialdepot` nodes removed by Quality Pass Q02 (EP-09 / R01 residuals)  
**Inputs:** [`ledger/quality_pass_q02.csv`](../ledger/quality_pass_q02.csv), [`ledger/remediation_r01.csv`](../ledger/remediation_r01.csv), [`reports/quality_pass_q02.md`](quality_pass_q02.md)  
**Ledger:** [`ledger/provenance_g08.csv`](../ledger/provenance_g08.csv)  
**Mode:** read-only git + repo; no graph mutation  

---

## 1. Executive summary

All 17 nodes trace to **project-batch `*.kg.jsonl` exports** (May 13–15 2026) where dossiers with **unspecified or multi-site donor provenance** were modelled as extra `:Bauwerk` nodes — explicit *Unbekannt* / *Aggregiert* / network-pool stubs wired via `AUS_BAUWERK` / `NUTZT_BAUWERK`. They were **never** created with `primary_source_url` or `source_urls`.

Lifecycle:

1. **Create** — per-project graph export under `intake/archive/2026-05-15_project_batches_legacy/` → consolidated to `processed/projects/records/` (commit `13c165fd`, 2026-05-15) → imported via `_scripts/import_jsonl_to_neo4j.py`.
2. **Relabel** — `2026-05-20_radical_quality_reset` Phase **1.4** (`mig_1_4_materialdepot.cypher`): 23 overloaded donor placeholders `:Bauwerk` → `:Materialdepot` (Agent 4).
3. **Deprecate** — `2026-06-06` Quality Pass **Q02**: 16 `delete_node` + 1 `merge_node` (`bw_externe_stahl_donor_stockholder` → `bw_cleveland_steel_and_tubes_stock`); WBS70 `AUS_SPENDER` redirected to `bw_school_type_dresden_donor`.

**Root-cause bucket (all 17):** `aggregate_stub` — intentional donor-pool abstraction, not missing URL remediation debt.

---

## 2. Donor-pool abstraction decision (documented)

### 2.1 Original modelling intent (batch exports)

When a reuse dossier names **reused material** but not a **discrete donor building or depot**, batch authors added a sibling `:Bauwerk` node so `AUS_BAUWERK` / `FROM_DONOR` edges had a graph target. Naming conventions make the abstraction explicit:

| Pattern | Example node | Typical `note` / `name` |
|---|---|---|
| **Unknown source** | `bw_maison_dna_unknown_brick_donor` | *Unbekannte Spenderquelle der wiederverwendeten Ziegel* |
| **Multi-site aggregate** | `bw_paris_material_sources_circular_pavilion` | *Aggregierte Pariser Materialquellen* + enumerated sites in `note` |
| **Supply network** | `bw_chiro_itterbeek_reuse_supply_network` | *Aggregierter Donor-/Lieferpool aus Franck, RotorDC, …* |
| **Donor building-group** | `bw_donor_gebaudegruppe_resource_rows_mauerwerk` | *abgebrochene / rückgebaute Gebäude, genaue Donoren zu prüfen* |
| **Waste stream** | `bw_unknown_demolition_wood_streams` | *als aggregierter Donorstrom modelliert* |

This pattern appears across batches (e.g. `p_musee_de_folklore_mouscron` uses *Aggregierter Donorknoten* in `note` for a related stub not in the Q02-17 set).

**Design trade-off:** preserve **topology** (BG → donor endpoint) and **honest uncertainty** in the node label rather than inventing a findable depot URL or leaving donor edges unwired.

### 2.2 Critical review (May 2026)

[`CRITICAL_REVIEW_AND_PLAN.md`](../../intake/runs/2026-05-20_radical_quality_reset/reports/CRITICAL_REVIEW_AND_PLAN.md) §4.1 diagnosed `:Bauwerk` overload: the same `AUS_BAUWERK` rel type pointed at stockholders, companies, networks, regional aggregates, and explicit *Unbekannt* placeholders. Phase **1.4** was the pragmatic relabel — not a semantic fix:

> Relabel 23 placeholder Bauwerke (`stock`/`pool`/`aggregiert`/`liefer`/`unbekannt`/`donor`/`depot`/`lager` patterns) → `:Materialdepot`. Bauwerk 209 → 186.

All 17 Q02 nodes appear in `mig_1_4_materialdepot.cypher` ID list.

### 2.3 Verification wave reversal (Jun 2026)

Agents **R01**, **10**, **09** re-adjudicated: no official page names these nodes as depots → `MISSING_EVIDENCE` / `ESCALATE_HUMAN`. **Q02** executed the human decision: **do not re-introduce aggregate Materialdepot stubs**; re-wire only when dossiers name discrete donor `Bauwerk` nodes ([`quality_pass_q02.md`](quality_pass_q02.md) §6).

**Policy going forward:** donor-pool abstractions belong in **dossier-level honesty** or future typed edges (e.g. `donor_resolution_status`), not as unsourced `:Materialdepot` nodes with `BELEGT_IN` → dossier only.

---

## 3. Git pickaxe (`git log -S <node_id>`)

Searched `--all` under `_neo4j/`, `_archive/`, `_scripts/`. Earliest hits cluster on **2026-05-13** batch-migration commits; later churn is consolidation (`13c165fd`), review exports (`f9cf1a8c`–`ed1d81d9`), and Q02 deletion artifacts.

| First-commit bucket | Commit | Date | Subject | Node count |
|---|---|---|---|---:|
| `neo4j migration 2` | `188ebdc5` | 2026-05-13 | neo4j migration 2 | 2 |
| `migration ready` | `15222140` | 2026-05-13 | migration ready | 6 |
| `migrate 3` | `3fa49bd7` | 2026-05-13 | migrate 3 | 3 |
| `migrate 5` | `5dd44245` | 2026-05-13 | migrate 5 | 5 |
| `restructure … data 2` | `d0ded72f` | 2026-05-15 | restructure and double checking data 2 | 1 |

Per-node earliest commits are in [`ledger/provenance_g08.csv`](../ledger/provenance_g08.csv) (`first_git_commit` column). Processed-path consolidation: **`13c165fd`** (2026-05-15, *restructure and double checking Data*) for 16/17; **`d0ded72f`** for `bw_wbs70_donor_groeditz`.

Post-deletion review churn: all 17 ids reappear in **`ed1d81d9`** (2026-06-06) via verification ledgers/patches — not re-creation.

---

## 4. Per-node provenance table

| node_id | placeholder class | source project | batch archive | Q02 action |
|---|---|---|---|---|
| `bw_berlin_fitout_donor_sources` | aggregate multi-site | `p_impact_hub_berlin_crclr_fitout` | batch_006 | delete |
| `bw_chiro_itterbeek_reuse_supply_network` | network pool | `p_chiro_d_itterbeek_dilbeek` | batch_003 | delete |
| `bw_donor_gebaudegruppe_resource_rows_mauerwerk` | donor group | `p_resource_rows_copenhagen` | batch_012 | delete |
| `bw_externe_stahl_donor_stockholder` | aggregate duplicate | `p_timber_square_london` | batch_013 | **merge** → Cleveland |
| `bw_holbein_grosvenor_donor_projects` | portfolio aggregate | `p_holbein_gardens_london` | batch_006 | delete |
| `bw_lo_reninge_reuse_brick_source` | unknown source | `p_lo_reninge_town_hall_facade` | batch_008 | delete |
| `bw_maison_des_canaux_unspecified_donors` | unknown source | `p_maison_des_canaux_paris` | batch_009 | delete |
| `bw_maison_dna_unknown_brick_donor` | unknown source | `p_maison_dna_asse` | batch_009 | delete |
| `bw_messebau_lager_hannover` | generic unverifiable | `p_recyclinghaus_hannover` | batch_011 | delete |
| `bw_p2_massenwohnungsbau_donor_unknown` | unknown source | `p_broethen_twin_house_hoyerswerda` | batch_003 | delete |
| `bw_paris_material_sources_circular_pavilion` | aggregate multi-site | `p_circular_pavilion_paris` | batch_004 | delete |
| `bw_paris_regional_donor_sources_ferme_du_rail` | regional aggregate | `p_ferme_du_rail_paris` | batch_005 | delete |
| `bw_unbekannte_donor_buildings_zinneke_material_lots` | unknown source | `p_zinneke_feder_masui4ever_brussels` | batch_014 | delete |
| `bw_unbekanntes_transformationsgebaeude_kellerwaende` | unknown source | `p_recrete_footbridge_reused_concrete_blocks` | batch_011 | delete |
| `bw_unknown_brick_donor_sources_gjg` | unknown source | `p_gjg_house_gentbrugge` | batch_005 | delete |
| `bw_unknown_demolition_wood_streams` | waste stream | `p_cascadeup_london_secondary_timber_glulam_demonstrator` | batch_003 | delete |
| `bw_wbs70_donor_groeditz` | building-type placeholder | `p_association_house_groeditz` | batch_015 | delete + redirect |

Full paths, commit hashes, and notes: **17 rows** in `ledger/provenance_g08.csv`.

---

## 5. Placeholder class breakdown

| Class | Count | Rationale |
|---|---:|---|
| `unknown_source` | 7 | Name contains *Unbekannt* / *unknown*; dossier admits donor not named |
| `aggregate_*` (multi-site, regional, portfolio, stream, group) | 8 | Multiple or unnamed donors pooled into one endpoint |
| `network_pool` | 1 | Chiro supply-network abstraction |
| `generic_unverifiable` | 1 | Messebau label without named depot |
| `aggregate_duplicate` | 1 | Timber Square external steel duplicates Cleveland node (merged not deleted) |

---

## 6. Method

1. Enumerated Q02-17 from `quality_pass_q02.csv` / `remediation_r01.csv` (R01-N-002…022 minus 5 PROVEN survivors).
2. Located canonical node definitions in `processed/projects/records/*.kg.jsonl` and matching `intake/archive/2026-05-15_project_batches_legacy/**/p_*.kg.jsonl`.
3. `git log --reverse -S<node_id>` on `_neo4j`, `_archive`, `_scripts` for first introduction; filtered review-only reappearances.
4. Cross-walked relabel (`mig_1_4_materialdepot.cypher`) and deprecation (`quality_pass_q02_deprecate.patch.jsonl`) from intake/review runs.
5. Classified placeholder type from node `name` / `name_full` / `note` and Agent 10/R01 adjudication text.

**No Neo4j writes.** Post-Q02 graph: **5** sourced `:Materialdepot` nodes remain (R01 PROVEN set).
