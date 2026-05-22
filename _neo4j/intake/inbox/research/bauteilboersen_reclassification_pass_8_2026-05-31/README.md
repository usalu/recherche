# Bauteilbörsen Reclassification Pass 8 — 2026-05-31

This package reruns the strict/review split after the user supplied additional product/shop URLs. It does not invent claims: every added Material/Bauteiltyp row has a URL, quote, and line/source reference.

## What changed

- **BauKarussell** moved from `NO_CLOSED_SET_MATERIAL_BT_EVIDENCE_IN_FINAL_PASS` to strict import candidates based on the first-party shop/product-list rows: Eichenparkett/Parkett Buche, Glas Pendelleuchte, and the category tree.
- **re:store / Materialnomaden** moved from no strict evidence to strict material/type candidates based on first-party product pages: Betonsteine, Natursteinbelag Schiefer, Natursteinpflaster, Dachziegel Biberschwanz, and Lärchenschindel.
- **Building Spares Market** moved from no strict evidence to strict/review coverage from first-party live listings and the about/category examples. The user-supplied chipboard advert URL was *not* used as strict evidence because the direct fetch timed out; the actor is still supported by fetched first-party pages.
- **Gebruiktebouwmaterialen.com** moved to strong strict category-level evidence from its first-party category tree and product rows.
- **Material Index** had its first-party marketplace category tree promoted for Bauteiltyp coverage; material request examples remain review-only.
- **Salza, Raedificare, ReSource Marktplaats, Loopfront, Material Reuse Portal, Globechain, BatRecup** are confirmed as material-reuse or construction-reuse platforms, but public pages do not expose enough product/category evidence for broad strict closed-set material/type import.
- **Warp It** is reclassified as adjacent/general resource redistribution rather than a core construction-material bauteilbörse.

## Main files

- `csv/PASS8_CONSOLIDATED_STRICT_IMPORT_CANDIDATES_MATERIAL_BAUTEILTYP.csv` — pass 7 strict rows plus pass 8 strict additions/promotions.
- `csv/PASS8_STRICT_IMPORT_ADDITIONS_AND_PROMOTIONS.csv` — only the new/promoted pass 8 strict rows.
- `csv/PASS8_REVIEW_ONLY_ADDITIONS.csv` — newly found evidence that is useful but not strict import-ready.
- `csv/PASS8_RECLASSIFIED_ACTOR_COVERAGE_SUMMARY.csv` — per-actor status after reclassification.
- `csv/PASS8_ACTOR_SCOPE_EVIDENCE_AND_NON_IMPORT_DECISIONS.csv` — actor-level yes/no/adjacent materialbörse decisions where product evidence remains unavailable.
- `csv/PASS8_USER_PROVIDED_URL_STATUS.csv` — exactly how the user-provided URLs were handled.
- `csv/PASS8_SOURCE_EVIDENCE_LEDGER.csv` — trace table with URL, quote, line reference, basis and decision.
- `json_per_actor/*.pass8.reclassification.json` — per-actor machine-readable pass 8 deltas.

## Strict rule applied

A Material/Bauteiltyp row is strict only when the source itself supports the target claim. If the source only says “marketplace/platform/material reuse” without product/category terms, it stays in `scope` or `review_only`.

