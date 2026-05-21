// ==========================================================================
// mig_r3_b_reuse_rule_relevant_for
// Wire :ReuseRule to :Projekt via country x material match.
// Idempotent: one edge per rule/project pair.
// ==========================================================================

MATCH (rule:ReuseRule)-[:APPLIES_IN]->(l:Land)<-[:LIEGT_IN_LAND]-(p:Projekt),
      (rule)-[:APPLIES_TO]->(m:Material)
WHERE exists{
  (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m)
}
MERGE (rule)-[r:RELEVANT_FOR]->(p)
ON CREATE SET r.evidence_origin = 'topology_synthesized',
              r.evidence_basis = 'country_material_match',
              r.evidence_confidence = 'teilweise_belegt',
              r.evidence_source_id = 'r3_b_topology',
              r.evidence_excerpt = NULL,
              r.derivation_note = 'Country x Material match. Country: ' + l.id +
                                  '. Material: ' + m.id + '. Rule: ' + rule.id + '.',
              r.migration_origin = 'mig_r3_b_reuse_rule_relevant_for';

// Audits
MATCH ()-[r:RELEVANT_FOR]->()
RETURN 'relevant_for_total' AS check, count(r) AS c;

MATCH (rule:ReuseRule)
OPTIONAL MATCH (rule)-[r:RELEVANT_FOR]->(:Projekt)
RETURN rule.id AS rule_id, count(r) AS projekt_count
ORDER BY projekt_count DESC, rule_id ASC;

MATCH (p:Projekt {id:'p_ferme_du_rail_paris'})
OPTIONAL MATCH (:ReuseRule)-[r:RELEVANT_FOR]->(p)
RETURN 'ferme_du_rail_rule_count' AS check, count(r) AS c, 0 AS expected_zero;

MATCH (p:Projekt {id:'p_holbein_gardens_london'})
OPTIONAL MATCH (:ReuseRule)-[r:RELEVANT_FOR]->(p)
RETURN 'holbein_rule_count' AS check, count(r) AS c;

MATCH ()-[r:RELEVANT_FOR]->()
WHERE r.evidence_origin <> 'topology_synthesized'
   OR r.evidence_basis IS NULL
   OR r.evidence_confidence IS NULL
   OR r.evidence_source_id IS NULL
   OR r.migration_origin IS NULL
RETURN 'relevant_for_missing_evidence' AS check, count(r) AS violations;
