# Orchestration — Review-based remediation, 2026-05-21

**Read first if you are an agent that landed here cold.** This document is the conductor's score for a 5-agent remediation of `mit-bestand`. You belong to exactly one of agents 1–5 (or you are the orchestrator). Find your row below and read your brief next.

---

## §1 Agent assignment

| Agent | Brief | Phases | Effort | Branch prefix |
|---|---|---|:---:|---|
| **Orchestrator (Claude)** | This doc + [ORCHESTRATOR_PART_R5.md](ORCHESTRATOR_PART_R5.md) | R5 (Bauteilgruppe disambiguation) + integration audit | S | `orch/r5-and-integrate` |
| **Agent 1** | [AGENT_1_evidence_honesty.md](AGENT_1_evidence_honesty.md) | R1 (evidence_origin split + bookkeeping flag) + R8 (`:DataIssue` audit relationship) | L | `agent1/r1-r8-evidence` |
| **Agent 2** | [AGENT_2_schema_restoration.md](AGENT_2_schema_restoration.md) | R2 (restore 5 demoted labels) + R10 (deprecated-type audit nodes) | L | `agent2/r2-r10-restore` |
| **Agent 3** | [AGENT_3_structural_completion.md](AGENT_3_structural_completion.md) | R3 (`:HAS_BAUWERK`, `:RELEVANT_FOR`) + R9 (actor-stub edge rename) | M | `agent3/r3-r9-structure` |
| **Agent 4** | [AGENT_4_data_model.md](AGENT_4_data_model.md) | R4 (lift `*_facts` JSON to `:Kennwert` nodes) | L | `agent4/r4-kennwert` |
| **Agent 5** | [AGENT_5_loader_hardening.md](AGENT_5_loader_hardening.md) | R7 (dossier loader hardening + 7 orphans + dual-naming merge) | L | `agent5/r7-loader` |

R6 (full schema language unification) is **deferred** by decision; not assigned in this round.

---

## §2 Why these 5 + 1

The review found three groups of problems:

1. **Trust dishonesty.** The `evidence_origin='curated'` flag was satisfied by string concatenation rather than curation, and the audit gate was the driver of data rewrites (`Repair D`). Fixing this is foundational. → Agent 1.
2. **Topology losses.** Five labels (`Layer`, `LebenszyklusModul`, `RechtlicheBedingung`, `ZertifizierungBewertungssystem`, `Tool`) were collapsed into stringly-typed lists; key structural edges (`:Projekt→:Bauwerk`, `:ReuseRule→:Projekt`) were never built; quantitative facts hide in JSON strings; `:Bauteilgruppe` is overloaded. → Agents 2, 3, 4, Orchestrator.
3. **Ingestion incoherence.** 16 dossier dual-name pairs, 7 orphan dossiers, retired-type drift in dossier text. → Agent 5.

The split groups phases that touch the same data slice (minimising lock conflicts) and balances effort. R5 went to the orchestrator because it is small, independent, and a useful test of the integration pipeline before the heavier phases land.

---

## §3 Dependency graph

```
                ┌───────────────────────────────────────────────┐
                │ Stage 0 — shared baseline (orchestrator)      │
                │   • Snapshot of mit-bestand                   │
                │   • Branch from wip/kinan2 at agreed commit   │
                │   • Each agent forks own feature branch       │
                └───────────────────────────────────────────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        │                            │                            │
   Stage 1 (parallel-safe — additive only)
        │                            │                            │
   ┌────▼─────┐                ┌─────▼─────┐               ┌──────▼────┐
   │ Agent 1  │                │ Agent 5   │               │ Orch (R5) │
   │ R1 only  │                │ R7.a / b  │               │ bg_kind   │
   └────┬─────┘                │ (resolve  │               │ tagging   │
        │                      │  orphans, │               └─────┬─────┘
        │                      │  merge    │                     │
        │                      │  dual)    │                     │
        │                      └─────┬─────┘                     │
        │                            │                            │
        └────────────────┬───────────┘                            │
                         │                                         │
                Stage 2 (sequential / dependent)                   │
                         │                                         │
                  ┌──────▼─────┐                                  │
                  │  Agent 4   │  R4 needs R1's enum              │
                  │  R4        │                                  │
                  └──────┬─────┘                                  │
                         │                                         │
        ┌────────────────┼────────────────┐                       │
        │                │                │                       │
   ┌────▼─────┐     ┌────▼─────┐    ┌─────▼──────┐               │
   │ Agent 2  │     │ Agent 3  │    │ Agent 5    │               │
   │ R2 only  │     │ R3 only  │    │ R7.c + d   │ R7.c needs R4 │
   └────┬─────┘     └────┬─────┘    └─────┬──────┘               │
        │                │                │                       │
        │                │                │                       │
                Stage 3 (cleanup / dependent on Stage 2)
        │                │                                         │
   ┌────▼─────┐     ┌────▼─────┐                                  │
   │ Agent 2  │     │ Agent 3  │                                  │
   │ R10      │     │ R9       │                                  │
   └────┬─────┘     └────┬─────┘                                  │
        │                │                                         │
        └────────────────┴─────────────────────────────────────────┤
                                                                   │
                Stage 4 — integration audit (orchestrator)         │
                  • Replays all migrations in dep order on live    │
                  • Runs cross-agent verification queries          │
                  • Produces FINAL_REVIEW_PLAN_AUDIT.md            │
                                                                   ▼
                                                                Agent 1
                                                                  R8
                                                                  (last — depends on
                                                                  every other migration
                                                                  to seed correct
                                                                  :DataIssue counts)
```

**Critical rule:** **Agent 1's R8 runs LAST**, after every other migration, because `:DataIssue` nodes need to know the post-migration state of every edge they reference. R8's seed pass classifies issues that survive R1–R10.

---

## §4 Shared baseline and branching

### §4.1 Baseline snapshot

The orchestrator takes the baseline first:

```bash
# From wip/kinan2 HEAD (commit 24ccfb8f or later)
python _scripts/_snapshot_predelete.py \
  --output _neo4j/intake/runs/2026-05-21_review_based_plan/baseline_snapshot/ \
  --include-stats
```

Outputs:
- `nodes.jsonl` — every node with id, labels, properties
- `relationships.jsonl` — every edge with type, endpoints, properties
- `stats.json` — `apoc.meta.stats()` output
- `label_counts.json` — node count per label
- `rel_type_counts.json` — edge count per type

Every agent must reference this snapshot as their starting state. Discrepancies between snapshot and live-at-start (e.g., if another commit lands between snapshot and your migration) must be reported.

### §4.2 Branching

Each agent works on a feature branch off the baseline commit:

```bash
git switch -c <agent-branch>     # see §1 table for branch prefix
```

Branches must NOT merge to `wip/kinan2` until the orchestrator's Stage-4 integration audit passes.

Each agent's branch contains **only**:
- Their migration `.cypher` files under `_neo4j/intake/runs/2026-05-21_review_based_plan/<agent_label>/migrations/`
- Their runner script (`logs/<agent_label>_runner.py`) and audit JSONLs (`logs/<agent_label>_*.json`)
- Their report (`reports/<agent_label>_report.md`)
- Their done flag(s) (`<PHASE>_DONE.flag`)

Each branch should be ≤ 25 files and ≤ 5,000 lines so the orchestrator can review and merge cleanly.

### §4.3 No agent writes outside its own subdirectory

Hard rule. If your migration needs to update a file outside `_neo4j/intake/runs/2026-05-21_review_based_plan/<your_agent_label>/`, raise it in your handoff doc and the orchestrator handles it during Stage 4.

---

## §5 Conflict-avoidance matrix

What each agent WRITES vs READS, so you know what you must not race on.

| Agent | Writes (mutates) | Reads (consults) |
|---|---|---|
| Agent 1 R1 | `evidence_origin` on **every relationship**; `evidence_confidence` on bookkeeping edges; sets `is_bookkeeping` | nothing else |
| Agent 1 R8 | new `:DataIssue` nodes + `:CONCERNS` edges | every edge (post all other migrations) |
| Agent 2 R2 | new `:Layer` / `:LCAModule` / `:RechtlicheBedingung` / `:Zertifizierungssystem` nodes; new TEILT_LAYER / BERECHNET_NACH_MODUL / HAT_RECHTLICHE_BEDINGUNG / HAT_ZERTIFIZIERUNG / GILT_IN_LAND edges; adds `:Tool` secondary label to `:Software` | `Bauteiltyp.brand_layer`, `Projekt.lca_module_scope`, `<src>.legal_conditions`, `Projekt.certifications`, `Software.kind` |
| Agent 2 R10 | new `:DeprecatedType` nodes | label registry |
| Agent 3 R3 | new `:HAS_BAUWERK` edges (`Projekt`→`Bauwerk`); new `:RELEVANT_FOR` edges (`ReuseRule`→`Projekt`) | `:HAT_BAUTEILGRUPPE`, `:FROM_DONOR`, `:INTO_RECEIVER`, `:APPLIES_IN`, `:APPLIES_TO`, `:NUTZT_MATERIAL`, `:LIEGT_IN_LAND` |
| Agent 3 R9 | renames `:ASSOZIIERT_MIT_PROJEKT` → `:STUB_PROJECT_LINK` | nothing else mutated; reads dossier text via `:Quelle.text_content` if R7.d populated it |
| Agent 4 R4 | new `:Kennwert` nodes + `:HAT_KENNWERT` edges; later strips `Projekt.*_facts` JSON properties (gated) | `Projekt.reuse_share_facts`, `Projekt.co2_facts`, `Projekt.cost_facts`; `evidence_origin` enum (must be R1-extended) |
| Agent 5 R7 | merges `qu_*_dossier` → `q_<slug>_md`; creates 7 new `:Projekt`/`:Programm` nodes; populates `:Quelle.text_content` (case_markdown); creates `:Kennwert` (R7.c, using R4's schema) | `:Quelle.aliases`, `:Quelle.quelltyp`, dossier `.md` files |
| Orchestrator R5 | `:Bauteilgruppe.bg_kind` property on all 369 BGs | `:FROM_DONOR`, `:INTO_RECEIVER` |
| Orchestrator Stage 4 | nothing (read-only) | the entire post-migration graph |

### §5.1 Read-write race table

| Pair | Race? | Resolution |
|---|---|---|
| Agent 1 R1 ↔ Agent 4 R4 | Yes — R4 reads new `evidence_origin` enum | R4 starts ONLY after R1 lands in main |
| Agent 5 R7.a/b ↔ Agent 3 R3 | Yes — R3 must include the 7 new projects | R3 starts ONLY after R7.a/b lands |
| Agent 5 R7.c ↔ Agent 4 R4 | Yes — R7.c writes `:Kennwert` using R4's schema | R7.c starts ONLY after R4 lands |
| Agent 2 R10 ↔ Agent 2 R2 | Yes — R10 audits which labels are still empty after R2 | R10 starts ONLY after R2 lands (same agent, sequential) |
| Agent 1 R8 ↔ all others | Yes — R8 must run last | R8 is gated on Stage 3 complete |
| Orchestrator R5 ↔ all others | No — `bg_kind` is a property add, no semantic overlap | Run anytime, parallel-safe |
| Agent 1 R1 ↔ Agent 2 R2 | No — R2 sets `evidence_origin` on new edges; if R2 uses old enum value, R1 will reclassify it | Either order; recommend R1 first so R2 sees the new enum |
| Agent 3 R3 ↔ Agent 5 R7.d | No — R7.d adds `:Quelle.text_content`, R3 doesn't read Quelle text | Parallel-safe |

### §5.2 Sequencing summary (deterministic)

```
1. Orchestrator: baseline snapshot
2. Parallel: Agent 1 R1, Agent 5 R7.a, Agent 5 R7.b, Orchestrator R5
3. Wait for stage-2 gate
4. Sequential: Agent 4 R4
5. Parallel: Agent 2 R2, Agent 3 R3, Agent 5 R7.c, Agent 5 R7.d
6. Parallel: Agent 2 R10, Agent 3 R9
7. Agent 1 R8 (last)
8. Orchestrator Stage 4: integration audit
```

---

## §6 Common conventions

Every agent must follow these. Non-conformance = orchestrator rejects the branch.

### §6.1 File layout

```
_neo4j/intake/runs/2026-05-21_review_based_plan/<agent_label>/
├── PHASE_<X>_DONE.flag                    one flag per logical phase
├── migrations/
│   └── mig_<phase>_<purpose>.cypher       canonical, idempotent Cypher
├── logs/
│   ├── <agent_label>_runner.py            executor; reads creds from .cursor/mcp.json
│   ├── <agent_label>_probe_pre.json       pre-migration live counts
│   ├── <agent_label>_probe_post.json      post-migration live counts
│   ├── <agent_label>_audit.jsonl          per-statement audit trail
│   └── <agent_label>_progress.log         human-readable progress log
└── reports/
    └── <agent_label>_report.md            structured report (template §6.6)
```

### §6.2 Cypher conventions

- Every migration MUST be **idempotent** — running it twice produces the same end state.
- Every migration MUST use `MERGE` for new nodes/edges, never `CREATE` (unless guarded by `WHERE NOT exists{...}`).
- Every new edge MUST carry the 5 evidence properties: `evidence_origin`, `evidence_basis`, `evidence_confidence`, `evidence_source_id`, `migration_origin`.
- `evidence_origin` MUST use the R1-extended enum: `{source_curated, topology_synthesized, registry_derived, inferred, external_unfolded}`.
  - If your migration creates edges from registry data → `registry_derived`.
  - If your migration creates edges from graph topology (e.g., R3's `HAS_BAUWERK` derived from BG paths) → `topology_synthesized`.
  - If your migration creates edges from a rule/heuristic → `inferred`.
  - Do NOT use `source_curated` unless the edge is grounded in a verbatim cell from a source document.
- Every node/edge created MUST carry `migration_origin = '<your_migration_id>'`.
- Every audit query at the bottom of your migration MUST return 0 violations or the runner aborts.

### §6.3 Runner conventions

- Use Python with the `neo4j` driver 5.x; read creds from `.cursor/mcp.json` via `_scripts/neo4j_env.resolve_connection()`.
- Use the `default_access_mode` = `WRITE` for migrations; `READ` for probes and verification.
- Page large queries with `SKIP/LIMIT` to avoid timeouts.
- Write `<agent>_probe_pre.json` before any mutation, `<agent>_probe_post.json` after.
- Append every executed Cypher statement (with row counts and timings) to `<agent>_audit.jsonl`.

### §6.4 Done-flag conventions

`PHASE_<X>_DONE.flag` is a JSON file:

```json
{
  "phase": "R1",
  "agent": "agent_1_evidence_honesty",
  "completed_at_utc": "2026-05-22T11:42:13+00:00",
  "verified": true,
  "verification_query_results": { /* per-gate results */ },
  "extra": { /* phase-specific metrics */ }
}
```

### §6.5 Done flags expected (per agent)

| Agent | Flags |
|---|---|
| Agent 1 | `PHASE_R1_DONE.flag`, `PHASE_R8_DONE.flag` |
| Agent 2 | `PHASE_R2_DONE.flag`, `PHASE_R10_DONE.flag` |
| Agent 3 | `PHASE_R3_DONE.flag`, `PHASE_R9_DONE.flag` |
| Agent 4 | `PHASE_R4_DONE.flag` |
| Agent 5 | `PHASE_R7_DONE.flag` (covers R7.a–d) |
| Orchestrator | `PHASE_R5_DONE.flag`, `STAGE_4_AUDIT_DONE.flag` |

### §6.6 Report template

Every agent's `reports/<agent>_report.md` contains:

```markdown
# Agent <N> — Phase R<X>[+R<Y>] Report

- **Agent:** <agent_label>
- **Database:** mit-bestand
- **Branch:** <branch>
- **Commit at start:** <sha>
- **Commit at end:** <sha>
- **Completed (UTC):** <iso>
- **Verdict:** PASS | PARTIAL | FAIL

## Executive summary
<3-5 sentence summary>

## Before / after counts
| Metric | Before | After | Δ |

## Acceptance gates
| Gate | Expected | Live | Verdict |

## Issues raised (for orchestrator)
- <bullet of unresolved/unexpected findings>

## Risks / follow-ups
- <bullet>

## Open questions for D1–D10
- <which decisions you encountered and how you handled them>

## Artefacts
```
<paths>
```

## Handoff
<what the next agent / orchestrator needs to know>
```

---

## §7 Handoff protocol

### §7.1 When you finish your phase

1. Push your branch to remote.
2. Open a PR against `wip/kinan2` titled `<agent_label> — Phase <X>` with the report as PR body.
3. Tag the orchestrator (`@kinan` or write a row in the handoff log §7.3).
4. Do NOT merge yourself.

### §7.2 What the orchestrator does on receive

1. Reviews PR diff (≤ 25 files expected).
2. Pulls the branch locally, runs the agent's runner against a forked dev db.
3. Checks that done flags exist, audits pass, idempotency holds (re-running produces same state).
4. Merges into a holding branch `orch/integrate-2026-05-21`.
5. After all 5 agents land in `orch/integrate-2026-05-21`, orchestrator runs Stage 4 audit.
6. If audit passes, fast-forward `wip/kinan2`.

### §7.3 Handoff log

The orchestrator maintains [HANDOFF_LOG.md](HANDOFF_LOG.md) in this directory. Each row:

```markdown
| 2026-05-22 14:00 | agent_1 | R1 complete (3,802 edges reclassified); 17 evidence-origin enum violations resolved | PR #42 | PASS |
```

Update this log when you finish; the orchestrator reviews on cadence.

---

## §8 Decisions (D1–D10 from [REVIEW_BASED_PLAN.md](../REVIEW_BASED_PLAN.md) §14)

Each agent's brief lists which D-numbers block their phase. The current standing on each:

| ID | Decision | Status | Default | Who blocks |
|---|---|---|---|---|
| D1 | Registry-derived edges: `belegt` or `teilweise_belegt`? | OPEN | downgrade | Agent 1 R1 |
| D2 | Delete mirror properties after R2 lands? | OPEN | delete next cycle | Agent 2 R2 follow-up |
| D3 | Add `:Bauteilgruppe-[:DERIVED_FROM]->:Bauteilgruppe` in R3? | OPEN | defer | Agent 3 R3 |
| D4 | `:Kennwert.category` enum or kennwert-string only? | OPEN | enum | Agent 4 R4 |
| D5 | Lift `quality_tier_facts` to `:Kennwert`? | OPEN | no | Agent 4 R4 |
| D6 | Secondary labels `:BauteilgruppeBatch` / `:BauteilgruppeCategory`? | OPEN | property-only | Orchestrator R5 |
| D7 | Schema language (EN vs DE)? | DEFERRED | — | R6 (not in this round) |
| D8 | Classify `q_refair_bordeaux_md` as `:Programm` or `:Marktmodell`? | OPEN | `:Programm` | Agent 5 R7.b |
| D9 | Add `Quelle.text_content` for case_markdown? | OPEN | yes | Agent 5 R7.d |
| D10 | R8: apply audit policy retrospectively? | OPEN | yes | Agent 1 R8 |

**Each agent must record in their report which D-numbers they hit and how they resolved them.** If a decision is open and your phase can't proceed without it, flag it in [HANDOFF_LOG.md](HANDOFF_LOG.md) and pause.

---

## §9 Stage 4 — orchestrator integration audit

After all 5 agents land:

1. Replay every migration in dependency order against a fresh fork of the live db.
2. Re-run the radical-quality-reset's Q1–Q7 acceptance queries with **honest** filters:
   - Q1: filter `evidence_origin='source_curated'` only (expect 0 or very few).
   - Q2: filter pollutant edges by `evidence_basis IN ['documented']` only (expect 0).
   - Q3: `MATCH (:Projekt)-[:HAT_KENNWERT]->(:Kennwert)` graph-native (expect ≥ R4 baseline).
   - Q4: filter `:BETEILIGT_AN` only (no `:STUB_PROJECT_LINK`); expect ≤ 1.
   - Q5: `MATCH (:ReuseRule)-[:RELEVANT_FOR]->(:Projekt)` (new R3 edge); expect non-zero for UK/BE/DE/NL/CH/FI/NO projects, zero for France.
   - Q6: 5-bucket origin distribution.
   - Q7: ZITIERT_QUELLE chains, with `:Quelle.text_content` excerpts now visible.
3. Run cross-agent invariants:
   - Every `evidence_origin` is in the R1-extended enum.
   - Every `evidence_origin='source_curated'` edge has a non-null, non-synthetic `evidence_excerpt`.
   - No node has both `:Bauteilgruppe` and `:Layer` (label-purity check).
   - Every `:Projekt` has either a `bg_kind` distribution (from R5) or no BG (a tier-3 stub).
   - `:DataIssue` count is non-zero; per-`:Projekt` issue density is queryable.
   - Q1–Q7 numbers from the new audit do NOT match the old Pass-2 audit (that's the goal).

4. Write `FINAL_REVIEW_PLAN_AUDIT.md` and `STAGE_4_AUDIT_DONE.flag`.

---

## §10 Glossary (one screen)

Terms used across all 5 agent briefs:

- **mit-bestand** — the Neo4j database name (bolt://localhost:7687).
- **`source_curated`** — new R1 value for `evidence_origin`. Means: a human read a verbatim cell from a source dossier and recorded the excerpt. NOT to be created from graph topology.
- **`topology_synthesized`** — new R1 value. Means: this edge or property was generated by a migration from existing graph structure (e.g., R3's `HAS_BAUWERK` from BG paths; Repair D's auto-excerpts; the era→pollutant inference).
- **`registry_derived`** — new R1 value. Means: this edge originates from a master registry (`q_akteursliste_master_md`, etc.).
- **`inferred`** — existing value, retained. Means: derived by a rule (era×material; year→era).
- **`external_unfolded`** — new R1 value. Means: derived from a citation array via `mig_4c_1`.
- **`is_bookkeeping`** — new R1 property. `true` for plumbing edges (`ANCHORED_BY`).
- **`:DataIssue`** — new R8 node. Records a known data-quality concern as a queryable artefact instead of fixing it via reclassification.
- **`:Kennwert`** — new R4 node. Holds one quantitative fact (reuse share, CO₂ saving, cost) with units, method, bilanzgrenze.
- **`bg_kind`** — new R5 property on `:Bauteilgruppe`. `'batch'` (has FROM_DONOR or INTO_RECEIVER) or `'category'` (no donor/receiver edges).
- **`:HAS_BAUWERK`** — new R3 edge from `:Projekt` to `:Bauwerk` with `role: 'donor'|'receiver'`.
- **`:RELEVANT_FOR`** — new R3 edge from `:ReuseRule` to `:Projekt` derived via country×material match.
- **`:STUB_PROJECT_LINK`** — new R9 type, renamed from `:ASSOZIIERT_MIT_PROJEKT` for honest naming.
- **`:DeprecatedType`** — new R10 node. Records old-name → new-name mapping for retired labels/types.

---

## §11 Escalation

If you (any agent) hit something the brief doesn't cover:

1. **Do not improvise** on schema decisions. Pause and write to [HANDOFF_LOG.md](HANDOFF_LOG.md).
2. **Do not delete data** outside the explicit scope of your phase.
3. **Do not push to `wip/kinan2`** directly; only via PR.
4. **Do not run R8** before Stage 3 completes (i.e., before R1–R7, R9, R10, and the orchestrator's R5 all merged into `orch/integrate-2026-05-21`).

If the live db state at start of your phase disagrees with the baseline snapshot, abort and write the discrepancy to the handoff log. Do not migrate against an unexpected state.

---

## §12 What "done" looks like for this whole effort

- 5 agent branches + 1 orchestrator branch all merged into `orch/integrate-2026-05-21`.
- All 9 done flags present (`PHASE_R1`–`R10` except R6).
- `STAGE_4_AUDIT_DONE.flag` present.
- `FINAL_REVIEW_PLAN_AUDIT.md` written, showing the honest Q1–Q7 numbers.
- `HANDOFF_LOG.md` complete.
- `wip/kinan2` fast-forwarded.
- Kinan signs off on the final audit and decides whether to keep R6 (language unification) for a later round.

After that, the graph will have:
- Honest `evidence_origin` distribution (5 values, not 3).
- Restored queryable nodes for Layer, LCAModule, RechtlicheBedingung, Zertifizierungssystem (+ `:Tool` secondary label).
- Direct `:Projekt→:Bauwerk` and `:ReuseRule→:Projekt` edges.
- `:Kennwert` nodes for all reuse/CO₂/cost facts.
- Clean separation between `:BETEILIGT_AN` and `:STUB_PROJECT_LINK`.
- `:Bauteilgruppe.bg_kind` disambiguation.
- 7 fewer orphan dossiers; 16 dual-naming pairs resolved.
- `:DataIssue` audit trail visible at the graph level.
- A new honest Q1–Q7 baseline that supersedes [FINAL_PASS2_AUDIT.md](../intake/runs/2026-05-20_radical_quality_reset/FINAL_PASS2_AUDIT.md).

**Tier-1 cohort will likely shrink from 11 to 3–5 projects.** That drop is the success metric.

---

**End of ORCHESTRATION.md.** Now read your assigned brief.
