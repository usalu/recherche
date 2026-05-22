# Semantic minimum property proposal

**Created UTC:** 2026-06-01T07:11:05.903743+00:00
**Database:** `mit-bestand`
**Graph counts:** 39165 nodes / 80135 relationships

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
| node | `Akteur` | `source_scope` | list[str]:5; str:664 | move_to_provenance_model |
| node | `Bauteilgruppe` | `direct_reuse_relevant` | bool:7; str:1 | review_sparse |
| node | `Bauteilgruppe` | `menge_m2` | float:2; int:12 | review_sparse |
| node | `Bauteilgruppe` | `menge_t` | float:3; int:4 | review_sparse |
| node | `Bauteilgruppe` | `tragend` | bool:121; str:3 | review_domain_property |
| node | `DossierEntityTarget` | `exact_match_candidate_ids` | list[]:2282; list[str]:309 | review_relationship_duplicate |
| node | `ExternalLink` | `url_redirect_chain` | list[]:1827; list[str]:804 | move_to_provenance_model |
| node | `Norm` | `evidence_basis` | list[str]:1; str:68 | move_to_provenance_model |
| node | `Norm` | `evidence_origin` | list[str]:1; str:68 | move_to_provenance_model |
| node | `Norm` | `source_scope` | list[str]:1; str:102 | move_to_provenance_model |
| node | `Projekt` | `co2_facts` | list[]:54; list[str]:27 | review_domain_property |
| node | `Projekt` | `cost_facts` | list[]:9; list[str]:72 | review_domain_property |
| node | `Projekt` | `reuse_share_facts` | list[]:59; list[str]:22 | review_domain_property |
| node | `Quelle` | `url_redirect_chain` | list[]:1827; list[str]:804 | move_to_provenance_model |
| node | `ResearchDocument` | `url_redirect_chain` | list[]:158; list[str]:35 | move_to_provenance_model |
| node | `SectionRef` | `url_redirect_chain` | list[]:416; list[str]:213 | move_to_provenance_model |
| relationship | `BELEGT_IN` | `id` | list[str]:1; str:2119 | keep_minimum |
| relationship | `HAT_AKTEURROLLE` | `id` | list[str]:7; str:1302 | keep_minimum |
| relationship | `HAT_AKTEURTYP` | `evidence_basis` | list[str]:1; str:673 | review_keep_or_source_edge |
| relationship | `HAT_AKTEURTYP` | `id` | list[str]:3; str:671 | keep_minimum |
| relationship | `HAT_STATUS` | `id` | list[str]:3; str:652 | keep_minimum |
