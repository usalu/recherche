# Source Status Scope Addendum

- Database: `mit-bestand`
- Migration: `mig_source_status_scope_addendum_2026_05_28`
- Started: `2026-05-28T11:20:41.516514+00:00`

## Rule

`ANCHORED_BY` is ontology bookkeeping and `HAS_SOURCE_LINK` is source inventory. Neither is fact proof, so neither should carry `source_status`.

## Writes

- `backed_up_relationships`: 723
- `anchored_by_status_removed`: 703
- `has_source_link_status_removed`: 20

## Gates

- `all_non_fact_relationships_with_source_status`: `0`
- `anchored_by_needs_source_review`: `0`
- `fact_exact_status_without_url`: `0`
- `fact_url_without_exact_status`: `0`

## Backup

- `E:/recherche/_neo4j/intake/runs/2026-05-28_source_status_correction/logs/removed_scope_source_status_backup.jsonl`
