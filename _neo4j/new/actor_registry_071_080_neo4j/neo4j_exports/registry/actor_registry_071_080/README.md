# Actor registry actors 071–080 — Neo4j JSONL

This folder converts actors 71–80 from `akteursliste_master.md` into the repo/MCP graph format.

## Modeling decisions

- `Sterne` is ignored completely.
- Source sections are modeled as `Akteurrolle`, not as a new `AkteurFokus` label.
- Person-to-organisation links use `VERBUNDEN_MIT_AKTEUR`.
- Person-to-project/research-program links use `ASSOZIIERT_MIT_PROJEKT` with `needs_verification: true`.
- `BETEILIGT_AN` is intentionally not used here, because the actor registry alone should not prove exact project participation.
- External non-mail URLs become `Quelle` nodes.
- `mailto:` links are ignored.
- The master actor list is also a `Quelle` node.

## Files

```text
actors_071_080.registry.kg.jsonl
controlled_terms.delta.jsonl
schema_patch.actor_registry_v1_2.json
manifest.json
validation_report.md
```

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

## Required schema extension

```text
VERBUNDEN_MIT_AKTEUR
ASSOZIIERT_MIT_PROJEKT
```

Use `ASSOZIIERT_MIT_PROJEKT` as a weak bridge only. Later research or project-file evidence can upgrade it to `BETEILIGT_AN`.
