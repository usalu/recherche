# Legacy lineage audit

**Date:** 2026-05-15  
**Reason:** The repository was migrated away from the old folder-based `research/` / `_database` workflow. Neo4j is now the source of truth.

## Summary

| Area | Current reading | Status |
|---|---|---|
| `_archive/research/` | historical folder tree from the former workflow | `legacy_only` |
| former root guidance in `AGENTS.md` / `HANDOFF.md` | incorrectly described `research/` as live | `superseded` |
| `_neo4j/batch/` | project/case-study import history built under the former folder-first assumptions | `needs_review_before_current_use` |
| `_neo4j/new/` | actor-registry import history; more Neo4j-native, but still includes reconciliation inherited from the older era | `reviewed_for_structure`, `semantic_review_still_recommended` |

## Stale references found outside the archive

These live files still mentioned `research/` or `_database/` before this cleanup:

- `AGENTS.md`
- `HANDOFF.md`
- `_neo4j/batch/PIPELINE.md`
- `_neo4j/batch/ANALYSIS.md`
- `_scripts/import_database_folder_to_neo4j.py`
- `_scripts/verify_plan_coverage.py`
- `_scripts/build_node_catalogs.py`
- `_scripts/merge_neo4j_schema_export_vocab.py`
- `_scripts/export_neo4j_schema.py`
- `_scripts/neo4j_graph_version.py`
- `_scripts/transform_registry_jsonl_to_canonical.py` (comment only)

## Trust classification

### `projects`

Observed under the former `_neo4j/batch/` tree:

- batches `001–014`: documented and validated in the old workflow;
- batches `015–020`: present without matching manifest / agent notes / validation reports;
- `neo4j_batch_006_exports/neo4j_complete_repo_package/`: package snapshot containing duplicate copies of earlier batches.

Initial status:

| Slice | Status | Why |
|---|---|---|
| `001–014` | `legacy_review_required` | likely useful, but lineage depends on retired folder-first assumptions |
| `015–020` | `pending_review` | incomplete package metadata |
| duplicate package snapshot | `archived_duplicate` | packaging artifact, not a separate current dataset |

### `actor_registry`

Observed under the former `_neo4j/new/` tree:

- 12 transport chunks;
- 12 derived canonical chunk files;
- 703 node records collapse to 588 unique node IDs;
- 2896 relationship records collapse to 2639 unique semantic relationships.

Initial status:

| Slice | Status | Why |
|---|---|---|
| source chunks | `archived_input` | transport units only |
| merged processed dataset | `processed_reviewed_structure` | safe structural dedupe performed; semantic identity decisions still deserve periodic review |

## Legacy scripts requiring explicit review before reuse

| Script | Why it is legacy-sensitive |
|---|---|
| `_scripts/import_database_folder_to_neo4j.py` | assumes folder tree input as the import source |
| `_scripts/verify_plan_coverage.py` | validates the retired folder-first model |
| `_scripts/build_node_catalogs.py` | emits docs from old inventory files |
| `_scripts/merge_neo4j_schema_export_vocab.py` | merges schema with old `_database` inventory |
| `_scripts/export_neo4j_schema.py` | still documents the old output location |
| `_scripts/neo4j_graph_version.py` | still documents old `_database` storage |
| `_scripts/run_neo4j_current_build_review.py` | reads the archived `_neo4j/batch/` tree. **Superseded** by `_scripts/run_neo4j_round002_baseline.py` (2026-05-15). Left in place as the reproducible record of the pre-cleanup round-001 audit; do not run against the current state. |

## Rule going forward

If a file, script, or dataset derives authority from `research/` or `_database/`, it is **not current by default**. It must be:

1. reviewed against the live Neo4j graph,
2. reclassified,
3. then either promoted, rewritten, or retired.
