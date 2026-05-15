# Validation report — batch_009

| Check | Result |
|---|---|
| JSONL schema | PASS |
| Manifest schema | PASS |
| Relationship endpoints against batch + seed + delta | PASS |
| Local node degree ≥ 2 | PASS |
| BELEGT_IN.datenqualitaet = Belegt | PASS |
| No Fallbeispiel nodes | PASS |
| No Kennwert nodes | PASS |

## File counts

| file | nodes | relationships |
|---|---:|---:|
| controlled_terms.delta.jsonl | 0 | 0 |
| p_lycee_michel_lucius_conversion_luxembourg.kg.jsonl | 18 | 186 |
| p_maison_des_canaux_paris.kg.jsonl | 12 | 126 |
| p_maison_dna_asse.kg.jsonl | 10 | 71 |
| p_maison_vignette_auderghem.kg.jsonl | 18 | 161 |
| p_mehrow_pilot_house.kg.jsonl | 11 | 97 |

## Notes
- Lycée Michel Lucius: campus-internal reuse modeled separately from Block 6000 Bestandserhalt and RC concrete recycling.
- Maison des Canaux: kept cautious because exact component quantities and suppliers are weakly documented; only fixed elements modeled.
- Maison DnA: reused brick outer structure modeled as direct reuse; inner timber box kept as non-direct-reuse context.
- Maison Vignette: fixed reused facade bricks, tiles, bluestone slabs and sanitary objects modeled; new bio-based structure excluded from direct reuse.
- Mehrow Pilot House: WBS70 wall and slab components modeled as structural direct reuse; PRECS/taz cost and quantity metrics stored as scalar properties.