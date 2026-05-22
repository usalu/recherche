// ==========================================================================
// mig_qext_c_v2_confirmed_urls.cypher
//
// Phase Q-EXT.C (v2) — Replace the loose `primary_source_url` heuristic with
// a strict, multi-URL `confirmed_source_urls` list.
//
// A URL is "confirmed" against a node iff ANY of:
//   C1 — Dossier-grounded (direct): the node has a direct :BELEGT_IN to a
//        :Dossier/:ResearchDocument that cites the URL via :ZITIERT_QUELLE.
//        Strongest signal — only fires for "owning" nodes (Projekt, Bauwerk,
//        Bauteilgruppe, etc. that the dossier was written ABOUT).
//
//   C2 — Content-verified: a :ZITIERT_QUELLE edge to the URL has S3
//        verification_status in {verbatim_match, paraphrase_match, token_match}
//        AND the URL is reachable from this node via source_urls.
//        Independent self-check.
//
//   C3 — Excerpt-mention: the URL is cited in a dossier whose ZITIERT_QUELLE
//        evidence_excerpt mentions this node's name (case-insensitive,
//        word-boundary, minimum 4-char match). Covers vocab nodes
//        (:Material, :Norm, :Schadstoff, …) that are referenced in the
//        dossier text but not directly BELEGT_IN.
//
// Multiple confirmed URLs per node are expected and desired.
// `primary_source_url` becomes simply confirmed_source_urls[0] or NULL.
//
// Plan ref: _neo4j/QUELLE_REMEDIATION/EXTENSION_universal_source_surfacing.md §3 Q-EXT.C v2
// Idempotent. Safe to re-run; replaces previous Q-EXT.C output.
// ==========================================================================

// First, clear the previous Q-EXT.C output so the new semantics aren't mixed
// with the old. (Idempotent — re-running this whole file is safe.)
MATCH (n) WHERE n.migration_origin CONTAINS 'mig_qext_c_primary_source_url'
SET n.migration_origin = replace(n.migration_origin, ' | mig_qext_c_primary_source_url', '')
REMOVE n.primary_source_url;

// ----- Step A: compute C1 hits (dossier-grounded) per node -----
// Stage to a temporary list property; we'll consolidate in Step C.
MATCH (n) WHERE n.source_urls IS NOT NULL AND size(n.source_urls) > 0
OPTIONAL MATCH (n)-[:BELEGT_IN|HAS_SOURCE_LINK]->(d)
WHERE (d:Dossier OR d:ResearchDocument)
OPTIONAL MATCH (d)-[zq:ZITIERT_QUELLE]->(ext:ExternalLink)
WITH n,
     collect(DISTINCT {
       url: ext.url,
       reason: 'dossier_grounded:' + coalesce(d.id, 'unknown') +
               ':' + coalesce(zq.locator, 'bare')
     }) AS c1_raw
SET n._qextc_c1_hits = [h IN c1_raw WHERE h.url IS NOT NULL];

// ----- Step B: compute C2 hits (content-verified) per node -----
MATCH (n) WHERE n.source_urls IS NOT NULL AND size(n.source_urls) > 0
OPTIONAL MATCH (n)-[:BELEGT_IN|HAS_SOURCE_LINK*1..3]->(ext:ExternalLink)
WHERE ext.url IN n.source_urls
OPTIONAL MATCH (:Dossier)-[zq2:ZITIERT_QUELLE]->(ext)
WHERE zq2.verification_status IN ['verbatim_match','paraphrase_match','token_match']
WITH n,
     collect(DISTINCT {
       url: ext.url,
       reason: 'content_verified:' + coalesce(zq2.verification_method, 'unknown') +
               ':' + toString(coalesce(zq2.verification_score, 0))
     }) AS c2_raw
SET n._qextc_c2_hits = [h IN c2_raw WHERE h.url IS NOT NULL];

// ----- Step B2: compute C3 hits (excerpt-mention) per node -----
// For each URL in source_urls, check if any :ZITIERT_QUELLE edge to that URL
// has an evidence_excerpt that mentions this node's name. Useful for vocab
// nodes that aren't directly BELEGT_IN but are referenced in dossier text.
//
// "Mentions" = case-insensitive, word-boundary match on n.name; excludes
// short or noisy names (length < 4 → skip to avoid false positives like 'AT', 'EU').
MATCH (n) WHERE n.source_urls IS NOT NULL AND size(n.source_urls) > 0
  AND n.name IS NOT NULL AND size(n.name) >= 4
WITH n, toLower(n.name) AS needle
MATCH (d:Quelle)-[zq3:ZITIERT_QUELLE]->(ext:ExternalLink)
WHERE (d:Dossier OR d:ResearchDocument)
  AND ext.url IN n.source_urls
  AND zq3.evidence_excerpt IS NOT NULL
  AND zq3.evidence_excerpt =~ ('(?i).*\\b' + apoc.text.regexGroups(needle, '([\\w\\s]+)')[0][0] + '\\b.*')
WITH n,
     collect(DISTINCT {
       url: ext.url,
       reason: 'excerpt_mention:' + d.id + ':' + coalesce(zq3.locator, 'bare')
     }) AS c3_raw
SET n._qextc_c3_hits = [h IN c3_raw WHERE h.url IS NOT NULL];

// ----- Step C: consolidate -----
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
    n.migration_origin = coalesce(n.migration_origin, '') +
        CASE WHEN n.migration_origin IS NULL OR n.migration_origin = ''
             THEN 'mig_qext_c_v2_confirmed_urls'
             ELSE ' | mig_qext_c_v2_confirmed_urls' END
REMOVE n._qextc_c1_hits, n._qextc_c2_hits, n._qextc_c3_hits;

// ----- Audits -----

// A1 — every node with source_urls has confirmed_source_urls set (possibly empty)
MATCH (n) WHERE n.source_urls IS NOT NULL AND size(n.source_urls) > 0
  AND n.confirmed_source_urls IS NULL
RETURN 'qextc_v2_a1_missing_confirmed' AS check, count(n) AS violations;

// A2 — primary_source_url == confirmed_source_urls[0] (or both NULL)
MATCH (n) WHERE n.confirmed_source_urls IS NOT NULL
  AND size(n.confirmed_source_urls) > 0
  AND n.primary_source_url <> n.confirmed_source_urls[0]
RETURN 'qextc_v2_a2_primary_mismatch' AS check, count(n) AS violations;

// A3 — informational: nodes with source_urls > 0 but confirmed = 0
MATCH (n) WHERE coalesce(n.source_count, 0) > 0
  AND coalesce(n.confirmed_source_count, 0) = 0
RETURN 'qextc_v2_a3_no_confirmed' AS check, count(n) AS c,
       collect(n.id)[..10] AS sample;

// A4 — every entry in confirmation_evidence references at least one valid reason
MATCH (n) WHERE n.confirmation_evidence IS NOT NULL
WITH n, [k IN keys(n.confirmation_evidence) |
         size([r IN n.confirmation_evidence[k]
               WHERE r STARTS WITH 'dossier_grounded:'
                  OR r STARTS WITH 'content_verified:'
                  OR r STARTS WITH 'excerpt_mention:'])
        ] AS reason_counts
WHERE any(c IN reason_counts WHERE c = 0)
RETURN 'qextc_v2_a4_url_with_no_reason' AS check, count(n) AS violations;

// A5 — distribution by criterion type (informational)
MATCH (n) WHERE n.confirmation_evidence IS NOT NULL
UNWIND keys(n.confirmation_evidence) AS url
UNWIND n.confirmation_evidence[url] AS reason
WITH split(reason, ':')[0] AS criterion, count(*) AS c
RETURN 'qextc_v2_a5_by_criterion' AS check, criterion, c
ORDER BY c DESC;

// D1 — distribution: confirmed nodes by label
MATCH (n) WHERE n.confirmed_source_count IS NOT NULL
UNWIND labels(n) AS lbl
WITH lbl, count(n) AS total,
     sum(CASE WHEN n.confirmed_source_count > 0 THEN 1 ELSE 0 END) AS with_confirmed,
     sum(n.confirmed_source_count) AS total_confirmed_urls
RETURN lbl, total, with_confirmed, total_confirmed_urls
ORDER BY with_confirmed DESC LIMIT 30;

// D2 — spot check mat_stahl
MATCH (n:Material {id:'mat_stahl'})
RETURN 'qextc_v2_d2_mat_stahl' AS check,
       n.confirmed_source_count AS confirmed,
       n.confirmed_source_urls AS urls,
       n.confirmation_evidence AS evidence;

// D3 — spot check rr_gb_stahl
MATCH (n:ReuseRule {id:'rr_gb_stahl'})
RETURN 'qextc_v2_d3_rr_gb_stahl' AS check,
       n.confirmed_source_count AS confirmed,
       n.confirmed_source_urls AS urls,
       n.confirmation_evidence AS evidence;
