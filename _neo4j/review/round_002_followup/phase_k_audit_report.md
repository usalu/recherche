# Phase K — Graph orphan + structural audit

**Snapshot:** 2296 nodes / 16822 relationships.

## 1. Orphan rate per label

Labels with at least one orphan, sorted by orphan-share.

| Label | Total | Orphan | Orphan % |
|---|---:|---:|---:|
| Layer | 6 | 2 | 33.3% |
| Wirtschaft | 12 | 4 | 33.3% |
| Programm | 17 | 5 | 29.4% |
| Akteurrolle | 25 | 7 | 28.0% |
| Leistungsanforderung | 12 | 3 | 25.0% |
| RechtlicheBedingung | 9 | 2 | 22.2% |
| Bauproduktstatus | 15 | 3 | 20.0% |
| Marktmodell | 11 | 2 | 18.2% |
| BauwerkEra | 6 | 1 | 16.7% |
| Funktionswechsel | 6 | 1 | 16.7% |
| ZustandsKlasse | 6 | 1 | 16.7% |
| PruefungNachweis | 20 | 3 | 15.0% |
| ZertifizierungBewertungssystem | 7 | 1 | 14.3% |
| Bausystem | 9 | 1 | 11.1% |
| Beschaffungsweg | 10 | 1 | 10.0% |
| HuerdeKategorie | 10 | 1 | 10.0% |
| Verbindungstechnik | 12 | 1 | 8.3% |
| Methode | 13 | 1 | 7.7% |
| Aufbereitungsverfahren | 45 | 2 | 4.4% |
| Norm | 30 | 1 | 3.3% |
| Akteur | 582 | 6 | 1.0% |

## 2. Relationship-type usage

Rare rel types (≤ 3 instances) — candidates for review or removal.

| Rel type | Count |
|---|---:|
| HAT_SCHADSTOFF | 1 |
| ERHALT_FOERDERUNG_DURCH | 2 |

_Total rel types in use: 67._

## 3. Bauteilgruppe coverage of reuse-quality dimensions

Of 306 Bauteilgruppen, how many carry each kind of edge after all phases?

| Dimension | Rel type | BGs with edge |
|---|---|---:|
| Material | NUTZT_MATERIAL | 301/306 (98%) |
| Aufbereitung | HAT_AUFBEREITUNG | 225/306 (74%) |
| Prüfung | HAT_PRUEFUNG | 194/306 (63%) |
| Verbindungstechnik | HAT_VERBINDUNGSTECHNIK | 80/306 (26%) |
| Marktmodell | HAT_MARKTMODELL | 237/306 (77%) |
| Defekt | HAT_DEFEKT | 31/306 (10%) |
| Bauproduktstatus | HAT_BAUPRODUKTSTATUS | 37/306 (12%) |
| Norm | REFERENZIERT_NORM | 15/306 (5%) |
| Rückbauverfahren | HAT_RUECKBAUVERFAHREN | 179/306 (58%) |
| Logistik | HAT_LOGISTIK | 178/306 (58%) |

## 4. Projekt coverage of project-level dimensions

Of 76 non-stub Projekt nodes:

| Dimension | Rel type | Projekte with edge |
|---|---|---:|
| Land | LIEGT_IN_LAND | 64/76 (84%) |
| Bauwerk | NUTZT_BAUWERK | 75/76 (99%) |
| Bauteilgruppe | HAT_BAUTEILGRUPPE | 75/76 (99%) |
| Defekt-Befund | HAT_DEFEKT_BEFUND | 20/76 (26%) |
| Matching | HAT_MATCHINGQUALITAET | 75/76 (99%) |
| Marktmodell | HAT_DOMINANT_MARKTMODELL | 54/76 (71%) |
| Akzeptanz | HAT_DOMINANT_AKZEPTANZ | 8/76 (11%) |
| Wirtschaft | HAT_WIRTSCHAFT | 19/76 (25%) |
| LCA-Modul | BERECHNET_NACH_MODUL | 6/76 (8%) |
| Norm | REFERENZIERT_NORM | 3/76 (4%) |

## 5. P-6 Methode split candidates

Currently **13 Methode nodes** — too heterogenous to be one label.

Top 30 most-used Methoden by BG-degree (these are candidates for sub-labels):

| ID | BG degree | Name |
|---|---:|---|
| `meth_form_follows_availability` | 93 | Form_Follows_Availability |
| `meth_reuse_assessment` | 73 | ReUse_Assessment |
| `meth_bauteilkatalogisierung` | 39 | Bauteilkatalogisierung |
| `meth_building_material_scouting` | 39 | Building_Material_Scouting |
| `meth_design_for_disassembly` | 23 | Design_for_Disassembly |
| `meth_reversibilitaet` | 22 | Reversibilitaet |
| `meth_materialinventur` | 20 | Materialinventur |
| `meth_reuse_ausschreibung` | 15 | ReUse_Ausschreibung |
| `meth_pre_deconstruction_audit` | 8 | Pre_Deconstruction_Audit |
| `meth_urban_mining` | 6 | Urban_Mining |
| `meth_wiederverwendungskriterien` | 1 | Wiederverwendungskriterien |
| `meth_abrissmonitoring` | 0 | Abrissmonitoring |
| `meth_zirkulaere_ausschreibung` | 0 | Zirkulaere_Ausschreibung |

## 6. P-11 Huerde category audit

- 28 Huerde nodes.
- 10 HuerdeKategorie nodes.
