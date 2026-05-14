# Round 003 Query Review: Donor / Receiver Completeness

## Result In Context

After the technical baseline, donor/receiver completeness is the first semantic query theme. The graph has 48 direct-reuse Bauteilgruppen without donor and 1 without receiver. None are auto-fixed here; every candidate is conservatively classified `SOURCE_CHECK`.

## Candidate Counts

| issue | count |
| --- | --- |
| missing_donor | 48 |
| missing_receiver | 1 |

## Review Table

| issue | disposition | project_id | bg_id | bg_name | known_other_endpoint |
| --- | --- | --- | --- | --- | --- |
| missing_donor | SOURCE_CHECK | p_altes_hobelwerk_winterthur | bg_altes_hobelwerk_laminatplatten | Kasten aus recycelten Laminatfurnierplatten (Cirkla) | bw_altes_hobelwerk_winterthur |
| missing_donor | SOURCE_CHECK | p_awm_muenster_circular_office | bg_awm_kabelkanaele_upcycling | Kabelkanäle als Regalböden und Leuchten (Upcycling) | bw_awm_muenster_office |
| missing_donor | SOURCE_CHECK | p_be_ware_reallabor_berlin | bg_be_ware_altholz_tragwerk | Altholz / Sekundärmaterialien als Tragwerk (mehrere Teilprojekte) | bw_be_ware_hub_spandau |
| missing_donor | SOURCE_CHECK | p_bedzed_london_hackbridge | bg_bedzed_misc_reuse | Diverses Reuse-Material (Türen, Bordsteine, Steinplatten, Geländerrohre) | bw_bedzed_housing_hackbridge |
| missing_donor | SOURCE_CHECK | p_bedzed_london_hackbridge | bg_bedzed_structural_steel | Wiedergewonnene Stahlträger (98t, 95% des Tragwerkstahls) | bw_bedzed_housing_hackbridge |
| missing_donor | SOURCE_CHECK | p_bedzed_london_hackbridge | bg_bedzed_timber_studs | Wiedergewonnene Nadelholzständer (54 km) | bw_bedzed_housing_hackbridge |
| missing_donor | SOURCE_CHECK | p_biopartner_5_leiden_oegstgeest | bg_biopartner_5_innenwaende_trennwaende | Wiederverwendete Innenwände und Trennwände | bw_biopartner_5 |
| missing_donor | SOURCE_CHECK | p_biopartner_5_leiden_oegstgeest | bg_biopartner_5_pflaster_naturstein_bodenmaterial | Wiederverwendete Pflaster-, Naturstein- und Bodenmaterialien | bw_biopartner_5 |
| missing_donor | SOURCE_CHECK | p_biopartner_5_leiden_oegstgeest | bg_biopartner_5_sanitaerobjekte | Wiederverwendete Sanitärobjekte | bw_biopartner_5 |
| missing_donor | SOURCE_CHECK | p_bluecity_offices_rotterdam | bg_bluecity_balustraden_oelplattform | Mögliche wiederverwendete Balustraden | bw_bluecity_offices |
| missing_donor | SOURCE_CHECK | p_bluecity_offices_rotterdam | bg_bluecity_betonbloecke_trennwaende | Betonblöcke als Trennwände | bw_bluecity_offices |
| missing_donor | SOURCE_CHECK | p_bluecity_offices_rotterdam | bg_bluecity_red_cedar_fensterrahmen_trennwaende | Red-Cedar-Fensterrahmen als Trennwände / innere Fassade | bw_bluecity_offices |
| missing_donor | SOURCE_CHECK | p_bluecity_offices_rotterdam | bg_bluecity_wiederverwendeter_stahl | Wiederverwendeter Stahl im Büroausbau | bw_bluecity_offices |
| missing_donor | SOURCE_CHECK | p_brent_cross_town_primary_substation_london | bg_brent_cross_oval_substation_screen | Ovaler Substation-Screen | bw_brent_cross_substation_screen |
| missing_donor | SOURCE_CHECK | p_brighton_waste_house_brighton | bg_brighton_betonbloecke | Wiederverwendete Betonblöcke | bw_brighton_waste_house |
| missing_donor | SOURCE_CHECK | p_brighton_waste_house_brighton | bg_brighton_holz_sperrholz | Holz und Sperrholz aus Reststücken | bw_brighton_waste_house |
| missing_donor | SOURCE_CHECK | p_brighton_waste_house_brighton | bg_brighton_teppichfliesen_fassade | Gebrauchte Teppichfliesen als Fassaden-/Außenschicht | bw_brighton_waste_house |
| missing_donor | SOURCE_CHECK | p_brighton_waste_house_brighton | bg_brighton_vinylbanner_dampfbremse | Vinylbanner als Dampfbremse | bw_brighton_waste_house |
| missing_donor | SOURCE_CHECK | p_crclr_house_impact_hub_berlin | bg_crclr_mdf_schwarz | Schwarzes MDF aus Berliner Club | bw_bestandshalle_crclr_kindl_areal |
| missing_donor | SOURCE_CHECK | p_crclr_house_impact_hub_berlin | bg_crclr_stahl_treppen | Stahlbauteile Hallendach als Treppenwangen | bw_bestandshalle_crclr_kindl_areal |
| missing_donor | SOURCE_CHECK | p_crclr_house_impact_hub_berlin | bg_crclr_tueren | Türen + Schiebetüren aus ehem. Impact Hub Berlin | bw_bestandshalle_crclr_kindl_areal |
| missing_donor | SOURCE_CHECK | p_elys_kultur_gewerbehaus_basel | bg_elys_bestehende_fassade | Bestehende grüne Trapezblechfassade teilweise erhalten | bw_elys_lysp_kultur_gewerbehaus |
| missing_donor | SOURCE_CHECK | p_elys_kultur_gewerbehaus_basel | bg_elys_fenster_fassade | ~200 verschiedene Fenster als Fassade (Lagerware/Fehlbestellungen) | bw_elys_lysp_kultur_gewerbehaus |
| missing_donor | SOURCE_CHECK | p_elys_kultur_gewerbehaus_basel | bg_elys_rueckbauholz_glulam | ~150m³ Rückbauholz als neue Leimbinder | bw_elys_lysp_kultur_gewerbehaus |
| missing_donor | SOURCE_CHECK | p_elys_kultur_gewerbehaus_basel | bg_elys_trapezblech | Trapezbleche aus ehem. Coop-Weinlager (beige) | bw_elys_lysp_kultur_gewerbehaus |
| missing_donor | SOURCE_CHECK | p_hobelwerk_haus_d_oberwinterthur | bg_hobelwerk_d_fenster_ausbau | Fenster + Ausbauteile (Reuse, Detaildaten begrenzt) | bw_hobelwerk_haus_d_winterthur |
| missing_donor | SOURCE_CHECK | p_k118_kopfbau_halle_118_winterthur | bg_k118_floor_finishes_bricks_panels | Wiederverwendete Naturstein-/Granitplatten, Klinker und Holzplatten | bw_k118_halle_118 |
| missing_donor | SOURCE_CHECK | p_k118_kopfbau_halle_118_winterthur | bg_k118_windows_cladding_insulation | Wiederverwendete Fenster, Fassadenbleche und EPS-Dämmung | bw_k118_halle_118 |
| missing_donor | SOURCE_CHECK | p_ka13_kristian_augusts_gate_13_oslo | bg_ka13_office_fronts_doors_facade | Wiederverwendete Bürofronten, Türen und Fassadenbekleidung | bw_ka13_oslo |
| missing_donor | SOURCE_CHECK | p_ka13_kristian_augusts_gate_13_oslo | bg_ka13_tga_sanitary_radiators | Wiederverwendete Radiatoren, Sanitär und Lüftungskanäle | bw_ka13_oslo |
| missing_donor | SOURCE_CHECK | p_lysp8_basel_lysbuechelareal | bg_lysp8_brettschichtholz | Brettschichtholz-Deckenelemente (~400m²) aus Formel-E-Pavillon | bw_lysp8_basel |
| missing_donor | SOURCE_CHECK | p_lysp8_basel_lysbuechelareal | bg_lysp8_dachziegel_fassade | Dachziegel als Fassadenverkleidung | bw_lysp8_basel |
| missing_donor | SOURCE_CHECK | p_lysp8_basel_lysbuechelareal | bg_lysp8_faserzement_fassade | Faserzement-Fassadenplatten (Reuse) | bw_lysp8_basel |
| missing_donor | SOURCE_CHECK | p_lysp8_basel_lysbuechelareal | bg_lysp8_fensterlaeden | Fensterläden Metall aus Zürcher Siedlung | bw_lysp8_basel |
| missing_donor | SOURCE_CHECK | p_lysp8_basel_lysbuechelareal | bg_lysp8_kuechen | ~30 Küchenzeilen (Reuse) | bw_lysp8_basel |
| missing_donor | SOURCE_CHECK | p_lysp8_basel_lysbuechelareal | bg_lysp8_sanitaer | WC-Becken, Armaturen, Sanitärkeramik | bw_lysp8_basel |
| missing_donor | SOURCE_CHECK | p_peoples_pavilion_eindhoven | bg_peoples_pavilion_borrowed_facade_elements | Geliehene Fassadenelemente | bw_peoples_pavilion_receiver |
| missing_donor | SOURCE_CHECK | p_peoples_pavilion_eindhoven | bg_peoples_pavilion_concrete_elements | Geliehene Betonpfähle / Betonelemente | bw_peoples_pavilion_receiver |
| missing_donor | SOURCE_CHECK | p_peoples_pavilion_eindhoven | bg_peoples_pavilion_glass_roof | Geliehenes Glasdach | bw_peoples_pavilion_receiver |
| missing_donor | SOURCE_CHECK | p_peoples_pavilion_eindhoven | bg_peoples_pavilion_wooden_beams | Geliehene Holzträger | bw_peoples_pavilion_receiver |
| missing_donor | SOURCE_CHECK | p_plp_london_hq_circular_studio_fitout | bg_plp_reclaimed_marble_feste_oberflaechen | Reclaimed marble / feste Oberflächen | bw_plp_circular_studio_white_chapel |
| missing_donor | SOURCE_CHECK | p_recyclinghaus_hannover | bg_recyclinghaus_abbruchziegel_innenwaende | Abbruchziegel in nichttragenden Innenwänden | bw_recyclinghaus_hannover |
| missing_donor | SOURCE_CHECK | p_recyclinghaus_hannover | bg_recyclinghaus_sanitaer_feste_einbauten | wiederverwendete Waschbecken / Sanitäreinbauten | bw_recyclinghaus_hannover |
| missing_donor | SOURCE_CHECK | p_recyclinghaus_hannover | bg_recyclinghaus_wellblech_fassade | wiederverwendetes Wellblech als Fassadenkomponente | bw_recyclinghaus_hannover |
| missing_donor | SOURCE_CHECK | p_reusebox_heilbronn | bg_reusebox_altholz | Altholz (Ausbau + Fassade) | bw_reusebox_heilbronn |
| missing_donor | SOURCE_CHECK | p_reusebox_heilbronn | bg_reusebox_stahltraeger | Wiedergewonnene Stahlträger (Tragwerk) | bw_reusebox_heilbronn |
| missing_donor | SOURCE_CHECK | p_trae_high_rise_aarhus | bg_trae_high_rise_aarhus_troldtekt_akustikplatten | Troldtekt-Akustikplatten | bw_tr_high_rise_holzhochhaus |
| missing_donor | SOURCE_CHECK | p_villa_welpeloo_enschede | bg_villa_welpeloo_enschede_bau_montagelift_als_innenlift | Bau-/Montagelift als Innenlift | bw_villa_welpeloo_wohnhaus_und_kunstlager |
| missing_receiver | SOURCE_CHECK | p_lysbuechel_parkhaus_basel | bg_lysbuechel_parkhaus_betonteile | Betonfertigteile: Stützen, Träger, Deckenplatten, Rampenplatten | bw_lysbuechel_parkhaus_basel |

## Patch Output

- `query_donor_receiver.patch.jsonl` is intentionally empty until source evidence confirms exact donor/receiver endpoints.
