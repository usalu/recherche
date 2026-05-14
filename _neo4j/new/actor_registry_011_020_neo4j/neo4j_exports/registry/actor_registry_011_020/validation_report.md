# Validation report — actor registry actors 011–020

Source file: `akteursliste_master.md`

## Result

- JSONL parse: PASS
- Relationship endpoints against local registry + controlled seed + first10 actor registry: PASS
- Local node degree ≥ 2: PASS
- `Sterne` imported: NO
- Uses `Akteurrolle` instead of new `AkteurFokus`: YES
- Uses weak `ASSOZIIERT_MIT_PROJEKT` instead of confirmed `BETEILIGT_AN`: YES

## Counts

| file | nodes | relationships |
|---|---:|---:|
| controlled_terms.delta.jsonl | 1 | 0 |
| actors_011_020.registry.kg.jsonl | 69 | 263 |

## Actors included

11. Benjamin Poignon
12. Charlotte Bofinger
13. Eike Roswag-Klinge
14. Marco Graber
15. Thomas Pulver
16. Jeroen Bergsma
17. Nils Nolting
18. Søren Nielsen
19. Anders Lendager
20. Andrea Klinge

## Requires schema patch

Add relationship types:

```text
VERBUNDEN_MIT_AKTEUR
ASSOZIIERT_MIT_PROJEKT
```

Do not convert `ASSOZIIERT_MIT_PROJEKT` to `BETEILIGT_AN` until a project file or external source confirms exact participation.

## Missing endpoints

0

## Local nodes below degree 2

0
