# Validation report — batch_002

## Files

- `p_biopartner_5_leiden_oegstgeest.kg.jsonl`: 21 nodes, 137 relationships
- `p_bluecity_offices_rotterdam.kg.jsonl`: 18 nodes, 108 relationships
- `p_boulder_fire_station_3.kg.jsonl`: 18 nodes, 114 relationships
- `p_brent_cross_town_primary_substation_london.kg.jsonl`: 23 nodes, 138 relationships
- `p_brighton_waste_house_brighton.kg.jsonl`: 18 nodes, 133 relationships
- `controlled_terms.delta.jsonl`: 1 nodes, 1 relationships

## Checks

- JSON schema: PASS
- Manifest schema: PASS
- Relationship endpoints: PASS against batch files + controlled vocabulary seed
- BELEGT_IN `datenqualitaet`: PASS, always `Belegt`
- Forbidden legacy properties removed: PASS
- No `Fallbeispiel` or `Kennwert` nodes: PASS
- Generated node degree >= 2 within batch/global endpoint graph: PASS
- Minimum per-project requirements: PASS

## Modeling notes

- `Bewertung` is kept as a scalar property on `Projekt`.
- City, country, Bauobjektklasse, Bauobjektrolle, Akteurrolle, and Akteurtyp are modeled as nodes/relationships, not scalar properties.
- Quantitative values such as area, reused mass, CO₂ saving, dates, and counts are scoped as properties on `Projekt`, `Bauwerk`, or `Bauteilgruppe`.
- External source URLs are stored on the markdown `Quelle.external_sources` arrays to keep source provenance without creating one-edge external-source nodes.
- `mat_textil` is the only proposed controlled term in this batch; it is used by Brighton Waste House textile/infill material groups.
