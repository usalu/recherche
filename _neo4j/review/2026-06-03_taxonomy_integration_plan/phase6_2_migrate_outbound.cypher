// =====================================================================
// Phase 6.2 — Migrate outbound edges from old :Aufbereitungsverfahren
//
// Two outbound rel types live on :Aufbereitungsverfahren and would be lost
// if we hard-deleted the old av_* nodes without first preserving them:
//
//   (:Aufbereitungsverfahren)-[:TYPISCH_BEI_MATERIAL]->(:Material)   ~22
//   (:Aufbereitungsverfahren)-[:BELEGT_IN]->(:Quelle:ResearchDocument) ~25
//
// Reattach onto the new canonical (via the same aufb_map as P6.1).
// MERGE dedupes when multiple old av_* collapse to one new canonical
// (e.g. av_drahtglasschneiden + av_zuschnitt both → av_zuschnitt_und_vereinzelung
//  and both have TYPISCH_BEI_MATERIAL → mat_glas would dedupe).
//
// Uses the same $aufb_map as Phase 6.1.
// =====================================================================

:param aufb_map => {
  av_reinigung:                              'av_reinigung_und_oberflaeche',
  av_beton_anhaftungen_entfernen:            'av_reinigung_und_oberflaeche',
  av_glas_reinigung_entkitten:               'av_reinigung_und_oberflaeche',
  av_aluminium_reinigung_entdichtung:        'av_reinigung_und_oberflaeche',
  av_naturstein_reinigung_schleifen_zuschnitt: 'av_reinigung_und_oberflaeche',
  av_moertelentfernung_ziegel:               'av_reinigung_und_oberflaeche',
  av_lehm_sieben_mischen:                    'av_reinigung_und_oberflaeche',
  av_hobeln_schleifen_holz:                  'av_reinigung_und_oberflaeche',
  av_sandstrahlen:                           'av_reinigung_und_oberflaeche',
  av_entrosten_korrosionsbehandlung:         'av_reinigung_und_oberflaeche',
  av_korrosionsschutz_beschichten:           'av_reinigung_und_oberflaeche',
  av_oberflaechenbehandlung_metall:          'av_reinigung_und_oberflaeche',
  av_zuschnitt:                              'av_zuschnitt_und_vereinzelung',
  av_drahtglasschneiden:                     'av_zuschnitt_und_vereinzelung',
  av_entmoertelung_von_fliesen:              'av_zuschnitt_und_vereinzelung',
  av_holz_zuschnitt_reparatur:               'av_zuschnitt_und_vereinzelung',
  av_betonfertigteil_saegen:                 'av_zuschnitt_und_vereinzelung',
  av_mauerwerk_diamantsaegen_modul:          'av_zuschnitt_und_vereinzelung',
  av_stahl_zuschnitt_bohrung:                'av_zuschnitt_und_vereinzelung',
  av_daemmstoff_zuschnitt:                   'av_zuschnitt_und_vereinzelung',
  av_qualitaetssicherung:                    'av_pruefung_sortierung_qs',
  av_holz_festigkeitssortierung:             'av_pruefung_sortierung_qs',
  av_glas_pruefung_sortierung:               'av_pruefung_sortierung_qs',
  av_betonfertigteil_tagging_sortierung:     'av_pruefung_sortierung_qs',
  av_aluminiumfenster_pruefung_sortierung:   'av_pruefung_sortierung_qs',
  av_holz_trocknung_feuchtekonditionierung:  'av_pruefung_sortierung_qs',
  av_reparatur:                              'av_reparatur_und_refurbishment',
  av_rekonditionierung:                      'av_reparatur_und_refurbishment',
  av_leuchten_refurbishment:                 'av_reparatur_und_refurbishment',
  av_fenster_refurbishment:                  'av_reparatur_und_refurbishment',
  av_aluminiumfenster_beschlag_dichtung:     'av_reparatur_und_refurbishment',
  av_remanufacturing:                        'av_remanufacturing_und_upcycling',
  av_holzaufbereitung:                       'av_remanufacturing_und_upcycling',
  av_verstaerkung:                           'av_verstaerkung_und_schutz'
};


// ---------- §1. TYPISCH_BEI_MATERIAL ----------

MATCH (av_old:Aufbereitungsverfahren)-[r_old:TYPISCH_BEI_MATERIAL]->(mat:Material)
WHERE av_old.id IN keys($aufb_map)
WITH av_old, r_old, mat, $aufb_map[av_old.id] AS new_id
MATCH (av_new:Aufbereitungsverfahren {id: new_id})
MERGE (av_new)-[r_new:TYPISCH_BEI_MATERIAL]->(mat)
ON CREATE SET r_new.evidence_basis           = r_old.evidence_basis,
              r_new.evidence_confidence      = r_old.evidence_confidence,
              r_new.evidence_url             = r_old.evidence_url,
              r_new.evidence_quote           = r_old.evidence_quote,
              r_new.evidence_source_id       = r_old.evidence_source_id,
              r_new.legacy_aufbereitung_id   = av_old.id,
              r_new.legacy_aufbereitung_name = av_old.name,
              r_new.legacy_rel_id            = r_old.id,
              r_new.review_run               = 'taxonomy_integration_2026_06_03_phase6_2',
              r_new.migrated_at              = datetime()
DELETE r_old;


// ---------- §2. BELEGT_IN ----------

MATCH (av_old:Aufbereitungsverfahren)-[r_old:BELEGT_IN]->(q)
WHERE av_old.id IN keys($aufb_map)
  AND (q:Quelle OR q:ResearchDocument)
WITH av_old, r_old, q, $aufb_map[av_old.id] AS new_id
MATCH (av_new:Aufbereitungsverfahren {id: new_id})
MERGE (av_new)-[r_new:BELEGT_IN]->(q)
ON CREATE SET r_new.evidence_basis           = r_old.evidence_basis,
              r_new.evidence_confidence      = r_old.evidence_confidence,
              r_new.evidence_url             = r_old.evidence_url,
              r_new.evidence_quote           = r_old.evidence_quote,
              r_new.legacy_aufbereitung_id   = av_old.id,
              r_new.legacy_aufbereitung_name = av_old.name,
              r_new.legacy_rel_id            = r_old.id,
              r_new.review_run               = 'taxonomy_integration_2026_06_03_phase6_2',
              r_new.migrated_at              = datetime()
DELETE r_old;


// ---------- §3. Post-checks ----------

// 3.1 Old av_* should now have zero outbound edges (TYPISCH_BEI_MATERIAL + BELEGT_IN)
MATCH (av_old:Aufbereitungsverfahren)-[r:TYPISCH_BEI_MATERIAL|BELEGT_IN]->()
WHERE av_old.id IN keys($aufb_map)
RETURN 'FAIL' AS status, av_old.id, type(r), count(r) AS remaining;
// expected: 0 rows

// 3.2 New canonical have inherited the rels (deduped)
MATCH (av_new:Aufbereitungsverfahren {source_scope: 'controlled_vocab_seed'})
       -[r:TYPISCH_BEI_MATERIAL|BELEGT_IN]->()
RETURN 'INFO' AS status, av_new.id, type(r) AS rel, count(r) AS edges_inherited
ORDER BY av_new.id, rel;
