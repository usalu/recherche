// Verify the digital-barriers taxonomy integration (read-only).
// Convention: assertion rows return status='OK' else 'FAIL'; anomaly queries must return 0 rows.
// Run: python _scripts/_run_cypher_file.py --cypher <this file>
// Framework nodes are identified by having a barriere_code property.

// 1. Exactly 8 domain roots (:HuerdeKategorie with no parent edge, single-letter code).
MATCH (d:HuerdeKategorie) WHERE d.barriere_code IS NOT NULL AND NOT (d)-[:HAT_HUERDEKATEGORIE]->()
RETURN '1_domains' AS check, CASE WHEN count(d)=8 THEN 'OK' ELSE 'FAIL' END AS status, count(d) AS n;

// 2. Every non-domain framework node has EXACTLY ONE parent (0 anomaly rows expected).
MATCH (n) WHERE n.barriere_code IS NOT NULL AND n.barriere_code =~ '.*[0-9].*'
WITH n, size([(n)-[:HAT_HUERDEKATEGORIE]->() | 1]) AS parents
WHERE parents <> 1
RETURN '2_parent_anomaly' AS check, n.barriere_code AS code, n.id AS id, parents;

// 3. Every framework node (has barriere_code) is marked :BarriereReferenz (0 rows expected).
MATCH (n) WHERE n.barriere_code IS NOT NULL AND NOT n:BarriereReferenz
RETURN '3_missing_marker' AS check, n.id AS id;

// 4. The 9 observed hurdles must NOT be marked and must have no barriere_code (0 rows expected).
MATCH (h:Huerde) WHERE h.id IN [
  'h_akzeptanzproblem','h_heterogenitaet_chargen','h_unkonventionelles_material',
  'h_mengenunsicherheit','h_verfuegbarkeitsproblem','h_terminunsicherheit',
  'h_aufbereitungsaufwand','h_witterung_feuchte','h_fehlende_lagerflaeche']
  AND (h:BarriereReferenz OR h.barriere_code IS NOT NULL)
RETURN '4_observed_wrongly_marked' AS check, h.id AS id;

// 5. Total observed HAT_HUERDE edges = 204 (237 - 33 dropped), all targeting :Huerde leaves.
MATCH ()-[r:HAT_HUERDE]->(h:Huerde)
RETURN '5_hat_huerde_total' AS check,
  CASE WHEN count(r)=204 THEN 'OK' ELSE 'CHECK' END AS status, count(r) AS n;

// 6. No HAT_HUERDE points at a category node (0 rows expected).
MATCH ()-[:HAT_HUERDE]->(h) WHERE h:HuerdeKategorie AND NOT h:Huerde
RETURN '6_huerde_targets_category' AS check, h.id AS id;

// 7. Dropped nodes are gone (0 rows expected). Fehlende_Lagerflaeche is KEPT (reclassified).
MATCH (n) WHERE n.id IN ['h_entwurfsbindung','h_ausschreibungsproblem']
RETURN '7_removed_present' AS check, n.id AS id;

// 8. The 9 reclassified hurdles: no leftover category, exactly one parent (0 rows expected).
MATCH (h:Huerde) WHERE h.id IN [
  'h_akzeptanzproblem','h_heterogenitaet_chargen','h_unkonventionelles_material',
  'h_mengenunsicherheit','h_verfuegbarkeitsproblem','h_terminunsicherheit',
  'h_aufbereitungsaufwand','h_witterung_feuchte','h_fehlende_lagerflaeche']
WITH h, size([(h)-[:HAT_HUERDEKATEGORIE]->() | 1]) AS parents
WHERE h.category IS NOT NULL OR parents <> 1
RETURN '8_reclassify_anomaly' AS check, h.id AS id, h.category AS category, parents;

// 9. ID-prefix purity for framework nodes (0 rows expected).
MATCH (n) WHERE n.barriere_code IS NOT NULL AND NOT (n.id STARTS WITH 'h_' OR n.id STARTS WITH 'huek_')
RETURN '9_bad_id_prefix' AS check, n.id AS id;

// 10. Rollback rehearsal — what a review_run cleanup would touch (informational).
MATCH (n {review_run:'digital_barriers_2026_08_06'})
RETURN '10_rollback_nodes' AS check, count(n) AS taxonomy_nodes;
MATCH ()-[r {review_run:'digital_barriers_2026_08_06'}]->()
RETURN '10_rollback_rels' AS check, count(r) AS review_run_rels;
