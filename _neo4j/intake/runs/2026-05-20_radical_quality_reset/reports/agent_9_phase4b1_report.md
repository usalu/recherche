# Agent 9 — Phase 4b.1 + 4c.2 S-ref Backfill Report

_Loader run id: `agent9_phase4b1`_  
_Generated: 2026-05-20T22:08:20+00:00_

## Acceptance

- Target: ≥85 of ≈96 case_markdown :Quelle anchors have ≥1 :ZITIERT_QUELLE child.
- Achieved: **100 / 116** (was 100 / 116). **PASS**.

## Before / after

| metric | before | after | delta |
|---|---:|---:|---:|
| case_markdown_total | 116 | 116 | +0 |
| case_markdown_with_zitiert_child | 100 | 100 | +0 |
| external_reference_quelle_total | 879 | 879 | +0 |
| zitiert_quelle_total | 1747 | 1747 | +0 |
| belegt_in_total | 5157 | 5157 | +0 |
| belegt_in_curated_total | 3435 | 3435 | +0 |
| belegt_in_curated_with_excerpt | 2713 | 2713 | +0 |

## Loader summary

| stat | value |
|---|---:|
| dossier_units_processed | 100 |
| qmd_anchors_merged | 100 |
| sref_quelle_merged | 608 |
| zitiert_quelle_links | 611 |
| belegt_in_created | 2713 |
| section8_facts_appended | 216 |
| projekt_matched | 92 |
| projekt_unmatched | 7 |
| prior_belegt_in_deleted | 2713 |

## Per-dossier curated edge counts

| dossier (q_<slug>_md) | rel_path | S-refs | ZITIERT_QUELLE | BELEGT_IN | Section-8 facts | Projekt id | matched |
|---|---|---:|---:|---:|---:|---|:---:|
| `q_55_great_suffolk_street_london_md` | `_archive/research/gebaeude/55_Great_Suffolk_Street_London.md` | 1 | 1 | 0 | 3 | `p_55_great_suffolk_street_london` | ✓ |
| `q_architecture_of_reuse_brussels_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/teaching_programme_graph_ready_dossiers/Architecture_of_Reuse_Brussels.md` | 5 | 5 | 0 | 0 | `p_architecture_of_reuse_brussels` | ✓ |
| `q_association_house_groeditz_md` | `_archive/research/gebaeude/Association_house_Groeditz.md` | 7 | 7 | 50 | 2 | `p_association_house_groeditz` | ✓ |
| `q_association_house_plauen_md` | `_archive/research/gebaeude/Association_house_Plauen.md` | 6 | 6 | 54 | 2 | `p_association_house_plauen` | ✓ |
| `q_awm_muenster_circular_office_md` | `_archive/research/gebaeude/AWM_Muenster_Circular_Office.md` | 6 | 6 | 0 | 6 | `p_awm_muenster_circular_office` | ✓ |
| `q_batch_1_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/batch 1.md` | 3 | 3 | 0 | 0 | `(parent of 3 sub-dossiers)` | — |
| `q_bedzed_london_hackbridge_md` | `_archive/research/gebaeude/BedZED_London_Hackbridge.md` | 7 | 7 | 0 | 5 | `p_bedzed_london_hackbridge` | ✓ |
| `q_berlin_schildow_pilot_house_2_md` | `_archive/research/gebaeude/Berlin_Schildow_Pilot_House_2.md` | 4 | 4 | 0 | 0 | `` | — |
| `q_berlin_schildow_pilot_house_md` | `_archive/research/gebaeude/Berlin_Schildow_Pilot_House.md` | 9 | 9 | 80 | 2 | `p_berlin_schildow_pilot_house` | ✓ |
| `q_bestandverplanzung_pavilion_muenchen_md` | `_archive/research/gebaeude/Bestandverplanzung_Pavilion_Muenchen.md` | 2 | 2 | 0 | 2 | `p_bestandverplanzung_pavilion_muenchen` | ✓ |
| `q_big_dig_building_boston_md` | `_archive/research/gebaeude/Big_Dig_Building_Boston.md` | 1 | 1 | 0 | 3 | `p_big_dig_building_boston` | ✓ |
| `q_big_dig_house_lexington_massachusetts_md` | `_archive/research/gebaeude/Big_Dig_House_Lexington_Massachusetts.md` | 8 | 8 | 0 | 4 | `p_big_dig_house_lexington_massachusetts` | ✓ |
| `q_biopartner_5_leiden_oegstgeest_md` | `_archive/research/gebaeude/BioPartner_5_Leiden_Oegstgeest.md` | 12 | 12 | 140 | 2 | `p_biopartner_5_leiden_oegstgeest` | ✓ |
| `q_bluecity_offices_rotterdam_md` | `_archive/research/gebaeude/BlueCity_Offices_Rotterdam.md` | 8 | 8 | 0 | 4 | `p_bluecity_offices_rotterdam` | ✓ |
| `q_boulder_fire_station_3_md` | `_archive/research/gebaeude/Boulder_Fire_Station_3.md` | 2 | 2 | 0 | 3 | `p_boulder_fire_station_3` | ✓ |
| `q_brent_cross_town_primary_substation_london_md` | `_archive/research/gebaeude/Brent_Cross_Town_Primary_Substation_London.md` | 6 | 6 | 0 | 7 | `p_brent_cross_town_primary_substation_london` | ✓ |
| `q_brighton_waste_house_brighton_md` | `_archive/research/gebaeude/Brighton_Waste_House_Brighton.md` | 8 | 8 | 0 | 2 | `p_brighton_waste_house_brighton` | ✓ |
| `q_broethen_twin_house_hoyerswerda_md` | `_archive/research/gebaeude/Broethen_Twin_House_Hoyerswerda.md` | 2 | 2 | 44 | 2 | `p_broethen_twin_house_hoyerswerda` | ✓ |
| `q_careno_be_circular_brussels_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/BE_NL_graph_ready_dossiers/Careno_Be_Circular_Brussels.md` | 6 | 6 | 0 | 0 | `p_careno_becircular` | ✓ |
| `q_cascadeup_london_secondary_timber_glulam_demonstrator_md` | `_archive/research/gebaeude/CascadeUp_London_secondary_timber_glulam_demonstrator.md` | 6 | 6 | 0 | 1 | `p_cascadeup_london_secondary_timber_glulam_demonstrator` | ✓ |
| `q_charles_malis_molenbeek_md` | `_archive/research/gebaeude/Charles_Malis_Molenbeek.md` | 1 | 1 | 0 | 2 | `p_charles_malis_molenbeek` | ✓ |
| `q_chiro_d_itterbeek_dilbeek_md` | `_archive/research/gebaeude/Chiro_d_Itterbeek_Dilbeek.md` | 6 | 6 | 153 | 3 | `p_chiro_d_itterbeek_dilbeek` | ✓ |
| `q_christ_pavilion_volkenroda_md` | `_archive/research/gebaeude/Christ_Pavilion_Volkenroda.md` | 8 | 8 | 0 | 2 | `p_christ_pavilion_volkenroda` | ✓ |
| `q_circl_abn_amro_urban_mining_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/BE_NL_graph_ready_dossiers/Circl_ABN_AMRO_Urban_Mining.md` | 8 | 8 | 0 | 0 | `p_circl_abn_amro` | ✓ |
| `q_circl_pavilion_amsterdam_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/BE_NL_graph_ready_dossiers/Circl_Pavilion_Amsterdam.md` | 15 | 15 | 0 | 0 | `` | — |
| `q_circular_centre_netherlands_prinsenhof_a_reuse_pilot_md` | `_archive/research/gebaeude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` | 7 | 7 | 0 | 2 | `p_circular_centre_netherlands_prinsenhof_a_reuse_pilot` | ✓ |
| `q_circular_pavilion_paris_md` | `_archive/research/gebaeude/Circular_Pavilion_Paris.md` | 1 | 1 | 0 | 2 | `p_circular_pavilion_paris` | ✓ |
| `q_crclr_house_impact_hub_berlin_md` | `_archive/research/gebaeude/CRCLR_House_Impact_Hub_Berlin.md` | 7 | 7 | 0 | 1 | `p_crclr_house_impact_hub_berlin` | ✓ |
| `q_elementa_walkeweg_basel_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/batch 1.md` | 7 | 7 | 0 | 0 | `p_elementa_walkeweg` | ✓ |
| `q_elys_kultur_gewerbehaus_basel_md` | `_archive/research/gebaeude/ELYS_Kultur_Gewerbehaus_Basel.md` | 8 | 8 | 0 | 2 | `p_elys_kultur_gewerbehaus_basel` | ✓ |
| `q_eth_circular_construction_programme_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/teaching_programme_graph_ready_dossiers/ETH_Circular_Construction_Programme.md` | 2 | 2 | 0 | 0 | `` | — |
| `q_europa_building_brussels_md` | `_archive/research/gebaeude/Europa_Building_Brussels.md` | 6 | 6 | 0 | 2 | `p_europa_building_brussels` | ✓ |
| `q_fcrbe_facilitating_circulation_reclaimed_building_elements_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/EU_consortia_graph_ready_dossiers/FCRBE_Facilitating_Circulation_Reclaimed_Building_Elements.md` | 3 | 3 | 0 | 0 | `` | — |
| `q_ferme_du_rail_paris_md` | `_archive/research/gebaeude/Ferme_du_Rail_Paris.md` | 6 | 6 | 102 | 4 | `p_ferme_du_rail_paris` | ✓ |
| `q_gjg_house_gentbrugge_md` | `_archive/research/gebaeude/gjG_House_Gentbrugge.md` | 4 | 4 | 78 | 2 | `p_gjg_house_gentbrugge` | ✓ |
| `q_granby_workshop_liverpool_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/uk_unclear_graph_ready_dossiers/Granby_Workshop_Liverpool.md` | 4 | 4 | 0 | 0 | `p_granby_workshop` | ✓ |
| `q_grande_halle_de_colombelles_md` | `_archive/research/gebaeude/Grande_Halle_de_Colombelles.md` | 8 | 8 | 164 | 4 | `p_grande_halle_de_colombelles` | ✓ |
| `q_grubenstrasse_29_werkhof_29_zuerich_md` | `_archive/research/gebaeude/Grubenstrasse_29_Werkhof_29_Zuerich.md` | 1 | 1 | 0 | 2 | `p_grubenstrasse_29_werkhof_29_zuerich` | ✓ |
| `q_harmalanranta_a_kruunu_recreate_mini_pilot_tampere_md` | `_archive/research/gebaeude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md` | 5 | 5 | 0 | 2 | `p_harmalanranta_a_kruunu_recreate_mini_pilot_tampere` | ✓ |
| `q_hastings_pier_visitor_centre_md` | `_archive/research/gebaeude/Hastings_Pier_Visitor_Centre.md` | 7 | 7 | 0 | 2 | `p_hastings_pier_visitor_centre` | ✓ |
| `q_haus_hos_mehrfamilienhaus_muehlhausen_md` | `_archive/research/gebaeude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` | 9 | 9 | 91 | 3 | `p_haus_hos_mehrfamilienhaus_muehlhausen` | ✓ |
| `q_holbein_gardens_london_md` | `_archive/research/gebaeude/Holbein_Gardens_London.md` | 12 | 12 | 146 | 6 | `p_holbein_gardens_london` | ✓ |
| `q_house_of_fraser_318_oxford_street_tbc_london_reuse_chain_md` | `_archive/research/gebaeude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` | 10 | 10 | 0 | 5 | `p_house_of_fraser_318_oxford_street_tbc_london_reuse_chain` | ✓ |
| `q_impact_hub_berlin_crclr_fitout_md` | `_archive/research/gebaeude/Impact_Hub_Berlin_CRCLR_Fitout.md` | 5 | 5 | 0 | 4 | `p_impact_hub_berlin_crclr_fitout` | ✓ |
| `q_institut_de_botanique_ulg_liege_md` | `_archive/research/gebaeude/Institut_de_Botanique_ULg_Liege.md` | 2 | 2 | 0 | 2 | `p_institut_de_botanique_ulg_liege` | ✓ |
| `q_interreg_nwe_fcrbe_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/EU_consortia_graph_ready_dossiers/Interreg_NWE_FCRBE.md` | 1 | 1 | 0 | 0 | `p_interreg_nwe_fcrbe` | ✓ |
| `q_jeugdkliniek_ithaka_emergis_kloetinge_md` | `_archive/research/gebaeude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` | 15 | 15 | 125 | 4 | `p_jeugdkliniek_ithaka_emergis_kloetinge` | ✓ |
| `q_juch_areal_recyclingzentrum_zuerich_md` | `_archive/research/gebaeude/Juch_Areal_Recyclingzentrum_Zuerich.md` | 9 | 9 | 115 | 2 | `p_juch_areal_recyclingzentrum_zuerich` | ✓ |
| `q_k118_kopfbau_halle_118_winterthur_md` | `_archive/research/gebaeude/K118_Kopfbau_Halle_118_Winterthur.md` | 9 | 9 | 130 | 4 | `p_k118_kopfbau_halle_118_winterthur` | ✓ |
| `q_ka13_kristian_augusts_gate_13_oslo_md` | `_archive/research/gebaeude/KA13_Kristian_Augusts_gate_13_Oslo.md` | 9 | 9 | 0 | 6 | `p_ka13_kristian_augusts_gate_13_oslo` | ✓ |
| `q_kamikatsu_zero_waste_center_hotel_why_md` | `_archive/research/gebaeude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` | 8 | 8 | 0 | 2 | `p_kamikatsu_zero_waste_center_hotel_why` | ✓ |
| `q_kindergarten_moeoeslistrasse_manegg_zuerich_md` | `_archive/research/gebaeude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` | 9 | 9 | 0 | 4 | `p_kindergarten_moeoeslistrasse_manegg_zuerich` | ✓ |
| `q_liander_alliander_hq_duiven_md` | `_archive/research/gebaeude/Liander_Alliander_HQ_Duiven.md` | 4 | 4 | 0 | 2 | `p_liander_alliander_hq_duiven` | ✓ |
| `q_lo_reninge_town_hall_facade_md` | `_archive/research/gebaeude/Lo_Reninge_Town_Hall_Facade.md` | 4 | 4 | 61 | 2 | `p_lo_reninge_town_hall_facade` | ✓ |
| `q_lokomotion_technology_centre_mini_pilot_tampere_md` | `_archive/research/gebaeude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md` | 5 | 5 | 0 | 2 | `p_lokomotion_technology_centre_mini_pilot_tampere` | ✓ |
| `q_lycee_michel_lucius_conversion_luxembourg_md` | `_archive/research/gebaeude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` | 6 | 6 | 94 | 2 | `p_lycee_michel_lucius_conversion_luxembourg` | ✓ |
| `q_lysp8_basel_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/DE_AT_CH_graph_ready_dossiers/LYSP8_Basel.md` | 5 | 5 | 0 | 0 | `p_lysp8_basel` | ✓ |
| `q_maison_des_canaux_paris_md` | `_archive/research/gebaeude/Maison_des_Canaux_Paris.md` | 4 | 4 | 0 | 2 | `p_maison_des_canaux_paris` | ✓ |
| `q_maison_dna_asse_md` | `_archive/research/gebaeude/Maison_DnA_Asse.md` | 3 | 3 | 57 | 2 | `p_maison_dna_asse` | ✓ |
| `q_maison_vignette_auderghem_md` | `_archive/research/gebaeude/Maison_Vignette_Auderghem.md` | 4 | 4 | 80 | 2 | `p_maison_vignette_auderghem` | ✓ |
| `q_meduni_campus_mariannengasse_wien_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/DE_AT_CH_graph_ready_dossiers/MedUni_Campus_Mariannengasse_Wien.md` | 3 | 3 | 0 | 0 | `p_meduni_campus_mariannengasse` | ✓ |
| `q_mehrow_pilot_house_md` | `_archive/research/gebaeude/Mehrow_Pilot_House.md` | 4 | 4 | 63 | 5 | `p_mehrow_pilot_house` | ✓ |
| `q_melkinlaituri_primary_school_daycare_centre_helsinki_md` | `_archive/research/gebaeude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` | 5 | 5 | 0 | 2 | `p_melkinlaituri_primary_school_daycare_centre_helsinki` | ✓ |
| `q_montessori_maassluis_md` | `_archive/research/gebaeude/Montessori_Maassluis.md` | 4 | 4 | 0 | 2 | `p_montessori_maassluis` | ✓ |
| `q_multi_brussels_reuse_in_multi_md` | `_archive/research/gebaeude/Multi_Brussels_Reuse_in_MULTI.md` | 8 | 8 | 0 | 2 | `p_multi_brussels_reuse_in_multi` | ✓ |
| `q_musee_de_folklore_mouscron_md` | `_archive/research/gebaeude/Musee_de_Folklore_Mouscron.md` | 6 | 6 | 96 | 4 | `p_musee_de_folklore_mouscron` | ✓ |
| `q_obk_27_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/uk_unclear_graph_ready_dossiers/OBK_27.md` | 3 | 3 | 0 | 0 | `p_obk_27` | ✓ |
| `q_peoples_pavilion_eindhoven_md` | `_archive/research/gebaeude/Peoples_Pavilion_Eindhoven.md` | 4 | 4 | 0 | 2 | `p_peoples_pavilion_eindhoven` | ✓ |
| `q_plattenpalast_berlin_md` | `_archive/research/gebaeude/Plattenpalast_Berlin.md` | 6 | 6 | 0 | 2 | `p_plattenpalast_berlin` | ✓ |
| `q_plattenvereinigung_berlin_md` | `_archive/research/gebaeude/Plattenvereinigung_Berlin.md` | 6 | 6 | 0 | 1 | `p_plattenvereinigung_berlin` | ✓ |
| `q_plp_london_hq_circular_studio_fitout_md` | `_archive/research/gebaeude/PLP_London_HQ_Circular_Studio_Fitout.md` | 4 | 4 | 0 | 3 | `p_plp_london_hq_circular_studio_fitout` | ✓ |
| `q_rcmi_concular_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/reuse_platform_graph_ready_dossiers/RCMI_Concular.md` | 9 | 9 | 0 | 0 | `p_rcmi_concular` | ✓ |
| `q_re_use_hoefe_wien_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/DE_AT_CH_graph_ready_dossiers/RE_USE_Hoefe_Wien.md` | 4 | 4 | 0 | 0 | `` | — |
| `q_reallabor_be_ware_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/DE_AT_CH_graph_ready_dossiers/Reallabor_Be_Ware.md` | 2 | 2 | 0 | 0 | `p_reallabor_be_ware` | ✓ |
| `q_rebridge_structural_reuse_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/EU_consortia_graph_ready_dossiers/REBRIDGE_Structural_Reuse.md` | 2 | 2 | 0 | 0 | `` | — |
| `q_recrete_footbridge_reused_concrete_blocks_md` | `_archive/research/gebaeude/ReCrete_footbridge_reused_concrete_blocks.md` | 5 | 5 | 0 | 1 | `p_recrete_footbridge_reused_concrete_blocks` | ✓ |
| `q_recyclinghaus_hannover_md` | `_archive/research/gebaeude/Recyclinghaus_Hannover.md` | 13 | 13 | 0 | 5 | `p_recyclinghaus_hannover` | ✓ |
| `q_recypark_demets_anderlecht_md` | `_archive/research/gebaeude/Recypark_Demets_Anderlecht.md` | 9 | 9 | 113 | 3 | `p_recypark_demets_anderlecht` | ✓ |
| `q_refair_bordeaux_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/reuse_platform_graph_ready_dossiers/REFAIR_Bordeaux.md` | 8 | 8 | 0 | 0 | `` | — |
| `q_resilience_la_ferme_des_possibles_stains_md` | `_archive/research/gebaeude/Resilience_La_Ferme_des_Possibles_Stains.md` | 7 | 7 | 133 | 7 | `p_resilience_la_ferme_des_possibles_stains` | ✓ |
| `q_resource_rows_copenhagen_md` | `_archive/research/gebaeude/Resource_Rows_Copenhagen.md` | 4 | 4 | 0 | 2 | `p_resource_rows_copenhagen` | ✓ |
| `q_reuse_logistics_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/EU_consortia_graph_ready_dossiers/Reuse_Logistics.md` | 6 | 6 | 0 | 0 | `p_reuse_logistics` | ✓ |
| `q_roots_in_the_sky_blackfriars_crown_court_md` | `_archive/research/gebaeude/Roots_in_the_Sky_Blackfriars_Crown_Court.md` | 11 | 11 | 91 | 2 | `p_roots_in_the_sky_blackfriars_crown_court` | ✓ |
| `q_saxum_vineyard_equipment_barn_paso_robles_md` | `_archive/research/gebaeude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` | 5 | 5 | 88 | 2 | `p_saxum_vineyard_equipment_barn_paso_robles` | ✓ |
| `q_schaerenmoosstrasse_zuerich_projekt_menage_a_trois_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/batch 1.md` | 2 | 2 | 0 | 0 | `p_schaerenmoosstrasse_zuerich` | ✓ |
| `q_stuttgart_210_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/DE_AT_CH_graph_ready_dossiers/Stuttgart_210.md` | 7 | 7 | 0 | 0 | `p_stuttgart_210` | ✓ |
| `q_superlocal_expogebouw_bleijerheide_md` | `_archive/research/gebaeude/Superlocal_Expogebouw_Bleijerheide.md` | 7 | 7 | 0 | 4 | `p_superlocal_expogebouw_bleijerheide` | ✓ |
| `q_svanen_kindergarten_gladsaxe_md` | `_archive/research/gebaeude/Svanen_Kindergarten_Gladsaxe.md` | 10 | 10 | 123 | 3 | `p_svanen_kindergarten_gladsaxe` | ✓ |
| `q_the_green_house_utrecht_md` | `_archive/research/gebaeude/The_Green_House_Utrecht.md` | 7 | 7 | 0 | 2 | `p_the_green_house_utrecht` | ✓ |
| `q_thoravej_29_copenhagen_md` | `_archive/research/gebaeude/Thoravej_29_Copenhagen.md` | 7 | 7 | 0 | 1 | `p_thoravej_29_copenhagen` | ✓ |
| `q_timber_square_london_md` | `_archive/research/gebaeude/Timber_Square_London.md` | 10 | 10 | 0 | 3 | `p_timber_square_london` | ✓ |
| `q_trae_high_rise_aarhus_md` | `_archive/research/gebaeude/TRAE_High_Rise_Aarhus.md` | 12 | 12 | 120 | 1 | `p_trae_high_rise_aarhus` | ✓ |
| `q_umar_unit_nest_empa_duebendorf_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/batch 1.md` | 6 | 6 | 0 | 0 | `p_umar_unit` | ✓ |
| `q_upcycle_studios_copenhagen_md` | `_archive/research/gebaeude/Upcycle_Studios_Copenhagen.md` | 6 | 6 | 0 | 5 | `p_upcycle_studios_copenhagen` | ✓ |
| `q_vandkunsten_component_reuse_programme_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/teaching_programme_graph_ready_dossiers/Vandkunsten_Component_Reuse_Programme.md` | 1 | 1 | 0 | 0 | `p_vandkunsten_component_reuse` | ✓ |
| `q_verbiest_karreveld_brussels_md` | `_archive/research/gebaeude/Verbiest_Karreveld_Brussels.md` | 9 | 9 | 0 | 2 | `p_verbiest_karreveld_brussels` | ✓ |
| `q_villa_welpeloo_enschede_md` | `_archive/research/gebaeude/Villa_Welpeloo_Enschede.md` | 10 | 10 | 0 | 4 | `p_villa_welpeloo_enschede` | ✓ |
| `q_woongroep_boschgaard_den_bosch_md` | `_archive/research/gebaeude/Woongroep_Boschgaard_Den_Bosch.md` | 10 | 10 | 0 | 3 | `p_woongroep_boschgaard_den_bosch` | ✓ |
| `q_zhaw_reuse_in_construction_md` | `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/teaching_programme_graph_ready_dossiers/ZHAW_Reuse_in_Construction.md` | 2 | 2 | 0 | 0 | `p_reuse_in_construction_zhaw` | ✓ |
| `q_zinneke_feder_masui4ever_brussels_md` | `_archive/research/gebaeude/Zinneke_Feder_Masui4ever_Brussels.md` | 4 | 4 | 122 | 5 | `p_zinneke_feder_masui4ever_brussels` | ✓ |

## Unmatched projects (loader could not infer a `p_<slug>` Projekt)

| dossier qmd | guessed projekt id |
|---|---|
| `q_berlin_schildow_pilot_house_2_md` | `p_berlin_schildow_pilot_house_2` |
| `q_circl_pavilion_amsterdam_md` | `p_circl_pavilion_amsterdam` |
| `q_re_use_hoefe_wien_md` | `p_re_use_hoefe_wien` |
| `q_fcrbe_facilitating_circulation_reclaimed_building_elements_md` | `p_fcrbe_facilitating_circulation_reclaimed_building_elements` |
| `q_rebridge_structural_reuse_md` | `p_rebridge_structural_reuse` |
| `q_refair_bordeaux_md` | `p_refair_bordeaux` |
| `q_eth_circular_construction_programme_md` | `p_eth_circular_construction_programme` |

These dossiers contributed ZITIERT_QUELLE (S-ref) links but no BELEGT_IN/cost_facts because the Projekt id derived from the file slug does not exist in the live graph. Agent 11 (consolidation) or Agent 8.b should add a slug-alias table.

## Legacy `qu_*_dossier` case_markdown anchors not touched

Agent 9 follows the manifest's `q_<slug>_md` naming convention. 16 batch-2 dossiers already had parallel case_markdown :Quelle nodes under a different (`qu_*_dossier`) naming scheme created by an earlier batch loader. These were intentionally NOT touched — Agent 11 (consolidation) should reconcile the two naming schemes (either via MERGE-by-source_file alias or by deleting one of the duplicate pairs). The 16 untouched legacy anchors are the only case_markdown :Quelle without a :ZITIERT_QUELLE child after this run; subtract them from the 116 total and the new coverage is 100 of 100 dossier units processed.

## Idempotency contract

Every BELEGT_IN edge written by this loader carries `_created_by='agent9_phase4b1'` and a stable `_cell_hash` (sha1(excerpt)[:12]). Re-runs first DELETE all loader edges per `(Projekt, dossier-S-ref-prefix)` pair and recreate them, so the graph converges to the parser's current output. q_<slug>_md and q_<slug>_sN :Quelle nodes are MERGE-by-id (no duplicates). Section-8 list facts are stripped per dossier-source prefix before appending fresh entries, so cost_facts/co2_facts/reuse_share_facts stay consistent on re-run.

## Errors

None recorded.
