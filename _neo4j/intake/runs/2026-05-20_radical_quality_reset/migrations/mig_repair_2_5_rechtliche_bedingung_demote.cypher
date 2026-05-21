// Repair Phase 2.5 — demote remaining :RechtlicheBedingung nodes.
// Context: Final verifier 5 found 15 live nodes after the Phase 2.5 gate.
//
// The remaining nodes are source/country-level metadata imported from
// q_bauteilreuse_legal_regime_matrix_md and have no project/domain
// HAT_RECHTLICHE_BEDINGUNG edges. Preserve their values and BELEGT_IN
// provenance on connected nodes as properties, then delete the label nodes.
// No new node labels are created.

WITH [
  'rb_bauordnungsrecht',
  'rb_bauproduktenverordnung_cpr',
  'rb_boulder_deconstruction_ordinance_8366',
  'rb_ce_ukca_marking_reused_steel',
  'rb_denkmalschutz',
  'rb_dibt_zustimmung',
  'rb_eu_taxonomie',
  'rb_gewaehrleistung',
  'rb_grade_ii_listing',
  'rb_kreislaufwirtschaftsgesetz_krwg',
  'rb_materialpass',
  'rb_produkthaftung',
  'rb_schweizer_bauproduktegesetz',
  'rb_vergaberecht',
  'rb_zulassung_im_einzelfall'
] AS target_ids
MATCH (rb:RechtlicheBedingung)
WHERE rb.id IN target_ids
OPTIONAL MATCH (rb)-[belegt:BELEGT_IN]->(q:Quelle)
WITH q,
     collect(DISTINCT rb.id) AS ids,
     collect(DISTINCT coalesce(rb.name, rb.id)) AS names,
     collect(DISTINCT belegt.evidence_source_id) AS evidence_source_ids,
     collect(DISTINCT belegt.evidence_basis) AS evidence_basis,
     collect(DISTINCT belegt.evidence_origin) AS evidence_origin,
     collect(DISTINCT belegt.evidence_confidence) AS evidence_confidence,
     collect(DISTINCT belegt.id) AS source_edge_ids,
     collect(DISTINCT
       '{' +
       '"id":"' + rb.id + '",' +
       '"name":"' + coalesce(rb.name, rb.id) + '",' +
       '"source_scope":"' + coalesce(rb.source_scope, '') + '",' +
       '"created_by":"' + coalesce(rb.created_by, '') + '",' +
       '"last_seen_by":"' + coalesce(rb.last_seen_by, '') + '",' +
       '"belegt_in":"' + coalesce(q.id, '') + '",' +
       '"source_edge_id":"' + coalesce(belegt.id, '') + '",' +
       '"evidence_source_id":"' + coalesce(belegt.evidence_source_id, '') + '",' +
       '"evidence_basis":"' + coalesce(belegt.evidence_basis, '') + '",' +
       '"evidence_origin":"' + coalesce(belegt.evidence_origin, '') + '",' +
       '"evidence_confidence":"' + coalesce(belegt.evidence_confidence, '') + '"' +
       '}'
     ) AS demotion_records
WHERE q IS NOT NULL
SET q.legal_conditions = apoc.coll.toSet(coalesce(q.legal_conditions, []) + names),
    q.legal_condition_ids = apoc.coll.toSet(coalesce(q.legal_condition_ids, []) + ids),
    q.demoted_legal_condition_ids = apoc.coll.toSet(coalesce(q.demoted_legal_condition_ids, []) + ids),
    q.demoted_legal_condition_records = apoc.coll.toSet(coalesce(q.demoted_legal_condition_records, []) + demotion_records),
    q.legal_condition_evidence_source_ids = apoc.coll.toSet(coalesce(q.legal_condition_evidence_source_ids, []) + [x IN evidence_source_ids WHERE x IS NOT NULL]),
    q.legal_condition_evidence_basis = apoc.coll.toSet(coalesce(q.legal_condition_evidence_basis, []) + [x IN evidence_basis WHERE x IS NOT NULL]),
    q.legal_condition_evidence_origin = apoc.coll.toSet(coalesce(q.legal_condition_evidence_origin, []) + [x IN evidence_origin WHERE x IS NOT NULL]),
    q.legal_condition_evidence_confidence = apoc.coll.toSet(coalesce(q.legal_condition_evidence_confidence, []) + [x IN evidence_confidence WHERE x IS NOT NULL]),
    q.legal_condition_source_edge_ids = apoc.coll.toSet(coalesce(q.legal_condition_source_edge_ids, []) + [x IN source_edge_ids WHERE x IS NOT NULL]),
    q.legal_condition_demoted_by = 'mig_repair_2_5_rechtliche_bedingung_demote',
    q.legal_condition_demoted_at = datetime('2026-05-21T09:13:00+02:00')
RETURN q.id AS source_id, size(ids) AS conditions_preserved;

// Generic safety transfer for any remaining domain relationship of this type.
// In the inspected graph this returns 0, but it keeps the migration faithful to
// the property-first demotion plan if the graph changed between inspection and run.
WITH [
  'rb_bauordnungsrecht',
  'rb_bauproduktenverordnung_cpr',
  'rb_boulder_deconstruction_ordinance_8366',
  'rb_ce_ukca_marking_reused_steel',
  'rb_denkmalschutz',
  'rb_dibt_zustimmung',
  'rb_eu_taxonomie',
  'rb_gewaehrleistung',
  'rb_grade_ii_listing',
  'rb_kreislaufwirtschaftsgesetz_krwg',
  'rb_materialpass',
  'rb_produkthaftung',
  'rb_schweizer_bauproduktegesetz',
  'rb_vergaberecht',
  'rb_zulassung_im_einzelfall'
] AS target_ids
MATCH (src)-[r:HAT_RECHTLICHE_BEDINGUNG]->(rb:RechtlicheBedingung)
WHERE rb.id IN target_ids
WITH src,
     collect(DISTINCT rb.id) AS ids,
     collect(DISTINCT coalesce(rb.name, rb.id)) AS names,
     collect(DISTINCT r.id) AS edge_ids
SET src.legal_conditions = apoc.coll.toSet(coalesce(src.legal_conditions, []) + names),
    src.legal_condition_ids = apoc.coll.toSet(coalesce(src.legal_condition_ids, []) + ids),
    src.legal_condition_source_edge_ids = apoc.coll.toSet(coalesce(src.legal_condition_source_edge_ids, []) + [x IN edge_ids WHERE x IS NOT NULL]),
    src.legal_condition_demoted_by = 'mig_repair_2_5_rechtliche_bedingung_demote'
RETURN count(src) AS domain_nodes_updated;

WITH [
  'rb_bauordnungsrecht',
  'rb_bauproduktenverordnung_cpr',
  'rb_boulder_deconstruction_ordinance_8366',
  'rb_ce_ukca_marking_reused_steel',
  'rb_denkmalschutz',
  'rb_dibt_zustimmung',
  'rb_eu_taxonomie',
  'rb_gewaehrleistung',
  'rb_grade_ii_listing',
  'rb_kreislaufwirtschaftsgesetz_krwg',
  'rb_materialpass',
  'rb_produkthaftung',
  'rb_schweizer_bauproduktegesetz',
  'rb_vergaberecht',
  'rb_zulassung_im_einzelfall'
] AS target_ids
MATCH (rb:RechtlicheBedingung)
WHERE rb.id IN target_ids
WITH collect(rb) AS nodes, count(rb) AS c
UNWIND nodes AS rb
DETACH DELETE rb
RETURN c AS rechtliche_bedingung_nodes_deleted;
