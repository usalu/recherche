# Run: project batches legacy reorganization

- Raw source archived at: `_neo4j/intake/archive/2026-05-15_project_batches_legacy/raw_tree/`
- Processed output written to: `_neo4j/processed/projects/`
- Review status: `legacy_review_required`

## What changed

- Historical batch packaging was preserved as raw archive.
- Duplicate packaged project files were collapsed into one retained project file per filename.
- Project records remain grouped by project, not by historical batch.
- Delta vocabulary records were deduplicated into a merged processed file.

See `_neo4j/processed/projects/merge_report.md` and `_neo4j/review/LEGACY_LINEAGE_AUDIT.md`.
