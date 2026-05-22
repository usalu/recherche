# Graph metadata sidecar

Offloaded node/relationship metadata from `property_cleanup_2026_06_05` phases **4b** and **5b**.

Live Neo4j entities keep a single pointer: **`metadata_sidecar_key`**. Full payloads live here.

## Files

| File | Contents |
|------|----------|
| `entity_metadata.jsonl` | One row per affected node or relationship |
| `manifest.json` | Run metadata and row counts |
| `qa/needs_source_url_review.csv` | QA backlog (rels flagged `needs_source_url_review`) |

## Key format

| Entity | Key pattern | Example |
|--------|-------------|---------|
| Node | `node:{id}` | `node:bg_stahl_gelaender_verbiest` |
| Relationship | `rel:{reltype}:{from_id}->{to_id}` | `rel:HAT_BAUTEILTYP:bg_abc->bt_fenster` |

## Lookup

1. Read `metadata_sidecar_key` in Neo4j Browser.
2. Find the row in `entity_metadata.jsonl`:

```powershell
Select-String -Path entity_metadata.jsonl -Pattern "node:bg_stahl_gelaender_verbiest"
```

3. Inspect `archived_properties` for offloaded fields; `kept_on_graph` snapshots what remained on the entity.

## Cypher examples

```cypher
// Node with archived source titles
MATCH (n:Bauteilgruppe {id: 'bg_...'})
RETURN n.metadata_sidecar_key, n.source_urls, keys(n);

// Relationship with archived review metadata
MATCH ()-[r:HAT_BAUTEILTYP]->()
WHERE r.metadata_sidecar_key IS NOT NULL
RETURN r.metadata_sidecar_key, r.confidence, r.source_url
LIMIT 5;
```

## Drop list

Patterns for `source_titles` filtering: [`../source_title_drop_patterns.txt`](../source_title_drop_patterns.txt)
