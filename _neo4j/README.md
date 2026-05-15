# Neo4j workspace

Neo4j is the current source of truth for the graph.

This folder exists to support **reproducible intake, review, and import**, not to replace the database as truth.

## Layout

| Path | Purpose |
|---|---|
| `contracts/` | supported input contracts, schemas, templates |
| `processed/` | cleaned import payloads and provenance derived from completed intakes |
| `intake/inbox/` | future raw drops arrive here unchanged |
| `intake/archive/` | preserved raw packages after processing |
| `intake/runs/` | reports and manifests for each processing run |
| `review/` | lineage audits and unresolved trust questions |

## Operating principles

1. Batches and chunks are transport units, not durable domain entities.
2. Keep raw input, processed output, and provenance separate.
3. Merge only by explicit semantic identity rules.
4. Preserve enough lineage to answer:
   - where did this record come from,
   - how was it merged,
   - what still needs review.
5. Anything inherited from the retired `research/` / `_database` workflow is legacy until reviewed.

## Current datasets

| Dataset | Current processed form |
|---|---|
| `projects` | one file per project under `processed/projects/records/` |
| `actor_registry` | one merged dataset under `processed/actor_registry/` |

See `review/LEGACY_LINEAGE_AUDIT.md` before treating any older artifact as current.
