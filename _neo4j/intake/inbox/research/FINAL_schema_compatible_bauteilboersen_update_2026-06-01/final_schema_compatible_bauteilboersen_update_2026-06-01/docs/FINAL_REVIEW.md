# Final review — Bauteilbörsen Swiss/schema-compatible update

Generated/finalised: 2026-06-01

- Import actors: 16
- Import actors with 2+ evidence URLs: 16 / 16
- Strict material/type rows: 98
- Strict material rows: 22
- Strict Bauteiltyp rows: 76
- Off-vocabulary review rows kept out of import: 6

## Actor readiness

| anchor_id | evidence URLs | material edges | bauteiltyp edges | status |
|---|---:|---:|---:|---|
| `bauteilboerse_basel_overall` | 4 | 1 | 4 | OK |
| `wick_reuse_roto_baumarkt` | 3 | 2 | 5 | OK |
| `btvz_zuerichsee_oberland` | 4 | 2 | 5 | OK |
| `reuzi_ch` | 3 | 2 | 5 | OK |
| `materiuum_geneve_ressourcerie` | 4 | 4 | 8 | OK |
| `gruner_reuse_platform` | 4 | 0 | 8 | OK |
| `syphon_ag_bauteilboerse_biel_bruegg` | 3 | 0 | 4 | OK |
| `hiltbrunner_reuse_riedtwil_wiederverwendung` | 3 | 0 | 4 | OK |
| `bauteilverwertung_koeppel_klein` | 3 | 0 | 4 | OK |
| `archipel_sion_ressourcerie` | 3 | 5 | 6 | OK |
| `ressourcerie_lausanne_materiuum_ruul` | 3 | 2 | 4 | OK |
| `la_ressourcerie_fribourg` | 3 | 3 | 4 | OK |
| `ggzatwork_laden2_bauteile_zug` | 3 | 0 | 4 | OK |
| `stiftung_chance_bauteile_zuerich_glattbrugg` | 3 | 0 | 2 | OK |
| `salza` | 3 | 0 | 0 | OK |
| `baumatpool_ch` | 3 | 1 | 9 | OK |

## Decision

This package is ready for a schema-compatible Neo4j import, assuming the controlled-vocabulary nodes from the existing Bauteilbörse subgraph are already present. Generic material evidence such as `Metall` or `Baumaterialien` was not imported because those IDs are outside the current closed Material vocabulary.