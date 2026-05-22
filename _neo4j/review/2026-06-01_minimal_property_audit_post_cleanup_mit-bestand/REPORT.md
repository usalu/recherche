# Minimal property audit

**Created UTC:** 2026-06-01T08:32:29.466299+00:00
**Database:** `mit-bestand`
**Connection:** `bolt://localhost:7687` as `neo4j`
**Graph counts:** 10497 nodes / 31599 relationships

## Outputs

| File | Purpose |
|---|---|
| `node_property_minimization.csv` | Every label/property pair classified for minimum retention. |
| `relationship_property_minimization.csv` | Every reltype/property pair classified for minimum retention. |
| `action_totals.csv` | Counts by action bucket and priority. |
| `patch_ready_drop_candidates.csv` | P0/P1 drop candidates only. |
| `semantic_minimum_proposal.md` | Human-readable minimum schema proposal. |

## Action totals

| Entity | Action | Priority | Pairs | Occurrences |
|---|---|---|---:|---:|
| node | `drop_or_archive_meta_node` | P0 | 1 | 13 |
| node | `keep_minimum` | P0 | 128 | 24608 |
| node | `review_relationship_duplicate` | P0 | 6 | 3294 |
| relationship | `keep_minimum` | P0 | 68 | 26296 |
| node | `keep_minimum` | P1 | 26 | 30640 |
| node | `keep_or_model_fact` | P1 | 7 | 1602 |
| node | `move_to_provenance_model` | P1 | 22 | 2873 |
| relationship | `review_keep_or_provenance` | P1 | 76 | 27421 |
| relationship | `review_keep_or_source_edge` | P1 | 792 | 273772 |
| node | `review_keep_if_distinct` | P2 | 13 | 365 |
| node | `review_keep_if_used` | P2 | 5 | 19 |
| node | `review_sparse` | P2 | 1 | 16 |
| relationship | `review_duplicate_id` | P2 | 3 | 12235 |
| relationship | `review_sparse` | P2 | 17 | 211 |
| node | `review_domain_property` | P3 | 68 | 18029 |
| relationship | `review_domain_property` | P3 | 123 | 109643 |

## Review/meta node counts

| Label | Nodes |
|---|---:|
| `DeprecatedType` | 13 |
| `DossierEntityTarget` | 2591 |
| `ReuseRule` | 20 |

## Node action bucket counts

| Action | Label/property pairs |
|---|---:|
| `drop_or_archive_meta_node` | 1 |
| `keep_minimum` | 154 |
| `keep_or_model_fact` | 7 |
| `move_to_provenance_model` | 22 |
| `review_domain_property` | 68 |
| `review_keep_if_distinct` | 13 |
| `review_keep_if_used` | 5 |
| `review_relationship_duplicate` | 6 |
| `review_sparse` | 1 |

## Relationship action bucket counts

| Action | Reltype/property pairs |
|---|---:|
| `keep_minimum` | 68 |
| `review_domain_property` | 123 |
| `review_duplicate_id` | 3 |
| `review_keep_or_provenance` | 76 |
| `review_keep_or_source_edge` | 792 |
| `review_sparse` | 17 |
