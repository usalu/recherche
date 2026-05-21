# Final Verification — Phase 1.2 + 1.3 against live `mit-bestand`

- **Verifier:** Final Verifier 2 of 12 (read-only, no migrations executed)
- **Verified at:** 2026-05-21 (live `mit-bestand`, bolt://localhost:7687)
- **Plan reference:** `c:/Users/Kinosh/.cursor/plans/radical_quality-first_reset_8d1e2b66.plan.md`, sections 1.2 + 1.3
- **Run directory:** `E:/recherche/_neo4j/intake/runs/2026-05-20_radical_quality_reset/`

---

## Overall verdict

| Phase | Acceptance gates owned by the phase | Live status |
| ----- | ----------------------------------- | ----------- |
| 1.2 (anchor relabel) | 1, 2, 3, 4, 6, 8 → PASS · 5, 7 → **FAIL** (regression introduced post-1.2 by `agent10_phase4b_3`) | **REGRESSED** |
| 1.3 (propagated flag) | 9, 10, 11, 12, 13, 14, 15 → PASS | **PASS** |

Phase 1.3 is fully intact. Phase 1.2's structural intent (relabel anchors, retype edges, drop deg-0 Quelle) is still visible in the migration script, the done-flag, the deleted-evidence trail, and the surviving 702 `ANCHORED_BY` edges, but the actor-registry loader run in Phase 4b.3 silently introduced a duplicate `:Quelle` node with the anchor's id and 202 fresh `BELEGT_IN` edges onto the surviving `:OntologyAnchor`. Two of the eight Phase 1.2 gates therefore fail against the live graph.

---

## Phase 1.2 — line-by-line

### Gate 1 — `migrations/mig_1_2_anchor_relabel.cypher` exists — **PASS**

Path: `E:/recherche/_neo4j/intake/runs/2026-05-20_radical_quality_reset/migrations/mig_1_2_anchor_relabel.cypher`. File present, three labelled sections (1.2.a relabel, 1.2.b retype `BELEGT_IN`→`ANCHORED_BY`, 1.2.c hard-delete deg-0 `:Quelle`). Header documents the pre-migration counts (`q_controlled_vocab_seed` deg 457, `q_akteursliste_master_md` deg 259, 21 deg-0 Quelle archived) and the expected effects.

### Gate 2 — `PHASE_1_2_DONE.flag` parseable — **PASS**

Located at `logs/PHASE_1_2_DONE.flag` (not the run root — Agent 3 placed all 1.2/1.3 done-flags under `logs/`). Valid JSON, contains the canonical `before`/`after` block:

- `before.anchors_as_quelle = 2`, `before.anchored_by_to_anchors = 0`, `before.belegt_in_to_anchors = 716`.
- `after.anchors_as_quelle = 0`, `after.anchored_by_to_anchors = 716`, `after.belegt_in_to_anchors = 0`.
- `before/after.total_nodes`: 2442 → 2441; `total_rels`: 19714 → 19604 (Δ-110 matches 1.3.b+1.3.c).

The file proves the migration **completed correctly on 2026-05-20T20:57:50+00:00**; the regression observed today (see Gates 5 + 7) is post-migration.

### Gate 3 — `deleted/phase1_2_quelle.jsonl` exists — **PASS**

Path: `deleted/phase1_2_quelle.jsonl`. File present, 22 records (1 header + 21 deg-0 `:Quelle` rows). Header is explicit about the wave-1 orchestration overlap: 21 of the 22 IDs were preempted by Agent 5 during Phase 1.5; Phase 1.2.c only deleted 1 new collateral deg-0 `:Quelle` (`q_phase20_kette_autodiscovery`) that emerged from Phase 1.1. Forensic completeness preserved.

### Gate 4 — `MATCH (a:OntologyAnchor) RETURN count(a)` == 2 — **PASS**

Live query returned 2. Both anchors visible:

| `elementId` | `id` | labels | in-deg | out-deg |
| --- | --- | --- | --- | --- |
| `4:…:807` | `q_controlled_vocab_seed` | `[OntologyAnchor]` | 443 | 0 |
| `4:…:6180` | `q_akteursliste_master_md` | `[OntologyAnchor]` | 461 | 319 |

### Gate 5 — `MATCH (q:Quelle) WHERE q.id IN […] RETURN count(q)` == 0 — **FAIL (live = 1)**

Live query returned 1: a duplicate `:Quelle` node with `id = 'q_akteursliste_master_md'` exists (`elementId 4:…:1777`), distinct from the OntologyAnchor (`elementId 4:…:6180`). Properties:

```text
created_by:    "agent10_phase4b_3"
last_seen_by:  "agent10_phase4b_3"
quelltyp:      "actor_registry_markdown"
source_scope:  "actor_registry"
```

The duplicate is a Phase 4b.3 regression: Agent 10's actor-registry loader matched on `id` only, without checking labels, and re-created a `:Quelle` shell after Phase 1.2 had relabelled the original to `:OntologyAnchor`. The OntologyAnchor was preserved correctly; the new `:Quelle` is a parallel shadow node.

### Gate 6 — `MATCH ()-[r:ANCHORED_BY]->(:OntologyAnchor) RETURN count(r)` in [690, 730] — **PASS (live = 702)**

702 is inside the acceptance window. Net delta vs. the `PHASE_1_2_DONE.flag` snapshot is -14 ANCHORED_BY (716 → 702). Two anchors share the count: `q_controlled_vocab_seed` keeps 443 incoming `ANCHORED_BY`; `q_akteursliste_master_md` keeps 259 (461 in-deg − 202 BELEGT_IN, see Gate 7). The -14 drift comes from downstream node deletions in later phases (1.5 / 1.6 / 2.x) detaching their owning anchored-by edges; this is the expected, in-range topology change.

### Gate 7 — `MATCH ()-[r:BELEGT_IN]->(:OntologyAnchor) RETURN count(r)` == 0 — **FAIL (live = 202)**

Live query returned 202. All 202 edges terminate on `OntologyAnchor` `q_akteursliste_master_md` (`elementId 4:…:6180`) and originate from `:Akteur` (200) and `:Land` (2) source nodes. Sampled property shape:

```text
evidence_origin:     "curated"
evidence_basis:      "cell_citation"
evidence_confidence: "belegt"
evidence_source_id:  "q_akteursliste_master_md"
source_scope:        "actor_registry"
id:                  "r_<akteur>__BELEGT_IN__q_akteursliste_master_md"
```

This is the second half of the Phase 4b.3 regression observed in Gate 5. The actor-registry loader created 202 fresh `:BELEGT_IN` edges from registry actors directly onto the OntologyAnchor — a contract violation of Phase 1.2 (anchors must only receive `:ANCHORED_BY`). The same 202 source nodes also have parallel `:BELEGT_IN` edges to the duplicate `:Quelle` (404 total `:BELEGT_IN` from the loader; 202 land on the OntologyAnchor and trip this gate).

### Gate 8 — 5 sampled `ANCHORED_BY` edges have canonical shape — **PASS**

Five sampled `(n)-[r:ANCHORED_BY]->(a:OntologyAnchor)` edges (`mm_kauf_neu`, `mm_kauf_gebraucht`, `mm_spende`, `mm_leasing`, `mm_rueckkauf` all → `q_controlled_vocab_seed`):

| field | sampled values |
| --- | --- |
| `evidence_origin` | `derived` (5/5) |
| `evidence_basis` | `controlled_vocab` (5/5) |
| `evidence_confidence` | `bookkeeping` (5/5) |
| `evidence_source_id` | `q_controlled_vocab_seed` (5/5) |
| `evidence_excerpt` | absent / null (5/5) |

Matches `mig_1_2_anchor_relabel.cypher` step 1.2.b verbatim.

---

## Phase 1.3 — line-by-line

### Gate 9 — `migrations/mig_1_3_flag_propagated.cypher` exists — **PASS**

File present, three sections (1.3.a flag 319 propagated `HAT_MARKTMODELL` excerpts; 1.3.b drop `HAT_DOMINANT_MARKTMODELL`; 1.3.c drop `HAT_DOMINANT_AKZEPTANZ`). Header documents pre-migration counts 319 / 86 / 24.

### Gate 10 — `PHASE_1_3_DONE.flag` parseable — **PASS**

Located at `logs/PHASE_1_3_DONE.flag`. Valid JSON, identical `before`/`after` block to 1.2 (Agent 3 wrote one combined flag per phase). Records `hat_marktmodell_with_propagated_excerpt 319 → 0`, `hat_marktmodell_with_propagated_basis 0 → 319`, `hat_dominant_marktmodell 86 → 0`, `hat_dominant_akzeptanz 24 → 0`.

### Gate 11 — `count(:HAT_DOMINANT_MARKTMODELL)` == 0 — **PASS (live = 0)**

### Gate 12 — `count(:HAT_DOMINANT_AKZEPTANZ)` == 0 — **PASS (live = 0)**

### Gate 13 — `:HAT_MARKTMODELL {evidence_basis:'propagated'}` in [310, 330] — **PASS (live = 319)**

### Gate 14 — `:HAT_MARKTMODELL` where `source_excerpt CONTAINS 'propagated'` == 0 — **PASS (live = 0)**

### Gate 15 — 5 sampled propagated edges have canonical shape with `original_source_excerpt` preserved — **PASS**

Five sampled `(:Bauteilgruppe)-[r:HAT_MARKTMODELL {evidence_basis:'propagated'}]->(:Marktmodell)` edges (sources: `bg_reuse_stahl_mehrere_55gss_external_core`, `bg_reuse_mehrere_mehrere_alliander_common_roof_atrium` ×3, `bg_reuse_mehrere_ausbau_alliander_material_passport_inventory`; targets: `mm_spende`, `mm_plattform_vermittelt`, `mm_take_back_service`):

| field | sampled values |
| --- | --- |
| `evidence_origin` | `derived` (5/5) |
| `evidence_basis` | `propagated` (5/5) |
| `evidence_confidence` | `bookkeeping` (5/5) |
| `source_excerpt` | `null` (5/5) — correctly removed |
| `original_source_excerpt` | `"propagated from project HAT_DOMINANT_MARKTMODELL (project-wide sourcing)"` (5/5) — preserved as audit field |

Matches `mig_1_3_flag_propagated.cypher` step 1.3.a verbatim.

---

## Root-cause note on the Phase 1.2 regression

The Phase 1.2 migration ran correctly on 2026-05-20T20:57:50+00:00; the `PHASE_1_2_DONE.flag` `after` block proves zero `BELEGT_IN` to the anchors and zero `:Quelle` named `q_akteursliste_master_md` at that moment.

Between then and today, `agent10_phase4b_3` (`logs/agent10_research_registry_loader.py`) replayed the actor registry JSONL. Agent 10's own report (`reports/agent_10_phase4b_report.md`, line 46) notes that "the 8th anchor (`akteursliste_master_md`) already existed from prior waves; its 277 `ZITIERT_QUELLE` edges to actor URLs are managed by 4b.3", but it does **not** flag that:

1. The loader's MERGE on `:Quelle {id: ...}` failed to match the relabelled `:OntologyAnchor` (because labels are part of MERGE matching) and silently created a parallel `:Quelle` shell, and
2. The loader then wrote 202 `:Akteur`/`:Land -[:BELEGT_IN]-> q_akteursliste_master_md` edges that landed on the surviving `:OntologyAnchor` (Cypher `MATCH (q {id:'...'})` resolves on id alone, regardless of label).

Concretely, the live graph today looks like:

```text
:OntologyAnchor {id:'q_akteursliste_master_md'}      // eid 6180, ANCHORED_BY in-deg 259, BELEGT_IN in-deg 202 (regression)
:Quelle         {id:'q_akteursliste_master_md'}      // eid 1777, BELEGT_IN in-deg 202 (regression duplicate)
```

This is the root cause of both Gate 5 and Gate 7 failures. Fix candidates (out of scope for this read-only verifier):

- Relabel the duplicate `:Quelle` (eid 1777) to `:OntologyAnchor`, then merge it into eid 6180, **or**
- Retype the 202 `:BELEGT_IN` edges on eid 6180 to `:ANCHORED_BY` with the bookkeeping shape (Phase 1.2.b semantics), and delete or relabel the duplicate `:Quelle`.

The Phase 1.2 contract is "anchors only receive `:ANCHORED_BY` with `derived/bookkeeping` evidence". The loader's 202 edges carry `curated/cell_citation/belegt` evidence; even if retyped they would need re-shaping. The cleaner of the two fixes is therefore to merge the duplicate and retype the edges into the Phase 1.2 canonical shape.

---

## Files touched by this verifier

- **Created:** `reports/final_verify_phase1_2_3.md` (this file).
- **Migrations run:** none (read-only).
- **Database writes:** none (read-only).
