# Conflict analysis — 2026-05-31 Project Reuse-Focus Cleanup

Pre-flight check before applying the patch bundle. Every finding is grounded
in a live-graph query (see `_inspect_status.py` audit trail + `evidence.jsonl`
+ `resolution.jsonl`) or apply-tool code review.

**Verdict:** the cleanup is sound. **One pre-Phase-C amendment required** (R1
script rewrites). Other risks (R2/R3) collapsed to non-issues after schema +
source-record inspection.

---

## A. No conflicts — safe to proceed

### A1. Existing batch2 v2 promotions are partial — not blocking
`prog_stuttgart_210`, `prog_re_use_hoefe`, `prog_rebridge`,
`prog_reallabor_be_ware`, `prog_fcrbe` ALL exist as `:Programm` canonicals.
Their `p_*` `:Projekt` twins also exist. Phase B's merges complete the work
that the prior pass started. Apply tool's `merge_node` unions properties and
labels safely; no add_node needed.

### A2. Op names validated against `apply_neo4j_review_patch.SUPPORTED_OPS`
The build script imports `SUPPORTED_OPS` from
[_scripts/apply_neo4j_review_patch.py:47-53](../../../_scripts/apply_neo4j_review_patch.py)
and rejects any emitted op outside the set. Validation passed:
`projects.phaseA.patch.jsonl` (3 ops) + `projects.phaseB.patch.jsonl` (7 ops)
use only `delete_node`, `set_property`, `merge_node`.

### A3. Merge op key contract verified
`projects.phaseB.patch.jsonl` uses `"from"` and `"to"` keys (not `src_id`/`dst_id`),
matching `_neo4j/review/round_002_followup/patches/batch2/phase_batch2_v2_1d2b_programm_merges.patch.jsonl`.

### A4. Schema enum already permits target labels
[_neo4j/contracts/project_batches_v1_1/schemas/kg_jsonl_record_schema.json](../../contracts/project_batches_v1_1/schemas/kg_jsonl_record_schema.json)
lines 66-73 already list `Programm`, `Software`, `Tool`, `Marktmodell` in the
labels enum. No schema diff needed (R2 collapsed).

### A5. No source-record clobber risk for merge / delete candidates
Glob check confirms ZERO `_neo4j/processed/projects/records/p_*.kg.jsonl` source
records exist for any merge or delete candidate. Future re-imports cannot
restore the deleted/merged-away nodes (R3 collapsed).

### A6. Granby Workshop — graph evidence overridden by explicit user instruction
Graph evidence shows `reclaimed_proof = true` (NUTZT_BAUWERK=1,
HAT_BAUTEILGRUPPE=4, HAT_METHODE=1). User explicitly instructed removal on
2026-05-31. Decision row marks `delete_cascade` with cascade aux ops AND a
surface list (5 Akteure + 1 Bauwerk + 1 Stadt are NOT auto-deleted — they're
real-world entities). User must separately decide on the surface entities,
particularly `bw_granby_workshop_liverpool` (the donor building).

### A7. REFAIR and RCMI/Concular are `absent_from_graph` at `:Projekt` level
Resolver found `software_refair` (:Software), `refair_bordeaux` (:Akteur),
`tool_rcmi` (:Software+:Tool), `software_concular` (:Software), `concular`
(:Akteur) — but NO `:Projekt`. User-intended reclassifications are already in
place. No action required.

---

## B. Open decisions surfaced for user review

See [MANUAL_REVIEW_CHECKPOINT.md](MANUAL_REVIEW_CHECKPOINT.md) for the full list.
Summary:

- B1. Eggshell Pavilion + Up Sticks Dundee: marginal reclaimed evidence (only
  HAT_BAUTEILGRUPPE / HAT_METHODE, no donor/receiver/wva/nutzt). User decides
  delete vs keep.
- B2. Careno Be.Circular: relabel to `:Material`, relabel to `:Tool`, or keep
  as `:Projekt`. No `:Produkt` label exists.
- B3. ETH Circular Construction (student): merge into `prog_mas_dfab` MAS DFAB
  course or keep standalone? User decides.
- B4. MedUni Campus Mariannengasse: create new `:Bauwerk` or `:Projekt` stub
  for the donor building? Or accept absence?

---

## C. Required amendment before Phase C

### C1. R1 — Hard-coded `:Projekt` query rewrites
Phase C strips `:Projekt` from 5 canonicals (prog_fcrbe, prog_re_use_hoefe,
prog_rebridge, prog_reallabor_be_ware, prog_stuttgart_210). After Phase C:

- `MATCH (p:Projekt) RETURN count(p)` in dashboards / gap-audits drops by 5
  and reads wrong unless the queries also count `:Programm`.
- 4 dashboard queries in `_scripts/run_neo4j_current_build_review.py`
- 8 gap-audit queries in `_scripts/_gap_survey.py`
- 3 page-gen queries in `_scripts/generate_page_links.py`,
  `generate_project_links.py`, `generate_review_lists.py`
- 1 image-pipeline query in `_scripts/harvest_project_images.py`

See [dependency_fixes/hard_coded_projekt_query_audit.csv](dependency_fixes/hard_coded_projekt_query_audit.csv)
for per-row recommended action. `scratch/` and `batch2_v2_generators/` and the
`run_neo4j_round002_baseline.py` baseline are annotate-only.

**Gate:** do not apply Phase C until C1 is closed (or explicitly deferred with
a timestamped follow-up note).

---

## D. Apply order (verified — updated 2026-05-31)

1. **Pre-apply snapshot** of:
   - 90 ids in `projects.phaseA.delete_targets.txt` (Circle House + OBK 27 + Careno + Eggshell + Granby + each project's exclusive aux nodes: Bauteilgruppe / DataIssue / Kennwert / project-scoped Dossier).
   - 8 ids in `projects.phaseB.merge_targets.txt` (the merged-away stubs).
2. **Phase A**: 91 ops (90 delete_node cascade + 1 set_property rename for LYSP8). Independent of Phase B.
3. **Phase B**: 8 merge_node ops (added B4 ETH Circular Construction student → prog_mas_dfab).
4. Resolve C1 (R1 query rewrites).
5. **Phase C**: REMOVE :Projekt on 6 canonicals (was 5; added prog_mas_dfab).
6. Apply R4, R5 advisories.
7. Append ledger entry to a new `rollback.md` in this directory.

---

## E. Rollback hooks

- **Phase A** (90 deletes) requires pre-apply snapshot of every id in
  `projects.phaseA.delete_targets.txt`. Without it, the deletes are
  unrecoverable. This file now generated alongside the patches.
- **Phase B** merges are reversible from the snapshot: the apply tool emits
  an apply_report.json with before/after counts; restoring the pre-merge ids
  requires `add_node` + relationship-redirect Cypher, using the snapshot as
  the source of truth.
- **Phase C** label strip is trivially reversible: `MATCH (n:Programm) WHERE
  n.id IN [...] SET n:Projekt`.

## F. Surface entities (NOT auto-cascaded — separate user decision)

Per the cascade rule, only project-scoped bookkeeping nodes
(Bauteilgruppe / DataIssue / Kennwert / project-scoped Dossier) are deleted
with the project. Real-world entities are surfaced for review:

| Project | Surface entity | Label | Edge | Suggestion |
|---|---|---|---|---|
| Circle House | `kasper_guldager_jensen` | Akteur | STUB_PROJECT_LINK | Keep — real person, may appear in other contexts |
| OBK 27 | `cyril_pressacco`, `thibaut_barrault` | Akteur | STUB_PROJECT_LINK | Keep — real people |
| Careno | `tool_retile` | Software+Tool | NUTZT_SOFTWARE | Surface — Re-Tile is the Careno-specific tool. Delete only if removing Careno fully. |
| Careno | `brussels_capital_region`, `bbri` | Akteur | ERHALT_FOERDERUNG_DURCH, BETEILIGT_AN | Keep — real organisations |
| Careno | `meth_wiederverwendungskriterien` | Methode | HAT_METHODE | Keep — methodology vocab |
| Eggshell | `stadt_weil_am_rhein` | Stadt | LIEGT_IN_STADT | Keep — real city |
| Granby | `bw_granby_workshop_liverpool` | Bauwerk | NUTZT_BAUWERK | **Decide:** donor building. Delete if removing Granby donor side too. |
| Granby | `stadt_liverpool` | Stadt | LIEGT_IN_STADT | Keep — real city |
| Granby | `assemble`, `granby_4_streets_clt`, `granby_workshop_cic`, `will_shannon`, `lewis_jones` | Akteur | BETEILIGT_AN / STUB_PROJECT_LINK | Keep — real people/organisations |
