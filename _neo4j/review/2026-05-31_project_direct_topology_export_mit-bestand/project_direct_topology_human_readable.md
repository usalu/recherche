# Project Reuse Workflow - Clean Topology

Created UTC: `2026-05-31T13:17:03.427170+00:00`
Database: `mit-bestand`

This is a cleaned, human-readable project topology focused on reuse workflow.

This view keeps the project reuse workflow only and omits evidence, metric, classification, and review-helper material.

Kept in this view: actors, locations, built context, component groups, reuse strategy, process/logistics/procurement, checks, risks, constraints, tools, programmes, and rules.

Projects: `101`
Reuse-workflow edges: `3911`

## Edge Groups

- Actors and Delivery Chain: `670`
- Place and Built Context: `908`
- Components and Construction System: `379`
- Reuse Strategy and Process: `922`
- Risk, Checks, and Constraints: `808`
- Tools, Programmes, and Frameworks: `224`

## Relation Types Kept

- `BETEILIGT_AN`: 508
- `HAT_BAUTEILGRUPPE`: 363
- `REQUIRES_VERIFICATION_FOR`: 347
- `HAT_HUERDE`: 297
- `HAT_METHODE`: 197
- `HAS_BAUWERK`: 184
- `HAT_WIEDERVERWENDUNGSART`: 182
- `HAT_MATCHINGQUALITAET`: 179
- `NUTZT_BAUWERK`: 168
- `STUB_PROJECT_LINK`: 162
- `HAT_INTERVENTION`: 138
- `HAT_NUTZUNG`: 137
- `HAT_PROZESSPHASE`: 112
- `RELEVANT_FOR`: 103
- `HAT_LOGISTIK`: 98
- `HAT_STATUS`: 93
- `LIEGT_IN_STADT`: 90
- `LIEGT_IN_LAND`: 87
- `HAT_RESSOURCENQUELLE`: 71
- `HAT_PRUEFUNG`: 63
- `HAT_BESCHAFFUNGSWEG`: 61
- `HAT_WIRTSCHAFT`: 44
- `HAT_HUERDEKATEGORIE`: 39
- `TEIL_VON_PROGRAMM`: 31
- `REFERENZIERT_NORM`: 26
- `HAT_DEFEKT_BEFUND`: 25
- `HAT_AUFBEREITUNG`: 22
- `NUTZT_SOFTWARE`: 17
- `HAT_ZERTIFIZIERUNG`: 12
- `HAT_BAUOBJEKTKLASSE`: 11
- `HAT_BAUWEISE`: 9
- `BERECHNET_NACH_MODUL`: 8
- `HAT_RECHTLICHE_BEDINGUNG`: 7
- `HAT_WIRTSCHAFTSASPEKT`: 5
- `ERHALT_FOERDERUNG_DURCH`: 4
- `HAS_RISK_POLLUTANT`: 4
- `HAT_BAUSYSTEM`: 3
- `HAT_TRAGWERKSPRINZIP`: 3
- `HAT_VERBINDUNGSTECHNIK`: 1

## Projects

### 1. 55 Great Suffolk Street, London

Project ID: `p_55_great_suffolk_street_london`
Reuse-workflow edges: `35`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `AKT II` (`akt_ii`) -> `BETEILIGT_AN` -> Project
- Akteur `CBRE` (`cbre`) -> `BETEILIGT_AN` -> Project
- Akteur `Cantillon` (`cantillon`) -> `BETEILIGT_AN` -> Project
- Akteur `Cleveland Steel & Tubes` (`cleveland_steel_tubes`) -> `BETEILIGT_AN` -> Project
- Akteur `Fabrix` (`fabrix`) -> `BETEILIGT_AN` -> Project
- Akteur `Gardiner & Theobald` (`gardiner_and_theobald`) -> `BETEILIGT_AN` -> Project
- Akteur `Hawkins\Brown` (`hawkins_brown`) -> `BETEILIGT_AN` -> Project
- Akteur `Opera` (`opera`) -> `BETEILIGT_AN` -> Project
- Akteur `Symmetrys` (`symmetrys`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `1 Broadgate, London` (`bw_1_broadgate_london`)
- Project -> `HAS_BAUWERK` -> Bauwerk `55 Great Suffolk Street warehouse` (`bw_55_great_suffolk_street_warehouse`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Erweiterung` (`bai_erweiterung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Sanierung` (`bai_sanierung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Unklar` (`status_unklar`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Vereinigtes Königreich` (`land_vereinigtes_koenigreich`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `London` (`stadt_london`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `55 Great Suffolk Street warehouse` (`bw_55_great_suffolk_street_warehouse`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Reused steel profiles for external core` (`bg_reuse_stahl_mehrere_55gss_external_core`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Exakte Spezifikations-Übereinstimmung` (`mq_spec_exact`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch geplante Beschaffung` (`mq_temporal_planned`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Urban_Mining` (`meth_urban_mining`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**REFERENZIERT_NORM**
- Project -> `REFERENZIERT_NORM` -> Norm `DIN_EN_15804` (`norm_din_en_15804`)
- Project -> `REFERENZIERT_NORM` -> Norm `DIN_EN_15978` (`norm_din_en_15978`)
- Project -> `REFERENZIERT_NORM` -> Norm `ISO_14040` (`norm_iso_14040`)
- Project -> `REFERENZIERT_NORM` -> Norm `ISO_14044` (`norm_iso_14044`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**BERECHNET_NACH_MODUL**
- Project -> `BERECHNET_NACH_MODUL` -> LCAModule `A1-A3 Produkt` (`lz_a1_a3`)
- Project -> `BERECHNET_NACH_MODUL` -> LCAModule `A4-A5 Errichtung` (`lz_a4_a5`)
**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx höher, Subvention/Förderung deckt Mehrkosten` (`wi_capex_hoeher_subvention`)
**RELEVANT_FOR**
- ReuseRule `Vereinigtes Königreich × Stahl reuse rule` (`rr_gb_stahl`) -> `RELEVANT_FOR` -> Project

### 2. Association house, Gröditz

Project ID: `p_association_house_groeditz`
Reuse-workflow edges: `14`

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `School type Dresden donor building` (`bw_school_type_dresden_donor`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Sport-/Vereinshaus Gröditz` (`bw_association_house_groeditz`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Sozialbau` (`nut_sozialbau`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Deutschland` (`land_deutschland`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Gröditz` (`stadt_groeditz`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Sport-/Vereinshaus Gröditz` (`bw_association_house_groeditz`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Reused Dresden-type precast concrete components` (`bg_reuse_stahlbeton_mehrere_groeditz_dresden_type_precast_components`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Reused WBS70 precast panels` (`bg_reuse_stahlbeton_mehrere_groeditz_wbs70_precast_panels`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Bauteilkatalogisierung` (`meth_bauteilkatalogisierung`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)

### 3. Association house, Plauen

Project ID: `p_association_house_plauen`
Reuse-workflow edges: `14`

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `IW73/6 mass-housing donor building` (`bw_iw73_6_mass_housing_donor`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Sport-/Vereinshaus Plauen` (`bw_association_house_plauen`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Sozialbau` (`nut_sozialbau`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Deutschland` (`land_deutschland`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Plauen` (`stadt_plauen`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Sport-/Vereinshaus Plauen` (`bw_association_house_plauen`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Reused IW73/6 precast concrete components` (`bg_reuse_stahlbeton_mehrere_plauen_iw73_6_precast_components`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Bauteilkatalogisierung` (`meth_bauteilkatalogisierung`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)

### 4. AWM Münster – zirkulärer Büroausbau 3. OG

Project ID: `p_awm_muenster_circular_office`
Reuse-workflow edges: `36`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Abfallwirtschaftsbetriebe Münster` (`abfallwirtschaftsbetriebe_muenster`) -> `BETEILIGT_AN` -> Project
- Akteur `Concular` (`concular`) -> `BETEILIGT_AN` -> Project
- Akteur `Petra Jablonická` (`petra_jablonicka`) -> `BETEILIGT_AN` -> Project
- Akteur `Sven Urselmann` (`sven_urselmann`) -> `BETEILIGT_AN` -> Project
- Akteur `Urselmann Interior` (`urselmann_interior`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Petra Jablonická` (`petra_jablonicka`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Sven Urselmann` (`sven_urselmann`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `AWM Münster administrative building` (`bw_awm_muenster_admin_building`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Behrensbau Düsseldorf donor source` (`bw_behrensbau_duesseldorf_donor`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Public building and retail material sources for AWM interior` (`bw_public_building_material_sources_awm`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Fit_out` (`bai_fit_out`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Deutschland` (`land_deutschland`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Münster` (`stadt_muenster`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `AWM Münster administrative building` (`bw_awm_muenster_admin_building`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Fixed wall cladding from old chair parts` (`bg_reuse_holz_wand_awm_cladding_old_chairs`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Reused WC partitions` (`bg_reuse_kunststoff_wand_awm_wc_partitions`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Reused cable trays as shelves and lighting carriers` (`bg_reuse_stahl_mehrere_awm_cable_trays_shelves_lights`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Reused glass partitions and doors` (`bg_reuse_glas_mehrere_awm_partitions_doors`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Reused wood for fixed built-ins` (`bg_reuse_holz_ausbau_awm_fixed_builtins`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Urban_Mining` (`meth_urban_mining`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Upcycling` (`wva_upcycling`)

#### Risk, Checks, and Constraints

**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Deutschland × Holz reuse rule` (`rr_de_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Deutschland × Stahl reuse rule` (`rr_de_stahl`) -> `RELEVANT_FOR` -> Project

### 5. BedZED / Beddington Zero Energy Development

Project ID: `p_bedzed_london_hackbridge`
Reuse-workflow edges: `43`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Arup` (`arup`) -> `BETEILIGT_AN` -> Project
- Akteur `Bill Dunster / ZEDfactory` (`zedfactory_bill_dunster`) -> `BETEILIGT_AN` -> Project
- Akteur `BioRegional` (`bioregional`) -> `BETEILIGT_AN` -> Project
- Akteur `Ellis & Moore Consulting Engineers` (`ellis_and_moore`) -> `BETEILIGT_AN` -> Project
- Akteur `Gardiner & Theobald` (`gardiner_and_theobald`) -> `BETEILIGT_AN` -> Project
- Akteur `Peabody Trust` (`peabody_trust`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `BedZED mixed-use quarter` (`bw_bedzed_quarter_hackbridge`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Brighton Railway Station donor source` (`bw_brighton_railway_station_donor`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Local demolition and reclaim sources around BedZED` (`bw_local_demolition_sources_bedzed`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Mischnutzung` (`nut_mischnutzung`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Vereinigtes Königreich` (`land_vereinigtes_koenigreich`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `London` (`stadt_london`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `BedZED mixed-use quarter` (`bw_bedzed_quarter_hackbridge`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Reused fixed secondary components` (`bg_reuse_mehrere_mehrere_bedzed_fixed_secondary_components`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Reused softwood wall studs` (`bg_reuse_holz_wand_bedzed_studs`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Reused structural steel frame for workspaces` (`bg_reuse_stahl_mehrere_bedzed_structural`)

#### Reuse Strategy and Process

**HAT_AUFBEREITUNG**
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `Entrosten / Korrosionsbehandlung` (`av_entrosten_korrosionsbehandlung`)
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `av_oberflaechenbehandlung_metall`
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Regional geografisches Matching (50–500 km)` (`mq_geographic_regional`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**HAS_RISK_POLLUTANT**
- Project -> `HAS_RISK_POLLUTANT` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Keine relevanten Defekte (positive Befund)` (`def_keine_befunde`)
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Korrosion` (`def_korrosion`)
**HAT_PRUEFUNG**
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_restquerschnitt`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_rostgrad`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_sichtpruefung`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_ultraschall_dickenmessung`
**REFERENZIERT_NORM**
- Project -> `REFERENZIERT_NORM` -> Norm `Historic Sections Book` (`norm_historic_sections_book`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx vergleichbar mit Neubau` (`wi_capex_neutral`)
**RELEVANT_FOR**
- ReuseRule `Vereinigtes Königreich × Holz reuse rule` (`rr_gb_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Vereinigtes Königreich × Stahl reuse rule` (`rr_gb_stahl`) -> `RELEVANT_FOR` -> Project

### 6. Berlin-Schildow Pilot House / Berlin-Schildow 2nd pilot house

Project ID: `p_berlin_schildow_pilot_house`
Reuse-workflow edges: `28`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Architekturbüro Conclus` (`architekturbuero_conclus`) -> `BETEILIGT_AN` -> Project
- Akteur `Claus Asam` (`claus_asam`) -> `BETEILIGT_AN` -> Project
- Akteur `Detlev Lange / Familie Lange` (`familie_lange`) -> `BETEILIGT_AN` -> Project
- Akteur `Hervé / Joel Biele` (`herve_joel_biele`) -> `BETEILIGT_AN` -> Project
- Akteur `IEMB / TU Berlin` (`iemb_tu_berlin`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Berliner/Marzahner WBS70-Plattenbau` (`bw_berlin_marzahn_wbs70_plattenbau`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Schildow Pilotwohnhaus` (`bw_schildow_pilot_house`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Prototyp` (`status_prototyp`)
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Deutschland` (`land_deutschland`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Schildow` (`stadt_schildow`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Berliner/Marzahner WBS70-Plattenbau` (`bw_berlin_marzahn_wbs70_plattenbau`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Schildow Pilotwohnhaus` (`bw_schildow_pilot_house`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Zugeschnittene WBS70-Stahlbetonfertigteile` (`bg_reuse_stahlbeton_mehrere_schildow_zugeschnittene_wbs70_betonfertigteile`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Just_in_Time` (`log_just_in_time`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transportdistanz` (`log_transportdistanz`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Regional geografisches Matching (50–500 km)` (`mq_geographic_regional`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Korrosion` (`def_korrosion`)
**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)

#### Tools, Programmes, and Frameworks

**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Pilotprojekt` (`prog_pilotprojekt`)

### 7. Bestandverplanzung Pavilion, München

Project ID: `p_bestandverplanzung_pavilion_muenchen`
Reuse-workflow edges: `18`

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Bestandverplanzung Pavilion` (`bw_bestandverplanzung_pavilion`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Bungalows des Olympischen Dorfes München` (`bw_olympisches_dorf_bungalows_muenchen`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Translozierung` (`bai_translozierung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Wiederaufbau` (`bai_wiederaufbau`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Prototyp` (`status_prototyp`)
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Deutschland` (`land_deutschland`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `München` (`stadt_muenchen`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Bestandverplanzung Pavilion` (`bw_bestandverplanzung_pavilion`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Bungalows des Olympischen Dorfes München` (`bw_olympisches_dorf_bungalows_muenchen`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Betonfertigteil-Paneele aus Olympiadorf-Bungalows` (`bg_reuse_beton_mehrere_bestandverplanzung_betonfertigteil_paneele`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Urban_Mining` (`meth_urban_mining`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Deutschland × Beton reuse rule` (`rr_de_beton`) -> `RELEVANT_FOR` -> Project

### 8. Big Dig Building, Boston/Cambridge

Project ID: `p_big_dig_building_boston`
Reuse-workflow edges: `33`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Jinhee Park` (`jinhee_park`) -> `BETEILIGT_AN` -> Project
- Akteur `John Hong` (`john_hong`) -> `BETEILIGT_AN` -> Project
- Akteur `Paul Pedini` (`paul_pedini`) -> `BETEILIGT_AN` -> Project
- Akteur `Single Speed Design` (`single_speed_design`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Big Dig Building` (`bw_big_dig_building`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Boston Big Dig / Central Artery Tunnel Project infrastructure` (`bw_boston_big_dig_infrastructure`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Prototyp` (`status_prototyp`)
- Project -> `HAT_STATUS` -> Status `Verworfen` (`status_verworfen`)
- Project -> `HAT_STATUS` -> Status `Vorgeschlagen` (`status_vorgeschlagen`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `USA` (`land_usa`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Boston` (`stadt_boston`)
- Project -> `LIEGT_IN_STADT` -> Stadt `Cambridge, Massachusetts` (`stadt_cambridge_ma`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Big Dig Building` (`bw_big_dig_building`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Boston Big Dig / Central Artery Tunnel Project infrastructure` (`bw_boston_big_dig_infrastructure`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Geplante Big-Dig-Infrastrukturbauteile` (`bg_planned_mehrere_mehrere_big_dig_building_geplante_infrastrukturbauteile`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Urban_Mining` (`meth_urban_mining`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donor_Infrastruktur` (`rq_donor_infrastruktur`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Urban_Mining` (`wva_urban_mining`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Haftung` (`h_haftung`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Unkonventionelles_Material` (`h_unkonventionelles_material`)
- Project -> `HAT_HUERDE` -> Huerde `Verfuegbarkeitsproblem` (`h_verfuegbarkeitsproblem`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx höher, Subvention/Förderung deckt Mehrkosten` (`wi_capex_hoeher_subvention`)
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Wettbewerb` (`prog_wettbewerb`)

### 9. Big Dig House, Lexington, Massachusetts

Project ID: `p_big_dig_house_lexington_massachusetts`
Reuse-workflow edges: `27`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Jinhee Park` (`jinhee_park`) -> `BETEILIGT_AN` -> Project
- Akteur `John Hong` (`john_hong`) -> `BETEILIGT_AN` -> Project
- Akteur `Paul Pedini` (`paul_pedini`) -> `BETEILIGT_AN` -> Project
- Akteur `Single Speed Design` (`single_speed_design`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Big Dig House` (`bw_big_dig_house`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Boston Big Dig / dismantled I-93 infrastructure` (`bw_boston_big_dig_i_93_infrastructure`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `USA` (`land_usa`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Lexington, Massachusetts` (`stadt_lexington_ma`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Big Dig House` (`bw_big_dig_house`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Boston Big Dig / dismantled I-93 infrastructure` (`bw_boston_big_dig_i_93_infrastructure`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Inverset-Stahlbetonpaneele` (`bg_reuse_stahlbeton_mehrere_big_dig_house_inverset_panels`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Ramp-, Pier- und Roadway-Komponenten` (`bg_reuse_mehrere_mehrere_big_dig_house_ramp_pier_roadway_components`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Stahlträger und Stahlstützen` (`bg_reuse_stahl_mehrere_big_dig_house`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Transport` (`log_transport`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `International / interkontinental` (`mq_geographic_intl`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donor_Infrastruktur` (`rq_donor_infrastruktur`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Urban_Mining` (`wva_urban_mining`)

#### Risk, Checks, and Constraints

**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

### 10. BioPartner 5, Leiden / Oegstgeest

Project ID: `p_biopartner_5_leiden_oegstgeest`
Reuse-workflow edges: `51`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `BioPartner Center Leiden` (`biopartner_center_leiden`) -> `BETEILIGT_AN` -> Project
- Akteur `De Vries en Verburg` (`de_vries_en_verburg`) -> `BETEILIGT_AN` -> Project
- Akteur `Deerns` (`deerns`) -> `BETEILIGT_AN` -> Project
- Akteur `IMd Raadgevende Ingenieurs` (`imd_raadgevende_ingenieurs`) -> `BETEILIGT_AN` -> Project
- Akteur `Leiden University / Gorlaeus donor source` (`leiden_university`) -> `BETEILIGT_AN` -> Project
- Akteur `Popma ter Steege Architecten / PTSA` (`popma_ter_steege_architecten`) -> `BETEILIGT_AN` -> Project
- Akteur `STONE22` (`stone22`) -> `BETEILIGT_AN` -> Project
- Akteur `Vic Obdam Staalbouw` (`vic_obdam_staalbouw`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `BioPartner 5` (`bw_biopartner_5`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Ehemaliges Gorlaeus-Hochhaus / Gorlaeus Laboratory` (`bw_gorlaeus_hochhaus`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Ehemaliges Gorlaeus-Hochhaus / Leiden University donor source` (`bw_biopartner_gorlaeus_hochhaus`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Mischnutzung` (`nut_mischnutzung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Niederlande` (`land_niederlande`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Leiden` (`stadt_leiden`)
- Project -> `LIEGT_IN_STADT` -> Stadt `Oegstgeest` (`stadt_oegstgeest`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `BioPartner 5` (`bw_biopartner_5`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Ehemaliges Gorlaeus-Hochhaus / Gorlaeus Laboratory` (`bw_gorlaeus_hochhaus`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Abbruchschutt / Mauerwerkspuin in grüner Fassade` (`bg_reuse_ziegel_fassade_biopartner_5_abbruchschutt_gruene`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Innenwände und Trennwände` (`bg_reuse_holz_wand_biopartner_5_innenwaende_trennwaende`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Pflaster-, Naturstein- und Bodenmaterialien` (`bg_reuse_naturstein_boden_biopartner_5_pflaster_bodenmaterial`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Sanitärobjekte` (`bg_reuse_keramik_technik_biopartner_5_sanitaerobjekte`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Stahlträger, Stützen und Rahmen` (`bg_reuse_stahl_mehrere_biopartner_5_stuetzen_rahmen`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Lokale_Wiederverwendung` (`log_lokale_wiederverwendung`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Design_for_Disassembly` (`meth_design_for_disassembly`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Design_for_Disassembly` (`wva_design_for_disassembly`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Urban_Mining` (`wva_urban_mining`)

#### Risk, Checks, and Constraints

**HAS_RISK_POLLUTANT**
- Project -> `HAS_RISK_POLLUTANT` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Korrosion` (`def_korrosion`)
**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Gewaehrleistung` (`h_gewaehrleistung`)
- Project -> `HAT_HUERDE` -> Huerde `Kompatibilitaetsproblem` (`h_kompatibilitaetsproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Terminunsicherheit` (`h_terminunsicherheit`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_ZERTIFIZIERUNG**
- Project -> `HAT_ZERTIFIZIERUNG` -> Zertifizierungssystem `Paris_Proof` (`zbs_paris_proof`)
**RELEVANT_FOR**
- ReuseRule `Niederlande × Holz reuse rule` (`rr_nl_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Niederlande × Stahl reuse rule` (`rr_nl_stahl`) -> `RELEVANT_FOR` -> Project

### 11. BlueCity Offices Rotterdam

Project ID: `p_bluecity_offices_rotterdam`
Reuse-workflow edges: `45`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Bik Bouw` (`bik_bouw`) -> `BETEILIGT_AN` -> Project
- Akteur `BlueCity / Blue City 010 BV` (`bluecity`) -> `BETEILIGT_AN` -> Project
- Akteur `COUP` (`coup`) -> `BETEILIGT_AN` -> Project
- Akteur `Floris Schiferli` (`floris_schiferli`) -> `BETEILIGT_AN` -> Project
- Akteur `Superuse Studios` (`Superuse_Studios`) -> `BETEILIGT_AN` -> Project
- Akteur `Workspot` (`workspot`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Jan Jongert` (`jan_jongert`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Jeroen Bergsma` (`jeroen_bergsma`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Superuse Studios` (`Superuse_Studios`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `BlueCity Offices / erster Büroflügel` (`bw_bluecity_offices`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Tropicana Rotterdam / BlueCity Bestand` (`bw_bluecity_tropicana_rotterdam`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Fit_out` (`bai_fit_out`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umnutzung` (`bai_umnutzung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Niederlande` (`land_niederlande`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Rotterdam` (`stadt_rotterdam`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `BlueCity Offices / erster Büroflügel` (`bw_bluecity_offices`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Ehemaliges Tropicana / Club Tropicana Rotterdam` (`bw_tropicana_rotterdam`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Betonblöcke als Trennwände` (`bg_reuse_beton_wand_bluecity_betonbloecke_trennwaende`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Mögliche wiederverwendete Balustraden` (`bg_reuse_stahl_gelaender_bluecity_oelplattform`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Red-Cedar-Fensterrahmen als Trennwände / innere Fassade` (`bg_reuse_mehrere_mehrere_bluecity_red_cedar_fensterrahmen_trennwaende`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendeter Stahl im Büroausbau` (`bg_reuse_stahl_ausbau_bluecity`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Informelles_Netzwerk` (`bweg_informelles_netzwerk`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Adaptives_ReUse` (`wva_adaptives_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Brandschutzkonflikt` (`h_brandschutzkonflikt`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Kompatibilitaetsproblem` (`h_kompatibilitaetsproblem`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**NUTZT_SOFTWARE**
- Project -> `NUTZT_SOFTWARE` -> Software:Tool `Oogstkaart / Harvest Map logic` (`tool_oogstkaart_harvest_map`)
**RELEVANT_FOR**
- ReuseRule `Niederlande × Beton reuse rule` (`rr_nl_beton`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Niederlande × Holz reuse rule` (`rr_nl_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Niederlande × Stahl reuse rule` (`rr_nl_stahl`) -> `RELEVANT_FOR` -> Project

### 12. Boulder Fire Station 3 / City of Boulder Fire Rescue Station #3

Project ID: `p_boulder_fire_station_3`
Reuse-workflow edges: `42`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Boulder Community Health / Boulder Community Hospital` (`boulder_community_health`) -> `BETEILIGT_AN` -> Project
- Akteur `City of Boulder` (`city_of_boulder`) -> `BETEILIGT_AN` -> Project
- Akteur `Davis Partnership Architects` (`davis_partnership_architects`) -> `BETEILIGT_AN` -> Project
- Akteur `Full Metal Iron` (`full_metal_iron`) -> `BETEILIGT_AN` -> Project
- Akteur `KL&A Engineers and Builders` (`kla_engineers_and_builders`) -> `BETEILIGT_AN` -> Project
- Akteur `Mark Young Construction` (`mark_young_construction`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Boulder Community Hospital / Boulder Community Health hospital` (`bw_boulder_community_hospital`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Fire Station 3 & Fire Administration` (`bw_boulder_fire_station_3`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Infrastruktur` (`nut_infrastruktur`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `USA` (`land_usa`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Boulder, Colorado` (`stadt_boulder_colorado`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Boulder Community Hospital / Boulder Community Health hospital` (`bw_boulder_community_hospital`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Fire Station 3 & Fire Administration` (`bw_boulder_fire_station_3`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `89 salvaged wide-flange steel members` (`bg_reuse_stahl_mehrere_boulder_wide_flange_members`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Boulder Community Hospital structural steel stockpile` (`bg_reuse_stahl_traeger_boulder_hospital_stockpile`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Neue Glulam Columns im Hybridtragwerk` (`bg_reuse_holz_stuetze_boulder_glulam`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `PV-Dach / große Dachfläche` (`bg_reuse_glas_mehrere_boulder_pv_roof`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Eigenbestand` (`bweg_eigenbestand`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Bauteiltracking` (`log_bauteiltracking`)
- Project -> `HAT_LOGISTIK` -> Logistik `Lagerung` (`log_lagerung`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Bauteilkatalogisierung` (`meth_bauteilkatalogisierung`)
- Project -> `HAT_METHODE` -> Methode `Pre_Deconstruction_Audit` (`meth_pre_deconstruction_audit`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Materialstockpile` (`rq_materialstockpile`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Urban_Mining` (`wva_urban_mining`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Aufbereitungsaufwand` (`h_aufbereitungsaufwand`)
- Project -> `HAT_HUERDE` -> Huerde `Fehlende_Standardisierung` (`h_fehlende_standardisierung`)
- Project -> `HAT_HUERDE` -> Huerde `Kompatibilitaetsproblem` (`h_kompatibilitaetsproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
**HAT_RECHTLICHE_BEDINGUNG**
- Project -> `HAT_RECHTLICHE_BEDINGUNG` -> RechtlicheBedingung `Boulder Deconstruction Ordinance 8366 / 2020` (`rb_boulder_deconstruction_ordinance_8366`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

### 13. Brent Cross Town Primary Substation

Project ID: `p_brent_cross_town_primary_substation_london`
Reuse-workflow edges: `47`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Arup` (`arup`) -> `BETEILIGT_AN` -> Project
- Akteur `Bourne Special Projects / Bourne Group` (`bourne_special_projects`) -> `BETEILIGT_AN` -> Project
- Akteur `Brent Cross South Limited Partnership` (`brent_cross_south_limited_partnership`) -> `BETEILIGT_AN` -> Project
- Akteur `Cleveland Steel & Tubes` (`cleveland_steel_tubes`) -> `BETEILIGT_AN` -> Project
- Akteur `Galldris Group` (`galldris_group`) -> `BETEILIGT_AN` -> Project
- Akteur `IF_DO` (`if_do`) -> `BETEILIGT_AN` -> Project
- Akteur `Lakwena` (`lakwena`) -> `BETEILIGT_AN` -> Project
- Akteur `London Borough of Barnet` (`london_borough_of_barnet`) -> `BETEILIGT_AN` -> Project
- Akteur `Related Argent` (`related_argent`) -> `BETEILIGT_AN` -> Project
- Akteur `Whitby Wood` (`whitby_wood`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Substation screen / oval steel structure` (`bw_brent_cross_substation_screen`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Surplus / cancelled oil-and-gas pipeline projects` (`bw_cancelled_oil_gas_pipeline_projects`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Infrastruktur` (`nut_infrastruktur`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Vereinigtes Königreich` (`land_vereinigtes_koenigreich`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `London` (`stadt_london`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Substation screen / oval steel structure` (`bw_brent_cross_substation_screen`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Surplus / cancelled oil-and-gas pipeline projects` (`bw_cancelled_oil_gas_pipeline_projects`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Neue façade support members` (`bg_reuse_stahl_fassade_brent_cross_new_support_members`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Ovaler Substation-Screen` (`bg_reuse_stahl_mehrere_brent_cross_oval_substation_screen`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Reclaimed tubular bracing members` (`bg_reuse_stahl_mehrere_brent_cross_bracing_members`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Reclaimed tubular steel columns` (`bg_reuse_stahl_mehrere_brent_cross_tubular_columns`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Direktvermittlung` (`bweg_direktvermittlung`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialverfuegbarkeit` (`log_materialverfuegbarkeit`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Haendler` (`rq_haendler`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Produktionsueberschuss` (`rq_produktionsueberschuss`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Upcycling` (`wva_upcycling`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Entwurfsbindung` (`h_entwurfsbindung`)
- Project -> `HAT_HUERDE` -> Huerde `Kompatibilitaetsproblem` (`h_kompatibilitaetsproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Verfuegbarkeitsproblem` (`h_verfuegbarkeitsproblem`)
**HAT_RECHTLICHE_BEDINGUNG**
- Project -> `HAT_RECHTLICHE_BEDINGUNG` -> RechtlicheBedingung `CE marking for reused steel` (`rb_ce_marking_reused_steel`)
- Project -> `HAT_RECHTLICHE_BEDINGUNG` -> RechtlicheBedingung `UKCA marking for reused steel` (`rb_ukca_marking_reused_steel`)
**REFERENZIERT_NORM**
- Project -> `REFERENZIERT_NORM` -> Norm `DIN_EN_15804` (`norm_din_en_15804`)
- Project -> `REFERENZIERT_NORM` -> Norm `DIN_EN_15978` (`norm_din_en_15978`)
- Project -> `REFERENZIERT_NORM` -> Norm `SCI P427 protocol` (`norm_sci_p427`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**BERECHNET_NACH_MODUL**
- Project -> `BERECHNET_NACH_MODUL` -> LCAModule `D Beyond (Reuse)` (`lz_d`)
**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx höher, Subvention/Förderung deckt Mehrkosten` (`wi_capex_hoeher_subvention`)
**RELEVANT_FOR**
- ReuseRule `Vereinigtes Königreich × Stahl reuse rule` (`rr_gb_stahl`) -> `RELEVANT_FOR` -> Project

### 14. Brighton Waste House / Brighton Wild House

Project ID: `p_brighton_waste_house_brighton`
Reuse-workflow edges: `48`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Cat Fletcher / Freegle` (`cat_fletcher_freegle`) -> `BETEILIGT_AN` -> Project
- Akteur `Duncan Baker-Brown` (`duncan_baker_brown`) -> `BETEILIGT_AN` -> Project
- Akteur `Greater Brighton Metropolitan College` (`greater_brighton_metropolitan_college`) -> `BETEILIGT_AN` -> Project
- Akteur `Mears Group` (`mears_group`) -> `BETEILIGT_AN` -> Project
- Akteur `Studierende, Schulkinder und Freiwillige` (`studierende_freiwillige`) -> `BETEILIGT_AN` -> Project
- Akteur `University of Brighton` (`university_of_brighton`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `BakerBrown` (`bakerbrown`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Duncan Baker-Brown` (`duncan_baker_brown`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `University of Brighton` (`university_of_brighton`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Brighton Waste House / Brighton Wild House` (`bw_brighton_waste_house`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Schule_Bildung` (`nut_schule_bildung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Vereinigtes Königreich` (`land_vereinigtes_koenigreich`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Brighton` (`stadt_brighton`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Brighton Waste House / Brighton Wild House` (`bw_brighton_waste_house`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Denim jeans als Dämm-/Hohlraumfüllung` (`bg_reuse_textil_daemmung_brighton_denim`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Gebrauchte Teppichfliesen als Fassaden-/Außenschicht` (`bg_reuse_mehrere_mehrere_brighton_teppichfliesen_fassade`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Holz und Sperrholz aus Reststücken` (`bg_reuse_holz_mehrere_brighton_sperrholz`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Vinylbanner als Dampfbremse` (`bg_reuse_kunststoff_technik_brighton_vinylbanner_dampfbremse`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Betonblöcke` (`bg_reuse_beton_mehrere_brighton_betonbloecke`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Zahnbürsten und Medienabfall als Hohlraumfüllung` (`bg_reuse_kunststoff_daemmung_brighton_zahnbuersten_medienabfall_infill`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Informelles_Netzwerk` (`bweg_informelles_netzwerk`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Spende` (`bweg_spende`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Lagerung` (`log_lagerung`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Baustelle` (`rq_baustelle`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Produktionsueberschuss` (`rq_produktionsueberschuss`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Recycling` (`wva_recycling`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Upcycling` (`wva_upcycling`)

#### Risk, Checks, and Constraints

**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Hohlraum / Delamination` (`def_hohlraum_delamination`)
**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Brandschutzkonflikt` (`h_brandschutzkonflikt`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Hygieneanforderung` (`h_hygieneanforderung`)
- Project -> `HAT_HUERDE` -> Huerde `Unkonventionelles_Material` (`h_unkonventionelles_material`)
- Project -> `HAT_HUERDE` -> Huerde `Witterung_Feuchte` (`h_witterung_feuchte`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Vereinigtes Königreich × Holz reuse rule` (`rr_gb_holz`) -> `RELEVANT_FOR` -> Project

### 15. Broethen Twin-House, Hoyerswerda

Project ID: `p_broethen_twin_house_hoyerswerda`
Reuse-workflow edges: `22`

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Broethen Twin-House / Doppelhaus Hoyerswerda` (`bw_broethen_twin_house`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Deutschland` (`land_deutschland`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Hoyerswerda / Broethen` (`stadt_hoyerswerda`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Broethen Twin-House / Doppelhaus Hoyerswerda` (`bw_broethen_twin_house`)
- Project -> `NUTZT_BAUWERK` -> Materialdepot `Unbekanntes P2-Massenwohnungsbau-Spendergebaeude` (`bw_p2_massenwohnungsbau_donor_unknown`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `P2-Deckenplatten` (`bg_reuse_stahlbeton_decke_broethen_p2_deckenplatten`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `P2-Wandplatten` (`bg_reuse_stahlbeton_wand_broethen_p2_wandplatten`)

#### Reuse Strategy and Process

**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Lokale_Wiederverwendung` (`log_lokale_wiederverwendung`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transportdistanz` (`log_transportdistanz`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Anschlussproblem` (`h_anschlussproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Bruch_Beschaedigungsrisiko` (`h_bruch_beschaedigungsrisiko`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)

### 16. Careno - Be.Circular Brussels — Ceramic Floor Tile Reuse Research (Rotor + RotorDC, Be.Circular grant 2016)

Project ID: `p_careno_becircular`
Reuse-workflow edges: `24`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `BBRI — Belgian Building Research Institute (Careno partner)` (`bbri`) -> `BETEILIGT_AN` -> Project
- Akteur `Rotor` -> `BETEILIGT_AN` -> Project
- Akteur `RotorDC` (`rotordc`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Lionel Billiet` (`lionel_billiet`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Sébastien Paulet` (`sebastien_paulet`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Belgien` (`land_belgien`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Brüssel` (`stadt_bruessel`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Careno — Historic ceramic flooring tiles, circa 1900-1960 (raw stock, mortar+grout residues)` (`bg_reuse_glas_keramik_boden_careno_historic_tiles`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Careno — Re-Tile machine-cleaned reclaimed floor tiles (mortar removed)` (`bg_reuse_glas_keramik_boden_careno_retile_cleaned`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Careno — RotorDC reclaimed ceramic tile stock (online + physical shop)` (`bg_reuse_glas_keramik_boden_careno_rotor_stock`)

#### Reuse Strategy and Process

**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
- Project -> `HAT_METHODE` -> Methode `Wiederverwendungskriterien` (`meth_wiederverwendungskriterien`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Aufbereitungsaufwand` (`h_aufbereitungsaufwand`)
- Project -> `HAT_HUERDE` -> Huerde `Bruch_Beschaedigungsrisiko` (`h_bruch_beschaedigungsrisiko`)
- Project -> `HAT_HUERDE` -> Huerde `Fehlende_Standardisierung` (`h_fehlende_standardisierung`)
- Project -> `HAT_HUERDE` -> Huerde `Gewaehrleistung` (`h_gewaehrleistung`)
- Project -> `HAT_HUERDE` -> Huerde `Materialqualitaet_Unklar` (`h_materialqualitaet_unklar`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)

#### Tools, Programmes, and Frameworks

**ERHALT_FOERDERUNG_DURCH**
- Project -> `ERHALT_FOERDERUNG_DURCH` -> Akteur `Brussels-Capital Region — Careno Be.Circular grant authority` (`brussels_capital_region`)
**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx höher, Subvention/Förderung deckt Mehrkosten` (`wi_capex_hoeher_subvention`)
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Geschaeftsmodell` (`wi_geschaeftsmodell`)
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Preisbildung` (`wi_preisbildung`)
**NUTZT_SOFTWARE**
- Project -> `NUTZT_SOFTWARE` -> Software:Tool `Re-Tile — Ceramic Tile Cleaning Machine (RotorDC + Be.Circular, 2022)` (`tool_retile`)
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Be.Circular Brussels — circular-economy initiative grant programme` (`prog_be_circular`)

### 17. CascadeUp / London secondary-timber glulam demonstrator

Project ID: `p_cascadeup_london_secondary_timber_glulam_demonstrator`
Reuse-workflow edges: `40`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Dr Colin Rose` (`colin_rose`) -> `BETEILIGT_AN` -> Project
- Akteur `UCL Circular Economy Lab` (`ucl_circular_economy_lab`) -> `BETEILIGT_AN` -> Project
- Akteur `UK CLT` (`uk_clt`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `CascadeUp modularer Demonstrator` (`bw_cascadeup_modular_demonstrator`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Schule_Bildung` (`nut_schule_bildung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Prototyp` (`status_prototyp`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Vereinigtes Königreich` (`land_vereinigtes_koenigreich`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `London` (`stadt_london`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `CascadeUp modularer Demonstrator` (`bw_cascadeup_modular_demonstrator`)
- Project -> `NUTZT_BAUWERK` -> Materialdepot `Unbekannte Rueckbauholz- / demolition-waste-streams` (`bw_unknown_demolition_wood_streams`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `CLST-Bodenpaneele` (`bg_reuse_holz_mehrere_cascadeup_clst_floor_panels`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `CLST-Wandpaneele` (`bg_reuse_holz_wand_cascadeup_clst`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `glulamST-Tragwerksrahmen / Balken und Stuetzen` (`bg_reuse_holz_mehrere_cascadeup_glulamst_frame`)

#### Reuse Strategy and Process

**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialverfuegbarkeit` (`log_materialverfuegbarkeit`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Bauteilkatalogisierung` (`meth_bauteilkatalogisierung`)
- Project -> `HAT_METHODE` -> Methode `Design_for_Disassembly` (`meth_design_for_disassembly`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Baustelle` (`rq_baustelle`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Design_for_Disassembly` (`wva_design_for_disassembly`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Remanufacturing` (`wva_remanufacturing`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Upcycling` (`wva_upcycling`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Aufbereitungsaufwand` (`h_aufbereitungsaufwand`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Fehlende_Standardisierung` (`h_fehlende_standardisierung`)
- Project -> `HAT_HUERDE` -> Huerde `Gewaehrleistung` (`h_gewaehrleistung`)
- Project -> `HAT_HUERDE` -> Huerde `Haftung` (`h_haftung`)
- Project -> `HAT_HUERDE` -> Huerde `Materialqualitaet_Unklar` (`h_materialqualitaet_unklar`)
- Project -> `HAT_HUERDE` -> Huerde `Verfuegbarkeitsproblem` (`h_verfuegbarkeitsproblem`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Vereinigtes Königreich × Holz reuse rule` (`rr_gb_holz`) -> `RELEVANT_FOR` -> Project

### 19. Chiro d’Itterbeek / Sanitary block, Dilbeek

Project ID: `p_chiro_d_itterbeek_dilbeek`
Reuse-workflow edges: `65`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Bouwstocks` (`bouwstocks`) -> `BETEILIGT_AN` -> Project
- Akteur `CC Autrement` (`cc_autrement`) -> `BETEILIGT_AN` -> Project
- Akteur `Commune de Dilbeek` (`commune_de_dilbeek`) -> `BETEILIGT_AN` -> Project
- Akteur `Franck` (`franck`) -> `BETEILIGT_AN` -> Project
- Akteur `Gebruiktebouwmaterialen` (`gebruiktebouwmaterialen`) -> `BETEILIGT_AN` -> Project
- Akteur `Namur Croisade pauvreté` (`namur_croisade_pauvrete`) -> `BETEILIGT_AN` -> Project
- Akteur `Rotor` -> `BETEILIGT_AN` -> Project
- Akteur `RotorDC` (`rotordc`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Sanitary block for the Itterbeek Chiro` (`bw_chiro_itterbeek_sanitary_block`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Erweiterung` (`bai_erweiterung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Sozialbau` (`nut_sozialbau`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Belgien` (`land_belgien`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Dilbeek / Itterbeek` (`stadt_dilbeek`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Sanitary block for the Itterbeek Chiro` (`bw_chiro_itterbeek_sanitary_block`)
- Project -> `NUTZT_BAUWERK` -> Materialdepot `Reuse-/Surplus-Liefernetz Chiro d’Itterbeek` (`bw_chiro_itterbeek_reuse_supply_network`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Außentüren` (`bg_reuse_holz_tuer_chiro_external`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Bodenfliesen` (`bg_reuse_keramik_boden_chiro_tiles`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Dachziegel (Chiro)` (`bg_reuse_ziegel_dach_chiro_tiles`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Fassadenziegel (Chiro)` (`bg_reuse_ziegel_mehrere_chiro_facade`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Holzfenster` (`bg_reuse_holz_fenster_chiro`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Leuchten` (`bg_reuse_unbekannt_technik_chiro_luminaires`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Sanitärobjekte (Chiro)` (`bg_reuse_mehrere_technik_chiro_sanitary_fixtures`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Stahl-U-Profile als Außenstürze` (`bg_reuse_stahl_mehrere_chiro_u_lintels`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Surplus-Betonblöcke` (`bg_reuse_beton_wand_chiro_surplus_blocks`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Surplus-Dämmung Boden/Wand` (`bg_reuse_daemmstoff_daemmung_chiro_surplus_floor_wall`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Surplus-Dämmung Decke` (`bg_reuse_daemmstoff_daemmung_chiro_surplus_ceiling`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Surplus-Holzrahmen / Dachtragwerk` (`bg_reuse_holz_mehrere_chiro_surplus_roof_frame`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wandfliesen` (`bg_reuse_keramik_wand_chiro_tiles`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Bauteilboerse` (`bweg_bauteilboerse`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Direktvermittlung` (`bweg_direktvermittlung`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Spende` (`bweg_spende`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Lokale_Wiederverwendung` (`log_lokale_wiederverwendung`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialverfuegbarkeit` (`log_materialverfuegbarkeit`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
- Project -> `HAT_METHODE` -> Methode `Zirkulaere_Ausschreibung` (`meth_zirkulaere_ausschreibung`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Bauteilboerse` (`rq_bauteilboerse`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Haendler` (`rq_haendler`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Materialstockpile` (`rq_materialstockpile`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Produktionsueberschuss` (`rq_produktionsueberschuss`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Upcycling` (`wva_upcycling`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Kompatibilitaetsproblem` (`h_kompatibilitaetsproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Mengenunsicherheit` (`h_mengenunsicherheit`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Terminunsicherheit` (`h_terminunsicherheit`)
- Project -> `HAT_HUERDE` -> Huerde `Verfuegbarkeitsproblem` (`h_verfuegbarkeitsproblem`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Asbest` (`s_asbest`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `KMF — Künstliche Mineralfasern (alte Mineralwolle vor 1996/2000)` (`s_kmf`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Versteckte Kosten (Lagerung/Prüfung/Logistik)` (`wi_hidden_costs_lagerung_pruefung`)
**RELEVANT_FOR**
- ReuseRule `Belgien × Beton reuse rule` (`rr_be_beton`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Belgien × Holz reuse rule` (`rr_be_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Belgien × Stahl reuse rule` (`rr_be_stahl`) -> `RELEVANT_FOR` -> Project

### 20. Christus-Pavillon / Christ Pavilion Volkenroda

Project ID: `p_christ_pavilion_volkenroda`
Reuse-workflow edges: `40`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Andreas Felger` (`andreas_felger`) -> `BETEILIGT_AN` -> Project
- Akteur `Evangelisch-Lutherische Landeskirche Hannover` (`ev_luth_landeskirche_hannover`) -> `BETEILIGT_AN` -> Project
- Akteur `Evangelisches Buero fuer die Weltausstellung Expo 2000` (`evangelisches_buero_expo_2000`) -> `BETEILIGT_AN` -> Project
- Akteur `Joachim Zais` (`joachim_zais`) -> `BETEILIGT_AN` -> Project
- Akteur `Kloster Volkenroda / Jesus-Bruderschaft` (`kloster_volkenroda_jesus_bruderschaft`) -> `BETEILIGT_AN` -> Project
- Akteur `Meinhard von Gerkan` (`meinhard_von_gerkan`) -> `BETEILIGT_AN` -> Project
- Akteur `gmp Architekten von Gerkan, Marg und Partner` (`gmp_architekten`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Christus-Pavillon EXPO 2000 Hannover` (`bw_christus_pavillon_expo_hannover`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Christus-Pavillon Volkenroda` (`bw_christus_pavillon_volkenroda`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Translozierung` (`bai_translozierung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Wiederaufbau` (`bai_wiederaufbau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Deutschland` (`land_deutschland`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Volkenroda / Koerner` (`stadt_volkenroda_koerner`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Christus-Pavillon EXPO 2000 Hannover` (`bw_christus_pavillon_expo_hannover`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Christus-Pavillon Volkenroda` (`bw_christus_pavillon_volkenroda`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Dachtragwerk Christusraum` (`bg_reuse_stahl_mehrere_christ_pavilion_roof_structure`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Gesamtes transloziertes Pavillonensemble` (`bg_reuse_mehrere_mehrere_christ_pavilion_complete_ensemble`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Kreuzgang / Stahl-Glas-Fassade und Vitrinen` (`bg_reuse_mehrere_mehrere_christ_pavilion_cloister_glass_facade`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Marmor-Glas-Wand Christusraum` (`bg_reuse_mehrere_mehrere_christ_pavilion_marble_glass_wall`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Neun kreuzfoermige Stahlstuetzen` (`bg_reuse_stahl_stuetze_christ_pavilion_cross`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Sichtbetonteile des translozierten Ensembles` (`bg_reuse_beton_mehrere_christ_pavilion_fair_faced_parts`)

#### Reuse Strategy and Process

**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Bauteiltracking` (`log_bauteiltracking`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transport` (`log_transport`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Design_for_Disassembly` (`meth_design_for_disassembly`)
- Project -> `HAT_METHODE` -> Methode `Reversibilitaet` (`meth_reversibilitaet`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Design_for_Disassembly` (`wva_design_for_disassembly`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Anschlussproblem` (`h_anschlussproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Bruch_Beschaedigungsrisiko` (`h_bruch_beschaedigungsrisiko`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Witterung_Feuchte` (`h_witterung_feuchte`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Deutschland × Beton reuse rule` (`rr_de_beton`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Deutschland × Stahl reuse rule` (`rr_de_stahl`) -> `RELEVANT_FOR` -> Project
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `EXPO 2000 Hannover` (`prog_expo_2000`)

### 21. Circl / ABN AMRO urban mining context

Project ID: `p_circl_abn_amro`
Reuse-workflow edges: `59`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `ABN AMRO Bank N.V. — Circl pavilion client / initiator` (`abn_amro`) -> `BETEILIGT_AN` -> Project
- Akteur `BAM Bouw + Techniek (Royal BAM Group) — Circl construction team` (`bam_bouw_techniek`) -> `BETEILIGT_AN` -> Project
- Akteur `De Groot & Visser` (`de_groot_en_visser`) -> `BETEILIGT_AN` -> Project
- Akteur `Delft University of Technology — Circl research partner + REBRIDGE partner` (`tu_delft`) -> `BETEILIGT_AN` -> Project
- Akteur `Donkergroen — Circl landscape / plant-module supplier` (`donkergroen`) -> `BETEILIGT_AN` -> Project
- Akteur `Exasun — Circl solar panel supplier` (`exasun`) -> `BETEILIGT_AN` -> Project
- Akteur `Fagerhult — Circl DC lighting supplier (leased)` (`fagerhult`) -> `BETEILIGT_AN` -> Project
- Akteur `Icon Real Estate (Victory Group) — Circl site redevelopment lead` (`icon_real_estate`) -> `BETEILIGT_AN` -> Project
- Akteur `New Horizon Urban Mining — Circl second-hand fire-hose-reel cabinet supplier` (`new_horizon_urban_mining`) -> `BETEILIGT_AN` -> Project
- Akteur `TRAJECT — Circl construction-team coordinator` (`traject`) -> `BETEILIGT_AN` -> Project
- Akteur `Ter Velde & Den Besten — 3D laser scanning provider (Circl digital twin)` (`ter_velde_den_besten`) -> `BETEILIGT_AN` -> Project
- Akteur `Vermaat — Circl circular catering operator` (`vermaat`) -> `BETEILIGT_AN` -> Project
- Akteur `Victory Group — owner of ABN AMRO complex including Circl post-2024` (`victory_group`) -> `BETEILIGT_AN` -> Project
- Akteur `lcp-circulair (Lagemaat + cepezedprojects alliance) — Circl dismantling contractor` (`lcp_circulair`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Hans Hammink` (`hans_hammink`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Michel Baars` (`michel_baars`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Circl — ABN AMRO Circular Pavilion Amsterdam (2017–2025, dismantled)` (`bw_circl_pavilion_amsterdam`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Rueckbau` (`bai_rueckbau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Mischnutzung` (`nut_mischnutzung`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Niederlande` (`land_niederlande`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Amsterdam` (`stadt_amsterdam`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Circl — ABN AMRO Circular Pavilion Amsterdam (2017–2025, dismantled)` (`bw_circl_pavilion_amsterdam`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Circl — 16,000 old jeans incorporated as ceiling insulation (Denimtex)` (`bg_reuse_daemmstoff_daemmung_circl_jeans_insulation`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Circl — 500 roof solar panels, ~7 years old, lower output than new panels (Exasun)` (`bg_dismantled_mehrere_technik_circl_solar_panels`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Circl — C2C-certified Tarkett iQ One flooring` (`bg_planned_kunststoff_boden_circl_c2c_tarkett`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Circl — Conference-room window frames, carefully removed from demolished office buildings` (`bg_reuse_mehrere_fenster_circl_conference_windows`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Circl — Floor structure (less suitable for reuse than anticipated per Icon dismantling progress)` (`bg_dismantled_mehrere_boden_circl_floor_structure`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Circl — Fully demountable locally-sourced larch timber support structure (installed 2017; dismantled 2024-2025)` (`bg_dismantled_holz_mehrere_circl_larch_structure`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Circl — Leased Fagerhult DC lighting (product-service system)` (`bg_planned_mehrere_technik_circl_leased_lighting`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Circl — Leased lifts (product-service system, supplier ownership, 10-year return)` (`bg_planned_mehrere_technik_circl_leased_lifts`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Circl — Rejected wooden window frames cut into floorboards` (`bg_reuse_holz_boden_circl_window_frame_floor`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Circl — Remountable façade with C2C-certified plant modules (De Groot & Visser + Donkergroen)` (`bg_planned_mehrere_fassade_circl_remountable_facade`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Circl — Restored ABN AMRO furniture (intra-konzern reuse)` (`bg_reuse_mehrere_ausbau_circl_restored_furniture`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Circl — Roof terrace + garden planting harvested by local residents (Stichting Struikroven)` (`bg_reuse_mehrere_ausbau_circl_greenery_harvest`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Circl — Second-hand fire-hose-reel cabinets (New Horizon Urban Mining supplier)` (`bg_reuse_metall_technik_circl_fire_hose_cabinets`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Circl — Stuccoed walls + tribune felt from old ABN AMRO business clothing` (`bg_reuse_textil_wand_circl_clothing_felt`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Circl — Tile floors from reused concrete with PCM` (`bg_reuse_mineralisch_boden_circl_pcm_tiles`)

#### Reuse Strategy and Process

**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Abrissmonitoring` (`meth_abrissmonitoring`)
- Project -> `HAT_METHODE` -> Methode `Design_for_Disassembly` (`meth_design_for_disassembly`)
- Project -> `HAT_METHODE` -> Methode `Urban_Mining` (`meth_urban_mining`)
- Project -> `HAT_METHODE` -> Methode `Zirkulaere_Ausschreibung` (`meth_zirkulaere_ausschreibung`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Anschlussproblem` (`h_anschlussproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Dauerhaftigkeit_Restlebensdauer` (`h_dauerhaftigkeit_restlebensdauer`)
- Project -> `HAT_HUERDE` -> Huerde `Materialqualitaet_Unklar` (`h_materialqualitaet_unklar`)
- Project -> `HAT_HUERDE` -> Huerde `Zustand_Unklar` (`h_zustand_unklar`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx höher, Marketing-/Branding-Payback` (`wi_capex_hoeher_marketing_payback`)
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Geschaeftsmodell` (`wi_geschaeftsmodell`)
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Lebenszykluskosten` (`wi_lebenszykluskosten`)
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Restwert` (`wi_restwert`)
**NUTZT_SOFTWARE**
- Project -> `NUTZT_SOFTWARE` -> Software `LLMNT Material Passport Platform (Circl digital twin)` (`software_llmnt`)
**RELEVANT_FOR**
- ReuseRule `Niederlande × Holz reuse rule` (`rr_nl_holz`) -> `RELEVANT_FOR` -> Project
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `ABN AMRO Mission 2030 — circular-economy knowledge-sharing programme` (`prog_abn_amro_mission_2030`)

### 22. Circle House

Project ID: `p_circle_house`
Reuse-workflow edges: `6`

#### Actors and Delivery Chain

**STUB_PROJECT_LINK**
- Akteur `Kasper Guldager Jensen` (`kasper_guldager_jensen`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Katrine West Kristensen` (`katrine_west_kristensen`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Søren Nielsen` (`soren_nielsen`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Vandkunsten` (`vandkunsten`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Dänemark` (`land_daenemark`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Aarhus` (`stadt_aarhus`)

### 23. Circular Centre Netherlands / Prinsenhof A reuse pilot

Project ID: `p_circular_centre_netherlands_prinsenhof_a_reuse_pilot`
Reuse-workflow edges: `52`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Dycore` (`dycore`) -> `BETEILIGT_AN` -> Project
- Akteur `IMd Raadgevende Ingenieurs` (`imd_raadgevende_ingenieurs`) -> `BETEILIGT_AN` -> Project
- Akteur `Lagemaat Heerde` (`lagemaat_heerde`) -> `BETEILIGT_AN` -> Project
- Akteur `Provincie Gelderland` (`provincie_gelderland`) -> `BETEILIGT_AN` -> Project
- Akteur `ReCreate Dutch cluster` (`recreate_dutch_cluster`) -> `BETEILIGT_AN` -> Project
- Akteur `cepezed` -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Circulair Centrum Nederland / Circular Centre Netherlands, Heerde` (`bw_ccn_heerde_receiver`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Prinsenhof A, Arnhem` (`bw_prinsenhof_a_arnhem_donor`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Rueckbau` (`bai_rueckbau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Schule_Bildung` (`nut_schule_bildung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Geplant` (`status_geplant`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Niederlande` (`land_niederlande`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Arnhem` (`stadt_arnhem`)
- Project -> `LIEGT_IN_STADT` -> Stadt `Heerde` (`stadt_heerde`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Circulair Centrum Nederland / Circular Centre Netherlands, Heerde` (`bw_ccn_heerde_receiver`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Prinsenhof A, Arnhem` (`bw_prinsenhof_a_arnhem_donor`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Betonbruestungen / parapets` (`bg_reuse_beton_fassade_ccn_parapets`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Hohlkoerperdecken / kanaalplaatvloeren` (`bg_reuse_stahlbeton_decke_ccn_hollow_core_slabs`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Prefab-Fassadenelemente` (`bg_reuse_stahlbeton_mehrere_ccn_prefab_facade_elements`)

#### Reuse Strategy and Process

**HAT_AUFBEREITUNG**
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `Sägen von Betonfertigteilen` (`av_betonfertigteil_saegen`)
**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Eigenbestand` (`bweg_eigenbestand`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Lagerung` (`log_lagerung`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transport` (`log_transport`)
- Project -> `HAT_LOGISTIK` -> Logistik `Zwischenlagerung` (`log_zwischenlagerung`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Aufbereitung` (`phase_aufbereitung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Planung` (`phase_planung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Rueckbau` (`phase_rueckbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Refurbishment` (`wva_refurbishment`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Urban_Mining` (`wva_urban_mining`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Aufbereitungsaufwand` (`h_aufbereitungsaufwand`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Entwurfsbindung` (`h_entwurfsbindung`)
- Project -> `HAT_HUERDE` -> Huerde `Fehlende_Lagerflaeche` (`h_fehlende_lagerflaeche`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
**HAT_PRUEFUNG**
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_bewehrungsscan`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_hebepunktnachweis`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_risspruefung`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_schnittplan`
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Niederlande × Beton reuse rule` (`rr_nl_beton`) -> `RELEVANT_FOR` -> Project
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Forschungsprojekt` (`prog_forschungsprojekt`)
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Pilotprojekt` (`prog_pilotprojekt`)

### 24. Circular Pavilion Paris

Project ID: `p_circular_pavilion_paris`
Reuse-workflow edges: `54`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Bonnefrite` (`bonnefrite`) -> `BETEILIGT_AN` -> Project
- Akteur `Camping Design` (`camping_design`) -> `BETEILIGT_AN` -> Project
- Akteur `Encore Heureux` (`encore_heureux`) -> `BETEILIGT_AN` -> Project
- Akteur `TRIBU` (`tribu`) -> `BETEILIGT_AN` -> Project
- Akteur `Technische Dienste der Stadt Paris` (`services_techniques_ville_de_paris`) -> `BETEILIGT_AN` -> Project
- Akteur `Ville de Paris – Pavillon de l Arsenal` (`ville_de_paris_pavillon_arsenal`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Julien Choppin` (`julien_choppin`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Nicola Delon` (`nicola_delon`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Circular Pavilion at Parvis de l Hotel de Ville` (`bw_circular_pavilion_paris`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Schule_Bildung` (`nut_schule_bildung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
- Project -> `HAT_STATUS` -> Status `Temporaer` (`status_temporaer`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Frankreich` (`land_frankreich`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Paris` (`stadt_paris`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Circular Pavilion at Parvis de l Hotel de Ville` (`bw_circular_pavilion_paris`)
- Project -> `NUTZT_BAUWERK` -> Materialdepot `Aggregierte Pariser Materialquellen fuer Circular Pavilion` (`bw_paris_material_sources_circular_pavilion`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `180 Holztueren als Fassade` (`bg_reuse_holz_mehrere_circular_pavilion_doors_facade`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Ehemalige Ausstellungspaneele` (`bg_reuse_holz_mehrere_circular_pavilion_exhibition_panels`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Holzstruktur aus Baustellenresten` (`bg_reuse_holz_mehrere_circular_pavilion_structure`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Mineral-/Steinwolle als Innendaemmung` (`bg_reuse_daemmstoff_daemmung_circular_pavilion_mineral_wool`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Terrassen-Caillebotis aus Paris-Plage` (`bg_reuse_holz_boden_circular_pavilion_terrace_decking`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Vier grosse Leuchten aus oeffentlichem Bestand` (`bg_reuse_unbekannt_technik_circular_pavilion_lights`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Eigenbestand` (`bweg_eigenbestand`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Informelles_Netzwerk` (`bweg_informelles_netzwerk`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transport` (`log_transport`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Planung` (`phase_planung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Baustelle` (`rq_baustelle`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Lager` (`rq_lager`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Produktionsueberschuss` (`rq_produktionsueberschuss`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Design_for_Disassembly` (`wva_design_for_disassembly`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Upcycling` (`wva_upcycling`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Brandschutzkonflikt` (`h_brandschutzkonflikt`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Heterogenitaet_Chargen` (`h_heterogenitaet_chargen`)
- Project -> `HAT_HUERDE` -> Huerde `Unkonventionelles_Material` (`h_unkonventionelles_material`)
- Project -> `HAT_HUERDE` -> Huerde `Witterung_Feuchte` (`h_witterung_feuchte`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Asbest` (`s_asbest`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `KMF — Künstliche Mineralfasern (alte Mineralwolle vor 1996/2000)` (`s_kmf`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

### 25. CRCLR House / Impact Hub Berlin

Project ID: `p_crclr_house_impact_hub_berlin`
Reuse-workflow edges: `74`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Akustik-Ingenieurbuero Moll` (`akustik_ingenieurbuero_moll`) -> `BETEILIGT_AN` -> Project
- Akteur `Concular` (`concular`) -> `BETEILIGT_AN` -> Project
- Akteur `Die Zusammenarbeiter` (`die_zusammenarbeiter`) -> `BETEILIGT_AN` -> Project
- Akteur `LXSY Architektur` (`lxsy_architektur`) -> `BETEILIGT_AN` -> Project
- Akteur `Solares Bauen` (`solares_bauen`) -> `BETEILIGT_AN` -> Project
- Akteur `TRNSFRM eG` (`trnsfrm_eg`) -> `BETEILIGT_AN` -> Project
- Akteur `ZRS Ingenieure` (`zrs_ingenieure`) -> `BETEILIGT_AN` -> Project
- Akteur `brandkontrolle` -> `BETEILIGT_AN` -> Project
- Akteur `eZeit` (`ezeit`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Christian Schöningh` (`christian_schoeningh`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Die Zusammenarbeiter` (`die_zusammenarbeiter`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Kim Le Roux` (`kim_le_roux`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Margit Sichrovsky` (`margit_sichrovsky`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `TRNSFRM eG` (`trnsfrm_eg`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Wiebke Ahues` (`wiebke_ahues`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Externe Reuse-Quellen CRCLR` (`bw_crclr_external_reuse_sources`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Aufstockung` (`bai_aufstockung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Fit_out` (`bai_fit_out`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umnutzung` (`bai_umnutzung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Mischnutzung` (`nut_mischnutzung`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Deutschland` (`land_deutschland`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Berlin` (`stadt_berlin`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Externe Reuse-Quellen CRCLR` (`bw_crclr_external_reuse_sources`)
- Project -> `NUTZT_BAUWERK` -> Materialdepot `Ehemalige Lager-/Fassladehalle auf dem Kindl-Areal / CRCLR House` (`bw_crclr_kindl_hall`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Holzgalerie / Innenausbau aus heterogenen Restmaterialien` (`bg_reuse_holz_mehrere_crclr_recycled_gallery_interior`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Stahlfachwerktraeger fuer Gewaechshausdach / unsicherer Umfang` (`bg_reuse_stahl_mehrere_crclr_trusses_greenhouse`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Stahlpfetten / I-Traeger aus Hallendach als Treppenwangen` (`bg_reuse_stahl_mehrere_crclr_roof_to_stair_stringers`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Vorhangfassadenelemente, Blech und Glas` (`bg_reuse_mehrere_fassade_crclr_curtain_wall_sheet_glass`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Holz-Alu-Fenster / Außenfenster` (`bg_reuse_mehrere_mehrere_crclr_wood_aluminium_windows`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Sanitärobjekte / Duschtassen` (`bg_reuse_keramik_technik_crclr_sanitary_objects`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Eigenbestand` (`bweg_eigenbestand`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Informelles_Netzwerk` (`bweg_informelles_netzwerk`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Lagerung` (`log_lagerung`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
- Project -> `HAT_METHODE` -> Methode `Design_for_Disassembly` (`meth_design_for_disassembly`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
- Project -> `HAT_METHODE` -> Methode `Reversibilitaet` (`meth_reversibilitaet`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Dokumentation` (`phase_dokumentation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Pruefung` (`phase_pruefung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Rueckbau` (`phase_rueckbau`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Baustelle` (`rq_baustelle`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Lager` (`rq_lager`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Adaptives_ReUse` (`wva_adaptives_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Bestandserhalt` (`wva_bestandserhalt`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Design_for_Disassembly` (`wva_design_for_disassembly`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Same_Site_ReUse` (`wva_same_site_reuse`)

#### Risk, Checks, and Constraints

**HAS_RISK_POLLUTANT**
- Project -> `HAS_RISK_POLLUTANT` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Bauproduktstatus` (`h_bauproduktstatus`)
- Project -> `HAT_HUERDE` -> Huerde `Brandschutzkonflikt` (`h_brandschutzkonflikt`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Gewaehrleistung` (`h_gewaehrleistung`)
- Project -> `HAT_HUERDE` -> Huerde `Haftung` (`h_haftung`)
- Project -> `HAT_HUERDE` -> Huerde `Materialqualitaet_Unklar` (`h_materialqualitaet_unklar`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Deutschland × Holz reuse rule` (`rr_de_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Deutschland × Stahl reuse rule` (`rr_de_stahl`) -> `RELEVANT_FOR` -> Project

### 26. Eggshell Pavilion ETH MAS DFAB 2022 (Gramazio Kohler Research; Weil am Rhein, DE)

Project ID: `p_eggshell_pavilion`
Reuse-workflow edges: `8`

#### Place and Built Context

**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Deutschland` (`land_deutschland`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Weil am Rhein` (`stadt_weil_am_rhein`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Eggshell Pavilion — robotic 3D-printed recycled formwork material, reversible connections (ETH MAS DFAB 2022)` (`bg_reuse_mehrere_mehrere_eggshell_recycled_structure`)

#### Reuse Strategy and Process

**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Design_for_Disassembly` (`meth_design_for_disassembly`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Bauproduktstatus` (`h_bauproduktstatus`)
- Project -> `HAT_HUERDE` -> Huerde `Unkonventionelles_Material` (`h_unkonventionelles_material`)

#### Tools, Programmes, and Frameworks

**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `MAS Architektur und Digitale Fabrikation, ETH Zürich (Gramazio Kohler Research)` (`prog_mas_dfab`)

### 27. ELEMENTA Walkeweg Basel — Wohnbau mit Wiederverwendung von Bestandskomponenten (Kanton Basel-Stadt Wettbewerb)

Project ID: `p_elementa_walkeweg`
Reuse-workflow edges: `48`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `AFC — cost management / quantity surveying` (`afc_basel`) -> `BETEILIGT_AN` -> Project
- Akteur `Ana Olalquiaga — architect at PARABASE` (`ana_olalquiaga`) -> `BETEILIGT_AN` -> Project
- Akteur `Anima Engineering AG — specialist engineering` (`anima_engineering`) -> `BETEILIGT_AN` -> Project
- Akteur `Bauteilbörse Basel — component exchange platform` (`bauteilboerse_basel`) -> `BETEILIGT_AN` -> Project
- Akteur `Caretta+Weidmann — façade engineering` (`caretta_weidmann`) -> `BETEILIGT_AN` -> Project
- Akteur `Digvis GmbH — digital visualisation (ELEMENTA)` (`digvis_gmbh`) -> `BETEILIGT_AN` -> Project
- Akteur `GTI Engineering — MEP / building services (ELEMENTA)` (`gti_engineering`) -> `BETEILIGT_AN` -> Project
- Akteur `Kanton Basel-Stadt — ELEMENTA public authority / programme owner` (`kanton_basel_stadt`) -> `BETEILIGT_AN` -> Project
- Akteur `Mario Monotti — structural engineer at Monotti Ingegneri` (`mario_monotti`) -> `BETEILIGT_AN` -> Project
- Akteur `Monotti Ingegneri Consulenti SA — structural engineer (ELEMENTA)` (`monotti_ingegneri`) -> `BETEILIGT_AN` -> Project
- Akteur `Roger Keller — landscape architect at USUS` (`roger_keller`) -> `BETEILIGT_AN` -> Project
- Akteur `Senn Technology AG — specialist engineering` (`senn_technology`) -> `BETEILIGT_AN` -> Project
- Akteur `USUS Landschaftsarchitektur — landscape architect (ELEMENTA)` (`usus_la`) -> `BETEILIGT_AN` -> Project
- Akteur `Zirkular` (`zirkular`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Carla Ferrando Costansa` (`carla_ferrando_costansa`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Pablo Garrido Arnaiz` (`pablo_garrido_arnaiz`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `ELEMENTA Walkeweg Basel — Wohnbau mit Wiederverwendung von Bestandskomponenten` (`bw_elementa_walkeweg_basel`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Lysbüchel Parkgarage Basel — donor for ELEMENTA RC columns/slabs/rib-panels` (`bw_lysbueechel_garage_basel`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Schweiz` (`land_schweiz`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Basel` (`stadt_basel`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `ELEMENTA Walkeweg Basel — Wohnbau mit Wiederverwendung von Bestandskomponenten` (`bw_elementa_walkeweg_basel`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `ELEMENTA — Brettstapeldecken (new renewable wood)` (`bg_planned_holz_decke_elementa_brettstapel`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `ELEMENTA — Lehmbauplatten + Lehmputz (clay boards + plaster)` (`bg_planned_lehm_erde_wand_elementa_clay`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `ELEMENTA — RC rib-panel load-bearing exterior wall (Baufeld D from Lysbüchel garage)` (`bg_reuse_mineralisch_wand_elementa_baufeld_d`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `ELEMENTA — Reused RC column-beam structure (Baufeld C from Lysbüchel garage)` (`bg_reuse_mineralisch_stuetze_elementa_baufeld_c`)

#### Reuse Strategy and Process

**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Bauteilkatalogisierung` (`meth_bauteilkatalogisierung`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
- Project -> `HAT_METHODE` -> Methode `Pre_Deconstruction_Audit` (`meth_pre_deconstruction_audit`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Entwurfsbindung` (`h_entwurfsbindung`)
- Project -> `HAT_HUERDE` -> Huerde `Heterogenitaet_Chargen` (`h_heterogenitaet_chargen`)
- Project -> `HAT_HUERDE` -> Huerde `Terminunsicherheit` (`h_terminunsicherheit`)
- Project -> `HAT_HUERDE` -> Huerde `Toleranzen` (`h_toleranzen`)
- Project -> `HAT_HUERDE` -> Huerde `Verfuegbarkeitsproblem` (`h_verfuegbarkeitsproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Zustand_Unklar` (`h_zustand_unklar`)
**REFERENZIERT_NORM**
- Project -> `REFERENZIERT_NORM` -> Norm `SIA 269 — Existing structures: Grundlagen / Erhaltung von Tragwerken` (`norm_sia_269`)
- Project -> `REFERENZIERT_NORM` -> Norm `SIA 380/1 — Heizwärmebedarf (Schweiz)` (`norm_sia_380_1`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Asbest` (`s_asbest`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx höher, Subvention/Förderung deckt Mehrkosten` (`wi_capex_hoeher_subvention`)
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx niedriger (direkte Materialersparnis)` (`wi_capex_niedriger_direkter_ersparnis`)
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Lebenszykluskosten` (`wi_lebenszykluskosten`)
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Versteckte Kosten (Lagerung/Prüfung/Logistik)` (`wi_hidden_costs_lagerung_pruefung`)
**HAT_ZERTIFIZIERUNG**
- Project -> `HAT_ZERTIFIZIERUNG` -> Zertifizierungssystem `EcoTool (ZBS)` (`zbs_ecotool`)
**NUTZT_SOFTWARE**
- Project -> `NUTZT_SOFTWARE` -> Software `EcoTool — ökologische Bilanz (Pflichtnachweis Wettbewerb Lysbüchel)` (`software_ecotool`)
- Project -> `NUTZT_SOFTWARE` -> Software:Tool `Bauteilkatalog / Bauteilpass` (`tool_bauteilkatalog`)

### 28. ELYS Kultur- und Gewerbehaus Basel

Project ID: `p_elys_kultur_gewerbehaus_basel`
Reuse-workflow edges: `79`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `HUSNER AG Holzbau` (`husner_ag_holzbau`) -> `BETEILIGT_AN` -> Project
- Akteur `Haustec Engineering` (`haustec_engineering`) -> `BETEILIGT_AN` -> Project
- Akteur `Hochbauamt Basel-Stadt` (`hochbauamt_basel_stadt`) -> `BETEILIGT_AN` -> Project
- Akteur `Immobilien Basel-Stadt` (`immobilien_basel_stadt`) -> `BETEILIGT_AN` -> Project
- Akteur `Jauslin Stebler` (`jauslin_stebler`) -> `BETEILIGT_AN` -> Project
- Akteur `Pro Engineering` (`pro_engineering`) -> `BETEILIGT_AN` -> Project
- Akteur `Rapp AG` (`rapp_ag`) -> `BETEILIGT_AN` -> Project
- Akteur `S+B` (`s_plus_b`) -> `BETEILIGT_AN` -> Project
- Akteur `Zirkular` (`zirkular`) -> `BETEILIGT_AN` -> Project
- Akteur `baubüro in situ` (`baubuero_in_situ`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Barbara Buser` (`barbara_buser`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Benjamin Poignon` (`benjamin_poignon`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Charlotte Bofinger` (`charlotte_bofinger`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Kerstin Müller` (`kerstin_mueller`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Marc Angst` (`marc_angst`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Michel Massmünster` (`michel_massmuenster`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Pascal Hentschel` (`pascal_hentschel`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Zirkular` (`zirkular`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `baubüro in situ` (`baubuero_in_situ`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Ehemaliges Coop-Verteilzentrum / Grossbaeckerei Basel` (`bw_elys_former_coop_distribution_center`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Ehemaliges Coop-Verteilzentrum / Grossbaeckerei Basel` (`bw_elys_former_coop_distribution_center`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Regionale Rueckbau- und Lagerquellen fuer ELYS-Fassade` (`bw_elys_regional_reuse_sources`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Sanierung` (`bai_sanierung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umnutzung` (`bai_umnutzung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Mischnutzung` (`nut_mischnutzung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Schweiz` (`land_schweiz`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Basel` (`stadt_basel`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Ehemaliges Coop-Verteilzentrum / Grossbaeckerei Basel` (`bw_elys_former_coop_distribution_center`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Regionale Rueckbau- und Lagerquellen fuer ELYS-Fassade` (`bw_elys_regional_reuse_sources`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `200 Fenster aus Lagerrestbeständen` (`bg_reuse_glas_mehrere_elys_restposten_windows`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Altholz aus Rückbauten / Dachstühlen` (`bg_reuse_holz_mehrere_elys_frame`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Aluminium-Trapezblech als Fassadenbekleidung` (`bg_reuse_aluminium_fassade_elys_trapezoidal_sheet`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Erhaltene Betonhallen / Tragstruktur` (`bg_retained_mehrere_mehrere_elys_concrete_halls`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Gitterroste / Brüstungsgitter und Garagentor` (`bg_reuse_stahl_mehrere_elys_gratings_and_garage_door`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Reuse-Fassade als Holzrahmen-Bauteilsystem` (`bg_reuse_holz_fassade_elys_reuse_system`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Steinwolledämmung aus Restposten / Abfallprodukten` (`bg_reuse_daemmstoff_mehrere_elys_stone_wool_restock_insulation`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Eigenbestand` (`bweg_eigenbestand`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Informelles_Netzwerk` (`bweg_informelles_netzwerk`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Lagerung` (`log_lagerung`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Aufbereitung` (`phase_aufbereitung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Dokumentation` (`phase_dokumentation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Lager` (`rq_lager`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Produktionsueberschuss` (`rq_produktionsueberschuss`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Adaptives_ReUse` (`wva_adaptives_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Bestandserhalt` (`wva_bestandserhalt`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Upcycling` (`wva_upcycling`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Gewaehrleistung` (`h_gewaehrleistung`)
- Project -> `HAT_HUERDE` -> Huerde `Heterogenitaet_Chargen` (`h_heterogenitaet_chargen`)
- Project -> `HAT_HUERDE` -> Huerde `Materialqualitaet_Unklar` (`h_materialqualitaet_unklar`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Verfuegbarkeitsproblem` (`h_verfuegbarkeitsproblem`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Asbest` (`s_asbest`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `KMF — Künstliche Mineralfasern (alte Mineralwolle vor 1996/2000)` (`s_kmf`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Schweiz × Beton reuse rule` (`rr_ch_beton`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Schweiz × Holz reuse rule` (`rr_ch_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Schweiz × Stahl reuse rule` (`rr_ch_stahl`) -> `RELEVANT_FOR` -> Project

### 29. ETH Circular Construction student reuse project

Project ID: `p_eth_circular_construction_student_reuse_project`
Reuse-workflow edges: `1`

#### Actors and Delivery Chain

**STUB_PROJECT_LINK**
- Akteur `Catherine De Wolf` (`catherine_de_wolf`) -> `STUB_PROJECT_LINK` -> Project

### 30. ETH Circular Construction — student reuse demonstrator/news

Project ID: `p_eth_circular_construction_student_reuse`
Reuse-workflow edges: `2`

#### Actors and Delivery Chain

**STUB_PROJECT_LINK**
- Akteur `Fabio Gramazio` (`fabio_gramazio`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Matthias Kohler` (`matthias_kohler`) -> `STUB_PROJECT_LINK` -> Project

### 31. Europa Building Brussels / Résidence Palace – Europa

Project ID: `p_europa_building_brussels`
Reuse-workflow edges: `60`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Belgian Buildings Agency / Regie der Gebouwen` (`belgian_buildings_agency`) -> `BETEILIGT_AN` -> Project
- Akteur `Bopro` (`bopro`) -> `BETEILIGT_AN` -> Project
- Akteur `Buro Happold` (`buro_happold`) -> `BETEILIGT_AN` -> Project
- Akteur `Jan De Nul` (`jan_de_nul`) -> `BETEILIGT_AN` -> Project
- Akteur `Philippe Samyn and Partners` (`philippe_samyn_and_partners`) -> `BETEILIGT_AN` -> Project
- Akteur `Studio Valle Progettazioni` (`studio_valle_progettazioni`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `EU-weite Renovierungs- und Abbruchquellen für Holzfensterrahmen` (`bw_eu_window_donor_sources`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Europa Building Brussels` (`bw_europa_building_brussels`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Residence Palace Block A` (`bw_residence_palace_block_a`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umnutzung` (`bai_umnutzung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Belgien` (`land_belgien`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Brüssel` (`stadt_bruessel`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `EU-weite Renovierungs- und Abbruchquellen für Holzfensterrahmen` (`bw_eu_window_donor_sources`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Europa Building Brussels` (`bw_europa_building_brussels`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Residence Palace Block A` (`bw_residence_palace_block_a`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `3.750 restaurierte Holzfensterrahmen als Patchwork-Fassade` (`bg_reuse_holz_mehrere_europa_restored_window_frames`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Erhaltene Teile des Residence Palace Block A` (`bg_retained_mehrere_mehrere_europa_residence_palace_parts`)

#### Reuse Strategy and Process

**HAT_AUFBEREITUNG**
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `Aluminiumfenster — Beschläge + Dichtungen tauschen` (`av_aluminiumfenster_beschlag_dichtung`)
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `Fenster-Refurbishment (Beschläge + Dichtungen)` (`av_fenster_refurbishment`)
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `Glas-Reinigung + Entkitten` (`av_glas_reinigung_entkitten`)
**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Informelles_Netzwerk` (`bweg_informelles_netzwerk`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transport` (`log_transport`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Aufbereitung` (`phase_aufbereitung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Adaptives_ReUse` (`wva_adaptives_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Bestandserhalt` (`wva_bestandserhalt`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Dauerhaftigkeit_Restlebensdauer` (`h_dauerhaftigkeit_restlebensdauer`)
- Project -> `HAT_HUERDE` -> Huerde `Heterogenitaet_Chargen` (`h_heterogenitaet_chargen`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Witterung_Feuchte` (`h_witterung_feuchte`)
**HAT_PRUEFUNG**
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_beschlagpruefung`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_dichtheit`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_dichtungszustand`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_funktionspruefung`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_glasbruch_sichtpruefung`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_schadstoffanalyse_kitt`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_ug_wert`
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Asbest` (`s_asbest`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Belgien × Beton reuse rule` (`rr_be_beton`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Belgien × Holz reuse rule` (`rr_be_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Belgien × Naturstein reuse rule` (`rr_be_naturstein`) -> `RELEVANT_FOR` -> Project

### 32. FCRBE — Facilitating the Circulation of Reclaimed Building Elements

Project ID: `p_fcrbe`
Reuse-workflow edges: `2`

#### Actors and Delivery Chain

**STUB_PROJECT_LINK**
- Akteur `Hugo Topalov` (`hugo_topalov`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Sarah Westerfeld` (`sarah_westerfeld`) -> `STUB_PROJECT_LINK` -> Project

### 33. Ferme du Rail Paris

Project ID: `p_ferme_du_rail_paris`
Reuse-workflow edges: `64`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Albert & Compagnie` (`albert_et_compagnie`) -> `BETEILIGT_AN` -> Project
- Akteur `Bellastock — French reuse architecture/research collective (FCRBE partner)` (`bellastock`) -> `BETEILIGT_AN` -> Project
- Akteur `Grand Huit` (`grand_huit`) -> `BETEILIGT_AN` -> Project
- Akteur `Mélanie Devret` (`melanie_devret`) -> `BETEILIGT_AN` -> Project
- Akteur `Pouget Consultants` (`pouget_consultants`) -> `BETEILIGT_AN` -> Project
- Akteur `Réhabail` (`rehabail`) -> `BETEILIGT_AN` -> Project
- Akteur `Scoping` (`scoping`) -> `BETEILIGT_AN` -> Project
- Akteur `Travail & Vie` (`travail_et_vie`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Clara Simay` (`clara_simay`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Grand Huit` (`grand_huit`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Julia Turpin` (`julia_turpin`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `La Ferme du Rail Neubauensemble` (`bw_ferme_du_rail_receiver`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Mischnutzung` (`nut_mischnutzung`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Sozialbau` (`nut_sozialbau`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Frankreich` (`land_frankreich`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Paris` (`stadt_paris`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `La Ferme du Rail Neubauensemble` (`bw_ferme_du_rail_receiver`)
- Project -> `NUTZT_BAUWERK` -> Materialdepot `Aggregierte Pariser und regionale Reuse-Gisements fuer La Ferme du Rail` (`bw_paris_regional_donor_sources_ferme_du_rail`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Bitumen- und Betonblöcke als Außenwege` (`bg_reuse_mehrere_boden_ferme_bitumen_concrete_blocks_paths`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Fliesen / Fayence als Badwandbelag` (`bg_reuse_keramik_mehrere_ferme_tiles_bathroom_walls`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Granitbordsteine als Stützmauer` (`bg_reuse_naturstein_mehrere_ferme_granite_kerbstones_retaining_wall`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Holzfensterrahmen als Akroterie, Pflanztröge und Geländer` (`bg_reuse_holz_mehrere_ferme_window_frames_roof_terrace`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Holzfensterrahmen als Holzpflaster / Parkett bois de bout` (`bg_reuse_holz_mehrere_ferme_window_frames_endgrain_floor`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Stein- und Bürofußbodenplatten als Beläge/Füllplatten` (`bg_reuse_naturstein_boden_ferme_slabs_fill`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Textile / rezyklierte Fasern als Sonnenschutzstores` (`bg_reuse_textil_mehrere_ferme_textile_sun_shading`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendetes Holz für feste Schränke` (`bg_reuse_holz_ausbau_ferme_fixed_cupboards`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Informelles_Netzwerk` (`bweg_informelles_netzwerk`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Lagerung` (`log_lagerung`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transport` (`log_transport`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Regional geografisches Matching (50–500 km)` (`mq_geographic_regional`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Aufbereitung` (`phase_aufbereitung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Planung` (`phase_planung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Baustelle` (`rq_baustelle`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Produktionsueberschuss` (`rq_produktionsueberschuss`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Upcycling` (`wva_upcycling`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Aufbereitungsaufwand` (`h_aufbereitungsaufwand`)
- Project -> `HAT_HUERDE` -> Huerde `Fehlende_Lagerflaeche` (`h_fehlende_lagerflaeche`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Terminunsicherheit` (`h_terminunsicherheit`)
- Project -> `HAT_HUERDE` -> Huerde `Witterung_Feuchte` (`h_witterung_feuchte`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Asbest` (`s_asbest`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Wettbewerb` (`prog_wettbewerb`)

### 34. gjG House, Gentbrugge / Ghent

Project ID: `p_gjg_house_gentbrugge`
Reuse-workflow edges: `36`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `BLAF Architecten` (`blaf_architecten`) -> `BETEILIGT_AN` -> Project
- Akteur `Barbara Oelbrandt` (`barbara_oelbrandt`) -> `BETEILIGT_AN` -> Project
- Akteur `G-build` (`g_build`) -> `BETEILIGT_AN` -> Project
- Akteur `Tecclem` (`tecclem`) -> `BETEILIGT_AN` -> Project
- Akteur `Vlieghe` (`vlieghe`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `gjG House` (`bw_gjg_house_receiver`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Belgien` (`land_belgien`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Gentbrugge / Ghent` (`stadt_gentbrugge`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `gjG House` (`bw_gjg_house_receiver`)
- Project -> `NUTZT_BAUWERK` -> Materialdepot `unbekannte Donorquellen der wiederverwendeten Ziegel` (`bw_unknown_brick_donor_sources_gjg`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Gekrümmte strukturell autonome Außenmauer / Ziegelschale` (`bg_reuse_ziegel_mehrere_gjg_curved_shell`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Stahl-/Holz-Infill-Struktur` (`bg_reuse_mehrere_mehrere_gjg_steel_wood_infill_structure`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Informelles_Netzwerk` (`bweg_informelles_netzwerk`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Materialverfuegbarkeit` (`log_materialverfuegbarkeit`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Planung` (`phase_planung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Unbekannt` (`rq_unbekannt`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Anschlussproblem` (`h_anschlussproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Materialqualitaet_Unklar` (`h_materialqualitaet_unklar`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Belgien × Holz reuse rule` (`rr_be_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Belgien × Stahl reuse rule` (`rr_be_stahl`) -> `RELEVANT_FOR` -> Project

### 35. Granby Workshop Liverpool — Assemble + Granby 4 Streets CLT (recycled terrazzo + architectural ceramics CIC)

Project ID: `p_granby_workshop`
Reuse-workflow edges: `18`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Assemble` (`assemble`) -> `BETEILIGT_AN` -> Project
- Akteur `Granby 4 Streets CLT — community land trust collaborator` (`granby_4_streets_clt`) -> `BETEILIGT_AN` -> Project
- Akteur `Granby Workshop CIC — operator / manufacturer` (`granby_workshop_cic`) -> `BETEILIGT_AN` -> Project
- Akteur `Will Shannon — collaborator on Granby Rock terrazzo development` (`will_shannon`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Lewis Jones` (`lewis_jones`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Vereinigtes Königreich` (`land_vereinigtes_koenigreich`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Liverpool` (`stadt_liverpool`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Granby Workshop CIC Liverpool — recycled terrazzo + architectural ceramics manufacturer` (`bw_granby_workshop_liverpool`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Granby Workshop — Brick & Slate Terrazzo (recycled brick + roofing slate as aggregate, BS 5385-5:2009)` (`bg_reuse_ziegel_boden_granby_brick_slate_terrazzo`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Granby Workshop — Granby Rock recycled terrazzo (broken bricks + roofing slates + skip waste → terrazzo aggregate)` (`bg_reuse_mehrere_boden_granby_rock_terrazzo`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Granby Workshop — bespoke waste-stream terrazzo mixes (client-supplied materials or workshop materials)` (`bg_reuse_mehrere_boden_granby_bespoke_waste`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Granby Workshop — first products (bathroom tiles, door handles, fireplaces) made in Granby for renovated houses` (`bg_reuse_glas_keramik_ausbau_granby_first_house_products`)

#### Reuse Strategy and Process

**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Heterogenitaet_Chargen` (`h_heterogenitaet_chargen`)
- Project -> `HAT_HUERDE` -> Huerde `Mengenunsicherheit` (`h_mengenunsicherheit`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Geschaeftsmodell` (`wi_geschaeftsmodell`)
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Preisbildung` (`wi_preisbildung`)

### 36. Grande Halle de Colombelles / Le WIP

Project ID: `p_grande_halle_de_colombelles`
Reuse-workflow edges: `67`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Albert & Co` (`albert_and_co`) -> `BETEILIGT_AN` -> Project
- Akteur `Construire` (`construire`) -> `BETEILIGT_AN` -> Project
- Akteur `Encore Heureux` (`encore_heureux`) -> `BETEILIGT_AN` -> Project
- Akteur `Le WIP` (`le_wip`) -> `BETEILIGT_AN` -> Project
- Akteur `Ligne B.E.` (`ligne_be`) -> `BETEILIGT_AN` -> Project
- Akteur `Normandie Aménagement` (`normandie_amenagement`) -> `BETEILIGT_AN` -> Project
- Akteur `Stéphanie Paly` (`stephanie_paly`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Grande Halle de Colombelles / ehemalige SMN-Werkstatt` (`bw_grande_halle_receiver`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Grande Halle de Colombelles / ehemalige SMN-Werkstatt` (`bw_grande_halle_receiver`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Regionale Rückbau- und Sanierungsbaustellen um Caen / Colombelles` (`bw_colombelles_regional_donor_sources`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Sanierung` (`bai_sanierung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umnutzung` (`bai_umnutzung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Mischnutzung` (`nut_mischnutzung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Frankreich` (`land_frankreich`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Colombelles` (`stadt_colombelles`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Grande Halle de Colombelles / ehemalige SMN-Werkstatt` (`bw_grande_halle_receiver`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Regionale Rückbau- und Sanierungsbaustellen um Caen / Colombelles` (`bw_colombelles_regional_donor_sources`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Erhaltene Bestand-Betonstruktur der Halle` (`bg_retained_mehrere_mehrere_grande_halle_concrete_structure`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Holzpfetten / Holzstücke als Balkon-, Treppen- oder Geländerbauteile` (`bg_reuse_holz_mehrere_grande_halle_purlins_access_parts`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Metallträger / poutres métalliques, unklarer Wiedereinbau` (`bg_reuse_stahl_traeger_grande_halle_metal`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Außenschreinerei / Fenster` (`bg_reuse_mehrere_mehrere_grande_halle_external_window_joinery`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Fliesen / Fayence` (`bg_reuse_keramik_mehrere_grande_halle_tiles_faience`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Mineralwolle-Dämmung` (`bg_reuse_daemmstoff_daemmung_grande_halle_mineral_wool`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Radiatoren` (`bg_reuse_mehrere_technik_grande_halle_radiators`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Sanitärobjekte` (`bg_reuse_mehrere_technik_grande_halle_sanitary_objects`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Türen und Brandschutztüren` (`bg_reuse_holz_tuer_grande_halle_fire`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Ausschreibung` (`bweg_ausschreibung`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Lagerung` (`log_lagerung`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
- Project -> `HAT_LOGISTIK` -> Logistik `Zwischenlagerung` (`log_zwischenlagerung`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Bauteilkatalogisierung` (`meth_bauteilkatalogisierung`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Ausschreibung` (`meth_reuse_ausschreibung`)
- Project -> `HAT_METHODE` -> Methode `Zirkulaere_Ausschreibung` (`meth_zirkulaere_ausschreibung`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Aufbereitung` (`phase_aufbereitung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Planung` (`phase_planung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Baustelle` (`rq_baustelle`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Adaptives_ReUse` (`wva_adaptives_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Aufbereitungsaufwand` (`h_aufbereitungsaufwand`)
- Project -> `HAT_HUERDE` -> Huerde `Ausschreibungsproblem` (`h_ausschreibungsproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Fehlende_Lagerflaeche` (`h_fehlende_lagerflaeche`)
- Project -> `HAT_HUERDE` -> Huerde `Gewaehrleistung` (`h_gewaehrleistung`)
- Project -> `HAT_HUERDE` -> Huerde `Haftung` (`h_haftung`)
- Project -> `HAT_HUERDE` -> Huerde `Mengenunsicherheit` (`h_mengenunsicherheit`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Asbest` (`s_asbest`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `KMF — Künstliche Mineralfasern (alte Mineralwolle vor 1996/2000)` (`s_kmf`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Versteckte Kosten (Lagerung/Prüfung/Logistik)` (`wi_hidden_costs_lagerung_pruefung`)
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `FCRBE — Facilitating the Circulation of Reclaimed Building Elements` (`prog_fcrbe`)
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Interreg_North_West_Europe` (`prog_interreg_nwe`)

### 37. Grubenstrasse 29 / Werkhof 29, Zürich

Project ID: `p_grubenstrasse_29_werkhof_29_zuerich`
Reuse-workflow edges: `68`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Bauteilladen Winterthur` (`bauteilladen_winterthur`) -> `BETEILIGT_AN` -> Project
- Akteur `Modissa Immobilien AG` (`modissa_immobilien_ag`) -> `BETEILIGT_AN` -> Project
- Akteur `Tschudin Rückbau und Demontagen GmbH` (`tschudin_rueckbau_demontagen`) -> `BETEILIGT_AN` -> Project
- Akteur `Zirkular` (`zirkular`) -> `BETEILIGT_AN` -> Project
- Akteur `baubüro in situ` (`baubuero_in_situ`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Externe Rückbauprojekte und Bauteilquellen für Werkhof 29` (`bw_grubenstrasse_external_donor_sources`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Werkhof 29 / ehemaliges Gewerbe- und Schlossereigebäude` (`bw_werkhof_29_receiver`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Werkhof 29 / ehemaliges Gewerbe- und Schlossereigebäude` (`bw_werkhof_29_receiver`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Aufstockung` (`bai_aufstockung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Sanierung` (`bai_sanierung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Mischnutzung` (`nut_mischnutzung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Schweiz` (`land_schweiz`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Zürich` (`stadt_zuerich`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Externe Rückbauprojekte und Bauteilquellen für Werkhof 29` (`bw_grubenstrasse_external_donor_sources`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Werkhof 29 / ehemaliges Gewerbe- und Schlossereigebäude` (`bw_werkhof_29_receiver`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Blaue Stahlblechfassade` (`bg_reuse_stahl_fassade_grubenstrasse_blue_sheets`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Erhalt und Ertüchtigung des Bestandsgebäudes` (`bg_retained_mehrere_mehrere_grubenstrasse_existing_building`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Stahlbauteile für Laubengänge, Treppentürme und Gitterroste` (`bg_reuse_stahl_mehrere_grubenstrasse_access_structures`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Außentreppe` (`bg_reuse_stahl_treppe_grubenstrasse_outer`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Dachbleche` (`bg_reuse_mehrere_dach_grubenstrasse_sheets`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Dämmplatten` (`bg_reuse_daemmstoff_daemmung_grubenstrasse_plates`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Fenster und Türen` (`bg_reuse_mehrere_mehrere_grubenstrasse_windows_doors`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Geländer` (`bg_reuse_stahl_gelaender_grubenstrasse_railings`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Heizkörper und Sanitärapparate` (`bg_reuse_mehrere_technik_grubenstrasse_radiators_sanitary`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Bauteilboerse` (`bweg_bauteilboerse`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Direktvermittlung` (`bweg_direktvermittlung`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialverfuegbarkeit` (`log_materialverfuegbarkeit`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transport` (`log_transport`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Bauteilkatalogisierung` (`meth_bauteilkatalogisierung`)
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Planung` (`phase_planung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Bauteilboerse` (`rq_bauteilboerse`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Lager` (`rq_lager`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Produktionsueberschuss` (`rq_produktionsueberschuss`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Adaptives_ReUse` (`wva_adaptives_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Weiterbauen_im_Bestand` (`wva_weiterbauen_im_bestand`)

#### Risk, Checks, and Constraints

**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Korrosion` (`def_korrosion`)
**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Entwurfsbindung` (`h_entwurfsbindung`)
- Project -> `HAT_HUERDE` -> Huerde `Gewaehrleistung` (`h_gewaehrleistung`)
- Project -> `HAT_HUERDE` -> Huerde `Materialqualitaet_Unklar` (`h_materialqualitaet_unklar`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Verfuegbarkeitsproblem` (`h_verfuegbarkeitsproblem`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Asbest` (`s_asbest`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `KMF — Künstliche Mineralfasern (alte Mineralwolle vor 1996/2000)` (`s_kmf`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Schweiz × Beton reuse rule` (`rr_ch_beton`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Schweiz × Holz reuse rule` (`rr_ch_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Schweiz × Stahl reuse rule` (`rr_ch_stahl`) -> `RELEVANT_FOR` -> Project

### 38. Hastings Pier Visitor Centre / reclaimed timber cladding

Project ID: `p_hastings_pier_visitor_centre`
Reuse-workflow edges: `57`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Hastings & Bexhill Wood Recycling` (`hastings_bexhill_wood_recycling`) -> `BETEILIGT_AN` -> Project
- Akteur `Hastings Pier Charity` (`hastings_pier_charity`) -> `BETEILIGT_AN` -> Project
- Akteur `KLH` (`klh`) -> `BETEILIGT_AN` -> Project
- Akteur `National Lottery Heritage Fund` (`national_lottery_heritage_fund`) -> `BETEILIGT_AN` -> Project
- Akteur `PT Projects` (`pt_projects`) -> `BETEILIGT_AN` -> Project
- Akteur `Ramboll` (`ramboll`) -> `BETEILIGT_AN` -> Project
- Akteur `dRMM Architects` (`drmm_architects`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Brandschaden / alte Pier-Deckflächen Hastings Pier` (`bw_hastings_pier_fire_damaged_deck`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Erhaltene/restaurierte Hastings Pier Gesamtstruktur` (`bw_hastings_pier_retained_heritage_context`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Erhaltene/restaurierte Hastings Pier Gesamtstruktur` (`bw_hastings_pier_retained_heritage_context`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Hastings Pier Visitor Centre` (`bw_hastings_pier_visitor_centre`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Sanierung` (`bai_sanierung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Wiederaufbau` (`bai_wiederaufbau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Infrastruktur` (`nut_infrastruktur`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Vereinigtes Königreich` (`land_vereinigtes_koenigreich`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Hastings` (`stadt_hastings`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Brandschaden / alte Pier-Deckflächen Hastings Pier` (`bw_hastings_pier_fire_damaged_deck`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Erhaltene/restaurierte Hastings Pier Gesamtstruktur` (`bw_hastings_pier_retained_heritage_context`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Hastings Pier Visitor Centre` (`bw_hastings_pier_visitor_centre`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Gespaltene längere Hartholzstücke als Bekleidung von Toiletten / Outbuildings` (`bg_reuse_holz_fassade_hastings_outbuilding_cladding`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Neues CLT-Tragwerk des Visitor Centre` (`bg_reuse_holz_mehrere_hastings_clt_visitor_centre_structure`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Restaurierte Pier-Unterstruktur und viktorianischer Pavillon` (`bg_retained_mehrere_mehrere_hastings_pier_restoration`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete tropische Hartholz-Deckbohlen als Fassadenbekleidung` (`bg_reuse_holz_fassade_hastings_hardwood_cladding`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Eigenbestand` (`bweg_eigenbestand`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Lokale_Wiederverwendung` (`log_lokale_wiederverwendung`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialverfuegbarkeit` (`log_materialverfuegbarkeit`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Aufbereitung` (`phase_aufbereitung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Baustelle` (`rq_baustelle`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Adaptives_ReUse` (`wva_adaptives_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Same_Site_ReUse` (`wva_same_site_reuse`)

#### Risk, Checks, and Constraints

**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Brandschaden` (`def_brandschaden`)
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Oberflächenmangel / Verfärbung` (`def_oberflaechenmangel`)
**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Brandschutzkonflikt` (`h_brandschutzkonflikt`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Mengenunsicherheit` (`h_mengenunsicherheit`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Witterung_Feuchte` (`h_witterung_feuchte`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx höher, Subvention/Förderung deckt Mehrkosten` (`wi_capex_hoeher_subvention`)
**RELEVANT_FOR**
- ReuseRule `Vereinigtes Königreich × Holz reuse rule` (`rr_gb_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Vereinigtes Königreich × Stahl reuse rule` (`rr_gb_stahl`) -> `RELEVANT_FOR` -> Project

### 39. Haus HOS / Mehrfamilienhaus Mühlhausen

Project ID: `p_haus_hos_mehrfamilienhaus_muehlhausen`
Reuse-workflow edges: `43`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Architekturbüro Hose` (`architekturbuero_hose`) -> `BETEILIGT_AN` -> Project
- Akteur `BTU Cottbus / Dr. Angelika Mettke` (`btu_cottbus_angelika_mettke`) -> `BETEILIGT_AN` -> Project
- Akteur `Privater Bauherr Haus HOS` (`haus_hos_privater_bauherr`) -> `BETEILIGT_AN` -> Project
- Akteur `Seidl + Seidl Architekten` (`seidl_seidl_architekten`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Haus HOS Mehrfamilienhaus Mühlhausen` (`bw_haus_hos_receiver`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Rückbaustelle / Plattenbau in Leinefelde` (`bw_leinefelde_plattenbau_donor`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Deutschland` (`land_deutschland`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Leinefelde` (`stadt_leinefelde`)
- Project -> `LIEGT_IN_STADT` -> Stadt `Mühlhausen, Thüringen` (`stadt_muehlhausen_thueringen`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Haus HOS Mehrfamilienhaus Mühlhausen` (`bw_haus_hos_receiver`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Rückbaustelle / Plattenbau in Leinefelde` (`bw_leinefelde_plattenbau_donor`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Stahlbeton-Deckenelemente` (`bg_reuse_stahlbeton_mehrere_haus_hos_floor_elements`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Stahlbeton-Treppen / Podeste` (`bg_reuse_stahlbeton_treppe_haus_hos`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Stahlbeton-Wandelemente` (`bg_reuse_stahlbeton_wand_haus_hos_elements`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Direktvermittlung` (`bweg_direktvermittlung`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transport` (`log_transport`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transportdistanz` (`log_transportdistanz`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Regional geografisches Matching (50–500 km)` (`mq_geographic_regional`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Bauteilkatalogisierung` (`meth_bauteilkatalogisierung`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Rueckbau` (`phase_rueckbau`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Transport` (`phase_transport`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Remanufacturing` (`wva_remanufacturing`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Akzeptanzproblem` (`h_akzeptanzproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Anschlussproblem` (`h_anschlussproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Entwurfsbindung` (`h_entwurfsbindung`)
- Project -> `HAT_HUERDE` -> Huerde `Gewaehrleistung` (`h_gewaehrleistung`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Deutschland × Beton reuse rule` (`rr_de_beton`) -> `RELEVANT_FOR` -> Project
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Pilotprojekt` (`prog_pilotprojekt`)

### 40. Holbein Gardens, London

Project ID: `p_holbein_gardens_london`
Reuse-workflow edges: `63`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Barr Gazetas` (`barr_gazetas`) -> `BETEILIGT_AN` -> Project
- Akteur `Blenheim House` (`blenheim_house`) -> `BETEILIGT_AN` -> Project
- Akteur `Cleveland Steel & Tubes` (`cleveland_steel_tubes`) -> `BETEILIGT_AN` -> Project
- Akteur `Eurban` (`eurban`) -> `BETEILIGT_AN` -> Project
- Akteur `Grosvenor` (`grosvenor`) -> `BETEILIGT_AN` -> Project
- Akteur `Heyne Tillett Steel / HTS` (`heyne_tillett_steel`) -> `BETEILIGT_AN` -> Project
- Akteur `TFT Consultants` (`tft_consultants`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Cleveland Steel and Tubes reclaimed steel stock` (`bw_cleveland_steel_reclaimed_stock`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Holbein Gardens 1980er Bürogebäude / Workplace Retrofit` (`bw_holbein_gardens_receiver`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Holbein Gardens 1980er Bürogebäude / Workplace Retrofit` (`bw_holbein_gardens_receiver`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Aufstockung` (`bai_aufstockung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Sanierung` (`bai_sanierung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Vereinigtes Königreich` (`land_vereinigtes_koenigreich`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `London` (`stadt_london`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Cleveland Steel and Tubes reclaimed steel stock` (`bw_cleveland_steel_reclaimed_stock`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Holbein Gardens 1980er Bürogebäude / Workplace Retrofit` (`bw_holbein_gardens_receiver`)
- Project -> `NUTZT_BAUWERK` -> Materialdepot `Grosvenor-Donor-Projekte für Reuse-Stahl` (`bw_holbein_grosvenor_donor_projects`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Erhaltener Betonrahmen und Bestandshülle` (`bg_retained_mehrere_mehrere_holbein_concrete_frame`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Neue CLT-Decken der Erweiterung` (`bg_reuse_holz_decke_holbein_new_clt_floors`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Reclaimed stone / brickwork, Menge und Rolle unklar` (`bg_reuse_ziegel_mehrere_holbein_stone`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Stahlträger und Stahlstützen für die Aufstockung` (`bg_reuse_stahl_mehrere_holbein_structural`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Bauteilboerse` (`bweg_bauteilboerse`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Direktvermittlung` (`bweg_direktvermittlung`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Lagerung` (`log_lagerung`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transport` (`log_transport`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Exakte Spezifikations-Übereinstimmung` (`mq_spec_exact`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Pre_Deconstruction_Audit` (`meth_pre_deconstruction_audit`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Aufbereitung` (`phase_aufbereitung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Pruefung` (`phase_pruefung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Haendler` (`rq_haendler`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Lager` (`rq_lager`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Adaptives_ReUse` (`wva_adaptives_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Weiterbauen_im_Bestand` (`wva_weiterbauen_im_bestand`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Gewaehrleistung` (`h_gewaehrleistung`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Terminunsicherheit` (`h_terminunsicherheit`)
- Project -> `HAT_HUERDE` -> Huerde `Verfuegbarkeitsproblem` (`h_verfuegbarkeitsproblem`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_ZERTIFIZIERUNG**
- Project -> `HAT_ZERTIFIZIERUNG` -> Zertifizierungssystem `BREEAM` (`zbs_breeam`)
- Project -> `HAT_ZERTIFIZIERUNG` -> Zertifizierungssystem `NABERS` (`zbs_nabers`)
- Project -> `HAT_ZERTIFIZIERUNG` -> Zertifizierungssystem `WELL` (`zbs_well`)
**RELEVANT_FOR**
- ReuseRule `Vereinigtes Königreich × Holz reuse rule` (`rr_gb_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Vereinigtes Königreich × Stahl reuse rule` (`rr_gb_stahl`) -> `RELEVANT_FOR` -> Project

### 41. House of Fraser / 318 Oxford Street → TBC.London steel reuse chain

Project ID: `p_house_of_fraser_318_oxford_street_tbc_london_reuse_chain`
Reuse-workflow edges: `74`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Civic Engineers` (`civic_engineers`) -> `BETEILIGT_AN` -> Project
- Akteur `Cleveland Steel & Tubes` (`cleveland_steel_tubes`) -> `BETEILIGT_AN` -> Project
- Akteur `ECE Architecture` (`ece_architecture`) -> `BETEILIGT_AN` -> Project
- Akteur `FORE Partnership` (`fore_partnership`) -> `BETEILIGT_AN` -> Project
- Akteur `Four Bay Structures` (`four_bay_structures`) -> `BETEILIGT_AN` -> Project
- Akteur `McLaren Construction` (`mclaren_construction`) -> `BETEILIGT_AN` -> Project
- Akteur `Stiff + Trevillion` (`stiff_trevillion`) -> `BETEILIGT_AN` -> Project
- Akteur `Studio PDP` (`studio_pdp`) -> `BETEILIGT_AN` -> Project
- Akteur `Webb Yates Engineers` (`webb_yates_engineers`) -> `BETEILIGT_AN` -> Project
- Akteur `Willmott Dixon` (`willmott_dixon`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `318 Oxford Street / former House of Fraser / The Elephant` (`bw_318_oxford_street_house_of_fraser`)
- Project -> `HAS_BAUWERK` -> Bauwerk `318 Oxford Street / former House of Fraser / The Elephant` (`bw_318_oxford_street_house_of_fraser`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Cleveland Steel and Tubes reclaimed steel stock` (`bw_cleveland_steel_reclaimed_stock`)
- Project -> `HAS_BAUWERK` -> Bauwerk `TBC.London / Tower Bridge Court, 224–226 Tower Bridge Road` (`bw_tbc_london_tower_bridge_court`)
- Project -> `HAS_BAUWERK` -> Bauwerk `TBC.London / Tower Bridge Court, 224–226 Tower Bridge Road` (`bw_tbc_london_tower_bridge_court`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Aufstockung` (`bai_aufstockung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Sanierung` (`bai_sanierung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `In_Bau` (`status_in_bau`)
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Vereinigtes Königreich` (`land_vereinigtes_koenigreich`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `London` (`stadt_london`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `318 Oxford Street / former House of Fraser / The Elephant` (`bw_318_oxford_street_house_of_fraser`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Cleveland Steel and Tubes reclaimed steel stock` (`bw_cleveland_steel_reclaimed_stock`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `TBC.London / Tower Bridge Court, 224–226 Tower Bridge Road` (`bw_tbc_london_tower_bridge_court`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `1930er Stahlträger vom House of Fraser in TBC.London` (`bg_reuse_stahl_mehrere_hof_1930s_beams_to_tbc`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Erhaltener 1990er Betonrahmen TBC` (`bg_retained_mehrere_mehrere_tbc_concrete_frame`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Handrails, fixtures, bricks und demolition materials mit unklarer fester Reuse-Funktion` (`bg_reuse_ziegel_mehrere_tbc_fixtures`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Refabrizierte Stahlstützen aus unteren Geschossen für neue obere Ebenen 318 Oxford Street` (`bg_reuse_stahl_mehrere_hof_self_columns`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Repurposed Cleveland steel für obere Etage TBC` (`bg_reuse_stahl_mehrere_tbc_repurposed_cleveland`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Bauteilboerse` (`bweg_bauteilboerse`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Direktvermittlung` (`bweg_direktvermittlung`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Bauteiltracking` (`log_bauteiltracking`)
- Project -> `HAT_LOGISTIK` -> Logistik `Just_in_Time` (`log_just_in_time`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transport` (`log_transport`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch geplante Beschaffung` (`mq_temporal_planned`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
- Project -> `HAT_METHODE` -> Methode `Pre_Deconstruction_Audit` (`meth_pre_deconstruction_audit`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
- Project -> `HAT_METHODE` -> Methode `Urban_Mining` (`meth_urban_mining`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Aufbereitung` (`phase_aufbereitung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Pruefung` (`phase_pruefung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Rueckbau` (`phase_rueckbau`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Haendler` (`rq_haendler`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Lager` (`rq_lager`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Refurbishment` (`wva_refurbishment`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Urban_Mining` (`wva_urban_mining`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Weiterbauen_im_Bestand` (`wva_weiterbauen_im_bestand`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Anschlussproblem` (`h_anschlussproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Fehlende_Lagerflaeche` (`h_fehlende_lagerflaeche`)
- Project -> `HAT_HUERDE` -> Huerde `Materialqualitaet_Unklar` (`h_materialqualitaet_unklar`)
- Project -> `HAT_HUERDE` -> Huerde `Mengenunsicherheit` (`h_mengenunsicherheit`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Terminunsicherheit` (`h_terminunsicherheit`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**NUTZT_SOFTWARE**
- Project -> `NUTZT_SOFTWARE` -> Software `Qflow` (`software_qflow`)
- Project -> `NUTZT_SOFTWARE` -> Software:Tool `Qflow delivery and waste ticket tracking` (`tool_qflow`)
**RELEVANT_FOR**
- ReuseRule `Vereinigtes Königreich × Holz reuse rule` (`rr_gb_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Vereinigtes Königreich × Stahl reuse rule` (`rr_gb_stahl`) -> `RELEVANT_FOR` -> Project

### 42. Härmälänranta / A-Kruunu ReCreate mini-pilot Tampere

Project ID: `p_harmalanranta_a_kruunu_recreate_mini_pilot_tampere`
Reuse-workflow edges: `46`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `A-Kruunu` (`kruunu`) -> `BETEILIGT_AN` -> Project
- Akteur `Consolis Parma` (`consolis_parma`) -> `BETEILIGT_AN` -> Project
- Akteur `LIIKE Oy Arkkitehtistudio` (`liike_oy_arkkitehtistudio`) -> `BETEILIGT_AN` -> Project
- Akteur `Ramboll Finland` (`ramboll_finland`) -> `BETEILIGT_AN` -> Project
- Akteur `Skanska Finland` (`skanska_finland`) -> `BETEILIGT_AN` -> Project
- Akteur `Tampere University / Satu Huuhka` (`tampere_university_satu_huuhka`) -> `BETEILIGT_AN` -> Project
- Akteur `Umacon` (`umacon`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Angelika Mettke` (`angelika_mettke`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Patrick Teuffel` (`patrick_teuffel`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Satu Huuhka` (`satu_huuhka`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `1980er Bürogebäude im Zentrum von Tampere` (`bw_tampere_1980s_office_donor`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Härmälänrannan Ernst` (`bw_harmalanrannan_ernst_receiver`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Finnland` (`land_finnland`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Tampere` (`stadt_tampere`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `1980er Bürogebäude im Zentrum von Tampere` (`bw_tampere_1980s_office_donor`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Härmälänrannan Ernst` (`bw_harmalanrannan_ernst_receiver`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Luftschutzraum-Deckenbereich als Einbauort` (`bg_reuse_mehrere_decke_harmalanranta_shelter_deck_zone`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Hohlkörperdecken / hollow-core slabs` (`bg_reuse_stahlbeton_decke_harmalanranta_hollow_core_slabs`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Direktvermittlung` (`bweg_direktvermittlung`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Bauteiltracking` (`log_bauteiltracking`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transportdistanz` (`log_transportdistanz`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Bauteilkatalogisierung` (`meth_bauteilkatalogisierung`)
- Project -> `HAT_METHODE` -> Methode `Pre_Deconstruction_Audit` (`meth_pre_deconstruction_audit`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Aufbereitung` (`phase_aufbereitung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Pruefung` (`phase_pruefung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Rueckbau` (`phase_rueckbau`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Transport` (`phase_transport`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Bruch_Beschaedigungsrisiko` (`h_bruch_beschaedigungsrisiko`)
- Project -> `HAT_HUERDE` -> Huerde `Fehlende_Standardisierung` (`h_fehlende_standardisierung`)
- Project -> `HAT_HUERDE` -> Huerde `Kompatibilitaetsproblem` (`h_kompatibilitaetsproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Toleranzen` (`h_toleranzen`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)

#### Tools, Programmes, and Frameworks

**ERHALT_FOERDERUNG_DURCH**
- Project -> `ERHALT_FOERDERUNG_DURCH` -> Programm `Horizon 2020 (EU Forschungsförderung)` (`prog_horizon_2020`)
**RELEVANT_FOR**
- ReuseRule `Finnland × Beton / hollow-core slabs reuse rule` (`rr_fi_beton_hollow_core_slabs`) -> `RELEVANT_FOR` -> Project
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `ReCreate` (`prog_recreate`)
- Project -> `TEIL_VON_PROGRAMM` -> Programm `ReCreate Finnish cluster mini-pilot` (`prog_recreate_local`)

### 43. Impact Hub Berlin / CRCLR Fit-out

Project ID: `p_impact_hub_berlin_crclr_fitout`
Reuse-workflow edges: `68`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Die Zusammenarbeiter` (`die_zusammenarbeiter`) -> `BETEILIGT_AN` -> Project
- Akteur `Impact Hub Berlin` (`impact_hub_berlin`) -> `BETEILIGT_AN` -> Project
- Akteur `LXSY Architektur` (`lxsy_architektur`) -> `BETEILIGT_AN` -> Project
- Akteur `TRNSFRM eG` (`trnsfrm_eg`) -> `BETEILIGT_AN` -> Project
- Akteur `ZRS Ingenieure` (`zrs_ingenieure`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Kim Le Roux` (`kim_le_roux`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Margit Sichrovsky` (`margit_sichrovsky`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Wiebke Ahues` (`wiebke_ahues`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Impact Hub Berlin Innenausbau im CRCLR House` (`bw_impact_hub_fitout_receiver`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Fit_out` (`bai_fit_out`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Sanierung` (`bai_sanierung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umnutzung` (`bai_umnutzung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Deutschland` (`land_deutschland`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Berlin` (`stadt_berlin`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `CRCLR House / ehemalige Kindl-Brauerei` (`bw_crclr_house_existing_context`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Impact Hub Berlin Innenausbau im CRCLR House` (`bw_impact_hub_fitout_receiver`)
- Project -> `NUTZT_BAUWERK` -> Materialdepot `Aggregierte Donorquellen: Boros/Berghain-Ausstellung, andere Baustellen, Tischlereireste` (`bw_berlin_fitout_donor_sources`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Holzgalerie / zweite Ebene, Wiederverwendung nicht belegt` (`bg_reuse_holz_mehrere_impact_gallery`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Holzlatten aus Tischlereiresten für Telefonboxen` (`bg_reuse_holz_mehrere_impact_offcuts_phone_booths`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Recycelte Filzpaneele für Akustik in Telefonboxen` (`bg_reuse_textil_mehrere_impact_recycled_felt_panels`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Red MDF boards als feste Empfangs-/Treffpunktzone` (`bg_reuse_mdf_ausbau_impact_red_mdf_reception`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Schwarze MDF-Platten als Schranktüren und Wandpaneele` (`bg_reuse_mdf_mehrere_impact_black_mdf_panels`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Türen, Fenster und Sanitär im CRCLR-Gesamtprojekt mit unscharfer Fit-out-Zuordnung` (`bg_reuse_mehrere_mehrere_impact_crclr_doors_windows_sanitary`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Ziegel im Empfang / Treffpunkt` (`bg_reuse_ziegel_mehrere_impact_reception`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Bauteilboerse` (`bweg_bauteilboerse`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Digitale_Plattform` (`bweg_digitale_plattform`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Informelles_Netzwerk` (`bweg_informelles_netzwerk`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Lagerung` (`log_lagerung`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialverfuegbarkeit` (`log_materialverfuegbarkeit`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Bauteilkatalogisierung` (`meth_bauteilkatalogisierung`)
- Project -> `HAT_METHODE` -> Methode `Design_for_Disassembly` (`meth_design_for_disassembly`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
- Project -> `HAT_METHODE` -> Methode `Reversibilitaet` (`meth_reversibilitaet`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Aufbereitung` (`phase_aufbereitung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Dokumentation` (`phase_dokumentation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Lagerung` (`phase_lagerung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Baustelle` (`rq_baustelle`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Bauteilboerse` (`rq_bauteilboerse`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Produktionsueberschuss` (`rq_produktionsueberschuss`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Design_for_Disassembly` (`wva_design_for_disassembly`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Recycling` (`wva_recycling`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Upcycling` (`wva_upcycling`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Brandschutzkonflikt` (`h_brandschutzkonflikt`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Gewaehrleistung` (`h_gewaehrleistung`)
- Project -> `HAT_HUERDE` -> Huerde `Mengenunsicherheit` (`h_mengenunsicherheit`)
- Project -> `HAT_HUERDE` -> Huerde `Verfuegbarkeitsproblem` (`h_verfuegbarkeitsproblem`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**NUTZT_SOFTWARE**
- Project -> `NUTZT_SOFTWARE` -> Software `Concular` (`software_concular`)
- Project -> `NUTZT_SOFTWARE` -> Software `Restado` (`software_restado`)
**RELEVANT_FOR**
- ReuseRule `Deutschland × Holz reuse rule` (`rr_de_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Deutschland × Stahl reuse rule` (`rr_de_stahl`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Deutschland × Ziegel reuse rule` (`rr_de_ziegel`) -> `RELEVANT_FOR` -> Project

### 44. Institut de Botanique de l’ULg, Liège

Project ID: `p_institut_de_botanique_ulg_liege`
Reuse-workflow edges: `27`

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Institut de Botanique de l’Université de Liège` (`bw_institut_botanique_ulg`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Institut de Botanique de l’Université de Liège` (`bw_institut_botanique_ulg`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Sanierung` (`bai_sanierung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Schule_Bildung` (`nut_schule_bildung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Belgien` (`land_belgien`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Liège / Lüttich` (`stadt_liege`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Institut de Botanique de l’Université de Liège` (`bw_institut_botanique_ulg`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Erhaltene Hauptstruktur des Bestandsgebäudes` (`bg_retained_mehrere_mehrere_botanique_main_structure`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete / rückgewonnene Holzfassade` (`bg_reuse_holz_fassade_botanique`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Weiterbauen_im_Bestand` (`wva_weiterbauen_im_bestand`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Brandschutzkonflikt` (`h_brandschutzkonflikt`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Materialqualitaet_Unklar` (`h_materialqualitaet_unklar`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Witterung_Feuchte` (`h_witterung_feuchte`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Belgien × Beton reuse rule` (`rr_be_beton`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Belgien × Holz reuse rule` (`rr_be_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Belgien × Stahl reuse rule` (`rr_be_stahl`) -> `RELEVANT_FOR` -> Project

### 45. Interreg NWE FCRBE

Project ID: `p_interreg_nwe_fcrbe`
Reuse-workflow edges: `1`

#### Actors and Delivery Chain

**STUB_PROJECT_LINK**
- Akteur `Michaël Ghyoot` (`michael_ghyoot`) -> `STUB_PROJECT_LINK` -> Project

### 46. Jeugdkliniek Ithaka / Emergis Kloetinge

Project ID: `p_jeugdkliniek_ithaka_emergis_kloetinge`
Reuse-workflow edges: `52`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `ABT` (`abt`) -> `BETEILIGT_AN` -> Project
- Akteur `Adviesbureau Lüning` (`adviesbureau_luning`) -> `BETEILIGT_AN` -> Project
- Akteur `Burobas` (`burobas`) -> `BETEILIGT_AN` -> Project
- Akteur `DWT Groep` (`dwt_groep`) -> `BETEILIGT_AN` -> Project
- Akteur `Emergis` (`emergis`) -> `BETEILIGT_AN` -> Project
- Akteur `Paree` (`paree`) -> `BETEILIGT_AN` -> Project
- Akteur `Rijkswaterstaat` (`rijkswaterstaat`) -> `BETEILIGT_AN` -> Project
- Akteur `Rothuizen Architecten / Taco Tuinhof` (`rothuizen_architecten`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Ehemaliges Rijkswaterstaat Districtskantoor Terneuzen` (`bw_rws_districtskantoor_terneuzen`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Erhaltener Emergis-Bestand Kloetinge` (`bw_emergis_bestand_kloetinge`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Erhaltener Emergis-Bestand Kloetinge` (`bw_emergis_bestand_kloetinge`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Kinder- en jeugdkliniek Ithaka / Emergis Kloetinge` (`bw_emergis_ithaka_kloetinge`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Sanierung` (`bai_sanierung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Sozialbau` (`nut_sozialbau`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Niederlande` (`land_niederlande`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Kloetinge` (`stadt_kloetinge`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Ehemaliges Rijkswaterstaat Districtskantoor Terneuzen` (`bw_rws_districtskantoor_terneuzen`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Erhaltener Emergis-Bestand Kloetinge` (`bw_emergis_bestand_kloetinge`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Kinder- en jeugdkliniek Ithaka / Emergis Kloetinge` (`bw_emergis_ithaka_kloetinge`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Azobé-Hartholz-Shingles im dritten Leben` (`bg_reuse_holz_fassade_ithaka_azobe_shingles`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Erhaltener Emergis-Bestand` (`bg_retained_mehrere_mehrere_ithaka_existing_clinic`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Teilweise wiederverwendete technische Bauteile` (`bg_reuse_mehrere_technik_ithaka_tga_beleuchtung_installationen`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Außenkozijnen / Fensterrahmen mit Sonnenschutz` (`bg_reuse_mehrere_mehrere_ithaka_kozijnen_fenster`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Holzfußböden und Straßenklinker` (`bg_reuse_mehrere_boden_ithaka_holzfussboeden_klinker`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Holzträger / houten balken` (`bg_reuse_holz_mehrere_ithaka_holztraeger_balken`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Innentüren mit Hang- und Schließwerk` (`bg_reuse_mehrere_mehrere_ithaka_innentueren_beschlaege`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Bauteilkatalogisierung` (`meth_bauteilkatalogisierung`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Adaptives_ReUse` (`wva_adaptives_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Korrosion` (`def_korrosion`)
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Verformung / Setzung / Verzug` (`def_verformung`)
**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Entwurfsbindung` (`h_entwurfsbindung`)
- Project -> `HAT_HUERDE` -> Huerde `Gewaehrleistung` (`h_gewaehrleistung`)
- Project -> `HAT_HUERDE` -> Huerde `Hygieneanforderung` (`h_hygieneanforderung`)
- Project -> `HAT_HUERDE` -> Huerde `Kompatibilitaetsproblem` (`h_kompatibilitaetsproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Witterung_Feuchte` (`h_witterung_feuchte`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx höher, Subvention/Förderung deckt Mehrkosten` (`wi_capex_hoeher_subvention`)
**RELEVANT_FOR**
- ReuseRule `Niederlande × Beton reuse rule` (`rr_nl_beton`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Niederlande × Holz reuse rule` (`rr_nl_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Niederlande × Stahl reuse rule` (`rr_nl_stahl`) -> `RELEVANT_FOR` -> Project

### 47. Juch-Areal Recyclingzentrum Zürich

Project ID: `p_juch_areal_recyclingzentrum_zuerich`
Reuse-workflow edges: `53`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Entsorgung + Recycling Zürich (ERZ)` (`erz_zuerich`) -> `BETEILIGT_AN` -> Project
- Akteur `Graber Pulver Architekt:innen` (`graber_pulver_architektinnen`) -> `BETEILIGT_AN` -> Project
- Akteur `Weber + Brönnimann AG` (`weber_broennimann`) -> `BETEILIGT_AN` -> Project
- Akteur `Zirkular` (`zirkular`) -> `BETEILIGT_AN` -> Project
- Akteur `manoa Landschaftsarchitekten` (`manoa_landschaftsarchitekten`) -> `BETEILIGT_AN` -> Project
- Stadt `Zürich` (`stadt_zuerich`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Graber Pulver` (`graber_pulver`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Kerstin Müller` (`kerstin_mueller`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Marc Angst` (`marc_angst`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Marco Graber` (`marco_graber`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Pascal Hentschel` (`pascal_hentschel`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Thomas Pulver` (`thomas_pulver`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Zirkular` (`zirkular`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `baubüro in situ` (`baubuero_in_situ`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Ehemalige Recyclinghalle Hagenholz` (`bw_hagenholz_recyclinghalle`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Kerenzerbergtunnel / Sicherheitsstollen` (`bw_kerenzerbergtunnel`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Neues Recyclingzentrum ERZ Juch-Areal` (`bw_juch_areal_recyclingzentrum`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Schellinghalle Rümlang` (`bw_schellinghalle_ruemlang`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Infrastruktur` (`nut_infrastruktur`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Geplant` (`status_geplant`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Schweiz` (`land_schweiz`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Zürich` (`stadt_zuerich`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Ehemalige Recyclinghalle Hagenholz` (`bw_hagenholz_recyclinghalle`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Kerenzerbergtunnel / Sicherheitsstollen` (`bw_kerenzerbergtunnel`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Neues Recyclingzentrum ERZ Juch-Areal` (`bw_juch_areal_recyclingzentrum`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Schellinghalle Rümlang` (`bw_schellinghalle_ruemlang`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Beton-Pilzstützen und Deckenelemente aus Schellinghalle Rümlang` (`bg_reuse_stahlbeton_mehrere_juch_schellinghalle_pilzstuetzen`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Gebrauchte Betonplatten aus dem Kerenzerbergtunnel` (`bg_reuse_beton_mehrere_juch_kerenzerberg_betonplatten`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Geplante 1:1 versetzte Stahlstruktur der Recyclinghalle Hagenholz` (`bg_reuse_stahl_mehrere_juch_hagenholz_stahlstruktur`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Bauteilkatalogisierung` (`meth_bauteilkatalogisierung`)
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Urban_Mining` (`wva_urban_mining`)

#### Risk, Checks, and Constraints

**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Korrosion` (`def_korrosion`)
**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Fehlende_Lagerflaeche` (`h_fehlende_lagerflaeche`)
- Project -> `HAT_HUERDE` -> Huerde `Haftung` (`h_haftung`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Terminunsicherheit` (`h_terminunsicherheit`)
- Project -> `HAT_HUERDE` -> Huerde `Verfuegbarkeitsproblem` (`h_verfuegbarkeitsproblem`)
**HAT_PRUEFUNG**
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `Beton-Bohrkernprüfung` (`pr_bohrkernpruefung_beton`)
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `Eignungspruefung_Baulehm` (`pr_eignungspruefung_baulehm`)
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `Korrosionsprüfung / Restdickenmessung` (`pr_korrosionspruefung`)
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `Zerstörende Prüfung (Sammelkategorie)` (`pr_zerstoerende_pruefung`)
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `Zustandsbewertung` (`pr_zustandsbewertung`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**NUTZT_SOFTWARE**
- Project -> `NUTZT_SOFTWARE` -> Software:Tool `BIM / digitaler Bauteilkatalog` (`tool_bim_bauteilkatalog`)
**RELEVANT_FOR**
- ReuseRule `Schweiz × Beton reuse rule` (`rr_ch_beton`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Schweiz × Stahl reuse rule` (`rr_ch_stahl`) -> `RELEVANT_FOR` -> Project

### 48. Jugendtreff Ingersheim — CLT-Reuse Pilot (Stuttgart 210 first reallab, 2024)

Project ID: `p_jugendtreff_ingersheim`
Reuse-workflow edges: `25`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Faltlhauser Krapf — structural engineer (Jugendtreff Ingersheim)` (`faltlhauser_krapf`) -> `BETEILIGT_AN` -> Project
- Akteur `Gemeinde Ingersheim — Jugendtreff Ingersheim client` (`gemeinde_ingersheim`) -> `BETEILIGT_AN` -> Project
- Akteur `Klingelhöfer Krötsch` (`klingelhoefer_kroetsch`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Jugendtreff Ingersheim — CLT-Reuse Pilot (Stuttgart 210, 2024)` (`bw_jugendtreff_ingersheim`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Stuttgart 21 Hauptbahnhof — donor for one-off CLT concrete formwork (78 elements secured for Stuttgart 210 reallabs)` (`bw_stuttgart21_hauptbahnhof`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Deutschland` (`land_deutschland`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Ingersheim` (`stadt_ingersheim`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Jugendtreff Ingersheim — CLT-Reuse Pilot (Stuttgart 210, 2024)` (`bw_jugendtreff_ingersheim`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Jugendtreff Ingersheim — 12 curved CLT formwork elements as primary structure (FW: formwork→structure)` (`bg_reuse_holz_mehrere_ingersheim_clt_structure`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Jugendtreff Ingersheim — CLT offcuts used for secondary fit-out elements` (`bg_reuse_holz_ausbau_ingersheim_clt_secondary`)

#### Reuse Strategy and Process

**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Urban_Mining` (`meth_urban_mining`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Bauproduktstatus` (`h_bauproduktstatus`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Unkonventionelles_Material` (`h_unkonventionelles_material`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**ERHALT_FOERDERUNG_DURCH**
- Project -> `ERHALT_FOERDERUNG_DURCH` -> Programm `Holzbau-Offensive Baden-Württemberg` (`prog_holzbau_offensive_bw`)
**RELEVANT_FOR**
- ReuseRule `Deutschland × Holz reuse rule` (`rr_de_holz`) -> `RELEVANT_FOR` -> Project
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Stuttgart 210 — weiterdenken, weiterbauen!` (`prog_stuttgart_210`)

### 49. K118 Kopfbau Halle 118 Winterthur

Project ID: `p_k118_kopfbau_halle_118_winterthur`
Reuse-workflow edges: `113`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Josef Kolb AG` (`josef_kolb_ag`) -> `BETEILIGT_AN` -> Project
- Akteur `Oberli Ingenieurbau AG` (`oberli_ingenieurbau`) -> `BETEILIGT_AN` -> Project
- Akteur `Stiftung Abendrot / Vorsorgestiftung Abendrot` (`stiftung_abendrot`) -> `BETEILIGT_AN` -> Project
- Akteur `Wetter AG` (`wetter_ag`) -> `BETEILIGT_AN` -> Project
- Akteur `ZHAW IKE` (`zhaw_ike`) -> `BETEILIGT_AN` -> Project
- Akteur `Zirkular` (`zirkular`) -> `BETEILIGT_AN` -> Project
- Akteur `baubüro in situ` (`baubuero_in_situ`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Barbara Buser` (`barbara_buser`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Benjamin Poignon` (`benjamin_poignon`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Charlotte Bofinger` (`charlotte_bofinger`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Kerstin Müller` (`kerstin_mueller`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Marc Angst` (`marc_angst`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Michel Massmünster` (`michel_massmuenster`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Pascal Hentschel` (`pascal_hentschel`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Zirkular` (`zirkular`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `baubüro in situ` (`baubuero_in_situ`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Bestehende Industriehalle Halle 118` (`bw_halle_118_bestand`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Bestehende Industriehalle Halle 118` (`bw_halle_118_bestand`)
- Project -> `HAS_BAUWERK` -> Bauwerk `ELYS-Projekt Basel / Teilrückbau-Halle` (`bw_elys_basel_donor`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Kopfbau Halle 118 / K.118 Aufstockung` (`bw_k118_halle_118`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Orion-Bürogebäude Zürich` (`bw_orion_zuerich_donor`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Aufstockung` (`bai_aufstockung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Schweiz` (`land_schweiz`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Winterthur` (`stadt_winterthur`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Bestehende Industriehalle Halle 118` (`bw_halle_118_bestand`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `ELYS-Projekt Basel / Teilrückbau-Halle` (`bw_elys_basel_donor`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Kopfbau Halle 118 / K.118 Aufstockung` (`bw_k118_halle_118`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Orion-Bürogebäude Zürich` (`bw_orion_zuerich_donor`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Erhaltene Industriehalle Halle 118 als Sockel` (`bg_retained_mehrere_mehrere_k118_halle_118`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Fenster, Fassadenbleche und EPS-Dämmung` (`bg_reuse_mehrere_mehrere_k118_windows_cladding_insulation`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Naturstein-/Granitplatten, Klinker und Holzplatten` (`bg_reuse_mehrere_mehrere_k118_floor_finishes_bricks_panels`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Stahlträger und Stützen der Aufstockung` (`bg_reuse_stahl_mehrere_k118_structure`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete externe Stahltreppe` (`bg_reuse_stahl_mehrere_k118_external_stair`)

#### Reuse Strategy and Process

**HAT_AUFBEREITUNG**
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `Aluminium-Reinigung + Entdichtung` (`av_aluminium_reinigung_entdichtung`)
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `Aluminiumfenster — Beschläge + Dichtungen tauschen` (`av_aluminiumfenster_beschlag_dichtung`)
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `Entrosten / Korrosionsbehandlung` (`av_entrosten_korrosionsbehandlung`)
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `Fenster-Refurbishment (Beschläge + Dichtungen)` (`av_fenster_refurbishment`)
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `Glas-/Fensterelement-Prüfung + Sortierung` (`av_glas_pruefung_sortierung`)
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `Glas-Reinigung + Entkitten` (`av_glas_reinigung_entkitten`)
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `Korrosionsschutz-Beschichtung / Neubeschichtung` (`av_korrosionsschutz_beschichten`)
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `Lehm sieben, brechen, anfeuchten, neu mischen` (`av_lehm_sieben_mischen`)
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `Naturstein-Reinigung, Schleifen, Zuschnitt` (`av_naturstein_reinigung_schleifen_zuschnitt`)
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `Sandstrahlen / Strahlreinigen` (`av_sandstrahlen`)
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `Stahl-Zuschnitt, Bohrung, Lochung` (`av_stahl_zuschnitt_bohrung`)
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `Zuschnitt` (`av_zuschnitt`)
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `av_aluminiumfenster_pruefung_sortierung`
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `av_daemmstoff_zuschnitt`
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `av_oberflaechenbehandlung_metall`
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch geplante Beschaffung` (`mq_temporal_planned`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Bauteilkatalogisierung` (`meth_bauteilkatalogisierung`)
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Weiterbauen_im_Bestand` (`wva_weiterbauen_im_bestand`)

#### Risk, Checks, and Constraints

**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Keine relevanten Defekte (positive Befund)` (`def_keine_befunde`)
**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Ausschreibungsproblem` (`h_ausschreibungsproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Entwurfsbindung` (`h_entwurfsbindung`)
- Project -> `HAT_HUERDE` -> Huerde `Fehlende_Lagerflaeche` (`h_fehlende_lagerflaeche`)
- Project -> `HAT_HUERDE` -> Huerde `Haftung` (`h_haftung`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
**HAT_PRUEFUNG**
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_beschlagpruefung`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_biegezug`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_bohrbild_pruefung`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_brandklasse`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_brandpruefung_beschichtung`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_dichtheit`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_dichtungszustand`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_feuchtemessung`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_fugenbild`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_funktionspruefung`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_glasbruch_sichtpruefung`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_glastyp_nachweis`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_haftzug`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_haftzug_beschichtung`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_kornverteilung`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_lambda_wert`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_massaufnahme`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_petrografie`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_restquerschnitt`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_rostgrad`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_rutschhemmung`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_schadstoffanalyse_kitt`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_schichtdicke`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_schnittkantenpruefung`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_schwindmass`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_sichtpruefung`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_statik_nachweis`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_ug_uw_wert`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_ug_wert`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_ultraschall_dickenmessung`
**REFERENZIERT_NORM**
- Project -> `REFERENZIERT_NORM` -> Norm `DIN_EN_15804` (`norm_din_en_15804`)
- Project -> `REFERENZIERT_NORM` -> Norm `ISO_14040` (`norm_iso_14040`)
- Project -> `REFERENZIERT_NORM` -> Norm `ISO_14044` (`norm_iso_14044`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Asbest` (`s_asbest`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `KMF — Künstliche Mineralfasern (alte Mineralwolle vor 1996/2000)` (`s_kmf`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**BERECHNET_NACH_MODUL**
- Project -> `BERECHNET_NACH_MODUL` -> LCAModule `A1-A3 Produkt` (`lz_a1_a3`)
**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx vergleichbar mit Neubau` (`wi_capex_neutral`)
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Versteckte Kosten (Lagerung/Prüfung/Logistik)` (`wi_hidden_costs_lagerung_pruefung`)
**RELEVANT_FOR**
- ReuseRule `Schweiz × Beton reuse rule` (`rr_ch_beton`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Schweiz × Holz reuse rule` (`rr_ch_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Schweiz × Naturstein reuse rule` (`rr_ch_naturstein`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Schweiz × Stahl reuse rule` (`rr_ch_stahl`) -> `RELEVANT_FOR` -> Project

### 50. KA13 / Kristian Augusts gate 13, Oslo

Project ID: `p_ka13_kristian_augusts_gate_13_oslo`
Reuse-workflow edges: `52`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Asplan Viak` (`asplan_viak`) -> `BETEILIGT_AN` -> Project
- Akteur `Entra AS` (`entra_as`) -> `BETEILIGT_AN` -> Project
- Akteur `FutureBuilt` (`futurebuilt`) -> `BETEILIGT_AN` -> Project
- Akteur `IWG Group / Spaces` (`iwg_spaces`) -> `BETEILIGT_AN` -> Project
- Akteur `Insenti` (`insenti`) -> `BETEILIGT_AN` -> Project
- Akteur `MAD arkitekter / Mad as` (`mad_arkitekter`) -> `BETEILIGT_AN` -> Project
- Akteur `Scenario Interiørarkitekter` (`scenario_interioerarkitekter`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `KA13 Bestandsgebäude der 1950er-Jahre` (`bw_ka13_existing_building`)
- Project -> `HAS_BAUWERK` -> Bauwerk `KA13 Bestandsgebäude der 1950er-Jahre` (`bw_ka13_existing_building`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Kristian Augusts gate 13 / KA13 Bürogebäude` (`bw_ka13_oslo`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Regjeringsbygg R4 / government quarter Oslo` (`bw_regjeringsbygg_r4`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Erweiterung` (`bai_erweiterung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Norwegen` (`land_norwegen`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Oslo` (`stadt_oslo`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `KA13 Bestandsgebäude der 1950er-Jahre` (`bw_ka13_existing_building`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Kristian Augusts gate 13 / KA13 Bürogebäude` (`bw_ka13_oslo`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Regjeringsbygg R4 / government quarter Oslo` (`bw_regjeringsbygg_r4`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Erhaltenes KA13-Bestandstragwerk und Außenwände` (`bg_retained_mehrere_mehrere_ka13_existing_structure`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Bürofronten, Türen und Fassadenbekleidung` (`bg_reuse_mehrere_mehrere_ka13_office_fronts_doors_facade`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Hohlkörperdecken aus Regjeringsbygg R4` (`bg_reuse_stahlbeton_decke_ka13_hollow_core_slabs`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Radiatoren, Sanitär und Lüftungskanäle` (`bg_reuse_mehrere_technik_ka13_tga_sanitary_radiators`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendeter Stahl in Bestand und Erweiterung` (`bg_reuse_stahl_mehrere_ka13`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Adaptives_ReUse` (`wva_adaptives_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Design_for_Disassembly` (`wva_design_for_disassembly`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Riss / Rissbildung` (`def_riss`)
**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Bauproduktstatus` (`h_bauproduktstatus`)
- Project -> `HAT_HUERDE` -> Huerde `Bruch_Beschaedigungsrisiko` (`h_bruch_beschaedigungsrisiko`)
- Project -> `HAT_HUERDE` -> Huerde `Gewaehrleistung` (`h_gewaehrleistung`)
- Project -> `HAT_HUERDE` -> Huerde `Haftung` (`h_haftung`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Verfuegbarkeitsproblem` (`h_verfuegbarkeitsproblem`)
**REFERENZIERT_NORM**
- Project -> `REFERENZIERT_NORM` -> Norm `DIN_EN_15804` (`norm_din_en_15804`)
- Project -> `REFERENZIERT_NORM` -> Norm `DIN_EN_15978` (`norm_din_en_15978`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**BERECHNET_NACH_MODUL**
- Project -> `BERECHNET_NACH_MODUL` -> LCAModule `D Beyond (Reuse)` (`lz_d`)
**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Versteckte Kosten (Lagerung/Prüfung/Logistik)` (`wi_hidden_costs_lagerung_pruefung`)
**RELEVANT_FOR**
- ReuseRule `Norwegen × Beton / hollow-core slabs reuse rule` (`rr_no_beton_hollow_core_slabs`) -> `RELEVANT_FOR` -> Project
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Pilotprojekt` (`prog_pilotprojekt`)

### 51. Kamikatsu Zero Waste Center / Hotel WHY

Project ID: `p_kamikatsu_zero_waste_center_hotel_why`
Reuse-workflow edges: `42`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Hiroshi Nakamura & NAP` (`hiroshi_nakamura_nap`) -> `BETEILIGT_AN` -> Project
- Akteur `Kamikatsu Town` (`kamikatsu_town`) -> `BETEILIGT_AN` -> Project
- Akteur `Kitajima Corporation` (`kitajima_corporation`) -> `BETEILIGT_AN` -> Project
- Akteur `Lokale Einwohner Kamikatsu` (`kamikatsu_residents`) -> `BETEILIGT_AN` -> Project
- Akteur `Yamada Noriaki Structural Design Office` (`yamada_noriaki_structural_design`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Altes Rathaus Kamikatsu` (`bw_kamikatsu_old_town_hall`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Kamikatsu Zero Waste Center / Hotel WHY` (`bw_kamikatsu_zero_waste_center_hotel_why`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Lokale Häuser und Altbestände Kamikatsu` (`bw_kamikatsu_local_houses`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Infrastruktur` (`nut_infrastruktur`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Mischnutzung` (`nut_mischnutzung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Japan` (`land_japan`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Kamikatsu, Tokushima Prefecture` (`stadt_kamikatsu`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Altes Rathaus Kamikatsu` (`bw_kamikatsu_old_town_hall`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Kamikatsu Zero Waste Center / Hotel WHY` (`bw_kamikatsu_zero_waste_center_hotel_why`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Lokale Häuser und Altbestände Kamikatsu` (`bw_kamikatsu_local_houses`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Alte Fliesen als Mosaik-, Boden- und Traufendetail` (`bg_reuse_keramik_mehrere_kamikatsu_old_tiles`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Alte Rathauswandteile als Exterior Receiving Wall` (`bg_reuse_mehrere_mehrere_kamikatsu_old_town_hall_wall_parts`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Alte Shoji-Schirme und Glastüren im Hotel` (`bg_reuse_mehrere_mehrere_kamikatsu_shoji_glass_doors`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Ca. 700 gespendete Fassadenfenster` (`bg_reuse_mehrere_mehrere_kamikatsu_donated_facade_windows`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Glas- und Keramikscherben als fester Bodenbelag` (`bg_reuse_mehrere_boden_kamikatsu_glass_ceramic_terrazzo`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `International / interkontinental` (`mq_geographic_intl`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching unproblematisch` (`mq_temporal_easy`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Recycling` (`wva_recycling`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Upcycling` (`wva_upcycling`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Brandschutzkonflikt` (`h_brandschutzkonflikt`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Heterogenitaet_Chargen` (`h_heterogenitaet_chargen`)
- Project -> `HAT_HUERDE` -> Huerde `Hygieneanforderung` (`h_hygieneanforderung`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Toleranzen` (`h_toleranzen`)
- Project -> `HAT_HUERDE` -> Huerde `Witterung_Feuchte` (`h_witterung_feuchte`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

### 52. Kindergarten Mööslistrasse / Manegg Zürich

Project ID: `p_kindergarten_moeoeslistrasse_manegg_zuerich`
Reuse-workflow edges: `62`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Bischof Föhn Architektur` (`bischof_foehn_architektur`) -> `BETEILIGT_AN` -> Project
- Akteur `Haerter + Partner AG` (`haerter_partner`) -> `BETEILIGT_AN` -> Project
- Akteur `Ingenieurbureau Heierli AG` (`heierli_ag`) -> `BETEILIGT_AN` -> Project
- Akteur `Meili Partner Baumanagement` (`meili_partner`) -> `BETEILIGT_AN` -> Project
- Akteur `Schmidiger + Rosasco AG` (`schmidiger_rosasco`) -> `BETEILIGT_AN` -> Project
- Akteur `Stadt Zürich / Amt für Hochbauten / Immobilien Stadt Zürich` (`stadt_zuerich_amt_hochbauten`) -> `BETEILIGT_AN` -> Project
- Akteur `Zirkular` (`zirkular`) -> `BETEILIGT_AN` -> Project
- Akteur `aik Architektur + Ingenieur Kollektiv` (`aik_architektur_ingenieur_kollektiv`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Bischof Föhn Architektur` (`bischof_foehn_architektur`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Fabian Sauser` (`fabian_sauser`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Norbert Föhn` (`norbert_foehn`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Stephan Bischof` (`stephan_bischof`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Ehemaliges Einkaufswagendepot` (`bw_einkaufswagendepot_zuerich`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Schulhaus Lavater` (`bw_schulhaus_lavater`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Städtische Occasionslager Zürich` (`bw_stadt_zuerich_occasionslager`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Werkhof Mööslistrasse / Kindergarten Manegg` (`bw_werkhof_moeoeslistrasse`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Werkhof Mööslistrasse / Kindergarten Manegg` (`bw_werkhof_moeoeslistrasse`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umnutzung` (`bai_umnutzung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Schule_Bildung` (`nut_schule_bildung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Schweiz` (`land_schweiz`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Zürich` (`stadt_zuerich`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Ehemaliges Einkaufswagendepot` (`bw_einkaufswagendepot_zuerich`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Schulhaus Lavater` (`bw_schulhaus_lavater`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Städtische Occasionslager Zürich` (`bw_stadt_zuerich_occasionslager`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Werkhof Mööslistrasse / Kindergarten Manegg` (`bw_werkhof_moeoeslistrasse`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Brandschutztüren aus Schulhaus Lavater` (`bg_reuse_mehrere_tuer_moeoeslistrasse_brandschutztueren_lavater`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Erhaltene Werkhofstruktur und Umnutzung ehemaliger Wohnungen` (`bg_reuse_mehrere_mehrere_moeoeslistrasse_bestand_werkhof`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Stahlpergola / Beschattung aus Einkaufswagendepot` (`bg_reuse_mehrere_mehrere_moeoeslistrasse_stahlpergola_beschattung`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Akustikelemente` (`bg_reuse_mehrere_mehrere_moeoeslistrasse_akustikelemente`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Außentreppe` (`bg_reuse_stahl_treppe_moeoeslistrasse_aussentreppe`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Sanitärapparate und gebrauchte Küche` (`bg_reuse_mehrere_mehrere_moeoeslistrasse_sanitaer_kueche`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Stahlträger / Unterzüge / Stützen` (`bg_reuse_stahl_mehrere_moeoeslistrasse_stuetzen`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching unproblematisch` (`mq_temporal_easy`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Bauteilkatalogisierung` (`meth_bauteilkatalogisierung`)
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Adaptives_ReUse` (`wva_adaptives_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Aufbereitungsaufwand` (`h_aufbereitungsaufwand`)
- Project -> `HAT_HUERDE` -> Huerde `Brandschutzkonflikt` (`h_brandschutzkonflikt`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Entwurfsbindung` (`h_entwurfsbindung`)
- Project -> `HAT_HUERDE` -> Huerde `Gewaehrleistung` (`h_gewaehrleistung`)
- Project -> `HAT_HUERDE` -> Huerde `Kompatibilitaetsproblem` (`h_kompatibilitaetsproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Asbest` (`s_asbest`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `KMF — Künstliche Mineralfasern (alte Mineralwolle vor 1996/2000)` (`s_kmf`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx vergleichbar mit Neubau` (`wi_capex_neutral`)
**NUTZT_SOFTWARE**
- Project -> `NUTZT_SOFTWARE` -> Software:Tool `Bauteilkatalog / Bauteilpass` (`tool_bauteilkatalog`)
**RELEVANT_FOR**
- ReuseRule `Schweiz × Beton reuse rule` (`rr_ch_beton`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Schweiz × Holz reuse rule` (`rr_ch_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Schweiz × Stahl reuse rule` (`rr_ch_stahl`) -> `RELEVANT_FOR` -> Project

### 53. Liander / Alliander HQ, Duiven

Project ID: `p_liander_alliander_hq_duiven`
Reuse-workflow edges: `41`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Alliander / Liander` (`alliander_liander`) -> `BETEILIGT_AN` -> Project
- Akteur `Madaster / Materialpass-Kontext` (`madaster_context`) -> `BETEILIGT_AN` -> Project
- Akteur `RAU Architects` (`rau_architects`) -> `BETEILIGT_AN` -> Project
- Akteur `Turntoo / Circularity-Kontext` (`turntoo`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Alliander / Liander Hauptquartier Duiven` (`bw_alliander_hq_duiven`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Bestandsensemble Alliander Duiven` (`bw_alliander_existing_campus`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Sanierung` (`bai_sanierung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Niederlande` (`land_niederlande`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Duiven` (`stadt_duiven`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Alliander / Liander Hauptquartier Duiven` (`bw_alliander_hq_duiven`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Bestandsensemble Alliander Duiven` (`bw_alliander_existing_campus`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Erhaltene Bestandsgebäude des Campus` (`bg_retained_mehrere_mehrere_alliander_existing_buildings`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Gemeinsame Überdachung / Atriumhülle als Transformationsbauteil` (`bg_reuse_mehrere_mehrere_alliander_common_roof_atrium`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Materialpass / dokumentiertes Materialinventar` (`bg_reuse_mehrere_ausbau_alliander_material_passport_inventory`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Teilweise wiederverwendete Innenausbau-Elemente` (`bg_reuse_mehrere_mehrere_alliander_interior_elements`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Adaptives_ReUse` (`wva_adaptives_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Bestandserhalt` (`wva_bestandserhalt`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Design_for_Disassembly` (`wva_design_for_disassembly`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Entwurfsbindung` (`h_entwurfsbindung`)
- Project -> `HAT_HUERDE` -> Huerde `Fehlende_Datenstandards` (`h_fehlende_datenstandards`)
- Project -> `HAT_HUERDE` -> Huerde `Gewaehrleistung` (`h_gewaehrleistung`)
- Project -> `HAT_HUERDE` -> Huerde `Kompatibilitaetsproblem` (`h_kompatibilitaetsproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_ZERTIFIZIERUNG**
- Project -> `HAT_ZERTIFIZIERUNG` -> Zertifizierungssystem `BREEAM` (`zbs_breeam`)
**RELEVANT_FOR**
- ReuseRule `Niederlande × Beton reuse rule` (`rr_nl_beton`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Niederlande × Holz reuse rule` (`rr_nl_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Niederlande × Stahl reuse rule` (`rr_nl_stahl`) -> `RELEVANT_FOR` -> Project

### 54. Lo-Reninge Town Hall façade / Stadhuis Lo

Project ID: `p_lo_reninge_town_hall_facade`
Reuse-workflow edges: `34`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Dexia` (`dexia`) -> `BETEILIGT_AN` -> Project
- Akteur `Lo-Reninge town council` (`lo_reninge_town_council`) -> `BETEILIGT_AN` -> Project
- Akteur `noAarchitecten` (`noaarchitecten`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Ehemaliges Kloster Lo-Reninge` (`bw_lo_reninge_former_convent`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Rathaus Lo-Reninge / ehemaliges Kloster` (`bw_lo_reninge_town_hall`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Erweiterung` (`bai_erweiterung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Sanierung` (`bai_sanierung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Belgien` (`land_belgien`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Lo-Reninge` (`stadt_lo_reninge`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Ehemaliges Kloster Lo-Reninge` (`bw_lo_reninge_former_convent`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Rathaus Lo-Reninge / ehemaliges Kloster` (`bw_lo_reninge_town_hall`)
- Project -> `NUTZT_BAUWERK` -> Materialdepot `Unbekannte Quelle der wiederverwendeten Ziegel` (`bw_lo_reninge_reuse_brick_source`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Erhaltenes ehemaliges Kloster` (`bg_retained_mehrere_mehrere_lo_reninge_convent`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Fassadenziegel` (`bg_reuse_ziegel_mehrere_lo_reninge_facade`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching unproblematisch` (`mq_temporal_easy`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Bestandserhalt` (`wva_bestandserhalt`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Heterogenitaet_Chargen` (`h_heterogenitaet_chargen`)
- Project -> `HAT_HUERDE` -> Huerde `Materialqualitaet_Unklar` (`h_materialqualitaet_unklar`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Witterung_Feuchte` (`h_witterung_feuchte`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Belgien × Holz reuse rule` (`rr_be_holz`) -> `RELEVANT_FOR` -> Project

### 55. Lokomotion Technology Centre mini-pilot Tampere

Project ID: `p_lokomotion_technology_centre_mini_pilot_tampere`
Reuse-workflow edges: `38`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Consolis Parma` (`consolis_parma`) -> `BETEILIGT_AN` -> Project
- Akteur `Metso Oyj` (`metso_oyj`) -> `BETEILIGT_AN` -> Project
- Akteur `Ramboll Finland` (`ramboll_finland`) -> `BETEILIGT_AN` -> Project
- Akteur `Satu Huuhka` (`satu_huuhka`) -> `BETEILIGT_AN` -> Project
- Akteur `Skanska Finland` (`skanska_finland`) -> `BETEILIGT_AN` -> Project
- Akteur `Tampere University / ReCreate Finnish cluster` (`tampere_university_recreate`) -> `BETEILIGT_AN` -> Project
- Akteur `Umacon` (`umacon`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Angelika Mettke` (`angelika_mettke`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Patrick Teuffel` (`patrick_teuffel`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Satu Huuhka` (`satu_huuhka`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `1980er Bürogebäude im Zentrum von Tampere` (`bw_tampere_1980s_office_donor`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Technikbau und Personalräume im Lokomotion-Projekt` (`bw_lokomotion_reuse_teilbereiche`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Infrastruktur` (`nut_infrastruktur`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `In_Bau` (`status_in_bau`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Finnland` (`land_finnland`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Tampere` (`stadt_tampere`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `1980er Bürogebäude im Zentrum von Tampere` (`bw_tampere_1980s_office_donor`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Consolis Parma Werk Nummela` (`bw_consolis_parma_nummela_werk`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Metso Lokomotion Technology Centre Phase 1` (`bw_lokomotion_technology_centre`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Technikbau und Personalräume im Lokomotion-Projekt` (`bw_lokomotion_reuse_teilbereiche`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `27 wiederverwendete Hohlkörperdecken` (`bg_reuse_stahlbeton_mehrere_lokomotion_hollow_core_slabs`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
- Project -> `HAT_METHODE` -> Methode `Pre_Deconstruction_Audit` (`meth_pre_deconstruction_audit`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Refurbishment` (`wva_refurbishment`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Aufbereitungsaufwand` (`h_aufbereitungsaufwand`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Gewaehrleistung` (`h_gewaehrleistung`)
- Project -> `HAT_HUERDE` -> Huerde `Kompatibilitaetsproblem` (`h_kompatibilitaetsproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Terminunsicherheit` (`h_terminunsicherheit`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)

#### Tools, Programmes, and Frameworks

**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `ReCreate` (`prog_recreate`)

### 56. Lycée Michel Lucius Conversion, Luxembourg

Project ID: `p_lycee_michel_lucius_conversion_luxembourg`
Reuse-workflow edges: `35`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Administration des bâtiments publics` (`administration_des_batiments_publics`) -> `BETEILIGT_AN` -> Project
- Akteur `Daedalus Engineering` (`daedalus_engineering`) -> `BETEILIGT_AN` -> Project
- Akteur `Schmets architectes` (`schmets_architectes`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Lycée Michel Lucius Block 3000` (`bw_lycee_block_3000`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Lycée Michel Lucius Block 6000` (`bw_lycee_block_6000`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Neue Esplanade und Außenanlagen Lycée Michel Lucius` (`bw_lycee_esplanade_aussenanlagen`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umnutzung` (`bai_umnutzung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Schule_Bildung` (`nut_schule_bildung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Luxemburg` (`land_luxemburg`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Luxembourg-Limpertsberg` (`stadt_luxembourg_limpertsberg`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Lycée Michel Lucius Block 3000` (`bw_lycee_block_3000`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Lycée Michel Lucius Block 6000` (`bw_lycee_block_6000`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Lycée Michel Lucius Campus` (`bw_lycee_michel_lucius_campus`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Neue Esplanade und Außenanlagen Lycée Michel Lucius` (`bw_lycee_esplanade_aussenanlagen`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `11,8 t Stahlprofile als Überdachung` (`bg_reuse_stahl_mehrere_lycee_profiles_canopy`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `12 Metall-Deckenpaneele / 4,3 m²` (`bg_reuse_stahl_mehrere_lycee_metal_ceiling_panels`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `135 m² wiederverwendete Straßenpflasterplatten` (`bg_reuse_beton_boden_lycee_paving_slabs`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `38 Fertigbetonelemente als Rinnen` (`bg_reuse_beton_mehrere_lycee_precast_channels`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `419 m² Gips-Akustikpaneele aus abgehängten Decken` (`bg_reuse_daemmstoff_mehrere_lycee_gypsum_acoustic_panels`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `61 m² Bodenblech als Fassadenbekleidung` (`bg_reuse_stahl_mehrere_lycee_floor_sheet_metal_facade`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Stahlfassadenpaneele als Geländer` (`bg_reuse_stahl_mehrere_lycee_facade_panels_railing`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Same_Site_ReUse` (`wva_same_site_reuse`)

#### Risk, Checks, and Constraints

**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Asbest` (`s_asbest`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `KMF — Künstliche Mineralfasern (alte Mineralwolle vor 1996/2000)` (`s_kmf`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx höher, Subvention/Förderung deckt Mehrkosten` (`wi_capex_hoeher_subvention`)
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Pilotprojekt` (`prog_pilotprojekt`)

### 57. LYSP8

Project ID: `p_lysp8`
Reuse-workflow edges: `1`

#### Actors and Delivery Chain

**STUB_PROJECT_LINK**
- Akteur `Kevin Straub` (`kevin_straub`) -> `STUB_PROJECT_LINK` -> Project

### 58. LysP8 — LysBüchelStrasse 8 Reuse Pilot Basel (Loeliger Strub / Zirkular / Stiftung Habitat)

Project ID: `p_lysp8_basel`
Reuse-workflow edges: `54`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Baugenossenschaft mehr als wohnen` (`mehr_als_wohnen`) -> `BETEILIGT_AN` -> Project
- Akteur `KIBAG — Oxacrete material production` (`kibag`) -> `BETEILIGT_AN` -> Project
- Akteur `Laia Meier — component hunting at Zirkular` (`laia_meier`) -> `BETEILIGT_AN` -> Project
- Akteur `Loeliger Strub Architektur GmbH — LysP8 lead architect` (`loeliger_strub`) -> `BETEILIGT_AN` -> Project
- Akteur `Martin Zeller` (`martin_zeller`) -> `BETEILIGT_AN` -> Project
- Akteur `Oxara AG — Oxacrete poured-earth floor supplier (LysP8)` (`oxara_ag`) -> `BETEILIGT_AN` -> Project
- Akteur `Pascal Hentschel` (`pascal_hentschel`) -> `BETEILIGT_AN` -> Project
- Akteur `Pirmin Jung Schweiz AG — LysP8 timber engineer` (`pirmin_jung_schweiz`) -> `BETEILIGT_AN` -> Project
- Akteur `Rebecca Brandmayer — component hunting at Zirkular` (`rebecca_brandmayer`) -> `BETEILIGT_AN` -> Project
- Akteur `Repoxit AG — construction / floor execution (Oxacrete)` (`repoxit_ag`) -> `BETEILIGT_AN` -> Project
- Akteur `Stiftung Habitat` (`stiftung_habitat`) -> `BETEILIGT_AN` -> Project
- Akteur `Zirkular` (`zirkular`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Kerstin Müller` (`kerstin_mueller`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Kevin Straub` (`kevin_straub`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Loeliger Strub Architektur GmbH — LysP8 lead architect` (`loeliger_strub`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Marc Angst` (`marc_angst`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Marc Loeliger` (`marc_loeliger`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Martin Zeller` (`martin_zeller`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Pascal Hentschel` (`pascal_hentschel`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Zirkular` (`zirkular`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `baubüro in situ` (`baubuero_in_situ`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `LysP8 — LysBüchelStrasse 8 Reuse Pilot Basel (Loeliger Strub / Zirkular / Stiftung Habitat)` (`bw_lysp8_basel`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Schweiz` (`land_schweiz`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Basel` (`stadt_basel`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `LysP8 — LysBüchelStrasse 8 Reuse Pilot Basel (Loeliger Strub / Zirkular / Stiftung Habitat)` (`bw_lysp8_basel`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `LysP8 — All kitchens reclaimed from a Zürich housing estate and stored for project` (`bg_reuse_holz_ausbau_lysp8_kitchens`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `LysP8 — DfD timber structure with screwed visible elements` (`bg_planned_holz_mehrere_lysp8_dfd_frame`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `LysP8 — Oxacrete Nossim poured-earth floor (Oxara + Repoxit + KIBAG)` (`bg_planned_lehm_erde_boden_lysp8_oxacrete`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `LysP8 — Reuse façade components: roof tiles, window shutters, fibre-cement panels, railings` (`bg_reuse_mehrere_fassade_lysp8_external_mix`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `LysP8 — Reused doors and tiles` (`bg_reuse_mehrere_ausbau_lysp8_doors_tiles`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `LysP8 — Reused steel grid grating steps for seat stair` (`bg_reuse_metall_boden_lysp8_grating_steps`)

#### Reuse Strategy and Process

**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
- Project -> `HAT_METHODE` -> Methode `Design_for_Disassembly` (`meth_design_for_disassembly`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Aufbereitungsaufwand` (`h_aufbereitungsaufwand`)
- Project -> `HAT_HUERDE` -> Huerde `Fehlende_Lagerflaeche` (`h_fehlende_lagerflaeche`)
- Project -> `HAT_HUERDE` -> Huerde `Terminunsicherheit` (`h_terminunsicherheit`)
- Project -> `HAT_HUERDE` -> Huerde `Toleranzen` (`h_toleranzen`)
- Project -> `HAT_HUERDE` -> Huerde `Verfuegbarkeitsproblem` (`h_verfuegbarkeitsproblem`)
**REFERENZIERT_NORM**
- Project -> `REFERENZIERT_NORM` -> Norm `SIA 269 — Existing structures: Grundlagen / Erhaltung von Tragwerken` (`norm_sia_269`)
- Project -> `REFERENZIERT_NORM` -> Norm `SIA 416 — Kennzahlen für Grundstücke und Gebäude (Schweiz)` (`norm_sia_416`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx vergleichbar mit Neubau` (`wi_capex_neutral`)
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Kostenvergleich` (`wi_kostenvergleich`)
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Lebenszykluskosten` (`wi_lebenszykluskosten`)
**RELEVANT_FOR**
- ReuseRule `Schweiz × Holz reuse rule` (`rr_ch_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Schweiz × Stahl reuse rule` (`rr_ch_stahl`) -> `RELEVANT_FOR` -> Project

### 59. Maison des Canaux, Paris

Project ID: `p_maison_des_canaux_paris`
Reuse-workflow edges: `28`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Les Canaux` (`les_canaux`) -> `BETEILIGT_AN` -> Project
- Akteur `Ville de Paris` (`ville_de_paris`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Maison des Canaux Bestandsgebäude am Canal` (`bw_maison_des_canaux_bestandsgebaeude`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Sanierung` (`bai_sanierung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umnutzung` (`bai_umnutzung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Frankreich` (`land_frankreich`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Paris` (`stadt_paris`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Maison des Canaux Bestandsgebäude am Canal` (`bw_maison_des_canaux_bestandsgebaeude`)
- Project -> `NUTZT_BAUWERK` -> Materialdepot `Unbekannte Reuse-Quellen Maison des Canaux` (`bw_maison_des_canaux_unspecified_donors`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Boden- und Wandbeläge` (`bg_reuse_mehrere_mehrere_maison_des_canaux_floor_wall_finishes`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Sanitärteile` (`bg_reuse_mehrere_mehrere_maison_des_canaux_sanitary_parts`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Türen / Raumabschlüsse` (`bg_reuse_mehrere_mehrere_maison_des_canaux_doors`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete feste Einbauten / technische Elemente` (`bg_reuse_mehrere_mehrere_maison_des_canaux_fixed_builtins`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Refurbishment` (`wva_refurbishment`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Versteckte Kosten (Lagerung/Prüfung/Logistik)` (`wi_hidden_costs_lagerung_pruefung`)

### 60. Maison DnA / dnA House, Asse

Project ID: `p_maison_dna_asse`
Reuse-workflow edges: `23`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `BLAF Architecten` (`blaf_architecten`) -> `BETEILIGT_AN` -> Project
- Akteur `Private Bauherrschaft Maison DnA` (`maison_dna_private_owner`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Maison DnA Einfamilienhaus mit Home Office` (`bw_maison_dna_receiver`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Belgien` (`land_belgien`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Asse` (`stadt_asse`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Maison DnA Einfamilienhaus mit Home Office` (`bw_maison_dna_receiver`)
- Project -> `NUTZT_BAUWERK` -> Materialdepot `Unbekannte Spenderquelle der wiederverwendeten Ziegel` (`bw_maison_dna_unknown_brick_donor`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Neue innere Holzrahmenbox als Energie- und Nutzungsschicht` (`bg_reuse_holz_mehrere_maison_dna_new_inner_box_context`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Ziegelwände als äußere autonome Struktur` (`bg_reuse_ziegel_mehrere_maison_dna_outer_walls`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Reversibilitaet` (`meth_reversibilitaet`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Asbest` (`s_asbest`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `KMF — Künstliche Mineralfasern (alte Mineralwolle vor 1996/2000)` (`s_kmf`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Belgien × Holz reuse rule` (`rr_be_holz`) -> `RELEVANT_FOR` -> Project

### 61. Maison Vignette, Auderghem

Project ID: `p_maison_vignette_auderghem`
Reuse-workflow edges: `30`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `2emain.be` (`2emain_be`) -> `BETEILIGT_AN` -> Project
- Akteur `BESP Stoffel & Partners / Pierre Stoffel` (`besp_stoffel_partners`) -> `BETEILIGT_AN` -> Project
- Akteur `Franck Bricks` (`frank_bricks`) -> `BETEILIGT_AN` -> Project
- Akteur `Karbon’ architecture & urbanisme` (`karbon_architecture_urbanisme`) -> `BETEILIGT_AN` -> Project
- Akteur `Private Bauherrschaft Maison Vignette` (`maison_vignette_private_owner`) -> `BETEILIGT_AN` -> Project
- Akteur `RotorDC` (`rotordc`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Diverse Reuse-Quellen Maison Vignette` (`bw_maison_vignette_unknown_donors`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Maison Vignette Einfamilienhaus` (`bw_maison_vignette_receiver`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Solvay-Gebäude als Fliesen-Donor` (`bw_solvay_building_tile_donor`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Belgien` (`land_belgien`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Auderghem / Brüssel` (`stadt_auderghem_brussels`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Diverse Reuse-Quellen Maison Vignette` (`bw_maison_vignette_unknown_donors`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Maison Vignette Einfamilienhaus` (`bw_maison_vignette_receiver`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Solvay-Gebäude als Fliesen-Donor` (`bw_solvay_building_tile_donor`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `13,5 m² wiederverwendete Terrakotta-Bodenfliesen` (`bg_reuse_keramik_mehrere_maison_vignette_terracotta_floor_tiles`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `21 m² wiederverwendete Wandfliesen aus Solvay-Gebäude` (`bg_reuse_keramik_mehrere_maison_vignette_wall_tiles_solvay`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `3.000 wiederverwendete Ziegel für 36 m² Fassaden-Claustra` (`bg_reuse_ziegel_mehrere_maison_vignette_facade_claustra`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `40 m² wiederverwendete Blausteinplatten` (`bg_reuse_naturstein_boden_maison_vignette_bluestone_slabs`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Sanitärobjekte von Rotor DC` (`bg_reuse_mehrere_mehrere_maison_vignette_sanitary_objects`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx höher, Subvention/Förderung deckt Mehrkosten` (`wi_capex_hoeher_subvention`)
**RELEVANT_FOR**
- ReuseRule `Belgien × Naturstein reuse rule` (`rr_be_naturstein`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Belgien × Stahl reuse rule` (`rr_be_stahl`) -> `RELEVANT_FOR` -> Project
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Foerderprogramm` (`prog_foerderprogramm`)

### 62. MedUni Campus Mariannengasse Wien — BauKarussell pre-demolition reuse

Project ID: `p_meduni_campus_mariannengasse`
Reuse-workflow edges: `37`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `BIG — Bundesimmobiliengesellschaft m.b.H. — MedUni Campus property client` (`big_bundesimmobilien`) -> `BETEILIGT_AN` -> Project
- Akteur `BauKarussell` (`baukarussell`) -> `BETEILIGT_AN` -> Project
- Akteur `DRZ — Demontage- und Recycling-Zentrum (BauKarussell social-enterprise partner)` (`drz_demontage_recycling`) -> `BETEILIGT_AN` -> Project
- Akteur `Die Kümmerei — BauKarussell social-enterprise partner` (`die_kuemmerei`) -> `BETEILIGT_AN` -> Project
- Akteur `Markus Meissner` (`markus_meissner`) -> `BETEILIGT_AN` -> Project
- Akteur `Medizinische Universität Wien — MedUni Campus user` (`meduni_wien`) -> `BETEILIGT_AN` -> Project
- Akteur `Thomas Romm` (`thomas_romm`) -> `BETEILIGT_AN` -> Project
- Akteur `Wiener Aufzugmuseum — MedUni Paternoster receiver (museum)` (`wiener_aufzugmuseum`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Markus Meissner` (`markus_meissner`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Thomas Romm` (`thomas_romm`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `MedUni Campus Mariannengasse Wien — BauKarussell pre-demolition reuse` (`bw_meduni_campus_mariannengasse`)
- Project -> `HAS_BAUWERK` -> Bauwerk `MedUni Campus Mariannengasse Wien — BauKarussell pre-demolition reuse` (`bw_meduni_campus_mariannengasse`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Rueckbau` (`bai_rueckbau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Schule_Bildung` (`nut_schule_bildung`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Österreich` (`land_oesterreich`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Wien` (`stadt_wien`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `MedUni Campus Mariannengasse Wien — BauKarussell pre-demolition reuse` (`bw_meduni_campus_mariannengasse`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `MedUni Mariannengasse — Bike workshop equipment (donor batch)` (`bg_reuse_metall_ausbau_medunicampus_bike_workshop`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `MedUni Mariannengasse — Doors repurposed as wall cladding (donor batch)` (`bg_reuse_holz_wand_medunicampus_doors_as_cladding`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `MedUni Mariannengasse — Fluorescent tubes (hazardous removal, not reuse)` (`bg_dismantled_glas_technik_medunicampus_fluorescent`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `MedUni Mariannengasse — Heavy-duty shelves (donor batch)` (`bg_reuse_metall_ausbau_medunicampus_heavy_shelves`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `MedUni Mariannengasse — Jugendstil glass ceiling retained in situ` (`bg_retained_mehrere_decke_medunicampus_glasdecke`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `MedUni Mariannengasse — Paternoster cabins (donor batch → Wiener Aufzugmuseum)` (`bg_reuse_mehrere_technik_medunicampus_paternoster`)

#### Reuse Strategy and Process

**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Bauteilkatalogisierung` (`meth_bauteilkatalogisierung`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
- Project -> `HAT_METHODE` -> Methode `Pre_Deconstruction_Audit` (`meth_pre_deconstruction_audit`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Akzeptanzproblem` (`h_akzeptanzproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Ausschreibungsproblem` (`h_ausschreibungsproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Terminunsicherheit` (`h_terminunsicherheit`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Geschaeftsmodell` (`wi_geschaeftsmodell`)
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Preisbildung` (`wi_preisbildung`)

### 63. Mehrow Pilot House

Project ID: `p_mehrow_pilot_house`
Reuse-workflow edges: `20`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Claus Asam / IEMB` (`claus_asam_iemb`) -> `BETEILIGT_AN` -> Project
- Akteur `Hervé Biele / Conclus` (`herve_biele_conclus`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Abgerissener Marzahner WBS70-Elfgeschosser` (`bw_marzahn_wbs70_eleven_storey_donor`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Mehrow Pilotwohnhaus / Einfamilienhaus` (`bw_mehrow_pilot_house_receiver`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Deutschland` (`land_deutschland`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Mehrow, Brandenburg` (`stadt_mehrow`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Abgerissener Marzahner WBS70-Elfgeschosser` (`bw_marzahn_wbs70_eleven_storey_donor`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Mehrow Pilotwohnhaus / Einfamilienhaus` (`bw_mehrow_pilot_house_receiver`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `22 wiederverwendete WBS70-Wandplatten` (`bg_reuse_stahlbeton_wand_mehrow_wbs70_slabs`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `27 wiederverwendete WBS70-Deckenplatten` (`bg_reuse_stahlbeton_mehrere_mehrow_wbs70_floor_slabs`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Regional geografisches Matching (50–500 km)` (`mq_geographic_regional`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFTSASPEKT**
- Project -> `HAT_WIRTSCHAFTSASPEKT` -> Wirtschaft `Kostenvergleich` (`wi_kostenvergleich`)
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Pilotprojekt` (`prog_pilotprojekt`)

### 64. Melkinlaituri Primary School and Day-care Centre Helsinki

Project ID: `p_melkinlaituri_primary_school_daycare_centre_helsinki`
Reuse-workflow edges: `26`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `City of Helsinki` (`city_of_helsinki`) -> `BETEILIGT_AN` -> Project
- Akteur `Consolis Parma` (`consolis_parma`) -> `BETEILIGT_AN` -> Project
- Akteur `Ramboll Finland` (`ramboll_finland`) -> `BETEILIGT_AN` -> Project
- Akteur `ReCreate Finnish cluster` (`recreate_finnish_cluster`) -> `BETEILIGT_AN` -> Project
- Akteur `Umacon` (`umacon`) -> `BETEILIGT_AN` -> Project
- Akteur `YIT` (`yit`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Angelika Mettke` (`angelika_mettke`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Patrick Teuffel` (`patrick_teuffel`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Satu Huuhka` (`satu_huuhka`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Melkinlaituri elementary school and daycare centre` (`bw_melkinlaituri_school_daycare_receiver`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Suutarila community centre, Helsinki` (`bw_suutarila_community_centre_donor`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Schule_Bildung` (`nut_schule_bildung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `In_Bau` (`status_in_bau`)
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Finnland` (`land_finnland`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Helsinki` (`stadt_helsinki`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Melkinlaituri elementary school and daycare centre` (`bw_melkinlaituri_school_daycare_receiver`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Suutarila community centre, Helsinki` (`bw_suutarila_community_centre_donor`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `64 reused hollow-core slabs from Suutarila community centre` (`bg_reuse_stahlbeton_mehrere_melkinlaituri_hollow_core_slabs`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Refurbishment` (`wva_refurbishment`)

#### Risk, Checks, and Constraints

**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)

#### Tools, Programmes, and Frameworks

**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Forschungsprojekt` (`prog_forschungsprojekt`)
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Pilotprojekt` (`prog_pilotprojekt`)

### 65. Montessori Maassluis

Project ID: `p_montessori_maassluis`
Reuse-workflow edges: `26`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `A. de Jong Groep` (`de_jong_groep`) -> `BETEILIGT_AN` -> Project
- Akteur `Anculus B.V.` (`anculus_bv`) -> `BETEILIGT_AN` -> Project
- Akteur `IMd Raadgevende Ingenieurs` (`imd_raadgevende_ingenieurs`) -> `BETEILIGT_AN` -> Project
- Akteur `Kraaijvanger Architects` (`kraaijvanger_architects`) -> `BETEILIGT_AN` -> Project
- Akteur `Stichting Montessorischolen Monton` (`stichting_montessorischolen_monton`) -> `BETEILIGT_AN` -> Project
- Akteur `VIA Landscape` (`via_landscape`) -> `BETEILIGT_AN` -> Project
- Akteur `Van Dijk Maasland B.V.` (`van_dijk_maasland_bv`) -> `BETEILIGT_AN` -> Project
- Akteur `Vintis installatieadviseurs` (`vintis_installatieadviseurs`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Angelika Mettke` (`angelika_mettke`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Patrick Teuffel` (`patrick_teuffel`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Montessorischool Maassluis Ersatzneubau` (`bw_montessori_maassluis_receiver`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Schule_Bildung` (`nut_schule_bildung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Geplant` (`status_geplant`)
- Project -> `HAT_STATUS` -> Status `In_Bau` (`status_in_bau`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Niederlande` (`land_niederlande`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Maassluis` (`stadt_maassluis`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Montessorischool Maassluis Ersatzneubau` (`bw_montessori_maassluis_receiver`)

#### Components and Construction System

**HAT_BAUSYSTEM**
- Project -> `HAT_BAUSYSTEM` -> Bausystem `Holz_Skelettbau` (`bsys_holz_skelettbau`)
**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Geplante wiederverwendete Hohlkörperdecken` (`bg_planned_stahlbeton_decke_montessori_maassluis_hollow_core_slabs`)
**HAT_BAUWEISE**
- Project -> `HAT_BAUWEISE` -> Bauweise `Hybridbauweise` (`bauw_hybridbauweise`)
**HAT_TRAGWERKSPRINZIP**
- Project -> `HAT_TRAGWERKSPRINZIP` -> Tragwerksprinzip `Skeletttragwerk` (`tp_skeletttragwerk`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)

### 66. Multi Brussels / Reuse in MULTI

Project ID: `p_multi_brussels_reuse_in_multi`
Reuse-workflow edges: `47`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `CONIX RDBM` (`conix_rdbm`) -> `BETEILIGT_AN` -> Project
- Akteur `Cordeel` (`cordeel`) -> `BETEILIGT_AN` -> Project
- Akteur `Immobel` (`immobel`) -> `BETEILIGT_AN` -> Project
- Akteur `Madaster / EPEA` (`madaster_epea`) -> `BETEILIGT_AN` -> Project
- Akteur `Rotor` -> `BETEILIGT_AN` -> Project
- Akteur `RotorDC` (`rotordc`) -> `BETEILIGT_AN` -> Project
- Akteur `Whitewood` (`whitewood`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Christine Conix` (`christine_conix`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Lionel Billiet` (`lionel_billiet`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Lionel Devlieger` (`lionel_devlieger`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Maarten Gielen` (`maarten_gielen`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Michaël Ghyoot` (`michael_ghyoot`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Sébastien Paulet` (`sebastien_paulet`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Ehemaliger Philips / Brouckère Tower, MULTI Brussels` (`bw_multi_brouckere_tower`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Ehemaliger Philips / Brouckère Tower, MULTI Brussels` (`bw_multi_brouckere_tower`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Externe Urban-Mining-Quellen für Naturstein und Granit` (`bw_multi_external_urban_mining_sources`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Sanierung` (`bai_sanierung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umnutzung` (`bai_umnutzung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Mischnutzung` (`nut_mischnutzung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Belgien` (`land_belgien`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Brüssel` (`stadt_bruessel`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Ehemaliger Philips / Brouckère Tower, MULTI Brussels` (`bw_multi_brouckere_tower`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Externe Urban-Mining-Quellen für Naturstein und Granit` (`bw_multi_external_urban_mining_sources`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wieder eingebaute Aufzugsmotoren` (`bg_reuse_stahl_technik_multi_reinstalled_elevator_motors`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Aluminiumprofile` (`bg_reuse_aluminium_mehrere_multi_profiles`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Blaustein-Fassadenblöcke und -platten` (`bg_reuse_naturstein_mehrere_multi_blaustein_facade_slabs`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Granit- und Natursteinplatten` (`bg_reuse_naturstein_boden_multi_granite_natural_tiles`)

#### Reuse Strategy and Process

**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Bauteiltracking` (`log_bauteiltracking`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
- Project -> `HAT_METHODE` -> Methode `Urban_Mining` (`meth_urban_mining`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Adaptives_ReUse` (`wva_adaptives_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Bestandserhalt` (`wva_bestandserhalt`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Same_Site_ReUse` (`wva_same_site_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Urban_Mining` (`wva_urban_mining`)

#### Risk, Checks, and Constraints

**HAS_RISK_POLLUTANT**
- Project -> `HAS_RISK_POLLUTANT` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_ZERTIFIZIERUNG**
- Project -> `HAT_ZERTIFIZIERUNG` -> Zertifizierungssystem `BREEAM` (`zbs_breeam`)
**RELEVANT_FOR**
- ReuseRule `Belgien × Naturstein reuse rule` (`rr_be_naturstein`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Belgien × Stahl reuse rule` (`rr_be_stahl`) -> `RELEVANT_FOR` -> Project

### 67. Musée de Folklore Vie Frontalière / MUSEF Mouscron

Project ID: `p_musee_de_folklore_mouscron`
Reuse-workflow edges: `23`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Bureau Bouwtechniek` (`bureau_bouwtechniek`) -> `BETEILIGT_AN` -> Project
- Akteur `Daidalos Peutz` (`daidalos_peutz`) -> `BETEILIGT_AN` -> Project
- Akteur `Greisch` (`greisch`) -> `BETEILIGT_AN` -> Project
- Akteur `Simon Boudvin` (`simon_boudvin`) -> `BETEILIGT_AN` -> Project
- Akteur `Taktyk` (`taktyk`) -> `BETEILIGT_AN` -> Project
- Akteur `V+ / Projectiles` (`vplus_projectiles`) -> `BETEILIGT_AN` -> Project
- Akteur `Ville de Mouscron` (`ville_de_mouscron`) -> `BETEILIGT_AN` -> Project
- Akteur `Westvlaamse Steencentrale / Interconstruct` (`westvlaamse_steencentrale_interconstruct`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Acht Abbruchquellen in Mouscron` (`bw_musef_eight_demolition_sources`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Musée de Folklore Vie Frontalière / MUSEF` (`bw_musef_mouscron_receiver`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Erweiterung` (`bai_erweiterung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Sanierung` (`bai_sanierung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Belgien` (`land_belgien`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Mouscron` (`stadt_mouscron`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Acht Abbruchquellen in Mouscron` (`bw_musef_eight_demolition_sources`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Musée de Folklore Vie Frontalière / MUSEF` (`bw_musef_mouscron_receiver`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Fassadenziegel aus acht Mouscron-Abbruchquellen` (`bg_reuse_ziegel_mehrere_musef_facade`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Urban_Mining` (`wva_urban_mining`)

### 68. OBK 27

Project ID: `p_obk_27`
Reuse-workflow edges: `2`

#### Actors and Delivery Chain

**STUB_PROJECT_LINK**
- Akteur `Cyril Pressacco` (`cyril_pressacco`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Thibaut Barrault` (`thibaut_barrault`) -> `STUB_PROJECT_LINK` -> Project

### 69. Pavilion Circl Amsterdam

Project ID: `p_pavilion_circl_amsterdam`
Reuse-workflow edges: `1`

#### Actors and Delivery Chain

**STUB_PROJECT_LINK**
- Akteur `Hans Hammink` (`hans_hammink`) -> `STUB_PROJECT_LINK` -> Project

### 70. People’s Pavilion Eindhoven

Project ID: `p_peoples_pavilion_eindhoven`
Reuse-workflow edges: `42`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Arup` (`arup`) -> `BETEILIGT_AN` -> Project
- Akteur `Dutch Design Foundation` (`dutch_design_foundation`) -> `BETEILIGT_AN` -> Project
- Akteur `Ham & Sybesma` (`ham_sybesma`) -> `BETEILIGT_AN` -> Project
- Akteur `IJB groep` (`ijb_groep`) -> `BETEILIGT_AN` -> Project
- Akteur `New Horizon` (`new_horizon`) -> `BETEILIGT_AN` -> Project
- Akteur `Overtreders W` (`overtreders_w`) -> `BETEILIGT_AN` -> Project
- Akteur `Stiho group` (`stiho_group`) -> `BETEILIGT_AN` -> Project
- Akteur `bureau SLA` (`bureau_sla`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Hester van Dijk` (`hester_van_dijk`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Peter van Assche` (`peter_van_assche`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Reinder Bakker` (`reinder_bakker`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `People’s Pavilion temporary DDW 2017 pavilion` (`bw_peoples_pavilion_receiver`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
- Project -> `HAT_STATUS` -> Status `Rueckgebaut` (`status_rueckgebaut`)
- Project -> `HAT_STATUS` -> Status `Temporaer` (`status_temporaer`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Niederlande` (`land_niederlande`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Eindhoven` (`stadt_eindhoven`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `People’s Pavilion temporary DDW 2017 pavilion` (`bw_peoples_pavilion_receiver`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Geliehene Betonpfähle / Betonelemente` (`bg_reuse_beton_fundament_peoples_pavilion_elements`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Geliehene Fassadenelemente` (`bg_reuse_mehrere_fassade_peoples_pavilion_borrowed_elements`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Geliehene Holzträger` (`bg_reuse_holz_traeger_peoples_pavilion`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Geliehenes Glasdach` (`bg_reuse_glas_dach_peoples_pavilion`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Pretty Plastic Schindeln aus Haushaltskunststoff` (`bg_reuse_kunststoff_fassade_peoples_pavilion_pretty_plastic_shingles`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Informelles_Netzwerk` (`bweg_informelles_netzwerk`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Design_for_Disassembly` (`meth_design_for_disassembly`)
- Project -> `HAT_METHODE` -> Methode `Reversibilitaet` (`meth_reversibilitaet`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Design_for_Disassembly` (`wva_design_for_disassembly`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Upcycling` (`wva_upcycling`)

#### Risk, Checks, and Constraints

**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Verformung / Setzung / Verzug` (`def_verformung`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFTSASPEKT**
- Project -> `HAT_WIRTSCHAFTSASPEKT` -> Wirtschaft `Geschaeftsmodell` (`wi_geschaeftsmodell`)
**RELEVANT_FOR**
- ReuseRule `Niederlande × Beton reuse rule` (`rr_nl_beton`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Niederlande × Holz reuse rule` (`rr_nl_holz`) -> `RELEVANT_FOR` -> Project

### 71. Plattenpalast Berlin

Project ID: `p_plattenpalast_berlin`
Reuse-workflow edges: `55`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Carsten Wiewiorra` (`ak_carsten_wiewiorra`) -> `BETEILIGT_AN` -> Project
- Akteur `TU Berlin / IEMB` (`ak_tu_berlin_iemb`) -> `BETEILIGT_AN` -> Project
- Akteur `Wiewiorra Hopp Architekten` (`ak_wiewiorra_hopp_architekten`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Palast der Republik Berlin` (`bw_palast_der_republik_berlin`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Peter-Behrens-Halle Berlin` (`bw_peter_behrens_halle_berlin`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Plattenpalast Kleinsthaus / Galerie` (`bw_plattenpalast_berlin`)
- Project -> `HAS_BAUWERK` -> Bauwerk `rückgebaute WBS70-Plattenbauten` (`bw_unbekannte_wbs70_plattenbauten`)
**HAT_BAUOBJEKTKLASSE**
- Project -> `HAT_BAUOBJEKTKLASSE` -> Bauobjektklasse `Gebaeude` (`bok_gebaeude`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Prototyp` (`status_prototyp`)
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Deutschland` (`land_deutschland`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Berlin` (`stadt_berlin`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Palast der Republik Berlin` (`bw_palast_der_republik_berlin`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Peter-Behrens-Halle Berlin` (`bw_peter_behrens_halle_berlin`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Plattenpalast Kleinsthaus / Galerie` (`bw_plattenpalast_berlin`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `rückgebaute WBS70-Plattenbauten` (`bw_unbekannte_wbs70_plattenbauten`)

#### Components and Construction System

**HAT_BAUSYSTEM**
- Project -> `HAT_BAUSYSTEM` -> Bausystem `Plattenbau` (`bsys_plattenbau`)
**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `13 WBS70-Wand- und Deckenelemente` (`bg_reuse_stahlbeton_mehrere_plattenpalast_wbs70_wand_deckenelemente`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Fenster und Rahmen aus dem Palast der Republik` (`bg_reuse_mehrere_mehrere_plattenpalast_palast_fenster`)
**HAT_BAUWEISE**
- Project -> `HAT_BAUWEISE` -> Bauweise `Fertigteilbauweise` (`bauw_fertigteilbauweise`)
**HAT_TRAGWERKSPRINZIP**
- Project -> `HAT_TRAGWERKSPRINZIP` -> Tragwerksprinzip `Wandtragwerk` (`tp_wandtragwerk`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Transport` (`log_transport`)
- Project -> `HAT_LOGISTIK` -> Logistik `Zwischenlagerung` (`log_zwischenlagerung`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Exakte Spezifikations-Übereinstimmung` (`mq_spec_exact`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
- Project -> `HAT_METHODE` -> Methode `Reversibilitaet` (`meth_reversibilitaet`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Aufbereitung` (`phase_aufbereitung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Rueckbau` (`phase_rueckbau`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Transport` (`phase_transport`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Urban_Mining` (`wva_urban_mining`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Akzeptanzproblem` (`h_akzeptanzproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Anschlussproblem` (`h_anschlussproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Toleranzen` (`h_toleranzen`)
**HAT_HUERDEKATEGORIE**
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Logistisch` (`hk_logistisch`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Rechtlich` (`hk_rechtlich`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Sozial_Organisatorisch` (`hk_sozial_organisatorisch`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Technisch` (`hk_technisch`)
**HAT_PRUEFUNG**
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `Beton-Bohrkernprüfung` (`pr_bohrkernpruefung_beton`)
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `Dokumentenprüfung / Herkunfts- und Bestandsnachweis` (`pr_dokumentenpruefung_bestand`)
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `Zerstörende Prüfung (Sammelkategorie)` (`pr_zerstoerende_pruefung`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Forschungsprojekt` (`prog_forschungsprojekt`)

### 72. Plattenvereinigung Berlin

Project ID: `p_plattenvereinigung_berlin`
Reuse-workflow edges: `62`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Bundeszentrale für politische Bildung (bpb)` (`ak_bpb`) -> `BETEILIGT_AN` -> Project
- Akteur `Deutsche Bundesstiftung Umwelt (DBU)` (`ak_deutsche_bundesstiftung_umwelt`) -> `BETEILIGT_AN` -> Project
- Akteur `TU Berlin Fachgebiet Bauphysik und Baukonstruktionen` (`ak_tu_berlin_bauphysik`) -> `BETEILIGT_AN` -> Project
- Akteur `zukunftsgeraeusche GbR` (`ak_zukunftsgeraeusche_gbr`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Olympisches Dorf München` (`bw_olympisches_dorf_muenchen`)
- Project -> `HAS_BAUWERK` -> Bauwerk `PH12-Punkthochhaus Frankfurt/Oder` (`bw_ph12_punkthochhaus_frankfurt_oder`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Peter-Behrens-Halle TU Berlin` (`bw_peter_behrens_halle_tu_berlin`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Plattenvereinigung Recyclinggebäude / Begegnungsraum` (`bw_plattenvereinigung_tempelhofer_feld`)
**HAT_BAUOBJEKTKLASSE**
- Project -> `HAT_BAUOBJEKTKLASSE` -> Bauobjektklasse `Gebaeude` (`bok_gebaeude`)
- Project -> `HAT_BAUOBJEKTKLASSE` -> Bauobjektklasse `Pavillon` (`bok_pavillon`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Translozierung` (`bai_translozierung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Schule_Bildung` (`nut_schule_bildung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Prototyp` (`status_prototyp`)
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
- Project -> `HAT_STATUS` -> Status `Temporaer` (`status_temporaer`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Deutschland` (`land_deutschland`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Berlin` (`stadt_berlin`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Olympisches Dorf München` (`bw_olympisches_dorf_muenchen`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `PH12-Punkthochhaus Frankfurt/Oder` (`bw_ph12_punkthochhaus_frankfurt_oder`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Peter-Behrens-Halle TU Berlin` (`bw_peter_behrens_halle_tu_berlin`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Plattenvereinigung Recyclinggebäude / Begegnungsraum` (`bw_plattenvereinigung_tempelhofer_feld`)

#### Components and Construction System

**HAT_BAUSYSTEM**
- Project -> `HAT_BAUSYSTEM` -> Bausystem `Plattenbau` (`bsys_plattenbau`)
**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Deckenelemente / Zwischendecke` (`bg_reuse_mehrere_decke_plattenvereinigung_deckenelemente`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Ost- und westdeutsche Betonfertigteile` (`bg_reuse_beton_mehrere_plattenvereinigung_betonfertigteile`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Treppenelemente` (`bg_reuse_mehrere_treppe_plattenvereinigung_treppenelemente`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wand- und Fassadenelemente aus Betonfertigteilen` (`bg_reuse_beton_mehrere_plattenvereinigung_wand_fassadenelemente`)
**HAT_BAUWEISE**
- Project -> `HAT_BAUWEISE` -> Bauweise `Fertigteilbauweise` (`bauw_fertigteilbauweise`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transport` (`log_transport`)
- Project -> `HAT_LOGISTIK` -> Logistik `Zwischenlagerung` (`log_zwischenlagerung`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Exakte Spezifikations-Übereinstimmung` (`mq_spec_exact`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Design_for_Disassembly` (`meth_design_for_disassembly`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
- Project -> `HAT_METHODE` -> Methode `Reversibilitaet` (`meth_reversibilitaet`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Betrieb` (`phase_betrieb`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Lagerung` (`phase_lagerung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Rueckbau` (`phase_rueckbau`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Transport` (`phase_transport`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Design_for_Disassembly` (`wva_design_for_disassembly`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Aufbereitungsaufwand` (`h_aufbereitungsaufwand`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Heterogenitaet_Chargen` (`h_heterogenitaet_chargen`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
**HAT_HUERDEKATEGORIE**
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Daten_Evidenz` (`hk_daten_evidenz`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Logistisch` (`hk_logistisch`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Sozial_Organisatorisch` (`hk_sozial_organisatorisch`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Technisch` (`hk_technisch`)
**HAT_PRUEFUNG**
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `Beton-Bohrkernprüfung` (`pr_bohrkernpruefung_beton`)
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `Dokumentenprüfung / Herkunfts- und Bestandsnachweis` (`pr_dokumentenpruefung_bestand`)
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `Zerstörende Prüfung (Sammelkategorie)` (`pr_zerstoerende_pruefung`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx höher, Subvention/Förderung deckt Mehrkosten` (`wi_capex_hoeher_subvention`)
**RELEVANT_FOR**
- ReuseRule `Deutschland × Beton reuse rule` (`rr_de_beton`) -> `RELEVANT_FOR` -> Project
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Forschungsprojekt` (`prog_forschungsprojekt`)

### 73. PLP London HQ circular studio fit-out

Project ID: `p_plp_london_hq_circular_studio_fitout`
Reuse-workflow edges: `61`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Contrax Furniture` (`ak_contrax_furniture`) -> `BETEILIGT_AN` -> Project
- Akteur `Grants of Shoreditch` (`ak_grants_of_shoreditch`) -> `BETEILIGT_AN` -> Project
- Akteur `Maconda` (`ak_maconda`) -> `BETEILIGT_AN` -> Project
- Akteur `Method` (`ak_method_contractor_london`) -> `BETEILIGT_AN` -> Project
- Akteur `PLP Architecture` (`plp_architecture`) -> `BETEILIGT_AN` -> Project
- Akteur `Solus` (`ak_solus`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Michael Polisano` (`michael_polisano`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `PLP Studio im White Chapel Building` (`bw_plp_circular_studio_white_chapel`)
- Project -> `HAS_BAUWERK` -> Bauwerk `The White Chapel Building` (`bw_white_chapel_building_london`)
- Project -> `HAS_BAUWERK` -> Bauwerk `vorheriges PLP Studio / Bestandsfit-out` (`bw_plp_previous_studio_london`)
**HAT_BAUOBJEKTKLASSE**
- Project -> `HAT_BAUOBJEKTKLASSE` -> Bauobjektklasse `Innenausbau` (`bok_innenausbau`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Fit_out` (`bai_fit_out`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Vereinigtes Königreich` (`land_vereinigtes_koenigreich`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `London` (`stadt_london`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `PLP Studio im White Chapel Building` (`bw_plp_circular_studio_white_chapel`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `The White Chapel Building` (`bw_white_chapel_building_london`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `vorheriges PLP Studio / Bestandsfit-out` (`bw_plp_previous_studio_london`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Materialbibliothek-Oberflächen aus Projektmustern` (`bg_reuse_mehrere_ausbau_plp_materialbibliothek_oberflaechen`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Reclaimed marble / feste Oberflächen` (`bg_reuse_naturstein_mehrere_plp_marble_feste_oberflaechen`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Terrazzo-/Spolia-Arbeits- und Küchenflächen` (`bg_reuse_mehrere_mehrere_plp_terrazzo_arbeits_kuechenflaechen`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `wiederverwendete feste Fit-out-Komponenten aus altem/neuem Studio` (`bg_reuse_mehrere_mehrere_plp_feste_fitout_komponenten`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Direktvermittlung` (`bweg_direktvermittlung`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Eigenbestand` (`bweg_eigenbestand`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Bauteiltracking` (`log_bauteiltracking`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Bauteilkatalogisierung` (`meth_bauteilkatalogisierung`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
- Project -> `HAT_METHODE` -> Methode `Pre_Deconstruction_Audit` (`meth_pre_deconstruction_audit`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Aufbereitung` (`phase_aufbereitung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Dokumentation` (`phase_dokumentation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Haendler` (`rq_haendler`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Lager` (`rq_lager`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Bestandserhalt` (`wva_bestandserhalt`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Refurbishment` (`wva_refurbishment`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Upcycling` (`wva_upcycling`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Fehlende_Datenstandards` (`h_fehlende_datenstandards`)
- Project -> `HAT_HUERDE` -> Huerde `Gewaehrleistung` (`h_gewaehrleistung`)
- Project -> `HAT_HUERDE` -> Huerde `Kompatibilitaetsproblem` (`h_kompatibilitaetsproblem`)
**HAT_HUERDEKATEGORIE**
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Daten_Evidenz` (`hk_daten_evidenz`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Technisch` (`hk_technisch`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Wirtschaftlich` (`hk_wirtschaftlich`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFTSASPEKT**
- Project -> `HAT_WIRTSCHAFTSASPEKT` -> Wirtschaft `Kostenvergleich` (`wi_kostenvergleich`)
- Project -> `HAT_WIRTSCHAFTSASPEKT` -> Wirtschaft `Restwert` (`wi_restwert`)
**NUTZT_SOFTWARE**
- Project -> `NUTZT_SOFTWARE` -> Software:Tool `Material passports / Maconda data workflow` (`tool_material_passports_maconda`)
**RELEVANT_FOR**
- ReuseRule `Vereinigtes Königreich × Holz reuse rule` (`rr_gb_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Vereinigtes Königreich × Stahl reuse rule` (`rr_gb_stahl`) -> `RELEVANT_FOR` -> Project

### 74. RCMI / Concular blueprint project

Project ID: `p_rcmi_concular`
Reuse-workflow edges: `1`

#### Actors and Delivery Chain

**STUB_PROJECT_LINK**
- Akteur `Dominik Campanella` (`dominik_campanella`) -> `STUB_PROJECT_LINK` -> Project

### 75. RE-USE Höfe

Project ID: `p_re_use_hoefe`
Reuse-workflow edges: `1`

#### Actors and Delivery Chain

**STUB_PROJECT_LINK**
- Akteur `Félix Dillmann` (`felix_dillmann`) -> `STUB_PROJECT_LINK` -> Project

### 76. Re:Crete footbridge — reused concrete blocks

Project ID: `p_recrete_footbridge_reused_concrete_blocks`
Reuse-workflow edges: `42`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `EPFL Structural Xploration Lab` (`ak_epfl_structural_xploration_lab`) -> `BETEILIGT_AN` -> Project
- Akteur `Re:Crete Forschungsteam` (`ak_recrete_forschungsteam`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Re:Crete Fußgängerbrücken-Prototyp` (`bw_recrete_footbridge_prototype`)
**HAT_BAUOBJEKTKLASSE**
- Project -> `HAT_BAUOBJEKTKLASSE` -> Bauobjektklasse `Infrastruktur` (`bok_infrastruktur`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Infrastruktur` (`nut_infrastruktur`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Prototyp` (`status_prototyp`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Schweiz` (`land_schweiz`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Re:Crete Fußgängerbrücken-Prototyp` (`bw_recrete_footbridge_prototype`)
- Project -> `NUTZT_BAUWERK` -> Materialdepot `unbekanntes Transformationsgebäude mit Ortbeton-Kellerwänden` (`bw_unbekanntes_transformationsgebaeude_kellerwaende`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `25 Betonblöcke / Bogensegmente aus Ortbeton-Kellerwänden` (`bg_reuse_beton_mehrere_recrete_betonbloecke_bogensegmente`)
**HAT_BAUWEISE**
- Project -> `HAT_BAUWEISE` -> Bauweise `Massivbauweise` (`bauw_massivbauweise`)
- Project -> `HAT_BAUWEISE` -> Bauweise `Ortbetonbauweise` (`bauw_ortbetonbauweise`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transport` (`log_transport`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Aufbereitung` (`phase_aufbereitung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Dokumentation` (`phase_dokumentation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Pruefung` (`phase_pruefung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Rueckbau` (`phase_rueckbau`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Transport` (`phase_transport`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Urban_Mining` (`wva_urban_mining`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Materialqualitaet_Unklar` (`h_materialqualitaet_unklar`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Toleranzen` (`h_toleranzen`)
- Project -> `HAT_HUERDE` -> Huerde `Verfuegbarkeitsproblem` (`h_verfuegbarkeitsproblem`)
**HAT_HUERDEKATEGORIE**
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Daten_Evidenz` (`hk_daten_evidenz`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Logistisch` (`hk_logistisch`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Rechtlich` (`hk_rechtlich`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Technisch` (`hk_technisch`)
**HAT_RECHTLICHE_BEDINGUNG**
- Project -> `HAT_RECHTLICHE_BEDINGUNG` -> RechtlicheBedingung `Zulassung_im_Einzelfall` (`rb_zulassung_im_einzelfall`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)

#### Tools, Programmes, and Frameworks

**NUTZT_SOFTWARE**
- Project -> `NUTZT_SOFTWARE` -> Software `Finite-Elemente-Modell / FE-Modell` (`software_recrete_finite_element_model`)
**RELEVANT_FOR**
- ReuseRule `Schweiz × Beton reuse rule` (`rr_ch_beton`) -> `RELEVANT_FOR` -> Project
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Forschungsprojekt` (`prog_forschungsprojekt`)

### 77. Reallabor B(e) Ware

Project ID: `p_reallabor_b_e_ware`
Reuse-workflow edges: `2`

#### Actors and Delivery Chain

**STUB_PROJECT_LINK**
- Akteur `Christof Ziegert` (`christof_ziegert`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Uwe Seiler` (`uwe_seiler`) -> `STUB_PROJECT_LINK` -> Project

### 78. Reallabor B(e) Ware

Project ID: `p_reallabor_be_ware`
Reuse-workflow edges: `8`

#### Actors and Delivery Chain

**STUB_PROJECT_LINK**
- Akteur `Andrea Klinge` (`andrea_klinge`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Eike Roswag-Klinge` (`eike_roswag_klinge`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Matthew Crabbe` (`matthew_crabbe`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `NBL Studio` (`nbl_studio`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Natural Building Lab` (`Natural_Building_Lab`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Nina Pawlicki` (`nina_pawlicki`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Sina Jansen` (`sina_jansen`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `ZRS Architekten Ingenieure` (`ZRS_Architekten_Ingenieure`) -> `STUB_PROJECT_LINK` -> Project

### 79. REBRIDGE structural reuse project

Project ID: `p_rebridge_structural_reuse_project`
Reuse-workflow edges: `1`

#### Actors and Delivery Chain

**STUB_PROJECT_LINK**
- Akteur `Corentin Fivet` (`corentin_fivet`) -> `STUB_PROJECT_LINK` -> Project

### 80. Recyclinghaus Hannover

Project ID: `p_recyclinghaus_hannover`
Reuse-workflow edges: `82`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `CITYFÖRSTER architecture + urbanism` (`ak_cityfoerster`) -> `BETEILIGT_AN` -> Project
- Akteur `DREWES + SPETH Beratende Ingenieure` (`ak_drewes_speth`) -> `BETEILIGT_AN` -> Project
- Akteur `Gundlach GmbH & Co. KG Wohnungsunternehmen` (`ak_gundlach_hannover`) -> `BETEILIGT_AN` -> Project
- Akteur `H2A` (`ak_h2a_hannover`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `CITYFÖRSTER` (`CITYFOERSTER`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Nils Nolting` (`nils_nolting`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Recyclinghaus Hannover / Einfamilienhaus` (`bw_recyclinghaus_hannover`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Sportzentrum / Sauna im Raum Hannover` (`bw_sportzentrum_sauna_hannover`)
- Project -> `HAS_BAUWERK` -> Bauwerk `alte/stillgelegte Lackiererei Hannover` (`bw_alte_lackiererei_hannover`)
- Project -> `HAS_BAUWERK` -> Bauwerk `ehemaliges Haus der Jugend / Jugendzentrum Hannover` (`bw_ehemaliges_haus_der_jugend_hannover`)
**HAT_BAUOBJEKTKLASSE**
- Project -> `HAT_BAUOBJEKTKLASSE` -> Bauobjektklasse `Gebaeude` (`bok_gebaeude`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Prototyp` (`status_prototyp`)
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Deutschland` (`land_deutschland`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Hannover` (`stadt_hannover`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Recyclinghaus Hannover / Einfamilienhaus` (`bw_recyclinghaus_hannover`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Sportzentrum / Sauna im Raum Hannover` (`bw_sportzentrum_sauna_hannover`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `alte/stillgelegte Lackiererei Hannover` (`bw_alte_lackiererei_hannover`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `ehemaliges Haus der Jugend / Jugendzentrum Hannover` (`bw_ehemaliges_haus_der_jugend_hannover`)
- Project -> `NUTZT_BAUWERK` -> Materialdepot `Messebau-Lager / Messebauer Hannover` (`bw_messebau_lager_hannover`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Abbruchziegel in nichttragenden Innenwänden` (`bg_reuse_ziegel_wand_recyclinghaus_abbruchziegel_innenwaende`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Faserzement-/Eternitplatten als Fassadenbekleidung` (`bg_reuse_faserzement_fassade_recyclinghaus_faserzement`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Holzleisten aus alten Saunabänken` (`bg_reuse_holz_mehrere_recyclinghaus_saunabank_holzleisten`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Messebauplatten als Wandverkleidung, Türen und Einbauten` (`bg_reuse_holz_mehrere_recyclinghaus_messebauplatten_innenausbau`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Profilbauglas aus alter Lackiererei` (`bg_reuse_glas_mehrere_recyclinghaus_profilbauglas`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Recyclingbeton in Fundament/Bodenplatte` (`bg_reuse_recyclingbeton_mehrere_recyclinghaus_fundament`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `wiederverwendete Aluminiumfenster mit neuer Verglasung` (`bg_reuse_glas_mehrere_recyclinghaus_aluminiumfenster`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `wiederverwendete Waschbecken / Sanitäreinbauten` (`bg_reuse_mehrere_mehrere_recyclinghaus_sanitaer_feste_einbauten`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `wiederverwendetes Wellblech als Fassadenkomponente` (`bg_reuse_stahl_fassade_recyclinghaus_wellblech`)
**HAT_BAUWEISE**
- Project -> `HAT_BAUWEISE` -> Bauweise `Holzbauweise` (`bauw_holzbauweise`)
- Project -> `HAT_BAUWEISE` -> Bauweise `Hybridbauweise` (`bauw_hybridbauweise`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Eigenbestand` (`bweg_eigenbestand`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Informelles_Netzwerk` (`bweg_informelles_netzwerk`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Lokale_Wiederverwendung` (`log_lokale_wiederverwendung`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transport` (`log_transport`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
- Project -> `HAT_METHODE` -> Methode `Design_for_Disassembly` (`meth_design_for_disassembly`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Aufbereitung` (`phase_aufbereitung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Betrieb` (`phase_betrieb`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Rueckbau` (`phase_rueckbau`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Transport` (`phase_transport`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Lager` (`rq_lager`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Design_for_Disassembly` (`wva_design_for_disassembly`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Recycling` (`wva_recycling`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Upcycling` (`wva_upcycling`)

#### Risk, Checks, and Constraints

**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Korrosion` (`def_korrosion`)
**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Kompatibilitaetsproblem` (`h_kompatibilitaetsproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Schadstoffbelastung` (`h_schadstoffbelastung`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Toleranzen` (`h_toleranzen`)
**HAT_HUERDEKATEGORIE**
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Daten_Evidenz` (`hk_daten_evidenz`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Logistisch` (`hk_logistisch`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Rechtlich` (`hk_rechtlich`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Technisch` (`hk_technisch`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Umwelt_Gesundheit` (`hk_umwelt_gesundheit`)
**HAT_RECHTLICHE_BEDINGUNG**
- Project -> `HAT_RECHTLICHE_BEDINGUNG` -> RechtlicheBedingung `Bauordnungsrecht` (`rb_bauordnungsrecht`)
- Project -> `HAT_RECHTLICHE_BEDINGUNG` -> RechtlicheBedingung `Zulassung_im_Einzelfall` (`rb_zulassung_im_einzelfall`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Asbest` (`s_asbest`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Deutschland × Holz reuse rule` (`rr_de_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Deutschland × Stahl reuse rule` (`rr_de_stahl`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Deutschland × Ziegel reuse rule` (`rr_de_ziegel`) -> `RELEVANT_FOR` -> Project
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Pilotprojekt` (`prog_pilotprojekt`)
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Reallabor` (`prog_reallabor`)

### 81. Recypark Demets / Recypark Anderlecht

Project ID: `p_recypark_demets_anderlecht`
Reuse-workflow edges: `51`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `51N4E` (`51n4e`) -> `BETEILIGT_AN` -> Project
- Akteur `Bruxelles-Propreté / Net Brussel` (`bruxelles_proprete_net_brussel`) -> `BETEILIGT_AN` -> Project
- Akteur `Bureau Greisch` (`bureau_greisch`) -> `BETEILIGT_AN` -> Project
- Akteur `Détang` (`detang`) -> `BETEILIGT_AN` -> Project
- Akteur `Les Marneurs / Janne Saario` (`les_marneurs_janne_saario`) -> `BETEILIGT_AN` -> Project
- Akteur `Rotor` -> `BETEILIGT_AN` -> Project
- Akteur `Witteveen+Bos` (`witteveen_bos`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAT_BAUOBJEKTKLASSE**
- Project -> `HAT_BAUOBJEKTKLASSE` -> Bauobjektklasse `Gebaeude` (`bok_gebaeude`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Infrastruktur` (`nut_infrastruktur`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Belgien` (`land_belgien`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Brüssel / Anderlecht` (`stadt_brussel_anderlecht`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Recypark Demets Hallenstruktur` (`bw_recypark_demets_hallenstruktur`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Brettschichtholzbögen Recypark Demets` (`bg_reuse_holz_mehrere_brettschichtholzbogen_recypark_demets`)
**HAT_BAUWEISE**
- Project -> `HAT_BAUWEISE` -> Bauweise `Holzbauweise` (`bauw_holzbauweise`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Transport` (`log_transport`)
- Project -> `HAT_LOGISTIK` -> Logistik `Zwischenlagerung` (`log_zwischenlagerung`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Aufbereitung` (`phase_aufbereitung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Lagerung` (`phase_lagerung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Pruefung` (`phase_pruefung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Rueckbau` (`phase_rueckbau`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Urban_Mining` (`wva_urban_mining`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Ausschreibungsproblem` (`h_ausschreibungsproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Fehlende_Lagerflaeche` (`h_fehlende_lagerflaeche`)
- Project -> `HAT_HUERDE` -> Huerde `Materialqualitaet_Unklar` (`h_materialqualitaet_unklar`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Verfuegbarkeitsproblem` (`h_verfuegbarkeitsproblem`)
**HAT_HUERDEKATEGORIE**
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Beschaffung_Markt` (`hk_beschaffung_markt`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Logistisch` (`hk_logistisch`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Rechtlich` (`hk_rechtlich`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Technisch` (`hk_technisch`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx höher, Subvention/Förderung deckt Mehrkosten` (`wi_capex_hoeher_subvention`)
**RELEVANT_FOR**
- ReuseRule `Belgien × Holz reuse rule` (`rr_be_holz`) -> `RELEVANT_FOR` -> Project

### 82. REFAIR Bordeaux reuse platform

Project ID: `p_refair_bordeaux_reemploi_platform`
Reuse-workflow edges: `2`

#### Actors and Delivery Chain

**STUB_PROJECT_LINK**
- Akteur `Orianne Scourzic` (`orianne_scourzic`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Tiphaine Berthomé` (`tiphaine_berthome`) -> `STUB_PROJECT_LINK` -> Project

### 83. Resource Rows Copenhagen

Project ID: `p_resource_rows_copenhagen`
Reuse-workflow edges: `46`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Lendager Group / Lendager Architects` (`lendager_group_lendager_architects`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Anders Lendager` (`anders_lendager`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Lendager` -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAT_BAUOBJEKTKLASSE**
- Project -> `HAT_BAUOBJEKTKLASSE` -> Bauobjektklasse `Gebaeude` (`bok_gebaeude`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Dänemark` (`land_daenemark`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Kopenhagen` (`stadt_kopenhagen`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Resource Rows Wohngebäude` (`bw_resource_rows_wohngebaude`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Ziegelfassadenmodule / Mauerwerksausschnitte Resource Rows` (`bg_reuse_ziegel_mehrere_resource_rows_ziegelfassade`)
**HAT_VERBINDUNGSTECHNIK**
- Project -> `HAT_VERBINDUNGSTECHNIK` -> Verbindungstechnik `Stahlrahmen für Fassadenmodul` (`vt_stahlrahmen_fassadenmodul`)

#### Reuse Strategy and Process

**HAT_AUFBEREITUNG**
- Project -> `HAT_AUFBEREITUNG` -> Aufbereitungsverfahren `Mauerwerk-Diamantsägen (Modulausschnitt)` (`av_mauerwerk_diamantsaegen_modul`)
**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transport` (`log_transport`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Aufbereitung` (`phase_aufbereitung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Rueckbau` (`phase_rueckbau`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Transport` (`phase_transport`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Urban_Mining` (`wva_urban_mining`)

#### Risk, Checks, and Constraints

**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Oberflächenmangel / Verfärbung` (`def_oberflaechenmangel`)
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Riss / Rissbildung` (`def_riss`)
**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Anschlussproblem` (`h_anschlussproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Toleranzen` (`h_toleranzen`)
- Project -> `HAT_HUERDE` -> Huerde `Witterung_Feuchte` (`h_witterung_feuchte`)
**HAT_HUERDEKATEGORIE**
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Daten_Evidenz` (`hk_daten_evidenz`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Logistisch` (`hk_logistisch`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Technisch` (`hk_technisch`)
**HAT_PRUEFUNG**
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_ankerpruefung`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_modulstatik`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_schnittplan`
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `pn_transportsicherung`
**REFERENZIERT_NORM**
- Project -> `REFERENZIERT_NORM` -> Norm `DIN_EN_15804` (`norm_din_en_15804`)
- Project -> `REFERENZIERT_NORM` -> Norm `DIN_EN_15978` (`norm_din_en_15978`)

#### Tools, Programmes, and Frameworks

**BERECHNET_NACH_MODUL**
- Project -> `BERECHNET_NACH_MODUL` -> LCAModule `B1-B7 Nutzung` (`lz_b`)
- Project -> `BERECHNET_NACH_MODUL` -> LCAModule `D Beyond (Reuse)` (`lz_d`)

### 84. Roots in the Sky / Blackfriars Crown Court

Project ID: `p_roots_in_the_sky_blackfriars_crown_court`
Reuse-workflow edges: `57`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `AKT II` (`akt_ii`) -> `BETEILIGT_AN` -> Project
- Akteur `Erith` (`erith`) -> `BETEILIGT_AN` -> Project
- Akteur `Fabrix London` (`fabrix_london`) -> `BETEILIGT_AN` -> Project
- Akteur `Howells` (`howells`) -> `BETEILIGT_AN` -> Project
- Akteur `Mace` (`mace`) -> `BETEILIGT_AN` -> Project
- Akteur `Sheppard Robson` (`sheppard_robson`) -> `BETEILIGT_AN` -> Project
- Akteur `Southwark Council` (`southwark_council`) -> `BETEILIGT_AN` -> Project
- Akteur `Studio RHE` (`studio_rhe`) -> `BETEILIGT_AN` -> Project
- Akteur `Symmetrys` (`symmetrys`) -> `BETEILIGT_AN` -> Project
- Akteur `iQ Student Accommodation` (`iq_student_accommodation`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAT_BAUOBJEKTKLASSE**
- Project -> `HAT_BAUOBJEKTKLASSE` -> Bauobjektklasse `Gebaeude` (`bok_gebaeude`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Aufstockung` (`bai_aufstockung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Mischnutzung` (`nut_mischnutzung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Geplant` (`status_geplant`)
- Project -> `HAT_STATUS` -> Status `Verworfen` (`status_verworfen`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Vereinigtes Königreich` (`land_vereinigtes_koenigreich`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `London` (`stadt_london`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Blackfriars Crown Court / geplantes Roots Empfängerbauwerk` (`bw_blackfriars_crown_court_geplantes_roots_empfangerbauwerk`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Bestandsfundamente und erste Geschosse Blackfriars` (`bg_reuse_mehrere_mehrere_bestandsfundamente_und_erste_geschosse_blackfriars`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Geplante Stahlträger / Stahlprofile Roots` (`bg_reuse_stahl_mehrere_geplante_stahltrager_roots`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Direktvermittlung` (`bweg_direktvermittlung`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Materialverfuegbarkeit` (`log_materialverfuegbarkeit`)
- Project -> `HAT_LOGISTIK` -> Logistik `Zwischenlagerung` (`log_zwischenlagerung`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch geplante Beschaffung` (`mq_temporal_planned`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Pre_Deconstruction_Audit` (`meth_pre_deconstruction_audit`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
- Project -> `HAT_METHODE` -> Methode `Urban_Mining` (`meth_urban_mining`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Lagerung` (`phase_lagerung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Planung` (`phase_planung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Pruefung` (`phase_pruefung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Transport` (`phase_transport`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Adaptives_ReUse` (`wva_adaptives_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Bestandserhalt` (`wva_bestandserhalt`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Bauproduktstatus` (`h_bauproduktstatus`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Haftung` (`h_haftung`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Terminunsicherheit` (`h_terminunsicherheit`)
- Project -> `HAT_HUERDE` -> Huerde `Verfuegbarkeitsproblem` (`h_verfuegbarkeitsproblem`)
**HAT_HUERDEKATEGORIE**
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Beschaffung_Markt` (`hk_beschaffung_markt`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Logistisch` (`hk_logistisch`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Rechtlich` (`hk_rechtlich`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Technisch` (`hk_technisch`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Wirtschaftlich` (`hk_wirtschaftlich`)
**HAT_RECHTLICHE_BEDINGUNG**
- Project -> `HAT_RECHTLICHE_BEDINGUNG` -> RechtlicheBedingung `Bauordnungsrecht` (`rb_bauordnungsrecht`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFTSASPEKT**
- Project -> `HAT_WIRTSCHAFTSASPEKT` -> Wirtschaft `Finanzierung` (`wi_finanzierung`)
**RELEVANT_FOR**
- ReuseRule `Vereinigtes Königreich × Stahl reuse rule` (`rr_gb_stahl`) -> `RELEVANT_FOR` -> Project

### 85. Résilience / La Ferme des Possibles Stains

Project ID: `p_resilience_la_ferme_des_possibles_stains`
Reuse-workflow edges: `70`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Association Réavie` (`association_reavie`) -> `BETEILIGT_AN` -> Project
- Akteur `Bellastock — French reuse architecture/research collective (FCRBE partner)` (`bellastock`) -> `BETEILIGT_AN` -> Project
- Akteur `Depuis 1920` (`depuis_1920`) -> `BETEILIGT_AN` -> Project
- Akteur `Frédéric Denise / Archipel Zéro` (`frederic_denise_archipel_zero`) -> `BETEILIGT_AN` -> Project
- Akteur `Métabolisme Urbain` (`metabolisme_urbain`) -> `BETEILIGT_AN` -> Project
- Akteur `Novaedia / Novædia` (`novaedia_novaedia`) -> `BETEILIGT_AN` -> Project
- Akteur `SOCOTEC` (`socotec`) -> `BETEILIGT_AN` -> Project
- Akteur `Terraterre` (`terraterre`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Archipel zéro` (`archipel_zero`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Bellastock — French reuse architecture/research collective (FCRBE partner)` (`bellastock`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Frédéric Denise` (`frederic_denise`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAT_BAUOBJEKTKLASSE**
- Project -> `HAT_BAUOBJEKTKLASSE` -> Bauobjektklasse `Gebaeude` (`bok_gebaeude`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Sozialbau` (`nut_sozialbau`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Frankreich` (`land_frankreich`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Stains` (`stadt_stains`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Résilience Betriebs- und Bürogebäude` (`bw_resilience_betriebs_und_burogebaude`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `BTC-Ziegel Mur Trombe Résilience` (`bg_reuse_lehm_mehrere_btc_ziegel_mur_trombe_resilience`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Doppeltverglaste Holzfenster Résilience` (`bg_reuse_holz_fenster_doppeltverglaste_holzfenster_resilience`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Einfachverglaste Holzfenster Résilience` (`bg_reuse_holz_mehrere_einfachverglaste_holzfenster_resilience`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Granitpflaster Résilience` (`bg_reuse_naturstein_boden_granitpflaster_resilience`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Gussradiatoren Résilience` (`bg_reuse_gusseisen_technik_gussradiatoren_resilience`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Leuchten Résilience` (`bg_reuse_mehrere_technik_leuchten_resilience`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Sanitärobjekte Résilience` (`bg_reuse_keramik_technik_sanitarobjekte_resilience`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Digitale_Plattform` (`bweg_digitale_plattform`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Direktvermittlung` (`bweg_direktvermittlung`)
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Rueckbauprojekt` (`bweg_rueckbauprojekt`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Lokale_Wiederverwendung` (`log_lokale_wiederverwendung`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
- Project -> `HAT_LOGISTIK` -> Logistik `Zwischenlagerung` (`log_zwischenlagerung`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Aufbereitung` (`phase_aufbereitung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Lagerung` (`phase_lagerung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Pruefung` (`phase_pruefung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Rueckbau` (`phase_rueckbau`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Bauteilboerse` (`rq_bauteilboerse`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donorgebaeude` (`rq_donorgebaeude`)
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Lager` (`rq_lager`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Upcycling` (`wva_upcycling`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Urban_Mining` (`wva_urban_mining`)

#### Risk, Checks, and Constraints

**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Verformung / Setzung / Verzug` (`def_verformung`)
**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Gewaehrleistung` (`h_gewaehrleistung`)
- Project -> `HAT_HUERDE` -> Huerde `Heterogenitaet_Chargen` (`h_heterogenitaet_chargen`)
- Project -> `HAT_HUERDE` -> Huerde `Hygieneanforderung` (`h_hygieneanforderung`)
- Project -> `HAT_HUERDE` -> Huerde `Kompatibilitaetsproblem` (`h_kompatibilitaetsproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
**HAT_HUERDEKATEGORIE**
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Daten_Evidenz` (`hk_daten_evidenz`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Logistisch` (`hk_logistisch`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Rechtlich` (`hk_rechtlich`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Technisch` (`hk_technisch`)
**REFERENZIERT_NORM**
- Project -> `REFERENZIERT_NORM` -> Norm `RT 2012` (`norm_rt_2012`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**NUTZT_SOFTWARE**
- Project -> `NUTZT_SOFTWARE` -> Software `INIES` (`software_inies`)

### 86. Saxum Vineyard Equipment Barn

Project ID: `p_saxum_vineyard_equipment_barn_paso_robles`
Reuse-workflow edges: `45`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Clayton & Little / Clayton Korte` (`clayton_little_clayton_korte`) -> `BETEILIGT_AN` -> Project
- Akteur `Pacific Energy Company` (`pacific_energy_company`) -> `BETEILIGT_AN` -> Project
- Akteur `Rarig Construction` (`rarig_construction`) -> `BETEILIGT_AN` -> Project
- Akteur `SSG Structural Engineers` (`ssg_structural_engineers`) -> `BETEILIGT_AN` -> Project
- Akteur `Saxum Vineyards` (`saxum_vineyards`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAT_BAUOBJEKTKLASSE**
- Project -> `HAT_BAUOBJEKTKLASSE` -> Bauobjektklasse `Depot_Lager` (`bok_depot_lager`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Lager_Depot` (`nut_lager_depot`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `USA` (`land_usa`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Paso Robles / Templeton Gap` (`stadt_paso_robles_templeton_gap`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Saxum Vineyard Equipment Barn` (`bw_saxum_vineyard_equipment_barn`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Drill-Stem-Pipe Dachtragwerk Saxum` (`bg_reuse_stahl_mehrere_drill_stem_pipe_dachtragwerk_saxum`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Drill-Stem-Pipe Stützen Saxum` (`bg_reuse_stahl_stuetze_drill_stem_pipe_stutzen_saxum`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wetternde Stahl-Offcut-Tore Saxum` (`bg_reuse_stahl_mehrere_wetternde_offcut_tore_saxum`)
**HAT_BAUWEISE**
- Project -> `HAT_BAUWEISE` -> Bauweise `Stahlbauweise` (`bauw_stahlbauweise`)
**HAT_TRAGWERKSPRINZIP**
- Project -> `HAT_TRAGWERKSPRINZIP` -> Tragwerksprinzip `Skeletttragwerk` (`tp_skeletttragwerk`)

#### Reuse Strategy and Process

**HAT_BESCHAFFUNGSWEG**
- Project -> `HAT_BESCHAFFUNGSWEG` -> Beschaffungsweg `Direktvermittlung` (`bweg_direktvermittlung`)
**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Lokale_Wiederverwendung` (`log_lokale_wiederverwendung`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialverfuegbarkeit` (`log_materialverfuegbarkeit`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `International / interkontinental` (`mq_geographic_intl`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
**HAT_PROZESSPHASE**
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Aufbereitung` (`phase_aufbereitung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Identifikation` (`phase_identifikation`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Planung` (`phase_planung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Pruefung` (`phase_pruefung`)
- Project -> `HAT_PROZESSPHASE` -> Prozessphase `Wiedereinbau` (`phase_wiedereinbau`)
**HAT_RESSOURCENQUELLE**
- Project -> `HAT_RESSOURCENQUELLE` -> Ressourcenquelle `Donor_Infrastruktur` (`rq_donor_infrastruktur`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Upcycling` (`wva_upcycling`)

#### Risk, Checks, and Constraints

**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Korrosion` (`def_korrosion`)
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Verformung / Setzung / Verzug` (`def_verformung`)
**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Anschlussproblem` (`h_anschlussproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Materialqualitaet_Unklar` (`h_materialqualitaet_unklar`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Toleranzen` (`h_toleranzen`)
- Project -> `HAT_HUERDE` -> Huerde `Unkonventionelles_Material` (`h_unkonventionelles_material`)
**HAT_HUERDEKATEGORIE**
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Daten_Evidenz` (`hk_daten_evidenz`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Rechtlich` (`hk_rechtlich`)
- Project -> `HAT_HUERDEKATEGORIE` -> HuerdeKategorie `Technisch` (`hk_technisch`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**NUTZT_SOFTWARE**
- Project -> `NUTZT_SOFTWARE` -> Software `RISA-3D` (`software_risa_3d`)

### 87. Schärenmoosstrasse 115/117 Zürich — ménage à trois (Stiftung PWG Wettbewerb 2022)

Project ID: `p_schaerenmoosstrasse_zuerich`
Reuse-workflow edges: `35`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Andreas Geser Landschaftsarchitekten AG` (`andreas_geser_landschaftsarchitekten`) -> `BETEILIGT_AN` -> Project
- Akteur `Andreas Geser — landscape architecture lead at AG Landschaftsarch.` (`andreas_geser`) -> `BETEILIGT_AN` -> Project
- Akteur `Michael Schmidlin — Bauingenieur Mitarbeit at Pérez Schmidlin` (`michael_schmidlin`) -> `BETEILIGT_AN` -> Project
- Akteur `Pérez Schmidlin Bauingenieure GmbH — structural engineer` (`perez_schmidlin_bauingenieure`) -> `BETEILIGT_AN` -> Project
- Akteur `Stefan Pérez — Bauingenieur Mitarbeit at Pérez Schmidlin` (`stefan_perez`) -> `BETEILIGT_AN` -> Project
- Akteur `Stiftung PWG — Schärenmoosstrasse Wettbewerb Bauherrschaft` (`stiftung_pwg`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Daniel Hoffmann` (`daniel_hoffmann`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Gian Trachsler` (`gian_trachsler`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Studio Trachsler Hoffmann` (`studio_trachsler_hoffmann`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Schärenmoosstrasse 115/117 Zürich — Umnutzung Büro zu Wohnen (Stiftung PWG Wettbewerb 2022)` (`bw_schaerenmoosstrasse_zuerich`)
- Project -> `HAS_BAUWERK` -> Bauwerk `UBS Datenzentrum Altstetten, Zürich — donor for SMS Zürich hall components` (`bw_ubs_altstetten`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umnutzung` (`bai_umnutzung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Schweiz` (`land_schweiz`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Zürich` (`stadt_zuerich`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Schärenmoosstrasse 115/117 Zürich — Umnutzung Büro zu Wohnen (Stiftung PWG Wettbewerb 2022)` (`bw_schaerenmoosstrasse_zuerich`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `SMS Zürich — Existing stair cores retained` (`bg_retained_stahlbeton_treppe_sms_zuerich_existing_stairs`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `SMS Zürich — Photovoltaic system, 250 m² PV roof array` (`bg_planned_mehrere_technik_sms_zuerich_pv_roof`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `SMS Zürich — Self-supporting steel arcade / Laubengang` (`bg_planned_stahl_fassade_sms_zuerich_arcade`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `SMS Zürich — Two-storey communal hall from UBS Datenzentrum Altstetten` (`bg_reuse_mehrere_mehrere_sms_zuerich_ubs_hall`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `SMS Zürich — existing Micro+Dixa buildings retained in place` (`bg_retained_mehrere_mehrere_sms_zuerich_existing_bldgs`)

#### Reuse Strategy and Process

**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Dauerhaftigkeit_Restlebensdauer` (`h_dauerhaftigkeit_restlebensdauer`)
- Project -> `HAT_HUERDE` -> Huerde `Entwurfsbindung` (`h_entwurfsbindung`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Toleranzen` (`h_toleranzen`)
- Project -> `HAT_HUERDE` -> Huerde `Zustand_Unklar` (`h_zustand_unklar`)
**REFERENZIERT_NORM**
- Project -> `REFERENZIERT_NORM` -> Norm `SIA 261 — Einwirkungen auf Tragwerke (Switzerland seismic+actions standard)` (`norm_sia_261`)
- Project -> `REFERENZIERT_NORM` -> Norm `SIA 500 — Hindernisfreie Bauten / barrier-free construction` (`norm_sia_500`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx höher, Payback über OpEx / LCA` (`wi_capex_hoeher_opex_payback`)
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx höher, Subvention/Förderung deckt Mehrkosten` (`wi_capex_hoeher_subvention`)
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Stiftung PWG Wettbewerb Schärenmoosstrasse (2022)` (`prog_stiftung_pwg`)

### 88. Stuttgart 210

Project ID: `p_stuttgart_210`
Reuse-workflow edges: `7`

#### Actors and Delivery Chain

**STUB_PROJECT_LINK**
- Akteur `HFT Stuttgart` (`hft_stuttgart`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `HTWG Konstanz` (`htwg_konstanz`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Katharina Raabe` (`katharina_raabe`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Klingelhöfer Krötsch` (`klingelhoefer_kroetsch`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Maximilian Stemmler` (`maximilian_stemmler`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Roman Kreuzer` (`roman_kreuzer`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Thomas Stark` (`thomas_stark`) -> `STUB_PROJECT_LINK` -> Project

### 89. SUPERLOCAL Expogebouw / Superlocal Pavilion

Project ID: `p_superlocal_expogebouw_bleijerheide`
Reuse-workflow edges: `52`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Bouwbedrijven Jongen` (`bouwbedrijven_jongen`) -> `BETEILIGT_AN` -> Project
- Akteur `Dusseldorp` (`dusseldorp`) -> `BETEILIGT_AN` -> Project
- Akteur `Gemeente Kerkrade` (`gemeente_kerkrade`) -> `BETEILIGT_AN` -> Project
- Akteur `HEEMwonen` (`heemwonen`) -> `BETEILIGT_AN` -> Project
- Akteur `IBA Parkstad` (`iba_parkstad`) -> `BETEILIGT_AN` -> Project
- Akteur `Maurer United` (`maurer_united`) -> `BETEILIGT_AN` -> Project
- Akteur `Volantis` (`volantis`) -> `BETEILIGT_AN` -> Project
- Akteur `Zuyd Hogeschool` (`zuyd_hogeschool`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Expogebouw / Superlocal Pavilion` (`bw_superlocal_expogebouw`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Hochhausflat Ursulastraat` (`bw_hochhausflat_ursulastraat`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Translozierung` (`bai_translozierung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Mischnutzung` (`nut_mischnutzung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Prototyp` (`status_prototyp`)
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Niederlande` (`land_niederlande`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Bleijerheide / Kerkrade` (`stadt_bleijerheide_kerkrade`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Expogebouw / Superlocal Pavilion` (`bw_superlocal_expogebouw`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Hochhausflat Ursulastraat` (`bw_hochhausflat_ursulastraat`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Drei Beton-Wohnungsteile / Großmodule` (`bg_reuse_mehrere_mehrere_superlocal_beton_wohnungsteile`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Fensterrahmen / Kozijnen` (`bg_reuse_mehrere_mehrere_superlocal_fenster_kozijnen`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Feste Küche und Installationen` (`bg_reuse_mehrere_mehrere_superlocal_feste_kueche_installationen`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Haustüren, Geländer und Brüstungen` (`bg_reuse_mehrere_mehrere_superlocal_haustueren_gelaender_bruestungen`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Heizkörper und Aluminiumrohre` (`bg_reuse_mehrere_technik_superlocal_tga_heizkoerper_aluminiumrohre`)

#### Reuse Strategy and Process

**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Bauteiltracking` (`log_bauteiltracking`)
- Project -> `HAT_LOGISTIK` -> Logistik `Lokale_Wiederverwendung` (`log_lokale_wiederverwendung`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transport` (`log_transport`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
- Project -> `HAT_METHODE` -> Methode `Urban_Mining` (`meth_urban_mining`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Same_Site_ReUse` (`wva_same_site_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Urban_Mining` (`wva_urban_mining`)

#### Risk, Checks, and Constraints

**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Riss / Rissbildung` (`def_riss`)
**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Bruch_Beschaedigungsrisiko` (`h_bruch_beschaedigungsrisiko`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Schadstoffbelastung` (`h_schadstoffbelastung`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**ERHALT_FOERDERUNG_DURCH**
- Project -> `ERHALT_FOERDERUNG_DURCH` -> Programm `Urban Innovative Actions (UIA, EU)` (`prog_urban_innovative_actions`)
**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx höher, Subvention/Förderung deckt Mehrkosten` (`wi_capex_hoeher_subvention`)
**RELEVANT_FOR**
- ReuseRule `Niederlande × Beton reuse rule` (`rr_nl_beton`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Niederlande × Holz reuse rule` (`rr_nl_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Niederlande × Stahl reuse rule` (`rr_nl_stahl`) -> `RELEVANT_FOR` -> Project

### 90. Svanen / The Swan Kindergarten Gladsaxe

Project ID: `p_svanen_kindergarten_gladsaxe`
Reuse-workflow edges: `49`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Aksel V. Jensen A/S` (`aksel_v_jensen`) -> `BETEILIGT_AN` -> Project
- Akteur `Ason A/S` (`ason_as`) -> `BETEILIGT_AN` -> Project
- Akteur `Gladsaxe Kommune / Gladsaxe Municipality` (`gladsaxe_kommune`) -> `BETEILIGT_AN` -> Project
- Akteur `Lendager` -> `BETEILIGT_AN` -> Project
- Akteur `NIRAS` (`niras`) -> `BETEILIGT_AN` -> Project
- Akteur `Sweco / Sweco Architects` (`sweco_architects`) -> `BETEILIGT_AN` -> Project
- Akteur `Tscherning` (`tscherning`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Børnehuset Svanen / The Swan Kindergarten` (`bw_svanen_kindergarten`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Ehemalige Gladsaxe School` (`bw_ehemalige_gladsaxe_school`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Rueckbau` (`bai_rueckbau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Schule_Bildung` (`nut_schule_bildung`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Sozialbau` (`nut_sozialbau`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Dänemark` (`land_daenemark`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Gladsaxe` (`stadt_gladsaxe`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Børnehuset Svanen / The Swan Kindergarten` (`bw_svanen_kindergarten`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Ehemalige Gladsaxe School` (`bw_ehemalige_gladsaxe_school`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Holz-Dachbinder / timber trusses` (`bg_reuse_holz_mehrere_svanen_dachbinder`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Holzrafters / træspær` (`bg_reuse_holz_mehrere_svanen_sparren`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Stahlfassadenelemente` (`bg_reuse_stahl_fassade_svanen_stahlfassadenelemente`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Dachziegel / roof tiles` (`bg_reuse_keramik_mehrere_svanen_dachziegel`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Ziegel / bricks` (`bg_reuse_ziegel_mehrere_svanen`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Zerkleinerter Beton als Recycling-Zuschlag` (`bg_reuse_mehrere_mehrere_svanen_beton_recycling_zuschlag`)

#### Reuse Strategy and Process

**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Lagerung` (`log_lagerung`)
- Project -> `HAT_LOGISTIK` -> Logistik `Lokale_Wiederverwendung` (`log_lokale_wiederverwendung`)
- Project -> `HAT_LOGISTIK` -> Logistik `Zwischenlagerung` (`log_zwischenlagerung`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
- Project -> `HAT_METHODE` -> Methode `Pre_Deconstruction_Audit` (`meth_pre_deconstruction_audit`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Ausschreibung` (`meth_reuse_ausschreibung`)
- Project -> `HAT_METHODE` -> Methode `Urban_Mining` (`meth_urban_mining`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Recycling` (`wva_recycling`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Same_Site_ReUse` (`wva_same_site_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Urban_Mining` (`wva_urban_mining`)

#### Risk, Checks, and Constraints

**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Korrosion` (`def_korrosion`)
**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Bruch_Beschaedigungsrisiko` (`h_bruch_beschaedigungsrisiko`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Schadstoffbelastung` (`h_schadstoffbelastung`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_ZERTIFIZIERUNG**
- Project -> `HAT_ZERTIFIZIERUNG` -> Zertifizierungssystem `Nordic Swan Ecolabel` (`zbs_nordic_swan_ecolabel`)

### 91. The Green House Utrecht

Project ID: `p_the_green_house_utrecht`
Reuse-workflow edges: `53`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Ballast Nedam` (`ballast_nedam`) -> `BETEILIGT_AN` -> Project
- Akteur `De Groot & Visser` (`de_groot_en_visser`) -> `BETEILIGT_AN` -> Project
- Akteur `Kampstaal` (`kampstaal`) -> `BETEILIGT_AN` -> Project
- Akteur `Pieters Bouwtechniek` (`pieters_bouwtechniek`) -> `BETEILIGT_AN` -> Project
- Akteur `R Creators` (`r_creators`) -> `BETEILIGT_AN` -> Project
- Akteur `Rijksvastgoedbedrijf / Central Government Real Estate Agency` (`rijksvastgoedbedrijf`) -> `BETEILIGT_AN` -> Project
- Akteur `Strukton Worksphere` (`strukton_worksphere`) -> `BETEILIGT_AN` -> Project
- Akteur `cepezed` -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Alte Kade in Tiel` (`bw_alte_kade_tiel`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Ehemalige Knoopkazerne` (`bw_knoopkazerne_utrecht`)
- Project -> `HAS_BAUWERK` -> Bauwerk `The Green House Utrecht` (`bw_the_green_house_utrecht`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umnutzung` (`bai_umnutzung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Mischnutzung` (`nut_mischnutzung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
- Project -> `HAT_STATUS` -> Status `Temporaer` (`status_temporaer`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Niederlande` (`land_niederlande`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Utrecht` (`stadt_utrecht`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Alte Kade in Tiel` (`bw_alte_kade_tiel`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Ehemalige Knoopkazerne` (`bw_knoopkazerne_utrecht`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `The Green House Utrecht` (`bw_the_green_house_utrecht`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Dämmung in Holzbodenelementen` (`bg_reuse_daemmstoff_mehrere_green_house_daemmung_holzbodenelemente`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Neues demontierbares Stahltragwerk` (`bg_reuse_stahl_mehrere_green_house_demontables_stahltragwerk`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Pflasterklinker Erdgeschoss` (`bg_reuse_mehrere_boden_green_house_pflasterklinker`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Pre-used wood Geschossdecke` (`bg_reuse_holz_mehrere_green_house_preused_holzdecke`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Rauchglas-Fassadenpaneele` (`bg_reuse_glas_mehrere_green_house_rauchglas_fassade`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete feste Wandverkleidung / wainscot` (`bg_reuse_holz_mehrere_green_house_feste_wandverkleidung`)

#### Reuse Strategy and Process

**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Materialverfuegbarkeit` (`log_materialverfuegbarkeit`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transport` (`log_transport`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Design_for_Disassembly` (`meth_design_for_disassembly`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Reversibilitaet` (`meth_reversibilitaet`)
- Project -> `HAT_METHODE` -> Methode `Urban_Mining` (`meth_urban_mining`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Design_for_Disassembly` (`wva_design_for_disassembly`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Urban_Mining` (`wva_urban_mining`)

#### Risk, Checks, and Constraints

**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Verformung / Setzung / Verzug` (`def_verformung`)
**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Entwurfsbindung` (`h_entwurfsbindung`)
- Project -> `HAT_HUERDE` -> Huerde `Kompatibilitaetsproblem` (`h_kompatibilitaetsproblem`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Asbest` (`s_asbest`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `KMF — Künstliche Mineralfasern (alte Mineralwolle vor 1996/2000)` (`s_kmf`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Niederlande × Holz reuse rule` (`rr_nl_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Niederlande × Stahl reuse rule` (`rr_nl_stahl`) -> `RELEVANT_FOR` -> Project

### 92. Thoravej 29 Copenhagen

Project ID: `p_thoravej_29_copenhagen`
Reuse-workflow edges: `50`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `ABC Rådgivende Ingeniører / ABC Consulting Engineers` (`abc_raadgivende_ingenioerer`) -> `BETEILIGT_AN` -> Project
- Akteur `Bikubenfonden / The Bikuben Foundation` (`bikubenfonden`) -> `BETEILIGT_AN` -> Project
- Akteur `DTU` (`dtu`) -> `BETEILIGT_AN` -> Project
- Akteur `Hoffmann A/S` (`hoffmann_as`) -> `BETEILIGT_AN` -> Project
- Akteur `Pihlmann Architects` (`pihlmann_architects`) -> `BETEILIGT_AN` -> Project
- Akteur `Sara Martinsen` (`sara_martinsen`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Pihlmann Architects` (`pihlmann_architects`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Søren Pihlmann` (`soren_pihlmann`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Thoravej 29 Bestandsgebäude` (`bw_thoravej_29`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Thoravej 29 Bestandsgebäude` (`bw_thoravej_29`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Sanierung` (`bai_sanierung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umnutzung` (`bai_umnutzung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Mischnutzung` (`nut_mischnutzung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Dänemark` (`land_daenemark`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Kopenhagen` (`stadt_kopenhagen`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Thoravej 29 Bestandsgebäude` (`bw_thoravej_29`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Fassaden-/Ziegelüberschuss zu Boden/Pflaster` (`bg_reuse_ziegel_mehrere_thoravej_fassade_zu_boden`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Kunststofffenster im Bestand` (`bg_reuse_mehrere_mehrere_thoravej_kunststofffenster_bestand`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `TT-/Betondecken zu Treppen` (`bg_reuse_mehrere_mehrere_thoravej_tt_decken_zu_treppen`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Türen zu Tischplatten / Möbelgrenze` (`bg_reuse_holz_mehrere_thoravej_tueren_zu_tischplatten`)

#### Reuse Strategy and Process

**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Lagerung` (`log_lagerung`)
- Project -> `HAT_LOGISTIK` -> Logistik `Lokale_Wiederverwendung` (`log_lokale_wiederverwendung`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
- Project -> `HAT_METHODE` -> Methode `Reversibilitaet` (`meth_reversibilitaet`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Adaptives_ReUse` (`wva_adaptives_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Bestandserhalt` (`wva_bestandserhalt`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Same_Site_ReUse` (`wva_same_site_reuse`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Dauerhaftigkeit_Restlebensdauer` (`h_dauerhaftigkeit_restlebensdauer`)
- Project -> `HAT_HUERDE` -> Huerde `Entwurfsbindung` (`h_entwurfsbindung`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
**REFERENZIERT_NORM**
- Project -> `REFERENZIERT_NORM` -> Norm `DIN_EN_15804` (`norm_din_en_15804`)
- Project -> `REFERENZIERT_NORM` -> Norm `DIN_EN_15978` (`norm_din_en_15978`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**BERECHNET_NACH_MODUL**
- Project -> `BERECHNET_NACH_MODUL` -> LCAModule `D Beyond (Reuse)` (`lz_d`)
**HAT_ZERTIFIZIERUNG**
- Project -> `HAT_ZERTIFIZIERUNG` -> Zertifizierungssystem `DGNB` (`zbs_dgnb`)

### 93. Timber Square London

Project ID: `p_timber_square_london`
Reuse-workflow edges: `60`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Alinea / T+T Alinea` (`alinea_tt_alinea`) -> `BETEILIGT_AN` -> Project
- Akteur `Bennetts Associates` (`bennetts_associates`) -> `BETEILIGT_AN` -> Project
- Akteur `Cleveland Steel & Tubes` (`cleveland_steel_tubes`) -> `BETEILIGT_AN` -> Project
- Akteur `Heyne Tillett Steel / HTS` (`heyne_tillett_steel`) -> `BETEILIGT_AN` -> Project
- Akteur `Hoare Lea` (`hoare_lea`) -> `BETEILIGT_AN` -> Project
- Akteur `Hybrid Structures` (`hybrid_structures`) -> `BETEILIGT_AN` -> Project
- Akteur `Landsec` (`landsec`) -> `BETEILIGT_AN` -> Project
- Akteur `Mace` (`mace`) -> `BETEILIGT_AN` -> Project
- Akteur `Opera` (`opera`) -> `BETEILIGT_AN` -> Project
- Akteur `Stora Enso` (`stora_enso`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Timber Square Ink Building` (`bw_timber_square_ink_building`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Timber Square Print Building` (`bw_timber_square_print_building`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Timber Square Print Building` (`bw_timber_square_print_building`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Aufstockung` (`bai_aufstockung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Mischnutzung` (`nut_mischnutzung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `In_Bau` (`status_in_bau`)
- Project -> `HAT_STATUS` -> Status `Unklar` (`status_unklar`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Vereinigtes Königreich` (`land_vereinigtes_koenigreich`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `London` (`stadt_london`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Timber Square Ink Building` (`bw_timber_square_ink_building`)
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Timber Square Print Building` (`bw_timber_square_print_building`)
- Project -> `NUTZT_BAUWERK` -> Materialdepot `Externe Stahl-Donorquellen / Cleveland Steel & Tubes stock` (`bw_externe_stahl_donor_stockholder`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `CLT-Hybriddecken als Kontextbauteil` (`bg_reuse_holz_mehrere_square_clt_hybrid_decken`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Demontierbare TGA-/Plant-Komponenten` (`bg_reuse_stahl_technik_timber_square_demontable_plant`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Retained Print Building Structure` (`bg_retained_mehrere_mehrere_timber_square_print_building_structure`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendete Stahlträger` (`bg_reuse_stahl_traeger_timber_square`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Wiederverwendeter Stahlträger als Empfangstresen` (`bg_reuse_stahl_mehrere_timber_square_reception_girder`)

#### Reuse Strategy and Process

**HAT_LOGISTIK**
- Project -> `HAT_LOGISTIK` -> Logistik `Materialmatching` (`log_materialmatching`)
- Project -> `HAT_LOGISTIK` -> Logistik `Materialverfuegbarkeit` (`log_materialverfuegbarkeit`)
- Project -> `HAT_LOGISTIK` -> Logistik `Transport` (`log_transport`)
**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
- Project -> `HAT_METHODE` -> Methode `Design_for_Disassembly` (`meth_design_for_disassembly`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Bestandserhalt` (`wva_bestandserhalt`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Design_for_Disassembly` (`wva_design_for_disassembly`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Urban_Mining` (`wva_urban_mining`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Brandschutzkonflikt` (`h_brandschutzkonflikt`)
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Mengenunsicherheit` (`h_mengenunsicherheit`)
- Project -> `HAT_HUERDE` -> Huerde `Technische_Freigabe` (`h_technische_freigabe`)
- Project -> `HAT_HUERDE` -> Huerde `Verfuegbarkeitsproblem` (`h_verfuegbarkeitsproblem`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_ZERTIFIZIERUNG**
- Project -> `HAT_ZERTIFIZIERUNG` -> Zertifizierungssystem `BREEAM` (`zbs_breeam`)
- Project -> `HAT_ZERTIFIZIERUNG` -> Zertifizierungssystem `NABERS` (`zbs_nabers`)
- Project -> `HAT_ZERTIFIZIERUNG` -> Zertifizierungssystem `WELL` (`zbs_well`)
**NUTZT_SOFTWARE**
- Project -> `NUTZT_SOFTWARE` -> Software:Tool `HTS Reused Steel Stockmatcher` (`tool_hts_stockmatcher`)
**RELEVANT_FOR**
- ReuseRule `Vereinigtes Königreich × Holz reuse rule` (`rr_gb_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Vereinigtes Königreich × Stahl reuse rule` (`rr_gb_stahl`) -> `RELEVANT_FOR` -> Project

### 94. TRÆ High-Rise

Project ID: `p_trae_high_rise_aarhus`
Reuse-workflow edges: `39`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Artelia Group` (`artelia_group`) -> `BETEILIGT_AN` -> Project
- Akteur `DOVISTA / KRONE` (`dovista_krone`) -> `BETEILIGT_AN` -> Project
- Akteur `Kilden & Hindby` (`kilden_hindby`) -> `BETEILIGT_AN` -> Project
- Akteur `Lendager` -> `BETEILIGT_AN` -> Project
- Akteur `PFA Ejendomme` (`pfa_ejendomme`) -> `BETEILIGT_AN` -> Project
- Akteur `a:gain` (`gain`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Ausgemusterte Windkraftanlagen als Rotorblatt-Donor` (`bw_ausgemusterte_windkraftanlagen_als_rotorblatt_donor`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Gellerupparken Rückbau-Wohnblöcke` (`bw_gellerupparken_rueckbau_wohnbloecke`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Herlev Dach / Industrie- und Farmdächer als Aluminium-Donor` (`bw_herlev_dach_industrie_und_farmdaecher_als_aluminium_donor`)
- Project -> `HAS_BAUWERK` -> Bauwerk `TRÆ High-Rise Holzhochhaus` (`bw_tr_high_rise_holzhochhaus`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Buero` (`nut_buero`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Mischnutzung` (`nut_mischnutzung`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Dänemark` (`land_daenemark`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Aarhus` (`stadt_aarhus`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `TRÆ High-Rise Holzhochhaus` (`bw_tr_high_rise_holzhochhaus`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Aluminium-Fassadenplatten` (`bg_reuse_aluminium_fassade_trae_high_rise_aarhus_fassadenplatten`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Holzböden aus alten Fensterrahmen und Gellerup-Bauteilen` (`bg_reuse_holz_boden_trae_aarhus_holzboden_gellerup`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Troldtekt-Akustikplatten` (`bg_reuse_daemmstoff_mehrere_trae_high_rise_aarhus_troldtekt_akustikplatten`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Upcycled window elements` (`bg_reuse_glas_fenster_trae_high_rise_aarhus_upcycled_elements`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Windturbinenflügel als Sonnenschutz` (`bg_reuse_unbekannt_fassade_trae_aarhus_windturbine_sonnenschutz`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Remanufacturing` (`wva_remanufacturing`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Upcycling` (`wva_upcycling`)

#### Risk, Checks, and Constraints

**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Korrosion` (`def_korrosion`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Asbest` (`s_asbest`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `KMF — Künstliche Mineralfasern (alte Mineralwolle vor 1996/2000)` (`s_kmf`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx höher, Marketing-/Branding-Payback` (`wi_capex_hoeher_marketing_payback`)

### 95. UMAR Unit — Urban Mining and Recycling, NEST Empa Dübendorf

Project ID: `p_umar_unit`
Reuse-workflow edges: `53`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Amstein+Walthert AG — building services engineer` (`amstein_walthert`) -> `BETEILIGT_AN` -> Project
- Akteur `Balzer Ingenieure AG — structural engineer` (`balzer_ingenieure`) -> `BETEILIGT_AN` -> Project
- Akteur `Desso / Tarkett — carpet supplier (take-back service)` (`desso_tarkett`) -> `BETEILIGT_AN` -> Project
- Akteur `Ecovative — mycelium insulation manufacturer` (`ecovative`) -> `BETEILIGT_AN` -> Project
- Akteur `Empa Swiss Federal Laboratories for Materials Science and Technology — UMAR client/host` (`empa`) -> `BETEILIGT_AN` -> Project
- Akteur `Lindner SE — Plafotherm ceiling panel supplier (product-as-service)` (`lindner_se`) -> `BETEILIGT_AN` -> Project
- Akteur `Magna Glaskeramik — sintered recycled-glass panel manufacturer` (`magna_glaskeramik`) -> `BETEILIGT_AN` -> Project
- Akteur `Nimbus — lighting designer (UMAR)` (`nimbus`) -> `BETEILIGT_AN` -> Project
- Akteur `RotorDC` (`rotordc`) -> `BETEILIGT_AN` -> Project
- Akteur `Weber Energie und Bauphysik — building physics` (`weber_energie_bauphysik`) -> `BETEILIGT_AN` -> Project
- Akteur `kaufmann zimmerei und tischlerei GmbH` (`kaufmann_zimmerei`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Dirk E. Hebel` (`dirk_e_hebel`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Felix Heisel` (`felix_heisel`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Vanessa Propach` (`vanessa_propach`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Werner Sobek` (`werner_sobek_p`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Werner Sobek` (`Werner_Sobek`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Générale de Banque / BNP Paribas Fortis HQ, Brussels — donor for UMAR's Jules Wabbes door handles (via Rotor)` (`bw_generale_de_banque_brussels`)
- Project -> `HAS_BAUWERK` -> Bauwerk `NEST Unit UMAR — Urban Mining and Recycling, Empa Dübendorf` (`bw_umar_unit_duebendorf`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Schweiz` (`land_schweiz`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Dübendorf` (`stadt_duebendorf`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `NEST Unit UMAR — Urban Mining and Recycling, Empa Dübendorf` (`bw_umar_unit_duebendorf`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `UMAR — Aluminium + copper facade elements` (`bg_reuse_metall_fassade_umar_alu_copper`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `UMAR — Desso/Tarkett carpets (take-back product-service system)` (`bg_reuse_kunststoff_boden_umar_carpets`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `UMAR — DfD untreated timber structure + facade` (`bg_reuse_holz_wand_umar_timber_facade`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `UMAR — Ecovative mycelium insulation boards` (`bg_reuse_daemmstoff_daemmung_umar_mycelium`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `UMAR — Jules Wabbes door handles (loan from Rotor; from Brussels Générale de Banque HQ)` (`bg_reuse_metall_tuer_umar_wabbes_handles`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `UMAR — Lindner Plafotherm heated/chilled ceiling panels (take-back service)` (`bg_reuse_verbundstoff_decke_umar_lindner_ceiling`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `UMAR — Magna Glaskeramik sintered recycled-glass panels (kitchen tabletop + bath cladding)` (`bg_reuse_glas_keramik_fassade_umar_magna_glass`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `UMAR — Recycled bricks + recycled insulation` (`bg_reuse_mineralisch_wand_umar_recycled_bricks`)

#### Reuse Strategy and Process

**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Bauteilkatalogisierung` (`meth_bauteilkatalogisierung`)
- Project -> `HAT_METHODE` -> Methode `Design_for_Disassembly` (`meth_design_for_disassembly`)
- Project -> `HAT_METHODE` -> Methode `Reversibilitaet` (`meth_reversibilitaet`)
- Project -> `HAT_METHODE` -> Methode `Urban_Mining` (`meth_urban_mining`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Datenluecke` (`h_datenluecke`)
- Project -> `HAT_HUERDE` -> Huerde `Dauerhaftigkeit_Restlebensdauer` (`h_dauerhaftigkeit_restlebensdauer`)
- Project -> `HAT_HUERDE` -> Huerde `Fehlende_Datenstandards` (`h_fehlende_datenstandards`)
- Project -> `HAT_HUERDE` -> Huerde `Fehlende_Standardisierung` (`h_fehlende_standardisierung`)
**REFERENZIERT_NORM**
- Project -> `REFERENZIERT_NORM` -> Norm `SIA 269 — Existing structures: Grundlagen / Erhaltung von Tragwerken` (`norm_sia_269`)
- Project -> `REFERENZIERT_NORM` -> Norm `SIA 380/1 — Heizwärmebedarf (Schweiz)` (`norm_sia_380_1`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx höher, Payback über OpEx / LCA` (`wi_capex_hoeher_opex_payback`)
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Geschaeftsmodell` (`wi_geschaeftsmodell`)
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Lebenszykluskosten` (`wi_lebenszykluskosten`)
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `Versteckte Kosten (Lagerung/Prüfung/Logistik)` (`wi_hidden_costs_lagerung_pruefung`)
**NUTZT_SOFTWARE**
- Project -> `NUTZT_SOFTWARE` -> Software:Tool `BIM / digitaler Bauteilkatalog` (`tool_bim_bauteilkatalog`)
**RELEVANT_FOR**
- ReuseRule `Schweiz × Holz reuse rule` (`rr_ch_holz`) -> `RELEVANT_FOR` -> Project
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `NEST — Empa Dübendorf living-lab research platform` (`prog_nest_empa`)

### 96. Up Sticks Dundee ETH MAS DFAB 2019 (Gramazio Kohler Research; V&A Dundee commission)

Project ID: `p_up_sticks_dundee`
Reuse-workflow edges: `14`

#### Place and Built Context

**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Vereinigtes Königreich` (`land_vereinigtes_koenigreich`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Dundee` (`stadt_dundee`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Up Sticks Dundee — robotically-drilled dowel-locked timber assembly (no glue, no nails) (ETH MAS DFAB 2019)` (`bg_reuse_holz_mehrere_upsticks_timber_frame`)

#### Reuse Strategy and Process

**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Design_for_Disassembly` (`meth_design_for_disassembly`)

#### Risk, Checks, and Constraints

**HAT_HUERDE**
- Project -> `HAT_HUERDE` -> Huerde `Bauproduktstatus` (`h_bauproduktstatus`)
- Project -> `HAT_HUERDE` -> Huerde `Unkonventionelles_Material` (`h_unkonventionelles_material`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Vereinigtes Königreich × Holz reuse rule` (`rr_gb_holz`) -> `RELEVANT_FOR` -> Project
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `MAS Architektur und Digitale Fabrikation, ETH Zürich (Gramazio Kohler Research)` (`prog_mas_dfab`)

### 97. Upcycle Studios Copenhagen

Project ID: `p_upcycle_studios_copenhagen`
Reuse-workflow edges: `35`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `AG Gruppen` (`ag_gruppen`) -> `BETEILIGT_AN` -> Project
- Akteur `Artelia` (`artelia`) -> `BETEILIGT_AN` -> Project
- Akteur `BOGL` (`bogl`) -> `BETEILIGT_AN` -> Project
- Akteur `Lendager` -> `BETEILIGT_AN` -> Project
- Akteur `MOE` (`moe`) -> `BETEILIGT_AN` -> Project
- Akteur `NREP` (`nrep`) -> `BETEILIGT_AN` -> Project
- Akteur `a:gain` (`gain`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Anders Lendager` (`anders_lendager`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Lendager` -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Copenhagen Metro construction waste source` (`bw_copenhagen_metro_construction_waste_source`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Upcycle Studios Reihenhausensemble` (`bw_upcycle_studios_reihenhausensemble`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Öffentliche Wohnbauten Nordjütland` (`bw_oeffentliche_wohnbauten_nordjuetland`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Mischnutzung` (`nut_mischnutzung`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Dänemark` (`land_daenemark`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Kopenhagen` (`stadt_kopenhagen`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Upcycle Studios Reihenhausensemble` (`bw_upcycle_studios_reihenhausensemble`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Dinesen-Offcuts als Böden/Wände/Fassaden` (`bg_reuse_holz_mehrere_upcycle_dinesen_offcuts`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Doppelverglaste Fenster` (`bg_reuse_glas_fenster_upcycle_studios_copenhagen_doppelverglaste`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Recyclingbeton aus Copenhagen Metro` (`bg_reuse_mehrere_mehrere_upcycle_recyclingbeton_metro`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Recycling` (`wva_recycling`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Remanufacturing` (`wva_remanufacturing`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Upcycling` (`wva_upcycling`)

#### Risk, Checks, and Constraints

**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

### 98. Verbiest + Karreveld

Project ID: `p_verbiest_karreveld_brussels`
Reuse-workflow edges: `45`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `AgwA` (`agwa`) -> `BETEILIGT_AN` -> Project
- Akteur `Daidalos Peutz` (`daidalos_peutz`) -> `BETEILIGT_AN` -> Project
- Akteur `Denis Dujardin` (`denis_dujardin`) -> `BETEILIGT_AN` -> Project
- Akteur `Evelia Macal` (`evelia_macal`) -> `BETEILIGT_AN` -> Project
- Akteur `JZH & Partners` (`jzh_partners`) -> `BETEILIGT_AN` -> Project
- Akteur `Kahle Acoustics` (`kahle_acoustics`) -> `BETEILIGT_AN` -> Project
- Akteur `Pouvoir Organisateur Pluriel / POP` (`pouvoir_organisateur_pluriel_pop`) -> `BETEILIGT_AN` -> Project
- Akteur `Sixco` (`sixco`) -> `BETEILIGT_AN` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Altes Projekt in Hanzinelle` (`bw_altes_projekt_in_hanzinelle`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Karreveld Bürogebäude zu Schule und Sportzentrum` (`bw_karreveld_buerogebaeude_zu_schule_und_sportzentrum`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Karreveld Bürogebäude zu Schule und Sportzentrum` (`bw_karreveld_buerogebaeude_zu_schule_und_sportzentrum`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Palais des Expositions Charleroi` (`bw_palais_des_expositions_charleroi`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Erweiterung` (`bai_erweiterung`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umnutzung` (`bai_umnutzung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Schule_Bildung` (`nut_schule_bildung`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Belgien` (`land_belgien`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Brüssel` (`stadt_bruessel`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Karreveld Bürogebäude zu Schule und Sportzentrum` (`bw_karreveld_buerogebaeude_zu_schule_und_sportzentrum`)
- Project -> `NUTZT_BAUWERK` -> Materialdepot `Verbiest Lagerhaus zu Haus und Atelier` (`bw_verbiest_lagerhaus_zu_haus_und_atelier`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Karreveld abgehängte Decken und Leuchten` (`bg_reuse_mehrere_mehrere_verbiest_karreveld_decken_leuchten`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Karreveld modulares Innenwandsystem` (`bg_reuse_mehrere_mehrere_verbiest_karreveld_innenwand_modular`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Verbiest Dach- und Terrassenfliesen` (`bg_reuse_keramik_mehrere_verbiest_karreveld_dach_terrasse`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Verbiest dekorative Fliesen aus Hanzinelle` (`bg_reuse_keramik_mehrere_verbiest_hanzinelle_fliesen`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Verbiest-Fliesen (Keramik/Stein) aus Palais des Expositions Charleroi` (`bg_reuse_keramik_boden_verbiest_charleroi`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Verbiest-Geländer aus Palais des Expositions Charleroi` (`bg_reuse_stahl_gelaender_verbiest_charleroi`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Verbiest-Steine (Natur-/Mauersteine) aus Palais des Expositions Charleroi` (`bg_reuse_naturstein_wand_verbiest_charleroi`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Materialinventur` (`meth_materialinventur`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Adaptives_ReUse` (`wva_adaptives_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Same_Site_ReUse` (`wva_same_site_reuse`)

#### Risk, Checks, and Constraints

**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Asbest` (`s_asbest`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `KMF — Künstliche Mineralfasern (alte Mineralwolle vor 1996/2000)` (`s_kmf`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Belgien × Naturstein reuse rule` (`rr_be_naturstein`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Belgien × Stahl reuse rule` (`rr_be_stahl`) -> `RELEVANT_FOR` -> Project

### 99. Villa Welpeloo Enschede

Project ID: `p_villa_welpeloo_enschede`
Reuse-workflow edges: `45`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Jan Jongert` (`jan_jongert`) -> `BETEILIGT_AN` -> Project
- Akteur `Jeroen Bergsma` (`jeroen_bergsma`) -> `BETEILIGT_AN` -> Project
- Akteur `Nico Plukkel` (`nico_plukkel`) -> `BETEILIGT_AN` -> Project
- Akteur `Private Bauherrschaft Villa Welpeloo` (`private_bauherrschaft_villa_welpeloo`) -> `BETEILIGT_AN` -> Project
- Akteur `Superuse Studios / 2012Architecten` (`superuse_studios_2012architecten`) -> `BETEILIGT_AN` -> Project
- Akteur `TKF / Twente cable factory` (`tkf_twente_cable_factory`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Césare Peeren` (`cesare_peeren`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Jan Jongert` (`jan_jongert`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Jeroen Bergsma` (`jeroen_bergsma`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Superuse Studios` (`Superuse_Studios`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Superuse on Site` (`superuse_on_site`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Paternoster- / Textilindustriemaschine Enschede` (`bw_paternoster_textilindustriemaschine_enschede`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Twente / TKF Kabelfabrik Materialquelle` (`bw_twente_tkf_kabelfabrik_materialquelle`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Villa Welpeloo Wohnhaus und Kunstlager` (`bw_villa_welpeloo_wohnhaus_und_kunstlager`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Niederlande` (`land_niederlande`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Enschede` (`stadt_enschede`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Villa Welpeloo Wohnhaus und Kunstlager` (`bw_villa_welpeloo_wohnhaus_und_kunstlager`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Bau-/Montagelift als Innenlift` (`bg_reuse_stahl_technik_villa_welpeloo_enschede_bau_montagelift_als_innenlift`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Holzfassade aus Kabeltrommeln` (`bg_reuse_holz_fassade_villa_welpeloo_enschede_holzfassade_aus_kabeltrommeln`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Polystyrol-Dämmplatten aus Restplatten` (`bg_reuse_kunststoff_daemmung_welpeloo_polystyrol_restplatten`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Stahlträger aus Paternoster-Textilmaschine` (`bg_reuse_stahl_mehrere_welpeloo_paternoster_textilmaschine`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Regional geografisches Matching (50–500 km)` (`mq_geographic_regional`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Urban_Mining` (`meth_urban_mining`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Upcycling` (`wva_upcycling`)

#### Risk, Checks, and Constraints

**HAT_DEFEKT_BEFUND**
- Project -> `HAT_DEFEKT_BEFUND` -> Defekt `Oberflächenmangel / Verfärbung` (`def_oberflaechenmangel`)
**HAT_PRUEFUNG**
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `Dokumentenprüfung / Herkunfts- und Bestandsnachweis` (`pr_dokumentenpruefung_bestand`)
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `Eignungspruefung_Baulehm` (`pr_eignungspruefung_baulehm`)
- Project -> `HAT_PRUEFUNG` -> PruefungNachweis `Korrosionsprüfung / Restdickenmessung` (`pr_korrosionspruefung`)
**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PCB` (`s_pcb`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Niederlande × Holz reuse rule` (`rr_nl_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Niederlande × Stahl reuse rule` (`rr_nl_stahl`) -> `RELEVANT_FOR` -> Project

### 100. Woongroep Boschgaard Den Bosch

Project ID: `p_woongroep_boschgaard_den_bosch`
Reuse-workflow edges: `42`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Bewohnerinitiative Boschgaard` (`bewohnerinitiative_boschgaard`) -> `BETEILIGT_AN` -> Project
- Akteur `Bouwbedrijf Versteegden` (`bouwbedrijf_versteegden`) -> `BETEILIGT_AN` -> Project
- Akteur `Superuse Studios` (`Superuse_Studios`) -> `BETEILIGT_AN` -> Project
- Akteur `Transfarmers` (`transfarmers`) -> `BETEILIGT_AN` -> Project
- Akteur `VanNimwegen` (`vannimwegen`) -> `BETEILIGT_AN` -> Project
- Akteur `Zayaz` (`zayaz`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Césare Peeren` (`cesare_peeren`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Jan Jongert` (`jan_jongert`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Jeroen Bergsma` (`jeroen_bergsma`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Superuse Studios` (`Superuse_Studios`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Superuse on Site` (`superuse_on_site`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Bibliothek De Brenthof Sint-Michielsgestel` (`bw_bibliothek_de_brenthof_sint_michielsgestel`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Boschgaard Wohnprojekt und Nachbarschaftszentrum` (`bw_boschgaard_wohnprojekt_und_nachbarschaftszentrum`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Stadskantoor Roosendaal` (`bw_stadskantoor_roosendaal`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Weitere regionale Rückbauquellen Boschgaard` (`bw_weitere_regionale_rueckbauquellen_boschgaard`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Neubau` (`bai_neubau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Sozialbau` (`nut_sozialbau`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Wohnen` (`nut_wohnen`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Niederlande` (`land_niederlande`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `s-Hertogenbosch` (`stadt_s_hertogenbosch`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Boschgaard Wohnprojekt und Nachbarschaftszentrum` (`bw_boschgaard_wohnprojekt_und_nachbarschaftszentrum`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Aluminium-Fassadensystem` (`bg_reuse_mehrere_mehrere_boschgaard_alu_fassade`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `HSB-Holz Balken und Ausbauholz` (`bg_reuse_holz_mehrere_boschgaard_hsb_balken_ausbau`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Holz-Dachspanten / Brettschichtholz-Kniespanten` (`bg_reuse_holz_mehrere_boschgaard_dachspanten`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Türen und Innenausbau` (`bg_reuse_mehrere_mehrere_boschgaard_tueren_innenausbau`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Temporales Matching durch Zwischenlagerung` (`mq_temporal_storage`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `Building_Material_Scouting` (`meth_building_material_scouting`)
- Project -> `HAT_METHODE` -> Methode `Form_Follows_Availability` (`meth_form_follows_availability`)
- Project -> `HAT_METHODE` -> Methode `Urban_Mining` (`meth_urban_mining`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Adaptives_ReUse` (`wva_adaptives_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Same_Site_ReUse` (`wva_same_site_reuse`)

#### Risk, Checks, and Constraints

**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**RELEVANT_FOR**
- ReuseRule `Niederlande × Holz reuse rule` (`rr_nl_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Niederlande × Stahl reuse rule` (`rr_nl_stahl`) -> `RELEVANT_FOR` -> Project

### 101. Zinneke / FEDER Masui4ever Brussels

Project ID: `p_zinneke_feder_masui4ever_brussels`
Reuse-workflow edges: `49`

#### Actors and Delivery Chain

**BETEILIGT_AN**
- Akteur `Brudex` (`brudex`) -> `BETEILIGT_AN` -> Project
- Akteur `De Coninck` (`de_coninck`) -> `BETEILIGT_AN` -> Project
- Akteur `ERDF / FEDER Brüssel-Hauptstadt` (`erdf_feder_bruessel_hauptstadt`) -> `BETEILIGT_AN` -> Project
- Akteur `Matriciel` (`matriciel`) -> `BETEILIGT_AN` -> Project
- Akteur `Ouest Architecture` (`ouest_architecture`) -> `BETEILIGT_AN` -> Project
- Akteur `Rotor` -> `BETEILIGT_AN` -> Project
- Akteur `Zinneke asbl` (`zinneke_asbl`) -> `BETEILIGT_AN` -> Project
**STUB_PROJECT_LINK**
- Akteur `Jan Haerens` (`jan_haerens`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Lionel Devlieger` (`lionel_devlieger`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Maarten Gielen` (`maarten_gielen`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Michaël Ghyoot` (`michael_ghyoot`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Ouest Architecture` (`ouest_architecture`) -> `STUB_PROJECT_LINK` -> Project
- Akteur `Stéphane Damsin` (`stephane_damsin`) -> `STUB_PROJECT_LINK` -> Project

#### Place and Built Context

**HAS_BAUWERK**
- Project -> `HAS_BAUWERK` -> Bauwerk `Bürohochhaus im Zentrum Brüssels als Lüftungs-Donor` (`bw_buerohochhaus_im_zentrum_bruessels_als_lueftungs_donor`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Ehemaliger Sitz der flämischen Regierung als Treppen-Donor` (`bw_ehemaliger_sitz_der_flaemischen_regierung_als_treppen_donor`)
- Project -> `HAS_BAUWERK` -> Bauwerk `Zinneke Masui4ever ehemaliger Werkstatt- und Verwaltungskomplex` (`bw_zinneke_masui4ever_ehemaliger_werkstatt_und_verwaltungskomplex`)
**HAT_INTERVENTION**
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umbau` (`bai_umbau`)
- Project -> `HAT_INTERVENTION` -> BauaufgabeIntervention `Umnutzung` (`bai_umnutzung`)
**HAT_NUTZUNG**
- Project -> `HAT_NUTZUNG` -> Nutzung `Gewerbe` (`nut_gewerbe`)
- Project -> `HAT_NUTZUNG` -> Nutzung `Kultur` (`nut_kultur`)
**HAT_STATUS**
- Project -> `HAT_STATUS` -> Status `Realisiert` (`status_realisiert`)
**LIEGT_IN_LAND**
- Project -> `LIEGT_IN_LAND` -> Land `Belgien` (`land_belgien`)
**LIEGT_IN_STADT**
- Project -> `LIEGT_IN_STADT` -> Stadt `Brüssel` (`stadt_bruessel`)
**NUTZT_BAUWERK**
- Project -> `NUTZT_BAUWERK` -> Bauwerk `Zinneke Masui4ever ehemaliger Werkstatt- und Verwaltungskomplex` (`bw_zinneke_masui4ever_ehemaliger_werkstatt_und_verwaltungskomplex`)

#### Components and Construction System

**HAT_BAUTEILGRUPPE**
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Eichenparkett und Azobé-Terrassendielen` (`bg_reuse_holz_boden_zinneke_feder_eichenparkett_azobe`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Fensterrahmen (Zinneke)` (`bg_reuse_mehrere_fenster_zinneke_feder_masui4ever_brussels_fensterrahmen`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Kompletter Lüftungsverbund` (`bg_reuse_stahl_technik_zinneke_feder_lueftung`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Stahl-Treppen` (`bg_reuse_stahl_treppe_zinneke_feder_masui4ever_brussels_treppen`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Stahlträger als Stürze` (`bg_reuse_stahl_traeger_zinneke_feder_stuerze`)
- Project -> `HAT_BAUTEILGRUPPE` -> Bauteilgruppe `Steinwolle-Dämmplatten` (`bg_reuse_daemmstoff_daemmung_zinneke_feder_steinwolle`)

#### Reuse Strategy and Process

**HAT_MATCHINGQUALITAET**
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Lokales geografisches Matching (<50 km)` (`mq_geographic_local`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Spezifikations-Anpassung nötig` (`mq_spec_anpassung`)
- Project -> `HAT_MATCHINGQUALITAET` -> MatchingQualitaet `Zweckänderung (Funktionswechsel)` (`mq_spec_zweckaenderung`)
**HAT_METHODE**
- Project -> `HAT_METHODE` -> Methode `ReUse_Assessment` (`meth_reuse_assessment`)
- Project -> `HAT_METHODE` -> Methode `ReUse_Ausschreibung` (`meth_reuse_ausschreibung`)
- Project -> `HAT_METHODE` -> Methode `Zirkulaere_Ausschreibung` (`meth_zirkulaere_ausschreibung`)
**HAT_WIEDERVERWENDUNGSART**
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Adaptives_ReUse` (`wva_adaptives_reuse`)
- Project -> `HAT_WIEDERVERWENDUNGSART` -> WiederverwendungsArt `Direkte_Wiederverwendung` (`wva_direkte_wiederverwendung`)

#### Risk, Checks, and Constraints

**REQUIRES_VERIFICATION_FOR**
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Asbest` (`s_asbest`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Bleifarbe` (`s_bleifarbe`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Formaldehyd (MDF / Spanplatten)` (`s_formaldehyd`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Holzschutzmittel` (`s_holzschutzmittel`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `KMF — Künstliche Mineralfasern (alte Mineralwolle vor 1996/2000)` (`s_kmf`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `PAK` (`s_pak`)
- Project -> `REQUIRES_VERIFICATION_FOR` -> Schadstoff `Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten` (`s_schwermetalle`)

#### Tools, Programmes, and Frameworks

**HAT_WIRTSCHAFT**
- Project -> `HAT_WIRTSCHAFT` -> Wirtschaft `CapEx höher, Subvention/Förderung deckt Mehrkosten` (`wi_capex_hoeher_subvention`)
**RELEVANT_FOR**
- ReuseRule `Belgien × Holz reuse rule` (`rr_be_holz`) -> `RELEVANT_FOR` -> Project
- ReuseRule `Belgien × Stahl reuse rule` (`rr_be_stahl`) -> `RELEVANT_FOR` -> Project
**TEIL_VON_PROGRAMM**
- Project -> `TEIL_VON_PROGRAMM` -> Programm `Foerderprogramm` (`prog_foerderprogramm`)
