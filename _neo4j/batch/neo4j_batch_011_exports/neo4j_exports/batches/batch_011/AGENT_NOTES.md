# Agent notes — batch_011

Import order for MCP/Neo4j agents:

1. Ensure global `controlled_vocabulary.seed.kg.jsonl` and constraints are loaded.
2. Import `controlled_terms.delta.jsonl` for this batch.
3. Import each `p_*.kg.jsonl` project chunk.
4. Use `id` as the stable Neo4j merge key for every node and relationship.

Modeling notes:

- `Projekt` is the central node. No `Fallbeispiel` nodes are emitted.
- `Bauteilgruppe` is used for counted reuse components and important separated non-counted circular components.
- `Kennwert` is never emitted as a node; values are scalar properties on project or component-group nodes.
- `datenqualitaet` is only a property on `BELEGT_IN` and always equals `Belegt`.
- Cities, countries, actor roles/types, building classes/roles, materials, methods and hurdles are connected nodes where possible.
- PLP fit-out: loose furniture, sofas, loose tables and decoration are excluded from counted Direct Reuse.
- Recyclinghaus: Fassade and fixed interior reuse are counted; recycling concrete and new timber structure are explicitly separated.
- Re:Crete: kept as infrastructure prototype / research demonstrator; useful technical Direct Reuse case but not a building Hauptfall.
