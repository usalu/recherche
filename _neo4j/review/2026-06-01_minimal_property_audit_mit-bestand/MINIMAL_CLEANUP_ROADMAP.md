# Minimal property cleanup roadmap

**Audit date:** 2026-06-01 Europe/Berlin  
**Database:** `mit-bestand`  
**Mode:** read-only audit; no graph writes

## Baseline

Live graph at scan time:

- 39,160 nodes.
- 79,888 relationships.
- 611,239 node-property occurrences.
- 756,805 relationship-property occurrences.
- Average node property count: 15.61.
- Average relationship property count: 9.47.

Classification outputs:

- `node_property_minimization.csv` — every label/property pair.
- `relationship_property_minimization.csv` — every reltype/property pair.
- `patch_ready_drop_candidates.csv` — P0/P1 drop candidates.
- `semantic_minimum_proposal.md` — minimum-retention rule set.

## Extreme-minimum target

Keep as the default:

- Semantic nodes: `id`, `name`.
- Controlled vocab: `id`, `name`, `scope_note`.
- Source nodes: `id`, `name`, `url`, `quelltyp`; maybe `source_file`.
- Fact nodes, if retained: only the literal fact fields (`kennwert`, `wert` / `wert_text`, `einheit`, `method`, `bilanzgrenze`).
- Relationships: `id`, plus one normalized provenance shape only where the relationship itself needs evidence.

Everything else must justify itself by query use, semantic non-derivability, or provenance necessity.

## Cleanup Phases

### Phase 1 — P0 property drops

Patch-ready after sample review:

- Node P0 drops: 36 label/property pairs, 5,504 occurrences.
- Relationship P0 drops: 9 reltype/property pairs, 2,733 occurrences.
- Total: 8,237 stored properties.

Main buckets:

- `candidate_source_count` across `DataIssue`, `Akteur`, `Bauteilgruppe`, `Bauwerk`, `Kennwert`, `Projekt`, `Quelle`, etc.
- `Programm.usage_countries`, `Programm.usage_project_count`.
- legacy `classified_at`, `scope`, `topic`, `not_yet_referenced_in_corpus`.
- relationship `scope` on `HAT_AKTEURROLLE`, `VERBUNDEN_MIT_AKTEUR`, `GEHÖRT_ZU`, `HAT_AKTEURTYP`, `LIEGT_IN_LAND`, `STUB_PROJECT_LINK`.
- `BELEGT_IN.candidate_source_count`.

This is the safest first patch because these are derivable or known legacy keys.

### Phase 2 — Generated/cache/import metadata drops

P1 drop candidates:

- Node P1 drops: 363 label/property pairs, 209,505 occurrences.
- Relationship P1 drops: 343 reltype/property pairs, 187,112 occurrences.
- Total: 396,617 stored properties.

High-volume examples:

- `DataIssue.migration_origin`, `DataIssue.created_at`, `DataIssue.source_trace_migration`.
- `CONCERNS.migration_origin`.
- `CITED_FROM_DOSSIER.unfolding_origin`, `imported_at_utc`, `source_status_corrected_at`, `migration_origin`.
- `Quelle` / `ExternalLink` URL probe/cache fields: `url_last_checked_at`, `url_probe_attempts`, `url_probe_duration_ms`, `url_response_headers`, `url_body_cache_path`, `url_body_md5`.
- repeated migration/status-normalization timestamps on `BELEGT_IN`, `CONCERNS`, `LIEGT_IN_LAND`, `HAT_MATERIALGRUPPE`, `NUTZT_MATERIAL`, etc.

Do this after Phase 1, with a backup. It is large but mostly mechanical.

### Phase 3 — Provenance model consolidation

Not a blind delete:

- Node provenance candidates: 315 label/property pairs, 168,440 occurrences.
- Relationship source/evidence candidates: 877 reltype/property pairs, 375,583 occurrences.

Problem:

- Provenance fields are spread across semantic nodes, source nodes, and relationship bags.
- `source_scope`, `evidence_*`, `source_status_*`, `source_trace_*`, URL status, and source URL fields are not consistently modeled.

Minimum target:

- Keep actual source identity on `Quelle` / source nodes.
- Keep fact support as `BELEGT_IN` or normalized relationship provenance.
- Remove source/probe/cache status from semantic nodes.
- Avoid duplicate source URLs both as node properties and relationship properties.

This phase needs a migration plan, not just a property-removal patch.

### Phase 4 — Topology-duplicate fields

Review before removal:

- Node relationship-duplicate candidates: 39 label/property pairs, 43,734 occurrences.
- Relationship duplicate-id candidates: 3 reltype/property pairs, 12,235 occurrences.

Confirmed probes:

- `Bauteilgruppe.primary_material_id`: 356 nodes have the prop; 321 have some `NUTZT_MATERIAL`; only 236 exactly match, mostly because `mat_mehrere` / `mat_unbekannt` summarize multiple material relationships.
- `Bauteilgruppe.primary_bauteiltyp_id`: 356 nodes have the prop; all 356 have `HAT_BAUTEILTYP`; only 166 exactly match, mostly because `bt_mehrere` summarizes multiple component-type relationships.
- `Bauteilgruppe.reuse_status`: 356 nodes have the prop; all 356 have `HAT_STATUS`; 354 have `HAT_WIEDERVERWENDUNGSART`.
- `Akteur.land`: 81 actors have the prop; 220 actors have `LIEGT_IN_LAND`.
- `Akteur` typing/roles are mostly relational: 663 have `HAT_AKTEURTYP`; 664 have `HAT_AKTEURROLLE`; 7 actors miss type or role coverage.

Recommendation:

- Do not remove `primary_*` until the summary/multiple-choice semantics are replaced or accepted as unnecessary.
- `reuse_status` is much closer to redundant and is a strong cleanup candidate after a per-value mapping check.
- `Akteur.land` should be migrated into `LIEGT_IN_LAND` where missing, then removed.

### Phase 5 — Review/meta graph compaction

The graph is dominated by review/meta objects:

- `DataIssue`: 28,729 nodes, average 14.55 properties.
- `DossierEntityTarget`: 2,591 nodes, average 12.24 properties.
- `ReuseRule`: 20 nodes, average 36 properties.
- `DeprecatedType`: 13 nodes, average 11 properties.

`DataIssue` connectivity:

- 48,385 `CONCERNS` relationships.
- 910 `HAS_DATA_ISSUE` relationships.
- 101 isolated `DataIssue` nodes.

Minimum-property cleanup alone will not solve this. Decide whether these review objects stay graph-native, move to `_neo4j/review/`, or compact into fewer audit nodes.

### Phase 6 — Domain property review

After the mechanical cleanup, review:

- Node domain properties: 154 label/property pairs, 44,349 occurrences.
- Relationship domain properties: 119 reltype/property pairs, 109,222 occurrences.

Examples to decide, not auto-delete:

- `Projekt.co2_facts`, `Projekt.cost_facts`, `Projekt.reuse_share_facts`.
- `Bauteilgruppe.tragend`, `menge_m2`, `menge_t`, `direct_reuse_relevant`.
- `CITED_FROM_DOSSIER` semantic fields like `entity_type`, `entity_value`, `section`, `locator`.

These determine whether the graph is a semantic graph or a mixed semantic/audit ledger.

## Type drift to fix early

- `Akteur.source_scope`: string/list drift.
- `Norm.source_scope`: string/list drift.
- `Bauteilgruppe.tragend`: boolean/string drift.
- `Bauteilgruppe.direct_reuse_relevant`: boolean/string drift.
- `Bauteilgruppe.menge_m2`, `Bauteilgruppe.menge_t`: int/float drift.
- Relationship `id` drift on `BELEGT_IN`, `HAT_AKTEURROLLE`, `HAT_AKTEURTYP`, `HAT_STATUS`.
- `HAT_AKTEURROLLE.scope` drift; this should likely be removed in Phase 1.

## Immediate next action

Generate Phase 1 patch only:

1. Back up `mit-bestand`.
2. Generate JSONL patch for P0 drops from `patch_ready_drop_candidates.csv`.
3. Dry-run with `_scripts/apply_neo4j_review_patch.py`.
4. Inspect dry-run op counts and sample before live apply.
5. Rerun `_scripts/_gap_survey.py` and this audit.

Do not start with the 396k P1 property cleanup until Phase 1 proves the workflow.
