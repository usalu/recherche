# Minimal properties Phase 1 Cypher apply report

**Applied:** 2026-06-01  
**Database:** `mit-bestand`  
**Backup:** `_neo4j/review/backups/2026-06-01_pre_minimal_properties_phase1_p0`

This follow-up handled the P0 relationship-property removals that could not be
represented safely in the JSONL patch because the target relationships had
missing or list-valued `r.id`.

| Relationship type | Property | Before | After | Removed |
|---|---|---:|---:|---:|
| `HAT_AKTEURROLLE` | `scope` | 7 | 0 | 7 |
| `HAT_AKTEURTYP` | `scope` | 2 | 0 | 2 |
| `HAT_KENNWERT` | `candidate_source_count` | 88 | 0 | 88 |

Total removed: **97** relationship-property occurrences.
