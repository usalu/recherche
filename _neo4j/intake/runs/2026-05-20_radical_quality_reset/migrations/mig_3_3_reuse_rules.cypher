// =====================================================================
// mig_3_3 — Phase 3.3: Country × material decision shelf
//
// Creates exactly 20 :ReuseRule nodes from the 20 rows of
//   _knowledge/themes/circular_construction_reuse_graph_gaps.md
// and wires them with:
//   (:ReuseRule)-[:APPLIES_IN]->(:Land)
//   (:ReuseRule)-[:APPLIES_TO]->(:Material)
//   (:ReuseRule)-[:REFERENZIERT_NORM]->(:Norm)
//
// Country/material identification:
//   * :Land nodes in mit-bestand do not carry an ISO code today. This
//     migration sets l.country_iso on each Land that maps to one of the
//     seven rule countries (UK, BE, DE, NL, CH, FI, NO) so future joins
//     by ISO code work.
//   * Material name lookup uses :Material.name; for the two
//     "Beton / hollow-core slabs" rows (Finland, Norway) we anchor on
//     :Material{id:'mat_beton'} and store the full text in
//     ReuseRule.material.
//
// Norms wiring:
//   * Each rule lists 5–8 key_norms in plain text. We MERGE
//     (:Norm{id: 'norm_' + slug(name), name: original_name})
//     and create :REFERENZIERT_NORM only if a node with the slugged id
//     or exact name already exists; otherwise we MERGE-create the Norm
//     with evidence_origin='inferred', source_scope='reuse_rule_seed'.
//
// Every node and every edge created here carries:
//     evidence_origin='inferred'
//     evidence_basis='research_file_row'
//     evidence_source_id='q_circular_construction_reuse_graph_gaps_md'
//     evidence_confidence='belegt'
//
// The runtime payload ($rule_rows) is supplied by agent11_runner.py
// (see logs/agent11_runner.py for the canonical 20-row JSON spec).
// =====================================================================

// 3_3.pre — Ensure each ReuseRule's target :Land carries a country_iso
//           code for downstream joins. Other Land nodes are untouched.
UNWIND [
  {land_id: 'land_vereinigtes_koenigreich', iso: 'GB'},
  {land_id: 'land_belgien',                 iso: 'BE'},
  {land_id: 'land_deutschland',             iso: 'DE'},
  {land_id: 'land_niederlande',             iso: 'NL'},
  {land_id: 'land_schweiz',                 iso: 'CH'},
  {land_id: 'land_finnland',                iso: 'FI'},
  {land_id: 'land_norwegen',                iso: 'NO'}
] AS row
MATCH (l:Land {id: row.land_id})
SET l.country_iso = coalesce(l.country_iso, row.iso);

// 3_3.a — Create / refresh the 20 :ReuseRule nodes
UNWIND $rule_rows AS row
MERGE (rule:ReuseRule {id: row.id})
SET   rule.name                = row.name,
      rule.rank                = row.rank,
      rule.country_iso         = row.country_iso,
      rule.country_name        = row.country_name,
      rule.material            = row.material,
      rule.material_id         = row.material_id,
      rule.priority            = row.priority,
      rule.project_cluster     = row.project_cluster,
      rule.key_norms           = row.key_norms,
      rule.legal_conditions    = row.legal_conditions,
      rule.required_tests      = row.required_tests,
      rule.pollutant_risks     = row.pollutant_risks,
      rule.processing_methods  = row.processing_methods,
      rule.evidence_origin     = 'inferred',
      rule.evidence_basis      = 'research_file_row',
      rule.evidence_source_id  = 'q_circular_construction_reuse_graph_gaps_md',
      rule.evidence_confidence = 'belegt',
      rule.source_scope        = 'research_file_row',
      rule.source_url          = row.source_url,
      rule.suggested_graph_action = row.suggested_graph_action;

// 3_3.b.1 — APPLIES_IN edges to existing :Land nodes
UNWIND $rule_rows AS row
MATCH (rule:ReuseRule {id: row.id})
MATCH (l:Land {id: row.land_id})
MERGE (rule)-[ai:APPLIES_IN]->(l)
ON CREATE SET ai.id                  = 'r_' + rule.id + '__APPLIES_IN__' + l.id,
              ai.evidence_origin     = 'inferred',
              ai.evidence_basis      = 'research_file_row',
              ai.evidence_source_id  = 'q_circular_construction_reuse_graph_gaps_md',
              ai.evidence_confidence = 'belegt';

// 3_3.b.2 — APPLIES_TO edges to existing :Material nodes
UNWIND $rule_rows AS row
MATCH (rule:ReuseRule {id: row.id})
MATCH (m:Material {id: row.material_id})
MERGE (rule)-[at:APPLIES_TO]->(m)
ON CREATE SET at.id                  = 'r_' + rule.id + '__APPLIES_TO__' + m.id,
              at.evidence_origin     = 'inferred',
              at.evidence_basis      = 'research_file_row',
              at.evidence_source_id  = 'q_circular_construction_reuse_graph_gaps_md',
              at.evidence_confidence = 'belegt';

// 3_3.c — REFERENZIERT_NORM edges; MERGE missing :Norm anchors as inferred
UNWIND $norm_rows AS row
MERGE (n:Norm {id: row.norm_id})
ON CREATE SET n.name                = row.norm_name,
              n.evidence_origin     = 'inferred',
              n.evidence_basis      = 'reuse_rule_key_norm',
              n.evidence_source_id  = 'q_circular_construction_reuse_graph_gaps_md',
              n.evidence_confidence = 'belegt',
              n.source_scope        = 'reuse_rule_seed';

UNWIND $referenziert_norm_rows AS row
MATCH (rule:ReuseRule {id: row.rule_id})
MATCH (n:Norm {id: row.norm_id})
MERGE (rule)-[rn:REFERENZIERT_NORM]->(n)
ON CREATE SET rn.id                  = 'r_' + rule.id + '__REFERENZIERT_NORM__' + n.id,
              rn.evidence_origin     = 'inferred',
              rn.evidence_basis      = 'research_file_row',
              rn.evidence_source_id  = 'q_circular_construction_reuse_graph_gaps_md',
              rn.evidence_confidence = 'belegt';

// 3_3.d — Audits
MATCH (r:ReuseRule)
RETURN 'reuse_rule_total' AS check, count(r) AS c;

MATCH (:ReuseRule)-[r:APPLIES_IN]->(:Land)
RETURN 'applies_in_total' AS check, count(r) AS c;

MATCH (:ReuseRule)-[r:APPLIES_TO]->(:Material)
RETURN 'applies_to_total' AS check, count(r) AS c;

MATCH (:ReuseRule)-[r:REFERENZIERT_NORM]->(:Norm)
RETURN 'referenziert_norm_total' AS check, count(r) AS c;

MATCH (rule:ReuseRule)
OPTIONAL MATCH (rule)-[r]->()
RETURN 'reuse_rule_avg_degree' AS check,
       round(toFloat(count(r)) / toFloat(count(DISTINCT rule)), 2) AS deg;
