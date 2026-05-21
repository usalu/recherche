// ==========================================================================
// mig_r2_b_restore_lca_module
// Restore :LCAModule nodes using original journal IDs (lz_*).
// Edges (BERECHNET_NACH_MODUL, METHODENGRUNDLAGE_NORM, ANCHORED_BY)
// are restored via Python-parameterized calls in the runner script.
// ==========================================================================

// R2.b.1 — Create :LCAModule nodes (original IDs from deleted journal)
UNWIND [
  {id:'lz_a1_a3', code:'A1_A3', name:'A1-A3 Produkt',
   scope_note:'Module A1-A3 per EN 15978: raw-material extraction, transport, manufacturing'},
  {id:'lz_a4_a5', code:'A4_A5', name:'A4-A5 Errichtung',
   scope_note:'Module A4-A5 per EN 15978: transport to site, construction-installation stage'},
  {id:'lz_b',     code:'B',     name:'B1-B7 Nutzung',
   scope_note:'Module B1-B7 per EN 15978: use stage incl. maintenance, repair, operational energy'},
  {id:'lz_c',     code:'C1_C4', name:'C1-C4 End-of-Life',
   scope_note:'Module C1-C4 per EN 15978: deconstruction, transport, waste processing, disposal'},
  {id:'lz_d',     code:'D',     name:'D Beyond (Reuse)',
   scope_note:'Module D per EN 15978: benefits beyond system boundary - reuse credit'}
] AS row
MERGE (lcm:LCAModule {id: row.id})
ON CREATE SET lcm.name = row.name,
              lcm.en15978_code = row.code,
              lcm.scope_note = row.scope_note,
              lcm.evidence_origin = 'source_curated',
              lcm.evidence_basis = 'controlled_vocab',
              lcm.evidence_source_id = 'q_en_15978_lifecycle_modules',
              lcm.evidence_confidence = 'belegt',
              lcm.source_scope = 'r2_b_lca_restore',
              lcm.migration_origin = 'mig_r2_b_restore_lca_module';

// Audits
MATCH (lcm:LCAModule) RETURN 'lca_module_count' AS check, count(lcm) AS c;
