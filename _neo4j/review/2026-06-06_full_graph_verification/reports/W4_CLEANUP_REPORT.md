# W4 Cleanup Report

**Date:** 2026-06-07T12:52:36Z · **Database:** `mit-bestand`

## Graph counts

| Metric | Before | After (expected) | After (actual) |
|---|---:|---:|---:|
| Nodes | 2263 | 2263 | 2263 |
| Relationships | 14819 | 14571 | 14571 |
| Δ rels | — | −248 | −248 |

## Delete summary

| Metric | Count |
|---|---:|
| W3 delete_rel total (01–05) | 636 |
| Skipped (bg_ involvement) | 416 |
| W3 eligible | 220 |
| v5 UNSUPPORTED extra | 28 |
| **Consolidated patch** | **248** |
| Dry-run would_delete_rel | 248 |
| Live deleted (actual Δ) | 248 |

### By agent

| Agent | Deletes |
|---|---:|
| W4-01 VMA | 29 |
| W4-02 HAT_BAUTEILTYP | 133 |
| W4-03 NUTZT_MATERIAL + sweep | 86 |

## Ledger v5 → v6

| Metric | v5 | v6 |
|---|---:|---:|
| Rows | 17081 | 16833 |
| PROVEN | — | 15006 (89.15%) |
| Rel rows removed | — | 248 |

## Patch

- `patches/w4_selective_unsupported_deletes.patch.jsonl`
- Apply report: `apply_reports/w4_selective_unsupported_deletes.patch.apply_report.md`
