# Semantic minimum property proposal

**Created UTC:** 2026-05-31T23:18:51.658077+00:00
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
| P0 | node | `DataIssue` | `candidate_source_count` | 3620 | derivable by query; should not live as stored property |
| P0 | node | `Akteur` | `candidate_source_count` | 553 | derivable by query; should not live as stored property |
| P0 | node | `Bauteilgruppe` | `candidate_source_count` | 304 | derivable by query; should not live as stored property |
| P0 | node | `Bauwerk` | `candidate_source_count` | 172 | derivable by query; should not live as stored property |
| P0 | node | `Kennwert` | `candidate_source_count` | 162 | derivable by query; should not live as stored property |
| P0 | node | `PruefungNachweis` | `candidate_source_count` | 113 | derivable by query; should not live as stored property |
| P0 | node | `Projekt` | `candidate_source_count` | 85 | derivable by query; should not live as stored property |
| P0 | node | `Norm` | `candidate_source_count` | 78 | derivable by query; should not live as stored property |
| P0 | node | `Quelle` | `candidate_source_count` | 78 | derivable by query; should not live as stored property |
| P0 | node | `Dossier` | `candidate_source_count` | 76 | derivable by query; should not live as stored property |
| P0 | node | `Aufbereitungsverfahren` | `candidate_source_count` | 52 | derivable by query; should not live as stored property |
| P0 | node | `Leistungsanforderung` | `candidate_source_count` | 41 | derivable by query; should not live as stored property |
| P0 | node | `Materialdepot` | `candidate_source_count` | 22 | derivable by query; should not live as stored property |
| P0 | node | `ReuseRule` | `candidate_source_count` | 20 | derivable by query; should not live as stored property |
| P0 | node | `Wiederverwendungskette` | `candidate_source_count` | 14 | derivable by query; should not live as stored property |
| P0 | node | `Programm` | `candidate_source_count` | 13 | derivable by query; should not live as stored property |
| P0 | node | `Programm` | `usage_countries` | 11 | derivable by query; should not live as stored property |
| P0 | node | `Programm` | `usage_project_count` | 11 | derivable by query; should not live as stored property |
| P0 | node | `Material` | `candidate_source_count` | 10 | derivable by query; should not live as stored property |
| P0 | node | `Software` | `candidate_source_count` | 10 | derivable by query; should not live as stored property |
| P0 | node | `Bauteiltyp` | `candidate_source_count` | 8 | derivable by query; should not live as stored property |
| P0 | node | `Programm` | `classified_at` | 6 | known legacy/intake key from older cleanup plans |
| P0 | node | `Norm` | `classified_at` | 5 | known legacy/intake key from older cleanup plans |
| P0 | node | `Norm` | `not_yet_referenced_in_corpus` | 5 | known legacy/intake key from older cleanup plans |
| P0 | node | `Norm` | `scope` | 5 | known legacy/intake key from older cleanup plans |
| P0 | node | `Norm` | `topic` | 5 | known legacy/intake key from older cleanup plans |
| P0 | node | `Tool` | `candidate_source_count` | 4 | derivable by query; should not live as stored property |
| P0 | node | `Leistungsanforderung` | `classified_at` | 3 | known legacy/intake key from older cleanup plans |
| P0 | node | `Schadstoff` | `scope` | 3 | known legacy/intake key from older cleanup plans |
| P0 | node | `Schadstoff` | `topic` | 3 | known legacy/intake key from older cleanup plans |
| P0 | node | `Verbindungstechnik` | `candidate_source_count` | 3 | derivable by query; should not live as stored property |
| P0 | node | `Leistungsanforderung` | `not_yet_referenced_in_corpus` | 2 | known legacy/intake key from older cleanup plans |
| P0 | node | `Leistungsanforderung` | `scope` | 2 | known legacy/intake key from older cleanup plans |
| P0 | node | `Leistungsanforderung` | `topic` | 2 | known legacy/intake key from older cleanup plans |
| P0 | node | `ResearchDocument` | `candidate_source_count` | 2 | derivable by query; should not live as stored property |
| P0 | node | `Akteur` | `akteur_kontext_text` | 1 | known legacy/intake key from older cleanup plans |
| P0 | relationship | `HAT_AKTEURROLLE` | `scope` | 1053 | legacy or query-derivable relationship metadata |
| P0 | relationship | `BELEGT_IN` | `candidate_source_count` | 644 | legacy or query-derivable relationship metadata |
| P0 | relationship | `VERBUNDEN_MIT_AKTEUR` | `scope` | 210 | legacy or query-derivable relationship metadata |
| P0 | relationship | `GEHÖRT_ZU` | `scope` | 209 | legacy or query-derivable relationship metadata |

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
| node | `Programm` | `usage_countries` | list[]:1; list[str]:10 | drop_candidate |
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
| relationship | `HAT_AKTEURROLLE` | `scope` | list[str]:2; str:1051 | drop_candidate |
| relationship | `HAT_AKTEURTYP` | `evidence_basis` | list[str]:1; str:682 | review_keep_or_source_edge |
| relationship | `HAT_AKTEURTYP` | `id` | list[str]:3; str:680 | keep_minimum |
| relationship | `HAT_STATUS` | `id` | list[str]:3; str:652 | keep_minimum |
