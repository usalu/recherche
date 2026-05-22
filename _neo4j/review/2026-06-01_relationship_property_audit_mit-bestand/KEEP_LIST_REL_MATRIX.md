# Relationship-property keep-list matrix (round 2, mit-bestand)

Generated from `rel_property_audit.json` / `rel_property_minimization.csv`.

## Baseline

- Relationships: **25,194**
- Property occurrences: **312,649** (avg ~12.4 per edge)
- Distinct relationship types: **76**

## Decision rule

A relationship property is kept **only if it carries genuine semantic meaning or
real evidence content**. Everything else - provenance bookkeeping, cache,
migration/cleanup audit trail, status flags - is dropped. Because the drop set is
effectively "everything that is not on the keep-list", the apply step uses a
**keep-list complement**: for every relationship, remove any property key not in
the keep set below. This is robust against stray bookkeeping keys not individually
enumerated.

## KEEP set (the only properties allowed to remain on any edge)

| Property | Why kept | Coverage (occ) |
| --- | --- | --- |
| `id` | Stable, deterministic edge identifier for addressability + rollback (`r_<from>__<TYPE>__<to>`). Backfilled where missing in Phase J. | 19,884 |
| `datenqualitaet` | Source-grade quality label (`Belegt` etc.) from the processed records. | small |
| `evidence_confidence` | Real confidence of the claim (`belegt` / `teilweise_belegt` / `inferiert` / `unklar`). | ~24,142 |
| `evidence_quote` | Verbatim supporting quote. | small |
| `evidence_url` | Direct evidence URL on edges that carry their own source link (e.g. `HAT_RESSOURCENQUELLE`, `NUTZT_MATERIAL`). | 98 |
| `original_source_excerpt` | Propagation note that records the originating claim. | 315 |
| `pollutant_basis` | Domain basis for `HAS_RISK_POLLUTANT` (`documented` / `material_only` / `era_and_material`). | 339 |
| `rolle` / `role` | Domain role on the relationship. | 209 / 183 |
| `connection_kind` | Domain kind on `VERBUNDEN_MIT_AKTEUR`. | 59 |
| `association_basis` | Domain basis on `BETEILIGT_AN` (why an actor is associated). | 53 |
| `reversibility` | Domain attribute on connection-technique edges. | 6 |
| `property_name` | Names the node property a provenance edge documents. | 20 |
| `inference_basis` | Domain basis for inferred actor links. | 29 |
| `not_confirmed_project_participation` | Semantic uncertainty flag on `BETEILIGT_AN`. | 129 |
| `individual_project_lead_uncertain` | Semantic uncertainty flag. | 2 |

Total kept occurrences: **45,566**.

## DROP set (removed from every edge - bookkeeping / cache / migration trail)

All other keys, dominated by:

`evidence_basis`, `evidence_origin`, `evidence_source_id`, `evidence_excerpt`,
`evidence_quality`, `evidence_note`, `evidence_cleanup_run`,
`evidence_confidence_status`, `previous_evidence_confidence`, `derivation_note`,
`review_status`, `review_run`, `needs_verification`, `is_bookkeeping`,
`archive_source_id`, `source_scope`, `source_role`,
`source_status*` (status / reason / migration / correction\*),
`source_resolution_status*`, `source_review_status*`, `source_url*`,
`verification_*`, `strict_*`, `cleanup_*`, `invalid_*`.

Total dropped occurrences: **267,083** (~85% of all edge properties).

## Safety note on `evidence_source_id`

On `BELEGT_IN` edges `evidence_source_id` duplicates the id of the `Quelle` the
edge already points to (the real evidence link is the edge target, not the
property). It is dropped only after the Phase F safety check (`rel-verify-drop`)
confirms it equals the target id (or is reconciled). No evidence trace is lost:
the URL lives on the `Quelle` node and the link is the `BELEGT_IN` edge itself.
