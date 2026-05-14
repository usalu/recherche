# Validation report — actor registry actors 051–060

Source file: `akteursliste_master.md`

## Result

- JSONL parse: PASS
- Relationship endpoints against local registry + controlled seed + previous actor registry + batch KG files: PASS
- Local node degree ≥ 2: PASS
- `Sterne` imported: NO
- Uses `Akteurrolle` instead of new `AkteurFokus`: YES
- Uses weak `ASSOZIIERT_MIT_PROJEKT` instead of confirmed `BETEILIGT_AN`: YES
- Mailto links imported as `Quelle`: NO

## Counts

| file | nodes | relationships |
|---|---:|---:|
| controlled_terms.delta.jsonl | 2 | 0 |
| actors_051_060.registry.kg.jsonl | 68 | 304 |

## Actors included

51. Michael Polisano
52. Nicola Delon
53. Petra Jablonická
54. Sven Urselmann
55. Wiebke Ahues
56. Angelika Mettke
57. Corentin Fivet
58. Patrick Teuffel
59. Satu Huuhka
60. Catherine De Wolf

## Project association notes

- Existing project IDs reused where available: `p_plp_london_hq_circular_studio_fitout`, `p_circular_pavilion_paris`, `p_impact_hub_berlin_crclr_fitout`, `p_crclr_house_impact_hub_berlin`, and ReCreate pilot project chunks already exported in earlier batches.
- Registry stubs created for actor-list-only cases: `p_awm_muenster_circular_office`, `p_rebridge_structural_reuse_project`, and `p_eth_circular_construction_student_reuse_project`.
- ReCreate programme-derived links to project chunks are weak and carry `association_basis` notes; they should not be interpreted as exact individual project participation.
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
