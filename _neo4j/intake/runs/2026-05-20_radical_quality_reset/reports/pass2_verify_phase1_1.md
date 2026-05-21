# Pass-2 Detailed Verification — Phase 1.1 (Verifier 1 of 12)

- **Phase**: 1.1 — `Wiederverwendungskette` demote-not-delete
- **Plan section**: `### 1.1 Wiederverwendungskette — demote-not-delete` in
  `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md`
- **Run dir**: `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\`
- **Database**: `mit-bestand` (live, read-only via Neo4j MCP `read-cypher`)
- **Verifier executed**: 2026-05-21
- **Mode**: Read-only (no writes performed)
- **Prior reports consumed**: `reports/agent_2_phase1_1_report.md`, `reports/final_verify_phase1_1.md`

## Summary

All **10** deep checks pass. Phase 1.1 is confirmed complete and consistent
against `mit-bestand`. The 297 demoted edges remain provenance-complete after
the downstream Phase-4 rename (`AUS_BAUWERK→FROM_DONOR`,
`EINGEBAUT_IN→INTO_RECEIVER`); the 14 surviving chains now expose the renamed
wiring, and no orphan `:Bauteilgruppe` was introduced by the demote.

## Check matrix

| # | Check | Expected | Observed | Result |
|---|-------|----------|----------|--------|
| 1 | `migrations/mig_1_1_demote_chains.cypher` present + idempotent | file present, idempotent semantics | file present (3 776 bytes). Idempotency: 1.1.b uses `apoc.merge.relationship(bg, type(r), {evidence_source_id: k.id}, shape, target, shape)` — re-run merges to existing demoted edge by `(bg, type, target, k.id)`; 1.1.c `DETACH DELETE` over the unwired-WHERE finds 0 matches after first run | **PASS** |
| 2 | `logs/PHASE_1_1_DONE.flag` parseable; `ok=true`, `chains_before=112`, `chains_after=14`, `chains_deleted=98`, `edges_demoted ≥ 290`, `unwired_remaining=0` | all literals match | parsed: `ok: true`, `chains_before: 112`, `chains_after: 14`, `chains_deleted: 98`, `edges_demoted: 297` (≥ 290), `unwired_remaining: 0` | **PASS** |
| 3 | `deleted/phase1_1_chains.jsonl` line-count == 98 | 98 | 98 | **PASS** |
| 4 | Live `count(:Wiederverwendungskette) == 14` | 14 | 14 | **PASS** |
| 5 | Every surviving chain has outgoing `FROM_DONOR` AND `INTO_RECEIVER` (no unwired chain) | 14/14 wired, 0 unwired | 14/14 wired (all chain IDs match the surviving set from `mig_1_1_counts.json`); unwired-count query returns 0 | **PASS** |
| 6 | Live edges with `migration_origin='mig_1_1_demote_chains'` ≥ 290; breakdown by type | ≥ 290 | **297** (HAT_PROZESSPHASE 119, HAT_METHODE 63, HAT_LOGISTIK 58, HAT_HUERDE 57) — identical to `logs/mig_1_1_counts.json` `edges_demoted_by_type` | **PASS** |
| 7 | Every demoted edge has non-null `evidence_source_id` AND (`evidence_basis='demoted_from_kette'` OR `derivation_note CONTAINS 'former_basis=demoted_from_kette'`) | 297/297 | 297/297 satisfy. `evidence_source_id` non-null on all 297. 240 carry `evidence_basis='demoted_from_kette'`; the remaining 57 carry `evidence_basis='propagated'` with `derivation_note='former_basis=demoted_from_kette'` (Phase 1.3 re-flagged the HAT_HUERDE bucket as `propagated` but preserved the demote trace via `derivation_note`) | **PASS** |
| 8 | No `:Bauteilgruppe` became orphan (every BG retains ≥ 1 project edge or chain edge) | 0 orphans | 0 orphans across all 369 `:Bauteilgruppe` nodes | **PASS** |
| 9 | `HAT_BAUTEILGRUPPE` edge count consistent before/after (none lost) | invariant | invariant. Phase 1.1 touches only `(chain)-[:HAT_*]->(target)` edges, never `:HAT_BAUTEILGRUPPE`. The 98-chain pre-delete snapshot (`deleted/phase1_1_chains.jsonl`) contains **0** `HAT_BAUTEILGRUPPE` mentions → none could be deleted by `DETACH DELETE`. Live count today: **369** | **PASS** |
| 10 | Sample 10 demoted edges with full property dump | dump captured | 10 edges sampled spanning all 4 demoted types (see below) | **PASS** |

## Live counts (mit-bestand)

```
MATCH (k:Wiederverwendungskette) RETURN count(k)
  -> 14

MATCH (k:Wiederverwendungskette)
WHERE NOT (exists{(k)-[:FROM_DONOR]->()} AND exists{(k)-[:INTO_RECEIVER]->()})
RETURN count(k)
  -> 0

MATCH ()-[r]->() WHERE r.migration_origin='mig_1_1_demote_chains'
RETURN type(r), count(r)
  -> HAT_PROZESSPHASE 119
  -> HAT_METHODE       63
  -> HAT_LOGISTIK      58
  -> HAT_HUERDE        57
  -> total            297

MATCH ()-[r:HAT_BAUTEILGRUPPE]->() RETURN count(r) -> 369

MATCH (bg:Bauteilgruppe)
WITH bg, exists{ ()-[:HAT_BAUTEILGRUPPE]->(bg) } AS has_proj,
         exists{ (bg)-[:TEIL_VON_KETTE]->(:Wiederverwendungskette) } AS has_chain
WHERE NOT has_proj AND NOT has_chain
RETURN count(bg) -> 0
```

## 14 surviving chains — wiring summary

All 14 have **both** `FROM_DONOR` and `INTO_RECEIVER`; none retain the
pre-Phase-4 `AUS_BAUWERK` / `EINGEBAUT_IN` types:

| Chain ID | FROM_DONOR | INTO_RECEIVER |
|----------|:----------:|:-------------:|
| `k_bestandserhalt_blackfriars_tragstruktur` | yes | yes |
| `k_geplante_reuse_kette_broadgate_stahl_nach_blackfriars` | yes | yes |
| `k_reuse_kette_brettschichtholzbogen_liege_bierset_nach_anderlecht` | yes | yes |
| `k_reuse_kette_btc_ville_des_terres_nach_stains` | yes | yes |
| `k_reuse_kette_doppeltverglaste_holzfenster_nach_stains` | yes | yes |
| `k_reuse_kette_drill_stem_pipe_dachtragwerk_nach_saxum_barn` | yes | yes |
| `k_reuse_kette_drill_stem_pipe_stutzen_nach_saxum_barn` | yes | yes |
| `k_reuse_kette_granitpflaster_stadt_paris_nach_stains` | yes | yes |
| `k_reuse_kette_holzfenster_epinay_nach_stains` | yes | yes |
| `k_reuse_kette_leuchten_engie_nach_stains` | yes | yes |
| `k_reuse_kette_mauerwerksmodule_donorgruppe_nach_resource_rows` | yes | yes |
| `k_reuse_kette_radiatoren_le_bon_coin_nach_stains` | yes | yes |
| `k_reuse_kette_sanitarobjekte_reavie_nach_stains` | yes | yes |
| `k_reuse_kette_stahl_offcuts_zu_saxum_toren` | yes | yes |

Set matches the surviving-chain list in `reports/agent_2_phase1_1_report.md`.

## Demoted-edge type distribution

| Type | Live count | `mig_1_1_counts.json` |
|------|-----------:|----------------------:|
| HAT_PROZESSPHASE | 119 | 119 |
| HAT_METHODE      |  63 |  63 |
| HAT_LOGISTIK     |  58 |  58 |
| HAT_HUERDE       |  57 |  57 |
| **total**        | **297** | **297** |

No drift since the Phase 1.1 write. No `HAT_STATUS` or
`HAT_WIEDERVERWENDUNGSART` demoted edges exist (correctly — the 98 unwired
chains carried none of those payloads, per `agent_2_phase1_1_report.md`).

## Provenance composition (297 demoted edges)

| Field | Coverage |
|-------|---------:|
| `evidence_source_id` non-null | 297 / 297 |
| `evidence_basis = 'demoted_from_kette'` | 240 |
| `evidence_basis = 'propagated'` with `derivation_note='former_basis=demoted_from_kette'` | 57 |
| Satisfies check 7 disjunction | **297 / 297** |

The 57 `propagated` edges are exactly the `HAT_HUERDE` bucket re-flagged by
Phase 1.3 (`mig_1_3_flag_propagated.cypher`), which preserves the demote
trace in `derivation_note`. This is by design and is explicitly accepted
by check 7's disjunction.

## Orphan-`:Bauteilgruppe` audit

```
MATCH (bg:Bauteilgruppe)
WITH bg, exists{()-[:HAT_BAUTEILGRUPPE]->(bg)} AS has_proj,
         exists{(bg)-[:TEIL_VON_KETTE]->(:Wiederverwendungskette)} AS has_chain
WHERE NOT has_proj AND NOT has_chain
RETURN count(bg)
  -> 0
```

**Zero** BGs orphaned by the chain deletion. Every one of the 369
`:Bauteilgruppe` retains at least one `:Projekt`-backed `HAT_BAUTEILGRUPPE`
in-edge or a `:TEIL_VON_KETTE` out-edge to a surviving chain (or both).

## `HAT_BAUTEILGRUPPE` invariance

The Phase 1.1 migration cypher only matches/demotes/deletes inside:

- `(:Bauteilgruppe)-[:TEIL_VON_KETTE]->(:Wiederverwendungskette)` (read),
- `(:Wiederverwendungskette)-[r:HAT_STATUS|HAT_WIEDERVERWENDUNGSART|HAT_HUERDE|HAT_LOGISTIK|HAT_PROZESSPHASE|HAT_METHODE]->(target)` (read + merge onto BG side),
- `DETACH DELETE k` for unwired chains.

`HAT_BAUTEILGRUPPE` is `(:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)`
and is never traversed by 1.1. The pre-delete snapshot for the 98 chains
contains **0** occurrences of the string `HAT_BAUTEILGRUPPE`, confirming
that the `DETACH DELETE` could not have severed any. Live count today:
**369** `:HAT_BAUTEILGRUPPE` edges (the same `:Bauteilgruppe` cardinality
implies a near-1:1 project anchoring).

## Sampled demoted edges (10 of 297)

| # | rel_type | bg_id | target_id | evidence_basis | evidence_source_id | demoted_at | derivation_note |
|---|----------|-------|-----------|----------------|---------------------|------------|------------------|
| 1 | HAT_HUERDE       | bg_retained_mehrere_mehrere_timber_square_print_building_structure | h_datenluecke           | propagated         | k_timber_square_reused_steel_chain          | 2026-05-20T20:52:48.404Z | former_basis=demoted_from_kette |
| 2 | HAT_HUERDE       | bg_retained_mehrere_mehrere_timber_square_print_building_structure | h_mengenunsicherheit    | propagated         | k_timber_square_reused_steel_chain          | 2026-05-20T20:52:48.404Z | former_basis=demoted_from_kette |
| 3 | HAT_HUERDE       | bg_retained_mehrere_mehrere_timber_square_print_building_structure | h_technische_freigabe   | propagated         | k_timber_square_reused_steel_chain          | 2026-05-20T20:52:48.404Z | former_basis=demoted_from_kette |
| 4 | HAT_LOGISTIK     | bg_retained_mehrere_mehrere_timber_square_print_building_structure | log_materialmatching    | demoted_from_kette | k_timber_square_reused_steel_chain          | 2026-05-20T20:52:48.404Z | —                                |
| 5 | HAT_LOGISTIK     | bg_retained_mehrere_mehrere_timber_square_print_building_structure | log_materialverfuegbarkeit | demoted_from_kette | k_timber_square_reused_steel_chain      | 2026-05-20T20:52:48.404Z | —                                |
| 6 | HAT_LOGISTIK     | bg_retained_mehrere_mehrere_timber_square_print_building_structure | log_transport           | demoted_from_kette | k_timber_square_reused_steel_chain          | 2026-05-20T20:52:48.404Z | —                                |
| 7 | HAT_METHODE      | bg_retained_mehrere_mehrere_timber_square_print_building_structure | meth_building_material_scouting | demoted_from_kette | k_timber_square_reused_steel_chain  | 2026-05-20T20:52:48.404Z | —                                |
| 8 | HAT_METHODE      | bg_retained_mehrere_mehrere_timber_square_print_building_structure | meth_design_for_disassembly | demoted_from_kette | k_timber_square_reused_steel_chain      | 2026-05-20T20:52:48.404Z | —                                |
| 9 | HAT_PROZESSPHASE | bg_retained_mehrere_mehrere_timber_square_print_building_structure | phase_dokumentation     | demoted_from_kette | k_timber_square_reused_steel_chain          | 2026-05-20T20:52:48.404Z | —                                |
| 10| HAT_PROZESSPHASE | bg_retained_mehrere_mehrere_timber_square_print_building_structure | phase_identifikation    | demoted_from_kette | k_timber_square_reused_steel_chain          | 2026-05-20T20:52:48.404Z | —                                |

All 10 samples carry the canonical shape:

```
{
  migration_origin:    'mig_1_1_demote_chains',
  evidence_basis:      'demoted_from_kette' | 'propagated',
  evidence_origin:     'derived',
  evidence_source_id:  <chain.id>            (non-null),
  evidence_confidence: 'unklar',
  demoted_at:          '2026-05-20T20:52:48.404Z'
  [derivation_note:    'former_basis=demoted_from_kette']   // only when evidence_basis='propagated'
}
```

`bg_labels = ['Bauteilgruppe']` on all samples; `target_labels` is the
matching anchor label (`Huerde`, `Logistik`, `Methode`, `Prozessphase`).

## Residual notes / observations

1. **Renamed wiring is the intended post-state.** The plan literal still
   reads `AUS_BAUWERK`/`EINGEBAUT_IN` for Phase 1.1 because Phase 4 had
   not yet run when 1.1 was written. Phase 4 renamed them to
   `FROM_DONOR`/`INTO_RECEIVER`, and the live graph now exposes only the
   new types on the 14 surviving chains. Check 5 (using the new names) is
   the correct post-state test; the historical
   `AUS_BAUWERK`/`EINGEBAUT_IN` counts are 0/0 on all surviving chains,
   as expected.
2. **57 `HAT_HUERDE` edges carry `evidence_basis='propagated'`.** This is
   the side effect of `mig_1_3_flag_propagated.cypher` (Phase 1.3), not a
   regression. The Phase 1.1 trace survives via
   `derivation_note='former_basis=demoted_from_kette'`, which is exactly
   the disjunction admitted by check 7.
3. **`PHASE_1_1_DONE.flag` is in `logs/`,** not the run-dir root. Both
   the spec and the prior final-verifier accept this location.
4. **No rollback evidence.** No edges have been deleted nor remapped
   since the migration. Counts and breakdowns match
   `logs/mig_1_1_counts.json` exactly.

## Overall

**PASS — 10 / 10 checks satisfied.** Phase 1.1 is fully complete and
provenance-consistent in `mit-bestand`. No remediation required.
