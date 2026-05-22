// ============================================================
// CORRECTION: Restore country scope semantics and add explicit
//             supranational scope modeling after land fanout
// Date: 2026-05-31
//
// Goals:
// 1. Correct EN / Eurocode country applicability where officially supported.
// 2. Introduce a separate :Geltungsbereich model for non-country scope.
// 3. Remove unproven CEN/TS country fanout.
// 4. Split mixed CE/UKCA legal node into separate CE and UKCA nodes.
// ============================================================

// Step 1: Add explicit scope nodes for non-country applicability
MERGE (gb:Geltungsbereich {id: 'geltungsbereich_en_cen_cenelec_mitglieder'})
ON CREATE SET
  gb.name = 'EN in CEN/CENELEC Mitgliedslaendern',
  gb.scope_type = 'standard_adoption',
  gb.scope_system = 'CEN/CENELEC',
  gb.scope_note = 'EN wird von den nationalen CEN/CENELEC-Mitgliedern als nationaler Standard umgesetzt.',
  gb.evidence_origin = 'source_curated',
  gb.evidence_basis = 'official_web_audit',
  gb.evidence_confidence = 'belegt',
  gb.evidence_source_id = 'scope_audit_2026_05_31',
  gb.migration_origin = 'mig_scope_correction_2026_05_31',
  gb.source_scope = 'scope_audit_2026_05_31';

MERGE (gb:Geltungsbereich {id: 'geltungsbereich_eurocodes_eu_efta_uk'})
ON CREATE SET
  gb.name = 'Eurocodes in EU/EFTA plus Vereinigtes Koenigreich',
  gb.scope_type = 'standard_adoption',
  gb.scope_system = 'Eurocodes',
  gb.scope_note = 'Eurocodes adopted in the 31 EU/EFTA Member States and the United Kingdom.',
  gb.evidence_origin = 'source_curated',
  gb.evidence_basis = 'official_web_audit',
  gb.evidence_confidence = 'belegt',
  gb.evidence_source_id = 'scope_audit_2026_05_31',
  gb.migration_origin = 'mig_scope_correction_2026_05_31',
  gb.source_scope = 'scope_audit_2026_05_31';

MERGE (gb:Geltungsbereich {id: 'geltungsbereich_cen_ts_europaeisch'})
ON CREATE SET
  gb.name = 'CEN Technical Specification europaeischer Deliverable-Raum',
  gb.scope_type = 'standardization_deliverable',
  gb.scope_system = 'CEN/CENELEC',
  gb.scope_note = 'European CEN/CENELEC technical specification deliverable, no country-level fanout asserted in this correction batch.',
  gb.evidence_origin = 'source_curated',
  gb.evidence_basis = 'official_web_audit',
  gb.evidence_confidence = 'teilweise_belegt',
  gb.evidence_source_id = 'scope_audit_2026_05_31',
  gb.migration_origin = 'mig_scope_correction_2026_05_31',
  gb.source_scope = 'scope_audit_2026_05_31';

MERGE (gb:Geltungsbereich {id: 'geltungsbereich_cpr_eea'})
ON CREATE SET
  gb.name = 'CPR / CE mit EEA-Relevanz',
  gb.scope_type = 'legal_market_scope',
  gb.scope_system = 'CPR',
  gb.scope_note = 'Construction Products Regulation / CE marking legal market context with EEA relevance.',
  gb.evidence_origin = 'source_curated',
  gb.evidence_basis = 'official_web_audit',
  gb.evidence_confidence = 'belegt',
  gb.evidence_source_id = 'scope_audit_2026_05_31',
  gb.migration_origin = 'mig_scope_correction_2026_05_31',
  gb.source_scope = 'scope_audit_2026_05_31';

MERGE (gb:Geltungsbereich {id: 'geltungsbereich_ukca_grossbritannien'})
ON CREATE SET
  gb.name = 'UKCA in Grossbritannien',
  gb.scope_type = 'legal_market_scope',
  gb.scope_system = 'UKCA',
  gb.scope_note = 'Great Britain market context for UKCA and continued CE recognition under UK rules.',
  gb.evidence_origin = 'source_curated',
  gb.evidence_basis = 'official_web_audit',
  gb.evidence_confidence = 'belegt',
  gb.evidence_source_id = 'scope_audit_2026_05_31',
  gb.migration_origin = 'mig_scope_correction_2026_05_31',
  gb.source_scope = 'scope_audit_2026_05_31';

MERGE (gb:Geltungsbereich {id: 'geltungsbereich_eu_regulierung'})
ON CREATE SET
  gb.name = 'EU-Regulierung',
  gb.scope_type = 'legal_regulation_scope',
  gb.scope_system = 'EU',
  gb.scope_note = 'EU regulation scope for Union-level legal regimes such as the EU Taxonomy.',
  gb.evidence_origin = 'source_curated',
  gb.evidence_basis = 'official_web_audit',
  gb.evidence_confidence = 'belegt',
  gb.evidence_source_id = 'scope_audit_2026_05_31',
  gb.migration_origin = 'mig_scope_correction_2026_05_31',
  gb.source_scope = 'scope_audit_2026_05_31';

// Step 2: Attach EN nodes to explicit supranational scope and correct misleading node properties
MATCH (n:Norm)
WHERE n.id IN ['norm_en_1090','norm_en_1168','norm_en_13162','norm_en_14081','norm_en_206','norm_en_771']
MATCH (gb:Geltungsbereich {id: 'geltungsbereich_en_cen_cenelec_mitglieder'})
MERGE (n)-[r:HAT_GELTUNGSBEREICH]->(gb)
ON CREATE SET
  r.id = n.id + '__HAT_GELTUNGSBEREICH__' + gb.id,
  r.evidence_origin = 'source_curated',
  r.evidence_basis = 'official_web_audit',
  r.evidence_confidence = 'belegt',
  r.evidence_source_id = 'scope_audit_2026_05_31',
  r.migration_origin = 'mig_scope_correction_2026_05_31',
  r.review_status = 'reviewed',
  r.source_scope = 'scope_audit_2026_05_31'
SET n.scope_note = 'EN national standard adoption across CEN/CENELEC members, country links reflect available member countries in this graph.',
    n.country_short = 'CEN';

// Step 3: Add missing country links for EN nodes based on CEN/CENELEC member implementation
MATCH (n:Norm)-[sample:GILT_IN_LAND]->(:Land)
WHERE n.id IN ['norm_en_1090','norm_en_1168','norm_en_13162','norm_en_14081','norm_en_206','norm_en_771']
WITH n, head(collect(sample)) AS sample
MATCH (target:Land)
WHERE target.id IN ['land_norwegen','land_schweiz','land_vereinigtes_koenigreich']
MERGE (n)-[nr:GILT_IN_LAND]->(target)
ON CREATE SET
  nr += properties(sample),
  nr.id = coalesce(n.id, elementId(n)) + '__GILT_IN_LAND__' + target.id,
  nr.evidence_origin = 'source_curated',
  nr.evidence_basis = 'official_web_audit',
  nr.evidence_confidence = 'belegt',
  nr.evidence_source_id = 'scope_audit_2026_05_31',
  nr.derivation_note = coalesce(sample.derivation_note, '') + ' | added from EN 34-country adoption audit 2026-05-31',
  nr.migration_origin = 'mig_scope_correction_2026_05_31',
  nr.review_status = 'reviewed',
  nr.source_resolution_status = 'reviewed';

// Step 4: Attach Eurocode nodes to explicit supranational scope and correct misleading node properties
MATCH (n:Norm)
WHERE n.id IN ['norm_en_1992','norm_en_1993','norm_en_1995','norm_en_1996']
MATCH (gb:Geltungsbereich {id: 'geltungsbereich_eurocodes_eu_efta_uk'})
MERGE (n)-[r:HAT_GELTUNGSBEREICH]->(gb)
ON CREATE SET
  r.id = n.id + '__HAT_GELTUNGSBEREICH__' + gb.id,
  r.evidence_origin = 'source_curated',
  r.evidence_basis = 'official_web_audit',
  r.evidence_confidence = 'belegt',
  r.evidence_source_id = 'scope_audit_2026_05_31',
  r.migration_origin = 'mig_scope_correction_2026_05_31',
  r.review_status = 'reviewed',
  r.source_scope = 'scope_audit_2026_05_31'
SET n.scope_note = 'Eurocode adoption across EU/EFTA states and the United Kingdom, country links reflect available countries in this graph.',
    n.country_short = 'EU/EFTA+UK';

// Step 5: Add missing country links for Eurocodes based on JRC Eurocodes statement
MATCH (n:Norm)-[sample:GILT_IN_LAND]->(:Land)
WHERE n.id IN ['norm_en_1992','norm_en_1993','norm_en_1995','norm_en_1996']
WITH n, head(collect(sample)) AS sample
MATCH (target:Land)
WHERE target.id IN ['land_norwegen','land_schweiz','land_vereinigtes_koenigreich']
MERGE (n)-[nr:GILT_IN_LAND]->(target)
ON CREATE SET
  nr += properties(sample),
  nr.id = coalesce(n.id, elementId(n)) + '__GILT_IN_LAND__' + target.id,
  nr.evidence_origin = 'source_curated',
  nr.evidence_basis = 'official_web_audit',
  nr.evidence_confidence = 'belegt',
  nr.evidence_source_id = 'scope_audit_2026_05_31',
  nr.derivation_note = coalesce(sample.derivation_note, '') + ' | added from Eurocodes EU/EFTA+UK audit 2026-05-31',
  nr.migration_origin = 'mig_scope_correction_2026_05_31',
  nr.review_status = 'reviewed',
  nr.source_resolution_status = 'reviewed';

// Step 6: Move CEN/TS nodes from unproven country links to explicit supranational scope only
MATCH (n:Norm)
WHERE n.id IN ['norm_cen_ts_17440','norm_cen_ts_1090_201_2024']
MATCH (gb:Geltungsbereich {id: 'geltungsbereich_cen_ts_europaeisch'})
MERGE (n)-[r:HAT_GELTUNGSBEREICH]->(gb)
ON CREATE SET
  r.id = n.id + '__HAT_GELTUNGSBEREICH__' + gb.id,
  r.evidence_origin = 'source_curated',
  r.evidence_basis = 'official_web_audit',
  r.evidence_confidence = 'teilweise_belegt',
  r.evidence_source_id = 'scope_audit_2026_05_31',
  r.migration_origin = 'mig_scope_correction_2026_05_31',
  r.review_status = 'reviewed',
  r.source_scope = 'scope_audit_2026_05_31'
SET n.scope_note = 'European CEN technical specification, country-level fanout removed pending dedicated source confirmation.'
REMOVE n.country_short;

MATCH (n:Norm)-[r:GILT_IN_LAND]->(:Land)
WHERE n.id IN ['norm_cen_ts_17440','norm_cen_ts_1090_201_2024']
DELETE r;

// Step 7: Split mixed CE/UKCA legal condition into separate CE and UKCA nodes
MERGE (ce:RechtlicheBedingung {id: 'rb_ce_marking_reused_steel'})
ON CREATE SET
  ce.name = 'CE marking for reused steel',
  ce.scope_note = 'CPR / CE legal market context for reused steel with EEA relevance.',
  ce.evidence_basis = 'controlled_vocab',
  ce.evidence_confidence = 'belegt',
  ce.evidence_origin = 'source_curated',
  ce.is_universal = false,
  ce.review_status = 'needs_source_url_review',
  ce.source_resolution_status = 'needs_source_url_review',
  ce.strict_source_url_cleanup = 'mig_strict_source_url_binding_cleanup_2026_05_23',
  ce.strict_source_url_cleanup_at = '2026-05-23T11:01:59.122927+00:00',
  ce.migration_origin = 'mig_r2_c_restore_legal | mig_qext_b_source_urls | mig_qext_c_primary_source_url | mig_scope_correction_2026_05_31',
  ce.source_scope = 'scope_audit_2026_05_31'
MERGE (ukca:RechtlicheBedingung {id: 'rb_ukca_marking_reused_steel'})
ON CREATE SET
  ukca.name = 'UKCA marking for reused steel',
  ukca.scope_note = 'Great Britain legal market context for reused steel under UKCA / continued CE recognition.',
  ukca.evidence_basis = 'controlled_vocab',
  ukca.evidence_confidence = 'belegt',
  ukca.evidence_origin = 'source_curated',
  ukca.is_universal = false,
  ukca.review_status = 'needs_source_url_review',
  ukca.source_resolution_status = 'needs_source_url_review',
  ukca.strict_source_url_cleanup = 'mig_strict_source_url_binding_cleanup_2026_05_23',
  ukca.strict_source_url_cleanup_at = '2026-05-23T11:01:59.122927+00:00',
  ukca.migration_origin = 'mig_r2_c_restore_legal | mig_qext_b_source_urls | mig_qext_c_primary_source_url | mig_scope_correction_2026_05_31',
  ukca.source_scope = 'scope_audit_2026_05_31';

// Step 8: Recreate incoming project / component references for both new legal nodes
MATCH (src)
WHERE src.id IN [
  'p_brent_cross_town_primary_substation_london',
  'bg_reuse_stahl_mehrere_brent_cross_bracing_members',
  'bg_reuse_stahl_mehrere_brent_cross_tubular_columns'
]
MATCH (replacement:RechtlicheBedingung)
WHERE replacement.id IN ['rb_ce_marking_reused_steel','rb_ukca_marking_reused_steel']
MERGE (src)-[nr:HAT_RECHTLICHE_BEDINGUNG]->(replacement)
ON CREATE SET
  nr.id = coalesce(src.id, elementId(src)) + '__HAT_RECHTLICHE_BEDINGUNG__' + replacement.id,
  nr.evidence_basis = 'cell_citation',
  nr.evidence_confidence = 'teilweise_belegt',
  nr.evidence_origin = 'source_curated',
  nr.evidence_source_id = 'scope_split_rewire_2026_05_31',
  nr.derivation_note = 'Recreated after splitting rb_ce_ukca_marking_reused_steel on 2026-05-31.',
  nr.migration_origin = 'mig_scope_correction_2026_05_31',
  nr.review_status = 'needs_source_url_review',
  nr.source_resolution_status = 'needs_source_url_review',
  nr.source_status = 'missing',
  nr.source_status_migration = 'mig_source_status_normalization_2026_05_28',
  nr.source_status_normalized_at = '2026-05-28T10:57:15.458609+00:00',
  nr.source_status_reason = 'no_exact_url_binding_needs_review',
  nr.source_trace_migrated_at = '2026-05-23T10:47:30.445168+00:00',
  nr.source_trace_migration = 'mig_trace_zitiert_quelle_to_urls_2026_05_23';

// Step 9: Recreate source evidence links for both new legal nodes
MATCH (q)
WHERE q.id IN ['q_bauteilreuse_legal_regime_matrix_md','q_brent_cross_town_primary_substation_london_md']
MATCH (replacement:RechtlicheBedingung)
WHERE replacement.id IN ['rb_ce_marking_reused_steel','rb_ukca_marking_reused_steel']
MERGE (replacement)-[nr:BELEGT_IN]->(q)
ON CREATE SET
  nr.id = replacement.id + '__BELEGT_IN__' + q.id,
  nr.evidence_basis = CASE q.id
    WHEN 'q_bauteilreuse_legal_regime_matrix_md' THEN 'controlled_vocab'
    ELSE 'cell_citation'
  END,
  nr.evidence_confidence = 'unklar',
  nr.evidence_origin = CASE q.id
    WHEN 'q_bauteilreuse_legal_regime_matrix_md' THEN 'topology_synthesized'
    ELSE 'source_curated'
  END,
  nr.evidence_source_id = CASE q.id
    WHEN 'q_bauteilreuse_legal_regime_matrix_md' THEN 'scope_split_copy_2026_05_31_topology'
    ELSE 'scope_split_copy_2026_05_31_curated'
  END,
  nr.derivation_note = 'Recreated after splitting rb_ce_ukca_marking_reused_steel on 2026-05-31.',
  nr.migration_origin = 'mig_scope_correction_2026_05_31',
  nr.review_status = 'needs_source_url_review',
  nr.source_resolution_status = 'needs_source_url_review',
  nr.source_status = 'missing',
  nr.source_status_migration = 'mig_source_status_normalization_2026_05_28',
  nr.source_status_normalized_at = '2026-05-28T10:57:15.458609+00:00',
  nr.source_status_reason = 'no_exact_url_binding_needs_review',
  nr.source_trace_migrated_at = '2026-05-23T10:47:30.445168+00:00',
  nr.source_trace_migration = 'mig_trace_zitiert_quelle_to_urls_2026_05_23';

// Step 10: Attach new legal nodes to explicit non-country scope nodes
MATCH (ce:RechtlicheBedingung {id: 'rb_ce_marking_reused_steel'})
MATCH (gb:Geltungsbereich {id: 'geltungsbereich_cpr_eea'})
MERGE (ce)-[r:HAT_GELTUNGSBEREICH]->(gb)
ON CREATE SET
  r.id = ce.id + '__HAT_GELTUNGSBEREICH__' + gb.id,
  r.evidence_origin = 'source_curated',
  r.evidence_basis = 'official_web_audit',
  r.evidence_confidence = 'belegt',
  r.evidence_source_id = 'scope_audit_2026_05_31',
  r.migration_origin = 'mig_scope_correction_2026_05_31',
  r.review_status = 'reviewed',
  r.source_scope = 'scope_audit_2026_05_31';

MATCH (ukca:RechtlicheBedingung {id: 'rb_ukca_marking_reused_steel'})
MATCH (gb:Geltungsbereich {id: 'geltungsbereich_ukca_grossbritannien'})
MERGE (ukca)-[r:HAT_GELTUNGSBEREICH]->(gb)
ON CREATE SET
  r.id = ukca.id + '__HAT_GELTUNGSBEREICH__' + gb.id,
  r.evidence_origin = 'source_curated',
  r.evidence_basis = 'official_web_audit',
  r.evidence_confidence = 'belegt',
  r.evidence_source_id = 'scope_audit_2026_05_31',
  r.migration_origin = 'mig_scope_correction_2026_05_31',
  r.review_status = 'reviewed',
  r.source_scope = 'scope_audit_2026_05_31';

// Step 11: Add concrete country links for the new legal nodes
MATCH (ce:RechtlicheBedingung {id: 'rb_ce_marking_reused_steel'})
MATCH (target:Land)
WHERE target.id IN [
  'land_belgien','land_daenemark','land_deutschland','land_finnland','land_frankreich',
  'land_italien','land_luxemburg','land_niederlande','land_oesterreich','land_portugal','land_norwegen'
]
MERGE (ce)-[r:GILT_IN_LAND]->(target)
ON CREATE SET
  r.id = ce.id + '__GILT_IN_LAND__' + target.id,
  r.evidence_origin = 'source_curated',
  r.evidence_basis = 'official_web_audit',
  r.evidence_confidence = 'belegt',
  r.evidence_source_id = 'scope_audit_2026_05_31',
  r.derivation_note = 'Created during CE/UKCA scope split 2026-05-31.',
  r.migration_origin = 'mig_scope_correction_2026_05_31',
  r.review_status = 'reviewed',
  r.source_resolution_status = 'reviewed';

MATCH (ukca:RechtlicheBedingung {id: 'rb_ukca_marking_reused_steel'})
MATCH (uk:Land {id: 'land_vereinigtes_koenigreich'})
MERGE (ukca)-[r:GILT_IN_LAND]->(uk)
ON CREATE SET
  r.id = ukca.id + '__GILT_IN_LAND__' + uk.id,
  r.evidence_origin = 'source_curated',
  r.evidence_basis = 'official_web_audit',
  r.evidence_confidence = 'belegt',
  r.evidence_source_id = 'scope_audit_2026_05_31',
  r.derivation_note = 'Created during CE/UKCA scope split 2026-05-31.',
  r.migration_origin = 'mig_scope_correction_2026_05_31',
  r.review_status = 'reviewed',
  r.source_resolution_status = 'reviewed';

// Step 12: Add explicit scope modeling for EU Taxonomy and keep EU-only country links intact
MATCH (rb:RechtlicheBedingung {id: 'rb_eu_taxonomie'})
MATCH (gb:Geltungsbereich {id: 'geltungsbereich_eu_regulierung'})
MERGE (rb)-[r:HAT_GELTUNGSBEREICH]->(gb)
ON CREATE SET
  r.id = rb.id + '__HAT_GELTUNGSBEREICH__' + gb.id,
  r.evidence_origin = 'source_curated',
  r.evidence_basis = 'official_web_audit',
  r.evidence_confidence = 'belegt',
  r.evidence_source_id = 'scope_audit_2026_05_31',
  r.migration_origin = 'mig_scope_correction_2026_05_31',
  r.review_status = 'reviewed',
  r.source_scope = 'scope_audit_2026_05_31';

// Step 13: Remove the deprecated mixed node after rewiring
MATCH (old:RechtlicheBedingung {id: 'rb_ce_ukca_marking_reused_steel'})
DETACH DELETE old;

// Step 14: Sanity checks
MATCH (n)
WHERE n.id IN [
  'norm_en_1090','norm_en_1168','norm_en_13162','norm_en_14081',
  'norm_en_1992','norm_en_1993','norm_en_1995','norm_en_1996',
  'norm_cen_ts_17440','norm_cen_ts_1090_201_2024',
  'rb_ce_marking_reused_steel','rb_ukca_marking_reused_steel','rb_eu_taxonomie'
]
OPTIONAL MATCH (n)-[:GILT_IN_LAND]->(land:Land)
OPTIONAL MATCH (n)-[:HAT_GELTUNGSBEREICH]->(gb:Geltungsbereich)
RETURN n.id AS id,
       labels(n) AS labels,
       collect(DISTINCT land.id) AS land_ids,
       collect(DISTINCT gb.id) AS geltungsbereich_ids
ORDER BY id;