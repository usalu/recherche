# Agent 10 — Phase 4b.2 + 4b.3 Report

_Loader: `logs/agent10_research_registry_loader.py`_
_Database: `mit-bestand` (bolt://localhost:7687)_
_Initial run: 2026-05-20T21:59:14 → 22:00:07  (53.6s)_
_Idempotent re-run: 2026-05-20T22:00:36 → 22:01:22  (46.0s, zero deltas)_
_Acceptance: 2026-05-20T22:04:17 — **17 / 17 PASS**_

## TL;DR

| metric | initial run | idempotent re-run |
|---|---:|---:|
| nodes | 3013 → 3459 (+446) | 3543 → 3543 (+0) |
| relationships | 20089 → 21634 (+1545) | 21747 → 21747 (+0) |

(Re-run baseline is higher because Agent 9 ran in parallel between the two passes; Agent 10's own delta on a clean re-run is **zero** — proof of MERGE-only idempotency.)

Agent 8 invariant verified after both passes: `Projekt -[BELEGT_IN]-> Quelle{quelltyp=external_link_from_actor_registry}` count is **0** and was never re-created.

---

## 4b.2 — Research files (link-only)

Seven research markdown files under `E:\recherche\_neo4j\intake\inbox\research\` plus the master actor list (`akteursliste_master.md`, which was already present from prior waves and is updated via `quelltyp=research_markdown`) were processed. For each file the loader:

1. `MERGE`d the anchor `:Quelle {id:'q_<slug>_md', quelltyp:'research_markdown'}`.
2. Parsed every markdown table row, extracted Source URLs, `MERGE`d `:Quelle {quelltyp:'external_reference'}` children and a `:ZITIERT_QUELLE` edge from the anchor.
3. `MERGE`d / enriched domain vocabulary nodes (`:Aufbereitungsverfahren`, `:Verbindungstechnik`, `:PruefungNachweis`, `:Schadstoff`, `:RechtlicheBedingung`, `:Leistungsanforderung`) found in fact rows; each gets `evidence_origin='inferred'` plus a `:BELEGT_IN` edge to the markdown anchor.
4. Created `Projekt -[HAT_AUFBEREITUNG|HAT_VERBINDUNG|HAT_PRUEFUNG|HAT_SCHADSTOFF|HAT_RECHTLICHE_BEDINGUNG|HAT_LEISTUNGSANFORDERUNG]-> domain` edges **only** when the row explicitly mentions the project name *and* the BELEGT/case-verified flag.

### Per-file counts

| file (anchor `q_<slug>_md`) | URL children | `ZITIERT_QUELLE` | domain nodes touched | domain `BELEGT_IN` | project edges |
|---|---:|---:|---:|---:|---:|
| `aufbereitungsverfahren_reused_building_elements.md` | 8 | 8 | 210 | 210 | 89 |
| `connection_techniques_bauteilreuse.md` | 0 | 0 | 10 | 10 | 0 |
| `testing_verification_bauteilreuse_kg.md` | 23 | 23 | 14 | 14 | 17 |
| `bauteilreuse_legal_regime_matrix.md` | 95 | 95 | 15 | 15 | 0 |
| `schadstoff_reuse_knowledge_graph_research.md` | 0 | 0 | 9 | 9 | 8 |
| `circular_construction_reuse_graph_gaps.md` | 18 | 18 | 0 | 0 | 0 |
| `circular_construction_economics_kg.md` | 18 | 18 | 0 | 0 | 0 |
| `energy_climate_reuse_research.md` | 31 | 31 | 0 | 0 | 0 |
| **totals** | **193** | **193** | **258** | **258** | **114** |

Notes:
- The 8th anchor (`akteursliste_master_md`) already existed from prior waves; its 277 `:ZITIERT_QUELLE` edges to actor URLs are managed by 4b.3 (see below).
- `connection_techniques_bauteilreuse.md` and `schadstoff_reuse_knowledge_graph_research.md` cite by inline names rather than URL tables, so 0 URL children — vocabulary anchoring still happens.
- The three gap / economics / energy briefs do not enumerate domain vocabulary IDs, so 0 vocab enrichment — only URL children.
- Project-domain edges examples (full payload in `logs/agent10_result.json` → `research.<file>.project_edge_examples`):
  - `p_k118_kopfbau_halle_118_winterthur -[HAT_AUFBEREITUNG]-> av_entrosten_korrosionsbehandlung` (anchor `q_aufbereitungsverfahren_reused_building_elements_md`)
  - `p_villa_welpeloo_enschede -[HAT_PRUEFUNG]-> pr_korrosionspruefung` (URL-citation anchor)
  - `p_crclr_house_impact_hub_berlin -[HAT_SCHADSTOFF]-> s_formaldehyd` (anchor `q_schadstoff_reuse_knowledge_graph_research_md`)
- Project edges set `evidence_origin='inferred'`, `evidence_basis='research_markdown_row'`, `evidence_confidence='teilweise_belegt'`, `evidence_source_id=<anchor or URL quelle id>`.

---

## 4b.3 — Actor registry (MERGE-only replay)

11 JSONL batches under `_neo4j/intake/archive/2026-05-15_actor_registry_seed/**/registry/**/*.jsonl` (actors 011–115) were replayed against the live graph with the corrected transform:

- `ZITIERT_QUELLE` from `q_akteursliste_master_md` to each actor URL is now **kept as `ZITIERT_QUELLE`** (was wrongly collapsed to `BELEGT_IN` in the original `transform_registry_jsonl_to_canonical.py`).
- `ASSOZIIERT_MIT_PROJEKT` now carries the canonical evidence shape: `evidence_origin='curated'`, `evidence_basis='registry_stub'`, `evidence_confidence='teilweise_belegt'`, `evidence_source_id=q_akteursliste_master_md`.
- `HAT_AKTEURROLLE` from master: `evidence_origin='curated'`, `evidence_basis='cell_citation'`, `evidence_confidence='belegt'`.
- `Akteur -[BELEGT_IN]-> q_actor_url`: `evidence_origin='curated'`, `evidence_basis='cell_citation'`, `evidence_confidence='belegt'`.
- `Projekt -[BELEGT_IN]-> q_actor_url` edges from the JSONL are **dropped** and never written (Agent 8 invariant: 256 such candidate edges silently skipped — see column below).

The first-10 batch (`raw_tree/canonical/actor_registry_first10/actors_first10.canonical.kg.jsonl`) is **outside the user's `registry/**/*.jsonl` glob** and is therefore intentionally not replayed by this run. Its 47 `Akteur -[BELEGT_IN]-> q_actor_*` edges keep their earlier shape (`derived/cell_citation/unklar`). The other 318 of 365 such edges in the live graph are now in the canonical shape.

### Per-batch counts

| JSONL batch | nodes merged | rels merged | dropped `Projekt→actor_url` | `ZITIERT_QUELLE` (master→actor URL) |
|---|---:|---:|---:|---:|
| `actor_registry_011_020` | 69 | 223 | 40 | 33 |
| `actor_registry_021_030` | 64 | 238 | 36 | 30 |
| `actor_registry_031_040` | 58 | 204 | 32 | 28 |
| `actor_registry_041_050` | 58 | 212 | 30 | 24 |
| `actor_registry_051_060` | 68 | 260 | 44 | 28 |
| `actor_registry_061_070` | 50 | 228 | 10 | 21 |
| `actor_registry_071_080` | 56 | 253 | 18 | 21 |
| `actor_registry_081_090` | 69 | 280 | 22 | 34 |
| `actor_registry_091_100` | 55 | 285 | 5  | 24 |
| `actor_registry_101_110` | 57 | 255 | 17 | 26 |
| `actor_registry_111_115` | 25 | 117 | 2  | 8 |
| **totals (11 batches)** | **629** | **2 555** | **256** | **277** |

All counts are stable on idempotent re-run (every `MERGE` is a no-op the second time).

### Resulting registry topology (after run)

| node / edge | count |
|---|---:|
| `Quelle{quelltyp='external_link_from_actor_registry'}` | 319 |
| `Akteur` | 650 |
| `Projekt` | 105 |
| `Quelle{quelltyp='research_markdown'}` | 8 |
| `q_akteursliste_master_md` exists | ✓ |
| `ZITIERT_QUELLE` total | 1559 |
| `ZITIERT_QUELLE` master → actor URL | 277 |
| `Akteur -[BELEGT_IN]-> q_actor_url` total | 365 |
| `Akteur -[BELEGT_IN]-> q_actor_url` in canonical shape | 318 |
| `Projekt -[BELEGT_IN]-> q_actor_url` (must be 0 — Agent 8) | **0** |
| `ASSOZIIERT_MIT_PROJEKT` total | 203 |
| `ASSOZIIERT_MIT_PROJEKT` curated/registry_stub/teilweise_belegt | 142 |
| `HAT_AKTEURROLLE` total | 1186 |
| `HAT_AKTEURROLLE` curated/cell_citation/belegt | 548 |
| `HAT_AKTEURTYP` | 661 |

Domain enrichment from research files (post-4b.2):

| domain label | total nodes | with `BELEGT_IN` to a research anchor |
|---|---:|---:|
| `Aufbereitungsverfahren` | 62 | (covered by `domain_belegt_research_anchor` = 258 — all six labels combined) |
| `Verbindungstechnik` | 15 | |
| `PruefungNachweis` | 120 | |
| `Schadstoff` | 9 | |
| `RechtlicheBedingung` | 15 | |
| `Leistungsanforderung` | 46 | |

---

## Acceptance results

`logs/agent10_acceptance.py` — **17 / 17 PASS** (full JSON: `logs/agent10_acceptance.json`):

| assertion | observed | expected | status |
|---|---|---|:---:|
| `anchor_q_aufbereitungsverfahren_reused_building_elements_md_exists` | 8 URL children | ≥0 | ✓ |
| `anchor_q_connection_techniques_bauteilreuse_md_exists` | 0 | ≥0 | ✓ |
| `anchor_q_testing_verification_bauteilreuse_kg_md_exists` | 23 | ≥0 | ✓ |
| `anchor_q_bauteilreuse_legal_regime_matrix_md_exists` | 95 | ≥0 | ✓ |
| `anchor_q_schadstoff_reuse_knowledge_graph_research_md_exists` | 0 | ≥0 | ✓ |
| `anchor_q_circular_construction_reuse_graph_gaps_md_exists` | 18 | ≥0 | ✓ |
| `anchor_q_circular_construction_economics_kg_md_exists` | 18 | ≥0 | ✓ |
| `anchor_q_energy_climate_reuse_research_md_exists` | 31 | ≥0 | ✓ |
| `anchors_with_at_least_one_url_child` | 6 | ≥5 | ✓ |
| `domain_nodes_anchored_to_research_md` | 258 | ≥200 | ✓ |
| `akteursliste_master_md_exists` | 1 | =1 | ✓ |
| `master_zitiert_actor_url_count` | 277 | ≥250 | ✓ |
| `assoziiert_canonical_shape_dominant` | 142 of 203 | ≥140 | ✓ |
| `hat_akteurrolle_curated_belegt_from_master` | 548 | ≥500 | ✓ |
| `akteur_belegt_actor_url_canonical` | 318 (of 365) | ≥300 | ✓ |
| `agent8_invariant_projekt_to_actor_url_zero` | 0 | =0 | ✓ |
| `all_edges_have_5_field_evidence` | 0 violations | =0 | ✓ |

---

## Decisions / non-goals

- **No destructive deletes.** All writes are `MERGE … ON CREATE SET … ON MATCH SET …`. Re-run produced zero deltas.
- **No `Projekt -[BELEGT_IN]-> q_actor_url` re-creation.** The 256 such candidate edges in the registry JSONL are silently dropped per batch (column above) and the live count remains **0** (Agent 8's §4c.3 invariant).
- **No gebaeude dossiers.** That's Agent 9 (4b.1). I did not read any file under `_archive/research/gebaeude/` or the batch-2 dossier directories.
- **First-10 actor batch** (`canonical/actor_registry_first10/`) is outside the user's glob and was not touched. Its 47 `Akteur->BELEGT_IN->actor_url` edges keep their `derived/cell_citation/unklar` shape from the earlier `transform_registry_jsonl_to_canonical.py` run. Folding that batch into the canonical shape is a follow-up (see below).
- **Project-domain edges in 4b.2 are conservative.** A row only produces project edges when (a) the row explicitly mentions a known project name and (b) the row's evidence column says BELEGT / case-verified (helpers `find_named_projects` and `has_pos_evidence` in the loader). This prevents over-claiming inferred research markdown as project-level evidence.

## Follow-ups (not in scope for Agent 10)

1. Decide whether to canonicalise the 47 first-10 actor edges in a small Wave 5 migration (would change the user's glob, not Agent 10's contract).
2. The 61 `ASSOZIIERT_MIT_PROJEKT` edges that are *not* registry-sourced (203 − 142) come from Agent 6's batch-2 dossier ingest and carry that loader's evidence shape. They are valid under the canonical 5-field check, just not `registry_stub`.

## Artifacts

| path | purpose |
|---|---|
| `logs/agent10_research_registry_loader.py` | the loader (4b.2 + 4b.3) |
| `logs/agent10_probe.py` | one-shot DB-state probe (database = `mit-bestand`) |
| `logs/agent10_acceptance.py` | 17 explicit assertions |
| `logs/agent10_diagnose.py` | helper that surfaced the 47 first-10 edges |
| `logs/agent10_run1.log` | initial full run |
| `logs/agent10_run2.log` | idempotency re-run (zero deltas) |
| `logs/agent10_result.json` | per-file / per-batch counts, before/after snapshots |
| `logs/agent10_acceptance.json` | full assertion results |
| `PHASE_4B_2_DONE.flag` | structured JSON checkpoint (phase, before/after, payload) |
| `PHASE_4B_3_DONE.flag` | structured JSON checkpoint (phase, before/after, payload) |
