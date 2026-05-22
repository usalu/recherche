# Execution order — taxonomy integration 2026-06-03

Run these files in order. Each section notes whether the step is **idempotent / reversible** or **destructive** (requires the Phase 0 backup to roll back).

All `cypher-shell` commands assume:
- The CSV files (`bauteilgruppe_id_map.csv`) are accessible from Neo4j's import directory, OR the `LOAD CSV` paths are updated to absolute paths.
- The `:param` blocks use cypher-shell parameter syntax. If running through the Neo4j Browser or another tool, convert `:param x => ...` to explicit map literals inside the queries.
- `--format plain` flag is recommended for human-readable post-check output.

---

## 0. Pre-flight (read-only / safe label fix)

| # | File | Mode | What it does |
|---|---|---|---|
| 0.1 | (manual) | safe | Confirm 2026-06-03 backup at [\_neo4j/review/2026-06-03_graph_schema_full_export_mit-bestand/live_graph.backup.jsonl](../2026-06-03_graph_schema_full_export_mit-bestand/live_graph.backup.jsonl) is restorable on a clone |
| 0.2 | — | n/a | Already complete (the 2026-06-03 full export) |
| 0.3 | [phase0_3_pre_deletion_scan.cypher](phase0_3_pre_deletion_scan.cypher) | read-only | Dump everything Phase 6 will touch; output to `snapshot_pre_integration/pre_deletion_scan.json` |
| 0.4 | [phase0_4_relabel_prog_projects.cypher](phase0_4_relabel_prog_projects.cypher) | reversible | Relabel 3 mislabeled `:Projekt` nodes → `:Programm` |

```bash
cypher-shell -d mit-bestand -f phase0_3_pre_deletion_scan.cypher --format plain \
  > snapshot_pre_integration/pre_deletion_scan.json
cypher-shell -d mit-bestand -f phase0_4_relabel_prog_projects.cypher
```

---

## 1. Phase 1 — decisions

Done. See [FINAL_PLAN.md](FINAL_PLAN.md) §"Decisions locked in".

---

## 2. Phase 2 — Markdown normalization

Done (non-destructive — Python only).

```bash
python phase2_normalize_and_filter.py
```

Output:
- `_neo4j/intake/inbox/research/new taxonomy edit/_normalized/` — 7 normalized batch files
- `_neo4j/intake/inbox/research/new taxonomy edit/_filtered_non_reuse_bgs.md` — 89 filtered rows for transparency
- [phase2_normalization_report.md](phase2_normalization_report.md) — summary

---

## 3. Phase 3 — resolver tables (no graph change)

Done.

| File | Status |
|---|---|
| Project ID map | Not needed (live + batch both use `p_*`) |
| [bauteilgruppe_id_map.csv](bauteilgruppe_id_map.csv) | Auto-generated; manual review skipped per FINAL_PLAN decision #8 |
| [vocabulary_id_map.csv](vocabulary_id_map.csv) | Hand-written; covers all 13+62+16+11+1 old vocab → new canonical |

---

## 4. Phase 4 — constraints + seed nodes

| # | File | Mode | What it does |
|---|---|---|---|
| 4 | [phase4_constraints_and_seeds.cypher](phase4_constraints_and_seeds.cypher) | additive / reversible | 5 new constraints; 30 new canonical seed nodes; tagged `review_run = 'taxonomy_integration_2026_06_03'` |

```bash
cypher-shell -d mit-bestand -f phase4_constraints_and_seeds.cypher
```

**Rollback (Phase 4 only):**
```cypher
MATCH (n) WHERE n.source_scope = 'controlled_vocab_seed'
              AND n.review_run = 'taxonomy_integration_2026_06_03'
              AND NOT (n)-[]-()
DELETE n;
DROP CONSTRAINT wiederverwendungsergebnis_id;  // and the other 4
```

---

## 5. Phase 5 — batch evidence MERGE

| # | File | Mode | What it does |
|---|---|---|---|
| 5.gen | [phase5_generate_evidence_cypher.py](phase5_generate_evidence_cypher.py) | Python | Generates [phase5_evidence.cypher](phase5_evidence.cypher) from normalized batches. **Re-run after any change to `_normalized/`.** |
| 5 | [phase5_evidence.cypher](phase5_evidence.cypher) | additive / reversible | 1,834 evidence MERGEs across 8 rel types. New Bauteilgruppen created with `bg_kind = 'partial_batch'`. |

```bash
python phase5_generate_evidence_cypher.py
cypher-shell -d mit-bestand -f phase5_evidence.cypher
```

**Per-rel-type counts** (from generator):
- `HAT_ERGEBNIS`             338
- `HAT_RESSOURCENQUELLE`     300
- `HAT_BAUTEILGRUPPE`        300
- `HAT_WIEDERVERWENDUNGSORT` 290
- `HAT_AUFBEREITUNG`         235
- `HAT_METHODE`              216
- `HAT_RUECKBAUVERFAHREN`    142
- `ANGEWENDET_AUF`            13

**Rollback (Phase 4 + 5 only):**
```cypher
MATCH ()-[r {review_run: 'taxonomy_integration_2026_06_03'}]-() DELETE r;
MATCH (bg:Bauteilgruppe {review_run: 'taxonomy_integration_2026_06_03'})
WHERE NOT (bg)<-[:HAT_BAUTEILGRUPPE]-() DELETE bg;
// then the Phase 4 seed-node rollback above
```

---

## 6. Phase 6 — DESTRUCTIVE retirement (no rollback except backup restore)

| # | File | Mode | What it does |
|---|---|---|---|
| 6.1 | [phase6_1_migrate_upstreams.cypher](phase6_1_migrate_upstreams.cypher) | reattach + delete | ~115 inbound edges from Akteur/Software/Tool/Norm/Programm/ReuseRule/Materialdepot rerouted to new canonical with `legacy_*_id` provenance |
| 6.2 | [phase6_2_migrate_outbound.cypher](phase6_2_migrate_outbound.cypher) | reattach + delete | ~47 outbound edges (`TYPISCH_BEI_MATERIAL`, `BELEGT_IN`) from `:Aufbereitungsverfahren` rerouted + deduped |
| 6.3 | [phase6_3_delete_replaceable_edges.cypher](phase6_3_delete_replaceable_edges.cypher) | DELETE only | ~2,478 placeholder edges from `:Bauteilgruppe` / `:Projekt` to old vocab — batches re-supplied these in Phase 5 |
| 6.4 | [phase6_4_delete_bauteilgruppen.cypher](phase6_4_delete_bauteilgruppen.cypher) | DELETE only | 35 `bg_reuse_*` orphans + 35 non-reuse BGs (`bg_retained_*` / `bg_planned_*` / `bg_dismantled_*` / `bg_candidate_*`) = 70 nodes |
| 6.5/6.6 | [phase6_5_6_delete_old_vocab_and_drop_constraint.cypher](phase6_5_6_delete_old_vocab_and_drop_constraint.cypher) | DELETE + drop constraint | 13 `meth_*` + 62 `av_*` + 16 `rq_*` + 1 `rv_betonfraesen` + 11 `wva_*` = 103 nodes; then `DROP CONSTRAINT wiederverwendungsart_id` |

```bash
# Run in order — each step has its own pre/post checks
cypher-shell -d mit-bestand -f phase6_1_migrate_upstreams.cypher
cypher-shell -d mit-bestand -f phase6_2_migrate_outbound.cypher
cypher-shell -d mit-bestand -f phase6_3_delete_replaceable_edges.cypher
cypher-shell -d mit-bestand -f phase6_4_delete_bauteilgruppen.cypher
cypher-shell -d mit-bestand -f phase6_5_6_delete_old_vocab_and_drop_constraint.cypher
```

**Rollback for any 6.x step: ONLY the Phase 0 backup restore.** Do not start Phase 6 until Phase 5 verifies green AND the backup is confirmed restorable on a clone.

---

## 7. Phase 7 — Verification

```bash
cypher-shell -d mit-bestand -f verify_integration.cypher --format plain
```

All §1–§11 checks must return `OK` (or `INFO` for advisory rows). Any `FAIL` blocks sign-off.

---

## Recommended dry-run procedure

1. Clone the live database to `mit-bestand-clone` (Neo4j `dbms.copy database`)
2. Run **Phases 4 + 5** on the clone, verify green
3. Run **Phase 6.1 + 6.2** on the clone, verify green
4. Run **Phase 6.3 + 6.4 + 6.5/6.6** on the clone, verify green
5. Run `verify_integration.cypher` on the clone, verify all OK
6. If any FAIL → diagnose against clone, fix the Cypher, repeat from step 1
7. Only when clone runs end-to-end green → apply same sequence to `mit-bestand` live

---

## File index (this directory)

| File | Purpose |
|---|---|
| `FINAL_PLAN.md` | Executive summary, locked decisions, before/after counts |
| `WHATS_HAPPENING.md` | Plain-language summary (KEEP/NEW/DELETE/REROUTE tags) |
| `INTEGRATION_PLAN.md` | Detailed phase descriptions |
| `CONNECTION_TYPE_AUDIT.md` | Edge-by-edge classification |
| `SEMANTIC_CONFLICT_AUDIT.md` | 15 conflicts and resolutions |
| `RICHNESS_AUDIT.md` | Why we can replace old vocab without losing quality |
| `BAUTEILGRUPPE_COMPARISON.md` | Live ↔ batch BG slug matching analysis |
| `RESOLVER_USAGE.md` | How the BG resolver works (optional/informational) |
| `PHASE_0_2_STATUS.md` | What Phase 0+2 produced |
| `EXECUTION_ORDER.md` | **(this file)** — run order & commands |
| `vocabulary_id_map.csv` | Old vocab id → new canonical id (75 rows) |
| `bauteilgruppe_id_map.csv` | Live BG → batch BG mapping (390 rows) |
| `bauteilgruppe_resolver_review.md` | Human-readable review queue (informational) |
| `phase2_normalize_and_filter.py` | Markdown normalizer + filter |
| `phase2_normalization_report.md` | P2 summary |
| `phase0_3_pre_deletion_scan.cypher` | Read-only forensic dump |
| `phase0_4_relabel_prog_projects.cypher` | Relabel 3 mislabeled projects |
| `phase4_constraints_and_seeds.cypher` | Constraints + 30 seed nodes |
| `phase5_generate_evidence_cypher.py` | Generator for Phase 5 Cypher |
| `phase5_evidence.cypher` | 1,834 evidence MERGEs (generated) |
| `phase6_1_migrate_upstreams.cypher` | Migrate non-replaceable upstream edges |
| `phase6_2_migrate_outbound.cypher` | Migrate outbound TYPISCH_BEI_MATERIAL + BELEGT_IN |
| `phase6_3_delete_replaceable_edges.cypher` | Delete BG/Projekt → old vocab edges |
| `phase6_4_delete_bauteilgruppen.cypher` | Delete 35 + 35 BGs |
| `phase6_5_6_delete_old_vocab_and_drop_constraint.cypher` | Delete 103 vocab nodes + drop constraint |
| `verify_integration.cypher` | Read-only verification suite |
