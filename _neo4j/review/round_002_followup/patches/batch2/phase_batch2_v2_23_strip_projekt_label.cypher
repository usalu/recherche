// Phase 23 — Strip :Projekt label from 6 dual-label :Programm:Projekt nodes.
//
// Per user decision (B1): "if they are not a project remove project otherwise
// its okay to connect to both. projects are related to a mission of building
// with Reuse whether planning,research,or engineering,etc.. what not a project
// is Baubörse,software or organisazion."
//
// All 6 dual-labels are programmes (Interreg, MAS, RFCS, Reallabor, teaching+
// research) — not buildings/missions. Strip :Projekt label.
//
// PRECONDITION: Phase 18 done (node_role normalized).

MATCH (n:Programm:Projekt) WHERE n.id IN [
  'prog_fcrbe',
  'prog_mas_dfab',
  'prog_re_use_hoefe',
  'prog_reallabor_be_ware',
  'prog_rebridge',
  'prog_stuttgart_210'
]
REMOVE n:Projekt
RETURN n.id AS id, labels(n) AS remaining_labels;

// === Verification ===
//
// MATCH (n:Programm:Projekt) RETURN n.id;
// EXPECTED: 0 rows (all dual-labels resolved to :Programm only).
//
// MATCH (n:Programm) WHERE n.id IN [...above ids] RETURN count(n);
// EXPECTED: 6.
//
// MATCH (n:Projekt) RETURN count(n) AS projekt_count;
// EXPECTED: 91 (was 97; -6 from label strip).
