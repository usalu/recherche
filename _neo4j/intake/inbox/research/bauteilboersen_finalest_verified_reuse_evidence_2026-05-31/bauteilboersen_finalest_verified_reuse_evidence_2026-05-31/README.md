# Bauteilbörsen finalest verified reuse evidence package

Created: 2026-05-31

This is the cleaned final package after comparing the readable markdown report against the last reclassification ZIP.

## Source of truth

Use these files first:

1. `csv/FINAL_IMPORT_SAFE_MATERIAL_BAUTEILTYP_CLAIMS.csv` — import-safe strict claims only.
2. `csv/FINAL_ACTOR_STATUS_AND_COVERAGE.csv` — one row per actor, all 39 actors included.
3. `json_per_actor/*.finalest.evidence.json` — per-actor strict/review/scope split.
4. `csv/FINAL_EVIDENCE_LEDGER_ALL_ROWS.csv` — all strict + review + scope rows in one place.

## Do not use as source of truth

The previous standalone markdown report `final_bauteilboersen_final_report.md` is preserved only indirectly through the comparison files. It was readable but not audit-safe. The comparison found missing actors, duplicate rows, and mismatches with pass 8.

## Counts

- Actors covered: 39
- Strict import-safe rows: 150
- Review-only rows retained: 235
- Scope-only actor rows: 10
- Actors with strict evidence: 18
- Actors with review-only evidence: 15
- Actors with scope-only evidence: 6
- Actors with no captured evidence: 0

## Import discipline

- Product/detail URL evidence is strongest.
- Category/listing pages are acceptable for Bauteiltyp and, only when explicit, Material.
- Aggregator/about/how-it-works pages confirm actor role or scope only.
- Do not convert generic terms into closed-set materials: `Metall ≠ Stahl`, `Stein ≠ Naturstein`, `tile/Fliesen/carrelage ≠ Keramik` unless explicitly ceramic/Keramik/Feinsteinzeug/céramique, etc.
