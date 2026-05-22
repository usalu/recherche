# Bauteilbörsen — Final Import Plan (30-actor scope)

**Date:** 2026-05-31 · **Database:** `mit-bestand` · **Review run tag:** `bauteilboersen_finalest_30_2026_05_31`

**Companion file:** [`MIGRATION_TESTS.cypher`](MIGRATION_TESTS.cypher) — pre-migration sanity checks (PART A) + post-migration validation (PART B) + diagnostics (PART C).

**Run order:**
1. Execute **PART A** tests (11 queries). All must PASS or WARN before proceeding.
2. Execute STEPs **0 → 1 → 2 → 3 → 4 → 5** of this plan (the classification layer).
3. Execute **STEPs 6A → 6B** of this plan (the strict-import layer).
4. Execute **PART B** tests (24 queries). All must PASS.
5. If any B test fails, run **PART C** diagnostics, then ROLLBACK (bottom of this file) and re-plan.

## Scope

- **30 TAKE actors** kept in the Bauteilbörse dataset (this plan).
- **7 TAKE_AS_RELATED_ONLY** (`globechain`, `loopfront`, `material_reuse_portal`, `new_horizon`, `raedificare`, `resource_marktplaats`, `salza`) — `at_materialhub_bauteilboerse` link removed; Akteur node stays.
- **2 DO_NOT_TAKE** (`reuse_and_trade`, `warp_it`) — same: type link removed; Akteur node stays.

## What this plan writes to Neo4j

| Layer | Operation | Count |
|---|---|---:|
| 0 | Remove `HAT_AKTEURTYP→at_materialhub_bauteilboerse` for the 9 non-TAKE actors | **−9** edges |
| 1 | Create `:Geschaeftsmodell` nodes | **+5** nodes |
| 2 | `HAT_GESCHAEFTSMODELL` edges (multi-edge: 17 single + 12 dual + 1 triple) | **+44** edges |
| 3 | `HAT_AKTEURROLLE` gap-fill per cluster | **idempotent, ~30–50** new edges |
| 4 | `HAT_METHODE` gap-fill per cluster | **idempotent, ~10–20** new edges |
| 5 | `HAT_MARKTMODELL` one per actor (live `mm_*` vocab) | **+30** edges |
| 6A | `NUTZT_MATERIAL` strict (14 actors) | **+40** edges |
| 6B | `HAT_BAUTEILTYP` strict (15 actors) | **+72** edges |
| **Net** | | **≈ +210, −9** |

**6A∪6B = 16 distinct actors with strict imports.** Intersection 13 actors; `rotordc` only in 6A (1 mat); `baticycle` and `material_index` only in 6B (no strict materials).

All new edges carry `evidence_basis` and `review_run` for rollback. No other properties.

---

## STEP 0 — Cleanup: remove non-TAKE actors from `at_materialhub_bauteilboerse`

```cypher
MATCH (a:Akteur)-[r:HAT_AKTEURTYP]->(:Akteurtyp {id:'at_materialhub_bauteilboerse'})
WHERE a.id IN [
  'globechain','loopfront','material_reuse_portal','new_horizon','raedificare',
  'resource_marktplaats','salza','reuse_and_trade','warp_it'
]
DELETE r;
// expect 9 edges deleted
```

---

## STEP 1 — Create the 5 `:Geschaeftsmodell` nodes

```cypher
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
```

---

## STEP 2 — Assign Geschäftsmodell (44 edges, multi-edge allowed)

```cypher
UNWIND [
  // ----- gm_shop_eigenstock (primary) -----
  {anchor:'articonnex',                                gm:'gm_shop_eigenstock',                  conf:'belegt'},
  {anchor:'bauteilladen_winterthur',                   gm:'gm_shop_eigenstock',                  conf:'belegt'},
  {anchor:'gebruiktebouwmaterialen',                   gm:'gm_shop_eigenstock',                  conf:'wahrscheinlich'},
  {anchor:'genbyg',                                    gm:'gm_shop_eigenstock',                  conf:'belegt'},
  // ----- gm_marketplace_vermittlung (primary single) -----
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
  // ----- gm_dienstleistung_urban_mining (primary single) -----
  {anchor:'baukarussell',                              gm:'gm_dienstleistung_urban_mining',      conf:'belegt'},
  // ----- gm_netzwerk_aggregator (primary single) -----
  {anchor:'bauteilnetz_deutschland',                   gm:'gm_netzwerk_aggregator',              conf:'belegt'},
  // ----- Dual-GM actors (12 × 2 = 24 edges) -----
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
  // ----- Triple-GM actor (1 × 3 = 3 edges) -----
  {anchor:'material_index',                            gm:'gm_marketplace_vermittlung',          conf:'belegt'},
  {anchor:'material_index',                            gm:'gm_dienstleistung_urban_mining',      conf:'belegt'},
  {anchor:'material_index',                            gm:'gm_saas_inventar_plattform',          conf:'wahrscheinlich'}
] AS row
MATCH (a:Akteur {id: row.anchor}), (g:Geschaeftsmodell {id: row.gm})
MERGE (a)-[r:HAT_GESCHAEFTSMODELL]->(g)
ON CREATE SET r.evidence_basis      = 'marktmodell_addendum_2026_05_31',
              r.evidence_confidence = row.conf,
              r.review_run          = 'bauteilboersen_finalest_30_2026_05_31';
// expect 44 edges
```

---

## STEP 3 — `HAT_AKTEURROLLE` gap-fill per cluster

Idempotent: existing role edges remain untouched. Only adds missing ones implied by the cluster.

```cypher
// gm_shop_eigenstock → adds 'Materialbroker' if not yet set
MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_shop_eigenstock'}),
      (r:Akteurrolle {id:'ar_materialbroker'})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(r)
ON CREATE SET rel.evidence_basis='gm_fingerprint_2026_05_31',
              rel.review_run   ='bauteilboersen_finalest_30_2026_05_31';

// gm_marketplace_vermittlung → adds 'Materialbroker' + 'Software_Digitalisierung'
UNWIND ['ar_materialbroker','ar_software_digitalisierung'] AS role_id
MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_marketplace_vermittlung'}),
      (r:Akteurrolle {id: role_id})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(r)
ON CREATE SET rel.evidence_basis='gm_fingerprint_2026_05_31',
              rel.review_run   ='bauteilboersen_finalest_30_2026_05_31';

// gm_dienstleistung_urban_mining → adds Rückbau, Aufbereitung, Materiallieferung, Reuse-Beratung
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

// gm_saas_inventar_plattform → adds Software_Digitalisierung, Forschung_Dokumentation
UNWIND ['ar_software_digitalisierung','ar_forschung_dokumentation'] AS role_id
MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_saas_inventar_plattform'}),
      (r:Akteurrolle {id: role_id})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(r)
ON CREATE SET rel.evidence_basis='gm_fingerprint_2026_05_31',
              rel.review_run   ='bauteilboersen_finalest_30_2026_05_31';

// gm_netzwerk_aggregator → adds Bildung_Wissenstransfer, Forschung_Dokumentation, Materialbroker
UNWIND ['ar_bildung_wissenstransfer','ar_forschung_dokumentation','ar_materialbroker'] AS role_id
MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_netzwerk_aggregator'}),
      (r:Akteurrolle {id: role_id})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(r)
ON CREATE SET rel.evidence_basis='gm_fingerprint_2026_05_31',
              rel.review_run   ='bauteilboersen_finalest_30_2026_05_31';
```

---

## STEP 4 — `HAT_METHODE` gap-fill per cluster

```cypher
// Urban mining cluster → meth_urban_mining + meth_pre_deconstruction_audit + meth_bauteilkatalogisierung
UNWIND [
  'meth_urban_mining',
  'meth_pre_deconstruction_audit',
  'meth_bauteilkatalogisierung'
] AS m_id
MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_dienstleistung_urban_mining'}),
      (m:Methode {id: m_id})
MERGE (a)-[rel:HAT_METHODE]->(m)
ON CREATE SET rel.evidence_basis='gm_fingerprint_2026_05_31',
              rel.review_run   ='bauteilboersen_finalest_30_2026_05_31';

// SaaS-inventar cluster → meth_materialinventur + meth_bauteilkatalogisierung + meth_abrissmonitoring
UNWIND ['meth_materialinventur','meth_bauteilkatalogisierung','meth_abrissmonitoring'] AS m_id
MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_saas_inventar_plattform'}),
      (m:Methode {id: m_id})
MERGE (a)-[rel:HAT_METHODE]->(m)
ON CREATE SET rel.evidence_basis='gm_fingerprint_2026_05_31',
              rel.review_run   ='bauteilboersen_finalest_30_2026_05_31';
```

---

## STEP 5 — `HAT_MARKTMODELL` (one mm_* per actor, live vocab)

```cypher
UNWIND [
  // Default: mm_kauf_gebraucht (purchase of used components)
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
MATCH (a:Akteur {id: row.anchor}), (m:Marktmodell {id: row.mm})
MERGE (a)-[r:HAT_MARKTMODELL]->(m)
ON CREATE SET r.evidence_basis='gm_fingerprint_2026_05_31',
              r.review_run   ='bauteilboersen_finalest_30_2026_05_31';
// expect 30 edges
```

---

## STEP 6A — Strict `NUTZT_MATERIAL` imports (16 actors → 40 edges)

```cypher
UNWIND [
  {anchor:'batiterre',                                 target:'mat_glas'},
  {anchor:'batiterre',                                 target:'mat_gusseisen'},
  {anchor:'batiterre',                                 target:'mat_holz'},
  {anchor:'batiterre',                                 target:'mat_kunststoff'},
  {anchor:'batiterre',                                 target:'mat_ziegel'},
  {anchor:'baukarussell',                              target:'mat_glas'},
  {anchor:'baukarussell',                              target:'mat_holz'},
  {anchor:'bauteilladen_winterthur',                   target:'mat_holz'},
  {anchor:'bauteilladen_winterthur',                   target:'mat_naturstein'},
  {anchor:'bauteilnetz_deutschland',                   target:'mat_keramik'},
  {anchor:'bauteilnetz_deutschland',                   target:'mat_ziegel'},
  {anchor:'building_spares_market',                    target:'mat_aluminium'},
  {anchor:'building_spares_market',                    target:'mat_beton'},
  {anchor:'building_spares_market',                    target:'mat_daemmstoff'},
  {anchor:'building_spares_market',                    target:'mat_glas'},
  {anchor:'building_spares_market',                    target:'mat_holz'},
  {anchor:'building_spares_market',                    target:'mat_stahl'},
  {anchor:'building_spares_market',                    target:'mat_ziegel'},
  {anchor:'cornermat_retrival',                        target:'mat_glas'},
  {anchor:'cornermat_retrival',                        target:'mat_holz'},
  {anchor:'cornermat_retrival',                        target:'mat_keramik'},
  {anchor:'cornermat_retrival',                        target:'mat_ziegel'},
  {anchor:'enviromate',                                target:'mat_keramik'},
  {anchor:'gebruiktebouwmaterialen',                   target:'mat_aluminium'},
  {anchor:'gebruiktebouwmaterialen',                   target:'mat_daemmstoff'},
  {anchor:'gebruiktebouwmaterialen',                   target:'mat_holz'},
  {anchor:'gebruiktebouwmaterialen',                   target:'mat_kunststoff'},
  {anchor:'gebruiktebouwmaterialen',                   target:'mat_stahl'},
  {anchor:'gebruiktebouwmaterialen',                   target:'mat_ziegel'},
  {anchor:'genbyg',                                    target:'mat_glas'},
  {anchor:'re_store_harvestmap_vienna',                target:'mat_beton'},
  {anchor:'re_store_harvestmap_vienna',                target:'mat_holz'},
  {anchor:'re_store_harvestmap_vienna',                target:'mat_keramik'},
  {anchor:'re_store_harvestmap_vienna',                target:'mat_naturstein'},
  {anchor:'reempro',                                   target:'mat_keramik'},
  {anchor:'reempro',                                   target:'mat_ziegel'},
  {anchor:'rotordc',                                   target:'mat_keramik'},
  {anchor:'software_restado',                          target:'mat_holz'},
  {anchor:'software_restado',                          target:'mat_keramik'},
  {anchor:'useagain_bauteilclick',                     target:'mat_stahl'}
] AS row
MATCH (a:Akteur {id: row.anchor}), (m:Material {id: row.target})
MERGE (a)-[r:NUTZT_MATERIAL]->(m)
ON CREATE SET r.evidence_basis     ='pass8_strict_import_2026_05_31',
              r.evidence_confidence='belegt',
              r.review_run         ='bauteilboersen_finalest_30_2026_05_31';
// expect 40 edges
```

## STEP 6B — Strict `HAT_BAUTEILTYP` imports (15 actors → 72 edges)

```cypher
UNWIND [
  {anchor:'baticycle',                                 target:'bt_ausbau'},
  {anchor:'baticycle',                                 target:'bt_boden'},
  {anchor:'baticycle',                                 target:'bt_decke'},
  {anchor:'baticycle',                                 target:'bt_technik'},
  {anchor:'baticycle',                                 target:'bt_tuer'},
  {anchor:'baticycle',                                 target:'bt_wand'},
  {anchor:'batiterre',                                 target:'bt_ausbau'},
  {anchor:'batiterre',                                 target:'bt_boden'},
  {anchor:'batiterre',                                 target:'bt_dach'},
  {anchor:'batiterre',                                 target:'bt_daemmung'},
  {anchor:'batiterre',                                 target:'bt_fenster'},
  {anchor:'batiterre',                                 target:'bt_gelaender'},
  {anchor:'batiterre',                                 target:'bt_technik'},
  {anchor:'batiterre',                                 target:'bt_treppe'},
  {anchor:'batiterre',                                 target:'bt_tuer'},
  {anchor:'batiterre',                                 target:'bt_wand'},
  {anchor:'baukarussell',                              target:'bt_boden'},
  {anchor:'baukarussell',                              target:'bt_dach'},
  {anchor:'baukarussell',                              target:'bt_fassade'},
  {anchor:'baukarussell',                              target:'bt_fenster'},
  {anchor:'baukarussell',                              target:'bt_technik'},
  {anchor:'baukarussell',                              target:'bt_tuer'},
  {anchor:'baukarussell',                              target:'bt_wand'},
  {anchor:'bauteilladen_winterthur',                   target:'bt_fenster'},
  {anchor:'bauteilnetz_deutschland',                   target:'bt_boden'},
  {anchor:'bauteilnetz_deutschland',                   target:'bt_dach'},
  {anchor:'building_spares_market',                    target:'bt_boden'},
  {anchor:'building_spares_market',                    target:'bt_dach'},
  {anchor:'building_spares_market',                    target:'bt_daemmung'},
  {anchor:'building_spares_market',                    target:'bt_fenster'},
  {anchor:'building_spares_market',                    target:'bt_traeger'},
  {anchor:'building_spares_market',                    target:'bt_tuer'},
  {anchor:'building_spares_market',                    target:'bt_wand'},
  {anchor:'cornermat_retrival',                        target:'bt_dach'},
  {anchor:'cornermat_retrival',                        target:'bt_fenster'},
  {anchor:'cornermat_retrival',                        target:'bt_technik'},
  {anchor:'cornermat_retrival',                        target:'bt_tuer'},
  {anchor:'cornermat_retrival',                        target:'bt_wand'},
  {anchor:'enviromate',                                target:'bt_boden'},
  {anchor:'gebruiktebouwmaterialen',                   target:'bt_boden'},
  {anchor:'gebruiktebouwmaterialen',                   target:'bt_dach'},
  {anchor:'gebruiktebouwmaterialen',                   target:'bt_daemmung'},
  {anchor:'gebruiktebouwmaterialen',                   target:'bt_fenster'},
  {anchor:'gebruiktebouwmaterialen',                   target:'bt_technik'},
  {anchor:'gebruiktebouwmaterialen',                   target:'bt_traeger'},
  {anchor:'gebruiktebouwmaterialen',                   target:'bt_treppe'},
  {anchor:'gebruiktebouwmaterialen',                   target:'bt_tuer'},
  {anchor:'gebruiktebouwmaterialen',                   target:'bt_wand'},
  {anchor:'genbyg',                                    target:'bt_fenster'},
  {anchor:'genbyg',                                    target:'bt_technik'},
  {anchor:'genbyg',                                    target:'bt_tuer'},
  {anchor:'material_index',                            target:'bt_ausbau'},
  {anchor:'material_index',                            target:'bt_boden'},
  {anchor:'material_index',                            target:'bt_technik'},
  {anchor:'material_index',                            target:'bt_tuer'},
  {anchor:'material_index',                            target:'bt_wand'},
  {anchor:'re_store_harvestmap_vienna',                target:'bt_boden'},
  {anchor:'re_store_harvestmap_vienna',                target:'bt_dach'},
  {anchor:'reempro',                                   target:'bt_ausbau'},
  {anchor:'reempro',                                   target:'bt_boden'},
  {anchor:'reempro',                                   target:'bt_daemmung'},
  {anchor:'reempro',                                   target:'bt_decke'},
  {anchor:'reempro',                                   target:'bt_fenster'},
  {anchor:'reempro',                                   target:'bt_technik'},
  {anchor:'reempro',                                   target:'bt_tuer'},
  {anchor:'reempro',                                   target:'bt_wand'},
  {anchor:'software_restado',                          target:'bt_boden'},
  {anchor:'software_restado',                          target:'bt_dach'},
  {anchor:'software_restado',                          target:'bt_tuer'},
  {anchor:'software_restado',                          target:'bt_wand'},
  {anchor:'useagain_bauteilclick',                     target:'bt_fenster'},
  {anchor:'useagain_bauteilclick',                     target:'bt_technik'}
] AS row
MATCH (a:Akteur {id: row.anchor}), (b:Bauteiltyp {id: row.target})
MERGE (a)-[r:HAT_BAUTEILTYP]->(b)
ON CREATE SET r.evidence_basis     ='pass8_strict_import_2026_05_31',
              r.evidence_confidence='belegt',
              r.review_run         ='bauteilboersen_finalest_30_2026_05_31';
// expect 72 edges
```

Note: `rotordc` appears in 6A but not 6B (strict evidence yields only `mat_keramik`, no `bt_*`).

---

## VERIFICATION

```cypher
// V1 — 9 type edges removed
MATCH (a:Akteur)-[:HAT_AKTEURTYP]->(:Akteurtyp {id:'at_materialhub_bauteilboerse'})
WHERE a.id IN [
  'globechain','loopfront','material_reuse_portal','new_horizon','raedificare',
  'resource_marktplaats','salza','reuse_and_trade','warp_it'
]
RETURN count(*) AS leftover;
// expect 0

// V2 — 5 Geschaeftsmodell nodes exist
MATCH (g:Geschaeftsmodell) WHERE g.review_run='bauteilboersen_finalest_30_2026_05_31'
RETURN count(g) AS gm_nodes;
// expect 5

// V3 — every TAKE actor has ≥1 Geschaeftsmodell
MATCH (a:Akteur) WHERE a.id IN [
  'articonnex','backacia','baticycle','batiterre','batrecup','baukarussell',
  'bauteilboerse_bremen','bauteilladen_winterthur','bauteilnetz_deutschland',
  'building_spares_market','cornermat_retrival','cycle_up','cycle_zero','enviromate',
  'gebruiktebouwmaterialen','genbyg','insert_marketplace','material_index',
  'materialenbank_leuven_atelier_circuler','materialrest24','r_place',
  're_store_harvestmap_vienna','reempro','rotordc','salvoweb','skop_marketplace',
  'software_restado','surplus_building_and_plumbing_materials','sustainability_yard',
  'useagain_bauteilclick'
]
OPTIONAL MATCH (a)-[r:HAT_GESCHAEFTSMODELL]->()
WITH a, count(r) AS gm
WHERE gm = 0 RETURN a.id;
// expect 0 rows

// V4 — cluster distribution
MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(g:Geschaeftsmodell)
RETURN g.id, count(a) AS actors ORDER BY actors DESC;
// expect:
//   gm_marketplace_vermittlung 17
//   gm_dienstleistung_urban_mining 13
//   gm_shop_eigenstock 11
//   gm_netzwerk_aggregator 2
//   gm_saas_inventar_plattform 1

// V5 — multi-edge distribution
MATCH (a:Akteur)-[r:HAT_GESCHAEFTSMODELL]->()
WITH a, count(r) AS n
RETURN n, count(a) AS actors ORDER BY n;
// expect: 1→17, 2→12, 3→1

// V6 — strict imports
MATCH (a:Akteur)-[r {review_run:'bauteilboersen_finalest_30_2026_05_31'}]->()
WHERE type(r) IN ['NUTZT_MATERIAL','HAT_BAUTEILTYP']
RETURN type(r), count(r);
// expect NUTZT_MATERIAL 40, HAT_BAUTEILTYP 72

// V7 — every TAKE actor has exactly one HAT_MARKTMODELL from this run
MATCH (a:Akteur)-[r:HAT_MARKTMODELL {review_run:'bauteilboersen_finalest_30_2026_05_31'}]->()
RETURN count(DISTINCT a) AS actors, count(r) AS edges;
// expect actors=30, edges=30
```

---

## ROLLBACK

One-liner — removes every edge and node created by this run:

```cypher
MATCH ()-[r {review_run:'bauteilboersen_finalest_30_2026_05_31'}]-() DELETE r;
MATCH (g:Geschaeftsmodell {review_run:'bauteilboersen_finalest_30_2026_05_31'}) DETACH DELETE g;
```

Re-creating the 9 removed `HAT_AKTEURTYP` edges (if you change your mind on TAKE_AS_RELATED_ONLY / DO_NOT_TAKE):
```cypher
UNWIND [
  'globechain','loopfront','material_reuse_portal','new_horizon','raedificare',
  'resource_marktplaats','salza','reuse_and_trade','warp_it'
] AS anchor_id
MATCH (a:Akteur {id: anchor_id}), (t:Akteurtyp {id:'at_materialhub_bauteilboerse'})
MERGE (a)-[r:HAT_AKTEURTYP]->(t)
ON CREATE SET r.evidence_basis='restored_from_finalest_30_rollback',
              r.review_run='bauteilboersen_finalest_30_rollback_2026_05_31';
```

---

## Execution order (suggested)

1. **Dry-run pass** — execute STEPs 0–5 first (cleanup + Geschäftsmodell + fingerprints + Marktmodell). Check V1–V5, V7.
2. **Strict imports** — execute STEP 6. Check V6.
3. **If anything looks wrong**, run ROLLBACK and re-plan.

Net: **30 actors fully classified across Akteurtyp + Akteurrolle + Methode + Marktmodell + Geschaeftsmodell**, plus **112 product-evidenced Material/Bauteiltyp edges** for the 16 strictest actors.
