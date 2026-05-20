// =====================================================================
// mig_4_1 — Phase 4.1: canonical 5-field evidence shape on every edge
//
// Run order:
//   4_1.a  Convert HAT_DEFEKT "propagated from …" excerpts → basis,
//          excerpt nulled, raw text preserved as derivation_note.
//   4_1.b  HAT_MARKTMODELL legacy (source, evidence) cleanup:
//          backfill evidence_source_id from legacy source if missing,
//          REMOVE legacy keys. Origin/basis/conf already correct.
//   4_1.c  All remaining edges with evidence_origin IS NULL get the
//          canonical 5-field shape filled in (origin='derived',
//          basis=per-relationship-default, excerpt=NULL,
//          evidence_source_id='mig_4_1', evidence_confidence='unklar').
//   4_1.d  Final hard-rule audits:
//          - curated requires excerpt
//          - bookkeeping only with origin='derived'
//          - excerpt may not contain 'propagated from'
//          - no edge has missing fields
//
// Idempotency: every step only acts on rows that don't already satisfy
// the post-condition; re-running is a no-op.
//
// Per-relationship evidence_basis enum (from plan §4.1):
//   - BELEGT_IN, BETEILIGT_AN, ASSOZIIERT_MIT_PROJEKT,
//     FROM_DONOR (== AUS_BAUWERK before mig_4_2),
//     INTO_RECEIVER (== EINGEBAUT_IN before mig_4_2),
//     HAT_BAUTEILGRUPPE, HAT_HUERDE, HAT_AKTEURROLLE
//          → 'cell_citation' | 'registry_stub' | 'propagated' | 'controlled_vocab'
//   - HAS_RISK_POLLUTANT, REQUIRES_VERIFICATION_FOR (not yet in graph)
//          → 'documented' | 'era_and_material' | 'material_only' | 'era_only'
//   - BUILT_IN_ERA (not yet in graph)
//          → 'cell_citation' | 'year_inferred' | 'era_unknown'
//   - APPLIES_IN, APPLIES_TO, REFERENZIERT_NORM (only REFERENZIERT_NORM exists today)
//          → 'research_file_row' | 'standards_body'
//   - All other rel types: default basis = 'controlled_vocab' (these are
//     classification edges from entities to vocabulary nodes — exactly
//     what 'controlled_vocab' is for).
// =====================================================================

// ---------------------------------------------------------------------
// 4_1.a — HAT_DEFEKT propagated-from-excerpt fixup (31 edges)
//
// Edges already have origin='derived', conf='unklar' from Phase 2.7's
// legacy strip. The excerpt mistakenly carries the lineage note
// "propagated from project HAT_DEFEKT_BEFUND via material grounding (...)".
// Per plan rule: that lineage signal lives in evidence_basis='propagated'
// and the raw note is preserved on a non-canonical field for audit.
// ---------------------------------------------------------------------

MATCH ()-[r]->()
WHERE r.evidence_excerpt IS NOT NULL
  AND toLower(r.evidence_excerpt) CONTAINS 'propagated from'
SET r.derivation_note    = r.evidence_excerpt,
    r.evidence_basis     = 'propagated',
    r.evidence_excerpt   = NULL,
    r.evidence_origin    = coalesce(r.evidence_origin,    'derived'),
    r.evidence_source_id = coalesce(r.evidence_source_id, 'mig_4_1'),
    r.evidence_confidence = coalesce(r.evidence_confidence, 'unklar');

// ---------------------------------------------------------------------
// 4_1.b — HAT_MARKTMODELL legacy (source, evidence) strip (319 edges)
//
// These already carry origin='derived', basis='propagated',
// confidence='bookkeeping'. The legacy `source` (e.g.
// 'round_003_project_propagation') is the only real provenance hint —
// we lift it into evidence_source_id if not already set, then REMOVE
// both legacy keys.
// ---------------------------------------------------------------------

MATCH ()-[r]->()
WHERE (r.source IS NOT NULL OR r.evidence IS NOT NULL)
SET r.evidence_source_id  = coalesce(r.evidence_source_id, r.source, 'mig_4_1'),
    r.evidence_origin     = coalesce(r.evidence_origin, 'derived'),
    r.evidence_basis      = coalesce(r.evidence_basis, 'propagated'),
    r.evidence_confidence = coalesce(r.evidence_confidence, 'bookkeeping')
REMOVE r.source, r.evidence;

// also drop any lingering source_excerpt / datenqualitaet (already 0
// per agent7_explore.json but the REMOVE is cheap & guarantees the
// closure post-Agent-6).
MATCH ()-[r]->()
WHERE r.source_excerpt IS NOT NULL OR r.datenqualitaet IS NOT NULL
SET r.evidence_excerpt   = coalesce(r.evidence_excerpt, r.source_excerpt),
    r.evidence_confidence = coalesce(
        r.evidence_confidence,
        CASE r.datenqualitaet
          WHEN 'belegt'           THEN 'belegt'
          WHEN 'teilweise_belegt' THEN 'teilweise_belegt'
          WHEN 'unklar'           THEN 'unklar'
          WHEN 'inferiert'        THEN 'inferiert'
          ELSE 'unklar'
        END
    )
REMOVE r.source_excerpt, r.datenqualitaet;

// ---------------------------------------------------------------------
// 4_1.c — Canonical 5-field backfill on the 13 247 edges that still
//          have evidence_origin IS NULL.
//
// All five fields are filled with safe defaults. evidence_excerpt is
// explicitly set to NULL (so the property KEY now exists on the edge
// — required so downstream queries can rely on `r.evidence_excerpt`
// without coalesce) ONLY for edges that don't already have a meaningful
// excerpt string.
// ---------------------------------------------------------------------

MATCH ()-[r]->()
WHERE r.evidence_origin IS NULL
WITH r,
     CASE type(r)
       // 'cell_citation | registry_stub | propagated | controlled_vocab' group
       WHEN 'BELEGT_IN'              THEN 'controlled_vocab'
       WHEN 'BETEILIGT_AN'           THEN 'controlled_vocab'
       WHEN 'ASSOZIIERT_MIT_PROJEKT' THEN 'registry_stub'
       WHEN 'AUS_BAUWERK'            THEN 'controlled_vocab'   // becomes FROM_DONOR in mig_4_2
       WHEN 'EINGEBAUT_IN'           THEN 'controlled_vocab'   // becomes INTO_RECEIVER in mig_4_2
       WHEN 'HAT_BAUTEILGRUPPE'      THEN 'controlled_vocab'
       WHEN 'HAT_HUERDE'             THEN 'controlled_vocab'
       WHEN 'HAT_AKTEURROLLE'        THEN 'controlled_vocab'
       // 'research_file_row | standards_body' group
       WHEN 'REFERENZIERT_NORM'      THEN 'standards_body'
       // everything else: controlled_vocab is the right default for
       // classification edges (entity → vocabulary node).
       ELSE 'controlled_vocab'
     END AS basis_default
SET r.evidence_origin     = 'derived',
    r.evidence_basis      = basis_default,
    r.evidence_source_id  = 'mig_4_1',
    r.evidence_confidence = 'unklar',
    r.evidence_excerpt    = CASE
      WHEN r.evidence_excerpt IS NULL THEN NULL
      WHEN toLower(r.evidence_excerpt) CONTAINS 'propagated from' THEN NULL
      ELSE r.evidence_excerpt
    END;

// Make sure every edge has an `evidence_excerpt` KEY (even if NULL) so
// queries can rely on the schema invariant.
MATCH ()-[r]->()
WHERE NOT 'evidence_excerpt' IN keys(r)
SET r.evidence_excerpt = NULL;

// ---------------------------------------------------------------------
// 4_1.e — BELEGT_IN.evidence_source_id backfill from destination Quelle id.
//          A BELEGT_IN edge cites the destination by construction, so
//          target.id IS the canonical source identifier.
// ---------------------------------------------------------------------

MATCH (a)-[r:BELEGT_IN]->(b:Quelle)
WHERE r.evidence_source_id IS NULL OR r.evidence_source_id = ''
SET r.evidence_source_id = b.id;

// ---------------------------------------------------------------------
// 4_1.f — Remap 'legacy_migration' basis on the 8 enumerated citation-
//          group types to per-relationship enum values.
// ---------------------------------------------------------------------

MATCH ()-[r:BELEGT_IN]->()
WHERE r.evidence_basis = 'legacy_migration'
SET r.evidence_basis = 'cell_citation';

MATCH ()-[r]->()
WHERE type(r) IN [
  'BETEILIGT_AN','ASSOZIIERT_MIT_PROJEKT',
  'AUS_BAUWERK','EINGEBAUT_IN',
  'HAT_BAUTEILGRUPPE','HAT_HUERDE','HAT_AKTEURROLLE'
]
AND r.evidence_basis = 'legacy_migration'
SET r.evidence_basis = 'controlled_vocab';

// ---------------------------------------------------------------------
// 4_1.g — REFERENZIERT_NORM basis must be in {research_file_row,
//          standards_body}. Existing non-enum values are remapped to
//          'standards_body'; the original value is captured on
//          derivation_note for traceability.
// ---------------------------------------------------------------------

MATCH ()-[r:REFERENZIERT_NORM]->()
WHERE NOT r.evidence_basis IN ['research_file_row','standards_body']
SET r.derivation_note = coalesce(r.derivation_note,
                                 'former_basis=' + r.evidence_basis),
    r.evidence_basis  = 'standards_body';

// ---------------------------------------------------------------------
// 4_1.h — HAT_HUERDE 'demoted_from_kette' (Phase-1.1 provenance) →
//          'propagated'. Original signal preserved on derivation_note.
//          Other rel types carrying the same basis are outside the
//          strict-enum group and keep the literal value.
// ---------------------------------------------------------------------

MATCH ()-[r:HAT_HUERDE]->()
WHERE r.evidence_basis = 'demoted_from_kette'
SET r.derivation_note = coalesce(r.derivation_note,
                                 'former_basis=demoted_from_kette'),
    r.evidence_basis  = 'propagated';

// ---------------------------------------------------------------------
// 4_1.d — Hard-rule audits — these MUST return 0; if any returns > 0
//         the runner aborts.
// ---------------------------------------------------------------------

// 1) curated requires excerpt
MATCH ()-[r]->()
WHERE r.evidence_origin = 'curated'
  AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt = '')
RETURN 'viol_curated_no_excerpt' AS rule, count(r) AS violations;

// 2) bookkeeping only with derived
MATCH ()-[r]->()
WHERE r.evidence_confidence = 'bookkeeping'
  AND coalesce(r.evidence_origin, '') <> 'derived'
RETURN 'viol_bk_not_derived' AS rule, count(r) AS violations;

// 3) excerpt may not contain 'propagated from'
MATCH ()-[r]->()
WHERE r.evidence_excerpt IS NOT NULL
  AND toLower(r.evidence_excerpt) CONTAINS 'propagated from'
RETURN 'viol_excerpt_propagated' AS rule, count(r) AS violations;

// 4) no silent NULLs on the five fields (excerpt may be NULL by design)
MATCH ()-[r]->()
WHERE r.evidence_origin     IS NULL
   OR r.evidence_basis      IS NULL
   OR r.evidence_source_id  IS NULL
   OR r.evidence_confidence IS NULL
RETURN 'viol_missing_field' AS rule, count(r) AS violations;

// 5) per-relationship enum compliance — citation group
MATCH ()-[r]->()
WHERE type(r) IN [
  'BELEGT_IN','BETEILIGT_AN','ASSOZIIERT_MIT_PROJEKT',
  'AUS_BAUWERK','FROM_DONOR','EINGEBAUT_IN','INTO_RECEIVER',
  'HAT_BAUTEILGRUPPE','HAT_HUERDE','HAT_AKTEURROLLE'
]
AND NOT r.evidence_basis IN ['cell_citation','registry_stub','propagated','controlled_vocab']
RETURN 'viol_citation_basis_enum' AS rule, count(r) AS violations;

// 6) per-relationship enum compliance — norm group
MATCH ()-[r]->()
WHERE type(r) IN ['REFERENZIERT_NORM','APPLIES_IN','APPLIES_TO']
  AND NOT r.evidence_basis IN ['research_file_row','standards_body']
RETURN 'viol_norm_basis_enum' AS rule, count(r) AS violations;
