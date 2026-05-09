# Manual Review Playbook

Work one node at a time. Nothing in this folder is imported automatically.

## Decision Options

- approve_move: move to one clean typed path.
- approve_split: split into multiple exact typed paths.
- merge_into_existing: merge evidence into an existing clean node.
- keep_review: leave unresolved.
- delete_from_final: do not import as semantic node.

## Files

- Node impact: _migration/25_manual_review_node_impact.csv
- Decision template: _migration/25_manual_review_decision_template.csv
- Held edges: _database/_edges/clean_edge_review_queue.csv

## First Nodes To Review

| node | held edges | class | recommended decision logic |
|---|---:|---|---|
| material/Metall | 46 | broad_material_fallback | Do not approve as clean material unless exact metal is unknown and source truly says only Metall. Prefer Stahl, Aluminium, Sekundaerstahl, or keep edge in review. |
| huerde/Performance_Nachweis | 33 | broad_barrier_fallback | Separate barrier from proof: use huerde/Technische_Freigabe or pruefung_nachweis/leistungsanforderung node. |
| bauteiltyp/Tragstruktur | 28 | wrong_scale_or_structural_system | Resolve to specific bauteiltyp, tragwerkstyp, or tragwerksprinzip; avoid generic component import. |
| bauteiltyp/Bauwerksteil | 27 | wrong_scale_or_structural_system | Resolve to bauobjekt, bauobjektrolle, or a precise bauteiltyp depending on source scale. |
| huerde/Logistikproblem | 20 | broad_barrier_fallback | Resolve to concrete hurdle such as Terminunsicherheit, Fehlende_Lagerflaeche, Verfuegbarkeitsproblem, or keep review. |
| bauteiltyp/Fliese | 16 | component_scope_unclear | Resolve as bauteiltyp/Boden or bauteiltyp/Wand plus material/Keramik if context is clear. |
| bauteiltyp/Kueche | 8 | component_scope_unclear | Usually fit-out: prefer bauteiltyp/Festes_Einbauteil or boundary logic if furniture/non-direct-reuse. |
| bauteiltyp/Landschaftselement | 8 | component_scope_unclear | Review source text and map to strongest real-world type before import. |
| bauteiltyp/Bruestung | 7 | component_scope_unclear | Resolve to bauteiltyp/Gelaender, Fassade, or parapet-like component based on case context. |
| bauteiltyp/Kern | 5 | wrong_scale_or_structural_system | Usually structural core: prefer tragwerkstyp/tragwerksprinzip or precise component if source is concrete. |
| datenpunkt/Timber_Square_London__001__Wiederverwendete_Stahltr_ger | 5 | datapoint_conflicts_with_reuse_item | Do not import as datenpunkt until it is converted to a measured value with unit/scope. |
| datenpunkt/ELYS_Kultur_Gewerbehaus_Basel__003__Fenster | 4 | datapoint_conflicts_with_reuse_item | Do not import as datenpunkt until it is converted to a measured value with unit/scope. |
| material/Guss | 4 | ambiguous_material_or_boundary | Resolve to Gusseisen, Stahlguss, or another exact material; otherwise keep in review. |
| material/Erde | 3 | ambiguous_material_or_boundary | Resolve to Lehm when construction-earth context is clear; otherwise keep source label only. |
| bauteiltyp/Auflager_Widerlager | 2 | component_scope_unclear | Review source text and map to strongest real-world type before import. |

## Rule

A node may enter _database only when its entity type is unambiguous and the target path follows entity/id.
