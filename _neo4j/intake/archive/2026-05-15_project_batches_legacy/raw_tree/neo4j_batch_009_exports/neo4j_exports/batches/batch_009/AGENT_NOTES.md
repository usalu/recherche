# Agent notes — batch_009

Import order:
1. Ensure global `controlled_vocabulary.seed.kg.jsonl` and Neo4j constraints are loaded.
2. Load `controlled_terms.delta.jsonl` for this batch. It is empty in batch_009.
3. Load each project `.kg.jsonl` independently with idempotent upsert by top-level `id`.
4. Merge relationships by top-level relationship `id`.

Modeling notes:
- `Projekt` is the central node; no `Fallbeispiel` emitted.
- `Kennwert` is not a node; metrics are scalar properties on `Projekt` or `Bauteilgruppe`.
- `datenqualitaet` appears only on `BELEGT_IN` and is always `Belegt`.
- Direct reuse is separated from Bestandserhalt, recycling and new bio-based construction.
- The five chunks are safe for parallel MCP agents because they use deterministic IDs and contain their own local source, building, actor and component nodes.
