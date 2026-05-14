# Tolaria / SQLite Clean Import Guide

Status: use this guide after phase 20 and phase 22.  
Do not import `_graph` directly anymore.

## Import Base

Use:

```text
_database/
```

Do not import:

```text
_graph/
_manual_review/
old legacy folders
```

Those remain provenance, staging, or manual-review material.

## Files To Import Automatically

### Ready SQLite Build

If you want the already-built SQLite file, use:

```text
_database/_system/reuse_ontology.sqlite
```

It contains:

```text
nodes: 3003
edges: 7695
edge_review: 228
```

Validation:

```text
dangling edge sources: 0
dangling edge targets: 0
```

### Nodes

```text
_database/_system/node_inventory.csv
```

This is the clean node list. Each row has:

```text
entity
id
typed_path
title
build_status
markdown_path
dateien_file_count
imported_source_count
```

Node identity rule:

```text
typed_path = entity/id
```

Never use a bare slug as a global ID.

### Edges

```text
_database/_edges/clean_confirmed_edges.csv
```

This is the clean automatic edge import file. It contains only edges where both endpoints exist in `_database`.

Important columns:

```text
source
source_entity
source_id
relation
target
target_entity
target_id
field
raw_label
confidence
resolution_rule
legacy_path
original_source
original_relation
original_target
edge_cleaning
```

Use `source_entity/source_id` and `target_entity/target_id` as the database foreign keys.

### SQLite Schema

```text
_database/_system/sqlite_schema.sql
```

This defines:

```text
nodes
edges
edge_review
```

## Files To Keep Out Of Automatic Import

### Manual Node Review

```text
_manual_review/nodes/
```

These are semantically unresolved nodes. Import only after manual decision.

### Edge Review

```text
_database/_edges/clean_edge_review_queue.csv
```

These edges are not broken; they are intentionally held back because their endpoint was excluded, marked `REVIEW_REQUIRED`, or split ambiguously.

Import into a review table only:

```text
edge_review
```

## Current Clean Import Counts

```text
nodes: 3003
automatic clean edges: 7695
normalized clean edges: 252
edge-review rows: 228
manual-review nodes: 27
```

## Relation Safety

The clean edge package rewrites obvious semantic moves:

```text
bauteiltyp/Ziegel -> material/Ziegel
  has_bauteiltyp becomes uses_material

material/Beton_Fertigteile -> bauteiltyp/Betonfertigteil
  uses_material becomes has_bauteiltyp

bauteiltyp/Dachtragwerk -> tragwerkstyp/Dachtragwerk
  has_bauteiltyp becomes has_tragwerkstyp

bauteiltyp/Moebel -> bewertungslogik_abgrenzung/Moebel_Dekoration_Nicht_Direct_Reuse
  has_bauteiltyp becomes has_bewertungslogik_abgrenzung
```

This prevents wrong-level imports and double counting.

## Recommended Import Order

1. Create SQLite tables from `_database/_system/sqlite_schema.sql`.
2. Import `_database/_system/node_inventory.csv` into `nodes`.
3. Import `_database/_edges/clean_confirmed_edges.csv` into `edges`.
4. Import `_database/_edges/clean_edge_review_queue.csv` into `edge_review`.
5. Keep `_manual_review/nodes` outside the graph until manually approved.

## Query Center

For reuse analysis, start from:

```text
reuse_einsatz
```

Then expand to:

```text
fallstudie
projekt
bauobjekt
akteur_beteiligung
akteur
bauteiltyp
material
tragwerkstyp
reuse_strategie
prozessphase
huerde
pruefung_nachweis
leistungsanforderung
norm
kennwertdefinition
quelle
```

## Approval Gate

Before import, check:

```text
_migration/20_clean_database_validation.md
_migration/22_Clean_Import_Readiness_Report.md
```

Required state:

```text
Build errors: 0
REVIEW_REQUIRED markers inside database nodes: 0
No manual-review node path duplicated inside _database
No relation-target mismatches in clean_confirmed_edges.csv
```
