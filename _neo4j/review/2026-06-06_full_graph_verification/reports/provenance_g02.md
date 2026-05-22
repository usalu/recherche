# Provenance report — Agent G2 (catalogue-edge PARTIAL backlog)

**Date:** 2026-06-06 · **Database:** `mit-bestand`  
**Ledger:** [`ledger/provenance_g02.csv`](../ledger/provenance_g02.csv)  
**Scope:** EP-03 / R07 / Q04 actor catalogue edges — `HAT_BAUTEILTYP` + `NUTZT_MATERIAL` with verdict **PARTIAL**

## Summary

| Metric | Count |
|---|---:|
| PARTIAL rows (EP-03 ledger) | **143** |
| HAT_BAUTEILTYP | **83** |
| NUTZT_MATERIAL | **60** |
| Matched in remediation_r07.csv | **143** |
| R07 recovery via actor homepage (`actor_node_source_urls`) | **137** |
| R07 recovery via enrichment JSON | **6** |

## Root cause — which intake created weak `evidence_url` without quotes

**Dossier source (all 143 PARTIAL rows):** enrichment slices in [`bauteilboerse_network_2026-06-01_project_part_actor_edges.json`](../../intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json) — `actor_edge_enrichment_existing_types_2026_06_01` (76), `actor_edge_enrichment_deep_existing_types_2026_06_01` (37), plus smaller `_deep_` / `_deeper_` slices.

**Script that writes `evidence_url` without `evidence_quote` (when import succeeds):**  
[`_neo4j/intake/runs/2026-06-02_bauteilboerse_actor_enrichment_import/_run_import_actor_enrichment_edges.py`](../../intake/runs/2026-06-02_bauteilboerse_actor_enrichment_import/_run_import_actor_enrichment_edges.py) — git `f9cf1a8c`. MERGE sets `evidence_url` + `evidence_basis`, **never** `evidence_quote`; tags `review_status=needs_source_url_review`.

**Why 107/143 still have no graph URL:** catalogue edges already existed on-graph from an earlier baseline network merge (`confidence=0.9`, null `review_run`). The 2026-06-02 importer **skipped** them via parallel-edge prevention (same `type` + actor + target, different `rel.id`). URLs remain in the network JSON slice only — never promoted to `evidence_url` on the live rel.

**Why 36/143 have graph URL but stay PARTIAL:** R07 remediation (`remediation_r07_2026_06_06`) added `evidence_url` + short `evidence_quote` for edges like `articonnex→bt_daemmung`, but EP-03/Q04 strict verbatim gate still fails (classification tokens on page, no edge-specific quote).

**Broader untagged backlog (outside this 143, same family):** 239 live Akteur catalogue edges carry legacy `confidence=0.9` with null `review_run` and no `evidence_url` / `evidence_quote` — baseline `r_{actor}__` merge from the 460-row network JSON slice without `enrichment_run`.

**Draft-only / not the live weak-url source:**  
[`GRAPH_IMPORT_CYPHER_REVIEW_ONLY.cypher`](../../intake/inbox/research/bauteilboersen_deeper_material_bauteiltyp_results/GRAPH_IMPORT_CYPHER_REVIEW_ONLY.cypher) documents URLs in comments but MERGE uses only `{confidence:'belegt'}` — review-only; enrichment JSON is the recoverable quote reservoir.

**Strict counterexample (has quotes):**  
[`IMPORT_SCHEMA_COMPATIBLE_BAUTEILBOERSEN.cypher`](../../intake/inbox/research/FINAL_schema_compatible_bauteilboersen_update_2026-06-01/final_schema_compatible_bauteilboersen_update_2026-06-01/cypher/IMPORT_SCHEMA_COMPATIBLE_BAUTEILBOERSEN.cypher) sets both `evidence_url` and `evidence_quote` from CSV.

## Origin class distribution (143 PARTIAL rows)

| Origin intake / class | Rows |
|---|---:|
| network_json slice actor_edge_enrichment_existing_types_2026_06_01 | 76 |
| network_json slice actor_edge_enrichment_deep_existing_types_2026_06_01 | 37 |
| network_json deep enrichment slice (pre-2026-06-02 import) | 18 |
| network_json slice edge_enrichment_deeper_existing_node_types_2026_06_01 | 8 |
| network_json deeper node-types slice | 4 |

## Weak evidence class

| Class | Rows |
|---|---:|
| url_in_json_no_quote_never_imported_to_graph | 107 |
| partial_despite_some_evidence | 36 |

## Git provenance (head commit per artefact)

| Artefact | `git log -1` |
|---|---|
| `_neo4j/intake/runs/2026-06-02_bauteilboerse_actor_enrichment_import/_run_import_actor_enrichment_edges.py` | f9cf1a8c 2026-06-02 updates |
| `_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json` | f9cf1a8c 2026-06-02 updates |
| `_neo4j/review/2026-06-06_full_graph_verification/_agent_r07_work/remediate_r07.py` | f9cf1a8c 2026-06-02 updates |
| `_neo4j/intake/inbox/research/bauteilboersen_deeper_material_bauteiltyp_results/*.enrichment.json` | f9cf1a8c 2026-06-02 updates |
| `_neo4j/intake/runs/2026-05-31_bauteilboersen_finalest_30/RUN_MIGRATION.cypher` | f9cf1a8c 2026-06-02 updates (strict pass8; not in this 143) |
| `IMPORT_SCHEMA_COMPATIBLE_BAUTEILBOERSEN.cypher` | f9cf1a8c 2026-06-02 updates (counterexample with quotes) |

Older evidence-field churn (pre-consolidation): `d37e5240`, `e9d7f605`, `28cf3919`, `6f183784`, `bd62286a` per [`EVIDENCE_URL_LOCATION_AUDIT.md`](../EVIDENCE_URL_LOCATION_AUDIT.md).

## Remediation trace (R07 → EP-03)

1. Agent 14 `needs_source_url_review` backlog → **R07** ([`ledger/remediation_r07.csv`](../ledger/remediation_r07.csv)): 145 catalogue edges in scope; **143** remain PARTIAL after fetch.
2. R07 applied **137** `ADD_SOURCE` patches ([`patches/remediation_r07_add_rel_sources.patch.jsonl`](../patches/remediation_r07_add_rel_sources.patch.jsonl)) with `review_run=remediation_r07_2026_06_06`.
3. EP-03 element proof re-adjudicated the same 143 as PARTIAL ([`ledger/element_proof_agent_03.csv`](../ledger/element_proof_agent_03.csv)); Q04 later downgraded 13 overlapping rows to `evidence_confidence=niedrig` ([`ledger/post_quality_p06_01.csv`](../ledger/post_quality_p06_01.csv)).

## Enrichment JSON crosswalk

Per-actor `*.enrichment.json` under [`bauteilboersen_deeper_material_bauteiltyp_results`](../../intake/inbox/research/bauteilboersen_deeper_material_bauteiltyp_results/) holds recoverable `evidence_urls` + `evidence_quote` for many actors. R07 used these where dossier rows exist; **137/143** PARTIAL rows fell back to **actor `primary_source_url` / `source_urls`** (homepage), which fails the strict verbatim quote gate.

## Recommended recovery order

1. Re-import quotes from matching `*.enrichment.json` / `*.finalest.evidence.json` where `target_id` matches.
2. For `r_deep_*` / baseline `confidence=0.9` rows, either prove from enrichment dossier or delete (Q04 pattern).
3. Do not treat `2026-06-02` importer `evidence_url`-only edges as PROVEN without adding `evidence_quote`.
