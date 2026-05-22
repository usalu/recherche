
# Bauteilbörsen deeper Material + Bauteiltyp pass

Generated: 2026-05-31

This zip is a third pass over all 39 anchors. It keeps the earlier per-anchor JSON structure and adds a material/Bauteiltyp-focused profile to every JSON.

## What changed vs. the previous zip

- Added/confirmed material and Bauteiltyp links where current or historical/secondary sources exposed stronger evidence.
- Added `material_bauteiltyp_profile` to each anchor JSON with confidence-bucketed IDs and explicit component-material pair hints where the source tied a named material to a component.
- Added `MATERIAL_BAUTEILTYP_MATRIX.csv` and `.md` for quick review.
- Added `HISTORY_AND_LIVE_SOURCE_REGISTER.csv` to collect all sources used in this pass and the previous/history URLs preserved from the earlier pass.
- Added `GRAPH_IMPORT_CYPHER_REVIEW_ONLY.cypher` for belegt Material/Bauteiltyp claims only.

## Important caveat

The source rule was treated conservatively: component-only words such as "doors" or "windows" do not become material claims unless a source names the material. For example, `bt_tuer` may be belegt while the material remains unpaired because doors can be wood, steel, glass, aluminum, or mixed.

PruefungNachweis, Aufbereitungsverfahren and Rueckbauverfahren IDs were not invented. Existing search-keyword evidence from the previous pass is retained and still needs graph-side lookup.
