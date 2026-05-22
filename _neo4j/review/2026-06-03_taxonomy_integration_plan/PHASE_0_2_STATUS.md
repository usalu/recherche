# Phase 0 + 2 — execution status

**Generated:** 2026-06-03
**Status:** Phase 2 done (Markdown only, no graph change). Phase 0.3 + 0.4 Cypher written, ready to run.

## What's been produced

### Phase 2 — Markdown normalization + filter (DONE)

- [phase2_normalize_and_filter.py](phase2_normalize_and_filter.py) — the normalizer
- [phase2_normalization_report.md](phase2_normalization_report.md) — per-batch summary
- [\_neo4j/intake/inbox/research/new taxonomy edit/\_normalized/](../../intake/inbox/research/new%20taxonomy%20edit/_normalized/) — normalized batch Markdowns
- [\_neo4j/intake/inbox/research/new taxonomy edit/\_filtered_non_reuse_bgs.md](../../intake/inbox/research/new%20taxonomy%20edit/_filtered_non_reuse_bgs.md) — 89 rows filtered out (anchored on non-`bg_reuse_*` BGs)

**Numbers:**
- Importable batches (01–06, 10): **1,923** rows in → **1,834** kept + **89** filtered
- 1,839 substitutions applied (rel aliases, target labels, id prefixes)
- Deferred batches (07, 08, 09): **505** rows — they use free-text `component_or_scope` columns with no `bg_*` slug ids, can't be slug-linked without a separate mapping pass. Excluded from this round.

**Substitution kinds:**
- `id_via_prefix` (719): id prefix rewrites e.g. `q_Externer_Spenderbau` → `rq_externer_spenderbau`
- `rel_alias` (516): rel renames e.g. `HAS_METHOD` → `HAT_METHODE`, `HAT_QUELLE` → `HAT_RESSOURCENQUELLE`
- `id` (473): direct id rewrites e.g. `Urban_Mining_und_Scouting` → `meth_urban_mining_und_scouting`
- `target_label` (300): e.g. `Quelle` → `Ressourcenquelle`
- `canon_norm` (191): out-of-vocab labels e.g. `Lokal_oder_Regional_importiert` → `Extern_importiert`
- `canon_norm_in_id` (128): same normalization applied inside id strings
- `canon_norm_rel` (28): rel-aware ambiguous label resolution (`Dekonstruktion_mit_Inventar` → `Selektiver_Rueckbau` or `Dokumentation_und_Monitoring` depending on rel context)

### Phase 0.4 — relabel `prog_*` Projekt nodes (READY)

- [phase0_4_relabel_prog_projects.cypher](phase0_4_relabel_prog_projects.cypher)

Trivial fix: 3 `:Projekt` nodes have `prog_*` ids — should be `:Programm`. Script has pre-check / apply / post-check / rollback blocks. Safe — only changes labels on 3 nodes.

### Phase 0.3 — pre-deletion scan (READY)

- [phase0_3_pre_deletion_scan.cypher](phase0_3_pre_deletion_scan.cypher)

Read-only. Dumps everything Phase 6 will touch:
- §1 old vocab nodes (103 expected: 13 + 62 + 16 + 11 + 1)
- §2 inbound edges (aggregated + full per-edge)
- §3 outbound edges (especially `TYPISCH_BEI_MATERIAL` and `BELEGT_IN` from `:Aufbereitungsverfahren`)
- §4 Bauteilgruppen scheduled for deletion (35 reuse orphans + 35 non-reuse)
- §5 DataIssue sanity (expected 0)

Run output to `snapshot_pre_integration/pre_deletion_scan.json`.

### Phase 3.3 — vocabulary id lookup map (READY)

- [vocabulary_id_map.csv](vocabulary_id_map.csv)

Deterministic mapping for Phase 6 migration. Columns: `old_label, old_id, new_label, new_id, note`. Covers all 13 `meth_*` → 6 canonical, all collapsible `av_*` → 6 canonical, all 16 `rq_*` → 6 canonical, `rv_betonfraesen` → `rv_schneidender_rueckbau`, all 11 `wva_*` → axis-shifted target.

---

## How to run

Order of operations (Phase 0 and 2 only — non-destructive):

```bash
# 1. Phase 2 normalization (already done; re-run anytime if batches change)
python _neo4j/review/2026-06-03_taxonomy_integration_plan/phase2_normalize_and_filter.py

# 2. Phase 0.4 — relabel prog_* projects (3 nodes)
cypher-shell -d mit-bestand -f _neo4j/review/2026-06-03_taxonomy_integration_plan/phase0_4_relabel_prog_projects.cypher

# 3. Phase 0.3 — pre-deletion scan (read-only, dumps to JSON)
mkdir -p _neo4j/review/2026-06-03_taxonomy_integration_plan/snapshot_pre_integration
cypher-shell -d mit-bestand --format json -f _neo4j/review/2026-06-03_taxonomy_integration_plan/phase0_3_pre_deletion_scan.cypher \
  > _neo4j/review/2026-06-03_taxonomy_integration_plan/snapshot_pre_integration/pre_deletion_scan.json
```

After P0.3 runs, inspect `pre_deletion_scan.json` to verify:
- 103 old vocab nodes flagged for deletion
- ~74 `:Methode` inbound edges to migrate (Akteur/Software/Tool/Norm)
- ~40 `:ReuseRule → :Aufbereitungsverfahren` to migrate
- ~22 `TYPISCH_BEI_MATERIAL` outbound to migrate
- ~25 `BELEGT_IN → :Quelle:ResearchDocument` outbound to migrate
- ~1 `:Materialdepot → :Ressourcenquelle` to migrate
- 70 BGs flagged for deletion (35 reuse orphans + 35 non-reuse)
- 0 DataIssues (fresh 2026-06-03 export confirmed they're already cleaned)

---

## What's NOT done yet (Phase 4 / 5 / 6 work)

| Phase | Deliverable | Status |
|---|---|---|
| 4 | `phase4_constraints_and_seeds.cypher` (constraints + 30 new canonical seed nodes) | not written |
| 5 | One Cypher file per importable batch, ~1,834 row MERGEs total | not written |
| 6.1 | `phase6_1_migrate_upstreams.cypher` (~115 edges rerouted) | not written |
| 6.2 | `phase6_2_migrate_outbound.cypher` (~47 edges rerouted+deduped) | not written |
| 6.3 | `phase6_3_delete_replaceable_edges.cypher` (~2,478 placeholder edges) | not written |
| 6.4b | `phase6_4b_delete_bg_reuse_orphans.cypher` (35 BGs) | not written |
| 6.4c | `phase6_4c_delete_non_reuse_bgs.cypher` (35 BGs) | not written |
| 6.5 | `phase6_5_delete_old_vocab_nodes.cypher` (103 nodes) | not written |
| 6.6 | `phase6_6_drop_wva_constraint.cypher` | not written |
| 7 | [verify_integration.cypher](verify_integration.cypher) (already drafted) | re-runnable now |

Next action: generate phase 4 + 5 + 6 Cypher from the normalized batch markdowns and the vocab map. This is the bulk of the remaining work; estimate is one focused session.

---

## Safety summary

| Step | Reversible? | How |
|---|---|---|
| Phase 2 (Markdown) | Yes | Originals untouched; delete `_normalized/` to restart |
| P0.4 relabel | Yes | Rollback block at end of [phase0_4_relabel_prog_projects.cypher](phase0_4_relabel_prog_projects.cypher) |
| P0.3 scan | Yes | Read-only, nothing to roll back |
| Phase 4 + 5 (additive) | Yes | Single `MATCH ()-[r {review_run: 'taxonomy_integration_2026_06_03'}]-() DELETE r` |
| Phase 6 (destructive) | Backup-only | Restore from [2026-06-03 full backup](../2026-06-03_graph_schema_full_export_mit-bestand/live_graph.backup.jsonl) |
