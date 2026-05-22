# `_knowledge/` — research corpus

Your human-readable research on **direct reuse of building components** (*Bauteilwiederverwendung* /
circular construction). This folder holds the **authored research documents** themselves; the Neo4j
graph machinery (imports, exports, audits, query scripts, provenance) lives separately under
[`../_neo4j/`](../_neo4j/).

> These documents are also cited as sources inside the graph (`source_file` paths + `evidence_source_id`
> slugs). When they were moved here, those `source_file` paths were **updated to point here**, so graph
> provenance still resolves. The filename-based slugs are unchanged.

## Contents

| Folder | What's in it |
|---|---|
| **`report/`** | `Zwischenbericht_Entwerfen_mit_Bestand_2026-07-10.md` — the interim project report (final reviewed) |
| **`themes/`** | 10 thematic research dossiers (see below) |
| **`reuse_bubbles/`** | 5 regional reuse-network studies (CH, FR, DE, NL, Rotor DC) |
| **`taxonomy/`** | the reuse-taxonomy v9 connection-expansion series + coverage report |
| **`bauteilboerse/`** | component-marketplace research interface data + market-model evidence |
| **`projects/`** | `PROJECTS_RESEARCH.md` — overview of the 74 building case studies (by `bewertung`) |

### `themes/`
- [schadstoff_reuse_knowledge_graph_research.md](themes/schadstoff_reuse_knowledge_graph_research.md) — pollutants / hazardous-substance regime
- [bauteilreuse_legal_regime_matrix.md](themes/bauteilreuse_legal_regime_matrix.md) — legal frameworks by country
- [circular_construction_economics_kg.md](themes/circular_construction_economics_kg.md) — economics
- [circular_construction_leistungsanforderungen.md](themes/circular_construction_leistungsanforderungen.md) — performance requirements
- [circular_construction_reuse_graph_gaps.md](themes/circular_construction_reuse_graph_gaps.md) — coverage gaps
- [connection_techniques_bauteilreuse.md](themes/connection_techniques_bauteilreuse.md) — connection / disassembly techniques
- [energy_climate_reuse_research.md](themes/energy_climate_reuse_research.md) — energy & climate
- [aufbereitungsverfahren_reused_building_elements.md](themes/aufbereitungsverfahren_reused_building_elements.md) — reprocessing methods
- [testing_verification_bauteilreuse_kg.md](themes/testing_verification_bauteilreuse_kg.md) — testing & verification
- [missing_underused_norm_nodes_reuse_kg.md](themes/missing_underused_norm_nodes_reuse_kg.md) — norms/standards gaps

### `reuse_bubbles/`
[swiss](reuse_bubbles/swiss_reuse_bubble_v2.md) · [france](reuse_bubbles/france_reuse_bubble_combined.md) · [germany](reuse_bubbles/germany_reuse_bubble_v1.md) · [netherlands](reuse_bubbles/netherlands_reuse_bubble_combined.md) · [rotor_dc](reuse_bubbles/rotor_dc_reuse_bubble_v2.md)

### `taxonomy/`
[coverage report](taxonomy/reuse_taxonomy_coverage_report_batches_01_09.md) · connection-expansion batches
[01](taxonomy/reuse_taxonomy_v9_connection_expansion_batch_01_markdown_only.md) ·
[02](taxonomy/reuse_taxonomy_v9_connection_expansion_batch_02.md) ·
[03](taxonomy/reuse_taxonomy_v9_connection_expansion_batch_03.md) ·
[04](taxonomy/reuse_taxonomy_v9_connection_expansion_batch_04.md) ·
[05](taxonomy/reuse_taxonomy_v9_connection_expansion_batch_05.md) ·
[06](taxonomy/reuse_taxonomy_v9_connection_expansion_batch_06.md) ·
[07](taxonomy/reuse_taxonomy_v9_connection_expansion_batch_07.md) ·
[08](taxonomy/reuse_taxonomy_v9_connection_expansion_batch_08.md) ·
[09](taxonomy/reuse_taxonomy_v9_connection_expansion_batch_09.md) ·
[10](taxonomy/reuse_taxonomy_v9_connection_expansion_batch_10.md) ·
[_filtered_non_reuse_bgs](taxonomy/_filtered_non_reuse_bgs.md)

### `bauteilboerse/`
- [BAUTEILBOERSEN_RESEARCH_INTERFACE_DATA_FINAL_CLEAN_2026-06-04.md](bauteilboerse/BAUTEILBOERSEN_RESEARCH_INTERFACE_DATA_FINAL_CLEAN_2026-06-04.md) — marketplace interface dataset
- [Bauteilboersen_Marktmodell_Channel_Evidence.docx](bauteilboerse/Bauteilboersen_Marktmodell_Channel_Evidence.docx) — market-model & channel evidence

## Related material that stays in `_neo4j/` (graph-coupled)

These are tied to graph data/scripts, so they remain in `_neo4j/` and are linked here:

- **Semantic reuse-network catalog** — [REUSE_NETWORK_CATALOG.md](../_neo4j/review/2026-06-16_semantic_reuse_network_catalog/REUSE_NETWORK_CATALOG.md) (ships with its query scripts + `graph_networks/` data)
- **Donor ↔ receiver research** — [donor_receiver_research_summary.md](../_neo4j/neo4j_donor_receiver_research_round004/reviews/donor_receiver_research_summary.md)
- **Bauteilbörse enrichment runs** — [deep enrichment](../_neo4j/intake/inbox/research/bauteilboersen_deep_enrichment_results/README.md) · [material/bauteiltyp](../_neo4j/intake/inbox/research/bauteilboersen_deeper_material_bauteiltyp_results/README.md) ([matrix](../_neo4j/intake/inbox/research/bauteilboersen_deeper_material_bauteiltyp_results/MATERIAL_BAUTEILTYP_MATRIX.md))

`_archive/research/` (the retired legacy folder tree) is **excluded by design**.

---

`_MIGRATION_MANIFEST.csv` records the cleanup history (files moved/deleted).
