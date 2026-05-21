# STATUS — review-based remediation

> Single-page state dashboard. Last sweep: **2026-05-21 14:00 +02:00**. **State: STAGE 4 COMPLETE. Verdict PASS WITH RESIDUALS.**

---

## 🎯 Headline

The full remediation pipeline ran end-to-end against `mit-bestand`. Final audit lives at [_neo4j/FINAL_REVIEW_PLAN_AUDIT.md](../FINAL_REVIEW_PLAN_AUDIT.md).

**Quelle remediation (Q1–Q5) is now ALSO STAGED** at [_neo4j/QUELLE_REMEDIATION_PLAN.md](../QUELLE_REMEDIATION_PLAN.md). It rolls back R7.d's `text_content` mistake, extracts every URL into first-class nodes, and surfaces `source_urls` on Projekt/Bauwerk/Akteur for instant Browser visibility. Runner ready: `python _neo4j/intake/runs/2026-05-21_quelle_remediation/logs/quelle_remediation_runner.py all`. User guide at [_neo4j/QUELLE_QUERY_GUIDE.md](../QUELLE_QUERY_GUIDE.md). CLI helper at `_scripts/find_sources.py`.

| Indicator | Pre-remediation | Post-remediation |
|---|---|---|
| Q1 (Reuse Story) under `source_curated` filter | 266 (synthetic) | **0** ← the honest signal |
| `evidence_origin='topology_synthesized'` visible separately | no | **19,071 edges** |
| `:Kennwert` queryable graph nodes | 0 | **258** |
| `:DataIssue` audit nodes | 0 | **1,454** |
| `:HAS_BAUWERK` direct edges (Projekt → Bauwerk) | 0 | **184** |
| `:RELEVANT_FOR` rule↔project edges | 0 | **103** |
| `:STUB_PROJECT_LINK` (honest name for unverified stubs) | 0 (hidden as ASSOZIIERT_MIT_PROJEKT) | **200** |
| `:Bauteilgruppe` with `bg_kind` | 0 | **369** (batch=254, partial=87, category=28) |
| Tier-1 cohort | 11 | 11 (see §3 below — needs FU-1 v2) |

---

## ✅ Phase board

| # | Phase | Owner | State | Flag |
|:-:|---|---|:-:|---|
| R1 | evidence_origin split + bookkeeping flag | agent 1 | ✅ DONE | `PHASE_R1_DONE.flag` |
| R2 | restore demoted labels | agent 2 | ✅ DONE | `PHASE_R2_DONE.flag` |
| R3 | HAS_BAUWERK + RELEVANT_FOR | agent 3 | ✅ DONE (184 + 103) | `PHASE_R3_DONE.flag` |
| R4 | Kennwert lift | agent 4 | ✅ DONE (258 nodes) | `PHASE_R4_DONE.flag` |
| R5 | bg_kind disambiguation | orchestrator | ✅ DONE (369 BGs tagged) | `PHASE_R5_DONE.flag` |
| R7.a/b | dual-naming merge + 1/7 orphans | agent 5 | ✅ DONE (partial) | `PHASE_R7AB_DONE.flag` |
| R7.c | Section-8 re-extraction | agent 5 | ⚠️ DEFERRED (absorbed by R4) | — |
| R7.d | Quelle.text_content + drift validator | agent 5 | ✅ DONE (95/100 + 59 drift) | `PHASE_R7D_DONE.flag` |
| R7 (composite) | umbrella | orchestrator | ✅ DONE | `PHASE_R7_DONE.flag` |
| R9 | ASSOZIIERT_MIT_PROJEKT → STUB_PROJECT_LINK | agent 3 | ✅ DONE (200 renamed) | `PHASE_R9_DONE.flag` |
| R10 | DeprecatedType audit nodes | agent 2 | ✅ DONE (13 nodes) | `PHASE_R10_DONE.flag` |
| R8 | DataIssue seed | agent 1 | ✅ DONE (1,454 nodes) | `PHASE_R8_DONE.flag` |
| **Stage 4** | **integration audit** | orchestrator | ✅ **DONE (51 queries, 0 errors)** | `STAGE_4_AUDIT_DONE.flag` |

---

## ⚠️ Residuals (10 follow-ups identified)

| ID | Topic | Source | Priority |
|---|---|---|---|
| **FU-10** | **Quelle remediation** — extract URLs from text_content, surface source_urls on nodes. **STAGED, ready to run.** | [QUELLE_REMEDIATION_PLAN.md](../QUELLE_REMEDIATION_PLAN.md) | **High** |
| FU-1 v2 | **Tier definition revision** — original FU-1 didn't shift the cohort because tier gate was BELEGT_IN-based, not HAT_BAUTEILGRUPPE-based. Need to add "≥ 1 source_curated HAT_BAUTEILGRUPPE on a batch BG" as sub-criterion. | Stage 4 audit §4 | **High** |
| FU-7 | 259 `source_curated` edges without `evidence_excerpt` (C4 residual) | Stage 4 §2 | **High** |
| FU-2 | Close 6 remaining R7.b orphan dossiers | [POST_STAGE4_FOLLOWUPS.md §2](POST_STAGE4_FOLLOWUPS.md) | Medium |
| FU-3 | R7.c.v2 — Section-8 re-extract for 16 `dossier_section8_missing` projects | DataIssue kind | Medium |
| FU-4 | Strip `*_facts` JSON mirrors | D2 | Low |
| FU-5 | R6 schema language unification | D7 | Low |
| FU-6 | Drift validator as hard pre-flight gate | R7.d output | Medium |
| FU-8 | 5 `case_markdown :Quelle` without `text_content` (path mismatch in R7.d resolver) | Stage 4 §1 (Q7) | Low — partly subsumed by FU-10 |
| FU-9 | 14 `:Projekt` flagged `residual_project_no_building_path` (no BG→Bauwerk topology) | R3 report appendix | Medium |

---

## 📊 Live graph state (post-Stage-4)

| Metric | Value | Source |
|---|---:|---|
| Total nodes | 5,546 | Stage 4 §0 |
| Total relationships | 27,044 | Stage 4 §0 |
| `:Kennwert` (R4) | 258 | reuse_share=39, co2_saving=46, cost=173 |
| `:Bauteilgruppe` with `bg_kind` | 369 | batch=254, partial=87, category=28 |
| `:Layer` (R2.a) | 6 | restored |
| `:LCAModule` (R2.b) | 5 | restored |
| `:RechtlicheBedingung` (R2.c) | 15 | restored (9 from journal + 6 stubs) |
| `:Zertifizierungssystem` (R2.d) | 8 | restored |
| `:Tool` secondary label (R2.e) | 8 | added |
| `:DeprecatedType` (R10) | 13 | new |
| `:DataIssue` (R8) | 1,454 | new |
| `:HAS_BAUWERK` edges | 184 (101 donor + 83 receiver) | R3.a |
| `:RELEVANT_FOR` edges | 103 | R3.b |
| `:STUB_PROJECT_LINK` edges | 200 | R9 rename |
| `is_bookkeeping=true` flagged edges | 1,022 | R1.g |
| **evidence_origin distribution** | | R1 |
| — `topology_synthesized` | 19,071 (70.5 %) | |
| — `source_curated` | 3,074 (11.4 %) | |
| — `registry_derived` | 1,727 (6.4 %) | |
| — `inferred` | 1,523 (5.6 %) | |
| — `external_unfolded` | 269 (1.0 %) | |

---

## 📋 What's next

1. **You** review [FINAL_REVIEW_PLAN_AUDIT.md](../FINAL_REVIEW_PLAN_AUDIT.md) and decide on FU-1 v2 + FU-7 priority.
2. Decide which FUs go into a follow-up round and which can wait.
3. The graph backlog is queryable: `MATCH (i:DataIssue {status:'open'}) RETURN i.kind, count(i)` returns the 1,454 issues to work through.

---

## 📁 Documents

| Topic | Where |
|---|---|
| **Final audit** | [_neo4j/FINAL_REVIEW_PLAN_AUDIT.md](../FINAL_REVIEW_PLAN_AUDIT.md) |
| Master orchestration | [ORCHESTRATION.md](ORCHESTRATION.md) |
| Per-agent briefs | `AGENT_<1-5>_<topic>.md` |
| Orchestrator decisions | [ORCHESTRATOR_DECISIONS.md](ORCHESTRATOR_DECISIONS.md) |
| Handoff log | [HANDOFF_LOG.md](HANDOFF_LOG.md) |
| Stage 4 plan | [STAGE_4_PLAN.md](STAGE_4_PLAN.md) |
| Post-Stage-4 follow-ups | [POST_STAGE4_FOLLOWUPS.md](POST_STAGE4_FOLLOWUPS.md) |
| Raw audit results | [stage_4_audit_results.json](../intake/runs/2026-05-21_review_based_plan/stage_4_integration/logs/stage_4_audit_results.json) |
| This dashboard | [STATUS.md](STATUS.md) |

---

**End of STATUS.md.**
