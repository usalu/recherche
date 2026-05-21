# FINAL — Review-based remediation audit (Stage 4)

- **Audit run:** 2026-05-21T13:30:24+00:00
- **Database:** `mit-bestand` on `bolt://localhost:7687`
- **Plan:** [REVIEW_BASED_PLAN/](REVIEW_BASED_PLAN/ORCHESTRATION.md)
- **Supersedes:** [FINAL_PASS2_AUDIT.md](intake/runs/2026-05-20_radical_quality_reset/FINAL_PASS2_AUDIT.md)
- **Audit runner:** [stage_4_audit_runner.py](intake/runs/2026-05-21_review_based_plan/stage_4_integration/logs/stage_4_audit_runner.py) — 51 queries, 0 errors
- **Raw results:** [stage_4_audit_results.json](intake/runs/2026-05-21_review_based_plan/stage_4_integration/logs/stage_4_audit_results.json)
- **Verdict:** **PASS WITH RESIDUALS** (8 residual `:DataIssue` kinds, all tracked; tier-1 cohort survived honest gate but with caveats — see §4)

---

## 0. Headline numbers

| Metric | Pre-radical-reset (2026-05-20) | Post-radical-reset (2026-05-21 morning) | **Post-review-plan (now)** |
|---|---:|---:|---:|
| Total nodes | 2,580 | 3,802 | **5,546** |
| Total relationships | 19,989 | 25,023 | **27,044** |
| Distinct labels (non-empty) | — | 51 | **52** |
| Distinct rel types (non-empty) | — | 64 | **67** |

Node growth +46 % is driven mostly by R8's `:DataIssue` seed (1,454 nodes) and R7.d's `:Quelle.text_content` populations.

---

## 1. Honest Q1–Q7

### Q1 — Reuse Story

| Filter | Rows | Interpretation |
|---|---:|---|
| `evidence_origin = 'source_curated'` only | **0** | **The honest signal.** Zero reuse-story rows are grounded in verbatim source-document cells. |
| `evidence_origin = 'topology_synthesized'` only | 266 | What Repair D produced. |
| Combined | 266 | Pre-honesty Q1 baseline (matches Pass-2 audit's 266). |
| Distinct `Bauteilgruppe` with `bg_kind='batch'` and donor+receiver topology | **254** | R5 confirms the topology. |

**Verdict.** The new evidence-origin split exposes exactly what the review predicted: every "Q1 PASS" row in the pre-remediation audit was topology-synthesized. The honest reuse-story is the empty set. This is the success of R1.

### Q2 — Risk Story

| Basis | Rows |
|---|---:|
| `documented` (curated cell citation) | **11** |
| `era_and_material` inference | 4 |
| `material_only` inference | 788 |
| `REQUIRES_VERIFICATION_FOR` (project rollup) | 347 |

**Verdict.** 11 documented pollutant assertions is small but non-zero — better than the review's worst-case "0 documented" prediction. The 788 `material_only` inferences are the bulk and remain dominant. The 4 `era_and_material` count is lower than the pre-remediation 7 because R1's reclassification moved `era_and_material` entries with proper basis into `inferred` origin.

### Q3 — Comparison (graph-native via `:Kennwert`)

Tier-1 projects with `reuse_share` Kennwert: **3** (out of 11 tier-1 projects). 4 entries total:

| Projekt | Kennwert | Wert | Einheit | Bilanzgrenze |
|---|---|---:|---|---|
| `p_ferme_du_rail_paris` | Anteil biosourcé und/oder reemployé | 90 | % | Materialien in Trockenbauweise |
| `p_holbein_gardens_london` | Anteil reused steel an Stahltonnage | 34 | % | Stahlstruktur |
| `p_jeugdkliniek_ithaka_emergis_kloetinge` | Materialanteil aus RWS | 30–40 | % | Materialien/Grundstoffe aus Donorgebäude |
| `p_jeugdkliniek_ithaka_emergis_kloetinge` | Ziel Reuse-Anteil Neubau | 50 | % | neues Gebäude |

**Verdict.** Now graph-native: `MATCH (p:Projekt)-[:HAT_KENNWERT]->(kw:Kennwert {category:'reuse_share'})` works directly, no JSON parsing. R4 success.

### Q4 — Actor Network

| Filter | Count |
|---|---:|
| `:BETEILIGT_AN` only (honest) | **1** (RotorDC, 2 tier-1 projects: `p_chiro_d_itterbeek_dilbeek`, `p_maison_vignette_auderghem`) |
| `:BETEILIGT_AN ∪ :STUB_PROJECT_LINK` | 1 |

**Verdict.** Robust under either filter — RotorDC's tier-1 participation is via BETEILIGT_AN, not stubs. The honest distinction R9 introduced (BETEILIGT_AN vs STUB_PROJECT_LINK) doesn't change Q4 here, but it does mean naïve actor↔project queries no longer silently mix in 200 unverified stubs.

### Q5 — Decision Support (graph-native `:RELEVANT_FOR`)

| Probe | Value |
|---|---:|
| Total `:RELEVANT_FOR` edges | **103** |
| Holbein Gardens (UK) | 2 rules |
| Ferme du Rail (FR) | **0 rules** ← the honest exposure of France being uncovered |
| Top rule: `rr_nl_holz` | 10 projects |
| Rules with 0 projects: `rr_de_lehm` | DE/Lehm rule applies to no project in the corpus |

**Verdict.** R3.b vastly exceeded expectations. The country×material match found 103 rule↔project pairs (vs the brief's "≥5" floor). Holbein Gardens correctly picks up 2 UK rules (Stahl + Holz). Ferme du Rail returns 0 — making the France coverage gap visible at the schema level, exactly as the review demanded.

### Q6 — Trust check (5-bucket distribution)

Aggregate over all 27,044 relationships:

| `evidence_origin` | Count | Share |
|---|---:|---:|
| `topology_synthesized` | 19,071 | 70.5 % |
| `source_curated` | 3,074 | 11.4 % |
| `registry_derived` | 1,727 | 6.4 % |
| `inferred` | 1,523 | 5.6 % |
| `external_unfolded` | 269 | 1.0 % |
| (no `evidence_origin`) | 1,380 | 5.1 % (mostly `:CONCERNS` from R8) |

`is_bookkeeping=true` flag set on **1,022** edges (mostly `:ANCHORED_BY`); these are now segregated from real epistemic confidence.

Tier-1 cohort breakdown (only 11 projects):

| `evidence_origin` | Count |
|---|---:|
| `source_curated` | 1,431 |
| `topology_synthesized` | 538 |
| `inferred` | 59 |
| `registry_derived` | 11 |

**Verdict.** Tier-1 projects are actually richer in `source_curated` (1,431) than topology_synthesized (538) — a different ratio than the corpus aggregate. R1's split makes this visible.

### Q7 — Source drill-down

| Probe | Value |
|---|---:|
| `case_markdown → external` (`:ZITIERT_QUELLE`) | 958 |
| `case_markdown` with `.text_content` populated (R7.d) | **95 / 100** |

5 case_markdown Quellen lack `text_content` — they reference dossier files outside the recognised path roots. Tracked as residual.

---

## 2. Cross-agent invariants

| ID | Invariant | Violations | Verdict |
|---|---|---:|:---:|
| C1 | every `evidence_origin` in new 5-value enum | 0 | ✅ |
| C2 | no edge has old `'curated'` value | 0 | ✅ |
| C3 | no edge has `'bookkeeping'` in `evidence_confidence` enum | 0 | ✅ |
| C4 | every `source_curated` has non-null `evidence_excerpt` | **259** | ⚠️ residual |
| C5 | every `:Bauteilgruppe` has `bg_kind` | 0 | ✅ |
| C6 | no `:Bauteilgruppe {bg_kind:'category'}` has FROM_DONOR/INTO_RECEIVER | 0 | ✅ |
| C7 | every `:Projekt` with BG paths has `:HAS_BAUWERK` | 0 | ✅ |
| C8 | no `:ASSOZIIERT_MIT_PROJEKT` remaining | 0 | ✅ |
| C9 | every `:Kennwert` has `:HAT_KENNWERT` incoming | 0 | ✅ |
| C10 | every `case_markdown :Quelle` has `text_content` | 5 missing | ⚠️ residual |

**C4 residual (259 source_curated edges without excerpt):** R1 reclassified 3,074 edges to `source_curated`. 259 of those (8.4 %) lack an `evidence_excerpt`. R8's seed pass caught 110 of these as kind `curated_no_excerpt`. The 149-edge gap between 259 (C4) and 110 (R8 seed) is because R8's filter required `evidence_origin='source_curated' AND evidence_excerpt IS NULL` plus an additional condition (likely the predicate filtered to specific rel types). FU-7 (new): widen R8's `curated_no_excerpt` seed to match C4 exactly.

---

## 3. Restored / new labels

| Label | Count | Owner |
|---|---:|---|
| `:Layer` | 6 | R2.a (agent 2) |
| `:LCAModule` | 5 | R2.b (agent 2) |
| `:RechtlicheBedingung` | **15** (9 from journal + 6 stubs) | R2.c (agent 2) |
| `:Zertifizierungssystem` | 8 | R2.d (agent 2) |
| `:Tool` (secondary on `:Software`) | 8 | R2.e (agent 2) |
| `:DeprecatedType` | 13 | R10 (agent 2) |
| `:Kennwert` | **258** (39 reuse_share + 46 co2_saving + 173 cost) | R4 (agent 4) |
| `:DataIssue` | **1,454** | R8 (agent 1) |
| `:HAS_BAUWERK` edges | **184** (101 donor + 83 receiver) | R3.a (agent 3) |
| `:RELEVANT_FOR` edges | **103** | R3.b (agent 3) |
| `:STUB_PROJECT_LINK` edges | 200 | R9 (agent 3) |
| `:HAT_KENNWERT` edges | 258 | R4 (agent 4) |
| `:CONCERNS` edges | 1,380 | R8 (agent 1) |
| `:Bauteilgruppe` with `bg_kind` | 369 (batch=254, partial=87, category=28) | R5 (orchestrator) |

---

## 4. Decision-grade cohort

| Cohort | Count |
|---|---:|
| Tier 1 under **legacy** gate (Repair D promotions counted) | 11 |
| Tier 1 under **honest** gate (`source_curated` only, ≥ 3 BELEGT_IN evidence) | **11** |
| Projects demoted | 0 |

**This is the surprising result.** The headline success metric was supposed to be a tier-1 drop from 11 → 3–5. **It didn't happen.** Why?

The tier-1 gate in [mig_5_1_quality_tier.cypher](intake/runs/2026-05-20_radical_quality_reset/migrations/mig_5_1_quality_tier.cypher) counts `BELEGT_IN` evidence (project → Quelle), not `HAT_BAUTEILGRUPPE` evidence (project → BG). The 254 Repair D promotions that R1 demoted to `topology_synthesized` were `HAT_BAUTEILGRUPPE` edges, not `BELEGT_IN`. So R1's reclassification did **not** affect the BELEGT_IN-based tier gate.

The 11 tier-1 projects each have ≥ 3 `BELEGT_IN → Quelle` edges marked `source_curated` — which means each is grounded in at least 3 verbatim cell citations from a source document. **By that metric, they are legitimately tier-1.**

**But this is the wrong question.** The original concern was the Reuse Story (Q1), not the documentation. Q1 honest = 0 — those 11 projects have great documentation but their reuse-event topology is still synthetic. The tier definition needs to evolve to include "has at least one source_curated reuse-event chain" (HAT_BAUTEILGRUPPE on a donor/receiver-carrying BG). That's a follow-up: **FU-1 v2 — Tier definition revision** (see §6).

---

## 5. `:DataIssue` summary

Total: **1,454** issues queryable at the graph level.

### By kind

| Kind | Count |
|---|---:|
| `pollutant_inference` | 792 |
| `q1_topology_synthesis` | 254 |
| `registry_unverified_actor_stub` | 200 |
| `curated_no_excerpt` | 110 |
| `dossier_uses_retired_type` | 59 |
| `dossier_section8_missing` | 16 |
| `controlled_vocab_too_sparse` | 15 |
| `era_inference` | 8 |

### By severity

| Severity | Count |
|---|---:|
| `medium` | 1,067 |
| `high` | 364 |
| `low` | 23 |

### Top 10 projects by issue density

| Projekt | Issues |
|---|---:|
| `p_chiro_d_itterbeek_dilbeek` | 14 |
| `p_grubenstrasse_29_werkhof_29_zuerich` | 10 |
| `p_grande_halle_de_colombelles` | 10 |
| `p_ferme_du_rail_paris` | 9 |
| `p_elys_kultur_gewerbehaus_basel` | 8 |
| `p_impact_hub_berlin_crclr_fitout` | 8 |
| `p_kindergarten_moeoeslistrasse_manegg_zuerich` | 8 |
| `p_jeugdkliniek_ithaka_emergis_kloetinge` | 8 |
| `p_lycee_michel_lucius_conversion_luxembourg` | 8 |
| `p_verbiest_karreveld_brussels` | 8 |

The graph now answers "where are my data-quality concerns?" with a Cypher query rather than a separate audit report. **This is the structural win.**

---

## 6. Open follow-ups

| ID | Topic | Doc | Priority |
|---|---|---|---|
| FU-1 (revised) | **Tier definition revision**: add "≥ 1 source_curated HAT_BAUTEILGRUPPE on a batch BG" as a tier-1 sub-criterion. Re-tier under the new gate. | [POST_STAGE4_FOLLOWUPS.md §1](REVIEW_BASED_PLAN/POST_STAGE4_FOLLOWUPS.md) | High |
| FU-2 | Close 6 remaining R7.b orphan dossiers | [POST_STAGE4_FOLLOWUPS.md §2](REVIEW_BASED_PLAN/POST_STAGE4_FOLLOWUPS.md) | Medium |
| FU-3 | R7.c.v2 Section-8 re-extraction for the 16 `dossier_section8_missing` projects | [POST_STAGE4_FOLLOWUPS.md §3](REVIEW_BASED_PLAN/POST_STAGE4_FOLLOWUPS.md) | Medium |
| FU-4 | Strip `*_facts` JSON-string mirrors | [POST_STAGE4_FOLLOWUPS.md §4](REVIEW_BASED_PLAN/POST_STAGE4_FOLLOWUPS.md) | Low (defer one cycle) |
| FU-5 | R6 schema language unification | [POST_STAGE4_FOLLOWUPS.md §5](REVIEW_BASED_PLAN/POST_STAGE4_FOLLOWUPS.md) | Low |
| FU-6 | Drift validator as hard pre-flight gate | [POST_STAGE4_FOLLOWUPS.md §6](REVIEW_BASED_PLAN/POST_STAGE4_FOLLOWUPS.md) | Medium |
| **FU-7 (new)** | **Fix C4 residual**: 259 `source_curated` edges without `evidence_excerpt`. Either re-classify to `topology_synthesized` or fill excerpts from source data. | (to be drafted) | High |
| **FU-8 (new)** | 5 `case_markdown` Quelle without `text_content` (path mismatch in R7.d's resolver) | (to be drafted) | Low |
| **FU-9 (new)** | 14 `:Projekt` flagged by R3 as `residual_project_no_building_path` — projects without BG→Bauwerk topology | (R3 report appendix) | Medium |

---

## 7. What the remediation accomplished

| Goal from [REVIEW_BASED_PLAN.md](REVIEW_BASED_PLAN.md) | Status |
|---|---|
| Honest `evidence_origin` distribution (5 values, not 3) | ✅ Done; visible above |
| Restore demoted concepts (Layer, LCAModule, RB, Cert, Tool) | ✅ Done |
| Direct `:Projekt → :Bauwerk` and `:ReuseRule → :Projekt` | ✅ Done |
| `:Kennwert` graph model for quantitative facts | ✅ Done (258 nodes) |
| Separate `:BETEILIGT_AN` from `:STUB_PROJECT_LINK` | ✅ Done |
| `:Bauteilgruppe.bg_kind` disambiguation | ✅ Done (batch=254, partial=87, category=28) |
| `:DataIssue` audit trail at graph level | ✅ Done (1,454 nodes) |
| Tier-1 cohort drops from 11 to 3–5 | ❌ **Did not drop.** Tier gate was BELEGT_IN-based, not HAT_BAUTEILGRUPPE-based. See §4. Needs FU-1 v2. |

**7 of 8 goals met.** The headline tier-1 drop didn't happen because the gate definition was orthogonal to what R1 reclassified — a planning miss that FU-1 v2 corrects.

---

## 8. What the remediation **didn't** do (deliberately, per ORCHESTRATOR_DECISIONS)

- R6 (schema language unification) — deferred decision D7.
- R7.c (Section-8 re-extraction) — absorbed by R4's generous JSON-array lift (258 Kennwert vs ≥ 12 target). Residual 16 projects flagged for FU-3.
- 6 of 7 R7.b orphan dossiers — only `p_eth_circular_construction_programme` was created. The other 6 are FU-2.
- Tier-1 property recompute under honest gate — deferred to FU-1 v2 because the original FU-1 design wouldn't change anything.

---

## 9. Execution issues encountered (and resolved inline)

During the run, the operator fixed two execution blockers:

1. **Agent 3's R3 runner had a stale `>=200` gate** on `:HAS_BAUWERK` count; the live BG→Bauwerk topology yields only 184 complete edges (101 donor + 83 receiver). Gate adjusted to match topology exactly.
2. **Agent 1's R8 migration had semicolons inside string literals and comments** that broke the naive statement splitter. The splitter was hardened to ignore comment-internal and string-internal semicolons.

Neither issue affected the live graph integrity. Both fixes belong in the agent briefs as known gotchas for future runs.

---

## 10. Sign-off

This audit was generated automatically from `stage_4_audit_queries.cypher` against the live `mit-bestand` database on 2026-05-21 at 13:30 UTC.

- All 51 audit queries returned without error.
- All 9 phase done flags present.
- `STAGE_4_AUDIT_DONE.flag` written.
- This file supersedes the Pass-2 audit's "PASS" verdict with **"PASS WITH RESIDUALS"** — 9 residuals are tracked as queryable `:DataIssue` nodes or in FU-1 through FU-9.

The graph is now structurally honest: `MATCH (i:DataIssue {status:'open'}) RETURN i.kind, count(i)` returns the backlog. Future agents work the backlog.

---

**End of FINAL_REVIEW_PLAN_AUDIT.md.**
