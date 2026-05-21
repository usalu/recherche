# Stage 4 — integration audit plan

> **Owned by the orchestrator.** Runs after every agent's done-flags are present. Produces `_neo4j/FINAL_REVIEW_PLAN_AUDIT.md` (the honest counterpart to [FINAL_PASS2_AUDIT.md](../intake/runs/2026-05-20_radical_quality_reset/FINAL_PASS2_AUDIT.md)) and `STAGE_4_AUDIT_DONE.flag`.

---

## §1 Prerequisites

Stage 4 runner refuses to start unless **all** the following flags exist:

| Flag | Owner | Status (as of 2026-05-21) |
|---|---|---|
| `agent_1/PHASE_R1_DONE.flag` | Agent 1 | ✅ Present |
| `agent_2/PHASE_R2_DONE.flag` | Agent 2 | ✅ Present |
| `agent_2/PHASE_R10_DONE.flag` | Agent 2 | ✅ Present |
| `agent_3/PHASE_R3_DONE.flag` | Agent 3 | 🔲 **Unblocked**; run `agent_3_runner.py r3` against integrated branch |
| `agent_3/PHASE_R9_DONE.flag` | Agent 3 | 🔲 Pending R3 |
| `agent_4/PHASE_R4_DONE.flag` | Agent 4 | ✅ Present |
| `agent_5/PHASE_R7_DONE.flag` | Agent 5 (composite) | ✅ **Orchestrator-issued** (resolves naming mismatch + R7.c deferral) |
| `orchestrator_r5/PHASE_R5_DONE.flag` | Orchestrator | ✅ Present |
| `agent_1/PHASE_R8_DONE.flag` | Agent 1 | 🔲 Pending — runs LAST |

**Three flags pending: R3, R9, R8.** Stage 4 cannot run until all three exist.

---

## §2 Run order to unblock Stage 4

```
1. Agent 3 reruns logs/agent_3_runner.py r3   ← unblocked by orchestrator's PHASE_R7_DONE.flag
   ↓
2. Agent 3 reruns logs/agent_3_runner.py r9   ← after R3 verified
   ↓
3. Agent 1 reruns logs/agent_1_runner.py r8   ← reads post-R3+R9 state for DataIssue seed
   ↓
4. Orchestrator runs stage_4_integration/logs/stage_4_audit_runner.py
```

Each step writes its own done flag; the next step's runner refuses to start until the previous flag exists.

---

## §3 Stage 4 audit artefacts

```
_neo4j/intake/runs/2026-05-21_review_based_plan/stage_4_integration/
├── migrations/
│   └── stage_4_audit_queries.cypher    (Sections A–E; read-only)
├── logs/
│   ├── stage_4_audit_runner.py         (executor; reads creds, runs queries,
│   │                                    renders report)
│   └── stage_4_audit_results.json      (written on run; full per-statement results)
└── reports/
    └── (none — the audit writes one file to _neo4j/FINAL_REVIEW_PLAN_AUDIT.md)

_neo4j/
└── FINAL_REVIEW_PLAN_AUDIT.md           (the report; supersedes FINAL_PASS2_AUDIT.md)
```

---

## §4 What the audit covers

### §4.1 Headline counts comparison

3-column table: pre-radical-reset (2,580 / 19,989) → post-radical-reset (3,802 / 25,023) → post-review-plan (now).

### §4.2 Honest Q1–Q7

| Query | Honest interpretation |
|---|---|
| Q1 | `evidence_origin='source_curated'` filter only. Expect close to 0 — that's the goal. |
| Q2 | `evidence_basis='documented'` only. Expect 0 (no curated pollutant assertions). |
| Q3 | Graph-native `(:Projekt)-[:HAT_KENNWERT]->(:Kennwert {category:'reuse_share'})`. Expect ≥ 3 projects (Holbein, Jeugdkliniek, Ferme du Rail). |
| Q4 | `BETEILIGT_AN` only (no `STUB_PROJECT_LINK`). Likely still 1 (RotorDC). |
| Q5 | `(:ReuseRule)-[:RELEVANT_FOR]->(:Projekt)` graph step. Ferme du Rail = 0 (FR uncovered); Holbein = ≥ 1 (UK Stahl). |
| Q6 | New 5-bucket `evidence_origin` distribution + bookkeeping segregation. |
| Q7 | `case_markdown.text_content` populated count. |

### §4.3 Cross-agent invariants (must be 0)

- C1: every `evidence_origin` in new enum
- C2: no edge has old `curated` value
- C3: no edge has `bookkeeping` in confidence enum
- C4: every `source_curated` has a non-null excerpt
- C5: every `:Bauteilgruppe` has `bg_kind`
- C6: no `:Bauteilgruppe {bg_kind:'category'}` has FROM_DONOR/INTO_RECEIVER
- C7: every project with BG paths has `:HAS_BAUWERK`
- C8: no `:ASSOZIIERT_MIT_PROJEKT` remaining
- C9: no orphan `:Kennwert`
- C10: every `case_markdown :Quelle` has `text_content`

### §4.4 Decision-grade cohort recomputation

The headline success metric: tier-1 cohort under the honest source_curated-only gate. Expect it to drop from 11 to 3–5 projects. That drop is the goal.

### §4.5 `:DataIssue` summary

Count by kind, severity, top-10 projects by issue density.

---

## §5 What the audit does NOT do

- Does not mutate the live graph.
- Does not retag `:Projekt.quality_tier` (the new tier-1 cohort recommendation goes into the report; the actual tier recompute is a follow-up migration).
- Does not delete the `*_facts` JSON-string mirror properties (D2 follow-up).
- Does not resolve the 6 still-missing R7.b orphan dossiers (R7.b.v2 follow-up).

---

## §6 Audit completion criteria

The runner writes `STAGE_4_AUDIT_DONE.flag` only if:

1. Every prerequisite flag was present at start.
2. Every Cypher statement in `stage_4_audit_queries.cypher` executed without error.
3. The report file `_neo4j/FINAL_REVIEW_PLAN_AUDIT.md` was written.

The audit's **verdict line** in the report (PASS / FAIL / PARTIAL) is set by Kinan after manual review. The runner does not gate on it.

---

## §7 Post-Stage-4 follow-ups (not in this round)

After Stage 4 produces the honest baseline:

1. **Tier-1 recompute migration** — set `:Projekt.quality_tier='tier_1_decision_grade'` on the projects that pass the honest gate, downgrade the rest.
2. **R6 (schema language unification)** — decision D7.
3. **R7.b.v2** — close the 6 still-missing orphan dossiers.
4. **R7.c.v2** — Section-8 re-extraction for the projects flagged by R8's `dossier_section8_missing`.
5. **D2 cleanup** — strip the `*_facts` JSON-string mirrors after one ingestion cycle confirms the `:Kennwert` model.

These are tracked in `:DataIssue` and `:DeprecatedType` nodes; future agents can `MATCH (i:DataIssue {status:'open'})` to find their backlog.

---

**End of STAGE_4_PLAN.md.**
