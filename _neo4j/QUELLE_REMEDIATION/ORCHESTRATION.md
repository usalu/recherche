# Quelle remediation — orchestration

**Read this first if you're an agent landing cold.**

You are one of six agents (S1–S6) executing a coordinated source-traceability remediation on `mit-bestand`. The orchestrator (Claude) sequences your work and merges branches.

---

## §1 Roles

| Agent | Branch prefix | Owns these phases |
|---|---|---|
| **Orchestrator (Claude)** | `orch/quelle-integrate` | Sequencing, conflict resolution, sign-off, ORCHESTRATOR_DECISIONS, HANDOFF_LOG, STATUS |
| **S1** | `agent_s1/url-extract` | URL discovery (all sources → `:ExternalLink`) |
| **S2** | `agent_s2/url-probe` | HTTP reachability + Wayback fallback + body cache |
| **S3** | `agent_s3/content-verify` | Excerpt-to-page content matching (3 tiers) |
| **S4** | `agent_s4/schema-cleanup` | Secondary labels + text_content strip + FU-8 |
| **S5** | `agent_s5/visibility` | Denormalised source_urls / quality / freshness / trust on Projekt/Bauwerk/Akteur |
| **S6** | `agent_s6/audit` | Final integration audit + DataIssue seed + CI gate |

---

## §2 Dependency graph

```
                  [Stage 4 audit baseline must be DONE]
                                  │
                                  ▼
                              ┌───────┐
                              │  S1   │
                              └───┬───┘
                                  │
                ┌─────────────────┼────────────────┐
                │                 │                │
                ▼                 ▼                │
            ┌───────┐         ┌───────┐            │
            │  S2   │         │  S4   │ ←─ parallel-safe with S2/S3
            └───┬───┘         └───────┘            │
                │                                  │
                ▼                                  │
            ┌───────┐                              │
            │  S3   │                              │
            └───┬───┘                              │
                │                                  │
                └────────────────┬─────────────────┘
                                 │
                                 ▼
                             ┌───────┐
                             │  S5   │
                             └───┬───┘
                                 │
                                 ▼
                             ┌───────┐
                             │  S6   │ ← runs last; reads everything
                             └───────┘
```

### §2.1 Hard prerequisites

| Agent | Refuses to start unless | Source of truth |
|---|---|---|
| S1 | (none — first phase) | runs against live mit-bestand |
| S2 | `agent_s1/PHASE_S1_DONE.flag` exists | flag file under run dir |
| S3 | `agent_s2/PHASE_S2_DONE.flag` exists | flag file |
| S4 | `agent_s1/PHASE_S1_DONE.flag` exists | flag file |
| S5 | `agent_s2/PHASE_S2_DONE.flag` AND `agent_s3/PHASE_S3_DONE.flag` exist | flag files |
| S6 | All five S1–S5 flags exist | flag files |

---

## §3 Conflict-avoidance matrix

What each agent writes (mutates) vs. reads (consults).

| Agent | Writes | Reads (must not also write to) |
|---|---|---|
| S1 | new `:Quelle :ExternalLink` nodes; new `:ZITIERT_QUELLE` edges; `:Dossier.text_content` (reads only); `evidence_excerpt` on edges (reads only) | dossier `.md` files on disk; existing `:Quelle` nodes |
| S2 | properties on `:ExternalLink` (`url_status`, `url_http_code`, `url_redirect_chain`, `url_content_type`, `url_body_cache_path`, `url_wayback_*`, `url_last_checked_at`); `:DataIssue` for dead URLs | only existing `:ExternalLink.url`; never mutates other nodes |
| S3 | properties on `:ZITIERT_QUELLE` and `:BELEGT_IN` edges (`verification_status`, `verification_score`, `verification_method`, `verified_at`, `verification_notes`); `:DataIssue` for no-match | `:ExternalLink.url_status`, `:ExternalLink.url_body_cache_path`; the body cache; edge `evidence_excerpt` (read) |
| S4 | secondary labels (`:Dossier`, `:ExternalLink`, `:ResearchDocument`, `:SectionRef`); strips `:Dossier.text_content` (after S1); resolves dossier-path FU-8 | nothing that S2/S3 are writing |
| S5 | properties on `:Projekt`, `:Bauwerk`, `:Akteur` (`source_urls`, `source_quality_summary`, `source_freshness_summary`, `source_trust_score`, `source_urls_updated_at`) | S2's `url_status` and S3's `verification_status` |
| S6 | new `:DataIssue` nodes; `FINAL_QUELLE_AUDIT.md`; `STAGE_S6_AUDIT_DONE.flag` | everything (read-only writes to `:DataIssue` only) |

### §3.1 The hard rules

- No two agents write the same property on the same node.
- No two agents create the same edge type between the same node pair.
- S2 is the only writer of `url_*` properties. S3 is the only writer of `verification_*` properties. S5 is the only writer of `source_*` properties.
- All writes carry `migration_origin` for forensic tracing.

---

## §4 Shared resources

### §4.1 The body cache

S2 writes HTTP response bodies to `_neo4j/intake/runs/2026-05-21_quelle_remediation/shared/url_bodies/<md5(url)>.{html,pdf,bin}`. S3 reads from it.

Cache contract:
- Filename: `<md5(normalised_url)>.<ext>`
- Compressed with gzip if `> 100 KB`
- Per-file companion metadata at `<md5>.meta.json`: `{url, fetched_at, http_code, content_type, content_length, content_encoding, redirect_chain}`
- Cache invalidation: `url_last_checked_at` older than 30 days → re-fetch
- Cache size cap: 2 GB total, eject oldest if exceeded

### §4.2 The URL probe registry

S2 writes a single append-only JSONL at `agent_s2_url_prober/logs/url_probe_results.jsonl` for forensic auditability. Format:
```
{"url": "...", "normalised_url": "...", "probed_at": "...", "http_code": 200, "content_type": "...", "final_url": "...", "redirect_chain": [...], "user_agent": "...", "duration_ms": 1234, "wayback_attempted": false, "wayback_snapshot_url": null}
```

### §4.3 Verification registry

S3 writes a similar log at `agent_s3_content_verifier/logs/verification_results.jsonl`:
```
{"edge_id": "...", "edge_type": "ZITIERT_QUELLE", "excerpt": "...", "page_url": "...", "method": "exact|fuzzy_85|token_80|skipped", "score": 0.0-1.0, "status": "verbatim|paraphrase|no_match|...", "verified_at": "..."}
```

---

## §5 Decision routing

When an agent encounters an ambiguity not covered by its brief:

1. Check [QUELLE_REMEDIATION_PLAN.md §10](../QUELLE_REMEDIATION_PLAN.md) — that's the 12 pre-decided defaults (QD-1 … QD-12).
2. If still ambiguous, write a row in [HANDOFF_LOG.md §7 — Blockers + escalations](HANDOFF_LOG.md). The orchestrator triages.
3. Do NOT improvise schema decisions. Pause your phase, record the blocker, wait.

Examples of decisions you can make yourself:
- Tweaking a regex for URL extraction.
- Choosing between HTTP HEAD and GET for reachability probe.
- Caching strategy details (compression algo, file extension naming).

Examples of decisions you cannot make yourself:
- Adding a new node label.
- Adding a new property to a label that another agent owns.
- Changing the fuzzy-match threshold from QD-3's default of 85.

---

## §6 Branch + handoff protocol

### §6.1 Each agent

1. Branch from `wip/kinan2` at the orchestrator-published baseline commit.
2. Work in `_neo4j/intake/runs/2026-05-21_quelle_remediation/<agent_dir>/`.
3. When the phase's done flag is written and acceptance gates pass:
   - Push branch to remote.
   - Open PR to `wip/kinan2`, body = the report markdown.
   - Append a row to [HANDOFF_LOG.md](HANDOFF_LOG.md).

### §6.2 The orchestrator

1. Reviews each PR.
2. Merges into `orch/quelle-integrate` holding branch.
3. On full pipeline land, runs S6.
4. After S6 PASS, fast-forwards `wip/kinan2`.

---

## §7 Common conventions

- **Done flag.** `PHASE_S<n>_DONE.flag` is a JSON file at the agent's run-directory root.
- **Audit JSONL.** Per-phase audit detail at `agent_s<n>/logs/<phase>_audit.jsonl`.
- **Report.** Human-readable at `agent_s<n>/reports/agent_s<n>_report.md`.
- **migration_origin** property on every node/edge mutation: `'mig_s<n>_<purpose>'`.
- **Idempotency.** Every migration MUST be safe to re-run.

---

## §8 What "done" looks like for this whole effort

All six S-flags present + `STAGE_S6_AUDIT_DONE.flag` + `_neo4j/FINAL_QUELLE_AUDIT.md` written.

After that, the user (Kinan) can ask:

```
"For project p_holbein_gardens_london, give me every source URL with verification status."
```

And get an immediate, complete, honest answer.

---

**End of ORCHESTRATION.md.**
