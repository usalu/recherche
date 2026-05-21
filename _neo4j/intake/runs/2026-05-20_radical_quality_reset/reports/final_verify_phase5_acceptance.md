# Final Verifier 12/12 — Phase 5 + Acceptance Queries Q1–Q7

- **Verifier:** Final Verifier 12 of 12 (read-only)
- **Plan:** `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md` §5 + Acceptance Q1–Q7
- **Run dir:** `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\`
- **Database:** `mit-bestand` on `bolt://localhost:7687`
- **Driver:** `neo4j-python 5.28.4`, creds from `E:\recherche\.cursor\mcp.json`
- **Verification time:** 2026-05-21 07:03 UTC (snapshot taken live; nothing written to the graph)
- **Artifacts:**
  - Live JSON dump: `logs/final_verify_phase5.json`
  - Verifier script: `logs/final_verify_phase5.py`
  - Diagnostic script (p_circle_house tier): `logs/final_verify_phase5_circle_house.py`

## 0. Executive verdict

**Phase 5 — PASS (7 of 8 sub-gates green; 1 deviation documented below).**
**Acceptance Q1–Q7 — 6 of 7 PASS, Q1 FAIL_DOCUMENTED** (known Phase 4b residual `HAT_BAUTEILGRUPPE.evidence_origin` gap, traced in `FINAL_PLAN_COMPLETION_AUDIT.md` §5.1; topology behind Q1 is fully present, evidence flag is the single missing column).

The single Phase 5 deviation: `p_circle_house` lives as `:Projekt` (as required) but with `quality_tier='tier_2_documentation_only'`, not `'tier_3_stub'`. The migration `mig_5_1_quality_tier.cypher` applied its plan-§5.1 formula deterministically; the project carries 2 of the 5 sub-criteria (`has_land`, `has_metric`) which lands it in Tier 2 per the formula. The plan's §5.3 *narrative* assumed Tier 3 for this id; the §5.1 *formula* says Tier 2. The formula and migration are internally consistent.

## 1. Phase 5 checks (8 items)

| # | Check | Expected | Live | Verdict |
|---|---|---|---|---|
| 1 | `migrations/mig_5_1_quality_tier.cypher` exists | file present | present (4 831 B) | **PASS** |
| 2 | `migrations/mig_5_3_relabel_programme.cypher` exists | file present | present (2 022 B) | **PASS** |
| 3 | `PHASE_5_DONE.flag` present | file present | present (6 398 B) | **PASS** |
| 4 | `reports/FINAL_PLAN_COMPLETION_AUDIT.md` exists | file present | present (19 711 B) | **PASS** |
| 5 | All Projekt have `quality_tier` | `count(:Projekt)` = `count(:Projekt WHERE quality_tier IS NOT NULL)` | 101 == 101 | **PASS** |
| 6 | Tier distribution thresholds | tier_1 ≥ 8, tier_2 ≥ 50, tier_3 ≥ 10 | 11 / 68 / 22 | **PASS** (matches plan target of ~11 / ~68 / ~22) |
| 7 | 4 relabelled programmes | count = 4 with `migration_origin='5_3_relabel_to_programm'` | 4 | **PASS** |
| 8 | `p_circle_house` still `:Projekt` with `quality_tier='tier_3_stub'` | label=Projekt, tier=tier_3_stub | label=Projekt, tier=tier_2_documentation_only | **DEVIATION** (see §1.1) |

### 1.1 Deviation — `p_circle_house` lives in Tier 2

Live sub-criteria for `p_circle_house` (from the property bag set by `mig_5_1_quality_tier.cypher`):

| Sub-criterion | Value |
|---|---|
| `quality_tier_has_year` | `false` |
| `quality_tier_has_land` | `true` |
| `quality_tier_has_components` | `false` |
| `quality_tier_has_metric` | `true` |
| `quality_tier_has_evidence` | `false` |
| Truthy count | **2 of 5** |
| Plan §5.1 formula → tier | **`tier_2_documentation_only`** (criterion: any ≥ 2) |

The plan's §5.1 formula (lines 1384-1388) deterministically assigns Tier 2 when 2 of the 5 sub-criteria are met. The §5.3 narrative said "Keep as :Projekt with quality_tier='tier_3_stub'" but did not write that override into the migration — and Phase 5.3's job (`mig_5_3_relabel_programme.cypher`) is only to relabel the other 4 ids, never to override the tier. The migration therefore matches plan §5.1; the §5.3 narrative was optimistic about how few criteria the project would satisfy.

This is *not* a Phase 5 implementation failure. It is a discrepancy between the plan's narrative (§5.3) and the plan's executable formula (§5.1). The verifier task statement quoted the §5.3 narrative. The migration ran exactly the §5.1 rule.

### 1.2 Relabel detail (all 5 affected ids, audit query from `mig_5_3_relabel_programme.cypher`)

| `id` | `labels` | `quality_tier` | `original_label` | `migration_origin` |
|---|---|---|---|---|
| `p_architecture_of_reuse_brussels` | `[Programm]` | `tier_3_stub` | `Projekt` | `5_3_relabel_to_programm` |
| `p_circle_house` | `[Projekt]` | `tier_2_documentation_only` | *null* | *null* |
| `p_reuse_in_construction_zhaw` | `[Programm]` | `tier_3_stub` | `Projekt` | `5_3_relabel_to_programm` |
| `p_reuse_logistics` | `[Programm]` | `tier_3_stub` | `Projekt` | `5_3_relabel_to_programm` |
| `p_vandkunsten_component_reuse` | `[Programm]` | `tier_3_stub` | `Projekt` | `5_3_relabel_to_programm` |

The 4 relabelled ids all carry `:Programm`, `original_label='Projekt'`, and `migration_origin='5_3_relabel_to_programm'`. `p_circle_house` retains `:Projekt` (correctly) with no migration marker (correctly, since 5.3 didn't touch it).

## 2. Acceptance queries Q1–Q7

All 7 plan acceptance queries ran in read-only sessions against `mit-bestand`. Results below are the raw row counts plus the verdict per the task spec ("PASS = returns ≥ 1 row OR is documented as expected-empty").

| Q | Subject | Live result | Verdict | Note |
|---|---|---|---|---|
| Q1 | Reuse Story (FROM_DONOR → BG → INTO_RECEIVER, curated HAT_BAUTEILGRUPPE) | **0** canonical rows; 266 rows on the topology-only variant; 254 Bauteilgruppen carry both `FROM_DONOR` and `INTO_RECEIVER`; 0 `HAT_BAUTEILGRUPPE` edges with `evidence_origin='curated'` | **FAIL_DOCUMENTED** | Documented residual in `FINAL_PLAN_COMPLETION_AUDIT.md` §5.1 (Phase 4b loader gap, out of Phase 5 scope; closeable by a single follow-up migration `mig_4b_4_hat_bg_promotion.cypher`). |
| Q2 | Risk Story — `MATCH (bg:Bauteilgruppe)-[r:HAS_RISK_POLLUTANT]->(s:Schadstoff) RETURN count(*)` | **799** | **PASS** | ≥ 700 threshold met. |
| Q3 | Comparison — `MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'}) UNWIND p.reuse_share_facts AS rs RETURN count(*)` | **4** | **PASS** | Non-empty; 4 entries across 3 Tier-1 projects (Maison Vignette, Lycée Michel Lucius, K.118 Winterthur per the Agent 12 sample). |
| Q4 | Actor Network (≥ 2 Tier-1 projects per Akteur) | **1** | **PASS** | Plan and verifier task explicitly permit 0 ("may be 0 if only 11 tier-1 projects"). 1 actor (`rotordc`) qualifies. With Tier 1+2 the cohort grows to 49 actors at c≥2 (documented in `FINAL_PLAN_COMPLETION_AUDIT.md` §4). |
| Q5 | Decision Support — `MATCH (rule:ReuseRule)-[:APPLIES_IN]->(:Land), (rule)-[:APPLIES_TO]->(:Material) RETURN count(rule)` | **20** | **PASS** | Exactly 20, matches plan target. |
| Q6 | Trust check — `MATCH (p:Projekt)-[r]-() RETURN r.evidence_origin, count(*)` | 3 rows: `derived = 3 205`, `curated = 2 939`, `inferred = 342` (aggregate across all 101 projects). Per-project (`p_chiro_d_itterbeek_dilbeek`): `curated = 153`, `derived = 55`, `inferred = 7` | **PASS** | All three origin categories return non-zero counts; tri-state evidence taxonomy is intact. |
| Q7 | Source drill-down — `MATCH (qmd:Quelle {quelltyp:'case_markdown'})-[:ZITIERT_QUELLE]->(ext:Quelle) RETURN count(ext)` | **958** | **PASS** | ≥ 500 threshold met. |

### 2.1 Q1 — re-verified per task instruction

The task asked to "re-verify" Q1 since the prior audit reported it as the single failure.

| Probe | Live count |
|---|---:|
| Bauteilgruppen with both a `FROM_DONOR` and an `INTO_RECEIVER` edge | **254** |
| Donor→BG→Receiver path rows joined with `HAT_BAUTEILGRUPPE` (any evidence_origin) | **266** |
| Donor→BG→Receiver path rows joined with `HAT_BAUTEILGRUPPE WHERE evidence_origin='curated'` | **0** |
| Total `HAT_BAUTEILGRUPPE` edges | 369 |
| Total `HAT_BAUTEILGRUPPE` edges with `evidence_origin='curated'` | **0** |

Diagnosis confirms `FINAL_PLAN_COMPLETION_AUDIT.md` §5.1: the topology that Q1 *walks* is present in full (254 BG carry both edges, 266 join rows exist), but the *evidence filter* `r.evidence_origin='curated'` cannot match anything because Phase 4b never promoted `HAT_BAUTEILGRUPPE.evidence_origin`. The remediation migration is documented in the audit (single statement, ~250 edges to be promoted; out of Phase 5 scope).

### 2.2 Q3, Q4 — row counts documented for transparency

The task spec said Q3 row count may be 0 (since no Tier-1 Projekt is *required* to carry `reuse_share_facts`); the live answer is 4. The task spec said Q4 may be 0 (since only 11 Tier-1 projects exist); the live answer is 1. Both queries return ≥ 1 row, so both pass under the verifier's "PASS = returns ≥ 1 row OR is documented as expected-empty" rule.

## 3. Final gate matrix

| Gate | Status |
|---|---|
| **Phase 5 file artifacts (4 files)** | 4/4 PASS |
| **Phase 5 live data — tier assignment** | 101/101 Projekt tiered |
| **Phase 5 live data — tier distribution** | tier_1=11, tier_2=68, tier_3=22 (all thresholds met) |
| **Phase 5 live data — 4 relabelled to :Programm** | 4/4 PASS |
| **Phase 5 live data — `p_circle_house` still :Projekt** | PASS |
| **Phase 5 live data — `p_circle_house` tier** | DEVIATION (Tier 2 not Tier 3; mig_5_1 formula-consistent) |
| **Acceptance Q1** | FAIL_DOCUMENTED (Phase 4b residual; topology intact) |
| **Acceptance Q2** | PASS (799 rows) |
| **Acceptance Q3** | PASS (4 rows) |
| **Acceptance Q4** | PASS (1 row; ≥0 permitted) |
| **Acceptance Q5** | PASS (20 rules) |
| **Acceptance Q6** | PASS (3 origin categories live) |
| **Acceptance Q7** | PASS (958 rows) |

**Net:** Phase 5 is complete and consistent with its own migrations. 6 of 7 acceptance queries pass live; the 1 failure (Q1) is a Phase 4b loader residual, fully documented and pre-flagged in the FINAL_PLAN_COMPLETION_AUDIT, not a Phase 5 defect.

## 4. JSON return

```json
{
  "phase_5_checks": {
    "file_artifacts": {
      "mig_5_1_quality_tier_exists": true,
      "mig_5_3_relabel_programme_exists": true,
      "phase_5_done_flag_exists": true,
      "final_plan_completion_audit_exists": true
    },
    "all_projekt_tiered": {"projekt_total": 101, "projekt_with_quality_tier": 101, "passed": true},
    "tier_distribution": {"tier_1": 11, "tier_2": 68, "tier_3": 22, "passed": true},
    "relabelled_to_programm": {"want": 4, "got": 4, "passed": true},
    "p_circle_house": {
      "labels": ["Projekt"],
      "quality_tier": "tier_2_documentation_only",
      "task_expected_tier": "tier_3_stub",
      "deviation": "tier_2 not tier_3 — formula-consistent (2 of 5 sub-criteria met); plan §5.3 narrative was looser than plan §5.1 formula",
      "passed_label_check": true,
      "passed_tier_check": false
    }
  },
  "acceptance_queries": {
    "Q1_reuse_story":          {"row_count": 0,   "verdict": "FAIL_DOCUMENTED",
                                "topology_only_rows": 266, "bg_with_donor_and_receiver": 254,
                                "hat_bauteilgruppe_curated": 0,
                                "note": "Phase 4b residual; documented in FINAL_PLAN_COMPLETION_AUDIT §5.1"},
    "Q2_risk_story":           {"row_count": 799, "verdict": "PASS"},
    "Q3_comparison":           {"row_count": 4,   "verdict": "PASS"},
    "Q4_actor_network":        {"row_count": 1,   "verdict": "PASS",
                                "note": "permitted to be 0; 1 actor (rotordc) qualifies"},
    "Q5_decision_support":     {"row_count": 20,  "verdict": "PASS"},
    "Q6_trust_check": {
      "aggregate_rows":  [{"origin":"derived","c":3205},{"origin":"curated","c":2939},{"origin":"inferred","c":342}],
      "per_project_rows":[{"origin":"curated","c":153},{"origin":"derived","c":55},{"origin":"inferred","c":7}],
      "verdict": "PASS"
    },
    "Q7_source_drilldown":     {"row_count": 958, "verdict": "PASS"}
  },
  "overall_verdict": "PASS_WITH_DOCUMENTED_RESIDUAL"
}
```
