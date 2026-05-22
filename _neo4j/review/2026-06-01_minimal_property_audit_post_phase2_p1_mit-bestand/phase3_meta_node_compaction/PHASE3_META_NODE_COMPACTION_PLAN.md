# Phase 3 meta-node compaction plan

**Prepared:** 2026-06-01  
**Database:** `mit-bestand`  
**Status:** not applied

Phase 1 and Phase 2 removed the safe property-only cleanup buckets. The next
large reduction is the review/meta graph, not ordinary semantic properties.

## Archive

Archive artifact:

`review_meta_nodes_archive.jsonl`

Exported labels:

- `DataIssue`
- `DossierEntityTarget`
- `DeprecatedType`

Archive contents:

| Record type | Count | Property occurrences |
|---|---:|---:|
| Nodes | 31,333 | 347,984 |
| Incident relationships | 55,640 | 255,373 |

Relationship types in archive:

| Type | Count |
|---|---:|
| `CONCERNS` | 48,321 |
| `CITED_FROM_DOSSIER` | 6,104 |
| `HAS_DATA_ISSUE` | 910 |
| `EXACT_MATCH_CANDIDATE` | 305 |

## Option A — compact `DataIssue` only

Delete:

- 28,729 `DataIssue` nodes.
- all incident `CONCERNS` / `HAS_DATA_ISSUE` relationships.

Expected reduction:

- 321,345 node-property occurrences.
- at least 49,231 incident relationships.
- relationship-property reduction depends on incident rel props at apply time.

This is the biggest obvious graph simplification. It keeps `DossierEntityTarget`
and `DeprecatedType` for separate review.

## Option B — compact all archived review/meta labels

Delete:

- `DataIssue`
- `DossierEntityTarget`
- `DeprecatedType`

Expected reduction:

- 31,333 nodes.
- 55,640 incident relationships.
- 603,357 total archived property occurrences.

This is much more aggressive because `DossierEntityTarget` may still be useful
for dossier/source expansion review.

## Option C — keep nodes, strip properties

Keep review/meta topology but reduce node bags. This avoids node deletion but
leaves a very large review graph in the semantic database. It is less clean
than A or B and less useful for the stated extreme-minimum goal.

## Recommendation

Choose **Option A first** if the intent is to make the live graph semantic
rather than a mixed semantic/audit ledger.

Required before apply:

1. Confirm `DataIssue` is no longer needed as live graph state.
2. Backup `mit-bestand`.
3. Apply a dedicated delete Cypher.
4. Rerun `_scripts/_gap_survey.py`.
5. Rerun `_scripts/audit_neo4j_minimal_properties.py`.

Do not mix Phase 3 with provenance cleanup. Provenance fields need their own
normalization plan.
