# Final Cleanup F02 — Merge-redirect rel re-proof (batch 1/2)

**Date:** 2026-06-06 · **Database:** `mit-bestand` · **Mode:** read-only (no graph mutation)  
**Ledger:** [`ledger/final_cleanup_f02.csv`](../ledger/final_cleanup_f02.csv)  
**Scope:** First **10** of **19** Q01/Q02 merge-redirect relationships — Cleveland/timber/WBS70 donor bundle (5) + `bt_decke` regulation edges (5)

## Scope recap

| Bundle | Edges | Prior state | New verdicts |
|---|---:|---|---|
| `bw_cleveland_steel_and_tubes_stock` geo + role | 3 | P6-new-rel-* synthetic PROVEN, empty quote | 2 PROVEN, 1 PARTIAL |
| `bg_stahl_traeger_timber_square` / WBS70 `AUS_SPENDER` | 2 | P6-new-rel-* + Agent 09 PARTIAL | 1 PROVEN, 1 PARTIAL |
| `bt_decke` regulation (EN 1168) | 5 | P6-new-rel-* + agent07-rel-* on merged-away `bt_hohlkoerperdecke` | **5 PROVEN** |
| **Σ (this batch)** | **10** | 10 empty-quote synthetic PROVEN | **8 PROVEN · 2 PARTIAL** |

## Verdict histogram

| Verdict | Count |
|---|---:|
| PROVEN | 8 |
| PARTIAL | 2 |
| UNVERIFIABLE | 0 |

## Evidence method

- **Regulation class** (`bt_decke` ×5): live `source_url` / `source_quote` on graph; re-fetched [EN 1168 iteh catalogue](https://standards.iteh.ai/catalog/standards/cen/e42ae69b-eeba-4f82-b1a2-a0ef748a1752/en-1168-2005a3-2011) (HTTP 200). Replaces P6-06 `basis_type=logic` rows with `basis_type=web` + verbatim `proof_quote`.
- **Donor/geo class**: [cleveland-steel.com](https://cleveland-steel.com/) (HTTP 200); [Timber Development UK](https://timberdevelopment.uk/print-and-ink-buildings-timber-square/) (HTTP 200); dossier `_archive/research/gebaeude/Association_house_Groeditz.md` for Gröditz WBS70 lineage.

## Key findings

### 1. `bt_decke` regulation bundle — full upgrade (5/5 PROVEN)

All five edges carry live `source_url` pointing to EN 1168 and inherited `source_quote` from pre-merge `bt_hohlkoerperdecke` (Agent 07). Fresh fetch confirms catalogue title and scope text for hollow-core slabs in floors/roofs. Prior synthetic rows `P6-new-rel-232327762353` … `P6-new-rel-131653075377` superseded.

### 2. Timber Square → Cleveland — PROVEN (1/1)

TDUK article names both endpoints verbatim:

> *125 tonnes of reused steel was used across both buildings at Timber Square, sourced from Cleveland Steel & Tubes*

Upgrades Q02 redirect survivor (`bg_stahl_traeger_timber_square` —[`AUS_SPENDER`]→ `bw_cleveland_steel_and_tubes_stock`) from Agent 09 PARTIAL (`09-aus_spender-0204` on deprecated `bw_externe_stahl_donor_stockholder`).

### 3. Cleveland `LIEGT_IN_STADT` → London — PARTIAL (geo contradiction)

First-party Cleveland site locates stock at **North Yorkshire, UK**, not London. Edge inherited from pre-merge `bw_cleveland_steel_reclaimed_stock` / Agent 09 `09-lis-0035` (“London stockyard” placeholder). **UK** edge (`LIEGT_IN_LAND`) is PROVEN; **London** city edge needs human relabel or delete.

### 4. WBS70 `AUS_SPENDER` → `bw_school_type_dresden_donor` — PARTIAL (donor mismatch)

Association house dossier documents **two** donor buildings:

> *279 Fertigteile aus einer Schule des Typs Dresden sowie 159 WBS70-Elemente aus einem weiteren Gebäude*

`bg_stahlbeton_mehrere_groeditz_wbs70_precast_panels` is the WBS70 batch; Q02 redirected its `AUS_SPENDER` from deprecated `bw_wbs70_donor_groeditz` to `bw_school_type_dresden_donor` as a pragmatic placeholder. Dossier attributes WBS70 panels to a **separate** building, not the Dresden-type school. **ESCALATE_HUMAN** — restore discrete WBS70 donor Bauwerk or accept documented ambiguity.

### 5. Cleveland `HAT_BAUOBJEKTROLLE` → `bor_donorobjekt` — PROVEN

Contract allows `:Materialdepot` → `:Bauobjektrolle` (EP-02 precedent). Cleveland first-party text on surplus stock from completed projects supports Donorobjekt semantics for the merged stockholder node.

## Worst prior states (upgraded or flagged)

1. **P6-new-rel-*** (all 10) — synthetic PROVEN with empty `proof_quote`; Evidence Gate violation closed for 8/10.
2. **09-aus_spender-0204** — PARTIAL unsourced depot; upgraded via TDUK for Cleveland target.
3. **09-aus_spender-0216** — PARTIAL; redirect target still semantically weak (see finding 4).
4. **09-lis-0035** — inherited London geo now PARTIAL with first-party contradiction.

## Remaining F02 scope (batch 2)

9 relationships not in this ledger: `bt_fassade` (2), `bt_fenster` (4), `mat_glas` (2), `p_timber_square_london` HAT_BAUWERK (1).

## Summary

Re-proved **10/19** merge-redirect relationships read-only on `mit-bestand`. **8 PROVEN** with non-empty verbatim `proof_quote` and correct `basis_type`; **2 PARTIAL** with quotes documenting geo/donor redirect debt for human follow-up. No Neo4j writes performed.
