// ==========================================================================
// mig_r10_deprecated_type_seed
// Record old-name to new-name mapping for retired labels/rel types.
// Run AFTER R2 is complete.
// ==========================================================================

UNWIND [
  {kind:'label',    old:'GraphVersion',                   new:'(none — dropped)',
   reason:'Experimental versioning label — never populated.'},
  {kind:'label',    old:'ZertifizierungBewertungssystem', new:'Zertifizierungssystem',
   reason:'Renamed in R2.d for brevity — old name preserved as alias on new nodes.'},
  {kind:'label',    old:'LebenszyklusModul',              new:'LCAModule',
   reason:'Renamed in R2.b — original IDs (lz_*) preserved on new nodes.'},
  {kind:'rel_type', old:'AUS_BAUWERK',                    new:'FROM_DONOR',
   reason:'Phase 4.2 rename.'},
  {kind:'rel_type', old:'EINGEBAUT_IN',                   new:'INTO_RECEIVER',
   reason:'Phase 4.2 rename.'},
  {kind:'rel_type', old:'HAT_SCHADSTOFF',                 new:'HAS_RISK_POLLUTANT',
   reason:'Phase 3.2 split into HAS_RISK_POLLUTANT + REQUIRES_VERIFICATION_FOR.'},
  {kind:'rel_type', old:'NUTZT_TOOL',                     new:'NUTZT_SOFTWARE',
   reason:'Phase 2.5.e Tool relabel.'},
  {kind:'rel_type', old:'ASSOZIIERT_MIT_PROJEKT',         new:'STUB_PROJECT_LINK',
   reason:'Renamed in R9 for honest stub semantics.'},
  {kind:'rel_type', old:'TEILT_LAYER',                    new:'(restored in R2.a)',
   reason:'Restored from brand_layer property by mig_r2_a_restore_layer.'},
  {kind:'rel_type', old:'BERECHNET_NACH_MODUL',           new:'(restored in R2.b)',
   reason:'Restored from Phase 2.5 deletion journal by mig_r2_b_restore_lca_module.'},
  {kind:'rel_type', old:'HAT_RECHTLICHE_BEDINGUNG',       new:'(restored in R2.c)',
   reason:'Restored from Phase 2.5 deletion journal by mig_r2_c_restore_legal.'},
  {kind:'rel_type', old:'GILT_IN_LAND',                   new:'(restored in R2.c via journal edges)',
   reason:'Restored from Phase 2.5 deletion journal by mig_r2_c_restore_legal.'},
  {kind:'rel_type', old:'HAT_ZERTIFIZIERUNG',             new:'(restored in R2.d)',
   reason:'Restored from Phase 2.5 deletion journal by mig_r2_d_restore_certifications.'}
] AS row
MERGE (d:DeprecatedType {id: 'dep_' + row.kind + '__' + replace(row.old, '_', '__')})
ON CREATE SET
  d.kind = row.kind,
  d.old_name = row.old,
  d.new_name = row.new,
  d.deprecated_at = date(),
  d.deprecated_by = 'mig_r10_deprecated_type_seed',
  d.reason = row.reason,
  d.evidence_origin = 'source_curated',
  d.evidence_basis = 'audit_record',
  d.evidence_confidence = 'belegt',
  d.migration_origin = 'mig_r10_deprecated_type_seed';

// Audits
MATCH (d:DeprecatedType) RETURN 'deprecated_type_count' AS check, count(d) AS c;
MATCH (d:DeprecatedType) RETURN d.kind AS kind, count(d) AS c ORDER BY kind;
