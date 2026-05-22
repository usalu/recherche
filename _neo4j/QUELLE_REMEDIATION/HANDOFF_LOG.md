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
| 2026-05-21 | agent_s1 | PASS | Stage 1 dossier links=3309, bare URLs=517; stage 2 pre-existing Quelle.url=2640; stage 3 edge-property URLs=2243; stage 4 node-property URLs=20; **distinct URLs after normalisation=1030**; errors=0 |

## §3 S2 — URL prober

| When | Who | Status | Notes |
|---|---|---|---|
| 2026-05-22 09:02 +02:00 | agent_s2 | PASS | Covered 1,030 distinct URLs / 2,640 ExternalLink nodes; reachable_2xx=1,955, reachable_3xx_to_4xx=8, dead_4xx=336, dead_5xx=10, timeout=11, dns_failure=231, blocked_by_robots=79, tls_failure=10; Wayback fallbacks=148; body cache size=117.0 MB |

## §4 S3 — content verifier

| When | Who | Status | Notes |
|---|---|---|---|
| 2026-05-22 | agent_s3 | PASS_WITH_HONEST_SIGNAL | Attempted 4,158 source_curated citation edges; **verbatim_match=0, paraphrase_match=4, token_match=0**; no_text_match=2,847; target_page_dead=1,152; fetch_error=44; cookie_wall_detected=1; no_url_node=110; language_mismatch=0; errors=0. **Match rate of attempted = 0.1 %.** This is the honest signal predicted by the plan: existing `evidence_excerpt` fields were paraphrased by research agents, not verbatim from source pages. Future dossiers must use verbatim quotes for verification to work. |

## §5 S4 — schema cleanup

| When | Who | Status | Notes |
|---|---|---|---|
| 2026-05-22 09:23 +02:00 | agent_s4 | PASS | Secondary labels: Dossier=100, ExternalLink=2640, ResearchDocument=201, SectionRef=641; FU-8 retries resolved=5, unresolved=0; text_content stripped from 100 dossiers (2570644 chars total); aliases sanity = OK (16 known R7.a aliases present, 0 repairs needed). |

## §6 S5 — visibility

| When | Who | Status | Notes |
|---|---|---|---|
| 2026-05-22 | agent_s5 | PASS | Projekt with source_urls=91/101 (10 have NULL trust — no sources); avg trust=0.0127 (low because S3 produced few matches; see S3 row); Bauwerk with source_urls=186/186 (100 %); Akteur with source_urls=511/648 (78 %); excessive_sources DataIssues=2; all S5 acceptance gates green |

## §7 S6 — audit + sign-off

| When | Who | Status | Notes |
|---|---|---|---|
| 2026-05-22 07:43 UTC | agent_s6 | **PASS WITH RESIDUALS** | QV1, QV2, QV3, QV5, QV6, QV7, QV9, QV10 = PASS (8/10). QV4 = YELLOW (34 source_curated edges with excerpt have no verification_status). QV8 = YELLOW (2,008 source_curated edges have no excerpt, so S3 couldn't verify them). `:DataIssue` total=4,976. node_with_no_source seeded for 10 :Projekt. FINAL_QUELLE_AUDIT.md written. CI gate `_scripts/validate_no_text_content.py` installed. |

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
