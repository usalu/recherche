# Donor / Receiver Source Research Round 004

## Scope

Input: `donor_receiver_candidates.json` from Round 003 with 49 candidates:

- 48 `missing_donor`
- 1 `missing_receiver`

This round checked the uploaded markdown source files and produced a patch file that can be applied by the Neo4j import agent.

## Main result

| metric | count |
|---|---:|
| candidates reviewed | 49 |
| source files available in uploaded corpus | 34 |
| source files missing / deferred | 15 |
| patch operations produced | 131 |
| controlled terms proposed | 8 |

## Resolution status counts

| status | count |
|---|---:|
| borrowed_pool | 4 |
| exact_building | 1 |
| not_applicable_retention | 1 |
| resource_source | 22 |
| same_site | 3 |
| unknown | 18 |


## Patch operation counts

| op | count |
|---|---:|
| add_node | 3 |
| add_rel | 59 |
| noop_reviewed | 20 |
| set_property | 49 |


## Key modelling decisions

1. Exact `AUS_BAUWERK` relationships were added only where the source file gives a sufficiently clear donor object, for example Gorlaeus-Hochhaus for BioPartner floor materials, Tropicana for BlueCity concrete blocks, the CRCLR Bestandshalle for roof steel, and the ELYS former beverage-storage / roof-build-up source for trapezoidal sheet.
2. If the source confirms reuse but does not identify a donor building, the Bauteilgruppe is resolved through `HAT_RESSOURCENQUELLE` and `donor_resolution_status = resource_source`, not through a fake donor node.
3. Borrowed temporary material in People’s Pavilion is resolved as `borrowed_pool` with `HAT_RESSOURCENQUELLE -> rq_borrowed_material_pool` and `HAT_BESCHAFFUNGSWEG -> bweg_leihmodell`.
4. Retained existing elements are not treated as missing donors. They receive `donor_resolution_status = not_applicable_retention`.
5. Source files that were not in the uploaded corpus are deferred with `noop_reviewed`; no external assumptions were turned into graph facts.

## Files

- `controlled_terms/controlled_terms.delta.jsonl` — add these controlled terms before applying the patch.
- `patches/donor_receiver_source_research.patch.jsonl` — all patch operations.
- `reviews/donor_receiver_research_results.jsonl` — human-readable research decision per candidate.
- `cypher/post_patch_donor_receiver_review.cypher` — query to re-check unresolved candidates after import.
