# CORRECTIONS to 2026-05-19 Import Plan
# Audit date: 2026-05-19
# Method: Full live Neo4j schema query against all node types, relationship types,
#         and existing Bauteilgruppe pattern (confirmed against bg_reuse_stahl_gelaender_verbiest_charleroi)

## CRITICAL ERRORS — will cause import to fail or create wrong graph structure

---

### C1 — RELATIONSHIP NAME: `HAT_BAUAUFGABE` does not exist
**Locations:** Phase 8 (all five projects)
**Wrong:** `HAT_BAUAUFGABE`
**Correct:** `HAT_INTERVENTION`
**Evidence:** `CALL db.relationshipTypes()` shows `HAT_INTERVENTION`; query
`MATCH ()-[r:HAT_INTERVENTION]->(n:BauaufgabeIntervention)` confirmed.

---

### C2 — RELATIONSHIP NAME: `HAT_NORM` does not exist
**Locations:** Phase 8 (Schärenmoosstrasse, UMAR, ELEMENTA)
**Wrong:** `HAT_NORM: norm_sia_schweiz`
**Correct:** `REFERENZIERT_NORM: norm_sia_schweiz`
**Evidence:** Norm nodes have incoming rel type `REFERENZIERT_NORM` only (confirmed
by querying all incoming rels to Norm nodes and checking existing Projekt→Norm usage).

---

### C3 — RELATIONSHIP NAME: `HAT_SOFTWARE` does not exist
**Locations:** Phase 8 (UMAR, ELEMENTA)
**Wrong:** `HAT_SOFTWARE: software_ecotool`
**Correct:** `NUTZT_SOFTWARE: software_ecotool`
**Evidence:** `NUTZT_SOFTWARE` confirmed for both Projekt and Bauteilgruppe sources.

---

### C4 — RELATIONSHIP NAME: `HAT_TOOL` does not exist
**Locations:** Phase 8 (UMAR, ELEMENTA, Circl)
**Wrong:** `HAT_TOOL: tool_bim_bauteilkatalog`
**Correct:** `NUTZT_TOOL: tool_bim_bauteilkatalog`
**Evidence:** `NUTZT_TOOL` confirmed for both Projekt and Bauteilgruppe sources.

---

### C5 — RELATIONSHIP NAME: `HAT_AKZEPTANZ` does not exist
**Locations:** Phase 8 (Schärenmoosstrasse, UMAR, ELEMENTA)
**Wrong:** `HAT_AKZEPTANZ: ak_oeffentlicher_bauherr_pilot`
**Correct:** `HAT_DOMINANT_AKZEPTANZ: ak_oeffentlicher_bauherr_pilot`
**Evidence:** `HAT_DOMINANT_AKZEPTANZ` confirmed in schema. No `HAT_AKZEPTANZ` exists.

---

### C6 — RELATIONSHIP NAME: `HAT_AUFBEREITUNGSVERFAHREN` does not exist (Bauteilgruppe level)
**Locations:** Phase 7 (all 20 Bauteilgruppen) — header label "Aufbereitungsverfahren:"
**Wrong:** The plan header label implies `HAT_AUFBEREITUNGSVERFAHREN`
**Correct:** `HAT_AUFBEREITUNG`
**Evidence:** Confirmed from existing `bg_reuse_stahl_gelaender_verbiest_charleroi` which uses
`HAT_AUFBEREITUNG → Aufbereitungsverfahren` nodes.

---

### C7 — RELATIONSHIP NAME: `HAT_PRUEFUNG_NACHWEIS` / ambiguity (Bauteilgruppe level)
**Locations:** Phase 7 (all relevant Bauteilgruppen) — header label "PruefungNachweis:"
**Wrong:** The plan header label implies `HAT_PRUEFUNGNACHWEIS` or similar
**Correct:** `HAT_PRUEFUNG`
**Evidence:** Confirmed from `bg_reuse_stahl_gelaender_verbiest_charleroi`:
`HAT_PRUEFUNG → pr_zustandsbewertung` (label: `PruefungNachweis`).

---

### C8 — RELATIONSHIP NAME: `HAT_ZUSTANDSKLASSE` does not exist
**Locations:** Phase 7 (all relevant Bauteilgruppen) — header label "ZustandsKlasse:"
**Status:** `ZustandsKlasse` nodes EXIST in the graph (6 nodes, e.g., `zk_neuwertig`),
but NO relationship type currently connects any node to them. Zero hits on
`MATCH (a)-[r]->(n:ZustandsKlasse)`.
**Resolution needed:** Introduce `HAT_ZUSTANDSKLASSE` as a new relationship type
(first use in this import run). This is an intentional schema extension, not an error
in the vocabulary node IDs.

---

### C9 — STRUCTURAL: `EINGEBAUT_IN` targets only `Bauwerk`, NOT `Projekt`
**Locations:** Phase 7 (all Bauteilgruppen) — `EINGEBAUT_IN: p_xxx`
**Wrong:** `EINGEBAUT_IN → p_pavilion_circl_amsterdam` (Projekt node)
**Correct two-step pattern:**
  1. Create a `Bauwerk` node for each receiving building (new in Phase 1.5 below)
  2. Use `Bauteilgruppe -[EINGEBAUT_IN]-> Bauwerk` (receiving bw node)
  3. Use `Projekt -[HAT_BAUTEILGRUPPE]-> Bauteilgruppe` (from Projekt to BG)
  4. Use `Projekt -[NUTZT_BAUWERK]-> Bauwerk` (from Projekt to its Bauwerk)
**Evidence:** All existing `EINGEBAUT_IN` targets are `Bauwerk` nodes only. The correct
Projekt→BG direction is `HAT_BAUTEILGRUPPE` (confirmed: source=Projekt, target=Bauteilgruppe).

---

## STRUCTURAL OMISSIONS — plan is missing required fields

---

### O1 — MISSING: `HAT_BAUTEILEBENE` on every Bauteilgruppe
Every existing Bauteilgruppe has `HAT_BAUTEILEBENE → Bauteilebene` node.
Available `Bauteilebene` nodes: `be_bauteilgruppe`, `be_einzelbauteil`, `be_gebaeudeteil`,
`be_materialcharge`, `be_oberflaechenschicht`, `be_system`.
**Default for all 20 new Bauteilgruppen:** `HAT_BAUTEILEBENE → be_bauteilgruppe`
Exception: `bg_careno_raw_tiles` / `bg_careno_cleaned_tiles` → `be_materialcharge`
(tile stocks are material charges, not assembled BGs).

---

### O2 — MISSING: `HAT_STATUS` on every Bauteilgruppe
Every existing Bauteilgruppe has `HAT_STATUS → Status` node.
**Assignments by status:**
| Bauteilgruppen | Status |
|---|---|
| All UMAR BGs | `status_realisiert` |
| All Circl BGs | `status_rueckgebaut` (dismantled 2025) |
| bg_mage_bestand | `status_realisiert` (existing buildings) |
| bg_mage_hall, bg_mage_arcade | `status_geplant` (unbuilt competition) |
| All ELEMENTA BGs | `status_geplant` |
| bg_careno_raw_tiles | `status_realisiert` |
| bg_careno_cleaned_tiles | `status_realisiert` |

---

### O3 — MISSING: `HAT_RESSOURCENQUELLE` on Bauteilgruppen with donor buildings
For all BGs that come from a source Bauwerk (i.e., those that have `AUS_BAUWERK`):
**Use:** `HAT_RESSOURCENQUELLE → rq_donorgebaeude`
**Affected:** bg_mage_hall, bg_mage_arcade, bg_umar_wabbes_handles,
bg_elementa_baufeld_c, bg_elementa_baufeld_d, all Careno tiles.
For BGs from RotorDC stock (Careno cleaned tiles): `HAT_RESSOURCENQUELLE → rq_lager`
For BGs from own stock (bg_mage_bestand): `HAT_RESSOURCENQUELLE → rq_baustelle`

---

### O4 — MISSING: New receiving Bauwerk nodes (4 nodes)
Phase 7 requires `EINGEBAUT_IN → Bauwerk`. These Bauwerk nodes do not yet exist
for our 5 projects. Must be created before Phase 7.
See new Phase 1.5 below.

---

## FACTUAL / LOGIC CORRECTIONS

---

### F1 — Circl P0 merge: `BELEGT_IN → q_akteursliste_master_md` already on canonical node
When merging `p_circl_abn_amro` into `p_pavilion_circl_amsterdam`:
- `p_circl_abn_amro -[BELEGT_IN]-> q_akteursliste_master_md` — DO NOT copy,
  this Quelle is already present on `p_pavilion_circl_amsterdam`.
- `p_circl_abn_amro -[BELEGT_IN]-> q_actor_michel_baars_02` — copy to canonical node.
- `p_circl_abn_amro -[BELEGT_IN]-> q_actor_michel_baars_03` — copy to canonical node.
- `michel_baars -[ASSOZIIERT_MIT_PROJEKT]-> p_circl_abn_amro` — RETARGET to
  `p_pavilion_circl_amsterdam` (INCOMING relationship, source is michel_baars).
- `p_circl_abn_amro -[HAT_DOMINANT_MARKTMODELL]-> mm_intra_konzern` — copy to canonical.

---

### F2 — Already-linked actors NOT in plan's create list (Phase 4)
These actors already exist in the graph AND already have `ASSOZIIERT_MIT_PROJEKT`
pointing at the relevant project. Do NOT recreate them. Do NOT re-link them.

| Actor id | Actor name | Project already linked |
|---|---|---|
| `studio_trachsler_hoffmann` | Studio Trachsler Hoffmann | `p_schaerenmoosstrasse_zuerich` |
| `daniel_hoffmann` | Daniel Hoffmann | `p_schaerenmoosstrasse_zuerich` |
| `gian_trachsler` | Gian Trachsler | `p_schaerenmoosstrasse_zuerich` |
| `dirk_e_hebel` | Dirk E. Hebel | `p_umar_unit` |
| `felix_heisel` | Felix Heisel | `p_umar_unit` |
| `vanessa_propach` | Vanessa Propach | `p_umar_unit` |
| `carla_ferrando_costansa` | Carla Ferrando Costansa | `p_elementa_walkeweg` |
| `pablo_garrido_arnaiz` | Pablo Garrido Arnaiz | `p_elementa_walkeweg` |
| `lionel_billiet` | Lionel Billiet | `p_careno_becircular` |
| `sebastien_paulet` | Sébastien Paulet | `p_careno_becircular` |
| `hans_hammink` | Hans Hammink | `p_pavilion_circl_amsterdam` |

Note: `carla_ferrando_costansa` and `pablo_garrido_arnaiz` are likely PARABASE
co-designers (relationship role is null; should be set to "Architekt" during this run).
`lionel_billiet` and `sebastien_paulet` are Rotor researchers.
`studio_trachsler_hoffmann` + `daniel_hoffmann` + `gian_trachsler` are the design
architects for Schärenmoosstrasse.

---

### F3 — ZertifizierungBewertungssystem for ELEMENTA / EcoTool
The plan creates `zbs_ecotool` and links it via `HAT_ZERTIFIZIERUNG`.
`HAT_ZERTIFIZIERUNG` targets `ZertifizierungBewertungssystem` from `Projekt` — CONFIRMED ✓.
However: EcoTool was a Basel competition REQUIREMENT (mandatory tool), not a green
building certification earned. Using `HAT_ZERTIFIZIERUNG` is semantically a stretch.
**Recommendation:** Use `NUTZT_SOFTWARE: software_ecotool` as primary. Optionally
add `HAT_ZERTIFIZIERUNG: zbs_ecotool` with a note property `{note: "Pflichtnachweis Wettbewerb Lysbüchel"}`
to distinguish it from achievement certifications like BREEAM/DGNB.

---

### F4 — `HAT_WIRTSCHAFT` vs `HAT_WIRTSCHAFTSASPEKT`
Two relationship types exist: `HAT_WIRTSCHAFT` and `HAT_WIRTSCHAFTSASPEKT`.
Both target `Wirtschaft` nodes. Existing Bauteilgruppen use `HAT_WIRTSCHAFTSASPEKT`.
The plan uses `HAT_WIRTSCHAFT` at Projekt level.
**Status:** `HAT_WIRTSCHAFT` is used at Projekt level in the existing graph (verified 
implicitly — the plan correctly uses `HAT_WIRTSCHAFT` for Projekt). Use 
`HAT_WIRTSCHAFTSASPEKT` at Bauteilgruppe level if Wirtschaft is needed there.

---

### F5 — `mg_holz_biobasiert` for Ecovative mycelium (bg_umar_mycelium)
Plan assigns `mg_holz_biobasiert` to mycelium insulation boards (Ecovative).
Mycelium is bio-based but NOT wood. More precise: `mg_daemmstoff` (insulation category).
However `mg_holz_biobasiert` is the combined bio-based/wood category and no dedicated
`mg_biobasiert_nicht_holz` exists. Flag: use `mg_daemmstoff` to be accurate about
the material class; add a node property `material_note = "mycelium / pilzbasiert"`.

---

### F6 — `bweg_leihmodell` for UMAR Lindner ceiling and Desso carpets  
Plan uses `bweg_leihmodell` for the take-back service products (Lindner, Desso).
`bweg_leihmodell` EXISTS ✓. However the Desso carpet model is specifically a product-service
system ("Cradle to Cradle" take-back). The `mm_take_back_service` Marktmodell captures this
better. `bweg_leihmodell` is acceptable but the distinction from classic leasing should
be noted in a relationship property.

---

## NEW PHASE 1.5 — Create receiving Bauwerk nodes (4 new nodes)

Required before Phase 7 because `EINGEBAUT_IN` targets Bauwerk.

| id | name | Status | Notes |
|----|------|--------|-------|
| `bw_schaerenmoosstrasse_zuerich` | Schärenmoosstrasse Zürich (Umnutzungsprojekt) | `status_geplant` | Unbuilt competition; both Micro + Dixa buildings + new hall |
| `bw_umar_unit_duebendorf` | UMAR Unit, NEST Empa Dübendorf | `status_realisiert` | Built 2017–18; in NEST research platform |
| `bw_elementa_walkeweg_basel` | ELEMENTA Walkeweg Basel | `status_geplant` | Planned 2027–2029 |
| `bw_circl_pavilion_amsterdam` | Circl Pavilion Amsterdam | `status_rueckgebaut` | Built 2017; dismantled March 2025 |

**Links for each:**
- `Bauwerk -[LIEGT_IN_STADT]-> Stadt` (use existing Stadt nodes)
- `Bauwerk -[HAT_STATUS]-> Status`
- `Projekt -[NUTZT_BAUWERK]-> Bauwerk` (link Projekt to its own Bauwerk)

Careno: no receiving Bauwerk — `p_careno_becircular -[HAT_BAUTEILGRUPPE]-> bg_careno_*`
without `EINGEBAUT_IN`.

---

## UPDATED SUMMARY — New nodes to create

| Label | Original count | Correction | Revised count |
|-------|---------------|------------|---------------|
| `Stadt` | 2 | no change | 2 |
| `Bauwerk` (source buildings) | 3 | no change | 3 |
| `Bauwerk` (receiving buildings) | 0 | +4 NEW (Phase 1.5) | 4 |
| `Programm` | 3 | no change | 3 |
| `Software` | 1 | no change | 1 |
| `ZertifizierungBewertungssystem` | 1 | no change | 1 |
| `Akteur` | 44 | no change | 44 |
| `Bauteilgruppe` | 20 | no change | 20 |
| **Total** | **74** | **+4** | **78** |

**New relationship types introduced:**
- `HAT_ZUSTANDSKLASSE` — first use (ZustandsKlasse nodes exist, no incoming rels yet)

---

## CONFIRMED CORRECT IN PLAN (nothing to change)

- All vocabulary node IDs: every single node referenced in Phase 7 was verified
  to exist, including: all Bauteiltyp ✓, Materialgruppe ✓, WiederverwendungsArt ✓,
  Beschaffungsweg ✓, Verbindungstechnik ✓, Rueckbauverfahren ✓, Aufbereitungsverfahren ✓,
  Defekt ✓, PruefungNachweis ✓, Bauproduktstatus ✓, Leistungsanforderung ✓,
  Schadstoff ✓, Logistik ✓, Marktmodell ✓.
- All Huerde, Methode, Wirtschaft, BauaufgabeIntervention, Nutzung node IDs ✓.
- `norm_sia_schweiz` ✓ and `bps_nta_8713` ✓.
- Akzeptanz node `ak_oeffentlicher_bauherr_pilot` ✓.
- Tool nodes: `tool_bim_bauteilkatalog` ✓, `tool_bauteilkatalog` ✓,
  `tool_material_passports_maconda` ✓.
- All Programm nodes used as "existing" actually exist:
  `prog_wettbewerb` ✓, `prog_forschungsprojekt` ✓, `prog_reallabor` ✓,
  `prog_kommunales_programm` ✓.
- New Programm nodes correctly identified as missing:
  `prog_nest_empa`, `prog_be_circular`, `prog_stiftung_pwg` — none exist ✓.
- New Software `software_ecotool` and ZBS `zbs_ecotool` correctly absent ✓.
- All Stadt nodes claimed as existing actually exist:
  `stadt_zuerich` ✓, `stadt_basel` ✓, `stadt_bruessel` ✓.
- New Stadt nodes correctly identified as missing:
  `stadt_duebendorf` and `stadt_amsterdam` — neither exists ✓.
- All actor nodes claimed as "already existing" are confirmed present ✓.
- None of the 44 new actor names collide with existing Akteur.name values ✓.
- `HAT_ZERTIFIZIERUNG` relationship type exists and targets ZertifizierungBewertungssystem ✓.
- `HAT_WIRTSCHAFT` ✓, `TEIL_VON_PROGRAMM` ✓, `HAT_DOMINANT_MARKTMODELL` ✓,
  `HAT_HUERDE` ✓, `HAT_METHODE` ✓, `HAT_NUTZUNG` ✓ all confirmed in schema.
- `REFERENZIERT_NORM: norm_sia_schweiz` — this rel type is correctly named in
  correction C2 above; `norm_sia_schweiz` node exists ✓.
- `bps_tracimat_be` noted as candidate for Careno (Belgian context) — EXISTS ✓ but
  `bps_project_specific` chosen is also valid.
