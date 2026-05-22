# Property cleanup apply summary

- Run: `property_cleanup_2026_06_05`
- Completed: 2026-06-05T15:39:48.261360+00:00

## Final stats

- Nodes: 2273
- Relationships: 15118
- Distinct node keys: 57 (was 107)
- Distinct rel keys: 22 (was 63)
- Avg props/node: 5.452 (was 8.2)
- Avg props/rel: 1.755 (was 4.3)

## Acceptance

- `nodes_with_phase_keys`: 0
- `legacy_internal_provenance_docs`: 0
- `rf_rechtsgrundlagen`: 0
- `import_decision_rels`: 0
- `merged_legacy_rel_ids_rels`: 0
- `source_scope_nodes`: 0
- `reuse_rule_nodes`: 20

## Regulation parity

- `gestuetzt_auf_regelwerk`: 167
- `gilt_in_land`: 281
- `triggers`: 1100
- `erfordert`: 1483

## Follow-up (Phases 4b, 5b, 9)

- Completed: 2026-06-05T20:29:56.228971+00:00
- Sidecar file: `_neo4j/review/2026-06-05_post_migration_property_cleanup/sidecar/entity_metadata.jsonl`

### Sidecar counts

- Rel `metadata_sidecar_key`: 615
- Node `metadata_sidecar_key`: 607
- Remaining `review_status` rels: 0
- Remaining `evidence_status` rels: 0
- Remaining `review_run` rels: 0
- Remaining `source_titles` nodes: 1001 (human titles only; no `.md`)
- Nodes with `.md` in `source_titles`: 0
- `source_urls` nodes unchanged: 404

### Regulation drift vs baseline

- `triggers`: 1130 (baseline 1100, delta +30)
- `erfordert`: 1578 (baseline 1483, delta +95)
- `gestuetzt_auf_regelwerk`: 167 (baseline 167, delta +0)
- `gilt_in_land`: 281 (baseline 281, delta +0)
