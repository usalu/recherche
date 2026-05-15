# Round 002 Baseline — Global Technical Audit

Generated: 2026-05-15T14:54:37.037870+00:00

**Inputs:** post-2026-05-15 processed payloads (`_neo4j/processed/projects/`, `_neo4j/processed/actor_registry/`) + live `mit-bestand`.
**Supersedes:** `_neo4j/review/round_001/global_audit_report.md` (the underlying 20-batch tree is archived).

## Summary

| Metric | Value |
| --- | --- |
| project_files | 75 |
| files_scanned | 78 |
| nodes_unique | 2163 |
| relationships_unique | 15841 |
| parse_errors | 0 |
| schema_errors | 642 |
| schema_errors_actor_registry | 642 |
| schema_errors_project_records | 0 |
| live_unknown_rel_types | 1 |
| live_unknown_labels | 1 |
| missing_endpoints | 0 |
| duplicate_node_conflicts | 105 |
| duplicate_node_conflict_ids | 44 |
| duplicate_relationship_conflicts | 0 |
| forbidden_nodes | 0 |
| bad_belegt_in | 319 |
| projects_no_source | 0 |
| projects_no_component_or_work | 27 |
| bg_no_source | 0 |
| bg_no_type | 0 |
| bg_no_material_or_level | 0 |
| low_degree_non_vocab_nodes | 20 |

## Inputs

| File | Lines (non-empty) |
| --- | --- |
| _neo4j\processed\projects\vocabulary\controlled_vocabulary.seed.kg.jsonl | 385 |
| _neo4j\processed\projects\vocabulary\controlled_terms.merged.kg.jsonl | 56 |
| _neo4j\processed\actor_registry\actor_registry.canonical.kg.jsonl | 3227 |
| + project records | 75 |

## Schema Errors by File

| File | Errors |
| --- | --- |
| _neo4j\processed\actor_registry\actor_registry.canonical.kg.jsonl | 642 |

## Contract Drift vs Live Graph

- Live rel types not in any contract: 1 — GEHÖRT_ZU
- Live node labels not in any contract: 1 — GraphVersion

## Blocking Findings

- Missing relationship endpoints: none
- Forbidden node labels in payloads: 0
- BELEGT_IN without datenqualitaet=Belegt: 319
- Projekt without BELEGT_IN: 0
- Projekt without component/work links: 27
- Bauteilgruppe without BELEGT_IN: 0
- Bauteilgruppe without HAT_BAUTEILTYP: 0
- Bauteilgruppe without NUTZT_MATERIAL or HAT_BAUTEILEBENE: 0

## Duplicate Node Property Conflicts (payloads)

44 unique node ids have conflicting properties across processed payloads.

| Node id | Label | Kind | Round-002 route | Canonical candidate | Aliases |
| --- | --- | --- | --- | --- | --- |
| a_cleveland_steel_tubes | Akteur | content | actor_registry | Cleveland Steel & Tubes | Cleveland Steel and Tubes |
| a_die_zusammenarbeiter | Akteur | content | actor_registry | Die Zusammenarbeiter | Die Zusammenarbeiter GmbH |
| a_encore_heureux | Akteur | content | actor_registry | Encore Heureux | Encore Heureux Architectes |
| a_imd_raadgevende_ingenieurs | Akteur | content | actor_registry | IMd Raadgevende Ingenieurs | IMd raadgevende ingenieurs |
| a_rotor | Akteur | content | actor_registry | ROTOR | Rotor |
| bw_tampere_1980s_office_donor | Bauwerk | content | round_003 | 1980er Bürogebäude im Zentrum von Tampere | Bürogebäude der frühen 1980er Jahre im Zentrum Tampere |
| land_belgien | Land | vocab | 2_stadt_land | Belgien |  |
| land_daenemark | Land | vocab | 2_stadt_land | Dänemark | Daenemark |
| land_deutschland | Land | vocab | 2_stadt_land | Deutschland |  |
| land_finnland | Land | vocab | 2_stadt_land | Finnland |  |
| land_frankreich | Land | vocab | 2_stadt_land | Frankreich |  |
| land_niederlande | Land | vocab | 2_stadt_land | Niederlande |  |
| land_schweiz | Land | vocab | 2_stadt_land | Schweiz |  |
| land_usa | Land | vocab | 2_stadt_land | USA |  |
| land_vereinigtes_koenigreich | Land | vocab | 2_stadt_land | Vereinigtes Königreich | Vereinigtes Koenigreich |
| mat_textil | Material | vocab | 1_material | Textil | Textil / textile Fasern, Textil / Filz / textile Fasern |
| norm_sci_p427 | Norm | vocab | 8_norm_pruefung | SCI P427 protocol | SCI P427 Structural Steel Reuse |
| p_awm_muenster_circular_office | Projekt | content | round_003 | AWM Münster Circular Office | AWM Münster – zirkulärer Büroausbau 3. OG |
| p_bluecity_offices_rotterdam | Projekt | content | round_003 | BlueCity Offices Rotterdam |  |
| p_brighton_waste_house_brighton | Projekt | content | round_003 | Brighton Waste House / Brighton Wild House |  |
| p_circular_pavilion_paris | Projekt | content | round_003 | Circular Pavilion Paris | Pavillon Circulaire / Circular Pavilion, Paris |
| p_crclr_house_impact_hub_berlin | Projekt | content | round_003 | CRCLR House / Impact Hub Berlin |  |
| p_elys_kultur_gewerbehaus_basel | Projekt | content | round_003 | ELYS Kultur- & Gewerbehaus Basel | ELYS Kultur- und Gewerbehaus Basel |
| p_ferme_du_rail_paris | Projekt | content | round_003 | Ferme du Rail Paris | La Ferme du Rail, Paris |
| p_harmalanranta_a_kruunu_recreate_mini_pilot_tampere | Projekt | content | round_003 | Härmälänranta / A-Kruunu ReCreate mini-pilot Tampere | Härmälänranta / A-Kruunu ReCreate mini-pilot, Tampere |
| p_impact_hub_berlin_crclr_fitout | Projekt | content | round_003 | Impact Hub Berlin / CRCLR Fit-out | Impact Hub Berlin Interior / CRCLR fit-out |
| p_juch_areal_recyclingzentrum_zuerich | Projekt | content | round_003 | Juch-Areal Recyclingzentrum Zürich | Juch-Areal Recyclingzentrum Zürich-Altstetten |
| p_k118_kopfbau_halle_118_winterthur | Projekt | content | round_003 | K118 Kopfbau Halle 118 Winterthur | K.118 / Kopfbau Halle 118, Winterthur |
| p_kindergarten_moeoeslistrasse_manegg_zuerich | Projekt | content | round_003 | Kindergarten Mööslistrasse / Manegg Zürich | Kindergarten Mööslistrasse / Manegg, Zürich |
| p_lokomotion_technology_centre_mini_pilot_tampere | Projekt | content | round_003 | Lokomotion Technology Centre mini-pilot Tampere | Lokomotion Technology Centre mini-pilot, Tampere |
| p_melkinlaituri_primary_school_daycare_centre_helsinki | Projekt | content | round_003 | Melkinlaituri Primary School and Day-care Centre Helsinki | Melkinlaituri Primary School and Day-care Centre, Helsinki |
| p_montessori_maassluis | Projekt | content | round_003 | Montessori Maassluis |  |
| p_multi_brussels_reuse_in_multi | Projekt | content | round_003 | Multi Brussels / Reuse in MULTI | MULTI Brussels / Reuse in MULTI |
| p_peoples_pavilion_eindhoven | Projekt | content | round_003 | People’s Pavilion Eindhoven | People’s Pavilion, Eindhoven |
| p_plp_london_hq_circular_studio_fitout | Projekt | content | round_003 | PLP London HQ circular studio fit-out | PLP Architecture HQ / Circular Studio Fit-out, London |
| p_recyclinghaus_hannover | Projekt | content | round_003 | Recyclinghaus Hannover |  |
| p_resilience_la_ferme_des_possibles_stains | Projekt | content | round_003 | Résilience / La Ferme des Possibles | Résilience / La Ferme des Possibles Stains |
| p_resource_rows_copenhagen | Projekt | content | round_003 | Resource Rows | Resource Rows Copenhagen |
| p_thoravej_29_copenhagen | Projekt | content | round_003 | Thoravej 29 Copenhagen |  |
| p_upcycle_studios_copenhagen | Projekt | content | round_003 | Upcycle Studios | Upcycle Studios Copenhagen |
| p_villa_welpeloo_enschede | Projekt | content | round_003 | Villa Welpeloo | Villa Welpeloo Enschede |
| p_woongroep_boschgaard_den_bosch | Projekt | content | round_003 | Woongroep Boschgaard Den Bosch | Woongroep Boschgaard / Collectief Ecosysteem Boschgaard |
| p_zinneke_feder_masui4ever_brussels | Projekt | content | round_003 | Zinneke / FEDER Masui4ever | Zinneke / FEDER Masui4ever Brussels |
| stadt_bruessel | Stadt | vocab | 2_stadt_land | Brüssel | Brussels / Bruxelles |

## Round-001 needs_review Re-routing

Round-001 emitted 25 canonicalization candidates. 13 of those reference ids that no longer exist in the live graph and have been dropped. 12 remain (plus 0 with unknown presence because the live DB was unavailable).

| Node id | Kind | Route | Canonical candidate | Present in live graph |
| --- | --- | --- | --- | --- |
| bw_tampere_1980s_office_donor | content | round_003 | 1980er Bürogebäude im Zentrum von Tampere | True |
| land_belgien | vocab | 2_stadt_land | Belgien | True |
| land_deutschland | vocab | 2_stadt_land | Deutschland | True |
| land_schweiz | vocab | 2_stadt_land | Schweiz | True |
| land_vereinigtes_koenigreich | vocab | 2_stadt_land | Vereinigtes Königreich | True |
| mat_textil | vocab | 1_material | Textil | True |
| norm_sci_p427 | vocab | 8_norm_pruefung | SCI P427 protocol | True |
| stadt_basel | vocab | 2_stadt_land | Basel | True |
| stadt_berlin | vocab | 2_stadt_land | Berlin | True |
| stadt_bruessel | vocab | 2_stadt_land | Brüssel | True |
| stadt_london | vocab | 2_stadt_land | London | True |
| stadt_winterthur | vocab | 2_stadt_land | Winterthur | True |

## Patch Output

- Deterministic patch: `_neo4j\review\round_002_baseline\post_apply\patches\global_technical.patch.jsonl`
- Deterministic patch operations: 44
- Round-001 needs_review filtered: `_neo4j\review\round_002_baseline\post_apply\needs_review.patch.jsonl` (12 records).
