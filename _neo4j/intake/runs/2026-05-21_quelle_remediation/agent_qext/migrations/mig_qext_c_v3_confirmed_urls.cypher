// ==========================================================================
// mig_qext_c_v3_confirmed_urls.cypher
//
// Phase Q-EXT.C (v3) — Confirmed-URL computation with refactored C3.
//
// Changes from v2:
//   1. C3 (excerpt-mention) accepts MULTIPLE search terms per node, supplied
//      by the runner as a per-node list of pre-expanded terms (name +
//      aliases + German↔English synonyms + id-stem).
//   2. The Cypher regex properly escapes special chars in the needle
//      (the v2 bug: apoc.text.regexGroups(needle, '([\\w\\s]+)')[0][0]
//      truncated 'CEN/TS 1090-201' to 'cen' — fixed here).
//   3. Each match records which TERM matched, not just which dossier, so
//      the user can see why ("matched via 'steel' synonym for 'Stahl'").
//   4. Body widened from ±120 chars to full table-row/paragraph by
//      mig_qext_a_v2 first; this migration assumes it has been run.
//
// Validation: local test (test_c3_refactored.py) against real research
// files showed match rates rising from 0–10 % (v2) to 24–95 % (v3) for
// the same node names.
//
// Idempotent. Replaces v2 output on re-run.
//
// RUNNER CONTRACT.
//   The driver runs this twice — once with $phase='compute' (writes the
//   confirmed sets), once with $phase='audit' (returns the distribution).
//   The driver supplies $node_search_terms as:
//       [ {node_id: 'mat_stahl',
//          terms: ['stahl', 'steel'],
//          name: 'Stahl'}, ... ]
//   This avoids putting the synonym map inside Cypher (cleaner, editable).
// ==========================================================================

// ----- Step 0 — clear previous confirmation output --------------------
MATCH (n) WHERE n.migration_origin CONTAINS 'mig_qext_c_v2_confirmed_urls'
   OR n.migration_origin CONTAINS 'mig_qext_c_primary_source_url'
REMOVE n.confirmed_source_urls, n.confirmed_source_count,
       n.confirmation_evidence, n.confirmed_urls_updated_at,
       n.primary_source_url;
// Note: keeps source_urls (from Q-EXT.B) and source_count untouched.

// ----- Step A — C1 (dossier-grounded direct) --------------------------
UNWIND $node_search_terms AS row
MATCH (n {id: row.node_id}) WHERE n.source_urls IS NOT NULL AND size(n.source_urls) > 0
OPTIONAL MATCH (n)-[:BELEGT_IN|HAS_SOURCE_LINK]->(d)
WHERE (d:Dossier OR d:ResearchDocument)
OPTIONAL MATCH (d)-[zq:ZITIERT_QUELLE]->(ext:ExternalLink)
WITH n, row,
     collect(DISTINCT {
       url: ext.url,
       reason: 'dossier_grounded:' + coalesce(d.id, 'unknown') +
               ':' + coalesce(zq.locator, 'bare')
     }) AS c1_raw
SET n._qextc_c1_hits = [h IN c1_raw WHERE h.url IS NOT NULL];

// ----- Step B — C2 (content-verified) ---------------------------------
UNWIND $node_search_terms AS row
MATCH (n {id: row.node_id}) WHERE n.source_urls IS NOT NULL AND size(n.source_urls) > 0
OPTIONAL MATCH (n)-[:BELEGT_IN|HAS_SOURCE_LINK*1..3]->(ext:ExternalLink)
WHERE ext.url IN n.source_urls
OPTIONAL MATCH (:Dossier)-[zq2:ZITIERT_QUELLE]->(ext)
WHERE zq2.verification_status IN ['verbatim_match','paraphrase_match','token_match']
WITH n, row,
     collect(DISTINCT {
       url: ext.url,
       reason: 'content_verified:' + coalesce(zq2.verification_method, 'unknown') +
               ':' + toString(coalesce(zq2.verification_score, 0))
     }) AS c2_raw
SET n._qextc_c2_hits = [h IN c2_raw WHERE h.url IS NOT NULL];

// ----- Step B2 — C3 (excerpt-mention, multi-term) --------------------
// For each (node, term) pair, find :ZITIERT_QUELLE whose evidence_excerpt
// matches term as a word. The match uses Cypher's =~ regex with proper
// escape — the runner pre-escapes the term and we just embed it.
UNWIND $node_search_terms AS row
UNWIND row.terms AS term
WITH row, term WHERE term IS NOT NULL AND size(term) >= 4
MATCH (n {id: row.node_id}) WHERE n.source_urls IS NOT NULL AND size(n.source_urls) > 0
MATCH (d:Quelle)-[zq3:ZITIERT_QUELLE]->(ext:ExternalLink)
WHERE (d:Dossier OR d:ResearchDocument)
  AND ext.url IN n.source_urls
  AND zq3.evidence_excerpt IS NOT NULL
  AND zq3.evidence_excerpt =~ ('(?i).*\\b' +
        apoc.text.regreplace(term, '([.\\^$*+?()\\[\\]{}|\\\\/-])', '\\\\$1') +
        '\\b.*')
WITH n, row,
     collect(DISTINCT {
       url: ext.url,
       reason: 'excerpt_mention:' + coalesce(d.id, 'unknown') +
               ':via_term:' + term
     }) AS c3_raw
SET n._qextc_c3_hits = coalesce(n._qextc_c3_hits, []) +
                       [h IN c3_raw WHERE h.url IS NOT NULL];

// ----- Step C — consolidate ------------------------------------------
MATCH (n) WHERE n._qextc_c1_hits IS NOT NULL
   OR n._qextc_c2_hits IS NOT NULL
   OR n._qextc_c3_hits IS NOT NULL
WITH n,
     coalesce(n._qextc_c1_hits, [])
   + coalesce(n._qextc_c2_hits, [])
   + coalesce(n._qextc_c3_hits, []) AS hits
WITH n, hits,
     apoc.coll.toSet([h IN hits | h.url]) AS confirmed_urls,
     apoc.map.groupBy(hits, 'url') AS grouped
WITH n, confirmed_urls, grouped,
     apoc.map.fromPairs(
       [u IN confirmed_urls | [u,
         apoc.coll.toSet([g IN coalesce(grouped[u], []) | g.reason])
       ]]
     ) AS evidence
SET n.confirmed_source_urls   = confirmed_urls,
    n.confirmed_source_count  = size(confirmed_urls),
    n.confirmation_evidence   = evidence,
    n.primary_source_url      = CASE WHEN size(confirmed_urls) > 0
                                     THEN confirmed_urls[0] ELSE NULL END,
    n.confirmed_urls_updated_at = date(),
    n.migration_origin = coalesce(n.migration_origin, '') + ' | mig_qext_c_v3_confirmed_urls'
REMOVE n._qextc_c1_hits, n._qextc_c2_hits, n._qextc_c3_hits;

// ----- Audits --------------------------------------------------------

// A1 — coverage: nodes with confirmed_source_urls > 0 per label
MATCH (n) WHERE n.confirmed_source_urls IS NOT NULL
UNWIND labels(n) AS lbl
WITH lbl, count(n) AS total_in_label,
     sum(CASE WHEN size(coalesce(n.confirmed_source_urls, [])) > 0 THEN 1 ELSE 0 END) AS with_confirmed
RETURN lbl, total_in_label, with_confirmed,
       round(100.0 * with_confirmed / total_in_label, 1) AS pct_confirmed
ORDER BY pct_confirmed DESC, with_confirmed DESC LIMIT 30;

// A2 — criterion distribution
MATCH (n) WHERE n.confirmation_evidence IS NOT NULL
UNWIND keys(n.confirmation_evidence) AS url
UNWIND n.confirmation_evidence[url] AS reason
RETURN split(reason, ':')[0] AS criterion, count(*) AS c
ORDER BY c DESC;

// A3 — spot checks for the test cases
MATCH (n:Material {id: 'mat_stahl'})
RETURN 'qext_c_v3_spot_mat_stahl' AS check,
       n.confirmed_source_count AS confirmed,
       n.primary_source_url AS primary,
       size(n.source_urls) AS broad,
       n.confirmed_source_urls AS confirmed_urls;

MATCH (n:Material {id: 'mat_holz'})
RETURN 'qext_c_v3_spot_mat_holz' AS check,
       n.confirmed_source_count AS confirmed,
       n.primary_source_url AS primary,
       size(n.source_urls) AS broad;

MATCH (n:Schadstoff {id: 's_asbest'})
RETURN 'qext_c_v3_spot_s_asbest' AS check,
       n.confirmed_source_count AS confirmed,
       n.primary_source_url AS primary,
       size(n.source_urls) AS broad;

MATCH (n:Norm) WHERE n.id CONTAINS 'cen_ts_1090'
RETURN 'qext_c_v3_spot_norm_cen_ts' AS check, n.id,
       n.confirmed_source_count AS confirmed,
       n.primary_source_url AS primary;
