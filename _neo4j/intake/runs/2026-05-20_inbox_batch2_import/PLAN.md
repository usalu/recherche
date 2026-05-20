> ⚠️ **SUPERSEDED** by [PLAN_v2.md](PLAN_v2.md), which incorporates all corrections from [CORRECTIONS_2026-05-20.md](CORRECTIONS_2026-05-20.md) and the user decisions documented in [HANDOFF.md §7](HANDOFF.md). This file is kept for diff/historic reference only — do not act on it.

---

# Plan: Batch 2 Import — 21 Inbox Dossiers (v3 — complete)

**Date:** 2026-05-20
**Version:** 3 — incorporates all PARKED_DECISIONS.md corrections, NAMING_AND_PROPERTIES_PLAN.md conventions, STUB_AKTEUR_DECISIONS.md, Phases A–P applied, and all 6 previously-missed inbox locations.

## TL;DR

Import / promote all 21 dossier files from `_neo4j/intake/inbox/projects/` into `mit-bestand`. Most target nodes ALREADY EXIST as stubs (per PARKED_DECISIONS.md, Phase H). The dominant pattern is PROMOTE/RELABEL/MERGE existing stubs — not bare add_node. Every new node must follow NAMING_AND_PROPERTIES_PLAN.md. Current graph: **2298 nodes / 16869 relationships** (Phases A–P all applied as of 2026-05-19).

External PLAN.md must be the first file written when execution begins.

---

## Critical corrections vs. previous plan

| # | Problem | Fix |
|---|---|---|
| 1 | Scope was 15 files in 4 folders | 21 files across 6 locations (3 folders missed) |
| 2 | Many "new" nodes already exist as stubs | Use set_node_properties + canonicalize_node NOT add_node |
| 3 | Wrong BG ids (project slug at front) | `bg_<reuse-status>_<material>_<bauteiltyp>_<discriminator>` — no project slug |
| 4 | Wrong ZustandsKlasse ids | Use only: zk_neuwertig, zk_gebrauchsspuren_funktional, zk_eingeschraenkt_nachbearbeitung, zk_eingeschraenkt_nutzungsklasse_reduzieren, zk_nicht_wiederverwendbar, zk_unbekannt_pruefung_offen |
| 5 | Wrong Marktmodell ids | Use only: mm_same_site, mm_plattform_vermittelt, mm_kauf_gebraucht, mm_kauf_neu, mm_spende, mm_take_back_service, mm_leasing, mm_rueckkauf, mm_forschungsprojekt_zuteilung, mm_intra_konzern, mm_unbekannt |
| 6 | Wrong Akzeptanz ids | Use only: ak_dgnb_zertifizierung, ak_breeam_zertifizierung, ak_leed_zertifizierung, ak_oeffentlicher_bauherr_pilot, ak_aesthetik_patinakultur |
| 7 | No BELEGT_IN on new nodes | Every new case-specific node MUST have BELEGT_IN → Quelle at creation |
| 8 | name too long | name ≤ 25 chars; long form → name_full |
| 9 | Wrong canonical Rotor id | `rotor_asbl_vzw` (NOT rotor or rotor_vzw) |
| 10 | Wrong canonical Zirkular id | `zirkular_gmbh` (NOT zirkular or zirkular_cirkla) |
| 11 | stiftung_habitat and eitel_partner as "new" | Both ALREADY IN GRAPH (KEEP stubs) |
| 12 | No apply-tool workflow | backup → JSONL patch → dry-run → live apply → verify → rollback.md → commit (3-word imperative) |

---

## Scope (21 files, 19 distinct dossiers)

### Previously covered (15 files in 4 folders)

| Folder | File | Graph action | Existing node |
|---|---|---|---|
| DE_AT_CH | LYSP8_Basel.md | PROMOTE stub | p_lysp8_basel (degree 23, HAS ALIASES) |
| DE_AT_CH | MedUni_Campus_Mariannengasse_Wien.md | PROMOTE stub | p_meduni_campus_mariannengasse (degree 5) |
| DE_AT_CH | Stuttgart_210.md | RELABEL → Programm + PROMOTE | p_stuttgart_210 (degree 26) |
| DE_AT_CH | Reallabor_Be_Ware.md | PROMOTE stub | p_reallabor_be_ware (degree 20) |
| DE_AT_CH | RE_USE_Hoefe_Wien.md | RELABEL → Programm | p_re_use_hoefe (degree 3) |
| EU_consortia | FCRBE_Facilitating_Circulation.md | RELABEL → Programm + enrich | p_fcrbe (degree 5) |
| EU_consortia | Interreg_NWE_FCRBE.md | MERGE into prog_fcrbe | p_interreg_nwe_fcrbe (degree 3) |
| EU_consortia | REBRIDGE_Structural_Reuse.md | RELABEL → Programm | p_rebridge_structural_reuse_project (degree 3) |
| EU_consortia | Reuse_Logistics.md | RELABEL → Programm | p_reuse_logistics (degree 3) |
| reuse_platform | RCMI_Concular.md | RELABEL → Plattform | p_rcmi_concular (degree 3) |
| reuse_platform | REFAIR_Bordeaux.md | RELABEL → Plattform | p_refair_bordeaux_reemploi_platform (degree 5) |
| teaching_programme | Architecture_of_Reuse_Brussels.md | RELABEL → Programm | p_architecture_of_reuse_brussels (degree 7) |
| teaching_programme | ETH_Circular_Construction_Programme.md | RELABEL → Programm (+ 2 child Projekts) | p_eth_circular_construction_student_reuse (degree 8, HAS ALIASES) |
| teaching_programme | Vandkunsten_Component_Reuse_Programme.md | RELABEL → Programm | p_vandkunsten_component_reuse (degree 7) |
| teaching_programme | ZHAW_Reuse_in_Construction.md | RELABEL → Programm | p_reuse_in_construction_zhaw (degree 8) |

### Previously missed (6 files in 3 locations)

| Location | File | Graph action | Existing node |
|---|---|---|---|
| BE_NL | Circl_Pavilion_Amsterdam.md | MERGE + PROMOTE + 16 BGs | p_pavilion_circl_amsterdam (5) → p_circl_abn_amro (4) |
| BE_NL | Circl_ABN_AMRO_Urban_Mining.md | DUPLICATE — actors only | same node |
| BE_NL | Careno_Be_Circular_Brussels.md | PROMOTE stub + 4 BGs + tool | p_careno_becircular (degree 5) |
| uk_unclear | Granby_Workshop_Liverpool.md | PROMOTE stub + 4 BGs | p_granby_workshop (degree 3) |
| uk_unclear | OBK_27.md | NEGATIVE FINDING → DELETE stub | p_obk_27 (degree 5) |
| root | batch 1.md | PROMOTE stub + 5 BGs + donor Bauwerk | p_schaerenmoosstrasse_zuerich (degree 10) |

---

## Phase 0: First execution step (non-DB)

0a. Create run folder: `e:\recherche\_neo4j\intake\runs\2026-05-20_inbox_batch2_import\`
0b. Write PLAN.md there (this file)
0c. Take fresh DB backup to `_neo4j/review/backups/batch2_pre_phase1/`
0d. Run pre-flight Cypher:

```cypher
// Verify graph state
MATCH (n) RETURN count(n) AS nodes;                    // expected ~2298
MATCH ()-[r]->() RETURN count(r) AS rels;              // expected ~16869

// Verify all PARKED stub ids still exist
MATCH (p:Projekt) WHERE p.id IN [
  'p_obk_27','p_pavilion_circl_amsterdam','p_circl_abn_amro',
  'p_fcrbe','p_interreg_nwe_fcrbe','p_architecture_of_reuse_brussels',
  'p_eth_circular_construction_student_reuse','p_reuse_in_construction_zhaw',
  'p_vandkunsten_component_reuse','p_rebridge_structural_reuse_project',
  'p_re_use_hoefe','p_reuse_logistics','p_rcmi_concular',
  'p_refair_bordeaux_reemploi_platform','p_stuttgart_210',
  'p_lysp8_basel','p_reallabor_be_ware','p_schaerenmoosstrasse_zuerich',
  'p_meduni_campus_mariannengasse','p_granby_workshop','p_careno_becircular'
] RETURN p.id, p.node_role, size([(p)-[r]-() | r]) AS degree;

// Verify akteur merge targets
MATCH (a:Akteur) WHERE a.id IN ['rotor_asbl_vzw','zirkular_gmbh']
RETURN a.id, a.name, size([(a)-[r]-() | r]) AS degree;

// Check already-existing actors (avoid duplicate add_node)
MATCH (a:Akteur) WHERE a.id IN [
  'tu_delft','abn_amro','bam','de_architekten_cie','assemble','lewis_jones','michel_baars',
  'stiftung_pwg','mehr_als_wohnen','stiftung_habitat','eitel_partner'
] RETURN a.id, a.name;

// Check already-existing software/tool/norm nodes
MATCH (n) WHERE n.id IN ['software_llmnt','llmnt','software_opalis','opalis','tool_retile',
  'n_bs_5385_5_2009','norm_bs_5385_5']
RETURN labels(n)[0] AS label, n.id, n.name;
```

---

## Phase 1: PARKED_DECISIONS cleanup

*(one patch file per sub-phase; each: dry-run → apply → verify → append rollback.md)*

Patch folder: `_neo4j/review/round_002_followup/patches/`

### 1a — Delete (`phase_batch2_1a_deletes.patch.jsonl`)

- `delete_node`: `p_obk_27` (OBK_27.md confirmed negative finding — no identifiable project)
- `delete_node`: `bizh` (unknown abbreviation, degree 0, no source_scope)
- `delete_node`: `dare_gmbh` (unclear firm, degree 1, no source_scope)

*Verify: none of these 3 ids found afterwards.*

### 1b — Akteur merges (`phase_batch2_1b_akteur_merges.patch.jsonl`)

- `merge_node`: `rotor_vzw` → `rotor_asbl_vzw` (Rotor cooperative dedup per STUB_AKTEUR_DECISIONS.md)
- `merge_node`: `zirkular_cirkla` → `zirkular_gmbh` (Zirkular GmbH dedup)
- NOTE: `zusammenkunft_berlin` stays — STUB_AKTEUR_DECISIONS.md reverted merge decision to KEEP

*Verify: rotor_vzw and zirkular_cirkla no longer exist; rotor_asbl_vzw and zirkular_gmbh gain their rels.*

### 1c — Projekt merge / Circl dedup (`phase_batch2_1c_circl_merge.patch.jsonl`)

- `merge_node`: `p_pavilion_circl_amsterdam` → `p_circl_abn_amro`
- p_circl_abn_amro becomes canonical; all 5 rels of p_pavilion_circl_amsterdam redirect here

*Verify: p_pavilion_circl_amsterdam no longer exists; p_circl_abn_amro has degree ≥ 9.*

### 1d — Relabel Projekt → Programm (`phase_batch2_1d_relabel_programm.patch.jsonl`)

Each relabel = `add_node` [Programm, new id] + `merge_node` [old Projekt id → new Programm id]

| old p_* id | new prog_* id | name (≤25) | name_full |
|---|---|---|---|
| p_fcrbe | prog_fcrbe | `FCRBE` | Facilitating the Circulation of Reclaimed Building Elements |
| p_interreg_nwe_fcrbe | → merge into prog_fcrbe | — | redundant; redirect all rels to prog_fcrbe |
| p_architecture_of_reuse_brussels | prog_architecture_of_reuse_bxl | `Arch. of Reuse BXL` | Architecture of Reuse Brussels |
| p_eth_circular_construction_student_reuse | prog_eth_circular_constr | `ETH Circular Constr.` | ETH Circular Construction Student Reuse (**union existing aliases!**) |
| p_reuse_in_construction_zhaw | prog_reuse_in_construction_zhaw | `ZHAW Reuse Constr.` | ZHAW Reuse in Construction |
| p_vandkunsten_component_reuse | prog_vandkunsten_component | `Vandkunsten Reuse R&D` | Vandkunsten Component Reuse Programme |
| p_rebridge_structural_reuse_project | prog_rebridge | `ReBridge` | ReBridge — Structural Reuse Research |
| p_re_use_hoefe | prog_re_use_hoefe | `RE_USE Höfe Wien` | RE_USE Höfe Wien |
| p_stuttgart_210 | prog_stuttgart_210 | `Stuttgart 210` | Stuttgart 210 — weiterdenken, weiterbauen! |
| p_reuse_logistics | prog_reuse_logistics | `Reuse Logistics` | Reuse Logistics / Urban Bricolage (HTWG) |

**ALIASES note:** Query `MATCH (p {id:'p_eth_circular_construction_student_reuse'}) RETURN p.aliases` before canonicalize_node. Union existing aliases with any new ones. Same for p_lysp8_basel.

*Verify: all 10 old p_* ids gone; 10 new prog_* ids exist with label Programm and their original rels.*

### 1e — Relabel Projekt → Plattform (`phase_batch2_1e_relabel_plattform.patch.jsonl`)

Each = `add_node` [Plattform] + `merge_node` [old → new]

| old p_* id | new plattform_* id | name (≤25) | name_full |
|---|---|---|---|
| p_refair_bordeaux_reemploi_platform | plattform_refair | `REFAIR` | REFAIR Bordeaux Réemploi Platform |
| p_rcmi_concular | plattform_rcmi_concular | `RCMI / Concular` | RCMI / Concular — Digital Materials Matching |

*Verify: both old ids gone; 2 Plattform nodes exist.*

---

## Phase 2: Shared supporting nodes

*(must complete before Phases 4–7; can run in parallel with Phase 3)*

Patch: `phase_batch2_2_shared_nodes.patch.jsonl`

### New Programm nodes (no existing stub)

- `prog_be_circular`: name `Be.Circular Brussels`, name_full `Be.Circular Programme Brussels-Capital Region (PREC)`
- `prog_mas_dfab`: name `MAS DFAB ETH`, name_full `MAS Architecture and Digital Fabrication ETH Zürich`

### New Software / Tool nodes (check existence first via Phase 0d query)

- `software_llmnt`: name `LLMNT`, name_full `LLMNT Material Passport Platform (Circl digital twin)`
- `tool_retile`: name `Re-Tile`, name_full `Re-Tile — Ceramic Tile Cleaning and Reuse Machine (Rotor 2022)`
- `software_opalis`: name `Opalis`, name_full `Opalis — Online Surplus Material Platform (FCRBE/Rotor)` — **check first**

### New Norm nodes (check existence first)

- `n_bs_5385_5_2009`: name `BS 5385-5:2009`, name_full `BS 5385-5:2009 Code of practice for wall and floor tiling — Part 5`

### New Bauwerk node (donor building)

- `bw_ubs_datacenter_altstetten`: name `UBS Datenz. Altstetten`, name_full `UBS Datenzentrum Altstetten, Zürich (demolition project; donor building for Schärenmoosstrasse hall components)`
- BELEGT_IN → qu_batch1_sms_zuerich_dossier

### Stadt nodes (check existence first)

```cypher
MATCH (s:Stadt) WHERE s.name IN ['Amsterdam','Liverpool','Bordeaux'] RETURN s.id, s.name;
```

Create only if missing: `stadt_amsterdam`, `stadt_liverpool`, `stadt_bordeaux`.

All Phase 2 nodes: every node must have BELEGT_IN → relevant Quelle.

---

## Phase 3: Quelle nodes

*(can run in parallel with Phase 2; must complete before any BELEGT_IN edge)*

Patch: `phase_batch2_3_quellen.patch.jsonl`

One Quelle per dossier file (quelltyp: `case_markdown`):

| id | source_file | name (≤25) |
|---|---|---|
| qu_lysp8_basel_dossier | LYSP8_Basel.md | `LYSP8 Basel dossier` |
| qu_medunicampus_wien_dossier | MedUni_Campus_Mariannengasse_Wien.md | `MedUni Wien dossier` |
| qu_stuttgart210_dossier | Stuttgart_210.md | `Stuttgart 210 dossier` |
| qu_beware_dossier | Reallabor_Be_Ware.md | `BE-WARE dossier` |
| qu_reusehoefe_dossier | RE_USE_Hoefe_Wien.md | `RE_USE Höfe dossier` |
| qu_fcrbe_dossier | FCRBE_Facilitating_Circulation.md | `FCRBE dossier` |
| qu_rebridge_dossier | REBRIDGE_Structural_Reuse.md | `ReBridge dossier` |
| qu_reuselogistics_dossier | Reuse_Logistics.md | `Reuse Logistics dossier` |
| qu_rcmi_concular_dossier | RCMI_Concular.md | `RCMI Concular dossier` |
| qu_refair_dossier | REFAIR_Bordeaux.md | `REFAIR Bordeaux dossier` |
| qu_arch_reuse_bxl_dossier | Architecture_of_Reuse_Brussels.md | `Arch. Reuse BXL dossier` |
| qu_eth_circular_constr_dossier | ETH_Circular_Construction_Programme.md | `ETH Circ. Constr. dossier` |
| qu_vandkunsten_dossier | Vandkunsten_Component_Reuse_Programme.md | `Vandkunsten dossier` |
| qu_zhaw_reuse_dossier | ZHAW_Reuse_in_Construction.md | `ZHAW Reuse dossier` |
| qu_careno_becircular_dossier | Careno_Be_Circular_Brussels.md | `Careno Be.Circular dossier` |
| qu_circl_pavilion_dossier | Circl_Pavilion_Amsterdam.md | `Circl Pavilion dossier` |
| qu_granby_workshop_dossier | Granby_Workshop_Liverpool.md | `Granby Workshop dossier` |
| qu_batch1_sms_zuerich_dossier | batch 1.md | `SMS Zürich dossier` |

---

## Phase 4: Promote stub Projekte

*(depends on Phases 1c, 2, 3)*

Sequence per project: `set_node_properties` → `canonicalize_node` → add BETEILIGT_AN rels.
HAT_BAUTEILGRUPPE rels added in Phase 6.

### 4a: p_lysp8_basel (`phase_batch2_4a_lysp8.patch.jsonl`)

- `set_node_properties`: node_role='full_projekt', projektstatus_text='competition winner; construction status TBC', source_scope='case_markdown'
- `canonicalize_node`: name='LYSP8 Basel', name_full='LYSP8 — LysBüchelStrasse 8 Reuse Pilot Basel'
  — **Query existing aliases first; provide the union.**
- BETEILIGT_AN: eitel_partner (ALREADY IN GRAPH), stiftung_habitat (ALREADY IN GRAPH), zirkular_gmbh (canonical post-1b)
- BELEGT_IN → qu_lysp8_basel_dossier

### 4b: p_meduni_campus_mariannengasse (`phase_batch2_4b_medunicampus.patch.jsonl`)

- `set_node_properties`: node_role='full_projekt', name='MedUni Campus Wien', name_full='MedUni Campus Mariannengasse Wien — Bestandstransformation'
- Add actor rels from dossier
- BELEGT_IN → qu_medunicampus_wien_dossier

### 4c: prog_stuttgart_210 + child Projekt (`phase_batch2_4c_stuttgart210.patch.jsonl`)

After Phase 1d, prog_stuttgart_210 exists as Programm. Enrich with programme context.
Create child Projekt:
- `p_jugendtreff_ingersheim`: name='Jugendtreff Ingersheim', name_full='Jugendtreff Ingersheim — CLT-Reuse Pilot Stuttgart 210'
  - VERBUNDEN_MIT → prog_stuttgart_210
  - BELEGT_IN → qu_stuttgart210_dossier

### 4d: p_reallabor_be_ware (`phase_batch2_4d_beware.patch.jsonl`)

- `set_node_properties`: node_role='full_projekt', name='Reallabor BE-WARE', name_full='Reallabor BE-WARE Berlin — Urban Mining Reallabor'
- Add actor rels (check for existing TU Berlin actors)
- BELEGT_IN → qu_beware_dossier

### 4e: p_schaerenmoosstrasse_zuerich (`phase_batch2_4e_sms_zuerich.patch.jsonl`)

- `set_node_properties`: node_role='full_projekt', name='Schärenmoosstr. ZH', name_full='Schärenmoosstrasse 115/117 Zürich — Büro zu Wohnen (Stiftung PWG, 2022)'
- BETEILIGT_AN: studio_trachsler_hoffmann, perez_schmidlin_bauingenieure, andreas_geser_landschaftsarchitekten, stiftung_pwg (all new — Phase 5)
- Persons: daniel_hoffmann, gian_trachsler, stefan_perez, michael_schmidlin, andreas_geser
- LIEGT_IN → Stadt Zürich (existing)
- BELEGT_IN → qu_batch1_sms_zuerich_dossier

### 4f: p_granby_workshop (`phase_batch2_4f_granby.patch.jsonl`)

- `set_node_properties`: node_role='full_projekt', name='Granby Workshop', name_full='Granby Workshop Liverpool — Recycled Terrazzo and Building Materials CIC'
- BETEILIGT_AN: assemble (check existing id first), will_shannon, granby_workshop_cic, granby_4_streets_clt
- lewis_jones: check if already linked; if so, verify rel type
- LIEGT_IN → stadt_liverpool
- BELEGT_IN → qu_granby_workshop_dossier

### 4g: p_careno_becircular (`phase_batch2_4g_careno.patch.jsonl`)

- `set_node_properties`: node_role='full_projekt', name='Careno Be.Circular', name_full='Careno Be.Circular Brussels — Ceramic Floor Tile Reuse Research'
- BETEILIGT_AN: rotor_asbl_vzw (canonical post-1b), lionel_billiet, sebastien_paulet, bbri
- VERBUNDEN_MIT → prog_be_circular
- BELEGT_IN → qu_careno_becircular_dossier

### 4h: p_circl_abn_amro (`phase_batch2_4h_circl.patch.jsonl`)

After Phase 1c, p_circl_abn_amro has ≥9 rels. Enrich:
- `set_node_properties`: node_role='full_projekt', name='Circl Amsterdam', name_full='Circl — ABN AMRO Circular Pavilion Amsterdam (2017–2025, demolished)'
- BETEILIGT_AN (verify each before adding):
  - hans_hammink (Person, architect)
  - de_architekten_cie (architect)
  - abn_amro (client — check existing)
  - tu_delft (research — check existing)
  - bam_bouw_techniek (contractor — check vs existing `bam`)
  - new_horizon_urban_mining (supplier)
  - lcp_circulair (demolition)
  - icon_real_estate
  - michel_baars (Person — already linked; verify)
  - donkergroen
- HAT_SOFTWARE → software_llmnt
- LIEGT_IN → stadt_amsterdam
- BELEGT_IN → qu_circl_pavilion_dossier

---

## Phase 5: New Akteure nodes

*(ALL preceded by existence check; do NOT create if already exists)*

Patch: `phase_batch2_5_akteure.patch.jsonl`

### New Persons

| id | name | GEHÖRT_ZU | Dossier |
|---|---|---|---|
| hans_hammink | Hans Hammink | de_architekten_cie | Circl |
| lionel_billiet | Lionel Billiet | rotor_asbl_vzw | Careno |
| sebastien_paulet | Sébastien Paulet | rotor_asbl_vzw | Careno |
| will_shannon | Will Shannon | assemble / granby_workshop_cic | Granby |
| daniel_hoffmann | Daniel Hoffmann | studio_trachsler_hoffmann | SMS Zürich |
| gian_trachsler | Gian Trachsler | studio_trachsler_hoffmann | SMS Zürich |
| stefan_perez | Stefan Pérez | perez_schmidlin_bauingenieure | SMS Zürich |
| michael_schmidlin | Michael Schmidlin | perez_schmidlin_bauingenieure | SMS Zürich |
| andreas_geser | Andreas Geser | andreas_geser_landschaftsarchitekten | SMS Zürich |

### New Organisations (check existence before creating)

| id | name (≤25) | Akteurtyp | Dossier |
|---|---|---|---|
| de_architekten_cie | `de Architekten Cie.` | Architekturbüro | Circl |
| abn_amro | `ABN AMRO` | Bauherr | Circl |
| new_horizon_urban_mining | `New Horizon` | Bauteilhändler | Circl |
| lcp_circulair | `lcp-circulair` | Rückbauunternehmen | Circl |
| icon_real_estate | `Icon Real Estate` | Projektentwickler | Circl |
| victory_group | `Victory Group` | Eigentümer | Circl |
| bam_bouw_techniek | `BAM Bouw + Techniek` | Generalunternehmer | Circl |
| donkergroen | `Donkergroen` | Landschaftsarchitekt | Circl |
| ter_velde_den_besten | `Ter Velde & Den Besten` | Surveyor/Scanning | Circl |
| bbri | `BBRI` | Forschungseinrichtung | Careno |
| granby_workshop_cic | `Granby Workshop CIC` | CIC | Granby |
| granby_4_streets_clt | `Granby 4 Streets CLT` | CLT | Granby |
| studio_trachsler_hoffmann | `Studio Trachsler Hoffm.` | Architekturbüro | SMS ZH |
| perez_schmidlin_bauingenieure | `Pérez Schmidlin Ing.` | Ingenieurbüro | SMS ZH |
| andreas_geser_landschaftsarchitekten | `AG Landschaftsarch.` | Landschaftsarchitekt | SMS ZH |
| stiftung_pwg | `Stiftung PWG` | Bauherr | SMS ZH |

All actors: BELEGT_IN → relevant Quelle (quelltyp: `case_markdown`).

---

## Phase 6: Bauteilgruppen

**BG id convention (mandatory):**
```
bg_<reuse-status>_<material>_<bauteiltyp>_<discriminator>
```

- **reuse-status:** `reuse / retained / planned / dismantled`
- **material:** `stahl / holz / beton / stahlbeton / glas / keramik / ziegel / naturstein / daemmstoff / aluminium / kunststoff / mdf / recyclingbeton / mehrere / unbekannt`
- **bauteiltyp:** `traeger / stuetze / wand / decke / dach / fassade / fenster / tuer / treppe / ausbau / belag / boden / daemmung / technik / mehrere`
- **discriminator:** mandatory; globally unique; ≤5 tokens

**Required BG properties on every node:**
- `reuse_status` (enum string)
- `primary_material_id` (mat_* id)
- `primary_bauteiltyp_id` (bt_* id)
- `name` (≤25 chars)
- `name_full`
- `BELEGT_IN` → Quelle node
- `HAT_BAUTEILGRUPPE` ← Projekt node

### 6a: LYSP8 Basel — 6 BGs (`phase_batch2_6a_bg_lysp8.patch.jsonl`)

| id | name (≤25) | reuse_status | notes |
|---|---|---|---|
| bg_reuse_mehrere_fassade_lysp8_external_mix | `LYSP8 Fassade Mix` | reuse | tiles, shutters, railings |
| bg_reuse_holz_ausbau_lysp8_kitchens | `LYSP8 Küchen ZH-Wohns.` | reuse | alte: kitchens from Wohnsiedlung ZH; mm_kauf_gebraucht |
| bg_reuse_stahl_belag_lysp8_grating_steps | `LYSP8 Gitterrost Stufen` | reuse | mm_kauf_gebraucht |
| bg_reuse_mehrere_ausbau_lysp8_doors_tiles | `LYSP8 Türen+Fliesen` | reuse | mm_kauf_gebraucht |
| bg_planned_holz_mehrere_lysp8_dfd_frame | `LYSP8 DfD Holztragwerk` | planned | designed for future disassembly |
| bg_planned_unbekannt_boden_lysp8_earthen_floor | `LYSP8 Lehmestrich` | planned | Oxacrete bio-based earthen floor |

Vocab: zk_gebrauchsspuren_funktional (BGs 1–4).

### 6b: MedUni Wien — 6 BGs (`phase_batch2_6b_bg_medunicampus.patch.jsonl`)

| id | name (≤25) | reuse_status | notes |
|---|---|---|---|
| bg_reuse_mehrere_technik_medunicampus_paternoster | `MedUni Paternoster` | reuse | mm_kauf_gebraucht |
| bg_reuse_stahl_ausbau_medunicampus_bike_workshop | `MedUni Fahrradwerkst.` | reuse | mm_kauf_gebraucht |
| bg_reuse_stahl_ausbau_medunicampus_heavy_shelves | `MedUni Schwerlastregale` | reuse | mm_kauf_gebraucht |
| bg_retained_mehrere_decke_medunicampus_glasdecke | `MedUni Jugendstildecke` | retained | Jugendstil glass ceiling; mm_same_site |
| bg_reuse_holz_wand_medunicampus_doors_as_cladding | `MedUni Türen→Wandverk.` | reuse | alte: doors; neue: wall cladding; mm_kauf_gebraucht |
| bg_dismantled_glas_technik_medunicampus_fluorescent | `MedUni Leuchtstoffr.` | dismantled | fluorescent tubes; hazardous removal |

### 6c: Stuttgart 210 / Jugendtreff Ingersheim — 3 BGs (`phase_batch2_6c_bg_stuttgart210.patch.jsonl`)

BGs attached to p_jugendtreff_ingersheim:

| id | name (≤25) | reuse_status | notes |
|---|---|---|---|
| bg_reuse_holz_mehrere_stuttgart210_clt_structure | `Ingersheim CLT Tragwerk` | reuse | alte: CLT formwork Stuttgart 21 Bahnhof; mm_kauf_gebraucht |
| bg_reuse_holz_ausbau_stuttgart210_clt_secondary | `Ingersheim CLT Ausbau` | reuse | CLT offcuts for secondary elements |
| bg_dismantled_holz_mehrere_stuttgart21_station_clt | `Stuttgart 21 CLT Donor` | dismantled | donor batch from Stuttgart 21 Bahnhof |

Wiederverwendungskette: wk_stuttgart21_clt_to_ingersheim (Phase 7).

### 6d: Reallabor BE-WARE — 3 BGs (`phase_batch2_6d_bg_beware.patch.jsonl`)

| id | name (≤25) | reuse_status | notes |
|---|---|---|---|
| bg_reuse_mehrere_mehrere_beware_urban_mining_mix | `BE-WARE Urban Mining` | reuse | mixed urban mining batch |
| bg_planned_mehrere_ausbau_beware_dfd_fitout | `BE-WARE DfD Ausbau` | planned | DfD interior fitout |
| bg_reuse_mehrere_boden_beware_salvaged_floor | `BE-WARE Altboden` | reuse | salvaged flooring; mm_kauf_gebraucht |

### 6e: RE_USE Höfe Wien — 2+ BGs (`phase_batch2_6e_bg_reusehoefe.patch.jsonl`)

**Read RE_USE_Hoefe_Wien.md during execution to identify specific Höfe and their BGs.**
Minimum stubs:

| id | name (≤25) | reuse_status |
|---|---|---|
| bg_reuse_mehrere_mehrere_reusehoefe_batch | `RE_USE Höfe Mix` | reuse |
| bg_planned_mehrere_fassade_reusehoefe_circpanel | `RE_USE Höfe Fassade` | planned |

### 6f: FCRBE / REBRIDGE / Reuse Logistics / Architecture BXL / ZHAW / Vandkunsten

No BGs directly on Programm nodes. During execution, read each dossier to:
- Add VERBUNDEN_MIT rels to child/pilot Projekts already in graph
- Add key actor BETEILIGT_AN rels
- Create demonstrator Projekt stubs if dossier specifies buildings with evidence

**FCRBE** specifically: check whether its 34 pilot case studies already exist in graph as stubs or full Projekts. Add VERBUNDEN_MIT → prog_fcrbe for those already present.

### 6g: ETH Circular Construction — 2 child Projekts + BGs (`phase_batch2_6g_bg_eth.patch.jsonl`)

New Projekts under prog_eth_circular_constr:
- `p_eggshell_pavilion`: name='Eggshell Pavilion', name_full='Eggshell Pavilion ETH MAS DFAB 2022'
  - BG: `bg_reuse_mehrere_mehrere_eggshell_recycled_structure` — name: `Eggshell Recycled Struct.`
  - VERBUNDEN_MIT → prog_eth_circular_constr, prog_mas_dfab
- `p_up_sticks_dundee`: name='Up Sticks Dundee', name_full='Up Sticks Dundee ETH MAS DFAB 2019'
  - BG: `bg_reuse_holz_mehrere_upsticks_timber_frame` — name: `Up Sticks Holzrahmen`
  - VERBUNDEN_MIT → prog_eth_circular_constr, prog_mas_dfab

**Read ETH_Circular_Construction_Programme.md to confirm these demonstrators and add further detail.**

### 6h: Careno Be.Circular — 4 BGs (`phase_batch2_6h_bg_careno.patch.jsonl`)

| id | name (≤25) | reuse_status | notes |
|---|---|---|---|
| bg_reuse_keramik_belag_careno_historic_tiles | `Careno Hist. Fliesen` | reuse | alte: ceramic floor tiles 1900s–1960s; mm_plattform_vermittelt (RotorDC); zk_gebrauchsspuren_funktional |
| bg_reuse_keramik_belag_careno_mortar_cleaned | `Careno Re-Tile Fliesen` | reuse | treated by Re-Tile machine; mm_kauf_gebraucht |
| bg_reuse_keramik_belag_careno_rotor_stock | `Careno RotorDC Lager` | reuse | RotorDC tile stock; mm_plattform_vermittelt |
| bg_reuse_keramik_belag_careno_bespoke_waste | `Careno Abfallmix` | reuse | bespoke waste-stream tile mixes; mm_kauf_gebraucht |

Actor link: HAT_TOOL → tool_retile.
Programme link: VERBUNDEN_MIT → prog_be_circular.

### 6i: Circl Amsterdam — 16 BGs (`phase_batch2_6i_bg_circl.patch.jsonl`)

| id | name (≤25) | reuse_status | notes |
|---|---|---|---|
| bg_reuse_holz_belag_circl_window_frame_floor | `Circl Fensterrahmen Boden` | reuse | alte: rejected wooden window frames; neue: wooden floorboards; mm_kauf_gebraucht |
| bg_reuse_beton_belag_circl_pcm_tiles | `Circl PCM Fliesenb.` | reuse | alte: reused concrete; neue: tile floors + PCM; mm_kauf_gebraucht |
| bg_dismantled_holz_mehrere_circl_larch_structure | `Circl Lärchentragswerk` | dismantled | DfD larch; installed 2017, dismantled 2024 → storage; mm_kauf_gebraucht |
| bg_reuse_daemmstoff_daemmung_circl_jeans_insulation | `Circl Jeans-Dämmung` | reuse | 16,000 old jeans; alte: jeans; neue: ceiling insulation; mm_spende |
| bg_reuse_mehrere_fenster_circl_conference_windows | `Circl Bürofenster` | reuse | alte: demolished office windows; mm_kauf_gebraucht; zk_gebrauchsspuren_funktional |
| bg_reuse_mehrere_ausbau_circl_restored_furniture | `Circl ABN Möbel` | reuse | alte: used ABN AMRO furniture; mm_intra_konzern |
| bg_planned_mehrere_technik_circl_leased_lifts | `Circl Mietaufzüge` | planned | take-back after 10 years; mm_leasing |
| bg_planned_mehrere_technik_circl_leased_lighting | `Circl Mietbeleuchtung` | planned | service model; mm_leasing |
| bg_reuse_mehrere_technik_circl_fire_hose_cabinets | `Circl Löschwandkästen` | reuse | second-hand from New Horizon; mm_plattform_vermittelt |
| bg_reuse_mehrere_wand_circl_clothing_felt | `Circl Textilfilz Wände` | reuse | alte: old ABN AMRO business clothing; mm_intra_konzern |
| bg_planned_mehrere_belag_circl_c2c_tarkett_floor | `Circl C2C Tarkett Boden` | planned | C2C-certified Tarkett iQ One; mm_kauf_gebraucht |
| bg_planned_mehrere_fassade_circl_remountable_facade | `Circl Remontierb. Fass.` | planned | C2C plant-module façade; actor: donkergroen |
| bg_dismantled_aluminium_fassade_circl_facade_sections | `Circl Fassadensekt.` | dismantled | some sawn into; zk_eingeschraenkt_nachbearbeitung |
| bg_dismantled_mehrere_boden_circl_floor_structure | `Circl Bodenaufbau` | dismantled | less suitable for reuse; zk_eingeschraenkt_nachbearbeitung |
| bg_dismantled_mehrere_technik_circl_solar_panels | `Circl Solaranlage` | dismantled | 500 panels, 7 years old; zk_gebrauchsspuren_funktional |
| bg_reuse_mehrere_ausbau_circl_greenery_harvest | `Circl Bepflanzung` | reuse | harvested by local residents; mm_spende |

Software: HAT_SOFTWARE → software_llmnt.
Wiederverwendungskette: wk_circl_larch_dismantling_chain (Phase 7).

### 6j: Granby Workshop Liverpool — 4 BGs (`phase_batch2_6j_bg_granby.patch.jsonl`)

| id | name (≤25) | reuse_status | notes |
|---|---|---|---|
| bg_reuse_mehrere_belag_granby_rock_terrazzo | `Granby Rock Terrazzo` | reuse | alte: broken bricks + slates + skip waste; mm_kauf_gebraucht; Norm: n_bs_5385_5_2009 |
| bg_reuse_ziegel_belag_granby_brick_slate_terrazzo | `Granby Brick+Slate Terr.` | reuse | Brick & Slate Terrazzo product; mm_kauf_gebraucht |
| bg_reuse_mehrere_ausbau_granby_first_house_products | `Granby Ersthaus-Produkte` | reuse | tiles, handles, fireplaces; mm_kauf_gebraucht |
| bg_reuse_mehrere_belag_granby_bespoke_waste | `Granby Abfallmix Belag` | reuse | bespoke waste-stream mixes; mm_kauf_gebraucht |

Vocab: ak_aesthetik_patinakultur (V&A + Crafts Council permanent collections).
Wiederverwendungskette: wk_granby_rock_terrazzo_chain (Phase 7).

### 6k: Schärenmoosstrasse Zürich — 5 BGs (`phase_batch2_6k_bg_sms_zuerich.patch.jsonl`)

| id | name (≤25) | reuse_status | notes |
|---|---|---|---|
| bg_reuse_mehrere_mehrere_sms_zuerich_ubs_hall | `SMS ZH UBS-Halle` | reuse | donor = bw_ubs_datacenter_altstetten; LIEFERT_MATERIAL_AUS → Bauwerk; zk_unbekannt_pruefung_offen; mm_kauf_gebraucht |
| bg_retained_mehrere_mehrere_sms_zuerich_existing_bldgs | `SMS ZH Bestand Micro+Dixa` | retained | existing buildings retained; mm_same_site |
| bg_planned_stahl_fassade_sms_zuerich_arcade | `SMS ZH Stahl-Laubengang` | planned | DfD steel arcade |
| bg_retained_stahlbeton_treppe_sms_zuerich_existing_stairs | `SMS ZH Bestandstreppen` | retained | retained stair cores; mm_same_site |
| bg_planned_mehrere_technik_sms_zuerich_pv_roof | `SMS ZH PV-Anlage Dach` | planned | 250 m² PV |

Wiederverwendungskette: wk_ubs_altstetten_hall_to_sms (Phase 7).

---

## Phase 7: Wiederverwendungsketten

Patch: `phase_batch2_7_ketten.patch.jsonl`

| id | name (≤25) | name_full |
|---|---|---|
| wk_stuttgart21_clt_to_ingersheim | `Stuttgart21 CLT→Ingersheim` | CLT formwork from Stuttgart 21 Bahnhof → structural reuse in Jugendtreff Ingersheim |
| wk_ubs_altstetten_hall_to_sms | `UBS Altstetten→SMS ZH` | Hall components from UBS Datenzentrum Altstetten → two-storey hall in Schärenmoosstrasse Zürich |
| wk_granby_rock_terrazzo_chain | `Granby Rock Terrazzo Chain` | Broken bricks + slates + skip waste → Granby Rock terrazzo products sold via CIC |
| wk_circl_larch_dismantling_chain | `Circl Lärche DfD Chain` | Locally sourced larch 2017 → Circl structure → circular dismantling 2024 → storage for future reuse |
| wk_careno_rotor_tile_cleaning | `Careno Fliesen Re-Tile` | Historic ceramic tiles → Re-Tile treatment → sale via RotorDC |

---

## Phase 8: Graph connectivity cross-links

*(can run parallel with Phase 7)*

Key bridges — primary stated goal of this import:

| Bridge | Nodes connected | Rel types |
|---|---|---|
| rotor_asbl_vzw | prog_fcrbe + prog_architecture_of_reuse_bxl + p_careno_becircular | BETEILIGT_AN + VERBUNDEN_MIT |
| tu_delft | prog_rebridge + prog_fcrbe + p_circl_abn_amro | BETEILIGT_AN |
| zirkular_gmbh | p_lysp8_basel + p_elementa_walkeweg (check existing) | BETEILIGT_AN |
| prog_be_circular | p_careno_becircular + prog_fcrbe | VERBUNDEN_MIT |
| bw_ubs_datacenter_altstetten | p_schaerenmoosstrasse_zuerich (via BG donor link) | LIEFERT_MATERIAL_AUS |
| assemble (check id) | p_granby_workshop + existing Assemble projects in graph | BETEILIGT_AN |

For every inferred / propagated edge: `r.source = 'batch2_import_2026-05-20'`

---

## Phase 9: Verification

```cypher
// 1. Node and rel counts
MATCH (n) RETURN count(n) AS nodes;           // expected: ~2450+
MATCH ()-[r]->() RETURN count(r) AS rels;     // expected: ~17500+

// 2. All new BGs have BELEGT_IN
MATCH (bg:Bauteilgruppe)
WHERE NOT EXISTS { (bg)-[:BELEGT_IN]->(:Quelle) }
RETURN bg.id, bg.name LIMIT 20;
// Expected: 0 rows

// 3. All promoted Projekts have node_role = 'full_projekt'
MATCH (p:Projekt)
WHERE p.id IN [
  'p_lysp8_basel','p_reallabor_be_ware','p_schaerenmoosstrasse_zuerich',
  'p_meduni_campus_mariannengasse','p_granby_workshop',
  'p_careno_becircular','p_circl_abn_amro'
]
AND (p.node_role IS NULL OR p.node_role <> 'full_projekt')
RETURN p.id, p.node_role;
// Expected: 0 rows

// 4. PARKED_DECISIONS cleanup confirmed
MATCH (n) WHERE n.id IN [
  'p_obk_27','bizh','dare_gmbh','rotor_vzw','zirkular_cirkla',
  'p_pavilion_circl_amsterdam'
] RETURN n.id;
// Expected: 0 rows

// 5. All old p_* relabeled ids gone, new prog_* / plattform_* nodes exist
MATCH (n) WHERE n.id IN [
  'p_fcrbe','p_interreg_nwe_fcrbe','p_architecture_of_reuse_brussels',
  'p_eth_circular_construction_student_reuse','p_reuse_in_construction_zhaw',
  'p_vandkunsten_component_reuse','p_rebridge_structural_reuse_project',
  'p_re_use_hoefe','p_stuttgart_210','p_reuse_logistics',
  'p_refair_bordeaux_reemploi_platform','p_rcmi_concular'
] RETURN n.id;
// Expected: 0 rows

// 6. BG name length check (all new BGs ≤ 25 chars)
MATCH (bg:Bauteilgruppe)
WHERE size(bg.name) > 25
RETURN bg.id, bg.name, size(bg.name) AS len ORDER BY len DESC LIMIT 10;

// 7. Wiederverwendungsketten created
MATCH (wk:Wiederverwendungskette) WHERE wk.id IN [
  'wk_stuttgart21_clt_to_ingersheim','wk_ubs_altstetten_hall_to_sms',
  'wk_granby_rock_terrazzo_chain','wk_circl_larch_dismantling_chain',
  'wk_careno_rotor_tile_cleaning'
] RETURN wk.id, wk.name;
// Expected: 5 rows

// 8. New actor nodes exist and have BELEGT_IN
MATCH (a:Akteur) WHERE a.id IN [
  'hans_hammink','lionel_billiet','sebastien_paulet','will_shannon',
  'de_architekten_cie','new_horizon_urban_mining','lcp_circulair',
  'bbri','granby_workshop_cic','studio_trachsler_hoffmann','stiftung_pwg'
]
OPTIONAL MATCH (a)-[:BELEGT_IN]->(q:Quelle)
RETURN a.id, q.id AS quelle;
// Expected: 11 rows, all with non-null quelle
```

---

## Apply-tool workflow protocol (every patch)

1. `git -c core.longpaths=true status` — confirm clean working tree
2. Backup: `_neo4j/review/backups/<phase>_pre_apply/`
3. Generate JSONL patch: `_neo4j/review/round_002_followup/patches/<phase>.patch.jsonl`
4. Dry-run: `python _scripts/apply_neo4j_review_patch.py --dry-run patches/<phase>.patch.jsonl`
5. Live apply: `APPLY <patch-file-name> TO mit-bestand`
6. Post-apply Cypher verification
7. Append to `rollback.md`
8. `git -c core.longpaths=true add -A && git -c core.longpaths=true commit -m "<3-word imperative>"` — NO AI trailers

---

## Decisions and scope boundaries

### Explicit decisions

- **p_stuttgart_210 → Programm** — dossier reveals research programme; override PARKED_DECISIONS PROMOTE to RELABEL + child Projekt p_jugendtreff_ingersheim
- **p_circl_abn_amro** = canonical target; p_pavilion_circl_amsterdam merges into it (Phase 1c)
- **ALIASES union required** for p_lysp8_basel and p_eth_circular_construction_student_reuse — query before canonicalize_node
- **Circl BG reuse_status** = `dismantled` for structural elements (installed 2017, removed 2024); `planned` for service-model / leased / DfD-designed
- **zusammenkunft_berlin** = KEEP; STUB_AKTEUR_DECISIONS.md reverted merge decision — no canonical duplicate found
- **p_umar_unit** and **p_elementa_walkeweg** = KEEP STUB; no new dossier for them in this batch

### Included

- All 21 inbox files processed (18 imports + 1 deletion + 2 duplicates merged)
- All PARKED_DECISIONS.md operations from the dossier set
- All STUB_AKTEUR_DECISIONS.md merges and deletes
- New BGs with correct id convention
- New Wiederverwendungsketten for significant reuse chains
- Cross-connectivity bridges (stated goal)

### Excluded from this batch

- QUELLE_PLAN.md controlled-vocab BELEGT_IN backfill — future session
- Actor registry people_to_add_checklist.md entries without dossier-specific links (Felix Heisel, Dirk Hebel, Werner Sobek, Annette Hillebrandt, Peter van Assche, Hester van Dijk, Reinder Bakker) — lower priority
- Phases L–P naming cleanup — already applied; new nodes must conform from creation

---

## Open questions for execution agent

1. Do `assemble`, `assemble_studio`, `tu_delft`, `abn_amro`, `bam` already exist? → Phase 0d query resolves this
2. Do `software_llmnt`, `software_opalis`, `tool_retile`, `n_bs_5385_5_2009` already exist? → Phase 0d query resolves this
3. Which specific Höfe does RE_USE_Hoefe_Wien.md describe? → Read file before Phase 6e
4. Does FCRBE dossier list 34 pilot Projekts? Are they already in graph? → Read file before Phase 6f
5. Does Vandkunsten dossier specify buildings with BGs, or only programme context? → Read file before Phase 6 (Vandkunsten)
6. Exact current aliases on p_lysp8_basel? → `MATCH (p {id:'p_lysp8_basel'}) RETURN p.aliases`

---

## Reference files

- `e:\recherche\_neo4j\intake\inbox\projects\` — all 21 dossier files
- `e:\recherche\_neo4j\review\round_002_followup\PARKED_DECISIONS.md`
- `e:\recherche\_neo4j\review\round_002_followup\STUB_AKTEUR_DECISIONS.md`
- `e:\recherche\_neo4j\review\round_002_followup\NAMING_AND_PROPERTIES_PLAN.md`
- `e:\recherche\_neo4j\review\round_002_followup\rollback.md`
- `e:\recherche\_scripts\apply_neo4j_review_patch.py`
- Batch 1 plan: `e:\recherche\_neo4j\intake\runs\2026-05-19_inbox_projects_import\PLAN.md`
