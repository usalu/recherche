# Round 001 Global Technical Audit

Generated: 2026-05-14T11:46:33.517637+00:00

## Summary

| Metric | Value |
| --- | --- |
| batches | 20 |
| project_files | 97 |
| files_scanned | 114 |
| nodes_unique | 1699 |
| relationships_unique | 14028 |
| parse_errors | 0 |
| schema_errors | 0 |
| manifest_errors | 6 |
| overlay_errors | 0 |
| overlay_nodes | 2 |
| overlay_relationships | 0 |
| missing_endpoints | 0 |
| duplicate_node_conflicts | 74 |
| duplicate_node_conflict_ids | 25 |
| duplicate_relationship_conflicts | 0 |
| forbidden_nodes | 0 |
| bad_belegt_in | 0 |
| projects_no_source | 0 |
| projects_no_component_or_work | 2 |
| bg_no_source | 0 |
| bg_no_type | 0 |
| bg_no_material_or_level | 0 |

## Current Batch Selection

| Batch | Path | Projects | Manifest | Delta | Delta rows |
| --- | --- | --- | --- | --- | --- |
| batch_001 | _neo4j\batch\neo4j_batch_001_exports\batches\batch_001 | 4 | yes | yes | 0 |
| batch_002 | _neo4j\batch\neo4j_batch_002_exports\neo4j_exports\batches\batch_002 | 5 | yes | yes | 2 |
| batch_003 | _neo4j\batch\neo4j_batch_003_exports\batches\batch_003 | 5 | yes | yes | 12 |
| batch_004 | _neo4j\batch\neo4j_batch_004_exports\neo4j_exports\batches\batch_004 | 5 | yes | yes | 4 |
| batch_005 | _neo4j\batch\neo4j_batch_005_exports\neo4j_exports\batches\batch_005 | 5 | yes | yes | 9 |
| batch_006 | _neo4j\batch\neo4j_batch_006_exports\neo4j_complete_repo_package\batches\batch_006 | 5 | yes | yes | 10 |
| batch_007 | _neo4j\batch\neo4j_batch_007_exports\neo4j_exports\batches\batch_007 | 5 | yes | yes | 10 |
| batch_008 | _neo4j\batch\neo4j_batch_008_exports\neo4j_exports\batches\batch_008 | 5 | yes | yes | 11 |
| batch_009 | _neo4j\batch\neo4j_batch_009_exports\neo4j_exports\batches\batch_009 | 5 | yes | yes | 0 |
| batch_010 | _neo4j\batch\neo4j_batch_010_exports\neo4j_exports\batches\batch_010 | 5 | yes | yes | 0 |
| batch_011 | _neo4j\batch\neo4j_batch_011_exports\neo4j_exports\batches\batch_011 | 5 | yes | yes | 3 |
| batch_012 | _neo4j\batch\neo4j_batch_012_exports\neo4j_exports\batches\batch_012 | 5 | yes | yes | 0 |
| batch_013 | _neo4j\batch\neo4j_batch_013_exports\neo4j_exports\batches\batch_013 | 5 | yes | yes | 2 |
| batch_014 | _neo4j\batch\neo4j_batch_014_exports\neo4j_exports\batches\batch_014 | 6 | yes | yes | 0 |
| batch_015 | _neo4j\batch\neo4j_batch_015_exports\neo4j_exports\batches\batch_015 | 5 | no | yes | 1 |
| batch_016 | _neo4j\batch\neo4j_batch_016_exports\neo4j_exports\batches\batch_016 | 5 | no | no | 0 |
| batch_017 | _neo4j\batch\neo4j_batch_017_exports\neo4j_exports\batches\batch_017 | 5 | no | no | 0 |
| batch_018 | _neo4j\batch\neo4j_batch_018_exports\neo4j_exports\batches\batch_018 | 4 | no | no | 0 |
| batch_019 | _neo4j\batch\neo4j_batch_019_exports\neo4j_exports\batches\batch_019 | 4 | no | yes | 1 |
| batch_020 | _neo4j\batch\neo4j_batch_020_exports\neo4j_exports\batches\batch_020 | 4 | no | no | 0 |

## Accepted Patch Overlay

- Overlay patches: _neo4j\review\round_001\patches\accepted_blockers.patch.jsonl
- Overlay nodes: 2
- Overlay relationships: 0
- Overlay errors: 0

## Blocking Findings

- Missing relationship endpoints: none
- Missing manifests: batch_015, batch_016, batch_017, batch_018, batch_019, batch_020
- Missing controlled term delta files: batch_016, batch_017, batch_018, batch_020

## Missing Endpoint Details

| Missing id | Side | Relationship | File | Line |
| --- | --- | --- | --- | --- |
| none |  |  |  |  |

## Duplicate Node Property Conflicts

25 unique node ids have conflicting properties across export files.

| Node id | Canonical candidate | Aliases |
| --- | --- | --- |
| a_arup | Arup |  |
| a_bellastock | Bellastock |  |
| a_cleveland_steel_tubes | Cleveland Steel & Tubes | Cleveland Steel and Tubes |
| a_die_zusammenarbeiter | Die Zusammenarbeiter | Die Zusammenarbeiter GmbH |
| a_encore_heureux | Encore Heureux | Encore Heureux Architectes |
| a_imd_raadgevende_ingenieurs | IMd Raadgevende Ingenieurs | IMd raadgevende ingenieurs |
| a_immobilien_basel_stadt | Immobilien Basel-Stadt |  |
| a_lxsy_architektur | LXSY Architektur |  |
| a_rotor | ROTOR | Rotor |
| a_symmetrys | Symmetrys |  |
| a_trnsfrm_eg | TRNSFRM eG |  |
| bw_halle_2_ringberlin | Halle 2 ringberlin – Sheddach 1938 |  |
| bw_lysbuechel_parkhaus_basel | Lysbuechel Parkhaus Basel | Lysbuechel Parkhaus Basel (Spender) |
| bw_tampere_1980s_office_donor | 1980er Bürogebäude im Zentrum von Tampere | Bürogebäude der frühen 1980er Jahre im Zentrum Tampere |
| land_belgien | Belgien |  |
| land_deutschland | Deutschland |  |
| land_schweiz | Schweiz |  |
| land_vereinigtes_koenigreich | Vereinigtes Königreich | Vereinigtes Koenigreich |
| mat_textil | Textil | Textil / textile Fasern, Textil / Filz / textile Fasern |
| norm_sci_p427 | SCI P427 protocol | SCI P427 Structural Steel Reuse |
| stadt_basel | Basel |  |
| stadt_berlin | Berlin |  |
| stadt_bruessel | Brüssel | Brussels / Bruxelles |
| stadt_london | London |  |
| stadt_winterthur | Winterthur |  |

## Schema And Integrity Notes

- JSON parse errors: 0
- Record schema errors: 0
- Manifest errors: 6
- Overlay errors: 0
- Forbidden nodes: 0
- BELEGT_IN without datenqualitaet=Belegt: 0
- Projekt without BELEGT_IN: 0
- Bauteilgruppe without BELEGT_IN: 0
- Bauteilgruppe without HAT_BAUTEILTYP: 0

## Patch Output

- Patch file: `_neo4j\review\round_001_after_apply_overlay\patches\global_technical.patch.jsonl`
- Patch operations: 25
- Generated placeholders live under `_neo4j\review\round_001_after_apply_overlay\placeholders` and are review outputs only.
