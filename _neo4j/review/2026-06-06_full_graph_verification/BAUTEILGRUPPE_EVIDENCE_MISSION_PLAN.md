# Bauteilgruppe Evidence Mission Plan

**Date:** 2026-06-07T12:53:56Z · **Database:** `mit-bestand` · **Mode:** PLAN ONLY (no deletes)

## Why sensitive

- **364** `:Bauteilgruppe` nodes; all ids use `bg_` prefix; **no** `canonical_name` / `primary_source_url` on nodes.
- **6684** live edges touch Bauteilgruppe (**W4 skipped 416** pending W3 deletes).
- Naming encodes material + component + project slug (`bg_stahlbeton_mehrere_haus_hos_floor_elements`) from **multiple intake sources**; `name` display string often differs.
- v5 ledger: **852** UNSUPPORTED rel rows involve bg_ (deferred from W4).
- Rel properties carry **no** `evidence_url` / `evidence_quote` on bg_ outbound edges today.

## Scope inventory

| Surface | Count |
|---|---:|
| Bauteilgruppe nodes | 364 |
| Outbound rels | 6251 |
| Inbound rels | 433 |
| Total touching edges | 6684 |

### Outbound rel types (top)

| rel_type | count |
|---|---:|
| ERFORDERT_NACHWEIS | 955 |
| TRIGGERS_REGULIERUNGSFRAGE | 722 |
| HAT_PROZESSPHASE | 567 |
| HAT_BESCHAFFUNGSWEG | 468 |
| HAT_BAUTEILTYP | 465 |
| NUTZT_MATERIAL | 390 |
| HAT_MATERIALGRUPPE | 375 |
| HAT_LOGISTIK | 337 |
| HAT_RUECKBAUVERFAHREN | 305 |
| HAT_ERGEBNIS | 291 |
| IN_EMPFANGSOBJEKT | 278 |
| HAT_RESSOURCENQUELLE | 256 |

### Inbound rel types

| rel_type | count |
|---|---:|
| HAT_BAUTEILGRUPPE | 364 |
| BETEILIGT_AN | 69 |

## Naming variants (samples)

- `bg_stahl_gelaender_verbiest_charleroi` → display name: **Geländer aus Charleroi** (bg_kind=batch)
- `bg_keramik_boden_verbiest_charleroi` → display name: **Fliesen aus Charleroi** (bg_kind=batch)
- `bg_naturstein_wand_verbiest_charleroi` → display name: **Steine aus Charleroi** (bg_kind=batch)
- `bg_stahl_mehrere_55gss_external_core` → display name: **Steel profiles for…** (bg_kind=batch)
- `bg_stahl_mehrere_awm_cable_trays_shelves_lights` → display name: **Cable trays as shelves…** (bg_kind=batch)
- `bg_glas_mehrere_awm_partitions_doors` → display name: **Glass partitions and…** (bg_kind=batch)
- `bg_kunststoff_wand_awm_wc_partitions` → display name: **WC partitions** (bg_kind=batch)
- `bg_holz_ausbau_awm_fixed_builtins` → display name: **Wood for fixed built-ins** (bg_kind=batch)

### Material token distribution (id segment 2)

| token | count |
|---|---:|
| mehrere | 73 |
| holz | 73 |
| stahl | 61 |
| stahlbeton | 20 |
| ziegel | 16 |
| beton | 16 |
| keramik | 13 |
| glas | 11 |
| daemmstoff | 11 |
| metall | 10 |
| naturstein | 10 |
| technik | 5 |
| kunststoff | 5 |
| stein | 5 |
| aluminium | 4 |

## Evidence rules (multi-source naming)

1. **Node identity:** keep `bg_*` id stable; treat `name` as display alias — never merge on string similarity alone.
2. **Catalogue edges (`HAT_BAUTEILTYP`, `NUTZT_MATERIAL`):** require verbatim quote from project page OR marketplace listing linking component type/material.
3. **Cross-source reconciliation:** when dossier name ≠ graph `name`, record both in `notes` + `proof_quote`; prefer `primary_source_url` on **entity** not synthetic Quelle nodes.
4. **Delete gate:** same as W4 — internet research attempted + UNSUPPORTED; bg_ edges never auto-deleted without dedicated mission sign-off.

## Proposed sub-missions (disjoint agents)

| Mission | Scope | ~edges | Notes |
|---|---|---:|---|
| BG-M1 | HAT_BAUTEILTYP + NUTZT_MATERIAL catalogue edges | 855 | Tier-C vocab; multi-source naming; 0 rel evidence_url today |
| BG-M2 | Process axis (HAT_PROZESSPHASE, HAT_BESCHAFFUNGSWEG, HAT_LOGISTIK) | 1372 | Contract-inferred; needs project dossier quotes |
| BG-M3 | Regulation triggers (ERFORDERT_NACHWEIS, TRIGGERS_REGULIERUNGSFRAGE) | 1677 | Structural; evidence on law nodes not rels |
| BG-M4 | Spatial / donor links (AUS_SPENDER, IN_EMPFANGSOBJEKT, HAT_BAUTEILGRUPPE inbound) | 840 | Project geography + donor matching |
| BG-M5 | Material taxonomy (HAT_MATERIALGRUPPE, HAT_RUECKBAUVERFAHREN, HAT_AUFBEREITUNG) | 891 | Naming variants across intake batches |

## Disjoint agent proposals

| Agent | Mission | Read sources |
|---|---|---|
| BG-A1 | BG-M1 catalogue | Project dossiers in `intake/inbox/`, marketplace actor pages from `akteur_typ_projekt_geo.json` |
| BG-A2 | BG-M2 process axis | `contracts/`, project batch JSONL, graph `HAT_PROZESSPHASE` targets |
| BG-A3 | BG-M3 regulation | Regulation graph vocabulary run, law node `source_url` |
| BG-A4 | BG-M4 spatial/donor | `akteur_typ_projekt_geo.json`, `BETEILIGT_AN` / `AUS_SPENDER` graph export |
| BG-A5 | BG-M5 material taxonomy | `controlled_vocabulary.seed.kg.jsonl`, material group nodes |

## W4 exclusion recap

- **416** W3 `delete_rel` ops skipped because `from` or `to` is `bg_*`.
- **852** v5 UNSUPPORTED rel rows retained for this mission.

## References

- `akteur_typ_projekt_geo.json` — _neo4j\review\2026-06-06_project_bg_geo_extract\akteur_typ_projekt_geo.json
- `VERIFICATION_LEDGER_ELEMENT_v5.csv` — bg_ UNSUPPORTED rows
- W4 plan: `VERIFICATION_PLAN_W4_SELECTIVE_DELETE_4_AGENTS.md`
