// =====================================================================
// Phase 6.4 — Delete Bauteilgruppen
//
// 6.4b — bg_reuse_* orphans (35): live BGs with no batch slug match,
//        replaced by batches' evidence-backed set.
//
// 6.4c — all non-reuse BGs (35): bg_retained_/planned_/dismantled_/candidate_
//        nodes don't semantically belong to :Bauteilgruppe (per user
//        decision #8). Hard-delete regardless of batch coverage.
//
// Total: 70 nodes hard-deleted. Expected loss: ~600-800 non-vocab edges
// + property bags. Per RICHNESS_AUDIT, those non-vocab edges are also
// predominantly `topology_synthesized` / `unklar` placeholders.
//
// Run AFTER Phase 6.3 (which deletes the vocab edges that point at
// old vocab nodes — but the BG-deletion step here uses DETACH DELETE
// so any remaining edges are also removed).
// =====================================================================


// ---------- §1. Pre-check: enumerate the BGs we're about to delete ----------

// 1.1 bg_reuse_* orphans (loaded from bauteilgruppe_id_map.csv)
LOAD CSV WITH HEADERS FROM 'file:///bauteilgruppe_id_map.csv' AS row
WITH row WHERE row.action = 'no_batch_equiv' AND row.live_bg_id STARTS WITH 'bg_reuse_'
MATCH (bg:Bauteilgruppe {id: row.live_bg_id})
RETURN 'P6.4b PRE' AS phase, count(bg) AS bg_reuse_orphans_to_delete;
// expected: 35

// 1.2 non-reuse BGs
MATCH (bg:Bauteilgruppe)
WHERE bg.id STARTS WITH 'bg_retained_'
   OR bg.id STARTS WITH 'bg_planned_'
   OR bg.id STARTS WITH 'bg_dismantled_'
   OR bg.id STARTS WITH 'bg_candidate_'
RETURN 'P6.4c PRE' AS phase, count(bg) AS non_reuse_bgs_to_delete;
// expected: 35


// ---------- §2. Apply: delete bg_reuse_ orphans ----------

LOAD CSV WITH HEADERS FROM 'file:///bauteilgruppe_id_map.csv' AS row
WITH row WHERE row.action = 'no_batch_equiv' AND row.live_bg_id STARTS WITH 'bg_reuse_'
MATCH (bg:Bauteilgruppe {id: row.live_bg_id})
DETACH DELETE bg;


// ---------- §3. Apply: delete non-reuse BGs ----------

MATCH (bg:Bauteilgruppe)
WHERE bg.id STARTS WITH 'bg_retained_'
   OR bg.id STARTS WITH 'bg_planned_'
   OR bg.id STARTS WITH 'bg_dismantled_'
   OR bg.id STARTS WITH 'bg_candidate_'
DETACH DELETE bg;


// ---------- §4. Post-checks ----------

// 4.1 No bg_reuse_* orphan remains
LOAD CSV WITH HEADERS FROM 'file:///bauteilgruppe_id_map.csv' AS row
WITH row WHERE row.action = 'no_batch_equiv' AND row.live_bg_id STARTS WITH 'bg_reuse_'
MATCH (bg:Bauteilgruppe {id: row.live_bg_id})
RETURN 'FAIL' AS status, bg.id;
// expected: 0 rows

// 4.2 No non-reuse :Bauteilgruppe remains
MATCH (bg:Bauteilgruppe)
WHERE bg.id STARTS WITH 'bg_retained_'
   OR bg.id STARTS WITH 'bg_planned_'
   OR bg.id STARTS WITH 'bg_dismantled_'
   OR bg.id STARTS WITH 'bg_candidate_'
RETURN 'FAIL' AS status, bg.id;
// expected: 0 rows

// 4.3 Total :Bauteilgruppe count after both deletes
MATCH (bg:Bauteilgruppe)
WITH count(bg) AS total
RETURN 'INFO' AS status, total AS bauteilgruppe_count,
       '~304 expected (350 pre − 35 reuse orphans − 35 non-reuse + 24 batch-new from P5)' AS note;
