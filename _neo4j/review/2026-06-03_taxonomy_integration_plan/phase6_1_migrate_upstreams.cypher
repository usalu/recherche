// =====================================================================
// Phase 6.1 — Migrate non-replaceable upstream edges
//
// Reattach edges from upstream node types that batches DON'T re-supply
// (Akteur, Software, Tool, Norm, Programm, ReuseRule, Materialdepot)
// to the new canonical vocab nodes.
//
// IMPORTANT: don't copy r.id from old → new edge (would collide with
// the unique-id constraint while both exist). Set properties explicitly
// and leave r.id NULL on migrated edges (constraints allow NULL).
// Set legacy_*_id provenance + review_run tag for rollback/audit.
// =====================================================================

:param method_map => {
  meth_urban_mining:                'meth_urban_mining_und_scouting',
  meth_building_material_scouting:  'meth_urban_mining_und_scouting',
  meth_reuse_assessment:            'meth_bestands_und_reuse_assessment',
  meth_pre_deconstruction_audit:    'meth_bestands_und_reuse_assessment',
  meth_form_follows_availability:   'meth_verfuegbarkeitsbasiertes_design',
  meth_wiederverwendungskriterien:  'meth_verfuegbarkeitsbasiertes_design',
  meth_design_for_disassembly:      'meth_reversibles_design',
  meth_reversibilitaet:             'meth_reversibles_design',
  meth_reuse_ausschreibung:         'meth_zirkulaere_beschaffung',
  meth_zirkulaere_ausschreibung:    'meth_zirkulaere_beschaffung',
  meth_bauteilkatalogisierung:      'meth_dokumentation_und_monitoring',
  meth_materialinventur:            'meth_dokumentation_und_monitoring',
  meth_abrissmonitoring:            'meth_dokumentation_und_monitoring'
};


// ---------- §1. :Methode migration ----------

MATCH (upstream)-[r_old:HAT_METHODE]->(meth_old:Methode)
WHERE NOT upstream:Bauteilgruppe AND NOT upstream:Projekt
  AND meth_old.id IN keys($method_map)
WITH upstream, r_old, meth_old, $method_map[meth_old.id] AS new_id
MATCH (meth_new:Methode {id: new_id})
MERGE (upstream)-[r_new:HAT_METHODE]->(meth_new)
ON CREATE SET r_new.evidence_basis      = r_old.evidence_basis,
              r_new.evidence_confidence = r_old.evidence_confidence,
              r_new.evidence_url        = r_old.evidence_url,
              r_new.evidence_quote      = r_old.evidence_quote,
              r_new.evidence_source_id  = r_old.evidence_source_id,
              r_new.legacy_methode_id   = meth_old.id,
              r_new.legacy_methode_name = meth_old.name,
              r_new.legacy_rel_id       = r_old.id,
              r_new.review_run          = 'taxonomy_integration_2026_06_03_phase6_1',
              r_new.migrated_at         = datetime()
DELETE r_old;


// ---------- §2. :Aufbereitungsverfahren migration ----------

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

MATCH (upstream)-[r_old:HAT_AUFBEREITUNG]->(av_old:Aufbereitungsverfahren)
WHERE NOT upstream:Bauteilgruppe AND NOT upstream:Projekt
  AND av_old.id IN keys($aufb_map)
WITH upstream, r_old, av_old, $aufb_map[av_old.id] AS new_id
MATCH (av_new:Aufbereitungsverfahren {id: new_id})
MERGE (upstream)-[r_new:HAT_AUFBEREITUNG]->(av_new)
ON CREATE SET r_new.evidence_basis           = r_old.evidence_basis,
              r_new.evidence_confidence      = r_old.evidence_confidence,
              r_new.evidence_url             = r_old.evidence_url,
              r_new.evidence_quote           = r_old.evidence_quote,
              r_new.evidence_source_id       = r_old.evidence_source_id,
              r_new.legacy_aufbereitung_id   = av_old.id,
              r_new.legacy_aufbereitung_name = av_old.name,
              r_new.legacy_rel_id            = r_old.id,
              r_new.review_run               = 'taxonomy_integration_2026_06_03_phase6_1',
              r_new.migrated_at              = datetime()
DELETE r_old;


// ---------- §3. :Ressourcenquelle migration ----------

:param rq_map => {
  rq_donorgebaeude:              'rq_externer_spenderbau',
  rq_donor_infrastruktur:        'rq_externer_spenderbau',
  rq_baustelle:                  'rq_eigener_bestand',
  rq_bauteilboerse:              'rq_bauteilmarkt_oder_lager',
  rq_haendler:                   'rq_bauteilmarkt_oder_lager',
  rq_lager:                      'rq_bauteilmarkt_oder_lager',
  rq_supplier_stock:             'rq_bauteilmarkt_oder_lager',
  rq_materialstockpile:          'rq_bauteilmarkt_oder_lager',
  rq_borrowed_material_pool:     'rq_leihgabe_oder_service',
  rq_produktionsueberschuss:     'rq_restposten_abfall_unbekannt',
  rq_reclaimed_stock:            'rq_restposten_abfall_unbekannt',
  rq_surplus_stock:              'rq_restposten_abfall_unbekannt',
  rq_construction_waste_stream:  'rq_restposten_abfall_unbekannt',
  rq_demolition_waste_stream:    'rq_restposten_abfall_unbekannt',
  rq_unbekannt:                  'rq_restposten_abfall_unbekannt',
  rq_unknown_documented_source:  'rq_restposten_abfall_unbekannt'
};

MATCH (upstream)-[r_old:HAT_RESSOURCENQUELLE]->(rq_old:Ressourcenquelle)
WHERE NOT upstream:Bauteilgruppe AND NOT upstream:Projekt
  AND rq_old.id IN keys($rq_map)
WITH upstream, r_old, rq_old, $rq_map[rq_old.id] AS new_id
MATCH (rq_new:Ressourcenquelle {id: new_id})
MERGE (upstream)-[r_new:HAT_RESSOURCENQUELLE]->(rq_new)
ON CREATE SET r_new.evidence_basis               = r_old.evidence_basis,
              r_new.evidence_confidence          = r_old.evidence_confidence,
              r_new.evidence_url                 = r_old.evidence_url,
              r_new.evidence_quote               = r_old.evidence_quote,
              r_new.evidence_source_id           = r_old.evidence_source_id,
              r_new.legacy_ressourcenquelle_id   = rq_old.id,
              r_new.legacy_ressourcenquelle_name = rq_old.name,
              r_new.legacy_rel_id                = r_old.id,
              r_new.review_run                   = 'taxonomy_integration_2026_06_03_phase6_1',
              r_new.migrated_at                  = datetime()
DELETE r_old;


// ---------- §4. Post-checks ----------

MATCH ()-[r {review_run: 'taxonomy_integration_2026_06_03_phase6_1'}]->()
RETURN 'P6.1 migrated' AS phase, type(r) AS rel_type, count(r) AS n
ORDER BY rel_type;

// Residue: old-target edges from non-(BG|Projekt) upstreams (expected 0 after migration)
MATCH (upstream)-[r:HAT_METHODE]->(meth_old:Methode)
WHERE NOT upstream:Bauteilgruppe AND NOT upstream:Projekt
  AND meth_old.id IN keys($method_map)
RETURN 'P6.1 residue' AS phase, 'HAT_METHODE' AS rel, count(r) AS n;

MATCH (upstream)-[r:HAT_AUFBEREITUNG]->(av_old:Aufbereitungsverfahren)
WHERE NOT upstream:Bauteilgruppe AND NOT upstream:Projekt
  AND av_old.id IN keys($aufb_map)
RETURN 'P6.1 residue' AS phase, 'HAT_AUFBEREITUNG' AS rel, count(r) AS n;

MATCH (upstream)-[r:HAT_RESSOURCENQUELLE]->(rq_old:Ressourcenquelle)
WHERE NOT upstream:Bauteilgruppe AND NOT upstream:Projekt
  AND rq_old.id IN keys($rq_map)
RETURN 'P6.1 residue' AS phase, 'HAT_RESSOURCENQUELLE' AS rel, count(r) AS n;
