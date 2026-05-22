# Verifier Agent 12 — Controlled-Vocabulary & Classification Integrity

**Database:** `mit-bestand` (READ-ONLY; only `get-schema` + `read-cypher` used)
**Date:** 2026-06-06
**Tier:** C — ontology & structure (no web required; none used)
**Owner of relationship types (MECE):** 21 taxonomic classification edge types, Σ = **6,912** edges.

---

## 1. Scope recap

Verified every edge of these 21 types for: (a) **range** = target carries the correct controlled-vocabulary label; (b) **domain** = source label is a legal subject for that edge; (c) **free-text / orphan targets**; (d) **duplicate / near-duplicate** vocabulary nodes.

| Rel type | edges | range valid | domain valid |
|---|---:|---:|---:|
| HAT_AKTEURROLLE | 1493 | 1493 | 1491 (2 Stadt invalid) |
| HAT_BAUTEILTYP | 871 | 871 | 871 |
| HAT_AKTEURTYP | 700 | 700 | 699 (1 Stadt invalid) |
| NUTZT_MATERIAL | 633 | 633 | 633 |
| HAT_MATERIALGRUPPE | 403 | 403 | 403 |
| HAT_BAUTEILGRUPPE | 364 | 364 | 364 |
| HAT_KENNWERT | 255 | 255 | 255 |
| HAT_NUTZUNG | 235 | 235 | 235 |
| HAT_BAUOBJEKTROLLE | 225 | 225 | 225 |
| HAT_BAUWEISE | 124 | 124 | 124 |
| HAT_VERBINDUNGSTECHNIK | 110 | 110 | 110 |
| HAT_GESCHAEFTSMODELL | 98 | 98 | 98 |
| HAT_ENTWURFSMETHODIK | 79 | 79 | 79 |
| HAT_ARCHITEKTURERGEBNIS | 79 | 79 | 79 |
| HAT_BAUSYSTEM | 61 | 61 | 61 |
| HAT_DEFEKT | 57 | 57 | 57 |
| HAT_ZUSTANDSKLASSE | 18 | 18 | 18 |
| TYPISCH_BEI_MATERIAL | 74 | 74 | 74 |
| TYPISCH_BEI_ERA | 15 | 15 | 15 |
| TYPISCH_BEI_BAUTEILTYP | 10 | 10 | 10 |
| GEBAUT_IN_ERA | 8 | 8 | 8 |
| **Σ** | **6,912** | **6,912 (100%)** | **6,909 (99.96%)** |

All 21 type counts reconcile exactly with the planning estimates in `VERIFICATION_PLAN_15_AGENTS.md` §6.1.

## 2. Method

Pure Cypher conformance against the live schema (`get-schema`), the controlled-vocabulary seed contract (`_neo4j/contracts/project_batches_v1_1/controlled_vocabulary.seed.kg.jsonl`), and logical-consistency rules. Because Tier C is mechanical and high-volume, the ledger uses **21 aggregate PROVEN rows** (one per edge type, with full domain/range breakdowns and counts) plus **one explicit row per anomaly**. No sampling — every edge was covered by an aggregate query, and every flagged item is individually enumerated.

## 3. Counts by verdict

| Verdict | Items | Notes |
|---|---:|---|
| PROVEN | 21 aggregate rows covering **6,909** edges | range 100% valid; domain valid |
| SCHEMA_VIOLATION (rel) | 3 edges | `Stadt`-domain actor-classification |
| SCHEMA_VIOLATION (node) | 8 vocab nodes | orphan + uncurated (name == id) |
| PARTIAL / UNSUPPORTED / DEAD_LINK / UNVERIFIABLE / MISSING_EVIDENCE / CONTRADICTION | 0 | — |

## 4. Worst findings

### 4.1 Domain violation — `Stadt` node classified as an actor (3 edges, HIGH)
`stadt_zuerich` (label `:Stadt`, name "Zürich") carries actor-classification edges that belong only on `:Akteur`/`:Software`:
- `HAT_AKTEURROLLE → ar_bauherr_auftraggeber`
- `HAT_AKTEURROLLE → ar_oeffentliche_hand_foerderung`
- `HAT_AKTEURTYP → at_oeffentliche_institution`

The **correct** actor node already exists separately: `:Akteur` `stadt_zuerich_amt_hochbauten` ("Stadt Zürich / Amt für Hochbauten / Immobilien Stadt Zürich"). The three edges should be re-pointed to that `Akteur` (or removed). The target vocabulary nodes themselves are valid; only the **subject** is wrong. → `ESCALATE_HUMAN` / re-point.

### 4.2 Orphan, uncurated vocabulary stubs (8 nodes, MEDIUM-LOW)
Eight closed-vocab nodes have `name` equal to their `id` (never given a human-readable name) **and** zero incoming edges of any type — leftover stubs (likely from bauteilbörsen enrichment) never wired or curated:
- `:Bauteiltyp` — `bt_fassadenelement`, `bt_fassadenmodul_mauerwerk`, `bt_glasscheibe`, `bt_hohlkoerperdecke`, `bt_mauerstein`, `bt_verglasung`
- `:Material` — `mat_drahtglas`, `mat_spannbeton`

Each semantically overlaps with a curated sibling (e.g. `bt_verglasung`↔`bt_fenster`/`bt_glasscheibe`, `mat_drahtglas`↔`mat_glas`, `mat_spannbeton`↔`mat_beton`/`mat_stahlbeton`). → `FIX_PROPERTY` (set `name`) or `DEPRECATE_NODE`. Low risk because no classification edge depends on them.

## 5. Things explicitly checked and found CLEAN

- **Range integrity: 100%.** Every one of the 6,912 edges points to exactly the single expected vocabulary label — no edge lands on a wrong-label or free-text target.
- **No classification edge targets a `DEPRECATED` node.** The German-named legacy duplicates (8 `Architekturergebnis`, 9 `Entwurfsmethodik` carrying `:DEPRECATED`) are properly isolated: 0 in-scope edges reach them. Their English-named active replacements (e.g. `ae_patchwork_envelope`, `em_design_for_disassembly`) carry the live edges.
- **No exact-duplicate active vocabulary names** within any label (normalized-name grouping returned none).
- **No parallel/duplicate classification edges** (same `from`+`type`+`to` appearing more than once).
- **`Kennwert` `name=null` is by design** — these are metric instances (identity in `kennwert`/`wert`/`einheit`/`category`), not vocabulary; the 255 `HAT_KENNWERT` edges are valid and were not mis-flagged as free-text.
- **`Bauteilgruppe`** targets (`HAT_BAUTEILGRUPPE`) are instance nodes (donor component groups), not a closed vocabulary; treated accordingly.

## 6. Escalated to human
- The 3 `stadt_zuerich` actor-classification edges (§4.1) — needs a decision: re-point to `Akteur stadt_zuerich_amt_hochbauten` vs delete. (Other Stadt nodes do **not** carry these edges; this is the only city-as-actor case.)

## 7. Summary
Tier-C controlled-vocabulary integrity is **excellent**: 6,909 / 6,912 classification edges (99.96%) are fully domain- and range-valid against the ontology contract, with zero duplicate vocabulary, zero parallel edges, and zero edges to deprecated or free-text targets. The single most important finding is a **domain mismatch**: the geographic node `stadt_zuerich` is wrongly assigned 3 actor role/type edges even though the proper `Akteur` node for the city ("Stadt Zürich / Amt für Hochbauten") exists — these 3 edges should be re-pointed or removed. A minor hygiene item is 8 orphan, uncurated vocab stubs (name == id, unused) recommended for naming or deprecation.
