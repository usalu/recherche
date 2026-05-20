# Actor + entity extraction per dossier

**Purpose:** Authoritative per-dossier list of Akteure, Bauteilgruppen, Programme, Tools, Norms, Stadt/Land, and Quellen the patch generator must emit. Every row carries an evidence source and an explicit pre-existence assumption ("EXISTS_PRECHECK").

**Workflow:**
1. Patch generator reads this file.
2. For every row marked `EXISTS_PRECHECK: yes`, it runs the relevant Cypher (S26-S27 of [pre_flight_validation.cypher](pre_flight_validation.cypher)) to confirm.
3. Where the row exists, generator uses `set_node_properties` to enrich. Where absent, generator emits `add_node`.
4. Every new Akteur gets HAT_AKTEURROLLE + HAT_AKTEURTYP rels (per CORRECTIONS O4) + GEHÖRT_ZU where evidenced (O5).
5. Every new Bauwerk gets HAT_BAUOBJEKTROLLE + HAT_BAUOBJEKTKLASSE + LIEGT_IN_STADT + LIEGT_IN_LAND + HAT_STATUS (per CORRECTIONS O6/C8).
6. All new nodes get BELEGT_IN → primary dossier Quelle (case_markdown) at creation.

**Akteurrolle / Akteurtyp shorthand** (see CORRECTIONS O4 table for full list):
- `arch` = ar_entwurf_planung + at_unternehmen
- `struct` = ar_tragwerksplanung + at_unternehmen
- `engineer` = ar_fachplanung_nachweis + at_unternehmen
- `landscape` = ar_landschaftsplanung + at_unternehmen
- `client` = ar_bauherr_auftraggeber + at_unternehmen
- `client_pub` = ar_bauherr_auftraggeber + at_oeffentliche_institution
- `funder` = ar_oeffentliche_hand_foerderung + at_oeffentliche_institution
- `research` = ar_forschung_dokumentation + at_forschung_lehre
- `teach` = ar_bildung_wissenstransfer + at_forschung_lehre
- `reuse_consult` = ar_reuse_zirkularitaetsberatung + at_unternehmen
- `broker` = ar_materialbroker + at_materialhub_bauteilboerse
- `decon` = ar_rueckbau_bauteilernte_logistik + at_unternehmen
- `contract` = ar_bauausfuehrung_fertigung + at_unternehmen
- `supplier` = ar_materiallieferung_markt + at_unternehmen
- `software` = ar_software_digitalisierung + at_software_tool_anbieter
- `ngo` = ar_forschung_dokumentation + at_ngo_verband_netzwerk
- `person+arch` = ar_entwurf_planung + at_person
- `person+struct` = ar_tragwerksplanung + at_person
- `person+research` = ar_forschung_dokumentation + at_person
- `person+manage` = ar_projektmanagement_koordination + at_person

---

## 1. Schärenmoosstrasse Zürich (`p_schaerenmoosstrasse_zuerich`)

**Quelle:** `qu_batch1_schaerenmoosstrasse_dossier`, source_file `batch 1.md` (Section 1), quelltyp `case_markdown`

### Existing actors to link (PRECHECK + ASSOZIIERT_MIT_PROJEKT verify)

| id | name | already linked? |
|---|---|---|
| `studio_trachsler_hoffmann` | Studio Trachsler Hoffmann | yes — verify |
| `daniel_hoffmann` | Daniel Hoffmann | yes — verify |
| `gian_trachsler` | Gian Trachsler | yes — verify |

### New actors

| id | name | role-shorthand | GEHÖRT_ZU |
|---|---|---|---|
| `stiftung_pwg` | Stiftung PWG | client | — |
| `perez_schmidlin_bauingenieure` | Pérez Schmidlin Bauingenieure GmbH | struct | — |
| `andreas_geser_landschaftsarchitekten` | Andreas Geser Landschaftsarchitekten AG | landscape | — |
| `stefan_perez` | Stefan Pérez | person+struct | perez_schmidlin_bauingenieure |
| `michael_schmidlin` | Michael Schmidlin | person+struct | perez_schmidlin_bauingenieure |
| `andreas_geser` | Andreas Geser | ar_landschaftsplanung + at_person | andreas_geser_landschaftsarchitekten |
| `martin_zeller` | Martin Zeller | ar_kunst_gestaltung + at_person | studio_trachsler_hoffmann |

### Bauwerks

| id | name | role | class | status |
|---|---|---|---|---|
| `bw_schaerenmoosstrasse_zuerich` | Schärenmoosstr. ZH | bor_same_site_donor_receiver | bok_gebaeude | status_geplant |
| `bw_ubs_altstetten` | UBS Datenz. Altstetten | bor_donorobjekt | bok_gebaeude | status_rueckgebaut |

### Wiederverwendungskette
- `k_ubs_altstetten_hall_to_sms` (donor `bw_ubs_altstetten` → BG → receiver `bw_schaerenmoosstrasse_zuerich`)

### Programme

| id | name | already exists? |
|---|---|---|
| `prog_wettbewerb` | Wettbewerb | yes (existing) |
| `prog_stiftung_pwg` | Stiftung PWG Wettbewerb | NEW |

### Bauteilgruppen (5)

| id (new convention) | name (≤25) | reuse_status | EINGEBAUT_IN | AUS_BAUWERK | Notes |
|---|---|---|---|---|---|
| `bg_retained_mehrere_mehrere_sms_zuerich_existing_bldgs` | `SMS ZH Bestand` | retained | bw_schaerenmoosstrasse_zuerich | (same-site) | Micro + Dixa retained |
| `bg_retained_stahlbeton_treppe_sms_zuerich_existing_stairs` | `SMS ZH Bestandstreppen` | retained | bw_schaerenmoosstrasse_zuerich | — | Stair cores retained |
| `bg_reuse_mehrere_mehrere_sms_zuerich_ubs_hall` | `SMS ZH UBS-Halle` | reuse | bw_schaerenmoosstrasse_zuerich | bw_ubs_altstetten | Two-storey hall components |
| `bg_planned_stahl_fassade_sms_zuerich_arcade` | `SMS ZH Stahl-Laubengang` | planned | bw_schaerenmoosstrasse_zuerich | — | Steel arcade DfD |
| `bg_planned_mehrere_technik_sms_zuerich_pv_roof` | `SMS ZH PV-Anlage` | planned | bw_schaerenmoosstrasse_zuerich | — | 250 m² PV |

### Project-level vocab (HAT_INTERVENTION / HAT_NUTZUNG / etc.)
```
HAT_INTERVENTION: bai_umnutzung, bai_umbau
HAT_NUTZUNG: nut_wohnen, nut_gewerbe
HAT_METHODE: meth_form_follows_availability, meth_reuse_assessment
REFERENZIERT_NORM: norm_sia_schweiz
HAT_HUERDE: h_technische_freigabe, h_entwurfsbindung
HAT_WIRTSCHAFT: wi_capex_hoeher_subvention (verify)
TEIL_VON_PROGRAMM: prog_wettbewerb, prog_stiftung_pwg
HAT_DOMINANT_AKZEPTANZ: ak_oeffentlicher_bauherr_pilot
NUTZT_BAUWERK: bw_schaerenmoosstrasse_zuerich
```

---

## 2. UMAR Unit — NEST Empa Dübendorf (`p_umar_unit`)

**Quelle:** `qu_batch1_umar_dossier`, source_file `batch 1.md` (Section 2)

### Existing actors to link
| id | name |
|---|---|
| `dirk_e_hebel` | Dirk E. Hebel |
| `felix_heisel` | Felix Heisel |
| `vanessa_propach` | Vanessa Propach |
| `werner_sobek_p` | Werner Sobek (canonical) |

### Cleanup
- Remove duplicate `Werner_Sobek -[ASSOZIIERT_MIT_PROJEKT]-> p_umar_unit`. Keep `werner_sobek_p`.

### New actors (16)

| id | name | role | GEHÖRT_ZU |
|---|---|---|---|
| `empa` | Empa | client_pub | — |
| `kaufmann_zimmerei` | kaufmann zimmerei und tischlerei | contract | — |
| `amstein_walthert` | Amstein+Walthert AG | engineer | — |
| `balzer_ingenieure` | Balzer Ingenieure AG | struct | — |
| `weber_energie_bauphysik` | Weber Energie und Bauphysik | engineer | — |
| `lindner_se` | Lindner SE | supplier | — |
| `nimbus` | Nimbus | supplier | — |
| `magna_glaskeramik` | Magna Glaskeramik | supplier | — |
| `ecovative` | Ecovative | supplier | — |
| `desso_tarkett` | Desso / Tarkett | supplier | — |

Note: `rotordc` (existing) is also a Bauteillieferant for the Wabbes handles → BETEILIGT_AN.

### Bauwerks
| id | name | role | class | status |
|---|---|---|---|---|
| `bw_umar_unit_duebendorf` | UMAR Unit Dübendorf | bor_referenzobjekt | bok_gebaeudeteil | status_realisiert |
| `bw_generale_de_banque_brussels` | Générale de Banque BXL | bor_donorobjekt | bok_gebaeude | status_rueckgebaut |

### Wiederverwendungskette
- `k_wabbes_handles_to_umar` (donor `bw_generale_de_banque_brussels` → Rotor → BG `bg_reuse_metall_tuer_umar_wabbes_handles` → receiver `bw_umar_unit_duebendorf`)

### Programme (1 new)
| id | name |
|---|---|
| `prog_nest_empa` | NEST Empa Dübendorf |

### Bauteilgruppen (8)

| id | name (≤25) | reuse_status | EINGEBAUT_IN | AUS_BAUWERK | Notes |
|---|---|---|---|---|---|
| `bg_reuse_holz_wand_umar_timber_facade` | `UMAR Holz/Fassade` | reuse | bw_umar_unit_duebendorf | — | DfD timber structure + facade |
| `bg_reuse_metall_fassade_umar_alu_copper` | `UMAR Alu+Kupfer` | reuse | bw_umar_unit_duebendorf | — | Aluminium + copper facade |
| `bg_reuse_metall_tuer_umar_wabbes_handles` | `UMAR Wabbes Türgriffe` | reuse | bw_umar_unit_duebendorf | bw_generale_de_banque_brussels | Jules Wabbes door handles via Rotor |
| `bg_reuse_glas_keramik_fassade_umar_magna_glass` | `UMAR Magna Glas` | reuse | bw_umar_unit_duebendorf | — | Magna sintered recycled-glass panels |
| `bg_reuse_daemmstoff_daemmung_umar_mycelium` | `UMAR Pilzmyzel-Dämmung` | reuse | bw_umar_unit_duebendorf | — | Ecovative mycelium |
| `bg_reuse_kunststoff_boden_umar_carpets` | `UMAR Desso-Teppich` | reuse | bw_umar_unit_duebendorf | — | Take-back service Desso/Tarkett |
| `bg_reuse_verbundstoff_decke_umar_lindner_ceiling` | `UMAR Lindner-Decke` | reuse | bw_umar_unit_duebendorf | — | Plafotherm heated/chilled ceiling |
| `bg_reuse_mineralisch_wand_umar_recycled_bricks` | `UMAR Recyclingziegel` | reuse | bw_umar_unit_duebendorf | — | Recycled bricks + insulation |

### Funktionswechsel candidates (HAT_MATCHINGQUALITAET → mq_spec_zweckaenderung)
- `bg_reuse_metall_tuer_umar_wabbes_handles`: alte_funktion="bank door handles (Brussels HQ)", neue_funktion="research unit door handles"

### Project-level vocab
```
HAT_INTERVENTION: bai_neubau
HAT_NUTZUNG: nut_wohnen
HAT_METHODE: meth_design_for_disassembly, meth_reversibilitaet, meth_urban_mining, meth_bauteilkatalogisierung
REFERENZIERT_NORM: norm_sia_schweiz
HAT_HUERDE: h_fehlende_standardisierung, h_fehlende_datenstandards, h_datenluecke
HAT_WIRTSCHAFT: wi_capex_hoeher_opex_payback, wi_hidden_costs_lagerung_pruefung, wi_geschaeftsmodell
HAT_DOMINANT_MARKTMODELL: mm_take_back_service
NUTZT_TOOL: tool_bim_bauteilkatalog
TEIL_VON_PROGRAMM: prog_forschungsprojekt, prog_reallabor, prog_nest_empa
HAT_DOMINANT_AKZEPTANZ: ak_oeffentlicher_bauherr_pilot
NUTZT_BAUWERK: bw_umar_unit_duebendorf
```

---

## 3. ELEMENTA Walkeweg Basel (`p_elementa_walkeweg`)

**Quelle:** `qu_batch1_elementa_dossier`, source_file `batch 1.md` (Section 3)

### Existing actors to link
| id | name |
|---|---|
| `carla_ferrando_costansa` | Carla Ferrando Costansa (set rolle="Architekt") |
| `pablo_garrido_arnaiz` | Pablo Garrido Arnaiz (set rolle="Architekt") |
| `parabase` | PARABASE |
| `immobilien_basel_stadt` | Immobilien Basel-Stadt |
| `hochbauamt_basel_stadt` | Hochbauamt Basel-Stadt |
| `zirkular_gmbh` | Zirkular GmbH |

### New actors (12)

| id | name | role |
|---|---|---|
| `kanton_basel_stadt` | Kanton Basel-Stadt | funder |
| `monotti_ingegneri` | Monotti Ingegneri Consulenti SA | struct |
| `mario_monotti` | Mario Monotti | person+struct (GEHÖRT_ZU monotti_ingegneri) |
| `usus_la` | USUS Landschaftsarchitektur | landscape |
| `roger_keller` | Roger Keller | ar_landschaftsplanung + at_person (GEHÖRT_ZU usus_la) |
| `ana_olalquiaga` | Ana Olalquiaga | person+arch (GEHÖRT_ZU parabase) |
| `caretta_weidmann` | Caretta+Weidmann | engineer (fassade) |
| `gti_engineering` | GTI Engineering | engineer (mep) |
| `afc_basel` | AFC | engineer (cost) |
| `senn_technology` | Senn Technology AG | engineer |
| `anima_engineering` | Anima Engineering AG | engineer |
| `bauteilboerse_basel` | Bauteilbörse Basel | broker |
| `digvis_gmbh` | Digvis GmbH | software |

### Bauwerks
| id | name | role | class | status |
|---|---|---|---|---|
| `bw_elementa_walkeweg_basel` | ELEMENTA Walkeweg | bor_empfaengerobjekt | bok_gebaeude | status_geplant |
| `bw_lysbueechel_garage_basel` | Lysbüchel Parkgarage | bor_donorobjekt | bok_gebaeude | status_rueckgebaut |

### Wiederverwendungskette
- `k_lysbueechel_to_elementa` (donor `bw_lysbueechel_garage_basel` → BGs → receiver `bw_elementa_walkeweg_basel`)

### Software / Tool / ZBS
| id | label | name |
|---|---|---|
| `software_ecotool` | Software | EcoTool |
| `zbs_ecotool` | ZertifizierungBewertungssystem | EcoTool (ökologische Bilanz) |
| `tool_bauteilkatalog` | Tool | (already exists) |

### Bauteilgruppen (4)

| id | name (≤25) | reuse_status | EINGEBAUT_IN | AUS_BAUWERK | Notes |
|---|---|---|---|---|---|
| `bg_reuse_mineralisch_stuetze_elementa_baufeld_c` | `ELEMENTA Baufeld C` | reuse | bw_elementa_walkeweg_basel | bw_lysbueechel_garage_basel | RC column-beam |
| `bg_reuse_mineralisch_wand_elementa_baufeld_d` | `ELEMENTA Baufeld D` | reuse | bw_elementa_walkeweg_basel | bw_lysbueechel_garage_basel | RC rib-panel wall |
| `bg_planned_holz_decke_elementa_brettstapel` | `ELEMENTA Brettstapel` | planned | bw_elementa_walkeweg_basel | — | New renewable wood |
| `bg_planned_lehm_erde_wand_elementa_clay` | `ELEMENTA Lehm` | planned | bw_elementa_walkeweg_basel | — | Clay panels + plaster |

### Project-level vocab
```
HAT_INTERVENTION: bai_neubau
HAT_NUTZUNG: nut_wohnen
HAT_METHODE: meth_pre_deconstruction_audit, meth_bauteilkatalogisierung, meth_materialinventur, meth_form_follows_availability
REFERENZIERT_NORM: norm_sia_schweiz
HAT_HUERDE: h_entwurfsbindung, h_verfuegbarkeitsproblem, h_heterogenitaet_chargen, h_terminunsicherheit, h_toleranzen
HAT_WIRTSCHAFT: wi_capex_niedriger_direkter_ersparnis, wi_capex_hoeher_subvention, wi_hidden_costs_lagerung_pruefung, wi_lebenszykluskosten
HAT_DOMINANT_MARKTMODELL: mm_plattform_vermittelt
NUTZT_SOFTWARE: software_ecotool
NUTZT_TOOL: tool_bauteilkatalog
HAT_ZERTIFIZIERUNG: zbs_ecotool
TEIL_VON_PROGRAMM: prog_wettbewerb, prog_kommunales_programm
HAT_DOMINANT_AKZEPTANZ: ak_oeffentlicher_bauherr_pilot
NUTZT_BAUWERK: bw_elementa_walkeweg_basel
```

---

## 4. Careno Be.Circular (`p_careno_becircular`)

**Quelle:** `qu_careno_becircular_dossier`, source_file `Careno_Be_Circular_Brussels.md`

### Existing actors
| id |
|---|
| `lionel_billiet` (verify) |
| `sebastien_paulet` (verify) |
| `rotor_asbl_vzw` (canonical Rotor) |
| `rotordc` (canonical RotorDC) |

### New actors (2)

| id | name | role |
|---|---|---|
| `bbri` | BBRI — Belgian Building Research Institute | research |
| `brussels_capital_region` | Brussels-Capital Region | funder |

### Programme (3 — including parent + grant)
| id | name |
|---|---|
| `prog_be_circular` | Be.Circular (NEW) |
| `prog_prec` | PREC — Programme Régional pour l'Économie Circulaire (NEW; parent of be_circular) |

### Tool
| id | name |
|---|---|
| `tool_retile` | Re-Tile machine (NEW, developed 2022 by RotorDC with Be.Circular grant) |

### Bauteilgruppen (4) — NO receiving Bauwerk (research project)

| id | name (≤25) | reuse_status | Notes |
|---|---|---|---|
| `bg_reuse_glas_keramik_belag_careno_historic_tiles` | `Careno Hist. Fliesen` | reuse | Ceramic 1900-1960 (bauteilebene=be_materialcharge) |
| `bg_reuse_glas_keramik_belag_careno_retile_cleaned` | `Careno Re-Tile` | reuse | Re-Tile cleaned (be_materialcharge) |
| `bg_reuse_glas_keramik_belag_careno_rotor_stock` | `Careno RotorDC Lager` | reuse | RotorDC sales stock (be_materialcharge, rq_lager) |
| `bg_reuse_glas_keramik_belag_careno_bespoke` | `Careno Abfallmix` | reuse | Bespoke waste-stream (be_materialcharge) |

### Wiederverwendungskette
- `k_careno_rotor_tile_cleaning` (raw historic tiles → Re-Tile machine → cleaned tiles → RotorDC sale)

### Project-level vocab
```
HAT_METHODE: meth_wiederverwendungskriterien, meth_building_material_scouting
HAT_HUERDE: h_aufbereitungsaufwand, h_materialqualitaet_unklar, h_fehlende_standardisierung, h_bruch_beschaedigungsrisiko, h_gewaehrleistung
HAT_WIRTSCHAFT: wi_capex_hoeher_subvention, wi_preisbildung, wi_geschaeftsmodell
HAT_DOMINANT_MARKTMODELL: mm_plattform_vermittelt
TEIL_VON_PROGRAMM: prog_forschungsprojekt, prog_be_circular
ERHALT_FOERDERUNG_DURCH: brussels_capital_region
NUTZT_TOOL: tool_retile
LIEGT_IN_STADT: stadt_bruessel (existing)
LIEGT_IN_LAND: land_belgien (existing)
```

---

## 5. Circl Pavilion Amsterdam (canonical `p_circl_abn_amro` post-merge)

**Quelle:** `qu_circl_pavilion_dossier` + external_reference Quellen (see Quellen section below)

### Phase 1c merge: `p_pavilion_circl_amsterdam → p_circl_abn_amro`
Migrate properties (UNION, do not overwrite):
- `gross_floor_area: 2000` (m²)
- `bgf_m2: 2000`
- `fertigstellung_jahr: 2017`
- `bau_jahr_von: 2016`
- `year_opened_date: "2017-09-05"`
- `date_dismantled: "2025-03"`
- `bauwerkstatus: "rueckgebaut"`
- `adresse: "Gustav Mahlerplein, Amsterdam Zuidas"`

Migrate rels (per CORRECTIONS F2):
- `michel_baars -[ASSOZIIERT_MIT_PROJEKT]-> p_circl_abn_amro` (incoming, retarget if pavilion was target)
- `BELEGT_IN → q_actor_michel_baars_02`, `q_actor_michel_baars_03` (copy)
- `HAT_DOMINANT_MARKTMODELL → mm_intra_konzern` (copy)
- BELEGT_IN to `q_akteursliste_master_md` → SKIP (already on canonical)

### Existing actors to link
| id | name |
|---|---|
| `michel_baars` | Michel Baars (already linked) |
| `hans_hammink` | Hans Hammink (verify) |

### New actors (15)

| id | name | role | GEHÖRT_ZU |
|---|---|---|---|
| `de_architekten_cie` | de Architekten Cie. | arch | — |
| `abn_amro` | ABN AMRO | client | — |
| `tu_delft` | TU Delft | research (verify exists) | — |
| `bam_bouw_techniek` | BAM Bouw + Techniek | contract | bam (parent if exists) |
| `traject` | TRAJECT | person+manage (or unternehmen, verify) | — |
| `donkergroen` | Donkergroen | landscape | — |
| `new_horizon_urban_mining` | New Horizon Urban Mining | broker | — |
| `lcp_circulair` | lcp-circulair | decon | — |
| `icon_real_estate` | Icon Real Estate | client | victory_group |
| `victory_group` | Victory Group | client | — |
| `ter_velde_den_besten` | Ter Velde & Den Besten | software (3D scanning) | — |
| `vermaat` | Vermaat | ar_betrieb_nutzung + at_unternehmen | — |
| `exasun` | Exasun | supplier | — |
| `fagerhult` | Fagerhult | supplier | — |
| `de_groot_en_visser` | De Groot & Visser | supplier | — |

### Bauwerks
| id | name | role | class | status |
|---|---|---|---|---|
| `bw_circl_pavilion_amsterdam` | Circl Pavilion AMS | bor_donorobjekt (now dismantled) | bok_pavillon | status_rueckgebaut |

### Programme (1 new)
| id | name |
|---|---|
| `prog_abn_amro_mission_2030` | ABN AMRO Mission 2030 |

### Software / Tool
| id | label | name |
|---|---|---|
| `software_llmnt` | Software | LLMNT material passport platform |

### Bauteilgruppen (16 — per Plan 2 6i with corrections applied)

Convention reminder: `bg_<reuse-status>_<material>_<bauteiltyp>_<discriminator>`. All EINGEBAUT_IN → `bw_circl_pavilion_amsterdam` (now donor — but the components were *installed* there originally).

| id | name (≤25) | reuse_status | Notes (Funktionswechsel?) |
|---|---|---|---|
| `bg_reuse_holz_belag_circl_window_frame_floor` | `Circl Fenster→Boden` | reuse | **FW: window frame → floor** |
| `bg_reuse_mineralisch_belag_circl_pcm_tiles` | `Circl PCM-Fliesen` | reuse | Recycled concrete + PCM tiles |
| `bg_dismantled_holz_mehrere_circl_larch_structure` | `Circl Lärchentragwerk` | dismantled | DfD larch (2017 → dismantled 2024) |
| `bg_reuse_daemmstoff_daemmung_circl_jeans_insulation` | `Circl Jeans-Dämmung` | reuse | **FW: jeans → ceiling insulation** (16,000 jeans) |
| `bg_reuse_mehrere_fenster_circl_conference_windows` | `Circl Bürofenster` | reuse | From demolished office buildings (no specific donor BW) |
| `bg_reuse_mehrere_ausbau_circl_restored_furniture` | `Circl ABN-Möbel` | reuse | Refurbished ABN AMRO furniture (intra-konzern) |
| `bg_planned_mehrere_technik_circl_leased_lifts` | `Circl Mietaufzüge` | planned | Leased; supplier retains ownership |
| `bg_planned_mehrere_technik_circl_leased_lighting` | `Circl Mietbeleuchtung` | planned | Leased (Fagerhult DC lighting) |
| `bg_reuse_metall_technik_circl_fire_hose_cabinets` | `Circl Löschkästen` | reuse | New Horizon urban mining |
| `bg_reuse_kunststoff_wand_circl_clothing_felt` | `Circl Textilfilz-Wand` | reuse | **FW: business clothing → wall felt** |
| `bg_planned_kunststoff_belag_circl_c2c_tarkett` | `Circl Tarkett C2C` | planned | Tarkett iQ One |
| `bg_planned_mehrere_fassade_circl_remountable_facade` | `Circl Remontierb.Fass.` | planned | De Groot & Visser + Donkergroen plant modules |
| `bg_dismantled_metall_fassade_circl_facade_sections` | `Circl Fassadensekt.` | dismantled | Aluminium with glass; some sawn (zk_eingeschraenkt) |
| `bg_dismantled_mehrere_boden_circl_floor_structure` | `Circl Bodenaufbau` | dismantled | Less suitable for reuse (zk_eingeschraenkt) |
| `bg_dismantled_mehrere_technik_circl_solar_panels` | `Circl Solar` | dismantled | 500 panels, 7 years old (Exasun) |
| `bg_reuse_mehrere_ausbau_circl_greenery_harvest` | `Circl Bepflanzung` | reuse | Harvested by local residents |

### Project-level vocab
```
HAT_INTERVENTION: bai_neubau
HAT_NUTZUNG: nut_buero, nut_mischnutzung
HAT_METHODE: meth_design_for_disassembly, meth_zirkulaere_ausschreibung, meth_urban_mining, meth_abrissmonitoring
HAT_DOMINANT_MARKTMODELL: mm_intra_konzern
HAT_WIRTSCHAFT: wi_capex_hoeher_marketing_payback, wi_restwert
NUTZT_SOFTWARE: software_llmnt
TEIL_VON_PROGRAMM: prog_abn_amro_mission_2030
LIEGT_IN_STADT: stadt_amsterdam (NEW)
LIEGT_IN_LAND: land_niederlande (existing)
NUTZT_BAUWERK: bw_circl_pavilion_amsterdam
```

---

## 6. LYSP8 Basel (`p_lysp8_basel`)

**Quelle:** `qu_lysp8_basel_dossier`, source_file `LYSP8_Basel.md`

### Existing actors (PRECHECK)
| id |
|---|
| `kerstin_mueller` (or `kerstin_müller` — verify which) |
| `kevin_straub` |
| `marc_angst` |
| `marc_loeliger` |
| `baubuero_in_situ` (or `baubureau_in_situ` — verify) |
| `stiftung_habitat` (degree-0 stub — KEEP per PARKED_DECISIONS) |
| `eitel_partner` (degree-1 stub — KEEP per PARKED_DECISIONS) |
| `zirkular_gmbh` (canonical post-1b merge) |

### New actors (10)

| id | name | role | GEHÖRT_ZU |
|---|---|---|---|
| `loeliger_strub_architektur` | Loeliger Strub Architektur GmbH | arch | — |
| `pirmin_jung_schweiz` | Pirmin Jung Schweiz AG | engineer | — |
| `oxara_ag` | Oxara AG | supplier | — |
| `repoxit_ag` | Repoxit AG | contract | — |
| `kibag` | KIBAG | supplier | — |
| `pascal_hentschel` | Pascal Hentschel | person+research | zirkular_gmbh |
| `rebecca_brandmayer` | Rebecca Brandmayer | person+research | zirkular_gmbh |
| `laia_meier` | Laia Meier | person+research | zirkular_gmbh |
| `martin_zeller_lysp8` | Martin Zeller | person+arch | loeliger_strub_architektur |

(Note: if `martin_zeller` already exists from SMS Zürich actor list, use that id — verify S27.)

### Bauwerk
| id | name | role | class | status |
|---|---|---|---|---|
| `bw_lysp8_basel` | LysP8 Basel | bor_empfaengerobjekt | bok_gebaeude | status_realisiert |

Properties: `bgf_m2: 2250`, `bau_jahr_bis: 2025`, `geschosse_anzahl_min: 6`, `geschosse_anzahl_max: 10`, `number_of_units: 27`, `site_area_m2: 686`, `volume_m3: 7170`, `adresse: "Weinlagerstrasse 33, 4056 Basel"`, `entwurfsstart_jahr: 2020`.

### Aliases (UNION required) — Projekt
Existing aliases (per NAMING_AND_PROPERTIES_PLAN.md:61) + new: `["LYSP8", "LysP8", "Parzelle 8 Lysbüchel Süd"]`.

### Bauteilgruppen (6)

| id | name (≤25) | reuse_status | EINGEBAUT_IN | Notes |
|---|---|---|---|---|
| `bg_reuse_mehrere_fassade_lysp8_external_mix` | `LYSP8 Fassade-Mix` | reuse | bw_lysp8_basel | tiles, shutters, fibre-cement, railings |
| `bg_reuse_holz_ausbau_lysp8_kitchens` | `LYSP8 Küchen ZH-Wohns.` | reuse | bw_lysp8_basel | Zurich housing estate kitchens (link to `mehr_als_wohnen`?) |
| `bg_reuse_metall_belag_lysp8_grating_steps` | `LYSP8 Gitterrost` | reuse | bw_lysp8_basel | Steel grating steps |
| `bg_reuse_mehrere_ausbau_lysp8_doors_tiles` | `LYSP8 Türen+Fliesen` | reuse | bw_lysp8_basel | Doors + tiles |
| `bg_planned_holz_mehrere_lysp8_dfd_frame` | `LYSP8 DfD Holzbau` | planned | bw_lysp8_basel | DfD timber frame |
| `bg_planned_lehm_erde_boden_lysp8_oxacrete` | `LYSP8 Oxacrete-Boden` | planned | bw_lysp8_basel | Oxara poured-earth floor |

### Wiederverwendungskette
- `k_lysp8_zuerich_kitchens` (Zurich housing estate kitchens → LYSP8)

### Project-level vocab
```
HAT_INTERVENTION: bai_neubau
HAT_NUTZUNG: nut_wohnen, nut_gewerbe
HAT_METHODE: meth_design_for_disassembly, meth_reuse_assessment, meth_building_material_scouting
REFERENZIERT_NORM: norm_sia_schweiz
HAT_DOMINANT_AKZEPTANZ: ak_oeffentlicher_bauherr_pilot
LIEGT_IN_STADT: stadt_basel (existing)
LIEGT_IN_LAND: land_schweiz (existing)
NUTZT_BAUWERK: bw_lysp8_basel
node_role: 'full_projekt'
```

---

## 7. MedUni Campus Mariannengasse Wien (`p_meduni_campus_mariannengasse`)

**Quelle:** `qu_meduni_mariannengasse_dossier`

### New actors (8)

| id | name | role | GEHÖRT_ZU |
|---|---|---|---|
| `baukarussell` | BauKarussell | reuse_consult | — |
| `big_bundesimmobilien` | BIG — Bundesimmobiliengesellschaft m.b.H. | client_pub | — |
| `meduni_wien` | Medizinische Universität Wien | client_pub (research+client) | — |
| `drz_demontage_recycling` | DRZ — Demontage- und Recycling-Zentrum | decon | — |
| `die_kuemmerei` | Die Kümmerei | decon | — |
| `wiener_aufzugmuseum` | Wiener Aufzugmuseum | ngo (museum receiver) | — |
| `markus_meissner` | Markus Meissner | person+manage | baukarussell |
| `thomas_romm` | Thomas Romm | person+arch (founder) | baukarussell |

### Bauwerk
| id | name | role | class | status |
|---|---|---|---|---|
| `bw_meduni_campus_mariannengasse` | MedUni Campus Wien | bor_donorobjekt | bok_gebaeude | status_rueckgebaut |

Properties: `adresse: "Mariannengasse, Vienna"`, `reuse_masse_kg: 60400`, `bau_jahr_von: 2020 (next phase)`, `bauwerkstatus: "demolished"`.

### Wiederverwendungskette
- `k_meduni_paternoster_to_aufzugmuseum` (Paternoster cabins → Wiener Aufzugmuseum)

### Bauteilgruppen (6)

| id | name (≤25) | reuse_status | EINGEBAUT_IN | Notes |
|---|---|---|---|---|
| `bg_reuse_mehrere_technik_medunicampus_paternoster` | `MedUni Paternoster` | reuse | (not embedded — donor batch) | Goes to Aufzugmuseum |
| `bg_reuse_metall_ausbau_medunicampus_bike_workshop` | `MedUni Fahrradwerkst.` | reuse | (donor — external receivers) | Donor batch |
| `bg_reuse_metall_ausbau_medunicampus_heavy_shelves` | `MedUni Schwerlastregale` | reuse | (donor) | — |
| `bg_retained_mehrere_decke_medunicampus_glasdecke` | `MedUni Jugendstildecke` | retained | bw_meduni_campus_mariannengasse | Same-site (mm_same_site) |
| `bg_reuse_holz_wand_medunicampus_doors_as_cladding` | `MedUni Türen→Wand` | reuse | (donor) | **FW: door → wall cladding** |
| `bg_dismantled_glas_keramik_technik_medunicampus_fluorescent` | `MedUni Leuchtstoffr.` | dismantled | (donor — hazardous removal) | — |

### Project-level vocab
```
HAT_INTERVENTION: bai_rueckbau, bai_neubau (subsequent)
HAT_NUTZUNG: nut_schule_bildung
HAT_METHODE: meth_pre_deconstruction_audit, meth_bauteilkatalogisierung, meth_materialinventur
HAT_HUERDE: h_aufbereitungsaufwand, h_logistikaufwand
HAT_DOMINANT_MARKTMODELL: mm_spende (some), mm_plattform_vermittelt
HAT_DOMINANT_AKZEPTANZ: ak_oeffentlicher_bauherr_pilot
TEIL_VON_PROGRAMM: prog_forschungsprojekt (verify)
LIEGT_IN_STADT: stadt_wien (verify exists)
LIEGT_IN_LAND: land_oesterreich (existing)
NUTZT_BAUWERK: bw_meduni_campus_mariannengasse
```

---

## 8. Stuttgart 210 + Jugendtreff Ingersheim

**Quelle:** `qu_stuttgart210_dossier`

### Phase 1d: relabel `p_stuttgart_210 → prog_stuttgart_210`
Set typed properties: `start_year: 2023`, `status: "active"`, `host_institution: "HTWG Konstanz"`.

### New child Projekt
- `p_jugendtreff_ingersheim` — built pilot 2024.

### New actors (14)

| id | name | role | GEHÖRT_ZU |
|---|---|---|---|
| `htwg_konstanz` | HTWG Konstanz | research | — |
| `hft_stuttgart` | HFT Stuttgart | research | — |
| `klingelhoefer_kroetsch` | Klingelhöfer Krötsch Architekten | arch | — |
| `gemeinde_ingersheim` | Gemeinde Ingersheim | client_pub | — |
| `faltlhauser_krapf` | Faltlhauser Krapf | struct | — |
| `proholz_bw` | proHolz Baden-Württemberg | ngo | — |
| `zueblin_timber_gmbh` | ZÜBLIN Timber GmbH | supplier | ed_zueblin_ag |
| `ed_zueblin_ag` | Ed. Züblin AG | contract | — |
| `andreas_kretzer` | Andreas Kretzer | person+arch | hft_stuttgart |
| `katharina_raabe` | Katharina Raabe | person+arch | — |
| `maximilian_stemmler` | Maximilian Stemmler | person+arch | — |
| `roman_kreuzer` | Roman Kreuzer | person+research | htwg_konstanz |
| `stefan_kroetsch` | Stefan Krötsch | person+arch (professor) | htwg_konstanz |
| `thomas_stark` | Thomas Stark | person+research | htwg_konstanz |
| `mlr_bw` | Ministerium für Ernährung, Ländlichen Raum und Verbraucherschutz BW | funder | — |

### Bauwerk
| id | name | role | class | status |
|---|---|---|---|---|
| `bw_jugendtreff_ingersheim` | Jugendtreff Ingersheim | bor_empfaengerobjekt | bok_pavillon | status_realisiert |
| `bw_stuttgart21_hauptbahnhof` | Stuttgart 21 Hauptbahnhof | bor_donorobjekt | bok_infrastruktur | status_realisiert |

Properties for `bw_jugendtreff_ingersheim`: `bgf_m2: 50`, `fertigstellung_jahr: 2024`, `adresse: "Baumwasenweg, 74379 Ingersheim"`.

### New Programme
| id | name |
|---|---|
| `prog_holzbau_offensive_bw` | Holzbau-Offensive Baden-Württemberg |

### Wiederverwendungskette
- `k_stuttgart21_clt_to_ingersheim` (Stuttgart 21 CLT formwork → multiple Reallabs, first pilot = Jugendtreff Ingersheim)

### Bauteilgruppen (3+)

| id | name (≤25) | reuse_status | EINGEBAUT_IN | AUS_BAUWERK | Notes |
|---|---|---|---|---|---|
| `bg_reuse_holz_mehrere_ingersheim_clt_structure` | `Ingersheim CLT-Bau` | reuse | bw_jugendtreff_ingersheim | bw_stuttgart21_hauptbahnhof | 12 curved CLT elements (**FW: formwork → structure**) |
| `bg_reuse_holz_ausbau_ingersheim_clt_secondary` | `Ingersheim CLT-Ausbau` | reuse | bw_jugendtreff_ingersheim | bw_stuttgart21_hauptbahnhof | Secondary elements |
| `bg_dismantled_holz_mehrere_stuttgart21_donor_stock` | `S21 CLT-Lager` | dismantled | (depot) | bw_stuttgart21_hauptbahnhof | 78 elements in depot for future reallabs |

### Project-level vocab (on `p_jugendtreff_ingersheim`)
```
HAT_INTERVENTION: bai_neubau
HAT_NUTZUNG: nut_kultur (Jugendtreff)
HAT_METHODE: meth_form_follows_availability, meth_urban_mining
HAT_HUERDE: h_geometrie_unkonventionell (curved formwork)
HAT_DOMINANT_MARKTMODELL: mm_forschungsprojekt_zuteilung
TEIL_VON_PROGRAMM: prog_stuttgart_210
ERHALT_FOERDERUNG_DURCH: prog_holzbau_offensive_bw
LIEGT_IN_STADT: stadt_ingersheim (NEW)
LIEGT_IN_LAND: land_deutschland (existing)
NUTZT_BAUWERK: bw_jugendtreff_ingersheim
```

---

## 9. Reallabor BE-WARE (`p_reallabor_be_ware`)

**Quelle:** `qu_beware_dossier`

### Existing actors (verify)
- `andrea_klinge`, `christof_ziegert`, `eike_roswag_klinge`, `matthew_crabbe`, `nina_pawlicki`, `uwe_seiler`, `nbl_studio`

### New actors (7)

| id | name | role |
|---|---|---|
| `natural_building_lab` | Natural Building Lab (NBL) | research (TU Berlin) |
| `zrs_architekten_ingenieure` | ZRS Architekten Ingenieure | arch |
| `tu_berlin` | TU Berlin | research |
| `bezirk_charlottenburg_wilmersdorf` | Bezirk Charlottenburg-Wilmersdorf | client_pub |
| `senatsverwaltung_wirtschaft_energie_berlin` | Berliner Senatsverwaltung für Wirtschaft, Energie und Betriebe | funder |
| `stadtmanufaktur` | Stadtmanufaktur | research |
| `sina_jansen` | Sina Jansen | person+research |

### Stadt nodes
- `stadt_berlin` (verify exists)
- `stadt_berlin_spandau` (NEW — district)
- `stadt_berlin_charlottenburg_wilmersdorf` (NEW)
- `stadt_berlin_treptow_koepenick` (NEW)
- `stadt_berlin_lichtenberg` (NEW)

(Alternative: keep all as `stadt_berlin` and use district as actor/property; simplifies graph.)

### Bauteilgruppen (3 — per Plan 2 6d, names tightened)

| id | name (≤25) | reuse_status | Notes |
|---|---|---|---|
| `bg_reuse_holz_mehrere_beware_local_timber` | `BE-WARE Altholz` | reuse | Local secondary timber for structural use |
| `bg_planned_mehrere_mehrere_beware_dfd_fitout` | `BE-WARE DfD Ausbau` | planned | DfD interior fitout (TULIUM) |
| `bg_reuse_mehrere_fundament_beware_flying_foundation` | `BE-WARE Flugfundament` | reuse | TULIUM flying foundation w/ recycled RC |

### Project-level vocab
```
HAT_INTERVENTION: (none — programme)
HAT_METHODE: meth_urban_mining, meth_materialinventur
TEIL_VON_PROGRAMM: prog_reallabor
ERHALT_FOERDERUNG_DURCH: senatsverwaltung_wirtschaft_energie_berlin (or new prog node)
LIEGT_IN_STADT: stadt_berlin
LIEGT_IN_LAND: land_deutschland
node_role: 'full_projekt'
```

---

## 10. Granby Workshop Liverpool (`p_granby_workshop`)

**Quelle:** `qu_granby_workshop_dossier`

### Existing actors (verify)
- `lewis_jones`
- `assemble` (or `assemble_studio` — verify canonical)

### New actors (4)

| id | name | role | GEHÖRT_ZU |
|---|---|---|---|
| `granby_workshop_cic` | Granby Workshop CIC | supplier (CIC) | — |
| `granby_4_streets_clt` | Granby 4 Streets CLT | client_pub (CLT) | — |
| `will_shannon` | Will Shannon | person+arch | assemble |

### Stadt
- `stadt_liverpool` (NEW)

### Bauwerk (optional — workshop premises)
| id | name | role | class | status |
|---|---|---|---|---|
| `bw_granby_workshop_liverpool` | Granby Workshop | bor_referenzobjekt | bok_innenausbau | status_realisiert |

Properties: `adresse: "1 Aspen Grove, Aspen Yard, Liverpool L8 0SR"`, `bauwerkstatus: "active"`.

### Bauteilgruppen (4)

| id | name (≤25) | reuse_status | EINGEBAUT_IN | Notes |
|---|---|---|---|---|
| `bg_reuse_mehrere_belag_granby_rock_terrazzo` | `Granby Rock Terrazzo` | reuse | (external receivers — no specific EINGEBAUT_IN) | **FW: bricks/slates → terrazzo** |
| `bg_reuse_ziegel_belag_granby_brick_slate_terrazzo` | `Granby Brick+Slate` | reuse | (external) | **FW** |
| `bg_reuse_mehrere_ausbau_granby_first_house_products` | `Granby Ersthausprod.` | reuse | (external) | Tiles/handles/fireplaces |
| `bg_reuse_mehrere_belag_granby_bespoke_waste` | `Granby Abfallmix` | reuse | (external) | Bespoke waste-stream |

Note: These BGs do NOT have EINGEBAUT_IN (Granby manufactures products that go to external receivers). HAT_BAUTEILGRUPPE from `p_granby_workshop` is the only graph connection.

### Norm
- `norm_bs_5385_5_2009` (NEW; reference for all 4 BGs via REFERENZIERT_NORM)

### Project-level vocab
```
HAT_INTERVENTION: (none — manufacturer)
HAT_METHODE: meth_form_follows_availability
HAT_HUERDE: h_heterogenitaet_chargen (waste-stream variability)
HAT_DOMINANT_AKZEPTANZ: ak_aesthetik_patinakultur  ← V&A + Crafts Council collections!
HAT_DOMINANT_MARKTMODELL: mm_kauf_gebraucht
TEIL_VON_PROGRAMM: (Granby Four Streets neighbourhood regeneration — possibly new prog)
LIEGT_IN_STADT: stadt_liverpool
LIEGT_IN_LAND: land_grossbritannien (verify)
node_role: 'full_projekt'
```

---

## 11. FCRBE (`prog_fcrbe`, post-relabel)

**Quelle:** `qu_fcrbe_dossier`. Also: `qu_interreg_nwe_fcrbe_dossier` is a DUPLICATE — merge into the same Quelle.

### Typed Programm properties
```
type: "Interreg"
lead_organisation: "Rotor"
start_year: 2018
end_year: 2023
status: "concluded"
eu_funding_programme: "Interreg North-West Europe"
short_description: "The project aimed to increase by 50% the amount of reclaimed building elements circulated in North-West Europe by 2032."
```

### New actors (10 persons + 7 orgs)

| id | name | role | GEHÖRT_ZU |
|---|---|---|---|
| `michael_ghyoot` | Michaël Ghyoot | person+research | rotor_asbl_vzw |
| `thornton_kay` | Thornton Kay | person+broker | salvo_ltd |
| `lara_perez_duenas` | Lara Pérez Duenas | person+manage | embuild |
| `jeroen_vrijders` | Jeroen Vrijders | person+research | buildwise |
| `sylvain_laurenceau` | Sylvain Laurenceau | person+research | cstb |
| `corinne_bernair` | Corinne Bernair | person+manage | brussels_environment |
| `duncan_baker_brown` (EXISTS w/ aliases!) | Duncan Baker-Brown | person+research | university_of_brighton |
| `merel_limbeek` | Merel Limbeek | person+manage | city_of_utrecht |
| `salvo_ltd` | Salvo Ltd | broker | — |
| `embuild` | Embuild | ngo | — |
| `buildwise` | Buildwise | research | — |
| `cstb` | CSTB | research | — |
| `brussels_environment` | Brussels Environment | funder | — |
| `university_of_brighton` | University of Brighton | research | — |
| `city_of_utrecht` | City of Utrecht | client_pub | — |
| `bellastock` | Bellastock | arch (reuse consult) | — |
| `hugo_topalov` (verify EXISTS) | Hugo Topalov | person+arch | bellastock |
| `sarah_westerfeld` (verify EXISTS) | Sarah Westerfeld | person+? | — |

### Interreg NWE FCRBE
The `Interreg_NWE_FCRBE.md` dossier is explicitly a duplicate. Migrate `p_interreg_nwe_fcrbe → prog_fcrbe` and add `prog_fcrbe -[GEHÖRT_ZU]-> prog_interreg_nwe` (existing parent Programm).

### Stadt nodes (new for partner cities)
- `stadt_anderlecht` (NEW, verify)
- `stadt_canterbury` (NEW)
- `stadt_utrecht` (NEW, verify)
- `stadt_delft` (existing? verify)
- `stadt_paris` (existing? verify)
- `stadt_esch_sur_alzette` (NEW)

### Land nodes
- `land_belgien`, `land_grossbritannien`, `land_frankreich`, `land_niederlande`, `land_luxemburg` (verify all)

---

## 12. REBRIDGE (`prog_rebridge`, post-relabel)

**Quelle:** `qu_rebridge_dossier`

### Typed Programm properties
```
type: "other"
start_year: 2025
end_year: 2028
status: "active"
eu_funding_programme: "Research Fund for Coal and Steel (RFCS)"
grant_agreement_reference: "101157419"
eu_contribution_eur: 1695121.69
lead_organisation: "University of Stuttgart / Institute of Lightweight Structures and Conceptual Design"
short_description: "The project develops scientific and technical foundations for safe reuse of steel components from decommissioned bridge structures."
```

### New Stadt nodes
- `stadt_stuttgart` (verify exists; LIEGT_IN_LAND land_deutschland)
- `stadt_delft` (verify)
- `stadt_eindhoven` (NEW)
- `stadt_coimbra` (NEW)

### New Land nodes (verify which exist)
- `land_portugal` (NEW or verify)
- `land_luxemburg` (verify)
- `land_italien` (verify)

### Project-level link
```
LIEGT_IN_STADT: stadt_stuttgart (lead), stadt_delft, stadt_eindhoven, stadt_coimbra
LIEGT_IN_LAND: land_deutschland, land_niederlande, land_portugal, land_luxemburg, land_italien
```

---

## 13. RE_USE Höfe (`prog_re_use_hoefe`, post-relabel)

**Quelle:** `qu_reusehoefe_dossier`

### Naming correction
- `name: "RE-USE Höfe"` (drop "Wien")
- `name_full: "RE-USE Höfe — zirkuläre Lieferketten anhand der Fensterwiederverwendung"`
- `aliases: ["RE_USE Höfe Wien", "REUSE Yards"]`

### New actors (4)

| id | name | role | GEHÖRT_ZU |
|---|---|---|---|
| `verein_re_win` | Verein RE-WIN | ngo | — |
| `zhaw_ike` | ZHAW Institut Konstruktives Entwerfen (IKE) | research | zhaw |
| `michelle_schneider_zhaw` | Michelle Schneider | person+research | zhaw_ike |
| `felix_dillmann` | Félix Dillmann | person+research | verein_re_win |

### Stadt + Land
- `stadt_basel` (existing)
- `stadt_winterthur` (NEW or verify)
- `land_schweiz` (existing)
- `land_ukraine` (NEW)

### Project-level vocab
```
type: research/publication programme
status: "published 2025-03-13"
LIEGT_IN_STADT: stadt_basel, stadt_winterthur
LIEGT_IN_LAND: land_schweiz, land_ukraine
short_description: "publication/project documenting RE-WIN and Windows for Ukraine experience and proposing reuse yards for circular window-reuse chains"
```

---

## 14. Reuse Logistics (`p_reuse_logistics` — KEEP as Projekt)

**Quelle:** `qu_reuselogistics_dossier`

### Decision (per CORRECTIONS C14/F13)
Do NOT relabel to Programm. Create parent `prog_urban_bricolage` and link.

### New parent Programm
| id | name |
|---|---|
| `prog_urban_bricolage` | Urban Bricolage (SNSF-PRIMA) |

Typed properties: `start_year: 2022`, `end_year: 2026`, `status: "active"`, `lead_organisation: "University of Fribourg"`, `funding_programme: "SNSF PRIMA"`.

### New actors (5)

| id | name | role | GEHÖRT_ZU |
|---|---|---|---|
| `madlen_kobi` | Madlen Kobi | person+research (PI) | university_of_fribourg |
| `university_of_fribourg` | University of Fribourg | research | — |
| `materialnomaden` | materialnomaden GmbH | broker | — |
| `elena_sischarenco` | Elena Sischarenco | person+research | university_of_fribourg |
| `vanessa_feri` | Vanessa Feri | person+research | university_of_fribourg |
| `adam_przywara` | Adam Przywara | person+research | university_of_fribourg |
| `rahel_jud` | Rahel Jud | person+research | university_of_fribourg |

### Stadt
- `stadt_fribourg` (NEW)
- `stadt_wien` (verify exists)

### Project-level
```
TEIL_VON_PROGRAMM: prog_urban_bricolage
LIEGT_IN_STADT: stadt_fribourg, stadt_wien
LIEGT_IN_LAND: land_schweiz, land_oesterreich
```

---

## 15. REFAIR Bordeaux

**Quelle:** `qu_refair_dossier`

### Decision (per CORRECTIONS C12)
Do NOT create Plattform label. Apply Software + Akteur + Bauwerk shape.

### Nodes to create

| Label | id | name |
|---|---|---|
| Software | `software_refair` | REFAIR (digital platform) |
| Akteur | `la_fabrique_de_bordeaux_metropole` | La Fab (operator) |
| Bauwerk | `bw_base_du_reemploi_merignac` | Base du Réemploi Mérignac (depot) |

Bauwerk properties: `adresse: "26 avenue de la Somme, 33700 Mérignac"`, `bauobjektrolle: bor_zwischenlager`, `bauobjektklasse: bok_reuse_centre`.

### New actors (people)

| id | name | role | GEHÖRT_ZU |
|---|---|---|---|
| `orianne_scourzic` | Orianne Scourzic | person+arch | collectif_cancan |
| `tiphaine_berthome` | Tiphaine Berthomé | person+manage | la_fabrique_de_bordeaux_metropole |
| `valerie_jamet` | Valérie Jamet | person+manage | la_fabrique_de_bordeaux_metropole |
| `aurelie_heraut` | Aurélie Héraut | person+manage | la_fabrique_de_bordeaux_metropole |
| `jerome_goze` | Jérôme Goze | person+manage | la_fabrique_de_bordeaux_metropole |
| `collectif_cancan` | Collectif CANCAN | arch | — |

### Stadt
- `stadt_bordeaux` (NEW)
- `stadt_merignac` (NEW)

### Migration
- Migrate old `p_refair_bordeaux_reemploi_platform` rels:
  - Generic project/research rels → tag to `la_fabrique_de_bordeaux_metropole` (Akteur)
  - Platform-specific rels → tag to `software_refair`
  - Then `delete_node p_refair_bordeaux_reemploi_platform` (after snapshot logged to rollback.md).

---

## 16. RCMI / Concular

**Quelle:** `qu_rcmi_concular_dossier`

### Decision (per CORRECTIONS C12)
RCMI is a Tool/workflow, not Plattform. Concular exists as Akteur.

### Nodes to create
| Label | id | name |
|---|---|---|
| Tool | `tool_rcmi` | RCMI — Reclaimed Construction Material Insurance |

### Existing Akteur to verify + enrich
- `concular` (Concular GmbH) — set properties: `legal_form: "GmbH"`, `registration_number: "HRB 773941"`, `founded_year: 2020`, `headquarters_city: "Berlin"`, `headquarters_country: "DE"`.

### New persons

| id | name | role | GEHÖRT_ZU |
|---|---|---|---|
| `dominik_campanella` | Dominik Campanella | person+manage (CEO) | concular |
| `julius_schaeufele` | Julius Schäufele | person+manage (Geschäftsführer) | concular |
| `lenard_da_costa_kurek` | Lenard da Costa Kurek | person+research | concular |

### Migration
- Migrate old `p_rcmi_concular` rels to Akteur `concular` (the operating organisation) or to `tool_rcmi`.
- `delete_node p_rcmi_concular` (after snapshot).

---

## 17-20. ETH Circular Construction, Architecture of Reuse BXL, Vandkunsten, ZHAW

### Decision (per CORRECTIONS C14)
These dossiers explicitly say `identified_programme: no/uncertain`. Do NOT promote to Programm.

### ETH Circular Construction
- DROP `prog_eth_circular_constr`. Use existing `prog_mas_dfab` (verified programme).
- Migrate `p_eth_circular_construction_student_reuse` rels into `prog_mas_dfab` via `merge_node` (with aliases UNION).
- Create 2 child Projekts:
  - `p_eggshell_pavilion`: `bgf_m2: ?`, `adresse: "Weil am Rhein, Germany"`, LIEGT_IN_STADT `stadt_weil_am_rhein` (NEW), LIEGT_IN_LAND `land_deutschland`, TEIL_VON_PROGRAMM `prog_mas_dfab`. 1 BG: `bg_reuse_mehrere_mehrere_eggshell_recycled_structure`.
  - `p_up_sticks_dundee`: LIEGT_IN_STADT `stadt_dundee` (NEW), LIEGT_IN_LAND `land_grossbritannien`, TEIL_VON_PROGRAMM `prog_mas_dfab`. 1 BG: `bg_reuse_holz_mehrere_upsticks_timber_frame`.

### Architecture of Reuse Brussels
- KEEP `p_architecture_of_reuse_brussels` as Projekt (not Programm).
- Tag to `rotor_asbl_vzw`, `rotor_dc`, `christine_conix`, `lionel_devlieger`, `maarten_gielen` (all already in graph — verify).

### Vandkunsten
- KEEP `p_vandkunsten_component_reuse` as Projekt.
- Tag to `vandkunsten` (existing), `katrine_west_kristensen`, `soren_nielsen`.

### ZHAW Reuse in Construction
- KEEP `p_reuse_in_construction_zhaw` as Projekt.
- Tag to `zhaw`, `andreas_sonderegger`, `eva_stricker`, `guido_brandi`, `zhaw_ike` (existing? verify).

---

## 21. OBK_27 deletion

### Action (per CORRECTIONS F17)
Before delete:
```cypher
MATCH (n {id:'p_obk_27'})-[r]-(m)
RETURN type(r), m.id, m.name, properties(r);
```
Log result in rollback.md. Then `delete_node p_obk_27` if no high-value rel.

---

## Quellen consolidated

### One `case_markdown` Quelle per dossier (18 distinct dossiers; Interreg_NWE_FCRBE merges into qu_fcrbe)

| id | source_file | quelltyp |
|---|---|---|
| `qu_batch1_schaerenmoosstrasse_dossier` | `batch 1.md` (§1) | case_markdown |
| `qu_batch1_umar_dossier` | `batch 1.md` (§2) | case_markdown |
| `qu_batch1_elementa_dossier` | `batch 1.md` (§3) | case_markdown |
| `qu_careno_becircular_dossier` | `Careno_Be_Circular_Brussels.md` | case_markdown |
| `qu_circl_pavilion_dossier` | `Circl_Pavilion_Amsterdam.md` | case_markdown |
| `qu_circl_abn_amro_dossier` | `Circl_ABN_AMRO_Urban_Mining.md` | case_markdown (duplicate; merge into qu_circl_pavilion_dossier) |
| `qu_lysp8_basel_dossier` | `LYSP8_Basel.md` | case_markdown |
| `qu_meduni_mariannengasse_dossier` | `MedUni_Campus_Mariannengasse_Wien.md` | case_markdown |
| `qu_stuttgart210_dossier` | `Stuttgart_210.md` | case_markdown |
| `qu_beware_dossier` | `Reallabor_Be_Ware.md` | case_markdown |
| `qu_reusehoefe_dossier` | `RE_USE_Hoefe_Wien.md` | case_markdown |
| `qu_granby_workshop_dossier` | `Granby_Workshop_Liverpool.md` | case_markdown |
| `qu_obk_27_dossier` | `OBK_27.md` | case_markdown (delete after archive) |
| `qu_fcrbe_dossier` | `FCRBE_Facilitating_Circulation_Reclaimed_Building_Elements.md` + `Interreg_NWE_FCRBE.md` | case_markdown |
| `qu_rebridge_dossier` | `REBRIDGE_Structural_Reuse.md` | case_markdown |
| `qu_reuselogistics_dossier` | `Reuse_Logistics.md` | case_markdown |
| `qu_refair_dossier` | `REFAIR_Bordeaux.md` | case_markdown |
| `qu_rcmi_concular_dossier` | `RCMI_Concular.md` | case_markdown |
| `qu_arch_reuse_bxl_dossier` | `Architecture_of_Reuse_Brussels.md` | case_markdown |
| `qu_eth_mas_dfab_dossier` | `ETH_Circular_Construction_Programme.md` | case_markdown |
| `qu_vandkunsten_dossier` | `Vandkunsten_Component_Reuse_Programme.md` | case_markdown |
| `qu_zhaw_reuse_dossier` | `ZHAW_Reuse_in_Construction.md` | case_markdown |

### High-value `external_reference` Quellen (≥3 BG/Akteur references; 1 per dossier minimum)

Per CORRECTIONS F16, add these for the densest sources. (~30 nodes total — list shortened here; full set in PLAN_v2 Phase 3.)

Selected examples:
- `qu_circl_dutcharchitects_s1` (S1 in Circl dossier; URL: https://dutcharchitects.org/projects/circl-amsterdam)
- `qu_circl_abnamro_opening_s3` (S3; URL: https://www.abnamro.com/...)
- `qu_circl_abnamro_report_s4` (S4)
- `qu_circl_zuidas_dismantling_s6` (S6; March 2025)
- `qu_careno_rotor_s1` (S1; https://rotordb.org/en/projects/careno-becircular)
- `qu_careno_retile_s2` (S2; https://rotordc.com/projects/re-tile)
- `qu_granby_assemble_s2` (S2)
- `qu_granby_rock_terrazzo_s3` (S3)
- `qu_lysp8_zirkular_s1`
- `qu_lysp8_swissarc_s2`
- `qu_lysp8_oxara_s4`
- `qu_meduni_baukarussell_s2`
- `qu_stuttgart210_baunetzwissen_s7`
- `qu_fcrbe_interreg_s1`
- `qu_rebridge_unistuttgart_r1`

---

**End of actor_extraction_per_dossier.md.**

Cross-references: [CORRECTIONS_2026-05-20.md](CORRECTIONS_2026-05-20.md) for issue rationale; [pre_flight_validation.cypher](pre_flight_validation.cypher) for live verification; [PLAN_v2.md](PLAN_v2.md) for the apply-time patch sequence.
