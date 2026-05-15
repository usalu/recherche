# Vocab node degree report

Live Neo4j `mit-bestand`. Generated 2026-05-15.

Each section lists vocab nodes sorted by inbound degree from content nodes (Bauteilgruppe, Bauwerk, Projekt, Akteur — not Quelle). Zero rows = orphan in current corpus; 1-2 rows = sparse, candidate for review.

## Quick orphan summary

Labels with all-or-most zero-inbound nodes are the strongest candidates for vocabulary pruning.

| Label | total | zero-inbound | 1-inbound |
| --- |---:|---:|---:|
| Material | 19 | 1 | 3 |
| Materialgruppe | 10 | 0 | 1 |
| Bauteiltyp | 15 | 0 | 0 |
| Bauteilebene | 6 | 0 | 2 |
| Huerde | 28 | 0 | 0 |
| HuerdeKategorie | 10 | 1 | 0 |
| Akteurrolle | 24 | 7 | 0 |
| Akteurtyp | 10 | 0 | 1 |
| Bauobjektrolle | 6 | 0 | 1 |
| Bauobjektklasse | 8 | 0 | 1 |
| BauaufgabeIntervention | 10 | 0 | 0 |
| Bausystem | 9 | 1 | 1 |
| Bauweise | 6 | 0 | 1 |
| Tragwerksprinzip | 4 | 0 | 1 |
| Nutzung | 9 | 0 | 0 |
| Status | 11 | 0 | 1 |
| WiederverwendungsArt | 11 | 0 | 0 |
| Funktionswechsel | 6 | 1 | 0 |
| Land | 13 | 0 | 0 |
| Stadt | 62 | 0 | 13 |
| Norm | 16 | 5 | 3 |
| PruefungNachweis | 11 | 2 | 0 |
| Leistungsanforderung | 12 | 3 | 0 |
| Methode | 13 | 1 | 1 |
| Rueckbauverfahren | 5 | 0 | 0 |
| Aufbereitungsverfahren | 11 | 1 | 0 |
| Prozessphase | 10 | 0 | 0 |
| Logistik | 10 | 0 | 1 |
| Beschaffungsweg | 10 | 1 | 0 |
| Ressourcenquelle | 16 | 0 | 1 |
| Verbindungstechnik | 8 | 1 | 2 |
| RechtlicheBedingung | 9 | 3 | 3 |
| Schadstoff | 5 | 4 | 1 |
| Wirtschaft | 6 | 2 | 2 |
| ZertifizierungBewertungssystem | 7 | 1 | 3 |
| Programm | 15 | 7 | 2 |
| Tool | 6 | 0 | 1 |
| Software | 7 | 0 | 2 |

**Total zero-inbound vocab nodes: 42**  |  **Total 1-inbound: 48**

---

## Material (19 nodes)

| inbound | id | name |
| ---:|---|---|
| 0 | mat_stroh | Stroh |
| 1 | mat_bitumen | Bitumen |
| 1 | mat_faserzement | Faserzement / Eternit |
| 1 | mat_lehm | Lehm |
| 2 | mat_gusseisen | Gusseisen |
| 2 | mat_mdf | MDF / mitteldichte Faserplatte |
| 3 | mat_recyclingbeton | Recyclingbeton |
| 4 | mat_textil | Textil |
| 11 | mat_kunststoff | Kunststoff |
| 12 | mat_aluminium | Aluminium |
| 16 | mat_daemmstoff | Daemmstoff |
| 19 | mat_naturstein | Naturstein |
| 23 | mat_ziegel | Ziegel |
| 31 | mat_keramik | Keramik |
| 37 | mat_stahlbeton | Stahlbeton |
| 41 | mat_glas | Glas |
| 51 | mat_beton | Beton |
| 87 | mat_holz | Holz |
| 111 | mat_stahl | Stahl |

## Materialgruppe (10 nodes)

| inbound | id | name |
| ---:|---|---|
| 1 | mg_unbekannt | Unbekannt |
| 2 | mg_lehm_erde | Lehm_Erde |
| 3 | mg_recyclingmaterial | Recyclingmaterial |
| 5 | mg_kunststoff | Kunststoff |
| 10 | mg_verbundstoff | Verbundstoff |
| 14 | mg_daemmstoff | Daemmstoff |
| 43 | mg_glas_keramik | Glas_Keramik |
| 51 | mg_mineralisch | Mineralisch |
| 56 | mg_holz_biobasiert | Holz_Biobasiert |
| 68 | mg_metall | Metall |

## Bauteiltyp (15 nodes)

| inbound | id | name |
| ---:|---|---|
| 8 | bt_fundament | Fundament |
| 12 | bt_treppe | Treppe |
| 13 | bt_gelaender | Gelaender |
| 14 | bt_daemmung | Daemmung |
| 19 | bt_tuer | Tuer |
| 22 | bt_dach | Dach |
| 29 | bt_fenster | Fenster |
| 38 | bt_technik | Technik |
| 39 | bt_stuetze | Stuetze |
| 44 | bt_boden | Boden |
| 45 | bt_ausbau | Ausbau |
| 50 | bt_decke | Decke |
| 57 | bt_traeger | Traeger |
| 75 | bt_wand | Wand |
| 80 | bt_fassade | Fassade |

## Bauteilebene (6 nodes)

| inbound | id | name |
| ---:|---|---|
| 1 | be_gebaeudeteil | Gebaeudeteil |
| 1 | be_materialcharge | Materialcharge |
| 2 | be_einzelbauteil | Einzelbauteil |
| 6 | be_oberflaechenschicht | Oberflaechenschicht |
| 21 | be_system | System |
| 246 | be_bauteilgruppe | Bauteilgruppe |

## Huerde (28 nodes)

| inbound | id | name |
| ---:|---|---|
| 4 | h_ausschreibungsproblem | Ausschreibungsproblem |
| 4 | h_fehlende_datenstandards | Fehlende_Datenstandards |
| 6 | h_fehlende_standardisierung | Fehlende_Standardisierung |
| 7 | h_akzeptanzproblem | Akzeptanzproblem |
| 9 | h_schadstoffbelastung | Schadstoffbelastung |
| 11 | h_bauproduktstatus | Bauproduktstatus |
| 13 | h_fehlende_lagerflaeche | Fehlende_Lagerflaeche |
| 13 | h_haftung | Haftung |
| 13 | h_terminunsicherheit | Terminunsicherheit |
| 19 | h_unkonventionelles_material | Unkonventionelles_Material |
| 20 | h_dauerhaftigkeit_restlebensdauer | Dauerhaftigkeit_Restlebensdauer |
| 22 | h_entwurfsbindung | Entwurfsbindung |
| 23 | h_zustand_unklar | Zustand_Unklar |
| 24 | h_aufbereitungsaufwand | Aufbereitungsaufwand |
| 25 | h_hygieneanforderung | Hygieneanforderung |
| 27 | h_heterogenitaet_chargen | Heterogenitaet_Chargen |
| 29 | h_bruch_beschaedigungsrisiko | Bruch_Beschaedigungsrisiko |
| 32 | h_mengenunsicherheit | Mengenunsicherheit |
| 34 | h_verfuegbarkeitsproblem | Verfuegbarkeitsproblem |
| 40 | h_toleranzen | Toleranzen |
| 41 | h_brandschutzkonflikt | Brandschutzkonflikt |
| 44 | h_witterung_feuchte | Witterung_Feuchte |
| 45 | h_gewaehrleistung | Gewaehrleistung |
| 46 | h_anschlussproblem | Anschlussproblem |
| 53 | h_materialqualitaet_unklar | Materialqualitaet_Unklar |
| 59 | h_kompatibilitaetsproblem | Kompatibilitaetsproblem |
| 132 | h_datenluecke | Datenluecke |
| 179 | h_technische_freigabe | Technische_Freigabe |

## HuerdeKategorie (10 nodes)

| inbound | id | name |
| ---:|---|---|
| 0 | hk_unklar | Unklar |
| 3 | hk_planerisch | Planerisch |
| 3 | hk_sozial_organisatorisch | Sozial_Organisatorisch |
| 4 | hk_beschaffung_markt | Beschaffung_Markt |
| 7 | hk_wirtschaftlich | Wirtschaftlich |
| 8 | hk_umwelt_gesundheit | Umwelt_Gesundheit |
| 13 | hk_logistisch | Logistisch |
| 27 | hk_rechtlich | Rechtlich |
| 35 | hk_daten_evidenz | Daten_Evidenz |
| 63 | hk_technisch | Technisch |

## Akteurrolle (24 nodes)

| inbound | id | name |
| ---:|---|---|
| 0 | ar_brandschutz_barrierefreiheit | Brandschutz_Barrierefreiheit |
| 0 | ar_fassade | Fassade |
| 0 | ar_kunst_gestaltung | Kunst_Gestaltung |
| 0 | ar_landschaftsplanung | Landschaftsplanung |
| 0 | ar_software_digitalisierung | Software_Digitalisierung |
| 0 | ar_stahlbau_fertigung | Stahlbau_Fertigung |
| 0 | ar_tga_gebaeudetechnik | TGA_Gebaeudetechnik |
| 3 | ar_nachhaltigkeitsberatung | Nachhaltigkeitsberatung |
| 3 | ar_tragwerksplanung | Tragwerksplanung |
| 4 | ar_reuse_beratung | Reuse_Beratung |
| 16 | ar_unbestimmt | Unbestimmt |
| 17 | ar_aufbereitung_refurbishment | Aufbereitung_Refurbishment |
| 19 | ar_bildung_wissenstransfer | Bildung_Wissenstransfer |
| 30 | ar_oeffentliche_hand_foerderung | Oeffentliche_Hand_Foerderung |
| 33 | ar_betrieb_nutzung | Betrieb_Nutzung |
| 34 | ar_rueckbau_bauteilernte_logistik | Rueckbau_Bauteilernte_Logistik |
| 65 | ar_bauausfuehrung_fertigung | Bauausfuehrung_Fertigung |
| 75 | ar_projektmanagement_koordination | Projektmanagement_Koordination |
| 79 | ar_bauherr_auftraggeber | Bauherr_Auftraggeber |
| 86 | ar_materiallieferung_markt | Materiallieferung_Markt |
| 120 | ar_fachplanung_nachweis | Fachplanung_Nachweis |
| 126 | ar_forschung_dokumentation | Forschung_Dokumentation |
| 197 | ar_entwurf_planung | Entwurf_Planung |
| 203 | ar_reuse_zirkularitaetsberatung | Reuse_Zirkularitaetsberatung |

## Akteurtyp (10 nodes)

| inbound | id | name |
| ---:|---|---|
| 1 | at_unbekannt | Unbekannt |
| 4 | at_foerdergeber_programmtraeger | Foerdergeber_Programmtraeger |
| 8 | at_software_tool_anbieter | Software_Tool_Anbieter |
| 16 | at_materialhub_bauteilboerse | Materialhub_Bauteilboerse |
| 18 | at_ngo_verband_netzwerk | NGO_Verband_Netzwerk |
| 27 | at_oeffentliche_institution | Oeffentliche_Institution |
| 30 | at_organisation | Organisation |
| 36 | at_forschung_lehre | Forschung_Lehre |
| 143 | at_person | Person |
| 298 | at_unternehmen | Unternehmen |

## Bauobjektrolle (6 nodes)

| inbound | id | name |
| ---:|---|---|
| 1 | bor_referenzobjekt | Referenzobjekt |
| 9 | bor_zwischenlager | Zwischenlager |
| 18 | bor_same_site_donor_receiver | Same_Site_Donor_Receiver |
| 22 | bor_bestandsobjekt | Bestandsobjekt |
| 68 | bor_empfaengerobjekt | Empfaengerobjekt |
| 99 | bor_donorobjekt | Donorobjekt |

## Bauobjektklasse (8 nodes)

| inbound | id | name |
| ---:|---|---|
| 1 | bok_reuse_centre | Reuse_Centre |
| 3 | bok_quartier_areal | Quartier_Areal |
| 5 | bok_innenausbau | Innenausbau |
| 8 | bok_gebaeudeteil | Gebaeudeteil |
| 11 | bok_pavillon | Pavillon |
| 15 | bok_depot_lager | Depot_Lager |
| 18 | bok_infrastruktur | Infrastruktur |
| 153 | bok_gebaeude | Gebaeude |

## BauaufgabeIntervention (10 nodes)

| inbound | id | name |
| ---:|---|---|
| 3 | bai_wiederaufbau | Wiederaufbau |
| 4 | bai_translozierung | Translozierung |
| 5 | bai_fit_out | Fit_out |
| 6 | bai_erweiterung | Erweiterung |
| 6 | bai_rueckbau | Rueckbau |
| 7 | bai_aufstockung | Aufstockung |
| 15 | bai_umnutzung | Umnutzung |
| 17 | bai_sanierung | Sanierung |
| 23 | bai_umbau | Umbau |
| 50 | bai_neubau | Neubau |

## Bausystem (9 nodes)

| inbound | id | name |
| ---:|---|---|
| 0 | bsys_iw73 | IW73/6_Plattenbausystem |
| 1 | bsys_secondary_timber_glulamst | glulamST_secondary_timber |
| 2 | bsys_cross_laminated_secondary_timber_clst | CLST_cross_laminated_secondary_timber |
| 3 | bsys_holz_skelettbau | Holz_Skelettbau |
| 4 | bsys_p2_plattenbausystem | P2_Plattenbausystem |
| 6 | bsys_holzrahmenbau | Holzrahmenbau |
| 13 | bsys_plattenbau | Plattenbau |
| 14 | bsys_stahl_skelettbau | Stahl_Skelettbau |
| 21 | bsys_betonfertigteil_system | Betonfertigteil_System |

## Bauweise (6 nodes)

| inbound | id | name |
| ---:|---|---|
| 1 | bauw_ortbetonbauweise | Ortbetonbauweise |
| 22 | bauw_massivbauweise | Massivbauweise |
| 23 | bauw_hybridbauweise | Hybridbauweise |
| 25 | bauw_stahlbauweise | Stahlbauweise |
| 27 | bauw_holzbauweise | Holzbauweise |
| 31 | bauw_fertigteilbauweise | Fertigteilbauweise |

## Tragwerksprinzip (4 nodes)

| inbound | id | name |
| ---:|---|---|
| 1 | tp_fachwerk | Fachwerk |
| 3 | tp_wand_kern_tragwerk | Wand_Kern_Tragwerk |
| 26 | tp_wandtragwerk | Wandtragwerk |
| 42 | tp_skeletttragwerk | Skeletttragwerk |

## Nutzung (9 nodes)

| inbound | id | name |
| ---:|---|---|
| 6 | nut_lager_depot | Lager_Depot |
| 11 | nut_sozialbau | Sozialbau |
| 16 | nut_infrastruktur | Infrastruktur |
| 16 | nut_schule_bildung | Schule_Bildung |
| 20 | nut_mischnutzung | Mischnutzung |
| 33 | nut_kultur | Kultur |
| 33 | nut_wohnen | Wohnen |
| 35 | nut_buero | Buero |
| 36 | nut_gewerbe | Gewerbe |

## Status (11 nodes)

| inbound | id | name |
| ---:|---|---|
| 1 | status_wettbewerb | Wettbewerb |
| 3 | status_verworfen | Verworfen |
| 3 | status_vorgeschlagen | Vorgeschlagen |
| 5 | status_temporaer | Temporaer |
| 8 | status_in_bau | In_Bau |
| 8 | status_prototyp | Prototyp |
| 9 | status_geplant | Geplant |
| 9 | status_rueckgebaut | Rueckgebaut |
| 14 | status_unklar | Unklar |
| 35 | status_realisiert | Realisiert |
| 185 | status_gebaut | Gebaut |

## WiederverwendungsArt (11 nodes)

| inbound | id | name |
| ---:|---|---|
| 6 | wva_weiterbauen_im_bestand | Weiterbauen_im_Bestand |
| 10 | wva_remanufacturing | Remanufacturing |
| 17 | wva_recycling | Recycling |
| 22 | wva_design_for_disassembly | Design_for_Disassembly |
| 23 | wva_adaptives_reuse | Adaptives_ReUse |
| 23 | wva_urban_mining | Urban_Mining |
| 25 | wva_refurbishment | Refurbishment |
| 28 | wva_same_site_reuse | Same_Site_ReUse |
| 37 | wva_bestandserhalt | Bestandserhalt |
| 51 | wva_upcycling | Upcycling |
| 316 | wva_direkte_wiederverwendung | Direkte_Wiederverwendung |

## Funktionswechsel (6 nodes)

| inbound | id | name |
| ---:|---|---|
| 0 | fw_dekorative_funktion | Dekorative_Funktion |
| 4 | fw_unbekannt | Unbekannt |
| 13 | fw_technische_funktion | Technische_Funktion |
| 30 | fw_konstruktive_funktion | Konstruktive_Funktion |
| 39 | fw_neue_funktion | Neue_Funktion |
| 94 | fw_gleiche_funktion | Gleiche_Funktion |

## Land (13 nodes)

| inbound | id | name |
| ---:|---|---|
| 5 | land_japan | Japan |
| 5 | land_norwegen | Norwegen |
| 6 | land_luxemburg | Luxemburg |
| 11 | land_oesterreich | Österreich |
| 15 | land_finnland | Finnland |
| 16 | land_usa | USA |
| 18 | land_daenemark | Dänemark |
| 35 | land_frankreich | Frankreich |
| 38 | land_vereinigtes_koenigreich | Vereinigtes Königreich |
| 57 | land_belgien | Belgien |
| 61 | land_niederlande | Niederlande |
| 88 | land_schweiz | Schweiz |
| 120 | land_deutschland | Deutschland |

## Stadt (62 nodes)

| inbound | id | name |
| ---:|---|---|
| 1 | stadt_aarhus | Aarhus |
| 1 | stadt_berlin_marzahn | Berlin-Marzahn |
| 1 | stadt_brussel_anderlecht | Brüssel / Anderlecht |
| 1 | stadt_cambridge_ma | Cambridge, Massachusetts |
| 1 | stadt_duesseldorf | Düsseldorf |
| 1 | stadt_enschede | Enschede |
| 1 | stadt_frankfurt_oder | Frankfurt (Oder) |
| 1 | stadt_muenster | Münster |
| 1 | stadt_paso_robles_templeton_gap | Paso Robles / Templeton Gap |
| 1 | stadt_ruemlang | Rümlang |
| 1 | stadt_s_hertogenbosch | s-Hertogenbosch |
| 1 | stadt_stains | Stains |
| 1 | stadt_terneuzen | Terneuzen |
| 2 | stadt_arnhem | Arnhem |
| 2 | stadt_brighton | Brighton |
| 2 | stadt_eindhoven | Eindhoven |
| 2 | stadt_heerde | Heerde |
| 2 | stadt_leiden | Leiden |
| 2 | stadt_leinefelde | Leinefelde |
| 2 | stadt_lexington_ma | Lexington, Massachusetts |
| 2 | stadt_liege | Liège / Lüttich |
| 2 | stadt_maassluis | Maassluis |
| 2 | stadt_mehrow | Mehrow, Brandenburg |
| 2 | stadt_muehlhausen_thueringen | Mühlhausen, Thüringen |
| 2 | stadt_oegstgeest | Oegstgeest |
| 2 | stadt_plauen | Plauen |
| 2 | stadt_schildow | Schildow |
| 2 | stadt_volkenroda_koerner | Volkenroda / Koerner |
| 3 | stadt_asse | Asse |
| 3 | stadt_bleijerheide_kerkrade | Bleijerheide / Kerkrade |
| 3 | stadt_boulder_colorado | Boulder, Colorado |
| 3 | stadt_colombelles | Colombelles |
| 3 | stadt_dilbeek | Dilbeek / Itterbeek |
| 3 | stadt_duiven | Duiven |
| 3 | stadt_gentbrugge | Gentbrugge / Ghent |
| 3 | stadt_gladsaxe | Gladsaxe |
| 3 | stadt_groeditz | Gröditz |
| 3 | stadt_helsinki | Helsinki |
| 3 | stadt_hoyerswerda | Hoyerswerda / Broethen |
| 3 | stadt_kloetinge | Kloetinge |
| 3 | stadt_molenbeek_saint_jean | Molenbeek-Saint-Jean / Bruessel |
| 3 | stadt_mouscron | Mouscron |
| 3 | stadt_rotterdam | Rotterdam |
| 3 | stadt_winterthur | Winterthur |
| 4 | stadt_auderghem_brussels | Auderghem / Brüssel |
| 4 | stadt_basel | Basel |
| 4 | stadt_boston | Boston |
| 4 | stadt_hastings | Hastings |
| 4 | stadt_kamikatsu | Kamikatsu, Tokushima Prefecture |
| 4 | stadt_kopenhagen | Kopenhagen |
| 4 | stadt_lo_reninge | Lo-Reninge |
| 4 | stadt_muenchen | München |
| 4 | stadt_oslo | Oslo |
| 4 | stadt_utrecht | Utrecht |
| 5 | stadt_luxembourg_limpertsberg | Luxembourg-Limpertsberg |
| 7 | stadt_hannover | Hannover |
| 7 | stadt_tampere | Tampere |
| 9 | stadt_bruessel | Brüssel |
| 9 | stadt_paris | Paris |
| 13 | stadt_zuerich | Zürich |
| 16 | stadt_berlin | Berlin |
| 24 | stadt_london | London |

## Norm (16 nodes)

| inbound | id | name |
| ---:|---|---|
| 0 | norm_din_18940 | DIN_18940 |
| 0 | norm_din_en_15804 | DIN_EN_15804 |
| 0 | norm_din_en_15978 | DIN_EN_15978 |
| 0 | norm_iso_14040 | ISO_14040 |
| 0 | norm_iso_14044 | ISO_14044 |
| 1 | norm_historic_sections_book | Historic Sections Book |
| 1 | norm_iso_20887 | ISO_20887 |
| 1 | norm_rt_2012 | RT 2012 |
| 2 | norm_en_1090 | EN_1090 |
| 2 | norm_en_1168 | EN 1168 Precast concrete products - Hollow core slabs |
| 2 | norm_ns_3682 | NS 3682 Reuse of hollow-core slabs / Norwegian reuse standard |
| 2 | norm_sci_p440 | SCI P440 Reuse of Structural Steel |
| 3 | norm_crow_cur_4_2023 | CROW-CUR Guideline 4:2023 Reuse of hollow core slabs |
| 4 | norm_sia_schweiz | SIA / Swiss building standards context |
| 5 | norm_sci_p427 | SCI P427 protocol |
| 5 | norm_tek_norway | Norwegian building regulation TEK / documentation context |

## PruefungNachweis (11 nodes)

| inbound | id | name |
| ---:|---|---|
| 0 | pr_abbrandbemessung | Abbrandbemessung |
| 0 | pr_eignungspruefung_baulehm | Eignungspruefung_Baulehm |
| 3 | pr_brandschutznachweis | Brandschutznachweis |
| 4 | pr_schadstoffscreening | Schadstoffscreening |
| 6 | pr_zugversuch | Zugversuch |
| 7 | pr_schweissbarkeitspruefung | Schweissbarkeitspruefung |
| 12 | pr_geometrische_vermessung | Geometrische_Vermessung |
| 33 | pr_materialpruefung | Materialpruefung |
| 46 | pr_statische_nachweisfuehrung | Statische_Nachweisfuehrung |
| 59 | pr_sichtpruefung | Sichtpruefung |
| 150 | pr_zustandsbewertung | Zustandsbewertung |

## Leistungsanforderung (12 nodes)

| inbound | id | name |
| ---:|---|---|
| 0 | la_f90 | F90 |
| 0 | la_r90 | R90 |
| 0 | la_rei90 | REI90 |
| 3 | la_feuerwiderstand | Feuerwiderstand |
| 7 | la_schadstofffreiheit | Schadstofffreiheit |
| 9 | la_rueckbaubarkeit | Rueckbaubarkeit |
| 28 | la_schallschutz | Schallschutz |
| 44 | la_waermeschutz | Waermeschutz |
| 60 | la_feuchteschutz | Feuchteschutz |
| 94 | la_brandschutz | Brandschutz |
| 119 | la_tragfaehigkeit | Tragfaehigkeit |
| 142 | la_dauerhaftigkeit | Dauerhaftigkeit |

## Methode (13 nodes)

| inbound | id | name |
| ---:|---|---|
| 0 | meth_abrissmonitoring | Abrissmonitoring |
| 1 | meth_wiederverwendungskriterien | Wiederverwendungskriterien |
| 3 | meth_zirkulaere_ausschreibung | Zirkulaere_Ausschreibung |
| 16 | meth_pre_deconstruction_audit | Pre_Deconstruction_Audit |
| 19 | meth_reuse_ausschreibung | ReUse_Ausschreibung |
| 22 | meth_urban_mining | Urban_Mining |
| 31 | meth_reversibilitaet | Reversibilitaet |
| 35 | meth_design_for_disassembly | Design_for_Disassembly |
| 48 | meth_materialinventur | Materialinventur |
| 53 | meth_bauteilkatalogisierung | Bauteilkatalogisierung |
| 60 | meth_building_material_scouting | Building_Material_Scouting |
| 102 | meth_reuse_assessment | ReUse_Assessment |
| 132 | meth_form_follows_availability | Form_Follows_Availability |

## Rueckbauverfahren (5 nodes)

| inbound | id | name |
| ---:|---|---|
| 4 | rv_betonfraesen | Betonfraesen |
| 13 | rv_zerstoerungsarme_bergung | Zerstoerungsarme_Bergung |
| 72 | rv_demontage | Demontage |
| 84 | rv_ausbau_von_bauteilen | Ausbau_von_Bauteilen |
| 87 | rv_selektiver_rueckbau | Selektiver_Rueckbau |

## Aufbereitungsverfahren (11 nodes)

| inbound | id | name |
| ---:|---|---|
| 0 | av_drahtglasschneiden | Drahtglasschneiden |
| 4 | av_entmoertelung_von_fliesen | Entmoertelung_von_Fliesen |
| 4 | av_verstaerkung | Verstaerkung |
| 5 | av_leuchten_refurbishment | Leuchten_Refurbishment |
| 8 | av_remanufacturing | Remanufacturing |
| 23 | av_holzaufbereitung | Holzaufbereitung |
| 35 | av_reparatur | Reparatur |
| 47 | av_qualitaetssicherung | Qualitaetssicherung |
| 74 | av_rekonditionierung | Rekonditionierung |
| 78 | av_zuschnitt | Zuschnitt |
| 85 | av_reinigung | Reinigung |

## Prozessphase (10 nodes)

| inbound | id | name |
| ---:|---|---|
| 6 | phase_betrieb | Betrieb |
| 23 | phase_dokumentation | Dokumentation |
| 28 | phase_lagerung | Lagerung |
| 42 | phase_pruefung | Pruefung |
| 45 | phase_transport | Transport |
| 52 | phase_planung | Planung |
| 88 | phase_identifikation | Identifikation |
| 90 | phase_rueckbau | Rueckbau |
| 111 | phase_aufbereitung | Aufbereitung |
| 227 | phase_wiedereinbau | Wiedereinbau |

## Logistik (10 nodes)

| inbound | id | name |
| ---:|---|---|
| 1 | log_lagerflaeche | Lagerflaeche |
| 7 | log_just_in_time | Just_in_Time |
| 14 | log_transportdistanz | Transportdistanz |
| 17 | log_bauteiltracking | Bauteiltracking |
| 17 | log_zwischenlagerung | Zwischenlagerung |
| 23 | log_materialverfuegbarkeit | Materialverfuegbarkeit |
| 39 | log_lokale_wiederverwendung | Lokale_Wiederverwendung |
| 64 | log_lagerung | Lagerung |
| 91 | log_transport | Transport |
| 129 | log_materialmatching | Materialmatching |

## Beschaffungsweg (10 nodes)

| inbound | id | name |
| ---:|---|---|
| 0 | bweg_lager | Lager |
| 4 | bweg_leihmodell | Leihmodell |
| 8 | bweg_spende | Spende |
| 14 | bweg_ausschreibung | Ausschreibung |
| 15 | bweg_digitale_plattform | Digitale_Plattform |
| 17 | bweg_eigenbestand | Eigenbestand |
| 30 | bweg_informelles_netzwerk | Informelles_Netzwerk |
| 39 | bweg_direktvermittlung | Direktvermittlung |
| 44 | bweg_bauteilboerse | Bauteilboerse |
| 62 | bweg_rueckbauprojekt | Rueckbauprojekt |

## Ressourcenquelle (16 nodes)

| inbound | id | name |
| ---:|---|---|
| 1 | rq_demolition_waste_stream | Demolition_Waste_Stream |
| 2 | rq_construction_waste_stream | Construction_Waste_Stream |
| 2 | rq_surplus_stock | Surplus_Stock |
| 3 | rq_reclaimed_stock | Reclaimed_Stock |
| 3 | rq_supplier_stock | Supplier_Stock |
| 4 | rq_borrowed_material_pool | Borrowed_Material_Pool |
| 5 | rq_materialstockpile | Materialstockpile |
| 5 | rq_unknown_documented_source | Unknown_Documented_Source |
| 9 | rq_donor_infrastruktur | Donor_Infrastruktur |
| 14 | rq_unbekannt | Unbekannt |
| 26 | rq_haendler | Haendler |
| 38 | rq_bauteilboerse | Bauteilboerse |
| 40 | rq_produktionsueberschuss | Produktionsueberschuss |
| 50 | rq_baustelle | Baustelle |
| 51 | rq_lager | Lager |
| 150 | rq_donorgebaeude | Donorgebaeude |

## Verbindungstechnik (8 nodes)

| inbound | id | name |
| ---:|---|---|
| 0 | vt_verleimung | Verleimung |
| 1 | vt_mauerwerk_ausgleich | Mauerwerk_Ausgleichsschicht |
| 1 | vt_steckverbindung | Steckverbindung |
| 4 | vt_klemmverbindung | Klemmverbindung |
| 7 | vt_vermoertelung | Vermoertelung |
| 10 | vt_verschweissung | Verschweissung |
| 39 | vt_reversible_fuegung | Reversible_Fuegung |
| 40 | vt_verschraubung | Verschraubung |

## RechtlicheBedingung (9 nodes)

| inbound | id | name |
| ---:|---|---|
| 0 | rb_eu_taxonomie | EU_Taxonomie |
| 0 | rb_gewaehrleistung | Gewaehrleistung |
| 0 | rb_produkthaftung | Produkthaftung |
| 1 | rb_boulder_deconstruction_ordinance_8366 | Boulder Deconstruction Ordinance 8366 / 2020 |
| 1 | rb_grade_ii_listing | Grade_II_Listing |
| 1 | rb_vergaberecht | Vergaberecht |
| 3 | rb_bauordnungsrecht | Bauordnungsrecht |
| 3 | rb_ce_ukca_marking_reused_steel | CE/UKCA marking for reused steel |
| 3 | rb_zulassung_im_einzelfall | Zulassung_im_Einzelfall |

## Schadstoff (5 nodes)

| inbound | id | name |
| ---:|---|---|
| 0 | s_bleifarbe | Bleifarbe |
| 0 | s_holzschutzmittel | Holzschutzmittel |
| 0 | s_pak | PAK |
| 0 | s_pcb | PCB |
| 1 | s_asbest | Asbest |

## Wirtschaft (6 nodes)

| inbound | id | name |
| ---:|---|---|
| 0 | wi_lebenszykluskosten | Lebenszykluskosten |
| 0 | wi_preisbildung | Preisbildung |
| 1 | wi_finanzierung | Finanzierung |
| 1 | wi_geschaeftsmodell | Geschaeftsmodell |
| 2 | wi_restwert | Restwert |
| 7 | wi_kostenvergleich | Kostenvergleich |

## ZertifizierungBewertungssystem (7 nodes)

| inbound | id | name |
| ---:|---|---|
| 0 | zbs_leed | LEED |
| 1 | zbs_dgnb | DGNB |
| 1 | zbs_nordic_swan_ecolabel | Nordic Swan Ecolabel / Svanemærket |
| 1 | zbs_paris_proof | Paris_Proof |
| 2 | zbs_nabers | NABERS |
| 2 | zbs_well | WELL |
| 3 | zbs_breeam | BREEAM |

## Programm (15 nodes)

| inbound | id | name |
| ---:|---|---|
| 0 | prog_bbsm | BBSM |
| 0 | prog_interreg_nwe | Interreg_North_West_Europe |
| 0 | prog_kommunales_programm | Kommunales_Programm |
| 0 | prog_preuse | PREUSE |
| 0 | prog_reallabor | Reallabor |
| 0 | prog_reallabor_be_ware | Reallabor_Be_Ware |
| 0 | prog_zukunftbau | Zukunftbau |
| 1 | prog_fcrbe | FCRBE |
| 1 | prog_recreate_local | ReCreate Finnish cluster mini-pilot |
| 2 | prog_expo_2000 | EXPO 2000 Hannover |
| 2 | prog_foerderprogramm | Foerderprogramm |
| 2 | prog_wettbewerb | Wettbewerb |
| 3 | prog_recreate | ReCreate |
| 6 | prog_forschungsprojekt | Forschungsprojekt |
| 9 | prog_pilotprojekt | Pilotprojekt |

## Tool (6 nodes)

| inbound | id | name |
| ---:|---|---|
| 1 | tool_oogstkaart_harvest_map | Oogstkaart / Harvest Map logic |
| 2 | tool_bauteilkatalog | Bauteilkatalog / Bauteilpass |
| 2 | tool_bim_bauteilkatalog | BIM / digitaler Bauteilkatalog |
| 2 | tool_hts_stockmatcher | HTS Reused Steel Stockmatcher |
| 2 | tool_material_passports_maconda | Material passports / Maconda data workflow |
| 5 | tool_qflow | Qflow delivery and waste ticket tracking |

## Software (7 nodes)

| inbound | id | name |
| ---:|---|---|
| 1 | software_inies | INIES |
| 1 | software_risa_3d | RISA-3D |
| 2 | software_bim | Building Information Modeling / BIM |
| 2 | software_recrete_finite_element_model | Finite-Elemente-Modell / FE-Modell |
| 5 | software_qflow | Qflow |
| 9 | software_concular | Concular |
| 9 | software_restado | Restado |

