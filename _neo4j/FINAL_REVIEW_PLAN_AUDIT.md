# FINAL — Review-based remediation audit (Stage 4)

- **Audit run:** 2026-05-21T13:30:24.441988+00:00
- **Database:** mit-bestand
- **Plan:** [_neo4j/REVIEW_BASED_PLAN/](REVIEW_BASED_PLAN/ORCHESTRATION.md)
- **Supersedes:** [FINAL_PASS2_AUDIT.md](intake/runs/2026-05-20_radical_quality_reset/FINAL_PASS2_AUDIT.md)
- **Verdict:** _<set after manual review>_

## 0. Headline

| Metric | Pre-radical-reset (2026-05-20) | Post-radical-reset (2026-05-21 audit) | Post-review-plan (now) |
|---|---:|---:|---:|
| Total nodes | 2,580 | 3,802 | **5546** |
| Total relationships | 19,989 | 25,023 | **27044** |

## 1. Honest Q1–Q7

### Q1 — Reuse Story

| Filter | Row count | Honesty |
|---|---:|---|
| `evidence_origin='source_curated'` only | — | Honest signal |
| `evidence_origin='topology_synthesized'` only | — | What Repair D produced |
| Combined | — | Pre-honesty Q1 baseline |

### Q2 — Risk Story

| Basis | Row count |
|---|---:|
| `documented` (curated cell citation) | — |
| `era_and_material` inference | — |
| `material_only` inference | — |
| `REQUIRES_VERIFICATION_FOR` total | 347 |

### Q3 — Comparison (graph-native via :Kennwert)

Tier-1 projects with `reuse_share` Kennwert: **—**

(See `stage_4_audit_results.json` for the full per-project Kennwert dump.)

### Q4 — Actor Network

| Filter | Count |
|---|---:|
| BETEILIGT_AN only (honest) | — |
| BETEILIGT_AN ∪ STUB_PROJECT_LINK | — |

### Q5 — Decision Support (graph-native :RELEVANT_FOR)

| Probe | Count |
|---|---:|
| Total `:RELEVANT_FOR` edges | — |
| Ferme du Rail rules (must be 0 — FR uncovered) | — |
| Holbein Gardens rules (must be ≥ 1) | — |

### Q6 — Trust check (5-bucket distribution)

See `stage_4_audit_results.json` for the full distribution; bookkeeping count: **—** edges flagged separately.

### Q7 — Source drill-down

| Probe | Count |
|---|---:|
| case_markdown → external (ZITIERT_QUELLE) | — |
| case_markdown with `text_content` populated | — |

## 2. Cross-agent invariants

| Invariant | Violations |
|---|---:|
| C1 origin enum violation | — |
| C2 old 'curated' value remaining | — |
| C3 'bookkeeping' in confidence enum | — |
| C4 source_curated without excerpt | — |
| C5 :Bauteilgruppe without bg_kind | — |
| C6 :Bauteilgruppe category with topology | — |
| C7 :Projekt with BG paths but no :HAS_BAUWERK | — |
| C8 :ASSOZIIERT_MIT_PROJEKT remaining (must be 0 post-R9) | — |
| C9 :Kennwert orphan | — |

## 3. Restored / new labels

(See `stage_4_audit_results.json` for the per-label counts.)

## 4. Decision-grade cohort

| Cohort | Count |
|---|---:|
| Tier 1 under legacy gate (Repair D promotions counted) | — |
| Tier 1 under honest gate (`source_curated` only) | — |

**The drop is the success signal.** Recommend re-running tier computation with the honest gate as the only gate.

## 5. :DataIssue summary

Total `:DataIssue` count: **1454**

(See `stage_4_audit_results.json` for the breakdown by kind, severity, and per-project density.)

## 6. Open follow-ups

- R7.c deferred (see [REVIEW_BASED_PLAN/ORCHESTRATOR_DECISIONS.md](REVIEW_BASED_PLAN/ORCHESTRATOR_DECISIONS.md) OD-2).
- 6 of 7 R7.b orphan-dossier resolutions still pending (OD-4).
- R6 schema language unification not in this round.

## 7. Sign-off

This audit was generated automatically from `stage_4_audit_queries.cypher` against the live `mit-bestand` database. Validate against [HANDOFF_LOG.md](REVIEW_BASED_PLAN/HANDOFF_LOG.md) before accepting.
