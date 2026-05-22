# Keep-list decision matrix — extreme property minimization (mit-bestand)

**Date:** 2026-06-01  **Database:** `mit-bestand`  **Mode of this document:** proposal for approval; no graph writes yet.

## Goal
Reduce every in-scope node label to a hard minimum (target ~4 properties), keeping
only properties that are *consistent* (present across the label) and *necessary*
(irreducible semantic meaning not available via a relationship or a `Quelle` node).

## Inputs (all live, this graph state: 39,165 nodes / 80,135 rels)
- Fresh read-only audit: `node_property_minimization.csv`, `PER_LABEL_DIGEST.txt`.
- Relationship-coverage probes: `REL_COVERAGE_PROBES.md`.
- Per-pair verdicts: `KEEP_LIST_DECISION_MATRIX.csv`.
- Per-label summary + budget flags: `KEEP_LIST_DECISION_MATRIX_SUMMARY.md`.

## Verdict legend
| Verdict | Meaning | Pairs |
|---|---|---:|
| `keep_core` | `id` / `name` identity + caption | 127 |
| `keep_semantic` | domain-essential survivor (counts to the ~4 budget) | 74 |
| `domain_review` | surplus domain field; keep only if you actively query it | 54 |
| `drop` | bookkeeping / cache / provenance already carried by edges or re-derivable | 426 |
| `migrate_then_drop` | provenance is the ONLY copy (no `BELEGT_IN`) → migrate to edges first | 7 |
| `migrate_edge_then_drop` | topology duplicate with edge gaps → create missing edges first | 4 |
| `move_to_relationship` | topology duplicate with full edge coverage → drop after re-confirm | 1 |
| `meta_separate` | audit/meta label (`DataIssue`, `DossierEntityTarget`, `DeprecatedType`, `ReuseRule`, `OntologyAnchor`) → handled in the meta-node decision | 74 |

## Proposed minimal schema (highlights)
- **Controlled-vocabulary labels (~40):** `id`, `name` (+ `scope_note`/`name_full` where they carry a real definition). Drop `source_scope` (constant `controlled_vocab_seed`), `review_status`, `source_resolution_status`, all `strict_*`, all `evidence_*`.
- **Source layer:** `Quelle`/`ExternalLink` → `id`, `url`, `quelltyp`, `title`; `ResearchDocument` → `id`, `name`, `quelltyp`, `source_file`; `SectionRef` → `id`, `name`, `url`; `Dossier` → `id`, `name`, `quelltyp`. Drop the entire `url_*` probe/cache block, `source_url*`, `evidence_*`, `strict_*` (re-derivable by re-probing; not semantic).
- **Akteur:** `id`, `name`. All `source_*`/`strict_*`/`evidence_*`/`review_*` drop (provenance on `BELEGT_IN`, 532/669). `land` → migrate to `LIEGT_IN_LAND` then drop.
- **Bauteilgruppe:** core `id`, `name`, `bg_kind`, `reuse_status`; `primary_bauteiltyp_id` → relationship (already 100% `HAT_BAUTEILTYP`); `primary_material_id` → migrate missing `NUTZT_MATERIAL` (35) then drop; functional/quantity/boolean facets → `domain_review`.
- **Kennwert (justified fact label):** keep the fact fields (`kennwert`, `wert`/`wert_text`, `einheit`, `category`, `method`, `bilanzgrenze`, `fact_index`). **Provenance (`source_id`, `source_urls`) must be migrated to `BELEGT_IN` first** — Kennwert has zero `BELEGT_IN` today.
- **Land / BauwerkEra / Geltungsbereich / LCAModule / Norm:** justified above 4 because their attributes are the node's reason to exist.

See `KEEP_LIST_DECISION_MATRIX_SUMMARY.md` for the full per-label table.

## Phased enforcement (after approval; each phase: backup → dry-run → apply → gap-survey + re-audit)
1. **Provenance/cache drop** (`drop`, 426 pairs): the big reduction on source + semantic + vocab nodes. Safe because provenance is on `BELEGT_IN`/`Quelle` or is re-derivable cache.
2. **Provenance migration then drop** (`migrate_then_drop`, 7): build `BELEGT_IN` for `Kennwert`/`Norm` from `source_id`/`source_urls`/`evidence_source_id`, then drop the props.
3. **Topology-duplicate removal** (`move_to_relationship` 1 + `migrate_edge_then_drop` 4): re-confirm `HAT_BAUTEILTYP`; create missing `NUTZT_MATERIAL`(35) and `LIEGT_IN_LAND`(Akteur 79, Bauwerk/Materialdepot few); then drop `primary_*_id` / `land`.
4. **Domain pruning** (`domain_review`, 54): apply your keep/drop decisions on surplus domain fields.
5. **Meta-node decision** (`meta_separate`, 74; `DataIssue` 28,729 nodes): keep / strip / delete — separate gate.

## Open decision points (need your yes/no before writes)
1. **URL probe/health block** (`url_status`, `url_http_code`, `url_final_url`, `url_redirect_chain`, `url_content_*`, `url_server_header`, `url_wayback_*`, etc. on the source layer): drop entirely (re-derivable by re-probing) — **proposed**, vs keep one health field, vs move to a dedicated probe node.
2. **`source_scope`** (on 64 labels, mostly the constant `controlled_vocab_seed` / scan tags): drop everywhere — **proposed** — vs keep on entity/source labels for provenance lineage.
3. **`name_full` / `aliases` / `scope_note`**: counted inside the ~4 (current proposal) vs always-allowed on top.
4. **`domain_review` (54 fields)**: default action if you don't single any out — **proposed: keep them** (only flagged, not dropped) vs drop all to force a stricter minimum.
5. **`DataIssue` (28,729 nodes, 73% of the graph):** keep as audit ledger / strip-to-minimum / delete (Phase 3 Option A deletes `DataIssue` + incident edges).
