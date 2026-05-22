# Swiss Reuse Bubble — Evidence-Backed Integration Plan

**Run:** `2026-06-05_swiss_reuse_bubble`  
**Evidence dossier:** `_knowledge/reuse_bubbles/swiss_reuse_bubble_v2.md`  
**Graph dossier node:** `q_research_swiss_reuse_bubble_v2_md`  
**Baseline:** export `2026-06-03_graph_schema_full_export_mit-bestand` (live Neo4j verify before apply)

## Evidence contract (graph properties only)

| Where | Properties |
|---|---|
| Entity nodes | `primary_source_url`, `source_urls` |
| Relationships | `evidence_url`, `evidence_quote`, `evidence_confidence`, `evidence_basis`, `review_run`, `connection_kind` |

**Do not import:** `:Quelle:ExternalLink` intake nodes, `BELEGT_IN` → `q_url_*`, `evidence_source_id`, `archive_source_id`, `metadata_sidecar_key`, `evidence_claim_ids`.

**Out of scope for graph import:** §11 matrix scores, §12 interpretive conclusions, §13 synthesis labels.

Apply-time URL register (not canonical): [`EVIDENCE_REGISTER.csv`](EVIDENCE_REGISTER.csv), [`source_urls.json`](source_urls.json).

**Deprecated:** three-tier sidecar — see [`sidecar/DEPRECATED.md`](sidecar/DEPRECATED.md) and [`_neo4j/review/2026-06-06_reuse_bubble_quelle_cleanup/CLEANUP_SUMMARY.md`](../../../review/2026-06-06_reuse_bubble_quelle_cleanup/CLEANUP_SUMMARY.md).

---

## Already in graph — do not re-anchor

| Bubble element | Graph `id` | Evidence anchor already present |
|---|---|---|
| Cirkla | `cirkla` | partial `BELEGT_IN`; enrich in Phase 1 |
| Zirkular | `zirkular` | `q_actor_barbara_buser_02` |
| baubüro in situ | `baubuero_in_situ` | `q_url_5ef3423f578d8ccec9d847d64dc3b5bf` |
| K.118 | `p_k118_kopfbau_halle_118_winterthur` | `q_actor_barbara_buser_02` |
| ELYS | `p_elys_kultur_gewerbehaus_basel` | `q_elys_kultur_gewerbehaus_basel_s1` |
| useagain | `useagain_bauteilclick` | Cirkla directory + useagain.ch |
| Salza, Matériuum, Bauteilladen | `salza`, `materiuum`, `bauteilladen_winterthur` | marketplace homepages + Cirkla directory |
| Wick / ROTO | `wick_reuse_roto_baumarkt` | **not** separate `roto_reuse` node |
| Gruner ReUse | `gruner_reuse` **and** `gruner_reuse_platform` | dedup review before apply |
| Bauteilbörse Basel | `bauteilboerse_basel_overall` | library-of-reuse + Gruner news |
| Madaster, ETH | `madaster`, `eth_zuerich` | add CH URL in Phase 1 |
| Legal framework | `q_url_991a5f7d46f61c5f40b414f95b3ae0ca` | Zirkular project page |

**Cirkla connectivity gap (baseline):** `VERBUNDEN_MIT_AKTEUR` degree = 2 (`urban_bricolage`, `pascal_flammer_architekten` only).

---

## Phased patches (all evidence-backed)

### Phase 0 — `patches/phase0_sources_and_dossier.patch.jsonl`

- Add `q_research_swiss_reuse_bubble_v2_md` (`:Quelle:ResearchDocument`)
- Upsert all first-party `:Quelle:ExternalLink` nodes from source register + supplementary URLs (35 total)

### Phase 1 — `patches/phase1_enrichment_connectivity.patch.jsonl`

| Action | Evidence | Confidence |
|---|---|---|
| Cirkla `BELEGT_IN` ×4 core URLs | Cirkla homepage, association, directory, publications | belegt |
| Cirkla ↔ 6 directory actors | Cirkla expert profile URLs per actor | belegt |
| Cirkla ↔ baubuero (committee co-chair) | `q_url_9a4623e924a9afd9d134c8dadda0595b` | belegt |
| Cirkla ↔ salza (committee) | `q_actor_benjamin_poignon_03` (Olivier de Perrot) | belegt |
| Cirkla ↔ zirkular (practice triangle) | K.118 project page shared ecosystem | teilweise_belegt |
| `baubuero_in_situ` `BETEILIGT_AN` K.118 | Zirkular K.118: "architecture: baubüro in situ" | belegt |
| Promote `zirkular` K.118/ELYS stubs → `BETEILIGT_AN` | Same project pages | belegt |
| Madaster `BELEGT_IN` madaster.ch/en | Madaster CH homepage | belegt |

**Target after Phase 1:** Cirkla `VERBUNDEN_MIT_AKTEUR` degree ≥ 8.

### Phase 2 — `patches/phase2_new_nodes.patch.jsonl`

New nodes **only** with first-party `BELEGT_IN`:

| `id` | Label | Primary URL |
|---|---|---|
| `software_planular` | `:Software` | planular.net |
| `tool_swiss_inv` | `:Tool` | cirkla.ch/.../swiss-inv |
| `software_cirkla_scan` | `:Software` | cirkla.ch/.../cirkla-scan |
| `prog_swircular` | `:Programm` | swircular.ethz.ch |
| `prog_innosuisse_reuse_legal_framework_ch` | `:Programm` | zirkular.net legal framework |
| `c33_circular_construction_catalyst` | `:Akteur` | circularconstructioncatalyst.ch |
| `circular_hub_zurich` | `:Akteur` | circularhub.ch |
| `circular_economy_switzerland` | `:Akteur` | circular-economy-switzerland.ch |
| `sumami` | `:Akteur` | sumami.ch |

Edges: Cirkla→tools, Zirkular→Planular, ETH→SWIRCULAR, Zirkular/baubuero→legal framework program.

### Phase 3 — `patches/phase3_supply_chain.patch.jsonl`

| Path | Evidence | Confidence |
|---|---|---|
| Gruner → Bauteilbörse Basel → useagain | Gruner Roche news 2026-05-12 | belegt |
| useagain ↔ Bauteilladen | library-of-reuse.ch/pioneers/useagain | belegt |
| Cirkla ↔ Wick ReUse | Committee: Elias Knecht, ROTO-Reuse | belegt |
| sumami ↔ useagain | ETH sustainable-digital-construction reuse page | teilweise_belegt |
| Cirkla ↔ C33 / Circular Hub / CES | Coordination mandate overlap | teilweise_belegt |

---

## Pre-apply review queue

1. **Dedup:** `gruner_reuse` vs `gruner_reuse_platform` — merge review before Phase 3 edges on `gruner_reuse`.
2. **Stub drops:** Phase 1 drops `r_zirkular__assoziiert_mit_projekt__*` — confirm no downstream queries depend on `STUB_PROJECT_LINK` for K.118/ELYS.
3. **Live verify:** Run [`CONNECTIVITY_TESTS.cypher`](CONNECTIVITY_TESTS.cypher) before and after each phase; record in [`connectivity_report.json`](connectivity_report.json).

## Deferred (no dedicated first-party evidence)

See [`DEFERRED_NO_EVIDENCE.md`](DEFERRED_NO_EVIDENCE.md).

## Apply order

```
phase0 → baseline tests → phase1 → tests → phase2 → tests → phase3 → tests
```

No Neo4j writes until baseline audit passes `FINAL_AUDIT_REPORT.md` node/rel counts.
