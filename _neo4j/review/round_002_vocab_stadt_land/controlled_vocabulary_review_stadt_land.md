# Round 002 Controlled Vocabulary Review: Stadt + Land

## Result In Context

Live graph shows true geographic duplicate candidates. These should be reviewed before apply because merge operations must preserve all relationships and source evidence.

## Duplicate Name Candidates

| label | name_key | ids | count |
| --- | --- | --- | --- |
| Land | vereinigtes königreich | land_vereinigtes_koenigreich, land_vereinigtes_konigreich | 2 |
| Stadt | brüssel | stadt_bruessel, stadt_brussel | 2 |

## Country Snapshot

| id | name | inbound |
| --- | --- | --- |
| land_belgien | Belgien | 50 |
| land_daenemark | Daenemark | 2 |
| land_deutschland | Deutschland | 84 |
| land_danemark | Dänemark | 6 |
| land_finnland | Finnland | 12 |
| land_frankreich | Frankreich | 15 |
| land_japan | Japan | 5 |
| land_luxemburg | Luxemburg | 6 |
| land_niederlande | Niederlande | 39 |
| land_norwegen | Norwegen | 5 |
| land_schweiz | Schweiz | 41 |
| land_usa | USA | 14 |
| land_uk | United Kingdom | 7 |
| land_vereinigtes_koenigreich | Vereinigtes Königreich | 25 |
| land_vereinigtes_konigreich | Vereinigtes Königreich | 5 |

## Candidate Patch

- `controlled_vocabulary_stadt_land.patch.jsonl` contains 5 candidates: 4 merge operations and 1 canonical display-name operation.
- Do not apply until merge handling is implemented and dry-run reports relationship rewiring counts.
