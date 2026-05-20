// =====================================================================
// mig_3_1 — Phase 3.1: wire (:Bauwerk)-[:BUILT_IN_ERA]->(:BauwerkEra)
//
//   * Backfill from existing year property `baujahr` on :Bauwerk
//     (the alternative `jahr_errichtet` is NOT present in mit-bestand)
//   * Backfill from dossier-loaded evidence is a no-op: Phase 4b loaders
//     did not extract donor-era metadata into a queryable cypher source
//     (see logs/agent10_research_registry_loader.py outputs). Any future
//     dossier-emitted Bauwerk.baujahr will be picked up by re-running this
//     migration (MERGE-based, idempotent).
//   * Set era_unknown=true on every :Bauwerk and :Materialdepot that did
//     not pick up a :BUILT_IN_ERA edge after this pass.
//
// All edges created in this migration carry:
//     evidence_origin='curated'
//     evidence_basis='year_inferred'
//     evidence_source_id='bauwerk.baujahr_property'
//     evidence_confidence='belegt'
//
// Idempotency: MERGE on the edge; SET on properties; no DELETE.
// =====================================================================

// 3_1.a — Backfill from Bauwerk.baujahr (8 Bauwerke today)
MATCH (b:Bauwerk)
WHERE b.baujahr IS NOT NULL
WITH b, toInteger(b.baujahr) AS y
MATCH (e:BauwerkEra)
WHERE (e.id='era_vor_1900'            AND y <  1900)
   OR (e.id='era_1900_1945'           AND y >= 1900 AND y <= 1945)
   OR (e.id='era_nachkrieg_1945_1970' AND y >  1945 AND y <= 1970)
   OR (e.id='era_1970_1990'           AND y >  1970 AND y <= 1990)
   OR (e.id='era_1990_2000'           AND y >  1990 AND y <= 2000)
   OR (e.id='era_post_2000'           AND y >  2000)
MERGE (b)-[r:BUILT_IN_ERA]->(e)
ON CREATE SET r.id = 'r_' + b.id + '__BUILT_IN_ERA__' + e.id,
              r.evidence_origin     = 'curated',
              r.evidence_basis      = 'year_inferred',
              r.evidence_source_id  = 'bauwerk.baujahr_property',
              r.evidence_confidence = 'belegt'
ON MATCH SET  r.evidence_origin     = coalesce(r.evidence_origin, 'curated'),
              r.evidence_basis      = coalesce(r.evidence_basis, 'year_inferred'),
              r.evidence_source_id  = coalesce(r.evidence_source_id, 'bauwerk.baujahr_property'),
              r.evidence_confidence = coalesce(r.evidence_confidence, 'belegt');

// 3_1.b — Backfill from Materialdepot.baujahr (if any donor depot carries a year today)
MATCH (m:Materialdepot)
WHERE m.baujahr IS NOT NULL
WITH m, toInteger(m.baujahr) AS y
MATCH (e:BauwerkEra)
WHERE (e.id='era_vor_1900'            AND y <  1900)
   OR (e.id='era_1900_1945'           AND y >= 1900 AND y <= 1945)
   OR (e.id='era_nachkrieg_1945_1970' AND y >  1945 AND y <= 1970)
   OR (e.id='era_1970_1990'           AND y >  1970 AND y <= 1990)
   OR (e.id='era_1990_2000'           AND y >  1990 AND y <= 2000)
   OR (e.id='era_post_2000'           AND y >  2000)
MERGE (m)-[r:BUILT_IN_ERA]->(e)
ON CREATE SET r.id = 'r_' + m.id + '__BUILT_IN_ERA__' + e.id,
              r.evidence_origin     = 'curated',
              r.evidence_basis      = 'year_inferred',
              r.evidence_source_id  = 'materialdepot.baujahr_property',
              r.evidence_confidence = 'belegt';

// 3_1.c — Final pass: any :Bauwerk without :BUILT_IN_ERA → era_unknown=true
MATCH (b:Bauwerk)
WHERE NOT exists{ (b)-[:BUILT_IN_ERA]->() }
SET b.era_unknown = true;

// 3_1.d — Same for :Materialdepot
MATCH (m:Materialdepot)
WHERE NOT exists{ (m)-[:BUILT_IN_ERA]->() }
SET m.era_unknown = true;

// 3_1.e — Audits
MATCH (:Bauwerk)-[r:BUILT_IN_ERA]->(:BauwerkEra)
RETURN 'built_in_era_bauwerk_total' AS check, count(r) AS c;

MATCH (:Materialdepot)-[r:BUILT_IN_ERA]->(:BauwerkEra)
RETURN 'built_in_era_materialdepot_total' AS check, count(r) AS c;

MATCH (b:Bauwerk)
WHERE b.era_unknown = true
RETURN 'bauwerk_era_unknown_total' AS check, count(b) AS c;

MATCH (m:Materialdepot)
WHERE m.era_unknown = true
RETURN 'materialdepot_era_unknown_total' AS check, count(m) AS c;

MATCH (b:Bauwerk)
WHERE NOT exists{ (b)-[:BUILT_IN_ERA]->() } AND coalesce(b.era_unknown, false) <> true
RETURN 'bauwerk_neither_era_nor_unknown' AS check, count(b) AS c;
