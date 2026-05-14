# Batch 014 Validation Report

Generated files: 6 project chunks.

## Summary

- **p_trae_high_rise_aarhus.kg.jsonl** — PASS; nodes=32; relationships=218; missing_endpoints=0; nodes_lt_2_edges=0; schema_errors=0
- **p_upcycle_studios_copenhagen.kg.jsonl** — PASS; nodes=24; relationships=156; missing_endpoints=0; nodes_lt_2_edges=0; schema_errors=0
- **p_verbiest_karreveld_brussels.kg.jsonl** — PASS; nodes=31; relationships=241; missing_endpoints=0; nodes_lt_2_edges=0; schema_errors=0
- **p_villa_welpeloo_enschede.kg.jsonl** — PASS; nodes=28; relationships=185; missing_endpoints=0; nodes_lt_2_edges=0; schema_errors=0
- **p_woongroep_boschgaard_den_bosch.kg.jsonl** — PASS; nodes=29; relationships=219; missing_endpoints=0; nodes_lt_2_edges=0; schema_errors=0
- **p_zinneke_feder_masui4ever_brussels.kg.jsonl** — PASS; nodes=26; relationships=245; missing_endpoints=0; nodes_lt_2_edges=0; schema_errors=0

## Checks applied

- JSONL records validate against `schemas/kg_jsonl_record_schema.json`.
- All relationship endpoints exist either in the same project chunk or in `controlled_vocabulary.seed.kg.jsonl`.
- All emitted project-specific nodes have at least two incident edges. Controlled vocabulary seed nodes are exempt because they are global shared terms.
- `Datenqualitaet` appears only as `{"datenqualitaet":"Belegt"}` on `BELEGT_IN` relationships.
- `Kennwert` is not emitted as a node; numeric metrics are properties on `Projekt`, `Bauwerk`, or `Bauteilgruppe`.
- No `Fallbeispiel` records are emitted; `Projekt` is the central project node.

## Notes

- `controlled_terms.delta.jsonl` is intentionally empty: all newly emitted non-seed terms in this batch are project/shared concrete entities such as `Stadt`, `Land`, `Quelle`, `Bauwerk`, `Akteur`, `Bauteilgruppe`, or `Wiederverwendungskette`, not new controlled vocabulary classes.
- External sources listed in each markdown file are captured as `Quelle` nodes and cited from the markdown source node via `ZITIERT_QUELLE`.
