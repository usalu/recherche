# Validation report — actor registry actors 101–110

Source file: `akteursliste_master.md`

## Actors included

101. Umberto Lusso
102. Hugo Topalov
103. Félix Dillmann
104. Anna Buser
105. Sarah Westerfeld
106. Madlen Kobi
107. Carla Ferrando Costansa
108. Pablo Garrido Arnaiz
109. Cyril Pressacco
110. Kasper Guldager Jensen

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
| actors_101_110.registry.kg.jsonl | 57 | 272 |
| controlled_terms.delta.jsonl | 3 | 0 |

## Missing endpoints

None

## Local nodes below 2 edges

None
