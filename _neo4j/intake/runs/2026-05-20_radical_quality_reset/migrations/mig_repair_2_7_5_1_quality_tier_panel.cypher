// ===========================================================================
//  mig_repair_2_7_5_1_quality_tier_panel.cypher
//
//  Repair Agent E (2026-05-21) — fold 9 Phase-5.1 audit scalars on :Projekt
//  into a single compact JSON string property `quality_tier_facts`, so the
//  Phase 2.7 panel targets are met literally without losing any of the
//  Phase 5.1 tier-derivation provenance.
//
//  Background
//  ----------
//  Phase 5.1 (mig_5_1_quality_tier.cypher) added these scalars to every
//  :Projekt node (101 of 101 today):
//
//    quality_tier_computed_by        (STRING)
//    quality_tier_n_bg               (INTEGER)
//    quality_tier_n_bg_quantified    (INTEGER)
//    quality_tier_n_curated_evidence (INTEGER)
//    quality_tier_has_year           (BOOL)
//    quality_tier_has_land           (BOOL)
//    quality_tier_has_components     (BOOL)
//    quality_tier_has_metric         (BOOL)
//    quality_tier_has_evidence       (BOOL)
//
//  Final Verifier 6 (Phase 2.7) noted that this addition pushed the
//  :Projekt distinct property keys to 30 (target <=25) and per-node key
//  count to 21-26 (target <=18). The verifier explicitly recommended
//  folding these 9 scalars into one map/string property.
//
//  This repair therefore:
//    1. Encodes the 9 scalars as a JSON object (via apoc.convert.toJson),
//       sorted alphabetically inside the object, and stores it on each
//       :Projekt as a STRING property `quality_tier_facts` (one new key).
//    2. Removes the 9 scalars from the property bag.
//    3. Leaves `quality_tier` itself in place as a directly-visible string,
//       since the plan §5.1 keeps it as a permanent panel-visible attribute.
//
//  Result on the live graph (mit-bestand):
//    distinct keys on :Projekt: 30 -> 22  (<=25 ✓)
//    max per-node key count:    26 -> 18  (<=18 ✓ for max; <=14 for typical)
//
//  Idempotency
//  -----------
//  Guarded by `WHERE p.quality_tier_computed_by IS NOT NULL`.  A re-run is
//  a no-op once the fold has been applied; if `mig_5_1_quality_tier.cypher`
//  is later re-executed the 9 scalars will reappear and this repair can be
//  re-run to fold them again.
//
//  Reversibility
//  -------------
//  The JSON string carries every value verbatim, so the original scalar
//  bag can be reconstructed with:
//
//    MATCH (p:Projekt) WITH p, apoc.convert.fromJsonMap(p.quality_tier_facts) AS f
//    SET p.quality_tier_computed_by        = f.computed_by,
//        p.quality_tier_n_bg               = f.n_bg,
//        p.quality_tier_n_bg_quantified    = f.n_bg_quantified,
//        p.quality_tier_n_curated_evidence = f.n_curated_evidence,
//        p.quality_tier_has_year           = f.has_year,
//        p.quality_tier_has_land           = f.has_land,
//        p.quality_tier_has_components     = f.has_components,
//        p.quality_tier_has_metric         = f.has_metric,
//        p.quality_tier_has_evidence       = f.has_evidence
//    REMOVE p.quality_tier_facts;
//
//  No graph topology changes; no edge changes; no other label changes.
//  `quality_tier` itself is never touched (Tier 2 / 3 assignments stand).
// ===========================================================================

// ---------------------------------------------------------------------------
// Repair step 1 — fold the 9 scalars into `quality_tier_facts` JSON string
//                 and remove the originals.
// ---------------------------------------------------------------------------
MATCH (p:Projekt)
WHERE p.quality_tier_computed_by IS NOT NULL
WITH p, apoc.convert.toJson({
        computed_by:        p.quality_tier_computed_by,
        has_components:     p.quality_tier_has_components,
        has_evidence:       p.quality_tier_has_evidence,
        has_land:           p.quality_tier_has_land,
        has_metric:         p.quality_tier_has_metric,
        has_year:           p.quality_tier_has_year,
        n_bg:               p.quality_tier_n_bg,
        n_bg_quantified:    p.quality_tier_n_bg_quantified,
        n_curated_evidence: p.quality_tier_n_curated_evidence,
        repaired_by:        'mig_repair_2_7_5_1_quality_tier_panel',
        repaired_at:        '2026-05-21'
}) AS facts_json
SET p.quality_tier_facts = facts_json
REMOVE p.quality_tier_computed_by,
       p.quality_tier_has_components,
       p.quality_tier_has_evidence,
       p.quality_tier_has_land,
       p.quality_tier_has_metric,
       p.quality_tier_has_year,
       p.quality_tier_n_bg,
       p.quality_tier_n_bg_quantified,
       p.quality_tier_n_curated_evidence;

// ---------------------------------------------------------------------------
// Audit — post-state of the Projekt property panel.
// ---------------------------------------------------------------------------
MATCH (p:Projekt) UNWIND keys(p) AS k
RETURN count(DISTINCT k) AS projekt_distinct_keys_after;

MATCH (p:Projekt)
RETURN p.id AS id, size(keys(p)) AS n_keys
ORDER BY n_keys DESC LIMIT 5;

MATCH (p:Projekt)
WHERE p.quality_tier_facts IS NULL
RETURN count(p) AS projekt_without_facts_after;

MATCH (p:Projekt)
RETURN p.quality_tier AS tier, count(p) AS n
ORDER BY tier;
