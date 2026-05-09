# Phase 28 Material Metall Review Decision

## Decision

Keep material/Metall out of the clean database.

Reason: Metall is a broad fallback label, not a clean material knot. Use exact material nodes such as material/Stahl, material/Aluminium, material/Glas, material/Holz, material/Keramik, or material/Kunststoff when known.

## Database Change

No database nodes or clean edges were added. The decision is recorded in the manual decision template and in the edge decision CSV.

## Counts

- Held material/Metall edges reviewed: 46

| decision | rows |
|---|---:|
| partial_exact_materials_already_imported_keep_metal_unknown | 27 |
| keep_review_exact_metal_unknown | 16 |
| resolved_by_existing_exact_material | 3 |

## Sample Rows

| raw label | existing clean material edges | decision |
|---|---|---|
| Metall |  | keep_review_exact_metal_unknown |
| Metall |  | keep_review_exact_metal_unknown |
| Metall |  | keep_review_exact_metal_unknown |
| Metall |  | keep_review_exact_metal_unknown |
| Metall |  | keep_review_exact_metal_unknown |
| Metall |  | keep_review_exact_metal_unknown |
| Metall |  | keep_review_exact_metal_unknown |
| Metall |  | keep_review_exact_metal_unknown |
| Metall |  | keep_review_exact_metal_unknown |
| Metall |  | keep_review_exact_metal_unknown |
| Metall |  | keep_review_exact_metal_unknown |
| Metall / Technik |  | keep_review_exact_metal_unknown |

## Output

- _migration/28_material_metall_edge_review_decisions.csv
