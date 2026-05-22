# Comparison: pass 8 ZIP vs final markdown report

Compared files:
- Last ZIP: `bauteilboersen_reclassification_pass_8_2026-05-31.zip`
- Final markdown report: `final_bauteilboersen_final_report.md`

## Main finding
The last ZIP (`PASS8_RECLASSIFIED_ACTOR_COVERAGE_SUMMARY.csv` and strict/review CSVs) is more reliable than the final markdown report. The markdown report is a readable narrative summary, but it is not a safe import/control file because it omits several actors, contains one duplicate row, and sometimes turns review-only evidence into “verified” evidence.

## Counts
- Pass 8 actors: 39
- Final report table rows: 34
- Unique mapped final-report actors: 33
- Missing pass8 actors in final report: 6
- Duplicate final-report mapped actors: 1

## Missing from final markdown but present in pass 8
- `backacia`
- `batrecup`
- `enviromate`
- `materialrest24`
- `r_place`
- `salvoweb`

## Duplicate in final markdown
- `building_spares_market` appears as: Building Spares Market (UK), Building Spare Market (already covered)

## Actors where markdown overstates review-only evidence
- `articonnex` — Final report presents Articonnex materials/categories as verified, but pass8 has zero strict rows; all claims are review-only.
- `baticycle` — Pass8 supports 6 Bauteiltyp rows strictly but no strict material rows; final report lists materials, so material part should be review-only.
- `bauteilboerse_bremen` — Pass8 has zero strict rows for Bremen; final report labels categories/materials as verified. It should remain review-only unless product/listing rows are separately promoted.
- `genbyg` — Pass8 strict supports mat_glas and three BT; wood/brick materials are review-only. Final report lists oak/beech/bricks as verified.
- `insert_marketplace` — Pass8 has zero strict rows and only review BT; final report presents categories/materials as verified.
- `material_index` — Pass8 strict supports 5 Bauteiltyp rows but no strict materials; final report lists materials as verified.
- `materialenbank_leuven_atelier_circuler` — Pass8 has zero strict rows and many review rows; final report treats them as verified.
- `rotordc` — Pass8 strict has only mat_keramik; BT and other materials are review-only. Final report presents broad shop categories/materials as verified.
- `surplus_building_and_plumbing_materials` — Pass8 has zero strict rows; final report treats accepted/category list as verified materials/types. Keep as scope/review-only unless product URLs are added.
- `sustainability_yard` — Pass8 has zero strict rows; final report treats accepted-material list as verified inventory. Keep as scope/review-only.
- `useagain_bauteilclick` — Pass8 strict: mat_stahl, bt_fenster, bt_technik. Final report presents broad eBKP-H categories/materials as verified; most are review-only.

## Actors where markdown under-reports pass8 strict evidence
- `bauteilladen_winterthur` — Pass8 strict: mat_holz, mat_naturstein and bt_fenster. Final report emphasizes plastic windows, which is not in pass8 strict, and omits strict natural stone.
- `material_reuse_portal` — Pass8 has one strict bt_dach row from an aggregated product page; final report says no direct categories. Actor role as aggregator is correct, but the strict product row should be retained.
- `re_store_harvestmap_vienna` — Pass8 strict has 4 material IDs and 2 BT IDs; final report only keeps concrete/Betonsteine.
- `reempro` — Pass8 strict has mat_keramik, mat_ziegel and 8 BT. Final report says materials not specified.
- `reuse_and_trade` — Pass8 has two strict BT rows from listing evidence; final report says no product categories could be verified.

## Recommended source of truth
Use the pass 8 ZIP strict CSV as the source of truth for import-ready evidence. Use the final markdown only as a human-readable draft after correcting the mismatches above.