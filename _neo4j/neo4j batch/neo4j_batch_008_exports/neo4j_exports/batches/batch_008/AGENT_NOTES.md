# Agent notes — batch_008

Import order for MCP agents:

1. Ensure global `controlled_vocabulary.seed.kg.jsonl` has already been imported.
2. Import `controlled_terms.delta.jsonl` for this batch before project chunks.
3. Import project `.kg.jsonl` files independently and idempotently by `id`.
4. Upsert relationships by relationship `id`.

Batch-specific cautions:

- Kamikatsu includes strong public/educational zero-waste narrative, but fixed building reuse is separated from loose furniture and decoration.
- Kindergarten Mööslistrasse includes cost/THG metrics as scalar properties only; no Kennwert nodes.
- Liander/Alliander HQ is intentionally conservative because published information emphasizes circular transformation and energy strategy more than concrete direct-reuse component lists.
- Lo-Reninge is a facade/brick-reuse case; the former convent is not counted as direct reuse.
- Lokomotion is in construction and should be treated as a ReCreate mini-pilot; the reused slabs are real, but small relative to the total industrial project.
