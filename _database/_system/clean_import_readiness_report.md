# Phase 22 Clean Import Readiness Report

## Outputs

- _database/_system/node_inventory.csv
- _database/_edges/clean_confirmed_edges.csv
- _database/_edges/clean_edge_review_queue.csv
- _database/_system/sqlite_schema.sql

## Counts

- Clean database nodes: 3003
- Original phase-6 confirmed edges: 7923
- Clean importable edges: 7695
- Clean edges with normalized endpoint/relation: 252
- Edges held for review: 228
- Relation-target mismatches: 0

## Clean Edges By Relation

| relation | rows |
|---|---:|
| belongs_to_fallstudie | 1618 |
| belongs_to_projekt | 1492 |
| has_bauteiltyp | 700 |
| installed_in_bauobjekt | 637 |
| measured_on_bauobjekt | 617 |
| measures_kennwertdefinition | 609 |
| uses_material | 554 |
| has_huerde | 391 |
| has_akteurrolle | 298 |
| relates_to_bauobjekt | 238 |
| has_bewertungslogik_abgrenzung | 170 |
| has_projekt | 89 |
| has_bauobjekt | 88 |
| part_of_reuse_kette | 84 |
| has_pruefung_nachweis | 48 |
| involves_akteur | 44 |
| references_norm | 9 |
| has_tragwerkstyp | 6 |
| has_leistungsanforderung | 3 |

## Edge Review Reasons

| reason | rows |
|---|---:|
| target_manual_review | 208 |
| source_manual_review | 9 |
| target_ambiguous_split | 6 |
| source_not_imported; target_not_imported | 5 |

## Import Rule

Import only clean_confirmed_edges.csv automatically. Keep clean_edge_review_queue.csv out of the graph until each row is manually approved.
