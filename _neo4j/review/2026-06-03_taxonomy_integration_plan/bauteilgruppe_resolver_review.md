# Bauteilgruppe Resolver — manual review queue

Generated 378 entries.

- **auto_confirm** (exact slug): 273
- **auto_confirm** (high token match >=0.65): 0
- **needs_review** (0.35-0.65): 29
- **no_batch_equiv** (live BG unmatched): 48
- **new_candidate** (batch BG unmatched): 28

Decision keys (edit the CSV directly):
- `auto_confirm` -> resolver merges batch rows onto live BG
- `confirm`      -> human approves the proposed match
- `reject`       -> human says these aren't the same BG; mark live as no_batch_equiv and batch as new_candidate
- `merge_to:bg_X` -> assign to a different live or batch BG than the suggested one

## Per-project review

### p_biopartner_5_leiden_oegstgeest

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **new_candidate** | `_(none)_` | `bg_reuse_mehrere_ausbau_biopartner5_furniture_doors_candidate` | - |  |  | BioPartner Leiden says large-scale reuse ranges from donor steel to furniture and doors. |

### p_bluecity_offices_rotterdam

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **weak_guess** | `bg_reuse_stahl_gelaender_bluecity_oelplattform` | `bg_reuse_metall_gelaender_bluecity_oil_platform_balustrades` | 0.31 | Offshore-/Balustradenbauteil | unbekannte räumliche Einbauteile | Balustrades from a decommissioned oil platform are named among reclaimed office-wing materials. |
| **weak_guess** | `bg_reuse_beton_wand_bluecity_betonbloecke_trennwaende` | `bg_reuse_beton_innenwand_bluecity_original_concrete_blocks` | 0.21 | Bestands-/Baumaterial | Trennwände | Concrete blocks from the original water-park structure are repurposed into partition walls. |
| **weak_guess** | `bg_reuse_stahl_ausbau_bluecity` | `bg_reuse_stahl_tragwerk_bluecity_reused_steel` | 0.14 | unbekannt | unbekannte feste Bauteile im Büroausbau | Reused steel is named as the second material input for BlueCity Offices. |
| **no_batch_equiv** | `bg_reuse_mehrere_mehrere_bluecity_red_cedar_fensterrahmen_trennwaende` | `_(none)_` | - | Außenfenster | Trennwände und innere Fassade zwischen Büros und Gemeinschaftsbereichen |  |
| **new_candidate** | `_(none)_` | `bg_reuse_glas_innenwand_bluecity_reused_window_frames` | - |  |  | Reused window frames are described as the most important material input and are used as partition walls. |

### p_boulder_fire_station_3

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **no_batch_equiv** | `bg_reuse_glas_mehrere_boulder_pv_roof` | `_(none)_` | - | nicht anwendbar | Energieerzeugung |  |

### p_brent_cross_town_primary_substation_london

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **weak_guess** | `bg_reuse_stahl_fassade_brent_cross_new_support_members` | `bg_reuse_stahl_tragwerk_brent_cross_oil_pipeline_tubulars` | 0.27 | nicht anwendbar | Träger der farbigen Hülle / artwork | 33.46 tonnes of reclaimed/reused steel are reported for the substation. |
| **no_batch_equiv** | `bg_reuse_stahl_mehrere_brent_cross_bracing_members` | `_(none)_` | - | Pipeline-/Industrieprodukt | Aussteifung des Stahlrahmens |  |
| **no_batch_equiv** | `bg_reuse_stahl_mehrere_brent_cross_oval_substation_screen` | `_(none)_` | - | nicht anwendbar / Mischsystem | technische Einhausung und öffentliches Kunstwerk |  |
| **no_batch_equiv** | `bg_reuse_stahl_mehrere_brent_cross_tubular_columns` | `_(none)_` | - | Pipeline-/Industrieprodukt, teils ungenutzt | tragende Stützen des Substation-Screens |  |

### p_cascadeup_london_secondary_timber_glulam_demonstrator

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **weak_guess** | `bg_reuse_holz_mehrere_cascadeup_clst_floor_panels` | `bg_reuse_holz_wand_decke_cascadeup_clst_panels` | 0.26 | Rueckbauholz / unbekannt | Boden-/Deckenelement im Pilotbau | Secondary timber was manufactured into cross-laminated secondary timber wall and floor panels. |
| **weak_guess** | `bg_reuse_holz_mehrere_cascadeup_glulamst_frame` | `bg_reuse_holz_tragwerk_cascadeup_glulamst_frame` | 0.19 | massives Bauholz aus Rueckbau / vorherige Funktion unbekannt | tragender Rahmen des modularen Pilots | Secondary timber was manufactured into glued-laminated secondary timber for the structural frame. |
| **no_batch_equiv** | `bg_reuse_holz_wand_cascadeup_clst` | `_(none)_` | - | Rueckbauholz / unbekannt | Wand- und Raumbildung im Pilotbau |  |

### p_chiro_d_itterbeek_dilbeek

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **no_batch_equiv** | `bg_reuse_daemmstoff_daemmung_chiro_surplus_ceiling` | `_(none)_` | - | unbenutzt / Restposten | Deckendämmung |  |

### p_circl_abn_amro

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **no_batch_equiv** | `bg_dismantled_mehrere_boden_circl_floor_structure` | `_(none)_` | - |  |  |  |
| **no_batch_equiv** | `bg_dismantled_mehrere_technik_circl_solar_panels` | `_(none)_` | - |  |  |  |
| **no_batch_equiv** | `bg_planned_kunststoff_boden_circl_c2c_tarkett` | `_(none)_` | - |  |  |  |
| **no_batch_equiv** | `bg_planned_mehrere_technik_circl_leased_lighting` | `_(none)_` | - |  |  |  |
| **no_batch_equiv** | `bg_reuse_mehrere_ausbau_circl_greenery_harvest` | `_(none)_` | - |  |  |  |
| **no_batch_equiv** | `bg_reuse_metall_technik_circl_fire_hose_cabinets` | `_(none)_` | - |  |  |  |
| **no_batch_equiv** | `bg_reuse_mineralisch_boden_circl_pcm_tiles` | `_(none)_` | - |  |  |  |

### p_ferme_du_rail_paris

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **weak_guess** | `bg_reuse_naturstein_boden_ferme_slabs_fill` | `bg_reuse_stein_ferme_du_rail_reused_stones` | 0.19 | Dach- oder Bürofußbodenplatten | Boden-/Füllplatten; geplanter Dachterrasseneinsatz teils geändert | Reused stones are named among building materials. |
| **weak_guess** | `bg_reuse_holz_ausbau_ferme_fixed_cupboards` | `bg_reuse_holz_papier_ferme_du_rail_recycled_fibre_wall_panels` | 0.16 | unbekannt | feste Schränke in Wohnungen | Recycled wood or paper fibres are named for wall panels. |
| **weak_guess** | `bg_reuse_naturstein_mehrere_ferme_granite_kerbstones_retaining_wall` | `bg_reuse_keramik_fliese_ferme_du_rail_reused_tiles` | 0.14 | Bordstein | Stützmauer am Gemüsegarten | Reused tiles are named among building materials. |
| **no_batch_equiv** | `bg_reuse_holz_mehrere_ferme_window_frames_endgrain_floor` | `_(none)_` | - | Fenster | Holzpflaster / Parkett im Gemeinschaftsraum |  |
| **no_batch_equiv** | `bg_reuse_holz_mehrere_ferme_window_frames_roof_terrace` | `_(none)_` | - | Fenster | Dachterrassen-Akroterie, Pflanztröge, Geländer |  |
| **no_batch_equiv** | `bg_reuse_keramik_mehrere_ferme_tiles_bathroom_walls` | `_(none)_` | - | Restbestand / Bodenfliesen | Badwandbelag |  |
| **no_batch_equiv** | `bg_reuse_mehrere_boden_ferme_bitumen_concrete_blocks_paths` | `_(none)_` | - | Abbruchmaterial | Außenwege und Zirkulationen |  |
| **no_batch_equiv** | `bg_reuse_textil_mehrere_ferme_textile_sun_shading` | `_(none)_` | - | unklar | Sonnenschutzstores Restaurant |  |
| **new_candidate** | `_(none)_` | `bg_reuse_metall_ferme_du_rail_reused_metallic_elements` | - |  |  | Reused metallic elements are named among building materials. |
| **new_candidate** | `_(none)_` | `bg_reuse_textil_daemmung_ferme_du_rail_recycled_clothing_insulation` | - |  |  | Secondary source identifies recycled clothing from the Paris Emmaus network as insulation. |

### p_grande_halle_de_colombelles

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **no_batch_equiv** | `bg_reuse_keramik_mehrere_grande_halle_tiles_faience` | `_(none)_` | - | Wand-/Bodenbelag | Belag |  |

### p_grubenstrasse_29_werkhof_29_zuerich

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **weak_guess** | `bg_reuse_mehrere_dach_grubenstrasse_sheets` | `bg_reuse_mehrere_mehrere_grubenstrasse_site_storage` | 0.28 | Dach-/Blechdeckung | Dach/Shed-/Dachbereich | site storage of reuse material |
| **new_candidate** | `_(none)_` | `bg_reuse_holz_mehrere_grubenstrasse_old_roof_purlins` | - |  |  | alte Holzpfetten des vormaligen Flachdachs |

### p_hastings_pier_visitor_centre

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **needs_review** | `bg_reuse_holz_fassade_hastings_hardwood_cladding` | `bg_reuse_holz_fassade_hastings_pier_rescued_tropical_hardwood` | 0.38 | Deckbelag / Laufbelag auf Pier | Außenbekleidung Visitor Centre | Tropical hardwood pieces in the charred remains of the fire-damaged pier were rescued and reused. |
| **weak_guess** | `bg_reuse_holz_fassade_hastings_outbuilding_cladding` | `bg_reuse_holz_moebel_hastings_pier_deck_furniture` | 0.17 | Pier-Deckbohlen | Außenbekleidung Nebenbauten | Reclaimed timber boards were also used for external seating/furniture. |
| **no_batch_equiv** | `bg_retained_mehrere_mehrere_hastings_pier_restoration` | `_(none)_` | - | Pier und Pavillon | Pier und Restaurant-/Café-Pavillon |  |
| **no_batch_equiv** | `bg_reuse_holz_mehrere_hastings_clt_visitor_centre_structure` | `_(none)_` | - | neu | Tragwerk Visitor Centre |  |

### p_house_of_fraser_318_oxford_street_tbc_london_reuse_chain

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **no_batch_equiv** | `bg_reuse_ziegel_mehrere_tbc_fixtures` | `_(none)_` | - | Bauteile / Ausbauelemente im Bestand | unbekannte wiederverwendete Elemente in TBC |  |

### p_k118_kopfbau_halle_118_winterthur

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **weak_guess** | `bg_reuse_stahl_mehrere_k118_structure` | `bg_reuse_stahl_mehrere_k118_kopfbau_halle_118_winterthur_stahltraeger_candidate` | 0.24 | Tragwerk einer Halle im ELYS-Projekt Basel | Tragwerk der dreigeschossigen K.118-Aufstockung | Upcycling Architecture identifies the steel skeleton as formerly part of a distribution centre in Basel. |
| **weak_guess** | `bg_reuse_stahl_mehrere_k118_external_stair` | `bg_reuse_stahl_erschliessung_k118_aussentreppe_orion_candidate` | 0.19 | Fluchttreppe / Außentreppe Orion-Bürogebäude Zürich | Erschließung / Fluchtweg K.118 | Jidipi states the three new floors are accessed by a steel exterior staircase from the demolished Orion office building. |
| **weak_guess** | `bg_reuse_mehrere_mehrere_k118_floor_finishes_bricks_panels` | `bg_reuse_naturstein_fassade_k118_granit_orion_candidate` | 0.11 | Beläge / Bühnen- oder Rückbaubauteile | Böden, Wände und Innenausbau K.118 | Upcycling Architecture lists granite facades repurposed from the Orion office building. |
| **no_batch_equiv** | `bg_retained_mehrere_mehrere_k118_halle_118` | `_(none)_` | - | Industriehalle | Sockel und Bestand der Aufstockung |  |
| **no_batch_equiv** | `bg_reuse_mehrere_mehrere_k118_windows_cladding_insulation` | `_(none)_` | - | Hüll- und Ausbauteile aus Rückbauquellen | Hülle der K.118-Aufstockung |  |

### p_liander_alliander_hq_duiven

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **no_batch_equiv** | `bg_retained_mehrere_mehrere_alliander_existing_buildings` | `_(none)_` | - | Büro-/Betriebsgebäude | weitergenutzte Büro-/Campusstruktur |  |
| **no_batch_equiv** | `bg_reuse_mehrere_ausbau_alliander_material_passport_inventory` | `_(none)_` | - | Materialinformation | Datenbasis für Rückbaubarkeit und Zirkularität |  |
| **no_batch_equiv** | `bg_reuse_mehrere_mehrere_alliander_common_roof_atrium` | `_(none)_` | - | unbekannt / überwiegend neu oder unklar | räumliche Verbindung und Hülle des Campus |  |
| **no_batch_equiv** | `bg_reuse_mehrere_mehrere_alliander_interior_elements` | `_(none)_` | - | Innenausbau / Bauteile im Bestand oder Donorquellen | Innenausbau des HQ |  |
| **new_candidate** | `_(none)_` | `bg_reuse_asphalt_liander_existing_roofs` | - |  |  | asphalt from existing roofs recycled |
| **new_candidate** | `_(none)_` | `bg_reuse_bestand_liander_existing_constructions` | - |  |  | majority of existing constructions maintained |
| **new_candidate** | `_(none)_` | `bg_reuse_beton_liander_demolished_concrete` | - |  |  | concrete from demolished parts reused |
| **new_candidate** | `_(none)_` | `bg_reuse_decke_liander_existing_ceiling_plates` | - |  |  | existing ceiling plates reused |
| **new_candidate** | `_(none)_` | `bg_reuse_holz_fassade_liander_waste_wood_facades` | - |  |  | waste wood used for facades |
| **new_candidate** | `_(none)_` | `bg_reuse_sanitaer_liander_existing_toilets` | - |  |  | existing toilets reused |
| **new_candidate** | `_(none)_` | `bg_reuse_stahl_tragwerk_liander_extension_steel` | - |  |  | steel construction reused for extensions |
| **new_candidate** | `_(none)_` | `bg_reuse_tuer_moebel_liander_doors_to_furniture` | - |  |  | existing doors converted into new furniture |

### p_lo_reninge_town_hall_facade

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **weak_guess** | `bg_reuse_ziegel_mehrere_lo_reninge_facade` | `bg_reuse_ziegel_fassade_lo_reninge_reclaimed_yellow_brick` | 0.13 | Mauerwerk / Fassade unbekannter Herkunft | Fassadenmauerwerk der Erweiterung | The town hall extension uses recycled/reclaimed brick selected to relate to the convent brick. |
| **no_batch_equiv** | `bg_retained_mehrere_mehrere_lo_reninge_convent` | `_(none)_` | - | Kloster / Bestand | Rathausbestand und Kontext |  |
| **new_candidate** | `_(none)_` | `bg_reuse_papier_daemmung_lo_reninge_recycled_paper_insulation` | - |  |  | The timber-stud external walls are filled with recycled paper insulation. |

### p_maison_des_canaux_paris

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **weak_guess** | `bg_reuse_mehrere_mehrere_maison_des_canaux_fixed_builtins` | `bg_reuse_moebel_canaux_reclaimed_furniture` | 0.16 | unbekannt | feste Ausstattung / TGA / Beleuchtung | Reclaimed and refurbished furniture is repeatedly named in phase 1. |
| **weak_guess** | `bg_reuse_mehrere_mehrere_maison_des_canaux_floor_wall_finishes` | `bg_reuse_holz_boden_canaux_refurbished_wooden_floor` | 0.14 | Oberfläche / Belag | fester Innenausbau | Wooden floors were conserved/refurbished in most spaces. |
| **weak_guess** | `bg_reuse_mehrere_mehrere_maison_des_canaux_sanitary_parts` | `bg_reuse_keramik_fliese_canaux_terracotta_wall_covering` | 0.11 | Sanitärobjekt | Sanitärinstallation | Terracotta tiles were reused as wall coverings in sanitary rooms. |
| **weak_guess** | `bg_reuse_mehrere_mehrere_maison_des_canaux_doors` | `bg_reuse_holz_aussenraum_canaux_landing_doors_decking_lattice` | 0.11 | Tür / Raumabschluss | Tür / Raumabschluss | 378 landing doors from three sources were repurposed into terrace decking/lattice elements. |
| **new_candidate** | `_(none)_` | `bg_reuse_holz_ausbau_canaux_archive_furniture_acoustic_desks` | - |  |  | Archive furniture wood was used for desks/acoustic insulation or donated to workshops. |
| **new_candidate** | `_(none)_` | `bg_reuse_leuchten_canaux_lighting_fixtures_parchment` | - |  |  | Lighting fixtures and luminous artworks are named as reused/repurposed elements. |

### p_maison_vignette_auderghem

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **weak_guess** | `bg_reuse_keramik_mehrere_maison_vignette_terracotta_floor_tiles` | `bg_reuse_mehrere_maison_vignette_reclaimed_recycled_package` | 0.19 | Bodenbelag | Bodenbelag | The house uses bio-based and reclaimed/recycled materials including straw, clay plaster, reused bricks, adhesive-free ti |
| **weak_guess** | `bg_reuse_ziegel_mehrere_maison_vignette_facade_claustra` | `bg_reuse_ziegel_fassade_maison_vignette_reused_facing_bricks` | 0.15 | Mauerwerksziegel unbekannter Herkunft | vordere Fassaden-Claustra | Urban Brussels identifies reused facing bricks among the bio-based/reclaimed/recycled material set. |
| **no_batch_equiv** | `bg_reuse_keramik_mehrere_maison_vignette_wall_tiles_solvay` | `_(none)_` | - | Wand-/Innenbekleidung | Wandfliesen Sanitär/Innenraum |  |
| **no_batch_equiv** | `bg_reuse_mehrere_mehrere_maison_vignette_sanitary_objects` | `_(none)_` | - | Sanitärausstattung | Bäder und Atelierbecken |  |
| **no_batch_equiv** | `bg_reuse_naturstein_boden_maison_vignette_bluestone_slabs` | `_(none)_` | - | Boden-/Außenplatten unbekannter Herkunft | Eingangshalle und Terrasse |  |

### p_meduni_campus_mariannengasse

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **no_batch_equiv** | `bg_retained_mehrere_decke_medunicampus_glasdecke` | `_(none)_` | - |  |  |  |

### p_melkinlaituri_primary_school_daycare_centre_helsinki

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **new_candidate** | `_(none)_` | `bg_candidate_melkinlaituri_acoustic_ceiling_tiles_recycled_mineral_wool` | - |  |  | acoustic ceiling tiles contain approximately 50% recycled mineral wool content |
| **new_candidate** | `_(none)_` | `bg_candidate_melkinlaituri_recycled_glass_wool_insulation` | - |  |  | recycled glass wool specified for external wall assemblies and internal partitions |

### p_multi_brussels_reuse_in_multi

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **weak_guess** | `bg_reuse_naturstein_boden_multi_granite_natural_tiles` | `bg_reuse_stein_boden_multi_generale_granite_flooring` | 0.30 | Boden-/Außenbeläge aus externen Quellen | Treppenpodest, Atriumboden und öffentliche Terrasse | Flamed granite flooring from Generale de Banque was placed on the public staircase landing. |
| **weak_guess** | `bg_reuse_naturstein_mehrere_multi_blaustein_facade_slabs` | `bg_reuse_stein_multi_bluestone_blocks_plinth` | 0.30 | Fassadenbekleidung des Brouckère Tower | Terrasse, Wandbekleidung, Plinthe und Innenraumflächen | Bluestone blocks were dismantled from the plinth rear facade and reused in situ on the new plinth and atrium. |
| **weak_guess** | `bg_reuse_stahl_technik_multi_reinstalled_elevator_motors` | `bg_reuse_technik_multi_elevator_engines` | 0.22 | Aufzugstechnik im Bestandsgebäude | eine Etage höher wieder installierte Aufzugstechnik | Elevator engines were dismantled and reinstalled one floor up. |
| **no_batch_equiv** | `bg_reuse_aluminium_mehrere_multi_profiles` | `_(none)_` | - | Gebäude-/Fassadenelemente im Brouckère Tower | Balustraden und Lichtarmaturen |  |
| **new_candidate** | `_(none)_` | `bg_reuse_aluminium_profile_multi_facade_h_profiles` | - |  |  | Aluminium H-profiles from the original facade became lobby light fittings and atrium guardrails. |
| **new_candidate** | `_(none)_` | `bg_reuse_stein_boden_multi_bruges_bluestone_flagstones` | - |  |  | Bluestone flagstones from a square in Bruges were salvaged/dimensioned and installed as atrium flooring. |
| **new_candidate** | `_(none)_` | `bg_reuse_stein_boden_multi_paris_granite_terrace` | - |  |  | Public-terrace floor cladding consists of reclaimed granite from a Paris office building. |

### p_resource_rows_copenhagen

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **new_candidate** | `_(none)_` | `bg_reuse_holz_mehrere_resource_rows_metro_wastewood_candidate` | - |  |  | CMS states Resource Rows implemented wood discarded after Copenhagen metro construction projects. |

### p_schaerenmoosstrasse_zuerich

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **no_batch_equiv** | `bg_planned_mehrere_technik_sms_zuerich_pv_roof` | `_(none)_` | - |  |  |  |
| **no_batch_equiv** | `bg_planned_stahl_fassade_sms_zuerich_arcade` | `_(none)_` | - |  |  |  |
| **no_batch_equiv** | `bg_retained_mehrere_mehrere_sms_zuerich_existing_bldgs` | `_(none)_` | - |  |  |  |
| **no_batch_equiv** | `bg_retained_stahlbeton_treppe_sms_zuerich_existing_stairs` | `_(none)_` | - |  |  |  |
| **no_batch_equiv** | `bg_reuse_mehrere_mehrere_sms_zuerich_ubs_hall` | `_(none)_` | - |  |  |  |
| **new_candidate** | `_(none)_` | `bg_retained_mehrere_mehrere_schaerenmoos_office_structure` | - |  |  | The project is a conversion of existing commercial/office stock into housing; retained existing structure should be mapp |
| **new_candidate** | `_(none)_` | `bg_reuse_metall_fassade_schaerenmoos_fassade_absturz` | - |  |  | PWG reporting/search evidence mentions façade/cladding and fall-protection/railing ReUse metal elements. |
| **new_candidate** | `_(none)_` | `bg_reuse_stahl_mehrere_schaerenmoos_dachpergolen` | - |  |  | PWG reporting/search evidence separates ReUse steel roof pergolas from balcony/arcade elements. |
| **new_candidate** | `_(none)_` | `bg_reuse_stahl_mehrere_schaerenmoos_laubengang_balkone` | - |  |  | PWG public reporting/search evidence states the project uses ReUse steel elements for balcony/arcade elements; add as pl |

### p_superlocal_expogebouw_bleijerheide

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **no_batch_equiv** | `bg_reuse_mehrere_mehrere_superlocal_haustueren_gelaender_bruestungen` | `_(none)_` | - | Innen-/Außenbauteile der Flat | feste Einbauten, Hüll- und Sicherheitsbauteile im Pavillon |  |

### p_svanen_kindergarten_gladsaxe

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **new_candidate** | `_(none)_` | `bg_reuse_mehrere_mehrere_svanen_clock_dome_washbasins` | - |  |  | school clock, dome, washbasins and narrative elements is mapped as a recovered material/component stream from the former |

### p_the_green_house_utrecht

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **no_batch_equiv** | `bg_reuse_daemmstoff_mehrere_green_house_daemmung_holzbodenelemente` | `_(none)_` | - | Dämmmaterial / Herkunft unbekannt | Akustik-/Deckenelementfüllung |  |
| **no_batch_equiv** | `bg_reuse_holz_mehrere_green_house_feste_wandverkleidung` | `_(none)_` | - | Innenausbau / Oberfläche unbekannt | feste Innenoberfläche im Pavillon |  |

### p_timber_square_london

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **no_batch_equiv** | `bg_reuse_holz_mehrere_square_clt_hybrid_decken` | `_(none)_` | - | neu / nicht reused | Decken in Hybrid-Stahl/CLT-Struktur |  |

### p_umar_unit

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **weak_guess** | `bg_reuse_daemmstoff_daemmung_umar_mycelium` | `bg_reuse_daemmstoff_daemmung_umar_repurposed_insulation` | 0.20 |  |  | repurposed insulation materials |
| **no_batch_equiv** | `bg_reuse_glas_keramik_fassade_umar_magna_glass` | `_(none)_` | - |  |  |  |
| **no_batch_equiv** | `bg_reuse_holz_wand_umar_timber_facade` | `_(none)_` | - |  |  |  |
| **no_batch_equiv** | `bg_reuse_kunststoff_boden_umar_carpets` | `_(none)_` | - |  |  |  |
| **no_batch_equiv** | `bg_reuse_metall_fassade_umar_alu_copper` | `_(none)_` | - |  |  |  |

### p_upcycle_studios_copenhagen

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **weak_guess** | `bg_reuse_glas_fenster_upcycle_studios_copenhagen_doppelverglaste` | `bg_reuse_glas_fenster_upcycle_studios_repurposed_double_glazing` | 0.31 | Fenster in öffentlichen Wohnbauten | Fenster / Gebäudehülle | Repurposed double-glazing windows are named as a project material innovation. |
| **weak_guess** | `bg_reuse_mehrere_mehrere_upcycle_recyclingbeton_metro` | `bg_reuse_beton_tragwerk_upcycle_studios_recycled_concrete` | 0.17 | Betonabbruch / Metro-Baustellenabfall | Beton in Neubau | Recycled concrete is one of the named material innovations developed for the row houses. |
| **weak_guess** | `bg_reuse_holz_mehrere_upcycle_dinesen_offcuts` | `bg_reuse_holz_ausbau_upcycle_studios_discarded_flooring_boards` | 0.17 | Produktionsrest / floorboard offcuts | Boden, Wand und Fassadenbekleidung | Discarded flooring boards are named as a project material innovation. |

### p_woongroep_boschgaard_den_bosch

| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |
|---|---|---|---:|---|---|---|
| **new_candidate** | `_(none)_` | `bg_retained_mehrere_mehrere_boschgaard_existing_building` | - |  |  | The old community-centre building was retained as the basis for a self-build cohousing transformation. |
