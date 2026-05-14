# Actor registry actors 031–040 — Neo4j JSONL

This folder converts actors 31–40 from `akteursliste_master.md` into the repo/MCP graph format.

## Modeling decisions

- `Sterne` is ignored completely.
- The source section `Designer:innen / bauende Praxis` is modeled as `Akteurrolle`, not as a new `AkteurFokus` label.
- `ar_entwurf_bauende_praxis` is included again in `controlled_terms.delta.jsonl` as an idempotent required controlled term.
- Person-to-organisation links use `VERBUNDEN_MIT_AKTEUR`.
- Person-to-project links use `ASSOZIIERT_MIT_PROJEKT` with `needs_verification: true`.
- `BETEILIGT_AN` is intentionally not used here, because the actor registry alone should not prove exact project participation.
- External non-mail URLs become `Quelle` nodes.
- `mailto:` links are ignored.
- The master actor list is also a `Quelle` node.

## Files

```text
actors_031_040.registry.kg.jsonl
controlled_terms.delta.jsonl
schema_patch.actor_registry_v1_2.json
manifest.json
validation_report.md
```

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

## Required schema extension

```text
VERBUNDEN_MIT_AKTEUR
ASSOZIIERT_MIT_PROJEKT
```

Use `ASSOZIIERT_MIT_PROJEKT` as a weak bridge only. Later research or project-file evidence can upgrade it to `BETEILIGT_AN`.
