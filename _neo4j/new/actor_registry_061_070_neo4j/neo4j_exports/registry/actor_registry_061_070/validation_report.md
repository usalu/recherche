# Validation report — actor registry actors 061–070

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
| controlled_terms.delta.jsonl | 1 | 0 |
| actors_061_070.registry.kg.jsonl | 49 | 238 |

## Actors included

61. Ullrich Dickgiesser
62. Nicole Dähn
63. Dirk E. Hebel
64. Felix Heisel
65. Kevin Straub
66. Werner Sobek
67. Andreas Sonderegger
68. Anja Rosen
69. Annette Hillebrandt
70. Christof Ziegert

## Project association notes

- Registry stubs created for actor-list-only cases: `p_umar_unit`, `p_lysp8`, `p_reuse_in_construction_zhaw`, and `p_reallabor_b_e_ware`.
- `p_reuse_in_construction_zhaw` is a research-program stub. It is included only because the actor registry uses the same weak `ASSOZIIERT_MIT_PROJEKT` bridge for project-like programmes.
- `ASSOZIIERT_MIT_PROJEKT` remains weak and should not be interpreted as exact participation.
- No `BETEILIGT_AN` relationships are created in this registry chunk.

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
