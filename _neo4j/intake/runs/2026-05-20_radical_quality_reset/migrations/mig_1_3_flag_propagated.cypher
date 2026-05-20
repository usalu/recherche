// =============================================================================
// mig_1_3_flag_propagated.cypher
// Phase 1.3 — Propagated MARKTMODELL flagging + dominant-edge removal
// Author: Agent 3 (Wave 1)
// Plan ref: c:/Users/Kinosh/.cursor/plans/radical_quality-first_reset_8d1e2b66.plan.md
//           section 1.3
// Database: mit-bestand
//
// Pre-migration verified counts (snapshot 2026-05-20T20:42 + live re-check):
//   - HAT_MARKTMODELL edges with source_excerpt CONTAINS 'propagated' : 319 / 384
//     (sole literal observed: "propagated from project HAT_DOMINANT_MARKTMODELL
//                              (project-wide sourcing)")
//   - HAT_DOMINANT_MARKTMODELL edges : 86
//   - HAT_DOMINANT_AKZEPTANZ edges   : 24
//
// Expected effects:
//   1.3.a  319 HAT_MARKTMODELL edges flagged (source_excerpt removed; canonical
//          evidence shape set; original_source_excerpt preserved for audit)
//   1.3.b  86 HAT_DOMINANT_MARKTMODELL edges deleted
//   1.3.c  24 HAT_DOMINANT_AKZEPTANZ edges deleted
// Net edge delta: -110 (86+24). 319 edges keep their topology, lose their
// misleading template-string excerpt, and gain explicit `derived/bookkeeping`
// provenance.
// =============================================================================

// -----------------------------------------------------------------------------
// 1.3.a  Re-shape the 319 propagated HAT_MARKTMODELL excerpts.
// Preserve the literal template string under `original_source_excerpt` (audit
// field) and remove the misleading `source_excerpt` so queries cannot mistake
// the string for real evidence. The WITH clause materialises the original
// excerpt value before any SET/REMOVE runs, so ordering can never lose it.
// -----------------------------------------------------------------------------
MATCH ()-[r:HAT_MARKTMODELL]->()
WHERE r.source_excerpt CONTAINS 'propagated'
WITH r, r.source_excerpt AS original_excerpt
SET r.evidence_origin         = 'derived',
    r.evidence_basis          = 'propagated',
    r.evidence_excerpt        = NULL,
    r.evidence_confidence     = 'bookkeeping',
    r.original_source_excerpt = original_excerpt
REMOVE r.source_excerpt
RETURN count(r) AS hat_marktmodell_flagged;

// -----------------------------------------------------------------------------
// 1.3.b  Drop HAT_DOMINANT_MARKTMODELL — information is re-derivable from the
// surviving 384 HAT_MARKTMODELL edges by count/aggregation.
// -----------------------------------------------------------------------------
MATCH ()-[r:HAT_DOMINANT_MARKTMODELL]->()
DELETE r
RETURN count(*) AS hat_dominant_marktmodell_deleted;

// -----------------------------------------------------------------------------
// 1.3.c  Drop HAT_DOMINANT_AKZEPTANZ — same rationale (re-derivable from
// surviving HAT_AKZEPTANZ edges).
// -----------------------------------------------------------------------------
MATCH ()-[r:HAT_DOMINANT_AKZEPTANZ]->()
DELETE r
RETURN count(*) AS hat_dominant_akzeptanz_deleted;
