// =========================================================================
// Migration 4c.1 — Unfold :Quelle.external_sources arrays into
// :ZITIERT_QUELLE links + child :Quelle nodes.
//
// Status @ Agent 8 (2026-05-20): NO-OP on the live graph.
//   Already executed during Phase 2.7.b by Agent 6:
//     - 60 source :Quelle migrated
//     - 270 :ZITIERT_QUELLE edges created (evidence_basis='external_sources_array')
//     - 264 net new target :Quelle nodes (quelltyp='external_link')
//     - 0 :Quelle now retain `external_sources`
//   Forensic journal: deleted/phase2_7_external_sources.jsonl
//
// This migration is the canonical, idempotent form of that work. It is
// safe to re-run; the live count of `:Quelle.external_sources IS NOT NULL`
// must be 0 after every run.
//
// Plan reference: §4c.1 / §2.7.b.
// =========================================================================

// --- Sanity precheck (must return 0 BEFORE and AFTER) -------------------
MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL
RETURN count(q) AS quelle_with_external_sources_remaining;

// --- Canonical unfold pattern (parameterised per source :Quelle) --------
//
// Driver-side: for every :Quelle q where q.external_sources is non-null,
// for every raw citation string in that array, extract the first URL,
// build a stable target id (q_ext_<host>__<path>), MERGE the target
// :Quelle, and MERGE the (q)-[:ZITIERT_QUELLE]->(target) edge with the
// canonical 5-field evidence shape.
//
// :params {
//   target_id: 'q_ext_<slug>',
//   url:       'https://…',
//   title:     '<de-cited title>',
//   src_id:    '<source quelle id>',
//   raw:       '<original raw string>'
// }
//
// Cypher (one transaction per (source, raw_entry)):
//
//   MERGE (target:Quelle {id: $target_id})
//   ON CREATE SET target.url          = $url,
//                 target.quelltyp     = 'external_link',
//                 target.name         = $title,
//                 target.source_scope = 'mig_4c_1_external_sources',
//                 target._created_by  = 'mig_4c_1'
//   WITH target
//   MATCH (src:Quelle {id: $src_id})
//   MERGE (src)-[r:ZITIERT_QUELLE]->(target)
//   ON CREATE SET r.evidence_origin     = 'derived',
//                 r.evidence_basis      = 'external_sources_array',
//                 r.evidence_source_id  = 'mig_4c_1',
//                 r.evidence_confidence = 'unklar',
//                 r.evidence_excerpt    = $raw;
//
// After all entries for a given source :Quelle are migrated, REMOVE the
// `external_sources` property from the source node:
//
//   MATCH (src:Quelle {id: $src_id}) REMOVE src.external_sources;

// --- Acceptance checks ---------------------------------------------------
// (1) No source :Quelle retains the legacy array:
MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL
RETURN count(q) AS must_be_zero;

// (2) ZITIERT_QUELLE evidence_basis distribution (after the migration:
//     'external_sources_array' must be >= 269 from Phase 2.7.b / 4c.1):
MATCH ()-[r:ZITIERT_QUELLE]->()
RETURN coalesce(r.evidence_basis, '<null>') AS basis, count(r) AS c
ORDER BY c DESC;

// (3) Total :Quelle nodes with quelltyp='external_link' (target nodes
//     created by this migration; must be >= 264 after Agent-6 run):
MATCH (q:Quelle) WHERE q.quelltyp = 'external_link'
RETURN count(q) AS external_link_quelle_total;
