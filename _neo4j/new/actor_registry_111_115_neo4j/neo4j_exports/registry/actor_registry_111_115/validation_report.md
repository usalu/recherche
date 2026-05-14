# Validation report — actor registry actors 111–115

Source file: `akteursliste_master.md`

## Actors included

111. Thibaut Barrault
112. Thomas Rau
113. Julia Krafft
114. Lucas Klinkenbusch
115. Pascal Flammer

## Result

- JSONL parse: PASS
- Relationship endpoints against local registry + controlled seed + previous actor registry + batch KG files: PASS
- Local node degree ≥ 2: PASS
- `BELEGT_IN.datenqualitaet = Belegt`: PASS
- `Sterne` imported: NO
- Uses `Akteurrolle` instead of new `AkteurFokus`: YES
- Uses weak `ASSOZIIERT_MIT_PROJEKT` instead of confirmed `BETEILIGT_AN`: YES
- Mailto links imported as `Quelle`: NO

## Counts

| File | Nodes | Relationships |
|---|---:|---:|
| actors_111_115.registry.kg.jsonl | 25 | 119 |
| controlled_terms.delta.jsonl | 2 | 0 |

## Missing endpoints

None

## Local nodes below 2 edges

None
