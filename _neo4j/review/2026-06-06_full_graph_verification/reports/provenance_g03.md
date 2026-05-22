# Git Provenance — Agent G3 (PARTIAL geo & participation edges)

**Date:** 2026-06-06  
**Scope:** `verdict=PARTIAL` on `BETEILIGT_AN`, `LIEGT_IN_LAND`, `LIEGT_IN_STADT` in `VERIFICATION_LEDGER_ELEMENT.csv`  
**Row count:** **622** element-ledger rows → **13** provenance clusters  
**Ledger:** [`ledger/provenance_g03.csv`](ledger/provenance_g03.csv)  
**Cross-check:** [`ledger/agent_09.csv`](ledger/agent_09.csv) · [`_agent_09_build.py`](../_agent_09_build.py)  

---

## 1. Executive summary

Agent 09 flagged **751 PARTIAL** rows shard-wide; **622** fall in this G3 scope (geo + actor participation). The dominant failure mode is **not graph fabrication** but **evidence-channel degradation**: (a) **335** `LIEGT_IN_LAND` edges on organisational nodes with no address — structurally imported, honestly unconfirmable; (b) **197** `BETEILIGT_AN` actor→project links present in `akteur_typ_projekt_geo.json` but citing **placeholder `source_url` tokens** (`processed`, `archive`, empty) from the 2026-06-06 geo extract; (c) **63** actor→`Bauteilgruppe` `BETEILIGT_AN` edges from the **2026-06-01 project_part_actor import** (`import_all_for_now` policy, `evidence_confidence=abgeleitet`); (d) **27** `LIEGT_IN_STADT` benign native-name / missing-address partials.

Git first introduction of the weak-evidence import path: commit **`f9cf1a8c`** (2026-06-02) — `_run_import_all.py` + inbox JSON. Structural `LIEGT_IN_*` on actors: commit **`19e55129`** (2026-05-20) — `2026-05-20_inbox_batch2_import`. Geo property backfill: commit **`ed1d81d9`** (2026-06-06) — `apply_geo_import.py`.

## 2. Scope breakdown

| Rel type | PARTIAL rows |
|---|---:|
| `LIEGT_IN_LAND` | 335 |
| `BETEILIGT_AN` | 260 |
| `LIEGT_IN_STADT` | 27 |

## 3. Root-cause buckets

| Bucket | Rows | Origin run | Primary artifact |
|---|---:|---|---|
| `organisational_node_no_geo_address` | 335 | 2026-05-20_inbox_batch2_import / actor_registry | `pre-geo structural LIEGT_IN_* (no address on Akteur/Software/Programm)` |
| `placeholder_geo_source_token` | 197 | pre-2026-06-06_inbox_dossier_import | `_neo4j/review/2026-06-06_project_bg_geo_extract/akteur_typ_projekt_geo.json` |
| `shared_material_inference_import` | 63 | 2026-06-01_bauteilboerse_edge_enrichment | `_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json` |
| `missing_address_on_node` | 26 | pre-2026-06-06_inbox_dossier_import | `structural LIEGT_IN_STADT without node.adresse` |
| `geo_extract_placeholder_or_unconfirmed` | 1 | 2026-06-06_project_bg_geo_extract | `_neo4j/review/2026-06-06_project_bg_geo_extract/apply_geo_import.py` |

## 4. Agent 09 ledger trace

All **622** scoped rows carry `source_agent=09` (or `09+F08+…` for the 63 inference relabel cluster). Agent 09 adjudicated using:

- `_neo4j/review/2026-06-06_project_bg_geo_extract/akteur_typ_projekt_geo.json` — actor→project participation + `source_url`
- `reuse_geo_graph.json` / `donor_bauwerke_addresses.json` — donor/receiver chains
- `_agent_09_build.py` (commit per git blame on file head)

Key agent_09 proof-quote → git-origin mapping:

| proof_quote pattern | Rows | Git-introduced by |
|---|---:|---|
| `country_unconfirmed_no_address` | 335 | ``  `pre-geo structural LIEGT_IN_* (no address on Akteur/Software/Programm)` |
| `placeholder_source:empty` | 152 | `ed1d81d9b5be` 2026-06-06 `_neo4j/review/2026-06-06_project_bg_geo_extract/akteur_typ_projekt_geo.json` |
| `inferred_shared_material_candidate` | 38 | `f9cf1a8c8fd9` 2026-06-02 `_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json` |
| `city_unconfirmed_no_address` | 26 | ``  `structural LIEGT_IN_STADT without node.adresse` |
| `inferred_shared_material_candidate` | 25 | `f9cf1a8c8fd9` 2026-06-02 `_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json` |
| `placeholder_source:processed+archive` | 9 | `ed1d81d9b5be` 2026-06-06 `_neo4j/review/2026-06-06_project_bg_geo_extract/akteur_typ_projekt_geo.json` |
| `placeholder_source:processed+ELYS` | 8 | `ed1d81d9b5be` 2026-06-06 `_neo4j/review/2026-06-06_project_bg_geo_extract/akteur_typ_projekt_geo.json` |
| `placeholder_source:archive` | 7 | `ed1d81d9b5be` 2026-06-06 `_neo4j/review/2026-06-06_project_bg_geo_extract/akteur_typ_projekt_geo.json` |
| `placeholder_source:processed+web` | 7 | `ed1d81d9b5be` 2026-06-06 `_neo4j/review/2026-06-06_project_bg_geo_extract/akteur_typ_projekt_geo.json` |
| `placeholder_source:Council of the EU` | 6 | `ed1d81d9b5be` 2026-06-06 `_neo4j/review/2026-06-06_project_bg_geo_extract/akteur_typ_projekt_geo.json` |
| `placeholder_source:processed` | 6 | `ed1d81d9b5be` 2026-06-06 `_neo4j/review/2026-06-06_project_bg_geo_extract/akteur_typ_projekt_geo.json` |
| `placeholder_source:None` | 2 | `ed1d81d9b5be` 2026-06-06 `_neo4j/review/2026-06-06_project_bg_geo_extract/akteur_typ_projekt_geo.json` |

## 5. `project_part_actor_edges` JSON lineage

Source: [`_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json`](../../intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json)  

| enrichment_run slice | Imported by | review_run on graph | G3 impact |
|---|---|---|---|
| `project_part_actor_edge_enrichment_existing_node_types_2026_06_01` | `2026-06-01_project_part_actor_import_all/_run_import_all.py` | `project_part_actor_import_all_2026_06_01` | 91 edges; **63** flagged `RELABEL` (shared-material inference) |
| `actor_edge_enrichment_existing_types_2026_06_01` | `2026-06-02_bauteilboerse_actor_enrichment_import` | `bauteilboerse_actor_enrichment_import_2026_06_02` | includes `LIEGT_IN_LAND` singleton guard; mostly web-evidenced |
| `actor_edge_enrichment_deep_existing_types_2026_06_01` | same 06-02 importer | same | deep web pass edges |

The 06-01 importer **explicitly** downgraded all 91 edges to `evidence_confidence=abgeleitet` while preserving `import_original_evidence_confidence` — documented in run README as `import_all_for_now` / `needs_source_url_review`.

## 6. Dossier paths (`intake/inbox/`)

Actor→project PARTIAL rows trace to dossier markdown under `_neo4j/intake/inbox/` (project-named `.md` files). The geo extract copied `source_url` from dossier processing metadata, which sometimes stored **pipeline tokens** instead of HTTP URLs — Agent 09 correctly routed these to `PARTIAL` + `RESOURCE`.

Sample dossier hits recorded per cluster in `dossier_inbox_paths` column of the ledger CSV.

Examples (placeholder-source projects with real URLs elsewhere in inbox research):

| Project | PARTIAL actor edges | Dossier / research path with real URLs |
|---|---:|---|
| `p_circl_abn_amro` | 14 | `_knowledge/reuse_bubbles/netherlands_reuse_bubble_combined.md` (§4.6 Circl) |
| `p_55_great_suffolk_street_london` | 3 | `_neo4j/intake/inbox/research/new taxonomy edit/_normalized/reuse_taxonomy_v9_connection_expansion_batch_01_markdown_only.md` (v10A-001…) |
| `p_europa_building_brussels` | 6 | taxonomy batch files cite EU Council sources; geo extract stored token `Council of the EU` |
| `p_elys_kultur_gewerbehaus_basel` | 8 | geo extract token `processed+ELYS` — Basel dossier pipeline, not HTTP |

## 7. Git blame — import path timeline

| Path | First commit | Date | Blame@L1 |
|---|---|---|---|
| `_neo4j/intake/runs/2026-06-01_project_part_actor_import_all/_run_import_all.py` | `f9cf1a8c8fd9` | 2026-06-02 | `f9cf1a8c8fd9` 2026-06-02 |
| `_neo4j/intake/runs/2026-06-02_bauteilboerse_actor_enrichment_import/_run_import_actor_enrichment_edges.py` | `f9cf1a8c8fd9` | 2026-06-02 | `f9cf1a8c8fd9` 2026-06-02 |
| `_neo4j/review/2026-06-06_project_bg_geo_extract/apply_geo_import.py` | `ed1d81d9b5be` | 2026-06-06 | `ed1d81d9b5be` 2026-06-06 |
| `_neo4j/review/2026-06-06_project_bg_geo_extract/_generate_geo_import_patches.py` | `ed1d81d9b5be` | 2026-06-06 | `ed1d81d9b5be` 2026-06-06 |
| `_neo4j/review/2026-06-06_project_bg_geo_extract/_build_unified_geo_json.py` | `ed1d81d9b5be` | 2026-06-06 | `ed1d81d9b5be` 2026-06-06 |
| `_neo4j/review/2026-06-06_project_bg_geo_extract/reuse_geo_graph.json` | `ed1d81d9b5be` | 2026-06-06 | `ed1d81d9b5be` 2026-06-06 |
| `_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json` | `f9cf1a8c8fd9` | 2026-06-02 | `f9cf1a8c8fd9` 2026-06-02 |
| `_neo4j/review/2026-06-06_full_graph_verification/_agent_09_build.py` | `` |  | ``  |

## 8. Recommendations

1. **Do not upgrade** the 335 organisational `LIEGT_IN_LAND` partials without adding `adresse` — they are structurally honest.
2. **Re-fetch** actor→project edges where `akteur_typ_projekt_geo.json` has real `http` URLs but ledger says `fetched=false`.
3. **Replace placeholder tokens** in geo extract (`processed`, `archive`, `processed+web`) with dossier `primary_source_url` before any PROVEN upgrade.
4. **RELABEL or remove** the 63 `reuse_supply_or_material_hub_candidate` `BETEILIGT_AN` edges — same class as removed fabrication tier.
5. **Close deferred-evidence packet** [`MUST_FIND_EVIDENCE.md`](../../intake/runs/2026-06-01_project_part_actor_import_all/MUST_FIND_EVIDENCE.md) for the 91 import-all edges.

---

*Read-only git + repo analysis. No graph mutation.*
