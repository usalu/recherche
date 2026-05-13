# Agent Notes — Batch 014

## Import order
1. Ensure `controlled_vocabulary.seed.kg.jsonl` from the repo contract has already been imported.
2. Import project files in `batches/batch_014/*.kg.jsonl` using node pass first, relationship pass second.
3. `controlled_terms.delta.jsonl` is empty for this batch.

## Modelling decisions
- Each original markdown file maps to one central `Projekt` node.
- `Fallbeispiel` is not used.
- `Stadt`, `Land`, `Bauobjektklasse`, `Bauobjektrolle`, `Akteurrolle`, `Akteurtyp`, `Bauteiltyp`, `Material`, `Materialgruppe`, `Huerde`, and `HuerdeKategorie` are represented as nodes and relationships rather than scalar properties.
- `Datenqualitaet` remains only on `BELEGT_IN` relationships and is always `Belegt`.
- Reuse metrics and quantities are properties on the directly scoped object. Conflicting figures use min/max and notes.
- Source files and external source links are all represented as `Quelle` nodes.

## Batch source files
- TRAE_High_Rise_Aarhus.md
- Upcycle_Studios_Copenhagen.md
- Verbiest_Karreveld_Brussels.md
- Villa_Welpeloo_Enschede.md
- Woongroep_Boschgaard_Den_Bosch.md
- Zinneke_Feder_Masui4ever_Brussels.md
