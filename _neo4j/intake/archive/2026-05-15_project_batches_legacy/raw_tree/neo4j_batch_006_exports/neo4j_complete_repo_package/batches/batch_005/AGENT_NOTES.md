# Agent notes — batch_005

Import order for MCP/Neo4j agents:

1. Ensure global `controlled_vocabulary.seed.kg.jsonl` and `cypher/constraints.cypher` from the v1.1 contract are already loaded.
2. Import `controlled_terms.delta.jsonl` first. It adds `mat_bitumen`, `mat_textil`, and `prog_recreate`.
3. Import each `*.kg.jsonl` project file idempotently with `MERGE` on node property `id` and relationship property `id`.
4. Do not convert `bewertung`, `flaeche_m2`, counts, CO₂/water/cost/time values, years, or other Kennwerte into separate nodes.
5. Do not create `Fallbeispiel` or `Kennwert` labels.
6. Treat `counts_as_direct_reuse=false` on Bestandserhalt, unclear recycling, or context Bauteilgruppen as intentional.
7. Keep `BELEGT_IN.datenqualitaet` exactly `Belegt`.
8. Several projects contain source conflicts or ranges; they are stored as scalar min/max or conflict-note properties rather than separate Kennwert nodes.
