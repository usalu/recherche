// Phase C — Strip :Projekt label from canonical :Programm nodes that received
// merge contributions from :Projekt stubs in Phase B. Mirrors the prior
// phase_batch2_v2_23_strip_projekt_label.cypher pattern.
//
// User rule (verbatim from phase_batch2_v2_23):
//   "if they are not a project remove project otherwise its okay to connect to
//    both. projects are related to a mission of building with Reuse whether
//    planning, research, or engineering, etc. what not a project is Baubörse,
//    software or organisazion."
//
// PRECONDITION: Phase A + Phase B applied AND R1 (hard-coded :Projekt queries
// in _scripts/) resolved per dependency_fixes/hard_coded_projekt_query_audit.csv.
// do_not_apply_until=R1_resolved

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
// MATCH (n:Programm:Projekt) WHERE n.id IN [...above ids] RETURN n.id;
// EXPECTED: 0 rows.
