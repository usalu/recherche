// =============================================================================
// mig_repair_1_2_anchor_regression.cypher
// Repair Phase 1.2 regression introduced after the original anchor relabel.
// Database: mit-bestand
//
// Scope:
//   - q_akteursliste_master_md only.
//   - Retype/delete regressed BELEGT_IN edges that point at ontology anchors.
//   - Merge the duplicate :Quelle shell into the surviving :OntologyAnchor.
//   - Preserve actor-registry source-as-link behavior by keeping ZITIERT_QUELLE
//     on the OntologyAnchor and deleting only duplicate shell copies.
//
// Audit prerequisite:
//   logs/repair_phase1_2_anchor_regression_audit.jsonl must be written before
//   this migration is executed.
// =============================================================================

// 1. Convert regressed BELEGT_IN edges to the canonical Phase 1.2 anchor shape.
// Existing ANCHORED_BY edges are reused so the repair does not duplicate the
// 199 already-canonical source->anchor relationships.
MATCH (n)-[r:BELEGT_IN]->(a:OntologyAnchor {id: 'q_akteursliste_master_md'})
MERGE (n)-[ab:ANCHORED_BY]->(a)
ON CREATE SET
    ab.evidence_origin = 'derived',
    ab.evidence_basis = 'controlled_vocab',
    ab.evidence_source_id = a.id,
    ab.evidence_confidence = 'bookkeeping'
DELETE r
RETURN count(*) AS belegt_in_to_anchor_removed;

// 2. Preserve outgoing actor URL citations from the duplicate shell on the
// real anchor. In the regressed live graph these are duplicate relationships;
// MERGE still protects any non-duplicate citation before the shell edge is
// removed.
MATCH (q:Quelle {id: 'q_akteursliste_master_md'})
MATCH (a:OntologyAnchor {id: 'q_akteursliste_master_md'})
MATCH (q)-[r:ZITIERT_QUELLE]->(target)
MERGE (a)-[zr:ZITIERT_QUELLE]->(target)
ON CREATE SET zr = properties(r)
DELETE r
RETURN count(*) AS duplicate_zitiert_quelle_removed;

// 3. Remove the duplicate shell's BELEGT_IN edges. Their source nodes were
// already handled in step 1; these shell edges only keep the duplicate :Quelle
// alive and would become invalid again if merged onto the OntologyAnchor.
MATCH (n)-[r:BELEGT_IN]->(q:Quelle {id: 'q_akteursliste_master_md'})
DELETE r
RETURN count(*) AS duplicate_shell_belegt_in_removed;

// 4. Delete the duplicate :Quelle shell only after all relationships have been
// removed. The surviving OntologyAnchor count remains unchanged.
MATCH (q:Quelle {id: 'q_akteursliste_master_md'})
WHERE NOT exists { (q)--() }
DELETE q
RETURN count(*) AS duplicate_quelle_deleted;
