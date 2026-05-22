# Long-term plan — from snapshot project to maintained graph

**Status:** Draft for user review · **Horizon:** 18 months · **Author:** Claude (Opus 4.7)
**Date drafted:** 2026-05-22
**Supersedes:** the cycle of one-off remediations (review_based_plan, S1–S6, Q-EXT, FU-N)

> **What this is.** A plan to stop running reactive remediation rounds and start running a *maintained* knowledge graph. The graph stops being a series of audited snapshots and becomes a living system that gets *more* trustworthy over time, not less.

> **What changed in my thinking.** We've shipped three remediation rounds in three weeks. Each one produced honest data. Each one was followed by a finding that something else was broken. The pattern is reactive. The graph won't be sustainable until we stop fixing the past and start governing the present.

---

## §1 Why this plan exists

Three remediation rounds since 2026-05-14:

1. **Radical quality reset** (R1–R10, review_based_plan) — found 1,454 `:DataIssue`, restored 5 demoted labels, added missing structural edges, recomputed tiers, and ended with **PASS WITH RESIDUALS**.
2. **Quelle remediation** (S1–S6) — chased every URL, double-checked content. Result: only 4 of 4,158 verifications matched (0.1%). Honest signal. PASS WITH RESIDUALS.
3. **Universal source surfacing** (Q-EXT.A/B/C v1/v2) — extended source_urls to every domain node, added confirmed_source_urls with 3 strict criteria. Result: ongoing.

Each round produced more `:DataIssue` records: 1,454 → 4,976. **The backlog grew faster than we closed it.** That's the symptom of a snapshot project, not a maintained system.

The remediation work is technically excellent. The PROCESS is unsustainable.

---

## §2 Where we are now (the honest baseline)

| Metric | Value | Comment |
|---|---:|---|
| Total nodes | ~5,540 | grown ~3× in 3 weeks |
| Total relationships | ~27,000 | grown ~35% |
| `:DataIssue` open | **4,976** | the queryable backlog |
| URL `reachable_2xx` | 74 % | S2's chase result |
| URL `dead_*` | 22 % | needs replacement or Wayback fallback |
| S3 content-verified citations | **4 of 4,158** (0.1 %) | the root structural problem |
| Tier-1 projects with `confirmed_source_count ≥ 3` | (TBD after Q-EXT.C v2) | will likely be small |
| Time per remediation round | ~6 hours of orchestration + agent work | unsustainable as new data arrives |
| Forward ingestion rate | 0 batches/month | no automated path |

**The graph is honest about its state. It is not yet maintained.**

---

## §3 The vision — 18 months from today

A user lands on the graph cold and can:

1. **Click any node** and immediately see source URLs that have been verified in the last 30 days, with a confidence score that reflects reality.
2. **Add a new project** by submitting one markdown dossier through a PR. CI checks it for verbatim quotes, valid URLs, schema compliance. If clean, it merges. If not, the PR shows actionable diffs.
3. **Query "show me decision-grade reuse projects involving steel in Belgium"** and get 3–8 projects whose tier-1 status is provably grounded in verbatim cell citations from live, content-verified URLs.
4. **Trust the answer.** The graph's `:DataIssue` open count is < 100. Tier-1 means tier-1. Every claim has a clickable source.

That's the destination. Below: how we get there.

---

## §4 Five pillars

### §4.1 Pillar A — Ingestion contract (the "no garbage at the door" layer)

**Problem today.** Dossier authors paste paraphrases instead of verbatim quotes (root cause of 0.1% S3 match rate). Some still use retired schema names. There's no PR gate, no source-format validator. Everything is added live to the graph then audited later.

**Target state.** Every new dossier is a PR. CI runs:
- `validate_no_text_content.py` (already exists)
- `validate_dossier_schema.py` (already exists — needs activation as a gate)
- `validate_verbatim_excerpts.py` (NEW — for every `evidence_excerpt`, confirm the cited URL's body contains a substring match, OR the excerpt is marked `paraphrase=true` and stored separately)
- `validate_url_reachable.py` (NEW — every new URL must HTTP-probe 200 OR have a Wayback fallback)
- `validate_required_fields.py` (NEW — every node-creating row needs id, name, source_url, evidence_excerpt OR explicit `paraphrase=true`)

If any gate fails → PR can't merge. If all pass → loader runs against a staging Neo4j instance, then promotes to production on green.

**Schema delta.** Add to every newly-created edge:
```
evidence_excerpt              // verbatim or paraphrase
evidence_excerpt_kind         // 'verbatim' | 'paraphrase' | 'derived'  (NEW)
evidence_excerpt_verified_at  // date when last checked against source
```

`evidence_excerpt_kind='paraphrase'` is acceptable but visible — tier-1 gates can require verbatim.

**Effort estimate.** ~3 weeks to build the validators, ~1 week to migrate existing loaders, ~1 week to migrate existing dossiers to the new format. Total **5 weeks** (Phase L2).

### §4.2 Pillar B — Continuous verification (the "stay true" layer)

**Problem today.** Every URL was probed once (S2). Every citation was verified once (S3). Nothing re-checks. URLs go dead, pages change, the graph silently drifts.

**Target state.** Three scheduled jobs:

| Job | Frequency | What it does |
|---|---|---|
| **URL re-probe** | Monthly | Re-runs S2 on every `:ExternalLink` whose `url_last_checked_at` is > 30 days. Tags status changes; auto-creates `:DataIssue` on degradation (alive → dead). |
| **Content re-verify** | Quarterly | Re-runs S3 on every `:ZITIERT_QUELLE` whose body cache md5 has changed since last verify. Tags drift; auto-creates `:DataIssue` on regression. |
| **Wayback archival** | Every new URL on ingestion | Per QD-1: fire-and-forget `web.archive.org/save/<url>`. Insurance against future link rot. |

Implemented as:
- A `cron`-equivalent (GitHub Actions scheduled workflows, or a local Windows Task Scheduler entry, or one of the CronCreate harness hooks).
- Each job runs the existing S2 / S3 runner with a `--re-verify-since 30d` flag.
- Outputs are commits to `_neo4j/intake/runs/<auto-run-id>/`.

**Schema delta.** Add to `:ExternalLink`:
```
url_check_history             // list of {date, status, http_code}
                              //    last 12 entries kept
url_status_changed_at         // most recent date status changed
```

**Effort estimate.** ~2 weeks to set up the scheduler + retry-only flags. **Phase L3.**

### §4.3 Pillar C — Trust scoring + tier classification (the "honest signal" layer)

**Problem today.** The tier-1 gate counts `BELEGT_IN` evidence, not the actual citation chain. R1's reclassification didn't change the tier-1 cohort. The "decision-grade" label is detached from confirmable evidence.

**Target state.** Tier definition is reformulated and applied consistently:

```
A :Projekt is tier_1_decision_grade iff ALL:
  - year_completed IS NOT NULL
  - LIEGT_IN_LAND edge present
  - n_distinct_bauteilgruppen ≥ 3
  - has_quantification (n_bg_quantified ≥ 1 OR :HAT_KENNWERT ≥ 1 with confirmed_source_count ≥ 1)
  - n_source_curated_with_confirmed_url ≥ 3      ← NEW HONEST GATE
                                                    (BELEGT_IN edge with evidence_origin='source_curated'
                                                     AND ≥ 1 entry in the target's confirmed_source_urls)
```

The new criterion `n_source_curated_with_confirmed_url ≥ 3` means: at least 3 of the project's curated citations point at URLs whose content has been independently confirmed (via C1/C2/C3 from Q-EXT.C v2). That's what "decision-grade" should mean.

**Expected effect.** Tier-1 cohort drops from 11 (artificially inflated) to 3–8 (honest). The drop is the metric.

Tier recomputation runs:
- After every ingestion (PR merge).
- After every monthly URL re-probe (URLs going dead may demote a project).
- After every Q-EXT.B/C re-run.
- Manually via `_scripts/recompute_tiers.py`.

**Effort estimate.** ~1 week to define + implement the new gate, ~1 week to validate against historical snapshots. **Phase L4.**

### §4.4 Pillar D — Backlog management (the "work it down" layer)

**Problem today.** 4,976 `:DataIssue` open. No owner. No cadence. No closure pathway. They just accumulate.

**Target state.** Every `:DataIssue` has a lifecycle:

```
:DataIssue.status ∈ {
  'open',                  // newly emitted, untriaged
  'triaged',               // someone reviewed; assigned a kind + owner
  'in_review',             // someone is working on it
  'resolved',              // fixed; will be detached-deleted in next cleanup
  'wont_fix',              // accepted as-is (with a documented reason)
  'false_positive'         // emit logic was wrong
}
:DataIssue.owner            // 'kinan' | 'orchestrator' | 'contributor:<name>'
:DataIssue.triaged_at
:DataIssue.resolved_at
:DataIssue.resolution_evidence
```

Triage cadence: **weekly**, 30 minutes max. Each week the owner (Kinan) reviews the top 10 issues by severity:
1. `high` severity always first
2. Within severity, sort by `count(CONCERNS → Projekt {quality_tier:'tier_1_decision_grade'})` — issues touching tier-1 first
3. Within that, oldest `found_at` first

The orchestrator (me) emits a weekly triage report:
- Top 10 candidates
- Status changes since last week
- Burn-down trend (open count, week over week)

Closed `:DataIssue` are kept for forensic purposes for 90 days, then detached-deleted.

**Schema delta.** Add the lifecycle fields above to every `:DataIssue`.

**Effort estimate.** ~3 days to implement the lifecycle props + triage report. Burn-down is the long tail (target: 1 year). **Phase L5.**

### §4.5 Pillar E — Schema governance (the "no more ad-hoc cypher" layer)

**Problem today.** Schema changes happen via one-off Cypher migrations in run-specific directories. There's no central register. Constraints aren't enforced at the Neo4j level. New ingestion can write any label, any property, any combination.

**Target state.** Schema-as-code:

```
_neo4j/migrations/
├── 000_baseline.cypher                     # the existing schema, frozen
├── 001_add_:DataIssue_lifecycle.cypher
├── 002_add_evidence_excerpt_kind.cypher
├── 003_add_url_check_history.cypher
├── ...
└── current.cypher                          # symlink to highest applied
```

Each migration:
- Numbered.
- Idempotent (re-running is a no-op).
- Forward-only (no downgrades; rollback is a new forward migration).
- Tested against a staging instance before production.

Neo4j constraints enforced for the invariants:
```cypher
CREATE CONSTRAINT projekt_id_unique FOR (p:Projekt) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT externallink_url_unique FOR (e:ExternalLink) REQUIRE e.url IS UNIQUE;
CREATE CONSTRAINT evidence_origin_enum FOR ()-[r]-() REQUIRE r.evidence_origin IS NULL
  OR r.evidence_origin IN ['source_curated','topology_synthesized',
                            'registry_derived','inferred','external_unfolded'];
-- (etc., for every enum)
```

**Effort estimate.** ~2 weeks to extract baseline + write the migration framework. **Phase L6.**

---

## §5 Phased roadmap (18 months)

| Phase | Months | Focus | Exit criteria |
|---|---|---|---|
| **L0** | now | Finish Q-EXT.C v2; close out the current remediation cycle | `confirmed_source_urls` populated on every domain node; `:DataIssue` open ≤ 5,500 (current + ~500 new from Q-EXT) |
| **L1 — Stabilise** | 1–2 | Burn down the highest-severity DataIssue (`high` kind only); land FU-1 v2 (tier definition revision); document the current state as the "before" baseline | `:DataIssue {severity:'high'}` open ≤ 100; tier-1 cohort recomputed and stable |
| **L2 — Ingestion contract** | 3–4 | Build the 4 new validators; activate as CI gates; migrate existing loaders; convert 5 dossiers to verbatim-quote format as proof | A PR with a new dossier merges only after all gates pass; 5 dossiers in verbatim format show S3 match rate > 90% |
| **L3 — Continuous verification** | 5–7 | Wire monthly URL re-probe + quarterly content re-verify + Wayback proactive archival; expose status-change DataIssue | At least 1 successful monthly + 1 quarterly cycle completed; status-change DataIssue emerges as expected |
| **L4 — Trust scoring overhaul** | 8–10 | Apply new tier definition; recompute scores; expose dashboards (Neo4j Bloom + a simple HTML export); FU-7 source_curated-without-excerpt cleanup | Tier-1 cohort honest and stable; query "show tier-1 projects with full source verification" returns 3–8 |
| **L5 — Backlog burn-down** | 11–12 | Wire DataIssue lifecycle; weekly triage cadence; burn down `medium` + `low` | `:DataIssue` open ≤ 500 |
| **L6 — Schema governance** | 13–15 | Extract schema-as-code; migration framework; Neo4j constraints enforced; remove the freelance-Cypher option | Every schema change in `_neo4j/migrations/`; ingestion can't violate constraints |
| **L7 — Public surface** | 16–18 | Query guide refinement; per-Projekt JSON exports; optional public API; documentation reach | A first-time researcher can answer the 5 canonical queries within 10 minutes |

**Critical path.** L1 → L2 → L3. Everything else can flex.

---

## §6 What this plan deliberately does NOT do

- **Doesn't expand the corpus.** No new projects until ingestion contract is in place. Quality > quantity.
- **Doesn't add new agents / orchestrations.** The 6-agent S1–S6 split was instructive but expensive to coordinate. Long-term work is one or two scripts, not 6 LLM agents.
- **Doesn't switch databases.** Neo4j stays. Aura migration deferred to L7+ if at all.
- **Doesn't rename the schema to English.** R6 deferred indefinitely; the cost is too high and the benefit is debatable for a German-rooted corpus.
- **Doesn't try to translate the graph (de ↔ en).** Cross-language is out of scope.
- **Doesn't open-source the graph.** Hold until L7 and re-evaluate.
- **Doesn't fund a manual curator.** All work must be do-able by Kinan + AI assistant.

---

## §7 Roles + responsibilities

| Role | Who | What they own |
|---|---|---|
| **Direction + content** | Kinan | What gets added; which projects matter; which decisions are right |
| **Infrastructure + automation** | Orchestrator (Claude / future AI) | Migrations, validators, schedulers, audits, reports |
| **Curation** | Kinan + contributors via PR | Each new dossier is a contribution with verbatim quotes |
| **Triage** | Kinan (30 min/week) | Reviews top-10 :DataIssue queue |
| **Pipeline maintenance** | Orchestrator | Monthly + quarterly re-verify runs; status reports |

The orchestrator does the labor. Kinan does the judgement.

---

## §8 Success metrics — what "long-term done" looks like

### §8.1 Outcome metrics (the headlines)

| Metric | Today | Target (18 mo) |
|---|---:|---:|
| `:DataIssue` open | 4,976 | < 100 |
| URL `reachable_2xx` rate | 74 % | > 90 % |
| URL `dead_*` with Wayback fallback | ~25 % of dead | > 95 % of dead |
| S3 verification match rate | 0.1 % | > 60 % (verbatim quotes after L2) |
| Tier-1 with `confirmed_source_count ≥ 3` | unknown | 100 % of tier-1 |
| Tier-1 cohort size | 11 (artificially) | 5–10 (honest) |
| New ingestion CI failure rate | n/a | < 5 % (loader catches issues at PR) |
| Time from dossier submission to merge | manual hours | < 2 days |

### §8.2 Process metrics

| Metric | Today | Target |
|---|---|---|
| Manual orchestration per month | ~6 hours/round × 1–3 rounds | < 4 hours total |
| Schema changes via run-specific cypher | 100 % | 0 % (all via `_neo4j/migrations/`) |
| Issues that recur after fix | unknown | 0 (constraints prevent regression) |
| Triage cadence adherence | n/a | 50 of 52 weeks |

### §8.3 Trust metrics

| Metric | Today | Target |
|---|---|---|
| % of edges with `evidence_excerpt_kind` set | 0 | 100 % |
| % of nodes with `confirmed_source_urls` ≥ 1 | TBD post-v2 | ≥ 95 % |
| % of dossiers with verbatim-mode excerpts | < 5 % | ≥ 80 % |
| Time since last URL re-probe per `:ExternalLink` | varies (some never) | ≤ 31 days |

---

## §9 Open decisions blocking the plan

| ID | Decision | Default recommendation | Blocks |
|---|---|---|---|
| LT-1 | Run scheduled jobs locally (Windows Task Scheduler) or in cloud (GitHub Actions)? | **GitHub Actions** — better visibility, free for public repos, can call Neo4j Aura | L3 |
| LT-2 | Move to Neo4j Aura (managed cloud) or keep local self-hosted? | **Defer** — local is fine until L7; reconsider when CI needs to write |
| LT-3 | Enforce Neo4j constraints (write-time blocking) or audit-only (read-time verifying)? | **Enforce** — write-time. Catches regressions immediately. | L6 |
| LT-4 | Adopt SHACL / OWL for schema constraints? | **NO** — overkill. Neo4j native constraints + the existing audit suite are enough. | L6 |
| LT-5 | Make the graph publicly accessible (e.g., Bloom viewer with read-only auth)? | **Defer to L7** — assess after backlog burn-down. | L7 |
| LT-6 | Accept paraphrase excerpts forever or sunset them? | **Sunset over 6 months** — by end of L5, paraphrase-only edges are demoted to a lower tier. | L2, L4 |
| LT-7 | Continue running remediation rounds in parallel with L0–L7? | **NO** — pause new remediation work after L0; treat all future graph fixes as either a backlog burn-down (L5) or a new ingestion (L2). | L1 |
| LT-8 | Hire / engage a second contributor for ingestion? | **Optional** — only needed if Kinan's bandwidth becomes the constraint. The orchestrator removes most operational load. | flexible |

---

## §10 Risks + mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| L2 verbatim-quote requirement is too strict; existing dossier authors push back | Medium | Medium | Allow `paraphrase=true` mode with explicit lower tier ceiling. Migrate gradually. |
| Wayback Machine rate-limits proactive saves | Low | Low | Already covered in S2's rate-limit policy. |
| The `:DataIssue` lifecycle gets ignored after the first few weeks | High | Medium | Tie it to the monthly URL re-probe report — every cycle surfaces top 10 candidates; can't escape attention. |
| Neo4j constraint additions break existing data | Medium | High | Add constraints AFTER fixing violations; the L6 phase explicitly orders constraints after the backlog burn-down. |
| GitHub Actions has no access to local Neo4j | Certain | High if not addressed | Move to Aura at L3 or use a tunnel (ngrok) for CI write. Decision deferred. |
| User loses motivation during the 18-month horizon | Medium | High | Each phase produces a visible improvement. L1 closes the high-severity backlog visibly (4,976 → ~3,500). L2's first verbatim dossier produces an immediate S3-match win. |

---

## §11 What we have to commit to before L1 starts

These are the irreducible prerequisites:

1. **Stop adding new dossiers in the old format.** Today. Until L2 lands, the corpus is frozen at its current shape (modulo finishing Q-EXT.C v2).
2. **Schedule 30 minutes/week** for the triage cadence (L5 and onwards).
3. **Decide LT-1, LT-6, LT-7** before L1 starts. The others can flex.
4. **Tag this commit point as `v1.0-baseline`** in git. Every future improvement is measured against it.

---

## §12 What happens if we don't do this

Each future remediation round produces another 1,000–2,000 `:DataIssue` records. The orchestrator (me) will get more efficient at coordinating, but the *graph* gets less trustworthy because nobody is closing the loop. By month 6 without this plan, the `:DataIssue` count is plausibly 8,000–12,000 and a query like "tier-1 projects with verified sources" returns essentially nothing of value.

The cost of NOT doing this plan = the graph degrading into a museum of audited mistakes.

---

## §13 What the user (Kinan) sees at each phase boundary

| End of phase | What's visibly different |
|---|---|
| L0 | Click `mat_stahl` in Browser → see `confirmed_source_urls` with multiple reasons each |
| L1 | `:DataIssue` count dropped by ~30 %; tier-1 cohort reflects reality |
| L2 | First PR with a new dossier merges or is rejected on CI; first dossier in verbatim format shows S3 match rate ~95 % |
| L3 | Email / report arrives monthly: "X URLs went dead since last month; Y were Wayback-recovered" |
| L4 | Tier-1 projects displayed in Bloom with green ✓ for source verification; bad ones flagged amber |
| L5 | Burn-down chart shows `:DataIssue` open trending toward 100; weekly triage takes 20 min |
| L6 | Attempt to write a bad edge from the CLI fails immediately with a constraint error |
| L7 | A researcher (you OR an external user) opens the query guide and answers their question in 5 minutes |

---

## §14 Sequencing summary

```
L0 [now]    Q-EXT.C v2 + close out current remediation
                │
                ▼
L1 [1-2mo]  Stabilise — burn down 'high' DataIssue + FU-1 v2
                │
                ▼
L2 [3-4mo]  Ingestion contract — 4 validators + CI gates
                │
                ▼
L3 [5-7mo]  Continuous verification — monthly URL probe, quarterly S3
                │
                ▼
L4 [8-10mo] Trust scoring — honest tier + dashboards
                │
                ▼
L5 [11-12mo] Backlog burn-down — DataIssue lifecycle + weekly triage
                │
                ▼
L6 [13-15mo] Schema governance — migrations as code + Neo4j constraints
                │
                ▼
L7 [16-18mo] Public surface — query guides + JSON exports + (maybe) API
```

Each phase is independently committable. If L4 reveals that L2's verbatim contract isn't working, we re-enter L2 before progressing.

---

## §15 The very first action

Two things, before L1 even starts:

1. **Run Q-EXT.C v2** (still pending) to close out L0.
2. **Read this plan**, decide LT-1 / LT-6 / LT-7, and tag a `v1.0-baseline` commit.

After those: L1 begins with FU-1 v2 (tier definition revision) and the high-severity backlog burn-down. Both are already drafted as residuals.

---

## §16 Sign-off

This is a multi-quarter commitment. It's deliberately long because the graph deserves long-term thinking, not another quarterly remediation round.

The shorter version: **we stop fixing the graph and start running it.** Every change goes through a contract. Every URL gets re-checked. Every issue gets triaged. Every claim is grounded in a verifiable cell-citation. In 18 months a researcher can land on the graph and trust it.

---

**End of LONG_TERM_PLAN.md (rev. 2026-05-22).**
