# Source Status Normalization Report

- Database: `mit-bestand`
- Migration: `mig_source_status_normalization_2026_05_28`
- Started: `2026-05-28T10:57:15.458609+00:00`

## Rule

`exact` means a concrete valid URL is already on the fact relationship. `candidate` means only review leads exist. `missing` means no exact URL binding is known and review is required.

## Writes

- `direct_valid_endpoint_relationships_stamped`: 0
- `invalid_endpoint_fact_relationships_marked_missing`: 8
- `relationships_marked_exact`: 12841
- `relationships_marked_candidate`: 3666
- `relationships_marked_missing`: 17350

## Gates

- `zitiert_remaining`: `0`
- `exact_url_without_exact_status`: `0`
- `candidate_urls_without_candidate_status`: `0`
- `needs_review_without_candidate_or_missing`: `0`
- `review_relationship_with_trusted_url`: `0`
- `malformed_exact_source_url`: `0`
- `malformed_candidate_source_urls`: `{'relationships': 0, 'bad_urls': 0}`
- `direct_valid_endpoint_unstamped_non_audit`: `0`

## Notes

- Superseded in part by `_neo4j/intake/runs/2026-05-28_source_status_correction/reports/source_status_correction_report.md` and `_neo4j/intake/runs/2026-05-28_source_status_correction/reports/source_status_scope_addendum_report.md`: non-fact lineage/audit/bookkeeping/source-inventory edges were corrected so `CITED_FROM_DOSSIER`, `CONCERNS`, `ANCHORED_BY`, and `HAS_SOURCE_LINK` no longer carry `source_status`.
- No `.md` container or Dossier/ResearchDocument node was promoted to source truth.
- Invalid direct URL endpoints were exported for review and marked `missing` only when they were non-audit fact relationships.
- Candidate URL arrays remain candidates and are not counted as exact source coverage.
