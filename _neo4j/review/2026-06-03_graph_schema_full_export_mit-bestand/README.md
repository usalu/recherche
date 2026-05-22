# Neo4j graph schema and full graph export

Export date: 2026-06-03  
Database: `mit-bestand`  
Source of truth: live Neo4j via `_scripts/backup_neo4j_graph.py`

## Contents

| File | Purpose |
|---|---|
| `schema_snapshot.json` | Live labels, relationship type tokens, constraints, indexes, node counts by label, relationship counts by type. |
| `live_graph.backup.jsonl` | Complete logical graph export: all nodes followed by all relationships, including labels, properties, element ids, and stable backup keys. |
| `nodes.jsonl` | Derived split file containing only node records from `live_graph.backup.jsonl`. |
| `edges.jsonl` | Derived split file containing only relationship records from `live_graph.backup.jsonl`. |
| `node_types.json` | Derived label counts, label-set counts, and observed node properties by label. |
| `edge_types.json` | Derived relationship type counts and observed relationship properties by type. |
| `backup_manifest.json` | Manifest and checksums for the core backup files. |
| `split_export_manifest.json` | Manifest and checksums for the derived split files. |
| `counts.json` | Total node and relationship count. |

## Live counts

| Metric | Count |
|---|---:|
| Nodes | 5476 |
| Relationships | 24017 |
| Label tokens from Neo4j schema | 65 |
| Relationship type tokens from Neo4j schema | 82 |
| Labels observed on exported nodes | 63 |
| Relationship types observed on exported edges | 77 |

The schema token counts are intentionally kept separate from the observed
record counts. At export time, Neo4j reported these tokens without matching
current records in the full graph export:

| Token kind | Tokens without records |
|---|---|
| Labels | `GraphVersion`, `ZertifizierungBewertungssystem` |
| Relationship types | `AUS_BAUWERK`, `EINGEBAUT_IN`, `HAT_SCHADSTOFF`, `NUTZT_TOOL`, `ZITIERT_QUELLE` |

## Pre-export gap survey

`python _scripts/_gap_survey.py` was run before the export. It reported the
same live totals above and flagged these expected-zero checks as non-zero:

| Check | Count |
|---|---:|
| `r.id NULL` | 127 |
| `Case-specific nodes missing BELEGT_IN` | 4 |
| `BG missing HAT_MATERIALGRUPPE` | 1 |
| `BG missing HAT_WIEDERVERWENDUNGSART` | 2 |

No graph changes were made during this export.
