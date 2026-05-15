# Round 002 Controlled Vocabulary Review: ZertifizierungBewertungssystem + Programm + Tool + Software

**Generated:** 2026-05-15
**Baseline reference:** [`../round_002_baseline/global_audit_report.md`](../round_002_baseline/global_audit_report.md)

## Result in Context

Clean family. 7 + 15 + 6 + 7 = 35 nodes total, no same-name duplicates, no
hidden id-form duplicates. 8 orphans, all kept as proposed seed.

The `tool_qflow` / `software_qflow` pair *looks* like a duplicate at first
glance but is actually a **deliberate dual-modeling pattern**: the same
product (qflow) is registered both as a `Tool` and as a `Software` so it
can be referenced via `NUTZT_TOOL` and `NUTZT_SOFTWARE` from project and
Bauteilgruppe nodes. Both nodes are cross-linked (`tool_qflow →
NUTZT_SOFTWARE → software_qflow` and `software_qflow → NUTZT_TOOL →
tool_qflow`). No patch action.

## ZertifizierungBewertungssystem hub snapshot (live `mit-bestand`)

| id | name | inbound |
| --- | --- | ---: |
| zbs_breeam | BREEAM | 3 |
| zbs_nabers | NABERS | 2 |
| zbs_well | WELL | 2 |
| zbs_dgnb | DGNB | 1 |
| zbs_nordic_swan_ecolabel | Nordic Swan Ecolabel / Svanemärket | 1 |
| zbs_paris_proof | Paris_Proof | 1 |
| zbs_leed | LEED | 0 (seed) |

## Programm hub snapshot (live `mit-bestand`)

| id | name | inbound |
| --- | --- | ---: |
| prog_pilotprojekt | Pilotprojekt | 9 |
| prog_forschungsprojekt | Forschungsprojekt | 6 |
| prog_recreate | ReCreate | 3 |
| prog_expo_2000 | EXPO 2000 Hannover | 2 |
| prog_foerderprogramm | Foerderprogramm | 2 |
| prog_wettbewerb | Wettbewerb | 2 |
| prog_fcrbe | FCRBE | 1 |
| prog_recreate_local | ReCreate Finnish cluster mini-pilot | 1 |
| prog_bbsm | BBSM | 0 (seed) |
| prog_interreg_nwe | Interreg_North_West_Europe | 0 (seed) |
| prog_kommunales_programm | Kommunales_Programm | 0 (seed) |
| prog_preuse | PREUSE | 0 (seed) |
| prog_reallabor | Reallabor | 0 (seed) |
| prog_reallabor_be_ware | Reallabor_Be_Ware | 0 (seed) |
| prog_zukunftbau | Zukunftbau | 0 (seed) |

## Tool hub snapshot (live `mit-bestand`)

| id | name | inbound |
| --- | --- | ---: |
| tool_qflow | Qflow delivery and waste ticket tracking | 5 |
| tool_bauteilkatalog | Bauteilkatalog / Bauteilpass | 2 |
| tool_bim_bauteilkatalog | BIM / digitaler Bauteilkatalog | 2 |
| tool_hts_stockmatcher | HTS Reused Steel Stockmatcher | 2 |
| tool_material_passports_maconda | Material passports / Maconda data workflow | 2 |
| tool_oogstkaart_harvest_map | Oogstkaart / Harvest Map logic | 1 |

## Software hub snapshot (live `mit-bestand`)

| id | name | inbound |
| --- | --- | ---: |
| software_concular | Concular | 9 |
| software_restado | Restado | 9 |
| software_qflow | Qflow | 5 |
| software_bim | Building Information Modeling / BIM | 2 |
| software_recrete_finite_element_model | Finite-Elemente-Modell / FE-Modell | 2 |
| software_inies | INIES | 1 |
| software_risa_3d | RISA-3D | 1 |

## Same-name duplicates

None.

## Orphan check

| label | id | note |
| --- | --- | --- |
| ZertifizierungBewertungssystem | zbs_leed | well-known certification — keep |
| Programm × 7 | prog_bbsm, prog_interreg_nwe, prog_kommunales_programm, prog_preuse, prog_reallabor, prog_reallabor_be_ware, prog_zukunftbau | program names that may surface in future projects — keep |

## Candidate patch

`patches/controlled_vocabulary_zertifizierung.patch.jsonl` — 1 `noop_reviewed`.

## Human decision queue

- `tool_qflow` and `software_qflow`: confirmed as **deliberate dual-modeling**.
  No merge. Consider documenting this pattern in
  `_neo4j/neo4j_iterative_review_plan/plans/00_MASTER_REVIEW_STRATEGY.md`
  so future agents don't misread it as a duplicate.

## Acceptance status

- Live DB reachable: yes (`mit-bestand`).
- Active patch is UTF-8 LF, dry-run safe.
- No deferred ops.
