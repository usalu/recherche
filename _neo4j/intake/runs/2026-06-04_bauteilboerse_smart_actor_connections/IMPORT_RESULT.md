# Import result

**Run:** `bauteilboerse_smart_actor_connections_2026_06_04`  
**Executed:** 2026-06-04  
**Database:** `mit-bestand`

## Outcome

Imported four evidence-backed smart actor connections:

| Bauteilboerse | Relationship | Actor | Evidence |
|---|---|---|---|
| `baumab_kassel` | `VERBUNDEN_MIT_AKTEUR` | `stadt_kassel` | `https://baumab-kassel.de/konzept/` |
| `baumab_kassel` | `VERBUNDEN_MIT_AKTEUR` | `surap_gmbh` | `https://baumab-kassel.de/` |
| `zirkulie_bauteilboerse_triesen` | `BETRIEBEN_VON` | `stiftung_lebenswertes_liechtenstein` | `https://www.zirkulie.net/impressum` |
| `zirkulie_bauteilboerse_triesen` | `VERBUNDEN_MIT_AKTEUR` | `re_win` | `https://www.zirkulie.net/zentrum-fuer-zirkulaeres-bauen/bauteile-spenden` |

Importer result:

- relationships touched with this `review_run`: 21
- relevant outgoing relationships missing `r.id`: 0

## New actor readback

### `stadt_kassel`

- `HAT_AKTEURTYP`: `at_oeffentliche_institution`
- `HAT_AKTEURROLLE`: `ar_reuse_zirkularitaetsberatung`, `ar_oeffentliche_hand_foerderung`
- `LIEGT_IN_LAND`: `land_deutschland`
- `BELEGT_IN`: `https://baumab-kassel.de/impressum/`

### `surap_gmbh`

- `HAT_AKTEURTYP`: `at_unternehmen`, `at_software_tool_anbieter`
- `HAT_AKTEURROLLE`: `ar_software_digitalisierung`, `ar_nachhaltigkeitsberatung`
- `LIEGT_IN_LAND`: `land_deutschland`
- `BELEGT_IN`: `https://www.surap.de/`

### `stiftung_lebenswertes_liechtenstein`

- `HAT_AKTEURTYP`: `at_organisation`, `at_ngo_verband_netzwerk`
- `HAT_AKTEURROLLE`: `ar_reuse_zirkularitaetsberatung`, `ar_bildung_wissenstransfer`
- `LIEGT_IN_LAND`: `land_liechtenstein`
- `BELEGT_IN`: `https://www.zirkulie.net/impressum`

## Post-import gap survey

`python _scripts/_gap_survey.py` after import:

- total nodes: 5445
- total relationships: 21397
- distinct labels: 66
- distinct relationship types: 85

The pre-existing mandatory failures remain present. This run did not add unclassified actors and did not add outgoing relationships without `r.id`.
