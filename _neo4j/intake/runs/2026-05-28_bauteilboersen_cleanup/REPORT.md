# Bauteilboersen cleanup report

Date: 2026-05-28  
Database: `mit-bestand`

## Scope

Cleaned only reciprocal `VERBUNDEN_MIT_AKTEUR` relationships touching:

- actors typed `at_materialhub_bauteilboerse`;
- `bauteilnetz_deutschland`.

No node merges were applied. Live Neo4j already had canonical `rotordc` and `cleveland_steel_tubes` nodes; the duplicate-looking `a_*` IDs found in processed files were not present as live duplicate targets.

High-risk duplicate evidence/citation relationships such as `BELEGT_IN` and `CITED_FROM_DOSSIER` were not touched.

## Backup

Logical backup before writes:

`_neo4j/review/backups/2026-05-28_pre_bauteilboersen_cleanup`

Backup counts:

- nodes: 39,517
- relationships: 80,702

## Applied cleanup

Script:

`_scripts/cleanup_bauteilboersen_links.py --apply`

Outcome:

- reciprocal candidate pairs: 27
- inverse relationships removed: 27
- kept relationships annotated with `cleanup_bauteilboersen_bidirectional_dedup_run`
- removed inverse relationships archived in `removed_inverse_relationships.jsonl`

Post-apply counts:

- nodes: 39,517
- relationships: 80,675
- reciprocal Bauteilboersen/materialhub actor pairs remaining: 0
- annotated kept relationships: 27

## Verification files

- `dry_run_report.json`
- `apply_report.json`
- `post_apply_verification.json`
- `dry_run_reciprocal_candidates.json`
- `apply_reciprocal_candidates.json`
- `removed_inverse_relationships.jsonl`

## Gap survey note

`python _scripts/_gap_survey.py` was run before and after. Existing broader failures remain, but this cleanup only changed the intended relationship count by -27 and did not create actor orphans.
