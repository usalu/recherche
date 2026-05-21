// ==========================================================================
// mig_r5_bg_disambiguation.cypher
// Phase R5 — Tag every :Bauteilgruppe with bg_kind ∈ {batch, partial_batch, category}
//
// Plan ref: _neo4j/REVIEW_BASED_PLAN/ORCHESTRATOR_PART_R5.md
// Author: orchestrator (Claude)
// Database: mit-bestand
//
// Classification:
//   batch          = has FROM_DONOR AND INTO_RECEIVER
//   partial_batch  = has exactly one of FROM_DONOR / INTO_RECEIVER
//   category       = has neither
//
// Idempotent: re-running re-derives the same kind from current topology.
// Reversible: REMOVE bg.bg_kind on every :Bauteilgruppe undoes the migration.
// ==========================================================================

// R5.a — Classify and tag
MATCH (bg:Bauteilgruppe)
WITH bg,
     exists{(bg)-[:FROM_DONOR]->()}    AS has_donor,
     exists{(bg)-[:INTO_RECEIVER]->()} AS has_receiver
WITH bg,
     CASE
       WHEN has_donor AND has_receiver        THEN 'batch'
       WHEN has_donor XOR has_receiver        THEN 'partial_batch'
       ELSE 'category'
     END AS new_kind
SET bg.bg_kind = new_kind,
    bg.migration_origin = coalesce(bg.migration_origin, '') +
        CASE WHEN bg.migration_origin IS NULL OR bg.migration_origin = ''
             THEN 'mig_r5_bg_disambiguation'
             ELSE ' | mig_r5_bg_disambiguation' END;

// ==========================================================================
// Audits — runner asserts each
// ==========================================================================

// A1 — Every :Bauteilgruppe has a bg_kind
MATCH (bg:Bauteilgruppe) WHERE bg.bg_kind IS NULL
RETURN 'a1_bg_without_kind' AS rule, count(bg) AS violations;

// A2 — bg_kind respects the enum
MATCH (bg:Bauteilgruppe)
WHERE bg.bg_kind IS NOT NULL
  AND NOT bg.bg_kind IN ['batch','partial_batch','category']
RETURN 'a2_bg_kind_enum_violation' AS rule, count(bg) AS violations;

// A3 — No BG tagged 'category' has any FROM_DONOR or INTO_RECEIVER edge
MATCH (bg:Bauteilgruppe {bg_kind: 'category'})
WHERE exists{(bg)-[:FROM_DONOR]->()} OR exists{(bg)-[:INTO_RECEIVER]->()}
RETURN 'a3_category_with_donor_or_receiver' AS rule, count(bg) AS violations;

// A4 — Every 'batch' BG has BOTH FROM_DONOR and INTO_RECEIVER
MATCH (bg:Bauteilgruppe {bg_kind: 'batch'})
WHERE NOT exists{(bg)-[:FROM_DONOR]->()}
   OR NOT exists{(bg)-[:INTO_RECEIVER]->()}
RETURN 'a4_batch_missing_topology' AS rule, count(bg) AS violations;

// A5 — Every 'partial_batch' BG has exactly one of FROM_DONOR / INTO_RECEIVER
MATCH (bg:Bauteilgruppe {bg_kind: 'partial_batch'})
WITH bg, exists{(bg)-[:FROM_DONOR]->()} AS d, exists{(bg)-[:INTO_RECEIVER]->()} AS r
WHERE (d AND r) OR (NOT d AND NOT r)
RETURN 'a5_partial_batch_misclassified' AS rule, count(bg) AS violations;

// ==========================================================================
// Distribution report (informational)
// ==========================================================================

MATCH (bg:Bauteilgruppe)
RETURN bg.bg_kind AS kind, count(bg) AS c ORDER BY c DESC;

// Cross-check: Q1 canonical pattern picks up at least 254 distinct batches
MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe {bg_kind: 'batch'})-[:INTO_RECEIVER]->(receiver)
RETURN 'q1_canonical_batches_distinct' AS check, count(DISTINCT bg) AS c;

// Sanity for downstream: total bg with any menge_* property, by kind
MATCH (bg:Bauteilgruppe)
WHERE bg.menge_t IS NOT NULL OR bg.menge_kg IS NOT NULL
   OR bg.menge_m2 IS NOT NULL OR bg.menge_m3 IS NOT NULL
   OR bg.menge_stueck IS NOT NULL OR bg.menge_m IS NOT NULL
RETURN bg.bg_kind AS kind, count(bg) AS bg_with_mass
ORDER BY bg_with_mass DESC;
