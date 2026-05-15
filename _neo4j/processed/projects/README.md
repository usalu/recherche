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

This corpus descends from the retired folder-first workflow. It is organized for replay and review, but its files remain `legacy_review_required` or `pending_review` until checked against the live Neo4j graph.
