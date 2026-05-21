// ==========================================================================
// mig_r3_a_has_bauwerk
// Derive direct :Projekt -> :Bauwerk edges from BG donor/receiver topology.
// Idempotent: one edge per project/building/role.
// ==========================================================================

// R3.a.1 - donor edges
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:FROM_DONOR]->(b:Bauwerk)
MERGE (p)-[h:HAS_BAUWERK {role: 'donor'}]->(b)
ON CREATE SET h.evidence_origin = 'topology_synthesized',
              h.evidence_basis = 'derived_from_bg_topology',
              h.evidence_confidence = 'teilweise_belegt',
              h.evidence_source_id = 'r3_a_topology',
              h.evidence_excerpt = NULL,
              h.derivation_note = 'Aggregated from (p)-[:HAT_BAUTEILGRUPPE]->(bg)-[:FROM_DONOR]->(b).',
              h.migration_origin = 'mig_r3_a_has_bauwerk';

// R3.a.2 - receiver edges
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:INTO_RECEIVER]->(b:Bauwerk)
MERGE (p)-[h:HAS_BAUWERK {role: 'receiver'}]->(b)
ON CREATE SET h.evidence_origin = 'topology_synthesized',
              h.evidence_basis = 'derived_from_bg_topology',
              h.evidence_confidence = 'teilweise_belegt',
              h.evidence_source_id = 'r3_a_topology',
              h.evidence_excerpt = NULL,
              h.derivation_note = 'Aggregated from (p)-[:HAT_BAUTEILGRUPPE]->(bg)-[:INTO_RECEIVER]->(b).',
              h.migration_origin = 'mig_r3_a_has_bauwerk';

// Audits
MATCH ()-[r:HAS_BAUWERK]->()
RETURN 'has_bauwerk_total' AS check, count(r) AS c;

MATCH ()-[r:HAS_BAUWERK {role:'donor'}]->()
RETURN 'has_bauwerk_donor' AS check, count(r) AS c;

MATCH ()-[r:HAS_BAUWERK {role:'receiver'}]->()
RETURN 'has_bauwerk_receiver' AS check, count(r) AS c;

MATCH (p:Projekt)
WHERE exists{ (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:FROM_DONOR|INTO_RECEIVER]->(:Bauwerk) }
  AND NOT exists{ (p)-[:HAS_BAUWERK]->() }
RETURN 'projekt_with_bg_paths_no_has_bauwerk' AS check, count(p) AS violations;

MATCH ()-[r:HAS_BAUWERK]->()
WHERE r.evidence_origin <> 'topology_synthesized'
   OR r.evidence_basis IS NULL
   OR r.evidence_confidence IS NULL
   OR r.evidence_source_id IS NULL
   OR r.migration_origin IS NULL
RETURN 'has_bauwerk_missing_evidence' AS check, count(r) AS violations;
