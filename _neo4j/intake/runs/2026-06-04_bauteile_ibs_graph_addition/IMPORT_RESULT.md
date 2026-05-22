# Import result

**Run:** `bauteile_ibs_graph_addition_2026_06_04`  
**Executed:** 2026-06-04  
**Database:** `mit-bestand`

## Outcome

Imported one new `:Akteur` anchor:

- `bauteilkatalog_immobilien_basel_stadt` — Bauteilkatalog Immobilien Basel-Stadt

Importer result:

- relationships touched with this `review_run`: 40
- anchor outgoing relationships missing `r.id`: 0
- schema check: `OK`

Schema check counts:

| Check | Count |
|---|---:|
| `HAT_AKTEURTYP` | 1 |
| `LIEGT_IN_LAND` | 1 |
| `HAT_MARKTMODELL` | 1 |
| `HAT_GESCHAEFTSMODELL` | 1 |
| `HAT_AKTEURROLLE` | 7 |
| `BELEGT_IN` | 5 |
| `NUTZT_MATERIAL` | 5 |
| `HAT_BAUTEILTYP` | 9 |

## Readback

Classification:

- `HAT_AKTEURTYP`: `at_materialhub_bauteilboerse`
- `LIEGT_IN_LAND`: `land_schweiz`
- `HAT_MARKTMODELL`: `mm_kauf_gebraucht`
- `HAT_GESCHAEFTSMODELL`: `gm_dienstleistung_urban_mining`
- `HAT_AKTEURROLLE`: `ar_materialbroker`, `ar_aufbereitung_refurbishment`, `ar_forschung_dokumentation`, `ar_rueckbau_bauteilernte_logistik`, `ar_materiallieferung_markt`, `ar_reuse_zirkularitaetsberatung`, `ar_software_digitalisierung`
- `HAT_METHODE`: `meth_urban_mining_und_scouting`, `meth_bestands_und_reuse_assessment`, `meth_zirkulaere_beschaffung`, `meth_dokumentation_und_monitoring`

Evidence URLs:

- `https://bauteile-ibs.ch/`
- `https://bauteile-ibs.ch/components`
- `https://bauteile-ibs.ch/componentsmine`
- `https://bauteile-ibs.ch/contact`
- `https://bauteile-ibs.ch/info`

Strict material edges:

- `mat_aluminium`
- `mat_daemmstoff`
- `mat_glas`
- `mat_holz`
- `mat_stahl`

Strict component-type edges:

- `bt_daemmung`
- `bt_decke`
- `bt_fassade`
- `bt_fenster`
- `bt_gelaender`
- `bt_stuetze`
- `bt_technik`
- `bt_traeger`
- `bt_treppe`

Contextual edges:

- `BETEILIGT_AN`: `p_elementa_walkeweg`
- `BETRIEBEN_VON`: `immobilien_basel_stadt`
- `NUTZT_SOFTWARE`: `tool_bauteilkatalog`
- `VERBUNDEN_MIT_AKTEUR`: `digvis_gmbh`, `zirkular`, `bauteilboerse_basel_overall`

## Post-import gap survey

`python _scripts/_gap_survey.py` after import:

- total nodes: 5425
- total relationships: 21318
- distinct labels: 66
- distinct relationship types: 85

The pre-existing mandatory failures remain present. The IBS import did not add new `r.id NULL` relationships and the new anchor passes the Bauteilboerse schema check.
