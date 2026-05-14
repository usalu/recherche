# Validation report — actor registry actors 041–050

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
| actors_041_050.registry.kg.jsonl | 58 | 242 |

## Actors included

41. Hans Hammink
42. Hester van Dijk
43. Julia Turpin
44. Kim Le Roux
45. Margit Sichrovsky
46. Peter van Assche
47. Reinder Bakker
48. Christine Conix
49. Julien Choppin
50. Lewis Jones

## Project association notes

- Existing project IDs reused where available: `p_peoples_pavilion_eindhoven`, `p_ferme_du_rail_paris`, `p_impact_hub_berlin_crclr_fitout`, `p_crclr_house_impact_hub_berlin`, `p_multi_brussels_reuse_in_multi`, and `p_circular_pavilion_paris`.
- Registry stubs created for actor-list-only cases: `p_pavilion_circl_amsterdam`, `p_architecture_of_reuse_brussels`, and `p_granby_workshop`.
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
