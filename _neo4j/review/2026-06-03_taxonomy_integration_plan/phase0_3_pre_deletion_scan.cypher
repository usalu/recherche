// =====================================================================
// Phase 0.3 — Pre-deletion scan
//
// Read-only. Captures every node and every inbound/outbound edge that
// Phase 6 will touch (delete or migrate). The output should be dumped
// to JSON and stored at:
//   _neo4j/review/2026-06-03_taxonomy_integration_plan/snapshot_pre_integration/pre_deletion_scan.json
//
// The Phase 6 driver uses this scan to drive precise reattachment per
// (old_node, upstream_type) tuple and as a sanity check (if any edge
// remains in the live graph after Phase 6 that's not in this scan,
// abort).
//
// Each query below returns INFO rows; export them with the database
// driver of choice (cypher-shell --format json works).
// =====================================================================


// ---------- §1. Old vocab nodes ----------

// 1.1 All old vocab nodes that will be hard-deleted
MATCH (n)
WHERE n:Methode OR n:Aufbereitungsverfahren OR n:Ressourcenquelle
   OR n:WiederverwendungsArt
   OR (n:Rueckbauverfahren AND n.id = 'rv_betonfraesen')
RETURN 'OLD_VOCAB_NODE' AS kind,
       labels(n) AS labels,
       n.id AS id,
       n.name AS name,
       properties(n) AS props;
// expected: 13 Methode + 62 Aufbereitungsverfahren + 16 Ressourcenquelle + 11 WiederverwendungsArt + 1 rv_betonfraesen = 103 rows


// ---------- §2. Inbound edges to old vocab nodes ----------

// 2.1 Group by (source label, rel type) to see which upstreams exist
MATCH (src)-[r]->(t)
WHERE t:Methode OR t:Aufbereitungsverfahren OR t:Ressourcenquelle
   OR t:WiederverwendungsArt
   OR (t:Rueckbauverfahren AND t.id = 'rv_betonfraesen')
RETURN 'INBOUND_EDGE_SUMMARY' AS kind,
       labels(src) AS src_labels,
       type(r) AS rel_type,
       labels(t) AS target_labels,
       count(r) AS edge_count
ORDER BY edge_count DESC;

// 2.2 Full per-edge dump (heavy — for forensic audit)
MATCH (src)-[r]->(t)
WHERE t:Methode OR t:Aufbereitungsverfahren OR t:Ressourcenquelle
   OR t:WiederverwendungsArt
   OR (t:Rueckbauverfahren AND t.id = 'rv_betonfraesen')
RETURN 'INBOUND_EDGE' AS kind,
       labels(src) AS src_labels,
       src.id AS src_id,
       type(r) AS rel_type,
       properties(r) AS rel_props,
       labels(t) AS target_labels,
       t.id AS target_id;


// ---------- §3. Outbound edges from old vocab nodes ----------

// 3.1 Group by (rel type, target label)
MATCH (n)-[r]->(tgt)
WHERE n:Aufbereitungsverfahren OR n:Methode OR n:Ressourcenquelle
   OR n:WiederverwendungsArt OR (n:Rueckbauverfahren AND n.id = 'rv_betonfraesen')
RETURN 'OUTBOUND_EDGE_SUMMARY' AS kind,
       labels(n) AS source_labels,
       type(r) AS rel_type,
       labels(tgt) AS target_labels,
       count(r) AS edge_count
ORDER BY edge_count DESC;

// 3.2 Full per-edge dump for the migration recipe
MATCH (n)-[r]->(tgt)
WHERE n:Aufbereitungsverfahren OR n:Methode OR n:Ressourcenquelle
   OR n:WiederverwendungsArt OR (n:Rueckbauverfahren AND n.id = 'rv_betonfraesen')
RETURN 'OUTBOUND_EDGE' AS kind,
       labels(n) AS source_labels,
       n.id AS source_id,
       type(r) AS rel_type,
       properties(r) AS rel_props,
       labels(tgt) AS target_labels,
       tgt.id AS target_id;


// ---------- §4. Bauteilgruppen scheduled for deletion ----------

// 4.1 All bg_reuse_* with no batch match (35 expected — from bauteilgruppe_id_map.csv where action=no_batch_equiv AND prefix=bg_reuse_)
LOAD CSV WITH HEADERS FROM 'file:///bauteilgruppe_id_map.csv' AS row
WITH row
WHERE row.action = 'no_batch_equiv' AND row.live_bg_id STARTS WITH 'bg_reuse_'
MATCH (bg:Bauteilgruppe {id: row.live_bg_id})
RETURN 'BG_DELETE_REUSE_ORPHAN' AS kind,
       bg.id AS id,
       bg.name AS name,
       bg.alte_funktion AS alte_funktion,
       bg.neue_funktion AS neue_funktion,
       bg.reuse_status AS reuse_status,
       bg.bg_kind AS bg_kind;

// 4.2 All non-bg_reuse_* (35 expected — out of scope)
MATCH (bg:Bauteilgruppe)
WHERE bg.id STARTS WITH 'bg_retained_'
   OR bg.id STARTS WITH 'bg_planned_'
   OR bg.id STARTS WITH 'bg_dismantled_'
   OR bg.id STARTS WITH 'bg_candidate_'
RETURN 'BG_DELETE_NON_REUSE' AS kind,
       bg.id AS id,
       bg.name AS name,
       bg.alte_funktion AS alte_funktion,
       bg.neue_funktion AS neue_funktion,
       bg.reuse_status AS reuse_status,
       bg.bg_kind AS bg_kind;

// 4.3 Inbound and outbound edges of BGs about to be deleted (heavy — for property/edge preservation accounting)
MATCH (bg:Bauteilgruppe)
WHERE bg.id STARTS WITH 'bg_retained_'
   OR bg.id STARTS WITH 'bg_planned_'
   OR bg.id STARTS WITH 'bg_dismantled_'
   OR bg.id STARTS WITH 'bg_candidate_'
   OR EXISTS {
        MATCH (bg)
        WHERE bg.id STARTS WITH 'bg_reuse_'
          AND NOT EXISTS { MATCH (bg)<-[:HAT_BAUTEILGRUPPE]-(:Projekt) WHERE EXISTS {
              MATCH () WHERE bg.id IN [<list-from-csv>] }} }
OPTIONAL MATCH (bg)<-[r_in]-(src)
WITH bg, src, r_in
WHERE r_in IS NOT NULL
RETURN 'BG_TO_DELETE_INBOUND' AS kind,
       bg.id AS bg_id,
       labels(src) AS src_labels,
       src.id AS src_id,
       type(r_in) AS rel_type
LIMIT 10000;


// ---------- §5. DataIssue sanity check (expected 0) ----------

MATCH (di:DataIssue)
RETURN 'DATAISSUE_COUNT' AS kind, count(di) AS n;
// expected: 0 — already cleaned per 2026-06-03 fresh export
