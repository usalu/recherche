# 07 Freeze and Release Plan

## Goal

Create a stable repo release after patches are reviewed and applied.

## Freeze steps

1. Apply accepted patches to a staging graph or staging export.
2. Run global technical audit again.
3. Merge accepted controlled vocabulary deltas into:
   ```text
   vocabulary/controlled_vocabulary.seed.kg.jsonl
   ```
4. Merge accepted canonical names and aliases into:
   ```text
   registry/canonical_nodes.jsonl
   registry/aliases.jsonl
   ```
5. Regenerate:
   ```text
   all_batches_manifest.json
   ```
6. Run post-import Neo4j validation queries.
7. Produce release notes.

## Release output

```text
releases/
  v0.2-normalized/
    release_manifest.json
    release_notes.md
    validation_report.md
    accepted_patches/
    rejected_patches/
```

## Freeze criteria

Do not freeze unless:

```text
0 JSON parse errors
0 relationship endpoint errors
0 Fallbeispiel nodes
0 Kennwert nodes
0 BELEGT_IN without datenqualitaet=Belegt
0 duplicate relationship ids with conflicting endpoints
0 controlled terms without parent category when required
all project chunks have source links
all Bauteilgruppen have Bauteiltyp and evidence source
```
