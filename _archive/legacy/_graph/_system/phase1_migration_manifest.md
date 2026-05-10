# Phase 1 Migration Manifest

- Target root: _graph
- Migrated legacy source files: 177
- Generated stable knot nodes: 176
- Skipped files: 0
- Source map: _migration/legacy_to_new_map.csv
- Source manifest CSV: _migration/phase1_stable_knots_migrated.csv
- Node manifest CSV: _migration/phase1_stable_knots_nodes.csv
- Skipped CSV: _migration/phase1_stable_knots_skipped.csv

This phase is non-destructive. Legacy files were copied, not moved.

Duplicate source rows that target the same node are merged into one node with multiple `legacy_paths`.