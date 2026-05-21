# Review-based remediation plan — split brief

> Five-agent split of [REVIEW_BASED_PLAN.md](../REVIEW_BASED_PLAN.md). Use the table below to find your brief.

**Where are we right now?** → [STATUS.md](STATUS.md)

| If you are… | Read |
|---|---|
| Just landed; want the big picture | [ORCHESTRATION.md](ORCHESTRATION.md) |
| Looking for current state in one page | [STATUS.md](STATUS.md) |
| **Agent 1** (evidence honesty) | [AGENT_1_evidence_honesty.md](AGENT_1_evidence_honesty.md) |
| **Agent 2** (schema restoration) | [AGENT_2_schema_restoration.md](AGENT_2_schema_restoration.md) |
| **Agent 3** (structural completion) | [AGENT_3_structural_completion.md](AGENT_3_structural_completion.md) |
| **Agent 4** (data model) | [AGENT_4_data_model.md](AGENT_4_data_model.md) |
| **Agent 5** (loader hardening) | [AGENT_5_loader_hardening.md](AGENT_5_loader_hardening.md) |
| Orchestrator (Claude) | [ORCHESTRATOR_PART_R5.md](ORCHESTRATOR_PART_R5.md) |
| Orchestrator decisions log | [ORCHESTRATOR_DECISIONS.md](ORCHESTRATOR_DECISIONS.md) |
| Stage 4 audit plan | [STAGE_4_PLAN.md](STAGE_4_PLAN.md) |
| Post-Stage-4 follow-ups (FU-1…FU-6) | [POST_STAGE4_FOLLOWUPS.md](POST_STAGE4_FOLLOWUPS.md) |
| All — coordination | [HANDOFF_LOG.md](HANDOFF_LOG.md) |

## Where the original plan is

The full unsplit plan with all 10 phases (R1–R10), the 33-finding ledger, and the comparison tables lives at [../REVIEW_BASED_PLAN.md](../REVIEW_BASED_PLAN.md). Each agent brief here is a self-contained extraction; the full plan is referenced for cross-context only.

## Quick map: phases → agents

| Phase | Owner | What |
|---|---|---|
| R1 | Agent 1 | Split `evidence_origin` enum; move `bookkeeping` out of confidence enum |
| R2 | Agent 2 | Restore 5 demoted labels (Layer, LCAModule, RechtlicheBedingung, Zertifizierung, Tool-as-secondary) |
| R3 | Agent 3 | Add `:HAS_BAUWERK` and `:RELEVANT_FOR` structural edges |
| R4 | Agent 4 | Lift `*_facts` JSON-string properties to `:Kennwert` node model |
| R5 | **Orchestrator** | Tag `:Bauteilgruppe.bg_kind ∈ {batch, partial_batch, category}` |
| R6 | DEFERRED | Schema language unification (not in this round) |
| R7 | Agent 5 | Dossier loader hardening (16 dual-name merge, 7 orphan resolutions, Section-8 re-extract, drift validator) |
| R8 | Agent 1 | `:DataIssue` audit-relationship seed (LAST — runs after every other migration) |
| R9 | Agent 3 | Rename `:ASSOZIIERT_MIT_PROJEKT` → `:STUB_PROJECT_LINK` |
| R10 | Agent 2 | `:DeprecatedType` audit nodes for retired labels/types |

## Dependency at a glance

```
Stage 1 (parallel):  Agent 1 R1 ─┐  Agent 5 R7.a/b ─┐  Orchestrator R5
                                 │                  │
Stage 2 (gated):                 ├─→ Agent 4 R4 ───┘
                                 │
                                 ├─→ Agent 2 R2
                                 ├─→ Agent 3 R3
                                 ├─→ Agent 5 R7.c (depends: R4)
                                 └─→ Agent 5 R7.d
Stage 3 (cleanup):               ─→ Agent 2 R10 (depends: R2)
                                 ─→ Agent 3 R9 (depends: R3)
Stage 4 (final):                 ─→ Agent 1 R8 (depends: all above)
                                 ─→ Orchestrator integration audit
```

## File tree this brief ships

```
_neo4j/REVIEW_BASED_PLAN/
├── README.md                              ← you are here
├── STATUS.md                              ← one-page state dashboard
├── ORCHESTRATION.md                       ← master coordination
├── AGENT_1_evidence_honesty.md
├── AGENT_2_schema_restoration.md
├── AGENT_3_structural_completion.md
├── AGENT_4_data_model.md
├── AGENT_5_loader_hardening.md
├── ORCHESTRATOR_PART_R5.md                ← orchestrator's own phase
├── ORCHESTRATOR_DECISIONS.md              ← OD-1…OD-6 decisions during integration
├── STAGE_4_PLAN.md                        ← integration audit plan
├── POST_STAGE4_FOLLOWUPS.md               ← FU-1…FU-6 deferred work
└── HANDOFF_LOG.md                         ← append-only progress log

_neo4j/intake/runs/2026-05-21_review_based_plan/
├── agent_1_evidence_honesty/              (agent 1 artefacts + done flag)
├── agent_2_schema_restoration/            (agent 2 artefacts + done flags)
├── agent_3_structural_completion/         (agent 3 artefacts; R3 unblocked)
├── agent_4_data_model/                    (agent 4 artefacts + done flag)
├── agent_5_loader_hardening/              (agent 5 artefacts + composite R7 flag)
├── orchestrator_r5/                       (R5 done; bg_kind tagged on 369 BGs)
└── stage_4_integration/                   ← staged audit; runs when R3/R9/R8 land
    ├── migrations/stage_4_audit_queries.cypher
    └── logs/stage_4_audit_runner.py
```

Each agent should additionally create their own subdirectory under `_neo4j/intake/runs/2026-05-21_review_based_plan/<agent_label>/` following the conventions in [ORCHESTRATION.md §6.1](ORCHESTRATION.md).

## Sanity for the human reviewer

If you (Kinan) want to spot-check before agents start running:

1. Read [ORCHESTRATION.md §1–§5](ORCHESTRATION.md) — confirms the split makes sense.
2. Read [ORCHESTRATION.md §8](ORCHESTRATION.md) (D1–D10) — see open decisions; resolve any that block.
3. Skim each agent brief's §2 ("Mission") — confirms the chunk is what you wanted.
4. Open [ORCHESTRATOR_PART_R5.md](ORCHESTRATOR_PART_R5.md) §5 (the migration) — confirms my own work is what you wanted me to do.

If anything looks wrong: redline this README's table, the dep diagram, or the §8 decisions, and the orchestrator will rewire.
