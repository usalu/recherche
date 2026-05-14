# Final Final Approval Preview

Nothing has been moved. This is the complete proposed final preview for approval.

## Review These Files

- Full semantic node tree: _migration/final_final_tree_all_nodes.md
- Every old file archived once: _migration/final_final_legacy_source_tree.md
- Node approval matrix: _migration/final_final_node_approval_matrix.csv

## Final File Count Preview

- Semantic/core/knot node files: 2,390
- Schema-only final folders: 9
- Old source archive node files: 567
- Total proposed final index.md files: 2,957

Important: the current staging graph has only 96 `quelle` nodes. The clean final version should instead archive all 567 old mapped files once under `quelle`.
The 9 schema-only folders are included in the final ontology but should not create fake nodes.

## Decision Summary

| final_status | nodes |
|---|---:|
| hold_out_of_final | 6 |
| include_final | 2482 |
| include_if_approved | 4 |

## Proposed Entities And Knots

| folder | role | node files |
|---|---|---:|
| akteur | core entity | 65 |
| akteur_beteiligung | core entity | 238 |
| akteurrolle | controlled knot | 21 |
| aufbereitungsverfahren | controlled knot | 7 |
| bauaufgabe_intervention | controlled knot | 3 |
| bauobjekt | core entity | 88 |
| bauobjekt_beteiligung | core entity schema | 0 current nodes |
| bauobjektklasse | controlled knot | 1 |
| bauobjektrolle | controlled knot schema | 0 current nodes |
| bauobjektstatus | controlled knot schema | 0 current nodes |
| bausystem | controlled knot | 3 |
| bauteilebene | controlled knot schema | 0 current nodes |
| bauteiltyp | controlled knot | 53 |
| bauteilzustand | controlled knot schema | 0 current nodes |
| bauweise | controlled knot | 2 |
| beschaffungsweg | controlled knot | 2 |
| bewertungslogik_abgrenzung | controlled knot | 7 |
| datenqualitaet | controlled knot schema | 0 current nodes |
| datenmodell | controlled knot | 9 |
| datenpunkt | core entity | 619 |
| dokumenttyp | controlled knot | 16 |
| fallstudie | core entity | 99 |
| foerderprogramm | controlled knot | 5 |
| fuegung_verbindung | controlled knot | 12 |
| funktionswechsel | controlled knot schema | 0 current nodes |
| huerde | controlled knot | 30 |
| kennwertdefinition | controlled knot | 31 |
| kontextmerkmal | controlled knot | 2 |
| leistungsanforderung | controlled knot | 13 |
| logistik | controlled knot | 6 |
| material | controlled knot | 27 |
| methode | controlled knot | 11 |
| norm | controlled knot | 9 |
| nutzung | controlled knot schema | 0 current nodes |
| ort | controlled knot | 12 |
| programm_kontext | controlled knot schema | 0 current nodes |
| projekt | core entity | 89 |
| prozessphase | controlled knot | 9 |
| pruefung_nachweis | controlled knot | 11 |
| quelle | source archive entity | 567 old files |
| rechtliche_bedingung | controlled knot | 6 |
| ressourcenquelle | controlled knot | 1 |
| reuse_einsatz | core entity | 637 |
| reuse_einsatzstatus | auxiliary controlled knot | 1 |
| reuse_kette | core entity | 43 |
| reuse_kettenstation | core entity | 86 |
| reuse_strategie | controlled knot | 8 |
| rueckbauverfahren | controlled knot | 5 |
| schadstoff | controlled knot | 5 |
| software_digitaltool | core entity | 76 |
| tooltyp | controlled knot | 2 |
| tragwerksprinzip | controlled knot | 4 |
| tragwerkstyp | controlled knot | 9 |
| wirtschaft | controlled knot | 6 |
| zertifizierung_bewertungssystem | controlled knot | 1 |

## Source Of Final Nodes

| origin | node files |
|---|---:|
| generated actor from repeated case label | 9 |
| generated controlled knot | 118 |
| old knowledge | 364 |
| source archive / old knowledge | 567 old files |
| split reuse/building examples | 1899 |

## Hold / Exclude

Hold out of first final version:
- meta

Exclude empty or immature folders:
- akteurleistung
- akteurtyp
- beleg
- gebaeudetypologie
- plattformfunktion
- plattformzugang

## Final Shape

```text
_database/
  entity/id/index.md
  _edges/edges_reviewed.csv
  _edges/edges_review_queue.csv
```

Rule: full old text lives once in quelle; domain nodes become clean summaries/facts, not duplicated old files.
