# Import result

**Run:** `more_bauteilboersen_graph_addition_2026_06_04`  
**Executed:** 2026-06-04  
**Database:** `mit-bestand`

## Outcome

Imported two new `:Akteur` anchors:

- `baumab_kassel` — BauMaB Kassel / Bauteilbörse Kassel
- `zirkulie_bauteilboerse_triesen` — ZirkuLIE Bauteilbörse Triesen

Also added one new country node:

- `land_liechtenstein` — Liechtenstein

Importer result:

- relationships touched with this `review_run`: 58
- new anchors outgoing relationships missing `r.id`: 0
- schema check: `OK` for both anchors

## Schema check counts

| Anchor | Type | Land | Market model | Business models | Roles | Evidence URLs | Materials | Bauteiltypen | Check |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `baumab_kassel` | 1 | 1 | 1 | 3 | 7 | 5 | 3 | 4 | OK |
| `zirkulie_bauteilboerse_triesen` | 1 | 1 | 1 | 1 | 5 | 5 | 5 | 8 | OK |

## Readback

### BauMaB Kassel

Classification:

- `HAT_AKTEURTYP`: `at_materialhub_bauteilboerse`
- `LIEGT_IN_LAND`: `land_deutschland`
- `HAT_MARKTMODELL`: `mm_kauf_gebraucht`
- `HAT_GESCHAEFTSMODELL`: `gm_shop_eigenstock`, `gm_marketplace_vermittlung`, `gm_dienstleistung_urban_mining`
- `HAT_AKTEURROLLE`: `ar_materialbroker`, `ar_aufbereitung_refurbishment`, `ar_rueckbau_bauteilernte_logistik`, `ar_materiallieferung_markt`, `ar_reuse_zirkularitaetsberatung`, `ar_bildung_wissenstransfer`, `ar_software_digitalisierung`
- `HAT_METHODE`: `meth_urban_mining_und_scouting`, `meth_bestands_und_reuse_assessment`, `meth_zirkulaere_beschaffung`, `meth_dokumentation_und_monitoring`

Evidence URLs:

- `https://baumab-kassel.de/`
- `https://baumab-kassel.de/bauteilboerse/`
- `https://baumab-kassel.de/impressum/`
- `https://baumab-kassel.de/kaufen/`
- `https://baumab-kassel.de/verkaufen/`

Strict material edges:

- `mat_beton`
- `mat_glas`
- `mat_holz`

Strict component-type edges:

- `bt_dach`
- `bt_fenster`
- `bt_technik`
- `bt_tuer`

### ZirkuLIE Bauteilbörse Triesen

Classification:

- `HAT_AKTEURTYP`: `at_materialhub_bauteilboerse`
- `LIEGT_IN_LAND`: `land_liechtenstein`
- `HAT_MARKTMODELL`: `mm_kauf_gebraucht`
- `HAT_GESCHAEFTSMODELL`: `gm_shop_eigenstock`
- `HAT_AKTEURROLLE`: `ar_materialbroker`, `ar_materiallieferung_markt`, `ar_reuse_zirkularitaetsberatung`, `ar_bildung_wissenstransfer`, `ar_software_digitalisierung`
- `HAT_METHODE`: `meth_urban_mining_und_scouting`, `meth_zirkulaere_beschaffung`

Evidence URLs:

- `https://shop.zirkulie.net/`
- `https://shop.zirkulie.net/produkt-kategorie/gebaeudehuelle-2/fenster-gebaeudehuelle-2/`
- `https://shop.zirkulie.net/produkt-kategorie/innenausbau-2/tuere-innenausbau-2/`
- `https://www.zirkulie.net/impressum`
- `https://www.zirkulie.net/zentrum-fuer-zirkulaeres-bauen`

Strict material edges:

- `mat_aluminium`
- `mat_daemmstoff`
- `mat_glas`
- `mat_holz`
- `mat_kunststoff`

Strict component-type edges:

- `bt_boden`
- `bt_dach`
- `bt_daemmung`
- `bt_fassade`
- `bt_fenster`
- `bt_technik`
- `bt_treppe`
- `bt_tuer`

## Post-import gap survey

`python _scripts/_gap_survey.py` after import:

- total nodes: 5441
- total relationships: 21376
- distinct labels: 66
- distinct relationship types: 85

The pre-existing mandatory failures remain present. The new actors pass their Bauteilboerse schema checks and introduce no outgoing relationships without `r.id`.
