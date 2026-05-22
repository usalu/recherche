# Finalest Bauteilbörsen Evidence Package
This package supersedes the prior standalone markdown report. The source of truth is the CSV/JSON evidence ledger built from pass 8 plus pass 7 review evidence.
## Import rule
- Import only rows in `csv/FINAL_IMPORT_SAFE_MATERIAL_BAUTEILTYP_CLAIMS.csv`.
- Treat `csv/FINAL_REVIEW_ONLY_MATERIAL_BAUTEILTYP_CLAIMS.csv` as research evidence that still needs stronger product/detail/category proof.
- Treat `csv/FINAL_SCOPE_ONLY_ACTOR_EVIDENCE.csv` as actor-role evidence, not Material/Bauteiltyp facts.

## Summary
- Actors covered: **39**
- Actors with strict Material/Bauteiltyp evidence: **18**
- Actors with review-only Material/Bauteiltyp evidence: **15**
- Actors with scope-only evidence: **6**
- Actors with no public evidence captured in this package: **0**
- Strict import-safe rows: **150**
- Review-only rows retained after removing strict promotions: **235**
- Scope-only actor evidence rows: **10**

## Actor status table
| Actor | Status | Strict Materials | Strict Bauteiltypen | Review Materials | Review Bauteiltypen | Follow-up |
|---|---|---|---|---|---|---|
| `articonnex` | REVIEW_ONLY_EVIDENCE_AVAILABLE | — | — | mat_daemmstoff;mat_holz;mat_kunststoff | bt_ausbau;bt_boden;bt_daemmung;bt_fassade | only review evidence, not import-safe |
| `backacia` | REVIEW_ONLY_EVIDENCE_AVAILABLE | — | — | mat_holz;mat_kunststoff | bt_boden;bt_tuer | only review evidence, not import-safe |
| `baticycle` | STRICT_EVIDENCE_AVAILABLE | — | bt_ausbau;bt_boden;bt_decke;bt_technik;bt_tuer;bt_wand | — | — | no evidence captured |
| `batiterre` | STRICT_EVIDENCE_AVAILABLE | mat_glas;mat_gusseisen;mat_holz;mat_kunststoff;mat_ziegel | bt_ausbau;bt_boden;bt_dach;bt_daemmung;bt_fenster;bt_gelaender;bt_technik;bt_treppe;bt_tuer;bt_wand | mat_keramik;mat_naturstein | — | strict evidence present; review rows still available |
| `batrecup` | REVIEW_ONLY_EVIDENCE_AVAILABLE | — | — | mat_holz | bt_fenster;bt_tuer | only review evidence, not import-safe |
| `baukarussell` | STRICT_EVIDENCE_AVAILABLE | mat_glas;mat_holz | bt_boden;bt_dach;bt_fassade;bt_fenster;bt_technik;bt_tuer;bt_wand | — | — | no evidence captured |
| `bauteilboerse_bremen` | REVIEW_ONLY_EVIDENCE_AVAILABLE | — | — | mat_glas;mat_holz;mat_keramik;mat_kunststoff;mat_naturstein;mat_stahl | bt_ausbau;bt_boden;bt_dach;bt_fassade;bt_fenster;bt_technik;bt_treppe;bt_tuer;bt_wand | only review evidence, not import-safe |
| `bauteilladen_winterthur` | STRICT_EVIDENCE_AVAILABLE | mat_holz;mat_naturstein | bt_fenster | — | bt_boden;bt_technik;bt_treppe;bt_tuer | strict evidence present; review rows still available |
| `bauteilnetz_deutschland` | STRICT_EVIDENCE_AVAILABLE | mat_keramik;mat_ziegel | bt_boden;bt_dach | mat_holz | bt_fenster;bt_technik;bt_tuer;bt_wand | strict evidence present; review rows still available |
| `building_spares_market` | STRICT_EVIDENCE_AVAILABLE | mat_aluminium;mat_beton;mat_daemmstoff;mat_glas;mat_holz;mat_stahl;mat_ziegel | bt_boden;bt_dach;bt_daemmung;bt_fenster;bt_traeger;bt_tuer;bt_wand | — | — | no evidence captured |
| `cornermat_retrival` | STRICT_EVIDENCE_AVAILABLE | mat_glas;mat_holz;mat_keramik;mat_ziegel | bt_dach;bt_fenster;bt_technik;bt_tuer;bt_wand | mat_daemmstoff | bt_boden;bt_daemmung | strict evidence present; review rows still available |
| `cycle_up` | REVIEW_ONLY_EVIDENCE_AVAILABLE | — | — | mat_glas;mat_kunststoff | bt_fenster | only review evidence, not import-safe |
| `cycle_zero` | REVIEW_ONLY_EVIDENCE_AVAILABLE | — | — | mat_daemmstoff;mat_holz | bt_boden;bt_daemmung;bt_fenster;bt_technik;bt_tuer | only review evidence, not import-safe |
| `enviromate` | STRICT_EVIDENCE_AVAILABLE | mat_keramik | bt_boden | mat_daemmstoff;mat_holz | bt_daemmung;bt_treppe;bt_tuer | strict evidence present; review rows still available |
| `gebruiktebouwmaterialen` | STRICT_EVIDENCE_AVAILABLE | mat_aluminium;mat_daemmstoff;mat_holz;mat_kunststoff;mat_stahl;mat_ziegel | bt_boden;bt_dach;bt_daemmung;bt_fenster;bt_technik;bt_traeger;bt_treppe;bt_tuer;bt_wand | — | — | no evidence captured |
| `genbyg` | STRICT_EVIDENCE_AVAILABLE | mat_glas | bt_fenster;bt_technik;bt_tuer | mat_holz;mat_keramik | bt_boden | strict evidence present; review rows still available |
| `globechain` | SCOPE_ONLY_NO_MATERIAL_BT_CLAIMS | — | — | — | — | scope only, no Material/Bauteiltyp claim |
| `insert_marketplace` | REVIEW_ONLY_EVIDENCE_AVAILABLE | — | — | — | bt_fenster;bt_tuer | only review evidence, not import-safe |
| `loopfront` | SCOPE_ONLY_NO_MATERIAL_BT_CLAIMS | — | — | — | — | scope only, no Material/Bauteiltyp claim |
| `material_index` | STRICT_EVIDENCE_AVAILABLE | — | bt_ausbau;bt_boden;bt_technik;bt_tuer;bt_wand | mat_holz;mat_stahl;mat_ziegel | — | strict evidence present; review rows still available |
| `material_reuse_portal` | STRICT_EVIDENCE_AVAILABLE | — | bt_dach | mat_glas;mat_holz;mat_stahl | bt_boden;bt_decke;bt_fenster;bt_technik;bt_treppe;bt_tuer;bt_wand | strict evidence present; review rows still available |
| `materialenbank_leuven_atelier_circuler` | REVIEW_ONLY_EVIDENCE_AVAILABLE | — | — | mat_daemmstoff;mat_holz;mat_keramik;mat_kunststoff;mat_naturstein;mat_stahl | bt_boden;bt_daemmung;bt_fassade;bt_fenster;bt_technik;bt_traeger;bt_tuer;bt_wand | only review evidence, not import-safe |
| `materialrest24` | REVIEW_ONLY_EVIDENCE_AVAILABLE | — | — | mat_holz | bt_ausbau;bt_dach;bt_technik;bt_wand | only review evidence, not import-safe |
| `new_horizon` | REVIEW_ONLY_EVIDENCE_AVAILABLE | — | — | mat_beton | bt_dach;bt_fassade | only review evidence, not import-safe |
| `r_place` | REVIEW_ONLY_EVIDENCE_AVAILABLE | — | — | — | bt_technik | only review evidence, not import-safe |
| `raedificare` | SCOPE_ONLY_NO_MATERIAL_BT_CLAIMS | — | — | — | — | scope only, no Material/Bauteiltyp claim |
| `re_store_harvestmap_vienna` | STRICT_EVIDENCE_AVAILABLE | mat_beton;mat_holz;mat_keramik;mat_naturstein | bt_boden;bt_dach | — | — | no evidence captured |
| `reempro` | STRICT_EVIDENCE_AVAILABLE | mat_keramik;mat_ziegel | bt_ausbau;bt_boden;bt_daemmung;bt_decke;bt_fenster;bt_technik;bt_tuer;bt_wand | — | — | no evidence captured |
| `resource_marktplaats` | SCOPE_ONLY_NO_MATERIAL_BT_CLAIMS | — | — | — | — | scope only, no Material/Bauteiltyp claim |
| `reuse_and_trade` | STRICT_EVIDENCE_AVAILABLE | — | bt_boden;bt_tuer | mat_holz;mat_stahl | bt_gelaender;bt_technik;bt_treppe | strict evidence present; review rows still available |
| `rotordc` | STRICT_EVIDENCE_AVAILABLE | mat_keramik | — | mat_aluminium;mat_daemmstoff;mat_holz;mat_kunststoff;mat_naturstein;mat_stahl | bt_ausbau;bt_boden;bt_dach;bt_daemmung;bt_fassade;bt_technik;bt_treppe;bt_tuer;bt_wand | strict evidence present; review rows still available |
| `salvoweb` | REVIEW_ONLY_EVIDENCE_AVAILABLE | — | — | — | bt_tuer | only review evidence, not import-safe |
| `salza` | SCOPE_ONLY_NO_MATERIAL_BT_CLAIMS | — | — | — | — | scope only, no Material/Bauteiltyp claim |
| `skop_marketplace` | REVIEW_ONLY_EVIDENCE_AVAILABLE | — | — | mat_daemmstoff;mat_holz | bt_ausbau;bt_boden;bt_dach;bt_daemmung;bt_technik;bt_tuer;bt_wand | only review evidence, not import-safe |
| `software_restado` | STRICT_EVIDENCE_AVAILABLE | mat_holz;mat_keramik | bt_boden;bt_dach;bt_tuer;bt_wand | — | — | no evidence captured |
| `surplus_building_and_plumbing_materials` | REVIEW_ONLY_EVIDENCE_AVAILABLE | — | — | mat_daemmstoff;mat_holz;mat_ziegel | bt_dach;bt_daemmung;bt_technik;bt_wand | only review evidence, not import-safe |
| `sustainability_yard` | REVIEW_ONLY_EVIDENCE_AVAILABLE | — | — | mat_daemmstoff;mat_holz;mat_naturstein;mat_ziegel | bt_ausbau;bt_boden;bt_dach;bt_daemmung;bt_fassade;bt_fenster;bt_technik;bt_traeger;bt_tuer;bt_wand | only review evidence, not import-safe |
| `useagain_bauteilclick` | STRICT_EVIDENCE_AVAILABLE | mat_stahl | bt_fenster;bt_technik | mat_glas;mat_holz;mat_keramik;mat_kunststoff | bt_tuer | strict evidence present; review rows still available |
| `warp_it` | SCOPE_ONLY_NO_MATERIAL_BT_CLAIMS | — | — | — | — | scope only, no Material/Bauteiltyp claim |

## Notes on important corrections
- `baukarussell`, `building_spares_market`, `gebruiktebouwmaterialen`, and `re_store_harvestmap_vienna` were reclassified out of the old “no closed-set evidence” group because product/listing evidence was found.
- `material_reuse_portal`, `salza`, `raedificare`, `resource_marktplaats`, `globechain`, `loopfront`, and similar actors may be legitimate reuse/aggregator/software actors, but their public pages do not always prove actor-owned stock categories. Use scope-only or review-only evidence accordingly.
- The earlier `final_bauteilboersen_final_report.md` is not used as a source of truth because it omitted actors and over/under-reported multiple pass-8 claims. See `docs/PRIOR_MARKDOWN_REPORT_COMPARISON_SUMMARY.md`.
