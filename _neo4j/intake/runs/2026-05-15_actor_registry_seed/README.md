# Run: actor registry seed reorganization

- Raw source archived at: `_neo4j/intake/archive/2026-05-15_actor_registry_seed/raw_tree/`
- Processed output written to: `_neo4j/processed/actor_registry/`
- Review status: `processed_reviewed_structure`

## What changed

- Historical actor-registry chunks were preserved as raw archive.
- The 12 canonical chunk files were merged into one processed dataset.
- Chunk names survive as provenance only.
- Same-ID node conflicts were not hidden: they are flagged in provenance and written to `conflicts/node_conflicts.jsonl`.

See `_neo4j/processed/actor_registry/merge_report.md` and `_neo4j/review/LEGACY_LINEAGE_AUDIT.md`.
