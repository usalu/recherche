# Validation report — batch_001

## Files transformed

- `Berlin_Schildow_Pilot_House.md`
- `Berlin_Schildow_Pilot_House_2.md`
- `Bestandverplanzung_Pavilion_Muenchen.md`
- `Big_Dig_Building_Boston.md`
- `Big_Dig_House_Lexington_Massachusetts.md`

## Output project files

- `p_berlin_schildow_pilot_house.kg.jsonl`: 14 nodes, 98 relationships, 1 Projekt, 1 Bauteilgruppe, 2 Quelle
- `p_bestandverplanzung_pavilion_muenchen.kg.jsonl`: 7 nodes, 50 relationships, 1 Projekt, 1 Bauteilgruppe, 1 Quelle
- `p_big_dig_building_boston.kg.jsonl`: 12 nodes, 81 relationships, 1 Projekt, 1 Bauteilgruppe, 1 Quelle
- `p_big_dig_house_lexington_massachusetts.kg.jsonl`: 14 nodes, 119 relationships, 1 Projekt, 3 Bauteilgruppe, 1 Quelle

## Batch-specific modeling decisions

- Schildow Pilot House 1 and 2 are merged into one canonical `Projekt` to avoid duplicate graph entities.
- Big Dig Building is preserved as a proposed/aborted reuse concept, not as a built reuse case.
- No new controlled vocabulary terms were required; `controlled_terms.delta.jsonl` is empty.
- All `BELEGT_IN` relationships use `{"datenqualitaet":"Belegt"}`.
- `stadt`, `land`, `bauobjektklasse`, `bauobjektrolle`, `akteurrolle`, `akteurtyp`, `status`, `bauteiltyp`, `material`, `huerde`, and process concepts are modeled as connected nodes, not properties.
- Graph hygiene check passed: no project-file node has fewer than 2 incident relationships inside its own `.kg.jsonl` file.

## Validation result

PASSED: JSONL syntax, JSON schema, manifest schema, and relationship endpoint checks passed.
