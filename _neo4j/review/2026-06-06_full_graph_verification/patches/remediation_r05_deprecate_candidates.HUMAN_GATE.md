# Remediation R05 — DEPRECATE_NODE candidates (human gate)

**Agent:** R05 · **Date:** 2026-06-06 · **Database:** `mit-bestand`
**Do not auto-apply.** Each item requires human approval and a gated `merge_node` / `delete_node` patch.

---

## Decision matrix

| node | degree | in | curated overlap | regulation-only? | recommendation |
|---|---:|---:|---|---|---|
| `bt_fassadenelement` | 5 | 0 | 100% reg duplicate of `bt_fassade` | yes (5 outgoing reg edges) | **DEPRECATE** → merge into `bt_fassade` |
| `bt_glasscheibe` | 7 | 0 | 43% vs `bt_fenster`; **100% duplicate of `bt_verglasung`** | yes | **DEPRECATE** → merge into `bt_verglasung` |
| `bt_verglasung` | 7 | 0 | 43% vs `bt_fenster` | yes | **KEEP** (canonical glazing stub) |
| `mat_spannbeton` | 5 | 0 | 100% reg subset of `mat_beton` | yes | **Human choice:** DEPRECATE→`mat_beton` **or** KEEP for prestressed semantics |

**Explicit KEEP (not on this gate list):** `bt_fassadenmodul_mauerwerk`, `bt_hohlkoerperdecke`, `bt_mauerstein`, `mat_drahtglas` — regulation anchors with partial overlap only.

---

## 1. `bt_fassadenelement` → merge into `bt_fassade`

**Why deprecate:** Zero `HAT_BAUTEILTYP` inbound (vs 89 on `bt_fassade`). All five outgoing `TRIGGERS_REGULIERUNGSFRAGE` / `ERFORDERT_NACHWEIS` targets are identical to `bt_fassade`.

**Why it exists:** `build_vocabulary_graph.py` `TYPE_BY_RW["rw_en_13830"]` lists both `bt_fassade` and `bt_fassadenelement` as component anchors for EN 13830 curtain-wall scope.

**If approved:**
1. `merge_node` `bt_fassadenelement` → `bt_fassade` (redirects 5 outgoing reg edges).
2. Update `TYPE_BY_RW` / any off-graph seed to drop `bt_fassadenelement` or alias it to `bt_fassade`.
3. Re-run Agent 12 orphan scan.

**Risk if kept:** Harmless but redundant regulation subgraph; confuses vocabulary hygiene audits.

---

## 2. `bt_glasscheibe` → merge into `bt_verglasung`

**Why deprecate:** `bt_glasscheibe` and `bt_verglasung` share the **same seven** regulation targets (verified live). Neither has content-graph inbound edges. `bt_verglasung` is the broader, preferred label.

**Why they exist:** Both listed in `TYPE_BY_RW` for `rw_din_18008` and `rw_glas_reuse_igu`.

**If approved:**
1. `merge_node` `bt_glasscheibe` → `bt_verglasung`.
2. Deduplicate `TYPE_BY_RW` entries to a single glazing anchor.
3. Optional: add `HAT_BAUTEILTYP` from relevant `Bauteilgruppe` nodes to `bt_verglasung` when content wiring resumes.

**Risk if kept:** Duplicate regulation paths for identical claims.

---

## 3. `mat_spannbeton` → merge into `mat_beton` (optional)

**Why deprecate:** All five regulation targets on `mat_spannbeton` are a subset of `mat_beton`'s eight targets. Zero `NUTZT_MATERIAL` inbound (vs 44 on `mat_beton`).

**Why it exists:** `MAT_BY_RW["rw_en_1168"]` includes `mat_spannbeton` for prestressed hollow-core floor rules.

**If approved:**
1. `merge_node` `mat_spannbeton` → `mat_beton`.
2. Ensure `rw_en_1168` `BETRIFFT_MATERIAL` still resolves via `mat_beton` (+ `mat_stahlbeton`).

**If rejected (KEEP):** Document that `mat_spannbeton` is an intentional prestressed subtype anchor despite content-graph orphan status.

---

## Akteur orphans — not on deprecate list

`c33_circular_construction_catalyst`, `circular_economy_switzerland`, and `repurpose` are **real, sourced organisations**. Prior `VERBUNDEN_MIT_AKTEUR` mesh edges were correctly deleted (Tier 1/2 evidence audit). **Do not DEPRECATE.**

Approved structural fix (non-destructive): `LIEGT_IN_LAND` edges in `remediation_r05_connect_orphans.patch.jsonl`.

Substantive actor relationships (e.g. evidenced CH coordination ties, Repurpose↔Insert) require **fresh URL proof naming both endpoints** before any `VERBUNDEN_MIT_AKTEUR` restore.

---

## Apply discipline

```bash
# Safe property + structural connect (dry-run first)
python _scripts/apply_neo4j_review_patch.py \
  --patch _neo4j/review/2026-06-06_full_graph_verification/patches/remediation_r05_fix_property.patch.jsonl

python _scripts/apply_neo4j_review_patch.py \
  --patch _neo4j/review/2026-06-06_full_graph_verification/patches/remediation_r05_connect_orphans.patch.jsonl

# Deprecation merges — build separately after human sign-off
# --confirm "APPLY remediation_r05_deprecate_<item>.patch.jsonl TO mit-bestand"
```
