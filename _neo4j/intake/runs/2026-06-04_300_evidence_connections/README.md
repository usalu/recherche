# 300+ evidence-backed connections candidates

**Date:** 2026-06-04  
**Target database:** `mit-bestand`  
**Run:** `evidence_connections_300_2026_06_04`

**Current status, 2026-06-05:** not imported. The accidental 2026-06-04 import was rolled back and verified with 0 remaining relationships / 0 remaining endpoint nodes for this run.

## Purpose

Prepare at least 300 new graph connections with evidence, without relying on name similarity. Import requires explicit user confirmation.

## Source

`_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_existing_graph_connections_PRIORITY_DEEPER_KEEPALL.json`

This payload contains graph-ready connection candidates with real source URLs and node metadata.

## Selection rules

The importer includes an edge only when all are true:

- relationship has a real `http(s)` evidence URL;
- evidence URL is not `internal:`;
- relationship type already exists in the live graph;
- relationship is not already present by `r.id`;
- relationship is not already present as the same `(source.id, type, target.id)` triple;
- both endpoints have stable string `id` values in the source payload;
- relationship type is **not** `HAT_METHODE` and **not** `HAT_MARKTMODELL`.
- `Akteur -> Bauteilgruppe` is allowed only when the source actor is typed as a Bauteilbörse in Neo4j:
  `(:Akteur)-[:HAT_AKTEURTYP]->(:Akteurtyp {id:'at_materialhub_bauteilboerse'})`.

`HAT_METHODE` is skipped because the payload uses older method vocabulary IDs that are not currently present in the live graph. `HAT_MARKTMODELL` is skipped to avoid violating the one-market-model-per-actor rule.

## Expected scale

The original pre-import scan found 543 eligible new evidence-backed connections before the `Akteur -> Bauteilgruppe` rule:

- `BETEILIGT_AN`: 426
- `BELEGT_IN`: 67

After the corrected rule, the confirmation list is:

- total kept: 254
- total excluded: 289
- `BETEILIGT_AN`: 137
- `BELEGT_IN`: 67
- `FROM_DONOR`: 26
- `HAT_BAUTEILGRUPPE`: 21
- `NUTZT_BAUWERK`: 3

This is below the requested 300, so more valid evidence-backed connections are still needed before import.
- `FROM_DONOR`: 26
- `HAT_BAUTEILGRUPPE`: 21
- `NUTZT_BAUWERK`: 3

## Run

```powershell
$env:CONFIRM_BAUTEILBOERSE_300_IMPORT='YES'
python _neo4j/intake/runs/2026-06-04_300_evidence_connections/_run_import_300_evidence_connections.py
```

Without `CONFIRM_BAUTEILBOERSE_300_IMPORT=YES`, the script exits before selecting or importing anything.

## Rollback

```cypher
MATCH ()-[r {review_run:'evidence_connections_300_2026_06_04'}]->()
DELETE r;
```

Endpoint nodes created by this run are marked with:

```cypher
source_scope = 'evidence_connections_300_2026_06_04'
```

They can be reviewed separately before deletion.
