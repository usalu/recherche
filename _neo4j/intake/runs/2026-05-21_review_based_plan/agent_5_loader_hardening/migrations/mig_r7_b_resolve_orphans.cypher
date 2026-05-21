// ==========================================================================
// mig_r7_b_resolve_orphans
// 1. Create the one truly-missing Programm node (ETH Circular Construction
//    Programme — different from the student reuse Projekt).
// 2. Create BELEGT_IN edges from existing Projekt/Programm nodes to the
//    case_markdown Quellen that have no such link.
//    The full BELEGT_IN batch is driven from agent_5_runner.py ($link_rows).
// ==========================================================================

// R7.b.1 — Create missing Programm node
MERGE (p:Programm {id: 'p_eth_circular_construction_programme'})
ON CREATE SET
  p.name = 'ETH Circular Construction Programme',
  p.source_scope = 'r7_b_orphan_resolution',
  p.migration_origin = 'mig_r7_b_resolve_orphans',
  p.needs_dossier_extraction = true,
  p.evidence_origin = 'source_curated',
  p.evidence_basis = 'dossier_anchored',
  p.evidence_confidence = 'belegt';

// R7.b.2 — Link new Programm to its dossier Quelle
MATCH (p:Programm {id: 'p_eth_circular_construction_programme'})
MATCH (q:Quelle {id: 'q_eth_circular_construction_programme_md'})
MERGE (p)-[r:BELEGT_IN]->(q)
ON CREATE SET
  r.evidence_origin = 'source_curated',
  r.evidence_basis = 'cell_citation',
  r.evidence_source_id = 'q_eth_circular_construction_programme_md',
  r.evidence_confidence = 'belegt',
  r.migration_origin = 'mig_r7_b_resolve_orphans';

// R7.b.3 — Parameterized: bulk BELEGT_IN edges for all other orphan Quellen
// Runner calls with $link_rows = [{entity_id, quelle_id}]
// UNWIND $link_rows AS row
// MATCH (e {id: row.entity_id})
// MATCH (q:Quelle {id: row.quelle_id, quelltyp: 'case_markdown'})
// MERGE (e)-[r:BELEGT_IN]->(q)
// ON CREATE SET
//   r.evidence_origin = 'topology_synthesized',
//   r.evidence_basis = 'slug_match',
//   r.evidence_confidence = 'teilweise_belegt',
//   r.migration_origin = 'mig_r7_b_resolve_orphans'

// Audits
MATCH (p:Programm {id: 'p_eth_circular_construction_programme'})
RETURN 'eth_prog_created' AS check, p.id AS id, p.name AS name;

MATCH (q:Quelle {quelltyp:'case_markdown'})
WHERE NOT exists{MATCH (n)-[:BELEGT_IN]->(q) WHERE n:Projekt OR n:Programm}
RETURN 'case_markdown_still_orphan' AS check, count(q) AS violations;
