# STATUS — Quelle remediation (6-agent run)

> Single-page state dashboard. Last sweep: **2026-05-21 (planning)**. **State: PLANNED — ready for execution.**

---

## Phase board

| # | Phase | Owner | State | Flag |
|:-:|---|---|:-:|---|
| S1 | URL extractor | agent_s1 | 🔲 STAGED | `PHASE_S1_DONE.flag` |
| S2 | URL prober (HTTP + Wayback) | agent_s2 | 🔲 STAGED | `PHASE_S2_DONE.flag` |
| S3 | Content verifier (3-tier match) | agent_s3 | 🔲 STAGED | `PHASE_S3_DONE.flag` |
| S4 | Schema cleanup (labels + strip + FU-8) | agent_s4 | 🔲 STAGED | `PHASE_S4_DONE.flag` |
| S5 | Visibility surfacing | agent_s5 | 🔲 STAGED | `PHASE_S5_DONE.flag` |
| S6 | Audit + sign-off | agent_s6 | 🔲 STAGED | `STAGE_S6_AUDIT_DONE.flag` |

---

## Sequencing

```
S1 → S2 → S3 → S5 → S6
 │              ▲
 └─→ S4 ────────┘    (S4 parallel-safe)
```

Hard prerequisites enforced by each agent's runner.

---

## What's new vs. the legacy Q1–Q5 plan

| Aspect | Q1–Q5 (legacy) | S1–S6 (this run) |
|---|---|---|
| Discover every URL | Q1 | **S1** (same scope; now first-class agent) |
| Check if URL is alive | not done | **S2** (HTTP probe + Wayback) |
| Check if URL contains the claim | not done | **S3** (3-tier match) |
| Schema cleanup | Q2 + Q3 | **S4** (same + FU-8 retry) |
| Visibility | Q4 | **S5** (same + quality + freshness + trust score) |
| Audit | absent | **S6** (cross-cutting + CI gate) |

**The whole point of the 6-agent revision is S2 + S3** — chase the URL, double-check the content.

---

## Documents

| Topic | Where |
|---|---|
| Master plan | [../QUELLE_REMEDIATION_PLAN.md](../QUELLE_REMEDIATION_PLAN.md) |
| Index / agent map | [README.md](README.md) |
| Orchestration playbook | [ORCHESTRATION.md](ORCHESTRATION.md) |
| Handoff log | [HANDOFF_LOG.md](HANDOFF_LOG.md) |
| Decisions log | [HANDOFF_LOG.md §9](HANDOFF_LOG.md) (in-place) |
| This dashboard | [STATUS.md](STATUS.md) |
| Final audit (post-S6) | `_neo4j/FINAL_QUELLE_AUDIT.md` (will exist after S6 PASS) |

---

## Decisions to make before any agent runs

See [QUELLE_REMEDIATION_PLAN.md §10](../QUELLE_REMEDIATION_PLAN.md). 12 decisions (QD-1 to QD-12); all have sensible defaults. The user should redline any they want to change before agents start.

---

## What success looks like

Final state, after S6 PASS:

| Indicator | Expected |
|---|---|
| `:Dossier.text_content` non-null | **0** |
| `:ExternalLink.url_status='unchecked'` | **0** |
| Citations with `verification_status='unchecked'` | **0** |
| Projekt with `source_urls` array | **101** (all of them) |
| Projekt with `source_trust_score` (any value) | **100** (one stub has no sources) |
| Tier-1 projects with `source_trust_score ≥ 0.7` | **≥ 5** (honest signal) |
| `:DataIssue` count by kind | populated; backlog visible at graph level |
| `_neo4j/FINAL_QUELLE_AUDIT.md` | written |
| `_scripts/validate_no_text_content.py` | installed; CI gate active |

---

**End of STATUS.md.**
