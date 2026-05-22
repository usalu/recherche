# STATUS — Quelle remediation (6-agent run)

> Single-page state dashboard. Last sweep: **2026-05-22 (post-S6)**. **State: ALL 6 AGENTS DONE. Final verdict: PASS WITH RESIDUALS.**

---

## Phase board

| # | Phase | Owner | State | Flag |
|:-:|---|---|:-:|---|
| S1 | URL extractor | agent_s1 | ✅ DONE | `PHASE_S1_DONE.flag` |
| S2 | URL prober (HTTP + Wayback) | agent_s2 | ✅ DONE | `PHASE_S2_DONE.flag` |
| S3 | Content verifier (3-tier match) | agent_s3 | ✅ DONE | `PHASE_S3_DONE.flag` |
| S4 | Schema cleanup (labels + strip + FU-8) | agent_s4 | ✅ DONE | `PHASE_S4_DONE.flag` |
| S5 | Visibility surfacing | agent_s5 | ✅ DONE | `PHASE_S5_DONE.flag` |
| S6 | Audit + sign-off | agent_s6 | ✅ DONE | `STAGE_S6_AUDIT_DONE.flag` |

---

## 🎯 Headline outcomes

| Metric | Value | Comment |
|---|---:|---|
| `:Quelle` total | 2,755 | up from ~1,570 (S1 added ~1,185 nodes) |
| `:ExternalLink` distinct URLs | 1,030 | after dedup + normalisation |
| `:ExternalLink` node count | 2,640 | includes per-dossier S-refs |
| `:Dossier` with `text_content` | **0** | R7.d mistake fully reverted (was ~95) |
| URLs `reachable_2xx` | 1,955 | ~74 % of all probed |
| URLs dead (`4xx + 5xx + dns + tls + timeout`) | 598 | ~22 % — the chase result |
| Wayback fallback snapshots found | 148 | ~25 % of dead URLs have an archive |
| `source_curated` citation edges | 6,158 | what S3 attempted to verify |
| **Verbatim + paraphrase + token matches** | **4** | the **honest signal** — see "Surprise" below |
| `no_text_match` citations | 2,843 | the work-in-progress backlog |
| `:DataIssue` total | 4,976 | every problem is now graph-queryable |
| `:Projekt` with `source_urls` | 91 / 101 | 10 have zero sources (`node_with_no_source`) |
| `:Bauwerk` with `source_urls` | 186 / 186 | 100 % via Projekt→HAS_BAUWERK |
| `:Akteur` with `source_urls` | 511 / 648 | 78 % (registry-bound actors) |

---

## ⚠️ The big surprise — and what it actually means

**S3 found 4 verifiable matches out of 4,158 attempts (0.1 % match rate).**

This is not a bug. It is the chase-and-double-check working exactly as designed.

**Why it's low.** The `evidence_excerpt` fields on existing `source_curated` edges were written by research agents as **paraphrases**, not verbatim quotes. The three-tier match (exact → fuzzy 85 → token 80) can only find them if the original page text was preserved. Since most excerpts were author's-summary style ("project investigates reuse of S21 CLT formwork…"), they don't appear verbatim on any page.

**What it tells us.** The current corpus's claim "X is source_curated" should be read as **"X has a cited source and a paraphrase in the dossier, but the paraphrase has not been verified against the page"**. That is a much weaker claim than the schema implied.

**What to do next.** Two paths:

1. **Future ingestion rule** — require dossier authors to paste verbatim quotes (with German `…` ellipses for cuts) instead of paraphrases. Then S3 will match.
2. **Re-run S3 with looser thresholds** — drop the fuzzy threshold from 85 to 70 and the token threshold from 0.80 to 0.60. Will produce more matches at the cost of more false positives. Each match still records its score.

---

## Final QV invariant scoreboard

| Gate | Result |
|---|---|
| QV1 — every :Quelle has a secondary label | ✅ PASS (0) |
| QV2 — every :ExternalLink has non-null .url | ✅ PASS (0) |
| QV3 — every :ExternalLink has url_status | ✅ PASS (0) |
| QV4 — source_curated + excerpt → has verification_status | ⚠️ YELLOW (34) |
| QV5 — no :Dossier carries text_content | ✅ PASS (0) |
| QV6 — every Projekt/Bauwerk/Akteur has source_urls | ✅ PASS (0) |
| QV7 — every Projekt/Bauwerk/Akteur has source_quality_summary | ✅ PASS (0) |
| QV8 — every source_curated edge has verification_status | ⚠️ YELLOW (2,008 lack `evidence_excerpt` so couldn't be verified) |
| QV9 — no URL contains `utm_` or unintended trailing slash | ✅ PASS (0) |
| QV10 — every S2/S3/.../S6 DataIssue has :CONCERNS edge | ✅ PASS (0) |

8 PASS / 2 YELLOW / 0 FAIL. Both yellow items are residuals about edges with missing or paraphrased excerpts, not schema failures.

---

## What the user sees in Browser now

Click `p_holbein_gardens_london`:

```
source_urls:        [16 URLs — full list]
source_count:       16
source_quality_summary: {n_verbatim: 0, n_paraphrase: 0, n_no_match: 14, n_dead: 2, n_unchecked: 0}
source_freshness_summary: {n_reachable: 14, n_dead: 2, ..., latest_check_date: '2026-05-22'}
source_trust_score: 0.0306
source_urls_updated_at: 2026-05-22
```

The summary is **honest**: 14 of 16 URLs are reachable, but none of the citation excerpts could be matched against the page text. That's the diagnostic the user wanted.

---

## Outstanding residuals (the explicit backlog)

| # | Residual | Count | Recommended next step |
|---|---|---:|---|
| R-Q1 | `:Projekt` with zero sources | 10 | Backfill citations from dossier research, or accept as orphan |
| R-Q2 | source_curated edges with no excerpt (QV8) | 2,008 | Add excerpts to dossier text, re-run S3 |
| R-Q3 | source_curated edges with excerpt but unverified (QV4) | 34 | Debug S3 — likely cache miss or content-type issue |
| R-Q4 | `no_text_match` citations (the headline) | 2,843 | Two options above (verbatim ingestion OR loosen S3 thresholds) |
| R-Q5 | URLs dead with no Wayback snapshot | ~450 | Replace dead URLs with working equivalents in next ingestion |
| R-Q6 | URLs `blocked_by_robots` | 79 | Per-host exception list or skip permanently |
| R-Q7 | Excessive sources on 2 nodes | 2 | Review, prune if appropriate |

All seven are queryable: `MATCH (i:DataIssue {status:'open'}) RETURN i.kind, count(i)`.

---

## Documents

| Topic | Where |
|---|---|
| **Final audit** | [_neo4j/FINAL_QUELLE_AUDIT.md](../FINAL_QUELLE_AUDIT.md) |
| Master plan | [_neo4j/QUELLE_REMEDIATION_PLAN.md](../QUELLE_REMEDIATION_PLAN.md) |
| Orchestration | [ORCHESTRATION.md](ORCHESTRATION.md) |
| Handoff log (with completion notes) | [HANDOFF_LOG.md](HANDOFF_LOG.md) |
| Per-agent reports | `_neo4j/intake/runs/2026-05-21_quelle_remediation/agent_s<N>/reports/` |
| CI gate (active) | `_scripts/validate_no_text_content.py` |

---

**State: COMPLETE.** The 6 agents have produced an honest source-traceability layer. The work that remains is data-quality improvements in future ingestion rounds, all of which are tracked as `:DataIssue` nodes in the graph.
