# Round 003 queue

Pre-loaded items for the upcoming `PROJECT_CONTENT_REVIEW` round.

## Why a queue folder

`Bauwerk` (`bw_*`) and `Projekt` (`p_*`) duplicate-candidate findings
surfaced during the round-001 audit and round-002 baseline. They are
**not** vocab (round-002 scope) and they are **not** registry
canonicalization (actor-registry track). They are project-content
review work for round 003.

See [`ROUND_002_PLAN.md`](../ROUND_002_PLAN.md) §4.2 and §4.3.

## Queue

[`bauwerk_canonicalization.queue.jsonl`](bauwerk_canonicalization.queue.jsonl)
— 3 canonicalize_node candidates routed here on 2026-05-15:

- `bw_halle_2_ringberlin`
- `bw_lysbuechel_parkhaus_basel`
- `bw_tampere_1980s_office_donor`

Plus, surfaced during round-002 baseline but not yet queued in a file,
1 Projekt pair:

- `p_reallabor_be_ware` vs `p_reallabor_b_e_ware` — duplicate concept
  (live-graph), needs human disambiguation.

## What to do with the queue

Round 003 takes projects in chunks of 5
([`03_PROJECT_CONTENT_REVIEW_PLAN.md`](../../neo4j_iterative_review_plan/plans/03_PROJECT_CONTENT_REVIEW_PLAN.md)).
For each chunk:

1. Verify project root + source links.
2. Verify donor/receiver `Bauwerk` references — at this point, fold in
   the queued `bw_*` canonicalizations and the `p_reallabor_*` pair.
3. Verify Bauteilgruppen, metrics placement, actors and roles.

Use the extended apply runner (`merge_node`, `canonicalize_node`, etc.)
from round 002.

## Acceptance

Queue items are absorbed into per-chunk project review patches; this
file becomes empty once round 003 wraps.
