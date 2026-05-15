# Actor registry actors 051–060 — Neo4j JSONL

This folder converts actors 51–60 from `akteursliste_master.md` into the repo/MCP graph format.

## Modeling decisions

- `Sterne` is ignored completely.
- The source sections `Designer:innen / bauende Praxis` and `Technik / Forschung / Nachweis` are modeled as `Akteurrolle`, not as a new `AkteurFokus` label.
- Person-to-organisation links use `VERBUNDEN_MIT_AKTEUR`.
- Person-to-project links use `ASSOZIIERT_MIT_PROJEKT` with `needs_verification: true`.
- `BETEILIGT_AN` is intentionally not used here, because the actor registry alone should not prove exact project participation.
- External non-mail URLs become `Quelle` nodes.
- `mailto:` links are ignored.
- The master actor list is also a `Quelle` node.
- ReCreate-related project associations are intentionally weak programme-derived links and must be verified before becoming project participation.

## Files

```text
actors_051_060.registry.kg.jsonl
controlled_terms.delta.jsonl
schema_patch.actor_registry_v1_2.json
manifest.json
validation_report.md
```

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

## Required schema extension

```text
VERBUNDEN_MIT_AKTEUR
ASSOZIIERT_MIT_PROJEKT
```

Use `ASSOZIIERT_MIT_PROJEKT` as a weak bridge only. Later research or project-file evidence can upgrade it to `BETEILIGT_AN`.
