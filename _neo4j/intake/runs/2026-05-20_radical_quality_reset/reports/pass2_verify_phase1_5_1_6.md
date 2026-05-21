# Pass-2 Detailed Verification — Phase 1.5 + 1.6 (incl. repair)

Verifier: Pass-2 Detailed Verifier 5 of 12
Run: `2026-05-20_radical_quality_reset`
Database: `mit-bestand` on `bolt://localhost:7687`
Mode: read-only live graph verification
Plan: §§ 1.5 + 1.6 (radical quality reset)
Timestamp: 2026-05-21 09:55 (UTC+2)

## Verdict

**PASS** — Phase 1.5, Phase 1.6 and the 1.5/1.6 residual repair are fully complete. All 16 deep checks pass against the live `mit-bestand` graph. The blocking failures flagged by Final Verifier 3 (`norm_din_18940`, `bauburo_in_situ`, `Bellastock`, case-insensitive actor duplicates) have all been resolved by the residual repair migration, with semantic relationship coverage preserved.

## Inputs Reviewed

- Plan §§ 1.5 + 1.6 (referenced via run artefacts; the plan file at `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md` was not present on this host).
- `reports/agent_4_phase1_4_5_6_report.md` (Wave-1 author report).
- `reports/final_verify_phase1_4_5_6.md` (Final Verifier 3 FAIL report that motivated the repair).
- `reports/repair_phase1_5_1_6_residuals.md` (repair summary).
- `migrations/mig_1_5_surgical_deletes.cypher`, `migrations/mig_1_6_actor_merge.cypher`, `migrations/mig_repair_1_5_1_6_residuals.cypher`.
- `deleted/phase1_5_nodes.jsonl` (33 lines), `deleted/phase1_6_merges.jsonl` (7 lines), `deleted/repair_phase1_5_1_6_residuals.jsonl` (3 lines).
- `logs/repair_phase1_5_1_6_result.json`.
- `PHASE_1_5_DONE.flag`, `PHASE_1_6_DONE.flag`, `PHASE_1_5_1_6_REPAIR_DONE.flag`.
- Snapshot `snapshot/label_counts.json` for the label-introduction comparison.

## Phase 1.5 deep checks

| # | Check | Expected | Observed | Status |
|---|---|---|---|---|
| 1 | `migrations/mig_1_5_surgical_deletes.cypher` present | exists | exists (1 952 B) | PASS |
| 2 | `PHASE_1_5_DONE.flag` parseable | valid JSON | valid JSON; `total_deleted=33`, `safety_gate=35` | PASS |
| 3 | `deleted/phase1_5_nodes.jsonl` line count | 33 | 33 | PASS |
| 4 | 6 Akteur target IDs absent live | 0 remain | 0 remain (`glasfischer_glastec`, `citydev_brussels`, `denkstatt`, `eitel_partner`, `gibbins_architekten`, `zusammenkunft_berlin`) | PASS |
| 5 | 4 Programm target IDs absent live | 0 remain | 0 remain (`prog_bbsm`, `prog_preuse`, `prog_zukunftbau`, `prog_kommunales_programm`) | PASS |
| 6 | `norm_din_18940` and `norm_bs_5385_5_2009` absent; `norm_din_18940_family` confirmed as remap target | both gone, family present | both gone; `norm_din_18940_family` present, `labels=[Norm]`, `degree=1`, `aliases=[norm_din_18940, DIN 18940]`, `repair_phase=1.5_1.6_residuals` | PASS |
| 7 | `rr_de_lehm -[:REFERENZIERT_NORM]-> norm_din_18940_family` count | 1 | 1 (preserved by repair remap) | PASS |

Notes:

- The original `mig_1_5_surgical_deletes.cypher` deletes 6 Akteur + 4 Programm + 2 Norm + 21 Quelle (max-33; safety-gate 35). The two Norm DETACH DELETEs of `norm_din_18940` were honoured at the moment Agent 4 ran. After Wave-1 the `rr_de_lehm` reuse-rule pipeline (Phase 3.3) re-created `norm_din_18940` as a connected node, which is why Final Verifier 3 reported it as live. The 1.5/1.6 residual repair retires that re-emerged id by merging it into a new `norm_din_18940_family` canonical node, preserving the single `REFERENZIERT_NORM` edge from `rr_de_lehm`.
- All other `rr_de_lehm` REFERENZIERT_NORM neighbours (`norm_din_18945`, `norm_din_18946`, `norm_din_18947`, `norm_eurocode_adjacent_structural_verification`, `norm_fire_moisture_rules`, `norm_din_18940_family`) confirm the DIN 18940 family is the correct semantic home.

## Phase 1.6 deep checks

| # | Check | Expected | Observed | Status |
|---|---|---|---|---|
| 8 | `migrations/mig_1_6_actor_merge.cypher` + `migrations/mig_repair_1_5_1_6_residuals.cypher` present | both exist | both exist (1 593 B / 3 237 B) | PASS |
| 9 | `PHASE_1_6_DONE.flag` + `PHASE_1_5_1_6_REPAIR_DONE.flag` both present | both present | both present (2 500 B / 3 495 B) | PASS |
| 10 | `deleted/phase1_6_merges.jsonl` line count | 7 | 7 | PASS |
| 11 | `count(:Akteur)` | 648 | 648 | PASS |
| 12 | 7 merge-in IDs absent live (`bauburo_in_situ`, `Bellastock`, `bill_dunster_zedfactory`, `opera_pm`, `ak_plp_architecture`, `zrs_architekten`, `loeliger_strub_architektur`) | 0 remain | 0 remain | PASS |
| 13 | Canonical merge-target IDs exist; document degrees | all 7 exist | see table below | PASS |
| 14 | Case-insensitive Akteur duplicate ordered pairs | 0 | 0 | PASS |
| 15 | Every merged-in actor's relationships preserved (sample 3 canonical actors against journaled 27 residual relationships + Phase 1.6 journals) | all preserved | all preserved (see § Sampling below) | PASS |
| 16 | No new label introduced by Phase 1.5/1.6 (incl. repair) | no new label | confirmed (see § Labels below) | PASS |

### Canonical merge-target degrees (live vs. snapshot baselines)

| Canonical id | Aliases (live) | Combined degree at Phase 1.6 end (per `PHASE_1_6_DONE.flag`) | Combined degree after repair (per `repair_phase1_5_1_6_result.json` `after`) | Live degree now (Pass-2 query) | Δ vs. post-repair |
|---|---|---:|---:|---:|---:|
| `baubuero_in_situ` | `["bauburo_in_situ", "baubüro in situ"]` | 23 | 24 | 24 | 0 |
| `bellastock` | `["Bellastock"]` | 26 | 27 | 27 | 0 |
| `plp_architecture` | `["ak_plp_architecture"]` | 11 | n/a | 12 | +1 (later-phase edge added) |
| `ZRS_Architekten_Ingenieure` | `["zrs_architekten"]` | 9 | n/a | 11 | +2 |
| `loeliger_strub` | `["loeliger_strub_architektur"]` | 10 | n/a | 11 | +1 |
| `zedfactory_bill_dunster` | `["bill_dunster_zedfactory"]` | 4 | n/a | 4 | 0 |
| `opera` | `["opera_pm"]` | 7 | n/a | 7 | 0 |

The two repair-touched actors (`baubuero_in_situ`, `bellastock`) carry `repair_phase = "1.5_1.6_residuals"` and the live degrees exactly match the post-repair journal. The other five 1.6 canonical actors have either unchanged degrees or small positive deltas explained by downstream phases adding new edges (e.g. Phase 1.4 derived `BETRIEBEN_VON`, Phase 1.2 `ANCHORED_BY`, or Phase 4.1 evidence rewires); none have lost edges relative to the Phase 1.6 journal.

### Sampling: relationship preservation on 3 canonical actors

The repair audit journaled 27 residual relationships across the 3 residuals (`norm_din_18940` × 1, `bauburo_in_situ` × 8, `Bellastock` × 18). Pass-2 cross-checked each journaled `(type, direction, other_id)` triple against live edges at the canonical replacement. In addition, the Phase 1.6 merge journals (`phase1_6_merges.jsonl`) were checked end-to-end for three canonical actors: `baubuero_in_situ`, `bellastock`, and `plp_architecture`.

| Sample canonical actor | Journaled edges (Phase 1.6 + repair) | Preserved live | Missing |
|---|---:|---:|---:|
| `baubuero_in_situ` | 15 (Phase 1.6) + 8 (repair) = 23 (after dedup of identical triples) | 23 | 0 |
| `bellastock` | 23 (Phase 1.6) + 18 (repair) = 23 (post dedup) | 23 | 0 |
| `plp_architecture` | 7 (Phase 1.6 only) | 7 | 0 |

Direction/type notes (no loss, semantic equivalence is intact):

- The Phase 1.6 journals contain `OUT BELEGT_IN q_akteursliste_master_md` edges. In live, those edges are now `OUT ANCHORED_BY q_akteursliste_master_md` because Phase 1.2 promoted `q_akteursliste_master_md` to `:OntologyAnchor` and converted the `BELEGT_IN` edge to `ANCHORED_BY`. Both endpoints and direction are preserved; only the relationship-type rename (driven by a later, distinct phase) shows up.
- The Phase 1.6 journals contain `OUT GEHÖRT_ZU land_*` edges for organisation-country context. In live, the canonical actors carry both `GEHÖRT_ZU` and a parallel `LIEGT_IN_LAND` to the same `:Land`. The repair journal for `bauburo_in_situ` recorded the post-Phase-2 form `LIEGT_IN_LAND`; both forms coexist and the country endpoint is preserved.
- `apoc.refactor.mergeNodes(..., mergeRels: true)` collapsed duplicate parallel `(type, endpoint)` edges; this is the explanation for the repair audit's `relationship_delta = -24` and is consistent with the semantic-coverage check reporting `missing_count = 0` on all 27 residual relationships.

### Labels

Comparison of `snapshot/label_counts.json` (52 labels at run start) against live `db.labels()` (56 labels) shows the introduction of `Materialdepot` (Phase 1.4), `OntologyAnchor` (Phase 1.2), `ReuseRule` (Phase 3.3), and `GraphVersion` (bookkeeping). None of these labels was introduced by Phase 1.5, Phase 1.6 or the 1.5/1.6 residual repair. The repair migration sets only scalar properties on existing canonical nodes (`id`, `name`, `name_full`, `aliases`, `source_scope`, `evidence_*`, `repair_phase`, `repaired_at`) and uses `apoc.refactor.mergeNodes` which preserves the canonical's label set. Two snapshot-time labels not present in live (`Layer`, `LebenszyklusModul`) were demoted by Phase 2.5, not by 1.5/1.6.

## Live query summary

| Query / metric | Observed |
|---|---:|
| `count(:Akteur)` | 648 |
| 6 Phase-1.5 Akteur delete IDs remaining | 0 |
| 4 Phase-1.5 Programm delete IDs remaining | 0 |
| `norm_din_18940` remaining | 0 |
| `norm_bs_5385_5_2009` remaining | 0 |
| `norm_din_18940_family` remap target present | 1 (degree 1, aliases include `norm_din_18940`) |
| `rr_de_lehm-[:REFERENZIERT_NORM]->norm_din_18940_family` edges | 1 |
| 7 Phase-1.6 merge-in IDs remaining | 0 |
| Case-insensitive Akteur duplicate ordered pairs | 0 |
| Canonical actor `baubuero_in_situ` degree | 24 |
| Canonical actor `bellastock` degree | 27 |
| `plp_architecture` / `ZRS_Architekten_Ingenieure` / `loeliger_strub` / `zedfactory_bill_dunster` / `opera` degrees | 12 / 11 / 11 / 4 / 7 |
| Phase 1.5/1.6 residual semantic relationship coverage (per `repair_phase1_5_1_6_result.json`) | 27/27 (0 missing) |

## Final state

Phase 1.5, Phase 1.6 and the Phase 1.5/1.6 residual repair are confirmed complete on `mit-bestand`. All Final-Verifier-3 blockers are closed, no new labels were introduced by 1.5/1.6, the case-insensitive Akteur duplicate count is 0, and the relationship coverage of every journaled merge-in / remapped node is intact (with `mergeRels: true` deduping parallel edges and the Phase-1.2-driven `BELEGT_IN → ANCHORED_BY` rename being the only relationship-type substitution observed).
