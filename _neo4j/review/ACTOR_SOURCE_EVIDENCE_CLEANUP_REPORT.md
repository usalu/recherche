# Actor Source Evidence Cleanup Report

Date: 2026-05-28  
Database: `mit-bestand`  
Scope: global `Akteur` role/type/country evidence hygiene, with specific cleanup of the 2026-05-28 Bauteilboersen integration run.

## What Was Changed

- Applied `_neo4j/review/actor_source_evidence_cleanup.patch.jsonl`.
- Backup before apply: `_neo4j/review/backups/2026-05-28_pre_actor_source_evidence_cleanup`.
- Graph counts changed from 39,548 nodes / 81,064 relationships to 39,548 nodes / 81,031 relationships.
- Removed 33 duplicate recent country-path relationships of type `GEHÖRT_ZU` from actors to countries. The direct `LIEGT_IN_LAND` country relationship remains the country path.
- Removed all 147 recent `evidence_terms` properties from Bauteilboersen `HAT_AKTEURROLLE` relationships.
- Marked recent Bauteilboersen role/type/country/operator relationships as `needs_source_url_review` with `source_resolution_status = "needs_exact_claim_source_review"`.
- Marked older global actor role/type/country relationships whose `evidence_source_id` does not resolve to a visible `Quelle.url` as `needs_source_url_review` with `source_resolution_status = "evidence_source_id_not_resolved_to_visible_source_url"`.

## Post-Apply Validation

Validation output was written to:

- `_neo4j/review/actor_source_evidence_cleanup_postcheck.json`
- `_neo4j/review/actor_source_evidence_source_metadata_postcheck.json`

Key results:

| Check | Result |
|---|---:|
| Current graph size | 39,548 nodes / 81,031 relationships |
| Recent Bauteilboersen actor-country `GEHÖRT_ZU` duplicates | 0 |
| Recent Bauteilboersen `HAT_AKTEURROLLE.evidence_terms` | 0 |
| Recent forbidden relation types `HAS_DATA_ISSUE`, `ANCHORED_BY`, `BETEILIGT_AN`, `ZITIERT_QUELLE` | 0 |
| `q_url_*` Quelle nodes | 3,571 |
| `q_url_*` Quelle nodes with visible URL | 3,571 |
| Internal/missing-url actor role/type/country relationships left unmarked | 0 |

Recent Bauteilboersen relationship status after cleanup:

| Relationship type | Count | Status |
|---|---:|---|
| `BETRIEBEN_VON` | 2 | `needs_source_url_review` |
| `HAT_AKTEURROLLE` | 147 | `needs_source_url_review` |
| `HAT_AKTEURTYP` | 35 | `needs_source_url_review` |
| `LIEGT_IN_LAND` | 33 | `needs_source_url_review` |

Global internally sourced actor facts now marked:

| Relationship type | Count | Status |
|---|---:|---|
| `HAT_AKTEURROLLE` | 1,178 | `needs_source_url_review` |
| `HAT_AKTEURTYP` | 657 | `needs_source_url_review` |
| `LIEGT_IN_LAND` | 201 | `needs_source_url_review` |

## Source Metadata Gap

The cleanup did not pretend to resolve bibliographic metadata that is not present in the graph.

For all `q_url_*` Quelle nodes:

| Field | Count |
|---|---:|
| `url` | 3,571 / 3,571 |
| `title` | 885 / 3,571 |
| `publisher` | 0 / 3,571 |
| `retrieved_at` / `retrieved_date` / `accessed_at` | 0 / 3,571 |

For recent Bauteilboersen `BELEGT_IN` source relationships:

| Field on target Quelle | Count |
|---|---:|
| `url` | 131 / 131 |
| `title` | 1 / 131 |
| `publisher` | 0 / 131 |
| retrieved/accessed date | 0 / 131 |

## Important Limit

This was an evidence hygiene and de-risking pass, not a completed global source-reading audit.

No relationship was upgraded to verified unless the graph already had the required explicit source structure. Relationships without resolvable source URLs, or without exact claim-level verification, were downgraded to review-needed status instead of being treated as proven.

The remaining work is a source-by-source claim audit: open each actor-specific URL, extract title, publisher, retrieved date, and the exact claim supported, then attach the corresponding `Quelle` to the exact role/country/type/operator relationship it proves. Generic circular-construction pages, vague marketplace terms, and inherited review statuses should not be used as proof.

