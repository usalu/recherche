# Pass 8 Change Log and Decisions

## Reclassified from no closed-set evidence to strict import candidates

- `baukarussell`
- `building_spares_market`
- `gebruiktebouwmaterialen`
- `re_store_harvestmap_vienna`

## Partly promoted / strengthened

- `material_index`: Bauteiltyp category evidence promoted from review to strict; material examples kept review-only because they are “recent requests”, not confirmed stock.
- `enviromate`: first-party listing for Metro Tiles is strict; broader material/type list from ReLondon is review-only.
- `new_horizon`: product-overview snippets are review-only until a full first-party product page is fetched.
- `batrecup`: marketplace/app scope and examples found, but no public catalogue row.

## Confirmed materialbörse/platform, but no strict public Material/Bauteiltyp inventory in this pass

- `raedificare`
- `resource_marktplaats`
- `salza`
- `loopfront`
- `material_reuse_portal`
- `globechain`

## Reclassified as adjacent rather than core bauteilbörse

- `warp_it`: redistribution system for surplus furniture/equipment/resources; not primarily a construction-component materialbörse.

## Important conservative decisions

- `re_store_harvestmap_vienna` / Betonsteine: imported `mat_beton`; did **not** import `bt_wand`, `bt_boden`, or `bt_fundament` because the page title alone does not identify intended use.
- `building_spares_market` / chipboard advert URL: direct fetch timed out; not used for strict evidence. First-party homepage/about pages were used instead.
- Category trees are accepted for strict `HAT_BAUTEILTYP` and exact material labels when the category is clearly part of a shop/marketplace inventory.
- Third-party profiles are review-only unless they quote or clearly profile the actor’s portfolio and there is no first-party product page.
