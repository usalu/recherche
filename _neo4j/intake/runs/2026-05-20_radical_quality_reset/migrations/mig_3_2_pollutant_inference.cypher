// =====================================================================
// mig_3_2 — Phase 3.2: pollutant inference
//
// Replaces the legacy :HAT_SCHADSTOFF type with two new, semantically
// precise types:
//
//   (:Bauteilgruppe|:Projekt)-[:HAS_RISK_POLLUTANT]->(:Schadstoff)
//   (:Projekt)               -[:REQUIRES_VERIFICATION_FOR]->(:Schadstoff)
//
// Inference rules ranked by strength:
//   a) documented        — every existing :HAT_SCHADSTOFF edge is promoted
//                          to :HAS_RISK_POLLUTANT with basis='documented'.
//                          Original edge is deleted (idempotent on re-run
//                          because step (a) finds no HAT_SCHADSTOFF edges
//                          after the first run).
//   b) era_and_material  — :Bauteilgruppe whose donor :Bauwerk has a
//                          :BUILT_IN_ERA edge AND whose :NUTZT_MATERIAL
//                          target is :TYPISCH_BEI_MATERIAL of a :Schadstoff
//                          that is also :TYPISCH_BEI_ERA of the same era.
//   c) material_only     — fallback for the remaining material matches
//                          where (b) did not already fire.
//   d) project rollup    — for every (:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg)
//                          carrying a :HAS_RISK_POLLUTANT to s, emit a
//                          (:Projekt)-[:REQUIRES_VERIFICATION_FOR]->(s)
//                          edge tagged with the strongest pollutant_basis.
//
// NOTE on the donor edge: Phase 4.2 renamed :AUS_BAUWERK to :FROM_DONOR.
// Rule (b) uses :FROM_DONOR because the donor building's era determines
// the era during which the component (and any pollutants) was installed.
//
// Idempotency: MERGE on every created edge; properties are SET ON CREATE
// only when the basis is being upgraded (e.g. from material_only to
// era_and_material). Re-running produces zero new edges.
// =====================================================================

// 3_2.a — Promote any remaining :HAT_SCHADSTOFF edges to :HAS_RISK_POLLUTANT
MATCH (a)-[r:HAT_SCHADSTOFF]->(s:Schadstoff)
MERGE (a)-[r2:HAS_RISK_POLLUTANT]->(s)
ON CREATE SET r2.id                  = 'r_' + coalesce(a.id, elementId(a)) + '__HAS_RISK_POLLUTANT__' + s.id + '__documented',
              r2.evidence_origin     = coalesce(r.evidence_origin, 'curated'),
              r2.evidence_basis      = 'documented',
              r2.evidence_excerpt    = r.evidence_excerpt,
              r2.evidence_source_id  = coalesce(r.evidence_source_id, r.source),
              r2.evidence_confidence = coalesce(r.evidence_confidence, 'belegt'),
              r2.source_scope        = r.source_scope
ON MATCH SET  r2.evidence_basis      = 'documented',
              r2.evidence_origin     = coalesce(r.evidence_origin, r2.evidence_origin),
              r2.evidence_source_id  = coalesce(r.evidence_source_id, r.source, r2.evidence_source_id),
              r2.evidence_confidence = coalesce(r.evidence_confidence, r2.evidence_confidence)
WITH r
DELETE r;

// 3_2.b — Strongest inference rule: donor-era + bauteilgruppe-material both match
MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)
       <-[:TYPISCH_BEI_MATERIAL]-(s:Schadstoff)-[:TYPISCH_BEI_ERA]->(e:BauwerkEra)
MATCH (bg)-[:FROM_DONOR]->(b:Bauwerk)-[:BUILT_IN_ERA]->(e)
MERGE (bg)-[r:HAS_RISK_POLLUTANT]->(s)
ON CREATE SET r.id                  = 'r_' + bg.id + '__HAS_RISK_POLLUTANT__' + s.id + '__era_and_material',
              r.evidence_origin     = 'inferred',
              r.evidence_basis      = 'era_and_material',
              r.evidence_excerpt    = NULL,
              r.evidence_source_id  = 'q_schadstoff_reuse_knowledge_graph_research_md',
              r.evidence_confidence = 'inferiert'
ON MATCH SET  r.evidence_basis      = CASE
                                        WHEN r.evidence_basis IN ['documented'] THEN r.evidence_basis
                                        ELSE 'era_and_material'
                                      END,
              r.evidence_origin     = CASE
                                        WHEN r.evidence_basis = 'documented' THEN r.evidence_origin
                                        ELSE 'inferred'
                                      END,
              r.evidence_source_id  = coalesce(r.evidence_source_id, 'q_schadstoff_reuse_knowledge_graph_research_md');

// 3_2.c — Weaker rule: material-only (fires only when (b) did not already create the edge)
MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)<-[:TYPISCH_BEI_MATERIAL]-(s:Schadstoff)
WHERE NOT exists{ (bg)-[:HAS_RISK_POLLUTANT]->(s) }
MERGE (bg)-[r:HAS_RISK_POLLUTANT]->(s)
ON CREATE SET r.id                  = 'r_' + bg.id + '__HAS_RISK_POLLUTANT__' + s.id + '__material_only',
              r.evidence_origin     = 'inferred',
              r.evidence_basis      = 'material_only',
              r.evidence_excerpt    = NULL,
              r.evidence_source_id  = 'q_schadstoff_reuse_knowledge_graph_research_md',
              r.evidence_confidence = 'inferiert';

// 3_2.d — Project-level rollup
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)-[r:HAS_RISK_POLLUTANT]->(s:Schadstoff)
WITH p, s,
     CASE
       WHEN any(b IN collect(r.evidence_basis) WHERE b = 'documented') THEN 'documented'
       WHEN any(b IN collect(r.evidence_basis) WHERE b = 'era_and_material') THEN 'era_and_material'
       ELSE 'material_only'
     END AS strongest_basis
MERGE (p)-[v:REQUIRES_VERIFICATION_FOR]->(s)
ON CREATE SET v.id                  = 'r_' + p.id + '__REQUIRES_VERIFICATION_FOR__' + s.id,
              v.pollutant_basis     = strongest_basis,
              v.evidence_origin     = CASE strongest_basis WHEN 'documented' THEN 'curated' ELSE 'inferred' END,
              v.evidence_basis      = 'project_rollup',
              v.evidence_source_id  = 'q_schadstoff_reuse_knowledge_graph_research_md',
              v.evidence_confidence = CASE strongest_basis WHEN 'documented' THEN 'belegt' ELSE 'inferiert' END
ON MATCH SET  v.pollutant_basis     = strongest_basis,
              v.evidence_origin     = CASE strongest_basis WHEN 'documented' THEN 'curated' ELSE coalesce(v.evidence_origin, 'inferred') END,
              v.evidence_confidence = CASE strongest_basis WHEN 'documented' THEN 'belegt' ELSE coalesce(v.evidence_confidence, 'inferiert') END;

// 3_2.e — Audits
MATCH ()-[r:HAT_SCHADSTOFF]->()
RETURN 'hat_schadstoff_remaining' AS check, count(r) AS c;

MATCH ()-[r:HAS_RISK_POLLUTANT]->()
RETURN 'has_risk_pollutant_total' AS check, count(r) AS c;

MATCH ()-[r:HAS_RISK_POLLUTANT]->()
RETURN 'has_risk_pollutant_by_basis' AS check, r.evidence_basis AS basis, count(r) AS c
ORDER BY basis;

MATCH ()-[r:REQUIRES_VERIFICATION_FOR]->()
RETURN 'requires_verification_for_total' AS check, count(r) AS c;

MATCH ()-[r:REQUIRES_VERIFICATION_FOR]->()
RETURN 'requires_verification_for_by_basis' AS check, r.pollutant_basis AS basis, count(r) AS c
ORDER BY basis;
