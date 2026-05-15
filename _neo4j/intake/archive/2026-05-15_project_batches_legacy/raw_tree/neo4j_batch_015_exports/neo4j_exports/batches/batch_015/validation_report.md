# Validation report — requested cases batch v2

Schema version: `neo4j_reuse_graph_v1_1`

## Result

PASS — JSONL is syntactically valid, records validate against the v1.1 schema, and all relationship endpoints resolve either inside the same project file or in `controlled_vocabulary.seed.kg.jsonl`.

## Project files

- p_55_great_suffolk_street_london.kg.jsonl: 112 records (18 nodes, 94 relationships)
- p_bedzed_london_hackbridge.kg.jsonl: 113 records (17 nodes, 96 relationships)
- p_association_house_groeditz.kg.jsonl: 72 records (10 nodes, 62 relationships)
- p_association_house_plauen.kg.jsonl: 47 records (7 nodes, 40 relationships)
- p_awm_muenster_circular_office.kg.jsonl: 151 records (19 nodes, 132 relationships)

## Notes

- `Fallbeispiel` is not used; each case is modeled as `Projekt`.
- `datenqualitaet` appears only on `BELEGT_IN` relationships and is always `Belegt`.
- Numeric metrics are properties on `Projekt` or `Bauteilgruppe`, not separate Kennwert nodes.
- `Association house, Gröditz` and `Association house, Plauen` are intentionally compact old-case representations: one or two grouped `Bauteilgruppe` records instead of dozens of uncertain subtype rows.
- `AWM Münster` remains a comparison/appendix-style interior case with rating 2 and explicit notes excluding loose furniture from direct-reuse scoring.
- `controlled_terms.delta.jsonl` is empty because the few project-specific terms required for import are included directly in the corresponding project file.
