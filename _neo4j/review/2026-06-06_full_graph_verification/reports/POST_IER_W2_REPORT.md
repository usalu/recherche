# POST-IER W2 Campaign Report

**Date:** 2026-06-07T11:59:17Z · **Database:** `mit-bestand`
**Graph (final):** 2263 nodes / 14819 relationships
**Ledger v3:** 17109 rows · **93.31% PROVEN** (15964)
**Ledger v4:** 17081 rows · **91.72% PROVEN** (15667) · **Δ -1.59 pp**
**Stale v3 rows pruned:** 28

## Agent summary

| Agent | Scope | Processed | PROVEN/upgrades | Patches drafted | Patches applied |
|---|---:|---:|---:|---:|---:|
| W2-01 | 1262 | 300 | 0 | 0 | 0 |
| W2-02 | 215 | 215 | 105 | 0 | 1 |
| W2-03 | 42 | 42 | 0 | 0 | 1 |
| W2-04 | 334 | 334 | 3 | 0 | 0 |
| W2-05 | 17109 | 17081 | 15667 (91.72%) | 0 | 1 |

## v4 PROVEN% delta vs v3

**Δ −1.59 pp** is expected under strict catalogue gate: W2-01 re-adjudicated 300 empty-quote catalogue rels → **300 UNSUPPORTED** overlays (0 upgrades). Those rows were PROVEN in v3 without live `evidence_quote`; ledger now reflects strict gate. Offset batches 0–200 (POST-01) + 200–500 (W2-01) = **500/1262** processed; **~762** catalogue rels remain.

W2-02 `post_04` apply enriched **105** node sources already PROVEN in v3 (graph property write; no ledger verdict change). Residual **215** `MISSING_EVIDENCE` rows: **0** new web-search upgrades.

## Patch apply: post_02_schema_violation

- Applied: **True** · Error: none
- Graph before apply: 2263 / 14839
- Graph after apply: 2263 / 14819

## v4 verdict distribution

| verdict | count | share |
|---|---:|---:|
| PROVEN | 15667 | 91.72% |
| UNSUPPORTED | 464 | 2.72% |
| UNVERIFIABLE | 357 | 2.09% |
| PARTIAL | 331 | 1.94% |
| MISSING_EVIDENCE | 215 | 1.26% |
| SCHEMA_VIOLATION | 33 | 0.19% |
| CONTRADICTION | 14 | 0.08% |

## Outputs

- `VERIFICATION_LEDGER_ELEMENT_v4.csv`
- `ledger/w2_01.csv` … `ledger/w2_05.csv`
- `reports/w2_01_report.md` … `reports/w2_05_report.md`
- `reports/POST_IER_W2_REPORT.md`
- `patches/w2_01_catalogue_backfill.patch.jsonl` (dry-run)
- `patches/w2_04_partial_vma.patch.jsonl`

## Blockers / follow-up

- **W2-04 VMA:** 0 `delete_rel` ops — v3 `PARTIAL` rows lack `category inference` notes POST-05 used; **122** live `VERBUNDEN_MIT_AKTEUR` edges still lack `evidence_quote`/`evidence_url` (many ledger-PROVEN via proof_quote only). Needs dedicated live-graph VMA pass.
- **W2-01:** `post_01_catalogue_backfill.patch.jsonl` **not applied** (164/200 UNSUPPORTED in wave 1); W2-01 patch empty (0/300 strict-gate upgrades).
- **W2-03:** **14** `CONTRADICTION` rows remain in v4 (28 geo rels fixed; human-gated remainder).
- All destructive applies succeeded: post_04 (node props), post_03 (−7 rels), post_02 (−20 rels), w2_04 (none).
