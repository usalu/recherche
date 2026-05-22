// ==========================================================================
// mig_qext_c_v4_confirmed_urls.cypher
//
// Phase Q-EXT.C (v4) — Cross-confirmed source URLs.
//
// v4 replaces the previous criteria as follows:
//   C1 (kept)   — direct dossier-grounded edge
//   C2 (kept)   — S3 content-verified
//   C3 (DROPPED) — dossier-side-only mention (proven unreliable)
//   C4 (NEW)    — cross-confirmed: BOTH dossier-text AND page-body mention
//                 the node's term(s). The runner pre-computes this list
//                 (it needs to read disk-cached page bodies + parse text).
//
// The runner (qext_runner.run_confirm4) does the term-matching against
// both the dossier .md and the cached HTML/PDF body, then passes the
// resulting list to this migration as $node_results.
//
// Plan ref: _neo4j/QUELLE_REMEDIATION/REFACTOR_v4_decision.md
// Idempotent. Replaces v1/v2/v3 output on re-run.
// ==========================================================================

// ----- Step 0 — clear stale output from prior versions -----------------
MATCH (n) WHERE n.migration_origin CONTAINS 'mig_qext_c_v2_confirmed_urls'
   OR n.migration_origin CONTAINS 'mig_qext_c_v3_confirmed_urls'
   OR n.migration_origin CONTAINS 'mig_qext_c_primary_source_url'
REMOVE n.confirmed_source_urls, n.confirmed_source_count,
       n.confirmation_evidence, n.confirmed_urls_updated_at,
       n.primary_source_url;
// `source_urls` from Q-EXT.B is preserved as the broad candidate set.

// ----- Step 1 — write per-node confirmed sets (runner-supplied) -------
//
// Expected $node_results shape (list of maps):
//   { node_id, confirmed_urls, evidence }
//
// where evidence is a map: { url -> [reason_string, ...] }
// reasons use the v4 prefixes:
//   'c1_dossier_grounded:<dossier_id>:<sref>'
//   'c2_content_verified:<method>:<score>'
//   'c4_cross_confirmed:<dossier_id>:<d_term_or_none>:<p_term_or_none>'
//
// Runner passes the full pre-computed list in chunks of 100–200.

UNWIND $node_results AS row
MATCH (n {id: row.node_id})
SET n.confirmed_source_urls   = row.confirmed_urls,
    n.confirmed_source_count  = size(row.confirmed_urls),
    n.confirmation_evidence   = row.evidence,
    n.primary_source_url      = CASE WHEN size(row.confirmed_urls) > 0
                                     THEN row.confirmed_urls[0] ELSE NULL END,
    n.confirmed_urls_updated_at = date(),
    n.migration_origin = coalesce(n.migration_origin, '') +
        CASE WHEN n.migration_origin IS NULL OR n.migration_origin = ''
             THEN 'mig_qext_c_v4_cross_confirmed'
             ELSE ' | mig_qext_c_v4_cross_confirmed' END;

// ----- Audits ----------------------------------------------------------

// A1 — every node we wrote has a non-null confirmed_source_urls field
//      (it may be empty list — that's the honest signal)
MATCH (n) WHERE n.migration_origin CONTAINS 'mig_qext_c_v4_cross_confirmed'
  AND n.confirmed_source_urls IS NULL
RETURN 'qextc_v4_a1_missing_confirmed' AS check, count(n) AS violations;

// A2 — primary_source_url equals confirmed_source_urls[0] when present
MATCH (n)
WHERE n.confirmed_source_urls IS NOT NULL
  AND size(n.confirmed_source_urls) > 0
  AND n.primary_source_url <> n.confirmed_source_urls[0]
RETURN 'qextc_v4_a2_primary_mismatch' AS check, count(n) AS violations;

// A3 — distribution by reason prefix
MATCH (n) WHERE n.confirmation_evidence IS NOT NULL
UNWIND keys(n.confirmation_evidence) AS url
UNWIND n.confirmation_evidence[url] AS reason
RETURN split(reason, ':')[0] AS criterion, count(*) AS c
ORDER BY c DESC;

// A4 — per-label coverage
MATCH (n) WHERE n.confirmed_source_count IS NOT NULL
UNWIND labels(n) AS lbl
WITH lbl, count(n) AS total,
     sum(CASE WHEN n.confirmed_source_count > 0 THEN 1 ELSE 0 END) AS with_confirmed
RETURN lbl, total, with_confirmed,
       round(100.0 * with_confirmed / total, 1) AS pct_confirmed
ORDER BY pct_confirmed DESC, with_confirmed DESC LIMIT 30;

// A5 — spot checks for the test fixtures
MATCH (n:Material {id: 'mat_stahl'})
RETURN 'qextc_v4_spot_mat_stahl' AS check,
       n.confirmed_source_count AS confirmed,
       size(coalesce(n.source_urls, [])) AS broad,
       n.confirmed_source_urls AS urls;

MATCH (n:Projekt {id: 'p_holbein_gardens_london'})
RETURN 'qextc_v4_spot_holbein' AS check,
       n.confirmed_source_count AS confirmed,
       size(coalesce(n.source_urls, [])) AS broad,
       n.primary_source_url AS primary;

MATCH (n:Akteur) WHERE n.id CONTAINS 'rotor'
RETURN 'qextc_v4_spot_rotor' AS check, n.id,
       n.confirmed_source_count AS confirmed,
       n.primary_source_url AS primary;
