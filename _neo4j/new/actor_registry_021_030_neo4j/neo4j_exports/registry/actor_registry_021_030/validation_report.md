# Validation report — actor registry actors 021–030

Source file: `akteursliste_master.md`

## Result

- JSONL parse: PASS
- Relationship endpoints against local registry + controlled seed + previous actor registry + batch KG filenames: PASS
- Local node degree ≥ 2: PASS
- `Sterne` imported: NO
- Uses `Akteurrolle` instead of new `AkteurFokus`: YES
- Uses weak `ASSOZIIERT_MIT_PROJEKT` instead of confirmed `BETEILIGT_AN`: YES
- Mailto links imported as `Quelle`: NO

## Counts

| file | nodes | relationships |
|---|---:|---:|
| controlled_terms.delta.jsonl | 1 | 0 |
| actors_021_030.registry.kg.jsonl | 64 | 274 |

## Actors included

21. Stephan Bischof
22. Norbert Föhn
23. Fabian Sauser
24. Clara Simay
25. Duncan Baker-Brown
26. Frédéric Denise
27. Katharina Raabe
28. Marc Loeliger
29. Martin Zeller
30. Matthew Crabbe

## Requires schema patch

Add/keep relationship types:

```text
VERBUNDEN_MIT_AKTEUR
ASSOZIIERT_MIT_PROJEKT
```

Do not convert `ASSOZIIERT_MIT_PROJEKT` to `BETEILIGT_AN` until a project file or external source confirms exact participation.

## Missing endpoints

0

## Local nodes below degree 2

0
