// =================================================================
// RUN_MIGRATION.cypher  --  bauteilboersen_finalest_30_2026_05_31
// =================================================================
// Single executable script: STEPs 0 -> 6B in order.
// Pre-checks: run MIGRATION_TESTS.cypher PART A first.
// Post-checks: run MIGRATION_TESTS.cypher PART B after.
// All new edges/nodes tagged review_run='bauteilboersen_finalest_30_2026_05_31'
// =================================================================


// -----------------------------------------------------------------
// STEP 0 -- Remove HAT_AKTEURTYP -> at_materialhub_bauteilboerse
//           from the 9 non-TAKE actors. Expect 9 edges deleted.
// -----------------------------------------------------------------
MATCH (a:Akteur)-[r:HAT_AKTEURTYP]->(:Akteurtyp {id:'at_materialhub_bauteilboerse'})
WHERE a.id IN [
  'globechain','loopfront','material_reuse_portal','new_horizon','raedificare',
  'resource_marktplaats','salza','reuse_and_trade','warp_it'
]
DELETE r;


// -----------------------------------------------------------------
// STEP 1 -- Create :Geschaeftsmodell label + 5 nodes
// -----------------------------------------------------------------
CREATE CONSTRAINT geschaeftsmodell_id IF NOT EXISTS
  FOR (g:Geschaeftsmodell) REQUIRE g.id IS UNIQUE;

UNWIND [
  {id:'gm_shop_eigenstock',                 name:'Shop mit Eigenstock'},
  {id:'gm_marketplace_vermittlung',         name:'Multi-Vendor-Marktplatz'},
  {id:'gm_dienstleistung_urban_mining',     name:'Urban-Mining-Dienstleister mit Verkaufskanal'},
  {id:'gm_saas_inventar_plattform',         name:'SaaS-Inventarplattform'},
  {id:'gm_netzwerk_aggregator',             name:'Netzwerk / Aggregator / Redistribution'}
] AS row
MERGE (g:Geschaeftsmodell {id: row.id})
ON CREATE SET g.name         = row.name,
              g.source_scope = 'controlled_vocab_seed',
              g.review_run   = 'bauteilboersen_finalest_30_2026_05_31';


// -----------------------------------------------------------------
// STEP 2 -- Assign HAT_GESCHAEFTSMODELL: 17 single + 12 dual + 1 triple = 44 edges
// -----------------------------------------------------------------
UNWIND [
  // single-GM
  {anchor:'articonnex',                                gm:'gm_shop_eigenstock',                  conf:'belegt'},
  {anchor:'bauteilladen_winterthur',                   gm:'gm_shop_eigenstock',                  conf:'belegt'},
  {anchor:'gebruiktebouwmaterialen',                   gm:'gm_shop_eigenstock',                  conf:'wahrscheinlich'},
  {anchor:'genbyg',                                    gm:'gm_shop_eigenstock',                  conf:'belegt'},
  {anchor:'batrecup',                                  gm:'gm_marketplace_vermittlung',          conf:'belegt'},
  {anchor:'building_spares_market',                    gm:'gm_marketplace_vermittlung',          conf:'wahrscheinlich'},
  {anchor:'cycle_zero',                                gm:'gm_marketplace_vermittlung',          conf:'belegt'},
  {anchor:'enviromate',                                gm:'gm_marketplace_vermittlung',          conf:'belegt'},
  {anchor:'insert_marketplace',                        gm:'gm_marketplace_vermittlung',          conf:'wahrscheinlich'},
  {anchor:'materialrest24',                            gm:'gm_marketplace_vermittlung',          conf:'wahrscheinlich'},
  {anchor:'r_place',                                   gm:'gm_marketplace_vermittlung',          conf:'belegt'},
  {anchor:'software_restado',                          gm:'gm_marketplace_vermittlung',          conf:'belegt'},
  {anchor:'surplus_building_and_plumbing_materials',   gm:'gm_marketplace_vermittlung',          conf:'belegt'},
  {anchor:'sustainability_yard',                       gm:'gm_marketplace_vermittlung',          conf:'belegt'},
  {anchor:'useagain_bauteilclick',                     gm:'gm_marketplace_vermittlung',          conf:'wahrscheinlich'},
  {anchor:'baukarussell',                              gm:'gm_dienstleistung_urban_mining',      conf:'belegt'},
  {anchor:'bauteilnetz_deutschland',                   gm:'gm_netzwerk_aggregator',              conf:'belegt'},
  // dual-GM
  {anchor:'backacia',                                  gm:'gm_marketplace_vermittlung',          conf:'belegt'},
  {anchor:'backacia',                                  gm:'gm_dienstleistung_urban_mining',      conf:'belegt'},
  {anchor:'baticycle',                                 gm:'gm_shop_eigenstock',                  conf:'belegt'},
  {anchor:'baticycle',                                 gm:'gm_dienstleistung_urban_mining',      conf:'wahrscheinlich'},
  {anchor:'batiterre',                                 gm:'gm_shop_eigenstock',                  conf:'belegt'},
  {anchor:'batiterre',                                 gm:'gm_dienstleistung_urban_mining',      conf:'belegt'},
  {anchor:'bauteilboerse_bremen',                      gm:'gm_shop_eigenstock',                  conf:'belegt'},
  {anchor:'bauteilboerse_bremen',                      gm:'gm_dienstleistung_urban_mining',      conf:'wahrscheinlich'},
  {anchor:'cornermat_retrival',                        gm:'gm_dienstleistung_urban_mining',      conf:'belegt'},
  {anchor:'cornermat_retrival',                        gm:'gm_shop_eigenstock',                  conf:'wahrscheinlich'},
  {anchor:'cycle_up',                                  gm:'gm_marketplace_vermittlung',          conf:'belegt'},
  {anchor:'cycle_up',                                  gm:'gm_dienstleistung_urban_mining',      conf:'belegt'},
  {anchor:'materialenbank_leuven_atelier_circuler',    gm:'gm_dienstleistung_urban_mining',      conf:'belegt'},
  {anchor:'materialenbank_leuven_atelier_circuler',    gm:'gm_shop_eigenstock',                  conf:'belegt'},
  {anchor:'re_store_harvestmap_vienna',                gm:'gm_shop_eigenstock',                  conf:'belegt'},
  {anchor:'re_store_harvestmap_vienna',                gm:'gm_dienstleistung_urban_mining',      conf:'belegt'},
  {anchor:'reempro',                                   gm:'gm_marketplace_vermittlung',          conf:'belegt'},
  {anchor:'reempro',                                   gm:'gm_dienstleistung_urban_mining',      conf:'belegt'},
  {anchor:'rotordc',                                   gm:'gm_shop_eigenstock',                  conf:'belegt'},
  {anchor:'rotordc',                                   gm:'gm_dienstleistung_urban_mining',      conf:'belegt'},
  {anchor:'salvoweb',                                  gm:'gm_netzwerk_aggregator',              conf:'belegt'},
  {anchor:'salvoweb',                                  gm:'gm_marketplace_vermittlung',          conf:'belegt'},
  {anchor:'skop_marketplace',                          gm:'gm_marketplace_vermittlung',          conf:'belegt'},
  {anchor:'skop_marketplace',                          gm:'gm_dienstleistung_urban_mining',      conf:'wahrscheinlich'},
  // triple-GM
  {anchor:'material_index',                            gm:'gm_marketplace_vermittlung',          conf:'belegt'},
  {anchor:'material_index',                            gm:'gm_dienstleistung_urban_mining',      conf:'belegt'},
  {anchor:'material_index',                            gm:'gm_saas_inventar_plattform',          conf:'wahrscheinlich'}
] AS row
MATCH (a {id: row.anchor}), (g:Geschaeftsmodell {id: row.gm})
MERGE (a)-[r:HAT_GESCHAEFTSMODELL]->(g)
ON CREATE SET r.evidence_basis      = 'marktmodell_addendum_2026_05_31',
              r.evidence_confidence = row.conf,
              r.review_run          = 'bauteilboersen_finalest_30_2026_05_31';


// -----------------------------------------------------------------
// STEP 3 -- HAT_AKTEURROLLE fingerprint per cluster (idempotent)
// -----------------------------------------------------------------
// gm_shop_eigenstock -> ar_materialbroker
MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_shop_eigenstock'}),
      (r:Akteurrolle {id:'ar_materialbroker'})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(r)
ON CREATE SET rel.evidence_basis='gm_fingerprint_2026_05_31',
              rel.review_run   ='bauteilboersen_finalest_30_2026_05_31';

// gm_marketplace_vermittlung -> ar_materialbroker, ar_software_digitalisierung
UNWIND ['ar_materialbroker','ar_software_digitalisierung'] AS role_id
MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_marketplace_vermittlung'}),
      (r:Akteurrolle {id: role_id})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(r)
ON CREATE SET rel.evidence_basis='gm_fingerprint_2026_05_31',
              rel.review_run   ='bauteilboersen_finalest_30_2026_05_31';

// gm_dienstleistung_urban_mining -> ar_rueckbau_*, ar_aufbereitung_*, ar_materiallieferung_markt, ar_reuse_*
UNWIND [
  'ar_rueckbau_bauteilernte_logistik',
  'ar_aufbereitung_refurbishment',
  'ar_materiallieferung_markt',
  'ar_reuse_zirkularitaetsberatung'
] AS role_id
MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_dienstleistung_urban_mining'}),
      (r:Akteurrolle {id: role_id})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(r)
ON CREATE SET rel.evidence_basis='gm_fingerprint_2026_05_31',
              rel.review_run   ='bauteilboersen_finalest_30_2026_05_31';

// gm_saas_inventar_plattform -> ar_software_digitalisierung, ar_forschung_dokumentation
UNWIND ['ar_software_digitalisierung','ar_forschung_dokumentation'] AS role_id
MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_saas_inventar_plattform'}),
      (r:Akteurrolle {id: role_id})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(r)
ON CREATE SET rel.evidence_basis='gm_fingerprint_2026_05_31',
              rel.review_run   ='bauteilboersen_finalest_30_2026_05_31';

// gm_netzwerk_aggregator -> ar_bildung_wissenstransfer, ar_forschung_dokumentation, ar_materialbroker
UNWIND ['ar_bildung_wissenstransfer','ar_forschung_dokumentation','ar_materialbroker'] AS role_id
MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_netzwerk_aggregator'}),
      (r:Akteurrolle {id: role_id})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(r)
ON CREATE SET rel.evidence_basis='gm_fingerprint_2026_05_31',
              rel.review_run   ='bauteilboersen_finalest_30_2026_05_31';


// -----------------------------------------------------------------
// STEP 4 -- HAT_METHODE fingerprint per cluster (idempotent)
// -----------------------------------------------------------------
// urban_mining cluster -> meth_urban_mining, meth_pre_deconstruction_audit, meth_bauteilkatalogisierung
UNWIND ['meth_urban_mining','meth_pre_deconstruction_audit','meth_bauteilkatalogisierung'] AS m_id
MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_dienstleistung_urban_mining'}),
      (m:Methode {id: m_id})
MERGE (a)-[rel:HAT_METHODE]->(m)
ON CREATE SET rel.evidence_basis='gm_fingerprint_2026_05_31',
              rel.review_run   ='bauteilboersen_finalest_30_2026_05_31';

// saas_inventar cluster -> meth_materialinventur, meth_bauteilkatalogisierung, meth_abrissmonitoring
UNWIND ['meth_materialinventur','meth_bauteilkatalogisierung','meth_abrissmonitoring'] AS m_id
MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_saas_inventar_plattform'}),
      (m:Methode {id: m_id})
MERGE (a)-[rel:HAT_METHODE]->(m)
ON CREATE SET rel.evidence_basis='gm_fingerprint_2026_05_31',
              rel.review_run   ='bauteilboersen_finalest_30_2026_05_31';


// -----------------------------------------------------------------
// STEP 5 -- HAT_MARKTMODELL: one mm_* per actor. Expect 30 edges.
// -----------------------------------------------------------------
UNWIND [
  {anchor:'articonnex',                              mm:'mm_kauf_gebraucht'},
  {anchor:'backacia',                                mm:'mm_plattform_vermittelt'},
  {anchor:'baticycle',                               mm:'mm_kauf_gebraucht'},
  {anchor:'batiterre',                               mm:'mm_kauf_gebraucht'},
  {anchor:'batrecup',                                mm:'mm_spende'},
  {anchor:'baukarussell',                            mm:'mm_kauf_gebraucht'},
  {anchor:'bauteilboerse_bremen',                    mm:'mm_kauf_gebraucht'},
  {anchor:'bauteilladen_winterthur',                 mm:'mm_kauf_gebraucht'},
  {anchor:'bauteilnetz_deutschland',                 mm:'mm_plattform_vermittelt'},
  {anchor:'building_spares_market',                  mm:'mm_plattform_vermittelt'},
  {anchor:'cornermat_retrival',                      mm:'mm_kauf_gebraucht'},
  {anchor:'cycle_up',                                mm:'mm_plattform_vermittelt'},
  {anchor:'cycle_zero',                              mm:'mm_spende'},
  {anchor:'enviromate',                              mm:'mm_plattform_vermittelt'},
  {anchor:'gebruiktebouwmaterialen',                 mm:'mm_kauf_gebraucht'},
  {anchor:'genbyg',                                  mm:'mm_kauf_gebraucht'},
  {anchor:'insert_marketplace',                      mm:'mm_plattform_vermittelt'},
  {anchor:'material_index',                          mm:'mm_plattform_vermittelt'},
  {anchor:'materialenbank_leuven_atelier_circuler',  mm:'mm_kauf_gebraucht'},
  {anchor:'materialrest24',                          mm:'mm_plattform_vermittelt'},
  {anchor:'r_place',                                 mm:'mm_plattform_vermittelt'},
  {anchor:'re_store_harvestmap_vienna',              mm:'mm_kauf_gebraucht'},
  {anchor:'reempro',                                 mm:'mm_plattform_vermittelt'},
  {anchor:'rotordc',                                 mm:'mm_kauf_gebraucht'},
  {anchor:'salvoweb',                                mm:'mm_plattform_vermittelt'},
  {anchor:'skop_marketplace',                        mm:'mm_plattform_vermittelt'},
  {anchor:'software_restado',                        mm:'mm_plattform_vermittelt'},
  {anchor:'surplus_building_and_plumbing_materials', mm:'mm_plattform_vermittelt'},
  {anchor:'sustainability_yard',                     mm:'mm_plattform_vermittelt'},
  {anchor:'useagain_bauteilclick',                   mm:'mm_plattform_vermittelt'}
] AS row
MATCH (a {id: row.anchor}), (m:Marktmodell {id: row.mm})
MERGE (a)-[r:HAT_MARKTMODELL]->(m)
ON CREATE SET r.evidence_basis='gm_fingerprint_2026_05_31',
              r.review_run   ='bauteilboersen_finalest_30_2026_05_31';


// -----------------------------------------------------------------
// STEP 6A -- Strict NUTZT_MATERIAL imports (14 actors -> 40 edges)
// -----------------------------------------------------------------
UNWIND [
  {anchor:'batiterre',                               target:'mat_glas'},
  {anchor:'batiterre',                               target:'mat_gusseisen'},
  {anchor:'batiterre',                               target:'mat_holz'},
  {anchor:'batiterre',                               target:'mat_kunststoff'},
  {anchor:'batiterre',                               target:'mat_ziegel'},
  {anchor:'baukarussell',                            target:'mat_glas'},
  {anchor:'baukarussell',                            target:'mat_holz'},
  {anchor:'bauteilladen_winterthur',                 target:'mat_holz'},
  {anchor:'bauteilladen_winterthur',                 target:'mat_naturstein'},
  {anchor:'bauteilnetz_deutschland',                 target:'mat_keramik'},
  {anchor:'bauteilnetz_deutschland',                 target:'mat_ziegel'},
  {anchor:'building_spares_market',                  target:'mat_aluminium'},
  {anchor:'building_spares_market',                  target:'mat_beton'},
  {anchor:'building_spares_market',                  target:'mat_daemmstoff'},
  {anchor:'building_spares_market',                  target:'mat_glas'},
  {anchor:'building_spares_market',                  target:'mat_holz'},
  {anchor:'building_spares_market',                  target:'mat_stahl'},
  {anchor:'building_spares_market',                  target:'mat_ziegel'},
  {anchor:'cornermat_retrival',                      target:'mat_glas'},
  {anchor:'cornermat_retrival',                      target:'mat_holz'},
  {anchor:'cornermat_retrival',                      target:'mat_keramik'},
  {anchor:'cornermat_retrival',                      target:'mat_ziegel'},
  {anchor:'enviromate',                              target:'mat_keramik'},
  {anchor:'gebruiktebouwmaterialen',                 target:'mat_aluminium'},
  {anchor:'gebruiktebouwmaterialen',                 target:'mat_daemmstoff'},
  {anchor:'gebruiktebouwmaterialen',                 target:'mat_holz'},
  {anchor:'gebruiktebouwmaterialen',                 target:'mat_kunststoff'},
  {anchor:'gebruiktebouwmaterialen',                 target:'mat_stahl'},
  {anchor:'gebruiktebouwmaterialen',                 target:'mat_ziegel'},
  {anchor:'genbyg',                                  target:'mat_glas'},
  {anchor:'re_store_harvestmap_vienna',              target:'mat_beton'},
  {anchor:'re_store_harvestmap_vienna',              target:'mat_holz'},
  {anchor:'re_store_harvestmap_vienna',              target:'mat_keramik'},
  {anchor:'re_store_harvestmap_vienna',              target:'mat_naturstein'},
  {anchor:'reempro',                                 target:'mat_keramik'},
  {anchor:'reempro',                                 target:'mat_ziegel'},
  {anchor:'rotordc',                                 target:'mat_keramik'},
  {anchor:'software_restado',                        target:'mat_holz'},
  {anchor:'software_restado',                        target:'mat_keramik'},
  {anchor:'useagain_bauteilclick',                   target:'mat_stahl'}
] AS row
MATCH (a {id: row.anchor}), (m:Material {id: row.target})
MERGE (a)-[r:NUTZT_MATERIAL]->(m)
ON CREATE SET r.evidence_basis     ='pass8_strict_import_2026_05_31',
              r.evidence_confidence='belegt',
              r.review_run         ='bauteilboersen_finalest_30_2026_05_31';


// -----------------------------------------------------------------
// STEP 6B -- Strict HAT_BAUTEILTYP imports (15 actors -> 72 edges)
// -----------------------------------------------------------------
UNWIND [
  {anchor:'baticycle',                               target:'bt_ausbau'},
  {anchor:'baticycle',                               target:'bt_boden'},
  {anchor:'baticycle',                               target:'bt_decke'},
  {anchor:'baticycle',                               target:'bt_technik'},
  {anchor:'baticycle',                               target:'bt_tuer'},
  {anchor:'baticycle',                               target:'bt_wand'},
  {anchor:'batiterre',                               target:'bt_ausbau'},
  {anchor:'batiterre',                               target:'bt_boden'},
  {anchor:'batiterre',                               target:'bt_dach'},
  {anchor:'batiterre',                               target:'bt_daemmung'},
  {anchor:'batiterre',                               target:'bt_fenster'},
  {anchor:'batiterre',                               target:'bt_gelaender'},
  {anchor:'batiterre',                               target:'bt_technik'},
  {anchor:'batiterre',                               target:'bt_treppe'},
  {anchor:'batiterre',                               target:'bt_tuer'},
  {anchor:'batiterre',                               target:'bt_wand'},
  {anchor:'baukarussell',                            target:'bt_boden'},
  {anchor:'baukarussell',                            target:'bt_dach'},
  {anchor:'baukarussell',                            target:'bt_fassade'},
  {anchor:'baukarussell',                            target:'bt_fenster'},
  {anchor:'baukarussell',                            target:'bt_technik'},
  {anchor:'baukarussell',                            target:'bt_tuer'},
  {anchor:'baukarussell',                            target:'bt_wand'},
  {anchor:'bauteilladen_winterthur',                 target:'bt_fenster'},
  {anchor:'bauteilnetz_deutschland',                 target:'bt_boden'},
  {anchor:'bauteilnetz_deutschland',                 target:'bt_dach'},
  {anchor:'building_spares_market',                  target:'bt_boden'},
  {anchor:'building_spares_market',                  target:'bt_dach'},
  {anchor:'building_spares_market',                  target:'bt_daemmung'},
  {anchor:'building_spares_market',                  target:'bt_fenster'},
  {anchor:'building_spares_market',                  target:'bt_traeger'},
  {anchor:'building_spares_market',                  target:'bt_tuer'},
  {anchor:'building_spares_market',                  target:'bt_wand'},
  {anchor:'cornermat_retrival',                      target:'bt_dach'},
  {anchor:'cornermat_retrival',                      target:'bt_fenster'},
  {anchor:'cornermat_retrival',                      target:'bt_technik'},
  {anchor:'cornermat_retrival',                      target:'bt_tuer'},
  {anchor:'cornermat_retrival',                      target:'bt_wand'},
  {anchor:'enviromate',                              target:'bt_boden'},
  {anchor:'gebruiktebouwmaterialen',                 target:'bt_boden'},
  {anchor:'gebruiktebouwmaterialen',                 target:'bt_dach'},
  {anchor:'gebruiktebouwmaterialen',                 target:'bt_daemmung'},
  {anchor:'gebruiktebouwmaterialen',                 target:'bt_fenster'},
  {anchor:'gebruiktebouwmaterialen',                 target:'bt_technik'},
  {anchor:'gebruiktebouwmaterialen',                 target:'bt_traeger'},
  {anchor:'gebruiktebouwmaterialen',                 target:'bt_treppe'},
  {anchor:'gebruiktebouwmaterialen',                 target:'bt_tuer'},
  {anchor:'gebruiktebouwmaterialen',                 target:'bt_wand'},
  {anchor:'genbyg',                                  target:'bt_fenster'},
  {anchor:'genbyg',                                  target:'bt_technik'},
  {anchor:'genbyg',                                  target:'bt_tuer'},
  {anchor:'material_index',                          target:'bt_ausbau'},
  {anchor:'material_index',                          target:'bt_boden'},
  {anchor:'material_index',                          target:'bt_technik'},
  {anchor:'material_index',                          target:'bt_tuer'},
  {anchor:'material_index',                          target:'bt_wand'},
  {anchor:'re_store_harvestmap_vienna',              target:'bt_boden'},
  {anchor:'re_store_harvestmap_vienna',              target:'bt_dach'},
  {anchor:'reempro',                                 target:'bt_ausbau'},
  {anchor:'reempro',                                 target:'bt_boden'},
  {anchor:'reempro',                                 target:'bt_daemmung'},
  {anchor:'reempro',                                 target:'bt_decke'},
  {anchor:'reempro',                                 target:'bt_fenster'},
  {anchor:'reempro',                                 target:'bt_technik'},
  {anchor:'reempro',                                 target:'bt_tuer'},
  {anchor:'reempro',                                 target:'bt_wand'},
  {anchor:'software_restado',                        target:'bt_boden'},
  {anchor:'software_restado',                        target:'bt_dach'},
  {anchor:'software_restado',                        target:'bt_tuer'},
  {anchor:'software_restado',                        target:'bt_wand'},
  {anchor:'useagain_bauteilclick',                   target:'bt_fenster'},
  {anchor:'useagain_bauteilclick',                   target:'bt_technik'}
] AS row
MATCH (a {id: row.anchor}), (b:Bauteiltyp {id: row.target})
MERGE (a)-[r:HAT_BAUTEILTYP]->(b)
ON CREATE SET r.evidence_basis     ='pass8_strict_import_2026_05_31',
              r.evidence_confidence='belegt',
              r.review_run         ='bauteilboersen_finalest_30_2026_05_31';


// =================================================================
// DONE. Run MIGRATION_TESTS.cypher PART B now to verify.
// =================================================================
