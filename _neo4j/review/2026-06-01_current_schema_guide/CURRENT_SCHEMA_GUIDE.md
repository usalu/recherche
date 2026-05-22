# Current Graph Schema Guide -- mit-bestand

**Snapshot:** 2026-06-01  -  **Nodes:** 39,165  -  **Relationships:** 80,135  -  **Labels:** 68  -  **Relationship types:** 85

Use this as the reference for how new nodes/edges should be shaped. Anything outside the conventions below should either reuse an existing pattern or be discussed before importing.

---

## 1. Naming conventions

Every domain/semantic node carries an `id` property (string, snake_case, ASCII-only). The prefix encodes the label:

| Label | Count | id prefix |
|---|---:|---|
| `Akteur` | 669 | (varies -- actor name slug, e.g. `bauteilboerse_bremen`) |
| `Akteurrolle` | 24 | `ar_*` |
| `Akteurtyp` | 10 | `at_*` |
| `Akzeptanz` | 7 | `ak_*` |
| `Aufbereitungsverfahren` | 62 | `auf_*` |
| `BauaufgabeIntervention` | 10 | `bai_*` |
| `Bauobjektklasse` | 8 | `bok_*` |
| `Bauobjektrolle` | 6 | `bor_*` |
| `Bauproduktstatus` | 15 | `bps_*` |
| `Bausystem` | 9 | `bsy_*` |
| `Bauteilebene` | 6 | `bte_*` |
| `Bauteilgruppe` | 356 | `bg_*` |
| `Bauteiltyp` | 23 | `bt_*` |
| `Bauweise` | 6 | `bauw_*` |
| `Bauwerk` | 184 | `bw_*` (or building name slug) |
| `BauwerkEra` | 6 | `era_*` |
| `Beschaffungsweg` | 10 | `bweg_*` |
| `DataIssue` | 28,729 | (see existing nodes) |
| `Defekt` | 10 | `def_*` |
| `DeprecatedType` | 13 | (see existing nodes) |
| `Dossier` | 97 | `dossier_*` |
| `DossierEntityTarget` | 2,591 | (see existing nodes) |
| `ExternalLink` | 5,017 | `q_url_*` |
| `Funktionswechsel` | 6 | `fw_*` |
| `Geltungsbereich` | 6 | (see existing nodes) |
| `Geschaeftsmodell` | 5 | `gm_*`  (new, added 2026-05-31) |
| `GraphVersion` | 0 | (see existing nodes) |
| `Huerde` | 28 | `hue_*` |
| `HuerdeKategorie` | 10 | `huek_*` |
| `Kennwert` | 255 | `kw_*` |
| `LCAModule` | 5 | `lca_*` |
| `Land` | 16 | `land_*` |
| `Layer` | 6 | `layer_*` |
| `Leistungsanforderung` | 46 | `la_*` |
| `Logistik` | 10 | `log_*` |
| `Marktmodell` | 11 | `mm_*`  (transaction type) |
| `MatchingQualitaet` | 9 | `mq_*` |
| `Material` | 26 | `mat_*` |
| `Materialdepot` | 22 | `bw_*_stock` / project-specific |
| `Materialgruppe` | 11 | `mg_*` |
| `Methode` | 13 | `meth_*` |
| `Norm` | 103 | `norm_*` |
| `Nutzung` | 9 | `nutz_*` |
| `OntologyAnchor` | 2 | (see existing nodes) |
| `Programm` | 29 | `prog_*` |
| `Projekt` | 86 | `proj_*` (or project name slug) |
| `Prozessphase` | 10 | `pp_*` |
| `PruefungNachweis` | 120 | `pn_*` |
| `Quelle` | 5,330 | `q_url_*` (URL hash) or `q_research_*_md` |
| `RechtlicheBedingung` | 16 | `rb_*` |
| `ResearchDocument` | 402 | `q_research_*_md` |
| `Ressourcenquelle` | 16 | `rq_*` |
| `ReuseRule` | 20 | `rr_*` |
| `Rueckbauverfahren` | 5 | `rbv_*` |
| `Schadstoff` | 9 | `schad_*` |
| `SectionRef` | 636 | varies -- section anchor |
| `Software` | 18 | `software_*` (or product slug) |
| `Stadt` | 74 | `stadt_*` |
| `Status` | 9 | `st_*` |
| `Tool` | 7 | `tool_*` |
| `Tragwerksprinzip` | 4 | `tw_*` |
| `Verbindungstechnik` | 15 | `vbt_*` |
| `WiederverwendungsArt` | 11 | `wva_*` |
| `Wiederverwendungskette` | 14 | `wvk_*` |
| `Wirtschaft` | 12 | `wi_*` |
| `ZertifizierungBewertungssystem` | 0 | (see existing nodes) |
| `Zertifizierungssystem` | 8 | `zert_*` |
| `ZustandsKlasse` | 6 | `zk_*` |

**Rules:**
- IDs MUST be unique within their label (uniqueness constraints exist on most controlled-vocab labels).
- IDs use lowercase ASCII + underscore. No hyphens, no spaces, no umlauts (`ae`, `oe`, `ue`, `ss`).
- Every node has `name` (display string, may include umlauts) and `id` (slug).
- Vocabulary nodes (`Akteurrolle`, `Akteurtyp`, `Methode`, etc.) carry `source_scope = 'controlled_vocab_seed'`.

---

## 2. Relationship patterns (from-label -> rel -> to-label, top 60)

| Pattern | Count |
|---|---:|
| `(:DataIssue)-[:CONCERNS]->(:Bauteilgruppe)` | 11,732 |
| `(:DossierEntityTarget)-[:CITED_FROM_DOSSIER]->(:Quelle)` | 6,104 |
| `(:DataIssue)-[:CONCERNS]->(:Quelle)` | 5,414 |
| `(:DataIssue)-[:CONCERNS]->(:Akteur)` | 5,038 |
| `(:DataIssue)-[:CONCERNS]->(:Projekt)` | 4,496 |
| `(:Projekt)-[:BELEGT_IN]->(:Quelle)` | 2,850 |
| `(:DataIssue)-[:CONCERNS]->(:Bauwerk)` | 2,306 |
| `(:Akteur)-[:HAT_AKTEURROLLE]->(:Akteurrolle)` | 1,336 |
| `(:DataIssue)-[:CONCERNS]->(:Schadstoff)` | 1,201 |
| `(:DataIssue)-[:CONCERNS]->(:Akteurrolle)` | 1,186 |
| `(:DataIssue)-[:CONCERNS]->(:Huerde)` | 1,135 |
| `(:Akteur)-[:BELEGT_IN]->(:Quelle)` | 913 |
| `(:DataIssue)-[:CONCERNS]->(:Land)` | 861 |
| `(:DataIssue)-[:CONCERNS]->(:Prozessphase)` | 822 |
| `(:Bauteilgruppe)-[:HAS_RISK_POLLUTANT]->(:Schadstoff)` | 791 |
| `(:Bauteilgruppe)-[:HAT_HUERDE]->(:Huerde)` | 759 |
| `(:Bauteilgruppe)-[:HAT_PROZESSPHASE]->(:Prozessphase)` | 700 |
| `(:DataIssue)-[:CONCERNS]->(:OntologyAnchor)` | 695 |
| `(:DataIssue)-[:CONCERNS]->(:Aufbereitungsverfahren)` | 676 |
| `(:DataIssue)-[:CONCERNS]->(:Bauteiltyp)` | 674 |
| `(:Akteur)-[:HAT_AKTEURTYP]->(:Akteurtyp)` | 673 |
| `(:DataIssue)-[:CONCERNS]->(:Status)` | 673 |
| `(:DataIssue)-[:CONCERNS]->(:Material)` | 667 |
| `(:DataIssue)-[:CONCERNS]->(:PruefungNachweis)` | 665 |
| `(:DataIssue)-[:CONCERNS]->(:Akteurtyp)` | 658 |
| `(:DataIssue)-[:CONCERNS]->(:Leistungsanforderung)` | 655 |
| `(:DataIssue)-[:CONCERNS]->(:WiederverwendungsArt)` | 624 |
| `(:DataIssue)-[:CONCERNS]->(:Methode)` | 621 |
| `(:Bauteilgruppe)-[:HAT_BAUTEILTYP]->(:Bauteiltyp)` | 592 |
| `(:DataIssue)-[:CONCERNS]->(:Ressourcenquelle)` | 577 |
| `(:Bauteilgruppe)-[:HAT_LEISTUNGSANFORDERUNG]->(:Leistungsanforderung)` | 548 |
| `(:DataIssue)-[:CONCERNS]->(:Materialgruppe)` | 523 |
| `(:DataIssue)-[:CONCERNS]->(:Logistik)` | 509 |
| `(:Akteur)-[:BETEILIGT_AN]->(:Projekt)` | 492 |
| `(:Bauteilgruppe)-[:HAT_RESSOURCENQUELLE]->(:Ressourcenquelle)` | 482 |
| `(:Bauteilgruppe)-[:HAT_MATERIALGRUPPE]->(:Materialgruppe)` | 475 |
| `(:Bauteilgruppe)-[:NUTZT_MATERIAL]->(:Material)` | 465 |
| `(:DataIssue)-[:CONCERNS]->(:Stadt)` | 432 |
| `(:Bauteilgruppe)-[:HAT_WIEDERVERWENDUNGSART]->(:WiederverwendungsArt)` | 425 |
| `(:Bauteilgruppe)-[:HAT_AUFBEREITUNG]->(:Aufbereitungsverfahren)` | 411 |
| `(:DataIssue)-[:CONCERNS]->(:Kennwert)` | 406 |
| `(:Bauteilgruppe)-[:HAT_METHODE]->(:Methode)` | 404 |
| `(:Bauteilgruppe)-[:HAT_LOGISTIK]->(:Logistik)` | 397 |
| `(:DataIssue)-[:CONCERNS]->(:Marktmodell)` | 391 |
| `(:Bauteilgruppe)-[:HAT_MARKTMODELL]->(:Marktmodell)` | 374 |
| `(:DataIssue)-[:CONCERNS]->(:Bauteilebene)` | 374 |
| `(:Bauteilgruppe)-[:HAT_BAUTEILEBENE]->(:Bauteilebene)` | 359 |
| `(:Bauteilgruppe)-[:BELEGT_IN]->(:Quelle)` | 357 |
| `(:Bauteilgruppe)-[:HAT_STATUS]->(:Status)` | 357 |
| `(:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)` | 350 |
| `(:Bauteilgruppe)-[:HAT_PRUEFUNG]->(:PruefungNachweis)` | 345 |
| `(:Projekt)-[:REQUIRES_VERIFICATION_FOR]->(:Schadstoff)` | 339 |
| `(:Bauteilgruppe)-[:INTO_RECEIVER]->(:Bauwerk)` | 320 |
| `(:DataIssue)-[:CONCERNS]->(:Rueckbauverfahren)` | 306 |
| `(:DataIssue)-[:CONCERNS]->(:Funktionswechsel)` | 301 |
| `(:Bauteilgruppe)-[:HAT_RUECKBAUVERFAHREN]->(:Rueckbauverfahren)` | 299 |
| `(:Akteur)-[:VERBUNDEN_MIT_AKTEUR]->(:Akteur)` | 298 |
| `(:DataIssue)-[:CONCERNS]->(:Norm)` | 297 |
| `(:DataIssue)-[:CONCERNS]->(:Beschaffungsweg)` | 294 |
| `(:Bauteilgruppe)-[:HAT_FUNKTIONSWECHSEL]->(:Funktionswechsel)` | 293 |

---

## 3. Controlled vocabularies (pick from these for new nodes)

### `:Akteurtyp`  --  What kind of actor
Link via `[:HAT_AKTEURTYP]`.  Count: **10**.

| id | name |
|---|---|
| `at_foerdergeber_programmtraeger` | Foerdergeber_Programmtraeger |
| `at_forschung_lehre` | Forschung_Lehre |
| `at_materialhub_bauteilboerse` | Materialhub_Bauteilboerse |
| `at_ngo_verband_netzwerk` | NGO_Verband_Netzwerk |
| `at_oeffentliche_institution` | Oeffentliche_Institution |
| `at_organisation` | Organisation |
| `at_person` | Person |
| `at_software_tool_anbieter` | Software_Tool_Anbieter |
| `at_unbekannt` | Unbekannt |
| `at_unternehmen` | Unternehmen |

### `:Akteurrolle`  --  What role(s) an actor plays
Link via `[:HAT_AKTEURROLLE]`.  Count: **24**.

| id | name |
|---|---|
| `ar_aufbereitung_refurbishment` | Aufbereitung_Refurbishment |
| `ar_bauausfuehrung_fertigung` | Bauausfuehrung_Fertigung |
| `ar_bauherr_auftraggeber` | Bauherr_Auftraggeber |
| `ar_betrieb_nutzung` | Betrieb_Nutzung |
| `ar_bildung_wissenstransfer` | Bildung_Wissenstransfer |
| `ar_brandschutz_barrierefreiheit` | Brandschutz_Barrierefreiheit |
| `ar_entwurf_planung` | Entwurf_Planung |
| `ar_fachplanung_nachweis` | Fachplanung_Nachweis |
| `ar_fassade` | Fassade |
| `ar_forschung_dokumentation` | Forschung_Dokumentation |
| `ar_kunst_gestaltung` | Kunst_Gestaltung |
| `ar_landschaftsplanung` | Landschaftsplanung |
| `ar_materialbroker` | Materialbroker / Reuse-Marketplace-Betreiber |
| `ar_materiallieferung_markt` | Materiallieferung_Markt |
| `ar_nachhaltigkeitsberatung` | Nachhaltigkeitsberatung |
| `ar_oeffentliche_hand_foerderung` | Oeffentliche_Hand_Foerderung |
| `ar_projektmanagement_koordination` | Projektmanagement_Koordination |
| `ar_reuse_zirkularitaetsberatung` | Reuse_Zirkularitaetsberatung |
| `ar_rueckbau_bauteilernte_logistik` | Rueckbau_Bauteilernte_Logistik |
| `ar_software_digitalisierung` | Software_Digitalisierung |
| `ar_stahlbau_fertigung` | Stahlbau_Fertigung |
| `ar_tga_gebaeudetechnik` | TGA_Gebaeudetechnik |
| `ar_tragwerksplanung` | Tragwerksplanung |
| `ar_unbestimmt` | Unbestimmt |

### `:Geschaeftsmodell`  --  Business-model archetype (new, 2026-05-31)
Link via `[:HAT_GESCHAEFTSMODELL]`.  Count: **5**.

| id | name |
|---|---|
| `gm_dienstleistung_urban_mining` | Urban-Mining-Dienstleister mit Verkaufskanal |
| `gm_marketplace_vermittlung` | Multi-Vendor-Marktplatz |
| `gm_netzwerk_aggregator` | Netzwerk / Aggregator / Redistribution |
| `gm_saas_inventar_plattform` | SaaS-Inventarplattform |
| `gm_shop_eigenstock` | Shop mit Eigenstock |

### `:Marktmodell`  --  Transaction type
Link via `[:HAT_MARKTMODELL]`.  Count: **11**.

| id | name |
|---|---|
| `mm_forschungsprojekt_zuteilung` | Forschungs-Zuteilung |
| `mm_intra_konzern` | Intra-Konzern |
| `mm_kauf_gebraucht` | Kauf gebraucht |
| `mm_kauf_neu` | Kauf neu-äquiv. |
| `mm_leasing` | Leasing |
| `mm_plattform_vermittelt` | Plattform-Kauf |
| `mm_rueckkauf` | Rückkauf |
| `mm_same_site` | Same-site |
| `mm_spende` | Spende |
| `mm_take_back_service` | Take-Back |
| `mm_unbekannt` | Unbekannt |

### `:Methode`  --  Methodologies / approaches
Link via `[:HAT_METHODE]`.  Count: **13**.

| id | name |
|---|---|
| `meth_abrissmonitoring` | Abrissmonitoring |
| `meth_bauteilkatalogisierung` | Bauteilkatalogisierung |
| `meth_building_material_scouting` | Building_Material_Scouting |
| `meth_design_for_disassembly` | Design_for_Disassembly |
| `meth_form_follows_availability` | Form_Follows_Availability |
| `meth_materialinventur` | Materialinventur |
| `meth_pre_deconstruction_audit` | Pre_Deconstruction_Audit |
| `meth_reuse_assessment` | ReUse_Assessment |
| `meth_reuse_ausschreibung` | ReUse_Ausschreibung |
| `meth_reversibilitaet` | Reversibilitaet |
| `meth_urban_mining` | Urban_Mining |
| `meth_wiederverwendungskriterien` | Wiederverwendungskriterien |
| `meth_zirkulaere_ausschreibung` | Zirkulaere_Ausschreibung |

### `:Material`  --  Material families (closed set)
Link via `[:NUTZT_MATERIAL]`.  Count: **26**.

| id | name |
|---|---|
| `mat_aluminium` | Aluminium |
| `mat_beton` | Beton |
| `mat_bitumen` | Bitumen |
| `mat_daemmstoff` | Daemmstoff |
| `mat_drahtglas` | mat_drahtglas |
| `mat_faserzement` | Faserzement / Eternit |
| `mat_glas` | Glas |
| `mat_gusseisen` | Gusseisen |
| `mat_holz` | Holz |
| `mat_holz_clt` | CLT / Brettsperrholz |
| `mat_keramik` | Keramik |
| `mat_kunststoff` | Kunststoff |
| `mat_kupfer` | Kupfer |
| `mat_lehm` | Lehm |
| `mat_mdf` | MDF / mitteldichte Faserplatte |
| `mat_mehrere` | Mehrere |
| `mat_messing` | Messing |
| `mat_naturstein` | Naturstein |
| `mat_pcm_phasenwechsel` | PCM |
| `mat_recyclingbeton` | Recyclingbeton |
| `mat_spannbeton` | mat_spannbeton |
| `mat_stahl` | Stahl |
| `mat_stahlbeton` | Stahlbeton |
| `mat_stroh` | Stroh |
| `mat_textil` | Textil |
| `mat_ziegel` | Ziegel |

### `:Materialgruppe`  --  Material coarse-group (closed set)
Link via `[:HAT_MATERIALGRUPPE]`.  Count: **11**.

| id | name |
|---|---|
| `mg_daemmstoff` | Daemmstoff |
| `mg_glas_keramik` | Glas_Keramik |
| `mg_holz_biobasiert` | Holz_Biobasiert |
| `mg_kunststoff` | Kunststoff |
| `mg_lehm_erde` | Lehm_Erde |
| `mg_mehrere` | Mehrere |
| `mg_metall` | Metall |
| `mg_mineralisch` | Mineralisch |
| `mg_recyclingmaterial` | Recyclingmaterial |
| `mg_unbekannt` | Unbekannt |
| `mg_verbundstoff` | Verbundstoff |

### `:Bauteiltyp`  --  Building-component types (closed set)
Link via `[:HAT_BAUTEILTYP]`.  Count: **23**.

| id | name |
|---|---|
| `bt_ausbau` | Ausbau |
| `bt_boden` | Boden |
| `bt_dach` | Dach |
| `bt_daemmung` | Daemmung |
| `bt_decke` | Decke |
| `bt_fassade` | Fassade |
| `bt_fassadenelement` | bt_fassadenelement |
| `bt_fassadenelement_beton` | bt_fassadenelement_beton |
| `bt_fassadenmodul_mauerwerk` | bt_fassadenmodul_mauerwerk |
| `bt_fenster` | Fenster |
| `bt_fundament` | Fundament |
| `bt_gelaender` | Gelaender |
| `bt_glasscheibe` | bt_glasscheibe |
| `bt_hohlkoerperdecke` | bt_hohlkoerperdecke |
| `bt_mauerstein` | bt_mauerstein |
| `bt_mehrere` | Mehrere |
| `bt_stuetze` | Stuetze |
| `bt_technik` | Technik |
| `bt_traeger` | Traeger |
| `bt_treppe` | Treppe |
| `bt_tuer` | Tuer |
| `bt_verglasung` | bt_verglasung |
| `bt_wand` | Wand |

### `:Bauteilebene`  --  Brand shearing layer
Link via `[:HAT_BAUTEILEBENE]`.  Count: **6**.

| id | name |
|---|---|
| `be_bauteilgruppe` | Bauteilgruppe |
| `be_einzelbauteil` | Einzelbauteil |
| `be_gebaeudeteil` | Gebaeudeteil |
| `be_materialcharge` | Materialcharge |
| `be_oberflaechenschicht` | Oberflaechenschicht |
| `be_system` | System |

### `:Bauweise`  --  Construction method
Link via `[:HAT_BAUWEISE]`.  Count: **6**.

| id | name |
|---|---|
| `bauw_fertigteilbauweise` | Fertigteilbauweise |
| `bauw_holzbauweise` | Holzbauweise |
| `bauw_hybridbauweise` | Hybridbauweise |
| `bauw_massivbauweise` | Massivbauweise |
| `bauw_ortbetonbauweise` | Ortbetonbauweise |
| `bauw_stahlbauweise` | Stahlbauweise |

### `:Beschaffungsweg`  --  Procurement route
Link via `[:HAT_BESCHAFFUNGSWEG]`.  Count: **10**.

| id | name |
|---|---|
| `bweg_ausschreibung` | Ausschreibung |
| `bweg_bauteilboerse` | Bauteilboerse |
| `bweg_digitale_plattform` | Digitale_Plattform |
| `bweg_direktvermittlung` | Direktvermittlung |
| `bweg_eigenbestand` | Eigenbestand |
| `bweg_informelles_netzwerk` | Informelles_Netzwerk |
| `bweg_lager` | Lager |
| `bweg_leihmodell` | Leihmodell |
| `bweg_rueckbauprojekt` | Rueckbauprojekt |
| `bweg_spende` | Spende |

### `:Logistik`  --  Logistics handling
Link via `[:HAT_LOGISTIK]`.  Count: **10**.

| id | name |
|---|---|
| `log_bauteiltracking` | Bauteiltracking |
| `log_just_in_time` | Just_in_Time |
| `log_lagerflaeche` | Lagerflaeche |
| `log_lagerung` | Lagerung |
| `log_lokale_wiederverwendung` | Lokale_Wiederverwendung |
| `log_materialmatching` | Materialmatching |
| `log_materialverfuegbarkeit` | Materialverfuegbarkeit |
| `log_transport` | Transport |
| `log_transportdistanz` | Transportdistanz |
| `log_zwischenlagerung` | Zwischenlagerung |

### `:WiederverwendungsArt`  --  Type of reuse
Link via `[:HAT_WIEDERVERWENDUNGSART]`.  Count: **11**.

| id | name |
|---|---|
| `wva_adaptives_reuse` | Adaptives_ReUse |
| `wva_bestandserhalt` | Bestandserhalt |
| `wva_design_for_disassembly` | Design_for_Disassembly |
| `wva_direkte_wiederverwendung` | Direkte_Wiederverwendung |
| `wva_recycling` | Recycling |
| `wva_refurbishment` | Refurbishment |
| `wva_remanufacturing` | Remanufacturing |
| `wva_same_site_reuse` | Same_Site_ReUse |
| `wva_upcycling` | Upcycling |
| `wva_urban_mining` | Urban_Mining |
| `wva_weiterbauen_im_bestand` | Weiterbauen_im_Bestand |

### `:Bauproduktstatus`  --  Product status / certification
Link via `[:HAT_BAUPRODUKTSTATUS]`.  Count: **15**.

| id | name |
|---|---|
| `bps_abz_abg` | abZ / aBG (DE) |
| `bps_baupg_ch` | BauPG (CH) |
| `bps_bestand_no_status` | Bestand vor Ort |
| `bps_ce_eta` | CE (ETA) |
| `bps_ce_hen` | CE (hEN) |
| `bps_ibc_104_11_alternative` | IBC 104.11 (USA) |
| `bps_jis_jas_mlit` | JIS/JAS/MLIT (JP) |
| `bps_nta_8713` | NTA 8713 (NL) |
| `bps_pemd_fr` | PEMD (FR) |
| `bps_project_specific` | Projekt-Freigabe |
| `bps_tracimat_be` | Tracimat (BE) |
| `bps_ue_zeichen` | Ü-Zeichen (DE) |
| `bps_ukca` | UKCA |
| `bps_unbekannt` | Status unbekannt |
| `bps_zie_vbg` | ZiE / vBG (DE) |

### `:ZustandsKlasse`  --  Condition class
Link via `[:HAT_ZUSTANDSKLASSE]`.  Count: **6**.

| id | name |
|---|---|
| `zk_eingeschraenkt_nachbearbeitung` | Eingeschränkt: Nacharbeit |
| `zk_eingeschraenkt_nutzungsklasse_reduzieren` | Eingeschränkt: downgrade |
| `zk_gebrauchsspuren_funktional` | Gebraucht, funktional |
| `zk_neuwertig` | Neuwertig |
| `zk_nicht_wiederverwendbar` | Nicht reusable |
| `zk_unbekannt_pruefung_offen` | Prüfung offen |

### `:Akzeptanz`  --  Acceptance criteria
Link via `[:HAT_AKZEPTANZ]`.  Count: **7**.

| id | name |
|---|---|
| `ak_aesthetik_patinakultur` | Patina-Ästhetik |
| `ak_breeam_zertifizierung` | BREEAM |
| `ak_dgnb_zertifizierung` | DGNB |
| `ak_humanitarian_purpose` | Humanitärer Zweck |
| `ak_leed_zertifizierung` | LEED |
| `ak_oeffentliche_sichtbarkeit_lernort` | Sichtbarkeit / Lernort |
| `ak_oeffentlicher_bauherr_pilot` | Public-Bauherr Pilot |

### `:BauwerkEra`  --  Era of building
Link via `[:BUILT_IN_ERA]`.  Count: **6**.

| id | name |
|---|---|
| `era_1900_1945` | 1900–1945 |
| `era_1970_1990` | 1970–1990 |
| `era_1990_2000` | 1990–2000 |
| `era_nachkrieg_1945_1970` | Nachkrieg 1945–1970 |
| `era_post_2000` | nach 2000 |
| `era_vor_1900` | vor 1900 |

---

## 4. Notes for `:Projekt` nodes

Current `:Projekt` count: **86**.  Sample property keys present on existing projects:

```
id, name
area_m2_gross
bewertung
co2_facts
cost_facts
invalid_candidate_source_urls
name_full
node_role
primary_source_url
projektstatus_text
quality_tier
quality_tier_facts
reuse_share_facts
review_status
source_count
source_freshness_summary
source_quality_summary
source_resolution_status
source_scope
source_trust_score
source_urls
strict_candidate_url_array_cleanup
strict_invalid_url_cleanup
strict_source_url_cleanup
year_completed
```

**Conventions for new `:Projekt` nodes:**

- `id` slug: `proj_<short_name>` or project-name-slug, lowercase, snake_case.
- `name`: human-readable project title (umlauts OK).
- Anchor to a country (`LIEGT_IN_LAND` -> `:Land`) and a city (`LIEGT_IN_STADT` -> `:Stadt`) if known.
- Attach evidence URLs via `BELEGT_IN` -> `:Quelle` (`:ExternalLink`).
- Actors involved attach via `BETEILIGT_AN`: `(:Akteur)-[:BETEILIGT_AN]->(:Projekt)`.
- Buildings the project relates to attach via `HAS_BAUWERK`: `(:Projekt)-[:HAS_BAUWERK]->(:Bauwerk)`.
- Reuse mechanism: link to `:Marktmodell`, `:Beschaffungsweg`, `:WiederverwendungsArt`.
- Building-physics characterisation: link to `:Material`, `:Bauteiltyp`, `:Bauteilebene`, `:Bauweise`.
- Source the project from a `:ResearchDocument` via `GEHOERT_ZU` if it comes from a curated research file.

---

## 5. Relationship property conventions

Every newly-created relationship should carry these properties so it's auditable and rollback-able:

| Property | Purpose | Example |
|---|---|---|
| `evidence_basis` | What pass/source produced it | `'pass8_strict_import_2026_05_31'` |
| `evidence_confidence` | Confidence ladder | `'belegt'` / `'wahrscheinlich'` / `'unsicher'` |
| `evidence_url` | First-party URL (optional but preferred) | `'https://...'` |
| `evidence_quote` | Verbatim source quote, <=240 chars | `'Material: Keramik'` |
| `review_run` | Tag for one-line rollback | `'bauteilboersen_finalest_30_2026_05_31'` |
| `created_at` | ISO timestamp | `datetime()` |

**MERGE pattern:**

```cypher
MATCH (a {id: $anchor_id}), (t:<Label> {id: $target_id})
MERGE (a)-[r:<REL>]->(t)
ON CREATE SET r.evidence_basis      = $basis,
              r.evidence_confidence = $conf,
              r.evidence_url        = $url,
              r.evidence_quote      = $quote,
              r.review_run          = $run,
              r.created_at          = datetime();
```

Use `MATCH (a {id: $anchor_id})` (no label) so the pattern also matches `:Software`-labelled nodes like `software_restado` that participate in the actor classification.

---

## 6. Constraints and indexes

| Name | Type | Label(s) | Properties |
|---|---|---|---|
| `akteur_id` | NODE_PROPERTY_UNIQUENESS | ['Akteur'] | ['id'] |
| `akteurrolle_id` | NODE_PROPERTY_UNIQUENESS | ['Akteurrolle'] | ['id'] |
| `akteurtyp_id` | NODE_PROPERTY_UNIQUENESS | ['Akteurtyp'] | ['id'] |
| `aufbereitungsverfahren_id` | NODE_PROPERTY_UNIQUENESS | ['Aufbereitungsverfahren'] | ['id'] |
| `bauaufgabeintervention_id` | NODE_PROPERTY_UNIQUENESS | ['BauaufgabeIntervention'] | ['id'] |
| `bauobjektklasse_id` | NODE_PROPERTY_UNIQUENESS | ['Bauobjektklasse'] | ['id'] |
| `bauobjektrolle_id` | NODE_PROPERTY_UNIQUENESS | ['Bauobjektrolle'] | ['id'] |
| `bausystem_id` | NODE_PROPERTY_UNIQUENESS | ['Bausystem'] | ['id'] |
| `bauteilebene_id` | NODE_PROPERTY_UNIQUENESS | ['Bauteilebene'] | ['id'] |
| `bauteilgruppe_id` | NODE_PROPERTY_UNIQUENESS | ['Bauteilgruppe'] | ['id'] |
| `bauteiltyp_id` | NODE_PROPERTY_UNIQUENESS | ['Bauteiltyp'] | ['id'] |
| `bauweise_id` | NODE_PROPERTY_UNIQUENESS | ['Bauweise'] | ['id'] |
| `bauwerk_id` | NODE_PROPERTY_UNIQUENESS | ['Bauwerk'] | ['id'] |
| `beschaffungsweg_id` | NODE_PROPERTY_UNIQUENESS | ['Beschaffungsweg'] | ['id'] |
| `funktionswechsel_id` | NODE_PROPERTY_UNIQUENESS | ['Funktionswechsel'] | ['id'] |
| `geschaeftsmodell_id` | NODE_PROPERTY_UNIQUENESS | ['Geschaeftsmodell'] | ['id'] |
| `graphversion_tag_unique` | NODE_PROPERTY_UNIQUENESS | ['GraphVersion'] | ['tag'] |
| `huerde_id` | NODE_PROPERTY_UNIQUENESS | ['Huerde'] | ['id'] |
| `huerdekategorie_id` | NODE_PROPERTY_UNIQUENESS | ['HuerdeKategorie'] | ['id'] |
| `land_id` | NODE_PROPERTY_UNIQUENESS | ['Land'] | ['id'] |
| `leistungsanforderung_id` | NODE_PROPERTY_UNIQUENESS | ['Leistungsanforderung'] | ['id'] |
| `logistik_id` | NODE_PROPERTY_UNIQUENESS | ['Logistik'] | ['id'] |
| `material_id` | NODE_PROPERTY_UNIQUENESS | ['Material'] | ['id'] |
| `materialgruppe_id` | NODE_PROPERTY_UNIQUENESS | ['Materialgruppe'] | ['id'] |
| `methode_id` | NODE_PROPERTY_UNIQUENESS | ['Methode'] | ['id'] |
| `norm_id` | NODE_PROPERTY_UNIQUENESS | ['Norm'] | ['id'] |
| `nutzung_id` | NODE_PROPERTY_UNIQUENESS | ['Nutzung'] | ['id'] |
| `programm_id` | NODE_PROPERTY_UNIQUENESS | ['Programm'] | ['id'] |
| `prozessphase_id` | NODE_PROPERTY_UNIQUENESS | ['Prozessphase'] | ['id'] |
| `pruefungnachweis_id` | NODE_PROPERTY_UNIQUENESS | ['PruefungNachweis'] | ['id'] |
| `quelle_id` | NODE_PROPERTY_UNIQUENESS | ['Quelle'] | ['id'] |
| `rechtlichebedingung_id` | NODE_PROPERTY_UNIQUENESS | ['RechtlicheBedingung'] | ['id'] |
| `rel_aus_bauwerk_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['AUS_BAUWERK'] | ['id'] |
| `rel_belegt_in_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['BELEGT_IN'] | ['id'] |
| `rel_beteiligt_an_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['BETEILIGT_AN'] | ['id'] |
| `rel_eingebaut_in_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['EINGEBAUT_IN'] | ['id'] |
| `rel_hat_akteurrolle_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_AKTEURROLLE'] | ['id'] |
| `rel_hat_akteurtyp_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_AKTEURTYP'] | ['id'] |
| `rel_hat_aufbereitung_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_AUFBEREITUNG'] | ['id'] |
| `rel_hat_bauobjektklasse_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_BAUOBJEKTKLASSE'] | ['id'] |
| `rel_hat_bauobjektrolle_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_BAUOBJEKTROLLE'] | ['id'] |
| `rel_hat_bausystem_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_BAUSYSTEM'] | ['id'] |
| `rel_hat_bauteilebene_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_BAUTEILEBENE'] | ['id'] |
| `rel_hat_bauteiltyp_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_BAUTEILTYP'] | ['id'] |
| `rel_hat_bauweise_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_BAUWEISE'] | ['id'] |
| `rel_hat_beschaffungsweg_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_BESCHAFFUNGSWEG'] | ['id'] |
| `rel_hat_funktionswechsel_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_FUNKTIONSWECHSEL'] | ['id'] |
| `rel_hat_huerde_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_HUERDE'] | ['id'] |
| `rel_hat_huerdekategorie_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_HUERDEKATEGORIE'] | ['id'] |
| `rel_hat_intervention_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_INTERVENTION'] | ['id'] |
| `rel_hat_leistungsanforderung_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_LEISTUNGSANFORDERUNG'] | ['id'] |
| `rel_hat_logistik_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_LOGISTIK'] | ['id'] |
| `rel_hat_materialgruppe_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_MATERIALGRUPPE'] | ['id'] |
| `rel_hat_methode_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_METHODE'] | ['id'] |
| `rel_hat_nutzung_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_NUTZUNG'] | ['id'] |
| `rel_hat_prozessphase_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_PROZESSPHASE'] | ['id'] |
| `rel_hat_pruefung_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_PRUEFUNG'] | ['id'] |
| `rel_hat_rechtliche_bedingung_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_RECHTLICHE_BEDINGUNG'] | ['id'] |
| `rel_hat_ressourcenquelle_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_RESSOURCENQUELLE'] | ['id'] |
| `rel_hat_rueckbauverfahren_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_RUECKBAUVERFAHREN'] | ['id'] |
| `rel_hat_schadstoff_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_SCHADSTOFF'] | ['id'] |
| `rel_hat_status_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_STATUS'] | ['id'] |
| `rel_hat_tragwerksprinzip_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_TRAGWERKSPRINZIP'] | ['id'] |
| `rel_hat_verbindungstechnik_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_VERBINDUNGSTECHNIK'] | ['id'] |
| `rel_hat_wiederverwendungsart_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_WIEDERVERWENDUNGSART'] | ['id'] |
| `rel_hat_wirtschaftsaspekt_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_WIRTSCHAFTSASPEKT'] | ['id'] |
| `rel_hat_zertifizierung_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['HAT_ZERTIFIZIERUNG'] | ['id'] |
| `rel_liegt_in_land_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['LIEGT_IN_LAND'] | ['id'] |
| `rel_liegt_in_stadt_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['LIEGT_IN_STADT'] | ['id'] |
| `rel_nutzt_bauwerk_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['NUTZT_BAUWERK'] | ['id'] |
| `rel_nutzt_material_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['NUTZT_MATERIAL'] | ['id'] |
| `rel_nutzt_software_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['NUTZT_SOFTWARE'] | ['id'] |
| `rel_nutzt_tool_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['NUTZT_TOOL'] | ['id'] |
| `rel_referenziert_norm_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['REFERENZIERT_NORM'] | ['id'] |
| `rel_teil_von_kette_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['TEIL_VON_KETTE'] | ['id'] |
| `rel_teil_von_programm_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['TEIL_VON_PROGRAMM'] | ['id'] |
| `rel_zitiert_quelle_id` | RELATIONSHIP_PROPERTY_UNIQUENESS | ['ZITIERT_QUELLE'] | ['id'] |
| `ressourcenquelle_id` | NODE_PROPERTY_UNIQUENESS | ['Ressourcenquelle'] | ['id'] |
| `rueckbauverfahren_id` | NODE_PROPERTY_UNIQUENESS | ['Rueckbauverfahren'] | ['id'] |
| `schadstoff_id` | NODE_PROPERTY_UNIQUENESS | ['Schadstoff'] | ['id'] |
| `software_id` | NODE_PROPERTY_UNIQUENESS | ['Software'] | ['id'] |
| `stadt_id` | NODE_PROPERTY_UNIQUENESS | ['Stadt'] | ['id'] |
| `status_id` | NODE_PROPERTY_UNIQUENESS | ['Status'] | ['id'] |
| `tool_id` | NODE_PROPERTY_UNIQUENESS | ['Tool'] | ['id'] |
| `tragwerksprinzip_id` | NODE_PROPERTY_UNIQUENESS | ['Tragwerksprinzip'] | ['id'] |
| `verbindungstechnik_id` | NODE_PROPERTY_UNIQUENESS | ['Verbindungstechnik'] | ['id'] |
| `wiederverwendungsart_id` | NODE_PROPERTY_UNIQUENESS | ['WiederverwendungsArt'] | ['id'] |
| `wiederverwendungskette_id` | NODE_PROPERTY_UNIQUENESS | ['Wiederverwendungskette'] | ['id'] |
| `wirtschaft_id` | NODE_PROPERTY_UNIQUENESS | ['Wirtschaft'] | ['id'] |
| `zertifizierungbewertungssystem_id` | NODE_PROPERTY_UNIQUENESS | ['ZertifizierungBewertungssystem'] | ['id'] |

Active range indexes:

| Name | Label(s) | Properties | State |
|---|---|---|---|
| `akteur_id` | ['Akteur'] | ['id'] | ONLINE |
| `akteurrolle_id` | ['Akteurrolle'] | ['id'] | ONLINE |
| `akteurtyp_id` | ['Akteurtyp'] | ['id'] | ONLINE |
| `aufbereitungsverfahren_id` | ['Aufbereitungsverfahren'] | ['id'] | ONLINE |
| `bauaufgabeintervention_id` | ['BauaufgabeIntervention'] | ['id'] | ONLINE |
| `bauobjektklasse_id` | ['Bauobjektklasse'] | ['id'] | ONLINE |
| `bauobjektrolle_id` | ['Bauobjektrolle'] | ['id'] | ONLINE |
| `bausystem_id` | ['Bausystem'] | ['id'] | ONLINE |
| `bauteilebene_id` | ['Bauteilebene'] | ['id'] | ONLINE |
| `bauteilgruppe_id` | ['Bauteilgruppe'] | ['id'] | ONLINE |
| `bauteiltyp_id` | ['Bauteiltyp'] | ['id'] | ONLINE |
| `bauweise_id` | ['Bauweise'] | ['id'] | ONLINE |
| `bauwerk_id` | ['Bauwerk'] | ['id'] | ONLINE |
| `beschaffungsweg_id` | ['Beschaffungsweg'] | ['id'] | ONLINE |
| `funktionswechsel_id` | ['Funktionswechsel'] | ['id'] | ONLINE |
| `geschaeftsmodell_id` | ['Geschaeftsmodell'] | ['id'] | ONLINE |
| `graphversion_tag_unique` | ['GraphVersion'] | ['tag'] | ONLINE |
| `huerde_id` | ['Huerde'] | ['id'] | ONLINE |
| `huerdekategorie_id` | ['HuerdeKategorie'] | ['id'] | ONLINE |
| `land_id` | ['Land'] | ['id'] | ONLINE |
| `leistungsanforderung_id` | ['Leistungsanforderung'] | ['id'] | ONLINE |
| `logistik_id` | ['Logistik'] | ['id'] | ONLINE |
| `material_id` | ['Material'] | ['id'] | ONLINE |
| `materialgruppe_id` | ['Materialgruppe'] | ['id'] | ONLINE |
| `methode_id` | ['Methode'] | ['id'] | ONLINE |
| `norm_id` | ['Norm'] | ['id'] | ONLINE |
| `nutzung_id` | ['Nutzung'] | ['id'] | ONLINE |
| `programm_id` | ['Programm'] | ['id'] | ONLINE |
| `prozessphase_id` | ['Prozessphase'] | ['id'] | ONLINE |
| `pruefungnachweis_id` | ['PruefungNachweis'] | ['id'] | ONLINE |
| `quelle_id` | ['Quelle'] | ['id'] | ONLINE |
| `rechtlichebedingung_id` | ['RechtlicheBedingung'] | ['id'] | ONLINE |
| `rel_aus_bauwerk_id` | ['AUS_BAUWERK'] | ['id'] | ONLINE |
| `rel_belegt_in_id` | ['BELEGT_IN'] | ['id'] | ONLINE |
| `rel_beteiligt_an_id` | ['BETEILIGT_AN'] | ['id'] | ONLINE |
| `rel_eingebaut_in_id` | ['EINGEBAUT_IN'] | ['id'] | ONLINE |
| `rel_hat_akteurrolle_id` | ['HAT_AKTEURROLLE'] | ['id'] | ONLINE |
| `rel_hat_akteurtyp_id` | ['HAT_AKTEURTYP'] | ['id'] | ONLINE |
| `rel_hat_aufbereitung_id` | ['HAT_AUFBEREITUNG'] | ['id'] | ONLINE |
| `rel_hat_bauobjektklasse_id` | ['HAT_BAUOBJEKTKLASSE'] | ['id'] | ONLINE |
| `rel_hat_bauobjektrolle_id` | ['HAT_BAUOBJEKTROLLE'] | ['id'] | ONLINE |
| `rel_hat_bausystem_id` | ['HAT_BAUSYSTEM'] | ['id'] | ONLINE |
| `rel_hat_bauteilebene_id` | ['HAT_BAUTEILEBENE'] | ['id'] | ONLINE |
| `rel_hat_bauteiltyp_id` | ['HAT_BAUTEILTYP'] | ['id'] | ONLINE |
| `rel_hat_bauweise_id` | ['HAT_BAUWEISE'] | ['id'] | ONLINE |
| `rel_hat_beschaffungsweg_id` | ['HAT_BESCHAFFUNGSWEG'] | ['id'] | ONLINE |
| `rel_hat_funktionswechsel_id` | ['HAT_FUNKTIONSWECHSEL'] | ['id'] | ONLINE |
| `rel_hat_huerde_id` | ['HAT_HUERDE'] | ['id'] | ONLINE |
| `rel_hat_huerdekategorie_id` | ['HAT_HUERDEKATEGORIE'] | ['id'] | ONLINE |
| `rel_hat_intervention_id` | ['HAT_INTERVENTION'] | ['id'] | ONLINE |
| `rel_hat_leistungsanforderung_id` | ['HAT_LEISTUNGSANFORDERUNG'] | ['id'] | ONLINE |
| `rel_hat_logistik_id` | ['HAT_LOGISTIK'] | ['id'] | ONLINE |
| `rel_hat_materialgruppe_id` | ['HAT_MATERIALGRUPPE'] | ['id'] | ONLINE |
| `rel_hat_methode_id` | ['HAT_METHODE'] | ['id'] | ONLINE |
| `rel_hat_nutzung_id` | ['HAT_NUTZUNG'] | ['id'] | ONLINE |
| `rel_hat_prozessphase_id` | ['HAT_PROZESSPHASE'] | ['id'] | ONLINE |
| `rel_hat_pruefung_id` | ['HAT_PRUEFUNG'] | ['id'] | ONLINE |
| `rel_hat_rechtliche_bedingung_id` | ['HAT_RECHTLICHE_BEDINGUNG'] | ['id'] | ONLINE |
| `rel_hat_ressourcenquelle_id` | ['HAT_RESSOURCENQUELLE'] | ['id'] | ONLINE |
| `rel_hat_rueckbauverfahren_id` | ['HAT_RUECKBAUVERFAHREN'] | ['id'] | ONLINE |
| `rel_hat_schadstoff_id` | ['HAT_SCHADSTOFF'] | ['id'] | ONLINE |
| `rel_hat_status_id` | ['HAT_STATUS'] | ['id'] | ONLINE |
| `rel_hat_tragwerksprinzip_id` | ['HAT_TRAGWERKSPRINZIP'] | ['id'] | ONLINE |
| `rel_hat_verbindungstechnik_id` | ['HAT_VERBINDUNGSTECHNIK'] | ['id'] | ONLINE |
| `rel_hat_wiederverwendungsart_id` | ['HAT_WIEDERVERWENDUNGSART'] | ['id'] | ONLINE |
| `rel_hat_wirtschaftsaspekt_id` | ['HAT_WIRTSCHAFTSASPEKT'] | ['id'] | ONLINE |
| `rel_hat_zertifizierung_id` | ['HAT_ZERTIFIZIERUNG'] | ['id'] | ONLINE |
| `rel_liegt_in_land_id` | ['LIEGT_IN_LAND'] | ['id'] | ONLINE |
| `rel_liegt_in_stadt_id` | ['LIEGT_IN_STADT'] | ['id'] | ONLINE |
| `rel_nutzt_bauwerk_id` | ['NUTZT_BAUWERK'] | ['id'] | ONLINE |
| `rel_nutzt_material_id` | ['NUTZT_MATERIAL'] | ['id'] | ONLINE |
| `rel_nutzt_software_id` | ['NUTZT_SOFTWARE'] | ['id'] | ONLINE |
| `rel_nutzt_tool_id` | ['NUTZT_TOOL'] | ['id'] | ONLINE |
| `rel_referenziert_norm_id` | ['REFERENZIERT_NORM'] | ['id'] | ONLINE |
| `rel_teil_von_kette_id` | ['TEIL_VON_KETTE'] | ['id'] | ONLINE |
| `rel_teil_von_programm_id` | ['TEIL_VON_PROGRAMM'] | ['id'] | ONLINE |
| `rel_zitiert_quelle_id` | ['ZITIERT_QUELLE'] | ['id'] | ONLINE |
| `ressourcenquelle_id` | ['Ressourcenquelle'] | ['id'] | ONLINE |
| `rueckbauverfahren_id` | ['Rueckbauverfahren'] | ['id'] | ONLINE |
| `schadstoff_id` | ['Schadstoff'] | ['id'] | ONLINE |
| `software_id` | ['Software'] | ['id'] | ONLINE |
| `stadt_id` | ['Stadt'] | ['id'] | ONLINE |
| `status_id` | ['Status'] | ['id'] | ONLINE |
| `tool_id` | ['Tool'] | ['id'] | ONLINE |
| `tragwerksprinzip_id` | ['Tragwerksprinzip'] | ['id'] | ONLINE |
| `verbindungstechnik_id` | ['Verbindungstechnik'] | ['id'] | ONLINE |
| `wiederverwendungsart_id` | ['WiederverwendungsArt'] | ['id'] | ONLINE |
| `wiederverwendungskette_id` | ['Wiederverwendungskette'] | ['id'] | ONLINE |
| `wirtschaft_id` | ['Wirtschaft'] | ['id'] | ONLINE |
| `zertifizierungbewertungssystem_id` | ['ZertifizierungBewertungssystem'] | ['id'] | ONLINE |

---

## 7. Minimal Cypher for adding a new project

```cypher
// 1. Create the project node
MERGE (p:Projekt {id: 'proj_my_new_one'})
ON CREATE SET p.name = 'My New One',
              p.source_scope = 'curated_import',
              p.review_run = '<your_run_tag>',
              p.created_at = datetime();

// 2. Country + city
MATCH (p:Projekt {id:'proj_my_new_one'}), (l:Land {id:'land_deutschland'})
MERGE (p)-[:LIEGT_IN_LAND]->(l);

// 3. Evidence URL(s)
MERGE (q:Quelle:ExternalLink {url:'https://...'})
ON CREATE SET q.id = 'q_url_<hash>',
              q.evidence_basis = 'curated_import_<date>',
              q.evidence_confidence = 'belegt';
WITH q
MATCH (p:Projekt {id:'proj_my_new_one'})
MERGE (p)-[:BELEGT_IN]->(q);

// 4. Reuse-mechanism classification
MATCH (p:Projekt {id:'proj_my_new_one'}), (m:Marktmodell {id:'mm_kauf_gebraucht'})
MERGE (p)-[r:HAT_MARKTMODELL]->(m)
ON CREATE SET r.evidence_basis='curated_import_<date>', r.evidence_confidence='belegt';

// 5. Building-physics signal -- Material + Bauteiltyp
MATCH (p:Projekt {id:'proj_my_new_one'}), (mat:Material {id:'mat_holz'})
MERGE (p)-[r:NUTZT_MATERIAL]->(mat)
ON CREATE SET r.evidence_basis='curated_import_<date>', r.evidence_confidence='belegt',
              r.evidence_url='https://...', r.evidence_quote='exact source quote';

// 6. Involved actors
MATCH (p:Projekt {id:'proj_my_new_one'}), (a {id:'<existing_actor_id>'})
MERGE (a)-[r:BETEILIGT_AN]->(p)
ON CREATE SET r.evidence_basis='curated_import_<date>', r.evidence_confidence='belegt';
```

---

## 8. Common pitfalls

1. **Use label-agnostic MATCH for anchor lookups** (`MATCH (a {id: ...})` not `MATCH (a:Akteur {id: ...})`) -- some legacy nodes carry a different label (`:Software`, `:Materialdepot`, etc.) but participate in actor classification.
2. **Pre-aggregate via `WITH count(...)` before RETURNing constants** -- `MATCH (g:NonExistentLabel) RETURN 'literal' AS x, count(g) AS y` returns 0 rows in Neo4j when the label has no nodes. Pattern fix: `OPTIONAL MATCH (g:X) WITH count(g) AS n RETURN ...`.
3. **`bt_mehrere` is reserved for explicit batches** -- don't use it as a 'unknown component' placeholder.
4. **Material claims need explicit material wording in source** -- 'Türen' alone is `bt_tuer` evidence, not `mat_holz` evidence. Don't infer material from component type.
5. **`Fliesen`/`carrelage`/`tiles` != `mat_keramik`** unless the source says `Keramik`/`céramique`/`ceramic` explicitly. Same for `Jern`/`Metall`/`Metaal` != `mat_stahl`.
6. **Third-party sources are leads, not strict imports** -- always prefer first-party fetched pages with line refs.
7. **Marktmodell vs Geschaeftsmodell are different axes:** Marktmodell (`mm_*`) = how the transaction works (Kauf, Spende, Leasing). Geschaeftsmodell (`gm_*`) = how the operator delivers value (Shop, Marketplace, Urban-Mining service, SaaS, Aggregator).
