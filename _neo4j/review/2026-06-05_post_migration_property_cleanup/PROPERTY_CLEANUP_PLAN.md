# Property cleanup plan — post regulation migration (`mit-bestand`)

**Created:** 2026-06-05  
**Trigger:** Graph structure is clean after Phases 0–8 + Phase B, but **properties are visually noisy** in Browser/Bloom and duplicate facts already expressed as edges.  
**Database:** `mit-bestand` (live baseline below)  
**Precedent:** [`2026-06-01_minimal_property_audit`](../2026-06-01_minimal_property_audit_current_mit-bestand/CLEANUP_APPLY_SUMMARY.md) (209→106 node keys on the *old* 7.9k-node graph). This plan **re-applies the same principles** on the post-vocabulary 2.3k-node graph.

---

## 1. Live baseline (2026-06-05)

| Metric | Value |
|---|---:|
| Nodes | 2 273 |
| Relationships | 15 118 |
| Distinct **node** property keys | 107 |
| Node property occurrences | ~18 630 (avg **8.2** / node) |
| Distinct **relationship** property keys | 63 |
| Rel property occurrences | ~64 272 (avg **4.3** / rel) |
| Relationships missing `r.id` | 4 684 |

### What makes it “dirty” (ranked by distraction)

| Bucket | Example keys | ~Occurrences | Why it hurts |
|---|---|---:|---|
| **A. Migration bookkeeping** | `phase3/6/7/8/B_property_migration`, `phase*_updated_at_utc`, `renamed_at`, `renamed_in_run`, `legacy_id` | ~3 100 nodes | Visible in every Browser panel; zero query value post-migration |
| **B. Run tags** | `review_run` (nodes + rels) | ~6 850 | Tags the regulation run on 45% of rels |
| **C. Legacy archive arrays** | `legacy_internal_provenance_docs`, `legacy_rechtsgrundlagen*`, `legacy_jurisdiktion*`, `legacy_marktmodell`, `legacy_huerde_categories` | ~1 900+ nodes | Correct as audit trail, wrong as **live graph UI** |
| **D. Stale regulation props** | `Regulierungsfrage.rechtsgrundlagen[]` (empty on all 11), `Nachweisforderung.legacy_*_from_variant_a[]` | 27–11 nodes | Variant B moved law links to `GESTUETZT_AUF_REGELWERK` |
| **E. Import pipeline on rels** | `import_decision`, `candidate_source_*`, `source_resolution_status`, `import_original_evidence_confidence` | ~3 300 rels | Leftover from intake enrichment (353 rels × ~9 keys) |
| **F. Merge audit on rels** | `merged_legacy_rel_ids`, `merged_legacy_reltypes`, `legacy_methode_*` | ~2 750 rels | Needed during Phase 5–8 dedup; not for exploration |
| **G. Timestamp sprawl** | `updated_at_utc`, `created_at`, `migrated_at`, `batch_id` | ~6 900 rels | Mechanical metadata |
| **H. Duplicate evidence shape** | `source_url` + `source_urls` + `source_titles` + `source_scope`; rel `evidence_status` + numeric `confidence` | widespread | Same fact stored 2–4 times |
| **I. Meta staging nodes** | `ReuseRule` (20 nodes, **29 keys each**) | 20 nodes | Same role DossierEntityTarget had before Phase E |

### Labels with the worst property fan-out

| Label | Distinct keys | Notes |
|---|---:|---|
| `Bauteilgruppe` | 33 | Mix of real semantics + migration + legacy arrays |
| `Projekt` | 32 | matchingqualitaet_*, legacy arrays, phase tags |
| `ReuseRule` | 29 | Should not stay as a rich node type |
| `Nachweisforderung` / `*recht` | 10 each | 5 are migration/legacy, 5 are evidence (keep evidence) |

---

## 2. Target property model (canonical)

Align with [`FINAL_PLAN_V2.md`](../../intake/runs/2026-06-04_regulation_graph_vocabulary/FINAL_PLAN_V2.md) + Phase B:

### Nodes — always keep

| Label group | Keep |
|---|---|
| All navigable entities | `id`, `name` |
| `Bauteilgruppe` | `bg_kind`, `reuse_status`, `status`, `alte_funktion`, `neue_funktion`, `tragend`, `bauteilebene`, `wiederverwendungsort`, `funktionswechsel` (Phase 7 demotions — **semantic**) |
| `Projekt` | `name_full`, `nutzung_text`, `projektstatus_text`, `year_completed`, `area_m2_gross` |
| `Kennwert` | fact literals only (`kennwert`, `wert`, `wert_text`, `einheit`, `method`, `bilanzgrenze`, `category`, `fact_index`) |
| `Land` | reference facts (`country_iso2`, aliases, pollutant-year fields) |
| Typed law nodes (`*recht`) | `source_url`, `source_quote`, `confidence`, `rechtsbereiche` |
| `Nachweisforderung` | `id`, `name` only (laws via edges) |
| `Regulierungsfrage` | `id`, `name` only |

### Nodes — evidence (case/project), pick **one** shape

- **`source_urls[]`** (+ optional `source_titles[]` only if title ≠ URL and used in UI)
- Drop singleton `source_url` when `source_urls` exists
- Drop `source_scope` (obsolete since 2026-06-01 cleanup; still on 169 nodes)
- Drop categorical `evidence_status` when numeric `confidence` is set

### Nodes — archive outside graph

Export to `_neo4j/review/2026-06-05_post_migration_property_cleanup/archive/` then **remove from Neo4j**:

- `legacy_internal_provenance_docs[]` (1 442 nodes)
- `legacy_rechtsgrundlagen*`, `legacy_jurisdiktion*`, `legacy_rechtliche_bedingungen`
- `legacy_marktmodell` (212 BG — edge `HAT_BESCHAFFUNGSWEG` is canonical)
- `legacy_huerde_categories`
- `legacy_applicability_*` on `ReuseRule`

Provenance is preserved in JSONL with `{node_id, labels, property, value, export_run}`.

### Relationships — keep

| Edge class | Keep on rel |
|---|---|
| Factual / structural | *(none)* or `id` only if you rely on rel identity |
| Evidence-bearing (case facts, reuse, Schadstoff, Huerde) | `source_url`, `source_quote`, `confidence` |
| Regulation overlay (Phase B) | `confidence`, `source_url`, `source_quote` where already set |

### Relationships — drop

All of: `review_run`, `updated_at_utc`, `created_at`, `batch_id`, `enrichment_run`, `import_*`, `candidate_source_*`, `source_resolution_*`, `source_status*`, `merged_legacy_*`, `legacy_*`, `evidence_status` (after confidence backfill check), `evidence_basis`, `evidence_url`, `evidence_quote` (when duplicate of `source_*`), `applicability_reason`, `support_rules`, `input_source`, `original_source_excerpt`, `via_bauteilgruppe_id`, `semantic_basis` — **unless** a targeted query still depends on them (spot-check before drop).

---

## 3. Phased execution (gated — no commit without go-ahead)

Each phase: **snapshot → dry-run report → explicit approval → apply → acceptance → phase report JSON**.

### Phase 0 — Audit & target matrix

**Do**

1. Run property scan → `baseline_property_scan.json` + `node_property_matrix.csv` + `rel_property_matrix.csv`.
2. Extend [`KEEP_LIST_DECISION_MATRIX.csv`](../2026-06-01_minimal_property_audit_current_mit-bestand/KEEP_LIST_DECISION_MATRIX.csv) for **new labels**: 11 `*recht`, `Regulierungsfrage`, `Nachweisforderung`, `PruefungNachweis`, `BauwerkEra`.
3. Full logical snapshot: `property_cleanup_phase0_before.json`.
4. Flag **blockers**: any property currently the *only* representation of a fact not yet on an edge.

**Accept**

- Matrix covers all 51 active labels with keep/drop/archive decision per key.
- 0 unknown keys without classification.

---

### Phase 1 — Migration bookkeeping (safe, immediate UI win)

**Drop from nodes**

```
phase3_legacy_property_migration, phase3_updated_at_utc
phase6_property_migration, phase6_updated_at_utc
phase7_property_migration, phase7_updated_at_utc
phase8_property_migration, phase8_updated_at_utc
phaseB_property_migration, phaseB_updated_at_utc
renamed_at, renamed_in_run, legacy_id
review_run          // nodes only in this phase
```

**Accept**

- 0 nodes with any `phase*_property_migration` key.
- Graph counts unchanged (nodes/rels).

**Rollback:** `phase0_before.json`

---

### Phase 2 — Stale regulation properties

**Do**

1. `Nachweisforderung`: export then drop `legacy_rechtsgrundlagen_from_variant_a[]`, `legacy_rechtsgrundlagen_urls_from_variant_a[]`, `legacy_jurisdiktion_from_variant_a[]` (27 nodes). Laws live on `GESTUETZT_AUF_REGELWERK`.
2. `Regulierungsfrage`: drop empty `rechtsgrundlagen[]`, `rechtsgrundlagen_urls[]`, `jurisdiktion[]` (11 nodes — all empty arrays today).
3. Verify parity unchanged: `GESTUETZT_AUF_REGELWERK` = 167, `GILT_IN_LAND` = 281.

**Accept**

- 0 `Nachweisforderung` with `rechtsgrundlagen` or `legacy_*variant_a*` keys.
- 0 `Regulierungsfrage` with `rechtsgrundlagen*` / `jurisdiktion` keys.
- Export files exist before drop.

---

### Phase 3 — Archive legacy arrays (largest visual cleanup)

**Do**

1. Export all `legacy_internal_provenance_docs[]` → `archive/legacy_internal_provenance_docs.jsonl`.
2. Export `legacy_rechtsgrundlagen*` / `legacy_jurisdiktion*` / `legacy_rechtliche_bedingungen` from `Projekt`, `Bauteilgruppe`, `ReuseRule` → typed JSONL files.
3. Export `legacy_marktmodell` from BTG (212) → verify each BTG has `HAT_BESCHAFFUNGSWEG` or documented exception.
4. Export `legacy_huerde_categories` from BTG/Projekt.
5. **REMOVE** exported properties from graph.

**Accept**

- 0 nodes with `legacy_internal_provenance_docs`.
- 0 nodes with `legacy_rechtsgrundlagen*` / `legacy_marktmodell` / `legacy_huerde_categories`.
- Export row count ≥ prior occurrence count.
- No loss of **web** evidence: every node that had `source_urls` still has `source_urls`.

---

### Phase 4 — Relationship import & merge metadata

**Do**

1. Export rels carrying `merged_legacy_rel_ids` / `merged_legacy_reltypes` → `archive/merged_rel_audit.jsonl`.
2. Drop import pipeline keys from all reltypes (priority: `HAT_BAUTEILTYP`, `NUTZT_MATERIAL`, `BETEILIGT_AN` — 353 rels each).
3. Drop merge audit keys listed in §2.
4. Drop `review_run`, `updated_at_utc`, `created_at`, `batch_id`, `enrichment_run`, `migrated_at` from rels.

**Accept**

- 0 rels with `import_decision` or `candidate_source_urls`.
- 0 rels with `merged_legacy_rel_ids`.
- `FINAL_AUDIT_REPORT.md` edge counts unchanged (no rel deletions in this phase).

**Expected reduction:** ~15 000–20 000 rel property occurrences.

---

### Phase 5 — Evidence shape normalization

**Do**

1. **Nodes:** fold `source_url` into `source_urls[]` where both exist (20 nodes today); dedupe arrays.
2. Drop `source_scope` from all nodes (169).
3. Drop `source_titles` where derivable from URL or unused (1 638 — spot-check 20 samples first).
4. **Rels:** drop `evidence_status` where `confidence` is set; map any remaining categorical → numeric using Phase 1 mapping from FINAL_PLAN_V2.
5. Collapse duplicate `evidence_url` → `source_url`, `evidence_quote` → `source_quote`.

**Accept**

- 0 nodes with `source_scope`.
- 0 rels with `evidence_confidence` (already 0) or `evidence_status` without `confidence`.
- Spot-check: 10 random evidence rels still have `source_url` or `source_quote`.

---

### Phase 6 — Meta node compaction (`ReuseRule`)

**Decision needed before apply**

| Option | Action |
|---|---|
| **A (recommended)** | Export 20 `ReuseRule` nodes → JSONL; **DELETE** nodes. Facts already live on regulation overlay + material/land edges. |
| **B** | Strip to `id` + `name` only (drop other 27 keys). |
| **C** | Remodel into `Regulierungsfrage`/`Nachweisforderung` annotations (high effort; defer). |

**Accept (option A)**

- `ReuseRule` node count = 0.
- No orphaned edges (currently 0 rels — verify).

---

### Phase 7 — Relationship identity (`r.id`)

**Do**

- Either **generate** stable `r.id` for 4 684 rels missing it (uuid slug), **or**
- **Retire** `r.id` as a required field and update `_gap_survey.py` accordingly.

Recommendation: **generate** for evidence/regulation rels; leave factual rels without `id` if gap survey allows.

**Accept**

- Documented policy in `AGENTS.md`.
- Gap survey updated; 0 false FAILs.

---

### Phase 8 — Final audit & docs

**Hard checks**

```
MATCH (n) WHERE any(k IN keys(n) WHERE k STARTS WITH 'phase') RETURN count(n)     // 0
MATCH (n) WHERE n.legacy_internal_provenance_docs IS NOT NULL RETURN count(n)       // 0
MATCH (n:Regulierungsfrage) WHERE n.rechtsgrundlagen IS NOT NULL RETURN count(n)  // 0
MATCH ()-[r]->() WHERE r.import_decision IS NOT NULL RETURN count(r)                // 0
MATCH ()-[r]->() WHERE r.merged_legacy_rel_ids IS NOT NULL RETURN count(r)          // 0
MATCH (n:ReuseRule) RETURN count(n)                                               // 0 (if option A)
```

**Targets**

| Metric | Now | Target |
|---|---:|---:|
| Distinct node keys | 107 | **≤ 45** |
| Avg props / node | 8.2 | **≤ 4.5** |
| Distinct rel keys | 63 | **≤ 8** |
| Avg props / rel | 4.3 | **≤ 1.5** (factual), **≤ 3** (evidence) |

Update: `FINAL_AUDIT_REPORT.md`, `AGENTS.md`, obsolete `_gap_survey` invariants (`source_scope`).

---

## 4. Implementation notes

### Script location

Reuse patterns from:

- `_neo4j/review/2026-06-01_minimal_property_audit_*/phaseA_drop/` (batch REMOVE)
- `_neo4j/intake/runs/2026-06-04_regulation_graph_vocabulary/phase*_*.py` (snapshot + gated commit)

New runner: `_neo4j/review/2026-06-05_post_migration_property_cleanup/property_cleanup_apply.py`

Flags: `--phase N`, `--dry-run`, `--commit`, `--export-dir`.

### Guardrails

1. **No silent semantic loss:** export before every `legacy_*` drop.
2. **No edge deletion** in Phases 1–5 (property-only).
3. **Regulation parity** after Phases 2–3: GESTUETZT/GILT/TRIGGERS/ERFORDERT counts unchanged.
4. **Law node evidence** stays until explicitly moved to edges in a future pass.
5. Phases are **independent rollback units** via `phaseN_before.json`.

### What we are *not* cleaning in this plan

- Label/reltype renames (Phase 8 vocabulary run — done).
- `Bauteilebene`, `wiederverwendungsort`, `funktionswechsel` on BTG (intentional Phase 7 semantics).
- `matchingqualitaet_*` on Projekt (74 projects — separate domain decision; default **keep** unless you confirm unused).
- Pruning `source_urls[]` content (URL dedup is a later quality pass).

---

## 5. Recommended order & effort

| Phase | UI impact | Risk | Effort |
|---|---|---|---|
| **1** Bookkeeping | ★★★★ | very low | 1 h |
| **2** Regulation stale props | ★★★ | low | 2 h |
| **4** Rel import/merge meta | ★★★★★ | low | 3 h |
| **3** Legacy array archive | ★★★★★ | medium (export discipline) | 4 h |
| **5** Evidence normalization | ★★★ | medium | 4 h |
| **6** ReuseRule | ★★ | low | 1 h |
| **7** r.id policy | ★ | low | 2 h |
| **0 + 8** Audit/wrap | — | — | 3 h |

**Quick win path:** Phase 0 → 1 → 4 → 2 (same day, ~6 h).  
**Full cleanup:** through Phase 8 (~20 h including tests).

---

## 6. Open decisions (need your call before Phase 3/6)

1. **`legacy_internal_provenance_docs[]`:** archive-off-graph (recommended) vs. keep on a single `MigrationArchive` meta-node?
2. **`ReuseRule`:** delete (A) vs. strip (B)?
3. **`source_titles[]`:** drop entirely or keep where titles add meaning beyond URL?
4. **`r.id`:** backfill vs. retire requirement?
5. **`matchingqualitaet_*` on Projekt:** keep for matching-quality queries or demote to review export?

---

## 7. Status (applied 2026-06-05)

Phases **0–6 and 8** committed via `property_cleanup_apply.py --through 8 --commit`.

- Summary: [`CLEANUP_APPLY_SUMMARY.md`](CLEANUP_APPLY_SUMMARY.md)
- Archives: [`archive/`](archive/)
- Phase 6 used **Option B** (strip `ReuseRule` to `id`/`name`; kept 133 outgoing edges).
- Phase 7 (`r.id` backfill) deferred.

**Not dropped (semantic):** rel `basis`, `role`, `connection_kind`, `scope_note`, `rechtsgrundlage`.
**Kept:** `matchingqualitaet_*` on Projekt.

---

## 8. Follow-up (Phases 4b, 5b, 9 — applied 2026-06-05)

Offload noisy metadata to repo sidecar; graph keeps `metadata_sidecar_key` pointer only.

| Phase | Action |
|---|---|
| **4b** | Export rel `review_status`, `evidence_status`, `review_run` → `sidecar/entity_metadata.jsonl`; set pointer; remove props |
| **5b** | Filter `source_titles[]` via [`source_title_drop_patterns.txt`](source_title_drop_patterns.txt); archive matched nodes; remove entire `source_titles` property |
| **9** | Regulation drift report + doc refresh |

**Results:** 615 rel + 607 node sidecar rows; 0 rels with review metadata props; 0 nodes with `.md` in `source_titles`; 404 `source_urls` nodes unchanged.

**Lookup:** [`sidecar/README.md`](sidecar/README.md) · QA backlog: [`sidecar/qa/needs_source_url_review.csv`](sidecar/qa/needs_source_url_review.csv)

```bash
python property_cleanup_apply.py --through 9 --commit
python property_cleanup_apply.py --phase 5b --commit   # re-run after editing drop list
```
