# STATUS — review-based remediation

> Single-page state dashboard. Updated by the orchestrator on each sweep. Last sweep: **2026-05-21 13:45 +02:00**.

---

## Phase board

| # | Phase | Owner | State | Flag |
|:-:|---|---|:-:|---|
| R1 | evidence_origin split + bookkeeping flag | agent 1 | ✅ DONE | `PHASE_R1_DONE.flag` |
| R2 | restore demoted labels (Layer, LCAModule, RB, Cert, Tool) | agent 2 | ✅ DONE | `PHASE_R2_DONE.flag` |
| R3 | HAS_BAUWERK + RELEVANT_FOR edges | agent 3 | 🟡 UNBLOCKED — RUN NOW | — |
| R4 | Kennwert lift from JSON-string facts | agent 4 | ✅ DONE | `PHASE_R4_DONE.flag` |
| R5 | Bauteilgruppe bg_kind disambiguation | orchestrator | ✅ DONE | `PHASE_R5_DONE.flag` |
| R7.a/b | dual-naming merge + 1/7 orphans resolved | agent 5 | ✅ DONE (partial) | `PHASE_R7AB_DONE.flag` |
| R7.c | Section-8 re-extraction | agent 5 | ⚠️ DEFERRED (absorbed by R4) | — |
| R7.d | Quelle.text_content + drift validator | agent 5 | ✅ DONE | `PHASE_R7D_DONE.flag` |
| R7 (composite) | (umbrella for R7.a–d) | orchestrator | ✅ DONE | `PHASE_R7_DONE.flag` + `PHASE_R7_AB_DONE.flag` |
| R9 | ASSOZIIERT_MIT_PROJEKT → STUB_PROJECT_LINK rename | agent 3 | 🔲 BLOCKED on R3 | — |
| R10 | DeprecatedType audit nodes | agent 2 | ✅ DONE | `PHASE_R10_DONE.flag` |
| R8 | DataIssue seed (LAST) | agent 1 | 🔲 BLOCKED on R3+R9 | — |
| Stage 4 | integration audit + FINAL_REVIEW_PLAN_AUDIT.md | orchestrator | 🔲 BLOCKED on R8 | — |

---

## What to do next (in order)

1. **Agent 3:** `python _neo4j/intake/runs/2026-05-21_review_based_plan/agent_3_structural_completion/logs/agent_3_runner.py r3`
2. **Agent 3:** `python ../agent_3_runner.py r9` (after R3 verified)
3. **Agent 1:** `python _neo4j/intake/runs/2026-05-21_review_based_plan/agent_1_evidence_honesty/logs/agent_1_runner.py r8` (after R9)
4. **Orchestrator:** `python _neo4j/intake/runs/2026-05-21_review_based_plan/stage_4_integration/logs/stage_4_audit_runner.py`

Each step refuses to start unless the previous step's flag exists.

---

## Live graph state (as of last sweep)

| Metric | Value | Source |
|---|---:|---|
| Total nodes | 4,151 | Agent 5 R7.d post-probe |
| Total relationships | 25,377 | Agent 5 R7.d post-probe |
| `:Kennwert` (R4) | 258 | Agent 4 R4 |
| `:Bauteilgruppe` with `bg_kind` | 369 (batch=254, partial=87, category=28) | Orchestrator R5 |
| `:Layer` (R2.a) | 6 | Agent 2 R2 |
| `:LCAModule` (R2.b) | 5 | Agent 2 R2 |
| `:RechtlicheBedingung` (R2.c) | 15 | Agent 2 R2 |
| `:Zertifizierungssystem` (R2.d) | 8 | Agent 2 R2 |
| `:Tool` secondary label (R2.e) | 8 | Agent 2 R2 |
| `:DeprecatedType` (R10) | 13 | Agent 2 R10 |
| `:DataIssue` (R7.d drift) | 59 | Agent 5 R7.d |
| `is_bookkeeping=true` edges (R1) | 1,022 | Agent 1 R1 |
| `evidence_origin='source_curated'` | 2,803 | Agent 1 R1 |
| `evidence_origin='topology_synthesized'` | 18,701 | Agent 1 R1 |
| `evidence_origin='registry_derived'` | 1,727 | Agent 1 R1 |
| `evidence_origin='inferred'` | 1,523 | Agent 1 R1 |
| `evidence_origin='external_unfolded'` | 269 | Agent 1 R1 |

---

## Known open follow-ups (post-Stage 4)

| ID | Topic | Doc |
|---|---|---|
| FU-1 | Tier-1 honest recompute migration | [POST_STAGE4_FOLLOWUPS.md §1](POST_STAGE4_FOLLOWUPS.md) |
| FU-2 | R7.b.v2 — close 6 remaining orphan dossiers | [POST_STAGE4_FOLLOWUPS.md §2](POST_STAGE4_FOLLOWUPS.md) |
| FU-3 | R7.c.v2 — Section-8 re-extraction for R8-flagged projects | [POST_STAGE4_FOLLOWUPS.md §3](POST_STAGE4_FOLLOWUPS.md) |
| FU-4 | D2 cleanup — strip `*_facts` JSON-string mirrors | [POST_STAGE4_FOLLOWUPS.md §4](POST_STAGE4_FOLLOWUPS.md) |
| FU-5 | R6 — schema language unification (deferred decision D7) | [POST_STAGE4_FOLLOWUPS.md §5](POST_STAGE4_FOLLOWUPS.md) |
| FU-6 | Tighten audit: `dossier_uses_retired_type` drift validator pre-flight | [POST_STAGE4_FOLLOWUPS.md §6](POST_STAGE4_FOLLOWUPS.md) |

---

## Documents

| Topic | Where |
|---|---|
| Master orchestration | [ORCHESTRATION.md](ORCHESTRATION.md) |
| Per-agent briefs | `AGENT_<1-5>_<topic>.md` |
| Orchestrator's R5 phase | [ORCHESTRATOR_PART_R5.md](ORCHESTRATOR_PART_R5.md) |
| Orchestrator decisions | [ORCHESTRATOR_DECISIONS.md](ORCHESTRATOR_DECISIONS.md) |
| Handoff log | [HANDOFF_LOG.md](HANDOFF_LOG.md) |
| Stage 4 plan | [STAGE_4_PLAN.md](STAGE_4_PLAN.md) |
| Post-Stage-4 follow-ups | [POST_STAGE4_FOLLOWUPS.md](POST_STAGE4_FOLLOWUPS.md) |
| This dashboard | [STATUS.md](STATUS.md) |

---

**End of STATUS.md.**
