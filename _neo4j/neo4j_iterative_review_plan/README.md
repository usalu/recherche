# Neo4j Iterative Review Plan

Version: 1.0  
Date: 2026-05-14  
Purpose: Give repo agents a clear, repeatable plan to audit, correct, and optimize the Neo4j JSONL exports without rewriting everything.

## Core principle

Do **not** edit generated batch files directly during review.

Agents should produce:
1. a short report,
2. a patch file,
3. a manifest for the patch,
4. optional registry/vocabulary updates.

Original extraction files remain traceable. Corrections are applied through idempotent patch files.

## Recommended repo location

```text
neo4j_exports/
  review_plan/
    README.md
    plans/
    templates/
    schemas/
    examples/

  review/
    round_001/
      global_audit_report.md
      patch_manifest.json
      patches/
        global_technical.patch.jsonl
        canonical_nodes.patch.jsonl
        controlled_vocabulary.patch.kg.jsonl
        batch_001_content.patch.jsonl
      decisions.md
```

## Review rhythm

| Review type | Size | Frequency | Output |
|---|---:|---|---|
| Global technical audit | all available batches | every round | audit report + global patch |
| Controlled vocabulary review | 1 label family at a time | every round until stable | vocabulary/canonical patch |
| Project content review | 5 projects per run | continuously | batch patch + notes |
| Query-driven review | 1 research query, top 25 suspicious rows | after graph import | query report + patch |
| Freeze/release | all validated patches | after review rounds | release manifest |

## Best chunk sizes

- **Project content review:** 5 projects per agent run. Use 6 only when a source batch already has 6 files.
- **Controlled vocabulary review:** 1 label family per run, max 100 controlled nodes.
- **Canonical registry review:** max 100 duplicate/conflict candidates per run.
- **Patch file size:** max 250 operations per patch file. Split larger work into multiple files.
- **Query-driven review:** one query theme per run, max 25 suspicious results.
- **Final import validation:** all batches at once.

## Final target

A clean, stable, source-traceable graph where:
- `Projekt` is the root case node,
- `Bauteilgruppe` is the reusable component occurrence node,
- `Bauwerk` handles donor/receiver/physical-object logic,
- `Quelle` is the source-of-truth evidence node,
- metrics remain scalar properties,
- reusable concepts are nodes,
- patch files are idempotent and reviewable.
