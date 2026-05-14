# Agent notes — batch_006

Import order for MCP/Neo4j agents:

1. Ensure global `controlled_vocabulary.seed.kg.jsonl` and `cypher/constraints.cypher` from the v1.1 contract are loaded first.
2. Import `controlled_terms.delta.jsonl` before project files. It adds `mat_mdf`, `mat_textil`, `norm_sci_p427`, and `norm_sci_p440`.
3. Import each `*.kg.jsonl` file independently and idempotently with `MERGE` on node property `id` and relationship property `id`.
4. Do not generate `Fallbeispiel` or `Kennwert` nodes.
5. Keep metrics such as `bewertung`, `flaeche_m2`, `wiederverwendeter_stahl_t`, CO₂ values, costs, counts, years and ranges as scalar properties on the most relevant node.
6. Keep `BELEGT_IN.datenqualitaet` exactly `Belegt`.
7. Respect `counts_as_direct_reuse=false` for retained structures, furniture, recycling-only, and weakly documented/uncertain component groups.
8. House of Fraser/TBC contains unresolved public tonnage conflicts; do not collapse those properties into a single asserted value.
