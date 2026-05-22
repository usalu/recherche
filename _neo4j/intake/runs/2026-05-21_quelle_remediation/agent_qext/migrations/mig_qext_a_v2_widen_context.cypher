// ==========================================================================
// mig_qext_a_v2_widen_context.cypher
//
// Phase Q-EXT.A v2 — Refactored URL extraction with WIDER CONTEXT.
//
// Background. Local testing (test_c3_rule.py) showed C3 (excerpt-mention)
// matches only 0–10% of the time when evidence_excerpt is the original
// ±120-char window. Widening to the surrounding Markdown table row or
// paragraph pushes match rates to 24–95 %. This migration re-extracts
// the surrounding context from disk for every existing :ZITIERT_QUELLE
// edge that S1 / Q-EXT.A created, replacing the narrow evidence_excerpt
// with a wider one.
//
// IMPLEMENTATION: this Cypher is a TEMPLATE. The runner (qext_runner.py
// new sub-command 'rewiden') invokes it per-edge with parameters extracted
// from disk by re-parsing the source dossier/research-file.
//
// Parameters supplied by runner:
//   $edge_internal_id : the :ZITIERT_QUELLE edge id
//   $context          : the new wider context (table row OR paragraph)
//
// Idempotent. Re-running with the same context is a no-op.
// ==========================================================================

MATCH ()-[r:ZITIERT_QUELLE]->()
WHERE id(r) = $edge_internal_id
  AND r.migration_origin CONTAINS 'mig_qext_a_research_urls'
SET r.evidence_excerpt = $context,
    r.evidence_excerpt_v2 = true,           // marker: was widened
    r.evidence_excerpt_width = size($context),
    r.migration_origin = coalesce(r.migration_origin, '') + ' | mig_qext_a_v2_widen_context';

// ==========================================================================
// Audits
// ==========================================================================

// A1 — how many edges were widened
MATCH ()-[r:ZITIERT_QUELLE]->() WHERE r.evidence_excerpt_v2 = true
RETURN 'qext_a_v2_widened' AS check, count(r) AS c,
       avg(r.evidence_excerpt_width) AS avg_width,
       min(r.evidence_excerpt_width) AS min_width,
       max(r.evidence_excerpt_width) AS max_width;

// A2 — distribution of new context widths
MATCH ()-[r:ZITIERT_QUELLE]->() WHERE r.evidence_excerpt_v2 = true
WITH r.evidence_excerpt_width AS w,
     CASE
       WHEN r.evidence_excerpt_width < 200 THEN '0-200'
       WHEN r.evidence_excerpt_width < 500 THEN '200-500'
       WHEN r.evidence_excerpt_width < 1000 THEN '500-1000'
       WHEN r.evidence_excerpt_width < 2000 THEN '1000-2000'
       ELSE '2000+'
     END AS bin
RETURN bin, count(*) AS c
ORDER BY bin;
