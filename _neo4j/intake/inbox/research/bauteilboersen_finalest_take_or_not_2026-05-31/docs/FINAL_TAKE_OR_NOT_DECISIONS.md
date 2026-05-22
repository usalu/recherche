# Final take / do-not-take decision

Use this file as the simplified decision layer. It answers whether to keep each actor in the research dataset and whether to import exact Material/Bauteiltyp claims from the current evidence.

## Counts
- TAKE: 30
- TAKE AS RELATED ONLY: 7
- DO NOT TAKE: 2
- TAKE with exact Material/Bauteiltyp import: 16
- TAKE actor only, no exact claim import yet: 14

## Rule
- TAKE = keep in the Bauteilbörse / construction-material reuse dataset.
- TAKE AS RELATED ONLY = keep only if your scope includes digital tools, aggregators, apps, or urban-mining services; do not use as a direct stockholding Bauteilbörse.
- DO NOT TAKE = exclude from the Bauteilbörse dataset unless your scope is much broader than construction-material reuse.
- material_bauteiltyp_claims_to_import=YES means use only the strict rows from FINAL_IMPORT_SAFE_MATERIAL_BAUTEILTYP_CLAIMS.csv.

## TAKE
| Actor | Actor kind | Import exact Material/Bauteiltyp? | Reason |
|---|---|---:|---|
| `articonnex` | core marketplace/shop | NO | Relevant construction-material reuse/outlet actor; current exact material/type rows are not strict enough. |
| `backacia` | core marketplace/shop | NO | Relevant reuse marketplace; needs stronger product-level evidence before importing exact material/type claims. |
| `baticycle` | core marketplace/shop | YES | Strict public evidence for building-component categories. |
| `batiterre` | core marketplace/shop | YES | Strict public evidence for multiple materials and Bauteiltypen. |
| `batrecup` | core marketplace/app | NO | Core construction-material reuse app/catalogue, but exact material/type claims need stronger public product evidence. |
| `baukarussell` | core marketplace/shop | YES | Live catalogue/product evidence supports reuse materials and building-component categories. |
| `bauteilboerse_bremen` | core marketplace/shop | NO | Clearly relevant Bauteilbörse; current rows should be rechecked at product/detail level before exact import. |
| `bauteilladen_winterthur` | core marketplace/shop | YES | Strict evidence available for material/type claims. |
| `bauteilnetz_deutschland` | network/catalogue | YES | Product/detail pages prove exact material/type claims; network/catalgoue role is in scope. |
| `building_spares_market` | core marketplace/shop | YES | Strict first-party product/category evidence available. |
| `cornermat_retrival` | core marketplace/shop | YES | Strict first-party shop/listing evidence available. |
| `cycle_up` | core platform/marketplace | NO | Relevant reuse marketplace/platform; exact material/type claims need stronger public product evidence. |
| `cycle_zero` | app/platform | NO | Relevant app for construction-site materials; no safe exact public material/type import yet. |
| `enviromate` | core marketplace/shop | YES | Strict public listing evidence exists, though coverage is limited. |
| `gebruiktebouwmaterialen` | core marketplace/shop | YES | Strict category/product evidence available. |
| `genbyg` | core marketplace/shop | YES | Strict product/category evidence available. |
| `insert_marketplace` | core platform/marketplace | NO | Relevant circular construction-material platform; exact material/type claims need stronger product-level proof. |
| `material_index` | core marketplace/index | YES | Strict category-level construction component evidence available. |
| `materialenbank_leuven_atelier_circuler` | core material bank | NO | Relevant material bank; exact material/type claims need product-level confirmation. |
| `materialrest24` | core marketplace/shop | NO | Relevant materials surplus/reuse actor; exact claims need stronger direct evidence. |
| `r_place` | core marketplace/shop | NO | Relevant catalogue/marketplace; exact claims should be verified at product-level before import. |
| `re_store_harvestmap_vienna` | core marketplace/shop | YES | Strict product pages prove materials/types. |
| `reempro` | core marketplace/shop | YES | Strict category/product evidence available. |
| `rotordc` | core marketplace/shop | YES | Strict product evidence exists; additional broad claims remain review-only. |
| `salvoweb` | core marketplace/directory | NO | Relevant reuse marketplace/directory, but exact material/type evidence is too thin. |
| `skop_marketplace` | marketplace/aggregator | NO | Relevant marketplace for reuse materials; exact claims need product-level proof before import. |
| `software_restado` | core marketplace/shop | YES | Strict product/category evidence available. |
| `surplus_building_and_plumbing_materials` | core marketplace/shop | NO | Relevant building-material surplus actor; current evidence is category/scope rather than strict product-level import. |
| `sustainability_yard` | core marketplace/shop | NO | Relevant reclaimed/surplus building-material marketplace; current evidence mostly accepted-scope/category. |
| `useagain_bauteilclick` | core marketplace/shop | YES | Strict category/listing evidence available. |

## TAKE_AS_RELATED_ONLY
| Actor | Actor kind | Import exact Material/Bauteiltyp? | Reason |
|---|---|---:|---|
| `globechain` | broad reuse platform with construction vertical | NO | Relevant to reuse ecosystem but not a construction-specific public Bauteilbörse for exact claims. |
| `loopfront` | reuse software/platform | NO | Useful as digital reuse infrastructure, not a public materialbörse with stock categories. |
| `material_reuse_portal` | aggregator/search portal | NO | Take as aggregator; do not treat materials/types as its own stock. |
| `new_horizon` | urban mining/material supplier | NO | Relevant urban-mining reuse actor; no public marketplace-style exact material/type import yet. |
| `raedificare` | professional reuse marketplace/platform | NO | Relevant marketplace platform but catalogue is not open enough for exact public material/type claims. |
| `resource_marktplaats` | construction-materials app | NO | Relevant app/platform, but no public product categories for exact import. |
| `salza` | bauteil platform | NO | Relevant platform for reuse, but no open exact material/type categories. |

## DO_NOT_TAKE
| Actor | Actor kind | Import exact Material/Bauteiltyp? | Reason |
|---|---|---:|---|
| `reuse_and_trade` | general surplus/non-construction evidence | NO | Current evidence is furniture/general surplus, not clean construction-component reuse. |
| `warp_it` | general resource redistribution platform | NO | Adjacent reuse platform; not a core construction-material Bauteilbörse. |
