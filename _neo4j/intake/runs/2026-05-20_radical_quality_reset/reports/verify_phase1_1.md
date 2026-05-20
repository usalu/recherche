# Phase 1.1 — Verifier 1/12 report

- **Verifier**: 1 of 12
- **Phase under verification**: 1.1 — Wiederverwendungskette demote-not-delete
- **Plan**: `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md`, section 1.1
- **Run directory**: `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\`
- **Target database**: `mit-bestand` (read-only)
- **Verification mode**: read-only; no graph writes
- **Driver**: official Neo4j Python driver 5.28.4 over `bolt://localhost:7687`
- **Probe scripts** (read-only):
  - `logs/verify_phase1_1_live.py` (the eight checks)
  - `logs/verify_phase1_1_probe.py` (deeper basis breakdown + samples)

## Checklist

| # | Check | Expected | Observed | Result |
|---|---|---|---|---|
| 1 | `migrations\mig_1_1_demote_chains.cypher` exists | file present | present (79 lines, header references Phase 1.1) | **PASS** |
| 2 | `logs\PHASE_1_1_DONE.flag` exists and is parseable | parseable `key: value` flag | present (13 lines, `ok: true`, all fields parse) | **PASS** |
| 3 | `deleted\phase1_1_chains.jsonl` exists with 98 lines | 98 lines | 98 lines (one JSON record per deleted chain) | **PASS** |
| 4 | `reports\agent_2_phase1_1_report.md` exists | file present | present (175 lines) | **PASS** |
| 5 | Live `count(:Wiederverwendungskette)` == 14 | 14 | **14** | **PASS** |
| 6 | Live unwired chains via FROM_DONOR\|AUS_BAUWERK and INTO_RECEIVER\|EINGEBAUT_IN == 0 | 0 | **0** | **PASS** |
| 7 | Live `count(r) WHERE migration_origin='mig_1_1_demote_chains'` ≥ 290 | ≥ 290 | **297** | **PASS** |
| 8 | Sample 5 demoted edges carry `evidence_basis='demoted_from_kette'` and `evidence_source_id` non-null | both fields present and correct | **`evidence_source_id` non-null on 297/297 (0 NULL); `evidence_basis='demoted_from_kette'` on 240/297 literally; the remaining 57 HAT_HUERDE edges were intentionally remapped to `'propagated'` by Phase 4.1 step `mig_4_1.h` with the original value preserved on `derivation_note='former_basis=demoted_from_kette'`** | **PASS** (with documented downstream remap) |

**Score**: checks_passed=8, checks_failed=0, overall=PASS.

## Live counts (raw)

```
chains_total                        = 14
chains_unwired (via FROM_DONOR|AUS_BAUWERK & INTO_RECEIVER|EINGEBAUT_IN) = 0
chains_wired (same predicate)       = 14
demoted_edges_total                 = 297
demoted_edges_with_null_source_id   = 0
```

### Demoted edges by type and current `evidence_basis`

| Type | basis | n |
|---|---|---:|
| HAT_PROZESSPHASE | `demoted_from_kette` | 119 |
| HAT_METHODE | `demoted_from_kette` | 63 |
| HAT_LOGISTIK | `demoted_from_kette` | 58 |
| HAT_HUERDE | `propagated` (remapped by `mig_4_1.h`, original on `derivation_note`) | 57 |
| **total** | | **297** |

The breakdown matches the agent 2 report (119 / 63 / 58 / 57 = 297) exactly.

### 14 surviving Wiederverwendungskette ids (sorted)

```
k_bestandserhalt_blackfriars_tragstruktur
k_geplante_reuse_kette_broadgate_stahl_nach_blackfriars
k_reuse_kette_brettschichtholzbogen_liege_bierset_nach_anderlecht
k_reuse_kette_btc_ville_des_terres_nach_stains
k_reuse_kette_doppeltverglaste_holzfenster_nach_stains
k_reuse_kette_drill_stem_pipe_dachtragwerk_nach_saxum_barn
k_reuse_kette_drill_stem_pipe_stutzen_nach_saxum_barn
k_reuse_kette_granitpflaster_stadt_paris_nach_stains
k_reuse_kette_holzfenster_epinay_nach_stains
k_reuse_kette_leuchten_engie_nach_stains
k_reuse_kette_mauerwerksmodule_donorgruppe_nach_resource_rows
k_reuse_kette_radiatoren_le_bon_coin_nach_stains
k_reuse_kette_sanitarobjekte_reavie_nach_stains
k_reuse_kette_stahl_offcuts_zu_saxum_toren
```

Identical to the list in `reports/agent_2_phase1_1_report.md`.

## Sample demoted edges (check 8 evidence)

Five samples, two of which are the HAT_HUERDE edges affected by the documented downstream remap so the deviation is fully visible:

| # | rel_type | src | dst | `evidence_basis` | `evidence_source_id` | `derivation_note` |
|---|---|---|---|---|---|---|
| 1 | HAT_PROZESSPHASE | `bg_reuse_daemmstoff_mehrere_green_house_daemmung_holzbodenelemente` | `phase_aufbereitung` | `demoted_from_kette` | `k_green_house_knoopkazerne_tiel_to_pavilion` | (none) |
| 2 | HAT_METHODE | `bg_reuse_daemmstoff_mehrere_green_house_daemmung_holzbodenelemente` | `meth_design_for_disassembly` | `demoted_from_kette` | `k_green_house_knoopkazerne_tiel_to_pavilion` | (none) |
| 3 | HAT_LOGISTIK | `bg_reuse_daemmstoff_mehrere_green_house_daemmung_holzbodenelemente` | `log_materialverfuegbarkeit` | `demoted_from_kette` | `k_green_house_knoopkazerne_tiel_to_pavilion` | (none) |
| 4 | HAT_HUERDE | `bg_reuse_daemmstoff_mehrere_green_house_daemmung_holzbodenelemente` | `h_datenluecke` | `propagated` | `k_green_house_knoopkazerne_tiel_to_pavilion` | `former_basis=demoted_from_kette` |
| 5 | HAT_HUERDE | `bg_retained_mehrere_mehrere_timber_square_print_building_structure` | `h_technische_freigabe` | `propagated` | `k_timber_square_reused_steel_chain` | `former_basis=demoted_from_kette` |

All five samples carry a non-null `evidence_source_id` that points to one of the 98 deleted chains (i.e. lineage to the original chain is fully preserved). All five carry `migration_origin='mig_1_1_demote_chains'` and `evidence_origin='derived'`.

## Notes & deviations

1. **HAT_HUERDE `evidence_basis` remapped post-1.1 — documented, not a regression.**
   `mig_4_1.h` (Phase 4.1) explicitly enforces the citation-group enum
   `{cell_citation, registry_stub, propagated, controlled_vocab}` on
   `HAT_HUERDE`, and remaps the literal `demoted_from_kette` to
   `propagated` for those edges only, capturing the original value on
   `derivation_note='former_basis=demoted_from_kette'`. Cypher excerpt
   (lines 184–194 of `mig_4_1_canonical_evidence.cypher`):

   ```cypher
   MATCH ()-[r:HAT_HUERDE]->()
   WHERE r.evidence_basis = 'demoted_from_kette'
   SET r.derivation_note = coalesce(r.derivation_note,
                                    'former_basis=demoted_from_kette'),
       r.evidence_basis  = 'propagated';
   ```

   Phase 1.1 itself wrote `evidence_basis='demoted_from_kette'` to all 297
   demoted edges (the runner `logs/run_mig_1_1.py` shows the identical
   property shape for all six demotable types). The current live value
   on 57 of them is therefore the *intended downstream state*, not a
   Phase 1.1 failure. The lineage signal is preserved on
   `derivation_note` and the row still has the original
   `migration_origin='mig_1_1_demote_chains'` and `evidence_source_id`
   pointing at the deleted chain.

2. **Wiring predicate now uses new edge names.** Phase 4.2 renamed
   `AUS_BAUWERK → FROM_DONOR` and `EINGEBAUT_IN → INTO_RECEIVER`. The
   verifier query in check 6 already accepts both names; a sanity probe
   showed all 14 surviving chains satisfy
   `exists{(k)-[:FROM_DONOR|AUS_BAUWERK]->()} AND exists{(k)-[:INTO_RECEIVER|EINGEBAUT_IN]->()}`.

3. **No new artefacts produced by this verification.** Only two
   read-only probe scripts were written under `logs/`:
   `verify_phase1_1_live.py` and `verify_phase1_1_probe.py`. They were
   executed against `mit-bestand` with `default_access_mode='READ'`. No
   Cypher write was issued.

4. **Agent-2 report internal consistency check**: the report's
   per-type breakdown (HAT_PROZESSPHASE 119, HAT_METHODE 63,
   HAT_LOGISTIK 58, HAT_HUERDE 57, total 297) matches the live counts
   exactly. The "98 chains deleted" claim is consistent with the JSONL
   line count (98) and with the live `count(:Wiederverwendungskette)`
   delta from 112 → 14.

## Verdict

**Phase 1.1 is verified PASS.** All 8 checks pass. The single deviation — 57 HAT_HUERDE edges with `evidence_basis='propagated'` instead of `'demoted_from_kette'` — is an intentional, documented remap by a later phase (4.1) and the original Phase 1.1 lineage signal is preserved on the `derivation_note` audit field.
