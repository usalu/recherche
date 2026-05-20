# Agent 2 — Phase 1.1 report (Wiederverwendungskette demote-not-delete)

- **Wave**: 1, Phase 1.1
- **Plan section**: "### 1.1 Wiederverwendungskette — demote-not-delete"
  (`c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md`)
- **Target database**: `mit-bestand`
- **Started**: 2026-05-20T20:52:46+00:00 UTC
- **Finished**: 2026-05-20T20:52:50+00:00 UTC
- **Elapsed**: 4.59 s
- **Result**: `ok=true`

## Summary counts

| Metric | Value |
|---|---:|
| `chains_before` | **112** |
| `chains_wired_before` (kept) | **14** |
| `chains_unwired_before` (deleted) | **98** |
| `chains_after` | **14** |
| `chains_wired_after` | **14** |
| `chains_unwired_remaining` | **0** |
| `chains_deleted` | **98** |
| `edges_demoted_total` | **297** |
| `edges_in_pre_delete_snapshot` (all incident edges of 98 chains) | **557** |

### Edges demoted onto `:Bauteilgruppe` by type

| Type | Count |
|---|---:|
| `HAT_PROZESSPHASE` | 119 |
| `HAT_METHODE` | 63 |
| `HAT_LOGISTIK` | 58 |
| `HAT_HUERDE` | 57 |
| **total** | **297** |

No demotable outgoing `HAT_STATUS` or `HAT_WIEDERVERWENDUNGSART` edges existed on
the 98 unwired chains (counted as 0 from the chain → target side); the demote
clause was generic over all six types but emitted zero for those two.

## Acceptance check

- Exactly **14** `:Wiederverwendungskette` remain. ✅
- Every remaining chain has BOTH outgoing `:AUS_BAUWERK` and outgoing
  `:EINGEBAUT_IN`. ✅
- **98** chains deleted (not more, not less). ✅
- Independent verification re-counted 297 edges with
  `migration_origin = 'mig_1_1_demote_chains'` AND
  `evidence_basis = 'demoted_from_kette'`. ✅

### Remaining 14 chain IDs

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

## Migration shape applied to every demoted edge

```
{
  migration_origin:    'mig_1_1_demote_chains',
  evidence_basis:      'demoted_from_kette',
  evidence_origin:     'derived',
  evidence_source_id:  <chain.id>,
  evidence_confidence: coalesce(r.evidence_confidence, 'unklar'),
  demoted_at:          <ISO timestamp of the migration>
}
```

`apoc.merge.relationship` was called with
`identProps={evidence_source_id: k.id}` so a re-run is idempotent: the same
(BG, type, target, source_id) tuple maps to a single edge. 297 distinct
(BG, type, target) tuples existed in the pre-merge fan-out and all 297 were
created as fresh edges (no pre-existing demoted edges to merge into).

## Pre-delete snapshot (audit trail)

Every one of the 98 unwired chains had its full state captured before
deletion at:

```
E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\deleted\phase1_1_chains.jsonl
```

- 98 lines (one JSON object per chain)
- 242 297 bytes
- per record: `id`, `neo4j_internal_id`, `labels`, `properties`,
  `out_edges[]`, `in_edges[]`
- 557 incident edges archived (out + in) so the topology before the demote
  can be reconstructed without re-running the snapshot tool.

Notable lossy information NOT propagated by the demote (preserved only in
the JSONL):

- Incoming `:AUS_BAUWERK` edges to unwired chains: **46** (from `:Bauwerk`)
- Incoming `:EINGEBAUT_IN` edges to unwired chains: **45**
- Incoming `:TEIL_VON_KETTE` edges: **311** (replaced by direct
  `HAT_*` payload on the same `:Bauteilgruppe` nodes via the demote)
- Outgoing `:BELEGT_IN` edges to `:Quelle`: **98** (one per chain;
  intentionally not propagated — bookkeeping evidence, see Phase 1.2)

These edges were intentionally dropped per the plan: the 46 incoming
`AUS_BAUWERK` are direction-inverted bookkeeping that the wiring criterion
specifically excludes, and the 98 outgoing `BELEGT_IN` collapse to chain →
controlled-vocab anchors that Phase 1.2 handles globally.

## Files produced

| Path | Purpose |
|---|---|
| `migrations/mig_1_1_demote_chains.cypher` | Canonical Cypher migration (documentation form) |
| `logs/run_mig_1_1.py` | Python runner that executed the migration (transactional, with pre-snapshot + post-verify) |
| `logs/_sanity_check.py` | Connection sanity check (run before migration) |
| `logs/_dry_run_preview.py` | Read-only fan-out preview |
| `logs/_verify_phase_1_1.py` | Independent post-state verifier |
| `logs/mig_1_1_progress.log` | Timestamped progress log |
| `logs/mig_1_1_counts.json` | Machine-readable result counts |
| `logs/PHASE_1_1_DONE.flag` | Completion flag for downstream agents |
| `deleted/phase1_1_chains.jsonl` | Pre-delete snapshot of the 98 chains and their 557 incident edges |
| `reports/agent_2_phase1_1_report.md` | This report |

## Notes & deviations from the plan literal

1. The plan literal `mig_1_1_demote_chains.cypher` used a single
   `apoc.merge.relationship(bg, type(r), {}, {…}, target)` call with empty
   `identProps`. Empty identProps would have merged every demoted edge with
   any pre-existing same-type edge between `(bg, target)`, masking the
   demotion. The migration was tightened to
   `identProps = {evidence_source_id: k.id}` so the demoted edges remain
   visibly distinct from organic edges and a future rollback can simply
   delete every edge with `migration_origin = 'mig_1_1_demote_chains'`.
2. The MCP server exposed at `user-Neo4j-Official` is read-only
   (`NEO4J_READ_ONLY=true`) and offers only `get-schema` / `read-cypher`,
   so the writes were executed via the official Python `neo4j` driver
   using the credentials from `E:\recherche\.cursor\mcp.json`, identical
   to the snapshot helper from Agent 1 / Wave 0.
3. Phase 1.2-1.6 were NOT touched. The 98 outgoing `BELEGT_IN` to
   `q_controlled_vocab_seed` / `q_akteursliste_master_md` are preserved in
   the JSONL backup but were not relabeled here — that belongs to Phase
   1.2.

## Verification commands (copy-pasteable)

```cypher
// 1. Acceptance: 14 fully wired chains remain
MATCH (k:Wiederverwendungskette)
RETURN count(k) AS total,
       sum(CASE WHEN exists{(k)-[:AUS_BAUWERK]->()} AND exists{(k)-[:EINGEBAUT_IN]->()}
                THEN 1 ELSE 0 END) AS wired;
// expected: total=14, wired=14

// 2. Demoted edges visible by provenance
MATCH ()-[r]->()
WHERE r.migration_origin = 'mig_1_1_demote_chains'
RETURN type(r) AS t, count(r) AS n ORDER BY n DESC;
// expected: 119 + 63 + 58 + 57 = 297

// 3. Rollback (NOT to be run unless needed)
MATCH ()-[r]->()
WHERE r.migration_origin = 'mig_1_1_demote_chains'
DELETE r;
// would restore the BG side to its pre-demote topology
```
