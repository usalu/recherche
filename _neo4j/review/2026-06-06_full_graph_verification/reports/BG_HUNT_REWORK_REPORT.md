# BG Hunt Rework Campaign Report

**Generated:** 2026-06-07T16:09:42Z · **Database:** `mit-bestand`

## Scope
- Non-PROVEN catalogue bg_ edges: **823**

## Phase A (dossier re-score, no network)
| verdict | count |
|---|---:|
| PROVEN | 473 |
| PARTIAL | 262 |
| UNSUPPORTED | 88 |

## Merged outcomes
| verdict | count |
|---|---:|
| PROVEN | 473 |
| PARTIAL | 262 |
| UNSUPPORTED | 88 |

- PROVEN upgrades (patch-eligible): **473**
- ESCALATE_HUMAN (bundle policy): **0**
- New PROVEN (from non-PROVEN): **473**

## v8 → v9 bg_ rels
- v8 PROVEN: **5797** (86.73%)
- v9 PROVEN: **6270** (93.81%)

## Verdict deltas (overlay)
| transition | count |
|---|---:|
| UNSUPPORTED->PROVEN | 295 |
| PARTIAL->PROVEN | 178 |
| UNSUPPORTED->PARTIAL | 173 |

## Patch dry-run
- Ops: **473** · status: **ok**

## Regression (prior applied PROVEN)
- Failures: **2**
- `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1157505368583045620` → PARTIAL
- `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153001768955674869` → PARTIAL

## Sample new PROVEN (audit)

- `bg_stahl_mehrere_55gss_external_core` → `bt_traeger` (HAT_BAUTEILTYP): "Reused steel profiles for external core Stahlprofile für neuen externen Kern str..."
- `bg_stahl_mehrere_55gss_external_core` → `mat_stahl` (NUTZT_MATERIAL): "Retrofit/extension with reused steel in new external service and circulation cor..."
- `bg_stahlbeton_mehrere_groeditz_dresden_type_precast_components` → `bt_decke` (HAT_BAUTEILTYP): "wiederverwendete fertigteile anzahl: 438 Reused Dresden-type precast concrete co..."
- `bg_stahlbeton_mehrere_groeditz_dresden_type_precast_components` → `bt_treppe` (HAT_BAUTEILTYP): "Thinner representation of built sports/association house using reused precast co..."
- `bg_stahlbeton_mehrere_groeditz_dresden_type_precast_components` → `bt_wand` (HAT_BAUTEILTYP): "wiederverwendete fertigteile anzahl: 438 Reused Dresden-type precast concrete co..."
- `bg_stahlbeton_mehrere_groeditz_wbs70_precast_panels` → `bt_decke` (HAT_BAUTEILTYP): "wiederverwendete fertigteile anzahl: 438 Reused Dresden-type precast concrete co..."
- `bg_stahlbeton_mehrere_groeditz_wbs70_precast_panels` → `bt_wand` (HAT_BAUTEILTYP): "wiederverwendete fertigteile anzahl: 438 Reused Dresden-type precast concrete co..."
- `bg_stahlbeton_mehrere_groeditz_dresden_type_precast_components` → `mat_stahlbeton` (NUTZT_MATERIAL): "wiederverwendete fertigteile anzahl: 438 Reused Dresden-type precast concrete co..."
- `bg_stahlbeton_mehrere_groeditz_wbs70_precast_panels` → `mat_stahlbeton` (NUTZT_MATERIAL): "wiederverwendete fertigteile anzahl: 438 Reused Dresden-type precast concrete co..."
- `bg_stahlbeton_mehrere_plauen_iw73_6_precast_components` → `bt_boden` (HAT_BAUTEILTYP): "wiederverwendete fertigteile anzahl: 189 Reused IW73/6 precast concrete componen..."
- `bg_stahlbeton_mehrere_plauen_iw73_6_precast_components` → `bt_decke` (HAT_BAUTEILTYP): "wiederverwendete fertigteile anzahl: 189 Reused IW73/6 precast concrete componen..."
- `bg_stahlbeton_mehrere_plauen_iw73_6_precast_components` → `bt_wand` (HAT_BAUTEILTYP): "wiederverwendete fertigteile anzahl: 189 Reused IW73/6 precast concrete componen..."
- `bg_stahlbeton_mehrere_plauen_iw73_6_precast_components` → `mat_stahlbeton` (NUTZT_MATERIAL): "Thinner representation of built sport/association house reusing IW73/6 precast c..."
- `bg_glas_mehrere_awm_partitions_doors` → `bt_tuer` (HAT_BAUTEILTYP): "Reused glass partitions and doors Glastrennwände und Türen partitions and doors ..."
- `bg_glas_mehrere_awm_partitions_doors` → `bt_wand` (HAT_BAUTEILTYP): "Reused glass partitions and doors Glastrennwände und Türen partitions and doors ..."

## Artifacts
- `E:\recherche\_neo4j\review\2026-06-06_full_graph_verification\ledger\bg_hunt_rework_a.csv`
- `E:\recherche\_neo4j\review\2026-06-06_full_graph_verification\ledger\bg_hunt_rework_b.csv`
- `E:\recherche\_neo4j\review\2026-06-06_full_graph_verification\ledger\bg_hunt_rework_merged.csv`
- `E:\recherche\_neo4j\review\2026-06-06_full_graph_verification\patches\bg_hunt_rework_upgrades.patch.jsonl`
- `E:\recherche\_neo4j\review\2026-06-06_full_graph_verification\VERIFICATION_LEDGER_ELEMENT_v9.csv`
