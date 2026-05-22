> ⚠️ **SUPERSEDED by `FINAL_PLAN.md`** (locked decisions + phased migration, 2026-06-05).
> This file is the original exploratory plan, kept for history.

# Plan — Regulation/Proof Vocabulary Overlay

**Date:** 2026-06-04
**Target DB:** `mit-bestand`
**Run id (proposed):** `regulation_graph_vocab_2026_06_04`
**Source prompt:** `_neo4j/intake/inbox/research/reuse_regulation_graph_replacement_prompt_short.md`
**Status:** PLAN — doc-first, no DB writes yet.

---

## 1. Decisions (locked with user)

| Topic | Decision |
|---|---|
| Deliverable | **Doc first, then run.** Phase 1 = analysis + mapping tables (this folder). Phase 2 = idempotent overlay import, only after approval. |
| Strategy | **Rewire only where the live graph already holds clear, correct evidence.** No destructive relabel. Old vocab stays and is parkable. |
| New nodes | **Create fresh `Regulierungsfrage` / `Nachweisforderung` / `Regelwerk` nodes** from the prompt's seed lists + project evidence. Cross-link old→new, do not merge old nodes in. |
| Evidence | **Only migrate edges backed by a real `http(s)` URL.** See §3 — this is the binding constraint. |

---

## 2. Live-graph reality (probed 2026-06-04)

The target labels do **not** exist yet (0 nodes). The "weak" vocab exists and is richly connected:

| Old label | nodes | main incoming edge (count) | has own http evidence? |
|---|---:|---|---|
| `Huerde` | 28 | `HAT_HUERDE` (930) | no |
| `Schadstoff` | 13 | `HAS_RISK_POLLUTANT` (754), `REQUIRES_VERIFICATION_FOR` (339) | no |
| `Norm` | 103 | `REFERENZIERT_NORM` (143), `GILT_IN_LAND` (142) | no (72 BELEGT_IN → NULL-url Quelle) |
| `RechtlicheBedingung` | 16 | `HAT_RECHTLICHE_BEDINGUNG` (26) | no |
| `PruefungNachweis` | 120 | `HAT_PRUEFUNG` (465) | no |
| `Bauproduktstatus` | 15 | `HAT_BAUPRODUKTSTATUS` (34) | no |
| `Leistungsanforderung` | 46 | `HAT_LEISTUNGSANFORDERUNG` (452) | no |

Anchors all present: `Projekt` 86, `Bauteilgruppe` 364, `Bauteiltyp` 23, `Material` 26, `Land` 17.

`Norm` already **is** the prompt's `Regelwerk` layer (Eurocodes, EN 1090, DIN EN 13501 … are `norm_*` nodes with country links). `PruefungNachweis` already **is** `Nachweisforderung`. Only `Regulierungsfrage` (the question/topic grouping) is genuinely new content.

---

## 3. The binding constraint — where real evidence actually is

**No regulation edge carries an `http` URL, and the vocab nodes have no http source of their own.** The only real `http(s)` evidence near these relationships is on the **anchor** (`Projekt`/`Bauteilgruppe`) via `BELEGT_IN`→`Quelle(https)`.

Migratable pool under "real URL required" (source-anchor has http `BELEGT_IN`):

| Old relationship | total | migratable | maps to new edge |
|---|---:|---:|---|
| `HAT_PRUEFUNG` | 465 | 152 | `(anchor)-[:ERFORDERT_NACHWEIS]->(:Nachweisforderung)` |
| `REQUIRES_VERIFICATION_FOR` | 339 | 134 | `(:Projekt)-[:ERFORDERT_NACHWEIS]->(:Nachweisforderung)` (Schadstoff-check) |
| `REFERENZIERT_NORM` | 143 | 97 | `(anchor)-[:GESTUETZT_AUF_REGELWERK]->(:Regelwerk)` |
| `HAT_HUERDE` | 930 | 96 | `(anchor)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage)` |
| `HAT_BAUPRODUKTSTATUS` / `HAT_LEISTUNGSANFORDERUNG` / `REGULIERT` | 511 | 0 | — (no anchor http evidence; defer) |

> **Honesty caveat:** an anchor having a documented source page proves project provenance, not that the specific rule applies. `evidence_status` on these edges must be set accordingly (`case_documented` for the project's own URL; not `rule_documented`). Genuinely rigorous rule-level evidence needs the new-research option that was deferred.

**Implication:** the strict, defensible Phase-2 import is **~300–480 edges**, concentrated on `Nachweisforderung` and `Regelwerk`, with `Regulierungsfrage` thinner. `Bauproduktstatus`/`Leistungsanforderung` stay parked until evidence exists.

---

## 4. Target model (overlay, additive)

New labels + edge types (from prompt):

```
(:Projekt|:Bauteilgruppe|:Bauteiltyp|:Material|:Land)
  -[:TRIGGERS_REGULIERUNGSFRAGE]-> (:Regulierungsfrage)
  -[:ERFORDERT_NACHWEIS]->         (:Nachweisforderung)
  -[:GESTUETZT_AUF_REGELWERK]->    (:Regelwerk)
(:Regelwerk)-[:GILT_IN_LAND]->(:Land)
```

Old→new bridge edges (provenance, never deletes old):
```
(:Norm)-[:OLD_NODE_MAPPED_TO]->(:Regelwerk)
(:PruefungNachweis)-[:OLD_NODE_MAPPED_TO]->(:Nachweisforderung)
(:Huerde)-[:OLD_NODE_MAPPED_TO]->(:Regulierungsfrage)
```

Every new/migrated edge carries: `evidence_status, evidence_type, source_url, source_quote,
applicability_reason, missing_info, confidence, review_run, created_at_utc`.
New nodes carry `source_scope = 'regulation_graph_vocab_2026_06_04'` for clean rollback.

---

## 5. Node ID convention (fresh nodes)

| Label | id prefix | example |
|---|---|---|
| `Regulierungsfrage` | `rf_` | `rf_schadstofffrage`, `rf_brandschutzfrage` |
| `Nachweisforderung` | `nf_` | `nf_asbestcheck`, `nf_standsicherheitsnachweis` |
| `Regelwerk` | `rw_` | `rw_din_spec_91484`, `rw_eurocode_en_1990_1999` |

Seed counts from prompt: 10 `Regulierungsfrage`, 23 `Nachweisforderung`, ~40 `Regelwerk`.
`Regelwerk` seed list is reconciled against existing 103 `norm_*` nodes (bridge, don't duplicate).

---

## 6. Phase 1 deliverables (this run, no DB writes)

Build the 5 prompt tables as Markdown + machine-readable companions:

1. `01_replacement_vocabulary.md` — `old_label | old_node | replacement_label | replacement_node | action | reason`
2. `02_target_vocabulary.md` — full `rf_/nf_/rw_` node list with `core/optional/park` + `replaces_old_nodes`
3. `03_project_mapping.md` — per `Projekt`: triggered Regulierungsfrage / Nachweis / Regelwerk + evidence_status
4. `04_component_mapping.md` — per `Bauteilgruppe/Bauteiltyp/Material`
5. `selected_edges.jsonl` + `05_edge_import.csv` — CSV-ready, **only rows with real `http` source_url**
6. `GAPS.md` — the 511 edges with no usable evidence (parked, with what research would unlock them)

## 7. Phase 2 (after approval) — overlay import

- `_run_regulation_vocab_overlay.py`, modeled on
  `2026-06-04_300_evidence_connections/_run_import_300_evidence_connections.py`:
  - idempotent `MERGE` on node `id` and edge `id`;
  - tag everything `review_run = 'regulation_graph_vocab_2026_06_04'`;
  - reuse existing `mat_*/bt_*/land_*` anchor ids (closed sets — never invent);
  - selection gate identical to §3 (skip any row lacking http `source_url`).
- Rollback:
  ```cypher
  MATCH ()-[r {review_run:'regulation_graph_vocab_2026_06_04'}]->() DELETE r;
  MATCH (n {source_scope:'regulation_graph_vocab_2026_06_04'}) DETACH DELETE n;
  ```
- Validation: every new edge has 7 evidence fields; no off-vocab anchor ids; counts match Phase-1 CSV.

---

## 8. Open questions before Phase 1 build

1. **Regulierungsfrage is the thin layer** (only ~96 evidenced `Huerde` edges, 0 for Leistungsanforderung/Bauproduktstatus). Accept a thin Regulierungsfrage in v1, or invest the deferred research to populate it?
2. **Regelwerk vs existing `Norm`:** fresh `rw_*` nodes bridged to `norm_*` (chosen) will visually duplicate the 103 norms in any combined view. Confirm that's acceptable for the "clean graph view," or should the clean view filter old labels out.
3. **Anchor-source-as-edge-evidence** (§3 caveat): accept `evidence_status=case_documented` using the project's own URL, or hold these as `expert_inferred` with `missing_info` flagged?
