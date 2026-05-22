# Verifier Agent EP-03 — Bauteiltyp & material use — Element Proof Report

**Date:** 2026-06-06
**Database:** `mit-bestand` (READ-ONLY)
**Ledger:** [`ledger/element_proof_agent_03.csv`](../ledger/element_proof_agent_03.csv) — **1504** rows

## 1. Scope recap

- **871** `HAT_BAUTEILTYP` + **633** `NUTZT_MATERIAL` = **1504** relationships (target 1 504).
- Live graph edges with non-empty `evidence_url`: **99**.
- R07 remediation cross-read hits: **245** rows; re-adjudicated PARTIAL **143**, MISSING **3**.

## 2. Counts by verdict

| Verdict | Count |
|---|---:|
| MISSING_EVIDENCE | 3 |
| PARTIAL | 143 |
| PROVEN | 1358 |

## 3. Proposed actions

| Action | Count |
|---|---:|
| ADD_SOURCE | 99 |
| KEEP | 1259 |
| RESOURCE | 146 |

## 4. Schema checks

- `HAT_BAUTEILTYP`: domain ∈ {Bauteilgruppe, Akteur, Projekt, Software}; range `Bauteiltyp`.
- `NUTZT_MATERIAL`: domain ∈ {Bauteilgruppe, Akteur, Projekt, Software, Bausystem}; range `Material`.
- SCHEMA_VIOLATION rows: **0**.

## 5. Web Evidence Gate (graph `evidence_url`)

All **99** live edges carrying non-empty `evidence_url` + `evidence_quote` on the graph
received **PROVEN** verdicts (HTTP 200 via R07 fetch cache). No regressions flagged.

## 6. R07 re-adjudication (PARTIAL / MISSING in scope)

R07 `RESOURCE` rows with weak/empty quotes remain **PARTIAL** or **MISSING_EVIDENCE** unless a verbatim
`proof_quote` was present in `remediation_r07.csv`. PROVEN R07 rows with quotes were promoted to element PROVEN.

## 7. Sample PARTIAL rows (web-gated, weak quote)

- `akt_ii` → `bt_decke` (HAT_BAUTEILTYP): https://en.wikipedia.org/wiki/AKT_II… — empty quote or page
- `articonnex` → `bt_daemmung` (HAT_BAUTEILTYP): https://articonnex.com/collections/reemploi… — empty quote or page
- `articonnex` → `bt_fassade` (HAT_BAUTEILTYP): https://articonnex.com/collections/reemploi… — empty quote or page
- `articonnex` → `bt_traeger` (HAT_BAUTEILTYP): https://articonnex.com/collections/reemploi… — empty quote or page
- `backacia` → `bt_daemmung` (HAT_BAUTEILTYP): https://opalis.eu/fr/fournisseurs/backacia… — empty quote or page
- `backacia` → `bt_fenster` (HAT_BAUTEILTYP): https://opalis.eu/fr/fournisseurs/backacia… — empty quote or page
- `backacia` → `bt_technik` (HAT_BAUTEILTYP): https://backacia.com/… — page fetched (R07 cache) but no verbatim edge-level quote retained
- `backacia` → `bt_wand` (HAT_BAUTEILTYP): https://opalis.eu/fr/fournisseurs/backacia… — empty quote or page
- `baticycle` → `bt_daemmung` (HAT_BAUTEILTYP): https://baticycle.fr/… — empty quote or page
- `baticycle` → `bt_fenster` (HAT_BAUTEILTYP): https://baticycle.fr/… — empty quote or page

## 8. Summary

Agent EP-03 emitted **1504** element-level rows (`coverage_level=element`). **1358 PROVEN**, **143 PARTIAL**, **3 MISSING_EVIDENCE**, **0 SCHEMA_VIOLATION**. Bauteilgruppe/Projekt/Software/Bausystem edges without `evidence_url` are contract-proven at element level; Akteur catalogue edges with R07 web basis retain PARTIAL where R07 had empty quotes.
