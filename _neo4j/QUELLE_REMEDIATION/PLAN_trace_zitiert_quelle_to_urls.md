# Plan - trace every `:ZITIERT_QUELLE` to its actual URL

**Date:** 2026-05-22  
**Scope:** live Neo4j database `mit-bestand`; do not use `_archive/research/` as canonical input.  
**Goal:** completely replace the legacy semantic dependency on `:ZITIERT_QUELLE -> :ExternalLink` hops with explicit concrete URL properties on information-bearing nodes and relationships, while preserving provenance and review state.

This plan starts from the current rule: Neo4j is the source of truth. Local files are only used to explain lineage or rebuild reproducible artefacts after review.

---

## 0. Current live baseline

Read-only survey on `mit-bestand` found **8,229** `:ZITIERT_QUELLE` relationships.

| Start labels | End labels | Count | URL status |
|---|---:|---:|---|
| `:Quelle:ResearchDocument` | `:Quelle:ExternalLink` | 3,695 | end has `url` |
| `:Quelle:Dossier` | `:Quelle:ExternalLink` | 1,315 | end has `url` |
| `:Quelle:ExternalLink` | `:Quelle:ExternalLink` | 845 | end has `url` |
| `:Quelle:ExternalLink:SectionRef` | `:Quelle:ExternalLink` | 646 | end has `url` |
| `:Quelle:Dossier` | `:Quelle:ExternalLink:SectionRef` | 635 | end has `url` |
| `:Akteur` | `:Quelle:ExternalLink` | 366 | end has `url` |
| `:OntologyAnchor` | `:Quelle:ExternalLink` | 319 | end has `url` |
| `:Quelle:ExternalLink:ResearchDocument` | `:Quelle:ExternalLink` | 204 | end has `url` |
| `:Quelle:ResearchDocument` | `:Quelle:ExternalLink:ResearchDocument` | 193 | end has `url` |
| `:Quelle:Dossier` | `:Quelle:SectionRef` | 7 | end has `url` via `SectionRef` label mix? verify individually |
| `:Quelle:Dossier` | `:Quelle:Dossier` | 3 | **no URL; legacy topology artefact** |
| `:Projekt` | `:Quelle:ExternalLink` | 1 | end has `url` |

Relationship properties currently present:

| Property | Count |
|---|---:|
| `evidence_source_id`, `evidence_origin`, `evidence_confidence`, `evidence_basis` | 8,229 |
| `migration_origin`, `locator` | 6,759 |
| `evidence_excerpt` | 5,333 |
| `derivation_note` | 1,470 |
| `verification_status`, `verification_score`, `verification_method`, `verified_at`, `verification_attempts`, `verification_notes` | 1,335 |
| `verification_body_md5` | 857 |
| `id` | 563 |

Important boundary:
- **8,226 / 8,229** already terminate in URL-bearing nodes.
- The 3 non-URL edges are `q_batch_1_md -> Dossier` topology artefacts and must not be force-converted to URLs without review.
- Some live row-lineage edges named `:CITED_FROM_DOSSIER` carry a `source_url`, but the edge type is not source truth. The concrete dossier URL is the source truth; the target shape is a fact relationship or Claim carrying that exact URL.
- The same rule applies to every markdown container: building dossiers, Bauteilboerse files, `akteursliste_master.md`, registry files, and research `.md` files are not source truth. The links inside the relevant row/section are the source truth.
- Additional live survey: `:BELEGT_IN`, `:HAS_SOURCE_LINK`, and many domain relationships carry `evidence_source_id` / `evidence_origin` but no concrete `source_url`. Replacing `:ZITIERT_QUELLE` is therefore not enough; source URLs must be propagated to the information edge itself.

Strict end state:
- `MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r)` returns `0`.
- Every information-bearing relationship or Claim has a concrete `source_url`, or an explicit non-exact status.
- Every unresolved/non-URL provenance case has an explicit `:DataIssue` and `review_status`, not an implicit legacy source chain.
- `:ExternalLink` / `:UrlMetadata` nodes may remain as URL metadata, but they are no longer required to understand where a fact came from.

---

## 1. Provenance hunting overview

The migration must hunt concrete URLs through every currently observed provenance pattern. The table below is the working map; each row becomes a separate ledger class.

| Hunt kind | Live count | What it means | Required action |
|---|---:|---|---|
| Legacy source hop: `()-[:ZITIERT_QUELLE]->(url node)` | 8,226 of 8,229 | Old citation edges already point to URL-bearing nodes. | Copy `end.url` onto the relevant information-bearing edge/node, ledger it, then delete `:ZITIERT_QUELLE`. |
| Legacy non-URL hop: `()-[:ZITIERT_QUELLE]->(non-url)` | 3 of 8,229 | Current known case is `Dossier -> Dossier` topology residue. | Do not infer; review/retire with explicit `DataIssue`. |
| Dossier row URL already copied to lineage edge | 6,150 of 6,150 | Some row-level building traces already carry concrete URLs on an internal edge. | Use the URL value, not the edge type, as the reusable evidence. Accepted facts must copy that concrete URL onto the fact relationship or Claim. |
| Registry row URL, including `akteursliste_master.md` | review per row | Actor registry rows are containers with a `Links` column. | Use only the concrete links in the row as evidence for the actor/fact. The markdown file path itself is lineage only. |
| Research `.md` row/section URL | review per row/section | Research files are containers for tables/prose with links. | Use the concrete URL in the immediate row/section. Do not treat the research file node or file path as evidence. |
| Bauteilboerse `.md` URL list | review per file/section | Whole-file imports may have a `Quellen und Links` list. | Use the concrete URLs as candidates or exact evidence only when the scope is clear; the `.md` file itself is not evidence. |
| Direct URL endpoint: non-`ZITIERT_QUELLE` relationship ending at node with `.url` | 6,699, currently 0 with `source_url` | Facts/issues/source links point directly to `ExternalLink` / `SectionRef`, but the URL is still only on the node. | Copy endpoint `.url` onto the relationship before any URL-node dependency is removed. |
| `evidence_source_id` bridge | 24,146 relationships with `evidence_source_id` | Many domain edges point to a source id rather than a URL. | Resolve source id to source node; copy one URL as `source_url` or many as `source_urls`; unresolved goes to review. |
| Distinct source ids used by relationships | 934 ids | Source ids are mixed: graph nodes, run ids, legacy archive strings, free-text evidence. | Classify every id; graph-backed ids can be resolved automatically, non-graph ids require review or curated mapping. |
| Graph-backed source ids with URL-bearing source nodes | 620 of 934 distinct ids | These can be propagated without archive lookup. | Auto-copy URL set, preserving locator/evidence fields. |
| Source ids with no graph node | 284 of 934 distinct ids | Usually migration ids, archive strings, or free-text provenance. | Create review queue; do not silently trust retired archive paths. |
| Source ids with graph source but no URL | 30 of 934 distinct ids | Source node exists but lacks concrete URL path. | Review source node; add concrete URL or mark as non-URL provenance. |
| Node-level URL arrays/properties | 1,491 nodes | Some nodes already expose `source_urls`, `primary_source_url`, or `source_url`. | Preserve and use as fallback visibility; information edges still need their own URL trace. |

The hunt order is deterministic:

1. Prefer explicit `source_url` already on the relationship.
2. Else copy URL from direct URL endpoint.
3. Else resolve `evidence_source_id` to a source node and its concrete URL set.
4. Else use a row/section URL only when the exact row/section has a concrete URL; copy that URL onto the fact relationship or Claim.
5. Else add a review row; no archive-derived URL is accepted without explicit review.

---

## 2. Live node type sample catalogue

Generated live from Neo4j on 2026-05-23. Each row shows the current label count and up to seven examples. Labels with count `0` are still listed because they exist in the schema vocabulary and may affect cleanup gates.

| Node type / label | Count | 7 live examples |
|---|---:|---|
| `Akteur` | 648 | `2emain_be` (2emain.be); `2hs`; `3xn` (3XN); `51n4e` (51N4E); `CITYFOERSTER` (CITYFOERSTER); `Lendager`; `Natural_Building_Lab` (Natural Building Lab) |
| `Akteurrolle` | 24 | `ar_aufbereitung_refurbishment` (Aufbereitung_Refurbishment); `ar_bauausfuehrung_fertigung` (Bauausfuehrung_Fertigung); `ar_bauherr_auftraggeber` (Bauherr_Auftraggeber); `ar_betrieb_nutzung` (Betrieb_Nutzung); `ar_bildung_wissenstransfer` (Bildung_Wissenstransfer); `ar_brandschutz_barrierefreiheit` (Brandschutz_Barrierefreiheit); `ar_entwurf_planung` (Entwurf_Planung) |
| `Akteurtyp` | 10 | `at_foerdergeber_programmtraeger` (Foerdergeber_Programmtraeger); `at_forschung_lehre` (Forschung_Lehre); `at_materialhub_bauteilboerse` (Materialhub_Bauteilboerse); `at_ngo_verband_netzwerk` (NGO_Verband_Netzwerk); `at_oeffentliche_institution` (Oeffentliche_Institution); `at_organisation` (Organisation); `at_person` (Person) |
| `Akzeptanz` | 7 | `ak_aesthetik_patinakultur` (Patina-Aesthetik); `ak_breeam_zertifizierung` (BREEAM); `ak_dgnb_zertifizierung` (DGNB); `ak_humanitarian_purpose` (Humanitaerer Zweck); `ak_leed_zertifizierung` (LEED); `ak_oeffentliche_sichtbarkeit_lernort` (Sichtbarkeit / Lernort); `ak_oeffentlicher_bauherr_pilot` (Public-Bauherr Pilot) |
| `Aufbereitungsverfahren` | 62 | `av_aluminium_oberflaechenbehandlung`; `av_aluminium_reinigung_entdichtung` (Aluminium-Reinigung + Entdichtung); `av_aluminium_zuschnitt_bohrung` (Aluminium-Zuschnitt + Bohrung + Profilanpassung); `av_aluminiumfenster_beschlag_dichtung` (Aluminiumfenster Beschlaege + Dichtungen tauschen); `av_aluminiumfenster_pruefung_sortierung`; `av_beschichtung_entfernen`; `av_beton_anhaftungen_entfernen` (Reinigung von Beton-Anhaftungen) |
| `BauaufgabeIntervention` | 10 | `bai_aufstockung` (Aufstockung); `bai_erweiterung` (Erweiterung); `bai_fit_out` (Fit_out); `bai_neubau` (Neubau); `bai_rueckbau` (Rueckbau); `bai_sanierung` (Sanierung); `bai_translozierung` (Translozierung) |
| `Bauobjektklasse` | 8 | `bok_depot_lager` (Depot_Lager); `bok_gebaeude` (Gebaeude); `bok_gebaeudeteil` (Gebaeudeteil); `bok_infrastruktur` (Infrastruktur); `bok_innenausbau` (Innenausbau); `bok_pavillon` (Pavillon); `bok_quartier_areal` (Quartier_Areal) |
| `Bauobjektrolle` | 6 | `bor_bestandsobjekt` (Bestandsobjekt); `bor_donorobjekt` (Donorobjekt); `bor_empfaengerobjekt` (Empfaengerobjekt); `bor_referenzobjekt` (Referenzobjekt); `bor_same_site_donor_receiver` (Same_Site_Donor_Receiver); `bor_zwischenlager` (Zwischenlager) |
| `Bauproduktstatus` | 15 | `bps_abz_abg` (abZ / aBG (DE)); `bps_baupg_ch` (BauPG (CH)); `bps_bestand_no_status` (Bestand vor Ort); `bps_ce_eta` (CE (ETA)); `bps_ce_hen` (CE (hEN)); `bps_ibc_104_11_alternative` (IBC 104.11 (USA)); `bps_jis_jas_mlit` (JIS/JAS/MLIT (JP)) |
| `Bausystem` | 9 | `bsys_betonfertigteil_system` (Betonfertigteil_System); `bsys_cross_laminated_secondary_timber_clst` (CLST_cross_laminated_secondary_timber); `bsys_holz_skelettbau` (Holz_Skelettbau); `bsys_holzrahmenbau` (Holzrahmenbau); `bsys_iw73` (IW73/6_Plattenbausystem); `bsys_p2_plattenbausystem` (P2_Plattenbausystem); `bsys_plattenbau` (Plattenbau) |
| `Bauteilebene` | 6 | `be_bauteilgruppe` (Bauteilgruppe); `be_einzelbauteil` (Einzelbauteil); `be_gebaeudeteil` (Gebaeudeteil); `be_materialcharge` (Materialcharge); `be_oberflaechenschicht` (Oberflaechenschicht); `be_system` (System) |
| `Bauteilgruppe` | 369 | `bg_dismantled_glas_technik_medunicampus_fluorescent` (MedUni Leuchtstoffr.); `bg_dismantled_holz_mehrere_circl_larch_structure` (Circl Laerchentragwerk); `bg_dismantled_holz_mehrere_stuttgart21_donor_stock` (S21 CLT-Lager); `bg_dismantled_mehrere_boden_circl_floor_structure` (Circl Bodenaufbau); `bg_dismantled_mehrere_technik_circl_solar_panels` (Circl Solar); `bg_planned_holz_decke_elementa_brettstapel` (ELEMENTA Brettstapel); `bg_planned_holz_mehrere_lysp8_dfd_frame` (LysP8 DfD Holzbau) |
| `Bauteiltyp` | 23 | `bt_ausbau` (Ausbau); `bt_boden` (Boden); `bt_dach` (Dach); `bt_daemmung` (Daemmung); `bt_decke` (Decke); `bt_fassade` (Fassade); `bt_fassadenelement` |
| `Bauweise` | 6 | `bauw_fertigteilbauweise` (Fertigteilbauweise); `bauw_holzbauweise` (Holzbauweise); `bauw_hybridbauweise` (Hybridbauweise); `bauw_massivbauweise` (Massivbauweise); `bauw_ortbetonbauweise` (Ortbetonbauweise); `bauw_stahlbauweise` (Stahlbauweise) |
| `Bauwerk` | 186 | `bw_1_broadgate_1_2_broadgate_donor_stahl` (1 Broadgate); `bw_1_broadgate_london` (1 Broadgate, London); `bw_318_oxford_street_house_of_fraser` (318 Oxford Street); `bw_55_great_suffolk_street_warehouse` (55 Great Suffolk Street); `bw_alliander_existing_campus` (Bestandsensemble); `bw_alliander_hq_duiven` (Alliander); `bw_alte_kade_tiel` (Alte Kade in Tiel) |
| `BauwerkEra` | 6 | `era_1900_1945` (1900-1945); `era_1970_1990` (1970-1990); `era_1990_2000` (1990-2000); `era_nachkrieg_1945_1970` (Nachkrieg 1945-1970); `era_post_2000` (nach 2000); `era_vor_1900` (vor 1900) |
| `Beschaffungsweg` | 10 | `bweg_ausschreibung` (Ausschreibung); `bweg_bauteilboerse` (Bauteilboerse); `bweg_digitale_plattform` (Digitale_Plattform); `bweg_direktvermittlung` (Direktvermittlung); `bweg_eigenbestand` (Eigenbestand); `bweg_informelles_netzwerk` (Informelles_Netzwerk); `bweg_lager` (Lager) |
| `DataIssue` | 5907 | `di_actor_stub__CITYFOERSTER__p_recyclinghaus_hannover`; `di_actor_stub__Lendager__p_resource_rows_copenhagen`; `di_actor_stub__Lendager__p_upcycle_studios_copenhagen`; `di_actor_stub__Natural_Building_Lab__p_reallabor_be_ware`; `di_actor_stub__Natural_Building_Lab__prog_reallabor_be_ware`; `di_actor_stub__Superuse_Studios__p_bluecity_offices_rotterdam`; `di_actor_stub__Superuse_Studios__p_villa_welpeloo_enschede` |
| `Defekt` | 10 | `def_brandschaden` (Brandschaden); `def_chemische_belastung` (Chemisch belastet); `def_hohlraum_delamination` (Delamination); `def_holzwurm_pilzbefall` (Holzwurm/Pilz); `def_karbonatisierung` (Karbonatisierung); `def_keine_befunde` (Keine Befunde); `def_korrosion` (Korrosion) |
| `DeprecatedType` | 13 | `dep_label__GraphVersion`; `dep_label__LebenszyklusModul`; `dep_label__ZertifizierungBewertungssystem`; `dep_rel_type__ASSOZIIERT__MIT__PROJEKT`; `dep_rel_type__AUS__BAUWERK`; `dep_rel_type__BERECHNET__NACH__MODUL`; `dep_rel_type__EINGEBAUT__IN` |
| `Dossier` | 100 | `q_55_great_suffolk_street_london_md` (55_Great_Suffolk_Street); `q_architecture_of_reuse_brussels_md` (Architecture of Reuse Brussels); `q_association_house_groeditz_md` (Association_house_Groeditz); `q_association_house_plauen_md` (Association_house_Plauen); `q_awm_muenster_circular_office_md` (AWM_Muenster_Circular_Office); `q_batch_1_md` (Schaerenmoosstrasse Zuerich); `q_bedzed_london_hackbridge_md` (BedZED_London_Hackbridge) |
| `DossierEntityTarget` | 2591 | `det_0020ded6015328ef18e11bbf` (Flaeche Gesamtprojekt); `det_004186f92418ba6ed0c60186` (Betonbloecke Surplus); `det_0041ac8f71cf7115117459c5` (22 Wandplatten, 27 Deckenplatten); `det_00499b66d5e93d1cbe747143` (Sehr schwere Bauteile); `det_0060e5af83825bd3e412c884` (CO2 saving reused steel); `det_007bcfc09d78b0a3fba83232` (Fliesen / Kronkorken-Mosaik); `det_008cc7899a0ed72ab92c68e6` (Kostenreduktion) |
| `ExternalLink` | 5026 | `q_55_great_suffolk_street_london_s1` (ASBP - 55 Great Suffolk Street case study); `q_55_great_suffolk_street_london_s2` (New London Architecture - 55 Great Suffolk Street); `q_55_great_suffolk_street_london_s3` (Hawkins/Brown - 55 Great Suffolk Street); `q_55_great_suffolk_street_london_s4` (Opera PM - 55 Great Suffolk Street); `q_55_great_suffolk_street_london_s5` (UKGBC - 55 Great Suffolk Street); `q_55_great_suffolk_street_london_s6` (Architects Journal - Broadgate steel frame); `q_55_great_suffolk_street_london_s7` (RIBA Journal - Fabrix reused steel lessons) |
| `Funktionswechsel` | 6 | `fw_dekorative_funktion` (Dekorative_Funktion); `fw_gleiche_funktion` (Gleiche_Funktion); `fw_konstruktive_funktion` (Konstruktive_Funktion); `fw_neue_funktion` (Neue_Funktion); `fw_technische_funktion` (Technische_Funktion); `fw_unbekannt` (Unbekannt) |
| `GraphVersion` | 0 | (none) |
| `Huerde` | 28 | `h_akzeptanzproblem` (Akzeptanzproblem); `h_anschlussproblem` (Anschlussproblem); `h_aufbereitungsaufwand` (Aufbereitungsaufwand); `h_ausschreibungsproblem` (Ausschreibungsproblem); `h_bauproduktstatus` (Bauproduktstatus); `h_brandschutzkonflikt` (Brandschutzkonflikt); `h_bruch_beschaedigungsrisiko` (Bruch_Beschaedigungsrisiko) |
| `HuerdeKategorie` | 10 | `hk_beschaffung_markt` (Beschaffung_Markt); `hk_daten_evidenz` (Daten_Evidenz); `hk_logistisch` (Logistisch); `hk_planerisch` (Planerisch); `hk_rechtlich` (Rechtlich); `hk_sozial_organisatorisch` (Sozial_Organisatorisch); `hk_technisch` (Technisch) |
| `Kennwert` | 258 | `kw_p_55_great_suffolk_street_london_co2_saving_0`; `kw_p_55_great_suffolk_street_london_cost_0`; `kw_p_55_great_suffolk_street_london_cost_1`; `kw_p_55_great_suffolk_street_london_reuse_share_0`; `kw_p_55_great_suffolk_street_london_reuse_share_1`; `kw_p_association_house_groeditz_co2_saving_0`; `kw_p_association_house_groeditz_cost_0` |
| `LCAModule` | 5 | `lz_a1_a3` (A1-A3 Produkt); `lz_a4_a5` (A4-A5 Errichtung); `lz_b` (B1-B7 Nutzung); `lz_c` (C1-C4 End-of-Life); `lz_d` (D Beyond (Reuse)) |
| `Land` | 19 | `land_belgien` (Belgien); `land_daenemark` (Daenemark); `land_deutschland` (Deutschland); `land_eea` (Europaeischer Wirtschaftsraum (EU+EEA)); `land_eu` (Europaeische Union (Geltungsbereich)); `land_finnland` (Finnland); `land_frankreich` (Frankreich) |
| `Layer` | 6 | `layer_services` (Services); `layer_site` (Site); `layer_skin` (Skin); `layer_space_plan` (Space Plan); `layer_structure` (Structure); `layer_stuff` (Stuff) |
| `Leistungsanforderung` | 46 | `la_aesthetik`; `la_angemessene_anwendung`; `la_arbeitsschutz`; `la_bedienbarkeit`; `la_betriebssicherheit`; `la_brandschutz` (Brandschutz); `la_brandverhalten` |
| `Logistik` | 10 | `log_bauteiltracking` (Bauteiltracking); `log_just_in_time` (Just_in_Time); `log_lagerflaeche` (Lagerflaeche); `log_lagerung` (Lagerung); `log_lokale_wiederverwendung` (Lokale_Wiederverwendung); `log_materialmatching` (Materialmatching); `log_materialverfuegbarkeit` (Materialverfuegbarkeit) |
| `Marktmodell` | 11 | `mm_forschungsprojekt_zuteilung` (Forschungs-Zuteilung); `mm_intra_konzern` (Intra-Konzern); `mm_kauf_gebraucht` (Kauf gebraucht); `mm_kauf_neu` (Kauf neu-aequiv.); `mm_leasing` (Leasing); `mm_plattform_vermittelt` (Plattform-Kauf); `mm_rueckkauf` (Rueckkauf) |
| `MatchingQualitaet` | 9 | `mq_geographic_intl` (Geo: international); `mq_geographic_local` (Geo: lokal (<50 km)); `mq_geographic_regional` (Geo: regional); `mq_spec_anpassung` (Spec: Anpassung); `mq_spec_exact` (Spec: exakt); `mq_spec_zweckaenderung` (Spec: Zweckaenderung); `mq_temporal_easy` (Temporal: unproblematisch) |
| `Material` | 26 | `mat_aluminium` (Aluminium); `mat_beton` (Beton); `mat_bitumen` (Bitumen); `mat_daemmstoff` (Daemmstoff); `mat_drahtglas`; `mat_faserzement` (Faserzement / Eternit); `mat_glas` (Glas) |
| `Materialdepot` | 23 | `bw_bellastock_ville_des_terres_l_ile_saint_denis_lager` (Bellastock Ville des); `bw_berlin_fitout_donor_sources` (Berlin donors); `bw_chiro_itterbeek_reuse_supply_network` (Reuse-/Surplus-Liefernetz); `bw_cleveland_steel_and_tubes_stock` (Cleveland S&T stock); `bw_crclr_kindl_hall` (Ehemalige Lager-/Fassladehalle); `bw_donor_gebaudegruppe_resource_rows_mauerwerk` (Donor-Gebaeudegruppe); `bw_elys_ehemaliges_getraenkelager_areal` (Ehemaliges Getraenkelager) |
| `Materialgruppe` | 11 | `mg_daemmstoff` (Daemmstoff); `mg_glas_keramik` (Glas_Keramik); `mg_holz_biobasiert` (Holz_Biobasiert); `mg_kunststoff` (Kunststoff); `mg_lehm_erde` (Lehm_Erde); `mg_mehrere` (Mehrere); `mg_metall` (Metall) |
| `Methode` | 13 | `meth_abrissmonitoring` (Abrissmonitoring); `meth_bauteilkatalogisierung` (Bauteilkatalogisierung); `meth_building_material_scouting` (Building_Material_Scouting); `meth_design_for_disassembly` (Design_for_Disassembly); `meth_form_follows_availability` (Form_Follows_Availability); `meth_materialinventur` (Materialinventur); `meth_pre_deconstruction_audit` (Pre_Deconstruction_Audit) |
| `Norm` | 103 | `norm_bbl_nen` (Bbl/NEN); `norm_bbl_nen_links` (Bbl/NEN links); `norm_bs_4978` (BS 4978); `norm_cb_23_passports` (CB'23 passports); `norm_cen_ts_1090_201` (CEN/TS 1090-201); `norm_cen_ts_1090_201_2024` (CEN/TS 1090-201:2024); `norm_cen_ts_17440` (CEN/TS 17440) |
| `Nutzung` | 9 | `nut_buero` (Buero); `nut_gewerbe` (Gewerbe); `nut_infrastruktur` (Infrastruktur); `nut_kultur` (Kultur); `nut_lager_depot` (Lager_Depot); `nut_mischnutzung` (Mischnutzung); `nut_schule_bildung` (Schule_Bildung) |
| `OntologyAnchor` | 2 | `q_akteursliste_master_md` (akteursliste_master.md); `q_controlled_vocab_seed` (Controlled-vocab seed) |
| `Programm` | 29 | `p_architecture_of_reuse_brussels` (Architecture of Reuse); `p_eth_circular_construction_programme` (ETH Circular Construction Programme); `p_reuse_in_construction_zhaw` (Reuse in Construction); `p_reuse_logistics` (Reuse Logistics); `p_vandkunsten_component_reuse` (Vandkunsten Reused); `prog_abn_amro_mission_2030` (ABN AMRO Mission 2030); `prog_be_circular` (Be.Circular) |
| `Projekt` | 101 | `p_55_great_suffolk_street_london` (55 Great Suffolk Street); `p_association_house_groeditz` (Vereinshaus Groeditz); `p_association_house_plauen` (Vereinshaus Plauen); `p_awm_muenster_circular_office` (AWM Muenster); `p_bedzed_london_hackbridge` (BedZED); `p_berlin_schildow_pilot_house` (Berlin-Schildow Pilot); `p_bestandverplanzung_pavilion_muenchen` (Bestandverplanzung) |
| `Prozessphase` | 10 | `phase_aufbereitung` (Aufbereitung); `phase_betrieb` (Betrieb); `phase_dokumentation` (Dokumentation); `phase_identifikation` (Identifikation); `phase_lagerung` (Lagerung); `phase_planung` (Planung); `phase_pruefung` (Pruefung) |
| `PruefungNachweis` | 120 | `pn_ankerpruefung`; `pn_anwendungsbeschraenkung`; `pn_approval_process`; `pn_bauteilpass`; `pn_beschichtungszustand`; `pn_beschlagpruefung`; `pn_bewehrungsscan` |
| `Quelle` | 5343 | `q_55_great_suffolk_street_london_md` (55_Great_Suffolk_Street); `q_55_great_suffolk_street_london_s1` (ASBP - 55 Great Suffolk Street case study); `q_55_great_suffolk_street_london_s2` (New London Architecture - 55 Great Suffolk Street); `q_55_great_suffolk_street_london_s3` (Hawkins/Brown - 55 Great Suffolk Street); `q_55_great_suffolk_street_london_s4` (Opera PM - 55 Great Suffolk Street); `q_55_great_suffolk_street_london_s5` (UKGBC - 55 Great Suffolk Street); `q_55_great_suffolk_street_london_s6` (Architects Journal - Broadgate steel frame) |
| `RechtlicheBedingung` | 15 | `rb_bauordnungsrecht` (Bauordnungsrecht); `rb_bauproduktenverordnung_cpr` (Bauproduktenverordnung (CPR)); `rb_boulder_deconstruction_ordinance_8366` (Boulder Deconstruction Ordinance 8366 / 2020); `rb_ce_ukca_marking_reused_steel` (CE/UKCA marking for reused steel); `rb_denkmalschutz` (Denkmalschutz); `rb_dibt_zustimmung` (DIBt-Zustimmung im Einzelfall); `rb_eu_taxonomie` (EU_Taxonomie) |
| `ResearchDocument` | 403 | `q_aufbereitungsverfahren_reused_building_elements_md` (aufbereitungsverfahren_reused_building_elements.md); `q_bauteilreuse_legal_regime_matrix_md` (bauteilreuse_legal_regime_matrix.md); `q_circular_construction_economics_kg_md` (circular_construction_economics_kg.md); `q_circular_construction_reuse_graph_gaps_md` (circular_construction_reuse_graph_gaps.md); `q_connection_techniques_bauteilreuse_md` (connection_techniques_bauteilreuse.md); `q_energy_climate_reuse_research_md` (energy_climate_reuse_research.md); `q_research_55_great_suffolk_street_london_md` (55_Great_Suffolk_Street_London) |
| `Ressourcenquelle` | 16 | `rq_baustelle` (Baustelle); `rq_bauteilboerse` (Bauteilboerse); `rq_borrowed_material_pool` (Borrowed_Material_Pool); `rq_construction_waste_stream` (Construction_Waste_Stream); `rq_demolition_waste_stream` (Demolition_Waste_Stream); `rq_donor_infrastruktur` (Donor_Infrastruktur); `rq_donorgebaeude` (Donorgebaeude) |
| `ReuseRule` | 20 | `rr_be_beton` (Belgien x Beton reuse rule); `rr_be_holz` (Belgien x Holz reuse rule); `rr_be_naturstein` (Belgien x Naturstein reuse rule); `rr_be_stahl` (Belgien x Stahl reuse rule); `rr_ch_beton` (Schweiz x Beton reuse rule); `rr_ch_holz` (Schweiz x Holz reuse rule); `rr_ch_naturstein` (Schweiz x Naturstein reuse rule) |
| `Rueckbauverfahren` | 5 | `rv_ausbau_von_bauteilen` (Ausbau_von_Bauteilen); `rv_betonfraesen` (Betonfraesen); `rv_demontage` (Demontage); `rv_selektiver_rueckbau` (Selektiver_Rueckbau); `rv_zerstoerungsarme_bergung` (Zerstoerungsarme_Bergung) |
| `Schadstoff` | 9 | `s_asbest` (Asbest); `s_bleifarbe` (Bleifarbe); `s_formaldehyd` (Formaldehyd (MDF / Spanplatten)); `s_holzschutzmittel` (Holzschutzmittel); `s_kmf` (KMF - Kuenstliche Mineralfasern); `s_pak` (PAK); `s_pcb` (PCB) |
| `SectionRef` | 641 | `q_55_great_suffolk_street_london_s1` (ASBP - 55 Great Suffolk Street case study); `q_55_great_suffolk_street_london_s2` (New London Architecture - 55 Great Suffolk Street); `q_55_great_suffolk_street_london_s3` (Hawkins/Brown - 55 Great Suffolk Street); `q_55_great_suffolk_street_london_s4` (Opera PM - 55 Great Suffolk Street); `q_55_great_suffolk_street_london_s5` (UKGBC - 55 Great Suffolk Street); `q_55_great_suffolk_street_london_s6` (Architects Journal - Broadgate steel frame); `q_55_great_suffolk_street_london_s7` (RIBA Journal - Fabrix reused steel lessons) |
| `Software` | 19 | `software_bim` (Building Information Modeling / BIM); `software_concular` (Concular); `software_ecotool` (EcoTool); `software_inies` (INIES); `software_llmnt` (LLMNT); `software_opalis` (Opalis); `software_qflow` (Qflow) |
| `Stadt` | 76 | `stadt_aarhus` (Aarhus); `stadt_amsterdam` (Amsterdam); `stadt_arnhem` (Arnhem); `stadt_asse` (Asse); `stadt_auderghem_brussels` (Auderghem / Bruessel); `stadt_basel` (Basel); `stadt_berlin` (Berlin) |
| `Status` | 9 | `status_geplant` (Geplant); `status_in_bau` (In_Bau); `status_prototyp` (Prototyp); `status_realisiert` (Realisiert); `status_rueckgebaut` (Rueckgebaut); `status_temporaer` (Temporaer); `status_unklar` (Unklar) |
| `Tool` | 8 | `tool_bauteilkatalog` (Bauteilkatalog / Bauteilpass); `tool_bim_bauteilkatalog` (BIM / digitaler Bauteilkatalog); `tool_hts_stockmatcher` (HTS Reused Steel Stockmatcher); `tool_material_passports_maconda` (Material passports / Maconda data workflow); `tool_oogstkaart_harvest_map` (Oogstkaart / Harvest Map logic); `tool_qflow` (Qflow delivery and waste ticket tracking); `tool_rcmi` (RCMI) |
| `Tragwerksprinzip` | 4 | `tp_fachwerk` (Fachwerk); `tp_skeletttragwerk` (Skeletttragwerk); `tp_wand_kern_tragwerk` (Wand_Kern_Tragwerk); `tp_wandtragwerk` (Wandtragwerk) |
| `Verbindungstechnik` | 15 | `vt_bolzenverbindung` (Bolzenverbindung); `vt_demontierbarer_schwerlastanker` (Demontierbarer Schwerlastanker); `vt_holzduebel`; `vt_klemmverbindung` (Klemmverbindung); `vt_mauerwerk_ausgleich` (Mauerwerk_Ausgleichsschicht); `vt_mechanische_befestigung_unspezifiziert`; `vt_modulare_fassadenkassette` |
| `WiederverwendungsArt` | 11 | `wva_adaptives_reuse` (Adaptives_ReUse); `wva_bestandserhalt` (Bestandserhalt); `wva_design_for_disassembly` (Design_for_Disassembly); `wva_direkte_wiederverwendung` (Direkte_Wiederverwendung); `wva_recycling` (Recycling); `wva_refurbishment` (Refurbishment); `wva_remanufacturing` (Remanufacturing) |
| `Wiederverwendungskette` | 14 | `k_bestandserhalt_blackfriars_tragstruktur` (Bestandserhalt Blackfriars); `k_geplante_reuse_kette_broadgate_stahl_nach_blackfriars` (Geplante Reuse-Kette); `k_reuse_kette_brettschichtholzbogen_liege_bierset_nach_anderlecht` (Reuse-Kette Brettschichtholzbogen); `k_reuse_kette_btc_ville_des_terres_nach_stains` (Reuse-Kette BTC Ville); `k_reuse_kette_doppeltverglaste_holzfenster_nach_stains` (Reuse-Kette doppeltverglaste Holzfenster); `k_reuse_kette_drill_stem_pipe_dachtragwerk_nach_saxum_barn` (Drill-Stem-Pipe Dach); `k_reuse_kette_drill_stem_pipe_stutzen_nach_saxum_barn` (Drill-Stem-Pipe Stuetzen) |
| `Wirtschaft` | 12 | `wi_capex_hoeher_marketing_payback` (CapEx hoeher, Marketing-/Branding-Payback); `wi_capex_hoeher_opex_payback` (CapEx hoeher, Payback ueber OpEx / LCA); `wi_capex_hoeher_subvention` (CapEx hoeher, Subvention/Foerderung deckt Mehrkosten); `wi_capex_neutral` (CapEx vergleichbar mit Neubau); `wi_capex_niedriger_direkter_ersparnis` (CapEx niedriger); `wi_finanzierung` (Finanzierung); `wi_geschaeftsmodell` (Geschaeftsmodell) |
| `ZertifizierungBewertungssystem` | 0 | (none) |
| `Zertifizierungssystem` | 8 | `zbs_breeam` (BREEAM); `zbs_dgnb` (DGNB); `zbs_ecotool` (EcoTool (ZBS)); `zbs_leed` (LEED); `zbs_nabers` (NABERS); `zbs_nordic_swan_ecolabel` (Nordic Swan Ecolabel); `zbs_paris_proof` (Paris_Proof) |
| `ZustandsKlasse` | 6 | `zk_eingeschraenkt_nachbearbeitung` (Eingeschraenkt: Nacharbeit); `zk_eingeschraenkt_nutzungsklasse_reduzieren` (Eingeschraenkt: downgrade); `zk_gebrauchsspuren_funktional` (Gebraucht, funktional); `zk_neuwertig` (Neuwertig); `zk_nicht_wiederverwendbar` (Nicht reusable); `zk_unbekannt_pruefung_offen` (Pruefung offen) |

---

## 3. Deliverable shape

Create a reproducible migration run under:

`_neo4j/intake/runs/YYYY-MM-DD_trace_zitiert_quelle_to_urls/`

Expected artefacts:

| File | Purpose |
|---|---|
| `logs/zitiert_quelle_edge_inventory.jsonl` | one row per existing `:ZITIERT_QUELLE` relationship |
| `logs/zitiert_quelle_resolution_ledger.jsonl` | one row per relationship with resolved URL or explicit non-URL decision |
| `logs/information_source_url_ledger.jsonl` | one row per information-bearing relationship stamped with `source_url` / `source_urls` |
| `logs/source_url_unresolved_review.jsonl` | every information-bearing relationship still lacking a concrete URL |
| `reports/zitiert_quelle_trace_report.md` | counts, exceptions, before/after gates |
| `migrations/mig_trace_zitiert_quelle_to_urls.cypher` or runner | idempotent write migration |
| `migrations/mig_trace_zitiert_quelle_rollback.cypher` | rollback for edges/properties created by this run |

The ledger is the audit spine. Nothing gets deleted until every existing relationship is represented in that ledger.

---

## 4. Resolution model

For each existing `:ZITIERT_QUELLE` edge, write a ledger row with:

```json
{
  "zitiert_rel_element_id": "...",
  "zitiert_rel_id": "...",
  "start_id": "...",
  "start_labels": ["..."],
  "end_id": "...",
  "end_labels": ["..."],
  "resolved_url": "https://...",
  "resolved_url_node_id": "q_url_...",
  "locator": "S1",
  "evidence_basis": "...",
  "evidence_origin": "...",
  "evidence_excerpt": "...",
  "verification_status": "...",
  "migration_origin": "...",
  "resolution_status": "resolved_url | needs_review_non_url_end | retired_topology_artifact",
  "replacement_action": "copy_url_to_information_edge | copy_url_set_to_information_edge | mark_unresolved_review | delete_after_replacement"
}
```

Resolution rules:

1. If end node has `url`, set `resolved_url = end.url`.
2. If end node is `:SectionRef` and has `url`, set `resolved_url = end.url` but flag `source_kind = section_ref_url`.
3. If end node has no `url`, do not infer by name. Mark `needs_review_non_url_end`.
4. For the 3 `Dossier -> Dossier` artefacts, inspect their `derivation_note`, start/end IDs, and related `:DataIssue` records. Likely action: mark as `retired_topology_artifact`, not convert.
5. Preserve S2/S3 URL metadata by keeping the `ExternalLink` node as metadata, even if normal query paths stop depending on `:ZITIERT_QUELLE`.

For information-bearing relationships outside `:ZITIERT_QUELLE`:

1. If the relationship endpoint is a URL node, copy `end.url` onto the relationship as `source_url`.
2. If `r.evidence_source_id` points to a source node with one outgoing resolved URL, set `source_url`.
3. If `r.evidence_source_id` points to a source node with multiple outgoing resolved URLs and the existing relationship has no row locator, set `source_urls` to the complete URL list and set `source_resolution_status = 'url_set_requires_row_review'`.
4. If `r.evidence_source_id` is not a graph source node, do not use archived files by default. Set `source_resolution_status = 'needs_source_url_review'` and emit a review row.
5. If the relationship is inferential/topological, it still needs a source trace: either `source_urls` from the input evidence it was derived from, or `source_resolution_status = 'derived_no_direct_url_review_required'`.

---

## 5. Replacement targets by source type

The replacement should not be one generic edge. Use the source context.

| Current pattern | Replacement |
|---|---|
| `Dossier -[:ZITIERT_QUELLE]-> ExternalLink` | copy URL to `Dossier.source_urls` as inventory only; for row-level facts copy the concrete URL onto the fact relationship or Claim; then delete the `:ZITIERT_QUELLE` edge |
| `ResearchDocument -[:ZITIERT_QUELLE]-> ExternalLink` | copy URL to `ResearchDocument.source_urls` as inventory only; for row/section facts copy the concrete URL onto the fact relationship or Claim; then delete the `:ZITIERT_QUELLE` edge |
| `akteursliste_master.md` / registry source node -> `ExternalLink` | copy URL to registry inventory only; for actor identity/role/project facts copy the concrete row link onto the specific fact relationship or Claim |
| Bauteilboerse `.md` source node -> `ExternalLink` | copy URL to inventory only; if the file-level scope is clear, copy the concrete URL to the Materialdepot fact/Claim; otherwise keep as candidate |
| domain node (`Akteur`, `Projekt`) -> `ExternalLink` | copy URL to the domain relationship / node as `source_url`; then delete the `:ZITIERT_QUELLE` edge |
| `ExternalLink/SectionRef -> ExternalLink` | copy `target.url` into metadata properties such as `related_source_urls`; then delete the `:ZITIERT_QUELLE` edge |
| `OntologyAnchor -> ExternalLink` | copy URL to controlled-vocabulary evidence properties; then delete the `:ZITIERT_QUELLE` edge |
| `Dossier -> Dossier` | review/retire; no URL replacement unless a real cited URL is proven |

Target property contract for any replacement edge:

```cypher
source_url
source_url_node_id
source_urls
source_url_node_ids
source_url_status
source_url_http_code
source_url_wayback_snapshot
locator
evidence_source_id
evidence_origin
evidence_basis
evidence_confidence
evidence_excerpt
verification_status
verification_score
verification_method
verification_body_md5
migration_origin
supersedes_zitiert_rel_element_id
review_status
source_resolution_status
```

---

## 6. Execution phases

### Phase A - preflight and backup

Run:

```bash
python _scripts/_gap_survey.py
python _scripts/validate_no_text_content.py
```

Create a graph backup under `_neo4j/review/backups/` before any write.

Acceptance:
- current gap survey recorded in the run report;
- no `:Dossier.text_content` regression;
- backup path recorded.

### Phase B - inventory all legacy citation edges

Export every `:ZITIERT_QUELLE` edge from Neo4j into JSONL.

Cypher basis:

```cypher
MATCH (a)-[r:ZITIERT_QUELLE]->(b)
RETURN elementId(r) AS rel_element_id,
       r.id AS rel_id,
       labels(a) AS start_labels,
       a.id AS start_id,
       labels(b) AS end_labels,
       b.id AS end_id,
       b.url AS end_url,
       properties(r) AS rel_props,
       properties(b) AS end_props;
```

Acceptance:
- exported rows = live count of `:ZITIERT_QUELLE`;
- grouped counts match the baseline table or are explained by intervening work.

### Phase C - build the resolution ledger

Transform inventory into a ledger. The transform is read-only and deterministic.

Acceptance:
- `resolved_url` present for every URL-bearing end node;
- the only missing `resolved_url` rows are explicit review rows;
- no row resolves URL from name similarity or archived markdown.

### Phase D - write direct URL-bearing replacements

Write replacement properties/edges in an idempotent migration. This phase prepares deletion but does not delete `:ZITIERT_QUELLE` until Phase G gates pass.

Required writes:
- add `source_url` and `source_url_node_id` to each existing `:ZITIERT_QUELLE` where resolved, so the old edge is self-contained before deletion;
- add `source_url` to any relationship that directly points at a URL node (`BELEGT_IN`, `HAS_SOURCE_LINK`, `CONCERNS`, etc.);
- add `source_url` or `source_urls` to any information-bearing relationship whose `evidence_source_id` can be resolved through a source node's URL list;
- add `source_urls`, `source_count`, and `primary_source_url` to source-bearing container nodes (`Dossier`, `ResearchDocument`, `SectionRef`, registry source nodes) as inventory only;
- never treat `.md` source nodes or file paths as evidence; only their concrete row/section links can be promoted to `source_url`;
- create `:DataIssue` rows for information-bearing relationships that still lack concrete URL provenance.

Acceptance:

```cypher
MATCH ()-[r:ZITIERT_QUELLE]->(b)
WHERE b.url IS NOT NULL AND r.source_url <> b.url
RETURN count(r) AS bad;
```

Expected: `0`.

Information-edge acceptance:

```cypher
MATCH ()-[r]->()
WHERE (r.evidence_origin IS NOT NULL OR r.evidence_source_id IS NOT NULL)
  AND type(r) <> 'ZITIERT_QUELLE'
  AND r.source_url IS NULL
  AND (r.source_urls IS NULL OR size(r.source_urls) = 0)
  AND coalesce(r.source_resolution_status, '') <> 'needs_source_url_review'
RETURN type(r) AS rel_type, count(r) AS bad
ORDER BY bad DESC;
```

Expected: no rows.

### Phase E - update query surfaces

Update scripts/docs that still require the legacy hop:
- `_scripts/find_sources.py`
- `_neo4j/QUELLE_QUERY_GUIDE.md`
- any S5 visibility runner that reads only `BELEGT_IN -> Dossier -> ZITIERT_QUELLE`.

New queries should prefer direct URL properties on the fact relationship or Claim. A dossier edge is lineage context, not source truth:

```cypher
MATCH (n)-[r]->(m)
WHERE r.source_status = 'exact'
  AND r.source_url IS NOT NULL
RETURN n.id, type(r), m.id, r.source_url, r.source_note;
```

Legacy traversal remains as fallback until Phase G.

### Phase F - review the exceptions

Review all ledger rows with:
- `resolution_status <> 'resolved_url'`
- `end_labels` not containing `ExternalLink`
- start/end label pairs involving `ExternalLink -> ExternalLink`
- `evidence_origin = 'topology_synthesized'`

Acceptance:
- every exception has one of: `accepted_url_resolution`, `retired_topology_artifact`, `needs_human_context`;
- no exception is silently deleted.

### Phase G - delete `:ZITIERT_QUELLE`

Only after Phases A-F pass:

1. confirm every old edge has a ledger row;
2. confirm every URL-bearing old edge has a direct `source_url` replacement;
3. confirm user-facing queries no longer depend on `:ZITIERT_QUELLE`;
4. confirm the 3 non-URL artefacts have reviewed decisions;
5. run rollback dry-run.

Then delete only rows whose replacement is recorded in the ledger and whose `superseded_by_migration = <run_id>` is set.

Do not run a global delete by relationship type alone.

Post-delete acceptance:

```cypher
MATCH ()-[r:ZITIERT_QUELLE]->()
RETURN count(r) AS remaining_zitiert_quelle;
```

Expected: `0`.

---

## 7. Final gates

Required pass gates:

```cypher
MATCH ()-[r:ZITIERT_QUELLE]->(b)
WHERE b.url IS NOT NULL AND r.source_url IS NULL
RETURN count(r) AS unresolved_url_edges;
```

Expected before deletion: `0`.

```cypher
MATCH ()-[r:ZITIERT_QUELLE]->(b)
WHERE b.url IS NULL
RETURN labels(startNode(r)) AS start_labels,
       startNode(r).id AS start_id,
       labels(b) AS end_labels,
       b.id AS end_id,
       r.review_status AS review_status,
       count(*) AS count;
```

Expected before deletion: only reviewed non-URL artefacts. Expected after deletion: no rows.

```cypher
MATCH ()-[r]->()
WHERE r.supersedes_zitiert_rel_element_id IS NOT NULL
  AND r.source_url IS NULL
RETURN count(r) AS replacement_without_url;
```

Expected: `0`.

Do not use the existence of a `:CITED_FROM_DOSSIER` edge as a final proof gate. If that edge exists, it is only acceptable as internal row lineage; the final proof gate is the concrete URL on the fact relationship or Claim.

```cypher
MATCH ()-[r]->()
WHERE (r.evidence_origin IS NOT NULL OR r.evidence_source_id IS NOT NULL)
  AND type(r) <> 'ZITIERT_QUELLE'
  AND r.source_url IS NULL
  AND (r.source_urls IS NULL OR size(r.source_urls) = 0)
  AND coalesce(r.source_resolution_status, '') <> 'needs_source_url_review'
RETURN type(r) AS rel_type, count(r) AS missing_url
ORDER BY missing_url DESC;
```

Expected: no rows.

```cypher
MATCH (n)
WHERE any(label IN labels(n) WHERE label IN [
  'Projekt','Bauwerk','Akteur','Bauteilgruppe','Bauteiltyp','Material',
  'Kennwert','Huerde','Methode','Norm','ResearchDocument','Dossier'
])
AND n.source_url IS NULL
AND (n.source_urls IS NULL OR size(n.source_urls) = 0)
AND NOT exists {
  MATCH (n)-[r]-()
  WHERE r.source_url IS NOT NULL OR (r.source_urls IS NOT NULL AND size(r.source_urls) > 0)
}
RETURN labels(n) AS labels, count(n) AS nodes_without_url_trace
ORDER BY nodes_without_url_trace DESC;
```

Expected: only explicitly reviewed vocabulary/control nodes, otherwise `0`.

Always run:

```bash
python _scripts/_gap_survey.py
python _scripts/validate_no_text_content.py
```

---

## 8. Open decisions before implementation

1. Should `ExternalLink -> ExternalLink` relationships become metadata edges, or should their target URL be folded into the source `ExternalLink` node as `related_urls`?
2. Should `ResearchDocument` citations use a new `:CITED_FROM_RESEARCH` edge type, or an existing source-link type?
3. Who reviews the 3 `Dossier -> Dossier` non-URL artefacts?
4. For multi-URL source documents without row locators, is `source_urls` acceptable as a temporary concrete URL set, or must each row be manually reduced to one URL before deletion?

Recommended default:
- first migration stamps `source_url` / `source_urls` onto every resolvable information-bearing relationship and writes both ledgers;
- second migration updates query surfaces so no code relies on `:ZITIERT_QUELLE`;
- third migration deletes every ledger-covered `:ZITIERT_QUELLE`;
- final report proves `:ZITIERT_QUELLE = 0` and lists only reviewed unresolved source cases.
