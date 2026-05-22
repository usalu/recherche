# Semantic minimum property proposal

**Created UTC:** 2026-06-01T06:45:26.169178+00:00
**Database:** `mit-bestand`
**Graph counts:** 39160 nodes / 79888 relationships

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
| P1 | node | `DataIssue` | `migration_origin` | 24436 | generated/import/cache/debug metadata |
| P1 | node | `DataIssue` | `created_at` | 22846 | generated/import/cache/debug metadata |
| P1 | node | `DataIssue` | `source_trace_migration` | 22846 | generated/import/cache/debug metadata |
| P1 | node | `Quelle` | `migration_origin` | 5330 | generated/import/cache/debug metadata |
| P1 | node | `ExternalLink` | `extracted_at` | 5017 | generated/import/cache/debug metadata |
| P1 | node | `ExternalLink` | `migration_origin` | 5017 | generated/import/cache/debug metadata |
| P1 | node | `Quelle` | `extracted_at` | 5017 | generated/import/cache/debug metadata |
| P1 | node | `DataIssue` | `found_at` | 4972 | generated/import/cache/debug metadata |
| P1 | node | `DataIssue` | `found_by` | 4972 | generated/import/cache/debug metadata |
| P1 | node | `DataIssue` | `ref_label` | 4972 | generated/import/cache/debug metadata |
| P1 | node | `DataIssue` | `resolution_note` | 4972 | generated/import/cache/debug metadata |
| P1 | node | `ExternalLink` | `url_last_checked_at` | 2631 | generated/import/cache/debug metadata |
| P1 | node | `ExternalLink` | `url_probe_attempts` | 2631 | generated/import/cache/debug metadata |
| P1 | node | `ExternalLink` | `url_probe_duration_ms` | 2631 | generated/import/cache/debug metadata |
| P1 | node | `Quelle` | `url_last_checked_at` | 2631 | generated/import/cache/debug metadata |
| P1 | node | `Quelle` | `url_probe_attempts` | 2631 | generated/import/cache/debug metadata |
| P1 | node | `Quelle` | `url_probe_duration_ms` | 2631 | generated/import/cache/debug metadata |
| P1 | node | `DossierEntityTarget` | `migration_origin` | 2591 | generated/import/cache/debug metadata |
| P1 | node | `DossierEntityTarget` | `unfolding_origin` | 2591 | generated/import/cache/debug metadata |
| P1 | node | `ExternalLink` | `url_response_headers` | 2560 | generated/import/cache/debug metadata |
| P1 | node | `Quelle` | `url_response_headers` | 2560 | generated/import/cache/debug metadata |
| P1 | node | `ExternalLink` | `first_seen_in_research` | 2386 | generated/import/cache/debug metadata |
| P1 | node | `Quelle` | `first_seen_in_research` | 2386 | generated/import/cache/debug metadata |
| P1 | node | `ExternalLink` | `also_in_research` | 2127 | generated/import/cache/debug metadata |
| P1 | node | `Quelle` | `also_in_research` | 2127 | generated/import/cache/debug metadata |
| P1 | node | `DataIssue` | `ref_labels` | 2084 | generated/import/cache/debug metadata |
| P1 | node | `ExternalLink` | `url_body_cache_format` | 1946 | generated/import/cache/debug metadata |
| P1 | node | `Quelle` | `url_body_cache_format` | 1946 | generated/import/cache/debug metadata |
| P1 | node | `Quelle` | `source_trace_migrated_at` | 1914 | generated/import/cache/debug metadata |
| P1 | node | `Quelle` | `source_trace_migration` | 1914 | generated/import/cache/debug metadata |
| P1 | node | `ExternalLink` | `url_body_cache_path` | 1896 | generated/import/cache/debug metadata |
| P1 | node | `ExternalLink` | `url_body_md5` | 1896 | generated/import/cache/debug metadata |
| P1 | node | `Quelle` | `url_body_cache_path` | 1896 | generated/import/cache/debug metadata |
| P1 | node | `Quelle` | `url_body_md5` | 1896 | generated/import/cache/debug metadata |
| P1 | node | `ExternalLink` | `source_trace_migrated_at` | 1601 | generated/import/cache/debug metadata |
| P1 | node | `ExternalLink` | `source_trace_migration` | 1601 | generated/import/cache/debug metadata |
| P1 | node | `ExternalLink` | `also_in_dossier` | 930 | generated/import/cache/debug metadata |
| P1 | node | `ExternalLink` | `also_in_edge` | 930 | generated/import/cache/debug metadata |
| P1 | node | `ExternalLink` | `also_in_node` | 930 | generated/import/cache/debug metadata |
| P1 | node | `Quelle` | `also_in_dossier` | 930 | generated/import/cache/debug metadata |

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
| node | `ExternalLink` | `also_in_dossier` | list[]:318; list[str]:612 | drop_candidate |
| node | `ExternalLink` | `also_in_edge` | list[]:122; list[str]:808 | drop_candidate |
| node | `ExternalLink` | `also_in_node` | list[]:913; list[str]:17 | drop_candidate |
| node | `ExternalLink` | `url_redirect_chain` | list[]:1827; list[str]:804 | move_to_provenance_model |
| node | `Norm` | `evidence_basis` | list[str]:1; str:68 | move_to_provenance_model |
| node | `Norm` | `evidence_origin` | list[str]:1; str:68 | move_to_provenance_model |
| node | `Norm` | `source_scope` | list[str]:1; str:102 | move_to_provenance_model |
| node | `Projekt` | `co2_facts` | list[]:54; list[str]:27 | review_domain_property |
| node | `Projekt` | `cost_facts` | list[]:9; list[str]:72 | review_domain_property |
| node | `Projekt` | `reuse_share_facts` | list[]:59; list[str]:22 | review_domain_property |
| node | `Quelle` | `also_in_dossier` | list[]:318; list[str]:612 | drop_candidate |
| node | `Quelle` | `also_in_edge` | list[]:122; list[str]:808 | drop_candidate |
| node | `Quelle` | `also_in_node` | list[]:913; list[str]:17 | drop_candidate |
| node | `Quelle` | `url_redirect_chain` | list[]:1827; list[str]:804 | move_to_provenance_model |
| node | `ResearchDocument` | `url_redirect_chain` | list[]:158; list[str]:35 | move_to_provenance_model |
| node | `SectionRef` | `url_redirect_chain` | list[]:416; list[str]:213 | move_to_provenance_model |
| relationship | `BELEGT_IN` | `id` | list[str]:1; str:2119 | keep_minimum |
| relationship | `HAT_AKTEURROLLE` | `id` | list[str]:7; str:1302 | keep_minimum |
| relationship | `HAT_AKTEURTYP` | `evidence_basis` | list[str]:1; str:682 | review_keep_or_source_edge |
| relationship | `HAT_AKTEURTYP` | `id` | list[str]:3; str:680 | keep_minimum |
| relationship | `HAT_STATUS` | `id` | list[str]:3; str:652 | keep_minimum |
