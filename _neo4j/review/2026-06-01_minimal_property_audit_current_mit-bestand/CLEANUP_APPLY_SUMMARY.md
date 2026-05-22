# Minimal-property cleanup — apply summary (2026-06-01, mit-bestand)

All phases preceded by a full logical backup + dry-run. Backups (gitignored):
`_neo4j/review/backups/2026-06-01_pre_keep_list_cleanup` and `..._pre_dataissue_delete`.

## Result so far (Phases A-C applied)
- Distinct node-property keys: **209 -> 106**.
- Node-property occurrences: **449,083 -> 378,502**.
- Per-label property counts now match the approved matrix
  (e.g. Akteur 2, Quelle 4 core, Bauteilgruppe 7, Kennwert 9 (justified), Norm 5).

## Phase A — drop bookkeeping / cache / provenance (applied)
- Patch: `phaseA_drop/keep_list_drop.patch.jsonl` (7,810 nodes, 69,390 removals).
- 3,196 guarded keeps: identity/semantic props protected on multi-label nodes.
- Dropped: all `url_*` probe/cache, `source_url*`, `evidence_*`, `strict_*`,
  `source_scope`, `review_status`, generated/derived metadata, machine flags.

## Phase B — migrate Kennwert/Norm provenance, then drop (applied)
- Created `BELEGT_IN`: Kennwert 0->214, Norm 3->72.
- Dropped: Kennwert `source_id`/`source_urls`/`primary_source_url`;
  Norm `evidence_source_id`/`evidence_origin`/`evidence_confidence`/`evidence_basis`.

## Phase C — topology duplicates with edge migration, then drop (applied)
- Created edges: `NUTZT_MATERIAL` +30, `LIEGT_IN_LAND` Akteur +78, Bauwerk/Materialdepot +3.
- Dropped: Bauteilgruppe `primary_material_id` + `primary_bauteiltyp_id`;
  Akteur/Bauwerk/Materialdepot `land`.
- 5 `mat_unbekannt`-type BGs and 1 Akteur had no target node (value unrepresentable; dropped).

## Phase D — delete DataIssue (applied)
- Deleted 28,729 `DataIssue` nodes + their `CONCERNS`/`HAS_DATA_ISSUE` audit edges.
- Graph: **39,226 -> 10,497 nodes**, **80,830 -> 31,599 relationships**. 0 DataIssue remain.
- An external process was concurrently adding a few relationships during this run;
  node/DataIssue counts were stable so the batched DETACH DELETE was safe.

## Final state
- Node label/property pairs: **767 -> 277**. Distinct keys **209 -> 106**.
- type-drift pairs 21 -> 7. Post-cleanup audit:
  `_neo4j/review/2026-06-01_minimal_property_audit_post_cleanup_mit-bestand`.
- Remaining meta labels (left per Option A): DossierEntityTarget 2591, ReuseRule 20,
  DeprecatedType 13 — available for a separate decision if you want them compacted too.
- Gap survey: zero semantic-relationship regressions (BELEGT_IN/HAT_MATERIALGRUPPE/
  HAT_WIEDERVERWENDUNGSART unchanged from pre-cleanup); `r.id NULL` improved
  10,408 -> 5,303; only the approved `source_scope` invariant now fails.

## Phase E — remove the dossier citation staging layer (applied)
- Decision: the only source of truth is the direct `BELEGT_IN` links.
- Verified safe first: `CITED_FROM_DOSSIER` reached only 70 `Quelle`, and all 70
  already had a direct `BELEGT_IN` (0 would lose provenance).
- Deleted the whole `DossierEntityTarget` layer: 2,591 nodes + 6,409 edges
  (`CITED_FROM_DOSSIER` 6,104 + `EXACT_MATCH_CANDIDATE` 305).
- `ZITIERT_QUELLE` was already absent (0).
- Graph: 10,496 -> **7,905 nodes**, 31,603 -> **25,194 relationships**.
- `ReuseRule` (20) + `DeprecatedType` (13) intentionally kept — candidates to be
  remodelled into proper node types later, not deleted.
- Gap survey: no new regressions (same 4 pre-existing items).

## Known consequence to revisit
- Dropping `source_scope` everywhere (approved) trips the legacy `_gap_survey.py`
  mandatory check "Nodes missing source_scope". That invariant is now obsolete under
  the approved minimal schema and should be updated/removed in the gap survey.
- Other `_gap_survey` FAILs (`r.id NULL`, 4 nodes missing `BELEGT_IN`, BG rel gaps)
  are pre-existing and unrelated to this cleanup.
