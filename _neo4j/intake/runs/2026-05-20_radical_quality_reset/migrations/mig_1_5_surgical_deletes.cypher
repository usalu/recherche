// =========================================================================
// Migration 1.5 — Surgical deletes (max 33 nodes; abort gate at >35).
//   6 :Akteur (deg <= 1)
//   4 :Programm (deg 0)
//   2 :Norm (deg 0)
//  21 :Quelle (deg 0, dossier stubs)
//
// All nodes are journalled to ../deleted/phase1_5_nodes.jsonl by the
// Python runner BEFORE these DETACH DELETEs execute.
// Reversibility: replay the JSONL file (one node per line) via the
// snapshot's `nodes.jsonl` schema.
// =========================================================================

// --- 1.5.a Akteur (6)
MATCH (a:Akteur)
WHERE a.id IN [
  'glasfischer_glastec',
  'citydev_brussels',
  'denkstatt',
  'eitel_partner',
  'gibbins_architekten',
  'zusammenkunft_berlin'
]
DETACH DELETE a;

// --- 1.5.b Programm (4)
MATCH (p:Programm)
WHERE p.id IN [
  'prog_bbsm',
  'prog_preuse',
  'prog_zukunftbau',
  'prog_kommunales_programm'
]
DETACH DELETE p;

// --- 1.5.c Norm (2)
MATCH (n:Norm)
WHERE n.id IN [
  'norm_bs_5385_5_2009',
  'norm_din_18940'
]
DETACH DELETE n;

// --- 1.5.d Quelle deg-0 dossier stubs (21)
//   (Skipped silently if Agent 3 already deleted them under Phase 1.2.)
MATCH (q:Quelle)
WHERE q.id IN [
  'qu_arch_reuse_bxl_dossier',
  'qu_careno_retile_s2',
  'qu_careno_rotor_s1',
  'qu_circl_abnamro_opening_s3',
  'qu_circl_abnamro_report_s4',
  'qu_circl_dutcharchitects_s1',
  'qu_circl_icon_digital_twin_s7',
  'qu_circl_zuidas_dismantling_s6',
  'qu_fcrbe_interreg_s1',
  'qu_granby_assemble_s2',
  'qu_granby_rock_terrazzo_s3',
  'qu_lysp8_oxara_s4',
  'qu_lysp8_swissarc_s2',
  'qu_lysp8_zirkular_s1',
  'qu_meduni_baukarussell_s2',
  'qu_rcmi_concular_dossier',
  'qu_rebridge_unistuttgart_r1',
  'qu_stuttgart210_baunetzwissen_s7',
  'qu_stuttgart210_holzbauoffensive_s5',
  'qu_vandkunsten_dossier',
  'qu_zhaw_reuse_dossier'
]
  AND NOT (q)--()
DETACH DELETE q;
