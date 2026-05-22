# Semantic minimum property proposal

**Created UTC:** 2026-06-01T08:32:29.463299+00:00
**Database:** `mit-bestand`
**Graph counts:** 10497 nodes / 31599 relationships

## Minimum rule set

| Object | Minimum properties | Notes |
|---|---|---|
| All semantic nodes | `id`, `name` | `name_full`, `aliases`, `note` only when actively useful. |
| Controlled vocabulary nodes | `id`, `name`, `scope_note` | Drop import/debug fields; keep definitions. |
| `Quelle` / source nodes | `id`, `name`, `url`, `quelltyp`, maybe `source_file` | Probe/cache state should be external or normalized, not spread across node bags. |
| `Kennwert` facts | `id`, `kennwert`, `wert`/`wert_text`, `einheit`, `method`, `bilanzgrenze` | Keep only if the graph keeps fact nodes; otherwise model as relationships. |
| Relationships | `id` plus normalized provenance only where needed | Edge provenance should be consistent, not arbitrary evidence/cache fields. |
| Review/meta nodes | none in semantic graph | Archive/compact `DataIssue` and similar nodes unless they are part of active QA workflow. |

## Patch-ready drop candidates

These are classification candidates only. Review samples before generating a patch.

| Priority | Entity | Group | Property | Occurrences | Reason |
|---|---|---|---|---:|---|

## Do not blindly delete

- `source_scope` is messy but provenance-critical; normalize before removing.
- `evidence_*` may be wrong on semantic nodes but still needs migration into a source/edge model if it is the only provenance.
- `primary_material_id`, `primary_bauteiltyp_id`, `reuse_status`, `land`, and similar fields likely duplicate relationships; confirm relationship coverage first.
- `DataIssue` volume should be handled as a graph-model decision, not a property-only cleanup.

## Type drift pairs

| Entity | Group | Property | Types | Action |
|---|---|---|---|---|
| node | `Bauteilgruppe` | `tragend` | bool:121; str:3 | review_domain_property |
| node | `DossierEntityTarget` | `exact_match_candidate_ids` | list[]:2282; list[str]:309 | review_relationship_duplicate |
| relationship | `BELEGT_IN` | `id` | list[str]:1; str:2119 | keep_minimum |
| relationship | `HAT_AKTEURROLLE` | `id` | list[str]:7; str:1302 | keep_minimum |
| relationship | `HAT_AKTEURTYP` | `evidence_basis` | list[str]:1; str:673 | review_keep_or_source_edge |
| relationship | `HAT_AKTEURTYP` | `id` | list[str]:3; str:671 | keep_minimum |
| relationship | `HAT_STATUS` | `id` | list[str]:3; str:652 | keep_minimum |
