# Phase 1 P0 minimal-property cleanup — applied

**Applied:** 2026-06-01  
**Database:** `mit-bestand`  
**Backup:** `_neo4j/review/backups/2026-06-01_pre_minimal_properties_phase1_p0`

## What changed

Phase 1 removed low-risk P0 properties only: known legacy keys, query-derivable
counts, and stale relationship `scope` / `candidate_source_count` properties.

No nodes or relationships were added/deleted.

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Nodes | 39,160 | 39,160 | 0 |
| Relationships | 79,888 | 79,888 | 0 |
| Node-property occurrences | 611,239 | 605,817 | -5,422 |
| Relationship-property occurrences | 756,805 | 754,072 | -2,733 |
| Total property occurrences | 1,368,044 | 1,359,889 | -8,155 |

## Applied artifacts

- JSONL patch: `minimal_properties_phase1_p0.patch.jsonl`
- JSONL apply report: `_neo4j/review/apply_reports/minimal_properties_phase1_p0.patch.apply_report.md`
- Cypher follow-up: `minimal_properties_phase1_unaddressed_relationships.cypher`
- Cypher apply report: `minimal_properties_phase1_cypher_apply_report.md`

## JSONL result

- Records: 8,012.
- Node update records: 5,376.
- Relationship update records: 2,636.
- Load errors: 0.
- Rejected / needs review: none.

## Cypher follow-up result

Handled P0 relationship properties that could not be represented in JSONL
because target relationships had missing or list-valued `r.id`.

- `HAT_AKTEURROLLE.scope`: 7 removed.
- `HAT_AKTEURTYP.scope`: 2 removed.
- `HAT_KENNWERT.candidate_source_count`: 88 removed.

## Post-checks

All Phase 1 target keys are now absent:

- Remaining Phase 1 node keys: 0.
- Remaining Phase 1 node `scope` keys on targeted labels: 0.
- Remaining Phase 1 relationship keys: 0.

Gap survey still reports pre-existing semantic gaps, but no count regression:

- Nodes: 39,160.
- Relationships: 79,888.
- Case-specific nodes missing `BELEGT_IN`: 4.
- `BG missing HAT_MATERIALGRUPPE`: 1.
- `BG missing HAT_WIEDERVERWENDUNGSART`: 2.

## Current post-cleanup audit

Fresh audit after Phase 1:

`_neo4j/review/2026-06-01_minimal_property_audit_post_phase1_p0_mit-bestand/`

Headline:

- Node label/property pairs: 1,126.
- Relationship type/property pairs: 1,427.
- Remaining patch-ready P1 drop surface: 396,617 property occurrences.
- Type drift pairs: 27.
