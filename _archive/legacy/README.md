# Legacy archive (removed from the working tree)

The former `_archive/legacy/` subtree (old `_graph/`, `_extract/`, `_manual_review/`, pre-`_database/` entity stubs, etc.) was **deleted from this repository** in **2026-05** after consolidation into `_database/`.

- **Canonical knowledge and edges:** `_database/` (see `_database/_system/SCHEMA.md`).
- **Normative graph contract:** [`.cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md`](../../.cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md) and `_scripts/import_database_folder_to_neo4j.py`.
- **Recovery:** use `git log` / `git show` on commits before the removal, or restore paths from an older clone — nothing was rewritten with `--force` on the remote; history still contains the blobs until garbage-collected locally.

Dropped-knot prose (taxonomy decisions) remains under `_archive/dropped_knots/` (separate folder).
