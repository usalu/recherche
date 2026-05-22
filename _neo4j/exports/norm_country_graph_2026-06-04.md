# Norm-Country Graph Export

- Exported: 2026-06-04 02:18:51
- Neo4j database: `mit-bestand`
- Output file: `_neo4j/exports/norm_country_graph_2026-06-04.md`
- Scope: all `:Norm` nodes, their direct `:GILT_IN_LAND` countries, and every relationship incident to each norm.

## Counts

| Metric | Count |
| --- | --- |
| Norm nodes | 103 |
| Incident relationships touching Norm | 387 |
| Norm -> Land direct GILT_IN_LAND | 142 |
| Projekt -> Norm REFERENZIERT_NORM | 26 |
| Bauteilgruppe -> Norm REFERENZIERT_NORM | 17 |
| ReuseRule -> Norm REFERENZIERT_NORM | 93 |

## Relationship Types Around Norms

| Relationship type | Count |
| --- | --- |
| REFERENZIERT_NORM | 150 |
| GILT_IN_LAND | 142 |
| BELEGT_IN | 72 |
| HAT_GELTUNGSBEREICH | 12 |
| METHODENGRUNDLAGE_NORM | 8 |
| HAT_BAUTEILTYP | 1 |
| HAT_LEISTUNGSANFORDERUNG | 1 |
| HAT_METHODE | 1 |

## Cypher Used

```cypher
// Graph view: norms + direct countries + all immediate neighbors
MATCH (n:Norm)
OPTIONAL MATCH countryPath = (n)-[:GILT_IN_LAND]->(:Land)
OPTIONAL MATCH connectedPath = (n)-[r]-(x)
RETURN countryPath, connectedPath;

// Country-aware context through projects, component groups, and reuse rules
MATCH path = (:Norm)-[:GILT_IN_LAND]->(:Land)
RETURN path
UNION
MATCH path = (:Land)<-[:LIEGT_IN_LAND]-(:Projekt)-[:REFERENZIERT_NORM]->(:Norm)
RETURN path
UNION
MATCH path = (:Land)<-[:LIEGT_IN_LAND]-(:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:REFERENZIERT_NORM]->(:Norm)
RETURN path
UNION
MATCH path = (:Land)<-[:APPLIES_IN]-(:ReuseRule)-[:REFERENZIERT_NORM]->(:Norm)
RETURN path;
```

## Country Summary By Norm

| Norm ID | Norm | Direct GILT_IN_LAND | ReuseRule countries | Project countries | BG project countries |
| --- | --- | --- | --- | --- | --- |
| norm_bs_4978 | BS 4978 |  | Vereinigtes Königreich |  |  |
| norm_bbl_nen | Bbl/NEN |  | Niederlande |  |  |
| norm_bbl_nen_links | Bbl/NEN links |  | Niederlande |  |  |
| norm_cb_23_passports | CB'23 passports |  | Niederlande |  |  |
| norm_cen_ts_1090_201 | CEN/TS 1090-201 |  | Belgien, Deutschland, Niederlande, Schweiz |  |  |
| norm_cen_ts_1090_201_2024 | CEN/TS 1090-201:2024 |  |  |  |  |
| norm_cen_ts_17440 | CEN/TS 17440 |  |  |  |  |
| norm_crow_cur_4_2023 | CROW-CUR 4:2023 | Niederlande |  |  | Finnland, Niederlande |
| norm_dibt_mvv_tb | DIBt/MVV TB |  | Deutschland |  |  |
| norm_din_18008 | DIN 18008 | Deutschland |  |  |  |
| norm_din_18940_family | DIN 18940 family |  | Deutschland |  |  |
| norm_din_18945 | DIN 18945 |  | Deutschland |  |  |
| norm_din_18946 | DIN 18946 |  | Deutschland |  |  |
| norm_din_18947 | DIN 18947 |  | Deutschland |  |  |
| norm_din_4074 | DIN 4074 | Deutschland | Deutschland |  |  |
| norm_din_68800 | DIN 68800 | Deutschland | Deutschland |  |  |
| norm_din_en_1090_2 | DIN EN 1090-2 |  | Deutschland |  |  |
| norm_din_en_1168 | DIN EN 1168 |  | Deutschland |  |  |
| norm_din_en_13369 | DIN EN 13369 |  | Deutschland |  |  |
| norm_din_en_14081 | DIN EN 14081 |  | Deutschland |  |  |
| norm_din_en_15804 | DIN EN 15804 |  |  | Dänemark, Norwegen, Schweiz, Vereinigtes Königreich |  |
| norm_din_en_15978 | DIN EN 15978 |  |  | Dänemark, Norwegen, Vereinigtes Königreich |  |
| norm_din_en_1993 | DIN EN 1993 |  | Deutschland |  |  |
| norm_din_en_1996 | DIN EN 1996 |  | Deutschland |  |  |
| norm_din_en_206 | DIN EN 206 |  | Deutschland |  |  |
| norm_din_en_338 | DIN EN 338 |  | Deutschland |  |  |
| norm_en_1090 | EN 1090 | Belgien, Deutschland, Dänemark, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Norwegen, Portugal, Schweiz, Vereinigtes Königreich, Österreich |  |  | Vereinigtes Königreich |
| norm_en_1090_2 | EN 1090-2 |  | Belgien, Vereinigtes Königreich |  |  |
| norm_en_1168 | EN 1168 | Belgien, Deutschland, Dänemark, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Norwegen, Portugal, Schweiz, Vereinigtes Königreich, Österreich | Belgien, Finnland, Niederlande, Norwegen |  | Finnland |
| norm_en_12058 | EN 12058 |  | Belgien |  |  |
| norm_en_12371 | EN 12371 |  | Belgien |  |  |
| norm_en_12372 | EN 12372 |  | Belgien |  |  |
| norm_en_13162 | EN 13162 | Belgien, Deutschland, Dänemark, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Norwegen, Portugal, Schweiz, Vereinigtes Königreich, Österreich |  |  |  |
| norm_en_13224 | EN 13224 |  | Belgien |  |  |
| norm_en_13369 | EN 13369 |  | Belgien, Niederlande |  |  |
| norm_en_1341 | EN 1341 |  | Belgien |  |  |
| norm_en_13747 | EN 13747 |  | Belgien |  |  |
| norm_en_13755 | EN 13755 |  | Belgien |  |  |
| norm_en_14081 | EN 14081 | Belgien, Deutschland, Dänemark, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Norwegen, Portugal, Schweiz, Vereinigtes Königreich, Österreich | Vereinigtes Königreich |  |  |
| norm_en_14231 | EN 14231 |  | Belgien |  |  |
| norm_en_1469 | EN 1469 |  | Belgien |  |  |
| norm_en_1936 | EN 1936 |  | Belgien |  |  |
| norm_en_1992 | EN 1992 (Eurocode 2) | Belgien, Deutschland, Dänemark, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Norwegen, Portugal, Schweiz, Vereinigtes Königreich, Österreich |  |  |  |
| norm_en_1993 | EN 1993 (Eurocode 3) | Belgien, Deutschland, Dänemark, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Norwegen, Portugal, Schweiz, Vereinigtes Königreich, Österreich |  |  |  |
| norm_en_1995 | EN 1995 (Eurocode 5) | Belgien, Deutschland, Dänemark, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Norwegen, Portugal, Schweiz, Vereinigtes Königreich, Österreich |  |  |  |
| norm_en_1996 | EN 1996 (Eurocode 6) | Belgien, Deutschland, Dänemark, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Norwegen, Portugal, Schweiz, Vereinigtes Königreich, Österreich |  |  |  |
| norm_en_206 | EN 206 | Belgien, Deutschland, Dänemark, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Norwegen, Portugal, Schweiz, Vereinigtes Königreich, Österreich | Belgien, Niederlande |  |  |
| norm_en_338 | EN 338 |  | Vereinigtes Königreich |  |  |
| norm_en_771 | EN 771 | Belgien, Deutschland, Dänemark, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Norwegen, Portugal, Schweiz, Vereinigtes Königreich, Österreich |  |  |  |
| norm_en_771_1 | EN 771-1 |  | Deutschland |  |  |
| norm_en_772 | EN 772 |  | Deutschland |  |  |
| norm_en_998 | EN 998 |  | Deutschland |  |  |
| norm_en_sia_product_references | EN/SIA product references |  | Schweiz |  |  |
| norm_en_sn_12058 | EN/SN 12058 |  | Schweiz |  |  |
| norm_en_sn_1469 | EN/SN 1469 |  | Schweiz |  |  |
| norm_eurocode_2 | Eurocode 2 |  | Belgien, Deutschland, Finnland, Niederlande, Norwegen |  |  |
| norm_eurocode_3 | Eurocode 3 |  | Belgien, Niederlande, Vereinigtes Königreich |  |  |
| norm_eurocode_5 | Eurocode 5 |  | Belgien, Deutschland, Niederlande |  |  |
| norm_eurocode_5_uk_na | Eurocode 5 / UK NA |  | Vereinigtes Königreich |  |  |
| norm_eurocode_6 | Eurocode 6 |  | Deutschland |  |  |
| norm_eurocode_adjacent_structural_verification | Eurocode-adjacent structural verification |  | Deutschland |  |  |
| norm_eurocode_related_timber_product_standards | Eurocode-related timber product standards |  | Schweiz |  |  |
| norm_finnish_national_annexes | Finnish national annexes |  | Finnland |  |  |
| norm_fire_durability_rules | Fire/durability rules |  | Belgien |  |  |
| norm_fire_moisture_rules | Fire/moisture rules |  | Deutschland, Vereinigtes Königreich |  |  |
| norm_fire_moisture_durability_requirements | Fire/moisture/durability requirements |  | Schweiz |  |  |
| norm_frost_rules | Frost rules |  | Deutschland |  |  |
| norm_historic_sections_book | Historic Sections Book | Vereinigtes Königreich |  | Vereinigtes Königreich | Vereinigtes Königreich |
| norm_iso_14040 | ISO 14040 |  |  | Schweiz, Vereinigtes Königreich |  |
| norm_iso_14044 | ISO 14044 |  |  | Schweiz, Vereinigtes Königreich |  |
| norm_iso_20887 | ISO 20887 |  |  |  |  |
| norm_mvv_tb_dibt_pathway | MVV TB/DIBt pathway |  | Deutschland |  |  |
| norm_nbn_en_14081 | NBN EN 14081 |  | Belgien |  |  |
| norm_nbn_en_338 | NBN EN 338 |  | Belgien |  |  |
| norm_nbn_national_annexes | NBN national annexes |  | Belgien |  |  |
| norm_nen_8700 | NEN 8700 | Niederlande |  |  |  |
| norm_nen_en_1090_2 | NEN EN 1090-2 |  | Niederlande |  |  |
| norm_nen_en_14081 | NEN EN 14081 |  | Niederlande |  |  |
| norm_nen_en_338 | NEN EN 338 |  | Niederlande |  |  |
| norm_nen_fire_moisture_rules | NEN fire/moisture rules |  | Niederlande |  |  |
| norm_ns_3682 | NS 3682 | Norwegen |  |  | Norwegen |
| norm_ns_3682_2022 | NS 3682:2022 |  | Norwegen |  |  |
| norm_pd_cen_ts_1090_201 | PD CEN/TS 1090-201 |  | Vereinigtes Königreich |  |  |
| norm_rt_2012 | RT 2012 | Frankreich |  | Frankreich |  |
| norm_recreate_qa_procedure | ReCreate QA procedure |  | Finnland |  |  |
| norm_sci_p427 | SCI P427 protocol | Vereinigtes Königreich |  | Vereinigtes Königreich | Vereinigtes Königreich |
| norm_sci_p440 | SCI P440 | Vereinigtes Königreich |  |  | Vereinigtes Königreich |
| norm_sci_protocol | SCI protocol |  | Vereinigtes Königreich |  |  |
| norm_sia_schweiz | SIA (CH) | Schweiz |  |  | Schweiz |
| norm_sia_261 | SIA 261 |  |  | Schweiz |  |
| norm_sia_262 | SIA 262 |  | Schweiz |  |  |
| norm_sia_263 | SIA 263 |  | Schweiz |  |  |
| norm_sia_265 | SIA 265 |  | Schweiz |  |  |
| norm_sia_269 | SIA 269 |  | Schweiz | Schweiz |  |
| norm_sia_380_1 | SIA 380/1 |  |  | Schweiz |  |
| norm_sia_416 | SIA 416 |  |  | Schweiz |  |
| norm_sia_500 | SIA 500 |  |  | Schweiz |  |
| norm_sia_facade_anchorage_rules | SIA façade/anchorage rules |  | Schweiz |  |  |
| norm_sia_fire_durability_rules | SIA fire/durability rules |  | Schweiz |  |  |
| norm_swiss_baupg | Swiss BauPG |  | Schweiz |  |  |
| norm_tek_norway | TEK (NO) | Norwegen |  |  | Norwegen |
| norm_tek17 | TEK17 |  | Norwegen |  |  |
| norm_ukca_ce_interface | UKCA/CE interface |  | Vereinigtes Königreich |  |  |

## Full Incident Edge List

| Source ID | Source labels | Source name | Rel type | Target ID | Target labels | Target name | Rel properties |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bg_stahl_mehrere_juch_hagenholz_stahlstruktur | Bauteilgruppe | 1:1 versetzte Stahlstruk… | REFERENZIERT_NORM | norm_sia_schweiz | Norm | SIA (CH) | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahl_mehrere_juch_hagenholz_stahlstruktur__REFERENZIERT_NORM__norm_sia_schweiz"} |
| bg_stahlbeton_mehrere_lokomotion_hollow_core_slabs | Bauteilgruppe | 27 wiederve… (Lokomotion) | REFERENZIERT_NORM | norm_crow_cur_4_2023 | Norm | CROW-CUR 4:2023 | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahlbeton_mehrere_lokomotion_hollow_core_slabs__REFERENZIERT_NORM__norm_crow_cur_4_2023"} |
| bg_stahlbeton_mehrere_lokomotion_hollow_core_slabs | Bauteilgruppe | 27 wiederve… (Lokomotion) | REFERENZIERT_NORM | norm_en_1168 | Norm | EN 1168 | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahlbeton_mehrere_lokomotion_hollow_core_slabs__REFERENZIERT_NORM__norm_en_1168"} |
| p_55_great_suffolk_street_london | Projekt | 55 Great Suffolk Street | REFERENZIERT_NORM | norm_din_en_15804 | Norm | DIN EN 15804 | {"evidence_confidence": "teilweise_belegt", "id": "r_p_55_great_suffolk_street_london__REFERENZIERT_NORM__norm_din_en_15804"} |
| p_55_great_suffolk_street_london | Projekt | 55 Great Suffolk Street | REFERENZIERT_NORM | norm_din_en_15978 | Norm | DIN EN 15978 | {"evidence_confidence": "teilweise_belegt", "id": "r_p_55_great_suffolk_street_london__REFERENZIERT_NORM__norm_din_en_15978"} |
| p_55_great_suffolk_street_london | Projekt | 55 Great Suffolk Street | REFERENZIERT_NORM | norm_iso_14040 | Norm | ISO 14040 | {"evidence_confidence": "teilweise_belegt", "id": "r_p_55_great_suffolk_street_london__REFERENZIERT_NORM__norm_iso_14040"} |
| p_55_great_suffolk_street_london | Projekt | 55 Great Suffolk Street | REFERENZIERT_NORM | norm_iso_14044 | Norm | ISO 14044 | {"evidence_confidence": "teilweise_belegt", "id": "r_p_55_great_suffolk_street_london__REFERENZIERT_NORM__norm_iso_14044"} |
| lz_a1_a3 | LCAModule | A1-A3 Produkt | METHODENGRUNDLAGE_NORM | norm_din_en_15804 | Norm | DIN EN 15804 | {"evidence_confidence": "unklar", "id": "r_lz_a1_a3__METHODENGRUNDLAGE_NORM__norm_din_en_15804"} |
| lz_a1_a3 | LCAModule | A1-A3 Produkt | METHODENGRUNDLAGE_NORM | norm_iso_14040 | Norm | ISO 14040 | {"evidence_confidence": "unklar", "id": "r_lz_a1_a3__METHODENGRUNDLAGE_NORM__norm_iso_14040"} |
| lz_a1_a3 | LCAModule | A1-A3 Produkt | METHODENGRUNDLAGE_NORM | norm_iso_14044 | Norm | ISO 14044 | {"evidence_confidence": "unklar", "id": "r_lz_a1_a3__METHODENGRUNDLAGE_NORM__norm_iso_14044"} |
| lz_a4_a5 | LCAModule | A4-A5 Errichtung | METHODENGRUNDLAGE_NORM | norm_din_en_15978 | Norm | DIN EN 15978 | {"evidence_confidence": "unklar", "id": "r_lz_a4_a5__METHODENGRUNDLAGE_NORM__norm_din_en_15978"} |
| lz_b | LCAModule | B1-B7 Nutzung | METHODENGRUNDLAGE_NORM | norm_din_en_15978 | Norm | DIN EN 15978 | {"evidence_confidence": "unklar", "id": "r_lz_b__METHODENGRUNDLAGE_NORM__norm_din_en_15978"} |
| norm_bs_4978 | Norm | BS 4978 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_bs_4978__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_bbl_nen | Norm | Bbl/NEN | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_bbl_nen__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_bbl_nen_links | Norm | Bbl/NEN links | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_bbl_nen_links__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| p_bedzed_london_hackbridge | Projekt | BedZED | REFERENZIERT_NORM | norm_historic_sections_book | Norm | Historic Sections Book | {"evidence_confidence": "unklar", "id": "r_p_bedzed_london_hackbridge__REFERENZIERT_NORM__norm_historic_sections_book"} |
| rr_be_beton | ReuseRule | Belgien × Beton reuse rule | REFERENZIERT_NORM | norm_en_1168 | Norm | EN 1168 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_beton__REFERENZIERT_NORM__norm_en_1168"} |
| rr_be_beton | ReuseRule | Belgien × Beton reuse rule | REFERENZIERT_NORM | norm_en_13224 | Norm | EN 13224 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_beton__REFERENZIERT_NORM__norm_en_13224"} |
| rr_be_beton | ReuseRule | Belgien × Beton reuse rule | REFERENZIERT_NORM | norm_en_13369 | Norm | EN 13369 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_beton__REFERENZIERT_NORM__norm_en_13369"} |
| rr_be_beton | ReuseRule | Belgien × Beton reuse rule | REFERENZIERT_NORM | norm_en_13747 | Norm | EN 13747 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_beton__REFERENZIERT_NORM__norm_en_13747"} |
| rr_be_beton | ReuseRule | Belgien × Beton reuse rule | REFERENZIERT_NORM | norm_en_206 | Norm | EN 206 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_beton__REFERENZIERT_NORM__norm_en_206"} |
| rr_be_beton | ReuseRule | Belgien × Beton reuse rule | REFERENZIERT_NORM | norm_eurocode_2 | Norm | Eurocode 2 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_beton__REFERENZIERT_NORM__norm_eurocode_2"} |
| rr_be_holz | ReuseRule | Belgien × Holz reuse rule | REFERENZIERT_NORM | norm_eurocode_5 | Norm | Eurocode 5 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_holz__REFERENZIERT_NORM__norm_eurocode_5"} |
| rr_be_holz | ReuseRule | Belgien × Holz reuse rule | REFERENZIERT_NORM | norm_fire_durability_rules | Norm | Fire/durability rules | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_holz__REFERENZIERT_NORM__norm_fire_durability_rules"} |
| rr_be_holz | ReuseRule | Belgien × Holz reuse rule | REFERENZIERT_NORM | norm_nbn_en_14081 | Norm | NBN EN 14081 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_holz__REFERENZIERT_NORM__norm_nbn_en_14081"} |
| rr_be_holz | ReuseRule | Belgien × Holz reuse rule | REFERENZIERT_NORM | norm_nbn_en_338 | Norm | NBN EN 338 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_holz__REFERENZIERT_NORM__norm_nbn_en_338"} |
| rr_be_naturstein | ReuseRule | Belgien × Naturstein reuse rule | REFERENZIERT_NORM | norm_en_12058 | Norm | EN 12058 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_naturstein__REFERENZIERT_NORM__norm_en_12058"} |
| rr_be_naturstein | ReuseRule | Belgien × Naturstein reuse rule | REFERENZIERT_NORM | norm_en_12371 | Norm | EN 12371 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_naturstein__REFERENZIERT_NORM__norm_en_12371"} |
| rr_be_naturstein | ReuseRule | Belgien × Naturstein reuse rule | REFERENZIERT_NORM | norm_en_12372 | Norm | EN 12372 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_naturstein__REFERENZIERT_NORM__norm_en_12372"} |
| rr_be_naturstein | ReuseRule | Belgien × Naturstein reuse rule | REFERENZIERT_NORM | norm_en_1341 | Norm | EN 1341 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_naturstein__REFERENZIERT_NORM__norm_en_1341"} |
| rr_be_naturstein | ReuseRule | Belgien × Naturstein reuse rule | REFERENZIERT_NORM | norm_en_13755 | Norm | EN 13755 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_naturstein__REFERENZIERT_NORM__norm_en_13755"} |
| rr_be_naturstein | ReuseRule | Belgien × Naturstein reuse rule | REFERENZIERT_NORM | norm_en_14231 | Norm | EN 14231 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_naturstein__REFERENZIERT_NORM__norm_en_14231"} |
| rr_be_naturstein | ReuseRule | Belgien × Naturstein reuse rule | REFERENZIERT_NORM | norm_en_1469 | Norm | EN 1469 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_naturstein__REFERENZIERT_NORM__norm_en_1469"} |
| rr_be_naturstein | ReuseRule | Belgien × Naturstein reuse rule | REFERENZIERT_NORM | norm_en_1936 | Norm | EN 1936 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_naturstein__REFERENZIERT_NORM__norm_en_1936"} |
| rr_be_stahl | ReuseRule | Belgien × Stahl reuse rule | REFERENZIERT_NORM | norm_cen_ts_1090_201 | Norm | CEN/TS 1090-201 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_stahl__REFERENZIERT_NORM__norm_cen_ts_1090_201"} |
| rr_be_stahl | ReuseRule | Belgien × Stahl reuse rule | REFERENZIERT_NORM | norm_en_1090_2 | Norm | EN 1090-2 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_stahl__REFERENZIERT_NORM__norm_en_1090_2"} |
| rr_be_stahl | ReuseRule | Belgien × Stahl reuse rule | REFERENZIERT_NORM | norm_eurocode_3 | Norm | Eurocode 3 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_stahl__REFERENZIERT_NORM__norm_eurocode_3"} |
| rr_be_stahl | ReuseRule | Belgien × Stahl reuse rule | REFERENZIERT_NORM | norm_nbn_national_annexes | Norm | NBN national annexes | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_stahl__REFERENZIERT_NORM__norm_nbn_national_annexes"} |
| bg_stahlbeton_mehrere_juch_schellinghalle_pilzstuetzen | Bauteilgruppe | Beton-Pilzstützen und… | REFERENZIERT_NORM | norm_sia_schweiz | Norm | SIA (CH) | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahlbeton_mehrere_juch_schellinghalle_pilzstuetzen__REFERENZIERT_NORM__norm_sia_schweiz"} |
| bg_beton_mehrere_juch_kerenzerberg_betonplatten | Bauteilgruppe | Betonplatten aus dem… | REFERENZIERT_NORM | norm_sia_schweiz | Norm | SIA (CH) | {"evidence_confidence": "unklar", "id": "r_bg_reuse_beton_mehrere_juch_kerenzerberg_betonplatten__REFERENZIERT_NORM__norm_sia_schweiz"} |
| p_brent_cross_town_primary_substation_london | Projekt | Brent Cross Town… | REFERENZIERT_NORM | norm_din_en_15804 | Norm | DIN EN 15804 | {"evidence_confidence": "teilweise_belegt", "id": "r_p_brent_cross_town_primary_substation_london__REFERENZIERT_NORM__norm_din_en_15804"} |
| p_brent_cross_town_primary_substation_london | Projekt | Brent Cross Town… | REFERENZIERT_NORM | norm_din_en_15978 | Norm | DIN EN 15978 | {"evidence_confidence": "teilweise_belegt", "id": "r_p_brent_cross_town_primary_substation_london__REFERENZIERT_NORM__norm_din_en_15978"} |
| p_brent_cross_town_primary_substation_london | Projekt | Brent Cross Town… | REFERENZIERT_NORM | norm_sci_p427 | Norm | SCI P427 protocol | {"evidence_confidence": "unklar", "id": "r_p_brent_cross_town_primary_substation_london__REFERENZIERT_NORM__norm_sci_p427"} |
| bg_mehrere_mehrere_ka13_office_fronts_doors_facade | Bauteilgruppe | Bürofronten | REFERENZIERT_NORM | norm_tek_norway | Norm | TEK (NO) | {"evidence_confidence": "unklar", "id": "r_bg_reuse_mehrere_mehrere_ka13_office_fronts_doors_facade__REFERENZIERT_NORM__norm_tek_norway"} |
| lz_c | LCAModule | C1-C4 End-of-Life | METHODENGRUNDLAGE_NORM | norm_din_en_15978 | Norm | DIN EN 15978 | {"evidence_confidence": "unklar", "id": "r_lz_c__METHODENGRUNDLAGE_NORM__norm_din_en_15978"} |
| norm_cb_23_passports | Norm | CB'23 passports | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_cb_23_passports__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_cen_ts_1090_201 | Norm | CEN/TS 1090-201 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_cen_ts_1090_201__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_cen_ts_1090_201_2024 | Norm | CEN/TS 1090-201:2024 | HAT_GELTUNGSBEREICH | geltungsbereich_cen_ts_europaeisch | Geltungsbereich | CEN Technical Specification europaeischer Deliverable-Raum | {"evidence_confidence": "teilweise_belegt", "id": "norm_cen_ts_1090_201_2024__HAT_GELTUNGSBEREICH__geltungsbereich_cen_ts_europaeisch"} |
| norm_cen_ts_17440 | Norm | CEN/TS 17440 | HAT_GELTUNGSBEREICH | geltungsbereich_cen_ts_europaeisch | Geltungsbereich | CEN Technical Specification europaeischer Deliverable-Raum | {"evidence_confidence": "teilweise_belegt", "id": "norm_cen_ts_17440__HAT_GELTUNGSBEREICH__geltungsbereich_cen_ts_europaeisch"} |
| norm_crow_cur_4_2023 | Norm | CROW-CUR 4:2023 | GILT_IN_LAND | land_niederlande | Land | Niederlande | {"evidence_confidence": "unklar", "id": "r_norm_crow_cur_4_2023__GILT_IN_LAND__land_niederlande"} |
| norm_crow_cur_4_2023 | Norm | CROW-CUR 4:2023 | HAT_BAUTEILTYP | bt_decke | Bauteiltyp | Decke | {"evidence_confidence": "unklar", "id": "r_norm_crow_cur_4_2023__HAT_BAUTEILTYP__bt_decke"} |
| norm_crow_cur_4_2023 | Norm | CROW-CUR 4:2023 | HAT_LEISTUNGSANFORDERUNG | la_tragfaehigkeit | Leistungsanforderung | Tragfaehigkeit | {"evidence_confidence": "unklar", "id": "r_norm_crow_cur_4_2023__HAT_LEISTUNGSANFORDERUNG__la_tragfaehigkeit"} |
| norm_crow_cur_4_2023 | Norm | CROW-CUR 4:2023 | HAT_METHODE | meth_bestands_und_reuse_assessment | Methode | Bestands_und_ReUse_Assessment | {"evidence_confidence": "unklar", "legacy_methode_id": "meth_reuse_assessment", "legacy_methode_name": "ReUse_Assessment", "legacy_rel_id": "r_norm_crow_cur_4_2023__HAT_METHODE__meth_reuse_assessment", "migrated_at": "2026-06-03T23:47:06.160000000+00:00", "review_run": "taxonomy_integration_2026_06_03_phase6_1"} |
| norm_crow_cur_4_2023 | Norm | CROW-CUR 4:2023 | REFERENZIERT_NORM | norm_en_1168 | Norm | EN 1168 | {"evidence_confidence": "unklar", "id": "r_norm_crow_cur_4_2023__REFERENZIERT_NORM__norm_en_1168"} |
| norm_crow_cur_4_2023 | Norm | CROW-CUR 4:2023 | REFERENZIERT_NORM | norm_en_1168 | Norm | EN 1168 | {"evidence_confidence": "unklar", "id": "r_norm_crow_cur_4_2023__REFERENZIERT_NORM__norm_en_1168"} |
| lz_d | LCAModule | D Beyond (Reuse) | METHODENGRUNDLAGE_NORM | norm_din_en_15804 | Norm | DIN EN 15804 | {"evidence_confidence": "unklar", "id": "r_lz_d__METHODENGRUNDLAGE_NORM__norm_din_en_15804"} |
| lz_d | LCAModule | D Beyond (Reuse) | METHODENGRUNDLAGE_NORM | norm_din_en_15978 | Norm | DIN EN 15978 | {"evidence_confidence": "unklar", "id": "r_lz_d__METHODENGRUNDLAGE_NORM__norm_din_en_15978"} |
| norm_dibt_mvv_tb | Norm | DIBt/MVV TB | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_dibt_mvv_tb__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_din_18008 | Norm | DIN 18008 | GILT_IN_LAND | land_deutschland | Land | Deutschland | {"evidence_confidence": "unklar", "id": "r_norm_din_18008__GILT_IN_LAND__land_deutschland"} |
| norm_din_18940_family | Norm | DIN 18940 family | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_18940_family__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_din_18945 | Norm | DIN 18945 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_18945__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_din_18946 | Norm | DIN 18946 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_18946__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_din_18947 | Norm | DIN 18947 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_18947__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_din_4074 | Norm | DIN 4074 | GILT_IN_LAND | land_deutschland | Land | Deutschland | {"evidence_confidence": "unklar", "id": "r_norm_din_4074__GILT_IN_LAND__land_deutschland"} |
| norm_din_68800 | Norm | DIN 68800 | GILT_IN_LAND | land_deutschland | Land | Deutschland | {"evidence_confidence": "unklar", "id": "r_norm_din_68800__GILT_IN_LAND__land_deutschland"} |
| norm_din_en_1090_2 | Norm | DIN EN 1090-2 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_en_1090_2__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_din_en_1168 | Norm | DIN EN 1168 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_en_1168__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_din_en_13369 | Norm | DIN EN 13369 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_en_13369__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_din_en_14081 | Norm | DIN EN 14081 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_en_14081__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_din_en_1993 | Norm | DIN EN 1993 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_en_1993__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_din_en_1996 | Norm | DIN EN 1996 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_en_1996__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_din_en_206 | Norm | DIN EN 206 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_en_206__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_din_en_338 | Norm | DIN EN 338 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_en_338__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| rr_de_beton | ReuseRule | Deutschland × Beton reuse rule | REFERENZIERT_NORM | norm_dibt_mvv_tb | Norm | DIBt/MVV TB | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_beton__REFERENZIERT_NORM__norm_dibt_mvv_tb"} |
| rr_de_beton | ReuseRule | Deutschland × Beton reuse rule | REFERENZIERT_NORM | norm_din_en_1168 | Norm | DIN EN 1168 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_beton__REFERENZIERT_NORM__norm_din_en_1168"} |
| rr_de_beton | ReuseRule | Deutschland × Beton reuse rule | REFERENZIERT_NORM | norm_din_en_13369 | Norm | DIN EN 13369 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_beton__REFERENZIERT_NORM__norm_din_en_13369"} |
| rr_de_beton | ReuseRule | Deutschland × Beton reuse rule | REFERENZIERT_NORM | norm_din_en_206 | Norm | DIN EN 206 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_beton__REFERENZIERT_NORM__norm_din_en_206"} |
| rr_de_beton | ReuseRule | Deutschland × Beton reuse rule | REFERENZIERT_NORM | norm_eurocode_2 | Norm | Eurocode 2 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_beton__REFERENZIERT_NORM__norm_eurocode_2"} |
| rr_de_holz | ReuseRule | Deutschland × Holz reuse rule | REFERENZIERT_NORM | norm_din_4074 | Norm | DIN 4074 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_holz__REFERENZIERT_NORM__norm_din_4074"} |
| rr_de_holz | ReuseRule | Deutschland × Holz reuse rule | REFERENZIERT_NORM | norm_din_68800 | Norm | DIN 68800 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_holz__REFERENZIERT_NORM__norm_din_68800"} |
| rr_de_holz | ReuseRule | Deutschland × Holz reuse rule | REFERENZIERT_NORM | norm_din_en_14081 | Norm | DIN EN 14081 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_holz__REFERENZIERT_NORM__norm_din_en_14081"} |
| rr_de_holz | ReuseRule | Deutschland × Holz reuse rule | REFERENZIERT_NORM | norm_din_en_338 | Norm | DIN EN 338 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_holz__REFERENZIERT_NORM__norm_din_en_338"} |
| rr_de_holz | ReuseRule | Deutschland × Holz reuse rule | REFERENZIERT_NORM | norm_eurocode_5 | Norm | Eurocode 5 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_holz__REFERENZIERT_NORM__norm_eurocode_5"} |
| rr_de_lehm | ReuseRule | Deutschland × Lehm reuse rule | REFERENZIERT_NORM | norm_din_18940_family | Norm | DIN 18940 family | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_lehm__REFERENZIERT_NORM__norm_din_18940"} |
| rr_de_lehm | ReuseRule | Deutschland × Lehm reuse rule | REFERENZIERT_NORM | norm_din_18945 | Norm | DIN 18945 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_lehm__REFERENZIERT_NORM__norm_din_18945"} |
| rr_de_lehm | ReuseRule | Deutschland × Lehm reuse rule | REFERENZIERT_NORM | norm_din_18946 | Norm | DIN 18946 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_lehm__REFERENZIERT_NORM__norm_din_18946"} |
| rr_de_lehm | ReuseRule | Deutschland × Lehm reuse rule | REFERENZIERT_NORM | norm_din_18947 | Norm | DIN 18947 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_lehm__REFERENZIERT_NORM__norm_din_18947"} |
| rr_de_lehm | ReuseRule | Deutschland × Lehm reuse rule | REFERENZIERT_NORM | norm_eurocode_adjacent_structural_verification | Norm | Eurocode-adjacent structural verification | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_lehm__REFERENZIERT_NORM__norm_eurocode_adjacent_structural_verification"} |
| rr_de_lehm | ReuseRule | Deutschland × Lehm reuse rule | REFERENZIERT_NORM | norm_fire_moisture_rules | Norm | Fire/moisture rules | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_lehm__REFERENZIERT_NORM__norm_fire_moisture_rules"} |
| rr_de_stahl | ReuseRule | Deutschland × Stahl reuse rule | REFERENZIERT_NORM | norm_cen_ts_1090_201 | Norm | CEN/TS 1090-201 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_stahl__REFERENZIERT_NORM__norm_cen_ts_1090_201"} |
| rr_de_stahl | ReuseRule | Deutschland × Stahl reuse rule | REFERENZIERT_NORM | norm_din_en_1090_2 | Norm | DIN EN 1090-2 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_stahl__REFERENZIERT_NORM__norm_din_en_1090_2"} |
| rr_de_stahl | ReuseRule | Deutschland × Stahl reuse rule | REFERENZIERT_NORM | norm_din_en_1993 | Norm | DIN EN 1993 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_stahl__REFERENZIERT_NORM__norm_din_en_1993"} |
| rr_de_stahl | ReuseRule | Deutschland × Stahl reuse rule | REFERENZIERT_NORM | norm_mvv_tb_dibt_pathway | Norm | MVV TB/DIBt pathway | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_stahl__REFERENZIERT_NORM__norm_mvv_tb_dibt_pathway"} |
| rr_de_ziegel | ReuseRule | Deutschland × Ziegel reuse rule | REFERENZIERT_NORM | norm_din_en_1996 | Norm | DIN EN 1996 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_ziegel__REFERENZIERT_NORM__norm_din_en_1996"} |
| rr_de_ziegel | ReuseRule | Deutschland × Ziegel reuse rule | REFERENZIERT_NORM | norm_en_771_1 | Norm | EN 771-1 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_ziegel__REFERENZIERT_NORM__norm_en_771_1"} |
| rr_de_ziegel | ReuseRule | Deutschland × Ziegel reuse rule | REFERENZIERT_NORM | norm_en_772 | Norm | EN 772 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_ziegel__REFERENZIERT_NORM__norm_en_772"} |
| rr_de_ziegel | ReuseRule | Deutschland × Ziegel reuse rule | REFERENZIERT_NORM | norm_en_998 | Norm | EN 998 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_ziegel__REFERENZIERT_NORM__norm_en_998"} |
| rr_de_ziegel | ReuseRule | Deutschland × Ziegel reuse rule | REFERENZIERT_NORM | norm_eurocode_6 | Norm | Eurocode 6 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_ziegel__REFERENZIERT_NORM__norm_eurocode_6"} |
| rr_de_ziegel | ReuseRule | Deutschland × Ziegel reuse rule | REFERENZIERT_NORM | norm_frost_rules | Norm | Frost rules | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_ziegel__REFERENZIERT_NORM__norm_frost_rules"} |
| p_elementa_walkeweg | Projekt | ELEMENTA Walkeweg | REFERENZIERT_NORM | norm_sia_269 | Norm | SIA 269 | {"evidence_confidence": "unklar", "id": "r_p_elementa_walkeweg__REFERENZIERT_NORM__norm_sia_269"} |
| p_elementa_walkeweg | Projekt | ELEMENTA Walkeweg | REFERENZIERT_NORM | norm_sia_380_1 | Norm | SIA 380/1 | {"evidence_confidence": "unklar", "id": "r_p_elementa_walkeweg__REFERENZIERT_NORM__norm_sia_380_1"} |
| norm_en_1090 | Norm | EN 1090 | GILT_IN_LAND | land_belgien | Land | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_belgien"} |
| norm_en_1090 | Norm | EN 1090 | GILT_IN_LAND | land_deutschland | Land | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_deutschland"} |
| norm_en_1090 | Norm | EN 1090 | GILT_IN_LAND | land_daenemark | Land | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_daenemark"} |
| norm_en_1090 | Norm | EN 1090 | GILT_IN_LAND | land_finnland | Land | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_finnland"} |
| norm_en_1090 | Norm | EN 1090 | GILT_IN_LAND | land_frankreich | Land | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_frankreich"} |
| norm_en_1090 | Norm | EN 1090 | GILT_IN_LAND | land_italien | Land | Italien | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_italien"} |
| norm_en_1090 | Norm | EN 1090 | GILT_IN_LAND | land_luxemburg | Land | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_luxemburg"} |
| norm_en_1090 | Norm | EN 1090 | GILT_IN_LAND | land_niederlande | Land | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_niederlande"} |
| norm_en_1090 | Norm | EN 1090 | GILT_IN_LAND | land_norwegen | Land | Norwegen | {"evidence_confidence": "belegt", "id": "norm_en_1090__GILT_IN_LAND__land_norwegen"} |
| norm_en_1090 | Norm | EN 1090 | GILT_IN_LAND | land_portugal | Land | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_portugal"} |
| norm_en_1090 | Norm | EN 1090 | GILT_IN_LAND | land_schweiz | Land | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_1090__GILT_IN_LAND__land_schweiz"} |
| norm_en_1090 | Norm | EN 1090 | GILT_IN_LAND | land_vereinigtes_koenigreich | Land | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_1090__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| norm_en_1090 | Norm | EN 1090 | GILT_IN_LAND | land_oesterreich | Land | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_oesterreich"} |
| norm_en_1090 | Norm | EN 1090 | HAT_GELTUNGSBEREICH | geltungsbereich_en_cen_cenelec_mitglieder | Geltungsbereich | EN in CEN/CENELEC Mitgliedslaendern | {"evidence_confidence": "belegt", "id": "norm_en_1090__HAT_GELTUNGSBEREICH__geltungsbereich_en_cen_cenelec_mitglieder"} |
| norm_en_1090_2 | Norm | EN 1090-2 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_1090_2__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_en_1168 | Norm | EN 1168 | GILT_IN_LAND | land_belgien | Land | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_belgien"} |
| norm_en_1168 | Norm | EN 1168 | GILT_IN_LAND | land_deutschland | Land | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_deutschland"} |
| norm_en_1168 | Norm | EN 1168 | GILT_IN_LAND | land_daenemark | Land | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_daenemark"} |
| norm_en_1168 | Norm | EN 1168 | GILT_IN_LAND | land_finnland | Land | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_finnland"} |
| norm_en_1168 | Norm | EN 1168 | GILT_IN_LAND | land_frankreich | Land | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_frankreich"} |
| norm_en_1168 | Norm | EN 1168 | GILT_IN_LAND | land_italien | Land | Italien | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_italien"} |
| norm_en_1168 | Norm | EN 1168 | GILT_IN_LAND | land_luxemburg | Land | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_luxemburg"} |
| norm_en_1168 | Norm | EN 1168 | GILT_IN_LAND | land_niederlande | Land | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_niederlande"} |
| norm_en_1168 | Norm | EN 1168 | GILT_IN_LAND | land_norwegen | Land | Norwegen | {"evidence_confidence": "belegt", "id": "norm_en_1168__GILT_IN_LAND__land_norwegen"} |
| norm_en_1168 | Norm | EN 1168 | GILT_IN_LAND | land_portugal | Land | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_portugal"} |
| norm_en_1168 | Norm | EN 1168 | GILT_IN_LAND | land_schweiz | Land | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_1168__GILT_IN_LAND__land_schweiz"} |
| norm_en_1168 | Norm | EN 1168 | GILT_IN_LAND | land_vereinigtes_koenigreich | Land | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_1168__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| norm_en_1168 | Norm | EN 1168 | GILT_IN_LAND | land_oesterreich | Land | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_oesterreich"} |
| norm_en_1168 | Norm | EN 1168 | HAT_GELTUNGSBEREICH | geltungsbereich_en_cen_cenelec_mitglieder | Geltungsbereich | EN in CEN/CENELEC Mitgliedslaendern | {"evidence_confidence": "belegt", "id": "norm_en_1168__HAT_GELTUNGSBEREICH__geltungsbereich_en_cen_cenelec_mitglieder"} |
| norm_en_1168 | Norm | EN 1168 | REFERENZIERT_NORM | norm_crow_cur_4_2023 | Norm | CROW-CUR 4:2023 | {"evidence_confidence": "unklar", "id": "r_norm_en_1168__REFERENZIERT_NORM__norm_crow_cur_4_2023"} |
| norm_en_1168 | Norm | EN 1168 | REFERENZIERT_NORM | norm_crow_cur_4_2023 | Norm | CROW-CUR 4:2023 | {"evidence_confidence": "unklar", "id": "r_norm_en_1168__REFERENZIERT_NORM__norm_crow_cur_4_2023"} |
| norm_en_12058 | Norm | EN 12058 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_12058__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_en_12371 | Norm | EN 12371 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_12371__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_en_12372 | Norm | EN 12372 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_12372__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_en_13162 | Norm | EN 13162 | GILT_IN_LAND | land_belgien | Land | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_belgien"} |
| norm_en_13162 | Norm | EN 13162 | GILT_IN_LAND | land_deutschland | Land | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_deutschland"} |
| norm_en_13162 | Norm | EN 13162 | GILT_IN_LAND | land_daenemark | Land | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_daenemark"} |
| norm_en_13162 | Norm | EN 13162 | GILT_IN_LAND | land_finnland | Land | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_finnland"} |
| norm_en_13162 | Norm | EN 13162 | GILT_IN_LAND | land_frankreich | Land | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_frankreich"} |
| norm_en_13162 | Norm | EN 13162 | GILT_IN_LAND | land_italien | Land | Italien | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_italien"} |
| norm_en_13162 | Norm | EN 13162 | GILT_IN_LAND | land_luxemburg | Land | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_luxemburg"} |
| norm_en_13162 | Norm | EN 13162 | GILT_IN_LAND | land_niederlande | Land | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_niederlande"} |
| norm_en_13162 | Norm | EN 13162 | GILT_IN_LAND | land_norwegen | Land | Norwegen | {"evidence_confidence": "belegt", "id": "norm_en_13162__GILT_IN_LAND__land_norwegen"} |
| norm_en_13162 | Norm | EN 13162 | GILT_IN_LAND | land_portugal | Land | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_portugal"} |
| norm_en_13162 | Norm | EN 13162 | GILT_IN_LAND | land_schweiz | Land | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_13162__GILT_IN_LAND__land_schweiz"} |
| norm_en_13162 | Norm | EN 13162 | GILT_IN_LAND | land_vereinigtes_koenigreich | Land | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_13162__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| norm_en_13162 | Norm | EN 13162 | GILT_IN_LAND | land_oesterreich | Land | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_oesterreich"} |
| norm_en_13162 | Norm | EN 13162 | HAT_GELTUNGSBEREICH | geltungsbereich_en_cen_cenelec_mitglieder | Geltungsbereich | EN in CEN/CENELEC Mitgliedslaendern | {"evidence_confidence": "belegt", "id": "norm_en_13162__HAT_GELTUNGSBEREICH__geltungsbereich_en_cen_cenelec_mitglieder"} |
| norm_en_13224 | Norm | EN 13224 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_13224__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_en_13369 | Norm | EN 13369 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_13369__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_en_1341 | Norm | EN 1341 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_1341__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_en_13747 | Norm | EN 13747 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_13747__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_en_13755 | Norm | EN 13755 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_13755__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_en_14081 | Norm | EN 14081 | GILT_IN_LAND | land_belgien | Land | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_belgien"} |
| norm_en_14081 | Norm | EN 14081 | GILT_IN_LAND | land_deutschland | Land | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_deutschland"} |
| norm_en_14081 | Norm | EN 14081 | GILT_IN_LAND | land_daenemark | Land | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_daenemark"} |
| norm_en_14081 | Norm | EN 14081 | GILT_IN_LAND | land_finnland | Land | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_finnland"} |
| norm_en_14081 | Norm | EN 14081 | GILT_IN_LAND | land_frankreich | Land | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_frankreich"} |
| norm_en_14081 | Norm | EN 14081 | GILT_IN_LAND | land_italien | Land | Italien | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_italien"} |
| norm_en_14081 | Norm | EN 14081 | GILT_IN_LAND | land_luxemburg | Land | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_luxemburg"} |
| norm_en_14081 | Norm | EN 14081 | GILT_IN_LAND | land_niederlande | Land | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_niederlande"} |
| norm_en_14081 | Norm | EN 14081 | GILT_IN_LAND | land_norwegen | Land | Norwegen | {"evidence_confidence": "belegt", "id": "norm_en_14081__GILT_IN_LAND__land_norwegen"} |
| norm_en_14081 | Norm | EN 14081 | GILT_IN_LAND | land_portugal | Land | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_portugal"} |
| norm_en_14081 | Norm | EN 14081 | GILT_IN_LAND | land_schweiz | Land | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_14081__GILT_IN_LAND__land_schweiz"} |
| norm_en_14081 | Norm | EN 14081 | GILT_IN_LAND | land_vereinigtes_koenigreich | Land | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_14081__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| norm_en_14081 | Norm | EN 14081 | GILT_IN_LAND | land_oesterreich | Land | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_oesterreich"} |
| norm_en_14081 | Norm | EN 14081 | HAT_GELTUNGSBEREICH | geltungsbereich_en_cen_cenelec_mitglieder | Geltungsbereich | EN in CEN/CENELEC Mitgliedslaendern | {"evidence_confidence": "belegt", "id": "norm_en_14081__HAT_GELTUNGSBEREICH__geltungsbereich_en_cen_cenelec_mitglieder"} |
| norm_en_14231 | Norm | EN 14231 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_14231__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_en_1469 | Norm | EN 1469 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_1469__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_en_1936 | Norm | EN 1936 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_1936__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_en_1992 | Norm | EN 1992 (Eurocode 2) | GILT_IN_LAND | land_belgien | Land | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_belgien"} |
| norm_en_1992 | Norm | EN 1992 (Eurocode 2) | GILT_IN_LAND | land_deutschland | Land | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_deutschland"} |
| norm_en_1992 | Norm | EN 1992 (Eurocode 2) | GILT_IN_LAND | land_daenemark | Land | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_daenemark"} |
| norm_en_1992 | Norm | EN 1992 (Eurocode 2) | GILT_IN_LAND | land_finnland | Land | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_finnland"} |
| norm_en_1992 | Norm | EN 1992 (Eurocode 2) | GILT_IN_LAND | land_frankreich | Land | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_frankreich"} |
| norm_en_1992 | Norm | EN 1992 (Eurocode 2) | GILT_IN_LAND | land_italien | Land | Italien | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_italien"} |
| norm_en_1992 | Norm | EN 1992 (Eurocode 2) | GILT_IN_LAND | land_luxemburg | Land | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_luxemburg"} |
| norm_en_1992 | Norm | EN 1992 (Eurocode 2) | GILT_IN_LAND | land_niederlande | Land | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_niederlande"} |
| norm_en_1992 | Norm | EN 1992 (Eurocode 2) | GILT_IN_LAND | land_norwegen | Land | Norwegen | {"evidence_confidence": "belegt", "id": "norm_en_1992__GILT_IN_LAND__land_norwegen"} |
| norm_en_1992 | Norm | EN 1992 (Eurocode 2) | GILT_IN_LAND | land_portugal | Land | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_portugal"} |
| norm_en_1992 | Norm | EN 1992 (Eurocode 2) | GILT_IN_LAND | land_schweiz | Land | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_1992__GILT_IN_LAND__land_schweiz"} |
| norm_en_1992 | Norm | EN 1992 (Eurocode 2) | GILT_IN_LAND | land_vereinigtes_koenigreich | Land | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_1992__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| norm_en_1992 | Norm | EN 1992 (Eurocode 2) | GILT_IN_LAND | land_oesterreich | Land | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_oesterreich"} |
| norm_en_1992 | Norm | EN 1992 (Eurocode 2) | HAT_GELTUNGSBEREICH | geltungsbereich_eurocodes_eu_efta_uk | Geltungsbereich | Eurocodes in EU/EFTA plus Vereinigtes Koenigreich | {"evidence_confidence": "belegt", "id": "norm_en_1992__HAT_GELTUNGSBEREICH__geltungsbereich_eurocodes_eu_efta_uk"} |
| norm_en_1993 | Norm | EN 1993 (Eurocode 3) | GILT_IN_LAND | land_belgien | Land | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_belgien"} |
| norm_en_1993 | Norm | EN 1993 (Eurocode 3) | GILT_IN_LAND | land_deutschland | Land | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_deutschland"} |
| norm_en_1993 | Norm | EN 1993 (Eurocode 3) | GILT_IN_LAND | land_daenemark | Land | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_daenemark"} |
| norm_en_1993 | Norm | EN 1993 (Eurocode 3) | GILT_IN_LAND | land_finnland | Land | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_finnland"} |
| norm_en_1993 | Norm | EN 1993 (Eurocode 3) | GILT_IN_LAND | land_frankreich | Land | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_frankreich"} |
| norm_en_1993 | Norm | EN 1993 (Eurocode 3) | GILT_IN_LAND | land_italien | Land | Italien | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_italien"} |
| norm_en_1993 | Norm | EN 1993 (Eurocode 3) | GILT_IN_LAND | land_luxemburg | Land | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_luxemburg"} |
| norm_en_1993 | Norm | EN 1993 (Eurocode 3) | GILT_IN_LAND | land_niederlande | Land | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_niederlande"} |
| norm_en_1993 | Norm | EN 1993 (Eurocode 3) | GILT_IN_LAND | land_norwegen | Land | Norwegen | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_norwegen"} |
| norm_en_1993 | Norm | EN 1993 (Eurocode 3) | GILT_IN_LAND | land_portugal | Land | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_portugal"} |
| norm_en_1993 | Norm | EN 1993 (Eurocode 3) | GILT_IN_LAND | land_schweiz | Land | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_1993__GILT_IN_LAND__land_schweiz"} |
| norm_en_1993 | Norm | EN 1993 (Eurocode 3) | GILT_IN_LAND | land_vereinigtes_koenigreich | Land | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_1993__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| norm_en_1993 | Norm | EN 1993 (Eurocode 3) | GILT_IN_LAND | land_oesterreich | Land | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_oesterreich"} |
| norm_en_1993 | Norm | EN 1993 (Eurocode 3) | HAT_GELTUNGSBEREICH | geltungsbereich_eurocodes_eu_efta_uk | Geltungsbereich | Eurocodes in EU/EFTA plus Vereinigtes Koenigreich | {"evidence_confidence": "belegt", "id": "norm_en_1993__HAT_GELTUNGSBEREICH__geltungsbereich_eurocodes_eu_efta_uk"} |
| norm_en_1995 | Norm | EN 1995 (Eurocode 5) | GILT_IN_LAND | land_belgien | Land | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_belgien"} |
| norm_en_1995 | Norm | EN 1995 (Eurocode 5) | GILT_IN_LAND | land_deutschland | Land | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_deutschland"} |
| norm_en_1995 | Norm | EN 1995 (Eurocode 5) | GILT_IN_LAND | land_daenemark | Land | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_daenemark"} |
| norm_en_1995 | Norm | EN 1995 (Eurocode 5) | GILT_IN_LAND | land_finnland | Land | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_finnland"} |
| norm_en_1995 | Norm | EN 1995 (Eurocode 5) | GILT_IN_LAND | land_frankreich | Land | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_frankreich"} |
| norm_en_1995 | Norm | EN 1995 (Eurocode 5) | GILT_IN_LAND | land_italien | Land | Italien | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_italien"} |
| norm_en_1995 | Norm | EN 1995 (Eurocode 5) | GILT_IN_LAND | land_luxemburg | Land | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_luxemburg"} |
| norm_en_1995 | Norm | EN 1995 (Eurocode 5) | GILT_IN_LAND | land_niederlande | Land | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_niederlande"} |
| norm_en_1995 | Norm | EN 1995 (Eurocode 5) | GILT_IN_LAND | land_norwegen | Land | Norwegen | {"evidence_confidence": "belegt", "id": "norm_en_1995__GILT_IN_LAND__land_norwegen"} |
| norm_en_1995 | Norm | EN 1995 (Eurocode 5) | GILT_IN_LAND | land_portugal | Land | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_portugal"} |
| norm_en_1995 | Norm | EN 1995 (Eurocode 5) | GILT_IN_LAND | land_schweiz | Land | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_1995__GILT_IN_LAND__land_schweiz"} |
| norm_en_1995 | Norm | EN 1995 (Eurocode 5) | GILT_IN_LAND | land_vereinigtes_koenigreich | Land | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_1995__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| norm_en_1995 | Norm | EN 1995 (Eurocode 5) | GILT_IN_LAND | land_oesterreich | Land | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_oesterreich"} |
| norm_en_1995 | Norm | EN 1995 (Eurocode 5) | HAT_GELTUNGSBEREICH | geltungsbereich_eurocodes_eu_efta_uk | Geltungsbereich | Eurocodes in EU/EFTA plus Vereinigtes Koenigreich | {"evidence_confidence": "belegt", "id": "norm_en_1995__HAT_GELTUNGSBEREICH__geltungsbereich_eurocodes_eu_efta_uk"} |
| norm_en_1996 | Norm | EN 1996 (Eurocode 6) | GILT_IN_LAND | land_belgien | Land | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_belgien"} |
| norm_en_1996 | Norm | EN 1996 (Eurocode 6) | GILT_IN_LAND | land_deutschland | Land | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_deutschland"} |
| norm_en_1996 | Norm | EN 1996 (Eurocode 6) | GILT_IN_LAND | land_daenemark | Land | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_daenemark"} |
| norm_en_1996 | Norm | EN 1996 (Eurocode 6) | GILT_IN_LAND | land_finnland | Land | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_finnland"} |
| norm_en_1996 | Norm | EN 1996 (Eurocode 6) | GILT_IN_LAND | land_frankreich | Land | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_frankreich"} |
| norm_en_1996 | Norm | EN 1996 (Eurocode 6) | GILT_IN_LAND | land_italien | Land | Italien | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_italien"} |
| norm_en_1996 | Norm | EN 1996 (Eurocode 6) | GILT_IN_LAND | land_luxemburg | Land | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_luxemburg"} |
| norm_en_1996 | Norm | EN 1996 (Eurocode 6) | GILT_IN_LAND | land_niederlande | Land | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_niederlande"} |
| norm_en_1996 | Norm | EN 1996 (Eurocode 6) | GILT_IN_LAND | land_norwegen | Land | Norwegen | {"evidence_confidence": "belegt", "id": "norm_en_1996__GILT_IN_LAND__land_norwegen"} |
| norm_en_1996 | Norm | EN 1996 (Eurocode 6) | GILT_IN_LAND | land_portugal | Land | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_portugal"} |
| norm_en_1996 | Norm | EN 1996 (Eurocode 6) | GILT_IN_LAND | land_schweiz | Land | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_1996__GILT_IN_LAND__land_schweiz"} |
| norm_en_1996 | Norm | EN 1996 (Eurocode 6) | GILT_IN_LAND | land_vereinigtes_koenigreich | Land | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_1996__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| norm_en_1996 | Norm | EN 1996 (Eurocode 6) | GILT_IN_LAND | land_oesterreich | Land | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_oesterreich"} |
| norm_en_1996 | Norm | EN 1996 (Eurocode 6) | HAT_GELTUNGSBEREICH | geltungsbereich_eurocodes_eu_efta_uk | Geltungsbereich | Eurocodes in EU/EFTA plus Vereinigtes Koenigreich | {"evidence_confidence": "belegt", "id": "norm_en_1996__HAT_GELTUNGSBEREICH__geltungsbereich_eurocodes_eu_efta_uk"} |
| norm_en_206 | Norm | EN 206 | GILT_IN_LAND | land_belgien | Land | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_belgien"} |
| norm_en_206 | Norm | EN 206 | GILT_IN_LAND | land_deutschland | Land | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_deutschland"} |
| norm_en_206 | Norm | EN 206 | GILT_IN_LAND | land_daenemark | Land | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_daenemark"} |
| norm_en_206 | Norm | EN 206 | GILT_IN_LAND | land_finnland | Land | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_finnland"} |
| norm_en_206 | Norm | EN 206 | GILT_IN_LAND | land_frankreich | Land | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_frankreich"} |
| norm_en_206 | Norm | EN 206 | GILT_IN_LAND | land_italien | Land | Italien | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_italien"} |
| norm_en_206 | Norm | EN 206 | GILT_IN_LAND | land_luxemburg | Land | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_luxemburg"} |
| norm_en_206 | Norm | EN 206 | GILT_IN_LAND | land_niederlande | Land | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_niederlande"} |
| norm_en_206 | Norm | EN 206 | GILT_IN_LAND | land_norwegen | Land | Norwegen | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_norwegen"} |
| norm_en_206 | Norm | EN 206 | GILT_IN_LAND | land_portugal | Land | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_portugal"} |
| norm_en_206 | Norm | EN 206 | GILT_IN_LAND | land_schweiz | Land | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_206__GILT_IN_LAND__land_schweiz"} |
| norm_en_206 | Norm | EN 206 | GILT_IN_LAND | land_vereinigtes_koenigreich | Land | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_206__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| norm_en_206 | Norm | EN 206 | GILT_IN_LAND | land_oesterreich | Land | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_oesterreich"} |
| norm_en_206 | Norm | EN 206 | HAT_GELTUNGSBEREICH | geltungsbereich_en_cen_cenelec_mitglieder | Geltungsbereich | EN in CEN/CENELEC Mitgliedslaendern | {"evidence_confidence": "belegt", "id": "norm_en_206__HAT_GELTUNGSBEREICH__geltungsbereich_en_cen_cenelec_mitglieder"} |
| norm_en_338 | Norm | EN 338 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_338__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_en_771 | Norm | EN 771 | GILT_IN_LAND | land_belgien | Land | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_belgien"} |
| norm_en_771 | Norm | EN 771 | GILT_IN_LAND | land_deutschland | Land | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_deutschland"} |
| norm_en_771 | Norm | EN 771 | GILT_IN_LAND | land_daenemark | Land | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_daenemark"} |
| norm_en_771 | Norm | EN 771 | GILT_IN_LAND | land_finnland | Land | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_finnland"} |
| norm_en_771 | Norm | EN 771 | GILT_IN_LAND | land_frankreich | Land | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_frankreich"} |
| norm_en_771 | Norm | EN 771 | GILT_IN_LAND | land_italien | Land | Italien | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_italien"} |
| norm_en_771 | Norm | EN 771 | GILT_IN_LAND | land_luxemburg | Land | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_luxemburg"} |
| norm_en_771 | Norm | EN 771 | GILT_IN_LAND | land_niederlande | Land | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_niederlande"} |
| norm_en_771 | Norm | EN 771 | GILT_IN_LAND | land_norwegen | Land | Norwegen | {"evidence_confidence": "belegt", "id": "norm_en_771__GILT_IN_LAND__land_norwegen"} |
| norm_en_771 | Norm | EN 771 | GILT_IN_LAND | land_portugal | Land | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_portugal"} |
| norm_en_771 | Norm | EN 771 | GILT_IN_LAND | land_schweiz | Land | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_771__GILT_IN_LAND__land_schweiz"} |
| norm_en_771 | Norm | EN 771 | GILT_IN_LAND | land_vereinigtes_koenigreich | Land | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_771__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| norm_en_771 | Norm | EN 771 | GILT_IN_LAND | land_oesterreich | Land | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_oesterreich"} |
| norm_en_771 | Norm | EN 771 | HAT_GELTUNGSBEREICH | geltungsbereich_en_cen_cenelec_mitglieder | Geltungsbereich | EN in CEN/CENELEC Mitgliedslaendern | {"evidence_confidence": "belegt", "id": "norm_en_771__HAT_GELTUNGSBEREICH__geltungsbereich_en_cen_cenelec_mitglieder"} |
| norm_en_771_1 | Norm | EN 771-1 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_771_1__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_en_772 | Norm | EN 772 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_772__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_en_998 | Norm | EN 998 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_998__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_en_sia_product_references | Norm | EN/SIA product references | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_sia_product_references__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_en_sn_12058 | Norm | EN/SN 12058 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_sn_12058__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_en_sn_1469 | Norm | EN/SN 1469 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_sn_1469__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_eurocode_2 | Norm | Eurocode 2 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_eurocode_2__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_eurocode_3 | Norm | Eurocode 3 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_eurocode_3__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_eurocode_5 | Norm | Eurocode 5 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_eurocode_5__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_eurocode_5_uk_na | Norm | Eurocode 5 / UK NA | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_eurocode_5_uk_na__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_eurocode_6 | Norm | Eurocode 6 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_eurocode_6__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_eurocode_adjacent_structural_verification | Norm | Eurocode-adjacent structural verification | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_eurocode_adjacent_structural_verification__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_eurocode_related_timber_product_standards | Norm | Eurocode-related timber product standards | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_eurocode_related_timber_product_standards__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_finnish_national_annexes | Norm | Finnish national annexes | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_finnish_national_annexes__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| rr_fi_beton_hollow_core_slabs | ReuseRule | Finnland × Beton / hollow-core slabs reuse rule | REFERENZIERT_NORM | norm_en_1168 | Norm | EN 1168 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_fi_beton_hollow_core_slabs__REFERENZIERT_NORM__norm_en_1168"} |
| rr_fi_beton_hollow_core_slabs | ReuseRule | Finnland × Beton / hollow-core slabs reuse rule | REFERENZIERT_NORM | norm_eurocode_2 | Norm | Eurocode 2 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_fi_beton_hollow_core_slabs__REFERENZIERT_NORM__norm_eurocode_2"} |
| rr_fi_beton_hollow_core_slabs | ReuseRule | Finnland × Beton / hollow-core slabs reuse rule | REFERENZIERT_NORM | norm_finnish_national_annexes | Norm | Finnish national annexes | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_fi_beton_hollow_core_slabs__REFERENZIERT_NORM__norm_finnish_national_annexes"} |
| rr_fi_beton_hollow_core_slabs | ReuseRule | Finnland × Beton / hollow-core slabs reuse rule | REFERENZIERT_NORM | norm_recreate_qa_procedure | Norm | ReCreate QA procedure | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_fi_beton_hollow_core_slabs__REFERENZIERT_NORM__norm_recreate_qa_procedure"} |
| norm_fire_durability_rules | Norm | Fire/durability rules | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_fire_durability_rules__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_fire_moisture_rules | Norm | Fire/moisture rules | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_fire_moisture_rules__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_fire_moisture_durability_requirements | Norm | Fire/moisture/durability requirements | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_fire_moisture_durability_requirements__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_frost_rules | Norm | Frost rules | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_frost_rules__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_historic_sections_book | Norm | Historic Sections Book | BELEGT_IN | q_bedzed_london_hackbridge_md | Quelle:Dossier | BedZED_London_Hackbridge… | {"evidence_confidence": "unklar", "id": "r_norm_historic_sections_book__BELEGT_IN__q_bedzed_london_hackbridge_md"} |
| norm_historic_sections_book | Norm | Historic Sections Book | GILT_IN_LAND | land_vereinigtes_koenigreich | Land | Vereinigtes Königreich | {"evidence_confidence": "unklar", "id": "r_norm_historic_sections_book__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| bg_stahlbeton_decke_ccn_hollow_core_slabs | Bauteilgruppe | Hohlkoerperdecken | REFERENZIERT_NORM | norm_crow_cur_4_2023 | Norm | CROW-CUR 4:2023 | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahlbeton_decke_ccn_hollow_core_slabs__REFERENZIERT_NORM__norm_crow_cur_4_2023"} |
| bg_stahlbeton_decke_ka13_hollow_core_slabs | Bauteilgruppe | Hohlkörperdecken aus… | REFERENZIERT_NORM | norm_ns_3682 | Norm | NS 3682 | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahlbeton_decke_ka13_hollow_core_slabs__REFERENZIERT_NORM__norm_ns_3682"} |
| bg_stahlbeton_decke_ka13_hollow_core_slabs | Bauteilgruppe | Hohlkörperdecken aus… | REFERENZIERT_NORM | norm_tek_norway | Norm | TEK (NO) | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahlbeton_decke_ka13_hollow_core_slabs__REFERENZIERT_NORM__norm_tek_norway"} |
| p_k118_kopfbau_halle_118_winterthur | Projekt | K.118 Winterthur | REFERENZIERT_NORM | norm_din_en_15804 | Norm | DIN EN 15804 | {"evidence_confidence": "teilweise_belegt", "id": "r_p_k118_kopfbau_halle_118_winterthur__REFERENZIERT_NORM__norm_din_en_15804"} |
| p_k118_kopfbau_halle_118_winterthur | Projekt | K.118 Winterthur | REFERENZIERT_NORM | norm_iso_14040 | Norm | ISO 14040 | {"evidence_confidence": "teilweise_belegt", "id": "r_p_k118_kopfbau_halle_118_winterthur__REFERENZIERT_NORM__norm_iso_14040"} |
| p_k118_kopfbau_halle_118_winterthur | Projekt | K.118 Winterthur | REFERENZIERT_NORM | norm_iso_14044 | Norm | ISO 14044 | {"evidence_confidence": "teilweise_belegt", "id": "r_p_k118_kopfbau_halle_118_winterthur__REFERENZIERT_NORM__norm_iso_14044"} |
| p_ka13_kristian_augusts_gate_13_oslo | Projekt | KA13 | REFERENZIERT_NORM | norm_din_en_15804 | Norm | DIN EN 15804 | {"evidence_confidence": "teilweise_belegt", "id": "r_p_ka13_kristian_augusts_gate_13_oslo__REFERENZIERT_NORM__norm_din_en_15804"} |
| p_ka13_kristian_augusts_gate_13_oslo | Projekt | KA13 | REFERENZIERT_NORM | norm_din_en_15978 | Norm | DIN EN 15978 | {"evidence_confidence": "teilweise_belegt", "id": "r_p_ka13_kristian_augusts_gate_13_oslo__REFERENZIERT_NORM__norm_din_en_15978"} |
| p_lysp8_basel | Projekt | LYSP8 Basel | REFERENZIERT_NORM | norm_sia_269 | Norm | SIA 269 | {"evidence_confidence": "unklar", "id": "r_p_lysp8_basel__REFERENZIERT_NORM__norm_sia_269"} |
| p_lysp8_basel | Projekt | LYSP8 Basel | REFERENZIERT_NORM | norm_sia_416 | Norm | SIA 416 | {"evidence_confidence": "unklar", "id": "r_p_lysp8_basel__REFERENZIERT_NORM__norm_sia_416"} |
| norm_mvv_tb_dibt_pathway | Norm | MVV TB/DIBt pathway | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_mvv_tb_dibt_pathway__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_nbn_en_14081 | Norm | NBN EN 14081 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_nbn_en_14081__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_nbn_en_338 | Norm | NBN EN 338 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_nbn_en_338__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_nbn_national_annexes | Norm | NBN national annexes | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_nbn_national_annexes__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_nen_8700 | Norm | NEN 8700 | GILT_IN_LAND | land_niederlande | Land | Niederlande | {"evidence_confidence": "unklar", "id": "r_norm_nen_8700__GILT_IN_LAND__land_niederlande"} |
| norm_nen_en_1090_2 | Norm | NEN EN 1090-2 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_nen_en_1090_2__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_nen_en_14081 | Norm | NEN EN 14081 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_nen_en_14081__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_nen_en_338 | Norm | NEN EN 338 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_nen_en_338__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_nen_fire_moisture_rules | Norm | NEN fire/moisture rules | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_nen_fire_moisture_rules__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_ns_3682 | Norm | NS 3682 | GILT_IN_LAND | land_norwegen | Land | Norwegen | {"evidence_confidence": "unklar", "id": "r_norm_ns_3682__GILT_IN_LAND__land_norwegen"} |
| norm_ns_3682 | Norm | NS 3682 | REFERENZIERT_NORM | norm_tek_norway | Norm | TEK (NO) | {"evidence_confidence": "unklar", "id": "r_norm_ns_3682__REFERENZIERT_NORM__norm_tek_norway"} |
| norm_ns_3682 | Norm | NS 3682 | REFERENZIERT_NORM | norm_tek_norway | Norm | TEK (NO) | {"evidence_confidence": "unklar", "id": "r_norm_ns_3682__REFERENZIERT_NORM__norm_tek_norway"} |
| norm_ns_3682_2022 | Norm | NS 3682:2022 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_ns_3682_2022__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| rr_nl_beton | ReuseRule | Niederlande × Beton reuse rule | REFERENZIERT_NORM | norm_bbl_nen | Norm | Bbl/NEN | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_beton__REFERENZIERT_NORM__norm_bbl_nen"} |
| rr_nl_beton | ReuseRule | Niederlande × Beton reuse rule | REFERENZIERT_NORM | norm_en_1168 | Norm | EN 1168 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_beton__REFERENZIERT_NORM__norm_en_1168"} |
| rr_nl_beton | ReuseRule | Niederlande × Beton reuse rule | REFERENZIERT_NORM | norm_en_13369 | Norm | EN 13369 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_beton__REFERENZIERT_NORM__norm_en_13369"} |
| rr_nl_beton | ReuseRule | Niederlande × Beton reuse rule | REFERENZIERT_NORM | norm_en_206 | Norm | EN 206 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_beton__REFERENZIERT_NORM__norm_en_206"} |
| rr_nl_beton | ReuseRule | Niederlande × Beton reuse rule | REFERENZIERT_NORM | norm_eurocode_2 | Norm | Eurocode 2 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_beton__REFERENZIERT_NORM__norm_eurocode_2"} |
| rr_nl_holz | ReuseRule | Niederlande × Holz reuse rule | REFERENZIERT_NORM | norm_cb_23_passports | Norm | CB'23 passports | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_holz__REFERENZIERT_NORM__norm_cb_23_passports"} |
| rr_nl_holz | ReuseRule | Niederlande × Holz reuse rule | REFERENZIERT_NORM | norm_eurocode_5 | Norm | Eurocode 5 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_holz__REFERENZIERT_NORM__norm_eurocode_5"} |
| rr_nl_holz | ReuseRule | Niederlande × Holz reuse rule | REFERENZIERT_NORM | norm_nen_en_14081 | Norm | NEN EN 14081 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_holz__REFERENZIERT_NORM__norm_nen_en_14081"} |
| rr_nl_holz | ReuseRule | Niederlande × Holz reuse rule | REFERENZIERT_NORM | norm_nen_en_338 | Norm | NEN EN 338 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_holz__REFERENZIERT_NORM__norm_nen_en_338"} |
| rr_nl_holz | ReuseRule | Niederlande × Holz reuse rule | REFERENZIERT_NORM | norm_nen_fire_moisture_rules | Norm | NEN fire/moisture rules | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_holz__REFERENZIERT_NORM__norm_nen_fire_moisture_rules"} |
| rr_nl_stahl | ReuseRule | Niederlande × Stahl reuse rule | REFERENZIERT_NORM | norm_bbl_nen_links | Norm | Bbl/NEN links | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_stahl__REFERENZIERT_NORM__norm_bbl_nen_links"} |
| rr_nl_stahl | ReuseRule | Niederlande × Stahl reuse rule | REFERENZIERT_NORM | norm_cen_ts_1090_201 | Norm | CEN/TS 1090-201 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_stahl__REFERENZIERT_NORM__norm_cen_ts_1090_201"} |
| rr_nl_stahl | ReuseRule | Niederlande × Stahl reuse rule | REFERENZIERT_NORM | norm_eurocode_3 | Norm | Eurocode 3 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_stahl__REFERENZIERT_NORM__norm_eurocode_3"} |
| rr_nl_stahl | ReuseRule | Niederlande × Stahl reuse rule | REFERENZIERT_NORM | norm_nen_en_1090_2 | Norm | NEN EN 1090-2 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_stahl__REFERENZIERT_NORM__norm_nen_en_1090_2"} |
| rr_no_beton_hollow_core_slabs | ReuseRule | Norwegen × Beton / hollow-core slabs reuse rule | REFERENZIERT_NORM | norm_en_1168 | Norm | EN 1168 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_no_beton_hollow_core_slabs__REFERENZIERT_NORM__norm_en_1168"} |
| rr_no_beton_hollow_core_slabs | ReuseRule | Norwegen × Beton / hollow-core slabs reuse rule | REFERENZIERT_NORM | norm_eurocode_2 | Norm | Eurocode 2 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_no_beton_hollow_core_slabs__REFERENZIERT_NORM__norm_eurocode_2"} |
| rr_no_beton_hollow_core_slabs | ReuseRule | Norwegen × Beton / hollow-core slabs reuse rule | REFERENZIERT_NORM | norm_ns_3682_2022 | Norm | NS 3682:2022 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_no_beton_hollow_core_slabs__REFERENZIERT_NORM__norm_ns_3682_2022"} |
| rr_no_beton_hollow_core_slabs | ReuseRule | Norwegen × Beton / hollow-core slabs reuse rule | REFERENZIERT_NORM | norm_tek17 | Norm | TEK17 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_no_beton_hollow_core_slabs__REFERENZIERT_NORM__norm_tek17"} |
| norm_pd_cen_ts_1090_201 | Norm | PD CEN/TS 1090-201 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_pd_cen_ts_1090_201__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_rt_2012 | Norm | RT 2012 | BELEGT_IN | q_resilience_la_ferme_des_possibles_stains_md | Quelle:Dossier | Resilience_La_Ferme_des_… | {"evidence_confidence": "unklar", "id": "r_norm_rt_2012__BELEGT_IN__q_resilience_la_ferme_des_possibles_stains_md"} |
| norm_rt_2012 | Norm | RT 2012 | GILT_IN_LAND | land_frankreich | Land | Frankreich | {"evidence_confidence": "unklar", "id": "r_norm_rt_2012__GILT_IN_LAND__land_frankreich"} |
| bg_mehrere_technik_ka13_tga_sanitary_radiators | Bauteilgruppe | Radiatoren (Ka13) | REFERENZIERT_NORM | norm_tek_norway | Norm | TEK (NO) | {"evidence_confidence": "unklar", "id": "r_bg_reuse_mehrere_technik_ka13_tga_sanitary_radiators__REFERENZIERT_NORM__norm_tek_norway"} |
| norm_recreate_qa_procedure | Norm | ReCreate QA procedure | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_recreate_qa_procedure__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| p_resource_rows_copenhagen | Projekt | Resource Rows | REFERENZIERT_NORM | norm_din_en_15804 | Norm | DIN EN 15804 | {"evidence_confidence": "teilweise_belegt", "id": "r_p_resource_rows_copenhagen__REFERENZIERT_NORM__norm_din_en_15804"} |
| p_resource_rows_copenhagen | Projekt | Resource Rows | REFERENZIERT_NORM | norm_din_en_15978 | Norm | DIN EN 15978 | {"evidence_confidence": "teilweise_belegt", "id": "r_p_resource_rows_copenhagen__REFERENZIERT_NORM__norm_din_en_15978"} |
| p_resilience_la_ferme_des_possibles_stains | Projekt | Résilience | REFERENZIERT_NORM | norm_rt_2012 | Norm | RT 2012 | {"evidence_confidence": "unklar", "id": "r_p_resilience_la_ferme_des_possibles_stains__REFERENZIERT_NORM__norm_rt_2012"} |
| norm_sci_p427 | Norm | SCI P427 protocol | BELEGT_IN | q_brent_cross_town_primary_substation_london_md | Quelle:Dossier | Brent_Cross_Town_Primary… | {"evidence_confidence": "unklar", "id": "r_norm_sci_p427__BELEGT_IN__q_brent_cross_town_primary_substation_london_md"} |
| norm_sci_p427 | Norm | SCI P427 protocol | GILT_IN_LAND | land_vereinigtes_koenigreich | Land | Vereinigtes Königreich | {"evidence_confidence": "unklar", "id": "r_norm_sci_p427__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| norm_sci_p427 | Norm | SCI P427 protocol | REFERENZIERT_NORM | norm_sci_p440 | Norm | SCI P440 | {"evidence_confidence": "unklar", "id": "r_norm_sci_p427__REFERENZIERT_NORM__norm_sci_p440"} |
| norm_sci_p427 | Norm | SCI P427 protocol | REFERENZIERT_NORM | norm_sci_p440 | Norm | SCI P440 | {"evidence_confidence": "unklar", "id": "r_norm_sci_p427__REFERENZIERT_NORM__norm_sci_p440"} |
| norm_sci_p440 | Norm | SCI P440 | GILT_IN_LAND | land_vereinigtes_koenigreich | Land | Vereinigtes Königreich | {"evidence_confidence": "unklar", "id": "r_norm_sci_p440__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| norm_sci_p440 | Norm | SCI P440 | REFERENZIERT_NORM | norm_sci_p427 | Norm | SCI P427 protocol | {"evidence_confidence": "unklar", "id": "r_norm_sci_p440__REFERENZIERT_NORM__norm_sci_p427"} |
| norm_sci_p440 | Norm | SCI P440 | REFERENZIERT_NORM | norm_sci_p427 | Norm | SCI P427 protocol | {"evidence_confidence": "unklar", "id": "r_norm_sci_p440__REFERENZIERT_NORM__norm_sci_p427"} |
| norm_sci_protocol | Norm | SCI protocol | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_sci_protocol__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_sia_schweiz | Norm | SIA (CH) | GILT_IN_LAND | land_schweiz | Land | Schweiz | {"evidence_confidence": "unklar", "id": "r_norm_sia_schweiz__GILT_IN_LAND__land_schweiz"} |
| norm_sia_schweiz | Norm | SIA (CH) | REFERENZIERT_NORM | norm_iso_20887 | Norm | ISO 20887 | {"evidence_confidence": "unklar", "id": "r_norm_sia_schweiz__REFERENZIERT_NORM__norm_iso_20887"} |
| norm_sia_schweiz | Norm | SIA (CH) | REFERENZIERT_NORM | norm_iso_20887 | Norm | ISO 20887 | {"evidence_confidence": "unklar", "id": "r_norm_sia_schweiz__REFERENZIERT_NORM__norm_iso_20887"} |
| norm_sia_262 | Norm | SIA 262 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_sia_262__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_sia_263 | Norm | SIA 263 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_sia_263__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_sia_265 | Norm | SIA 265 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_sia_265__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_sia_facade_anchorage_rules | Norm | SIA façade/anchorage rules | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_sia_facade_anchorage_rules__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_sia_fire_durability_rules | Norm | SIA fire/durability rules | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_sia_fire_durability_rules__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| rr_ch_beton | ReuseRule | Schweiz × Beton reuse rule | REFERENZIERT_NORM | norm_en_sia_product_references | Norm | EN/SIA product references | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_beton__REFERENZIERT_NORM__norm_en_sia_product_references"} |
| rr_ch_beton | ReuseRule | Schweiz × Beton reuse rule | REFERENZIERT_NORM | norm_sia_262 | Norm | SIA 262 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_beton__REFERENZIERT_NORM__norm_sia_262"} |
| rr_ch_beton | ReuseRule | Schweiz × Beton reuse rule | REFERENZIERT_NORM | norm_sia_269 | Norm | SIA 269 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_beton__REFERENZIERT_NORM__norm_sia_269"} |
| rr_ch_holz | ReuseRule | Schweiz × Holz reuse rule | REFERENZIERT_NORM | norm_eurocode_related_timber_product_standards | Norm | Eurocode-related timber product standards | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_holz__REFERENZIERT_NORM__norm_eurocode_related_timber_product_standards"} |
| rr_ch_holz | ReuseRule | Schweiz × Holz reuse rule | REFERENZIERT_NORM | norm_fire_moisture_durability_requirements | Norm | Fire/moisture/durability requirements | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_holz__REFERENZIERT_NORM__norm_fire_moisture_durability_requirements"} |
| rr_ch_holz | ReuseRule | Schweiz × Holz reuse rule | REFERENZIERT_NORM | norm_sia_265 | Norm | SIA 265 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_holz__REFERENZIERT_NORM__norm_sia_265"} |
| rr_ch_naturstein | ReuseRule | Schweiz × Naturstein reuse rule | REFERENZIERT_NORM | norm_en_sn_12058 | Norm | EN/SN 12058 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_naturstein__REFERENZIERT_NORM__norm_en_sn_12058"} |
| rr_ch_naturstein | ReuseRule | Schweiz × Naturstein reuse rule | REFERENZIERT_NORM | norm_en_sn_1469 | Norm | EN/SN 1469 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_naturstein__REFERENZIERT_NORM__norm_en_sn_1469"} |
| rr_ch_naturstein | ReuseRule | Schweiz × Naturstein reuse rule | REFERENZIERT_NORM | norm_sia_facade_anchorage_rules | Norm | SIA façade/anchorage rules | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_naturstein__REFERENZIERT_NORM__norm_sia_facade_anchorage_rules"} |
| rr_ch_stahl | ReuseRule | Schweiz × Stahl reuse rule | REFERENZIERT_NORM | norm_cen_ts_1090_201 | Norm | CEN/TS 1090-201 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_stahl__REFERENZIERT_NORM__norm_cen_ts_1090_201"} |
| rr_ch_stahl | ReuseRule | Schweiz × Stahl reuse rule | REFERENZIERT_NORM | norm_sia_263 | Norm | SIA 263 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_stahl__REFERENZIERT_NORM__norm_sia_263"} |
| rr_ch_stahl | ReuseRule | Schweiz × Stahl reuse rule | REFERENZIERT_NORM | norm_sia_fire_durability_rules | Norm | SIA fire/durability rules | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_stahl__REFERENZIERT_NORM__norm_sia_fire_durability_rules"} |
| rr_ch_stahl | ReuseRule | Schweiz × Stahl reuse rule | REFERENZIERT_NORM | norm_swiss_baupg | Norm | Swiss BauPG | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_stahl__REFERENZIERT_NORM__norm_swiss_baupg"} |
| p_schaerenmoosstrasse_zuerich | Projekt | Schärenmoosstr. ZH | REFERENZIERT_NORM | norm_sia_261 | Norm | SIA 261 | {"evidence_confidence": "unklar", "id": "r_p_schaerenmoosstrasse_zuerich__REFERENZIERT_NORM__norm_sia_261"} |
| p_schaerenmoosstrasse_zuerich | Projekt | Schärenmoosstr. ZH | REFERENZIERT_NORM | norm_sia_500 | Norm | SIA 500 | {"evidence_confidence": "unklar", "id": "r_p_schaerenmoosstrasse_zuerich__REFERENZIERT_NORM__norm_sia_500"} |
| bg_stahl_mehrere_ka13 | Bauteilgruppe | Stahl in Bestand und… | REFERENZIERT_NORM | norm_tek_norway | Norm | TEK (NO) | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahl_mehrere_ka13__REFERENZIERT_NORM__norm_tek_norway"} |
| bg_stahl_mehrere_k118_structure | Bauteilgruppe | Stahlträger und Stützen… | REFERENZIERT_NORM | norm_sia_schweiz | Norm | SIA (CH) | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahl_mehrere_k118_structure__REFERENZIERT_NORM__norm_sia_schweiz"} |
| bg_stahl_mehrere_holbein_structural | Bauteilgruppe | Stahlträger un… (Holbein) | REFERENZIERT_NORM | norm_en_1090 | Norm | EN 1090 | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahl_mehrere_holbein_structural__REFERENZIERT_NORM__norm_en_1090"} |
| bg_stahl_mehrere_holbein_structural | Bauteilgruppe | Stahlträger un… (Holbein) | REFERENZIERT_NORM | norm_sci_p427 | Norm | SCI P427 protocol | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahl_mehrere_holbein_structural__REFERENZIERT_NORM__norm_sci_p427"} |
| bg_stahl_mehrere_holbein_structural | Bauteilgruppe | Stahlträger un… (Holbein) | REFERENZIERT_NORM | norm_sci_p440 | Norm | SCI P440 | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahl_mehrere_holbein_structural__REFERENZIERT_NORM__norm_sci_p440"} |
| bg_stahl_mehrere_55gss_external_core | Bauteilgruppe | Steel profiles for… | REFERENZIERT_NORM | norm_en_1090 | Norm | EN 1090 | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahl_mehrere_55gss_external_core__REFERENZIERT_NORM__norm_en_1090"} |
| bg_stahl_mehrere_bedzed_structural | Bauteilgruppe | Structural steel frame… | REFERENZIERT_NORM | norm_historic_sections_book | Norm | Historic Sections Book | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahl_mehrere_bedzed_structural__REFERENZIERT_NORM__norm_historic_sections_book"} |
| norm_swiss_baupg | Norm | Swiss BauPG | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_swiss_baupg__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| norm_tek_norway | Norm | TEK (NO) | GILT_IN_LAND | land_norwegen | Land | Norwegen | {"evidence_confidence": "unklar", "id": "r_norm_tek_norway__GILT_IN_LAND__land_norwegen"} |
| norm_tek_norway | Norm | TEK (NO) | REFERENZIERT_NORM | norm_ns_3682 | Norm | NS 3682 | {"evidence_confidence": "unklar", "id": "r_norm_tek_norway__REFERENZIERT_NORM__norm_ns_3682"} |
| norm_tek_norway | Norm | TEK (NO) | REFERENZIERT_NORM | norm_ns_3682 | Norm | NS 3682 | {"evidence_confidence": "unklar", "id": "r_norm_tek_norway__REFERENZIERT_NORM__norm_ns_3682"} |
| norm_tek17 | Norm | TEK17 | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_tek17__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| p_thoravej_29_copenhagen | Projekt | Thoravej 29 Copenhagen | REFERENZIERT_NORM | norm_din_en_15804 | Norm | DIN EN 15804 | {"evidence_confidence": "teilweise_belegt", "id": "r_p_thoravej_29_copenhagen__REFERENZIERT_NORM__norm_din_en_15804"} |
| p_thoravej_29_copenhagen | Projekt | Thoravej 29 Copenhagen | REFERENZIERT_NORM | norm_din_en_15978 | Norm | DIN EN 15978 | {"evidence_confidence": "teilweise_belegt", "id": "r_p_thoravej_29_copenhagen__REFERENZIERT_NORM__norm_din_en_15978"} |
| norm_ukca_ce_interface | Norm | UKCA/CE interface | BELEGT_IN | q_circular_construction_reuse_graph_gaps_md | Quelle:ResearchDocument | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_ukca_ce_interface__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| p_umar_unit | Projekt | UMAR Unit | REFERENZIERT_NORM | norm_sia_269 | Norm | SIA 269 | {"evidence_confidence": "unklar", "id": "r_p_umar_unit__REFERENZIERT_NORM__norm_sia_269"} |
| p_umar_unit | Projekt | UMAR Unit | REFERENZIERT_NORM | norm_sia_380_1 | Norm | SIA 380/1 | {"evidence_confidence": "unklar", "id": "r_p_umar_unit__REFERENZIERT_NORM__norm_sia_380_1"} |
| rr_gb_holz | ReuseRule | Vereinigtes Königreich × Holz reuse rule | REFERENZIERT_NORM | norm_bs_4978 | Norm | BS 4978 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_holz__REFERENZIERT_NORM__norm_bs_4978"} |
| rr_gb_holz | ReuseRule | Vereinigtes Königreich × Holz reuse rule | REFERENZIERT_NORM | norm_en_14081 | Norm | EN 14081 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_holz__REFERENZIERT_NORM__norm_en_14081"} |
| rr_gb_holz | ReuseRule | Vereinigtes Königreich × Holz reuse rule | REFERENZIERT_NORM | norm_en_338 | Norm | EN 338 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_holz__REFERENZIERT_NORM__norm_en_338"} |
| rr_gb_holz | ReuseRule | Vereinigtes Königreich × Holz reuse rule | REFERENZIERT_NORM | norm_eurocode_5_uk_na | Norm | Eurocode 5 / UK NA | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_holz__REFERENZIERT_NORM__norm_eurocode_5_uk_na"} |
| rr_gb_holz | ReuseRule | Vereinigtes Königreich × Holz reuse rule | REFERENZIERT_NORM | norm_fire_moisture_rules | Norm | Fire/moisture rules | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_holz__REFERENZIERT_NORM__norm_fire_moisture_rules"} |
| rr_gb_stahl | ReuseRule | Vereinigtes Königreich × Stahl reuse rule | REFERENZIERT_NORM | norm_en_1090_2 | Norm | EN 1090-2 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_stahl__REFERENZIERT_NORM__norm_en_1090_2"} |
| rr_gb_stahl | ReuseRule | Vereinigtes Königreich × Stahl reuse rule | REFERENZIERT_NORM | norm_eurocode_3 | Norm | Eurocode 3 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_stahl__REFERENZIERT_NORM__norm_eurocode_3"} |
| rr_gb_stahl | ReuseRule | Vereinigtes Königreich × Stahl reuse rule | REFERENZIERT_NORM | norm_pd_cen_ts_1090_201 | Norm | PD CEN/TS 1090-201 | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_stahl__REFERENZIERT_NORM__norm_pd_cen_ts_1090_201"} |
| rr_gb_stahl | ReuseRule | Vereinigtes Königreich × Stahl reuse rule | REFERENZIERT_NORM | norm_sci_protocol | Norm | SCI protocol | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_stahl__REFERENZIERT_NORM__norm_sci_protocol"} |
| rr_gb_stahl | ReuseRule | Vereinigtes Königreich × Stahl reuse rule | REFERENZIERT_NORM | norm_ukca_ce_interface | Norm | UKCA/CE interface | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_stahl__REFERENZIERT_NORM__norm_ukca_ce_interface"} |

## Norm Details

### BS 4978

| Property | Value |
| --- | --- |
| id | norm_bs_4978 |
| name | BS 4978 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Vereinigtes Königreich (land_vereinigtes_koenigreich) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_bs_4978__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_gb_holz | Vereinigtes Königreich × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_holz__REFERENZIERT_NORM__norm_bs_4978"} |


### Bbl/NEN

| Property | Value |
| --- | --- |
| id | norm_bbl_nen |
| name | Bbl/NEN |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Niederlande (land_niederlande) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_bbl_nen__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_nl_beton | Niederlande × Beton reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_beton__REFERENZIERT_NORM__norm_bbl_nen"} |


### Bbl/NEN links

| Property | Value |
| --- | --- |
| id | norm_bbl_nen_links |
| name | Bbl/NEN links |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Niederlande (land_niederlande) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_bbl_nen_links__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_nl_stahl | Niederlande × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_stahl__REFERENZIERT_NORM__norm_bbl_nen_links"} |


### CB'23 passports

| Property | Value |
| --- | --- |
| id | norm_cb_23_passports |
| name | CB'23 passports |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Niederlande (land_niederlande) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_cb_23_passports__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_nl_holz | Niederlande × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_holz__REFERENZIERT_NORM__norm_cb_23_passports"} |


### CEN/TS 1090-201

| Property | Value |
| --- | --- |
| id | norm_cen_ts_1090_201 |
| name | CEN/TS 1090-201 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien), Deutschland (land_deutschland), Niederlande (land_niederlande), Schweiz (land_schweiz) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_cen_ts_1090_201__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_stahl | Belgien × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_stahl__REFERENZIERT_NORM__norm_cen_ts_1090_201"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_stahl | Deutschland × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_stahl__REFERENZIERT_NORM__norm_cen_ts_1090_201"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_nl_stahl | Niederlande × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_stahl__REFERENZIERT_NORM__norm_cen_ts_1090_201"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_ch_stahl | Schweiz × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_stahl__REFERENZIERT_NORM__norm_cen_ts_1090_201"} |


### CEN/TS 1090-201:2024

| Property | Value |
| --- | --- |
| beschreibung | European CEN technical specification, country-level fanout removed pending dedicated source confirmation. |
| id | norm_cen_ts_1090_201_2024 |
| name | CEN/TS 1090-201:2024 |
| name_full | CEN/TS 1090-201:2024 — Assessment of Reclaimed Structural Steel |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | HAT_GELTUNGSBEREICH | Geltungsbereich | geltungsbereich_cen_ts_europaeisch | CEN Technical Specification europaeischer Deliverable-Raum | {"evidence_confidence": "teilweise_belegt", "id": "norm_cen_ts_1090_201_2024__HAT_GELTUNGSBEREICH__geltungsbereich_cen_ts_europaeisch"} |


### CEN/TS 17440

| Property | Value |
| --- | --- |
| beschreibung | European CEN technical specification, country-level fanout removed pending dedicated source confirmation. |
| id | norm_cen_ts_17440 |
| name | CEN/TS 17440 |
| name_full | CEN/TS 17440 — Assessment of Existing Structures |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | HAT_GELTUNGSBEREICH | Geltungsbereich | geltungsbereich_cen_ts_europaeisch | CEN Technical Specification europaeischer Deliverable-Raum | {"evidence_confidence": "teilweise_belegt", "id": "norm_cen_ts_17440__HAT_GELTUNGSBEREICH__geltungsbereich_cen_ts_europaeisch"} |


### CROW-CUR 4:2023

| Property | Value |
| --- | --- |
| id | norm_crow_cur_4_2023 |
| name | CROW-CUR 4:2023 |
| name_full | CROW-CUR Guideline 4:2023 Reuse of hollow core slabs |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Niederlande (land_niederlande) |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country |  |
| BG Projekt country | Finnland (land_finnland), Niederlande (land_niederlande) |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | GILT_IN_LAND | Land | land_niederlande | Niederlande | {"evidence_confidence": "unklar", "id": "r_norm_crow_cur_4_2023__GILT_IN_LAND__land_niederlande"} |
| -> | HAT_BAUTEILTYP | Bauteiltyp | bt_decke | Decke | {"evidence_confidence": "unklar", "id": "r_norm_crow_cur_4_2023__HAT_BAUTEILTYP__bt_decke"} |
| -> | HAT_LEISTUNGSANFORDERUNG | Leistungsanforderung | la_tragfaehigkeit | Tragfaehigkeit | {"evidence_confidence": "unklar", "id": "r_norm_crow_cur_4_2023__HAT_LEISTUNGSANFORDERUNG__la_tragfaehigkeit"} |
| -> | HAT_METHODE | Methode | meth_bestands_und_reuse_assessment | Bestands_und_ReUse_Assessment | {"evidence_confidence": "unklar", "legacy_methode_id": "meth_reuse_assessment", "legacy_methode_name": "ReUse_Assessment", "legacy_rel_id": "r_norm_crow_cur_4_2023__HAT_METHODE__meth_reuse_assessment", "migrated_at": "2026-06-03T23:47:06.160000000+00:00", "review_run": "taxonomy_integration_2026_06_03_phase6_1"} |
| <- | REFERENZIERT_NORM | Bauteilgruppe | bg_stahlbeton_mehrere_lokomotion_hollow_core_slabs | 27 wiederve… (Lokomotion) | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahlbeton_mehrere_lokomotion_hollow_core_slabs__REFERENZIERT_NORM__norm_crow_cur_4_2023"} |
| <- | REFERENZIERT_NORM | Norm | norm_en_1168 | EN 1168 | {"evidence_confidence": "unklar", "id": "r_norm_en_1168__REFERENZIERT_NORM__norm_crow_cur_4_2023"} |
| <- | REFERENZIERT_NORM | Bauteilgruppe | bg_stahlbeton_decke_ccn_hollow_core_slabs | Hohlkoerperdecken | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahlbeton_decke_ccn_hollow_core_slabs__REFERENZIERT_NORM__norm_crow_cur_4_2023"} |
| -> | REFERENZIERT_NORM | Norm | norm_en_1168 | EN 1168 | {"evidence_confidence": "unklar", "id": "r_norm_crow_cur_4_2023__REFERENZIERT_NORM__norm_en_1168"} |


### DIBt/MVV TB

| Property | Value |
| --- | --- |
| id | norm_dibt_mvv_tb |
| name | DIBt/MVV TB |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_dibt_mvv_tb__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_beton | Deutschland × Beton reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_beton__REFERENZIERT_NORM__norm_dibt_mvv_tb"} |


### DIN 18008

| Property | Value |
| --- | --- |
| beschreibung | German design code for structural and façade glass. |
| country_short | DE |
| id | norm_din_18008 |
| name | DIN 18008 |
| name_full | DIN 18008 — Glass in building, design and execution (DE) |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Deutschland (land_deutschland) |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | GILT_IN_LAND | Land | land_deutschland | Deutschland | {"evidence_confidence": "unklar", "id": "r_norm_din_18008__GILT_IN_LAND__land_deutschland"} |


### DIN 18940 family

| Property | Value |
| --- | --- |
| id | norm_din_18940_family |
| name | DIN 18940 family |
| name_full | DIN 18940/18945/18946/18947 family |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_18940_family__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_lehm | Deutschland × Lehm reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_lehm__REFERENZIERT_NORM__norm_din_18940"} |


### DIN 18945

| Property | Value |
| --- | --- |
| id | norm_din_18945 |
| name | DIN 18945 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_18945__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_lehm | Deutschland × Lehm reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_lehm__REFERENZIERT_NORM__norm_din_18945"} |


### DIN 18946

| Property | Value |
| --- | --- |
| id | norm_din_18946 |
| name | DIN 18946 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_18946__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_lehm | Deutschland × Lehm reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_lehm__REFERENZIERT_NORM__norm_din_18946"} |


### DIN 18947

| Property | Value |
| --- | --- |
| id | norm_din_18947 |
| name | DIN 18947 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_18947__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_lehm | Deutschland × Lehm reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_lehm__REFERENZIERT_NORM__norm_din_18947"} |


### DIN 4074

| Property | Value |
| --- | --- |
| beschreibung | German visual strength-grading rules for structural sawn timber. |
| country_short | DE |
| id | norm_din_4074 |
| name | DIN 4074 |
| name_full | DIN 4074 — Visual strength grading of structural timber (DE) |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Deutschland (land_deutschland) |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | GILT_IN_LAND | Land | land_deutschland | Deutschland | {"evidence_confidence": "unklar", "id": "r_norm_din_4074__GILT_IN_LAND__land_deutschland"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_holz | Deutschland × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_holz__REFERENZIERT_NORM__norm_din_4074"} |


### DIN 68800

| Property | Value |
| --- | --- |
| beschreibung | German wood-protection standard; relevant for reused exterior/structural timber. |
| country_short | DE |
| id | norm_din_68800 |
| name | DIN 68800 |
| name_full | DIN 68800 — Wood preservation and durability classes (DE) |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Deutschland (land_deutschland) |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | GILT_IN_LAND | Land | land_deutschland | Deutschland | {"evidence_confidence": "unklar", "id": "r_norm_din_68800__GILT_IN_LAND__land_deutschland"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_holz | Deutschland × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_holz__REFERENZIERT_NORM__norm_din_68800"} |


### DIN EN 1090-2

| Property | Value |
| --- | --- |
| id | norm_din_en_1090_2 |
| name | DIN EN 1090-2 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_en_1090_2__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_stahl | Deutschland × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_stahl__REFERENZIERT_NORM__norm_din_en_1090_2"} |


### DIN EN 1168

| Property | Value |
| --- | --- |
| id | norm_din_en_1168 |
| name | DIN EN 1168 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_en_1168__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_beton | Deutschland × Beton reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_beton__REFERENZIERT_NORM__norm_din_en_1168"} |


### DIN EN 13369

| Property | Value |
| --- | --- |
| id | norm_din_en_13369 |
| name | DIN EN 13369 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_en_13369__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_beton | Deutschland × Beton reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_beton__REFERENZIERT_NORM__norm_din_en_13369"} |


### DIN EN 14081

| Property | Value |
| --- | --- |
| id | norm_din_en_14081 |
| name | DIN EN 14081 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_en_14081__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_holz | Deutschland × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_holz__REFERENZIERT_NORM__norm_din_en_14081"} |


### DIN EN 15804

| Property | Value |
| --- | --- |
| id | norm_din_en_15804 |
| name | DIN EN 15804 |
| name_full | DIN_EN_15804 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country | Dänemark (land_daenemark), Norwegen (land_norwegen), Schweiz (land_schweiz), Vereinigtes Königreich (land_vereinigtes_koenigreich) |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| <- | METHODENGRUNDLAGE_NORM | LCAModule | lz_a1_a3 | A1-A3 Produkt | {"evidence_confidence": "unklar", "id": "r_lz_a1_a3__METHODENGRUNDLAGE_NORM__norm_din_en_15804"} |
| <- | METHODENGRUNDLAGE_NORM | LCAModule | lz_d | D Beyond (Reuse) | {"evidence_confidence": "unklar", "id": "r_lz_d__METHODENGRUNDLAGE_NORM__norm_din_en_15804"} |
| <- | REFERENZIERT_NORM | Projekt | p_55_great_suffolk_street_london | 55 Great Suffolk Street | {"evidence_confidence": "teilweise_belegt", "id": "r_p_55_great_suffolk_street_london__REFERENZIERT_NORM__norm_din_en_15804"} |
| <- | REFERENZIERT_NORM | Projekt | p_brent_cross_town_primary_substation_london | Brent Cross Town… | {"evidence_confidence": "teilweise_belegt", "id": "r_p_brent_cross_town_primary_substation_london__REFERENZIERT_NORM__norm_din_en_15804"} |
| <- | REFERENZIERT_NORM | Projekt | p_k118_kopfbau_halle_118_winterthur | K.118 Winterthur | {"evidence_confidence": "teilweise_belegt", "id": "r_p_k118_kopfbau_halle_118_winterthur__REFERENZIERT_NORM__norm_din_en_15804"} |
| <- | REFERENZIERT_NORM | Projekt | p_ka13_kristian_augusts_gate_13_oslo | KA13 | {"evidence_confidence": "teilweise_belegt", "id": "r_p_ka13_kristian_augusts_gate_13_oslo__REFERENZIERT_NORM__norm_din_en_15804"} |
| <- | REFERENZIERT_NORM | Projekt | p_resource_rows_copenhagen | Resource Rows | {"evidence_confidence": "teilweise_belegt", "id": "r_p_resource_rows_copenhagen__REFERENZIERT_NORM__norm_din_en_15804"} |
| <- | REFERENZIERT_NORM | Projekt | p_thoravej_29_copenhagen | Thoravej 29 Copenhagen | {"evidence_confidence": "teilweise_belegt", "id": "r_p_thoravej_29_copenhagen__REFERENZIERT_NORM__norm_din_en_15804"} |


### DIN EN 15978

| Property | Value |
| --- | --- |
| id | norm_din_en_15978 |
| name | DIN EN 15978 |
| name_full | DIN_EN_15978 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country | Dänemark (land_daenemark), Norwegen (land_norwegen), Vereinigtes Königreich (land_vereinigtes_koenigreich) |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| <- | METHODENGRUNDLAGE_NORM | LCAModule | lz_a4_a5 | A4-A5 Errichtung | {"evidence_confidence": "unklar", "id": "r_lz_a4_a5__METHODENGRUNDLAGE_NORM__norm_din_en_15978"} |
| <- | METHODENGRUNDLAGE_NORM | LCAModule | lz_b | B1-B7 Nutzung | {"evidence_confidence": "unklar", "id": "r_lz_b__METHODENGRUNDLAGE_NORM__norm_din_en_15978"} |
| <- | METHODENGRUNDLAGE_NORM | LCAModule | lz_c | C1-C4 End-of-Life | {"evidence_confidence": "unklar", "id": "r_lz_c__METHODENGRUNDLAGE_NORM__norm_din_en_15978"} |
| <- | METHODENGRUNDLAGE_NORM | LCAModule | lz_d | D Beyond (Reuse) | {"evidence_confidence": "unklar", "id": "r_lz_d__METHODENGRUNDLAGE_NORM__norm_din_en_15978"} |
| <- | REFERENZIERT_NORM | Projekt | p_55_great_suffolk_street_london | 55 Great Suffolk Street | {"evidence_confidence": "teilweise_belegt", "id": "r_p_55_great_suffolk_street_london__REFERENZIERT_NORM__norm_din_en_15978"} |
| <- | REFERENZIERT_NORM | Projekt | p_brent_cross_town_primary_substation_london | Brent Cross Town… | {"evidence_confidence": "teilweise_belegt", "id": "r_p_brent_cross_town_primary_substation_london__REFERENZIERT_NORM__norm_din_en_15978"} |
| <- | REFERENZIERT_NORM | Projekt | p_ka13_kristian_augusts_gate_13_oslo | KA13 | {"evidence_confidence": "teilweise_belegt", "id": "r_p_ka13_kristian_augusts_gate_13_oslo__REFERENZIERT_NORM__norm_din_en_15978"} |
| <- | REFERENZIERT_NORM | Projekt | p_resource_rows_copenhagen | Resource Rows | {"evidence_confidence": "teilweise_belegt", "id": "r_p_resource_rows_copenhagen__REFERENZIERT_NORM__norm_din_en_15978"} |
| <- | REFERENZIERT_NORM | Projekt | p_thoravej_29_copenhagen | Thoravej 29 Copenhagen | {"evidence_confidence": "teilweise_belegt", "id": "r_p_thoravej_29_copenhagen__REFERENZIERT_NORM__norm_din_en_15978"} |


### DIN EN 1993

| Property | Value |
| --- | --- |
| id | norm_din_en_1993 |
| name | DIN EN 1993 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_en_1993__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_stahl | Deutschland × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_stahl__REFERENZIERT_NORM__norm_din_en_1993"} |


### DIN EN 1996

| Property | Value |
| --- | --- |
| id | norm_din_en_1996 |
| name | DIN EN 1996 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_en_1996__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_ziegel | Deutschland × Ziegel reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_ziegel__REFERENZIERT_NORM__norm_din_en_1996"} |


### DIN EN 206

| Property | Value |
| --- | --- |
| id | norm_din_en_206 |
| name | DIN EN 206 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_en_206__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_beton | Deutschland × Beton reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_beton__REFERENZIERT_NORM__norm_din_en_206"} |


### DIN EN 338

| Property | Value |
| --- | --- |
| id | norm_din_en_338 |
| name | DIN EN 338 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_din_en_338__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_holz | Deutschland × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_holz__REFERENZIERT_NORM__norm_din_en_338"} |


### EN 1090

| Property | Value |
| --- | --- |
| beschreibung | EN national standard adoption across CEN/CENELEC members, country links reflect available member countries in this graph. |
| country_short | CEN |
| id | norm_en_1090 |
| name | EN 1090 |
| name_full | EN_1090 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Belgien (land_belgien), Deutschland (land_deutschland), Dänemark (land_daenemark), Finnland (land_finnland), Frankreich (land_frankreich), Italien (land_italien), Luxemburg (land_luxemburg), Niederlande (land_niederlande), Norwegen (land_norwegen), Portugal (land_portugal), Schweiz (land_schweiz), Vereinigtes Königreich (land_vereinigtes_koenigreich), Österreich (land_oesterreich) |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country |  |
| BG Projekt country | Vereinigtes Königreich (land_vereinigtes_koenigreich) |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | GILT_IN_LAND | Land | land_belgien | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_belgien"} |
| -> | GILT_IN_LAND | Land | land_deutschland | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_deutschland"} |
| -> | GILT_IN_LAND | Land | land_daenemark | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_daenemark"} |
| -> | GILT_IN_LAND | Land | land_finnland | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_finnland"} |
| -> | GILT_IN_LAND | Land | land_frankreich | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_frankreich"} |
| -> | GILT_IN_LAND | Land | land_italien | Italien | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_italien"} |
| -> | GILT_IN_LAND | Land | land_luxemburg | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_luxemburg"} |
| -> | GILT_IN_LAND | Land | land_niederlande | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_niederlande"} |
| -> | GILT_IN_LAND | Land | land_norwegen | Norwegen | {"evidence_confidence": "belegt", "id": "norm_en_1090__GILT_IN_LAND__land_norwegen"} |
| -> | GILT_IN_LAND | Land | land_portugal | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_portugal"} |
| -> | GILT_IN_LAND | Land | land_schweiz | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_1090__GILT_IN_LAND__land_schweiz"} |
| -> | GILT_IN_LAND | Land | land_vereinigtes_koenigreich | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_1090__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| -> | GILT_IN_LAND | Land | land_oesterreich | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_1090__GILT_IN_LAND__land_oesterreich"} |
| -> | HAT_GELTUNGSBEREICH | Geltungsbereich | geltungsbereich_en_cen_cenelec_mitglieder | EN in CEN/CENELEC Mitgliedslaendern | {"evidence_confidence": "belegt", "id": "norm_en_1090__HAT_GELTUNGSBEREICH__geltungsbereich_en_cen_cenelec_mitglieder"} |
| <- | REFERENZIERT_NORM | Bauteilgruppe | bg_stahl_mehrere_holbein_structural | Stahlträger un… (Holbein) | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahl_mehrere_holbein_structural__REFERENZIERT_NORM__norm_en_1090"} |
| <- | REFERENZIERT_NORM | Bauteilgruppe | bg_stahl_mehrere_55gss_external_core | Steel profiles for… | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahl_mehrere_55gss_external_core__REFERENZIERT_NORM__norm_en_1090"} |


### EN 1090-2

| Property | Value |
| --- | --- |
| id | norm_en_1090_2 |
| name | EN 1090-2 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien), Vereinigtes Königreich (land_vereinigtes_koenigreich) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_1090_2__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_stahl | Belgien × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_stahl__REFERENZIERT_NORM__norm_en_1090_2"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_gb_stahl | Vereinigtes Königreich × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_stahl__REFERENZIERT_NORM__norm_en_1090_2"} |


### EN 1168

| Property | Value |
| --- | --- |
| beschreibung | EN national standard adoption across CEN/CENELEC members, country links reflect available member countries in this graph. |
| country_short | CEN |
| id | norm_en_1168 |
| name | EN 1168 |
| name_full | EN 1168 Precast concrete products - Hollow core slabs |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Belgien (land_belgien), Deutschland (land_deutschland), Dänemark (land_daenemark), Finnland (land_finnland), Frankreich (land_frankreich), Italien (land_italien), Luxemburg (land_luxemburg), Niederlande (land_niederlande), Norwegen (land_norwegen), Portugal (land_portugal), Schweiz (land_schweiz), Vereinigtes Königreich (land_vereinigtes_koenigreich), Österreich (land_oesterreich) |
| ReuseRule APPLIES_IN | Belgien (land_belgien), Finnland (land_finnland), Niederlande (land_niederlande), Norwegen (land_norwegen) |
| Direct Projekt country |  |
| BG Projekt country | Finnland (land_finnland) |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | GILT_IN_LAND | Land | land_belgien | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_belgien"} |
| -> | GILT_IN_LAND | Land | land_deutschland | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_deutschland"} |
| -> | GILT_IN_LAND | Land | land_daenemark | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_daenemark"} |
| -> | GILT_IN_LAND | Land | land_finnland | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_finnland"} |
| -> | GILT_IN_LAND | Land | land_frankreich | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_frankreich"} |
| -> | GILT_IN_LAND | Land | land_italien | Italien | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_italien"} |
| -> | GILT_IN_LAND | Land | land_luxemburg | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_luxemburg"} |
| -> | GILT_IN_LAND | Land | land_niederlande | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_niederlande"} |
| -> | GILT_IN_LAND | Land | land_norwegen | Norwegen | {"evidence_confidence": "belegt", "id": "norm_en_1168__GILT_IN_LAND__land_norwegen"} |
| -> | GILT_IN_LAND | Land | land_portugal | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_portugal"} |
| -> | GILT_IN_LAND | Land | land_schweiz | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_1168__GILT_IN_LAND__land_schweiz"} |
| -> | GILT_IN_LAND | Land | land_vereinigtes_koenigreich | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_1168__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| -> | GILT_IN_LAND | Land | land_oesterreich | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_1168__GILT_IN_LAND__land_oesterreich"} |
| -> | HAT_GELTUNGSBEREICH | Geltungsbereich | geltungsbereich_en_cen_cenelec_mitglieder | EN in CEN/CENELEC Mitgliedslaendern | {"evidence_confidence": "belegt", "id": "norm_en_1168__HAT_GELTUNGSBEREICH__geltungsbereich_en_cen_cenelec_mitglieder"} |
| <- | REFERENZIERT_NORM | Bauteilgruppe | bg_stahlbeton_mehrere_lokomotion_hollow_core_slabs | 27 wiederve… (Lokomotion) | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahlbeton_mehrere_lokomotion_hollow_core_slabs__REFERENZIERT_NORM__norm_en_1168"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_beton | Belgien × Beton reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_beton__REFERENZIERT_NORM__norm_en_1168"} |
| <- | REFERENZIERT_NORM | Norm | norm_crow_cur_4_2023 | CROW-CUR 4:2023 | {"evidence_confidence": "unklar", "id": "r_norm_crow_cur_4_2023__REFERENZIERT_NORM__norm_en_1168"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_fi_beton_hollow_core_slabs | Finnland × Beton / hollow-core slabs reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_fi_beton_hollow_core_slabs__REFERENZIERT_NORM__norm_en_1168"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_nl_beton | Niederlande × Beton reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_beton__REFERENZIERT_NORM__norm_en_1168"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_no_beton_hollow_core_slabs | Norwegen × Beton / hollow-core slabs reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_no_beton_hollow_core_slabs__REFERENZIERT_NORM__norm_en_1168"} |
| -> | REFERENZIERT_NORM | Norm | norm_crow_cur_4_2023 | CROW-CUR 4:2023 | {"evidence_confidence": "unklar", "id": "r_norm_en_1168__REFERENZIERT_NORM__norm_crow_cur_4_2023"} |


### EN 12058

| Property | Value |
| --- | --- |
| id | norm_en_12058 |
| name | EN 12058 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_12058__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_naturstein | Belgien × Naturstein reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_naturstein__REFERENZIERT_NORM__norm_en_12058"} |


### EN 12371

| Property | Value |
| --- | --- |
| id | norm_en_12371 |
| name | EN 12371 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_12371__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_naturstein | Belgien × Naturstein reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_naturstein__REFERENZIERT_NORM__norm_en_12371"} |


### EN 12372

| Property | Value |
| --- | --- |
| id | norm_en_12372 |
| name | EN 12372 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_12372__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_naturstein | Belgien × Naturstein reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_naturstein__REFERENZIERT_NORM__norm_en_12372"} |


### EN 13162

| Property | Value |
| --- | --- |
| beschreibung | EN national standard adoption across CEN/CENELEC members, country links reflect available member countries in this graph. |
| country_short | CEN |
| id | norm_en_13162 |
| name | EN 13162 |
| name_full | EN 13162 — Factory-made mineral wool thermal insulation |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Belgien (land_belgien), Deutschland (land_deutschland), Dänemark (land_daenemark), Finnland (land_finnland), Frankreich (land_frankreich), Italien (land_italien), Luxemburg (land_luxemburg), Niederlande (land_niederlande), Norwegen (land_norwegen), Portugal (land_portugal), Schweiz (land_schweiz), Vereinigtes Königreich (land_vereinigtes_koenigreich), Österreich (land_oesterreich) |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | GILT_IN_LAND | Land | land_belgien | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_belgien"} |
| -> | GILT_IN_LAND | Land | land_deutschland | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_deutschland"} |
| -> | GILT_IN_LAND | Land | land_daenemark | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_daenemark"} |
| -> | GILT_IN_LAND | Land | land_finnland | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_finnland"} |
| -> | GILT_IN_LAND | Land | land_frankreich | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_frankreich"} |
| -> | GILT_IN_LAND | Land | land_italien | Italien | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_italien"} |
| -> | GILT_IN_LAND | Land | land_luxemburg | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_luxemburg"} |
| -> | GILT_IN_LAND | Land | land_niederlande | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_niederlande"} |
| -> | GILT_IN_LAND | Land | land_norwegen | Norwegen | {"evidence_confidence": "belegt", "id": "norm_en_13162__GILT_IN_LAND__land_norwegen"} |
| -> | GILT_IN_LAND | Land | land_portugal | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_portugal"} |
| -> | GILT_IN_LAND | Land | land_schweiz | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_13162__GILT_IN_LAND__land_schweiz"} |
| -> | GILT_IN_LAND | Land | land_vereinigtes_koenigreich | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_13162__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| -> | GILT_IN_LAND | Land | land_oesterreich | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_13162__GILT_IN_LAND__land_oesterreich"} |
| -> | HAT_GELTUNGSBEREICH | Geltungsbereich | geltungsbereich_en_cen_cenelec_mitglieder | EN in CEN/CENELEC Mitgliedslaendern | {"evidence_confidence": "belegt", "id": "norm_en_13162__HAT_GELTUNGSBEREICH__geltungsbereich_en_cen_cenelec_mitglieder"} |


### EN 13224

| Property | Value |
| --- | --- |
| id | norm_en_13224 |
| name | EN 13224 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_13224__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_beton | Belgien × Beton reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_beton__REFERENZIERT_NORM__norm_en_13224"} |


### EN 13369

| Property | Value |
| --- | --- |
| id | norm_en_13369 |
| name | EN 13369 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien), Niederlande (land_niederlande) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_13369__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_beton | Belgien × Beton reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_beton__REFERENZIERT_NORM__norm_en_13369"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_nl_beton | Niederlande × Beton reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_beton__REFERENZIERT_NORM__norm_en_13369"} |


### EN 1341

| Property | Value |
| --- | --- |
| id | norm_en_1341 |
| name | EN 1341 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_1341__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_naturstein | Belgien × Naturstein reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_naturstein__REFERENZIERT_NORM__norm_en_1341"} |


### EN 13747

| Property | Value |
| --- | --- |
| id | norm_en_13747 |
| name | EN 13747 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_13747__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_beton | Belgien × Beton reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_beton__REFERENZIERT_NORM__norm_en_13747"} |


### EN 13755

| Property | Value |
| --- | --- |
| id | norm_en_13755 |
| name | EN 13755 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_13755__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_naturstein | Belgien × Naturstein reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_naturstein__REFERENZIERT_NORM__norm_en_13755"} |


### EN 14081

| Property | Value |
| --- | --- |
| beschreibung | EN national standard adoption across CEN/CENELEC members, country links reflect available member countries in this graph. |
| country_short | CEN |
| id | norm_en_14081 |
| name | EN 14081 |
| name_full | EN 14081 — Strength-graded structural timber |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Belgien (land_belgien), Deutschland (land_deutschland), Dänemark (land_daenemark), Finnland (land_finnland), Frankreich (land_frankreich), Italien (land_italien), Luxemburg (land_luxemburg), Niederlande (land_niederlande), Norwegen (land_norwegen), Portugal (land_portugal), Schweiz (land_schweiz), Vereinigtes Königreich (land_vereinigtes_koenigreich), Österreich (land_oesterreich) |
| ReuseRule APPLIES_IN | Vereinigtes Königreich (land_vereinigtes_koenigreich) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | GILT_IN_LAND | Land | land_belgien | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_belgien"} |
| -> | GILT_IN_LAND | Land | land_deutschland | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_deutschland"} |
| -> | GILT_IN_LAND | Land | land_daenemark | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_daenemark"} |
| -> | GILT_IN_LAND | Land | land_finnland | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_finnland"} |
| -> | GILT_IN_LAND | Land | land_frankreich | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_frankreich"} |
| -> | GILT_IN_LAND | Land | land_italien | Italien | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_italien"} |
| -> | GILT_IN_LAND | Land | land_luxemburg | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_luxemburg"} |
| -> | GILT_IN_LAND | Land | land_niederlande | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_niederlande"} |
| -> | GILT_IN_LAND | Land | land_norwegen | Norwegen | {"evidence_confidence": "belegt", "id": "norm_en_14081__GILT_IN_LAND__land_norwegen"} |
| -> | GILT_IN_LAND | Land | land_portugal | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_portugal"} |
| -> | GILT_IN_LAND | Land | land_schweiz | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_14081__GILT_IN_LAND__land_schweiz"} |
| -> | GILT_IN_LAND | Land | land_vereinigtes_koenigreich | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_14081__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| -> | GILT_IN_LAND | Land | land_oesterreich | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_14081__GILT_IN_LAND__land_oesterreich"} |
| -> | HAT_GELTUNGSBEREICH | Geltungsbereich | geltungsbereich_en_cen_cenelec_mitglieder | EN in CEN/CENELEC Mitgliedslaendern | {"evidence_confidence": "belegt", "id": "norm_en_14081__HAT_GELTUNGSBEREICH__geltungsbereich_en_cen_cenelec_mitglieder"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_gb_holz | Vereinigtes Königreich × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_holz__REFERENZIERT_NORM__norm_en_14081"} |


### EN 14231

| Property | Value |
| --- | --- |
| id | norm_en_14231 |
| name | EN 14231 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_14231__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_naturstein | Belgien × Naturstein reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_naturstein__REFERENZIERT_NORM__norm_en_14231"} |


### EN 1469

| Property | Value |
| --- | --- |
| id | norm_en_1469 |
| name | EN 1469 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_1469__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_naturstein | Belgien × Naturstein reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_naturstein__REFERENZIERT_NORM__norm_en_1469"} |


### EN 1936

| Property | Value |
| --- | --- |
| id | norm_en_1936 |
| name | EN 1936 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_1936__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_naturstein | Belgien × Naturstein reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_naturstein__REFERENZIERT_NORM__norm_en_1936"} |


### EN 1992 (Eurocode 2)

| Property | Value |
| --- | --- |
| beschreibung | Eurocode adoption across EU/EFTA states and the United Kingdom, country links reflect available countries in this graph. |
| country_short | EU/EFTA+UK |
| id | norm_en_1992 |
| name | EN 1992 (Eurocode 2) |
| name_full | EN 1992 — Eurocode 2 (Concrete structures) |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Belgien (land_belgien), Deutschland (land_deutschland), Dänemark (land_daenemark), Finnland (land_finnland), Frankreich (land_frankreich), Italien (land_italien), Luxemburg (land_luxemburg), Niederlande (land_niederlande), Norwegen (land_norwegen), Portugal (land_portugal), Schweiz (land_schweiz), Vereinigtes Königreich (land_vereinigtes_koenigreich), Österreich (land_oesterreich) |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | GILT_IN_LAND | Land | land_belgien | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_belgien"} |
| -> | GILT_IN_LAND | Land | land_deutschland | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_deutschland"} |
| -> | GILT_IN_LAND | Land | land_daenemark | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_daenemark"} |
| -> | GILT_IN_LAND | Land | land_finnland | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_finnland"} |
| -> | GILT_IN_LAND | Land | land_frankreich | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_frankreich"} |
| -> | GILT_IN_LAND | Land | land_italien | Italien | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_italien"} |
| -> | GILT_IN_LAND | Land | land_luxemburg | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_luxemburg"} |
| -> | GILT_IN_LAND | Land | land_niederlande | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_niederlande"} |
| -> | GILT_IN_LAND | Land | land_norwegen | Norwegen | {"evidence_confidence": "belegt", "id": "norm_en_1992__GILT_IN_LAND__land_norwegen"} |
| -> | GILT_IN_LAND | Land | land_portugal | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_portugal"} |
| -> | GILT_IN_LAND | Land | land_schweiz | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_1992__GILT_IN_LAND__land_schweiz"} |
| -> | GILT_IN_LAND | Land | land_vereinigtes_koenigreich | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_1992__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| -> | GILT_IN_LAND | Land | land_oesterreich | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_1992__GILT_IN_LAND__land_oesterreich"} |
| -> | HAT_GELTUNGSBEREICH | Geltungsbereich | geltungsbereich_eurocodes_eu_efta_uk | Eurocodes in EU/EFTA plus Vereinigtes Koenigreich | {"evidence_confidence": "belegt", "id": "norm_en_1992__HAT_GELTUNGSBEREICH__geltungsbereich_eurocodes_eu_efta_uk"} |


### EN 1993 (Eurocode 3)

| Property | Value |
| --- | --- |
| beschreibung | Eurocode adoption across EU/EFTA states and the United Kingdom, country links reflect available countries in this graph. |
| country_short | EU/EFTA+UK |
| id | norm_en_1993 |
| name | EN 1993 (Eurocode 3) |
| name_full | EN 1993 — Eurocode 3 (Steel structures) |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Belgien (land_belgien), Deutschland (land_deutschland), Dänemark (land_daenemark), Finnland (land_finnland), Frankreich (land_frankreich), Italien (land_italien), Luxemburg (land_luxemburg), Niederlande (land_niederlande), Norwegen (land_norwegen), Portugal (land_portugal), Schweiz (land_schweiz), Vereinigtes Königreich (land_vereinigtes_koenigreich), Österreich (land_oesterreich) |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | GILT_IN_LAND | Land | land_belgien | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_belgien"} |
| -> | GILT_IN_LAND | Land | land_deutschland | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_deutschland"} |
| -> | GILT_IN_LAND | Land | land_daenemark | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_daenemark"} |
| -> | GILT_IN_LAND | Land | land_finnland | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_finnland"} |
| -> | GILT_IN_LAND | Land | land_frankreich | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_frankreich"} |
| -> | GILT_IN_LAND | Land | land_italien | Italien | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_italien"} |
| -> | GILT_IN_LAND | Land | land_luxemburg | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_luxemburg"} |
| -> | GILT_IN_LAND | Land | land_niederlande | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_niederlande"} |
| -> | GILT_IN_LAND | Land | land_norwegen | Norwegen | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_norwegen"} |
| -> | GILT_IN_LAND | Land | land_portugal | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_portugal"} |
| -> | GILT_IN_LAND | Land | land_schweiz | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_1993__GILT_IN_LAND__land_schweiz"} |
| -> | GILT_IN_LAND | Land | land_vereinigtes_koenigreich | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_1993__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| -> | GILT_IN_LAND | Land | land_oesterreich | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_1993__GILT_IN_LAND__land_oesterreich"} |
| -> | HAT_GELTUNGSBEREICH | Geltungsbereich | geltungsbereich_eurocodes_eu_efta_uk | Eurocodes in EU/EFTA plus Vereinigtes Koenigreich | {"evidence_confidence": "belegt", "id": "norm_en_1993__HAT_GELTUNGSBEREICH__geltungsbereich_eurocodes_eu_efta_uk"} |


### EN 1995 (Eurocode 5)

| Property | Value |
| --- | --- |
| beschreibung | Eurocode adoption across EU/EFTA states and the United Kingdom, country links reflect available countries in this graph. |
| country_short | EU/EFTA+UK |
| id | norm_en_1995 |
| name | EN 1995 (Eurocode 5) |
| name_full | EN 1995 — Eurocode 5 (Timber structures) |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Belgien (land_belgien), Deutschland (land_deutschland), Dänemark (land_daenemark), Finnland (land_finnland), Frankreich (land_frankreich), Italien (land_italien), Luxemburg (land_luxemburg), Niederlande (land_niederlande), Norwegen (land_norwegen), Portugal (land_portugal), Schweiz (land_schweiz), Vereinigtes Königreich (land_vereinigtes_koenigreich), Österreich (land_oesterreich) |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | GILT_IN_LAND | Land | land_belgien | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_belgien"} |
| -> | GILT_IN_LAND | Land | land_deutschland | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_deutschland"} |
| -> | GILT_IN_LAND | Land | land_daenemark | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_daenemark"} |
| -> | GILT_IN_LAND | Land | land_finnland | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_finnland"} |
| -> | GILT_IN_LAND | Land | land_frankreich | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_frankreich"} |
| -> | GILT_IN_LAND | Land | land_italien | Italien | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_italien"} |
| -> | GILT_IN_LAND | Land | land_luxemburg | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_luxemburg"} |
| -> | GILT_IN_LAND | Land | land_niederlande | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_niederlande"} |
| -> | GILT_IN_LAND | Land | land_norwegen | Norwegen | {"evidence_confidence": "belegt", "id": "norm_en_1995__GILT_IN_LAND__land_norwegen"} |
| -> | GILT_IN_LAND | Land | land_portugal | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_portugal"} |
| -> | GILT_IN_LAND | Land | land_schweiz | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_1995__GILT_IN_LAND__land_schweiz"} |
| -> | GILT_IN_LAND | Land | land_vereinigtes_koenigreich | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_1995__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| -> | GILT_IN_LAND | Land | land_oesterreich | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_1995__GILT_IN_LAND__land_oesterreich"} |
| -> | HAT_GELTUNGSBEREICH | Geltungsbereich | geltungsbereich_eurocodes_eu_efta_uk | Eurocodes in EU/EFTA plus Vereinigtes Koenigreich | {"evidence_confidence": "belegt", "id": "norm_en_1995__HAT_GELTUNGSBEREICH__geltungsbereich_eurocodes_eu_efta_uk"} |


### EN 1996 (Eurocode 6)

| Property | Value |
| --- | --- |
| beschreibung | Eurocode adoption across EU/EFTA states and the United Kingdom, country links reflect available countries in this graph. |
| country_short | EU/EFTA+UK |
| id | norm_en_1996 |
| name | EN 1996 (Eurocode 6) |
| name_full | EN 1996 — Eurocode 6 (Masonry structures) |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Belgien (land_belgien), Deutschland (land_deutschland), Dänemark (land_daenemark), Finnland (land_finnland), Frankreich (land_frankreich), Italien (land_italien), Luxemburg (land_luxemburg), Niederlande (land_niederlande), Norwegen (land_norwegen), Portugal (land_portugal), Schweiz (land_schweiz), Vereinigtes Königreich (land_vereinigtes_koenigreich), Österreich (land_oesterreich) |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | GILT_IN_LAND | Land | land_belgien | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_belgien"} |
| -> | GILT_IN_LAND | Land | land_deutschland | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_deutschland"} |
| -> | GILT_IN_LAND | Land | land_daenemark | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_daenemark"} |
| -> | GILT_IN_LAND | Land | land_finnland | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_finnland"} |
| -> | GILT_IN_LAND | Land | land_frankreich | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_frankreich"} |
| -> | GILT_IN_LAND | Land | land_italien | Italien | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_italien"} |
| -> | GILT_IN_LAND | Land | land_luxemburg | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_luxemburg"} |
| -> | GILT_IN_LAND | Land | land_niederlande | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_niederlande"} |
| -> | GILT_IN_LAND | Land | land_norwegen | Norwegen | {"evidence_confidence": "belegt", "id": "norm_en_1996__GILT_IN_LAND__land_norwegen"} |
| -> | GILT_IN_LAND | Land | land_portugal | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_portugal"} |
| -> | GILT_IN_LAND | Land | land_schweiz | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_1996__GILT_IN_LAND__land_schweiz"} |
| -> | GILT_IN_LAND | Land | land_vereinigtes_koenigreich | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_1996__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| -> | GILT_IN_LAND | Land | land_oesterreich | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_1996__GILT_IN_LAND__land_oesterreich"} |
| -> | HAT_GELTUNGSBEREICH | Geltungsbereich | geltungsbereich_eurocodes_eu_efta_uk | Eurocodes in EU/EFTA plus Vereinigtes Koenigreich | {"evidence_confidence": "belegt", "id": "norm_en_1996__HAT_GELTUNGSBEREICH__geltungsbereich_eurocodes_eu_efta_uk"} |


### EN 206

| Property | Value |
| --- | --- |
| beschreibung | EN national standard adoption across CEN/CENELEC members, country links reflect available member countries in this graph. |
| country_short | CEN |
| id | norm_en_206 |
| name | EN 206 |
| name_full | EN 206 — Concrete specification, performance, production and conformity |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Belgien (land_belgien), Deutschland (land_deutschland), Dänemark (land_daenemark), Finnland (land_finnland), Frankreich (land_frankreich), Italien (land_italien), Luxemburg (land_luxemburg), Niederlande (land_niederlande), Norwegen (land_norwegen), Portugal (land_portugal), Schweiz (land_schweiz), Vereinigtes Königreich (land_vereinigtes_koenigreich), Österreich (land_oesterreich) |
| ReuseRule APPLIES_IN | Belgien (land_belgien), Niederlande (land_niederlande) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | GILT_IN_LAND | Land | land_belgien | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_belgien"} |
| -> | GILT_IN_LAND | Land | land_deutschland | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_deutschland"} |
| -> | GILT_IN_LAND | Land | land_daenemark | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_daenemark"} |
| -> | GILT_IN_LAND | Land | land_finnland | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_finnland"} |
| -> | GILT_IN_LAND | Land | land_frankreich | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_frankreich"} |
| -> | GILT_IN_LAND | Land | land_italien | Italien | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_italien"} |
| -> | GILT_IN_LAND | Land | land_luxemburg | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_luxemburg"} |
| -> | GILT_IN_LAND | Land | land_niederlande | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_niederlande"} |
| -> | GILT_IN_LAND | Land | land_norwegen | Norwegen | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_norwegen"} |
| -> | GILT_IN_LAND | Land | land_portugal | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_portugal"} |
| -> | GILT_IN_LAND | Land | land_schweiz | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_206__GILT_IN_LAND__land_schweiz"} |
| -> | GILT_IN_LAND | Land | land_vereinigtes_koenigreich | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_206__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| -> | GILT_IN_LAND | Land | land_oesterreich | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_206__GILT_IN_LAND__land_oesterreich"} |
| -> | HAT_GELTUNGSBEREICH | Geltungsbereich | geltungsbereich_en_cen_cenelec_mitglieder | EN in CEN/CENELEC Mitgliedslaendern | {"evidence_confidence": "belegt", "id": "norm_en_206__HAT_GELTUNGSBEREICH__geltungsbereich_en_cen_cenelec_mitglieder"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_beton | Belgien × Beton reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_beton__REFERENZIERT_NORM__norm_en_206"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_nl_beton | Niederlande × Beton reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_beton__REFERENZIERT_NORM__norm_en_206"} |


### EN 338

| Property | Value |
| --- | --- |
| id | norm_en_338 |
| name | EN 338 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Vereinigtes Königreich (land_vereinigtes_koenigreich) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_338__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_gb_holz | Vereinigtes Königreich × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_holz__REFERENZIERT_NORM__norm_en_338"} |


### EN 771

| Property | Value |
| --- | --- |
| beschreibung | EN national standard adoption across CEN/CENELEC members, country links reflect available member countries in this graph. |
| country_short | CEN |
| id | norm_en_771 |
| name | EN 771 |
| name_full | EN 771 — Masonry units (specification series) |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Belgien (land_belgien), Deutschland (land_deutschland), Dänemark (land_daenemark), Finnland (land_finnland), Frankreich (land_frankreich), Italien (land_italien), Luxemburg (land_luxemburg), Niederlande (land_niederlande), Norwegen (land_norwegen), Portugal (land_portugal), Schweiz (land_schweiz), Vereinigtes Königreich (land_vereinigtes_koenigreich), Österreich (land_oesterreich) |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | GILT_IN_LAND | Land | land_belgien | Belgien | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_belgien"} |
| -> | GILT_IN_LAND | Land | land_deutschland | Deutschland | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_deutschland"} |
| -> | GILT_IN_LAND | Land | land_daenemark | Dänemark | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_daenemark"} |
| -> | GILT_IN_LAND | Land | land_finnland | Finnland | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_finnland"} |
| -> | GILT_IN_LAND | Land | land_frankreich | Frankreich | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_frankreich"} |
| -> | GILT_IN_LAND | Land | land_italien | Italien | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_italien"} |
| -> | GILT_IN_LAND | Land | land_luxemburg | Luxemburg | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_luxemburg"} |
| -> | GILT_IN_LAND | Land | land_niederlande | Niederlande | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_niederlande"} |
| -> | GILT_IN_LAND | Land | land_norwegen | Norwegen | {"evidence_confidence": "belegt", "id": "norm_en_771__GILT_IN_LAND__land_norwegen"} |
| -> | GILT_IN_LAND | Land | land_portugal | Portugal | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_portugal"} |
| -> | GILT_IN_LAND | Land | land_schweiz | Schweiz | {"evidence_confidence": "belegt", "id": "norm_en_771__GILT_IN_LAND__land_schweiz"} |
| -> | GILT_IN_LAND | Land | land_vereinigtes_koenigreich | Vereinigtes Königreich | {"evidence_confidence": "belegt", "id": "norm_en_771__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| -> | GILT_IN_LAND | Land | land_oesterreich | Österreich | {"evidence_confidence": "unklar", "id": "norm_en_771__GILT_IN_LAND__land_oesterreich"} |
| -> | HAT_GELTUNGSBEREICH | Geltungsbereich | geltungsbereich_en_cen_cenelec_mitglieder | EN in CEN/CENELEC Mitgliedslaendern | {"evidence_confidence": "belegt", "id": "norm_en_771__HAT_GELTUNGSBEREICH__geltungsbereich_en_cen_cenelec_mitglieder"} |


### EN 771-1

| Property | Value |
| --- | --- |
| id | norm_en_771_1 |
| name | EN 771-1 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_771_1__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_ziegel | Deutschland × Ziegel reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_ziegel__REFERENZIERT_NORM__norm_en_771_1"} |


### EN 772

| Property | Value |
| --- | --- |
| id | norm_en_772 |
| name | EN 772 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_772__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_ziegel | Deutschland × Ziegel reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_ziegel__REFERENZIERT_NORM__norm_en_772"} |


### EN 998

| Property | Value |
| --- | --- |
| id | norm_en_998 |
| name | EN 998 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_998__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_ziegel | Deutschland × Ziegel reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_ziegel__REFERENZIERT_NORM__norm_en_998"} |


### EN/SIA product references

| Property | Value |
| --- | --- |
| id | norm_en_sia_product_references |
| name | EN/SIA product references |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Schweiz (land_schweiz) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_sia_product_references__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_ch_beton | Schweiz × Beton reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_beton__REFERENZIERT_NORM__norm_en_sia_product_references"} |


### EN/SN 12058

| Property | Value |
| --- | --- |
| id | norm_en_sn_12058 |
| name | EN/SN 12058 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Schweiz (land_schweiz) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_sn_12058__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_ch_naturstein | Schweiz × Naturstein reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_naturstein__REFERENZIERT_NORM__norm_en_sn_12058"} |


### EN/SN 1469

| Property | Value |
| --- | --- |
| id | norm_en_sn_1469 |
| name | EN/SN 1469 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Schweiz (land_schweiz) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_en_sn_1469__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_ch_naturstein | Schweiz × Naturstein reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_naturstein__REFERENZIERT_NORM__norm_en_sn_1469"} |


### Eurocode 2

| Property | Value |
| --- | --- |
| id | norm_eurocode_2 |
| name | Eurocode 2 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien), Deutschland (land_deutschland), Finnland (land_finnland), Niederlande (land_niederlande), Norwegen (land_norwegen) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_eurocode_2__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_beton | Belgien × Beton reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_beton__REFERENZIERT_NORM__norm_eurocode_2"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_beton | Deutschland × Beton reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_beton__REFERENZIERT_NORM__norm_eurocode_2"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_fi_beton_hollow_core_slabs | Finnland × Beton / hollow-core slabs reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_fi_beton_hollow_core_slabs__REFERENZIERT_NORM__norm_eurocode_2"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_nl_beton | Niederlande × Beton reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_beton__REFERENZIERT_NORM__norm_eurocode_2"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_no_beton_hollow_core_slabs | Norwegen × Beton / hollow-core slabs reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_no_beton_hollow_core_slabs__REFERENZIERT_NORM__norm_eurocode_2"} |


### Eurocode 3

| Property | Value |
| --- | --- |
| id | norm_eurocode_3 |
| name | Eurocode 3 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien), Niederlande (land_niederlande), Vereinigtes Königreich (land_vereinigtes_koenigreich) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_eurocode_3__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_stahl | Belgien × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_stahl__REFERENZIERT_NORM__norm_eurocode_3"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_nl_stahl | Niederlande × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_stahl__REFERENZIERT_NORM__norm_eurocode_3"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_gb_stahl | Vereinigtes Königreich × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_stahl__REFERENZIERT_NORM__norm_eurocode_3"} |


### Eurocode 5

| Property | Value |
| --- | --- |
| id | norm_eurocode_5 |
| name | Eurocode 5 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien), Deutschland (land_deutschland), Niederlande (land_niederlande) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_eurocode_5__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_holz | Belgien × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_holz__REFERENZIERT_NORM__norm_eurocode_5"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_holz | Deutschland × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_holz__REFERENZIERT_NORM__norm_eurocode_5"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_nl_holz | Niederlande × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_holz__REFERENZIERT_NORM__norm_eurocode_5"} |


### Eurocode 5 / UK NA

| Property | Value |
| --- | --- |
| id | norm_eurocode_5_uk_na |
| name | Eurocode 5 / UK NA |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Vereinigtes Königreich (land_vereinigtes_koenigreich) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_eurocode_5_uk_na__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_gb_holz | Vereinigtes Königreich × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_holz__REFERENZIERT_NORM__norm_eurocode_5_uk_na"} |


### Eurocode 6

| Property | Value |
| --- | --- |
| id | norm_eurocode_6 |
| name | Eurocode 6 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_eurocode_6__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_ziegel | Deutschland × Ziegel reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_ziegel__REFERENZIERT_NORM__norm_eurocode_6"} |


### Eurocode-adjacent structural verification

| Property | Value |
| --- | --- |
| id | norm_eurocode_adjacent_structural_verification |
| name | Eurocode-adjacent structural verification |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_eurocode_adjacent_structural_verification__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_lehm | Deutschland × Lehm reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_lehm__REFERENZIERT_NORM__norm_eurocode_adjacent_structural_verification"} |


### Eurocode-related timber product standards

| Property | Value |
| --- | --- |
| id | norm_eurocode_related_timber_product_standards |
| name | Eurocode-related timber product standards |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Schweiz (land_schweiz) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_eurocode_related_timber_product_standards__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_ch_holz | Schweiz × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_holz__REFERENZIERT_NORM__norm_eurocode_related_timber_product_standards"} |


### Finnish national annexes

| Property | Value |
| --- | --- |
| id | norm_finnish_national_annexes |
| name | Finnish national annexes |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Finnland (land_finnland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_finnish_national_annexes__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_fi_beton_hollow_core_slabs | Finnland × Beton / hollow-core slabs reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_fi_beton_hollow_core_slabs__REFERENZIERT_NORM__norm_finnish_national_annexes"} |


### Fire/durability rules

| Property | Value |
| --- | --- |
| id | norm_fire_durability_rules |
| name | Fire/durability rules |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_fire_durability_rules__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_holz | Belgien × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_holz__REFERENZIERT_NORM__norm_fire_durability_rules"} |


### Fire/moisture rules

| Property | Value |
| --- | --- |
| id | norm_fire_moisture_rules |
| name | Fire/moisture rules |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland), Vereinigtes Königreich (land_vereinigtes_koenigreich) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_fire_moisture_rules__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_lehm | Deutschland × Lehm reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_lehm__REFERENZIERT_NORM__norm_fire_moisture_rules"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_gb_holz | Vereinigtes Königreich × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_holz__REFERENZIERT_NORM__norm_fire_moisture_rules"} |


### Fire/moisture/durability requirements

| Property | Value |
| --- | --- |
| id | norm_fire_moisture_durability_requirements |
| name | Fire/moisture/durability requirements |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Schweiz (land_schweiz) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_fire_moisture_durability_requirements__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_ch_holz | Schweiz × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_holz__REFERENZIERT_NORM__norm_fire_moisture_durability_requirements"} |


### Frost rules

| Property | Value |
| --- | --- |
| id | norm_frost_rules |
| name | Frost rules |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_frost_rules__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_ziegel | Deutschland × Ziegel reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_ziegel__REFERENZIERT_NORM__norm_frost_rules"} |


### Historic Sections Book

| Property | Value |
| --- | --- |
| id | norm_historic_sections_book |
| name | Historic Sections Book |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Vereinigtes Königreich (land_vereinigtes_koenigreich) |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country | Vereinigtes Königreich (land_vereinigtes_koenigreich) |
| BG Projekt country | Vereinigtes Königreich (land_vereinigtes_koenigreich) |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:Dossier | q_bedzed_london_hackbridge_md | BedZED_London_Hackbridge… | {"evidence_confidence": "unklar", "id": "r_norm_historic_sections_book__BELEGT_IN__q_bedzed_london_hackbridge_md"} |
| -> | GILT_IN_LAND | Land | land_vereinigtes_koenigreich | Vereinigtes Königreich | {"evidence_confidence": "unklar", "id": "r_norm_historic_sections_book__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| <- | REFERENZIERT_NORM | Projekt | p_bedzed_london_hackbridge | BedZED | {"evidence_confidence": "unklar", "id": "r_p_bedzed_london_hackbridge__REFERENZIERT_NORM__norm_historic_sections_book"} |
| <- | REFERENZIERT_NORM | Bauteilgruppe | bg_stahl_mehrere_bedzed_structural | Structural steel frame… | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahl_mehrere_bedzed_structural__REFERENZIERT_NORM__norm_historic_sections_book"} |


### ISO 14040

| Property | Value |
| --- | --- |
| id | norm_iso_14040 |
| name | ISO 14040 |
| name_full | ISO_14040 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country | Schweiz (land_schweiz), Vereinigtes Königreich (land_vereinigtes_koenigreich) |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| <- | METHODENGRUNDLAGE_NORM | LCAModule | lz_a1_a3 | A1-A3 Produkt | {"evidence_confidence": "unklar", "id": "r_lz_a1_a3__METHODENGRUNDLAGE_NORM__norm_iso_14040"} |
| <- | REFERENZIERT_NORM | Projekt | p_55_great_suffolk_street_london | 55 Great Suffolk Street | {"evidence_confidence": "teilweise_belegt", "id": "r_p_55_great_suffolk_street_london__REFERENZIERT_NORM__norm_iso_14040"} |
| <- | REFERENZIERT_NORM | Projekt | p_k118_kopfbau_halle_118_winterthur | K.118 Winterthur | {"evidence_confidence": "teilweise_belegt", "id": "r_p_k118_kopfbau_halle_118_winterthur__REFERENZIERT_NORM__norm_iso_14040"} |


### ISO 14044

| Property | Value |
| --- | --- |
| id | norm_iso_14044 |
| name | ISO 14044 |
| name_full | ISO_14044 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country | Schweiz (land_schweiz), Vereinigtes Königreich (land_vereinigtes_koenigreich) |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| <- | METHODENGRUNDLAGE_NORM | LCAModule | lz_a1_a3 | A1-A3 Produkt | {"evidence_confidence": "unklar", "id": "r_lz_a1_a3__METHODENGRUNDLAGE_NORM__norm_iso_14044"} |
| <- | REFERENZIERT_NORM | Projekt | p_55_great_suffolk_street_london | 55 Great Suffolk Street | {"evidence_confidence": "teilweise_belegt", "id": "r_p_55_great_suffolk_street_london__REFERENZIERT_NORM__norm_iso_14044"} |
| <- | REFERENZIERT_NORM | Projekt | p_k118_kopfbau_halle_118_winterthur | K.118 Winterthur | {"evidence_confidence": "teilweise_belegt", "id": "r_p_k118_kopfbau_halle_118_winterthur__REFERENZIERT_NORM__norm_iso_14044"} |


### ISO 20887

| Property | Value |
| --- | --- |
| id | norm_iso_20887 |
| name | ISO 20887 |
| name_full | ISO_20887 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| <- | REFERENZIERT_NORM | Norm | norm_sia_schweiz | SIA (CH) | {"evidence_confidence": "unklar", "id": "r_norm_sia_schweiz__REFERENZIERT_NORM__norm_iso_20887"} |


### MVV TB/DIBt pathway

| Property | Value |
| --- | --- |
| id | norm_mvv_tb_dibt_pathway |
| name | MVV TB/DIBt pathway |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Deutschland (land_deutschland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_mvv_tb_dibt_pathway__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_de_stahl | Deutschland × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_de_stahl__REFERENZIERT_NORM__norm_mvv_tb_dibt_pathway"} |


### NBN EN 14081

| Property | Value |
| --- | --- |
| id | norm_nbn_en_14081 |
| name | NBN EN 14081 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_nbn_en_14081__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_holz | Belgien × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_holz__REFERENZIERT_NORM__norm_nbn_en_14081"} |


### NBN EN 338

| Property | Value |
| --- | --- |
| id | norm_nbn_en_338 |
| name | NBN EN 338 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_nbn_en_338__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_holz | Belgien × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_holz__REFERENZIERT_NORM__norm_nbn_en_338"} |


### NBN national annexes

| Property | Value |
| --- | --- |
| id | norm_nbn_national_annexes |
| name | NBN national annexes |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Belgien (land_belgien) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_nbn_national_annexes__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_be_stahl | Belgien × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_be_stahl__REFERENZIERT_NORM__norm_nbn_national_annexes"} |


### NEN 8700

| Property | Value |
| --- | --- |
| beschreibung | Dutch national standard for assessment of existing structures; relevant to structural reuse. |
| country_short | NL |
| id | norm_nen_8700 |
| name | NEN 8700 |
| name_full | NEN 8700 — Existing-structure assessment (Netherlands) |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Niederlande (land_niederlande) |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | GILT_IN_LAND | Land | land_niederlande | Niederlande | {"evidence_confidence": "unklar", "id": "r_norm_nen_8700__GILT_IN_LAND__land_niederlande"} |


### NEN EN 1090-2

| Property | Value |
| --- | --- |
| id | norm_nen_en_1090_2 |
| name | NEN EN 1090-2 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Niederlande (land_niederlande) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_nen_en_1090_2__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_nl_stahl | Niederlande × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_stahl__REFERENZIERT_NORM__norm_nen_en_1090_2"} |


### NEN EN 14081

| Property | Value |
| --- | --- |
| id | norm_nen_en_14081 |
| name | NEN EN 14081 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Niederlande (land_niederlande) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_nen_en_14081__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_nl_holz | Niederlande × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_holz__REFERENZIERT_NORM__norm_nen_en_14081"} |


### NEN EN 338

| Property | Value |
| --- | --- |
| id | norm_nen_en_338 |
| name | NEN EN 338 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Niederlande (land_niederlande) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_nen_en_338__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_nl_holz | Niederlande × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_holz__REFERENZIERT_NORM__norm_nen_en_338"} |


### NEN fire/moisture rules

| Property | Value |
| --- | --- |
| id | norm_nen_fire_moisture_rules |
| name | NEN fire/moisture rules |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Niederlande (land_niederlande) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_nen_fire_moisture_rules__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_nl_holz | Niederlande × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_nl_holz__REFERENZIERT_NORM__norm_nen_fire_moisture_rules"} |


### NS 3682

| Property | Value |
| --- | --- |
| id | norm_ns_3682 |
| name | NS 3682 |
| name_full | NS 3682 Reuse of hollow-core slabs / Norwegian reuse standard |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Norwegen (land_norwegen) |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country |  |
| BG Projekt country | Norwegen (land_norwegen) |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | GILT_IN_LAND | Land | land_norwegen | Norwegen | {"evidence_confidence": "unklar", "id": "r_norm_ns_3682__GILT_IN_LAND__land_norwegen"} |
| <- | REFERENZIERT_NORM | Bauteilgruppe | bg_stahlbeton_decke_ka13_hollow_core_slabs | Hohlkörperdecken aus… | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahlbeton_decke_ka13_hollow_core_slabs__REFERENZIERT_NORM__norm_ns_3682"} |
| <- | REFERENZIERT_NORM | Norm | norm_tek_norway | TEK (NO) | {"evidence_confidence": "unklar", "id": "r_norm_tek_norway__REFERENZIERT_NORM__norm_ns_3682"} |
| -> | REFERENZIERT_NORM | Norm | norm_tek_norway | TEK (NO) | {"evidence_confidence": "unklar", "id": "r_norm_ns_3682__REFERENZIERT_NORM__norm_tek_norway"} |


### NS 3682:2022

| Property | Value |
| --- | --- |
| id | norm_ns_3682_2022 |
| name | NS 3682:2022 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Norwegen (land_norwegen) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_ns_3682_2022__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_no_beton_hollow_core_slabs | Norwegen × Beton / hollow-core slabs reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_no_beton_hollow_core_slabs__REFERENZIERT_NORM__norm_ns_3682_2022"} |


### PD CEN/TS 1090-201

| Property | Value |
| --- | --- |
| id | norm_pd_cen_ts_1090_201 |
| name | PD CEN/TS 1090-201 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Vereinigtes Königreich (land_vereinigtes_koenigreich) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_pd_cen_ts_1090_201__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_gb_stahl | Vereinigtes Königreich × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_stahl__REFERENZIERT_NORM__norm_pd_cen_ts_1090_201"} |


### RT 2012

| Property | Value |
| --- | --- |
| id | norm_rt_2012 |
| name | RT 2012 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Frankreich (land_frankreich) |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country | Frankreich (land_frankreich) |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:Dossier | q_resilience_la_ferme_des_possibles_stains_md | Resilience_La_Ferme_des_… | {"evidence_confidence": "unklar", "id": "r_norm_rt_2012__BELEGT_IN__q_resilience_la_ferme_des_possibles_stains_md"} |
| -> | GILT_IN_LAND | Land | land_frankreich | Frankreich | {"evidence_confidence": "unklar", "id": "r_norm_rt_2012__GILT_IN_LAND__land_frankreich"} |
| <- | REFERENZIERT_NORM | Projekt | p_resilience_la_ferme_des_possibles_stains | Résilience | {"evidence_confidence": "unklar", "id": "r_p_resilience_la_ferme_des_possibles_stains__REFERENZIERT_NORM__norm_rt_2012"} |


### ReCreate QA procedure

| Property | Value |
| --- | --- |
| id | norm_recreate_qa_procedure |
| name | ReCreate QA procedure |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Finnland (land_finnland) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_recreate_qa_procedure__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_fi_beton_hollow_core_slabs | Finnland × Beton / hollow-core slabs reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_fi_beton_hollow_core_slabs__REFERENZIERT_NORM__norm_recreate_qa_procedure"} |


### SCI P427 protocol

| Property | Value |
| --- | --- |
| id | norm_sci_p427 |
| name | SCI P427 protocol |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Vereinigtes Königreich (land_vereinigtes_koenigreich) |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country | Vereinigtes Königreich (land_vereinigtes_koenigreich) |
| BG Projekt country | Vereinigtes Königreich (land_vereinigtes_koenigreich) |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:Dossier | q_brent_cross_town_primary_substation_london_md | Brent_Cross_Town_Primary… | {"evidence_confidence": "unklar", "id": "r_norm_sci_p427__BELEGT_IN__q_brent_cross_town_primary_substation_london_md"} |
| -> | GILT_IN_LAND | Land | land_vereinigtes_koenigreich | Vereinigtes Königreich | {"evidence_confidence": "unklar", "id": "r_norm_sci_p427__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| <- | REFERENZIERT_NORM | Projekt | p_brent_cross_town_primary_substation_london | Brent Cross Town… | {"evidence_confidence": "unklar", "id": "r_p_brent_cross_town_primary_substation_london__REFERENZIERT_NORM__norm_sci_p427"} |
| <- | REFERENZIERT_NORM | Norm | norm_sci_p440 | SCI P440 | {"evidence_confidence": "unklar", "id": "r_norm_sci_p440__REFERENZIERT_NORM__norm_sci_p427"} |
| <- | REFERENZIERT_NORM | Bauteilgruppe | bg_stahl_mehrere_holbein_structural | Stahlträger un… (Holbein) | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahl_mehrere_holbein_structural__REFERENZIERT_NORM__norm_sci_p427"} |
| -> | REFERENZIERT_NORM | Norm | norm_sci_p440 | SCI P440 | {"evidence_confidence": "unklar", "id": "r_norm_sci_p427__REFERENZIERT_NORM__norm_sci_p440"} |


### SCI P440

| Property | Value |
| --- | --- |
| id | norm_sci_p440 |
| name | SCI P440 |
| name_full | SCI P440 Reuse of Structural Steel |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Vereinigtes Königreich (land_vereinigtes_koenigreich) |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country |  |
| BG Projekt country | Vereinigtes Königreich (land_vereinigtes_koenigreich) |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | GILT_IN_LAND | Land | land_vereinigtes_koenigreich | Vereinigtes Königreich | {"evidence_confidence": "unklar", "id": "r_norm_sci_p440__GILT_IN_LAND__land_vereinigtes_koenigreich"} |
| <- | REFERENZIERT_NORM | Norm | norm_sci_p427 | SCI P427 protocol | {"evidence_confidence": "unklar", "id": "r_norm_sci_p427__REFERENZIERT_NORM__norm_sci_p440"} |
| <- | REFERENZIERT_NORM | Bauteilgruppe | bg_stahl_mehrere_holbein_structural | Stahlträger un… (Holbein) | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahl_mehrere_holbein_structural__REFERENZIERT_NORM__norm_sci_p440"} |
| -> | REFERENZIERT_NORM | Norm | norm_sci_p427 | SCI P427 protocol | {"evidence_confidence": "unklar", "id": "r_norm_sci_p440__REFERENZIERT_NORM__norm_sci_p427"} |


### SCI protocol

| Property | Value |
| --- | --- |
| id | norm_sci_protocol |
| name | SCI protocol |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Vereinigtes Königreich (land_vereinigtes_koenigreich) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_sci_protocol__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_gb_stahl | Vereinigtes Königreich × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_stahl__REFERENZIERT_NORM__norm_sci_protocol"} |


### SIA (CH)

| Property | Value |
| --- | --- |
| id | norm_sia_schweiz |
| name | SIA (CH) |
| name_full | SIA / Swiss building standards context |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Schweiz (land_schweiz) |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country |  |
| BG Projekt country | Schweiz (land_schweiz) |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | GILT_IN_LAND | Land | land_schweiz | Schweiz | {"evidence_confidence": "unklar", "id": "r_norm_sia_schweiz__GILT_IN_LAND__land_schweiz"} |
| <- | REFERENZIERT_NORM | Bauteilgruppe | bg_stahl_mehrere_juch_hagenholz_stahlstruktur | 1:1 versetzte Stahlstruk… | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahl_mehrere_juch_hagenholz_stahlstruktur__REFERENZIERT_NORM__norm_sia_schweiz"} |
| <- | REFERENZIERT_NORM | Bauteilgruppe | bg_stahlbeton_mehrere_juch_schellinghalle_pilzstuetzen | Beton-Pilzstützen und… | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahlbeton_mehrere_juch_schellinghalle_pilzstuetzen__REFERENZIERT_NORM__norm_sia_schweiz"} |
| <- | REFERENZIERT_NORM | Bauteilgruppe | bg_beton_mehrere_juch_kerenzerberg_betonplatten | Betonplatten aus dem… | {"evidence_confidence": "unklar", "id": "r_bg_reuse_beton_mehrere_juch_kerenzerberg_betonplatten__REFERENZIERT_NORM__norm_sia_schweiz"} |
| <- | REFERENZIERT_NORM | Bauteilgruppe | bg_stahl_mehrere_k118_structure | Stahlträger und Stützen… | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahl_mehrere_k118_structure__REFERENZIERT_NORM__norm_sia_schweiz"} |
| -> | REFERENZIERT_NORM | Norm | norm_iso_20887 | ISO 20887 | {"evidence_confidence": "unklar", "id": "r_norm_sia_schweiz__REFERENZIERT_NORM__norm_iso_20887"} |


### SIA 261

| Property | Value |
| --- | --- |
| id | norm_sia_261 |
| name | SIA 261 |
| name_full | SIA 261 — Einwirkungen auf Tragwerke (Switzerland seismic+actions standard) |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country | Schweiz (land_schweiz) |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| <- | REFERENZIERT_NORM | Projekt | p_schaerenmoosstrasse_zuerich | Schärenmoosstr. ZH | {"evidence_confidence": "unklar", "id": "r_p_schaerenmoosstrasse_zuerich__REFERENZIERT_NORM__norm_sia_261"} |


### SIA 262

| Property | Value |
| --- | --- |
| id | norm_sia_262 |
| name | SIA 262 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Schweiz (land_schweiz) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_sia_262__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_ch_beton | Schweiz × Beton reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_beton__REFERENZIERT_NORM__norm_sia_262"} |


### SIA 263

| Property | Value |
| --- | --- |
| id | norm_sia_263 |
| name | SIA 263 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Schweiz (land_schweiz) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_sia_263__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_ch_stahl | Schweiz × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_stahl__REFERENZIERT_NORM__norm_sia_263"} |


### SIA 265

| Property | Value |
| --- | --- |
| id | norm_sia_265 |
| name | SIA 265 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Schweiz (land_schweiz) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_sia_265__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_ch_holz | Schweiz × Holz reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_holz__REFERENZIERT_NORM__norm_sia_265"} |


### SIA 269

| Property | Value |
| --- | --- |
| id | norm_sia_269 |
| name | SIA 269 |
| name_full | SIA 269 — Existing structures: Grundlagen / Erhaltung von Tragwerken |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Schweiz (land_schweiz) |
| Direct Projekt country | Schweiz (land_schweiz) |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| <- | REFERENZIERT_NORM | Projekt | p_elementa_walkeweg | ELEMENTA Walkeweg | {"evidence_confidence": "unklar", "id": "r_p_elementa_walkeweg__REFERENZIERT_NORM__norm_sia_269"} |
| <- | REFERENZIERT_NORM | Projekt | p_lysp8_basel | LYSP8 Basel | {"evidence_confidence": "unklar", "id": "r_p_lysp8_basel__REFERENZIERT_NORM__norm_sia_269"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_ch_beton | Schweiz × Beton reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_beton__REFERENZIERT_NORM__norm_sia_269"} |
| <- | REFERENZIERT_NORM | Projekt | p_umar_unit | UMAR Unit | {"evidence_confidence": "unklar", "id": "r_p_umar_unit__REFERENZIERT_NORM__norm_sia_269"} |


### SIA 380/1

| Property | Value |
| --- | --- |
| id | norm_sia_380_1 |
| name | SIA 380/1 |
| name_full | SIA 380/1 — Heizwärmebedarf (Schweiz) |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country | Schweiz (land_schweiz) |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| <- | REFERENZIERT_NORM | Projekt | p_elementa_walkeweg | ELEMENTA Walkeweg | {"evidence_confidence": "unklar", "id": "r_p_elementa_walkeweg__REFERENZIERT_NORM__norm_sia_380_1"} |
| <- | REFERENZIERT_NORM | Projekt | p_umar_unit | UMAR Unit | {"evidence_confidence": "unklar", "id": "r_p_umar_unit__REFERENZIERT_NORM__norm_sia_380_1"} |


### SIA 416

| Property | Value |
| --- | --- |
| id | norm_sia_416 |
| name | SIA 416 |
| name_full | SIA 416 — Kennzahlen für Grundstücke und Gebäude (Schweiz) |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country | Schweiz (land_schweiz) |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| <- | REFERENZIERT_NORM | Projekt | p_lysp8_basel | LYSP8 Basel | {"evidence_confidence": "unklar", "id": "r_p_lysp8_basel__REFERENZIERT_NORM__norm_sia_416"} |


### SIA 500

| Property | Value |
| --- | --- |
| id | norm_sia_500 |
| name | SIA 500 |
| name_full | SIA 500 — Hindernisfreie Bauten / barrier-free construction |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country | Schweiz (land_schweiz) |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| <- | REFERENZIERT_NORM | Projekt | p_schaerenmoosstrasse_zuerich | Schärenmoosstr. ZH | {"evidence_confidence": "unklar", "id": "r_p_schaerenmoosstrasse_zuerich__REFERENZIERT_NORM__norm_sia_500"} |


### SIA façade/anchorage rules

| Property | Value |
| --- | --- |
| id | norm_sia_facade_anchorage_rules |
| name | SIA façade/anchorage rules |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Schweiz (land_schweiz) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_sia_facade_anchorage_rules__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_ch_naturstein | Schweiz × Naturstein reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_naturstein__REFERENZIERT_NORM__norm_sia_facade_anchorage_rules"} |


### SIA fire/durability rules

| Property | Value |
| --- | --- |
| id | norm_sia_fire_durability_rules |
| name | SIA fire/durability rules |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Schweiz (land_schweiz) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_sia_fire_durability_rules__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_ch_stahl | Schweiz × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_stahl__REFERENZIERT_NORM__norm_sia_fire_durability_rules"} |


### Swiss BauPG

| Property | Value |
| --- | --- |
| id | norm_swiss_baupg |
| name | Swiss BauPG |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Schweiz (land_schweiz) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_swiss_baupg__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_ch_stahl | Schweiz × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_ch_stahl__REFERENZIERT_NORM__norm_swiss_baupg"} |


### TEK (NO)

| Property | Value |
| --- | --- |
| id | norm_tek_norway |
| name | TEK (NO) |
| name_full | Norwegian building regulation TEK / documentation context |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND | Norwegen (land_norwegen) |
| ReuseRule APPLIES_IN |  |
| Direct Projekt country |  |
| BG Projekt country | Norwegen (land_norwegen) |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | GILT_IN_LAND | Land | land_norwegen | Norwegen | {"evidence_confidence": "unklar", "id": "r_norm_tek_norway__GILT_IN_LAND__land_norwegen"} |
| <- | REFERENZIERT_NORM | Bauteilgruppe | bg_mehrere_mehrere_ka13_office_fronts_doors_facade | Bürofronten | {"evidence_confidence": "unklar", "id": "r_bg_reuse_mehrere_mehrere_ka13_office_fronts_doors_facade__REFERENZIERT_NORM__norm_tek_norway"} |
| <- | REFERENZIERT_NORM | Bauteilgruppe | bg_stahlbeton_decke_ka13_hollow_core_slabs | Hohlkörperdecken aus… | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahlbeton_decke_ka13_hollow_core_slabs__REFERENZIERT_NORM__norm_tek_norway"} |
| <- | REFERENZIERT_NORM | Norm | norm_ns_3682 | NS 3682 | {"evidence_confidence": "unklar", "id": "r_norm_ns_3682__REFERENZIERT_NORM__norm_tek_norway"} |
| <- | REFERENZIERT_NORM | Bauteilgruppe | bg_mehrere_technik_ka13_tga_sanitary_radiators | Radiatoren (Ka13) | {"evidence_confidence": "unklar", "id": "r_bg_reuse_mehrere_technik_ka13_tga_sanitary_radiators__REFERENZIERT_NORM__norm_tek_norway"} |
| <- | REFERENZIERT_NORM | Bauteilgruppe | bg_stahl_mehrere_ka13 | Stahl in Bestand und… | {"evidence_confidence": "unklar", "id": "r_bg_reuse_stahl_mehrere_ka13__REFERENZIERT_NORM__norm_tek_norway"} |
| -> | REFERENZIERT_NORM | Norm | norm_ns_3682 | NS 3682 | {"evidence_confidence": "unklar", "id": "r_norm_tek_norway__REFERENZIERT_NORM__norm_ns_3682"} |


### TEK17

| Property | Value |
| --- | --- |
| id | norm_tek17 |
| name | TEK17 |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Norwegen (land_norwegen) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_tek17__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_no_beton_hollow_core_slabs | Norwegen × Beton / hollow-core slabs reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_no_beton_hollow_core_slabs__REFERENZIERT_NORM__norm_tek17"} |


### UKCA/CE interface

| Property | Value |
| --- | --- |
| id | norm_ukca_ce_interface |
| name | UKCA/CE interface |


Country context:
| Context | Countries |
| --- | --- |
| Direct GILT_IN_LAND |  |
| ReuseRule APPLIES_IN | Vereinigtes Königreich (land_vereinigtes_koenigreich) |
| Direct Projekt country |  |
| BG Projekt country |  |

Connected nodes:
| Dir | Rel type | Connected labels | Connected ID | Connected name | Rel properties |
| --- | --- | --- | --- | --- | --- |
| -> | BELEGT_IN | Quelle:ResearchDocument | q_circular_construction_reuse_graph_gaps_md | circular_construction_reuse_graph_gaps.md | {"id": "r_norm_ukca_ce_interface__BELEGT_IN__q_circular_construction_reuse_graph_gaps_md"} |
| <- | REFERENZIERT_NORM | ReuseRule | rr_gb_stahl | Vereinigtes Königreich × Stahl reuse rule | {"evidence_confidence": "teilweise_belegt", "id": "r_rr_gb_stahl__REFERENZIERT_NORM__norm_ukca_ce_interface"} |

