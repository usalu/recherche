// ==========================================================================
// mig_r1_evidence_origin_split — split evidence_origin enum and
// move bookkeeping out of evidence_confidence
//
// New enum: evidence_origin ∈ {source_curated, topology_synthesized,
//                              registry_derived, inferred, external_unfolded}
// New property: is_bookkeeping: bool
// evidence_confidence loses 'bookkeeping' value (becomes 'unklar' + is_bookkeeping)
//
// Idempotent: re-running classifies any edges that already have new-enum
// values as a no-op (each WHERE clause filters on the OLD value).
// ==========================================================================

// R1.a — Repair D's Q1 promotion → topology_synthesized
//        Pre-count: 254 HAT_BAUTEILGRUPPE edges
MATCH ()-[r]->()
WHERE r.evidence_origin = 'curated'
  AND r.migration_origin IS NOT NULL
  AND r.migration_origin CONTAINS 'mig_repair_4_1_q1'
SET r.evidence_origin = 'topology_synthesized',
    r.derivation_note = coalesce(r.derivation_note, '') +
      ' | r1: curated→topology_synthesized (Repair D Q1 promotion was a relabel, not a curation)';

// R1.b — Repair D's A1–A5 registry excerpt fills → registry_derived
//        Pre-count: ~1,366 edges across HAT_AKTEURROLLE, HAT_AKTEURTYP,
//        LIEGT_IN_LAND, VERBUNDEN_MIT_AKTEUR, ASSOZIIERT_MIT_PROJEKT
MATCH ()-[r]->()
WHERE r.evidence_origin = 'curated'
  AND r.migration_origin IS NOT NULL
  AND r.migration_origin CONTAINS 'mig_repair_4_1_excerpts'
SET r.evidence_origin = 'registry_derived',
    r.derivation_note = coalesce(r.derivation_note, '') +
      ' | r1: curated→registry_derived (Repair D A1–A5 excerpts are auto-generated from registry identity)';

// R1.c — Repair D's B step (actor S-ref BELEGT_IN) → registry_derived
//        Pre-count: ~314
MATCH (:Akteur)-[r:BELEGT_IN]->(:Quelle)
WHERE r.evidence_origin = 'curated'
  AND r.evidence_source_id IS NOT NULL
  AND r.evidence_source_id STARTS WITH 'q_actor_'
SET r.evidence_origin = 'registry_derived',
    r.derivation_note = coalesce(r.derivation_note, '') +
      ' | r1: curated→registry_derived (actor S-ref BELEGT_IN)';

// R1.d — Repair D's unpack step (22 edges from Phase 1.6 merge artifacts) → topology_synthesized
MATCH ()-[r]->()
WHERE r.migration_origin IS NOT NULL
  AND r.migration_origin CONTAINS 'mig_repair_4_1_unpack'
SET r.evidence_origin = 'topology_synthesized',
    r.derivation_note = coalesce(r.derivation_note, '') +
      ' | r1: curated→topology_synthesized (merge-artifact unpack picked curated arbitrarily)';

// R1.e — mig_4c_1 external_sources unfold → external_unfolded
MATCH ()-[r:ZITIERT_QUELLE]->()
WHERE r.evidence_basis = 'external_sources_array'
SET r.evidence_origin = 'external_unfolded',
    r.derivation_note = coalesce(r.derivation_note, '') +
      ' | r1: derived→external_unfolded (mig_4c_1 citation-array unfold)';

// R1.f — All remaining 'curated' → 'source_curated'
//        These are the genuinely human-curated edges (dossier section parses).
MATCH ()-[r]->()
WHERE r.evidence_origin = 'curated'
SET r.evidence_origin = 'source_curated',
    r.derivation_note = coalesce(r.derivation_note, '') +
      ' | r1: curated→source_curated (default reclassification)';

// R1.g — Move bookkeeping out of evidence_confidence
//        Pre-count: 703 ANCHORED_BY edges
MATCH ()-[r]->()
WHERE r.evidence_confidence = 'bookkeeping'
SET r.is_bookkeeping = true,
    r.evidence_confidence = 'unklar',
    r.derivation_note = coalesce(r.derivation_note, '') +
      ' | r1: confidence=bookkeeping→unklar + is_bookkeeping=true';

// R1.h — ReuseRule contradiction fix
//        Pre-count: 60 edges (20 APPLIES_IN + 20 APPLIES_TO + ~20 REFERENZIERT_NORM)
MATCH (rule:ReuseRule)-[r]->()
WHERE r.evidence_origin = 'inferred' AND r.evidence_confidence = 'belegt'
SET r.evidence_confidence = 'teilweise_belegt',
    r.derivation_note = coalesce(r.derivation_note, '') +
      ' | r1: inferred+belegt was self-contradictory; downgraded to teilweise_belegt';

// R1.h-node — Also fix the ReuseRule node-level evidence_confidence
MATCH (rule:ReuseRule)
WHERE rule.evidence_origin = 'inferred' AND rule.evidence_confidence = 'belegt'
SET rule.evidence_confidence = 'teilweise_belegt';

// R1.i — D10 decision: downgrade registry_derived edges confidence to teilweise_belegt
//        (registry data is name-level belegt, not project-participation belegt)
MATCH ()-[r]->()
WHERE r.evidence_origin = 'registry_derived'
  AND r.evidence_confidence = 'belegt'
SET r.evidence_confidence = 'teilweise_belegt',
    r.derivation_note = coalesce(r.derivation_note, '') +
      ' | r1: registry_derived confidence belegt→teilweise_belegt (D10 conservative default)';

// ==========================================================================
// HARD-RULE AUDITS — runner MUST assert each returns 0
// ==========================================================================

// 1) No edge retains the old 'curated' value
MATCH ()-[r]->() WHERE r.evidence_origin = 'curated'
RETURN 'audit_old_curated_remaining' AS rule, count(r) AS violations;

// 2) No edge retains 'bookkeeping' in confidence enum
MATCH ()-[r]->() WHERE r.evidence_confidence = 'bookkeeping'
RETURN 'audit_bookkeeping_in_confidence' AS rule, count(r) AS violations;

// 3) Every evidence_origin in new 5-value enum
MATCH ()-[r]->()
WHERE r.evidence_origin IS NOT NULL
  AND NOT r.evidence_origin IN ['source_curated','topology_synthesized','registry_derived','inferred','external_unfolded']
RETURN 'audit_origin_enum_violation' AS rule, count(r) AS violations;

// 4) Every evidence_confidence in new 4-value enum
MATCH ()-[r]->()
WHERE r.evidence_confidence IS NOT NULL
  AND NOT r.evidence_confidence IN ['belegt','teilweise_belegt','unklar','inferiert']
RETURN 'audit_confidence_enum_violation' AS rule, count(r) AS violations;

// 5) is_bookkeeping=true count matches expected 703 ANCHORED_BY
MATCH ()-[r {is_bookkeeping: true}]->()
RETURN 'audit_is_bookkeeping_count' AS rule, count(r) AS c,
       703 AS expected;
