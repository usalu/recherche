# Processed projects dataset

This folder contains cleaned project import payloads derived from the older project-batch export tree.

## Contents

| Path | Meaning |
|---|---|
| `records/` | one retained file per project |
| `vocabulary/controlled_vocabulary.seed.kg.jsonl` | copied seed vocabulary when available |
| `vocabulary/controlled_terms.merged.kg.jsonl` | deduplicated delta-term records from batch exports |
| `provenance/projects.provenance.jsonl` | source paths, collapsed duplicate packaging, review status |
| `merge_report.md` | summary of the processing run |

## Trust status

The retained project corpus is user-confirmed through `batch_015`.

- `batch_001`-`batch_014`: original accepted project-batch chain.
- `batch_015`: accepted 2026-05-15 replacement package for the final five valid old-`gebaeude/` cases.
- old `batch_016`-`batch_020`: removed from the repo and live graph on 2026-05-15 after they failed the old-`gebaeude/` filename provenance rule.
