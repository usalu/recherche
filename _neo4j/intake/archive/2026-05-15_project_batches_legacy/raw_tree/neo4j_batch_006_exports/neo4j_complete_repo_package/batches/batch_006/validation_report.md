# Validation report — batch_006

## Schema validation
PASS — every JSONL record validates against `kg_jsonl_record_schema.json`.

## Manifest validation
PASS — manifest validates against `manifest_schema.json`.

## Endpoint validation
PASS — every relationship endpoint is present in the batch, controlled_terms.delta.jsonl, or the global controlled vocabulary seed.

## Node degree check
PASS — every node emitted inside each project file and delta file has at least 2 incident relationships within that file. External seed vocabulary nodes are referenced but not re-emitted.

## BELEGT_IN check
PASS — every BELEGT_IN relationship has `datenqualitaet` set to `Belegt`.

## File counts
| file | nodes | relationships |
|---|---:|---:|
| controlled_terms.delta.jsonl | 4 | 6 |
| p_hastings_pier_visitor_centre.kg.jsonl | 19 | 226 |
| p_haus_hos_mehrfamilienhaus_muehlhausen.kg.jsonl | 15 | 237 |
| p_holbein_gardens_london.kg.jsonl | 20 | 232 |
| p_house_of_fraser_318_oxford_street_tbc_london_reuse_chain.kg.jsonl | 26 | 360 |
| p_impact_hub_berlin_crclr_fitout.kg.jsonl | 22 | 435 |

## Batch-specific modeling notes
- Hastings Pier separates direct reuse of fixed hardwood cladding from furniture and heritage restoration/bestandserhalt.
- Haus HOS models WBS70-/Stahlbeton wall, floor and stair elements as separate score-relevant Bauteilgruppen connected to donor and receiver Bauwerk nodes.
- Holbein Gardens models only reclaimed structural steel as direct reuse; retained concrete frame and new CLT floors are context/non-direct-reuse component groups.
- House of Fraser/TBC is modeled as a reuse chain with separate donor, receiver and self-reuse paths; conflicting tonnage values are preserved as properties instead of being normalized away.
- Impact Hub Berlin is modeled as an interior fit-out comparison case; furniture, recycling and CRCLR main-building reuse are excluded or marked non-score-relevant.
- New controlled delta terms are `mat_mdf`, `mat_textil`, `norm_sci_p427`, and `norm_sci_p440`.
