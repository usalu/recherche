# Validation report — batch_003

## Schema validation
PASS — every JSONL record validates against `kg_jsonl_record_schema.json`.

## Node degree check
PASS — every node emitted inside each project file and delta file has at least 2 incident relationships within that file. External seed vocabulary nodes are referenced but not re-emitted.

## File counts
| file | nodes | relationships |
|---|---:|---:|
| controlled_terms.delta.jsonl | 3 | 9 |
| p_broethen_twin_house_hoyerswerda.kg.jsonl | 9 | 88 |
| p_cascadeup_london_secondary_timber_glulam_demonstrator.kg.jsonl | 13 | 146 |
| p_charles_malis_molenbeek.kg.jsonl | 19 | 138 |
| p_christ_pavilion_volkenroda.kg.jsonl | 22 | 211 |
| p_chiro_d_itterbeek_dilbeek.kg.jsonl | 28 | 357 |

## Batch-specific modeling notes
- Broethen keeps only the belegt P2 wall and floor plate groups; unknown windows/doors/roof/TGA rows from the old inventory are not emitted as entities.
- CascadeUp is modeled as remanufacturing/upcycling rather than pure 1:1 component reuse; `counts_as_direct_reuse=false` is set on glulamST/CLST component groups.
- Charles Malis separates limited Direct Reuse components from non-scoring Bestandserhalt components.
- Christ Pavilion is modeled as a translocation chain with two Bauwerk nodes: Hannover first-use/donor and Volkenroda receiver.
- Chiro separates direct reuse components from surplus/end-of-stock components with `counts_as_direct_reuse=false` and `counts_as_surplus=true`.
