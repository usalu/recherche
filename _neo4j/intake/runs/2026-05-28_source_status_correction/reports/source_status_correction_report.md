# Source Status Correction Report

- Database: `mit-bestand`
- Migration: `mig_source_status_correction_2026_05_28`
- Started: `2026-05-28T11:17:58.813088+00:00`

## Rule

`source_status` is only for fact/claim evidence. Lineage and audit edges may retain URLs as context, but they must not be marked `exact`, `candidate`, or `missing` source proof.

## Writes

- `backed_up_relationships`: 9670
- `lineage_status_removed`: 6150
- `audit_status_removed`: 3520

## Gates

- `zitiert_remaining`: `0`
- `non_fact_relationships_with_source_status`: `0`
- `non_fact_relationships_marked_exact`: `0`
- `fact_exact_url_without_exact_status`: `0`
- `fact_exact_status_without_url`: `0`
- `fact_candidate_urls_without_candidate_status`: `0`
- `review_relationship_with_trusted_url`: `0`

## Backup

- `E:/recherche/_neo4j/intake/runs/2026-05-28_source_status_correction/logs/removed_non_fact_source_status_backup.jsonl`

## Addendum

- Additional scope cleanup: `_neo4j/intake/runs/2026-05-28_source_status_correction/reports/source_status_scope_addendum_report.md`
- This also removed `source_status` from `ANCHORED_BY` and `HAS_SOURCE_LINK`, because they are bookkeeping/source-inventory edges rather than fact proof.
