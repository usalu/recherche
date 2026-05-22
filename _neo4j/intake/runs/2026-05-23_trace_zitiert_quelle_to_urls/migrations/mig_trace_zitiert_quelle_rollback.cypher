// Rollback marker for trace_zitiert_quelle_to_urls_2026-05-23.
// Full graph rollback should use:
//   _neo4j/review/backups/2026-05-23_pre_trace_zitiert_quelle_to_urls
//
// Property-only partial rollback is intentionally conservative:
// MATCH ()-[r]-()
// WHERE r.source_trace_migration = 'mig_trace_zitiert_quelle_to_urls_2026_05_23'
// REMOVE r.source_url, r.source_url_node_id, r.source_urls, r.source_url_node_ids,
//        r.source_url_status, r.source_url_http_code, r.source_url_wayback_snapshot,
//        r.source_url_last_checked_at, r.source_resolution_status,
//        r.source_trace_migration, r.source_trace_migrated_at,
//        r.superseded_by_migration, r.superseded_at, r.review_status;
//
// NOTE: deleted :ZITIERT_QUELLE relationships require restoring from the backup.
