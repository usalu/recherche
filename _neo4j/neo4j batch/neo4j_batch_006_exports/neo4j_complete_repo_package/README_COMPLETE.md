# Neo4j Complete Repo Package

This package contains the repo-ready Neo4j import contract plus all generated batch exports currently available.

## Contents

- `controlled_vocabulary.seed.kg.jsonl` — global controlled vocabulary seed.
- `cypher/constraints.cypher` — Neo4j uniqueness constraints.
- `schemas/` — JSON schemas for records and manifests.
- `templates/` — project/delta/manifest templates. Template placeholders are not meant to be imported directly.
- `batches/` — generated project batches ready for import.
- `docs/prompts_and_planning/` — migration source-of-truth prompt and planning templates.
- `archive_individual_batch_zips/` — previously generated individual ZIP exports.
- `PACKAGE_MANIFEST.json` — aggregate package inventory and validation summary.

## Included batches

- `batch_001`
- `batch_002`
- `batch_003`
- `batch_004`
- `batch_005`
- `batch_006`
- `batch_007`

## Import order for agents / MCP

1. Run `cypher/constraints.cypher` once.
2. Import `controlled_vocabulary.seed.kg.jsonl` once.
3. For each batch, import `controlled_terms.delta.jsonl` first.
4. Then import every `p_*.kg.jsonl` project chunk in that batch.
5. Use `id` as the stable upsert key for nodes and relationships.
6. For relationships, upsert by relationship `id`, with `from`, `type`, and `to` as consistency checks.

Do not import files under `templates/`; they are examples only.

## Validation summary

- JSON/JSONL syntax: PASS
- Relationship endpoint check for importable JSONL: PASS
- JSONL files: 44
- Records: 8021
- Nodes: 982
- Relationships: 7039
- Unique node ids: 928

See `PACKAGE_MANIFEST.json` for full counts.
