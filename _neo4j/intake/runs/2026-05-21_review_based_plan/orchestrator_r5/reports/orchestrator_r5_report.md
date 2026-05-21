# Orchestrator — Phase R5 Report (TEMPLATE — fill after running)

- **Agent:** orchestrator
- **Phase:** R5 (Bauteilgruppe disambiguation)
- **Database:** mit-bestand
- **Completed (UTC):** _<fill on completion>_
- **Verdict:** _<PASS | FAIL>_

> **This file is a placeholder.** The runner script
> `logs/orchestrator_r5_runner.py` overwrites it with a populated report on
> successful execution.
> If you see this header text after a run, the runner aborted before the
> report-write step. Investigate `logs/orchestrator_r5_audit.jsonl`.

## Executive summary

R5 tagged every `:Bauteilgruppe` with a `bg_kind` property classifying it as
`batch`, `partial_batch`, or `category` based on its FROM_DONOR /
INTO_RECEIVER edge topology. The disambiguation enables honest aggregation
queries (mass, count, reuse-share) and makes the Q1 canonical pattern's
"254 distinct BGs" filterable as `bg_kind='batch'`.

## Before / after counts

_Populated by runner._

| Metric | Before | After |
|---|---:|---:|
| Total `:Bauteilgruppe` | — | — |
| With `bg_kind` set | — | — |
| `FROM_DONOR` edges | — | — |
| `INTO_RECEIVER` edges | — | — |
| BG with both donor and receiver | — | — |

## bg_kind distribution

_Populated by runner._

## Acceptance gates

_Populated by runner. All gates must pass for the run to be considered complete._

| Gate | Value | Expectation |
|---|---:|---|
| `a1_bg_without_kind` | — | expect_zero |
| `a2_bg_kind_enum_violation` | — | expect_zero |
| `a3_category_with_donor_or_receiver` | — | expect_zero |
| `a4_batch_missing_topology` | — | expect_zero |
| `a5_partial_batch_misclassified` | — | expect_zero |
| `q1_canonical_batches_distinct` | — | expect_at_least_254 |

## Risks / follow-ups

- BGs tagged `partial_batch` are pending dossier follow-up (donor or
  receiver identified but not both). Recommend a future ingestion pass to
  complete the topology.
- BGs tagged `category` that carry a `menge_*` property are a data-quality
  issue. Agent 1's R8 seed pass should classify these.

## Open questions

- **D6** decided property-only (no secondary labels). If queries become
  noisy, revisit.

## Artefacts produced

```
_neo4j/intake/runs/2026-05-21_review_based_plan/orchestrator_r5/
├── PHASE_R5_DONE.flag
├── migrations/mig_r5_bg_disambiguation.cypher
├── logs/
│   ├── orchestrator_r5_runner.py
│   ├── orchestrator_r5_progress.log
│   ├── orchestrator_r5_audit.jsonl
│   ├── orchestrator_r5_probe_pre.json
│   └── orchestrator_r5_probe_post.json
└── reports/orchestrator_r5_report.md
```

## Handoff

R5 is independent and standalone. No downstream agent waits on it
specifically, but Stage 4 integration audit will consume `bg_kind` when
running honest aggregation queries.

The completion of R5 also validates the integration pipeline (snapshot →
branch → migration → flag → log) for the heavier phases that follow.
