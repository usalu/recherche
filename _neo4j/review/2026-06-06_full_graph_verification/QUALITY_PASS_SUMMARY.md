# Quality Pass Summary (Q1–Q5 + P6)

**Date:** 2026-06-06 · **Database:** `mit-bestand`
**Q5 apply status:** applied (39 ops; 2 BETEILIGT_AN geo-token upgrades reverted in ledger)
**P6-01 apply status:** applied (13 Q04 downgrade relabels; `evidence_confidence` → `niedrig`)

## Baseline (VERIFICATION_LEDGER_ELEMENT)

| Metric | Value |
|---|---:|
| Total element rows | 17,596 |
| Baseline PROVEN | 15,457 (87.8%) |

## Per-agent pass outcomes

### Q1 Schema & structural

- Rows adjudicated: **15**
- Upgraded to PROVEN: **4**
- DELETE/DEPRECATE proposed/applied: **0**
- ESCALATE_HUMAN: **1**

### Q2 Materialdepots

- Rows adjudicated: **17**
- Upgraded to PROVEN: **0**
- DELETE/DEPRECATE proposed/applied: **17**
- ESCALATE_HUMAN: **0**

### Q3 Compliance graph

- Rows adjudicated: **11**
- Upgraded to PROVEN: **5**
- DELETE/DEPRECATE proposed/applied: **0**
- ESCALATE_HUMAN: **0**

### Q4 Catalogue edges

- Rows adjudicated: **146**
- Upgraded to PROVEN: **26**
- DELETE/DEPRECATE proposed/applied: **107**
- DOWNGRADE relabels (`evidence_confidence=niedrig`): **13** (applied P6-01)
- ESCALATE_HUMAN: **0**

### Q5 Actor/participation + aggregator

- Rows adjudicated: **139**
- Upgraded to PROVEN: **36**
- DELETE/DEPRECATE proposed/applied: **1**
- ESCALATE_HUMAN: **47**

## Q5 detail

- Scope A (EP-09 actor rel residuals): **16** rows
- Scope B (external claim residuals): **123** rows
- Q5 upgrades to PROVEN: **36**

## P6 post-pass backlog

### P6-01 Q04 downgrade apply

- Patch: `quality_pass_q04_downgrades.patch.jsonl`
- Ops applied: **13** (`set_rel_properties`; `evidence_confidence`: belegt → niedrig)
- Graph impact: **0** node/rel count change
- Ledger: [`ledger/post_quality_p06_01.csv`](ledger/post_quality_p06_01.csv)
- Report: [`reports/post_quality_p06_01.md`](reports/post_quality_p06_01.md)
- Verified: all 13 Q04-tagged downgrade edges now `niedrig`; 26 upgrade edges remain `belegt`

## Projected PROVEN% (after Q1–Q5 ledger merges)

**15,493 / 17,596 = 88.05% PROVEN**

Negative verdict residuals (post-merge estimate):

- PARTIAL: 1015
- MISSING_EVIDENCE: 887
- UNVERIFIABLE: 124
- SCHEMA_VIOLATION: 52
- CONTRADICTION: 16
- REMEDIATED: 9
