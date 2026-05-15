# Actor registry actors 061–070 — Neo4j JSONL

This folder converts actors 61–70 from `akteursliste_master.md` into the repo/MCP graph format.

## Modeling decisions

- `Sterne` is ignored completely.
- The source section `Technik / Forschung / Nachweis` is modeled as `Akteurrolle`, not as a new `AkteurFokus` label.
- Person-to-organisation links use `VERBUNDEN_MIT_AKTEUR`.
- Person-to-project/research-program links use `ASSOZIIERT_MIT_PROJEKT` with `needs_verification: true`.
- `BETEILIGT_AN` is intentionally not used here, because the actor registry alone should not prove exact project participation.
- External non-mail URLs become `Quelle` nodes.
- `mailto:` links are ignored.
- The master actor list is also a `Quelle` node.

## Files

```text
actors_061_070.registry.kg.jsonl
controlled_terms.delta.jsonl
schema_patch.actor_registry_v1_2.json
manifest.json
validation_report.md
```

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

## Required schema extension

```text
VERBUNDEN_MIT_AKTEUR
ASSOZIIERT_MIT_PROJEKT
```

Use `ASSOZIIERT_MIT_PROJEKT` as a weak bridge only. Later research or project-file evidence can upgrade it to `BETEILIGT_AN`.
