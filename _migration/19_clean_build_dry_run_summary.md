# Phase 19 Clean Build Dry Run Summary

No files were moved, copied, or deleted.

## Outputs

- `_migration/19_clean_build_dry_run_manifest.csv`
- `_migration/19_manual_review_queue.csv`

## Counts By Status

| status | rows |
|---|---:|
| CONFIDENT | 3092 |
| EXCLUDED | 13 |
| REVIEW_REQUIRED | 27 |

## Counts By Action

| action | rows |
|---|---:|
| archive_source_once | 567 |
| create_node | 1 |
| create_schema_folder | 55 |
| delete_from_final | 7 |
| exclude_schema_folder | 7 |
| hold_out_of_final | 6 |
| keep_default | 2346 |
| keep_or_merge | 78 |
| manual_review | 27 |
| merge_to_clean_target | 2 |
| move_to_clean_target | 31 |
| split_to_clean_targets | 5 |

## Meaning

- `CONFIDENT` rows are approved decisions; rows with `delete_from_final` are approved non-imports.
- `REVIEW_REQUIRED` rows must stay in `_manual_review` until manually migrated.
- `EXCLUDED` rows are not part of the first clean database.
- `delete_from_final` rows are staging artifacts or forbidden pseudo-nodes and should not be imported.
