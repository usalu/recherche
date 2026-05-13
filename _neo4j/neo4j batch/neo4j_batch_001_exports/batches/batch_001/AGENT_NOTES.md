# Batch 001 agent notes

This batch follows `neo4j_reuse_graph_v1_1`. Import order for this batch:

1. Ensure global `cypher/constraints.cypher` has already run.
2. Ensure global `controlled_vocabulary.seed.kg.jsonl` has already been imported.
3. Import each `p_*.kg.jsonl` file: nodes first, then relationships.
4. `controlled_terms.delta.jsonl` is empty for this batch.

## Merge decisions

- `Berlin_Schildow_Pilot_House.md` and `Berlin_Schildow_Pilot_House_2.md` are intentionally merged into `p_berlin_schildow_pilot_house.kg.jsonl` because the second file is marked as `ANHANG / ZUSAMMENFÜHREN` and describes the same uncertain Schildow pilot identity.
- `Big_Dig_Building_Boston.md` is not a built direct-reuse case. It is kept as a project node for knowledge completeness, but it has `counts_as_built_direct_reuse=false` and its bauteil group has `counts_as_direct_reuse=false`.

## Quality conventions

- `datenqualitaet` appears only on `BELEGT_IN` relationships and is always `Belegt`.
- City, country, building class, building role, actor role, actor type, status, material, bauteil type, huerde, and method concepts are nodes/relationships, not scalar properties.
- Conflicting numeric facts are stored as min/max or note properties rather than collapsed into a false single value.
