# Quelle remediation — 6-agent split

> Find your agent below and read its brief. The master plan is at [_neo4j/QUELLE_REMEDIATION_PLAN.md](../QUELLE_REMEDIATION_PLAN.md).

| If you are… | Read |
|---|---|
| Just landed; want the big picture | [../QUELLE_REMEDIATION_PLAN.md](../QUELLE_REMEDIATION_PLAN.md) |
| **Agent S1** (URL extractor) | [AGENT_S1_url_extractor.md](AGENT_S1_url_extractor.md) |
| **Agent S2** (URL prober — chase URLs) | [AGENT_S2_url_prober.md](AGENT_S2_url_prober.md) |
| **Agent S3** (content verifier — double-check) | [AGENT_S3_content_verifier.md](AGENT_S3_content_verifier.md) |
| **Agent S4** (schema cleanup) | [AGENT_S4_schema_cleanup.md](AGENT_S4_schema_cleanup.md) |
| **Agent S5** (visibility surfacing) | [AGENT_S5_visibility.md](AGENT_S5_visibility.md) |
| **Agent S6** (audit + sign-off) | [AGENT_S6_audit_signoff.md](AGENT_S6_audit_signoff.md) |
| Orchestrator (Claude) — coordination | [ORCHESTRATION.md](ORCHESTRATION.md), [HANDOFF_LOG.md](HANDOFF_LOG.md), [ORCHESTRATOR_DECISIONS.md](ORCHESTRATOR_DECISIONS.md) |
| Current state at a glance | [STATUS.md](STATUS.md) |

## Quick map of phases

| Agent | Phase ID | What it produces |
|---|---|---|
| S1 | Discovery | `:Quelle :ExternalLink` nodes for every URL in the graph, with `url_origin` tag |
| S2 | Reachability | `url_status`, `url_http_code`, redirect chain, body cache, Wayback fallback |
| S3 | Content verification | `verification_status` on every citation edge (verbatim / paraphrase / no_match / dead / unchecked) |
| S4 | Schema cleanup | Secondary labels (`:Dossier`, `:ExternalLink`, …); strip `text_content` |
| S5 | Visibility | `source_urls`, `source_quality_summary`, `source_freshness_summary`, `source_trust_score` on Projekt/Bauwerk/Akteur |
| S6 | Audit | `FINAL_QUELLE_AUDIT.md` + `:DataIssue` seeding |

## Dependency at a glance

```
S1 ─┬──► S2 ──► S3 ──► S5 ──► S6
    │                    ▲
    └──► S4 ─────────────┘
```

S4 is parallel-safe with S2 and S3.
S5 reads from S2 (`url_status`) and S3 (`verification_status`).
S6 runs last, after everything else.

## File layout under `_neo4j/intake/runs/2026-05-21_quelle_remediation/`

```
agent_s1_url_extractor/       ← S1 artefacts (already partially populated by legacy Q1)
agent_s2_url_prober/          ← S2 artefacts (NEW in this revision)
agent_s3_content_verifier/    ← S3 artefacts (NEW)
agent_s4_schema_cleanup/      ← S4 artefacts (was Q2 + Q3 + FU-8)
agent_s5_visibility/          ← S5 artefacts (was Q4, extended)
agent_s6_audit_signoff/       ← S6 artefacts (NEW)
shared/                       ← shared body cache (S2 → S3), schemas, helpers
```

Each agent writes its own migrations, runner, logs, and reports under its own subdirectory. The orchestrator merges the artefacts at sign-off.
