# Agent notes — batch_012

- Import order: load the global controlled vocabulary seed once, then import this batch JSONL files. Repeated IDs are intended to MERGE.
- Treat `bewertung` as scalar on `Projekt`, not as a node.
- Treat all metric fields as scalar properties on `Projekt` or `Bauteilgruppe`.
- Use `BELEGT_IN` to connect every emitted evidence-bearing node to its case markdown `Quelle`; the relationship property is always `datenqualitaet: Belegt`.
- Roots in the Sky is deliberately preserved as a planned/failed learning case: useful for market, certification and timing hurdles, but not to be counted as built direct reuse.
- Resource Rows has intentionally sparse numeric metrics because the source file marks quantities, CO₂, area and donor data as unknown/uncertain.
