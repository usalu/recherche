// =========================================================================
// Migration 4c — Edge property strip:
//
//   "Hard rule after migration: no relationship may have a property whose
//    name contains `url`, `http`, `source_file`, or `external_sources`.
//    URLs exist only on :Quelle.url."   (plan §2.7 / §4c)
//
// Status @ Agent 8 (2026-05-20): NO-OP on the live graph.
//   Already executed across waves 1-2 (notably Phase 2.7.d by Agent 6,
//   which canonicalised 4 948 polluted edges into the 5-field evidence
//   shape and removed legacy `source` / `evidence` / `source_excerpt`
//   / `datenqualitaet` keys). Agent 8 verified the live graph and found
//   0 relationships with a key whose name contains url / http /
//   source_file / external_sources, and 0 distinct illegal key names.
//
// This script is the canonical, idempotent enforcement of the rule.
// =========================================================================

// --- Distinct illegal rel key audit (must return zero rows) -------------
MATCH ()-[r]->()
UNWIND keys(r) AS k
WITH DISTINCT k
WHERE toLower(k) CONTAINS 'url'
   OR toLower(k) CONTAINS 'http'
   OR toLower(k) CONTAINS 'source_file'
   OR toLower(k) CONTAINS 'external_sources'
RETURN k;

// --- Count of polluted edges (must return 0) ----------------------------
MATCH ()-[r]->()
WITH r, [k IN keys(r) WHERE toLower(k) CONTAINS 'url'
         OR toLower(k) CONTAINS 'http'
         OR toLower(k) CONTAINS 'source_file'
         OR toLower(k) CONTAINS 'external_sources'] AS bad
WHERE size(bad) > 0
RETURN count(r) AS polluted_edges_remaining;

// --- Canonical strip (parameterised by illegal key name) ----------------
//
// If a future run reintroduces any illegal key, the runner should iterate
// over the distinct-keys audit above and execute this pattern per key:
//
//   MATCH ()-[r]->() WHERE r[$k] IS NOT NULL
//   CALL apoc.create.removeRelProperties(r, [$k]) YIELD rel
//   RETURN count(rel) AS edges_stripped;
//
// All stripped values must first be journalled to
// `deleted/phase4c_edge_strip.jsonl` for reversibility.
