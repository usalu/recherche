# Actor registry actors 011–020 — Neo4j JSONL

This folder converts actors 11–20 from `akteursliste_master.md` into the repo/MCP graph format.

## Important modeling decisions

- `Sterne` is ignored completely.
- The source section `Designer:innen / bauende Praxis` is modeled as `Akteurrolle`, not as a new `AkteurFokus` label.
- `ar_entwurf_bauende_praxis` is included again in `controlled_terms.delta.jsonl` as an idempotent required controlled term.
- Person-to-organisation links use `VERBUNDEN_MIT_AKTEUR`.
- Person-to-project links use `ASSOZIIERT_MIT_PROJEKT` with `needs_verification: true`.
- `BETEILIGT_AN` is intentionally not used here, because the actor registry alone should not prove exact project participation.
- External URLs become `Quelle` nodes.
- The master actor list is also a `Quelle` node.

## Files

```text
actors_011_020.registry.kg.jsonl
controlled_terms.delta.jsonl
schema_patch.actor_registry_v1_2.json
manifest.json
validation_report.md
```

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

## Required schema extension

```text
VERBUNDEN_MIT_AKTEUR
ASSOZIIERT_MIT_PROJEKT
```

Use `ASSOZIIERT_MIT_PROJEKT` as a weak bridge only. Later research or project-file evidence can upgrade it to `BETEILIGT_AN`.
