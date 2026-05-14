# Agent notes — batch_010

Import order for this batch:

1. Ensure global `controlled_vocabulary.seed.kg.jsonl` has been imported.
2. Review/import `controlled_terms.delta.jsonl` (empty for this batch).
3. Import every `p_*.kg.jsonl` file using node upserts first, then relationship upserts.

Modeling notes:

- `Projekt` is the central entity. No `Fallbeispiel` nodes are emitted.
- Metrics are scalar properties; no `Kennwert` nodes are emitted.
- `BELEGT_IN` carries `datenqualitaet: "Belegt"` only.
- Bestandserhalt, furniture and loose decoration are not counted as Direct Reuse component groups.
- Montessori Maassluis is a watchlist/planned case; the hollow-core slab component group has `planned_reuse: true` and `counts_as_direct_reuse: false` until as-built evidence exists.
- People’s Pavilion is a temporary demonstrator; borrowed fixed construction elements are counted, loose furniture is excluded, and Pretty Plastic shingles are modeled as upcycling/recycling rather than classic component reuse.
