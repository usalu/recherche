# Agent 1 — Wave-0 Snapshot Report (`mit-bestand`)

**Run ID:** `2026-05-20_radical_quality_reset`
**Agent role:** 1 of 12 — pre-migration snapshot (Phase 6 prerequisite)
**Database:** `mit-bestand` on `bolt://localhost:7687`
**Plan:** `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md`

## Status

`SNAPSHOT_DONE.flag` written. `verified: true`. Counts match `apoc.meta.stats()`
exactly, independently re-checked by PowerShell line-count on the JSONL files.

## Timing

- Snapshot started: `2026-05-20T20:42:43+00:00`
- Snapshot finished: `2026-05-20T20:42:48+00:00`
- Elapsed: **5.32 s** (paged in 1 000-row chunks; 3 node pages + 20 rel pages)

## Counts

| Metric | Value (apoc.meta.stats) | JSONL line count | Match |
|---|---:|---:|:---:|
| Nodes | **2 580** | 2 580 | OK |
| Relationships | **19 989** | 19 989 | OK |
| Distinct labels | 53 | n/a | n/a |
| Distinct rel-type buckets | 68 | n/a | n/a |
| Property keys | 689 | n/a | n/a |

These counts equal the baseline declared in the plan
(Phase 1 acceptance: "Total nodes removed ≤ 35" against a 2 580-node baseline;
Phase 6: "Take a `mit-bestand` snapshot before Phase 1"; current AGENTS.md status:
"2 580 Knoten / 19 989 Relationen").

## Files written

```
E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\
├── SNAPSHOT_DONE.flag                  (283 B)
├── snapshot\
│   ├── nodes.jsonl                     (1 012 209 B, 2 580 lines)
│   ├── relationships.jsonl             (7 483 646 B, 19 989 lines)
│   ├── stats.json                      (17 496 B — full apoc.meta.stats)
│   ├── label_counts.json               (3 064 B — 53 entries)
│   └── rel_type_counts.json            (4 232 B — 68 entries)
├── logs\
│   ├── snapshot_helper.py              (the exporter)
│   └── snapshot_progress.log           (per-page progress)
├── migrations\                         (empty — for downstream agents)
├── deleted\                            (empty — Phase 1 reversibility sink)
└── reports\
    └── agent_1_snapshot_report.md      (this file)
```

`logs\snapshot_warnings.txt` is intentionally absent — no count mismatches occurred.

## JSONL record shape

`snapshot\nodes.jsonl`:

```json
{
  "id": "<node.id property or null>",
  "neo4j_internal_id": <int>,
  "labels": ["…"],
  "properties": { "…": "…" }
}
```

`snapshot\relationships.jsonl`:

```json
{
  "internal_id": <int>,
  "type": "RELTYPE",
  "start_node_internal_id": <int>,
  "end_node_internal_id": <int>,
  "start_node_id_property": "<a.id or null>",
  "end_node_id_property": "<b.id or null>",
  "properties": { "…": "…" }
}
```

`neo4j.time` / `neo4j.spatial` values are normalised to ISO strings (Date/DateTime/Time),
`str(Duration)`, or `{srid, coordinates}` for Points so the JSONL is round-trippable.

## How the snapshot was produced

1. Created the directory tree `snapshot/`, `migrations/`, `deleted/`, `logs/`,
   `reports/` under `_neo4j\intake\runs\2026-05-20_radical_quality_reset\`.
2. Confirmed reachability of `mit-bestand` via MCP
   (`project-0-recherche-Neo4j-Official` → `read-cypher` → `apoc.meta.stats()`).
3. Wrote `logs\snapshot_helper.py`, which:
   - reads connection settings from `E:\recherche\.cursor\mcp.json` via
     `_scripts\neo4j_env.resolve_connection()` (no creds hard-coded);
   - connects with the official `neo4j` Python driver 5.28.4 (read-only session);
   - fetches `apoc.meta.stats()`, label counts, and rel-type counts into
     `stats.json` / `label_counts.json` / `rel_type_counts.json`;
   - pages `MATCH (n) … ORDER BY id(n) SKIP $skip LIMIT 1000` into
     `nodes.jsonl`;
   - pages `MATCH (a)-[r]->(b) … ORDER BY id(r) SKIP $skip LIMIT 1000` into
     `relationships.jsonl`;
   - re-counts the JSONL files on disk and writes
     `SNAPSHOT_DONE.flag` with `verified: true|false`.
4. Independently re-counted both JSONL files with PowerShell as a paranoia check
   (`Get-Content … | Measure-Object -Line`). Both matched.

## Read-only guarantee

- MCP server is configured with `NEO4J_READ_ONLY=true` in `.cursor\mcp.json`.
- The Python driver session ran only `MATCH … RETURN …` and `CALL apoc.meta.stats()`.
- No Cypher write keywords were issued; no schema/admin commands; no PROFILE.
- The graph was not modified.

## Warnings / notes

- The Neo4j server returned routine deprecation warnings for `id()` (replaced by
  `elementId()` in 5.x). These are harmless. The plan and downstream agents key
  off `id(n)` as `neo4j_internal_id`, which is what is captured here. If a
  Wave-1/2 agent needs `elementId` it can recompute from the live DB; the
  internal id remains stable for the duration of this snapshot.
- `rel_type_count: 68` in the flag comes from counting `()-[:TYPE]->()`
  entries in `apoc.meta.stats().relTypes`; this is one higher than the
  "67 relationship types" figure in the plan's expected-end-state table.
  The difference is the historical/case relType `GEHÖRT_ZU` plus all 67 ASCII
  types vs. the plan's text count; both `label_counts.json` and
  `rel_type_counts.json` enumerate the actual live distribution and should be
  the authoritative reference for downstream agents.

## Acceptance criteria — checklist

- [x] `SNAPSHOT_DONE.flag` exists at
      `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\SNAPSHOT_DONE.flag`.
- [x] `nodes.jsonl` line count (2 580) == `stats.nodeCount` (2 580).
- [x] `relationships.jsonl` line count (19 989) == `stats.relCount` (19 989).
- [x] `reports\agent_1_snapshot_report.md` exists with counts and timing (this file).

## Handoff

The snapshot can be replayed end-to-end with the JSONL files alone (every node
carries `id`, `labels`, `properties`; every rel carries `type`, both endpoint
`id` properties, and `properties`). This satisfies the plan's `## Reversibility`
requirement that Phase 1 / 2 changes be reconstructable from a pre-migration
snapshot plus the per-step `deleted\*.jsonl` files that subsequent agents will
populate.

Agent 1 stops here. Downstream agents (Wave-1+) may begin Phase 1 work.
