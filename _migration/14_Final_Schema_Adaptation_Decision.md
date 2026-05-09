# Final Schema Adaptation Decision

## Decision

Adapt the final target to your ontology.

Do not redo the extraction. The existing `_graph` staging data is useful. The change is in the final schema and final move rules.

## Relevant Changes

### 1. Promote Important Empty Folders Into Final Schema

These were previously excluded because they had zero or almost zero nodes. That was too conservative.

They should be part of the final database schema:

```text
bauobjekt_beteiligung/
bauobjektrolle/
bauobjektstatus/
nutzung/
bauteilebene/
bauteilzustand/
funktionswechsel/
datenqualitaet/
programm_kontext/
```

Reason:

They are important ontology categories. Even if they start empty, they define where future facts will go.

### 2. Keep Current Extracted Nodes

Keep:

```text
fallstudie/
projekt/
bauobjekt/
reuse_einsatz/
reuse_kette/
reuse_kettenstation/
datenpunkt/
akteur/
akteur_beteiligung/
software_digitaltool/
quelle/
```

Reason:

These are already populated and match the target structure.

### 3. Keep Useful Extra Folders

These are not in your table, but they are useful and should stay:

```text
akteurrolle/
tooltyp/
foerderprogramm/
methode/
```

Reason:

- `akteurrolle` normalizes actor roles in projects.
- `tooltyp` classifies Restado, RotorDC, Madaster, etc.
- `foerderprogramm` stores concrete programs like BBSM/PREUSE.
- `methode` stores method knowledge such as Form Follows Availability.

### 4. Keep Out

These should not be in the first final database:

```text
meta/
akteurleistung/
akteurtyp/
beleg/
gebaeudetypologie/
plattformfunktion/
plattformzugang/
```

Reason:

They are redundant, meta-only, too immature, or covered by better folders.

## How The Final Move Should Change

When creating `_database`:

1. Copy/rewrite the approved populated nodes from `_graph`.
2. Create all final schema folders, including empty ontology folders.
3. Archive all 567 old mapped files once under `quelle`.
4. Do not copy `meta` into the final database.
5. Do not copy unresolved review rows as facts.
6. Use `_system/schema.md` to document empty folders until real nodes exist.

## Final Schema Delta

Before adaptation:

```text
empty ontology folders were excluded
```

After adaptation:

```text
empty ontology folders are included as schema folders
but they do not create fake data nodes
```

This is the cleanest path: stable ontology first, real data only where supported.
