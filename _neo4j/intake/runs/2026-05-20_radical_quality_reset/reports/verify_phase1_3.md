# Phase 1.3 Verification — Propagated MARKTMODELL Flagging

Verifier: 3 of 12  
Database: `mit-bestand` via `.cursor/mcp.json` Neo4j driver settings  
Mode: read-only graph verification

## Plan Reference

Plan section 1.3 expects:

- Flag, do not delete, propagated `HAT_MARKTMODELL` pseudo-evidence.
- Remove `HAT_DOMINANT_MARKTMODELL`.
- Remove `HAT_DOMINANT_AKZEPTANZ`.
- Preserve the original propagated excerpt under `original_source_excerpt` while clearing `source_excerpt`.

## File Checks

| Check | Result | Evidence |
| --- | --- | --- |
| `migrations/mig_1_3_flag_propagated.cypher` exists | PASS | Present |
| `logs/PHASE_1_3_DONE.flag` exists | PASS | Present |

## Live Neo4j Checks

| Check | Expected | Actual | Result |
| --- | ---: | ---: | --- |
| `MATCH ()-[r:HAT_DOMINANT_MARKTMODELL]->() RETURN count(r)` | 0 | 0 | PASS |
| `MATCH ()-[r:HAT_DOMINANT_AKZEPTANZ]->() RETURN count(r)` | 0 | 0 | PASS |
| `MATCH ()-[r:HAT_MARKTMODELL]->() WHERE r.evidence_basis='propagated' RETURN count(r)` | 315..325 | 319 | PASS |
| `MATCH ()-[r:HAT_MARKTMODELL]->() WHERE r.source_excerpt CONTAINS 'propagated' RETURN count(r)` | 0 | 0 | PASS |
| Propagated edges with `evidence_origin='derived'`, `evidence_confidence='bookkeeping'`, and preserved `original_source_excerpt` | 319 | 319 | PASS |

## Sample Review

Five sampled `HAT_MARKTMODELL` edges with `evidence_basis='propagated'` all had:

- `evidence_origin = 'derived'`
- `evidence_confidence = 'bookkeeping'`
- `original_source_excerpt = 'propagated from project HAT_DOMINANT_MARKTMODELL (project-wide sourcing)'`
- `source_excerpt = null`

Sample relationship ids:

- `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153049047955669195`
- `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153049047955669196`
- `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153049047955669197`
- `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153049047955669198`
- `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:1153049047955669199`

## JSON Return

```json
{
  "phase": "1.3",
  "checks_passed": 7,
  "checks_failed": 0,
  "overall": "PASS",
  "notes": "Migration and done flag are present. Live graph has zero dominant MARKTMODELL/AKZEPTANZ relationships, 319 propagated HAT_MARKTMODELL edges, no propagated source_excerpt values, and sampled propagated edges preserve original_source_excerpt with derived/bookkeeping provenance."
}
```
