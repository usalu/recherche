# Integration Sign-off — Reuse Taxonomy Migration

**Status: COMPLETE**
**Database:** `mit-bestand`
**Executed:** 2026-06-03 → 2026-06-04
**Pre-integration backup:** [\_neo4j/review/2026-06-03_graph_schema_full_export_mit-bestand/live_graph.backup.jsonl](../2026-06-03_graph_schema_full_export_mit-bestand/live_graph.backup.jsonl)
**Verification result:** **32 of 32 checks passed** ([\_final_verify.py](_final_verify.py))

---

## What landed

### Vocabulary axes — final state

| Label | Before | After | Status |
|---|---:|---:|---|
| `:Methode` | 13 | **6** | replaced by canonical |
| `:Aufbereitungsverfahren` | 62 | **6** | replaced by canonical |
| `:Ressourcenquelle` | 16 | **6** | replaced by canonical |
| `:Rueckbauverfahren` | 5 | **6** | 4 kept + 2 added, `rv_betonfraesen` removed |
| `:Wiederverwendungsergebnis` | – | **6** | brand-new axis (outcome) |
| `:Wiederverwendungsort` | – | **6** | brand-new axis (location) |
| `:WiederverwendungsArt` | 11 | **0** | label retired, constraint dropped |

### Bauteilgruppe — final state

| | Before | After |
|---|---:|---:|
| Total `:Bauteilgruppe` | 356 | **364** |
| Non-`bg_reuse_*` prefixes (retained/planned/dismantled/candidate) | 35 | **0** |
| Bauteilgruppen with `bg_*` id prefix | 356 | **364** |
| Bauteilgruppen with `bg_reuse_*` (legacy prefix) | 321 | **0** |

The `bg_reuse_` token was stripped after integration (redundant — every `:Bauteilgruppe` now represents reused material by definition). Original ids preserved on each node as `legacy_id`.

### Edge state

| Relationship | Total now | Migrated (Phase 6.1) | Migrated (Phase 6.2) | New (Phase 4+5) |
|---|---:|---:|---:|---:|
| `HAT_BAUTEILGRUPPE` | 364 | – | – | 78 new |
| `HAT_ERGEBNIS` | 294 | – | – | 294 |
| `HAT_WIEDERVERWENDUNGSORT` | 258 | – | – | 258 |
| `HAT_RESSOURCENQUELLE` | 264 | 1 | – | 263 |
| `HAT_METHODE` | 222 | 142 | – | 80 |
| `HAT_AUFBEREITUNG` | 267 | 37 | – | 232 (incl. 18 deduped `TYPISCH_BEI_MATERIAL`) |
| `HAT_RUECKBAUVERFAHREN` | 308 | – | – | 308 |
| `ANGEWENDET_AUF` | 13 | – | – | 13 |
| `HAT_WIEDERVERWENDUNGSART` | **0** | – | – | – |
| `BELEGT_IN` (from `:Aufbereitungsverfahren`) | preserved | – | 4 deduped | – |

**Total new evidence-backed edges in this run: 2,526**

### Confidence quality shift

| Tier | Before integration | After integration |
|---|---:|---:|
| `belegt` (sourced, high confidence) | ~0 | **1,784 (70.6%)** |
| `wahrscheinlich` (medium) | ~0 | **456 (18.0%)** |
| `unsicher` / `unklar` | ~2,459 | **286 (11.3%)** |

Old vocab edges were predominantly `evidence_origin: topology_synthesized` with `evidence_confidence: unklar` (per [RICHNESS_AUDIT.md](RICHNESS_AUDIT.md)). The new state replaces 2,478 placeholder edges with 2,526 evidence-backed edges carrying `evidence_url` + `evidence_quote` from batch source documents.

### Whole-graph delta

| | Before | After |
|---|---:|---:|
| Total nodes | 5,476 | 5,413 (−63) |
| Total relationships | 24,017 | 21,278 (−2,739) |
| `:DataIssue` | 0 | 0 |

---

## Phases executed (in order)

| Phase | Description | Outcome |
|---|---|---|
| 0.3 | Pre-deletion scan → JSON | [snapshot_pre_integration/pre_deletion_scan.json](snapshot_pre_integration/pre_deletion_scan.json) |
| 0.4 | Relabel `prog_*` `:Projekt` → `:Programm` | no-op (already correctly labeled in current graph) |
| 2 | Markdown normalization + non-reuse filter | 1,923 → 1,834 rows; 89 filtered |
| 4 | 5 new constraints + 32 seed nodes | all created |
| 5 | 1,834 evidence MERGE rows across 8 rel types | 78 new Bauteilgruppen, all rows attached |
| 6.1 | Migrate non-replaceable upstreams (`:Akteur/:Software/:Tool/:Norm/:Programm/:ReuseRule/:Materialdepot`) | 180 migrated with `legacy_*_id` provenance, 231 old deleted |
| 6.2 | Migrate outbound `TYPISCH_BEI_MATERIAL` + `BELEGT_IN` from old `av_*` | 22 migrated + deduped onto new canonical |
| 6.3 | Delete `:Bauteilgruppe / :Projekt → old vocab` placeholder edges | 2,183 deleted |
| 6.4 | Delete 35 `bg_reuse_*` orphans + 35 non-reuse BGs | 70 nodes, 1,582 rels detached |
| 6.5 | Hard-delete 103 old vocab nodes | done |
| 6.6 | Drop `wiederverwendungsart_id` constraint | done |
| post | Strip `bg_reuse_` → `bg_` prefix on all 364 BGs | done; `legacy_id` preserved |
| 7 | Final verification | **32/32 checks pass** |

---

## What's preserved for rollback / audit

- `legacy_methode_id` / `legacy_aufbereitung_id` / `legacy_ressourcenquelle_id` on every migrated edge
- `legacy_rel_id` pointing at the original rel's id
- `legacy_id` on every renamed Bauteilgruppe
- `review_run` tag identifying which phase produced each new edge:
  - `taxonomy_integration_2026_06_03` — Phase 4 + 5
  - `taxonomy_integration_2026_06_03_phase6_1` — Phase 6.1 reroutes
  - `taxonomy_integration_2026_06_03_phase6_2` — Phase 6.2 reroutes
  - `taxonomy_integration_2026_06_04_strip_reuse_prefix` — BG id rename

Rollback paths:
- Phase 4 + 5 + 6.1 + 6.2 edges → single Cypher `DELETE` keyed on `review_run`
- BG rename → trivial reverse via `legacy_id` property
- Phase 6.3 / 6.4 / 6.5 destructive deletions → **only path back is restoring the Phase 0 backup**

---

## Known accepted costs (per FINAL_PLAN.md)

- ~25–50 `:Bauteilgruppe` slug-drift duplicates: some BGs exist as both a pre-integration version and a batch-supplied version of the same physical component. Dedupe was deferred per user decision (skip manual resolver). Can be cleaned in a future pass with the [bauteilgruppe_resolver_review.md](bauteilgruppe_resolver_review.md) tooling preserved here.
- ~78 batch-derived Bauteilgruppen created in Phase 5 carry only the batch evidence edges; they lack the non-vocab axes (`HAT_BAUTEILTYP`, `NUTZT_MATERIAL`, `HAT_SCHADSTOFF`, …) that the original 286 BGs carry. Slug tokens can be parsed to enrich them in a follow-up.
- Batches 07–09 (505 evidence rows) deferred — they use free-text descriptor columns with no `bg_*` slug ids and cannot be slug-linked without a separate mapping pass.

---

## Mission status

**COMPLETE — migration landed cleanly.**

All 32 verification checks pass. The active graph contains only the six-axis canonical taxonomy. Evidence is now ~71% `belegt`-confidence with first-party `evidence_url` and `evidence_quote` on every new edge. The old placeholder-vocab layer has been retired, and every migrated upstream edge carries `legacy_*_id` provenance for audit.

The next research batch can be applied through the same Phase 2 → 5 pattern; the new canonical schema is now the stable foundation.
