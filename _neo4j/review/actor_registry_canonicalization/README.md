# Actor registry canonicalization track

This folder holds canonicalization candidates for the project-content
`a_*` actor-organization nodes. It is **not** part of the round-002 vocab
review — the vocab `Akteurrolle` / `Akteurtyp` family is handled in
[`../round_002_vocab_akteur_vocab/`](../round_002_vocab_akteur_vocab/).

## Why a separate track

`a_*` nodes are **content** (specific organizations and people), not
controlled vocabulary. Their canonicalization is informed by the
merged-actor-registry conflict log
[`../../processed/actor_registry/conflicts/node_conflicts.jsonl`](../../processed/actor_registry/conflicts/node_conflicts.jsonl)
and the actor-content live-graph state, not by the seed vocab.

See [`ROUND_002_PLAN.md`](../ROUND_002_PLAN.md) §4.2 and §4.3.

## Queue

[`round_001_needs_review.queue.jsonl`](round_001_needs_review.queue.jsonl) —
11 canonicalize_node candidates routed here from
[`../round_001_apply_test/needs_review.patch.jsonl`](../round_001_apply_test/needs_review.patch.jsonl)
on 2026-05-15. Each record is annotated with `routed_from`, `routed_at`,
`routed_by`.

## What to do with the queue

1. For each candidate, check the live graph: is the node still present?
   Is its current `name` / `aliases` already consistent with the proposed
   canonical form?
2. Cross-reference [`../../processed/actor_registry/conflicts/node_conflicts.jsonl`](../../processed/actor_registry/conflicts/node_conflicts.jsonl)
   to see whether the same node already has a recorded conflict; merge
   the canonicalize hint into the merge_report rationale.
3. Emit a patch JSONL with `canonicalize_node` (and optional `merge_node`
   for real id-form duplicates) using the extended apply runner.
4. Drop the queue entries that are stale (node has already been
   canonicalized) and keep the report of what was applied.

## Acceptance

This track is complete when the queue file is empty (or moved to an
archive subfolder) and the apply report for the actor-registry
canonicalization patch has landed.
