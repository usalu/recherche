# Handoff — Current Neo4j-first state

## Read this first

The repository has changed architecture.

- **Neo4j is the current source of truth.**
- The former folder-based knowledge tree is no longer live.
- `_archive/research/` is historical material only.
- Any script, note, or dataset that still depends on `research/` or `_database/` must be treated as **legacy until reviewed**.

The previous handoff that described `research/` as canonical has been preserved for history at:

```text
_archive/migration/HANDOFF_legacy_research_tree_2026-05-12.md
```

Do not use that older file as current operating guidance.

## Current working model

The durable distinction is now:

| Area | Role |
|---|---|
| Neo4j database | **Truth** |
| `_neo4j/processed/` | cleaned, reproducible import payloads plus provenance |
| `_neo4j/intake/inbox/` | future raw drops |
| `_neo4j/intake/archive/` | preserved raw source packages after processing |
| `_neo4j/intake/runs/` | reports for each processing run |
| `_neo4j/contracts/` | supported input contracts |
| `_neo4j/review/` | lineage and trust reviews |

Read next:

1. `_neo4j/README.md`
2. `_neo4j/review/LEGACY_LINEAGE_AUDIT.md`

## What happened in this cleanup

Two old import areas were reviewed together:

- `_neo4j/batch/` — older project/case-study ingestion packages, still carrying assumptions from the former folder-based system.
- `_neo4j/new/` — actor-registry import chunks, where the chunks were only transport units.

They are being reorganized so that:

- raw historical drops are archived,
- processed outputs are grouped by **dataset**, not by accidental batch folder,
- merge/provenance information is preserved,
- future drops can use one intake lifecycle instead of creating another ad-hoc folder.

## Trust rule

If an artifact originated from the old `research/` / `_database` era:

1. do **not** assume it is current,
2. check `_neo4j/review/LEGACY_LINEAGE_AUDIT.md`,
3. review before promoting it into current Neo4j workflows.

## Legacy scripts

These scripts still reflect the retired folder-first workflow and are not normal import entry points anymore:

- `_scripts/import_database_folder_to_neo4j.py`
- `_scripts/verify_plan_coverage.py`
- `_scripts/build_node_catalogs.py`
- `_scripts/merge_neo4j_schema_export_vocab.py`

They may still be useful for archaeology or controlled review, but they must not be treated as the live pipeline without explicit revision.

## Current next step

Use the Neo4j-first intake path:

1. put new raw packages into `_neo4j/intake/inbox/<dataset>/`,
2. process them with the intake tooling,
3. inspect the generated report,
4. import into Neo4j only after validation/review succeeds.
