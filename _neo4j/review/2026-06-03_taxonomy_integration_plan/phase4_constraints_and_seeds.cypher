// =====================================================================
// Phase 4 — Constraints + canonical seed nodes
//
// Idempotent. Run before Phase 5.
// review_run = 'taxonomy_integration_2026_06_03'
// =====================================================================


// ---------- §1. New constraints ----------

// Node uniqueness on the two brand-new labels
CREATE CONSTRAINT wiederverwendungsergebnis_id IF NOT EXISTS
  FOR (n:Wiederverwendungsergebnis) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT wiederverwendungsort_id IF NOT EXISTS
  FOR (n:Wiederverwendungsort) REQUIRE n.id IS UNIQUE;

// Relationship uniqueness on the new rel types
CREATE CONSTRAINT rel_hat_ergebnis_id IF NOT EXISTS
  FOR ()-[r:HAT_ERGEBNIS]-() REQUIRE r.id IS UNIQUE;

CREATE CONSTRAINT rel_hat_wiederverwendungsort_id IF NOT EXISTS
  FOR ()-[r:HAT_WIEDERVERWENDUNGSORT]-() REQUIRE r.id IS UNIQUE;

CREATE CONSTRAINT rel_angewendet_auf_id IF NOT EXISTS
  FOR ()-[r:ANGEWENDET_AUF]-() REQUIRE r.id IS UNIQUE;


// ---------- §2. Six new :Methode canonical (per C2) ----------

UNWIND [
  ['meth_urban_mining_und_scouting',       'Urban_Mining_und_Scouting'],
  ['meth_bestands_und_reuse_assessment',   'Bestands_und_ReUse_Assessment'],
  ['meth_verfuegbarkeitsbasiertes_design', 'Verfuegbarkeitsbasiertes_Design'],
  ['meth_reversibles_design',              'Reversibles_Design'],
  ['meth_zirkulaere_beschaffung',          'Zirkulaere_Beschaffung'],
  ['meth_dokumentation_und_monitoring',    'Dokumentation_und_Monitoring']
] AS row
MERGE (n:Methode {id: row[0]})
ON CREATE SET n.name           = row[1],
              n.source_scope   = 'controlled_vocab_seed',
              n.evidence_basis = 'taxonomy_integration_2026_06_03',
              n.review_run     = 'taxonomy_integration_2026_06_03',
              n.created_at     = datetime();


// ---------- §3. Six new :Aufbereitungsverfahren canonical (per C4) ----------

UNWIND [
  ['av_reinigung_und_oberflaeche',      'Reinigung_und_Oberflaeche'],
  ['av_zuschnitt_und_vereinzelung',     'Zuschnitt_und_Vereinzelung'],
  ['av_pruefung_sortierung_qs',         'Pruefung_Sortierung_QS'],
  ['av_reparatur_und_refurbishment',    'Reparatur_und_Refurbishment'],
  ['av_remanufacturing_und_upcycling',  'Remanufacturing_und_Upcycling'],
  ['av_verstaerkung_und_schutz',        'Verstaerkung_und_Schutz']
] AS row
MERGE (n:Aufbereitungsverfahren {id: row[0]})
ON CREATE SET n.name           = row[1],
              n.source_scope   = 'controlled_vocab_seed',
              n.evidence_basis = 'taxonomy_integration_2026_06_03',
              n.review_run     = 'taxonomy_integration_2026_06_03',
              n.created_at     = datetime();


// ---------- §4. Six new :Ressourcenquelle canonical (per C1 revised) ----------

UNWIND [
  ['rq_externer_spenderbau',         'Externer_Spenderbau'],
  ['rq_eigener_bestand',             'Eigener_Bestand'],
  ['rq_gleicher_standort',           'Gleicher_Standort'],
  ['rq_bauteilmarkt_oder_lager',     'Bauteilmarkt_oder_Lager'],
  ['rq_leihgabe_oder_service',       'Leihgabe_oder_Service'],
  ['rq_restposten_abfall_unbekannt', 'Restposten_Abfall_Unbekannt']
] AS row
MERGE (n:Ressourcenquelle {id: row[0]})
ON CREATE SET n.name           = row[1],
              n.source_scope   = 'controlled_vocab_seed',
              n.evidence_basis = 'taxonomy_integration_2026_06_03',
              n.review_run     = 'taxonomy_integration_2026_06_03',
              n.created_at     = datetime();


// ---------- §5. Two new :Rueckbauverfahren canonical (per C3) ----------
// (the other 4 — rv_selektiver_rueckbau, rv_ausbau_von_bauteilen,
// rv_demontage, rv_zerstoerungsarme_bergung — already exist; only add the 2 new)

UNWIND [
  ['rv_schneidender_rueckbau',          'Schneidender_Rueckbau'],
  ['rv_integrierter_rueckbau_und_lagerung', 'Integrierter_Rueckbau_und_Lagerung']
] AS row
MERGE (n:Rueckbauverfahren {id: row[0]})
ON CREATE SET n.name           = row[1],
              n.source_scope   = 'controlled_vocab_seed',
              n.evidence_basis = 'taxonomy_integration_2026_06_03',
              n.review_run     = 'taxonomy_integration_2026_06_03',
              n.created_at     = datetime();


// ---------- §6. Six brand-new :Wiederverwendungsergebnis canonical ----------

UNWIND [
  ['wver_bestandserhalt',         'Bestandserhalt'],
  ['wver_wv_gleiche_funktion',    'Wiederverwendung_gleiche_Funktion'],
  ['wver_wv_neue_funktion',       'Wiederverwendung_neue_Funktion'],
  ['wver_modul_oder_abschnittswv','Modul_oder_Abschnittswiederverwendung'],
  ['wver_material_reprocessing',  'Material_Reprocessing'],
  ['wver_geplant_oder_gelagert',  'Geplant_oder_Gelagert']
] AS row
MERGE (n:Wiederverwendungsergebnis {id: row[0]})
ON CREATE SET n.name           = row[1],
              n.source_scope   = 'controlled_vocab_seed',
              n.evidence_basis = 'taxonomy_integration_2026_06_03',
              n.review_run     = 'taxonomy_integration_2026_06_03',
              n.created_at     = datetime();


// ---------- §7. Six brand-new :Wiederverwendungsort canonical ----------

UNWIND [
  ['wvo_in_situ',                        'In_situ'],
  ['wvo_im_selben_gebaeude_versetzt',    'Im_selben_Gebaeude_versetzt'],
  ['wvo_auf_demselben_standort_versetzt','Auf_demselben_Standort_versetzt'],
  ['wvo_extern_importiert',              'Extern_importiert'],
  ['wvo_temporaer_oder_zurueckgegeben',  'Temporaer_oder_zurueckgegeben'],
  ['wvo_gelagert_oder_unbekannt',        'Gelagert_oder_Unbekannt']
] AS row
MERGE (n:Wiederverwendungsort {id: row[0]})
ON CREATE SET n.name           = row[1],
              n.source_scope   = 'controlled_vocab_seed',
              n.evidence_basis = 'taxonomy_integration_2026_06_03',
              n.review_run     = 'taxonomy_integration_2026_06_03',
              n.created_at     = datetime();


// ---------- §8. Post-check ----------

MATCH (n:Methode)                  WHERE n.review_run = 'taxonomy_integration_2026_06_03' WITH count(n) AS c_meth
MATCH (n:Aufbereitungsverfahren)   WHERE n.review_run = 'taxonomy_integration_2026_06_03' WITH c_meth, count(n) AS c_av
MATCH (n:Ressourcenquelle)         WHERE n.review_run = 'taxonomy_integration_2026_06_03' WITH c_meth, c_av, count(n) AS c_rq
MATCH (n:Rueckbauverfahren)        WHERE n.review_run = 'taxonomy_integration_2026_06_03' WITH c_meth, c_av, c_rq, count(n) AS c_rv
MATCH (n:Wiederverwendungsergebnis) WHERE n.review_run = 'taxonomy_integration_2026_06_03' WITH c_meth, c_av, c_rq, c_rv, count(n) AS c_wver
MATCH (n:Wiederverwendungsort)     WHERE n.review_run = 'taxonomy_integration_2026_06_03' WITH c_meth, c_av, c_rq, c_rv, c_wver, count(n) AS c_wvo
RETURN
  CASE WHEN c_meth = 6 AND c_av = 6 AND c_rq = 6 AND c_rv = 2
         AND c_wver = 6 AND c_wvo = 6
       THEN 'OK' ELSE 'FAIL' END AS status,
  c_meth AS methode_seeded,
  c_av   AS aufbereitung_seeded,
  c_rq   AS ressourcenquelle_seeded,
  c_rv   AS rueckbauverfahren_seeded,
  c_wver AS ergebnis_seeded,
  c_wvo  AS ort_seeded;
// expected: status='OK', meth=6, av=6, rq=6, rv=2, wver=6, wvo=6  (= 32 new seed nodes)


// ---------- §9. Rollback ----------
// Run only if you need to undo this phase BEFORE phase 5 runs (the seeds get
// edges in phase 5, after which DETACH DELETE is required).
//
// MATCH (n) WHERE n.review_run = 'taxonomy_integration_2026_06_03'
//   AND (n:Methode OR n:Aufbereitungsverfahren OR n:Ressourcenquelle
//        OR n:Rueckbauverfahren OR n:Wiederverwendungsergebnis OR n:Wiederverwendungsort)
//   AND NOT (n)-[]-()  // safety: only drop if no edges yet
// DELETE n;
// DROP CONSTRAINT wiederverwendungsergebnis_id IF EXISTS;
// DROP CONSTRAINT wiederverwendungsort_id IF EXISTS;
// DROP CONSTRAINT rel_hat_ergebnis_id IF EXISTS;
// DROP CONSTRAINT rel_hat_wiederverwendungsort_id IF EXISTS;
// DROP CONSTRAINT rel_angewendet_auf_id IF EXISTS;
