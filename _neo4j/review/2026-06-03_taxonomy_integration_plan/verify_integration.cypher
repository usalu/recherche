// =====================================================================
// Reuse Taxonomy Integration — Verification Suite
// Read-only. Re-runnable. Every section is independent.
// Run with `:USE mit-bestand;` and inspect each block's output.
//
// Convention: every check is a numbered query. A passing run produces
//   - either zero rows (for "find anomalies" queries)
//   - or exactly one row with `status = 'OK'` plus context
// Any FAIL row blocks sign-off.
//
// Run tag: 'taxonomy_integration_2026_06_03'
// =====================================================================


// ---------- §1. Schema additions present ----------

// 1.1 New constraints exist
SHOW CONSTRAINTS YIELD name
WHERE name IN [
  'wiederverwendungsergebnis_id',
  'wiederverwendungsort_id',
  'rel_hat_ergebnis_id',
  'rel_hat_wiederverwendungsort_id',
  'rel_angewendet_auf_id'
]
WITH collect(name) AS found
RETURN CASE WHEN size(found) = 5 THEN 'OK' ELSE 'FAIL' END AS status,
       found AS constraints_found;

// 1.2 Seed nodes exist and are exactly the six canonical
MATCH (n:Wiederverwendungsergebnis)
WITH collect(n.id) AS ids
RETURN CASE
  WHEN apoc.coll.subtract(
    ['wver_bestandserhalt','wver_wv_gleiche_funktion','wver_wv_neue_funktion',
     'wver_modul_oder_abschnittswv','wver_material_reprocessing','wver_geplant_oder_gelagert'],
    ids) = []
   AND size(ids) = 6
  THEN 'OK' ELSE 'FAIL' END AS status,
  ids AS wver_ids;

MATCH (n:Wiederverwendungsort)
WITH collect(n.id) AS ids
RETURN CASE
  WHEN apoc.coll.subtract(
    ['wvo_in_situ','wvo_im_selben_gebaeude_versetzt','wvo_auf_demselben_standort_versetzt',
     'wvo_extern_importiert','wvo_temporaer_oder_zurueckgegeben','wvo_gelagert_oder_unbekannt'],
    ids) = []
   AND size(ids) = 6
  THEN 'OK' ELSE 'FAIL' END AS status,
  ids AS wvo_ids;

// 1.3 Six new canonical :Methode nodes present (post C2(a) collapse)
MATCH (n:Methode)
WITH collect(n.id) AS ids
RETURN CASE
  WHEN apoc.coll.subtract(
    ['meth_urban_mining_und_scouting','meth_bestands_und_reuse_assessment',
     'meth_verfuegbarkeitsbasiertes_design','meth_reversibles_design',
     'meth_zirkulaere_beschaffung','meth_dokumentation_und_monitoring'],
    ids) = []
   AND size(ids) = 6
  THEN 'OK' ELSE 'FAIL' END AS status,
  ids AS active_methode_ids;
// expected: status='OK', exactly the 6 new canonical, no leftover meth_*

// 1.4 Six new canonical :Aufbereitungsverfahren nodes present (post C4(a) collapse)
MATCH (n:Aufbereitungsverfahren)
WITH collect(n.id) AS ids
RETURN CASE
  WHEN apoc.coll.subtract(
    ['av_reinigung_und_oberflaeche','av_zuschnitt_und_vereinzelung',
     'av_pruefung_sortierung_qs','av_reparatur_und_refurbishment',
     'av_remanufacturing_und_upcycling','av_verstaerkung_und_schutz'],
    ids) = []
   AND size(ids) = 6
  THEN 'OK' ELSE 'FAIL' END AS status,
  ids AS active_aufbereitung_ids;
// expected: status='OK', exactly the 6 new canonical, no leftover av_*

// 1.5 Two new :Rueckbauverfahren nodes added (per C3)
MATCH (n:Rueckbauverfahren)
WHERE n.id IN ['rv_schneidender_rueckbau','rv_integrierter_rueckbau_und_lagerung']
RETURN 'INFO' AS status, collect(n.id) AS new_rv_ids;
// expected: both present

// 1.6 Six new canonical :Ressourcenquelle nodes (revised C1: replace, not reuse)
MATCH (n:Ressourcenquelle)
WITH collect(n.id) AS ids
RETURN CASE
  WHEN apoc.coll.subtract(
    ['rq_externer_spenderbau','rq_eigener_bestand','rq_gleicher_standort',
     'rq_bauteilmarkt_oder_lager','rq_leihgabe_oder_service','rq_restposten_abfall_unbekannt'],
    ids) = []
   AND size(ids) = 6
  THEN 'OK' ELSE 'FAIL' END AS status,
  ids AS active_ressourcenquelle_ids;
// expected: exactly 6 new canonical, no leftover old rq_*

// 1.7 :Rueckbauverfahren totals exactly 6 (4 kept + 2 added)
MATCH (n:Rueckbauverfahren)
WITH collect(n.id) AS ids
RETURN CASE
  WHEN apoc.coll.subtract(
    ['rv_selektiver_rueckbau','rv_ausbau_von_bauteilen','rv_demontage',
     'rv_zerstoerungsarme_bergung','rv_schneidender_rueckbau','rv_integrierter_rueckbau_und_lagerung'],
    ids) = []
   AND size(ids) = 6
  THEN 'OK' ELSE 'FAIL' END AS status,
  ids AS active_rueckbauverfahren_ids;
// expected: exactly these 6; rv_betonfraesen must be gone


// ---------- §2. Duplicate prevention ----------

// 2.1 No duplicate :Projekt names (id collision OR two projekts with same name)
MATCH (p:Projekt)
WITH p.name AS name, collect(p.id) AS ids
WHERE size(ids) > 1
RETURN 'FAIL' AS status, name, ids;
// expected: 0 rows

// 2.2 No batch-style `p_*` project ids leaked in (live convention is bare slug)
MATCH (p:Projekt) WHERE p.id STARTS WITH 'p_'
RETURN 'FAIL' AS status, p.id, p.name;
// expected: 0 rows  (the Kennwert `kw_p_*` ids are unaffected, they're :Kennwert not :Projekt)

// 2.3 No duplicate :Bauteilgruppe per project (same id) — duplicates with different ids are
// an accepted cost of skipping the resolver and are reported as INFO in §13 below.
MATCH (proj:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
WITH proj.id AS pid, bg.id AS bgid, count(*) AS n
WHERE n > 1
RETURN 'FAIL' AS status, pid, bgid, n AS edge_multiplicity,
       'same (project, bauteilgruppe) pair appears more than once' AS note;
// expected: 0 rows

// 2.4 `*_candidate` Bauteilgruppe slugs — now expected to exist as the batch-supplied
// new candidates per FINAL_PLAN decision #8. Report as INFO not FAIL.
MATCH (bg:Bauteilgruppe) WHERE bg.id ENDS WITH '_candidate'
RETURN 'INFO' AS status, bg.id, bg.name,
       'expected: batch-introduced candidate component; ~25-50 of these is normal' AS note;

// 2.5 Vocabulary singleton: every label-axis combo unique by name
UNWIND ['Methode','Rueckbauverfahren','Aufbereitungsverfahren',
        'Wiederverwendungsergebnis','Wiederverwendungsort','Ressourcenquelle']
       AS lbl
CALL apoc.cypher.run(
  'MATCH (n:`' + lbl + '`) WITH n.name AS nm, collect(n.id) AS ids WHERE size(ids) > 1 RETURN nm, ids',
  {}) YIELD value
RETURN 'FAIL' AS status, lbl, value.nm AS name, value.ids AS ids;
// expected: 0 rows


// ---------- §3. Edge-count parity vs coverage report §3 ----------

// 3.1 New-axis edge counts roughly match parsed batch totals (±10% tolerance)
// Expected per axis after Batch 01 inclusion (totals from 10 batches, 2240 rows):
//   HAT_ERGEBNIS               ≈ 423   (388 batches 02–09 + 35 batch 01)
//   HAT_RESSOURCENQUELLE +Δrun ≈ 482 base + 379 new   (350 + 29)
//   HAT_WIEDERVERWENDUNGSORT   ≈ 367   (344 + 23)
//   HAT_BAUTEILGRUPPE +Δrun    ≈ 350 base + 340 new   (335 + 5; resolver folds many; expect smaller delta)
//   HAT_METHODE +Δrun          ≈ 0 base after C2(a) reattach to 6 canonical, + 298 new
//                                (the 404 pre-existing edges get rewired to the 6 canonical; total still ≈ 404 + new from batches)
//   HAT_AUFBEREITUNG +Δrun     ≈ 411 base reattached + 283 new
//   HAT_RUECKBAUVERFAHREN +Δrun ≈ 299 base + 136 new
//   ANGEWENDET_AUF             ≈ 14

MATCH ()-[r:HAT_ERGEBNIS]->()
WITH count(r) AS total,
     count(CASE WHEN r.review_run = 'taxonomy_integration_2026_06_03' THEN 1 END) AS new_in_run
RETURN CASE WHEN total >= 380 AND new_in_run >= 380 THEN 'OK' ELSE 'CHECK' END AS status,
       'HAT_ERGEBNIS' AS rel, total, new_in_run, 423 AS expected_min_from_batches;

MATCH ()-[r:HAT_WIEDERVERWENDUNGSORT]->()
WITH count(r) AS total,
     count(CASE WHEN r.review_run = 'taxonomy_integration_2026_06_03' THEN 1 END) AS new_in_run
RETURN CASE WHEN total >= 330 AND new_in_run >= 330 THEN 'OK' ELSE 'CHECK' END AS status,
       'HAT_WIEDERVERWENDUNGSORT' AS rel, total, new_in_run, 367 AS expected_min_from_batches;

MATCH ()-[r:HAT_RESSOURCENQUELLE]->()
WITH count(r) AS total,
     count(CASE WHEN r.review_run = 'taxonomy_integration_2026_06_03' THEN 1 END) AS new_in_run
RETURN CASE WHEN total >= 800 AND new_in_run >= 340 THEN 'OK' ELSE 'CHECK' END AS status,
       'HAT_RESSOURCENQUELLE' AS rel, total, new_in_run,
       482 AS base_pre_integration, 379 AS expected_min_new;

MATCH ()-[r:HAT_METHODE]->(m:Methode)
// Every HAT_METHODE edge must point at one of the 6 new canonical
WHERE NOT m.id IN ['meth_urban_mining_und_scouting','meth_bestands_und_reuse_assessment',
                   'meth_verfuegbarkeitsbasiertes_design','meth_reversibles_design',
                   'meth_zirkulaere_beschaffung','meth_dokumentation_und_monitoring']
RETURN 'FAIL' AS status, type(r), m.id AS pointed_to_non_canonical;
// expected: 0 rows

MATCH ()-[r:HAT_AUFBEREITUNG]->(av:Aufbereitungsverfahren)
WHERE NOT av.id IN ['av_reinigung_und_oberflaeche','av_zuschnitt_und_vereinzelung',
                    'av_pruefung_sortierung_qs','av_reparatur_und_refurbishment',
                    'av_remanufacturing_und_upcycling','av_verstaerkung_und_schutz']
RETURN 'FAIL' AS status, type(r), av.id AS pointed_to_non_canonical;
// expected: 0 rows

MATCH ()-[r:HAT_RESSOURCENQUELLE]->(q:Ressourcenquelle)
WHERE NOT q.id IN ['rq_externer_spenderbau','rq_eigener_bestand','rq_gleicher_standort',
                   'rq_bauteilmarkt_oder_lager','rq_leihgabe_oder_service','rq_restposten_abfall_unbekannt']
RETURN 'FAIL' AS status, type(r), q.id AS pointed_to_non_canonical;
// expected: 0 rows

// And no HAT_WIEDERVERWENDUNGSART edges anywhere
MATCH ()-[r:HAT_WIEDERVERWENDUNGSART]->()
RETURN CASE WHEN count(r) = 0 THEN 'OK' ELSE 'FAIL' END AS status,
       count(r) AS remaining_wva_edges;

MATCH ()-[r:ANGEWENDET_AUF]->()
WITH count(r) AS total
RETURN CASE WHEN total >= 10 AND total <= 30 THEN 'OK' ELSE 'CHECK' END AS status,
       'ANGEWENDET_AUF' AS rel, total, 14 AS expected_from_batches;


// ---------- §4. ID-prefix purity (schema conventions) ----------

// 4.1 Vocabulary nodes all carry the right id prefix
MATCH (n:Wiederverwendungsergebnis) WHERE NOT n.id STARTS WITH 'wver_'
RETURN 'FAIL' AS status, 'Wiederverwendungsergebnis' AS lbl, n.id;
MATCH (n:Wiederverwendungsort) WHERE NOT n.id STARTS WITH 'wvo_'
RETURN 'FAIL' AS status, 'Wiederverwendungsort' AS lbl, n.id;
// expected: 0 rows each

// 4.2 Every new Bauteilgruppe candidate inherits a project anchor
MATCH (bg:Bauteilgruppe {review_run: 'taxonomy_integration_2026_06_03'})
WHERE NOT (:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg)
RETURN 'FAIL' AS status, bg.id, bg.name;
// expected: 0 rows

// 4.3 Every new edge from this run has a target node carrying a controlled-vocab id
MATCH (bg:Bauteilgruppe)-[r {review_run: 'taxonomy_integration_2026_06_03'}]->(t)
WHERE NOT (
     (t:Wiederverwendungsergebnis     AND t.id STARTS WITH 'wver_')
  OR (t:Wiederverwendungsort          AND t.id STARTS WITH 'wvo_')
  OR (t:Ressourcenquelle              AND t.id STARTS WITH 'rq_')
  OR (t:Herkunft                      AND t.id STARTS WITH 'hk_')
  OR (t:Methode                       AND t.id STARTS WITH 'meth_')
  OR (t:Rueckbauverfahren             AND t.id STARTS WITH 'rv_')
  OR (t:Aufbereitungsverfahren        AND t.id STARTS WITH 'av_')
  OR (t:Bauteilgruppe                 AND t.id STARTS WITH 'bg_')
)
RETURN 'FAIL' AS status, bg.id, type(r), labels(t), t.id;
// expected: 0 rows


// ---------- §5. Legacy retirement clean ----------

// 5.1 Zero active HAT_WIEDERVERWENDUNGSART edges remain
MATCH ()-[r:HAT_WIEDERVERWENDUNGSART]->()
RETURN CASE WHEN count(r) = 0 THEN 'OK' ELSE 'FAIL' END AS status,
       count(r) AS remaining_legacy_edges;

// 5.2 Zero active :WiederverwendungsArt nodes
MATCH (n:WiederverwendungsArt)
RETURN CASE WHEN count(n) = 0 THEN 'OK' ELSE 'FAIL' END AS status,
       count(n) AS remaining_active_wva;

// 5.3 :WiederverwendungsArt label retires entirely — no nodes carry it, no _Legacy variants
MATCH (n) WHERE n:WiederverwendungsArt OR n:WiederverwendungsArt_Legacy
RETURN CASE WHEN count(n) = 0 THEN 'OK' ELSE 'FAIL' END AS status,
       count(n) AS any_wva_nodes_remaining,
       'expected 0 — label retires entirely' AS note;

// 5.4 No :*_Legacy labels anywhere (user policy: no legacy in graph)
MATCH (n)
WHERE n:Methode_Legacy OR n:Aufbereitungsverfahren_Legacy OR n:Ressourcenquelle_Legacy
   OR n:WiederverwendungsArt_Legacy OR n:Rueckbauverfahren_Legacy
RETURN CASE WHEN count(n) = 0 THEN 'OK' ELSE 'FAIL' END AS status,
       count(n) AS legacy_label_nodes,
       'expected 0 — no :*_Legacy labels per user "no legacy" policy' AS note;

// 5.5 No active :Methode node carries an old id (sanity check on hard-delete)
MATCH (n:Methode)
WHERE NOT n.id IN ['meth_urban_mining_und_scouting','meth_bestands_und_reuse_assessment',
                   'meth_verfuegbarkeitsbasiertes_design','meth_reversibles_design',
                   'meth_zirkulaere_beschaffung','meth_dokumentation_und_monitoring']
RETURN 'FAIL' AS status, n.id, n.name, 'old meth_* should have been hard-deleted in P6.5' AS note;
// expected: 0 rows

// 5.6 No active :Aufbereitungsverfahren node carries an old id
MATCH (n:Aufbereitungsverfahren)
WHERE NOT n.id IN ['av_reinigung_und_oberflaeche','av_zuschnitt_und_vereinzelung',
                   'av_pruefung_sortierung_qs','av_reparatur_und_refurbishment',
                   'av_remanufacturing_und_upcycling','av_verstaerkung_und_schutz']
RETURN 'FAIL' AS status, n.id, n.name, 'old av_* should have been hard-deleted in P6.5' AS note;
// expected: 0 rows

// 5.7 No active :Ressourcenquelle node carries an old id
MATCH (n:Ressourcenquelle)
WHERE NOT n.id IN ['rq_externer_spenderbau','rq_eigener_bestand','rq_gleicher_standort',
                   'rq_bauteilmarkt_oder_lager','rq_leihgabe_oder_service','rq_restposten_abfall_unbekannt']
RETURN 'FAIL' AS status, n.id, n.name, 'old rq_* should have been hard-deleted in P6.5' AS note;
// expected: 0 rows

// 5.8 rv_betonfraesen specifically must be gone (the only Rueckbau node deleted)
MATCH (n:Rueckbauverfahren {id: 'rv_betonfraesen'})
RETURN 'FAIL' AS status, n.id, 'should have been hard-deleted (folded into rv_schneidender_rueckbau)' AS note;
// expected: 0 rows

// 5.9 Migration provenance preserved on the 115+47 reattached edges (P6.1 + P6.2)
MATCH ()-[r:HAT_METHODE {review_run: 'taxonomy_integration_2026_06_03'}]->()
WHERE r.legacy_methode_id IS NOT NULL
WITH count(r) AS meth_provenance
MATCH ()-[r2:HAT_AUFBEREITUNG {review_run: 'taxonomy_integration_2026_06_03'}]->()
WHERE r2.legacy_aufbereitung_id IS NOT NULL
WITH meth_provenance, count(r2) AS auf_provenance
MATCH ()-[r3:HAT_RESSOURCENQUELLE {review_run: 'taxonomy_integration_2026_06_03'}]->()
WHERE r3.legacy_ressourcenquelle_id IS NOT NULL
WITH meth_provenance, auf_provenance, count(r3) AS rq_provenance
MATCH ()-[r4:TYPISCH_BEI_MATERIAL {review_run: 'taxonomy_integration_2026_06_03'}]->()
WHERE r4.legacy_aufbereitung_id IS NOT NULL
WITH meth_provenance, auf_provenance, rq_provenance, count(r4) AS typisch_provenance
RETURN 'INFO' AS status,
       meth_provenance,      // expected ~74 (Akteur 58 + Software 9 + Tool 6 + Norm 1)
       auf_provenance,       // expected ~40 (ReuseRule)
       rq_provenance,        // expected ~1  (Materialdepot)
       typisch_provenance;   // expected ≤22 (post-dedupe)

// 5.10 (removed — DataIssue is empty post-cleanup, no dangling-pointer risk)

// 5.11 No mislabeled :Projekt with prog_ id remaining
MATCH (p:Projekt) WHERE p.id STARTS WITH 'prog_'
RETURN 'FAIL' AS status, p.id, p.name, 'should have been relabeled :Programm in P0.4' AS note;
// expected: 0 rows


// ---------- §6. Edge-property contract ----------

// 6.1 Every new-run edge carries the required audit properties
MATCH ()-[r {review_run: 'taxonomy_integration_2026_06_03'}]->()
WITH r,
     [r.evidence_basis, r.evidence_confidence, r.review_run, r.created_at] AS required
WHERE any(p IN required WHERE p IS NULL)
RETURN 'FAIL' AS status, type(r) AS rel_type, r.id AS rel_id,
       r.evidence_basis, r.evidence_confidence, r.created_at;
// expected: 0 rows

// 6.2 evidence_confidence values are within the controlled ladder
MATCH ()-[r {review_run: 'taxonomy_integration_2026_06_03'}]->()
WHERE NOT r.evidence_confidence IN ['belegt','wahrscheinlich','unsicher']
RETURN 'FAIL' AS status, type(r), r.id, r.evidence_confidence;
// expected: 0 rows  (no leaked HIGH/MEDIUM/LOW)

// 6.3 evidence_quote truncated to schema limit (240 chars)
MATCH ()-[r {review_run: 'taxonomy_integration_2026_06_03'}]->()
WHERE r.evidence_quote IS NOT NULL AND size(r.evidence_quote) > 240
RETURN 'FAIL' AS status, type(r), r.id, size(r.evidence_quote) AS too_long;
// expected: 0 rows


// ---------- §7. Coverage parity ----------

// 7.1 Every project covered by row-level batches has at least one new-axis edge
// (Project-id list comes from project_id_map.csv; here we use a heuristic:
//  every :Projekt that was touched by this run should have ≥1 outgoing new-axis edge
//  OR ≥1 Bauteilgruppe with one.)
WITH ['p_55_great_suffolk_street','p_awm_muenster_zirkulaer_3og','p_bluecity_offices_rotterdam'] AS sample_batch_ids
// (full list lives in project_id_map.csv; this query samples 3 from each batch in CI)
UNWIND sample_batch_ids AS batch_pid
MATCH (proj:Projekt) WHERE proj.name CONTAINS replace(replace(batch_pid,'p_',''),'_',' ')
OPTIONAL MATCH (proj)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)
  -[r {review_run: 'taxonomy_integration_2026_06_03'}]->()
WITH batch_pid, proj.id AS live_pid, count(r) AS new_edges
RETURN CASE WHEN new_edges > 0 THEN 'OK' ELSE 'CHECK' END AS status,
       batch_pid, live_pid, new_edges;

// 7.2 The two summary-only projects from coverage report §5.A
// Either: have row-level evidence (C14=fix-now) OR carry the pending tag (C14=defer)
MATCH (proj:Projekt)
WHERE proj.id IN ['k118_kopfbau_halle_118_winterthur','meduni_campus_mariannengasse']
   OR proj.name CONTAINS 'K118' OR proj.name CONTAINS 'Mariannengasse'
OPTIONAL MATCH (proj)-[:HAT_BAUTEILGRUPPE]->(bg)
  -[r {review_run: 'taxonomy_integration_2026_06_03'}]->()
WITH proj, count(r) AS new_edges, proj.pending_row_level_evidence AS pending_flag
RETURN CASE
  WHEN new_edges > 0 OR pending_flag = true THEN 'OK'
  ELSE 'FAIL' END AS status,
  proj.id, proj.name, new_edges, pending_flag;


// ---------- §8. Confidence distribution & spot-checks ----------

// 8.1 Confidence distribution matches batch totals (HIGH 1618 / MEDIUM 379 / LOW 243 expected, all 10 batches)
MATCH ()-[r {review_run: 'taxonomy_integration_2026_06_03'}]->()
WITH r.evidence_confidence AS conf, count(*) AS n
RETURN 'INFO' AS status, conf, n
ORDER BY n DESC;
// reference: HIGH→belegt 1618, MEDIUM→wahrscheinlich 379, LOW→unsicher 243  (batches 01–10)

// 8.2 Spot-check one canonical chain end-to-end: BlueCity reused window frames
MATCH (proj:Projekt {id: 'p_bluecity_offices_rotterdam'})
  -[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
WHERE bg.name CONTAINS 'window' OR bg.id CONTAINS 'window' OR bg.id CONTAINS 'fenster'
OPTIONAL MATCH (bg)-[:HAT_ERGEBNIS]->(erg:Wiederverwendungsergebnis)
OPTIONAL MATCH (bg)-[:HAT_RESSOURCENQUELLE]->(qu:Ressourcenquelle)
OPTIONAL MATCH (bg)-[:HAT_WIEDERVERWENDUNGSORT]->(loc:Wiederverwendungsort)
OPTIONAL MATCH (bg)-[:HAT_AUFBEREITUNG]->(av:Aufbereitungsverfahren)
RETURN 'SPOT' AS status,
       bg.id AS bauteilgruppe,
       collect(DISTINCT erg.id) AS ergebnis,
       collect(DISTINCT qu.id) AS quelle,
       collect(DISTINCT loc.id) AS ort,
       collect(DISTINCT av.id) AS aufbereitung;

// 8.3 Spot-check Methode migration on the Akteur side: an actor that used urban_mining
// should now point at meth_urban_mining_und_scouting with legacy provenance preserved
MATCH (a:Akteur)-[r:HAT_METHODE]->(m:Methode {id: 'meth_urban_mining_und_scouting'})
WHERE r.legacy_methode_id = 'meth_urban_mining'
RETURN 'SPOT' AS status, count(*) AS migrated_actors,
       'expected > 0 if any Akteur previously linked to meth_urban_mining' AS note
LIMIT 1;

// 8.4 Spot-check Aufbereitung outbound migration: drahtglasschneiden's TYPISCH_BEI_MATERIAL
// should now hang off av_zuschnitt_und_vereinzelung
MATCH (av:Aufbereitungsverfahren {id: 'av_zuschnitt_und_vereinzelung'})
  -[r:TYPISCH_BEI_MATERIAL]->(m:Material)
WHERE r.legacy_aufbereitung_id = 'av_drahtglasschneiden'
RETURN 'SPOT' AS status, m.id AS material, r.legacy_aufbereitung_id AS came_from;


// ---------- §9. Rollback rehearsal (read-only) ----------

// What would `DELETE` of this run touch? (No mutation; just counts.)
MATCH ()-[r {review_run: 'taxonomy_integration_2026_06_03'}]->()
RETURN 'INFO' AS status,
       type(r) AS rel_type,
       count(r) AS rels_that_would_be_deleted
ORDER BY rels_that_would_be_deleted DESC;

MATCH (n {review_run: 'taxonomy_integration_2026_06_03'})
RETURN 'INFO' AS status,
       labels(n) AS node_labels,
       count(n) AS nodes_that_would_be_deleted
ORDER BY nodes_that_would_be_deleted DESC;


// ---------- §10. Final smoke test ----------

// 10.1 Overall counts post-integration (compare against snapshot_pre_integration/)
MATCH (n) WITH count(n) AS total_nodes
MATCH ()-[r]->() WITH total_nodes, count(r) AS total_rels
RETURN 'INFO' AS status, total_nodes, total_rels;

// 10.2 Every Bauteilgruppe with batch coverage has all four axes filled
// (ergebnis OR quelle OR ort OR aufbereitung) — measures completeness, not failure
MATCH (bg:Bauteilgruppe)
  WHERE EXISTS { MATCH (bg)-[{review_run:'taxonomy_integration_2026_06_03'}]-() }
OPTIONAL MATCH (bg)-[:HAT_ERGEBNIS]->()              WITH bg, count(*) AS has_erg
OPTIONAL MATCH (bg)-[:HAT_RESSOURCENQUELLE]->()      WITH bg, has_erg, count(*) AS has_quelle
OPTIONAL MATCH (bg)-[:HAT_WIEDERVERWENDUNGSORT]->()  WITH bg, has_erg, has_quelle, count(*) AS has_ort
OPTIONAL MATCH (bg)-[:HAT_AUFBEREITUNG]->()          WITH bg, has_erg, has_quelle, has_ort, count(*) AS has_auf
RETURN 'INFO' AS status,
       sum(CASE WHEN has_erg    > 0 THEN 1 ELSE 0 END) AS bg_with_ergebnis,
       sum(CASE WHEN has_quelle > 0 THEN 1 ELSE 0 END) AS bg_with_quelle,
       sum(CASE WHEN has_ort    > 0 THEN 1 ELSE 0 END) AS bg_with_ort,
       sum(CASE WHEN has_auf    > 0 THEN 1 ELSE 0 END) AS bg_with_aufbereitung,
       count(bg) AS bg_touched_total;


// ---------- §11. Bauteilgruppe — final-plan-specific checks ----------

// 11.1 Total :Bauteilgruppe count after integration:
//   350 pre − 35 bg_reuse_ orphans − 35 non-reuse out-of-scope + 24 batch-new = 304
// Allow ±10 tolerance for resolver edge cases.
MATCH (n:Bauteilgruppe)
WITH count(n) AS total
RETURN CASE WHEN total >= 294 AND total <= 314 THEN 'OK' ELSE 'CHECK' END AS status,
       total AS bauteilgruppe_count,
       '~304 expected (350 pre − 35 bg_reuse_ orphans − 35 non-reuse + 24 batch-new)' AS note;

// 11.1b Every surviving :Bauteilgruppe is bg_reuse_* — no non-reuse prefixes remain
MATCH (n:Bauteilgruppe)
WHERE NOT n.id STARTS WITH 'bg_reuse_'
RETURN 'FAIL' AS status, n.id, n.name,
       'non-reuse :Bauteilgruppe survives — Phase 6.4c should have deleted' AS note;
// expected: 0 rows

// 11.2 No :Projekt slipped through with prog_* id (P0.4 should have relabeled them)
MATCH (p:Projekt) WHERE p.id STARTS WITH 'prog_'
RETURN 'FAIL' AS status, p.id, p.name, 'should have been relabeled to :Programm in P0.4' AS note;
// expected: 0 rows

// 11.3 No bg_reuse_* survives without batch evidence
// After Phase 6.4b deletes the 35 bg_reuse_ orphans, every remaining bg_reuse_*
// must carry at least one batch-run edge. Surface the failures as FAIL.
MATCH (bg:Bauteilgruppe)
WHERE bg.id STARTS WITH 'bg_reuse_'
  AND NOT EXISTS {
        MATCH (bg)-[r {review_run: 'taxonomy_integration_2026_06_03'}]->()
        WHERE type(r) IN ['HAT_ERGEBNIS','HAT_WIEDERVERWENDUNGSORT',
                          'HAT_METHODE','HAT_AUFBEREITUNG',
                          'HAT_RESSOURCENQUELLE','HAT_RUECKBAUVERFAHREN']
      }
RETURN 'FAIL' AS status, bg.id, bg.name,
       'bg_reuse_* without batch evidence — Phase 6.4b should have deleted this' AS note;
// expected: 0 rows

// 11.3b (removed — non-reuse BGs are no longer kept; see 11.1b which asserts zero survive)

// 11.4 Probable slug-drift duplicates per project — INFO only
// For each project, list BGs with same material+bauteiltyp prefix (likely duplicates).
// Surfaces the accepted cost of skipping the resolver.
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
WITH p, split(bg.id, '_') AS toks, bg
WHERE size(toks) >= 4
WITH p.id AS project,
     toks[0] + '_' + toks[1] + '_' + toks[2] + '_' + toks[3] AS material_typ_prefix,
     collect(bg.id) AS slugs
WHERE size(slugs) > 1
RETURN 'INFO' AS status, project, material_typ_prefix, slugs,
       size(slugs) AS multiplicity,
       'BGs sharing material+bauteiltyp prefix in same project may be slug-drift duplicates' AS note
ORDER BY multiplicity DESC, project LIMIT 30;
