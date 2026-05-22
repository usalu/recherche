# Topology export staleness — appended to README after cleanup

The snapshot at `_neo4j/review/2026-05-31_project_direct_topology_export_mit-bestand/`
captures `:Projekt`-anchored topology BEFORE the 2026-05-31 reuse-project
cleanup. After Phase B (merges) and Phase C (strip `:Projekt`) are applied,
the snapshot will be stale for these specific ids:

**Merged away (:Projekt → :Programm canonical, source id retired):**
- `p_stuttgart_210` → `prog_stuttgart_210`
- `p_re_use_hoefe` → `prog_re_use_hoefe`
- `p_rebridge_structural_reuse_project` → `prog_rebridge`
- `p_interreg_nwe_fcrbe` → `prog_fcrbe`
- `p_reallabor_be_ware` → `prog_reallabor_be_ware`
- `p_reallabor_b_e_ware` → `prog_reallabor_be_ware`

**Merged away (:Projekt → :Projekt duplicate canonical):**
- `p_pavilion_circl_amsterdam` → `p_circl_abn_amro`

**Deleted (non-reuse / non-reclaimed):**
- `p_obk_27`
- `p_circle_house`

(Eggshell Pavilion + Up Sticks Dundee remain open for review — see MANUAL_REVIEW_CHECKPOINT.md.)

**To regenerate**, use the same script that produced the original snapshot
(`_scripts/export_project_direct_topology.py` or equivalent — see the
README's `provenance` block). Run AFTER Phase C completes.

Until regenerated, treat the snapshot as a 2026-05-31 historical reference,
not as a current source of truth.
