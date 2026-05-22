// =====================================================================
// Phase 0.4 — Relabel mis-labeled :Projekt nodes
//
// 3 nodes carry the :Projekt label but use a `prog_*` id (Programme convention).
// They should be :Programm. Fix the label before any vocab-edge migration
// runs in Phase 6, so their old-vocab edges follow the :Programm migration
// path (not the :Projekt one — :Projekt edges get DELETED, :Programm ones
// get REROUTED).
//
// review_run = 'taxonomy_integration_2026_06_03'
// Safe / reversible: only changes labels on 3 nodes.
// =====================================================================

// ---------- Pre-check: see what we'll change ----------
MATCH (p:Projekt)
WHERE p.id STARTS WITH 'prog_'
RETURN p.id, p.name, labels(p) AS labels_before;
// expected: 3 rows
//   prog_re_use_hoefe
//   prog_reallabor_be_ware
//   prog_stuttgart_210
// (verify these against the live graph before applying)


// ---------- Apply: add :Programm label, drop :Projekt ----------
MATCH (p:Projekt)
WHERE p.id STARTS WITH 'prog_'
SET p:Programm
REMOVE p:Projekt
SET p.review_run = coalesce(p.review_run, 'taxonomy_integration_2026_06_03'),
    p.relabel_note = 'P0.4 2026-06-03: corrected mislabeling — prog_* id implies :Programm not :Projekt';


// ---------- Post-check ----------

// 1. zero :Projekt nodes still have prog_ ids
MATCH (p:Projekt) WHERE p.id STARTS WITH 'prog_'
RETURN 'FAIL' AS status, p.id, p.name;
// expected: 0 rows

// 2. The 3 nodes now carry :Programm
MATCH (p:Programm) WHERE p.id STARTS WITH 'prog_'
RETURN 'OK' AS status, p.id, p.name, labels(p) AS labels_now;
// expected: 3 rows, each with labels including 'Programm'


// ---------- Rollback (run only if you need to revert) ----------
// MATCH (p:Programm)
// WHERE p.id STARTS WITH 'prog_'
//   AND p.relabel_note STARTS WITH 'P0.4 2026-06-03'
// SET p:Projekt
// REMOVE p:Programm
// REMOVE p.relabel_note;
