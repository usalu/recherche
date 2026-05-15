# Validation Checklist v1.1

## File structure

- [ ] File extension is `.kg.jsonl`.
- [ ] Every line is valid JSON.
- [ ] Every line validates against `schemas/kg_jsonl_record_schema.json`.
- [ ] No comments, markdown, trailing commas, or null values.
- [ ] Manifest validates against `schemas/manifest_schema.json`.

## Import readiness

- [ ] `controlled_vocabulary.seed.kg.jsonl` was imported before project files.
- [ ] `cypher/constraints.cypher` was run or equivalent constraints exist.
- [ ] Importer materializes top-level record `id` as Neo4j property `id`.
- [ ] Node records are imported before relationship records.

## Project file checks

- [ ] One normal project file has exactly one `Projekt` node.
- [ ] At least one `Quelle` node exists.
- [ ] `Projekt` has `BELEGT_IN` to the markdown `Quelle` with `datenqualitaet:"Belegt"`.
- [ ] At least one `Bauteilgruppe` exists.
- [ ] Every `Bauteilgruppe` has `HAT_BAUTEILTYP`, `NUTZT_MATERIAL`, and `BELEGT_IN`.
- [ ] Every `Bauwerk` has `HAT_BAUOBJEKTKLASSE`, `HAT_BAUOBJEKTROLLE`, and `BELEGT_IN`.
- [ ] Every `Akteur` has `HAT_AKTEURROLLE`, `HAT_AKTEURTYP` when inferable, and `BELEGT_IN`.
- [ ] Every relationship endpoint exists in the project file, controlled vocabulary seed, or controlled terms delta.

## Modeling checks

- [ ] `Fallbeispiel` is not used.
- [ ] `Datenqualitaet` is not a node.
- [ ] `Kennwert` is not a node.
- [ ] `stadt`, `land`, `bauobjektklasse`, `bauobjektrolle`, `bauteiltyp`, `material`, `huerde`, `akteurrolle`, `status`, `nutzung`, `norm`, and `pruefung` are not stored as reusable concept properties.
- [ ] Metrics are scalar properties on `Projekt`, `Bauwerk`, or `Bauteilgruppe`.
- [ ] Uncertainty and source conflicts are captured with `note` or min/max properties.
