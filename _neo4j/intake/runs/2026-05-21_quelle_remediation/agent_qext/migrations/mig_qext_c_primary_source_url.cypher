// ==========================================================================
// mig_qext_c_primary_source_url.cypher
//
// Phase Q-EXT.C — Pick the single best URL per node and set as
// :NodeLabel.primary_source_url.
//
// Priority (per EXTENSION_universal_source_surfacing.md §3):
//   1. The node's own .url / .website / .homepage (already-known)
//   2. The :ExternalLink with url_status='reachable_2xx' AND
//      verbatim_match verification (highest trust)
//   3. ... paraphrase_match
//   4. Any reachable_2xx URL
//   5. First URL in source_urls
//
// Idempotent. Re-running picks the same URL (deterministic ORDER BY).
// ==========================================================================

// Skip nodes already carrying primary_source_url from a prior run if their
// source_urls hasn't changed.
MATCH (n)
WHERE n.source_urls IS NOT NULL AND size(n.source_urls) > 0

// Step 1: prefer the node's own url-bearing property if present
WITH n, coalesce(n.url, n.website, n.homepage) AS own_url

// Step 2: find candidate ExternalLink nodes, ranked
OPTIONAL MATCH (n)-[:BELEGT_IN|HAS_SOURCE_LINK|ZITIERT_QUELLE*1..3]->(ext:ExternalLink)
WHERE ext.url IN n.source_urls

WITH n, own_url, ext,
     CASE coalesce(ext.url_status, 'unchecked')
       WHEN 'reachable_2xx' THEN 0
       WHEN 'reachable_3xx_to_4xx' THEN 1
       ELSE 2
     END AS reach_rank,
     CASE
       WHEN exists{(:Dossier)-[zq:ZITIERT_QUELLE {verification_status:'verbatim_match'}]->(ext)}
         THEN 0
       WHEN exists{(:Dossier)-[zq:ZITIERT_QUELLE {verification_status:'paraphrase_match'}]->(ext)}
         THEN 1
       WHEN exists{(:Dossier)-[zq:ZITIERT_QUELLE {verification_status:'token_match'}]->(ext)}
         THEN 2
       ELSE 3
     END AS verify_rank

ORDER BY reach_rank, verify_rank, ext.url
WITH n, own_url, collect(ext.url) AS ranked_urls

// Set primary_source_url with the priority chain
SET n.primary_source_url = coalesce(
      own_url,
      head([u IN ranked_urls WHERE u IS NOT NULL]),
      n.source_urls[0]
    ),
    n.migration_origin = coalesce(n.migration_origin, '') +
      CASE WHEN n.migration_origin IS NULL OR n.migration_origin = ''
           THEN 'mig_qext_c_primary_source_url'
           ELSE ' | mig_qext_c_primary_source_url' END;

// ==========================================================================
// Audits
// ==========================================================================

// QEXT-C.A1 — Every node with source_urls > 0 has primary_source_url
MATCH (n) WHERE n.source_urls IS NOT NULL AND size(n.source_urls) > 0
  AND n.primary_source_url IS NULL
RETURN 'qext_c_a1_missing_primary' AS check, count(n) AS violations,
       collect(n.id)[..10] AS sample;

// QEXT-C.A2 — primary_source_url must be in source_urls
MATCH (n) WHERE n.primary_source_url IS NOT NULL
  AND NOT n.primary_source_url IN coalesce(n.source_urls, [])
  AND n.primary_source_url <> coalesce(n.url, '')
  AND n.primary_source_url <> coalesce(n.website, '')
  AND n.primary_source_url <> coalesce(n.homepage, '')
RETURN 'qext_c_a2_primary_not_in_source_urls' AS check, count(n) AS violations,
       collect({id: n.id, primary: n.primary_source_url})[..10] AS sample;

// QEXT-C.D1 — Distribution: how many nodes per label have primary_source_url
MATCH (n) WHERE n.primary_source_url IS NOT NULL
UNWIND labels(n) AS lbl
RETURN lbl, count(n) AS nodes_with_primary
ORDER BY nodes_with_primary DESC LIMIT 30;

// QEXT-C.S1 — Spot check: Material mat_stahl
MATCH (n:Material {id: 'mat_stahl'})
RETURN 'qext_c_s1_mat_stahl' AS check,
       n.primary_source_url AS primary,
       n.source_count AS total_sources;

// QEXT-C.S2 — Spot check: ReuseRule (should pick the SCI / EN document)
MATCH (n:ReuseRule {id: 'rr_gb_stahl'})
RETURN 'qext_c_s2_rr_gb_stahl' AS check,
       n.primary_source_url AS primary,
       n.source_count AS total_sources;
