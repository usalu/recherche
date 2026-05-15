# Processed actor registry dataset

This folder contains the merged actor-registry payload derived from the former transport chunks.

## Contents

| Path | Meaning |
|---|---|
| `actor_registry.canonical.kg.jsonl` | merged canonical import payload |
| `provenance/actor_registry.provenance.jsonl` | one provenance row per merged node/relationship |
| `conflicts/node_conflicts.jsonl` | same-ID node records that differed across chunks and still need review |
| `merge_report.md` | dedupe summary and conflict note |

## Merge model

- Nodes merge by canonical `id`.
- Relationships merge by `(from, type, to, scope)`.
- Old chunk names remain as provenance only.

Neo4j remains the source of truth; this file is a cleaned import artifact, not the authority itself.
