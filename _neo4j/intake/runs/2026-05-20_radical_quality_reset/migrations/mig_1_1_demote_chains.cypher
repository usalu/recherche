// Migration 1.1 — Wiederverwendungskette: demote-not-delete
// Plan section 1.1, Agent 2, Wave 1, Phase 1.1
// DB: mit-bestand
//
// Goal:
//   - Keep the 14 :Wiederverwendungskette nodes that have BOTH outgoing
//     :AUS_BAUWERK and outgoing :EINGEBAUT_IN edges.
//   - Demote the 98 unwired chains: copy their outgoing
//     HAT_STATUS / HAT_WIEDERVERWENDUNGSART / HAT_HUERDE / HAT_LOGISTIK /
//     HAT_PROZESSPHASE / HAT_METHODE payload onto every connected
//     :Bauteilgruppe (via :TEIL_VON_KETTE), stamp provenance, then DETACH
//     DELETE the 98 chains.
//
// Provenance shape applied to every newly created edge on :Bauteilgruppe:
//   migration_origin     = 'mig_1_1_demote_chains'
//   evidence_basis       = 'demoted_from_kette'
//   evidence_origin      = 'derived'
//   evidence_source_id   = <chain.id>
//   evidence_confidence  = coalesce(r.evidence_confidence, 'unklar')
//   demoted_at           = <ISO timestamp>
//
// This file documents the canonical migration. The actual writes are
// executed by `logs/run_mig_1_1.py` which wraps the same statements in a
// single transaction and writes a pre-delete snapshot to
// `deleted/phase1_1_chains.jsonl`.
//
// ---------------------------------------------------------------------------

// 1.1.0 SANITY — log counts before any writes
MATCH (k:Wiederverwendungskette)
WITH count(k) AS chains_before
MATCH (k:Wiederverwendungskette)
WHERE NOT (exists{(k)-[:AUS_BAUWERK]->()} AND exists{(k)-[:EINGEBAUT_IN]->()})
RETURN chains_before, count(k) AS chains_unwired;
// expected: chains_before=112, chains_unwired=98

// 1.1.a Identify the 98 unwired chains
MATCH (k:Wiederverwendungskette)
WHERE NOT (exists{(k)-[:AUS_BAUWERK]->()} AND exists{(k)-[:EINGEBAUT_IN]->()})
RETURN count(k) AS unwired_chains;
// expected: 98

// 1.1.b For each unwired chain, demote its outgoing HAT_* payload onto every
//        :Bauteilgruppe that points at it via :TEIL_VON_KETTE.
//        Uses apoc.merge.relationship to fold duplicates and apoc.create.relationship
//        is intentionally avoided (we want idempotent type-aware merging).
MATCH (bg:Bauteilgruppe)-[:TEIL_VON_KETTE]->(k:Wiederverwendungskette)
WHERE NOT (exists{(k)-[:AUS_BAUWERK]->()} AND exists{(k)-[:EINGEBAUT_IN]->()})
MATCH (k)-[r:HAT_STATUS|HAT_WIEDERVERWENDUNGSART|HAT_HUERDE|HAT_LOGISTIK|HAT_PROZESSPHASE|HAT_METHODE]->(target)
WITH bg, k, r, target,
     {
       migration_origin:     'mig_1_1_demote_chains',
       evidence_basis:       'demoted_from_kette',
       evidence_origin:      'derived',
       evidence_source_id:   k.id,
       evidence_confidence:  coalesce(r.evidence_confidence, 'unklar'),
       demoted_at:           datetime()
     } AS shape
CALL apoc.merge.relationship(bg, type(r), {evidence_source_id: k.id}, shape, target, shape) YIELD rel
RETURN type(rel) AS rel_type, count(rel) AS edges_demoted;
// expected: ~57 demoted (HAT_PROZESSPHASE 23, HAT_METHODE 12, HAT_LOGISTIK 11, HAT_HUERDE 11)
// Note: actual BG×payload fan-out is larger (~311 BG inflows × 0.18 avg payload) but
// apoc.merge.relationship folds duplicates when (bg, type, k.id) match.

// 1.1.c Detach-delete the 98 unwired chains
MATCH (k:Wiederverwendungskette)
WHERE NOT (exists{(k)-[:AUS_BAUWERK]->()} AND exists{(k)-[:EINGEBAUT_IN]->()})
WITH k, k.id AS deleted_id
DETACH DELETE k
RETURN count(deleted_id) AS chains_deleted;
// expected: 98

// 1.1.d Acceptance — 14 fully wired chains remain
MATCH (k:Wiederverwendungskette)
RETURN count(k) AS chains_after,
       sum(CASE WHEN exists{(k)-[:AUS_BAUWERK]->()} AND exists{(k)-[:EINGEBAUT_IN]->()}
                THEN 1 ELSE 0 END) AS chains_wired_after;
// expected: chains_after=14, chains_wired_after=14
