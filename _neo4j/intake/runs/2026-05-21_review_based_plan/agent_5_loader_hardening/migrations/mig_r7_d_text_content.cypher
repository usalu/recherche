// ==========================================================================
// mig_r7_d_text_content
// Audit queries only. Actual text_content population is driven by
// agent_5_runner.py which reads each dossier .md file and calls:
//   MATCH (q:Quelle {id: $quelle_id})
//   SET q.text_content = $text, q.text_content_loaded_at = date(),
//       q.migration_origin = coalesce(q.migration_origin,'') + ' | r7_d_text_content'
// ==========================================================================

// Audit: how many case_markdown Quellen now have text_content
MATCH (q:Quelle {quelltyp:'case_markdown'})
WHERE q.text_content IS NOT NULL
RETURN 'case_markdown_with_text' AS check, count(q) AS c;

// Audit: how many still missing
MATCH (q:Quelle {quelltyp:'case_markdown'})
WHERE q.text_content IS NULL
RETURN 'case_markdown_without_text' AS check, count(q) AS c;

// Audit: DataIssue drift findings
MATCH (d:DataIssue {kind: 'dossier_uses_retired_type'})
RETURN 'drift_issues_count' AS check, count(d) AS c;

MATCH (d:DataIssue {kind: 'dossier_uses_retired_type'})
RETURN d.ref_label AS retired_type, count(d) AS occurrences
ORDER BY occurrences DESC;
