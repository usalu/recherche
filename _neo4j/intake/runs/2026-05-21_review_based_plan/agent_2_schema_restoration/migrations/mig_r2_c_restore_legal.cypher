// ==========================================================================
// mig_r2_c_restore_legal
// Restore :RechtlicheBedingung nodes from deleted journal.
// Additional stub nodes are created for RB IDs referenced in
// Quelle.legal_conditions but absent from the journal.
// Edges (HAT_RECHTLICHE_BEDINGUNG, GILT_IN_LAND, BELEGT_IN) are
// restored via Python-parameterized calls in the runner script.
// ==========================================================================

// R2.c.1 — Nodes from journal: passed as $rb_rows parameter from Python
// Pattern:
// UNWIND $rb_rows AS row
// MERGE (rb:RechtlicheBedingung {id: row.id})
// ON CREATE SET rb.name = row.name,
//               rb += row.props,
//               rb.evidence_origin = 'source_curated',
//               rb.evidence_basis = 'controlled_vocab',
//               rb.evidence_confidence = 'belegt',
//               rb.source_scope = 'r2_c_legal_restore',
//               rb.migration_origin = 'mig_r2_c_restore_legal'

// R2.c.2 — Stub nodes for RB IDs referenced in Quelle.legal_conditions
//           but not captured in the Phase 2.5 deletion journal
UNWIND [
  {id:'rb_bauproduktenverordnung_cpr',  name:'Bauproduktenverordnung (CPR)'},
  {id:'rb_denkmalschutz',              name:'Denkmalschutz'},
  {id:'rb_dibt_zustimmung',            name:'DIBt-Zustimmung im Einzelfall'},
  {id:'rb_kreislaufwirtschaftsgesetz_krwg', name:'Kreislaufwirtschaftsgesetz (KrWG)'},
  {id:'rb_materialpass',               name:'Materialpass-Pflicht'},
  {id:'rb_schweizer_bauproduktegesetz', name:'Schweizer Bauproduktegesetz (BauPG)'}
] AS row
MERGE (rb:RechtlicheBedingung {id: row.id})
ON CREATE SET rb.name = row.name,
              rb.evidence_origin = 'topology_synthesized',
              rb.evidence_basis = 'registry_stub',
              rb.evidence_confidence = 'unklar',
              rb.source_scope = 'r2_c_legal_restore_stub',
              rb.migration_origin = 'mig_r2_c_restore_legal',
              rb.stub_note = 'Referenced in q_bauteilreuse_legal_regime_matrix_md.legal_conditions but not in Phase 2.5 deletion journal. Stub created for linkability.';

// R2.c.3 — BELEGT_IN from all RB nodes to the legal-regime matrix Quelle
MATCH (rb:RechtlicheBedingung)
WHERE rb.migration_origin CONTAINS 'mig_r2_c_restore_legal'
MATCH (q:Quelle {id: 'q_bauteilreuse_legal_regime_matrix_md'})
MERGE (rb)-[r:BELEGT_IN]->(q)
ON CREATE SET r.evidence_origin = 'topology_synthesized',
              r.evidence_basis = 'controlled_vocab',
              r.evidence_confidence = 'unklar',
              r.migration_origin = 'mig_r2_c_restore_legal';

// R2.c.4 — ANCHORED_BY bookkeeping (if the controlled_vocab_seed Quelle exists)
MATCH (rb:RechtlicheBedingung)
WHERE rb.migration_origin CONTAINS 'mig_r2_c_restore_legal'
  AND rb.evidence_basis = 'controlled_vocab'
MATCH (q:Quelle {id: 'q_controlled_vocab_seed'})
MERGE (rb)-[r:ANCHORED_BY]->(q)
ON CREATE SET r.evidence_origin = 'topology_synthesized',
              r.evidence_basis = 'controlled_vocab',
              r.evidence_confidence = 'unklar',
              r.is_bookkeeping = true,
              r.migration_origin = 'mig_r2_c_restore_legal';

// Audits
MATCH (rb:RechtlicheBedingung) RETURN 'rb_count' AS check, count(rb) AS c;
MATCH ()-[r:HAT_RECHTLICHE_BEDINGUNG]->() RETURN 'hat_rb_count' AS check, count(r) AS c;
MATCH (:RechtlicheBedingung)-[r:GILT_IN_LAND]->(:Land) RETURN 'rb_gilt_in_land_count' AS check, count(r) AS c;
