# Quelle Remediation — Report (TEMPLATE — populated by runner)

- **Agent:** orchestrator_quelle_remediation
- **Plan:** [QUELLE_REMEDIATION_PLAN.md](../../../../QUELLE_REMEDIATION_PLAN.md)
- **Database:** mit-bestand
- **Completed (UTC):** _<fill on completion>_
- **Verdict:** _<PASS | FAIL>_

> This file is a placeholder. The runner can be extended to populate it
> automatically; for now, fill manually after running.

## Phase status

| Phase | Flag | Verdict | Notes |
|---|---|:---:|---|
| Q1 — URL extraction | `PHASE_Q1_DONE.flag` | — | candidates processed: —, URLs extracted: — |
| Q2 — secondary labels | `PHASE_Q2_DONE.flag` | — | Dossier: —, ExternalLink: —, ResearchDocument: —, SectionRef: — |
| Q3 — text_content strip | `PHASE_Q3_DONE.flag` | — | dossiers stripped: —, total chars removed: — |
| Q4 — surface source_urls | `PHASE_Q4_DONE.flag` | — | Projekt with URLs: —, avg sources: —, Bauwerk with URLs: —, Akteur with URLs: — |
| Q5 — docs + script | n/a (no graph mutation) | — | [QUELLE_QUERY_GUIDE.md](../../../../QUELLE_QUERY_GUIDE.md), `_scripts/find_sources.py` |

## Before / after counts

| Metric | Before | After |
|---|---:|---:|
| `:Quelle` total | — | — |
| `:Dossier` (secondary label) | 0 | — |
| `:ExternalLink` (secondary label) | 0 | — |
| `:ResearchDocument` (secondary label) | 0 | — |
| `:SectionRef` (secondary label) | 0 | — |
| `:Dossier` with `text_content` | ~95 | 0 |
| `:Projekt` with `source_urls` non-empty | 0 | — |
| `:Bauwerk` with `source_urls` non-empty | 0 | — |
| `:Akteur` with `source_urls` non-empty | 0 | — |

## Sample (post-Q4)

```
$ python _scripts/find_sources.py p_holbein_gardens_london
# p_holbein_gardens_london — Holbein Gardens, London
# 12 source URL(s)
https://www.akt-uk.com/...
https://www.bregroup.com/...
...
```

```
$ python _scripts/find_sources.py p_stuttgart_210 --full
# p_stuttgart_210 — Stuttgart 210
# labels: Projekt
# 7 source URL(s)

- https://www.stuttgart210.de/
    dossier: q_stuttgart_210_md    sref: S1
    excerpt: research programme and built youth-pavilion pilot...

- https://www.baunetzwissen.de/...
    dossier: q_stuttgart_210_md    sref: S7
    excerpt: twelve reused formwork elements...
```

## Risks observed

- _<populate after run>_

## Residuals

- 5 dossiers without `text_content` (FU-8) — their URLs are NOT extracted by Q1.
- Q4 flags any Projekt with `source_count > 50` as `:DataIssue {kind:'too_many_sources'}`. Manual review.
- The 16 dossiers with parallel `qu_*_dossier` aliases from R7.a — confirm that URL extraction worked on the canonical `q_<slug>_md` form.

## Handoff

After this run:
1. Update [REVIEW_BASED_PLAN/STATUS.md](../../../../REVIEW_BASED_PLAN/STATUS.md) — Quelle remediation row to DONE.
2. Add an FU-10 row in [FINAL_REVIEW_PLAN_AUDIT.md](../../../../FINAL_REVIEW_PLAN_AUDIT.md) §6 marking this complete.
3. Re-run `_scripts/_gap_survey.py` to confirm no regressions on the pre-existing data-quality checks.
4. The next ingestion pipeline must NEVER write `Quelle.text_content`. Add a CI gate that fails the build if any `:Dossier` has `text_content IS NOT NULL` post-ingestion.

---

**End of report template.**
