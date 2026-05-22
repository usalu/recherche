# Handoff log — Quelle remediation 2026-05-21 (6-agent run)

> Append-only log of agent handoffs. Each agent adds **one row** when finishing a phase.

**Convention:**
- Newest entry at the bottom.
- Date in ISO local + UTC offset, e.g. `2026-05-22 14:00 +02:00`.
- Status: `STAGED`, `RUNNING`, `PASS`, `PASS_WITH_RESIDUALS`, `FAIL`, `BLOCKED`.

---

## §1 Stage 0 — baseline

| When | Who | What | Branch / PR | Status | Notes |
|---|---|---|---|---|---|
| _<fill>_ | orchestrator | Baseline snapshot of mit-bestand at start of Quelle remediation | — | _<…>_ | nodes=4151, rels=25377 (post-Stage-4 review audit) |

---

## §2 S1 — URL extractor

| When | Who | Status | Notes |
|---|---|---|---|
| _<fill>_ | agent_s1 | _<…>_ | URLs extracted: total=<n>, dossier_md=<n>, dossier_bare=<n>, pre_existing=<n>, edge_property=<n>, node_property=<n>; top dossier by URL count: <id>/<count> |

## §3 S2 — URL prober

| When | Who | Status | Notes |
|---|---|---|---|
| 2026-05-22 09:02 +02:00 | agent_s2 | PASS | Covered 1,030 distinct URLs / 2,640 ExternalLink nodes; reachable_2xx=1,955, reachable_3xx_to_4xx=8, dead_4xx=336, dead_5xx=10, timeout=11, dns_failure=231, blocked_by_robots=79, tls_failure=10; Wayback fallbacks=148; body cache size=117.0 MB |

## §4 S3 — content verifier

| When | Who | Status | Notes |
|---|---|---|---|
| _<fill>_ | agent_s3 | _<…>_ | Verified <n> citations; verbatim_match=<n>, paraphrase_match=<n>, token_match=<n>, no_text_match=<n>, target_page_dead=<n>, cookie_wall=<n>, js_required=<n>, language_mismatch=<n>, fetch_error=<n>; top no-match project: <id>/<count> |

## §5 S4 — schema cleanup

| When | Who | Status | Notes |
|---|---|---|---|
| _<fill>_ | agent_s4 | _<…>_ | Secondary labels: Dossier=<n>, ExternalLink=<n>, ResearchDocument=<n>, SectionRef=<n>; FU-8 retries resolved=<n>, unresolved=<n>; text_content stripped from <n> dossiers (<n> chars total); aliases sanity = OK |

## §6 S5 — visibility

| When | Who | Status | Notes |
|---|---|---|---|
| _<fill>_ | agent_s5 | _<…>_ | Projekt with source_urls=<n>; avg source_count=<n>; trust ≥ 0.7=<n>; Bauwerk with source_urls=<n>; Akteur with source_urls=<n>; excessive_sources DataIssues=<n> |

## §7 S6 — audit + sign-off

| When | Who | Status | Notes |
|---|---|---|---|
| _<fill>_ | agent_s6 | _<…>_ | All 10 QV invariants=<violations sum>; FINAL_QUELLE_AUDIT.md written; CI gate installed; verdict=<PASS/PASS_WITH_RESIDUALS/FAIL> |

---

## §8 Blockers + escalations

If you cannot proceed, write here. The orchestrator triages.

| When | Who | What's blocked | Why | Resolution |
|---|---|---|---|---|
| | | | | |

---

## §9 Decision resolutions (QD-1 through QD-12)

| ID | Topic | Decided | Decided by | Resolution |
|---|---|---|---|---|
| QD-1 | Proactive Wayback archiving | _<open>_ | _<…>_ | _<YES default>_ |
| QD-2 | Respect robots.txt | _<open>_ | _<…>_ | _<YES default>_ |
| QD-3 | Fuzzy threshold (Tier B) | _<open>_ | _<…>_ | _<85 default>_ |
| QD-4 | Token threshold (Tier C) | _<open>_ | _<…>_ | _<0.80 default>_ |
| QD-5 | Wayback as verification source | _<open>_ | _<…>_ | _<YES default>_ |
| QD-6 | Cross-lingual handling | _<open>_ | _<…>_ | _<no_text_match + language_mismatch note>_ |
| QD-7 | Compute source_trust_score | _<open>_ | _<…>_ | _<YES default>_ |
| QD-8 | HTTP User-Agent | _<open>_ | _<…>_ | _<honest identifier + email>_ |
| QD-9 | CI gate validate_no_text_content | _<open>_ | _<…>_ | _<YES default>_ |
| QD-10 | HTTP probe timeout | _<open>_ | _<…>_ | _<10s connect + 20s read>_ |
| QD-11 | Max body cache size per URL | _<open>_ | _<…>_ | _<5 MB>_ |
| QD-12 | Cookie wall as no_text_match | _<open>_ | _<…>_ | _<YES default>_ |

---

**End of HANDOFF_LOG.md.**
