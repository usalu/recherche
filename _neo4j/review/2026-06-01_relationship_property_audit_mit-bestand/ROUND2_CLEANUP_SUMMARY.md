# Round 2 deep cleanup - apply summary (mit-bestand)

Second cleanup round, focused on what the multi-perspective scan surfaced after
the round-1 node-property work: relationship-property bloat, orphaned sources,
and duplicate sources. All write phases were backed up, dry-run, applied, then
gap-surveyed.

## Before -> after

| Metric | Round-2 start | Round-2 end |
| --- | --- | --- |
| Nodes | 7,905 | **5,463** |
| Relationships | 25,194 | **23,796** |
| Relationship property occurrences | 312,649 | **46,769** (-85%) |
| Avg props / edge | ~12.4 | **~2.0** |
| Orphan source/misc nodes | ~4,535 | **2,112** (pending decision) |
| Duplicate URLs | 994 groups / 3,375 nodes | **0** (+ uniqueness constraint) |
| `r.id` NULL edges | 5,310 | **0** |

## Phases applied

- **Phase F - relationship property minimization.** Migrated every id-bearing
  provenance property (`evidence_source_id` / `source_url_node_id` /
  `archive_source_id`) that pointed to a real unlinked source into a node-level
  `BELEGT_IN` edge (+1,158 edges; safety gate drove "edges losing a real source
  pointer" 3,531 -> 0), then dropped the 46-key bookkeeping complement from every
  edge. 267k property occurrences removed; the 15 semantic/evidence keys kept.
  Backup: `_neo4j/review/backups/2026-06-01_pre_phaseF_rel_property_min`.
- **Source reconnection.** Built a url->entity index from the processed
  source-of-truth records and reconnected 580 orphan sources to their case via
  `HAS_SOURCE_LINK`. Backup: `.../2026-06-01_pre_source_reconnect`.
- **Phase H - source dedup + uniqueness.** Merged 2,442 duplicate-URL `Quelle`
  into one canonical node per normalized URL (all edges re-pointed, 621 redundant
  parallel edges collapsed), nulled empty-string URLs, and added the
  `quelle_url_unique` constraint. Backup: `.../2026-06-01_pre_quelle_dedup`.
- **Phase J - rel hygiene.** Collapsed 2,515 parallel duplicate edges (identical
  after the property drop; same target so no evidence lost) and backfilled the
  deterministic `r.id` (`r_<from>__<TYPE>__<to>`) on every remaining edge.
  Backup: `.../2026-06-01_pre_phaseJ_hygiene`.

## Gap survey (final)

`r.id NULL` now 0 (was FAIL). Remaining FAILs are pre-existing domain-data gaps,
not cleanup artifacts:
- Case-specific nodes missing `BELEGT_IN`: 4
- BG missing `HAT_MATERIALGRUPPE`: 1, BG missing `HAT_WIEDERVERWENDUNGSART`: 2

## Open decisions (no auto-action taken)

1. **2,096 residual orphan sources** - see `RESIDUAL_ORPHANS.md` (keep / delete / tag).
2. **13 `DeprecatedType` schema-migration markers** - disconnected meta bookkeeping
   (e.g. `dep_label__GraphVersion`); candidates for deletion like round-1 `DataIssue`.
3. Carried over: `ReuseRule` (20) already first-class (no action); 3 unused but
   valid vocab nodes (`Layer` Site/Stuff, `Zertifizierungssystem` LEED) kept.
