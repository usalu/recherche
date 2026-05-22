# POST-IER W3 Campaign Report

**Date:** 2026-06-07T12:35:20Z · **Database:** `mit-bestand`
**Graph (final):** 2263 nodes / 14819 relationships
**Ledger v4:** 17081 rows · **91.72% PROVEN** (15667)
**Ledger v5:** 17081 rows · **87.85% PROVEN** (15006) · **Δ -3.87 pp**
**Stale v4 rows pruned:** 20

## Agent summary

| Agent | Scope | Processed | PROVEN | UNSUPPORTED | Upgrades drafted | DELETE drafted | Patches applied |
|---|---:|---:|---:|---:|---:|---:|---:|
| W3-01 | 1262 | 190 | 40 | 133 | 40 | 133 | 1 |
| W3-02 | 1222 | 190 | 3 | 180 | 3 | 180 | 1 |
| W3-03 | 1219 | 190 | 0 | 190 | 0 | 190 | 0 |
| W3-04 | 1219 | 149 | 35 | 104 | 35 | 104 | 1 |
| W3-05 | 122 | 122 | 93 | 29 | 93 | 29 | 1 |
| W3-06 | 215 | 165 | 1 | 0 | 1 | 0 | 1 |
| W3-07 | 215 | 50 | 0 | 0 | 0 | 0 | 0 |
| W3-08 | 331 | 331 | 0 | 0 | 0 | 0 | 0 |
| W3-09 | 47 | 47 | 0 | 0 | 0 | 0 | 0 |

**Total upgrade ops drafted:** 172 · **DELETE ops drafted (not applied):** 636
**Patch apply rounds (upgrade-only):** 5

## v5 verdict distribution

| verdict | count | share |
|---|---:|---:|
| PROVEN | 15006 | 87.85% |
| UNSUPPORTED | 1093 | 6.40% |
| PARTIAL | 364 | 2.13% |
| UNVERIFIABLE | 357 | 2.09% |
| MISSING_EVIDENCE | 214 | 1.25% |
| SCHEMA_VIOLATION | 33 | 0.19% |
| CONTRADICTION | 14 | 0.08% |

## Outputs

- `VERIFICATION_LEDGER_ELEMENT_v5.csv`
- `ledger/w3_01.csv` … `ledger/w3_10.csv`
- `reports/w3_01_report.md` … `reports/w3_10_report.md`
- `reports/POST_IER_W3_REPORT.md`
- `patches/w3_01_catalogue_backfill.patch.jsonl` … `patches/w3_09_tier_d.patch.jsonl`

## Apply policy

- Non-destructive upgrades (`set_rel_properties`, `set_node_properties`) auto-applied when dry-run clean.
- DELETE patches drafted only — **not applied** in W3.

## Remaining blockers

- **UNSUPPORTED (1093):** catalogue strict-gate failures + VMA DELETE drafts pending human review.
- **MISSING_EVIDENCE (214):** nodes without recoverable web source.
- **PARTIAL (364):** weak entity gate or dossier-only address.
- **CONTRADICTION (14):** geo human-merge proposals in w3_09.
- **UNVERIFIABLE (357):** persons and opaque nodes.
- **DELETE drafts (636):** require explicit approval before apply.
