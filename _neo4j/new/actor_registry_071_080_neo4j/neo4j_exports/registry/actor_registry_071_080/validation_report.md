# Validation report — actor registry actors 071–080

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
| actors_071_080.registry.kg.jsonl | 56 | 271 |

## Actors included

71. Fabio Gramazio
72. Matthias Kohler
73. Eva Stricker
74. Georg Hubmann
75. Guido Brandi
76. Thomas Stark
77. Uwe Seiler
78. Vanessa Propach
79. Vera van Maaren
80. Maarten Gielen

## Project association notes

- `ASSOZIIERT_MIT_PROJEKT` remains weak and should not be interpreted as exact participation.
- `Maarten Gielen` is linked weakly to Zinneke, Reuse in Multi, and Architecture of Reuse Brussels through actor-registry links.
- Research/programme stubs are included for ETH Circular Construction, Reuse in Construction / ZHAW, Stuttgart 210, Reallabor B(e) Ware, and UMAR where source links point to project-like items.
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
