# Remediation R05 — Orphan Akteur + Vocab Stubs

**Agent:** R05 · **Date:** 2026-06-06 · **Database:** `mit-bestand` (read-cypher)
**Sources:** Agent 14 orphan scan · Agent 12 vocab audit · `REMEDIATION_PLAN.md` §5
**Output ledger:** [`ledger/remediation_r05.csv`](../ledger/remediation_r05.csv)

## Summary

| Group | nodes | degree-0 | proposed CONNECT | FIX_PROPERTY | DEPRECATE (human gate) | KEEP |
|---|---:|---:|---:|---:|---:|---:|
| Akteur orphans | 3 | 3 | 3 | 1 (`repurpose.land`) | 0 | 3 (as entities) |
| Vocab stubs | 8 | 0 inbound each | — | 8 names (already applied) | 3 candidates | 5 |

**Key finding:** The three `Akteur` nodes are **fully disconnected** (degree 0) after the reuse-bubble evidence audit removed unsupported mesh edges. They remain **valid, sourced organisations** — connect structurally via `LIEGT_IN_LAND`, do not deprecate.

The eight vocab stubs are **content-graph orphans** (0 `HAT_BAUTEILTYP` / `NUTZT_MATERIAL` inbound) but **not graph-isolated**: each carries 4–7 outgoing regulation edges (`TRIGGERS_REGULIERUNGSFRAGE`, `ERFORDERT_NACHWEIS`). Human-readable names were backfilled on 2026-06-06 via `fix_property.patch.jsonl`.

---

## 1. Akteur orphans

| id | name | degree | in | out | primary_source_url | overlap / context | action |
|---|---|---:|---:|---:|---|---|---|
| `c33_circular_construction_catalyst` | Circular Construction Catalyst 2033 | 0 | 0 | 0 | circularconstructioncatalyst.ch | CH coordination actor; Tier-2 `cirkla→c33` removed | **CONNECT** `LIEGT_IN_LAND→land_schweiz` |
| `circular_economy_switzerland` | Circular Economy Switzerland | 0 | 0 | 0 | circular-economy-switzerland.ch | CH movement; Tier-2 `cirkla→ces` removed | **CONNECT** `LIEGT_IN_LAND→land_schweiz` |
| `repurpose` | Repurpose | 0 | 0 | 0 | repurpose.nl | NL consultancy / Madopt operator; all Dutch mesh edges Tier-1 deleted; stray `land=NL` | **CONNECT** `LIEGT_IN_LAND→land_niederlande` + **FIX_PROPERTY** drop `land` |

**Not proposed:** Restoring deleted `VERBUNDEN_MIT_AKTEUR` mesh edges — every prior edge failed the two-endpoint evidence test ([`EVIDENCE_AUDIT.md`](../../2026-06-06_cross_bubble_extension/EVIDENCE_AUDIT.md)). `madopt` was intentionally folded into `repurpose` (no separate node).

**Deferred:** Substantive actor relationships need freshly sourced URLs naming **both** endpoints (AGENTS.md rule 3).

---

## 2. Vocab stubs vs curated nodes

Curated comparison set: `bt_fassade`, `bt_fenster`, `mat_glas`, `mat_beton`.

| stub | label | degree | in | out | curated | curated inbound | reg overlap | stub-only reg targets | action |
|---|---|---:|---:|---:|---|---:|---:|---|---|
| `bt_fassadenelement` | Bauteiltyp | 5 | 0 | 5 | `bt_fassade` | 89 | **100%** (5/5) | — | **DEPRECATE_NODE** (human gate) |
| `bt_fassadenmodul_mauerwerk` | Bauteiltyp | 7 | 0 | 7 | `bt_fassade` | 89 | 71% (5/7) | materialprüfung, tragwerk | **KEEP** |
| `bt_glasscheibe` | Bauteiltyp | 7 | 0 | 7 | `bt_fenster` | 72 | 43% (3/7) | sicherheitsglas, absturz, tragwerk | **DEPRECATE_NODE** → `bt_verglasung` |
| `bt_hohlkoerperdecke` | Bauteiltyp | 5 | 0 | 5 | `bt_fassade`* | 89 | 40% (2/5) | standsicherheit, materialprüfung, tragwerk | **KEEP** |
| `bt_mauerstein` | Bauteiltyp | 4 | 0 | 4 | `bt_fassade` | 89 | 50% (2/4) | materialprüfung, tragwerk | **KEEP** |
| `bt_verglasung` | Bauteiltyp | 7 | 0 | 7 | `bt_fenster` | 72 | 43% (3/7) | sicherheitsglas, absturz, tragwerk | **KEEP** (canonical glazing stub) |
| `mat_drahtglas` | Material | 7 | 0 | 7 | `mat_glas` | 69 | 71% (5/7) | absturz, tragwerk | **KEEP** (wired-glass subtype) |
| `mat_spannbeton` | Material | 5 | 0 | 5 | `mat_beton` | 44 | **100% subset** (5/5 ⊆ 8) | — | **DEPRECATE_NODE** (human gate) |

\* `bt_hohlkoerperdecke` is semantically a deck/slab type (`rw_en_1168`); `bt_decke` has no outgoing regulation edges in the live graph, so overlap with `bt_fassade` is expected to be low.

### Duplicate pairs (regulation subgraph)

- **`bt_fassadenelement` ≡ `bt_fassade`** — identical five regulation targets.
- **`bt_glasscheibe` ≡ `bt_verglasung`** — identical seven regulation targets.
- **`mat_spannbeton` ⊂ `mat_beton`** — all spannbeton targets already on beton.

These stubs exist as fine-grain anchors in `build_vocabulary_graph.py` (`TYPE_BY_RW` / `MAT_BY_RW`). Deprecation requires `merge_node` plus off-graph vocabulary list updates — see human gate doc.

---

## 3. Patches drafted

| patch | ops | type | status |
|---|---:|---|---|
| [`remediation_r05_fix_property.patch.jsonl`](../patches/remediation_r05_fix_property.patch.jsonl) | 9 | 1× `remove_node_properties` + 8× `noop_reviewed` (names already live) | safe to dry-run |
| [`remediation_r05_connect_orphans.patch.jsonl`](../patches/remediation_r05_connect_orphans.patch.jsonl) | 3 | `add_rel` `LIEGT_IN_LAND` | safe to dry-run |
| [`remediation_r05_deprecate_candidates.HUMAN_GATE.md`](../patches/remediation_r05_deprecate_candidates.HUMAN_GATE.md) | — | merge/deprecate instructions only | **human gate** |

### Apply (non-destructive batch)

```bash
python _scripts/apply_neo4j_review_patch.py \
  --patch _neo4j/review/2026-06-06_full_graph_verification/patches/remediation_r05_fix_property.patch.jsonl

python _scripts/apply_neo4j_review_patch.py \
  --patch _neo4j/review/2026-06-06_full_graph_verification/patches/remediation_r05_connect_orphans.patch.jsonl
```

Live apply requires `--confirm "APPLY <patch> TO mit-bestand"` per project discipline.

---

## 4. Method

- Live graph queries via Neo4j MCP `read-cypher` on `mit-bestand` (2 296 nodes / 15 338 rels baseline).
- Degree = total incident edges; **orphan** for Akteur = degree 0; **content orphan** for vocab = 0 inbound `HAT_BAUTEILTYP` / `NUTZT_MATERIAL`.
- Regulation overlap = shared `TRIGGERS_REGULIERUNGSFRAGE` + `ERFORDERT_NACHWEIS` targets vs nominated curated node.
- Cross-checked against Agent 01/05/12/14 ledger rows and `fix_property.patch.jsonl` apply report.

Generated 2026-06-06.
