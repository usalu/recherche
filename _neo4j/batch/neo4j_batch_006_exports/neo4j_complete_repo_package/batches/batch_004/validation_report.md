# Validation report — batch_004

## Schema validation
PASS — every JSONL record validates against `kg_jsonl_record_schema.json`.

## Endpoint validation
PASS — every relationship endpoint is present in the batch, controlled_terms.delta.jsonl, or the global controlled vocabulary seed.

## Node degree check
PASS — every node emitted inside each project file and delta file has at least 2 incident relationships within that file. External seed vocabulary nodes are referenced but not re-emitted.

## BELEGT_IN check
PASS — every BELEGT_IN relationship has `datenqualitaet` set to `Belegt`.

## File counts
| file | nodes | relationships |
|---|---:|---:|
| controlled_terms.delta.jsonl | 1 | 3 |
| p_circular_centre_netherlands_prinsenhof_a_reuse_pilot.kg.jsonl | 17 | 199 |
| p_circular_pavilion_paris.kg.jsonl | 19 | 231 |
| p_crclr_house_impact_hub_berlin.kg.jsonl | 21 | 306 |
| p_elys_kultur_gewerbehaus_basel.kg.jsonl | 24 | 342 |
| p_europa_building_brussels.kg.jsonl | 16 | 146 |

## Batch-specific modeling notes
- Circular Centre Netherlands is kept as planned/watchlist: demolition, storage, and preparation are modeled, but the main component groups have `planned_reuse=true` and `counts_as_direct_reuse=false` until as-built reuse is documented.
- Circular Pavilion excludes loose furniture from score-relevant Bauteilgruppen; fixed doors, insulation, panels, decking, lights, and timber structure are represented.
- CRCLR House separates direct reuse of Dachstahl/Fenster/Sanitaer/Fassadenteile from Bestandserhalt of the hall and mixed reuse/recycling/upcycling in the interior.
- ELYS separates the 91 t CO₂ reuse value from the 7,000 t CO₂e Bestandserhalt value, and models the Reuse-Fassade as a Bauteilsystem plus sub-groups.
- Europa Building models 3,750 restored wooden window frames as the score-relevant direct reuse element; Residence Palace integration is marked as Bestandserhalt.
