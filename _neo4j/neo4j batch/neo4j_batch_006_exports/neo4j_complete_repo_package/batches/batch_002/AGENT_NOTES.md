# Agent notes — batch_002

This batch is optimized for MCP import into Neo4j.

Import order:
1. Load `neo4j_repo_output_contract_v2/cypher/constraints.cypher` once in the database.
2. Load `controlled_vocabulary.seed.kg.jsonl` once.
3. Review and load `controlled_terms.delta.jsonl` for `mat_textil`.
4. Load project `.kg.jsonl` files: nodes first, relationships second.

Important modeling choices:
- No `Fallbeispiel` nodes are used.
- No `Kennwert` nodes are used; values are properties on the scoped entity.
- `BELEGT_IN` always points to the project markdown source `Quelle` and always has `datenqualitaet: "Belegt"`.
- External URLs are stored on each markdown `Quelle` as `external_sources` to preserve provenance without creating one-edge source nodes.
- Known source conflicts are stored as min/max properties and/or `note` fields.
- `counts_as_direct_reuse` is retained on `Bauteilgruppe` for ingestion filters and QA, especially where materials are context or experimental rather than direct structural reuse.
