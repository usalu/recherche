// ==========================================================================
// mig_r2_d_restore_certifications
// Restore :Zertifizierungssystem nodes using original journal IDs (zbs_*).
// HAT_ZERTIFIZIERUNG and BELEGT_IN edges are restored via Python-
// parameterized calls in the runner script.
// ==========================================================================

// R2.d.1 — Create :Zertifizierungssystem nodes (original journal IDs)
UNWIND [
  {id:'zbs_breeam',             name:'BREEAM',                         scheme_kind:'multi_criteria'},
  {id:'zbs_leed',               name:'LEED',                           scheme_kind:'multi_criteria'},
  {id:'zbs_dgnb',               name:'DGNB',                           scheme_kind:'multi_criteria'},
  {id:'zbs_well',               name:'WELL',                           scheme_kind:'health_wellness'},
  {id:'zbs_nabers',             name:'NABERS',                         scheme_kind:'operational_energy'},
  {id:'zbs_paris_proof',        name:'Paris_Proof',                    scheme_kind:'carbon_target'},
  {id:'zbs_nordic_swan_ecolabel', name:'Nordic Swan Ecolabel',         scheme_kind:'ecolabel'},
  {id:'zbs_ecotool',            name:'EcoTool (ZBS)',                   scheme_kind:'methodology_tool'}
] AS row
MERGE (z:Zertifizierungssystem {id: row.id})
ON CREATE SET z.name = row.name,
              z.scheme_kind = row.scheme_kind,
              z.aliases = ['ZertifizierungBewertungssystem'],
              z.evidence_origin = 'source_curated',
              z.evidence_basis = 'controlled_vocab',
              z.evidence_source_id = 'r2_d_cert_restore',
              z.evidence_confidence = 'belegt',
              z.source_scope = 'r2_d_cert_restore',
              z.migration_origin = 'mig_r2_d_restore_certifications';

// R2.d.2 — ANCHORED_BY bookkeeping
MATCH (z:Zertifizierungssystem) WHERE z.migration_origin = 'mig_r2_d_restore_certifications'
MATCH (q:Quelle {id: 'q_controlled_vocab_seed'})
MERGE (z)-[r:ANCHORED_BY]->(q)
ON CREATE SET r.evidence_origin = 'topology_synthesized',
              r.evidence_basis = 'controlled_vocab',
              r.evidence_confidence = 'unklar',
              r.is_bookkeeping = true,
              r.migration_origin = 'mig_r2_d_restore_certifications';

// Audits
MATCH (z:Zertifizierungssystem) RETURN 'cert_count' AS check, count(z) AS c;
MATCH ()-[r:HAT_ZERTIFIZIERUNG]->() RETURN 'hat_zert_count' AS check, count(r) AS c;
