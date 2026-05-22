// =================================================================
// MIGRATION TESTS — bauteilboersen_finalest_30_2026_05_31
// =================================================================
// Run PART A *before* executing FINAL_IMPORT_PLAN.md
// Run PART B *after*  executing FINAL_IMPORT_PLAN.md
// Each test returns a single row: { test_id, status:'PASS'|'FAIL', observed, expected }
// =================================================================


// =================================================================
// PART A  --  PRE-MIGRATION (preview / dry-run)
// =================================================================
// All A tests must PASS before running the migration.
// =================================================================

// A.1 — All 3 required Marktmodell IDs exist in live graph
WITH ['mm_kauf_gebraucht','mm_plattform_vermittelt','mm_spende'] AS req
OPTIONAL MATCH (n:Marktmodell) WHERE n.id IN req
WITH req, collect(DISTINCT n.id) AS found
WITH req, found, [x IN req WHERE NOT x IN found] AS missing
RETURN 'A.1 marktmodell_present' AS test_id,
       CASE WHEN size(missing)=0 THEN 'PASS' ELSE 'FAIL' END AS status,
       size(found) AS observed, 3 AS expected, missing AS missing_ids;

// A.2 — All 11 required Material IDs exist
WITH ['mat_aluminium','mat_beton','mat_daemmstoff','mat_glas','mat_gusseisen',
      'mat_holz','mat_keramik','mat_kunststoff','mat_naturstein','mat_stahl','mat_ziegel'] AS req
OPTIONAL MATCH (n:Material) WHERE n.id IN req
WITH req, collect(DISTINCT n.id) AS found
WITH req, found, [x IN req WHERE NOT x IN found] AS missing
RETURN 'A.2 material_present' AS test_id,
       CASE WHEN size(missing)=0 THEN 'PASS' ELSE 'FAIL' END AS status,
       size(found) AS observed, 11 AS expected, missing AS missing_ids;

// A.3 — All 13 required Bauteiltyp IDs exist
WITH ['bt_ausbau','bt_boden','bt_dach','bt_daemmung','bt_decke','bt_fassade',
      'bt_fenster','bt_gelaender','bt_technik','bt_traeger','bt_treppe','bt_tuer','bt_wand'] AS req
OPTIONAL MATCH (n:Bauteiltyp) WHERE n.id IN req
WITH req, collect(DISTINCT n.id) AS found
WITH req, found, [x IN req WHERE NOT x IN found] AS missing
RETURN 'A.3 bauteiltyp_present' AS test_id,
       CASE WHEN size(missing)=0 THEN 'PASS' ELSE 'FAIL' END AS status,
       size(found) AS observed, 13 AS expected, missing AS missing_ids;

// A.4 — All 8 required Akteurrolle IDs exist
WITH ['ar_materialbroker','ar_software_digitalisierung','ar_rueckbau_bauteilernte_logistik',
      'ar_aufbereitung_refurbishment','ar_materiallieferung_markt','ar_reuse_zirkularitaetsberatung',
      'ar_forschung_dokumentation','ar_bildung_wissenstransfer'] AS req
OPTIONAL MATCH (n:Akteurrolle) WHERE n.id IN req
WITH req, collect(DISTINCT n.id) AS found
WITH req, found, [x IN req WHERE NOT x IN found] AS missing
RETURN 'A.4 akteurrolle_present' AS test_id,
       CASE WHEN size(missing)=0 THEN 'PASS' ELSE 'FAIL' END AS status,
       size(found) AS observed, 8 AS expected, missing AS missing_ids;

// A.5 — All 5 required Methode IDs exist
WITH ['meth_urban_mining','meth_pre_deconstruction_audit','meth_bauteilkatalogisierung',
      'meth_materialinventur','meth_abrissmonitoring'] AS req
OPTIONAL MATCH (n:Methode) WHERE n.id IN req
WITH req, collect(DISTINCT n.id) AS found
WITH req, found, [x IN req WHERE NOT x IN found] AS missing
RETURN 'A.5 methode_present' AS test_id,
       CASE WHEN size(missing)=0 THEN 'PASS' ELSE 'FAIL' END AS status,
       size(found) AS observed, 5 AS expected, missing AS missing_ids;

// A.6 — All 30 TAKE anchors exist (any label, software_restado is :Software)
WITH ['articonnex','backacia','baticycle','batiterre','batrecup','baukarussell',
      'bauteilboerse_bremen','bauteilladen_winterthur','bauteilnetz_deutschland',
      'building_spares_market','cornermat_retrival','cycle_up','cycle_zero','enviromate',
      'gebruiktebouwmaterialen','genbyg','insert_marketplace','material_index',
      'materialenbank_leuven_atelier_circuler','materialrest24','r_place',
      're_store_harvestmap_vienna','reempro','rotordc','salvoweb','skop_marketplace',
      'software_restado','surplus_building_and_plumbing_materials','sustainability_yard',
      'useagain_bauteilclick'] AS req
OPTIONAL MATCH (a) WHERE a.id IN req
WITH req, collect(DISTINCT a.id) AS found
WITH req, found, [x IN req WHERE NOT x IN found] AS missing
RETURN 'A.6 take_anchors_present' AS test_id,
       CASE WHEN size(missing)=0 THEN 'PASS' ELSE 'FAIL' END AS status,
       size(found) AS observed, 30 AS expected, missing AS missing_ids;

// A.7 — All 9 non-TAKE actors currently have at_materialhub_bauteilboerse type
WITH ['globechain','loopfront','material_reuse_portal','new_horizon','raedificare',
      'resource_marktplaats','salza','reuse_and_trade','warp_it'] AS req
OPTIONAL MATCH (a:Akteur)-[:HAT_AKTEURTYP]->(:Akteurtyp {id:'at_materialhub_bauteilboerse'})
WHERE a.id IN req
WITH req, collect(DISTINCT a.id) AS found
WITH req, found, [x IN req WHERE NOT x IN found] AS not_typed
RETURN 'A.7 non_take_currently_typed' AS test_id,
       CASE WHEN size(found)=9 THEN 'PASS' ELSE 'WARN' END AS status,
       size(found) AS observed, 9 AS expected, not_typed AS not_currently_typed;
// FAIL meaning: some non-TAKE actor doesn't carry the type yet — STEP 0 will be a no-op for those,
// which is OK; the test is informational. WARN = inspect, not blocking.

// A.8 — No prior `:Geschaeftsmodell` label exists (clean slate)
OPTIONAL MATCH (g:Geschaeftsmodell)
WITH count(g) AS n
RETURN 'A.8 no_prior_geschaeftsmodell' AS test_id,
       CASE WHEN n=0 THEN 'PASS' ELSE 'FAIL' END AS status,
       n AS observed, 0 AS expected;

// A.9 — No prior edges tagged with this review_run (idempotency check)
OPTIONAL MATCH ()-[r {review_run:'bauteilboersen_finalest_30_2026_05_31'}]-()
WITH count(r) AS n
RETURN 'A.9 no_prior_review_run_edges' AS test_id,
       CASE WHEN n=0 THEN 'PASS' ELSE 'FAIL' END AS status,
       n AS observed, 0 AS expected;

// A.10 — Preview: how many edges WOULD STEP 0 remove? (should be exactly 9)
MATCH (a:Akteur)-[r:HAT_AKTEURTYP]->(:Akteurtyp {id:'at_materialhub_bauteilboerse'})
WHERE a.id IN ['globechain','loopfront','material_reuse_portal','new_horizon','raedificare',
               'resource_marktplaats','salza','reuse_and_trade','warp_it']
RETURN 'A.10 preview_step0_removal' AS test_id,
       CASE WHEN count(r)=9 THEN 'PASS' ELSE 'WARN' END AS status,
       count(r) AS observed, 9 AS expected;

// A.11 — Sanity: current at_materialhub_bauteilboerse population (baseline)
MATCH (a:Akteur)-[:HAT_AKTEURTYP]->(:Akteurtyp {id:'at_materialhub_bauteilboerse'})
RETURN 'A.11 baseline_materialhub_count' AS test_id,
       'INFO' AS status,
       count(a) AS observed_baseline_count;
// Note observed count here — after STEP 0 it should drop by exactly 9.


// =================================================================
// PART B  --  POST-MIGRATION (finalized-state verification)
// =================================================================
// All B tests must PASS after running the migration.
// =================================================================

// B.0 — Quick summary banner
RETURN 'B.0 post_migration_run_start' AS test_id, datetime() AS observed_at;

// B.1 — STEP 0 cleanup verified: no non-TAKE actor still has at_materialhub_bauteilboerse
OPTIONAL MATCH (a:Akteur)-[:HAT_AKTEURTYP]->(:Akteurtyp {id:'at_materialhub_bauteilboerse'})
WHERE a.id IN ['globechain','loopfront','material_reuse_portal','new_horizon','raedificare',
               'resource_marktplaats','salza','reuse_and_trade','warp_it']
WITH count(a) AS n, collect(a.id) AS leftover
RETURN 'B.1 step0_cleanup_done' AS test_id,
       CASE WHEN n=0 THEN 'PASS' ELSE 'FAIL' END AS status,
       n AS observed, 0 AS expected,
       leftover AS leftover_actors;

// B.2 — 5 :Geschaeftsmodell nodes created
MATCH (g:Geschaeftsmodell {review_run:'bauteilboersen_finalest_30_2026_05_31'})
RETURN 'B.2 geschaeftsmodell_nodes_count' AS test_id,
       CASE WHEN count(g)=5 THEN 'PASS' ELSE 'FAIL' END AS status,
       count(g) AS observed, 5 AS expected,
       collect(g.id) AS created_ids;

// B.3 — Exactly 5 distinct GM IDs and they are the right ones
MATCH (g:Geschaeftsmodell {review_run:'bauteilboersen_finalest_30_2026_05_31'})
WITH collect(g.id) AS got,
     ['gm_shop_eigenstock','gm_marketplace_vermittlung','gm_dienstleistung_urban_mining',
      'gm_saas_inventar_plattform','gm_netzwerk_aggregator'] AS expected
RETURN 'B.3 geschaeftsmodell_id_set' AS test_id,
       CASE WHEN size([x IN expected WHERE NOT x IN got])=0
                 AND size([x IN got WHERE NOT x IN expected])=0
            THEN 'PASS' ELSE 'FAIL' END AS status,
       got AS observed, expected AS expected;

// B.4 — 44 HAT_GESCHAEFTSMODELL edges with this run tag
MATCH ()-[r:HAT_GESCHAEFTSMODELL {review_run:'bauteilboersen_finalest_30_2026_05_31'}]->()
RETURN 'B.4 hat_geschaeftsmodell_count' AS test_id,
       CASE WHEN count(r)=44 THEN 'PASS' ELSE 'FAIL' END AS status,
       count(r) AS observed, 44 AS expected;

// B.5 — Cluster in-degree distribution
MATCH (a)-[:HAT_GESCHAEFTSMODELL]->(g:Geschaeftsmodell)
WITH g.id AS cluster, count(a) AS actors
WITH collect({cluster: cluster, actors: actors}) AS got
WITH got,
     [{cluster:'gm_marketplace_vermittlung',         actors:17},
      {cluster:'gm_dienstleistung_urban_mining',     actors:13},
      {cluster:'gm_shop_eigenstock',                 actors:11},
      {cluster:'gm_netzwerk_aggregator',             actors: 2},
      {cluster:'gm_saas_inventar_plattform',         actors: 1}] AS expected
RETURN 'B.5 cluster_distribution' AS test_id,
       CASE WHEN all(e IN expected WHERE e IN got)
                 AND all(g IN got      WHERE g IN expected)
            THEN 'PASS' ELSE 'FAIL' END AS status,
       got AS observed, expected AS expected;

// B.6 — Multi-edge distribution per actor (17 single / 12 dual / 1 triple)
MATCH (a)-[r:HAT_GESCHAEFTSMODELL]->()
WHERE a.id IN ['articonnex','backacia','baticycle','batiterre','batrecup','baukarussell',
               'bauteilboerse_bremen','bauteilladen_winterthur','bauteilnetz_deutschland',
               'building_spares_market','cornermat_retrival','cycle_up','cycle_zero','enviromate',
               'gebruiktebouwmaterialen','genbyg','insert_marketplace','material_index',
               'materialenbank_leuven_atelier_circuler','materialrest24','r_place',
               're_store_harvestmap_vienna','reempro','rotordc','salvoweb','skop_marketplace',
               'software_restado','surplus_building_and_plumbing_materials','sustainability_yard',
               'useagain_bauteilclick']
WITH a, count(r) AS n
WITH n, count(a) AS actors ORDER BY n
WITH collect({n_edges: n, actors: actors}) AS got
WITH got, [{n_edges:1, actors:17},{n_edges:2, actors:12},{n_edges:3, actors:1}] AS expected
RETURN 'B.6 multi_edge_distribution' AS test_id,
       CASE WHEN all(e IN expected WHERE e IN got)
                 AND all(g IN got      WHERE g IN expected)
            THEN 'PASS' ELSE 'FAIL' END AS status,
       got AS observed, expected AS expected;

// B.7 — Every TAKE actor has at least one HAT_GESCHAEFTSMODELL
WITH ['articonnex','backacia','baticycle','batiterre','batrecup','baukarussell',
      'bauteilboerse_bremen','bauteilladen_winterthur','bauteilnetz_deutschland',
      'building_spares_market','cornermat_retrival','cycle_up','cycle_zero','enviromate',
      'gebruiktebouwmaterialen','genbyg','insert_marketplace','material_index',
      'materialenbank_leuven_atelier_circuler','materialrest24','r_place',
      're_store_harvestmap_vienna','reempro','rotordc','salvoweb','skop_marketplace',
      'software_restado','surplus_building_and_plumbing_materials','sustainability_yard',
      'useagain_bauteilclick'] AS req
UNWIND req AS anchor
OPTIONAL MATCH (a {id: anchor})-[gm:HAT_GESCHAEFTSMODELL]->()
WITH anchor, count(gm) AS gm_count
WHERE gm_count = 0
WITH collect(anchor) AS missing
RETURN 'B.7 every_take_actor_has_gm' AS test_id,
       CASE WHEN size(missing)=0 THEN 'PASS' ELSE 'FAIL' END AS status,
       size(missing) AS observed_missing, 0 AS expected_missing,
       missing AS actors_without_gm;

// B.8 — Exactly 30 HAT_MARKTMODELL edges with this run tag (one per actor)
MATCH ()-[r:HAT_MARKTMODELL {review_run:'bauteilboersen_finalest_30_2026_05_31'}]->()
RETURN 'B.8 hat_marktmodell_count' AS test_id,
       CASE WHEN count(r)=30 THEN 'PASS' ELSE 'FAIL' END AS status,
       count(r) AS observed, 30 AS expected;

// B.9 — Each TAKE actor has exactly one HAT_MARKTMODELL from this run
MATCH (a:Akteur)-[r:HAT_MARKTMODELL {review_run:'bauteilboersen_finalest_30_2026_05_31'}]->()
WITH a, count(r) AS n WHERE n <> 1
RETURN 'B.9 one_marktmodell_per_actor' AS test_id,
       CASE WHEN count(a)=0 THEN 'PASS' ELSE 'FAIL' END AS status,
       count(a) AS observed_violations, 0 AS expected_violations,
       collect(a.id + ':' + toString(n)) AS violators;

// B.10 — Strict NUTZT_MATERIAL count = 40
MATCH ()-[r:NUTZT_MATERIAL {review_run:'bauteilboersen_finalest_30_2026_05_31'}]->()
RETURN 'B.10 nutzt_material_count' AS test_id,
       CASE WHEN count(r)=40 THEN 'PASS' ELSE 'FAIL' END AS status,
       count(r) AS observed, 40 AS expected;

// B.11 — Strict HAT_BAUTEILTYP count = 72
MATCH ()-[r:HAT_BAUTEILTYP {review_run:'bauteilboersen_finalest_30_2026_05_31'}]->()
RETURN 'B.11 hat_bauteiltyp_count' AS test_id,
       CASE WHEN count(r)=72 THEN 'PASS' ELSE 'FAIL' END AS status,
       count(r) AS observed, 72 AS expected;

// B.12 — Per-actor strict-import row count (16 distinct actors total)
MATCH (a)-[r:NUTZT_MATERIAL|HAT_BAUTEILTYP {review_run:'bauteilboersen_finalest_30_2026_05_31'}]->()
WITH a.id AS actor, type(r) AS rel_type, count(r) AS n
ORDER BY actor, rel_type
WITH collect(actor + '/' + rel_type + ':' + toString(n)) AS observed_per_actor,
     count(DISTINCT actor) AS distinct_actors
RETURN 'B.12 strict_import_per_actor' AS test_id,
       CASE WHEN distinct_actors=16 THEN 'PASS' ELSE 'FAIL' END AS status,
       distinct_actors AS observed, 16 AS expected,
       observed_per_actor AS per_actor;

// B.13 — Spot check: rotordc has gm_shop_eigenstock + gm_dienstleistung_urban_mining + mat_keramik
MATCH (a:Akteur {id:'rotordc'})
OPTIONAL MATCH (a)-[:HAT_GESCHAEFTSMODELL]->(g:Geschaeftsmodell)
WITH a, collect(DISTINCT g.id) AS gms
OPTIONAL MATCH (a)-[:NUTZT_MATERIAL]->(m:Material {id:'mat_keramik'})
WITH a, gms, collect(DISTINCT m.id) AS mats
RETURN 'B.13 rotordc_spot_check' AS test_id,
       CASE WHEN size([x IN ['gm_shop_eigenstock','gm_dienstleistung_urban_mining'] WHERE x IN gms])=2
                 AND 'mat_keramik' IN mats
            THEN 'PASS' ELSE 'FAIL' END AS status,
       {gms: gms, mats: mats} AS observed;

// B.14 — Spot check: material_index has 3 GM clusters (triple)
MATCH (a:Akteur {id:'material_index'})-[:HAT_GESCHAEFTSMODELL]->(g:Geschaeftsmodell)
WITH collect(DISTINCT g.id) AS gms
RETURN 'B.14 material_index_triple_gm' AS test_id,
       CASE WHEN size([x IN ['gm_marketplace_vermittlung','gm_dienstleistung_urban_mining',
                              'gm_saas_inventar_plattform'] WHERE x IN gms])=3
            THEN 'PASS' ELSE 'FAIL' END AS status,
       gms AS observed;

// B.15 — Spot check: batiterre has 5 mat + 10 bt
MATCH (a:Akteur {id:'batiterre'})
OPTIONAL MATCH (a)-[rm:NUTZT_MATERIAL {review_run:'bauteilboersen_finalest_30_2026_05_31'}]->()
WITH a, count(rm) AS mat_n
OPTIONAL MATCH (a)-[rb:HAT_BAUTEILTYP {review_run:'bauteilboersen_finalest_30_2026_05_31'}]->()
WITH mat_n, count(rb) AS bt_n
RETURN 'B.15 batiterre_strict_counts' AS test_id,
       CASE WHEN mat_n=5 AND bt_n=10 THEN 'PASS' ELSE 'FAIL' END AS status,
       {mat: mat_n, bt: bt_n} AS observed,
       {mat: 5, bt: 10} AS expected;

// B.16 — Spot check: rotordc has 0 strict bt (only mat_keramik)
MATCH (a:Akteur {id:'rotordc'})
OPTIONAL MATCH (a)-[rb:HAT_BAUTEILTYP {review_run:'bauteilboersen_finalest_30_2026_05_31'}]->()
WITH count(rb) AS bt_n
RETURN 'B.16 rotordc_no_strict_bt' AS test_id,
       CASE WHEN bt_n=0 THEN 'PASS' ELSE 'FAIL' END AS status,
       bt_n AS observed, 0 AS expected;

// B.17 — Spot check: baticycle has 0 strict mat (only 6 bt)
MATCH (a:Akteur {id:'baticycle'})
OPTIONAL MATCH (a)-[rm:NUTZT_MATERIAL {review_run:'bauteilboersen_finalest_30_2026_05_31'}]->()
WITH count(rm) AS mat_n
RETURN 'B.17 baticycle_no_strict_mat' AS test_id,
       CASE WHEN mat_n=0 THEN 'PASS' ELSE 'FAIL' END AS status,
       mat_n AS observed, 0 AS expected;

// B.18 — Spot check: batrecup + cycle_zero map to mm_spende (free apps)
MATCH (a:Akteur)-[:HAT_MARKTMODELL {review_run:'bauteilboersen_finalest_30_2026_05_31'}]->(m:Marktmodell)
WHERE a.id IN ['batrecup','cycle_zero']
WITH collect({actor: a.id, mm: m.id}) AS observed
RETURN 'B.18 spende_apps' AS test_id,
       CASE WHEN all(x IN observed WHERE x.mm='mm_spende') AND size(observed)=2
            THEN 'PASS' ELSE 'FAIL' END AS status,
       observed;

// B.19 — Fingerprint check: every urban-mining actor has rb logistic role
MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_dienstleistung_urban_mining'})
OPTIONAL MATCH (a)-[:HAT_AKTEURROLLE]->(r:Akteurrolle {id:'ar_rueckbau_bauteilernte_logistik'})
WITH a, r WHERE r IS NULL
WITH collect(a.id) AS missing
RETURN 'B.19 urban_mining_role_fingerprint' AS test_id,
       CASE WHEN size(missing)=0 THEN 'PASS' ELSE 'FAIL' END AS status,
       size(missing) AS observed_missing, 0 AS expected_missing,
       missing AS actors_missing_role;

// B.20 — Fingerprint check: every urban-mining actor links meth_urban_mining
MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_dienstleistung_urban_mining'})
OPTIONAL MATCH (a)-[:HAT_METHODE]->(m:Methode {id:'meth_urban_mining'})
WITH a, m WHERE m IS NULL
WITH collect(a.id) AS missing
RETURN 'B.20 urban_mining_method_fingerprint' AS test_id,
       CASE WHEN size(missing)=0 THEN 'PASS' ELSE 'FAIL' END AS status,
       size(missing) AS observed_missing, 0 AS expected_missing,
       missing AS actors_missing_method;

// B.21 — at_materialhub_bauteilboerse population dropped by exactly 9 vs baseline (A.11)
// (manual check: compare to A.11 observed_baseline_count; difference must be 9)
MATCH (a:Akteur)-[:HAT_AKTEURTYP]->(:Akteurtyp {id:'at_materialhub_bauteilboerse'})
RETURN 'B.21 final_materialhub_count' AS test_id,
       'INFO' AS status,
       count(a) AS observed_final_count;

// B.22 — No orphan edges (sanity): every HAT_GESCHAEFTSMODELL points at a real Geschaeftsmodell
OPTIONAL MATCH ()-[r:HAT_GESCHAEFTSMODELL {review_run:'bauteilboersen_finalest_30_2026_05_31'}]->(g)
WITH r, g
WHERE r IS NOT NULL AND NOT g:Geschaeftsmodell
WITH count(r) AS n
RETURN 'B.22 no_orphan_gm_edges' AS test_id,
       CASE WHEN n=0 THEN 'PASS' ELSE 'FAIL' END AS status,
       n AS observed, 0 AS expected;

// B.23 — Schema invariant: every :Akteur with HAT_GESCHAEFTSMODELL also has HAT_AKTEURTYP and HAT_MARKTMODELL
//        Non-Akteur nodes (e.g. :Software software_restado) are exempt — their label is the classification.
MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->()
WITH DISTINCT a
OPTIONAL MATCH (a)-[t:HAT_AKTEURTYP]->()
WITH a, count(t) AS t_cnt
OPTIONAL MATCH (a)-[mm:HAT_MARKTMODELL]->()
WITH a, t_cnt, count(mm) AS mm_cnt
WHERE t_cnt = 0 OR mm_cnt = 0
WITH collect({actor: a.id, has_type: t_cnt, has_marktmodell: mm_cnt}) AS incomplete
RETURN 'B.23 schema_completeness_akteur_only' AS test_id,
       CASE WHEN size(incomplete)=0 THEN 'PASS' ELSE 'FAIL' END AS status,
       size(incomplete) AS observed_incomplete, 0 AS expected_incomplete,
       incomplete AS incomplete_actors;


// =================================================================
// PART C  --  DIAGNOSTICS (run only if any B test fails)
// =================================================================

// C.1 — Show every actor's full Geschaeftsmodell assignment
MATCH (a:Akteur)-[r:HAT_GESCHAEFTSMODELL]->(g:Geschaeftsmodell)
RETURN a.id AS actor, collect({gm: g.id, conf: r.evidence_confidence}) AS gms
ORDER BY actor;

// C.2 — Show every actor's strict-import edge counts
MATCH (a:Akteur)
WHERE a.id IN ['articonnex','backacia','baticycle','batiterre','batrecup','baukarussell',
               'bauteilboerse_bremen','bauteilladen_winterthur','bauteilnetz_deutschland',
               'building_spares_market','cornermat_retrival','cycle_up','cycle_zero','enviromate',
               'gebruiktebouwmaterialen','genbyg','insert_marketplace','material_index',
               'materialenbank_leuven_atelier_circuler','materialrest24','r_place',
               're_store_harvestmap_vienna','reempro','rotordc','salvoweb','skop_marketplace',
               'software_restado','surplus_building_and_plumbing_materials','sustainability_yard',
               'useagain_bauteilclick']
OPTIONAL MATCH (a)-[rm:NUTZT_MATERIAL {review_run:'bauteilboersen_finalest_30_2026_05_31'}]->(m)
WITH a, collect(DISTINCT m.id) AS mats
OPTIONAL MATCH (a)-[rb:HAT_BAUTEILTYP {review_run:'bauteilboersen_finalest_30_2026_05_31'}]->(b)
WITH a.id AS actor, mats, collect(DISTINCT b.id) AS bts
RETURN actor, size(mats) AS mat_n, mats, size(bts) AS bt_n, bts
ORDER BY size(mats)+size(bts) DESC;

// C.3 — List the 9 non-TAKE actors and their current Akteurtyp(s) post-cleanup
MATCH (a:Akteur)
WHERE a.id IN ['globechain','loopfront','material_reuse_portal','new_horizon','raedificare',
               'resource_marktplaats','salza','reuse_and_trade','warp_it']
OPTIONAL MATCH (a)-[:HAT_AKTEURTYP]->(t:Akteurtyp)
RETURN a.id AS actor, collect(DISTINCT t.id) AS types_remaining
ORDER BY actor;


// =================================================================
// EXPECTED FINAL STATE (after migration)
// =================================================================
// :Geschaeftsmodell nodes ............................. 5
// HAT_GESCHAEFTSMODELL edges (review_run-tagged) ...... 44
// HAT_MARKTMODELL edges (review_run-tagged) ........... 30
// NUTZT_MATERIAL edges (review_run-tagged) ............ 40
// HAT_BAUTEILTYP edges (review_run-tagged) ............ 72
// HAT_AKTEURTYP→at_materialhub_bauteilboerse removed .. 9
// HAT_AKTEURROLLE / HAT_METHODE fingerprint edges .... idempotent (count varies)
// Total new edges ..................................... ~210
// Net edges removed ................................... 9
// =================================================================
