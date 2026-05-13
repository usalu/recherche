# Validation report — batch_010
## Result
PASS
## Checks
- JSONL schema: PASS- Manifest schema: PASS- Relationship endpoints: PASS- Local node degree >= 2: PASS- BELEGT_IN.datenqualitaet = Belegt: PASS- No Fallbeispiel nodes: PASS- No Kennwert nodes: PASS
## Counts
| file | nodes | relationships |
|---|---:|---:|
| p_melkinlaituri_primary_school_daycare_centre_helsinki.kg.jsonl | 13 | 96 |
| p_montessori_maassluis.kg.jsonl | 14 | 82 |
| p_multi_brussels_reuse_in_multi.kg.jsonl | 17 | 134 |
| p_musee_de_folklore_mouscron.kg.jsonl | 15 | 91 |
| p_peoples_pavilion_eindhoven.kg.jsonl | 18 | 163 |
| controlled_terms.delta.jsonl | 0 | 0 |

## Notes
- All emitted local nodes have at least two incident relationships inside their chunk.
- Montessori Maassluis is intentionally modeled as planned/watchlist, not as verified as-built Direct Reuse.
- Multi Brussels separates Direct Reuse component groups from the broader Bestandserhalt of the concrete structure.
