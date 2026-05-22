# Minimal Source Referencing: 5 Node Samples Per Label

Generated from live Neo4j database `mit-bestand` on 2026-05-23.

Purpose: make the source model concrete. The rule is simple: nodes identify things; relationship facts or Claim nodes carry `source_status`, and only exact facts carry `source_url`.

Important correction: markdown/document lineage edges are not source truth. Dossiers, research files, Bauteilboerse files, and `akteursliste_master.md` contain URLs; those concrete URLs are the source truth. If a sampled row mentions a dossier/research/registry file or `CITED_FROM_DOSSIER`, treat it as row/context lineage only until the concrete URL is copied onto the fact relationship or Claim.

Columns: `state` describes current visible source material on the sampled node or adjacent relationships. `attach source how` is the proposed minimal rule.

## Labels

| Label | Count |
|---|---:|
| `DataIssue` | 29061 |
| `Quelle` | 5343 |
| `ExternalLink` | 5026 |
| `DossierEntityTarget` | 2591 |
| `Akteur` | 648 |
| `SectionRef` | 641 |
| `ResearchDocument` | 403 |
| `Bauteilgruppe` | 369 |
| `Kennwert` | 258 |
| `Bauwerk` | 186 |
| `PruefungNachweis` | 120 |
| `Norm` | 103 |
| `Projekt` | 101 |
| `Dossier` | 100 |
| `Stadt` | 76 |
| `Aufbereitungsverfahren` | 62 |
| `Leistungsanforderung` | 46 |
| `Programm` | 29 |
| `Huerde` | 28 |
| `Material` | 26 |
| `Akteurrolle` | 24 |
| `Bauteiltyp` | 23 |
| `Materialdepot` | 23 |
| `ReuseRule` | 20 |
| `Land` | 19 |
| `Software` | 19 |
| `Ressourcenquelle` | 16 |
| `Bauproduktstatus` | 15 |
| `RechtlicheBedingung` | 15 |
| `Verbindungstechnik` | 15 |
| `Wiederverwendungskette` | 14 |
| `DeprecatedType` | 13 |
| `Methode` | 13 |
| `Wirtschaft` | 12 |
| `Marktmodell` | 11 |
| `Materialgruppe` | 11 |
| `WiederverwendungsArt` | 11 |
| `Akteurtyp` | 10 |
| `BauaufgabeIntervention` | 10 |
| `Beschaffungsweg` | 10 |
| `Defekt` | 10 |
| `HuerdeKategorie` | 10 |
| `Logistik` | 10 |
| `Prozessphase` | 10 |
| `Bausystem` | 9 |
| `MatchingQualitaet` | 9 |
| `Nutzung` | 9 |
| `Schadstoff` | 9 |
| `Status` | 9 |
| `Bauobjektklasse` | 8 |
| `Tool` | 8 |
| `Zertifizierungssystem` | 8 |
| `Akzeptanz` | 7 |
| `Bauobjektrolle` | 6 |
| `Bauteilebene` | 6 |
| `Bauweise` | 6 |
| `BauwerkEra` | 6 |
| `Funktionswechsel` | 6 |
| `Layer` | 6 |
| `ZustandsKlasse` | 6 |
| `LCAModule` | 5 |
| `Rueckbauverfahren` | 5 |
| `Tragwerksprinzip` | 4 |
| `OntologyAnchor` | 2 |

## Samples

### `DataIssue` (29061)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=di_actor_stub__CITYFOERSTER__p_recyclinghaus_hannover; status=open; severity=medium; ref_id=r_CITYFOERSTER__ASSOZIIERT_MIT_PROJEKT__p_recyclinghaus_hannover | none visible | 1 rels; exact 0; cand 0; review 0; CONCERNS | review/audit node, no fact source required |
| 2 | id=di_actor_stub__Lendager__p_resource_rows_copenhagen; status=open; severity=medium; ref_id=r_Lendager__ASSOZIIERT_MIT_PROJEKT__p_resource_rows_copenhagen | none visible | 1 rels; exact 0; cand 0; review 0; CONCERNS | review/audit node, no fact source required |
| 3 | id=di_actor_stub__Lendager__p_upcycle_studios_copenhagen; status=open; severity=medium; ref_id=r_Lendager__ASSOZIIERT_MIT_PROJEKT__p_upcycle_studios_copenhagen | none visible | 1 rels; exact 0; cand 0; review 0; CONCERNS | review/audit node, no fact source required |
| 4 | id=di_actor_stub__Natural_Building_Lab__p_reallabor_be_ware; status=open; severity=medium; ref_id=r_natural_building_lab__ASSOZIIERT_MIT_PROJEKT__p_reallabor_be_ware | none visible | 1 rels; exact 0; cand 0; review 0; CONCERNS | review/audit node, no fact source required |
| 5 | id=di_actor_stub__Natural_Building_Lab__prog_reallabor_be_ware; status=open; severity=medium; ref_id=r_Natural_Building_Lab__ASSOZIIERT_MIT_PROJEKT__prog_reallabor_be_ware | none visible | 1 rels; exact 0; cand 0; review 0; CONCERNS | review/audit node, no fact source required |

### `Quelle` (5343)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=q_url_4355c6af7f5e034ee6866841bf19ea11; url=https://maryon.ch/v2/wp-content/uploads/2023.Juni_ARCH_EN.pdf; evidence_source_id=q_research_reuse_knowledge_graph_coverage_audit_md; evidence_basis=markdown_link_extraction | none visible | 0 rels; exact 0; cand 0; review 0;  | metadata node; do not use as proof alone |
| 2 | id=q_url_1443e44464c9060f4eefdc4804a611e0; url=https://www.glasstec-online.com/en/Media_News/Magazine/Stories/Reusing_glass_ins...; evidence_source_id=q_research_reuse_knowledge_graph_coverage_audit_md; evidence_basis=markdown_link_extraction | none visible | 0 rels; exact 0; cand 0; review 0;  | metadata node; do not use as proof alone |
| 3 | id=q_url_f0ff7753b0264cbbfeb4b4c29570bb56; url=https://il.boell.org/en/2023/03/29/promoting-circular-economy-construction-secto...; evidence_source_id=q_research_reuse_knowledge_graph_coverage_audit_md; evidence_basis=markdown_link_extraction | none visible | 0 rels; exact 0; cand 0; review 0;  | metadata node; do not use as proof alone |
| 4 | id=q_url_d7a72171312d05683570e279b9b59fe0; url=https://www.ark.fi/en/2024/02/a-pioneer-of-the-circular-economy; evidence_source_id=q_research_reuse_knowledge_graph_coverage_audit_md; evidence_basis=markdown_link_extraction | none visible | 0 rels; exact 0; cand 0; review 0;  | metadata node; do not use as proof alone |
| 5 | id=q_url_27f7f7d5d9d114b4aed4ad7ee6b8c10c; url=https://lxsy.de/en/projects/boelllab; evidence_source_id=q_research_reuse_knowledge_graph_coverage_audit_md; evidence_basis=markdown_link_extraction | none visible | 0 rels; exact 0; cand 0; review 0;  | metadata node; do not use as proof alone |

### `ExternalLink` (5026)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=q_url_4355c6af7f5e034ee6866841bf19ea11; url=https://maryon.ch/v2/wp-content/uploads/2023.Juni_ARCH_EN.pdf; evidence_source_id=q_research_reuse_knowledge_graph_coverage_audit_md; evidence_basis=markdown_link_extraction | none visible | 0 rels; exact 0; cand 0; review 0;  | metadata node; do not use as proof alone |
| 2 | id=q_url_1443e44464c9060f4eefdc4804a611e0; url=https://www.glasstec-online.com/en/Media_News/Magazine/Stories/Reusing_glass_ins...; evidence_source_id=q_research_reuse_knowledge_graph_coverage_audit_md; evidence_basis=markdown_link_extraction | none visible | 0 rels; exact 0; cand 0; review 0;  | metadata node; do not use as proof alone |
| 3 | id=q_url_f0ff7753b0264cbbfeb4b4c29570bb56; url=https://il.boell.org/en/2023/03/29/promoting-circular-economy-construction-secto...; evidence_source_id=q_research_reuse_knowledge_graph_coverage_audit_md; evidence_basis=markdown_link_extraction | none visible | 0 rels; exact 0; cand 0; review 0;  | metadata node; do not use as proof alone |
| 4 | id=q_url_d7a72171312d05683570e279b9b59fe0; url=https://www.ark.fi/en/2024/02/a-pioneer-of-the-circular-economy; evidence_source_id=q_research_reuse_knowledge_graph_coverage_audit_md; evidence_basis=markdown_link_extraction | none visible | 0 rels; exact 0; cand 0; review 0;  | metadata node; do not use as proof alone |
| 5 | id=q_url_27f7f7d5d9d114b4aed4ad7ee6b8c10c; url=https://lxsy.de/en/projects/boelllab; evidence_source_id=q_research_reuse_knowledge_graph_coverage_audit_md; evidence_basis=markdown_link_extraction | none visible | 0 rels; exact 0; cand 0; review 0;  | metadata node; do not use as proof alone |

### `DossierEntityTarget` (2591)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=det_f7c1f4bc02fd80828cf70184; name=$645,000 excl. land / $175/sf / $150/sf; unfolding_kind=dossier_row; created_at_utc=2026-05-22T15:56:47.268904+00:00 | exact nearby | 2 rels; exact 2; cand 0; review 0; CITED_FROM_DOSSIER | row lineage only; source truth is the concrete dossier URL on the fact/Claim |
| 2 | id=det_e8c24d486a369ef21a9e2379; name=1,9 Mio. CHF Objektkredit; unfolding_kind=dossier_row; created_at_utc=2026-05-22T15:56:47.391721+00:00 | exact nearby | 1 rels; exact 1; cand 0; review 0; CITED_FROM_DOSSIER | row lineage only; source truth is the concrete dossier URL on the fact/Claim |
| 3 | id=det_5ec5e1015244a72010f87f26; name=1.270 m²; unfolding_kind=dossier_row; created_at_utc=2026-05-22T15:56:47.481217+00:00 | exact nearby | 1 rels; exact 1; cand 0; review 0; CITED_FROM_DOSSIER | row lineage only; source truth is the concrete dossier URL on the fact/Claim |
| 4 | id=det_6db9922b717520a6db2ce157; name=1.300 m²; unfolding_kind=dossier_row; created_at_utc=2026-05-22T15:56:47.276000+00:00 | exact nearby | 2 rels; exact 2; cand 0; review 0; CITED_FROM_DOSSIER | row lineage only; source truth is the concrete dossier URL on the fact/Claim |
| 5 | id=det_e91ca6615448b29a31fd913d; name=1.436 m²; unfolding_kind=dossier_row; created_at_utc=2026-05-22T15:56:47.481217+00:00 | exact nearby | 1 rels; exact 1; cand 0; review 0; CITED_FROM_DOSSIER | row lineage only; source truth is the concrete dossier URL on the fact/Claim |

### `Akteur` (648)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=2emain_be; name=2emain.be; migration_origin= \| mig_s5_visibility \| mig_qext_b_source_urls \| mig_qext_c_primary_source_url; strict_source_url_cleanup_at=2026-05-23T11:01:59.122927+00:00 | candidate nearby | 9 rels; exact 0; cand 1; review 4; BETEILIGT_AN, HAT_AKTEURROLLE, HAT_AKTEURTYP, BELEGT_IN, CONCERNS | identity on node; facts on relationships/Claim |
| 2 | id=2hs; name=2hs; actor_registry_loader_seen=agent10; migration_origin= \| mig_s5_visibility \| mig_qext_b_source_urls | candidate nearby | 28 rels; exact 0; cand 11; review 13; GEHÖRT_ZU, HAT_AKTEURTYP, LIEGT_IN_LAND, ANCHORED_BY, CONCERNS | identity on node; facts on relationships/Claim |
| 3 | id=3xn; name=3XN; actor_registry_loader_seen=agent10; migration_origin= \| mig_s5_visibility \| mig_qext_b_source_urls | candidate nearby | 26 rels; exact 0; cand 11; review 12; GEHÖRT_ZU, HAT_AKTEURROLLE, HAT_AKTEURTYP, LIEGT_IN_LAND, ANCHORED_BY | identity on node; facts on relationships/Claim |
| 4 | id=51n4e; name=51N4E; migration_origin= \| mig_s5_visibility \| mig_qext_b_source_urls \| mig_qext_c_primary_source_url; strict_source_url_cleanup_at=2026-05-23T11:01:59.122927+00:00 | candidate nearby | 10 rels; exact 0; cand 1; review 4; BETEILIGT_AN, HAT_AKTEURROLLE, HAT_AKTEURTYP, BELEGT_IN, CONCERNS | identity on node; facts on relationships/Claim |
| 5 | id=kruunu; name=A-Kruunu; migration_origin= \| mig_s5_visibility \| mig_qext_b_source_urls \| mig_qext_c_primary_source_url; strict_source_url_cleanup_at=2026-05-23T11:01:59.122927+00:00 | candidate nearby | 10 rels; exact 0; cand 1; review 4; BETEILIGT_AN, HAT_AKTEURROLLE, HAT_AKTEURTYP, BELEGT_IN, CONCERNS | identity on node; facts on relationships/Claim |

### `SectionRef` (641)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=q_kamikatsu_zero_waste_center_hotel_why_s1; name=**Q1 – Offizielle WHY-Seite, „Why Zero Waste in Kamikatsu Town?“:**; url=https://why-kamikatsu.jp/en/pages/why; url_status=reachable_2xx | exact nearby | 0 rels; exact 0; cand 0; review 0;  | metadata node; do not use as proof alone |
| 2 | id=q_the_green_house_utrecht_s1; name=**Q1 – cepezed, „The Green House“:**; url=https://www.cepezed.nl/en/project/the-green-house/22172; url_status=reachable_2xx | exact nearby | 0 rels; exact 0; cand 0; review 0;  | metadata node; do not use as proof alone |
| 3 | id=q_hastings_pier_visitor_centre_s1; name=**Q1 – dRMM Architects, „Hastings Pier“:**; url=https://drmmstudio.com/project/hastings-pier; url_status=reachable_2xx | exact nearby | 0 rels; exact 0; cand 0; review 0;  | metadata node; do not use as proof alone |
| 4 | id=q_kamikatsu_zero_waste_center_hotel_why_s2; name=**Q2 – Hiroshi Nakamura & NAP, „Kamikatsu Zero Waste Center“:**; url=https://www.nakam.info/en/works/kamikatsu0; url_status=reachable_2xx | exact nearby | 0 rels; exact 0; cand 0; review 0;  | metadata node; do not use as proof alone |
| 5 | id=q_the_green_house_utrecht_s2; name=**Q2 – cepezed.com, „The Green House“:**; url=https://www.cepezed.com/projects/the-green-house; url_status=reachable_2xx | exact nearby | 0 rels; exact 0; cand 0; review 0;  | metadata node; do not use as proof alone |

### `ResearchDocument` (403)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=q_research_testing_verification_bauteilreuse_kg_url_f35ba5ca; name=%3Ac5724abe-0fe0-4766-81d4-5218a4a5a828/13-ictb2021-koch.pdf; title=%3Ac5724abe-0fe0-4766-81d4-5218a4a5a828/13-ictb2021-koch.pdf; url=https://www.bfh.ch/dam/jcr%3Ac5724abe-0fe0-4766-81d4-5218a4a5a828/13-ictb2021-ko... | exact nearby | 0 rels; exact 0; cand 0; review 0;  | metadata node; do not use as proof alone |
| 2 | id=q_research_testing_verification_bauteilreuse_kg_url_07c6159c; name=-bauen/fachwissen/regelwerke/normen-fuer-den-lehmbau-3393643; title=-bauen/fachwissen/regelwerke/normen-fuer-den-lehmbau-3393643; url=https://www.baunetzwissen.de/gesund-bauen/fachwissen/regelwerke/normen-fuer-den-... | exact nearby | 1 rels; exact 1; cand 0; review 0; CONCERNS | metadata node; do not use as proof alone |
| 3 | id=q_research_circular_construction_reuse_graph_gaps_url_7a3fa4fd; name=-when-reusing-products-from-existing-structures_June2023.pdf; title=-when-reusing-products-from-existing-structures_June2023.pdf; url=https://platformcb23.nl/wp-content/uploads/PlatformCB23_guide_Quality-assessment... | exact nearby | 0 rels; exact 0; cand 0; review 0;  | metadata node; do not use as proof alone |
| 4 | id=q_research_testing_verification_bauteilreuse_kg_url_7a3fa4fd; name=-when-reusing-products-from-existing-structures_June2023.pdf; title=-when-reusing-products-from-existing-structures_June2023.pdf; url=https://platformcb23.nl/wp-content/uploads/PlatformCB23_guide_Quality-assessment... | exact nearby | 0 rels; exact 0; cand 0; review 0;  | metadata node; do not use as proof alone |
| 5 | id=q_research_aufbereitungsverfahren_reused_building_elements_url_d36c5356; name=.archdaily.com/968958/k118-kopfbau-halle-118-hauburo-in-situ; title=.archdaily.com/968958/k118-kopfbau-halle-118-hauburo-in-situ; url=https://www.archdaily.com/968958/k118-kopfbau-halle-118-hauburo-in-situ | exact nearby | 0 rels; exact 0; cand 0; review 0;  | metadata node; do not use as proof alone |

### `Bauteilgruppe` (369)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=bg_reuse_holz_fassade_botanique; name=/ rückgewonnene Holzfass…; name_full=Wiederverwendete / rückgewonnene Holzfassade; migration_origin=mig_r5_bg_disambiguation \| mig_qext_b_source_urls \| mig_qext_c_primary_source_ur... | candidate nearby | 70 rels; exact 0; cand 2; review 32; HAT_BAUTEILTYP, HAT_BAUTEILEBENE, HAT_STATUS, HAT_WIEDERVERWENDUNGSART, HAT_FUNKTIONSWECHSEL | relationship fact or Claim if attribute-like |
| 2 | id=bg_reuse_stahl_mehrere_lycee_profiles_canopy; name=11,8 t Stahlprofile als…; name_full=11,8 t Stahlprofile als Überdachung; migration_origin=mig_r5_bg_disambiguation \| mig_qext_b_source_urls \| mig_qext_c_primary_source_ur... | candidate nearby | 55 rels; exact 0; cand 2; review 26; HAT_TRAGWERKSPRINZIP, HAT_BAUWEISE, HAT_WIEDERVERWENDUNGSART, HAT_FUNKTIONSWECHSEL, NUTZT_MATERIAL | relationship fact or Claim if attribute-like |
| 3 | id=bg_reuse_stahl_mehrere_lycee_metal_ceiling_panels; name=12 Metall-Deckenpaneele; name_full=12 Metall-Deckenpaneele / 4,3 m²; migration_origin=mig_r5_bg_disambiguation \| mig_qext_b_source_urls \| mig_qext_c_primary_source_ur... | candidate nearby | 49 rels; exact 0; cand 2; review 23; HAT_STATUS, HAT_WIEDERVERWENDUNGSART, HAT_FUNKTIONSWECHSEL, NUTZT_MATERIAL, HAT_MATERIALGRUPPE | relationship fact or Claim if attribute-like |
| 4 | id=bg_reuse_stahlbeton_mehrere_plattenpalast_wbs70_wand_deckenelemente; name=13 WBS70-Wand- und…; primary_material_id=mat_stahlbeton; reuse_status=reuse | candidate nearby | 80 rels; exact 0; cand 2; review 39; HAT_BAUTEILEBENE, HAT_STATUS, HAT_WIEDERVERWENDUNGSART, NUTZT_MATERIAL, HAT_MATERIALGRUPPE | relationship fact or Claim if attribute-like |
| 5 | id=bg_reuse_keramik_mehrere_maison_vignette_terracotta_floor_tiles; name=13,5 m² wiederverwendete…; name_full=13,5 m² wiederverwendete Terrakotta-Bodenfliesen; migration_origin=mig_r5_bg_disambiguation \| mig_qext_b_source_urls \| mig_qext_c_primary_source_ur... | candidate nearby | 46 rels; exact 0; cand 2; review 22; HAT_BAUTEILEBENE, HAT_STATUS, HAT_WIEDERVERWENDUNGSART, NUTZT_MATERIAL, HAT_MATERIALGRUPPE | relationship fact or Claim if attribute-like |

### `Kennwert` (258)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=kw_p_55_great_suffolk_street_london_co2_saving_0; loader=unknown; kennwert=co2_einsparung_t; wert=50.0 | needs review | 4 rels; exact 0; cand 0; review 1; HAT_KENNWERT, CONCERNS, HAS_DATA_ISSUE | identity on node; facts on relationships/Claim |
| 2 | id=kw_p_55_great_suffolk_street_london_cost_0; method=Vergleich zu A1-A3 2.5 kgCO₂e/kg steel; loader=agent9_phase4b1; kennwert=CO₂-Einsparung Stahlreuse | candidate nearby | 4 rels; exact 0; cand 1; review 1; HAT_KENNWERT, CONCERNS, HAS_DATA_ISSUE | identity on node; facts on relationships/Claim |
| 3 | id=kw_p_55_great_suffolk_street_london_cost_1; method=—; loader=agent9_phase4b1; kennwert=Kosten | candidate nearby | 4 rels; exact 0; cand 1; review 1; HAT_KENNWERT, CONCERNS, HAS_DATA_ISSUE | identity on node; facts on relationships/Claim |
| 4 | id=kw_p_55_great_suffolk_street_london_reuse_share_0; loader=unknown; kennwert=reuse_anteil_prozent; wert=97.0 | needs review | 4 rels; exact 0; cand 0; review 1; HAT_KENNWERT, CONCERNS, HAS_DATA_ISSUE | identity on node; facts on relationships/Claim |
| 5 | id=kw_p_55_great_suffolk_street_london_reuse_share_1; method=20.35/20.98 t; loader=agent9_phase4b1; kennwert=Anteil reused steel am Kernstahl | candidate nearby | 4 rels; exact 0; cand 1; review 1; HAT_KENNWERT, CONCERNS, HAS_DATA_ISSUE | identity on node; facts on relationships/Claim |

### `Bauwerk` (186)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=bw_1_broadgate_1_2_broadgate_donor_stahl; name=1 Broadgate; name_full=1 Broadgate / 1–2 Broadgate Donor-Stahl; migration_origin= \| mig_s5_visibility \| mig_qext_b_source_urls \| mig_qext_c_primary_source_url | candidate nearby | 11 rels; exact 0; cand 1; review 5; HAT_BAUOBJEKTKLASSE, HAT_BAUOBJEKTROLLE, HAT_STATUS, BELEGT_IN, FROM_DONOR | identity on node; facts on relationships/Claim |
| 2 | id=bw_1_broadgate_london; name=1 Broadgate, London; migration_origin= \| mig_s5_visibility \| mig_qext_b_source_urls \| mig_qext_c_primary_source_url; strict_source_url_cleanup_at=2026-05-23T11:01:59.122927+00:00 | candidate nearby | 15 rels; exact 0; cand 1; review 7; HAT_BAUOBJEKTKLASSE, HAT_BAUOBJEKTROLLE, HAT_STATUS, LIEGT_IN_STADT, BELEGT_IN | identity on node; facts on relationships/Claim |
| 3 | id=bw_tampere_1980s_office_donor; name=1980er Bürogebäude im…; nutzung_text=Donorgebäude für Hohlkörperdecken; name_full=1980er Bürogebäude im Zentrum von Tampere | candidate nearby | 35 rels; exact 0; cand 2; review 17; NUTZT_BAUWERK, HAT_BAUOBJEKTKLASSE, HAT_BAUOBJEKTROLLE, HAT_TRAGWERKSPRINZIP, HAT_BAUWEISE | identity on node; facts on relationships/Claim |
| 4 | id=bw_318_oxford_street_house_of_fraser; name=318 Oxford Street; nutzung_text=ehemaliges Department Store, Donor und Self-Reuse-Projekt; name_full=318 Oxford Street / former House of Fraser / The Elephant | candidate nearby | 39 rels; exact 0; cand 1; review 19; NUTZT_BAUWERK, HAT_BAUOBJEKTKLASSE, HAT_TRAGWERKSPRINZIP, HAT_BAUWEISE, HAT_BAUSYSTEM | identity on node; facts on relationships/Claim |
| 5 | id=bw_55_great_suffolk_street_warehouse; name=55 Great Suffolk Street…; name_full=55 Great Suffolk Street warehouse; migration_origin= \| mig_s5_visibility \| mig_qext_b_source_urls \| mig_qext_c_primary_source_url | candidate nearby | 22 rels; exact 0; cand 1; review 10; NUTZT_BAUWERK, HAT_BAUOBJEKTKLASSE, HAT_BAUOBJEKTROLLE, HAT_STATUS, HAT_RECHTLICHE_BEDINGUNG | identity on node; facts on relationships/Claim |

### `PruefungNachweis` (120)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=pr_abbrandbemessung; name=Abbrandbemessung; last_seen_by=agent10_phase4b_2; archive_mentioned_in_corpus=True | candidate nearby | 7 rels; exact 0; cand 1; review 3; BELEGT_IN, IST_UNTERVERFAHREN_VON, ANCHORED_BY, CONCERNS | relationship fact or Claim if attribute-like |
| 2 | id=pr_bohrkernpruefung_beton; name=Beton-Bohrkernprüfung; last_seen_by=agent10_phase4b_2; scope_note=Core drilling and compression testing of concrete elements per EN 12504-1; in-si... | exact nearby | 17 rels; exact 3; cand 1; review 7; HAT_PRUEFUNG, BELEGT_IN, TYPISCH_BEI_MATERIAL, IST_UNTERVERFAHREN_VON, ANCHORED_BY | relationship fact or Claim if attribute-like |
| 3 | id=pr_brandschutznachweis; name=Brandschutznachweis; last_seen_by=agent10_phase4b_2; migration_origin=mig_qext_b_source_urls \| mig_qext_c_primary_source_url | candidate nearby | 13 rels; exact 0; cand 1; review 6; HAT_PRUEFUNG, BELEGT_IN, IST_UNTERVERFAHREN_VON, ANCHORED_BY, CONCERNS | relationship fact or Claim if attribute-like |
| 4 | id=pr_dokumentenpruefung_bestand; name=Dokumentenprüfung / Herkunfts- und Bestandsnachweis; last_seen_by=agent10_phase4b_2; scope_note=Document review: plans, calculations, maintenance/use records, prior investigati... | exact nearby | 30 rels; exact 2; cand 2; review 14; BELEGT_IN, ANCHORED_BY, CONCERNS, HAT_PRUEFUNG | relationship fact or Claim if attribute-like |
| 5 | id=pr_eignungspruefung_baulehm; name=Eignungspruefung_Baulehm; last_seen_by=agent10_phase4b_2; source_count=1 | exact nearby | 6 rels; exact 2; cand 1; review 2; HAT_PRUEFUNG, BELEGT_IN, ANCHORED_BY, CONCERNS | relationship fact or Claim if attribute-like |

### `Norm` (103)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=norm_bs_4978; name=BS 4978; evidence_basis=reuse_rule_key_norm; migration_origin=mig_qext_b_source_urls | candidate nearby | 4 rels; exact 0; cand 1; review 1; REFERENZIERT_NORM, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 2 | id=norm_bbl_nen; name=Bbl/NEN; evidence_basis=reuse_rule_key_norm; migration_origin=mig_qext_b_source_urls | candidate nearby | 4 rels; exact 0; cand 1; review 1; REFERENZIERT_NORM, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 3 | id=norm_bbl_nen_links; name=Bbl/NEN links; evidence_basis=reuse_rule_key_norm; migration_origin=mig_qext_b_source_urls | candidate nearby | 4 rels; exact 0; cand 1; review 1; REFERENZIERT_NORM, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=norm_cb_23_passports; name=CB'23 passports; evidence_basis=reuse_rule_key_norm; migration_origin=mig_qext_b_source_urls | candidate nearby | 4 rels; exact 0; cand 1; review 1; REFERENZIERT_NORM, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 5 | id=norm_cen_ts_1090_201; name=CEN/TS 1090-201; evidence_basis=reuse_rule_key_norm; migration_origin=mig_qext_b_source_urls | candidate nearby | 10 rels; exact 0; cand 4; review 4; REFERENZIERT_NORM, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `Projekt` (101)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=p_55_great_suffolk_street_london; name=55 Great Suffolk Street; name_full=55 Great Suffolk Street, London; year_completed=2024 | candidate nearby | 87 rels; exact 0; cand 5; review 41; NUTZT_BAUWERK, HAT_STATUS, HAT_WIEDERVERWENDUNGSART, HAT_INTERVENTION, HAT_METHODE | identity on node; facts on relationships/Claim |
| 2 | id=p_awm_muenster_circular_office; name=AWM Münster – zirkulärer…; name_full=AWM Münster – zirkulärer Büroausbau 3. OG; year_completed=2023 | candidate nearby | 99 rels; exact 0; cand 15; review 46; NUTZT_BAUWERK, HAT_STATUS, HAT_NUTZUNG, HAT_WIEDERVERWENDUNGSART, HAT_INTERVENTION | identity on node; facts on relationships/Claim |
| 3 | id=p_bedzed_london_hackbridge; name=BedZED; name_full=BedZED / Beddington Zero Energy Development; year_completed=2002 | candidate nearby | 103 rels; exact 0; cand 15; review 49; NUTZT_BAUWERK, HAT_STATUS, HAT_WIEDERVERWENDUNGSART, HAT_INTERVENTION, HAT_METHODE | identity on node; facts on relationships/Claim |
| 4 | id=p_berlin_schildow_pilot_house; name=Berlin-Schildow Pilot; source_count=6; name_full=Berlin-Schildow Pilot House / Berlin-Schildow 2nd pilot house | exact nearby | 149 rels; exact 79; cand 5; review 34; HAT_STATUS, HAT_WIEDERVERWENDUNGSART, HAT_INTERVENTION, HAT_METHODE, HAT_BESCHAFFUNGSWEG | identity on node; facts on relationships/Claim |
| 5 | id=p_bestandverplanzung_pavilion_muenchen; name=Bestandverplanzung…; name_full=Bestandverplanzung Pavilion, München; year_completed=2008 | candidate nearby | 45 rels; exact 0; cand 4; review 21; HAT_WIEDERVERWENDUNGSART, HAT_INTERVENTION, HAT_METHODE, HAT_RESSOURCENQUELLE, HAT_HUERDE | identity on node; facts on relationships/Claim |

### `Dossier` (100)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=q_55_great_suffolk_street_london_md; name=55_Great_Suffolk_Street_…; text_content_retry_result=resolved; source_count=6 | exact nearby | 130 rels; exact 96; cand 16; review 17; CONCERNS, BELEGT_IN, CITED_FROM_DOSSIER | metadata node; do not use as proof alone |
| 2 | id=q_awm_muenster_circular_office_md; name=AWM_Muenster_Circular_Of…; text_content_retry_result=resolved; source_count=6 | exact nearby | 141 rels; exact 107; cand 17; review 17; CONCERNS, BELEGT_IN, CITED_FROM_DOSSIER | metadata node; do not use as proof alone |
| 3 | id=q_architecture_of_reuse_brussels_md; name=Architecture of Reuse Brussels; migration_origin= \| r7_d_text_content \| mig_s4_a_secondary_labels \| mig_s4_b_text_strip; text_content_chars_pre_strip=14698 | needs review | 3 rels; exact 0; cand 0; review 1; BELEGT_IN, CONCERNS | metadata node; do not use as proof alone |
| 4 | id=q_association_house_groeditz_md; name=Association_house_Groedi…; text_content_retry_result=resolved; source_count=4 | exact nearby | 67 rels; exact 49; cand 9; review 9; CONCERNS, BELEGT_IN, CITED_FROM_DOSSIER | metadata node; do not use as proof alone |
| 5 | id=q_association_house_plauen_md; name=Association_house_Plauen…; text_content_retry_result=resolved; source_count=5 | exact nearby | 65 rels; exact 53; cand 6; review 6; BELEGT_IN, CONCERNS, CITED_FROM_DOSSIER | metadata node; do not use as proof alone |

### `Stadt` (76)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=stadt_aarhus; name=Aarhus; source_scope=controlled_vocab_seed | candidate nearby | 10 rels; exact 0; cand 1; review 5; LIEGT_IN_STADT, LIEGT_IN_LAND, BELEGT_IN, CONCERNS | relationship fact or Claim if attribute-like |
| 2 | id=stadt_amsterdam; name=Amsterdam; source_scope=case_markdown | needs review | 8 rels; exact 0; cand 0; review 4; LIEGT_IN_STADT, LIEGT_IN_LAND, BELEGT_IN, CONCERNS | relationship fact or Claim if attribute-like |
| 3 | id=stadt_arnhem; name=Arnhem; source_scope=controlled_vocab_seed | candidate nearby | 8 rels; exact 0; cand 1; review 4; LIEGT_IN_STADT, LIEGT_IN_LAND, BELEGT_IN, CONCERNS | relationship fact or Claim if attribute-like |
| 4 | id=stadt_asse; name=Asse; source_scope=controlled_vocab_seed | candidate nearby | 10 rels; exact 0; cand 1; review 5; LIEGT_IN_STADT, LIEGT_IN_LAND, BELEGT_IN, CONCERNS | relationship fact or Claim if attribute-like |
| 5 | id=stadt_auderghem_brussels; name=Auderghem / Brüssel; source_scope=controlled_vocab_seed | candidate nearby | 12 rels; exact 0; cand 1; review 6; LIEGT_IN_STADT, LIEGT_IN_LAND, BELEGT_IN, CONCERNS | relationship fact or Claim if attribute-like |

### `Aufbereitungsverfahren` (62)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=av_aluminium_reinigung_entdichtung; name=Aluminium-Reinigung + Entdichtung; last_seen_by=agent10_phase4b_2; scope_note=Cleaning of aluminium profiles + removal of old gaskets, glue, hardware. | candidate nearby | 11 rels; exact 0; cand 2; review 5; HAT_AUFBEREITUNG, BELEGT_IN, TYPISCH_BEI_MATERIAL, IST_UNTERVERFAHREN_VON, ANCHORED_BY | relationship fact or Claim if attribute-like |
| 2 | id=av_aluminium_zuschnitt_bohrung; name=Aluminium-Zuschnitt + Bohrung + Profilanpassung; last_seen_by=agent10_phase4b_2; scope_note=Cutting + drilling + dimensional adaptation of aluminium profiles for reuse. | candidate nearby | 9 rels; exact 0; cand 1; review 4; BELEGT_IN, TYPISCH_BEI_MATERIAL, IST_UNTERVERFAHREN_VON, ANCHORED_BY, CONCERNS | relationship fact or Claim if attribute-like |
| 3 | id=av_aluminiumfenster_beschlag_dichtung; name=Aluminiumfenster — Beschläge + Dichtungen tauschen; last_seen_by=agent10_phase4b_2; scope_note=Repair / replacement of gaskets, hardware, drainage on aluminium-frame windows. ... | candidate nearby | 11 rels; exact 0; cand 3; review 5; HAT_AUFBEREITUNG, BELEGT_IN, TYPISCH_BEI_MATERIAL, ANCHORED_BY, CONCERNS | relationship fact or Claim if attribute-like |
| 4 | id=av_betonfertigteil_tagging_sortierung; name=Bauteil-Tagging + Sortierung; last_seen_by=agent10_phase4b_2; scope_note=Labeling, provenance documentation, sortin by type/length/condition. Cross-cutti... | candidate nearby | 11 rels; exact 0; cand 1; review 5; HAT_AUFBEREITUNG, BELEGT_IN, IST_UNTERVERFAHREN_VON, ANCHORED_BY, CONCERNS | relationship fact or Claim if attribute-like |
| 5 | id=av_betonfertigteil_factory_refurbishment; name=Beton-Fertigteil Factory Refurbishment (Prozesspaket); last_seen_by=agent10_phase4b_2; scope_note=Bundled workshop process: cleaning + testing + cutting + fittings + tagging + st... | candidate nearby | 9 rels; exact 0; cand 1; review 4; BELEGT_IN, TYPISCH_BEI_MATERIAL, ANCHORED_BY, CONCERNS | relationship fact or Claim if attribute-like |

### `Leistungsanforderung` (46)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=la_brandschutz; name=Brandschutz; last_seen_by=agent10_phase4b_2; migration_origin=mig_qext_b_source_urls \| mig_qext_c_primary_source_url | candidate nearby | 194 rels; exact 0; cand 1; review 96; BELEGT_IN, ANCHORED_BY, EXACT_MATCH_CANDIDATE, HAT_LEISTUNGSANFORDERUNG, CONCERNS | relationship fact or Claim if attribute-like |
| 2 | id=la_dauerhaftigkeit; name=Dauerhaftigkeit; last_seen_by=agent10_phase4b_2; migration_origin=mig_qext_b_source_urls \| mig_qext_c_primary_source_url | candidate nearby | 316 rels; exact 0; cand 1; review 157; BELEGT_IN, ANCHORED_BY, EXACT_MATCH_CANDIDATE, HAT_LEISTUNGSANFORDERUNG, CONCERNS | relationship fact or Claim if attribute-like |
| 3 | id=la_f90; name=F90; source_resolution_status=needs_source_url_review; archive_mentioned_in_corpus=True | needs review | 4 rels; exact 0; cand 0; review 1; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=la_feuchteschutz; name=Feuchteschutz; last_seen_by=agent10_phase4b_2; migration_origin=mig_qext_b_source_urls \| mig_qext_c_primary_source_url | candidate nearby | 129 rels; exact 0; cand 1; review 64; BELEGT_IN, ANCHORED_BY, HAT_LEISTUNGSANFORDERUNG, CONCERNS | relationship fact or Claim if attribute-like |
| 5 | id=la_feuerwiderstand; name=Feuerwiderstand; source_resolution_status=needs_source_url_review; migration_origin=mig_qext_b_source_urls | needs review | 10 rels; exact 0; cand 0; review 4; HAT_LEISTUNGSANFORDERUNG, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `Programm` (29)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=prog_abn_amro_mission_2030; name=ABN AMRO Mission 2030; type=Unternehmensprogramm; short_description=ABN AMRO's circular-economy programme; Circl pavilion was its physical demonstra... | needs review | 5 rels; exact 0; cand 0; review 2; BELEGT_IN, TEIL_VON_PROGRAMM, CONCERNS | relationship fact or Claim if attribute-like |
| 2 | id=p_architecture_of_reuse_brussels; name=Architecture of Reuse…; name_full=Architecture of Reuse Brussels; migration_origin=5_3_relabel_to_programm \| mig_qext_b_source_urls \| mig_qext_c_primary_source_url | candidate nearby | 25 rels; exact 0; cand 4; review 12; LIEGT_IN_STADT, LIEGT_IN_LAND, BELEGT_IN, ANCHORED_BY, STUB_PROJECT_LINK | relationship fact or Claim if attribute-like |
| 3 | id=prog_be_circular; name=Be.Circular; type=Foerderprogramm; short_description=Be.Circular is a key measure of the Brussels Regional Programme for a Circular E... | needs review | 7 rels; exact 0; cand 0; review 3; BELEGT_IN, TEIL_VON_PROGRAMM, CONCERNS | relationship fact or Claim if attribute-like |
| 4 | id=p_eth_circular_construction_programme; name=ETH Circular Construction Programme; evidence_basis=dossier_anchored; migration_origin=mig_r7_b_resolve_orphans \| mig_qext_b_source_urls \| mig_qext_c_primary_source_ur... | candidate nearby | 4 rels; exact 0; cand 1; review 1; BELEGT_IN, CONCERNS | relationship fact or Claim if attribute-like |
| 5 | id=prog_expo_2000; name=EXPO 2000 Hannover; migration_origin=mig_qext_b_source_urls \| mig_qext_c_primary_source_url; strict_source_url_cleanup_at=2026-05-23T11:01:59.122927+00:00 | candidate nearby | 7 rels; exact 0; cand 1; review 3; BELEGT_IN, TEIL_VON_PROGRAMM, CONCERNS | relationship fact or Claim if attribute-like |

### `Huerde` (28)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=h_akzeptanzproblem; name=Akzeptanzproblem; source_resolution_status=needs_source_url_review; source_trace_migration=mig_trace_zitiert_quelle_to_urls_2026_05_23 | needs review | 22 rels; exact 0; cand 0; review 10; HAT_HUERDE, HAT_HUERDEKATEGORIE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 2 | id=h_anschlussproblem; name=Anschlussproblem; source_resolution_status=needs_source_url_review; source_trace_migration=mig_trace_zitiert_quelle_to_urls_2026_05_23 | needs review | 100 rels; exact 0; cand 0; review 49; HAT_HUERDEKATEGORIE, ANCHORED_BY, HAS_DATA_ISSUE, HAT_HUERDE, CONCERNS | relationship fact or Claim if attribute-like |
| 3 | id=h_aufbereitungsaufwand; name=Aufbereitungsaufwand; source_resolution_status=needs_source_url_review; source_trace_migration=mig_trace_zitiert_quelle_to_urls_2026_05_23 | needs review | 58 rels; exact 0; cand 0; review 28; HAT_HUERDEKATEGORIE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_HUERDE | relationship fact or Claim if attribute-like |
| 4 | id=h_ausschreibungsproblem; name=Ausschreibungsproblem; source_resolution_status=needs_source_url_review; source_trace_migration=mig_trace_zitiert_quelle_to_urls_2026_05_23 | needs review | 16 rels; exact 0; cand 0; review 7; HAT_HUERDE, HAT_HUERDEKATEGORIE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 5 | id=h_bauproduktstatus; name=Bauproduktstatus; source_resolution_status=needs_source_url_review; source_trace_migration=mig_trace_zitiert_quelle_to_urls_2026_05_23 | needs review | 36 rels; exact 0; cand 0; review 17; HAT_HUERDEKATEGORIE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_HUERDE | relationship fact or Claim if attribute-like |

### `Material` (26)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=mat_aluminium; name=Aluminium; last_seen_by=agent10_phase4b_2; migration_origin=mig_qext_b_source_urls \| mig_qext_c_primary_source_url | candidate nearby | 49 rels; exact 0; cand 1; review 24; HAT_MATERIALGRUPPE, BELEGT_IN, ANCHORED_BY, CONCERNS, NUTZT_MATERIAL | relationship fact or Claim if attribute-like |
| 2 | id=mat_beton; name=Beton; migration_origin=mig_qext_b_source_urls; strict_source_url_cleanup_at=2026-05-23T11:01:59.122927+00:00 | candidate nearby | 128 rels; exact 0; cand 6; review 63; HAT_MATERIALGRUPPE, TYPISCH_BEI_MATERIAL, ANCHORED_BY, HAS_DATA_ISSUE, NUTZT_MATERIAL | relationship fact or Claim if attribute-like |
| 3 | id=mat_bitumen; name=Bitumen; source_resolution_status=needs_source_url_review; source_trace_migration=mig_trace_zitiert_quelle_to_urls_2026_05_23 | needs review | 14 rels; exact 0; cand 0; review 6; NUTZT_MATERIAL, HAT_MATERIALGRUPPE, TYPISCH_BEI_MATERIAL, ANCHORED_BY, CONCERNS | relationship fact or Claim if attribute-like |
| 4 | id=mat_holz_clt; name=CLT / Brettsperrholz; source_resolution_status=needs_source_url_review; name_full=Cross-Laminated Timber / Brettsperrholz — kreuzweise verleimtes Massivholzpaneel | needs review | 10 rels; exact 0; cand 0; review 4; NUTZT_MATERIAL, HAT_MATERIALGRUPPE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 5 | id=mat_daemmstoff; name=Daemmstoff; source_resolution_status=needs_source_url_review; source_trace_migration=mig_trace_zitiert_quelle_to_urls_2026_05_23 | needs review | 46 rels; exact 0; cand 0; review 22; HAT_MATERIALGRUPPE, TYPISCH_BEI_MATERIAL, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `Akteurrolle` (24)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=ar_aufbereitung_refurbishment; name=Aufbereitung_Refurbishment; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | candidate nearby | 37 rels; exact 0; cand 7; review 18; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_AKTEURROLLE | relationship fact or Claim if attribute-like |
| 2 | id=ar_bauausfuehrung_fertigung; name=Bauausfuehrung_Fertigung; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | candidate nearby | 141 rels; exact 0; cand 13; review 70; ANCHORED_BY, HAS_DATA_ISSUE, HAT_AKTEURROLLE, CONCERNS | relationship fact or Claim if attribute-like |
| 3 | id=ar_bauherr_auftraggeber; name=Bauherr_Auftraggeber; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 175 rels; exact 0; cand 0; review 87; ANCHORED_BY, HAS_DATA_ISSUE, HAT_AKTEURROLLE, CONCERNS | relationship fact or Claim if attribute-like |
| 4 | id=ar_betrieb_nutzung; name=Betrieb_Nutzung; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 71 rels; exact 0; cand 0; review 35; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_AKTEURROLLE | relationship fact or Claim if attribute-like |
| 5 | id=ar_bildung_wissenstransfer; name=Bildung_Wissenstransfer; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | candidate nearby | 43 rels; exact 0; cand 19; review 21; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_AKTEURROLLE | relationship fact or Claim if attribute-like |

### `Bauteiltyp` (23)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=bt_ausbau; name=Ausbau; source_resolution_status=needs_source_url_review; brand_layer=space_plan | needs review | 110 rels; exact 0; cand 0; review 54; TEILT_LAYER, ANCHORED_BY, HAS_DATA_ISSUE, HAT_BAUTEILTYP, CONCERNS | relationship fact or Claim if attribute-like |
| 2 | id=bt_boden; name=Boden; source_resolution_status=needs_source_url_review; brand_layer=space_plan | needs review | 122 rels; exact 0; cand 0; review 60; TYPISCH_BEI_BAUTEILTYP, TEILT_LAYER, ANCHORED_BY, HAS_DATA_ISSUE, HAT_BAUTEILTYP | relationship fact or Claim if attribute-like |
| 3 | id=bt_dach; name=Dach; source_resolution_status=needs_source_url_review; brand_layer=skin | needs review | 57 rels; exact 0; cand 0; review 27; TYPISCH_BEI_BAUTEILTYP, TEILT_LAYER, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=bt_daemmung; name=Daemmung; source_resolution_status=needs_source_url_review; brand_layer=structure | needs review | 40 rels; exact 0; cand 0; review 19; TYPISCH_BEI_BAUTEILTYP, TEILT_LAYER, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 5 | id=bt_decke; name=Decke; source_resolution_status=needs_source_url_review; brand_layer=structure | needs review | 114 rels; exact 0; cand 0; review 56; TEILT_LAYER, ANCHORED_BY, HAS_DATA_ISSUE, HAT_BAUTEILTYP, CONCERNS | relationship fact or Claim if attribute-like |

### `Materialdepot` (23)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=bw_paris_regional_donor_sources_ferme_du_rail; name=Aggregierte Pariser und…; is_material_depot=True; name_full=Aggregierte Pariser und regionale Reuse-Gisements fuer La Ferme du Rail | candidate nearby | 31 rels; exact 0; cand 1; review 15; NUTZT_BAUWERK, HAT_BAUOBJEKTKLASSE, HAT_BAUOBJEKTROLLE, HAT_STATUS, LIEGT_IN_STADT | relationship fact or Claim if attribute-like |
| 2 | id=bw_paris_material_sources_circular_pavilion; name=Aggregierte Pariser…; is_material_depot=True; name_full=Aggregierte Pariser Materialquellen fuer Circular Pavilion | candidate nearby | 29 rels; exact 0; cand 1; review 14; NUTZT_BAUWERK, HAT_BAUOBJEKTKLASSE, HAT_BAUOBJEKTROLLE, HAT_STATUS, LIEGT_IN_STADT | relationship fact or Claim if attribute-like |
| 3 | id=bw_bellastock_ville_des_terres_l_ile_saint_denis_lager; name=Bellastock Ville des…; is_material_depot=True; name_full=Bellastock Ville des Terres / L’Île-Saint-Denis Lager | candidate nearby | 13 rels; exact 0; cand 1; review 6; HAT_BAUOBJEKTKLASSE, HAT_BAUOBJEKTROLLE, HAT_STATUS, BELEGT_IN, BETRIEBEN_VON | relationship fact or Claim if attribute-like |
| 4 | id=bw_berlin_fitout_donor_sources; name=Berlin donors; nutzung_text=Donorquellen für Interior-Reuse; is_material_depot=True | candidate nearby | 35 rels; exact 0; cand 1; review 17; NUTZT_BAUWERK, HAT_BAUOBJEKTKLASSE, HAT_BAUOBJEKTROLLE, HAT_STATUS, HAT_NUTZUNG | relationship fact or Claim if attribute-like |
| 5 | id=bw_cleveland_steel_and_tubes_stock; name=Cleveland S&T stock; is_material_depot=True; name_full=Cleveland Steel and Tubes reclaimed stock | candidate nearby | 13 rels; exact 0; cand 1; review 6; HAT_BAUOBJEKTKLASSE, HAT_BAUOBJEKTROLLE, HAT_STATUS, HAT_RESSOURCENQUELLE, BELEGT_IN | relationship fact or Claim if attribute-like |

### `ReuseRule` (20)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=rr_be_beton; name=Belgien × Beton reuse rule; evidence_basis=research_file_row; source_count=1 | exact nearby | 25 rels; exact 1; cand 8; review 12; APPLIES_IN, APPLIES_TO, RELEVANT_FOR, CONCERNS, HAS_SOURCE_LINK | relationship fact or Claim if attribute-like |
| 2 | id=rr_be_holz; name=Belgien × Holz reuse rule; evidence_basis=research_file_row; source_count=1 | exact nearby | 29 rels; exact 1; cand 6; review 14; REFERENZIERT_NORM, APPLIES_IN, APPLIES_TO, CONCERNS, HAS_SOURCE_LINK | relationship fact or Claim if attribute-like |
| 3 | id=rr_be_naturstein; name=Belgien × Naturstein reuse rule; evidence_basis=research_file_row; source_count=1 | exact nearby | 31 rels; exact 1; cand 10; review 15; APPLIES_IN, APPLIES_TO, RELEVANT_FOR, CONCERNS, HAS_SOURCE_LINK | relationship fact or Claim if attribute-like |
| 4 | id=rr_be_stahl; name=Belgien × Stahl reuse rule; evidence_basis=research_file_row; source_count=1 | exact nearby | 27 rels; exact 1; cand 6; review 13; REFERENZIERT_NORM, APPLIES_IN, APPLIES_TO, CONCERNS, HAS_SOURCE_LINK | relationship fact or Claim if attribute-like |
| 5 | id=rr_de_beton; name=Deutschland × Beton reuse rule; evidence_basis=research_file_row; source_count=1 | exact nearby | 23 rels; exact 1; cand 7; review 11; APPLIES_IN, APPLIES_TO, RELEVANT_FOR, CONCERNS, HAS_SOURCE_LINK | relationship fact or Claim if attribute-like |

### `Land` (19)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=land_belgien; name=Belgien; actor_registry_loader_seen=agent10; pcb_verbot_jahr=1986 | candidate nearby | 198 rels; exact 0; cand 34; review 99; HAT_TYPISCHEN_BAUPRODUKTSTATUS, ANCHORED_BY, APPLIES_IN, GEHÖRT_ZU, LIEGT_IN_LAND | relationship fact or Claim if attribute-like |
| 2 | id=land_deutschland; name=Deutschland; actor_registry_loader_seen=agent10; kmf_grenzwert_jahr=1996 | candidate nearby | 426 rels; exact 0; cand 78; review 213; GILT_IN_LAND, HAT_TYPISCHEN_BAUPRODUKTSTATUS, ANCHORED_BY, GEHÖRT_ZU, LIEGT_IN_LAND | relationship fact or Claim if attribute-like |
| 3 | id=land_daenemark; name=Dänemark; actor_registry_loader_seen=agent10; pcb_verbot_jahr=1986 | candidate nearby | 80 rels; exact 0; cand 16; review 40; BELEGT_IN, HAT_TYPISCHEN_BAUPRODUKTSTATUS, ANCHORED_BY, GEHÖRT_ZU, LIEGT_IN_LAND | relationship fact or Claim if attribute-like |
| 4 | id=land_eu; name=Europäische Union (Geltungsbereich); source_scope=controlled_vocab_seed; scope_type=supranational | needs review | 28 rels; exact 0; cand 0; review 14; CONCERNS, GILT_IN_LAND | relationship fact or Claim if attribute-like |
| 5 | id=land_eea; name=Europäischer Wirtschaftsraum (EU+EEA); source_scope=controlled_vocab_seed; scope_type=supranational | needs review | 8 rels; exact 0; cand 0; review 4; GILT_IN_LAND, CONCERNS | relationship fact or Claim if attribute-like |

### `Software` (19)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=tool_bim_bauteilkatalog; name=BIM / digitaler Bauteilkatalog; source_resolution_status=needs_source_url_review; kind=tool | needs review | 10 rels; exact 0; cand 0; review 4; NUTZT_SOFTWARE, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 2 | id=tool_bauteilkatalog; name=Bauteilkatalog / Bauteilpass; source_resolution_status=needs_source_url_review; kind=tool | needs review | 10 rels; exact 0; cand 0; review 4; NUTZT_SOFTWARE, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 3 | id=software_bim; name=Building Information Modeling / BIM; source_resolution_status=needs_source_url_review; kind=software | needs review | 10 rels; exact 0; cand 0; review 4; NUTZT_SOFTWARE, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=software_concular; name=Concular; kind=software; migration_origin=mig_qext_b_source_urls \| mig_qext_c_primary_source_url | candidate nearby | 23 rels; exact 0; cand 1; review 11; BELEGT_IN, NUTZT_SOFTWARE, CONCERNS | relationship fact or Claim if attribute-like |
| 5 | id=software_ecotool; name=EcoTool; source_resolution_status=needs_source_url_review; name_full=EcoTool — ökologische Bilanz (Pflichtnachweis Wettbewerb Lysbüchel) | needs review | 4 rels; exact 0; cand 0; review 1; NUTZT_SOFTWARE, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `Ressourcenquelle` (16)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=rq_baustelle; name=Baustelle; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 217 rels; exact 0; cand 0; review 108; ANCHORED_BY, HAS_DATA_ISSUE, HAT_RESSOURCENQUELLE, CONCERNS | relationship fact or Claim if attribute-like |
| 2 | id=rq_bauteilboerse; name=Bauteilboerse; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 79 rels; exact 0; cand 0; review 39; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_RESSOURCENQUELLE | relationship fact or Claim if attribute-like |
| 3 | id=rq_borrowed_material_pool; name=Borrowed_Material_Pool; datenqualitaet=Belegt; migration_origin=mig_qext_b_source_urls | needs review | 11 rels; exact 0; cand 0; review 5; HAT_RESSOURCENQUELLE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=rq_construction_waste_stream; name=Construction_Waste_Stream; datenqualitaet=Belegt; migration_origin=mig_qext_b_source_urls | needs review | 7 rels; exact 0; cand 0; review 3; HAT_RESSOURCENQUELLE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 5 | id=rq_demolition_waste_stream; name=Demolition_Waste_Stream; datenqualitaet=Belegt; migration_origin=mig_qext_b_source_urls | needs review | 5 rels; exact 0; cand 0; review 2; HAT_RESSOURCENQUELLE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `Bauproduktstatus` (15)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=bps_baupg_ch; name=BauPG (CH); scope_note=Swiss construction-products regime under BauPG.; name_full=BauPG-Status (CH, Schweizer Bauprodukteverordnung) | needs review | 29 rels; exact 0; cand 0; review 14; HAT_TYPISCHEN_BAUPRODUKTSTATUS, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_BAUPRODUKTSTATUS | relationship fact or Claim if attribute-like |
| 2 | id=bps_bestand_no_status; name=Bestand vor Ort; scope_note=On-site reuse without placing the element on the market — no Bauproduktstatus ne...; name_full=Bestand vor Ort weiterverwendet (kein neues Inverkehrbringen) | needs review | 71 rels; exact 0; cand 0; review 35; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_BAUPRODUKTSTATUS | relationship fact or Claim if attribute-like |
| 3 | id=bps_ce_eta; name=CE (ETA); scope_note=EU CPR alternative for non-hEN products; requires ETA assessment.; name_full=CE-Marking via Europäische Technische Bewertung (ETA) | needs review | 3 rels; exact 0; cand 0; review 1; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=bps_ce_hen; name=CE (hEN); scope_note=EU CPR; covers CE-marked construction products under harmonised European standar...; name_full=CE-Marking unter harmonisierter EN-Norm (hEN) | needs review | 25 rels; exact 0; cand 0; review 12; HAT_TYPISCHEN_BAUPRODUKTSTATUS, HAT_BAUPRODUKTSTATUS, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 5 | id=bps_ibc_104_11_alternative; name=IBC 104.11 (USA); scope_note=US IBC clause allowing alternative materials approved by the building official.; name_full=IBC 104.11 alternative materials and methods (USA) | needs review | 9 rels; exact 0; cand 0; review 4; HAT_TYPISCHEN_BAUPRODUKTSTATUS, HAT_BAUPRODUKTSTATUS, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `RechtlicheBedingung` (15)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=rb_bauordnungsrecht; name=Bauordnungsrecht; evidence_basis=controlled_vocab; scope_note=Building approval law applies in every corpus country; specific instruments diff... | needs review | 9 rels; exact 0; cand 0; review 4; HAT_RECHTLICHE_BEDINGUNG, BELEGT_IN, CONCERNS | relationship fact or Claim if attribute-like |
| 2 | id=rb_bauproduktenverordnung_cpr; name=Bauproduktenverordnung (CPR); evidence_basis=registry_stub; migration_origin=mig_r2_c_restore_legal \| mig_qext_b_source_urls \| mig_qext_c_primary_source_url | needs review | 3 rels; exact 0; cand 0; review 1; BELEGT_IN, CONCERNS | relationship fact or Claim if attribute-like |
| 3 | id=rb_boulder_deconstruction_ordinance_8366; name=Boulder Deconstruction Ordinance 8366 / 2020; evidence_basis=controlled_vocab; is_universal=False | needs review | 12 rels; exact 0; cand 0; review 4; HAT_RECHTLICHE_BEDINGUNG, BELEGT_IN, GILT_IN_LAND, CONCERNS, EXACT_MATCH_CANDIDATE | relationship fact or Claim if attribute-like |
| 4 | id=rb_ce_ukca_marking_reused_steel; name=CE/UKCA marking for reused steel; evidence_basis=controlled_vocab; is_universal=False | needs review | 17 rels; exact 0; cand 0; review 7; HAT_RECHTLICHE_BEDINGUNG, BELEGT_IN, GILT_IN_LAND, CONCERNS | relationship fact or Claim if attribute-like |
| 5 | id=rb_dibt_zustimmung; name=DIBt-Zustimmung im Einzelfall; evidence_basis=registry_stub; migration_origin=mig_r2_c_restore_legal \| mig_qext_b_source_urls \| mig_qext_c_primary_source_url | needs review | 3 rels; exact 0; cand 0; review 1; BELEGT_IN, CONCERNS | relationship fact or Claim if attribute-like |

### `Verbindungstechnik` (15)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=vt_bolzenverbindung; name=Bolzenverbindung; last_seen_by=agent10_phase4b_2; source_resolution_status=needs_source_url_review | needs review | 14 rels; exact 0; cand 0; review 6; HAT_VERBINDUNGSTECHNIK, BELEGT_IN, IST_UNTERVERFAHREN_VON, ANCHORED_BY, CONCERNS | relationship fact or Claim if attribute-like |
| 2 | id=vt_demontierbarer_schwerlastanker; name=Demontierbarer Schwerlastanker; last_seen_by=agent10_phase4b_2; source_resolution_status=needs_source_url_review | needs review | 10 rels; exact 0; cand 0; review 4; HAT_VERBINDUNGSTECHNIK, BELEGT_IN, IST_UNTERVERFAHREN_VON, ANCHORED_BY, CONCERNS | relationship fact or Claim if attribute-like |
| 3 | id=vt_klemmverbindung; name=Klemmverbindung; source_resolution_status=needs_source_url_review; migration_origin=mig_qext_b_source_urls | needs review | 16 rels; exact 0; cand 0; review 7; HAT_VERBINDUNGSTECHNIK, IST_UNTERVERFAHREN_VON, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=vt_mauerwerk_ausgleich; name=Mauerwerk_Ausgleichsschicht; note=Brick layer / masonry layer used as height compensation; migration_origin=mig_qext_b_source_urls \| mig_qext_c_primary_source_url | candidate nearby | 5 rels; exact 0; cand 1; review 2; HAT_VERBINDUNGSTECHNIK, BELEGT_IN, CONCERNS | relationship fact or Claim if attribute-like |
| 5 | id=vt_reversible_fuegung; name=Reversible_Fuegung; last_seen_by=agent10_phase4b_2; source_resolution_status=needs_source_url_review | needs review | 110 rels; exact 0; cand 0; review 54; BELEGT_IN, IST_UNTERVERFAHREN_VON, ANCHORED_BY, HAS_DATA_ISSUE, HAT_VERBINDUNGSTECHNIK | relationship fact or Claim if attribute-like |

### `Wiederverwendungskette` (14)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=k_bestandserhalt_blackfriars_tragstruktur; name=Bestandserhalt Blackfria…; methodische_abgrenzung=Bestandserhalt nicht als Direct Reuse werten; name_full=Bestandserhalt Blackfriars Tragstruktur | candidate nearby | 9 rels; exact 0; cand 1; review 4; TEIL_VON_KETTE, BELEGT_IN, FROM_DONOR, INTO_RECEIVER, CONCERNS | relationship fact or Claim if attribute-like |
| 2 | id=k_reuse_kette_drill_stem_pipe_dachtragwerk_nach_saxum_barn; name=Drill-Stem-Pipe Dach; name_full=Reuse-Kette Drill-Stem-Pipe Dachtragwerk nach Saxum Barn; migration_origin=mig_qext_b_source_urls \| mig_qext_c_primary_source_url | candidate nearby | 9 rels; exact 0; cand 1; review 4; TEIL_VON_KETTE, BELEGT_IN, FROM_DONOR, INTO_RECEIVER, CONCERNS | relationship fact or Claim if attribute-like |
| 3 | id=k_reuse_kette_drill_stem_pipe_stutzen_nach_saxum_barn; name=Drill-Stem-Pipe Stütze; name_full=Reuse-Kette Drill-Stem-Pipe Stützen nach Saxum Barn; migration_origin=mig_qext_b_source_urls \| mig_qext_c_primary_source_url | candidate nearby | 9 rels; exact 0; cand 1; review 4; TEIL_VON_KETTE, BELEGT_IN, FROM_DONOR, INTO_RECEIVER, CONCERNS | relationship fact or Claim if attribute-like |
| 4 | id=k_geplante_reuse_kette_broadgate_stahl_nach_blackfriars; name=Geplante Reuse-Kette…; status=geplant / nicht gebaut bestätigt; name_full=Geplante Reuse-Kette Broadgate-Stahl nach Blackfriars | candidate nearby | 9 rels; exact 0; cand 1; review 4; TEIL_VON_KETTE, BELEGT_IN, FROM_DONOR, INTO_RECEIVER, CONCERNS | relationship fact or Claim if attribute-like |
| 5 | id=k_reuse_kette_btc_ville_des_terres_nach_stains; name=Reuse-Kette BTC Ville…; name_full=Reuse-Kette BTC Ville des Terres nach Stains; migration_origin=mig_qext_b_source_urls \| mig_qext_c_primary_source_url | candidate nearby | 9 rels; exact 0; cand 1; review 4; TEIL_VON_KETTE, BELEGT_IN, FROM_DONOR, INTO_RECEIVER, CONCERNS | relationship fact or Claim if attribute-like |

### `DeprecatedType` (13)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=dep_label__GraphVersion; reason=Experimental versioning label — never populated.; evidence_basis=audit_record; old_name=GraphVersion | none visible | 0 rels; exact 0; cand 0; review 0;  | relationship fact or Claim if attribute-like |
| 2 | id=dep_label__LebenszyklusModul; reason=Renamed in R2.b — original IDs (lz_*) preserved on new nodes.; evidence_basis=audit_record; old_name=LebenszyklusModul | none visible | 0 rels; exact 0; cand 0; review 0;  | relationship fact or Claim if attribute-like |
| 3 | id=dep_label__ZertifizierungBewertungssystem; reason=Renamed in R2.d for brevity — old name preserved as alias on new nodes.; evidence_basis=audit_record; old_name=ZertifizierungBewertungssystem | none visible | 0 rels; exact 0; cand 0; review 0;  | relationship fact or Claim if attribute-like |
| 4 | id=dep_rel_type__ASSOZIIERT__MIT__PROJEKT; reason=Renamed in R9 for honest stub semantics.; evidence_basis=audit_record; old_name=ASSOZIIERT_MIT_PROJEKT | none visible | 0 rels; exact 0; cand 0; review 0;  | relationship fact or Claim if attribute-like |
| 5 | id=dep_rel_type__AUS__BAUWERK; reason=Phase 4.2 rename.; evidence_basis=audit_record; old_name=AUS_BAUWERK | none visible | 0 rels; exact 0; cand 0; review 0;  | relationship fact or Claim if attribute-like |

### `Methode` (13)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=meth_abrissmonitoring; name=Abrissmonitoring; source_resolution_status=needs_source_url_review; source_trace_migration=mig_trace_zitiert_quelle_to_urls_2026_05_23 | needs review | 6 rels; exact 0; cand 0; review 2; HAT_METHODE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 2 | id=meth_bauteilkatalogisierung; name=Bauteilkatalogisierung; source_resolution_status=needs_source_url_review; source_trace_migration=mig_trace_zitiert_quelle_to_urls_2026_05_23 | needs review | 116 rels; exact 0; cand 0; review 57; ANCHORED_BY, HAS_DATA_ISSUE, HAT_METHODE, CONCERNS | relationship fact or Claim if attribute-like |
| 3 | id=meth_building_material_scouting; name=Building_Material_Scouting; source_resolution_status=needs_source_url_review; source_trace_migration=mig_trace_zitiert_quelle_to_urls_2026_05_23 | needs review | 136 rels; exact 0; cand 0; review 67; ANCHORED_BY, HAS_DATA_ISSUE, HAT_METHODE, CONCERNS | relationship fact or Claim if attribute-like |
| 4 | id=meth_design_for_disassembly; name=Design_for_Disassembly; source_resolution_status=needs_source_url_review; source_trace_migration=mig_trace_zitiert_quelle_to_urls_2026_05_23 | needs review | 103 rels; exact 0; cand 0; review 50; ANCHORED_BY, HAS_DATA_ISSUE, EXACT_MATCH_CANDIDATE, HAT_METHODE, CONCERNS | relationship fact or Claim if attribute-like |
| 5 | id=meth_form_follows_availability; name=Form_Follows_Availability; source_resolution_status=needs_source_url_review; source_trace_migration=mig_trace_zitiert_quelle_to_urls_2026_05_23 | needs review | 282 rels; exact 0; cand 0; review 140; ANCHORED_BY, HAS_DATA_ISSUE, HAT_METHODE, CONCERNS | relationship fact or Claim if attribute-like |

### `Wirtschaft` (12)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=wi_capex_hoeher_marketing_payback; name=CapEx höher, Marketing-/Branding-Payback; scope_note=Reuse-Mehrkosten amortisieren über PR/Positionierung/Marktdifferenzierung.; migration_origin=mig_qext_b_source_urls | needs review | 7 rels; exact 0; cand 0; review 3; HAT_WIRTSCHAFT, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 2 | id=wi_capex_hoeher_opex_payback; name=CapEx höher, Payback über OpEx / LCA; scope_note=Upfront-Mehrkosten amortisieren über Lebenszyklusvorteile (Wartung, Energie, CO₂...; migration_origin=mig_qext_b_source_urls | needs review | 7 rels; exact 0; cand 0; review 3; HAT_WIRTSCHAFT, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 3 | id=wi_capex_hoeher_subvention; name=CapEx höher, Subvention/Förderung deckt Mehrkosten; scope_note=Reuse-Mehrkosten durch öffentliche Förderung oder Forschungsfinanzierung kompens...; migration_origin=mig_qext_b_source_urls | needs review | 31 rels; exact 0; cand 0; review 15; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_WIRTSCHAFT | relationship fact or Claim if attribute-like |
| 4 | id=wi_capex_niedriger_direkter_ersparnis; name=CapEx niedriger (direkte Materialersparnis); scope_note=Reuse spart Materialeinkauf; CapEx fällt unter Neubaureferenz.; migration_origin=mig_qext_b_source_urls | needs review | 7 rels; exact 0; cand 0; review 3; HAT_WIRTSCHAFT, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 5 | id=wi_capex_neutral; name=CapEx vergleichbar mit Neubau; scope_note=Investitionskosten in Größenordnung Neubaureferenz; Reuse als CO₂-/Materialeinsp...; migration_origin=mig_qext_b_source_urls | needs review | 11 rels; exact 0; cand 0; review 5; HAT_WIRTSCHAFT, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `Marktmodell` (11)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=mm_forschungsprojekt_zuteilung; name=Forschungs-Zuteilung; scope_note=Allocation via research project (UMAR, ReCreate pilots, etc.).; name_full=Forschungsprojekt-Zuteilung | needs review | 43 rels; exact 0; cand 0; review 21; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_MARKTMODELL | relationship fact or Claim if attribute-like |
| 2 | id=mm_intra_konzern; name=Intra-Konzern; scope_note=Material transferred within the same legal entity / corporate group; no third-pa...; name_full=Intra-Konzern-Transfer | needs review | 15 rels; exact 0; cand 0; review 7; HAT_MARKTMODELL, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 3 | id=mm_kauf_gebraucht; name=Kauf gebraucht; scope_note=Sale acknowledged as used material; reduced product-status expectations.; name_full=Kauf als Gebrauchtware | needs review | 47 rels; exact 0; cand 0; review 23; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_MARKTMODELL | relationship fact or Claim if attribute-like |
| 4 | id=mm_kauf_neu; name=Kauf neu-äquiv.; scope_note=Sale as if a new construction product; full CPR/CE conformity expected.; name_full=Kauf als Bauprodukt (Neuware-äquivalent) | needs review | 11 rels; exact 0; cand 0; review 5; HAT_MARKTMODELL, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 5 | id=mm_leasing; name=Leasing; scope_note=Element leased rather than purchased; ownership stays with provider. Liander HQ ...; name_full=Leasing / Mietverhältnis | needs review | 35 rels; exact 0; cand 0; review 17; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_MARKTMODELL | relationship fact or Claim if attribute-like |

### `Materialgruppe` (11)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=mg_daemmstoff; name=Daemmstoff; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 43 rels; exact 0; cand 0; review 21; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_MATERIALGRUPPE | relationship fact or Claim if attribute-like |
| 2 | id=mg_glas_keramik; name=Glas_Keramik; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 165 rels; exact 0; cand 0; review 82; ANCHORED_BY, HAS_DATA_ISSUE, HAT_MATERIALGRUPPE, CONCERNS | relationship fact or Claim if attribute-like |
| 3 | id=mg_holz_biobasiert; name=Holz_Biobasiert; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 217 rels; exact 0; cand 0; review 108; ANCHORED_BY, HAS_DATA_ISSUE, HAT_MATERIALGRUPPE, CONCERNS | relationship fact or Claim if attribute-like |
| 4 | id=mg_kunststoff; name=Kunststoff; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 47 rels; exact 0; cand 0; review 23; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_MATERIALGRUPPE | relationship fact or Claim if attribute-like |
| 5 | id=mg_lehm_erde; name=Lehm_Erde; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 11 rels; exact 0; cand 0; review 5; HAT_MATERIALGRUPPE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `WiederverwendungsArt` (11)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=wva_adaptives_reuse; name=Adaptives_ReUse; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 49 rels; exact 0; cand 0; review 24; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_WIEDERVERWENDUNGSART | relationship fact or Claim if attribute-like |
| 2 | id=wva_bestandserhalt; name=Bestandserhalt; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 83 rels; exact 0; cand 0; review 41; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_WIEDERVERWENDUNGSART | relationship fact or Claim if attribute-like |
| 3 | id=wva_design_for_disassembly; name=Design_for_Disassembly; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 65 rels; exact 0; cand 0; review 32; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_WIEDERVERWENDUNGSART | relationship fact or Claim if attribute-like |
| 4 | id=wva_direkte_wiederverwendung; name=Direkte_Wiederverwendung; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 701 rels; exact 0; cand 0; review 350; ANCHORED_BY, HAS_DATA_ISSUE, HAT_WIEDERVERWENDUNGSART, CONCERNS | relationship fact or Claim if attribute-like |
| 5 | id=wva_recycling; name=Recycling; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 59 rels; exact 0; cand 0; review 29; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_WIEDERVERWENDUNGSART | relationship fact or Claim if attribute-like |

### `Akteurtyp` (10)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=at_foerdergeber_programmtraeger; name=Foerdergeber_Programmtraeger; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 11 rels; exact 0; cand 0; review 5; HAT_AKTEURTYP, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 2 | id=at_forschung_lehre; name=Forschung_Lehre; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | candidate nearby | 89 rels; exact 0; cand 20; review 44; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_AKTEURTYP | relationship fact or Claim if attribute-like |
| 3 | id=at_materialhub_bauteilboerse; name=Materialhub_Bauteilboerse; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | candidate nearby | 39 rels; exact 0; cand 8; review 19; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_AKTEURTYP | relationship fact or Claim if attribute-like |
| 4 | id=at_ngo_verband_netzwerk; name=NGO_Verband_Netzwerk; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | candidate nearby | 49 rels; exact 0; cand 6; review 24; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_AKTEURTYP | relationship fact or Claim if attribute-like |
| 5 | id=at_oeffentliche_institution; name=Oeffentliche_Institution; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 73 rels; exact 0; cand 0; review 36; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_AKTEURTYP | relationship fact or Claim if attribute-like |

### `BauaufgabeIntervention` (10)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=bai_aufstockung; name=Aufstockung; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 17 rels; exact 0; cand 0; review 8; HAT_INTERVENTION, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 2 | id=bai_erweiterung; name=Erweiterung; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 15 rels; exact 0; cand 0; review 7; HAT_INTERVENTION, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 3 | id=bai_fit_out; name=Fit_out; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 13 rels; exact 0; cand 0; review 6; HAT_INTERVENTION, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=bai_neubau; name=Neubau; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 119 rels; exact 0; cand 0; review 59; ANCHORED_BY, HAS_DATA_ISSUE, HAT_INTERVENTION, CONCERNS | relationship fact or Claim if attribute-like |
| 5 | id=bai_rueckbau; name=Rueckbau; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 19 rels; exact 0; cand 0; review 9; HAT_INTERVENTION, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `Beschaffungsweg` (10)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=bweg_ausschreibung; name=Ausschreibung; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 33 rels; exact 0; cand 0; review 16; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_BESCHAFFUNGSWEG | relationship fact or Claim if attribute-like |
| 2 | id=bweg_bauteilboerse; name=Bauteilboerse; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 99 rels; exact 0; cand 0; review 49; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_BESCHAFFUNGSWEG | relationship fact or Claim if attribute-like |
| 3 | id=bweg_digitale_plattform; name=Digitale_Plattform; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 43 rels; exact 0; cand 0; review 21; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_BESCHAFFUNGSWEG | relationship fact or Claim if attribute-like |
| 4 | id=bweg_direktvermittlung; name=Direktvermittlung; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 95 rels; exact 0; cand 0; review 47; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_BESCHAFFUNGSWEG | relationship fact or Claim if attribute-like |
| 5 | id=bweg_eigenbestand; name=Eigenbestand; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 45 rels; exact 0; cand 0; review 22; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_BESCHAFFUNGSWEG | relationship fact or Claim if attribute-like |

### `Defekt` (10)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=def_brandschaden; name=Brandschaden; scope_note=Fire damage: SCI P427 excludes fire-exposed members from steel reuse.; migration_origin=mig_qext_b_source_urls | needs review | 17 rels; exact 0; cand 0; review 8; TYPISCH_BEI_MATERIAL, HAT_DEFEKT_BEFUND, HAT_DEFEKT, ANCHORED_BY, CONCERNS | relationship fact or Claim if attribute-like |
| 2 | id=def_chemische_belastung; name=Chemisch belastet; scope_note=Salt efflorescence, acid attack, oil contamination.; name_full=Chemische Belastung (Salze, Säuren, Öle) | needs review | 7 rels; exact 0; cand 0; review 3; TYPISCH_BEI_MATERIAL, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 3 | id=def_hohlraum_delamination; name=Delamination; scope_note=Voids, debonding, layer separation in composite/laminated elements.; name_full=Hohlraum / Delamination | needs review | 9 rels; exact 0; cand 0; review 4; TYPISCH_BEI_MATERIAL, HAT_DEFEKT_BEFUND, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=def_holzwurm_pilzbefall; name=Holzwurm/Pilz; scope_note=Biological attack on timber and bio-based materials.; name_full=Holzwurm / Pilzbefall / Schimmel | needs review | 9 rels; exact 0; cand 0; review 4; TYPISCH_BEI_MATERIAL, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 5 | id=def_karbonatisierung; name=Karbonatisierung; scope_note=Carbonation depth in concrete; affects rebar protection and remaining service li...; name_full=Karbonatisierung (Beton) | needs review | 9 rels; exact 0; cand 0; review 4; TYPISCH_BEI_MATERIAL, HAT_DEFEKT, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `HuerdeKategorie` (10)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=hk_beschaffung_markt; name=Beschaffung_Markt; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 11 rels; exact 0; cand 0; review 5; HAT_HUERDEKATEGORIE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 2 | id=hk_daten_evidenz; name=Daten_Evidenz; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 77 rels; exact 0; cand 0; review 38; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_HUERDEKATEGORIE | relationship fact or Claim if attribute-like |
| 3 | id=hk_logistisch; name=Logistisch; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 29 rels; exact 0; cand 0; review 14; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_HUERDEKATEGORIE | relationship fact or Claim if attribute-like |
| 4 | id=hk_planerisch; name=Planerisch; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 9 rels; exact 0; cand 0; review 4; HAT_HUERDEKATEGORIE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 5 | id=hk_rechtlich; name=Rechtlich; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 57 rels; exact 0; cand 0; review 28; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_HUERDEKATEGORIE | relationship fact or Claim if attribute-like |

### `Logistik` (10)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=log_bauteiltracking; name=Bauteiltracking; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 61 rels; exact 0; cand 0; review 30; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_LOGISTIK | relationship fact or Claim if attribute-like |
| 2 | id=log_just_in_time; name=Just_in_Time; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 23 rels; exact 0; cand 0; review 11; HAT_LOGISTIK, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 3 | id=log_lagerflaeche; name=Lagerflaeche; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 7 rels; exact 0; cand 0; review 3; HAT_LOGISTIK, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=log_lagerung; name=Lagerung; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 153 rels; exact 0; cand 0; review 76; ANCHORED_BY, HAS_DATA_ISSUE, HAT_LOGISTIK, CONCERNS | relationship fact or Claim if attribute-like |
| 5 | id=log_lokale_wiederverwendung; name=Lokale_Wiederverwendung; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 109 rels; exact 0; cand 0; review 54; ANCHORED_BY, HAS_DATA_ISSUE, HAT_LOGISTIK, CONCERNS | relationship fact or Claim if attribute-like |

### `Prozessphase` (10)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=phase_aufbereitung; name=Aufbereitung; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 242 rels; exact 0; cand 0; review 120; ANCHORED_BY, HAS_DATA_ISSUE, EXACT_MATCH_CANDIDATE, HAT_PROZESSPHASE, CONCERNS | relationship fact or Claim if attribute-like |
| 2 | id=phase_betrieb; name=Betrieb; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 21 rels; exact 0; cand 0; review 10; HAT_PROZESSPHASE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 3 | id=phase_dokumentation; name=Dokumentation; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 57 rels; exact 0; cand 0; review 28; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_PROZESSPHASE | relationship fact or Claim if attribute-like |
| 4 | id=phase_identifikation; name=Identifikation; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 221 rels; exact 0; cand 0; review 110; ANCHORED_BY, HAS_DATA_ISSUE, HAT_PROZESSPHASE, CONCERNS | relationship fact or Claim if attribute-like |
| 5 | id=phase_lagerung; name=Lagerung; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 70 rels; exact 0; cand 0; review 34; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, EXACT_MATCH_CANDIDATE, HAT_PROZESSPHASE | relationship fact or Claim if attribute-like |

### `Bausystem` (9)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=bsys_betonfertigteil_system; name=Betonfertigteil_System; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 45 rels; exact 0; cand 0; review 22; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_BAUSYSTEM | relationship fact or Claim if attribute-like |
| 2 | id=bsys_cross_laminated_secondary_timber_clst; name=CLST_cross_laminated_secondary_timber; migration_origin=mig_qext_b_source_urls; definition=Cross-laminated secondary timber from reclaimed solid wood; remanufactured panel... | needs review | 13 rels; exact 0; cand 0; review 6; HAT_TRAGWERKSPRINZIP, HAT_BAUWEISE, HAT_BAUSYSTEM, NUTZT_MATERIAL, ANCHORED_BY | relationship fact or Claim if attribute-like |
| 3 | id=bsys_holz_skelettbau; name=Holz_Skelettbau; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 9 rels; exact 0; cand 0; review 4; HAT_BAUSYSTEM, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=bsys_holzrahmenbau; name=Holzrahmenbau; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 15 rels; exact 0; cand 0; review 7; HAT_BAUSYSTEM, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 5 | id=bsys_iw73; name=IW73/6_Plattenbausystem; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 3 rels; exact 0; cand 0; review 1; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `MatchingQualitaet` (9)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=mq_geographic_intl; name=Geo: international; scope_note=Cross-border or transcontinental sourcing; high transport burden.; name_full=International / interkontinental | needs review | 9 rels; exact 0; cand 0; review 4; HAT_MATCHINGQUALITAET, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 2 | id=mq_geographic_local; name=Geo: lokal (<50 km); scope_note=Donor + receiver within ~50 km; lowest transport emissions.; name_full=Lokales geografisches Matching (<50 km) | needs review | 55 rels; exact 0; cand 0; review 27; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_MATCHINGQUALITAET | relationship fact or Claim if attribute-like |
| 3 | id=mq_geographic_regional; name=Geo: regional; scope_note=Regional supply chain.; name_full=Regional geografisches Matching (50–500 km) | needs review | 15 rels; exact 0; cand 0; review 7; HAT_MATCHINGQUALITAET, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=mq_spec_anpassung; name=Spec: Anpassung; scope_note=Cut, drill, refurbish to fit. Most common reuse case.; name_full=Spezifikations-Anpassung nötig | needs review | 153 rels; exact 0; cand 0; review 76; ANCHORED_BY, HAS_DATA_ISSUE, HAT_MATCHINGQUALITAET, CONCERNS | relationship fact or Claim if attribute-like |
| 5 | id=mq_spec_zweckaenderung; name=Spec: Zweckänderung; scope_note=Element repurposed to different function (e.g. granite facade → kitchen counter)...; name_full=Zweckänderung (Funktionswechsel) | needs review | 65 rels; exact 0; cand 0; review 32; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_MATCHINGQUALITAET | relationship fact or Claim if attribute-like |

### `Nutzung` (9)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=nut_buero; name=Buero; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 75 rels; exact 0; cand 0; review 37; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_NUTZUNG | relationship fact or Claim if attribute-like |
| 2 | id=nut_gewerbe; name=Gewerbe; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 79 rels; exact 0; cand 0; review 39; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_NUTZUNG | relationship fact or Claim if attribute-like |
| 3 | id=nut_infrastruktur; name=Infrastruktur; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 35 rels; exact 0; cand 0; review 17; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_NUTZUNG | relationship fact or Claim if attribute-like |
| 4 | id=nut_kultur; name=Kultur; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 71 rels; exact 0; cand 0; review 35; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_NUTZUNG | relationship fact or Claim if attribute-like |
| 5 | id=nut_lager_depot; name=Lager_Depot; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 15 rels; exact 0; cand 0; review 7; HAT_NUTZUNG, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `Schadstoff` (9)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=s_asbest; name=Asbest; last_seen_by=agent10_phase4b_2; migration_origin=mig_qext_b_source_urls | needs review | 97 rels; exact 0; cand 0; review 48; BELEGT_IN, TYPISCH_BEI_MATERIAL, TYPISCH_BEI_BAUTEILTYP, TYPISCH_BEI_ERA, ANCHORED_BY | relationship fact or Claim if attribute-like |
| 2 | id=s_bleifarbe; name=Bleifarbe; last_seen_by=agent10_phase4b_2; migration_origin=mig_qext_b_source_urls | needs review | 541 rels; exact 0; cand 0; review 270; BELEGT_IN, TYPISCH_BEI_MATERIAL, TYPISCH_BEI_BAUTEILTYP, TYPISCH_BEI_ERA, ANCHORED_BY | relationship fact or Claim if attribute-like |
| 3 | id=s_formaldehyd; name=Formaldehyd (MDF / Spanplatten); last_seen_by=agent10_phase4b_2; standards_body=EU REACH | needs review | 323 rels; exact 0; cand 0; review 161; BELEGT_IN, TYPISCH_BEI_MATERIAL, TYPISCH_BEI_ERA, ANCHORED_BY, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=s_holzschutzmittel; name=Holzschutzmittel; last_seen_by=agent10_phase4b_2; migration_origin=mig_qext_b_source_urls | needs review | 311 rels; exact 0; cand 0; review 155; BELEGT_IN, TYPISCH_BEI_MATERIAL, TYPISCH_BEI_ERA, ANCHORED_BY, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 5 | id=s_kmf; name=KMF — Künstliche Mineralfasern (alte Mineralwolle vor 1996/2000); last_seen_by=agent10_phase4b_2; standards_body=DE: TRGS 521 | needs review | 69 rels; exact 0; cand 0; review 34; BELEGT_IN, TYPISCH_BEI_MATERIAL, TYPISCH_BEI_ERA, ANCHORED_BY, CONCERNS | relationship fact or Claim if attribute-like |

### `Status` (9)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=status_geplant; name=Geplant; kind=lifecycle; migration_origin=mig_qext_b_source_urls | needs review | 45 rels; exact 0; cand 0; review 22; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_STATUS | relationship fact or Claim if attribute-like |
| 2 | id=status_in_bau; name=In_Bau; kind=lifecycle; migration_origin=mig_qext_b_source_urls | needs review | 19 rels; exact 0; cand 0; review 9; HAT_STATUS, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 3 | id=status_prototyp; name=Prototyp; kind=maturity; migration_origin=mig_qext_b_source_urls | needs review | 21 rels; exact 0; cand 0; review 10; HAT_STATUS, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=status_realisiert; name=Realisiert; kind=lifecycle; migration_origin=mig_qext_b_source_urls | needs review | 1163 rels; exact 0; cand 0; review 581; ANCHORED_BY, HAS_DATA_ISSUE, HAT_STATUS, CONCERNS | relationship fact or Claim if attribute-like |
| 5 | id=status_rueckgebaut; name=Rueckgebaut; kind=lifecycle; migration_origin=mig_qext_b_source_urls | needs review | 61 rels; exact 0; cand 0; review 30; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_STATUS | relationship fact or Claim if attribute-like |

### `Bauobjektklasse` (8)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=bok_depot_lager; name=Depot_Lager; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 33 rels; exact 0; cand 0; review 16; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_BAUOBJEKTKLASSE | relationship fact or Claim if attribute-like |
| 2 | id=bok_gebaeude; name=Gebaeude; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 323 rels; exact 0; cand 0; review 161; ANCHORED_BY, HAS_DATA_ISSUE, HAT_BAUOBJEKTKLASSE, CONCERNS | relationship fact or Claim if attribute-like |
| 3 | id=bok_gebaeudeteil; name=Gebaeudeteil; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 21 rels; exact 0; cand 0; review 10; HAT_BAUOBJEKTKLASSE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=bok_infrastruktur; name=Infrastruktur; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 41 rels; exact 0; cand 0; review 20; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_BAUOBJEKTKLASSE | relationship fact or Claim if attribute-like |
| 5 | id=bok_innenausbau; name=Innenausbau; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 15 rels; exact 0; cand 0; review 7; HAT_BAUOBJEKTKLASSE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `Tool` (8)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=tool_bim_bauteilkatalog; name=BIM / digitaler Bauteilkatalog; source_resolution_status=needs_source_url_review; kind=tool | needs review | 10 rels; exact 0; cand 0; review 4; NUTZT_SOFTWARE, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 2 | id=tool_bauteilkatalog; name=Bauteilkatalog / Bauteilpass; source_resolution_status=needs_source_url_review; kind=tool | needs review | 10 rels; exact 0; cand 0; review 4; NUTZT_SOFTWARE, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 3 | id=tool_hts_stockmatcher; name=HTS Reused Steel Stockmatcher; funktion=Abgleich von stock list und design list für wiederverwendete Stahlträger; kind=tool | candidate nearby | 8 rels; exact 0; cand 1; review 3; BELEGT_IN, NUTZT_SOFTWARE, CONCERNS, EXACT_MATCH_CANDIDATE | relationship fact or Claim if attribute-like |
| 4 | id=tool_material_passports_maconda; name=Material passports / Maconda data workflow; kind=tool; migration_origin= \| mig_r2_e_tool_secondary_label \| mig_qext_b_source_urls \| mig_qext_b_source_ur... | candidate nearby | 7 rels; exact 0; cand 1; review 3; BELEGT_IN, NUTZT_SOFTWARE, CONCERNS | relationship fact or Claim if attribute-like |
| 5 | id=tool_oogstkaart_harvest_map; name=Oogstkaart / Harvest Map logic; note=Materialsuche und Harvesting-Logik; konkrete Elementliste nicht vollständig öffe...; kind=tool | candidate nearby | 5 rels; exact 0; cand 1; review 2; BELEGT_IN, NUTZT_SOFTWARE, CONCERNS | relationship fact or Claim if attribute-like |

### `Zertifizierungssystem` (8)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=zbs_breeam; name=BREEAM; evidence_basis=controlled_vocab; migration_origin=mig_r2_d_restore_certifications \| mig_qext_b_source_urls \| mig_qext_c_primary_so... | needs review | 12 rels; exact 0; cand 0; review 5; HAT_ZERTIFIZIERUNG, BELEGT_IN, CONCERNS | relationship fact or Claim if attribute-like |
| 2 | id=zbs_dgnb; name=DGNB; evidence_basis=controlled_vocab; migration_origin=mig_r2_d_restore_certifications \| mig_qext_b_source_urls \| mig_qext_c_primary_so... | needs review | 6 rels; exact 0; cand 0; review 2; HAT_ZERTIFIZIERUNG, BELEGT_IN, CONCERNS | relationship fact or Claim if attribute-like |
| 3 | id=zbs_ecotool; name=EcoTool (ZBS); evidence_basis=controlled_vocab; migration_origin=mig_r2_d_restore_certifications \| mig_qext_b_source_urls | needs review | 4 rels; exact 0; cand 0; review 1; HAT_ZERTIFIZIERUNG, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=zbs_leed; name=LEED; evidence_basis=controlled_vocab; migration_origin=mig_r2_d_restore_certifications \| mig_qext_b_source_urls | needs review | 2 rels; exact 0; cand 0; review 0; CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 5 | id=zbs_nabers; name=NABERS; evidence_basis=controlled_vocab; migration_origin=mig_r2_d_restore_certifications \| mig_qext_b_source_urls \| mig_qext_c_primary_so... | needs review | 10 rels; exact 0; cand 0; review 4; HAT_ZERTIFIZIERUNG, BELEGT_IN, CONCERNS | relationship fact or Claim if attribute-like |

### `Akzeptanz` (7)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=ak_breeam_zertifizierung; name=BREEAM; scope_note=UK-basiertes Nachhaltigkeitszertifikat; Mat-Credits für Reuse.; name_full=BREEAM-Zertifizierung akzeptiert Reuse | needs review | 7 rels; exact 0; cand 0; review 3; GILT_IN_LAND, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 2 | id=ak_dgnb_zertifizierung; name=DGNB; scope_note=Deutsches Nachhaltigkeitszertifikat (DGNB) gewährt Bonuspunkte für Bauteilwieder...; name_full=DGNB-Zertifizierung akzeptiert Reuse | needs review | 9 rels; exact 0; cand 0; review 4; GILT_IN_LAND, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 3 | id=ak_humanitarian_purpose; name=Humanitärer Zweck; scope_note=Akzeptanztreiber: Projekt verfolgt explizit humanitäre oder sozialarbeiterische ...; name_full=Humanitärer/Sozialer Zweck — Akzeptanzgewinn durch Mission jenseits ökonomischer... | needs review | 3 rels; exact 0; cand 0; review 1; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=ak_leed_zertifizierung; name=LEED; scope_note=US-basiertes Nachhaltigkeitszertifikat; Materials & Resources credits für Reuse.; name_full=LEED-Zertifizierung akzeptiert Reuse | needs review | 7 rels; exact 0; cand 0; review 3; GILT_IN_LAND, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 5 | id=ak_aesthetik_patinakultur; name=Patina-Ästhetik; scope_note=Sichtbare Reuse-Ästhetik (Patina, Materialgeschichte) als gestalterischer Wert a...; name_full=Ästhetik-/Patinakultur akzeptiert | needs review | 3 rels; exact 0; cand 0; review 1; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `Bauobjektrolle` (6)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=bor_bestandsobjekt; name=Bestandsobjekt; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 47 rels; exact 0; cand 0; review 23; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_BAUOBJEKTROLLE | relationship fact or Claim if attribute-like |
| 2 | id=bor_donorobjekt; name=Donorobjekt; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 213 rels; exact 0; cand 0; review 106; ANCHORED_BY, HAS_DATA_ISSUE, HAT_BAUOBJEKTROLLE, CONCERNS | relationship fact or Claim if attribute-like |
| 3 | id=bor_empfaengerobjekt; name=Empfaengerobjekt; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 145 rels; exact 0; cand 0; review 72; ANCHORED_BY, HAS_DATA_ISSUE, HAT_BAUOBJEKTROLLE, CONCERNS | relationship fact or Claim if attribute-like |
| 4 | id=bor_referenzobjekt; name=Referenzobjekt; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 9 rels; exact 0; cand 0; review 4; HAT_BAUOBJEKTROLLE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 5 | id=bor_same_site_donor_receiver; name=Same_Site_Donor_Receiver; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 41 rels; exact 0; cand 0; review 20; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_BAUOBJEKTROLLE | relationship fact or Claim if attribute-like |

### `Bauteilebene` (6)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=be_bauteilgruppe; name=Bauteilgruppe; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 651 rels; exact 0; cand 0; review 325; ANCHORED_BY, HAS_DATA_ISSUE, HAT_BAUTEILEBENE, CONCERNS | relationship fact or Claim if attribute-like |
| 2 | id=be_einzelbauteil; name=Einzelbauteil; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 21 rels; exact 0; cand 0; review 10; HAT_BAUTEILEBENE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 3 | id=be_gebaeudeteil; name=Gebaeudeteil; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 5 rels; exact 0; cand 0; review 2; HAT_BAUTEILEBENE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=be_materialcharge; name=Materialcharge; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 15 rels; exact 0; cand 0; review 7; HAT_BAUTEILEBENE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 5 | id=be_oberflaechenschicht; name=Oberflaechenschicht; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 17 rels; exact 0; cand 0; review 8; HAT_BAUTEILEBENE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `Bauweise` (6)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=bauw_fertigteilbauweise; name=Fertigteilbauweise; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 65 rels; exact 0; cand 0; review 32; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_BAUWEISE | relationship fact or Claim if attribute-like |
| 2 | id=bauw_holzbauweise; name=Holzbauweise; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 57 rels; exact 0; cand 0; review 28; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_BAUWEISE | relationship fact or Claim if attribute-like |
| 3 | id=bauw_hybridbauweise; name=Hybridbauweise; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 49 rels; exact 0; cand 0; review 24; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_BAUWEISE | relationship fact or Claim if attribute-like |
| 4 | id=bauw_massivbauweise; name=Massivbauweise; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 47 rels; exact 0; cand 0; review 23; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_BAUWEISE | relationship fact or Claim if attribute-like |
| 5 | id=bauw_ortbetonbauweise; name=Ortbetonbauweise; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 5 rels; exact 0; cand 0; review 2; HAT_BAUWEISE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `BauwerkEra` (6)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=era_1900_1945; name=1900–1945; year_from=1900; notes=Industrialisation; reinforced concrete commercialised; PAK still high; some earl... | needs review | 9 rels; exact 0; cand 0; review 4; TYPISCH_BEI_ERA, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 2 | id=era_1970_1990; name=1970–1990; year_from=1970; notes=Still high asbestos / PCB / KMF; energy crisis drives insulation upgrades; first... | needs review | 17 rels; exact 0; cand 0; review 8; TYPISCH_BEI_ERA, ANCHORED_BY, BUILT_IN_ERA, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 3 | id=era_1990_2000; name=1990–2000; year_from=1990; notes=Country-specific asbestos bans (DE 1993, NL 1994, FR 1997, BE 1998, UK 2000); KM... | needs review | 9 rels; exact 0; cand 0; review 4; TYPISCH_BEI_ERA, ANCHORED_BY, BUILT_IN_ERA, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=era_nachkrieg_1945_1970; name=Nachkrieg 1945–1970; year_from=1945; notes=Wiederaufbau / Wirtschaftswunder. Highest asbestos use; PCB sealants begin; mine... | needs review | 17 rels; exact 0; cand 0; review 8; TYPISCH_BEI_ERA, ANCHORED_BY, BUILT_IN_ERA, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 5 | id=era_post_2000; name=nach 2000; year_from=2000; notes=Modern. Asbestos banned across EU/EEA; tight formaldehyde emission limits. | needs review | 5 rels; exact 0; cand 0; review 2; ANCHORED_BY, BUILT_IN_ERA, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `Funktionswechsel` (6)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=fw_dekorative_funktion; name=Dekorative_Funktion; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 3 rels; exact 0; cand 0; review 1; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 2 | id=fw_gleiche_funktion; name=Gleiche_Funktion; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 193 rels; exact 0; cand 0; review 96; ANCHORED_BY, HAS_DATA_ISSUE, HAT_FUNKTIONSWECHSEL, CONCERNS | relationship fact or Claim if attribute-like |
| 3 | id=fw_konstruktive_funktion; name=Konstruktive_Funktion; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 65 rels; exact 0; cand 0; review 32; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_FUNKTIONSWECHSEL | relationship fact or Claim if attribute-like |
| 4 | id=fw_neue_funktion; name=Neue_Funktion; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 315 rels; exact 0; cand 0; review 157; ANCHORED_BY, HAS_DATA_ISSUE, HAT_FUNKTIONSWECHSEL, CONCERNS | relationship fact or Claim if attribute-like |
| 5 | id=fw_technische_funktion; name=Technische_Funktion; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 29 rels; exact 0; cand 0; review 14; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_FUNKTIONSWECHSEL | relationship fact or Claim if attribute-like |

### `Layer` (6)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=layer_services; name=Services; evidence_source_id=q_brand_how_buildings_learn; evidence_basis=controlled_vocab | needs review | 3 rels; exact 0; cand 0; review 1; TEILT_LAYER, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 2 | id=layer_site; name=Site; evidence_source_id=q_brand_how_buildings_learn; evidence_basis=controlled_vocab | none visible | 1 rels; exact 0; cand 0; review 0; HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 3 | id=layer_skin; name=Skin; evidence_source_id=q_brand_how_buildings_learn; evidence_basis=controlled_vocab | needs review | 7 rels; exact 0; cand 0; review 3; TEILT_LAYER, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=layer_space_plan; name=Space Plan; evidence_source_id=q_brand_how_buildings_learn; evidence_basis=controlled_vocab | needs review | 11 rels; exact 0; cand 0; review 5; TEILT_LAYER, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 5 | id=layer_structure; name=Structure; evidence_source_id=q_brand_how_buildings_learn; evidence_basis=controlled_vocab | needs review | 13 rels; exact 0; cand 0; review 6; TEILT_LAYER, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `ZustandsKlasse` (6)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=zk_eingeschraenkt_nachbearbeitung; name=Eingeschränkt: Nacharbeit; scope_note=Wiederverwendbar nach Aufbereitung (Zuschnitt, Schliff, Beschichtung, Reinigung)...; name_full=Eingeschränkt, Nachbearbeitung nötig | needs review | 11 rels; exact 0; cand 0; review 5; TYPISCH_BEI_MATERIAL, HAT_ZUSTANDSKLASSE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 2 | id=zk_eingeschraenkt_nutzungsklasse_reduzieren; name=Eingeschränkt: downgrade; scope_note=Wiederverwendbar nur in geringerer Beanspruchungsklasse (downgrade, z.B. tragend...; name_full=Eingeschränkt, Nutzungsklasse reduzieren | needs review | 9 rels; exact 0; cand 0; review 4; TYPISCH_BEI_MATERIAL, HAT_ZUSTANDSKLASSE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 3 | id=zk_gebrauchsspuren_funktional; name=Gebraucht, funktional; scope_note=Sichtbare Patina/Verschleiß ohne funktionalen Einfluss; weiterhin im gleichen Nu...; name_full=Gebrauchsspuren, funktional unbeeinträchtigt | needs review | 39 rels; exact 0; cand 0; review 19; TYPISCH_BEI_MATERIAL, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_ZUSTANDSKLASSE | relationship fact or Claim if attribute-like |
| 4 | id=zk_neuwertig; name=Neuwertig; scope_note=Minimale Gebrauchsspuren; volle Wiederverwendungseignung in ursprünglicher Klass...; name_full=Neuwertig / wie neu | needs review | 37 rels; exact 0; cand 0; review 18; TYPISCH_BEI_MATERIAL, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_ZUSTANDSKLASSE | relationship fact or Claim if attribute-like |
| 5 | id=zk_nicht_wiederverwendbar; name=Nicht reusable; scope_note=Direkte Wiederverwendung nicht möglich; Pfad: stoffliches Recycling oder Entsorg...; name_full=Nicht wiederverwendbar (Recycling/Entsorgung) | needs review | 7 rels; exact 0; cand 0; review 3; TYPISCH_BEI_MATERIAL, HAT_ZUSTANDSKLASSE, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `LCAModule` (5)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=lz_a1_a3; name=A1-A3 Produkt; evidence_source_id=q_en_15978_lifecycle_modules; evidence_basis=controlled_vocab | needs review | 12 rels; exact 0; cand 0; review 5; METHODENGRUNDLAGE_NORM, BERECHNET_NACH_MODUL, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 2 | id=lz_a4_a5; name=A4-A5 Errichtung; evidence_source_id=q_en_15978_lifecycle_modules; evidence_basis=controlled_vocab | needs review | 6 rels; exact 0; cand 0; review 2; METHODENGRUNDLAGE_NORM, BERECHNET_NACH_MODUL, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 3 | id=lz_b; name=B1-B7 Nutzung; evidence_source_id=q_en_15978_lifecycle_modules; evidence_basis=controlled_vocab | needs review | 6 rels; exact 0; cand 0; review 2; METHODENGRUNDLAGE_NORM, BERECHNET_NACH_MODUL, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=lz_c; name=C1-C4 End-of-Life; evidence_source_id=q_en_15978_lifecycle_modules; evidence_basis=controlled_vocab | needs review | 4 rels; exact 0; cand 0; review 1; METHODENGRUNDLAGE_NORM, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 5 | id=lz_d; name=D Beyond (Reuse); evidence_source_id=q_en_15978_lifecycle_modules; evidence_basis=controlled_vocab | needs review | 14 rels; exact 0; cand 0; review 6; METHODENGRUNDLAGE_NORM, BERECHNET_NACH_MODUL, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |

### `Rueckbauverfahren` (5)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=rv_ausbau_von_bauteilen; name=Ausbau_von_Bauteilen; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 205 rels; exact 0; cand 0; review 102; ANCHORED_BY, HAS_DATA_ISSUE, HAT_RUECKBAUVERFAHREN, CONCERNS | relationship fact or Claim if attribute-like |
| 2 | id=rv_betonfraesen; name=Betonfraesen; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 11 rels; exact 0; cand 0; review 5; HAT_RUECKBAUVERFAHREN, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 3 | id=rv_demontage; name=Demontage; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 159 rels; exact 0; cand 0; review 79; ANCHORED_BY, HAS_DATA_ISSUE, HAT_RUECKBAUVERFAHREN, CONCERNS | relationship fact or Claim if attribute-like |
| 4 | id=rv_selektiver_rueckbau; name=Selektiver_Rueckbau; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 187 rels; exact 0; cand 0; review 93; ANCHORED_BY, HAS_DATA_ISSUE, HAT_RUECKBAUVERFAHREN, CONCERNS | relationship fact or Claim if attribute-like |
| 5 | id=rv_zerstoerungsarme_bergung; name=Zerstoerungsarme_Bergung; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 55 rels; exact 0; cand 0; review 27; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_RUECKBAUVERFAHREN | relationship fact or Claim if attribute-like |

### `Tragwerksprinzip` (4)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=tp_fachwerk; name=Fachwerk; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 5 rels; exact 0; cand 0; review 2; HAT_TRAGWERKSPRINZIP, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 2 | id=tp_skeletttragwerk; name=Skeletttragwerk; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 87 rels; exact 0; cand 0; review 43; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_TRAGWERKSPRINZIP | relationship fact or Claim if attribute-like |
| 3 | id=tp_wand_kern_tragwerk; name=Wand_Kern_Tragwerk; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 9 rels; exact 0; cand 0; review 4; HAT_TRAGWERKSPRINZIP, ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE | relationship fact or Claim if attribute-like |
| 4 | id=tp_wandtragwerk; name=Wandtragwerk; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed | needs review | 55 rels; exact 0; cand 0; review 27; ANCHORED_BY, CONCERNS, HAS_DATA_ISSUE, HAT_TRAGWERKSPRINZIP | relationship fact or Claim if attribute-like |

### `OntologyAnchor` (2)

| # | sample identity | state | adjacent rels | attach source how |
|---:|---|---|---|---|
| 1 | id=q_controlled_vocab_seed; name=Controlled-vocab seed; quelltyp=controlled_vocab_seed; name_full=Controlled vocabulary seed source — definitional taxonomy file (controlled_vocab... | needs review | 886 rels; exact 0; cand 0; review 443; ANCHORED_BY, CONCERNS | relationship fact or Claim if attribute-like |
| 2 | id=q_akteursliste_master_md; name=akteursliste_master.md; actor_registry_loader_seen=agent10; source_count=163 | exact nearby | 520 rels; exact 0; cand 260; review 260; ANCHORED_BY, CONCERNS | registry container only; source truth is the concrete row link |

