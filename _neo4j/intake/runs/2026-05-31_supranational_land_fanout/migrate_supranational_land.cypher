// ============================================================
// MIGRATION: Expand supranational Land nodes to actual countries
// Date: 2026-05-31
//
// land_eu  (12 rels) -> fan out to 10 EU member states in graph
// land_eea (4 rels)  -> fan out to EU + Norwegen (11 states)
// land_international -> connections dropped (LEED only, user instruction)
//
// EU countries in graph:
//   Belgien, Deutschland, Dänemark, Finnland, Frankreich,
//   Italien, Luxemburg, Niederlande, Portugal, Österreich
// EEA adds: Norwegen
// ============================================================

// Step 1: Fan out land_eu GILT_IN_LAND to all EU member states in graph
MATCH (source)-[r:GILT_IN_LAND]->(eu:Land {id: 'land_eu'})
MATCH (target:Land) WHERE target.id IN [
  'land_belgien', 'land_deutschland', 'land_daenemark', 'land_finnland',
  'land_frankreich', 'land_italien', 'land_luxemburg', 'land_niederlande',
  'land_portugal', 'land_oesterreich'
]
MERGE (source)-[nr:GILT_IN_LAND]->(target)
ON CREATE SET
  nr.id                       = coalesce(source.id, elementId(source)) + '__GILT_IN_LAND__' + target.id,
  nr.evidence_basis           = r.evidence_basis,
  nr.evidence_confidence      = r.evidence_confidence,
  nr.evidence_origin          = r.evidence_origin,
  nr.evidence_excerpt         = r.evidence_excerpt,
  nr.evidence_source_id       = r.evidence_source_id,
  nr.derivation_note          = coalesce(r.derivation_note, '') + ' | expanded from land_eu supranational scope 2026-05-31',
  nr.review_status            = r.review_status,
  nr.source_resolution_status = r.source_resolution_status,
  nr.source_status            = r.source_status,
  nr.source_status_migration  = r.source_status_migration,
  nr.source_status_normalized_at = r.source_status_normalized_at,
  nr.source_status_reason     = r.source_status_reason,
  nr.source_trace_migrated_at = r.source_trace_migrated_at,
  nr.source_trace_migration   = r.source_trace_migration;

// Step 2: Fan out land_eea GILT_IN_LAND to all EEA states (EU + Norwegen)
MATCH (source)-[r:GILT_IN_LAND]->(eea:Land {id: 'land_eea'})
MATCH (target:Land) WHERE target.id IN [
  'land_belgien', 'land_deutschland', 'land_daenemark', 'land_finnland',
  'land_frankreich', 'land_italien', 'land_luxemburg', 'land_niederlande',
  'land_portugal', 'land_oesterreich',
  'land_norwegen'
]
MERGE (source)-[nr:GILT_IN_LAND]->(target)
ON CREATE SET
  nr.id                       = coalesce(source.id, elementId(source)) + '__GILT_IN_LAND__' + target.id,
  nr.evidence_basis           = r.evidence_basis,
  nr.evidence_confidence      = r.evidence_confidence,
  nr.evidence_origin          = r.evidence_origin,
  nr.evidence_excerpt         = r.evidence_excerpt,
  nr.evidence_source_id       = r.evidence_source_id,
  nr.derivation_note          = coalesce(r.derivation_note, '') + ' | expanded from land_eea supranational scope 2026-05-31',
  nr.review_status            = r.review_status,
  nr.source_resolution_status = r.source_resolution_status,
  nr.source_status            = r.source_status,
  nr.source_status_migration  = r.source_status_migration,
  nr.source_status_normalized_at = r.source_status_normalized_at,
  nr.source_status_reason     = r.source_status_reason,
  nr.source_trace_migrated_at = r.source_trace_migrated_at,
  nr.source_trace_migration   = r.source_trace_migration;

// Step 3: Delete all 3 supranational nodes and all their remaining relationships
MATCH (n:Land) WHERE n.id IN ['land_eu', 'land_eea', 'land_international']
DETACH DELETE n;
