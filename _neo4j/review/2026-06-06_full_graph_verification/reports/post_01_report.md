# POST-01 Catalogue quote backfill

**Date:** 2026-06-07T10:00:11Z · **Agent:** POST-01 · **Database:** `mit-bestand`
**Scope size:** 1262 · **Rows emitted:** 200

## Verdict counts

| verdict | count |
|---|---:|
| UNSUPPORTED | 164 |
| PARTIAL | 20 |
| PROVEN | 16 |

**PROVEN in scope:** 16 (8.0%)

## Proposed actions

| action | count |
|---|---:|
| DELETE | 164 |
| DOWNGRADE | 20 |
| UPGRADE | 16 |

## Remainder

Live catalogue rels without `evidence_quote`: **~1262** total; this run processed **200** (batch cap 200).

Patch ops drafted (dry-run): **16** upgrades.

