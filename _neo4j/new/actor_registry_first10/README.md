# Actor registry first 10 — Neo4j JSONL

This folder converts the first 10 actors from `akteursliste_master.md` into the repo/MCP graph format.

## Important modeling decisions

- `Sterne` is ignored completely.
- The section heading `Designer:innen / bauende Praxis` is modeled as the existing label `Akteurrolle`, not as a new label.
- New controlled term proposed: `ar_entwurf_bauende_praxis`.
- Person-to-organisation links use `VERBUNDEN_MIT_AKTEUR`.
- Person-to-project links use `ASSOZIIERT_MIT_PROJEKT` with `needs_verification: true`.
- `BETEILIGT_AN` is intentionally not used here, because the actor registry alone should not prove exact project participation.
- External URLs become `Quelle` nodes.
- The master actor list is also a `Quelle` node.

## Files

```text
actors_first10.registry.kg.jsonl
controlled_terms.delta.jsonl
schema_patch.actor_registry_v1_2.json
manifest.json
validation_report.md
```

## First 10 actors included

1. Andreas Kretzer
2. Barbara Buser
3. Christian Schöningh
4. Césare Peeren
5. Jan Jongert
6. Kerstin Müller
7. Marc Angst
8. Michel Massmünster
9. Pascal Hentschel
10. Stefan Krötsch

## Required schema extension

```text
VERBUNDEN_MIT_AKTEUR
ASSOZIIERT_MIT_PROJEKT
```

Use `ASSOZIIERT_MIT_PROJEKT` as a weak bridge only. Later research or project-file evidence can upgrade it to `BETEILIGT_AN`.
