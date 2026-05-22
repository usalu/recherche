# Minimal property audit

**Created UTC:** 2026-05-31T23:18:51.661074+00:00
**Database:** `mit-bestand`
**Connection:** `bolt://localhost:7687` as `neo4j`
**Graph counts:** 39160 nodes / 79888 relationships

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
| node | `drop_candidate` | P0 | 36 | 5504 |
| node | `drop_or_archive_meta_node` | P0 | 12 | 195157 |
| node | `keep_minimum` | P0 | 127 | 54499 |
| node | `review_relationship_duplicate` | P0 | 39 | 43734 |
| relationship | `drop_candidate` | P0 | 9 | 2733 |
| relationship | `keep_minimum` | P0 | 69 | 69736 |
| node | `drop_candidate` | P1 | 363 | 209505 |
| node | `keep_minimum` | P1 | 30 | 31286 |
| node | `keep_or_model_fact` | P1 | 7 | 1602 |
| node | `move_to_provenance_model` | P1 | 315 | 168440 |
| relationship | `drop_candidate` | P1 | 343 | 187112 |
| relationship | `review_keep_or_provenance` | P1 | 77 | 27494 |
| relationship | `review_keep_or_source_edge` | P1 | 800 | 348089 |
| node | `review_keep_if_distinct` | P2 | 20 | 778 |
| node | `review_keep_if_used` | P2 | 20 | 90 |
| node | `review_sparse` | P2 | 39 | 474 |
| relationship | `review_duplicate_id` | P2 | 3 | 12235 |
| relationship | `review_sparse` | P2 | 16 | 184 |
| node | `review_domain_property` | P3 | 154 | 44349 |
| relationship | `review_domain_property` | P3 | 119 | 109222 |

## Review/meta node counts

| Label | Nodes |
|---|---:|
| `DataIssue` | 28729 |
| `DeprecatedType` | 13 |
| `DossierEntityTarget` | 2591 |
| `ReuseRule` | 20 |

## Node action bucket counts

| Action | Label/property pairs |
|---|---:|
| `drop_candidate` | 399 |
| `drop_or_archive_meta_node` | 12 |
| `keep_minimum` | 157 |
| `keep_or_model_fact` | 7 |
| `move_to_provenance_model` | 315 |
| `review_domain_property` | 154 |
| `review_keep_if_distinct` | 20 |
| `review_keep_if_used` | 20 |
| `review_relationship_duplicate` | 39 |
| `review_sparse` | 39 |

## Relationship action bucket counts

| Action | Reltype/property pairs |
|---|---:|
| `drop_candidate` | 352 |
| `keep_minimum` | 69 |
| `review_domain_property` | 119 |
| `review_duplicate_id` | 3 |
| `review_keep_or_provenance` | 77 |
| `review_keep_or_source_edge` | 800 |
| `review_sparse` | 16 |
