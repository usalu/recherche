// ==========================================================================
// mig_r7_a_dual_naming_merge
// Reconcile 16 qu_*_dossier nodes into their q_<slug>_md counterparts.
// The actual APOC merge is driven pair-by-pair in agent_5_runner.py.
// This file contains the post-merge audit queries only.
// Pre-condition: 16 qu_* nodes exist -- all 16 target q_*_md nodes exist.
// ==========================================================================

// Audit: verify no qu_*_dossier nodes remain
MATCH (q:Quelle) WHERE q.id STARTS WITH 'qu_' AND q.id ENDS WITH '_dossier'
RETURN 'qu_dossier_remaining' AS check, count(q) AS violations;

// Audit: verify merged q_*_md nodes carry the old id in aliases
MATCH (q:Quelle) WHERE q.aliases IS NOT NULL
  AND any(a IN q.aliases WHERE a STARTS WITH 'qu_')
RETURN 'q_md_with_qu_alias' AS check, count(q) AS c;

// Audit: total case_markdown Quelle count (should be pre-merge count minus 16)
MATCH (q:Quelle {quelltyp:'case_markdown'}) RETURN 'case_markdown_total' AS check, count(q) AS c;
