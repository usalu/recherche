# Schema-compatible Bauteilbörsen update

Generated: 2026-06-01  
Input ZIP: `bauteilboersen_swiss_bauteilboersen_added_2026-06-01`  
Schema: `BAUTEILBOERSE_SUBGRAPH_SCHEMA.md`

## What changed

1. Filtered the Swiss-additions evidence table to your closed `Material` and `Bauteiltyp` vocabularies.
2. Removed 6 off-vocabulary material edges from graph-import tables:
   - `mat_metall` x 3
   - `mat_baumaterial_unspecified` x 3
3. Kept the removed rows in `csv/OFF_VOCAB_REVIEW_ROWS_DO_NOT_IMPORT.csv` with a recommendation for each row.
4. Added two schema-fit web-discovery candidates:
   - `salza` — promote from related-only to core digital marketplace, but no strict material/type rows yet.
   - `baumatpool_ch` — new marketplace candidate with first-party category/listing evidence mapped to closed vocabulary IDs.
5. Generated Neo4j-oriented import CSVs and a Cypher import script.

## Import-ready files

- `csv/GRAPH_IMPORT_ACTORS_REQUIRED_EDGES.csv` — anchors and required schema edges.
- `csv/GRAPH_IMPORT_STRICT_MATERIAL_BAUTEILTYP_EDGES.csv` — only closed-vocabulary strict `NUTZT_MATERIAL` / `HAT_BAUTEILTYP` rows.
- `cypher/IMPORT_SCHEMA_COMPATIBLE_BAUTEILBOERSEN.cypher` — load script using precomputed `q_url_<md5>` IDs; APOC is not required.

## Review files

- `csv/OFF_VOCAB_REVIEW_ROWS_DO_NOT_IMPORT.csv` — facts found in sources but blocked by schema vocabulary.
- `csv/WEB_DISCOVERY_SOURCE_NOTES_SALZA_BAUMATPOOL.csv` — source notes for the two added candidates.
- `csv/SCHEMA_COMPATIBLE_ACTOR_DECISIONS_WITH_NEW_CANDIDATES.csv` — cleaned actor decision table with the two candidate additions.
- `csv/SCHEMA_COMPATIBLE_STRICT_MATERIAL_BAUTEILTYP_EVIDENCE.csv` — cleaned evidence table plus strict Baumatpool rows.

## Important caveats

- `mat_metall` is intentionally not imported because your schema has no generic metal material ID. Use `mat_stahl`, `mat_aluminium`, or `mat_gusseisen` only when the first-party source literally supports the specific material.
- `mat_baumaterial_unspecified` is intentionally not imported because generic “Baumaterial/Baustoffe” is not a material class in the closed set.
- Several ZIP actors have only one evidence URL in the source package. The Cypher validation will flag these as `MISSING_REQUIRED` until a second operator-controlled evidence URL is added.
- Geschäftsmodell and Marktmodell mappings in `GRAPH_IMPORT_ACTORS_REQUIRED_EDGES.csv` are suggested from actor kind/source text. Review before production import.
