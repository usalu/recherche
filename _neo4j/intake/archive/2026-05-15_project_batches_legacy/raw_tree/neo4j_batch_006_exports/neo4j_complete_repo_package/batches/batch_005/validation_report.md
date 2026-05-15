# Validation report — batch_005

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
| controlled_terms.delta.jsonl | 3 | 6 |
| p_ferme_du_rail_paris.kg.jsonl | 23 | 363 |
| p_gjg_house_gentbrugge.kg.jsonl | 14 | 115 |
| p_grande_halle_de_colombelles.kg.jsonl | 23 | 390 |
| p_grubenstrasse_29_werkhof_29_zuerich.kg.jsonl | 21 | 417 |
| p_harmalanranta_a_kruunu_recreate_mini_pilot_tampere.kg.jsonl | 17 | 153 |

## Batch-specific modeling notes
- La Ferme du Rail separates built Direct Reuse from the broader 90% biosourced/reused claim; fixed cupboards are included only as fixed built-in elements and textile sun shading is marked `counts_as_direct_reuse=false` because the source is unclear.
- gjG House models the reused brick shell as the central score-relevant Bauteilgruppe; the steel/wood infill is kept as non-reuse context.
- Grande Halle de Colombelles models Lot 01 Réemploi and direct-reuse component groups while explicitly separating retained concrete structure as Bestandserhalt.
- Grubenstrasse 29 / Werkhof 29 models the Bauteiljagd/reuse supply chain and separates reuse elements from the retained existing building.
- Härmälänranta models the 25 hollow-core slabs as direct structural reuse and keeps the shelter deck zone as non-reuse context; `prog_recreate` is added in the controlled terms delta.
