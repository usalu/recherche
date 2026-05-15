# Validation report — actor registry actors 031–040

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
| actors_031_040.registry.kg.jsonl | 58 | 236 |

## Actors included

31. Maximilian Stemmler
32. Nina Pawlicki
33. Roman Kreuzer
34. Sina Jansen
35. Søren Pihlmann
36. Daniel Hoffmann
37. Gian Trachsler
38. Jan Haerens
39. Stéphane Damsin
40. Katrine West Kristensen

## Project association notes

- `p_thoravej_29_copenhagen` and `p_zinneke_feder_masui4ever_brussels` should already exist from project batch exports.
- `p_stuttgart_210`, `p_reallabor_be_ware`, `p_schaerenmoosstrasse_zuerich`, `p_vandkunsten_component_reuse`, and `p_circle_house` are registry stubs unless a project-file import exists later.
- `ASSOZIIERT_MIT_PROJEKT` remains weak and should not be interpreted as exact participation.

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
