# Orchestrator part — R5 (Bauteilgruppe disambiguation)

> **This is the orchestrator's own phase work.** Outside of orchestration duties, the orchestrator runs R5 as the smallest, fully-standalone phase. R5 is parallel-safe with every other phase and has no upstream blockers — by design, so it can serve as a smoke test of the integration pipeline before the heavier phases land.

---

## §1 Why R5 is here

`:Bauteilgruppe` is the most ambiguous label in the graph:

- 369 nodes total.
- 254 are clearly **batches** (carry both `FROM_DONOR` and `INTO_RECEIVER` — the proof-of-reuse-chain topology that Repair D used to define "a real reuse event").
- ~32 are **partial batches** (have one direction but not both — donor identified but no receiver placement yet, or vice versa).
- ~83 are **categories** (neither donor nor receiver edges — they're vocabulary-level roll-ups: "structural steel in this project" without a specific batch).

Aggregation queries silently mix these three populations:

```cypher
MATCH (bg:Bauteilgruppe)
RETURN sum(coalesce(bg.menge_t, 0))   // tons of reused steel — but
                                       // includes categories that aren't tons,
                                       // just descriptors
```

That `sum` is wrong by design, and there's currently no way to filter cleanly.

This phase adds one property per BG: `bg_kind ∈ {'batch','partial_batch','category'}` and writes the deterministic classifier rule.

---

## §2 Mission

### §2.1 Phase R5 — Tag every `:Bauteilgruppe` with `bg_kind`

Heuristic:

| Topology | `bg_kind` |
|---|---|
| Has at least one `FROM_DONOR` AND at least one `INTO_RECEIVER` | `batch` |
| Has exactly one of `FROM_DONOR` / `INTO_RECEIVER` but not both | `partial_batch` |
| Has neither `FROM_DONOR` nor `INTO_RECEIVER` | `category` |

Optionally add the secondary labels `:BauteilgruppeBatch` / `:BauteilgruppePartial` / `:BauteilgruppeCategory`. **Decision D6 says: property-only.** Stick with that default — secondary labels add registry noise without query benefit at 369 nodes.

---

## §3 Dependencies

- **None.** R5 is independent of every other phase.
- R5 should run in Stage 1 as a smoke test.
- The orchestrator's Stage 4 audit consumes the new property when running honest aggregation queries.

---

## §4 Conflict avoidance

You write:
- `bg_kind` property on every `:Bauteilgruppe` (369 nodes).
- `migration_origin` appended on the same nodes.

You read:
- `:FROM_DONOR` and `:INTO_RECEIVER` edge presence per BG.

You MUST NOT:
- Add or remove any `:Bauteilgruppe` nodes.
- Touch any other property on `:Bauteilgruppe` (`name`, `id`, `menge_*`, etc. left alone).
- Add secondary labels (D6 says no).

---

## §5 Migration

File written to `_neo4j/intake/runs/2026-05-21_review_based_plan/orchestrator_r5/migrations/mig_r5_bg_disambiguation.cypher` ([open](../intake/runs/2026-05-21_review_based_plan/orchestrator_r5/migrations/mig_r5_bg_disambiguation.cypher)).

Inline:

```cypher
// ==========================================================================
// mig_r5_bg_disambiguation
// Tag every :Bauteilgruppe with bg_kind ∈ {batch, partial_batch, category}
// based on FROM_DONOR / INTO_RECEIVER topology.
//
// Idempotent: re-running classifies any unlabelled BG; never overwrites
// existing bg_kind that matches the current topology.
// ==========================================================================

MATCH (bg:Bauteilgruppe)
WITH bg,
     exists{(bg)-[:FROM_DONOR]->()}    AS has_donor,
     exists{(bg)-[:INTO_RECEIVER]->()} AS has_receiver
WITH bg,
     CASE
       WHEN has_donor AND has_receiver        THEN 'batch'
       WHEN has_donor XOR has_receiver        THEN 'partial_batch'
       ELSE 'category'
     END AS new_kind
SET bg.bg_kind = new_kind,
    bg.migration_origin = coalesce(bg.migration_origin, '') +
        CASE WHEN bg.migration_origin IS NULL OR bg.migration_origin = ''
             THEN 'mig_r5_bg_disambiguation'
             ELSE ' | mig_r5_bg_disambiguation' END;

// ==========================================================================
// Audits
// ==========================================================================

MATCH (bg:Bauteilgruppe) WHERE bg.bg_kind IS NULL
RETURN 'bg_without_kind' AS check, count(bg) AS violations;

MATCH (bg:Bauteilgruppe)
WHERE bg.bg_kind IS NOT NULL AND NOT bg.bg_kind IN ['batch','partial_batch','category']
RETURN 'bg_kind_enum_violation' AS check, count(bg) AS violations;

MATCH (bg:Bauteilgruppe)
RETURN bg.bg_kind AS kind, count(bg) AS c ORDER BY c DESC;

// Sanity: bg_kind='batch' count should be ≥ 254 (Repair D's Q1 cohort)
MATCH (bg:Bauteilgruppe {bg_kind: 'batch'})
RETURN 'batch_count' AS check, count(bg) AS c, 254 AS expected_lower_bound;

// Sanity: bg_kind='category' count = BGs with no donor/receiver edge
MATCH (bg:Bauteilgruppe {bg_kind: 'category'})
WHERE exists{(bg)-[:FROM_DONOR]->()} OR exists{(bg)-[:INTO_RECEIVER]->()}
RETURN 'category_with_donor_or_receiver' AS check, count(bg) AS violations;

// Cross-check: every batch BG appears in Q1's canonical pattern
MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe {bg_kind:'batch'})-[:INTO_RECEIVER]->(receiver)
RETURN 'q1_canonical_batches' AS check, count(DISTINCT bg) AS c;
```

---

## §6 Runner script

File: `_neo4j/intake/runs/2026-05-21_review_based_plan/orchestrator_r5/logs/orchestrator_r5_runner.py` ([open](../intake/runs/2026-05-21_review_based_plan/orchestrator_r5/logs/orchestrator_r5_runner.py)).

See file for full implementation. Skeleton:

1. Read creds from `.cursor/mcp.json` via `_scripts.neo4j_env.resolve_connection()`.
2. Probe: count `:Bauteilgruppe`, count by `bg_kind` (pre).
3. Execute `mig_r5_bg_disambiguation.cypher`.
4. Probe: same counts (post).
5. Verify: all gates from §7 below.
6. Write `PHASE_R5_DONE.flag` and `reports/orchestrator_r5_report.md`.

---

## §7 Acceptance gates

| Gate | Cypher | Expected |
|---|---|---|
| Every BG has `bg_kind` | `MATCH (bg:Bauteilgruppe) WHERE bg.bg_kind IS NULL RETURN count(bg)` | 0 |
| `bg_kind` enum clean | `MATCH (bg:Bauteilgruppe) WHERE NOT bg.bg_kind IN ['batch','partial_batch','category'] RETURN count(bg)` | 0 |
| Batch count | `MATCH (bg:Bauteilgruppe {bg_kind:'batch'}) RETURN count(bg)` | 254 |
| Category count + partial_batch count + batch count = 369 | `MATCH (bg:Bauteilgruppe) RETURN sum(CASE WHEN bg.bg_kind IS NOT NULL THEN 1 ELSE 0 END)` | 369 |
| No batch BG is wrongly classified as category | `MATCH (bg:Bauteilgruppe {bg_kind:'category'}) WHERE exists{(bg)-[:FROM_DONOR]->()} OR exists{(bg)-[:INTO_RECEIVER]->()} RETURN count(bg)` | 0 |
| Q1 canonical pattern returns ≥ 254 distinct BGs | `MATCH (d)<-[:FROM_DONOR]-(bg:Bauteilgruppe {bg_kind:'batch'})-[:INTO_RECEIVER]->(r) RETURN count(DISTINCT bg)` | ≥ 254 |

---

## §8 Rollback

```cypher
MATCH (bg:Bauteilgruppe) WHERE bg.bg_kind IS NOT NULL
REMOVE bg.bg_kind;
```

Single statement. Trivial.

---

## §9 What this enables for downstream

After R5, downstream queries become honest:

```cypher
// Total reused steel by mass — batches only
MATCH (bg:Bauteilgruppe {bg_kind: 'batch'})-[:NUTZT_MATERIAL]->(:Material {id:'mat_stahl'})
RETURN sum(coalesce(bg.menge_t, 0)) AS reused_steel_tons;

// Categories are vocabulary; should never carry mass
MATCH (bg:Bauteilgruppe {bg_kind: 'category'})
WHERE bg.menge_t IS NOT NULL OR bg.menge_kg IS NOT NULL OR bg.menge_stueck IS NOT NULL
RETURN 'category_with_mass' AS issue, bg.id, properties(bg);
// Any result here is a data-quality issue (will be picked up by R8 seed)

// Partial batches — pending dossier follow-up
MATCH (bg:Bauteilgruppe {bg_kind: 'partial_batch'})
OPTIONAL MATCH (bg)-[:FROM_DONOR]->(d:Bauwerk)
OPTIONAL MATCH (bg)-[:INTO_RECEIVER]->(r:Bauwerk)
RETURN bg.id, d.id AS donor, r.id AS receiver;
```

The Q3 honest rerun (Stage 4 audit) will use `bg_kind='batch'` as the filter, eliminating the silent inclusion of category BGs.

---

## §10 Risks

| Risk | Mitigation |
|---|---|
| A BG that should be batch is missing its donor/receiver edge in the current graph (loader bug) | It will be tagged `partial_batch` or `category`. R8 seed pass will create a `:DataIssue` of kind `bg_kind_mismatch_pending_loader_fix` — track for next ingestion cycle. |
| Repair D promoted some BGs based on "BG has FROM_DONOR AND INTO_RECEIVER" but the property says category | Cannot happen: R5 reads the same edges Repair D did. The 254-BG count must hold. If it doesn't, abort and investigate. |
| Future ingestion creates a BG with only one direction | New BG will be classified as `partial_batch`. Re-running R5 is idempotent. |

---

## §11 Open decisions

- **D6** (secondary labels): NO. Stick with property-only. If user later wants secondary labels, a separate small migration adds them via `SET bg:<kind-label>`.

---

## §12 Handoff

R5 is independent. Run anytime in Stage 1.

When done:

1. Push `orch/r5-and-integrate` to remote.
2. Update [HANDOFF_LOG.md](HANDOFF_LOG.md): `| <date> | orchestrator | R5 complete (batch: X, partial_batch: Y, category: Z) | <PR> | PASS |`.
3. R5's completion is also the orchestrator's confirmation that the integration pipeline (snapshot → branch → migration → flag → log) works.

---

## §13 What's also written by the orchestrator

In addition to R5, the orchestrator owns:

| Artefact | Location |
|---|---|
| `ORCHESTRATION.md` | [REVIEW_BASED_PLAN/ORCHESTRATION.md](ORCHESTRATION.md) |
| `HANDOFF_LOG.md` (template; agents update as they progress) | [REVIEW_BASED_PLAN/HANDOFF_LOG.md](HANDOFF_LOG.md) |
| Baseline snapshot of `mit-bestand` at start of run | `_neo4j/intake/runs/2026-05-21_review_based_plan/baseline_snapshot/` |
| Stage 4 integration audit migration + report | `_neo4j/intake/runs/2026-05-21_review_based_plan/stage_4_integration/` |
| Final post-remediation audit (parallel to FINAL_PASS2_AUDIT.md) | `FINAL_REVIEW_PLAN_AUDIT.md` |

---

## §14 What this file ships

```
_neo4j/intake/runs/2026-05-21_review_based_plan/orchestrator_r5/
├── migrations/
│   └── mig_r5_bg_disambiguation.cypher          ← ready to run
├── logs/
│   └── orchestrator_r5_runner.py                ← ready to run
└── reports/
    └── orchestrator_r5_report.md                ← template (fill after run)
```

---

**End of ORCHESTRATOR_PART_R5.md.**
