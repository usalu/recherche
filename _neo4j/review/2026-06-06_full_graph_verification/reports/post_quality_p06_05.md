# Post Quality Pass P6-05 — Element ledger surgery

**Date:** 2026-06-06 · **Database:** `mit-bestand`
**Mode:** READ-ONLY graph export + ledger reconcile (no graph writes)

## Live mit-bestand counts

| Metric | Value |
|---|---:|
| Nodes | 2,264 |
| Relationships | 15,063 |
| Export UTC | 2026-06-06T18:03:55.104835+00:00 |

## Ledger delta summary

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Element ledger rows | 17,596 | 17,308 | -288 |
| PROVEN rows | 15,431 | 15,349 | — |
| PROVEN % | 87.70% | 88.68% | — |

## Operations by quality-pass scope

| Scope | REMOVE | Notes |
|---|---:|---|
| Q1 merges + EP02 rel delete | 56 | 8 vocab stub merges + `stadt_zuerich` HAT_AKTEURTYP |
| Q2 depot deletes | 141 | 17 Materialdepot placeholders removed |
| Q4 catalogue deletes | 107 | 107 unsupported HAT_BAUTEILTYP / NUTZT_MATERIAL edges |
| Graph-absent (unclassified) | 1 | Incident rels on deleted nodes / other stale keys |
| **REMOVE total** | **305** | |

| Scope | ADD | Notes |
|---|---:|---|
| Q3 PruefungNachweis nodes | 5 | 5 catalog extensions |
| Q3 ERFUELLT_NACHWEIS edges | 12 | 12 fulfillment edges |
| **ADD total** | **17** | |

## Coverage check (ledger v2 vs live graph)

| Check | Count |
|---|---:|
| Live nodes | 2,264 |
| Live rels | 15,063 |
| Ledger-covered nodes | 2,264 |
| Ledger-covered rels | 15,044 |
| Uncovered live nodes | 0 |
| Uncovered live rels | 19 |

### Residual uncovered rels (out of P6-05 scope)

These 19 live edges have no ledger row yet — mostly **Q01 merge redirects** (regulation edges now on `bt_decke` / `bt_fassade` / `bt_fenster` / `mat_glas` survivors) and **Q02 redirect** (`bw_cleveland_steel_and_tubes_stock`, WBS70 `AUS_SPENDER`). Not stale deletions; new graph elementIds after merge/redirect. Deferred to a follow-up element-proof pass.

- `bw_cleveland_steel_and_tubes_stock` —[`HAT_BAUOBJEKTROLLE`]→ `bor_donorobjekt`
- `bw_cleveland_steel_and_tubes_stock` —[`LIEGT_IN_STADT`]→ `stadt_london`
- `bw_cleveland_steel_and_tubes_stock` —[`LIEGT_IN_LAND`]→ `land_vereinigtes_koenigreich`
- `bg_stahlbeton_mehrere_groeditz_wbs70_precast_panels` —[`AUS_SPENDER`]→ `bw_school_type_dresden_donor`
- `bg_stahl_traeger_timber_square` —[`AUS_SPENDER`]→ `bw_cleveland_steel_and_tubes_stock`
- `bt_decke` —[`ERFORDERT_NACHWEIS`]→ `nf_standsicherheitsnachweis`
- `bt_decke` —[`ERFORDERT_NACHWEIS`]→ `nf_materialpruefung`
- `bt_decke` —[`ERFORDERT_NACHWEIS`]→ `nf_produktstatus_und_leistungserklaerung`
- `bt_decke` —[`TRIGGERS_REGULIERUNGSFRAGE`]→ `rf_bauproduktstatus_frage`
- `bt_decke` —[`TRIGGERS_REGULIERUNGSFRAGE`]→ `rf_tragwerkssicherheit_frage`
- `bt_fassade` —[`ERFORDERT_NACHWEIS`]→ `nf_materialpruefung`
- `bt_fassade` —[`TRIGGERS_REGULIERUNGSFRAGE`]→ `rf_tragwerkssicherheit_frage`
- `bt_fenster` —[`ERFORDERT_NACHWEIS`]→ `nf_materialpruefung`
- `bt_fenster` —[`ERFORDERT_NACHWEIS`]→ `nf_sicherheitsglas_info`
- `bt_fenster` —[`ERFORDERT_NACHWEIS`]→ `nf_absturzsicherung`
- `bt_fenster` —[`TRIGGERS_REGULIERUNGSFRAGE`]→ `rf_tragwerkssicherheit_frage`
- `mat_glas` —[`ERFORDERT_NACHWEIS`]→ `nf_absturzsicherung`
- `mat_glas` —[`TRIGGERS_REGULIERUNGSFRAGE`]→ `rf_tragwerkssicherheit_frage`
- `p_timber_square_london` —[`HAT_BAUWERK`]→ `bw_cleveland_steel_and_tubes_stock`

## Outputs

- Draft ledger: [`VERIFICATION_LEDGER_ELEMENT_v2.csv`](../VERIFICATION_LEDGER_ELEMENT_v2.csv)
- Delta log: [`ledger/post_quality_p06_05.csv`](../ledger/post_quality_p06_05.csv)
- Graph export: [`_p06_05_work/graph_counts.json`](../_p06_05_work/graph_counts.json)

## Method

1. Exported live `elementId` index from `mit-bestand` (read-only).
2. Dropped ledger rows whose node/rel keys no longer resolve in the live graph.
3. Classified removals against Q01 merge/delete, Q02 depot delete, Q04 catalogue delete patch triples.
4. Appended element rows for Q03 `PruefungNachweis` nodes and `ERFUELLT_NACHWEIS` edges present in live graph but absent from ledger.

**Input baseline:** EP-10 merged ledger rebuilt from shards + `_agent10_work` graph snapshot (17,596 rows).

**Note:** This is a draft `v2` ledger — not yet promoted to canonical `VERIFICATION_LEDGER_ELEMENT.csv`.
