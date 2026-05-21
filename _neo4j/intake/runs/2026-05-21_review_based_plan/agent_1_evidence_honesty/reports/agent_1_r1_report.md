# Agent 1 R1 Report — Evidence Origin Split + Bookkeeping Flag

**Agent:** agent_1_evidence_honesty  
**Phase:** R1  
**Date:** 2026-05-21  
**Status:** PASS  

---

## §1 Pre-flight state

| Metric | Value |
|---|---|
| Total relationships | 25,023 |
| Total nodes | 3,802 |

### evidence_origin distribution (before R1)

| Value | Count | % |
|---|---|---|
| `derived` | 18,483* | 73.9 % |
| `curated` | 4,748* | 19.0 % |
| `inferred` | 1,523 | 6.1 % |
| `source_curated` | 2,803 | — |
| `registry_derived` | 1,669 | — |
| `topology_synthesized` | 276 | — |
| `external_unfolded` | 269 | — |

> *Note: The migration ran in three passes (due to semicolon-in-literal fixes). At the start of the final pass, R1.a–R1.g had already been applied from the first two passes, leaving `derived=18,483` and some new-enum values already present.

### evidence_confidence distribution (before R1, final-pass start)

| Value | Count |
|---|---|
| `unklar` | 19,462 |
| `teilweise_belegt` | 2,323 |
| `belegt` | 1,848 |
| `inferiert` | 1,390 |

---

## §2 Migration steps executed

| Step | Description | Edges affected |
|---|---|---|
| R1.a | `curated` + `mig_repair_4_1_q1` → `topology_synthesized` | 254 |
| R1.b | `curated` + `mig_repair_4_1_excerpts` → `registry_derived` | ~1,669 total |
| R1.c | Akteur BELEGT_IN `q_actor_*` → `registry_derived` | 4 |
| R1.d | `mig_repair_4_1_unpack` → `topology_synthesized` | 22 |
| R1.e | `ZITIERT_QUELLE` with `external_sources_array` basis → `external_unfolded` | 269 |
| R1.f | All remaining `curated` → `source_curated` | 2,803 |
| R1.g | `evidence_confidence='bookkeeping'` → `unklar` + `is_bookkeeping=true` | 1,022 |
| R1.h | ReuseRule `inferred+belegt` → `teilweise_belegt` | 133 edges + nodes |
| R1.i | `registry_derived` `belegt` → `teilweise_belegt` (D10 default) | 1,530 |
| R1.j | remaining `derived` `registry_stub` → `registry_derived` | 58 |
| R1.j (catch-all) | all remaining `derived` → `topology_synthesized` | 18,425 |

---

## §3 Post-flight state

### evidence_origin distribution (after R1)

| Value | Count |
|---|---|
| `topology_synthesized` | 18,701 |
| `source_curated` | 2,803 |
| `registry_derived` | 1,727 |
| `inferred` | 1,523 |
| `external_unfolded` | 269 |
| **Total with origin** | **25,023** |
| `derived` | **0** ✓ |
| `curated` | **0** ✓ |

### evidence_confidence distribution (after R1)

| Value | Count |
|---|---|
| `unklar` | 19,462 |
| `teilweise_belegt` | 2,323 |
| `belegt` | 1,848 |
| `inferiert` | 1,390 |
| `bookkeeping` | **0** ✓ |

### is_bookkeeping flag

| Property | Count |
|---|---|
| `is_bookkeeping = true` | 1,022 |

> Note: The brief estimated 703 `ANCHORED_BY` edges, but the actual count of edges with `evidence_confidence='bookkeeping'` was 1,022. All 1,022 are now flagged `is_bookkeeping=true` with `evidence_confidence='unklar'`. The difference (319 extra) may reflect edges from other relationship types or additional bookkeeping-confidence writes since the baseline estimate.

---

## §4 Acceptance gate results

| Gate | Condition | Result |
|---|---|---|
| `old_curated_remaining` | violations = 0 | **PASS** (0) |
| `bookkeeping_in_confidence` | violations = 0 | **PASS** (0) |
| `origin_enum_violation` | violations = 0 | **PASS** (0) |
| `confidence_enum_violation` | violations = 0 | **PASS** (0) |
| `is_bookkeeping_count` | c ≥ 698 | **PASS** (1022) |
| `topology_synthesized_count` | c ≥ 254 | **PASS** (18701) |
| `registry_derived_count` | c ≥ 1500 | **PASS** (1727) |
| `reuse_rule_contradiction` | violations = 0 | **PASS** (0) |

**All 8 gates: PASS**

---

## §5 Open decisions taken

**D10 (registry_derived confidence):** Applied conservative default — downgraded `registry_derived` edges with `evidence_confidence='belegt'` to `teilweise_belegt`. Registry data is name-level belegt, not project-participation belegt. Approximately 1,530 edges downgraded.

**D_derived_mapping (unlisted in brief):** The brief did not include an explicit step for reclassifying the 18,483 `derived` edges, but `derived` is not in the new 5-value enum. Resolution: `registry_stub` basis → `registry_derived` (58 edges); all remaining `derived` → `topology_synthesized` (18,425 edges). This is the conservative default since these were all programmatically generated. All edges retain their `evidence_basis` property for auditing purposes.

---

## §6 R8 readiness

Phase R8 (`:DataIssue` seed) is **waiting on Stage 3** completion per the orchestration dependency chain. R8 must not run until the orchestrator confirms Stages 1–3 complete in `HANDOFF_LOG.md`.

The migration file `mig_r8_data_issue_seed.cypher` is ready at:
`_neo4j/intake/runs/2026-05-21_review_based_plan/agent_1_evidence_honesty/migrations/mig_r8_data_issue_seed.cypher`

---

## §7 Artifacts

| File | Description |
|---|---|
| `migrations/mig_r1_evidence_origin_split.cypher` | R1 migration (idempotent) |
| `migrations/mig_r8_data_issue_seed.cypher` | R8 migration (staged, not yet run) |
| `logs/agent_1_runner.py` | Runner script |
| `logs/r1_probe_pre.json` | Pre-flight probe data |
| `logs/r1_probe_post.json` | Post-flight probe data |
| `logs/r1_audit.jsonl` | Per-statement execution log |
| `logs/r1_gates.json` | Acceptance gate results |
| `PHASE_R1_DONE.flag` | Done flag with full metadata |
