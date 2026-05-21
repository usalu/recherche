// ==========================================================================
// mig_r2_e_restore_tool_label
// Add :Tool as a secondary label on :Software nodes with kind='tool'.
// Preserves :Software primary label so existing queries still work.
// ==========================================================================

MATCH (s:Software {kind: 'tool'})
SET s:Tool,
    s.migration_origin = coalesce(s.migration_origin, '') + ' | mig_r2_e_tool_secondary_label';

// Audits
MATCH (t:Tool) RETURN 'tool_count' AS check, count(t) AS c;
MATCH (t:Tool) WHERE NOT 'Software' IN labels(t)
RETURN 'tool_without_software' AS check, count(t) AS violations;
MATCH (s:Software {kind:'tool'}) WHERE NOT 'Tool' IN labels(s)
RETURN 'software_tool_kind_without_tool_label' AS check, count(s) AS violations;
