# Minimal properties Phase 2 plan

**Generated UTC:** 2026-06-01T07:07:52.809788+00:00

Scope: P1 `drop_candidate` properties from the post-Phase-1 audit.

## Counts

- Statements: 706
- Node label/property rows: 363
- Relationship type/property rows: 343
- Audit property occurrences: 396617

## Files

- Cypher: `_neo4j\review\2026-06-01_minimal_property_audit_post_phase1_p0_mit-bestand\phase2_p1_generated_metadata\minimal_properties_phase2_p1_generated_metadata.cypher`
- Summary: `_neo4j\review\2026-06-01_minimal_property_audit_post_phase1_p0_mit-bestand\phase2_p1_generated_metadata\minimal_properties_phase2_p1_summary.json`

## Protocol

1. Count each statement before apply.
2. Backup `mit-bestand`.
3. Apply grouped Cypher.
4. Verify all targeted P1 rows are zero.
5. Rerun `_scripts/_gap_survey.py` and the minimal-property audit.
