# Case graph extract: `K118_Kopfbau_Halle_118_Winterthur`

**Scope:** Every `typed_path` in `node_inventory.csv` that contains this substring, plus every row in `clean_confirmed_edges.csv` where **source** or **target** is in that node set.

**Primary Fallbeispiel / Projekt / Bauwerk anchors (inventory):**

- `bauobjekt/K118_Kopfbau_Halle_118_Winterthur`
- `fallstudie/K118_Kopfbau_Halle_118_Winterthur`
- `projekt/K118_Kopfbau_Halle_118_Winterthur`

## Counts

| Metric | Value |
|---:|---:|
| Case-related inventory nodes | 36 |
| CSV edges (at least one endpoint in scope) | 349 |
| CSV edges (both endpoints in scope) | 91 |
| Distinct `relation` in this slice | 38 |

## Edges by `relation`

| Count | relation |
|---:|---|
| 44 | `has_logistik` |
| 33 | `has_rechtliche_bedingung` |
| 31 | `belongs_to_fallstudie` |
| 28 | `belongs_to_projekt` |
| 21 | `has_huerde` |
| 19 | `has_funktionswechsel` |
| 18 | `has_prozessphase` |
| 12 | `measures_kennwertdefinition` |
| 12 | `has_bauteiltyp` |
| 12 | `installed_in_bauobjekt` |
| 12 | `uses_material` |
| 11 | `has_reuse_strategie` |
| 11 | `has_reuse_einsatzstatus` |
| 11 | `has_wirtschaft` |
| 11 | `has_datenqualitaet` |
| 9 | `measured_on_bauobjekt` |
| 9 | `has_bauteilebene` |
| 8 | `has_akteurrolle` |
| 7 | `relates_to_bauobjekt` |
| 4 | `has_bauaufgabe_intervention` |
| 3 | `has_rueckbauverfahren` |
| 2 | `involves_akteur` |
| 2 | `has_pruefung_nachweis` |
| 2 | `part_of_reuse_kette` |
| 2 | `has_fuegung_verbindung` |
| 2 | `has_nutzung` |
| 2 | `has_bauobjektrolle` |
| 1 | `has_bauobjekt` |
| 1 | `has_projekt` |
| 1 | `located_in_ort` |
| 1 | `has_beschaffungsweg` |
| 1 | `has_bauweise` |
| 1 | `has_bausystem` |
| 1 | `has_tragwerksprinzip` |
| 1 | `has_bauobjektklasse` |
| 1 | `has_bauobjektstatus` |
| 1 | `has_ressourcenquelle` |
| 1 | `has_methode` |

## Inventory nodes by `entity`

### `akteur_beteiligung` (7)

- `akteur_beteiligung/K118_Kopfbau_Halle_118_Winterthur__001__Stiftung_Abendrot_Vorsorgestiftung_Abendrot` — Stiftung Abendrot / Vorsorgestiftung Abendrot - K.118 – Kopfbau Halle 118, Winterthur
- `akteur_beteiligung/K118_Kopfbau_Halle_118_Winterthur__002__baub_ro_in_situ` — baubüro in situ - K.118 – Kopfbau Halle 118, Winterthur
- `akteur_beteiligung/K118_Kopfbau_Halle_118_Winterthur__003__Zirkular_GmbH` — Zirkular GmbH - K.118 – Kopfbau Halle 118, Winterthur
- `akteur_beteiligung/K118_Kopfbau_Halle_118_Winterthur__004__ZHAW_IKE` — ZHAW IKE - K.118 – Kopfbau Halle 118, Winterthur
- `akteur_beteiligung/K118_Kopfbau_Halle_118_Winterthur__005__Oberli_Ingenieurbau_AG` — Oberli Ingenieurbau AG - K.118 – Kopfbau Halle 118, Winterthur
- `akteur_beteiligung/K118_Kopfbau_Halle_118_Winterthur__006__Josef_Kolb_AG` — Josef Kolb AG - K.118 – Kopfbau Halle 118, Winterthur
- `akteur_beteiligung/K118_Kopfbau_Halle_118_Winterthur__007__Wetter_AG` — Wetter AG - K.118 – Kopfbau Halle 118, Winterthur

### `bauobjekt` (1)

- `bauobjekt/K118_Kopfbau_Halle_118_Winterthur` — K.118 – Kopfbau Halle 118, Winterthur

### `datenpunkt` (9)

- `datenpunkt/K118_Kopfbau_Halle_118_Winterthur__001__Fl_che` — Fläche - K.118 – Kopfbau Halle 118, Winterthur
- `datenpunkt/K118_Kopfbau_Halle_118_Winterthur__002__Geschosse_Aufstockung` — Geschosse Aufstockung - K.118 – Kopfbau Halle 118, Winterthur
- `datenpunkt/K118_Kopfbau_Halle_118_Winterthur__003__Wiederverwendungsrate_Gewicht` — Wiederverwendungsrate Gewicht - K.118 – Kopfbau Halle 118, Winterthur
- `datenpunkt/K118_Kopfbau_Halle_118_Winterthur__004__Wiederverwendungsrate_Volumen` — Wiederverwendungsrate Volumen - K.118 – Kopfbau Halle 118, Winterthur
- `datenpunkt/K118_Kopfbau_Halle_118_Winterthur__005__CO_Reduktion` — CO₂-Reduktion - K.118 – Kopfbau Halle 118, Winterthur
- `datenpunkt/K118_Kopfbau_Halle_118_Winterthur__006__CO_Reduktion_absolut` — CO₂-Reduktion absolut - K.118 – Kopfbau Halle 118, Winterthur
- `datenpunkt/K118_Kopfbau_Halle_118_Winterthur__007__Prim_rmaterial_eingespart` — Primärmaterial eingespart - K.118 – Kopfbau Halle 118, Winterthur
- `datenpunkt/K118_Kopfbau_Halle_118_Winterthur__008__CO_Beitrag_Stahlreuse` — CO₂-Beitrag Stahlreuse - K.118 – Kopfbau Halle 118, Winterthur
- `datenpunkt/K118_Kopfbau_Halle_118_Winterthur__009__Kostenwirkung` — Kostenwirkung - K.118 – Kopfbau Halle 118, Winterthur

### `fallstudie` (1)

- `fallstudie/K118_Kopfbau_Halle_118_Winterthur` — K.118 – Kopfbau Halle 118, Winterthur

### `projekt` (1)

- `projekt/K118_Kopfbau_Halle_118_Winterthur` — K.118 – Kopfbau Halle 118, Winterthur

### `quelle` (2)

- `quelle/Geb_ude_K118_Kopfbau_Halle_118_Winterthur_md` — Geb_ude_K118_Kopfbau_Halle_118_Winterthur_md
- `quelle/gebaeude_K118_Kopfbau_Halle_118_Winterthur_md` — gebaeude_K118_Kopfbau_Halle_118_Winterthur_md

### `reuse_einsatz` (12)

- `reuse_einsatz/K118_Kopfbau_Halle_118_Winterthur__001__Stahltr_ger_St_tzen` — Stahlträger / Stützen - K.118 – Kopfbau Halle 118, Winterthur
- `reuse_einsatz/K118_Kopfbau_Halle_118_Winterthur__002__Profilbleche_Verbunddecken` — Profilbleche Verbunddecken - K.118 – Kopfbau Halle 118, Winterthur
- `reuse_einsatz/K118_Kopfbau_Halle_118_Winterthur__003__Externe_Treppe` — Externe Treppe - K.118 – Kopfbau Halle 118, Winterthur
- `reuse_einsatz/K118_Kopfbau_Halle_118_Winterthur__004__Fenster` — Fenster - K.118 – Kopfbau Halle 118, Winterthur
- `reuse_einsatz/K118_Kopfbau_Halle_118_Winterthur__005__Fassadenbleche_Profilbleche` — Fassadenbleche / Profilbleche - K.118 – Kopfbau Halle 118, Winterthur
- `reuse_einsatz/K118_Kopfbau_Halle_118_Winterthur__006__EPS_D_mmung` — EPS-Dämmung - K.118 – Kopfbau Halle 118, Winterthur
- `reuse_einsatz/K118_Kopfbau_Halle_118_Winterthur__007__Holzdachelemente` — Holzdachelemente - K.118 – Kopfbau Halle 118, Winterthur
- `reuse_einsatz/K118_Kopfbau_Halle_118_Winterthur__008__T_ren` — Türen - K.118 – Kopfbau Halle 118, Winterthur
- `reuse_einsatz/K118_Kopfbau_Halle_118_Winterthur__009__Dreischichtplatten_Holzplatten` — Dreischichtplatten / Holzplatten - K.118 – Kopfbau Halle 118, Winterthur
- `reuse_einsatz/K118_Kopfbau_Halle_118_Winterthur__010__Naturstein_Granitplatten` — Naturstein-/Granitplatten - K.118 – Kopfbau Halle 118, Winterthur
- `reuse_einsatz/K118_Kopfbau_Halle_118_Winterthur__011__Klinker_Backstein` — Klinker / Backstein - K.118 – Kopfbau Halle 118, Winterthur
- `reuse_einsatz/K118_Kopfbau_Halle_118_Winterthur__012__Sanit_r_TGA` — Sanitär / TGA - K.118 – Kopfbau Halle 118, Winterthur

### `reuse_kette` (1)

- `reuse_kette/K118_Kopfbau_Halle_118_Winterthur` — Reuse-Kette - K.118 – Kopfbau Halle 118, Winterthur

### `reuse_kettenstation` (2)

- `reuse_kettenstation/K118_Kopfbau_Halle_118_Winterthur__Donor` — Donor - K.118 – Kopfbau Halle 118, Winterthur
- `reuse_kettenstation/K118_Kopfbau_Halle_118_Winterthur__Receiver` — Receiver - K.118 – Kopfbau Halle 118, Winterthur

## Machine-readable edge list

TSV (349 rows, same columns as `clean_confirmed_edges.csv`): [`case_K118_Kopfbau_Halle_118_Winterthur_edges.tsv`](case_K118_Kopfbau_Halle_118_Winterthur_edges.tsv)

## Neo4j note

After import, predicates are **folded** (e.g. `belongs_to_fallstudie` → `GEHÖRT_ZU`, `has_logistik` → `HAT` with `art=logistik`, `uses_material` → `BENUTZT`). Use this CSV slice for **predicate-level** comparison to another document; use Browser for **folded** shape.
