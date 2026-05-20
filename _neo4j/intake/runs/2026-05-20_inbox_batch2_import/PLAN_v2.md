# PLAN_v2 — Batch 2 inbox import (revised)

**Date:** 2026-05-20
**Supersedes:** [PLAN.md](PLAN.md) (the original 2026-05-20 plan)
**Driver doc:** [CORRECTIONS_2026-05-20.md](CORRECTIONS_2026-05-20.md) — every change vs PLAN.md traces to a numbered entry there.
**Reference:** [actor_extraction_per_dossier.md](actor_extraction_per_dossier.md) — per-dossier actor/BG/Bauwerk/Quelle inventory.
**Validation script:** [pre_flight_validation.cypher](pre_flight_validation.cypher) — must be run before patch generation.

---

## TL;DR

Same goal as PLAN.md (import all 21 inbox dossiers, maximize connectivity within current graph), but PLAN_v2 fixes:

1. **All schema bugs from CORRECTIONS A.C1-C15** — `HAT_SOFTWARE`/`HAT_TOOL`/`VERBUNDEN_MIT`/`LIEFERT_MATERIAL_AUS`/`LIEGT_IN`/`HAT_AUFBEREITUNGSVERFAHREN`/`HAT_PRUEFUNG_NACHWEIS` are replaced; `wk_*` becomes `k_*`; `n_*` becomes `norm_*`; invented `Plattform` label dropped; invented `av_*` ids replaced.
2. **All structural omissions O1-O14** — every BG gets HAT_BAUTEILEBENE + HAT_STATUS + HAT_RESSOURCENQUELLE + (where applicable) NUTZT_MATERIAL + HAT_MATCHINGQUALITAET; every Akteur gets HAT_AKTEURROLLE + HAT_AKTEURTYP + (Persons) GEHÖRT_ZU; every Bauwerk gets HAT_BAUOBJEKTROLLE + HAT_BAUOBJEKTKLASSE; project-level Phase 8 vocab restored.
3. **All factual corrections F1-F27** — UMAR + ELEMENTA brought in scope from batch 1.md; Plan 1 receiving Bauwerks restored; all dossier-listed actors transcribed; typed Programm properties set; RE_USE Höfe location corrected; unverified Programm names kept as Projekt.
4. **Connectivity wins** — ~400 additional edges to central vocab hubs vs PLAN.md.

Current graph state: 2298 nodes / 17035 rels post-Phase R (2026-05-19). PLAN_v2 projects ~2520 nodes / ~18300 rels after apply.

---

## Phase ordering

```
0 — Pre-flight validation (run pre_flight_validation.cypher; resolve all S2-S40 mismatches)
1 — PARKED_DECISIONS cleanup (deletes, akteur merges, Circl merge, Projekt relabels)
2 — Shared supporting nodes (Bauwerks, Programme, Software, Tool, Norm, Stadt, Land)
3 — Quellen (one case_markdown per dossier + ~30 external_reference for high-value URLs)
4 — Promote stub Projekte (full_projekt + ALIASES UNION + actors)
5 — New Akteure (Persons + Organisations with HAT_AKTEURROLLE + HAT_AKTEURTYP + GEHÖRT_ZU)
6 — Bauteilgruppen (with full vocab + EINGEBAUT_IN → Bauwerk; NOT Projekt)
7 — Wiederverwendungsketten (k_* prefix; TEIL_VON_KETTE edges from BGs)
8 — Project-level vocab (Plan 1 Phase 8 restored + extended to all 23 projects)
9 — Bridge edges (cross-project connectivity catalysts)
10 — Verification + rollback ledger
```

Phases 0-3 run sequentially. Phases 4-5 must run before 6. Phase 7 needs Phase 6. Phase 8 needs Phase 4 + 5. Phase 9 needs all earlier. Phase 10 is post-apply.

---

## Phase 0 — Pre-flight validation

**Inputs:** [pre_flight_validation.cypher](pre_flight_validation.cypher) (40 sections).

**Procedure:**

```bash
# 1. Take fresh backup
python _scripts/backup_neo4j_graph.py --out-dir _neo4j/review/backups/batch2_v2_pre_apply

# 2. Run validation
python _scripts/run_cypher.py --file _neo4j/intake/runs/2026-05-20_inbox_batch2_import/pre_flight_validation.cypher \
                              --out _neo4j/intake/runs/2026-05-20_inbox_batch2_import/pre_flight_results.json

# 3. Resolve every "EXPECTED but got X" against CORRECTIONS_2026-05-20.md
# 4. Update CORRECTIONS_2026-05-20.md §A.X with live status
# 5. Update the per-phase patch generator scripts with the actual live ids
```

**Block-on:** Any S2/S3 mismatch (fabricated rel type), any S6/S7/S10/S15-S19 vocab id absence, any S26 missing Projekt id.

---

## Phase 1 — PARKED_DECISIONS cleanup

Patch directory: `_neo4j/review/round_002_followup/patches/batch2/`.

### 1a — Delete with snapshot logging

**Pre-delete Cypher (run + paste into rollback.md):**
```cypher
MATCH (n {id:'p_obk_27'})-[r]-(m)
RETURN type(r), m.id, m.name, properties(r);
// also for bizh and dare_gmbh:
MATCH (n {id:'bizh'})-[r]-(m) RETURN type(r), m.id, m.name, properties(r);
MATCH (n {id:'dare_gmbh'})-[r]-(m) RETURN type(r), m.id, m.name, properties(r);
```

Patch `phase_batch2_v2_1a_deletes.patch.jsonl`:
- `delete_node`: `p_obk_27` (OBK 27 confirmed negative-finding per dossier + PARKED_DECISIONS)
- `delete_node`: `bizh` (degree 0)
- `delete_node`: `dare_gmbh` (degree 1)

**Verify:** S26 returns 0 for these 3 ids.

### 1b — Akteur merges + Werner Sobek cleanup

Patch `phase_batch2_v2_1b_akteur_merges.patch.jsonl`:
- `merge_node`: `rotor_vzw → rotor_asbl_vzw` (per STUB_AKTEUR_DECISIONS)
- `merge_node`: `zirkular_cirkla → zirkular_gmbh`
- `delete_rel`: `Werner_Sobek -[ASSOZIIERT_MIT_PROJEKT]-> p_umar_unit` (keep `werner_sobek_p` canonical; per Plan 1 P0-A)
- Optional `merge_node`: `Werner_Sobek → werner_sobek_p` if no other unique data on the duplicate.

**Verify:** S29 returns rotor_asbl_vzw with higher degree, rotor_vzw absent.

### 1c — Circl merge (direction: pavilion → abn_amro per PARKED_DECISIONS)

**Pre-merge snapshot:**
```cypher
MATCH (p:Projekt) WHERE p.id IN ['p_pavilion_circl_amsterdam','p_circl_abn_amro']
OPTIONAL MATCH (p)-[r]-(m)
RETURN p.id, type(r), m.id, m.name, properties(r);
```

Patch `phase_batch2_v2_1c_circl_merge.patch.jsonl`:
- `set_node_properties` on `p_circl_abn_amro`: pre-set the union-target properties so merge_node's last-write-wins doesn't lose the pavilion's facts.
- `merge_node`: `p_pavilion_circl_amsterdam → p_circl_abn_amro`. Apply tool unions labels, merges properties, rewrites all r.id.

Properties to UNION-set on `p_circl_abn_amro` first (taken from pavilion node + dossier):
```
name: "Circl"
name_full: "Circl — ABN AMRO Circular Pavilion Amsterdam"
aliases: union(existing aliases on either, plus ["Circl pavilion","Circulair paviljoen Circl","Pavilion Circl Amsterdam"])
bgf_m2: 2000
fertigstellung_jahr: 2017
bau_jahr_von: 2016
year_opened_date: "2017-09-05"
date_dismantled: "2025-03"
bauwerkstatus: "rueckgebaut"
adresse: "Gustav Mahlerplein, Amsterdam Zuidas"
node_role: "full_projekt"
```

**Verify:** S26 shows only `p_circl_abn_amro` with degree ≥ 9 + the merged property set.

### 1d — Projekt → Programm relabels (verified programmes only)

For each pair below, emit `add_node` (new Programm with typed properties) then `merge_node` (old Projekt id → new Programm id).

**Important:** Only programmes with `identified_programme: yes` in the dossier. Per CORRECTIONS C14, the 4 unverified ones STAY as Projekt.

| old `p_*` id | new `prog_*` id | name (≤25) | name_full | typed properties |
|---|---|---|---|---|
| `p_fcrbe` | `prog_fcrbe` | `FCRBE` | Facilitating the Circulation of Reclaimed Building Elements | type="Interreg", start_year=2018, end_year=2023, status="concluded", eu_funding_programme="Interreg North-West Europe", lead_organisation="Rotor" |
| `p_interreg_nwe_fcrbe` | → MERGE into `prog_fcrbe` | — | — | — |
| `p_rebridge_structural_reuse_project` | `prog_rebridge` | `ReBridge` | ReBridge — Reuse of Steel Components from Existing Bridge Structures | type="other", start_year=2025, end_year=2028, status="active", eu_funding_programme="RFCS", grant_agreement_reference="101157419", eu_contribution_eur=1695121.69, lead_organisation="University of Stuttgart" |
| `p_re_use_hoefe` | `prog_re_use_hoefe` | `RE-USE Höfe` | RE-USE Höfe — zirkuläre Lieferketten anhand der Fensterwiederverwendung | aliases=["RE_USE Höfe Wien","REUSE Yards"], status="published" |
| `p_stuttgart_210` | `prog_stuttgart_210` | `Stuttgart 210` | Stuttgart 210 — weiterdenken, weiterbauen! | type="teaching+research", host_institution="HTWG Konstanz", status="active" |

**STAY as Projekt** (CORRECTIONS C14):
- `p_architecture_of_reuse_brussels` — Rotor-led work; tag actors but don't promote.
- `p_eth_circular_construction_student_reuse` — MERGE into `prog_mas_dfab` (verified programme; see Phase 2).
- `p_reuse_in_construction_zhaw` — KEEP Projekt.
- `p_vandkunsten_component_reuse` — KEEP Projekt.
- `p_reuse_logistics` — KEEP Projekt as child of new `prog_urban_bricolage`.
- `p_refair_bordeaux_reemploi_platform` — Akteur/Software/Bauwerk shape (see Phase 2/5); old Projekt to be deleted post-rel-migration.
- `p_rcmi_concular` — Akteur/Tool shape; old Projekt to be deleted post-rel-migration.

### 1e — Aliases UNION precondition

Patch generator MUST read live aliases for these 7 nodes (per `NAMING_AND_PROPERTIES_PLAN.md:61`) and UNION when running canonicalize_node:
- `imd_raadgevende_ingenieurs`, `cleveland_steel_tubes`, `rotor_dc`, `duncan_baker_brown`, `land_daenemark`, `p_lysp8_basel`, `p_eth_circular_construction_student_reuse`.

**Verify:** S35/S36 show the UNION result, not a destructive overwrite.

---

## Phase 2 — Shared supporting nodes

Patch `phase_batch2_v2_2_shared_nodes.patch.jsonl`. Every node carries `BELEGT_IN → relevant Quelle` at creation.

### Bauwerks (11 — see CORRECTIONS C8/C9)

#### Receiving buildings (7)
| id | name | role | class | status | stadt | properties |
|---|---|---|---|---|---|---|
| `bw_schaerenmoosstrasse_zuerich` | Schärenmoosstr. ZH | bor_same_site_donor_receiver | bok_gebaeude | status_geplant | stadt_zuerich | adresse="Schärenmoosstrasse 115/117, Zürich" |
| `bw_umar_unit_duebendorf` | UMAR Unit Dübendorf | bor_referenzobjekt | bok_gebaeudeteil | status_realisiert | stadt_duebendorf (NEW) | adresse="Überlandstrasse 129, 8600 Dübendorf"; bau_jahr_von=2017; fertigstellung_jahr=2018 |
| `bw_elementa_walkeweg_basel` | ELEMENTA Walkeweg | bor_empfaengerobjekt | bok_gebaeude | status_geplant | stadt_basel | adresse="Emilie Louise Frey-Strasse, 4053 Basel"; bgf_m2=20000; number_of_units=150 |
| `bw_circl_pavilion_amsterdam` | Circl Pavilion AMS | bor_donorobjekt (post-dismantling) | bok_pavillon | status_rueckgebaut | stadt_amsterdam (NEW) | adresse="Gustav Mahlerplein, Amsterdam"; bgf_m2=2000; bau_jahr_von=2016; fertigstellung_jahr=2017; date_dismantled="2025-03" |
| `bw_lysp8_basel` | LysP8 Basel | bor_empfaengerobjekt | bok_gebaeude | status_realisiert | stadt_basel | adresse="Weinlagerstrasse 33, 4056 Basel"; bgf_m2=2250; site_area_m2=686; volume_m3=7170; number_of_units=27; geschosse_anzahl_min=6; geschosse_anzahl_max=10 |
| `bw_meduni_campus_mariannengasse` | MedUni Campus Wien | bor_donorobjekt | bok_gebaeude | status_rueckgebaut | stadt_wien | adresse="Mariannengasse, Vienna"; reuse_masse_kg=60400 |
| `bw_jugendtreff_ingersheim` | Jugendtreff Ingersheim | bor_empfaengerobjekt | bok_pavillon | status_realisiert | stadt_ingersheim (NEW) | adresse="Baumwasenweg, 74379 Ingersheim"; bgf_m2=50; fertigstellung_jahr=2024 |

#### Donor buildings (3)
| id | name | role | class | status | stadt |
|---|---|---|---|---|---|
| `bw_ubs_altstetten` | UBS Datenzentrum Altstetten | bor_donorobjekt | bok_gebaeude | status_rueckgebaut | stadt_zuerich |
| `bw_generale_de_banque_brussels` | Générale de Banque BXL | bor_donorobjekt | bok_gebaeude | status_rueckgebaut | stadt_bruessel |
| `bw_lysbueechel_garage_basel` | Lysbüchel Parkgarage | bor_donorobjekt | bok_gebaeude | status_rueckgebaut | stadt_basel |

#### Other Bauwerk
| id | name | role | class | status | stadt |
|---|---|---|---|---|---|
| `bw_base_du_reemploi_merignac` | Base du Réemploi Mérignac | bor_zwischenlager | bok_reuse_centre | status_realisiert | stadt_merignac (NEW) |
| `bw_stuttgart21_hauptbahnhof` | Stuttgart 21 Hauptbahnhof | bor_donorobjekt | bok_infrastruktur | status_realisiert | stadt_stuttgart |
| `bw_granby_workshop_liverpool` (OPTIONAL) | Granby Workshop | bor_referenzobjekt | bok_innenausbau | status_realisiert | stadt_liverpool (NEW) |

Each gets: `HAT_BAUOBJEKTROLLE`, `HAT_BAUOBJEKTKLASSE`, `HAT_STATUS`, `LIEGT_IN_STADT`, `LIEGT_IN_LAND`, `BELEGT_IN`.

### Programme (8 new + 1 enriched existing)
| id | name | name_full | source dossier |
|---|---|---|---|
| `prog_nest_empa` | NEST Empa Dübendorf | NEST — Empa Dübendorf living-lab platform | batch1 UMAR |
| `prog_stiftung_pwg` | Stiftung PWG Wettbewerb | Stiftung PWG architecture competition | batch1 SMS |
| `prog_be_circular` | Be.Circular | Be.Circular Brussels — circular-economy initiative grant | Careno |
| `prog_prec` | PREC | Programme Régional pour l'Économie Circulaire (Brussels-Capital Region; parent of Be.Circular) | Careno |
| `prog_abn_amro_mission_2030` | ABN AMRO Mission 2030 | ABN AMRO Mission 2030 circular-economy programme | Circl |
| `prog_mas_dfab` | MAS DFAB ETH | MAS Architektur und Digitale Fabrikation ETH Zürich | ETH |
| `prog_holzbau_offensive_bw` | Holzbau-Offensive BW | Holzbau-Offensive Baden-Württemberg | Stuttgart 210 |
| `prog_urban_bricolage` | Urban Bricolage | Urban Bricolage — SNSF-PRIMA project (University of Fribourg, 2022-2026) | Reuse Logistics |

### Tools (2 new)
| id | name | name_full |
|---|---|---|
| `tool_retile` | Re-Tile | Re-Tile — Ceramic Tile Cleaning Machine (Rotor DC + Be.Circular, 2022) |
| `tool_rcmi` | RCMI | Reclaimed Construction Material Insurance (Concular + VHV) |

### Software (3-4 new — verify S23)
| id | name | name_full |
|---|---|---|
| `software_llmnt` | LLMNT | LLMNT material passport platform (Circl digital twin) |
| `software_ecotool` | EcoTool | EcoTool ökologische Bilanz (Basel competition tool) |
| `software_refair` | REFAIR | REFAIR — La Fab Bordeaux Réemploi platform |
| `software_opalis` (verify S23) | Opalis | Opalis — FCRBE-affiliated reused-materials directory |

### Norm (1 new)
| id | name | name_full |
|---|---|---|
| `norm_bs_5385_5_2009` | BS 5385-5:2009 | BS 5385-5:2009 — Code of practice for wall and floor tiling, Part 5 |

### ZertifizierungBewertungssystem
| id | name | name_full |
|---|---|---|
| `zbs_ecotool` | EcoTool | EcoTool (ökologische Bilanz — Pflichtnachweis Wettbewerb Lysbüchel) |

### Stadt nodes (NEW — verify S21 first)
Check each via S21; create only those absent:
`stadt_amsterdam`, `stadt_duebendorf`, `stadt_liverpool`, `stadt_bordeaux`, `stadt_merignac`, `stadt_winterthur`, `stadt_fribourg`, `stadt_ingersheim`, `stadt_weil_am_rhein`, `stadt_dundee`, `stadt_anderlecht`, `stadt_canterbury`, `stadt_esch_sur_alzette`, `stadt_eindhoven`, `stadt_coimbra` (+ optionally Berlin districts).

Each gets `LIEGT_IN_LAND → land_*`.

### Land nodes (NEW — verify S22 first)
Possibly missing: `land_ukraine`, `land_portugal`, `land_luxemburg`, `land_italien`. Each with `country_iso2`.

---

## Phase 3 — Quellen

Patch `phase_batch2_v2_3_quellen.patch.jsonl`.

### 22 case_markdown Quellen (one per dossier file; Interreg_NWE merges into FCRBE)

See [actor_extraction_per_dossier.md §Quellen consolidated](actor_extraction_per_dossier.md). Each carries:
```
quelltyp: "case_markdown"
source_file: "<filename>.md" (relative path)
url: (omit — local file)
access_date: "2026-05-19"
name: short id-suffix
name_full: full dossier title
```

### ~30 external_reference Quellen (high-value URLs only)

For each dossier with ≥ 3 BG/Akteur references to a single external URL, create an `external_reference` Quelle node. Then BG/Akteur creation patches in Phases 5/6 attach to the specific Quelle, not the catch-all `case_markdown`.

Examples (full list in [actor_extraction_per_dossier.md](actor_extraction_per_dossier.md)):
- `qu_circl_dutcharchitects_s1`, `qu_circl_abnamro_opening_s3`, `qu_circl_abnamro_report_s4`, `qu_circl_zuidas_dismantling_s6`, `qu_circl_icon_digital_twin_s7`
- `qu_careno_rotor_s1`, `qu_careno_retile_s2`
- `qu_lysp8_zirkular_s1`, `qu_lysp8_swissarc_s2`, `qu_lysp8_oxara_s4`
- `qu_meduni_baukarussell_s2`
- `qu_stuttgart210_baunetzwissen_s7`, `qu_stuttgart210_holzbauoffensive_s5`
- `qu_fcrbe_interreg_s1`
- `qu_rebridge_unistuttgart_r1`

---

## Phase 4 — Promote stub Projekte

Patch family `phase_batch2_v2_4*.patch.jsonl` (one per project).

Each sub-phase pattern:
1. `set_node_properties` — set `node_role='full_projekt'` + typed properties (bgf_m2, etc.)
2. `canonicalize_node` — set short name + name_full + UNION aliases (precondition: live aliases read)
3. `add_rel` — BELEGT_IN → primary case_markdown Quelle
4. `add_rel` — LIEGT_IN_STADT, LIEGT_IN_LAND
5. `add_rel` — NUTZT_BAUWERK → corresponding receiving Bauwerk
6. Phase 5/6/8 add actors/BGs/vocab

### 4a-4l (one per project — 23 total Projekte touched)

- 4a `p_lysp8_basel` (UNION aliases required)
- 4b `p_meduni_campus_mariannengasse`
- 4c `prog_stuttgart_210` (Programm after 1d) + new child `p_jugendtreff_ingersheim`
- 4d `p_reallabor_be_ware`
- 4e `p_schaerenmoosstrasse_zuerich`
- 4f `p_granby_workshop`
- 4g `p_careno_becircular`
- 4h `p_circl_abn_amro` (canonical post-1c — already enriched in 1c)
- 4i `p_umar_unit` — NEW vs PLAN.md (CORRECTIONS F1)
- 4j `p_elementa_walkeweg` — NEW vs PLAN.md (CORRECTIONS F1)
- 4k `prog_mas_dfab` enrichment + new children `p_eggshell_pavilion`, `p_up_sticks_dundee`
- 4l Akteur-shape migrations:
  - `p_refair_bordeaux_reemploi_platform` rels → `la_fabrique_de_bordeaux_metropole` + `software_refair` + `bw_base_du_reemploi_merignac`, then `delete_node`
  - `p_rcmi_concular` rels → `concular` + `tool_rcmi`, then `delete_node`

Full property + rel detail per project: [actor_extraction_per_dossier.md](actor_extraction_per_dossier.md) §1-§17.

---

## Phase 5 — New Akteure (~70 nodes)

Patch `phase_batch2_v2_5_akteure.patch.jsonl`. Includes existence pre-check for every id (apply tool's noop_existing).

For EVERY new Akteur:
```
add_node Akteur {id, name, name_full?, land?, source_scope: "case_markdown", aliases?: ["original spelling"]}
add_rel HAT_AKTEURTYP → at_*
add_rel HAT_AKTEURROLLE → ar_*
add_rel BELEGT_IN → primary case_markdown Quelle for that dossier
add_rel GEHÖRT_ZU → <organisation> (Persons only, where dossier evidences)
add_rel BETEILIGT_AN → <Projekt> (with rolle property)
```

Full list of ~70 actors across all 21 dossiers: [actor_extraction_per_dossier.md](actor_extraction_per_dossier.md).

### Summary by dossier (new actors count)

| Dossier | New Akteur count |
|---|---:|
| SMS Zürich | 7 |
| UMAR | 10 |
| ELEMENTA | 13 |
| Careno | 2 |
| Circl | 15 |
| LYSP8 | 10 |
| MedUni | 8 |
| Stuttgart 210 | 14 |
| Reallabor BE-WARE | 7 |
| Granby Workshop | 4 |
| FCRBE | 17 |
| REBRIDGE | (mostly existing partner-list orgs) |
| RE_USE Höfe | 4 |
| Reuse Logistics | 7 |
| REFAIR | 7 |
| RCMI/Concular | 3 |
| ETH (MAS DFAB) | (mostly existing seed actors) |
| Architecture of Reuse BXL | (all existing) |
| Vandkunsten | (all existing) |
| ZHAW | (all existing) |
| OBK_27 | (none) |
| **Total** | **~128** (many duplicates across dossiers; deduplicated to ~70 unique new Akteure) |

Estimated typed-rel writes for Phase 5: ~140 HAT_AKTEURROLLE + ~140 HAT_AKTEURTYP + ~30 GEHÖRT_ZU + ~70 BELEGT_IN + ~150 BETEILIGT_AN = **~530 new edges**.

---

## Phase 6 — Bauteilgruppen (~80 new BGs)

Patch family `phase_batch2_v2_6*.patch.jsonl` (one per project group).

### BG creation grammar (every BG must carry these)

```
add_node Bauteilgruppe {
  id: "bg_<reuse-status>_<material>_<bauteiltyp>_<discriminator>",
  name: "<≤25 chars>",
  name_full: "<full descriptive>",
  reuse_status: "reuse | retained | planned | dismantled",
  primary_material_id: "mat_*",  // singular pick; multi-material → mat_mehrere
  primary_bauteiltyp_id: "bt_*", // singular pick; multi → bt_mehrere
  alte_funktion: "<old function if FW>",   // CORRECTIONS O9
  neue_funktion: "<new function if FW>",   // CORRECTIONS O9
  counts_as_direct_reuse: true|false|null,
  source_scope: "case_markdown"
}
add_rel HAT_MATERIALGRUPPE → mg_*       // primary
add_rel NUTZT_MATERIAL → mat_*          // CORRECTIONS O8 — for each material
add_rel HAT_BAUTEILTYP → bt_*           // primary; multi-type → multiple rels
add_rel HAT_BAUTEILEBENE → be_*         // CORRECTIONS O1 — default be_bauteilgruppe
add_rel HAT_STATUS → status_*           // CORRECTIONS O2
add_rel HAT_RESSOURCENQUELLE → rq_*     // CORRECTIONS O3
add_rel HAT_WIEDERVERWENDUNGSART → wva_*
add_rel HAT_BESCHAFFUNGSWEG → bweg_*
add_rel HAT_VERBINDUNGSTECHNIK → vt_*    // optional
add_rel HAT_RUECKBAUVERFAHREN → rv_*     // optional
add_rel HAT_AUFBEREITUNG → av_*          // verified id from S6
add_rel HAT_PRUEFUNG → pr_*              // verified id from S7
add_rel HAT_ZUSTANDSKLASSE → zk_*        // NEW REL TYPE (first use; flag in rollback)
add_rel HAT_DEFEKT → def_*               // optional
add_rel HAT_BAUPRODUKTSTATUS → bps_*
add_rel HAT_LEISTUNGSANFORDERUNG → la_*
add_rel HAT_SCHADSTOFF → s_*             // ONLY when dossier evidences; do NOT fabricate
add_rel HAT_LOGISTIK → log_*
add_rel HAT_MARKTMODELL → mm_*           // when BG-specific market model differs from project default
add_rel HAT_MATCHINGQUALITAET → mq_*     // CORRECTIONS O9 — Funktionswechsel cases
add_rel AUS_BAUWERK → bw_*               // donor (NOT LIEFERT_MATERIAL_AUS)
add_rel EINGEBAUT_IN → bw_*              // receiver (NOT → Projekt)
add_rel BELEGT_IN → qu_*                 // dossier Quelle
add_rel HAT_BAUTEILGRUPPE ← p_*          // INCOMING: from Projekt to BG
add_rel TEIL_VON_KETTE → k_*             // when BG is part of a Wiederverwendungskette
```

### BG count by project
| Project | BG count |
|---|---:|
| SMS Zürich | 5 |
| UMAR | 8 |
| ELEMENTA | 4 |
| Careno | 4 |
| Circl (canonical p_circl_abn_amro) | 16 |
| LYSP8 | 6 |
| MedUni | 6 |
| Stuttgart 210 / Ingersheim | 3 |
| BE-WARE | 3 |
| Granby | 4 |
| ETH (Eggshell + Up Sticks) | 2 |
| **Total** | **61 new BGs** |

Full per-BG vocab spec: [actor_extraction_per_dossier.md](actor_extraction_per_dossier.md) §1-§17.

Estimated rel writes for Phase 6: 61 BGs × ~12 rels avg = **~730 new edges**.

### Funktionswechsel BG flagging (CORRECTIONS O9)

For every BG with `alte_funktion != neue_funktion`, emit:
- `Bauteilgruppe -[HAT_MATCHINGQUALITAET]-> mq_spec_zweckaenderung`
- BG property `alte_funktion` and `neue_funktion` (per GRAPH_SCHEMA.md:400-401)

8+ confirmed FW cases (see CORRECTIONS O9). Estimated +10 edges to mq_spec_zweckaenderung (already a 10-edge hub).

---

## Phase 7 — Wiederverwendungsketten (~8 new ketten)

Patch `phase_batch2_v2_7_ketten.patch.jsonl`. IDs use **`k_*`** prefix (CORRECTIONS C10).

| id | name (≤25) | name_full | donor BW | receiver BW |
|---|---|---|---|---|
| `k_stuttgart21_clt_to_ingersheim` | `S21 CLT→Ingersheim` | Stuttgart 21 CLT formwork → Jugendtreff Ingersheim CLT structure | bw_stuttgart21_hauptbahnhof | bw_jugendtreff_ingersheim |
| `k_ubs_altstetten_hall_to_sms` | `UBS Altst.→SMS ZH` | UBS Datenzentrum Altstetten hall components → Schärenmoosstrasse | bw_ubs_altstetten | bw_schaerenmoosstrasse_zuerich |
| `k_granby_rock_terrazzo_chain` | `Granby Rock Terrazzo` | Bricks/slates/skip waste → Granby Rock terrazzo | (multiple/unidentified) | (external markets) |
| `k_circl_larch_dismantling_chain` | `Circl Lärche DfD` | Locally sourced larch (2017) → DfD dismantling (2024) → storage for future reuse | bw_circl_pavilion_amsterdam | (storage depot) |
| `k_careno_rotor_tile_cleaning` | `Careno Fliesen Re-Tile` | Historic ceramic tiles 1900-1960 → Re-Tile cleaning → RotorDC sale | (multiple) | (external markets) |
| `k_wabbes_handles_to_umar` | `Wabbes→UMAR` (NEW) | Jules Wabbes door handles from Brussels Générale de Banque via Rotor → UMAR | bw_generale_de_banque_brussels | bw_umar_unit_duebendorf |
| `k_meduni_paternoster_to_aufzugmuseum` | `MedUni Paternoster→Mus.` (NEW) | Paternoster cabins from MedUni Mariannengasse → Wiener Aufzugmuseum | bw_meduni_campus_mariannengasse | (museum, no new BW) |
| `k_lysbueechel_to_elementa` | `Lysbüchel→ELEMENTA` (NEW) | Lysbüchel Parkgarage RC components → ELEMENTA Baufelder C+D | bw_lysbueechel_garage_basel | bw_elementa_walkeweg_basel |
| `k_lysp8_zuerich_kitchens` | `ZH-Küchen→LysP8` (NEW) | Zurich Wohnsiedlung kitchens → LysP8 fit-out | (TBC — possibly Mehr als wohnen) | bw_lysp8_basel |

### Wiring per kette

For each kette:
```
add_node Wiederverwendungskette {id, name, name_full}
add_rel BELEGT_IN → relevant Quelle
add_rel ← TEIL_VON_KETTE — Bauteilgruppe (one for each BG in the chain)
```

If Bauwerk-to-Kette rel exists (S34 finds one), wire donor + receiver Bauwerks too.

Estimated rel writes: 9 ketten × (~3 BGs avg) = ~27 TEIL_VON_KETTE edges.

---

## Phase 8 — Project-level vocabulary (restored from Plan 1; extended)

Patch family `phase_batch2_v2_8*.patch.jsonl`. Restores Plan 1 Phase 8 with corrected rel names + adds equivalents for the 14 new-scope projects.

For each of 23 projects, emit Projekt→Vocab edges per the table in [actor_extraction_per_dossier.md](actor_extraction_per_dossier.md). Pattern:

```
Projekt -[HAT_INTERVENTION]-> bai_*
Projekt -[HAT_NUTZUNG]-> nut_*
Projekt -[HAT_METHODE]-> meth_*
Projekt -[REFERENZIERT_NORM]-> norm_*
Projekt -[HAT_HUERDE]-> h_*
Projekt -[HAT_WIRTSCHAFT]-> wi_*
Projekt -[HAT_DOMINANT_MARKTMODELL]-> mm_*
Projekt -[HAT_DOMINANT_AKZEPTANZ]-> ak_*
Projekt -[NUTZT_SOFTWARE]-> software_*    // CORRECTED from HAT_SOFTWARE
Projekt -[NUTZT_TOOL]-> tool_*            // CORRECTED from HAT_TOOL
Projekt -[HAT_ZERTIFIZIERUNG]-> zbs_*
Projekt -[TEIL_VON_PROGRAMM]-> prog_*
Projekt -[ERHALT_FOERDERUNG_DURCH]-> prog_* or Akteur (funder)   // NEW in v2
Projekt -[NUTZT_BAUWERK]-> bw_*
```

Estimated rel writes for Phase 8: 23 projects × ~8 rel-types avg × ~1.5 targets avg = **~280 new edges**.

---

## Phase 9 — Cross-project bridges (connectivity catalysts)

Patch `phase_batch2_v2_9_bridges.patch.jsonl`.

Same intent as PLAN.md Phase 8 but corrected rel types. Every inferred bridge edge gets `r.source = "batch2_v2_import_2026-05-20"`, `r.evidence = "INFER"`.

| Bridge actor / programme / building | Connects (BETEILIGT_AN or similar) |
|---|---|
| `rotor_asbl_vzw` | prog_fcrbe + p_architecture_of_reuse_brussels + p_careno_becircular |
| `rotordc` | p_careno_becircular + p_umar_unit (Wabbes handles) |
| `tu_delft` | prog_rebridge + prog_fcrbe + p_circl_abn_amro |
| `zirkular_gmbh` | p_lysp8_basel + p_elementa_walkeweg |
| `prog_be_circular` | p_careno_becircular (TEIL_VON_PROGRAMM); prog_prec (TEIL_VON_PROGRAMM parent) |
| `assemble` | p_granby_workshop + existing Assemble projects in graph |
| `prog_mas_dfab` | p_eggshell_pavilion + p_up_sticks_dundee + (existing ETH projects) |
| `bw_ubs_altstetten` | p_schaerenmoosstrasse_zuerich (donor via BG) |
| `bw_lysbueechel_garage_basel` | p_elementa_walkeweg (donor via BG) |
| `bw_generale_de_banque_brussels` | p_umar_unit (donor via BG) |
| `bw_stuttgart21_hauptbahnhof` | p_jugendtreff_ingersheim + 4 future Reallabs (donor via BG depot) |

Plus the platform-merger fanout:
- All material-broker actors (`rotordc`, `concular`, `madaster`, `opalis`, `materialnomaden`) get `HAT_AKTEURROLLE → ar_materialbroker` (extending Phase C pattern).

Plus the Funktionswechsel hub (CORRECTIONS O9) — already covered in Phase 6 BG-level writes.

Estimated rel writes for Phase 9: **~40 new edges** (most connectivity already came from Phase 5/6/8).

---

## Phase 10 — Verification + rollback

### Cypher checks

```cypher
// 1. Final state
MATCH (n) WITH count(n) AS nodes
MATCH ()-[r]->() WITH nodes, count(r) AS rels
RETURN nodes, rels;
// EXPECTED: ~2520 nodes / ~18300 rels

// 2. Every new Bauteilgruppe has the 3 mandatory rels (O1/O2/O3)
MATCH (bg:Bauteilgruppe)
WHERE bg.source_scope = 'case_markdown' AND bg.id STARTS WITH 'bg_'
  AND NOT EXISTS { (bg)-[:HAT_BAUTEILEBENE]->() }
RETURN bg.id LIMIT 20;
// EXPECTED: 0 rows

MATCH (bg:Bauteilgruppe)
WHERE bg.source_scope = 'case_markdown' AND bg.id STARTS WITH 'bg_'
  AND NOT EXISTS { (bg)-[:HAT_STATUS]->() }
RETURN bg.id LIMIT 20;
// EXPECTED: 0 rows

// 3. Every new Akteur has typed role + type
MATCH (a:Akteur)
WHERE a.source_scope = 'case_markdown'
  AND NOT EXISTS { (a)-[:HAT_AKTEURROLLE]->() }
RETURN a.id LIMIT 20;
// EXPECTED: 0 rows

MATCH (a:Akteur)
WHERE a.source_scope = 'case_markdown'
  AND NOT EXISTS { (a)-[:HAT_AKTEURTYP]->() }
RETURN a.id LIMIT 20;
// EXPECTED: 0 rows

// 4. Every new Bauwerk has bauobjektrolle + bauobjektklasse
MATCH (bw:Bauwerk)
WHERE bw.source_scope = 'case_markdown'
  AND NOT EXISTS { (bw)-[:HAT_BAUOBJEKTROLLE]->() }
RETURN bw.id LIMIT 20;
// EXPECTED: 0 rows

// 5. Wiederverwendungskette prefix sanity
MATCH (k:Wiederverwendungskette) WHERE k.id STARTS WITH 'wk_'
RETURN k.id;
// EXPECTED: 0 rows (all use k_*)

// 6. Norm prefix sanity
MATCH (n:Norm) WHERE NOT n.id STARTS WITH 'norm_'
RETURN n.id;
// EXPECTED: 0 rows

// 7. No fabricated rel types
MATCH ()-[r]->()
WHERE type(r) IN ['HAT_SOFTWARE','HAT_TOOL','HAT_NORM','HAT_BAUAUFGABE',
                  'HAT_AKZEPTANZ','HAT_AUFBEREITUNGSVERFAHREN','HAT_PRUEFUNG_NACHWEIS',
                  'LIEFERT_MATERIAL_AUS','VERBUNDEN_MIT','LIEGT_IN']
RETURN type(r), count(*);
// EXPECTED: 0 rows

// 8. r.id integrity (CORRECTIONS XI.1)
MATCH ()-[r]->() WHERE r.id IS NULL
   OR r.id <> 'r_' + startNode(r).id + '__' + type(r) + '__' + endNode(r).id
RETURN type(r), count(*);
// EXPECTED: 0 rows after Phase R hygiene

// 9. Every promoted Projekt has node_role='full_projekt'
MATCH (p:Projekt) WHERE p.id IN [
  'p_lysp8_basel','p_meduni_campus_mariannengasse','p_reallabor_be_ware',
  'p_schaerenmoosstrasse_zuerich','p_granby_workshop','p_careno_becircular',
  'p_circl_abn_amro','p_umar_unit','p_elementa_walkeweg','p_jugendtreff_ingersheim',
  'p_eggshell_pavilion','p_up_sticks_dundee'
] AND (p.node_role IS NULL OR p.node_role <> 'full_projekt')
RETURN p.id, p.node_role;
// EXPECTED: 0 rows

// 10. Deleted nodes confirmed gone
MATCH (n) WHERE n.id IN [
  'p_obk_27','bizh','dare_gmbh','rotor_vzw','zirkular_cirkla',
  'p_pavilion_circl_amsterdam','p_interreg_nwe_fcrbe','p_refair_bordeaux_reemploi_platform',
  'p_rcmi_concular'
] RETURN n.id;
// EXPECTED: 0 rows

// 11. Case-specific nodes have BELEGT_IN
MATCH (n)
WHERE any(l IN labels(n) WHERE l IN
  ['Projekt','Bauteilgruppe','Bauwerk','Wiederverwendungskette','Stadt'])
  AND n.source_scope = 'case_markdown'
  AND NOT EXISTS { (n)-[:BELEGT_IN]->(:Quelle) }
RETURN labels(n)[0], n.id LIMIT 20;
// EXPECTED: 0 rows

// 12. Connectivity check — average degree of new nodes
MATCH (n) WHERE n.source_scope = 'case_markdown'
RETURN labels(n)[0] AS label, count(n) AS new_nodes,
       avg(size([(n)-[r]-() | r])) AS avg_degree
ORDER BY label;
// EXPECTED: avg_degree per label > 5 (connectivity goal achieved)
```

### Rollback ledger

Append to [_neo4j/review/round_002_followup/rollback.md](../../../review/round_002_followup/rollback.md):

```markdown
## Phase batch2_v2 — applied 2026-XX-XX

**Patch family:** batch2_v2_1a, 1b, 1c, 1d, 2, 3, 4a-4l, 5, 6a-6l, 7, 8a-8l, 9
**Pre-apply backup:** _neo4j/review/backups/batch2_v2_pre_apply/
**Before:** 2298 nodes / 17035 rels
**After:** ~2520 nodes / ~18300 rels (verify against §10.1)

[Full op breakdown table]

### Snapshot of deleted node rels (CORRECTIONS F17)
- p_obk_27: [paste rel snapshot from Phase 1a pre-delete Cypher]
- bizh: [paste]
- dare_gmbh: [paste]
- Werner_Sobek (if merged): [paste]
- p_pavilion_circl_amsterdam (pre-merge): [paste]
- p_interreg_nwe_fcrbe (pre-merge): [paste]
- p_refair_bordeaux_reemploi_platform (pre-rel-migration): [paste]
- p_rcmi_concular (pre-rel-migration): [paste]

### New rel types declared
- `HAT_ZUSTANDSKLASSE` — first use; ZustandsKlasse nodes exist, no prior incoming rels (intentional schema extension; documented in CORRECTIONS C6).

### Rollback procedure
[Phase-by-phase reverse-patch sequence; nuclear = restore from batch2_v2_pre_apply]
```

---

## Apply-tool workflow protocol (every patch)

1. `git -c core.longpaths=true status` — confirm clean working tree.
2. **Backup** to `_neo4j/review/backups/batch2_v2_<phase>_pre_apply/`.
3. **Pre-condition Cypher** asserts the prerequisite ids exist (precondition lives at the top of each patch file as a comment).
4. **Generate** JSONL patch under `_neo4j/review/round_002_followup/patches/batch2/`.
5. **Dry-run:** `python _scripts/apply_neo4j_review_patch.py --dry-run patches/batch2/<phase>.patch.jsonl`.
6. **Live apply:** confirmation phrase `APPLY <patch-file-name> TO mit-bestand`.
7. **Verify** via the relevant Phase 10 query section.
8. **Append** to rollback.md.
9. **Commit** with 3-word imperative subject (no AI co-author trailers).

---

## Net effect projection

| Item | PLAN.md (v1) | PLAN_v2 | Δ |
|---|---:|---:|---:|
| New Bauwerk nodes | 1 | 11 | +10 |
| New Akteur nodes | ~16 | ~70 | +54 |
| New Programm nodes | 2 | 8 | +6 |
| New Tool / Software / ZBS | 2 | 7 | +5 |
| New Norm | 1 (wrong prefix) | 1 (correct) | 0 |
| New Wiederverwendungskette | 5 (wrong prefix) | 9 (correct prefix) | +4 |
| New Bauteilgruppe | 65 | 61 (deduplicated) | -4 |
| New typed-rel edges (HAT_AKTEURROLLE, HAT_AKTEURTYP, HAT_BAUOBJEKTROLLE, NUTZT_MATERIAL, HAT_MATCHINGQUALITAET, GEHÖRT_ZU, etc.) | ~0 | ~250 | +250 |
| Project-level vocab edges (Phase 8) | sporadic | ~280 | +280 |
| BG-level vocab edges (Phase 6) | ~500 | ~730 | +230 |
| BELEGT_IN edges (Quellen + new nodes) | ~110 | ~220 | +110 |
| Wiederverwendungskette TEIL_VON_KETTE edges | 0 (missing) | ~30 | +30 |
| Bridge edges (Phase 9 / 10) | ~10 | ~40 | +30 |
| **Total approximate rel additions** | **~620** | **~1265** | **+645** |
| **Total approximate node additions** | **~80** | **~210** | **+130** |

PLAN_v2 adds **~2× the connectivity** of PLAN.md, with every new edge targeting a verified live id and every new node carrying source provenance.

---

## Decisions and scope boundaries (recorded)

| # | Decision | Rationale |
|---|---|---|
| D1 | Circl canonical = `p_circl_abn_amro` | PARKED_DECISIONS line 47; properties merged from pavilion |
| D2 | `Plattform` label dropped | Schema invention; dossiers (RCMI/REFAIR) reject classification |
| D3 | 4 unverified Programm names stay as Projekt | Dossiers say `identified_programme: no` |
| D4 | ETH dossier collapses to `prog_mas_dfab` | Only verified programme; aliases UNIONed |
| D5 | Reuse Logistics stays Projekt; new parent `prog_urban_bricolage` | Dossier confirms subproject relationship |
| D6 | UMAR + ELEMENTA brought in scope from batch 1.md | All 3 H1 sections of batch 1.md cover real projects |
| D7 | RE_USE Höfe "Wien" dropped from name (alias retained) | Dossier explicitly says Vienna location unverified |
| D8 | `k_*` prefix for Wiederverwendungskette | Match existing 63 nodes |
| D9 | `norm_bs_5385_5_2009` prefix | Match all 30 existing Norm ids |
| D10 | `bw_ubs_altstetten` (not bw_ubs_datacenter_altstetten) | Match Plan 1's shorter id |
| D11 | Werner Sobek canonical = `werner_sobek_p` | Plan 1 P0-A |
| D12 | Rotor canonical = `rotor_asbl_vzw` | STUB_AKTEUR_DECISIONS |
| D13 | Zirkular canonical = `zirkular_gmbh` | STUB_AKTEUR_DECISIONS |
| D14 | Brussels-Capital Region as new Akteur (not Region label) | No Region label exists |
| D15 | One case_markdown Quelle per dossier + ~30 external_reference Quellen | Per-claim provenance preserved without 200+ Quellen explosion |
| D16 | `HAT_ZUSTANDSKLASSE` declared as new rel type | First use; ZustandsKlasse nodes existed already |

---

## Excluded from this batch

- QUELLE_PLAN.md vocab-node BELEGT_IN backfill (future session per NAMING_AND_PROPERTIES_PLAN.md §7).
- 4 unverified Programm promotions (kept as Projekt per D3); revisit if new evidence surfaces.
- FCRBE's 37 pilot operations — Phase 6f checks which already exist; full cataloging deferred.
- Berlin district sub-Stadts (BE-WARE) — kept as Akteur properties for now; revisit if district-level Stadt becomes standard.
- Werner Sobek full merge (rel-delete only; full merge optional).
- Schadstoff fabrication on BGs where dossier says "unknown" (Lysbüchel garage PAK/asbest, Careno tile lead-glaze) — left as `s_unknown` / property `asbeststatus="not_screened"` instead.

---

## Open questions for execution agent

1. Run S4-S22 first — does `mehr_als_wohnen` already point at LYSP8's Zurich kitchen donor? If yes, link directly.
2. Run S10 — does `bt_belag` exist? If no, all `bg_*_belag_*` ids must use `_boden_` instead.
3. Run S6 — confirm which Aufbereitungsverfahren ids actually exist (drop Plan 1's invented `av_holzaufbereitung`, `av_remanufacturing`, `av_reinigung`).
4. Run S31 — what Circl-related Quellen already exist? Avoid id collisions in Phase 3.
5. Run S34 — does any Bauwerk-Kette rel type exist, or is BG-Kette the only entry-point?
6. PARKED_DECISIONS "MEDIA NOTE" — RE_USE Höfe scope: confirm dropping "Wien" from name is acceptable to user before final write.

---

## Reference files

- [PLAN.md](PLAN.md) — original 2026-05-20 plan (superseded; kept for diff)
- [CORRECTIONS_2026-05-20.md](CORRECTIONS_2026-05-20.md) — every change vs PLAN.md
- [actor_extraction_per_dossier.md](actor_extraction_per_dossier.md) — per-dossier authoritative inventory
- [pre_flight_validation.cypher](pre_flight_validation.cypher) — validation script
- [../2026-05-19_inbox_projects_import/PLAN.md](../2026-05-19_inbox_projects_import/PLAN.md) — Plan 1 (covers batch1.md only)
- [../2026-05-19_inbox_projects_import/CORRECTIONS.md](../2026-05-19_inbox_projects_import/CORRECTIONS.md) — Plan 1 audit (all findings absorbed)
- [../../../review/round_002_followup/NAMING_AND_PROPERTIES_PLAN.md](../../../review/round_002_followup/NAMING_AND_PROPERTIES_PLAN.md) — naming/id conventions
- [../../../review/round_002_followup/stub_research/GRAPH_SCHEMA.md](../../../review/round_002_followup/stub_research/GRAPH_SCHEMA.md) — node/rel reference
- [../../../review/round_002_followup/PARKED_DECISIONS.md](../../../review/round_002_followup/PARKED_DECISIONS.md) — stub Projekt decisions
- [../../../review/round_002_followup/STUB_AKTEUR_DECISIONS.md](../../../review/round_002_followup/STUB_AKTEUR_DECISIONS.md) — stub Akteur decisions
- [../../../review/round_002_followup/rollback.md](../../../review/round_002_followup/rollback.md) — apply ledger
- [../../../_scripts/apply_neo4j_review_patch.py](../../../_scripts/apply_neo4j_review_patch.py) — apply tool

---

**End of PLAN_v2.md.**
