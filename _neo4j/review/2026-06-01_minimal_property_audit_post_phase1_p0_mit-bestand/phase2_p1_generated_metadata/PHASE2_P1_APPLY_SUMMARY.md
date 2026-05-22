# Phase 2 P1 generated-metadata cleanup — applied

**Applied:** 2026-06-01  
**Database:** `mit-bestand`  
**Backup:** `_neo4j/review/backups/2026-06-01_pre_minimal_properties_phase2_p1_generated_metadata`

## What changed

Phase 2 removed P1 `drop_candidate` properties: generated/import/cache/debug
metadata identified in the post-Phase-1 minimization audit.

No nodes or relationships were added/deleted by this cleanup.

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Nodes | 39,165 | 39,165 | 0 |
| Relationships | 80,135 | 80,135 | 0 |
| Node-property occurrences | 605,837 | 449,083 | -156,754 |
| Relationship-property occurrences | 754,644 | 567,540 | -187,104 |
| Total property occurrences | 1,360,481 | 1,016,623 | -343,858 |

## Applied artifacts

- Plan: `MINIMAL_PROPERTIES_PHASE2_PLAN.md`
- Cypher: `minimal_properties_phase2_p1_generated_metadata.cypher`
- Pre-apply count check: `minimal_properties_phase2_p1_count_check_pre_apply.json`
- Apply report: `MINIMAL_PROPERTIES_PHASE2_APPLY_REPORT.md`
- Full per-statement report: `minimal_properties_phase2_p1_apply_report.json`
- Postcheck: `minimal_properties_phase2_p1_postcheck.json`

## Result

- Statements: 706.
- Targeted properties before apply: 343,858.
- Targeted properties after apply: 0.
- Targeted properties removed: 343,858.

The audit-estimated occurrence count was higher because multi-label nodes are
counted once per label/property pair in the audit, while a property exists only
once on the physical node.

## Current post-cleanup audit

Fresh audit after Phase 2:

`_neo4j/review/2026-06-01_minimal_property_audit_post_phase2_p1_mit-bestand/`

Headline:

- Node label/property pairs: 767.
- Relationship type/property pairs: 1,091.
- Patch-ready drop candidates: 0.
- Type drift pairs: 21.

## Remaining cleanup fronts

Phase 1 and Phase 2 exhausted the safe/mechanical `drop_candidate` buckets.
Remaining work requires model decisions:

- `move_to_provenance_model`: source/evidence fields that need normalized
  provenance, not blind deletion.
- `drop_or_archive_meta_node`: `DataIssue` / review graph compaction.
- `review_relationship_duplicate`: node fields duplicating relationships.
- `review_domain_property`: decide which factual properties are truly semantic.
