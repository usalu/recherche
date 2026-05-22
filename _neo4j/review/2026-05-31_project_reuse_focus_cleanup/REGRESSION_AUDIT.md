# Regression Audit — 2026-05-31 Project Reuse-Focus Cleanup

Status of each regression risk identified in the planning pass. Refer to the
plan file for full risk descriptions.

## R1 — Hard-coded `MATCH (p:Projekt)` queries (40+ in `_scripts/`)
**Status:** `fix_drafted`
**Fix artefact:** [dependency_fixes/hard_coded_projekt_query_audit.csv](dependency_fixes/hard_coded_projekt_query_audit.csv)
**Gate:** Phase C is BLOCKED until rewrites for `dashboard`, `gap-audit`, and
`page-gen` categories land. Scratch / batch2_v2_generators / baseline-frozen
rows are annotate-only. Counts in the audit: 8 gap-audit, 4 dashboard, 3 page-gen,
1 image-pipeline, 3 baseline-frozen, 1 historical-generator, 17+ scratch.

**2026-05-31 update:** Phase C now strips `:Projekt` from 6 canonicals (added
`prog_mas_dfab` from the B4 merge). The R1 impact is unchanged in shape, but
the count of canonicals losing `:Projekt` is now 6.

## R2 — JSONL contract schema enum allows only `"Projekt"`
**Status:** `not_applicable`
**Evidence:** [_neo4j/contracts/project_batches_v1_1/schemas/kg_jsonl_record_schema.json](../../contracts/project_batches_v1_1/schemas/kg_jsonl_record_schema.json) lines 24-78
already include `Programm` (line 66), `Software` (67), `Tool` (68), `Marktmodell`
(73). Original audit assumed `["Projekt"]` exclusivity; actual file contains the
full reuse-entity enum. No fix needed.

## R3 — Source JSONL records will clobber relabeled nodes on re-import
**Status:** `not_applicable`
**Evidence:** glob check shows ZERO source records under
`_neo4j/processed/projects/records/` for any merge candidate
(`p_stuttgart_210`, `p_re_use_hoefe`, `p_rebridge_structural_reuse_project`,
`p_reallabor_be_ware`, `p_reallabor_b_e_ware`, `p_interreg_nwe_fcrbe`,
`p_pavilion_circl_amsterdam`) or delete candidate (`p_obk_27`, `p_circle_house`).
These nodes were created out-of-band (batch2 v2 import or interactive Cypher),
not from a `kg.jsonl` source record. No clobber risk on re-import.

**Caveat:** the kept node `p_big_dig_building_boston` DOES have a source record
at [_neo4j/processed/projects/records/p_big_dig_building_boston.kg.jsonl](../../processed/projects/records/p_big_dig_building_boston.kg.jsonl).
That node is being kept as-is, so no clobber there either.

## R4 — Topology export snapshot scoped to `:Projekt` only
**Status:** `fix_drafted`
**Fix artefact:** [dependency_fixes/topology_export_staleness_note.md](dependency_fixes/topology_export_staleness_note.md)
**Action after apply:** append the staleness note to
`_neo4j/review/2026-05-31_project_direct_topology_export_mit-bestand/README.md`
and regenerate.

## R5 — `_neo4j/REVIEW_BASED_PLAN.md` and `FINAL_REVIEW_PLAN_AUDIT.md`
**Status:** `fix_drafted`
**Fix artefact:** [dependency_fixes/docs_audit_note.md](dependency_fixes/docs_audit_note.md)
**Action after apply:** apply the advisory banners + per-gate guidance.

---

## Gate criteria for applying Phase C

Phase C (`projects.phaseC_strip_projekt.cypher`) strips `:Projekt` from 5
canonical `:Programm` nodes that received merge contributions. Once stripped,
queries that say `MATCH (p:Projekt)` will no longer find those nodes. Therefore:

- [ ] R1 dashboard rows rewritten (4 queries in `run_neo4j_current_build_review.py`)
- [ ] R1 gap-audit rows decided (8 queries in `_gap_survey.py` — either rewrite or accept they only audit :Projekt)
- [ ] R1 page/image-gen scope decided (5 queries across `generate_*` and `harvest_*`)
- [ ] R4 topology export staleness note appended
- [ ] R5 doc banners applied (or explicitly deferred with timestamped note)

R2 and R3 are not applicable — no gates.

## Apply-order summary (updated 2026-05-31 after cascade + B4 user instruction)

1. **Backup**: [_scripts/_snapshot_predelete.py](../../../_scripts/_snapshot_predelete.py) over both:
   - `projects.phaseA.delete_targets.txt` (90 ids — projects + cascade aux)
   - `projects.phaseB.merge_targets.txt` (8 ids — about-to-be-merged stubs)
2. **Phase A**: 91 ops (90 delete_node cascade + 1 set_property rename for LYSP8). Independent of Phase B.
3. **Phase B**: 8 merge_node ops (was 7, added B4 ETH Circular Construction student → prog_mas_dfab).
4. **Resolve R1**: dashboard + gap + page-gen query rewrites per `dependency_fixes/hard_coded_projekt_query_audit.csv`.
5. **Phase C**: REMOVE :Projekt on 6 canonicals (was 5, added prog_mas_dfab from B4 merge).
6. Apply R4, R5 advisories.

Total mutations: 91 (Phase A) + 8 (Phase B) + 6 (Phase C) = 105 mutations.
