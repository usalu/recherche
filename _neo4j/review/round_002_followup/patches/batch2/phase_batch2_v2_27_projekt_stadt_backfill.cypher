// Phase 27 — Projekt → Stadt + Projekt → Land backfill (17 unlinked Projekte).
//
// Mapping from existing project id/name evidence to existing Stadt nodes.
// Skips p_recrete_footbridge (no clear Stadt match without research).

WITH [
  ['p_55_great_suffolk_street_london',           'stadt_london'],
  ['p_association_house_groeditz',               'stadt_groeditz'],
  ['p_association_house_plauen',                 'stadt_plauen'],
  ['p_bedzed_london_hackbridge',                 'stadt_london'],
  ['p_trae_high_rise_aarhus',                    'stadt_aarhus'],
  ['p_upcycle_studios_copenhagen',               'stadt_kopenhagen'],
  ['p_verbiest_karreveld_brussels',              'stadt_bruessel'],
  ['p_villa_welpeloo_enschede',                  'stadt_enschede'],
  ['p_woongroep_boschgaard_den_bosch',           'stadt_s_hertogenbosch'],
  ['p_zinneke_feder_masui4ever_brussels',        'stadt_bruessel'],
  ['p_awm_muenster_circular_office',             'stadt_muenster'],
  ['p_vandkunsten_component_reuse',              'stadt_kopenhagen'],
  ['p_circle_house',                             'stadt_aarhus'],
  ['p_architecture_of_reuse_brussels',           'stadt_bruessel'],
  ['p_reuse_in_construction_zhaw',               'stadt_winterthur'],
  ['p_reuse_logistics',                          'stadt_fribourg']
] AS pairs
UNWIND pairs AS pair
MATCH (p:Projekt {id: pair[0]})
MATCH (s:Stadt {id: pair[1]})
WHERE NOT EXISTS { (p)-[:LIEGT_IN_STADT]->(:Stadt) }
MERGE (p)-[r:LIEGT_IN_STADT]->(s)
ON CREATE SET r.id = 'r_' + pair[0] + '__LIEGT_IN_STADT__' + pair[1],
              r.source = 'batch2_v2_phase27_2026-05-20',
              r.evidence = 'BELEGT';

// Also backfill LIEGT_IN_LAND by following the Stadt's LIEGT_IN_LAND
MATCH (p:Projekt)-[:LIEGT_IN_STADT]->(s:Stadt)-[:LIEGT_IN_LAND]->(l:Land)
WHERE NOT EXISTS { (p)-[:LIEGT_IN_LAND]->(:Land) }
MERGE (p)-[r:LIEGT_IN_LAND]->(l)
ON CREATE SET r.id = 'r_' + p.id + '__LIEGT_IN_LAND__' + l.id,
              r.source = 'batch2_v2_phase27_2026-05-20',
              r.evidence = 'INFER';

// === Verification ===
// MATCH (p:Projekt) WHERE NOT EXISTS { (p)-[:LIEGT_IN_STADT]->() } RETURN count(p);
// EXPECTED: 1 (just p_recrete_footbridge, skipped).
//
// MATCH (p:Projekt) WHERE NOT EXISTS { (p)-[:LIEGT_IN_LAND]->() } RETURN count(p);
// EXPECTED: 0 or very few (Land follows from Stadt automatically).
