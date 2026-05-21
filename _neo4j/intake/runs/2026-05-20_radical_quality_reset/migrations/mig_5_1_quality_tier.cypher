// ===========================================================================
//  mig_5_1_quality_tier.cypher
//  Phase 5.1 — Compute Projekt.quality_tier on every :Projekt node.
//
//  Implements plan section 5.1 verbatim:
//    Tier 1 (decision-grade) requires ALL of:
//      - year_completed IS NOT NULL
//      - LIEGT_IN_LAND edge present
//      - count(distinct HAT_BAUTEILGRUPPE) >= 3
//      - at least one of:
//          (a) >=1 Bauteilgruppe with non-null quantity
//              (menge_t | menge_stueck | menge_m2 | menge_kg | menge_m)
//          (b) >=1 Projekt.reuse_share_facts entry
//          (c) >=1 Projekt.co2_facts entry
//      - >=3 BELEGT_IN edges with
//          evidence_origin='curated' AND evidence_excerpt IS NOT NULL
//          AND evidence_confidence IN ('belegt','teilweise_belegt')
//    Tier 2: any project meeting >=2 of the five sub-criteria but failing
//            the Tier 1 conjunction.
//    Tier 3: everything else.
// ===========================================================================

// ---------------------------------------------------------------------------
//  Pre-fix from Verifier 10: remap 15 REFERENZIERT_NORM edges that carry
//  evidence_confidence='mittel' (legacy 'mittel' label) so they fit the
//  canonical confidence vocabulary used by the tier computation and the
//  trust-check query.  All 15 originate from the Phase 2.5 LCA-module
//  demotion (former :LebenszyklusModul references DIN/ISO LCA norms).
// ---------------------------------------------------------------------------

MATCH ()-[r:REFERENZIERT_NORM]->()
WHERE r.evidence_confidence = 'mittel'
SET r.evidence_confidence = 'teilweise_belegt',
    r.derivation_note = CASE
        WHEN r.derivation_note IS NULL OR r.derivation_note = ''
            THEN 'mittel->teilweise_belegt via mig_5_1_pretier (Verifier 10 finding)'
        ELSE r.derivation_note + ' | mittel->teilweise_belegt via mig_5_1_pretier (Verifier 10 finding)'
    END;

// ---------------------------------------------------------------------------
//  Tier computation — single pass over every :Projekt node.
//  Idempotent: re-running overwrites quality_tier with the recomputed value.
// ---------------------------------------------------------------------------

MATCH (p:Projekt)
OPTIONAL MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
WITH p,
     count(DISTINCT bg) AS n_bg,
     sum(CASE WHEN bg.menge_t      IS NOT NULL
                OR bg.menge_stueck IS NOT NULL
                OR bg.menge_m2     IS NOT NULL
                OR bg.menge_kg     IS NOT NULL
                OR bg.menge_m      IS NOT NULL
              THEN 1 ELSE 0 END)  AS n_bg_quantified
OPTIONAL MATCH (p)-[bel:BELEGT_IN]->()
WITH p, n_bg, n_bg_quantified,
     sum(CASE WHEN bel.evidence_origin     = 'curated'
                AND bel.evidence_excerpt   IS NOT NULL
                AND bel.evidence_confidence IN ['belegt','teilweise_belegt']
              THEN 1 ELSE 0 END)  AS n_curated_evidence
WITH p, n_bg, n_bg_quantified, n_curated_evidence,
     (p.year_completed IS NOT NULL)                              AS has_year,
     exists{(p)-[:LIEGT_IN_LAND]->()}                            AS has_land,
     (n_bg >= 3)                                                 AS has_components,
     (n_bg_quantified >= 1
          OR size(coalesce(p.reuse_share_facts, [])) >= 1
          OR size(coalesce(p.co2_facts,         [])) >= 1)        AS has_metric,
     (n_curated_evidence >= 3)                                   AS has_evidence
SET p.quality_tier_n_bg                = n_bg,
    p.quality_tier_n_bg_quantified     = n_bg_quantified,
    p.quality_tier_n_curated_evidence  = n_curated_evidence,
    p.quality_tier_has_year            = has_year,
    p.quality_tier_has_land            = has_land,
    p.quality_tier_has_components      = has_components,
    p.quality_tier_has_metric          = has_metric,
    p.quality_tier_has_evidence        = has_evidence,
    p.quality_tier = CASE
        WHEN has_year AND has_land AND has_components AND has_metric AND has_evidence
            THEN 'tier_1_decision_grade'
        WHEN (toInteger(has_year)
              + toInteger(has_land)
              + toInteger(has_components)
              + toInteger(has_metric)
              + toInteger(has_evidence)) >= 2
            THEN 'tier_2_documentation_only'
        ELSE 'tier_3_stub'
    END,
    p.quality_tier_computed_by = 'mig_5_1_quality_tier';

// ---------------------------------------------------------------------------
//  Audit: distribution per tier.
// ---------------------------------------------------------------------------
MATCH (p:Projekt)
RETURN p.quality_tier AS tier, count(p) AS n
ORDER BY tier;
