# Validation report — batch_011

Validation result: PASS

## Files

| file | nodes | relationships |
|---|---:|---:|
| controlled_terms.delta.jsonl | 1 | 2 |
| p_plattenpalast_berlin.kg.jsonl | 13 | 147 |
| p_plattenvereinigung_berlin.kg.jsonl | 18 | 190 |
| p_plp_london_hq_circular_studio_fitout.kg.jsonl | 18 | 194 |
| p_recrete_footbridge_reused_concrete_blocks.kg.jsonl | 9 | 98 |
| p_recyclinghaus_hannover.kg.jsonl | 22 | 304 |

## Checks

- JSONL schema: PASS
- Manifest schema: PASS
- Relationship endpoints: PASS
- Local node degree ≥ 2: PASS
- `BELEGT_IN.datenqualitaet = Belegt`: PASS
- No `Fallbeispiel` nodes: PASS
- No `Kennwert` nodes: PASS

## Notes

- Controlled terms delta adds `mat_faserzement` only.
- PLP keeps 92% reused/donated as scalar project context and models only fixed fit-out components as Direct Reuse.
- Recyclinghaus keeps recycling concrete as `counts_as_direct_reuse=false` and does not count the new timber structure as Direct Reuse.
- Re:Crete is modeled as infrastructure prototype, not as a building Hauptfall.
