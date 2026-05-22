// =====================================================================
// Phase 6.5 + 6.6 — Delete old vocab nodes + drop retired constraint
//
// Phase 6.5: hard-delete every remaining old vocab node. After Phase 6.1
// (migrate non-replaceable upstreams), Phase 6.2 (migrate outbound), and
// Phase 6.3 (delete replaceable edges), these nodes should be detached
// and safe to DELETE.
//
// Phase 6.6: drop the constraint for the retired :WiederverwendungsArt
// label.
// =====================================================================


// ---------- §1. Sanity: any old vocab node still has edges? ----------

// 1.1 Old :Methode with leftover edges
MATCH (n:Methode)
WHERE NOT n.id IN ['meth_urban_mining_und_scouting','meth_bestands_und_reuse_assessment',
                   'meth_verfuegbarkeitsbasiertes_design','meth_reversibles_design',
                   'meth_zirkulaere_beschaffung','meth_dokumentation_und_monitoring']
  AND (n)-[]-()
RETURN 'FAIL' AS status, 'Methode' AS lbl, n.id,
       count{ (n)-[]-() } AS edges_remaining;
// expected: 0 rows. If any survive, P6.1 missed a case — investigate before P6.5 deletes.

// 1.2 Old :Aufbereitungsverfahren with leftover edges
MATCH (n:Aufbereitungsverfahren)
WHERE NOT n.id IN ['av_reinigung_und_oberflaeche','av_zuschnitt_und_vereinzelung',
                   'av_pruefung_sortierung_qs','av_reparatur_und_refurbishment',
                   'av_remanufacturing_und_upcycling','av_verstaerkung_und_schutz']
  AND (n)-[]-()
RETURN 'FAIL' AS status, 'Aufbereitungsverfahren' AS lbl, n.id,
       count{ (n)-[]-() } AS edges_remaining;
// expected: 0 rows

// 1.3 Old :Ressourcenquelle with leftover edges
MATCH (n:Ressourcenquelle)
WHERE NOT n.id IN ['rq_externer_spenderbau','rq_eigener_bestand','rq_gleicher_standort',
                   'rq_bauteilmarkt_oder_lager','rq_leihgabe_oder_service','rq_restposten_abfall_unbekannt']
  AND (n)-[]-()
RETURN 'FAIL' AS status, 'Ressourcenquelle' AS lbl, n.id,
       count{ (n)-[]-() } AS edges_remaining;
// expected: 0 rows

// 1.4 :Rueckbauverfahren rv_betonfraesen — should have no edges after P6.3
MATCH (n:Rueckbauverfahren {id: 'rv_betonfraesen'})
WHERE (n)-[]-()
RETURN 'FAIL' AS status, 'Rueckbauverfahren rv_betonfraesen' AS lbl,
       count{ (n)-[]-() } AS edges_remaining;
// expected: 0 rows

// 1.5 :WiederverwendungsArt — should have no edges after P6.3
MATCH (n:WiederverwendungsArt)
WHERE (n)-[]-()
RETURN 'FAIL' AS status, 'WiederverwendungsArt' AS lbl, n.id,
       count{ (n)-[]-() } AS edges_remaining;
// expected: 0 rows


// ---------- §2. Apply: delete old vocab nodes ----------

// 2.1 Delete old :Methode (13 expected)
MATCH (n:Methode)
WHERE NOT n.id IN ['meth_urban_mining_und_scouting','meth_bestands_und_reuse_assessment',
                   'meth_verfuegbarkeitsbasiertes_design','meth_reversibles_design',
                   'meth_zirkulaere_beschaffung','meth_dokumentation_und_monitoring']
DETACH DELETE n;

// 2.2 Delete old :Aufbereitungsverfahren (up to 62 expected)
MATCH (n:Aufbereitungsverfahren)
WHERE NOT n.id IN ['av_reinigung_und_oberflaeche','av_zuschnitt_und_vereinzelung',
                   'av_pruefung_sortierung_qs','av_reparatur_und_refurbishment',
                   'av_remanufacturing_und_upcycling','av_verstaerkung_und_schutz']
DETACH DELETE n;

// 2.3 Delete old :Ressourcenquelle (16 expected)
MATCH (n:Ressourcenquelle)
WHERE NOT n.id IN ['rq_externer_spenderbau','rq_eigener_bestand','rq_gleicher_standort',
                   'rq_bauteilmarkt_oder_lager','rq_leihgabe_oder_service','rq_restposten_abfall_unbekannt']
DETACH DELETE n;

// 2.4 Delete rv_betonfraesen
MATCH (n:Rueckbauverfahren {id: 'rv_betonfraesen'})
DETACH DELETE n;

// 2.5 Delete all :WiederverwendungsArt nodes (11 expected — entire axis retires)
MATCH (n:WiederverwendungsArt)
DETACH DELETE n;


// ---------- §3. Post-checks ----------

// 3.1 Exactly 6 :Methode survive
MATCH (n:Methode)
WITH collect(n.id) AS ids
RETURN CASE WHEN size(ids) = 6
              AND all(id IN ids WHERE id IN ['meth_urban_mining_und_scouting','meth_bestands_und_reuse_assessment',
                                              'meth_verfuegbarkeitsbasiertes_design','meth_reversibles_design',
                                              'meth_zirkulaere_beschaffung','meth_dokumentation_und_monitoring'])
            THEN 'OK' ELSE 'FAIL' END AS status,
       ids AS methode_ids;

// 3.2 Exactly 6 :Aufbereitungsverfahren survive
MATCH (n:Aufbereitungsverfahren)
WITH collect(n.id) AS ids
RETURN CASE WHEN size(ids) = 6 THEN 'OK' ELSE 'FAIL' END AS status,
       ids AS aufbereitung_ids;

// 3.3 Exactly 6 :Ressourcenquelle survive
MATCH (n:Ressourcenquelle)
WITH collect(n.id) AS ids
RETURN CASE WHEN size(ids) = 6 THEN 'OK' ELSE 'FAIL' END AS status,
       ids AS ressourcenquelle_ids;

// 3.4 Exactly 6 :Rueckbauverfahren survive
MATCH (n:Rueckbauverfahren)
WITH collect(n.id) AS ids
RETURN CASE WHEN size(ids) = 6 THEN 'OK' ELSE 'FAIL' END AS status,
       ids AS rueckbauverfahren_ids;

// 3.5 Zero :WiederverwendungsArt remain
MATCH (n:WiederverwendungsArt)
RETURN CASE WHEN count(n) = 0 THEN 'OK' ELSE 'FAIL' END AS status,
       count(n) AS wva_remaining;


// ---------- §4. Phase 6.6 — drop :WiederverwendungsArt constraint ----------

// 4.1 Pre-check: list any WiederverwendungsArt-related constraints
SHOW CONSTRAINTS YIELD name, labelsOrTypes
WHERE 'WiederverwendungsArt' IN labelsOrTypes
RETURN name;
// expected: wiederverwendungsart_id (1 row)

// 4.2 Drop the constraint
DROP CONSTRAINT wiederverwendungsart_id IF EXISTS;

// 4.3 Post-check
SHOW CONSTRAINTS YIELD name, labelsOrTypes
WHERE 'WiederverwendungsArt' IN labelsOrTypes
RETURN CASE WHEN count(*) = 0 THEN 'OK' ELSE 'FAIL' END AS status,
       count(*) AS wva_constraints_remaining;
