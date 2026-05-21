// ==========================================================================
// mig_r2_a_restore_layer
// Restore :Layer nodes and :TEILT_LAYER edges.
// Layer nodes are the Brand 6-layer model: site, structure, skin,
// services, space_plan, stuff.
// Edges are rebuilt from Bauteiltyp.brand_layer property (15 nodes).
// ==========================================================================

// R2.a.1 — Create :Layer nodes
UNWIND [
  {id:'layer_site',       name:'Site',       brand_position: 1},
  {id:'layer_structure',  name:'Structure',  brand_position: 2},
  {id:'layer_skin',       name:'Skin',       brand_position: 3},
  {id:'layer_services',   name:'Services',   brand_position: 4},
  {id:'layer_space_plan', name:'Space Plan', brand_position: 5},
  {id:'layer_stuff',      name:'Stuff',      brand_position: 6}
] AS row
MERGE (l:Layer {id: row.id})
ON CREATE SET l.name = row.name,
              l.brand_position = row.brand_position,
              l.evidence_origin = 'source_curated',
              l.evidence_basis = 'controlled_vocab',
              l.evidence_source_id = 'q_brand_how_buildings_learn',
              l.evidence_confidence = 'belegt',
              l.source_scope = 'r2_a_layer_restore',
              l.migration_origin = 'mig_r2_a_restore_layer';

// R2.a.2 — Recreate TEILT_LAYER edges from Bauteiltyp.brand_layer property
MATCH (bt:Bauteiltyp) WHERE bt.brand_layer IS NOT NULL
MATCH (l:Layer {id: 'layer_' + bt.brand_layer})
MERGE (bt)-[r:TEILT_LAYER]->(l)
ON CREATE SET r.evidence_origin = 'topology_synthesized',
              r.evidence_basis = 'controlled_vocab',
              r.evidence_source_id = 'r2_a_layer_restore',
              r.evidence_confidence = 'belegt',
              r.migration_origin = 'mig_r2_a_restore_layer';

// R2.a.3 — Recreate ANCHORED_BY edge to controlled_vocab_seed
MATCH (l:Layer) WHERE l.migration_origin = 'mig_r2_a_restore_layer'
MATCH (q:Quelle {id: 'q_controlled_vocab_seed'})
MERGE (l)-[r:ANCHORED_BY]->(q)
ON CREATE SET r.evidence_origin = 'topology_synthesized',
              r.evidence_basis = 'controlled_vocab',
              r.evidence_confidence = 'unklar',
              r.is_bookkeeping = true,
              r.migration_origin = 'mig_r2_a_restore_layer';

// Audits
MATCH (l:Layer) RETURN 'layer_count' AS check, count(l) AS c;
MATCH ()-[r:TEILT_LAYER]->() RETURN 'teilt_layer_count' AS check, count(r) AS c;
MATCH (bt:Bauteiltyp) WHERE bt.brand_layer IS NOT NULL
  AND NOT exists{(bt)-[:TEILT_LAYER]->(:Layer)}
RETURN 'bauteiltyp_no_edge' AS check, count(bt) AS violations;
