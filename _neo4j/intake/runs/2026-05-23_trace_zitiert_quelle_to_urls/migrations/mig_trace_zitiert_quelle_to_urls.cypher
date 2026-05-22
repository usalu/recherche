// Q-EXT source trace migration.
// The executable implementation is logs/trace_zitiert_quelle_to_urls_runner.py.
// This note exists so the run directory has a Cypher migration pointer.
//
// High-level operations:
// 1. Copy URL endpoint properties into concrete source_url/source_urls properties.
// 2. Mark unresolved information relationships for review.
// 3. Delete only :ZITIERT_QUELLE relationships stamped by this run.
