// =============================================================================
// mig_1_2_anchor_relabel.cypher
// Phase 1.2 — Ontology anchors: relabel + retype BELEGT_IN to ANCHORED_BY
// Author: Agent 3 (Wave 1)
// Plan ref: c:/Users/Kinosh/.cursor/plans/radical_quality-first_reset_8d1e2b66.plan.md
//           section 1.2
// Database: mit-bestand
//
// Pre-migration verified counts (snapshot 2026-05-20T20:42 + live re-check):
//   - q_controlled_vocab_seed   : :Quelle, 457 incoming BELEGT_IN
//   - q_akteursliste_master_md  : :Quelle, 259 incoming BELEGT_IN; plus
//                                 ZITIERT_QUELLE edges (untouched on purpose)
//   - 21 deg-0 :Quelle nodes (full ID list in deleted/phase1_2_quelle.jsonl)
//
// Expected effects:
//   1.2.a  2 :Quelle relabelled to :OntologyAnchor (label-only change)
//   1.2.b  716 BELEGT_IN re-typed to 716 ANCHORED_BY (net edge delta 0)
//   1.2.c  21 deg-0 :Quelle hard-deleted (archived to deleted/phase1_2_quelle.jsonl
//          BEFORE this migration runs)
// =============================================================================

// -----------------------------------------------------------------------------
// 1.2.a  Relabel the two ontology anchors from :Quelle to :OntologyAnchor.
// Rationale: both nodes carry bookkeeping degree (457 + 259 incoming BELEGT_IN);
// they dominate citation queries today. Removing :Quelle stops them flattening
// real external evidence.
// -----------------------------------------------------------------------------
MATCH (q:Quelle)
WHERE q.id IN ['q_controlled_vocab_seed', 'q_akteursliste_master_md']
REMOVE q:Quelle
SET q:OntologyAnchor
RETURN q.id AS relabelled_id, labels(q) AS new_labels;

// -----------------------------------------------------------------------------
// 1.2.b  Retype every BELEGT_IN edge that lands on an :OntologyAnchor to
// :ANCHORED_BY with the canonical evidence shape:
//   evidence_origin     = 'derived'
//   evidence_basis      = 'controlled_vocab'
//   evidence_excerpt    = NULL
//   evidence_source_id  = <anchor id>      (back-pointer for audits)
//   evidence_confidence = 'bookkeeping'
// The original BELEGT_IN edge properties (id/source/evidence/datenqualitaet/
// source_scope) are dropped on retype — they are preserved in
// snapshot/relationships.jsonl and this migration file itself for forensic
// audit.
// -----------------------------------------------------------------------------
MATCH (n)-[r:BELEGT_IN]->(a:OntologyAnchor)
CREATE (n)-[r2:ANCHORED_BY]->(a)
SET r2 = {
    evidence_origin:     'derived',
    evidence_basis:      'controlled_vocab',
    evidence_excerpt:    NULL,
    evidence_source_id:  a.id,
    evidence_confidence: 'bookkeeping'
}
DELETE r
RETURN count(*) AS belegt_in_to_anchored_by;

// -----------------------------------------------------------------------------
// 1.2.c  Hard-delete the 21 deg-0 :Quelle nodes that were archived in
// deleted/phase1_2_quelle.jsonl. Belt-and-braces guard: delete only nodes that
// are truly isolated (no incoming AND no outgoing edges).
// -----------------------------------------------------------------------------
MATCH (q:Quelle)
WHERE NOT exists { (q)<-[]-() } AND NOT exists { (q)-[]->() }
WITH q, q.id AS deleted_id
DELETE q
RETURN count(*) AS quelle_deleted, collect(deleted_id) AS deleted_ids;
