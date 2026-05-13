# Agent notes — batch_004

Import order for MCP/Neo4j agents:

1. Ensure global `controlled_vocabulary.seed.kg.jsonl` and `cypher/constraints.cypher` from the v1.1 contract are already loaded.
2. Import `controlled_terms.delta.jsonl` for the new CROW-CUR guideline node.
3. Import each `*.kg.jsonl` project file idempotently with `MERGE` on node property `id` and relationship property `id`.
4. Do not convert `bewertung`, `flaeche_m2`, counts, CO₂ values, years, or other Kennwerte into separate nodes.
5. Do not create `Fallbeispiel` or `Kennwert` labels.
6. Treat `counts_as_direct_reuse=false` on Bestandserhalt, surplus/restposten, remanufacturing, or not-yet-built planned reuse as intentional.
7. Keep `BELEGT_IN.datenqualitaet` exactly `Belegt`.
