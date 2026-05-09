# Current Graph Structure Report

## Short Answer

- No final move was done.
- The old knowledge base folders still exist.
- The new structure is a staging graph under `_graph`. It is not yet the cleaned final database.
- The migration copied/generated new nodes and edges; it did not replace the old repo.

## Folder Pattern

```text
_graph/
  ENTITAET/
    ID/
      index.md
      DATEIEN/
```

Each `index.md` is a node candidate for Tolaria/SQLite. `DATEIEN` contains copied or supporting source files when available.

## Old Folders Still Present

- Gebäude: True
- tragwerkssystem: True
- bauteilboerse: True
- material: True
- huerde: True
- prozessphase: True

## Current Entity Folders

| entity | node directories | index.md files | DATEIEN files | total files |
|---|---:|---:|---:|---:|
| _system | 0 | 0 | 0 | 13 |
| akteur | 65 | 65 | 57 | 122 |
| akteur_beteiligung | 238 | 238 | 0 | 238 |
| akteurleistung | 0 | 0 | 0 | 0 |
| akteurrolle | 21 | 21 | 0 | 21 |
| akteurtyp | 0 | 0 | 0 | 0 |
| aufbereitungsverfahren | 7 | 7 | 7 | 14 |
| bauaufgabe_intervention | 3 | 3 | 4 | 7 |
| bauobjekt | 88 | 88 | 90 | 178 |
| bauobjekt_beteiligung | 0 | 0 | 0 | 0 |
| bauobjektklasse | 1 | 1 | 1 | 2 |
| bauobjektrolle | 0 | 0 | 0 | 0 |
| bauobjektstatus | 0 | 0 | 0 | 0 |
| bausystem | 3 | 3 | 4 | 7 |
| bauteilebene | 0 | 0 | 0 | 0 |
| bauteiltyp | 53 | 53 | 26 | 79 |
| bauteilzustand | 0 | 0 | 0 | 0 |
| bauweise | 2 | 2 | 2 | 4 |
| beleg | 0 | 0 | 0 | 0 |
| beschaffungsweg | 2 | 2 | 7 | 9 |
| bewertungslogik_abgrenzung | 7 | 7 | 0 | 7 |
| datenmodell | 9 | 9 | 10 | 19 |
| datenpunkt | 619 | 619 | 0 | 619 |
| datenqualitaet | 0 | 0 | 0 | 0 |
| dokumenttyp | 16 | 16 | 18 | 34 |
| fallstudie | 99 | 99 | 101 | 200 |
| foerderprogramm | 5 | 5 | 6 | 11 |
| fuegung_verbindung | 12 | 12 | 12 | 24 |
| funktionswechsel | 0 | 0 | 0 | 0 |
| gebaeudetypologie | 0 | 0 | 0 | 0 |
| huerde | 30 | 30 | 13 | 43 |
| kennwertdefinition | 31 | 31 | 5 | 36 |
| kontextmerkmal | 2 | 2 | 2 | 4 |
| leistungsanforderung | 13 | 13 | 13 | 26 |
| logistik | 6 | 6 | 6 | 12 |
| material | 27 | 27 | 20 | 47 |
| meta | 6 | 6 | 6 | 12 |
| methode | 11 | 11 | 11 | 22 |
| norm | 9 | 9 | 8 | 17 |
| nutzung | 0 | 0 | 0 | 0 |
| ort | 12 | 12 | 12 | 24 |
| plattformfunktion | 0 | 0 | 0 | 0 |
| plattformzugang | 0 | 0 | 0 | 0 |
| programm_kontext | 0 | 0 | 0 | 0 |
| projekt | 89 | 89 | 91 | 180 |
| prozessphase | 9 | 9 | 9 | 18 |
| pruefung_nachweis | 11 | 11 | 11 | 22 |
| quelle | 96 | 96 | 96 | 192 |
| rechtliche_bedingung | 6 | 6 | 6 | 12 |
| ressourcenquelle | 1 | 1 | 6 | 7 |
| reuse_einsatz | 637 | 637 | 0 | 637 |
| reuse_einsatzstatus | 1 | 1 | 1 | 2 |
| reuse_kette | 43 | 43 | 0 | 43 |
| reuse_kettenstation | 86 | 86 | 0 | 86 |
| reuse_strategie | 8 | 8 | 10 | 18 |
| rueckbauverfahren | 5 | 5 | 5 | 10 |
| schadstoff | 5 | 5 | 5 | 10 |
| software_digitaltool | 76 | 76 | 96 | 172 |
| tooltyp | 2 | 2 | 7 | 9 |
| tragwerksprinzip | 4 | 4 | 4 | 8 |
| tragwerkstyp | 9 | 9 | 11 | 20 |
| wirtschaft | 6 | 6 | 6 | 12 |
| zertifizierung_bewertungssystem | 1 | 1 | 1 | 2 |

## Migration Status Summary

| migration_status | node count |
|---|---:|
| migrated_phase4_case_graph | 1899 |
| migrated_phase1_stable_knots | 166 |
| migrated_phase3_core_entities | 137 |
| migrated_phase5_legacy_source | 102 |
| migrated_phase2_semantic_corrections | 61 |
| migrated_phase7_promoted_review_knot | 42 |
| migrated_phase10_huerde_abgrenzung | 24 |
| migrated_phase9_actor_role_knot | 21 |
| migrated_phase12_bauteiltyp_gap | 19 |
| migrated_phase11_kennwertdefinition_gap | 12 |
| migrated_phase8_promoted_repeated_actor | 9 |

## Complete Per-Node Inventory

The complete per-node inventory is here: `_migration/current_graph_node_inventory.csv`.

Columns:
- `entity_folder`: folder under `_graph`.
- `id_folder`: node ID folder.
- `title`: node title from frontmatter.
- `migration_status`: which migration phase created or changed it.
- `came_from`: legacy path when the node records one.
- `action_done`: human-readable description of what was done.
- `path`: exact generated node file.

The complete physical file inventory is here: `_migration/current_graph_file_inventory.csv`.

## Important Warning

There are expected duplicates in this staging graph because one legacy file can become several semantic nodes. Example: a building case can become `fallstudie`, `projekt`, `bauobjekt`, many `reuse_einsatz`, many `datenpunkt`, and `akteur_beteiligung` nodes. That is not a final deduplicated database yet.

The real possible mistake is semantic over-linking: some generated edges classify one raw label into several knots. Those need a QA pass before final import.