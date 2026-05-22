// ==========================================================================
// mig_s4_d_alias_sanity.cypher
//
// Informational alias audit. The runner cross-references R7.a's journal and
// fixes only aliases that are known to have existed pre-merge.
// ==========================================================================

MATCH (d:Dossier)
WHERE d.id =~ 'q_.+_md'
WITH d, replace(replace(d.id, 'q_', 'qu_'), '_md', '_dossier') AS expected_alias
WHERE d.aliases IS NULL OR NOT (expected_alias IN d.aliases)
RETURN d.id AS dossier_id, expected_alias
LIMIT 20;

MATCH (d:Dossier)
WHERE d.aliases IS NOT NULL
  AND any(a IN d.aliases WHERE a STARTS WITH 'qu_' AND a ENDS WITH '_dossier')
RETURN 's4_d_known_qu_alias_count' AS check, count(d) AS c;
