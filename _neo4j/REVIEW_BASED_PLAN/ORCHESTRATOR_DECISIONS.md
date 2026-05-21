# Orchestrator decisions log

> Append-only. Each row is a decision the orchestrator made during integration that an agent's brief did not explicitly resolve. Decisions are stable; once recorded, agents may rely on them.

---

## OD-1 — Resolve `PHASE_R7_DONE.flag` naming mismatch (2026-05-21)

### Context

- Agent 3's brief and runner check for `PHASE_R7_DONE.flag` OR `PHASE_R7_AB_DONE.flag` (with underscore).
- Agent 5's runner wrote `PHASE_R7AB_DONE.flag` (no underscore between `AB` and `DONE`).
- Agent 3 R3 is blocked because the lookup misses by a hyphen-level difference.

### Decision

The orchestrator wrote three convergence flags inside `_neo4j/intake/runs/2026-05-21_review_based_plan/agent_5_loader_hardening/`:

| Flag | Role |
|---|---|
| `PHASE_R7AB_DONE.flag` | Agent 5's original (already present) |
| `PHASE_R7_AB_DONE.flag` | Alias with underscore (orchestrator-issued) |
| `PHASE_R7_DONE.flag` | Composite R7 done flag (orchestrator-issued) |

Agent 3 may proceed against any of the three.

### Rationale

- The underlying work (R7.a + R7.b + R7.d) is done and verified.
- Re-running Agent 5 only to rename a flag would re-execute migrations against the live db.
- A naming mismatch is exactly the kind of artefact `:DataIssue` is supposed to catch.

### Reversibility

Delete the two new flags; the original `PHASE_R7AB_DONE.flag` stays. No live-graph impact.

---

## OD-2 — Defer R7.c (Section-8 re-extraction) (2026-05-21)

### Context

- R7.c was specified in Agent 5's brief as: parse each `case_markdown` dossier's "Economy/Wirtschaft/co2/cost/reuse_share" cells and emit `:Kennwert` nodes via Agent 4's schema.
- Agent 5 did NOT run R7.c.
- Agent 4 R4 already produced **258 `:Kennwert` nodes** vs the brief's `≥ 12` expectation — far above target.

### Decision

R7.c is **deferred** to a future ingestion cycle. Stage 4 audit does not require it.

### Rationale

- Agent 4 R4's results show the JSON-array lift produced 39 reuse_share + 46 co2_saving + 173 cost = 258 `:Kennwert` nodes. This significantly exceeds the brief's target and covers the same kennwert types R7.c was supposed to extract.
- The remaining gap (dossiers whose Section-8 facts are still un-lifted) will be flagged by Agent 1 R8's seed pass under kind `dossier_section8_missing`. This makes the gap a queryable graph artefact.
- A future R7.c.v2 can be scoped to the specific `:Projekt` nodes flagged by R8.

### Risks

- Some quantitative facts present in dossier text but not in the original `*_facts` JSON arrays are missed for now. R8 surfaces this.
- Acceptable because: (a) the alternative is delaying Stage 4 indefinitely; (b) R8 makes the gap visible rather than invisible.

### Reversibility

A future migration can run the original R7.c spec without disturbing Stage 4's output.

---

## OD-3 — Apply D1: registry_derived confidence downgraded (2026-05-21)

### Context

Per Agent 1's R1 report row: "D10 applied (registry_derived belegt→teilweise_belegt)".

Agent 1 applied the recommended default for D1 (downgrade registry-derived confidence from `belegt` to `teilweise_belegt`). The HANDOFF_LOG note conflates D1 and D10; for clarity:

- **D1** (decided): registry_derived edges now carry `evidence_confidence='teilweise_belegt'`.
- **D10** (decided): R8 will apply the audit policy retrospectively. Stage 4 audit will recompute tier-1 cohort under the source_curated-only gate.

### Decision

Both D1 and D10 stand as resolved per Agent 1's choice. The HANDOFF_LOG entry §6 will be updated accordingly.

### Rationale

D1's downgrade reflects honest semantics: registry data is name-grade belegt, not project-participation belegt.
D10's retrospective recomputation is the whole point of the remediation: produce honest Q1–Q7 numbers.

---

## OD-4 — Apply D8 default (REFAIR Bordeaux as `:Programm`) (2026-05-21)

### Context

Agent 5 R7.b created `p_eth_circular_construction_programme` as `:Programm`. But the HANDOFF_LOG shows only **1 Programm created** vs the brief's expected 7 orphan resolutions. The other 6 were not created.

### Decision

Investigate whether the missing 6 orphan dossiers (Circl Pavilion Amsterdam, Re-Use Höfe Wien, Berlin Schildow Pilot House 2, FCRBE, REBRIDGE, REFAIR Bordeaux) are:

1. Already resolved by an earlier ingestion (Projekt exists with a different slug).
2. Genuinely unmatched (Agent 5's loader skipped).

Until investigated, the Stage 4 audit will report this gap. D8 default stands (REFAIR → `:Programm`) but is not yet applied to the live graph.

### Action

Stage 4 audit query will list orphan dossiers still without a matching `:Projekt`/`:Programm`. Future R7.b.v2 closes the gap if needed.

---

## OD-5 — Stage 4 audit prerequisites (2026-05-21)

### Decision

Stage 4 integration audit may proceed once the following flags exist:

- ✅ `agent_1/PHASE_R1_DONE.flag`
- ✅ `agent_2/PHASE_R2_DONE.flag` and `PHASE_R10_DONE.flag`
- 🔲 `agent_3/PHASE_R3_DONE.flag` and `PHASE_R9_DONE.flag` ← **pending Agent 3 runner execution**
- ✅ `agent_4/PHASE_R4_DONE.flag`
- ✅ `agent_5/PHASE_R7_DONE.flag` (composite, orchestrator-issued)
- ✅ `orchestrator_r5/PHASE_R5_DONE.flag`
- 🔲 `agent_1/PHASE_R8_DONE.flag` ← **runs LAST, after R3 + R9**

Once R3, R9, R8 are present, Stage 4 audit runs. See [STAGE_4_PLAN.md](STAGE_4_PLAN.md).

---

## OD-6 — Stage 4 audit shape (2026-05-21)

### Decision

Stage 4 integration audit will produce one master file `FINAL_REVIEW_PLAN_AUDIT.md` modeled on [FINAL_PASS2_AUDIT.md](../intake/runs/2026-05-20_radical_quality_reset/FINAL_PASS2_AUDIT.md), with these key columns:

| Metric | Pre-radical-reset | Post-radical-reset | Post-review-plan (now) |
|---|---:|---:|---:|

Plus the **honest Q1–Q7** results:

- Q1 with `evidence_origin='source_curated'` filter → expect ≈ 0 (was 266 under Repair D).
- Q2 with `evidence_basis='documented'` → expect 0 (was 799 under inference).
- Q3 with `(:Projekt)-[:HAT_KENNWERT]->(:Kennwert {category:'reuse_share'})` → expect ≥ 3 (graph-native).
- Q4 with `:BETEILIGT_AN` only (no `:STUB_PROJECT_LINK`) → likely 1 (RotorDC, unchanged).
- Q5 with `(:ReuseRule)-[:RELEVANT_FOR]->(:Projekt)` graph step → ≥ 5 covered pairs.
- Q6 with new 5-bucket `evidence_origin` distribution.
- Q7 with `:Quelle.text_content` excerpts.

The Stage 4 audit migration + runner are authored in [_neo4j/intake/runs/2026-05-21_review_based_plan/stage_4_integration/](../intake/runs/2026-05-21_review_based_plan/stage_4_integration/) ([open](../intake/runs/2026-05-21_review_based_plan/stage_4_integration/)).

---

**End of ORCHESTRATOR_DECISIONS.md (rev. 2026-05-21).**
