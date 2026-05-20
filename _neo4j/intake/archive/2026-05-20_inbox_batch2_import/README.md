# Archive — 2026-05-20 inbox batch2 import

**Raw drop preserved for provenance.** Do not edit files under `raw_tree/`.

These 21 dossier files were processed via the multi-phase batch2 v2 import. See:

- [`_neo4j/intake/runs/2026-05-20_inbox_batch2_import/HANDOFF.md`](../../runs/2026-05-20_inbox_batch2_import/HANDOFF.md) — overview for future agents
- [`_neo4j/intake/runs/2026-05-20_inbox_batch2_import/PLAN_v2.md`](../../runs/2026-05-20_inbox_batch2_import/PLAN_v2.md) — authoritative pre-apply plan
- [`_neo4j/intake/runs/2026-05-20_inbox_batch2_import/APPLY_ORDER.md`](../../runs/2026-05-20_inbox_batch2_import/APPLY_ORDER.md) — phase-by-phase apply order
- [`_neo4j/intake/runs/2026-05-20_inbox_batch2_import/REMAINING_GAPS.md`](../../runs/2026-05-20_inbox_batch2_import/REMAINING_GAPS.md) — what's still open
- [`_neo4j/review/round_002_followup/rollback.md`](../../../review/round_002_followup/rollback.md) — apply ledger + rollback procedure

Apply outcome: **+282 nodes / +2 954 relationships** against the `mit-bestand` Neo4j database (pre-batch2 baseline: 2 298 nodes / 17 035 rels → post-Phase-27: 2 580 / 19 989).

## Contents of `raw_tree/`

| Folder / file | Dossiers |
|---|---|
| `BE_NL_graph_ready_dossiers/` (+ `.zip`) | Careno Be Circular Brussels, Circl ABN AMRO, Circl Pavilion Amsterdam |
| `DE_AT_CH_graph_ready_dossiers/` (+ `.zip`) | LYSP8 Basel, MedUni Campus Mariannengasse Wien, RE_USE Höfe Wien, Reallabor Be-Ware, Stuttgart 210 |
| `EU_consortia_graph_ready_dossiers/` (+ `.zip`) | FCRBE, Interreg NWE FCRBE, REBRIDGE, Reuse Logistics |
| `batch 1.md` | SMS Zürich, UMAR, ELEMENTA (3 sub-dossiers in a single markdown file) |
| `reuse_platform_graph_ready_dossiers/` | RCMI Concular, REFAIR Bordeaux |
| `teaching_programme_graph_ready_dossiers/` (+ `.zip`) | Architecture of Reuse Brussels, ETH Circular Construction Programme, Vandkunsten, ZHAW Reuse in Construction |
| `uk_unclear_graph_ready_dossiers/` (+ `.zip`) | Granby Workshop Liverpool, OBK_27 |

The folder contains 21 dossier markdown files total + 5 zip archives of the original deliveries.

**Provenance status:** The 5 `.zip` files are kept alongside the extracted markdown folders for completeness; they are byte-identical to the originals delivered to `_neo4j/intake/inbox/projects/` and are kept to preserve the exact form of the drop.
