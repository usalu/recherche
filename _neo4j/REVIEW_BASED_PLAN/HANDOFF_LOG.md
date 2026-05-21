# Handoff log — Review-based remediation 2026-05-21

> Append-only log of agent handoffs. Each agent adds **one row** when finishing a phase. The orchestrator reads this to know when to merge branches and when to gate the next stage.

**Convention:**
- Newest entry at the bottom.
- Date/time in ISO local + UTC offset, e.g. `2026-05-22 14:00 +02:00`.
- "Status" column is one of: `STARTED`, `PASS`, `PARTIAL`, `FAIL`, `BLOCKED`.
- "Notes" should fit on one screen line; longer detail goes in your `reports/<agent>_report.md`.

---

## §1 Stage 0 — baseline

| When | Who | What | Branch / PR | Status | Notes |
|---|---|---|---|---|---|
| _<fill>_ | orchestrator | Baseline snapshot of mit-bestand taken | `orch/r5-and-integrate` | _<STARTED/PASS>_ | nodes=3802, rels=25023 (expected from FINAL_PASS2_AUDIT.md §1) |

---

## §2 Stage 1 — parallel-safe additive phases

| When | Who | What | Branch / PR | Status | Notes |
|---|---|---|---|---|---|
| _<fill>_ | agent_1 | R1 evidence_origin split + is_bookkeeping flag | `agent1/r1-r8-evidence` | _<STARTED/PASS>_ | _<reclassification counts: source_curated=X, topology_synthesized=Y, registry_derived=Z, is_bookkeeping=W>_ |
| _<fill>_ | agent_5 | R7.a dual-naming Quelle merge (16 pairs) | `agent5/r7-loader` | _<…>_ | _<merged_pairs=16>_ |
| _<fill>_ | agent_5 | R7.b 7 orphan dossiers resolved | `agent5/r7-loader` | _<…>_ | _<3 Projekt + 4 Programm created>_ |
| _<fill>_ | orchestrator | R5 bg_kind tagging (369 BGs) | `orch/r5-and-integrate` | _<…>_ | _<batch=X, partial_batch=Y, category=Z>_ |

---

## §3 Stage 2 — phases with dependencies

| When | Who | What | Branch / PR | Status | Notes |
|---|---|---|---|---|---|
| _<fill>_ | agent_4 | R4 Kennwert lift (depends: R1) | `agent4/r4-kennwert` | _<…>_ | _<Kennwert created: reuse_share=X, co2_saving=Y, cost=Z>_ |
| _<fill>_ | agent_2 | R2 restore demoted labels (depends: R1) | `agent2/r2-r10-restore` | _<…>_ | _<Layer=6, LCAModule=6, RB=X, Cert=Y, Tool secondary label=8>_ |
| _<fill>_ | agent_3 | R3 HAS_BAUWERK + RELEVANT_FOR (depends: R1, R7.a/b) | `agent3/r3-r9-structure` | _<…>_ | _<HAS_BAUWERK=X (donor=A, receiver=B), RELEVANT_FOR=Y>_ |
| _<fill>_ | agent_5 | R7.c Section-8 re-extraction (depends: R4) | `agent5/r7-loader` | _<…>_ | _<Kennwert from Section-8 = X>_ |
| _<fill>_ | agent_5 | R7.d Quelle.text_content + drift validator | `agent5/r7-loader` | _<…>_ | _<116 case_markdown populated; drift findings=X>_ |

---

## §4 Stage 3 — cleanup

| When | Who | What | Branch / PR | Status | Notes |
|---|---|---|---|---|---|
| _<fill>_ | agent_2 | R10 :DeprecatedType audit nodes (depends: R2) | `agent2/r2-r10-restore` | _<…>_ | _<DeprecatedType count=X>_ |
| _<fill>_ | agent_3 | R9 ASSOZIIERT_MIT_PROJEKT → STUB_PROJECT_LINK (depends: R3) | `agent3/r3-r9-structure` | _<…>_ | _<renamed 200 edges>_ |

---

## §5 Stage 4 — final

| When | Who | What | Branch / PR | Status | Notes |
|---|---|---|---|---|---|
| _<fill>_ | agent_1 | R8 :DataIssue seed (depends: Stages 1–3 done) | `agent1/r1-r8-evidence` | _<…>_ | _<DataIssue count by kind: q1_topology_synthesis=254, pollutant_inference=799, …>_ |
| _<fill>_ | orchestrator | Stage 4 integration audit | `orch/integrate-2026-05-21` | _<…>_ | _<FINAL_REVIEW_PLAN_AUDIT.md produced; honest Q1=X, Q2 doc=0, Q3 graph-native=Y, Q4 with STUB filter=Z>_ |

---

## §6 Decision resolutions

When an agent encounters one of D1–D10, record their choice here.

| D# | Topic | Decided | Decided by | Resolution |
|---|---|---|---|---|
| D1 | registry_derived confidence | _<open>_ | _<…>_ | _<downgrade to teilweise_belegt vs keep belegt>_ |
| D2 | delete mirror properties after R2 | _<open>_ | _<…>_ | _<defer to post-Stage-4>_ |
| D3 | :Bauteilgruppe-[:DERIVED_FROM]->:Bauteilgruppe | _<open>_ | _<…>_ | _<defer>_ |
| D4 | :Kennwert.category enum | _<resolved>_ | orchestrator | YES (default) |
| D5 | lift quality_tier_facts | _<resolved>_ | orchestrator | NO (default) |
| D6 | bg_kind secondary labels | _<resolved>_ | orchestrator | NO — property only (default) |
| D7 | schema language EN vs DE | _<deferred>_ | — | R6 not in this round |
| D8 | refair_bordeaux classification | _<open>_ | _<…>_ | _<:Programm default>_ |
| D9 | Quelle.text_content | _<open>_ | _<…>_ | _<YES default>_ |
| D10 | R8 retrospective tier recompute | _<open>_ | _<…>_ | _<YES; handled by orchestrator Stage 4>_ |

---

## §7 Blockers + escalations

If you cannot proceed, write here. The orchestrator triages.

| When | Who | What's blocked | Why | Resolution |
|---|---|---|---|---|
| | | | | |

---

## §8 Notes

- Append at the bottom of the relevant Stage table; do not edit older rows.
- If you need to amend an earlier row (e.g., your run had to be re-done), add a new row and reference the old one in "Notes": "supersedes 2026-05-22 14:00 row".
- The orchestrator's final Stage 4 audit references this log to produce `FINAL_REVIEW_PLAN_AUDIT.md`.

---

**End of HANDOFF_LOG.md.**
