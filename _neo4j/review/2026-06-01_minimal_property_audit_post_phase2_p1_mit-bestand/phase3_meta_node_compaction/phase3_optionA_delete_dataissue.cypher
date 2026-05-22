// Phase 3 Option A: compact DataIssue review nodes.
//
// STATUS: NOT APPLIED.
// Requires explicit approval because it deletes nodes and relationships.
//
// Backup first:
//   python _scripts/backup_neo4j_graph.py --out-dir _neo4j/review/backups/2026-06-01_pre_phase3_dataissue_compaction
//
// Precheck:
//   MATCH (d:DataIssue) RETURN count(d) AS dataissue_nodes, sum(size(keys(d))) AS dataissue_props;
//   MATCH (d:DataIssue)-[r]-() RETURN type(r) AS rel_type, count(r) AS rels, sum(size(keys(r))) AS rel_props ORDER BY rels DESC;

MATCH (d:DataIssue)
DETACH DELETE d;

// Postcheck:
//   MATCH (d:DataIssue) RETURN count(d) AS remaining_dataissue_nodes;
