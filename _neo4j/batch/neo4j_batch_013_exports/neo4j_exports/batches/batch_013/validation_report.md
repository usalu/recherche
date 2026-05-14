# Validation report — batch_013

Generated: 2026-05-13T19:28:15Z

## Files
- `p_superlocal_expogebouw_bleijerheide.kg.jsonl` — 20 nodes, 212 relationships
- `p_svanen_kindergarten_gladsaxe.kg.jsonl` — 20 nodes, 243 relationships
- `p_the_green_house_utrecht.kg.jsonl` — 22 nodes, 234 relationships
- `p_thoravej_29_copenhagen.kg.jsonl` — 16 nodes, 178 relationships
- `p_timber_square_london.kg.jsonl` — 24 nodes, 246 relationships
- `controlled_terms.delta.jsonl` — 2 controlled nodes, 0 relationships

## Checks
- JSONL parse: PASS
- Schema validation: PASS
- Relationship endpoints resolvable against seed + delta + batch: PASS
- Batch-local node degree >= 2: PASS
- BELEGT_IN datenqualitaet convention: PASS (all generated BELEGT_IN relationships use `datenqualitaet: Belegt`)

## Errors / warnings
- None blocking.

## Modeling notes
- `Projekt` is the only case/root node; no `Fallbeispiel` node is emitted.
- `Stadt`, `Land`, `Bauobjektklasse`, `Bauobjektrolle`, `Akteurrolle`, `Akteurtyp`, `Bauteiltyp`, `Materialgruppe`, `HuerdeKategorie` and related controlled concepts are modeled as nodes/relationships, not scalar properties.
- `Kennwert` is not emitted as a node; measurable values are scalar properties on `Projekt` or `Bauteilgruppe`.
- `Quelle` nodes are the source-of-truth targets; all generated local nodes and additional controlled terms are connected through `BELEGT_IN`.
- Methodological boundary cases are represented as `Bauteilgruppe` where useful, but with `direct_reuse_relevant:false` and appropriate `WiederverwendungsArt` such as `Bestandserhalt`, `Recycling`, or `Design_for_Disassembly`.
