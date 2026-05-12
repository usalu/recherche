# Relation catalogue — `_database/_edges` → Neo4j (plan §7.1)

Generated **2026-05-12 21:57 UTC** by `_scripts/extract_database_relations.py`.

Normative folding: `_scripts/neo4j_relation_fold.py` (same logic as `import_database_folder_to_neo4j.py`). Rows whose endpoints are skipped by the importer are still listed here for vocabulary completeness.

## Files scanned

- `_database/_edges/clean_confirmed_edges.csv` — **13746** rows with a `relation` value

## All distinct `relation` values (46)

| `relation` | rows | Neo4j type | Fold props (audit) |
| --- | ---: | --- | --- |
| `belongs_to_fallstudie` | 1618 | `GEHÖRT_ZU` | `csv_relation=belongs_to_fallstudie`, `rolle=fallbeispiel` |
| `belongs_to_projekt` | 1492 | `GEHÖRT_ZU` | `csv_relation=belongs_to_projekt`, `rolle=fallbeispiel` |
| `has_akteurrolle` | 298 | — (`SKIP_RELATIONS`) |  |
| `has_aufbereitungsverfahren` | 27 | `BENUTZT` | `csv_relation=has_aufbereitungsverfahren` |
| `has_bauaufgabe_intervention` | 87 | `HAT` | `art=intervention`, `csv_relation=has_bauaufgabe_intervention` |
| `has_bauobjekt` | 88 | — (`SKIP_RELATIONS`) |  |
| `has_bauobjektklasse` | 84 | — (`SKIP_RELATIONS`) |  |
| `has_bauobjektrolle` | 108 | — (`SKIP_RELATIONS`) |  |
| `has_bauobjektstatus` | 95 | `HAT` | `art=status`, `csv_relation=has_bauobjektstatus` |
| `has_bausystem` | 66 | `IST` | `csv_relation=has_bausystem` |
| `has_bauteilebene` | 275 | `IST` | `csv_relation=has_bauteilebene` |
| `has_bauteiltyp` | 637 | `IST` | `csv_relation=has_bauteiltyp` |
| `has_bauteilzustand` | 33 | `IST` | `csv_relation=has_bauteilzustand` |
| `has_bauweise` | 154 | `IST` | `csv_relation=has_bauweise` |
| `has_beschaffungsweg` | 17 | `IST` | `csv_relation=has_beschaffungsweg` |
| `has_bewertungslogik_abgrenzung` | 164 | `IST` | `axis=einordnung`, `csv_relation=has_bewertungslogik_abgrenzung` |
| `has_datenmodell` | 59 | — (`SKIP_RELATIONS`) |  |
| `has_datenqualitaet` | 841 | `IST` | `csv_relation=has_datenqualitaet` |
| `has_fuegung_verbindung` | 21 | `HAT` | `art=verbindungstechnik`, `csv_relation=has_fuegung_verbindung` |
| `has_funktionswechsel` | 640 | `IST` | `csv_relation=has_funktionswechsel` |
| `has_huerde` | 726 | `HAT` | `art=huerde`, `csv_relation=has_huerde` |
| `has_leistungsanforderung` | 3 | `IST` | `csv_relation=has_leistungsanforderung` |
| `has_logistik` | 492 | `HAT` | `art=logistik`, `csv_relation=has_logistik` |
| `has_nutzung` | 132 | `HAT` | `art=nutzung`, `csv_relation=has_nutzung` |
| `has_projekt` | 89 | — (`SKIP_RELATIONS`) |  |
| `has_prozessphase` | 394 | `HAT` | `art=prozessphase`, `csv_relation=has_prozessphase` |
| `has_pruefung_nachweis` | 52 | `HAT` | `art=pruefung`, `csv_relation=has_pruefung_nachweis` |
| `has_rechtliche_bedingung` | 724 | `HAT` | `art=recht`, `csv_relation=has_rechtliche_bedingung` |
| `has_reuse_einsatzstatus` | 407 | `HAT` | `art=status`, `csv_relation=has_reuse_einsatzstatus` |
| `has_reuse_strategie` | 248 | `HAT` | `art=wiederverwendungsart`, `axis=reuse_strategie`, `csv_relation=has_reuse_strategie` |
| `has_rueckbauverfahren` | 84 | `BENUTZT` | `csv_relation=has_rueckbauverfahren` |
| `has_schadstoff` | 1 | `HAT` | `art=schadstoff`, `csv_relation=has_schadstoff` |
| `has_tooltyp` | 60 | — (`SKIP_RELATIONS`) |  |
| `has_tragwerksprinzip` | 48 | `IST` | `csv_relation=has_tragwerksprinzip` |
| `has_tragwerkstyp` | 26 | — (`SKIP_RELATIONS`) |  |
| `has_wirtschaft` | 572 | `HAT` | `art=wirtschaft`, `csv_relation=has_wirtschaft` |
| `installed_in_bauobjekt` | 637 | `GEHÖRT_ZU` | `csv_relation=installed_in_bauobjekt`, `rolle=einbauort` |
| `involves_akteur` | 44 | — (`SKIP_RELATIONS`) |  |
| `located_in_ort` | 74 | `GEHÖRT_ZU` | `csv_relation=located_in_ort`, `rolle=stadt` |
| `measured_on_bauobjekt` | 617 | — (`SKIP_RELATIONS`) |  |
| `measures_kennwertdefinition` | 609 | — (`SKIP_RELATIONS`) |  |
| `part_of_reuse_kette` | 84 | `GEHÖRT_ZU` | `csv_relation=part_of_reuse_kette`, `rolle=kette` |
| `references_norm` | 9 | `HAT` | `art=norm`, `csv_relation=references_norm` |
| `relates_to_bauobjekt` | 238 | — (`SKIP_RELATIONS`) |  |
| `uses_material` | 553 | `BENUTZT` | `csv_relation=uses_material` |
| `uses_software_digitaltool` | 19 | `BENUTZT` | `csv_relation=uses_software_digitaltool` |

## Importer endpoint skips (not shown per row)

Edges are dropped before folding when `source_entity` / `target_entity` is in `SKIP_NODE_ENTITIES`, or `datenmodell` / `tooltyp`, or path `fuegung_verbindung/Reversible_Fuegung` — see `import_database_folder_to_neo4j.py`.
