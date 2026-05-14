# Validation report — batch_008

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
| controlled_terms.delta.jsonl | 5 | 6 |
| p_kamikatsu_zero_waste_center_hotel_why.kg.jsonl | 18 | 215 |
| p_kindergarten_moeoeslistrasse_manegg_zuerich.kg.jsonl | 24 | 286 |
| p_liander_alliander_hq_duiven.kg.jsonl | 15 | 150 |
| p_lo_reninge_town_hall_facade.kg.jsonl | 13 | 108 |
| p_lokomotion_technology_centre_mini_pilot_tampere.kg.jsonl | 17 | 136 |

## Notes
- Kamikatsu: loose furniture/decorative reuse excluded; fixed windows, openings, floor/wall materials modeled.
- Kindergarten Mööslistrasse: municipal pilot modeled with Bauteilkatalog/bauteilpass as controlled delta tool; Werkhof Bestand separated from direct reuse.
- Liander/Alliander HQ: broad circular transformation kept as comparison case; vague direct reuse data kept cautious.
- Lo-Reninge: only reused brick facade counted as direct reuse; convent restoration separated as Bestandserhalt.
- Lokomotion: 27 reused hollow-core slabs modeled as structural direct reuse in a small mini-pilot; EN 1168 and CROW-CUR guideline added as delta terms.
