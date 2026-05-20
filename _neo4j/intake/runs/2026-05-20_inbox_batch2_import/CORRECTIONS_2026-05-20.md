# CORRECTIONS to 2026-05-20 PLAN.md (batch2 inbox import)

**Audit dates:** 2026-05-19 + 2026-05-20
**Method:** Cross-reference against `_neo4j/intake/runs/2026-05-19_inbox_projects_import/CORRECTIONS.md`, `_neo4j/review/round_002_followup/NAMING_AND_PROPERTIES_PLAN.md`, `_neo4j/review/round_002_followup/stub_research/GRAPH_SCHEMA.md`, `_neo4j/review/round_002_followup/rollback.md`, `PARKED_DECISIONS.md`, `STUB_AKTEUR_DECISIONS.md`, and direct reading of all 21 inbox dossier markdown files.
**Status:** Findings recorded; live validation complete (2026-05-20). See **§Z — Live validation results** at the bottom for confirmations and overrides.

---

## How to read this document

Three sections — they answer different questions for the patch generator:

- **A. CRITICAL ERRORS** — Plan.md uses something that will fail apply or create wrong graph structure. Must fix before generating patches.
- **B. STRUCTURAL OMISSIONS** — Plan.md is missing required edges/properties that every comparable existing node has. Must add for graph integrity.
- **C. FACTUAL / SCOPE CORRECTIONS** — Plan.md inherits an unverified claim or skips dossier-evidenced content. Must reconcile with dossiers before apply.

Every entry follows the same shape:

> ### CXX — Title
> **Locations:** PLAN.md line(s)
> **Wrong:** what Plan 2 says
> **Correct:** what to do
> **Evidence:** source-of-truth file / cypher query / dossier line

---

## A. CRITICAL ERRORS

### C1 — RELATIONSHIP NAME: `HAT_SOFTWARE` does not exist
**Locations:** PLAN.md L315 (Circl Phase 4h), L495 (Circl Phase 6i)
**Wrong:** `HAT_SOFTWARE: software_llmnt`
**Correct:** **`NUTZT_SOFTWARE: software_llmnt`**
**Evidence:** `GRAPH_SCHEMA.md:462` `NUTZT_SOFTWARE | Bauwerk/Projekt → Software`. Confirmed by 2026-05-19 CORRECTIONS.md C3 (same finding for batch 1).

### C2 — RELATIONSHIP NAME: `HAT_TOOL` does not exist
**Locations:** PLAN.md L471 (Careno Phase 6h)
**Wrong:** `HAT_TOOL: tool_retile`
**Correct:** **`NUTZT_TOOL: tool_retile`**
**Evidence:** `GRAPH_SCHEMA.md:463` `NUTZT_TOOL | Bauwerk/Projekt → Tool`. Confirmed by 2026-05-19 CORRECTIONS.md C4.

### C3 — RELATIONSHIP NAME: `VERBUNDEN_MIT` does not exist
**Locations:** PLAN.md L269 (`VERBUNDEN_MIT → prog_stuttgart_210`), L297 (`VERBUNDEN_MIT → prog_be_circular`), L458-459 (Eggshell/Up Sticks), L546-548 (Phase 8 bridges)
**Wrong:** `VERBUNDEN_MIT`
**Correct:** Target-dependent:
- Projekt → Programm: **`TEIL_VON_PROGRAMM`** (membership) OR **`ERHALT_FOERDERUNG_DURCH`** (funded by)
- Akteur ↔ Akteur peer link: **`VERBUNDEN_MIT_AKTEUR`**
**Evidence:** `GRAPH_SCHEMA.md:440,466,467`. The bare `VERBUNDEN_MIT` is not a valid rel type. Verify in S2/S3 of [pre_flight_validation.cypher](pre_flight_validation.cypher).

### C4 — RELATIONSHIP NAME: `LIEFERT_MATERIAL_AUS` is fabricated
**Locations:** PLAN.md L514 (`bg_reuse_mehrere_mehrere_sms_zuerich_ubs_hall` donor link), L550 (Phase 8 bridges)
**Wrong:** `LIEFERT_MATERIAL_AUS → bw_ubs_datacenter_altstetten`
**Correct:** **`AUS_BAUWERK → bw_ubs_datacenter_altstetten`** (from the Bauteilgruppe, NOT the Projekt)
**Evidence:** `GRAPH_SCHEMA.md:441` `AUS_BAUWERK | Bauteilgruppe → Bauwerk`. The donor relationship lives on the BG, not the Projekt.

### C5 — RELATIONSHIP NAME: `LIEGT_IN` (bare) is ambiguous
**Locations:** PLAN.md L282, L290, L317 ("LIEGT_IN → Stadt Zürich")
**Wrong:** `LIEGT_IN` (no suffix)
**Correct:** **`LIEGT_IN_STADT`** for cities, **`LIEGT_IN_LAND`** for countries
**Evidence:** `GRAPH_SCHEMA.md:464-465`. Spell out — the patch generator cannot disambiguate.

### C6 — RELATIONSHIP NAME: ambiguous BG vocab labels
**Locations:** PLAN.md Phase 6 (all BG specs use header labels like "Aufbereitungsverfahren:", "PruefungNachweis:")
**Wrong:** The label-to-rel mapping is implicit and inherits Plan 1's wrong rel names
**Correct:** Apply the table from `2026-05-19/CORRECTIONS.md`:

| Plan label | Correct rel type |
|---|---|
| Bauteiltyp | `HAT_BAUTEILTYP` |
| Materialgruppe | `HAT_MATERIALGRUPPE` |
| Material (fine-grained) | `NUTZT_MATERIAL` ← NEW in v2 (per S37/rollback.md:39) |
| WiederverwendungsArt | `HAT_WIEDERVERWENDUNGSART` |
| Beschaffungsweg | `HAT_BESCHAFFUNGSWEG` |
| Verbindungstechnik | `HAT_VERBINDUNGSTECHNIK` |
| Rueckbauverfahren | `HAT_RUECKBAUVERFAHREN` |
| Aufbereitungsverfahren | `HAT_AUFBEREITUNG` (NOT `HAT_AUFBEREITUNGSVERFAHREN`) |
| ZustandsKlasse | `HAT_ZUSTANDSKLASSE` ← NEW rel type (first use in this run; flag in rollback) |
| Defekt | `HAT_DEFEKT` |
| PruefungNachweis | `HAT_PRUEFUNG` (NOT `HAT_PRUEFUNGNACHWEIS`) |
| Bauproduktstatus | `HAT_BAUPRODUKTSTATUS` |
| Leistungsanforderung | `HAT_LEISTUNGSANFORDERUNG` |
| Schadstoff | `HAT_SCHADSTOFF` |
| Logistik | `HAT_LOGISTIK` |
| Marktmodell | `HAT_MARKTMODELL` |
| Methode | `HAT_METHODE` |
| Bauteilebene | `HAT_BAUTEILEBENE` (mandatory per O1) |
| Status | `HAT_STATUS` (mandatory per O2) |
| Ressourcenquelle | `HAT_RESSOURCENQUELLE` (mandatory per O3) |
| MatchingQualitaet | `HAT_MATCHINGQUALITAET` ← NEW in v2 (Funktionswechsel et al.) |
| AUS_BAUWERK | `AUS_BAUWERK` |
| EINGEBAUT_IN | `EINGEBAUT_IN` (→ Bauwerk only, NOT Projekt — see C9) |

**Evidence:** `GRAPH_SCHEMA.md:436-475` + `2026-05-19/CORRECTIONS.md` C6/C7/C8.

### C7 — STRUCTURAL: `EINGEBAUT_IN` targets only Bauwerk, never Projekt
**Locations:** PLAN.md Phase 6 (all 65+ BGs)
**Wrong:** Patches imply `EINGEBAUT_IN → p_*` (Projekt)
**Correct:** Create receiving Bauwerk nodes (see C8) and route `EINGEBAUT_IN → bw_*`. Then `Projekt -[HAT_BAUTEILGRUPPE]-> Bauteilgruppe` and `Projekt -[NUTZT_BAUWERK]-> Bauwerk` express the project-to-BG and project-to-Bauwerk relationships.
**Evidence:** `GRAPH_SCHEMA.md:442` `EINGEBAUT_IN | Bauteilgruppe → Bauwerk`. Confirmed by 2026-05-19 CORRECTIONS.md C9.

### C8 — STRUCTURAL: missing receiving Bauwerk nodes
**Locations:** PLAN.md Phase 2 (only `bw_ubs_datacenter_altstetten` is created)
**Wrong:** No receiving Bauwerk for the 7 projects that need them
**Correct:** Create receiving Bauwerks before Phase 6 (`HAT_BAUTEILGRUPPE` + `EINGEBAUT_IN`):

| id | name | Status | Stadt | bauobjektrolle | bauobjektklasse |
|----|------|--------|-------|----------------|-----------------|
| `bw_schaerenmoosstrasse_zuerich` | Schärenmoosstr. ZH | `status_geplant` | `stadt_zuerich` | `bor_same_site_donor_receiver` | `bok_gebaeude` |
| `bw_umar_unit_duebendorf` | UMAR Unit Dübendorf | `status_realisiert` | `stadt_duebendorf` | `bor_referenzobjekt` | `bok_gebaeudeteil` |
| `bw_elementa_walkeweg_basel` | ELEMENTA Walkeweg | `status_geplant` | `stadt_basel` | `bor_empfaengerobjekt` | `bok_gebaeude` |
| `bw_circl_pavilion_amsterdam` | Circl Pavilion AMS | `status_rueckgebaut` | `stadt_amsterdam` | `bor_donorobjekt` (post-dismantling) | `bok_pavillon` |
| `bw_lysp8_basel` | LysP8 Basel | `status_realisiert` | `stadt_basel` | `bor_empfaengerobjekt` | `bok_gebaeude` |
| `bw_meduni_campus_mariannengasse` | MedUni Wien | `status_realisiert` | `stadt_wien` | `bor_donorobjekt` | `bok_gebaeude` |
| `bw_jugendtreff_ingersheim` | Jugendtreff Ingersheim | `status_realisiert` | `stadt_ingersheim` | `bor_empfaengerobjekt` | `bok_pavillon` |

Carenco and Granby do not get receiving Bauwerks (Careno is a research project; Granby is a manufacturer whose products go to *external* receivers).
**Evidence:** 2026-05-19 CORRECTIONS.md O4. PLAN.md silently drops this.

### C9 — STRUCTURAL: missing donor Bauwerk for ELEMENTA
**Locations:** PLAN.md Phase 2 (one donor only)
**Wrong:** Only `bw_ubs_datacenter_altstetten` is created
**Correct:** Add donor Bauwerks per Plan 1 Phase 5:

| id | name | Notes |
|----|------|-------|
| `bw_ubs_altstetten` (canonical) | UBS Datenzentrum Altstetten | Two-storey hall for SMS Zürich (rename Plan 2's `bw_ubs_datacenter_altstetten` to this — match Plan 1's id) |
| `bw_generale_de_banque_brussels` | Générale de Banque / BNP Paribas Fortis HQ | Wabbes door handles for UMAR (via Rotor) |
| `bw_lysbueechel_garage_basel` | Lysbüchel Parkgarage | RC columns/slabs/rib panels for ELEMENTA Baufelder C+D |

**Evidence:** `2026-05-19 PLAN.md` Phase 5; dossier batch 1.md (UMAR Wabbes paragraph, ELEMENTA Lysbüchel paragraph).

### C10 — IDS: `wk_*` Wiederverwendungskette prefix conflicts with existing `k_*`
**Locations:** PLAN.md L530-534 (5 new ketten with `wk_*` prefix)
**Wrong:** `wk_stuttgart21_clt_to_ingersheim`, `wk_ubs_altstetten_hall_to_sms`, etc.
**Correct:** Use **`k_*`** prefix:
- `k_stuttgart21_clt_to_ingersheim`
- `k_ubs_altstetten_hall_to_sms`
- `k_granby_rock_terrazzo_chain`
- `k_circl_larch_dismantling_chain`
- `k_careno_rotor_tile_cleaning`

**Evidence:** 63 existing Wiederverwendungskette nodes all use `k_*` (verified [phase_n.patch.jsonl:242-257](_neo4j/review/round_002_followup/patches/phase_n.patch.jsonl#L242)).

### C11 — ID: `n_bs_5385_5_2009` violates `norm_*` prefix convention
**Locations:** PLAN.md L192, L502, L513
**Wrong:** `n_bs_5385_5_2009`
**Correct:** **`norm_bs_5385_5_2009`**
**Evidence:** All 30 existing Norm node ids use `norm_*` prefix (e.g. `norm_en_206`, `norm_sia_schweiz`, `norm_cen_ts_1090_201_2024`) per `NAMING_AND_PROPERTIES_PLAN.md:315-321`.

### C12 — INVENTED LABEL: `Plattform`
**Locations:** PLAN.md Phase 1e (lines 161-168)
**Wrong:** `Plattform` label is not in the 53-label catalogue
**Correct:** Drop the `Plattform` label entirely. Apply per-dossier shape:
- **REFAIR Bordeaux:** dossier evidences platform-operator + digital software, NOT a "Plattform" node. Use:
  - `Akteur la_fabrique_de_bordeaux_metropole` (already exists? verify S27)
  - `Software software_refair` (the platform itself)
  - `Bauwerk bw_base_du_reemploi_merignac` (physical depot at 26 avenue de la Somme, 33700 Mérignac)
- **RCMI / Concular:** dossier explicitly says `entity_type="workflow feature"`, `reduces_to_existing_node="Concular GmbH"`, `node_type="Tool"`. Use:
  - Existing `Akteur concular` (verify S27)
  - New `Tool tool_rcmi`
- For both old `p_*` ids: DO NOT relabel. Mark as deprecated by retargeting incoming rels to the new actor/software/tool nodes, then delete the old Projekt.

**Evidence:** `GRAPH_SCHEMA.md:8-65` (53 labels enumerated); `RCMI_Concular.md:21,50` rejects Plattform classification; `REFAIR_Bordeaux.md:50` says `node_type=Software`.

### C13 — INVENTED IDS: `av_holzaufbereitung`, `av_remanufacturing`, `av_reinigung`, etc.
**Locations:** PLAN.md Phase 6 — multiple BG specs
**Wrong:** Plan 2 inherits from Plan 1 these unverified Aufbereitungsverfahren ids:
- `av_holzaufbereitung` (UMAR timber, [PLAN.md:363](PLAN.md#L363))
- `av_remanufacturing` (Magna glass, Desso carpets — [PLAN.md:412,442](PLAN.md#L412))
- `av_reinigung` (Wabbes handles, Careno tiles, fire-hose cabinets — [PLAN.md:393,468,611](PLAN.md#L393))
- `av_rekonditionierung` (Wabbes handles — [PLAN.md:393](PLAN.md#L393))
- `av_qualitaetssicherung` (Careno cleaned tiles — [PLAN.md:577](PLAN.md#L577))
- `av_entmoertelung_von_fliesen` (Careno raw tiles — [PLAN.md:562](PLAN.md#L562))
- `av_moertelentfernung_ziegel` ✓ exists (Phase D)
- `av_holz_aufbereitung` ← does not exist as a parent

**Correct:** Replace each with the live id confirmed by S6:

| Plan 2 invented id | Likely replacement (verify S6) |
|---|---|
| `av_holzaufbereitung` | `av_hobeln_schleifen_holz`, `av_holz_zuschnitt_reparatur`, or `av_kaskadierende_wiederverwendung` (parent) |
| `av_remanufacturing` | `av_kaskadierende_wiederverwendung` (parent) |
| `av_reinigung` | Material-specific: `av_glas_reinigung_entkitten` (glass), `av_naturstein_reinigung_schleifen_zuschnitt` (stone), `av_aluminium_reinigung_entdichtung` (aluminium) |
| `av_rekonditionierung` | `av_betonfertigteil_factory_refurbishment` (concrete) or `av_fenster_refurbishment` (windows) |
| `av_qualitaetssicherung` | (no live equivalent — drop or use `av_materialsortierung_chargenbildung`) |
| `av_entmoertelung_von_fliesen` | `av_moertelentfernung_ziegel` (closest live id; tiles ≠ bricks but pattern matches) |

**Evidence:** Phase D added 34 specific Aufbereitungsverfahren ([rollback.md:854](_neo4j/review/round_002_followup/rollback.md#L854)). Run S6 to enumerate the live full list.

### C14 — UNVERIFIED PROGRAMME NAMES: 4 dossiers explicitly say "identified_programme: no"
**Locations:** PLAN.md Phase 1d (relabels to Programm)
**Wrong:** Plan 2 creates Programm nodes for dossiers whose programme identity is unverified
**Correct:** For these 4, do NOT promote/relabel to Programm. Keep as Projekt (or merge into a verified parent):

| Plan 2 op | Dossier says | Action |
|---|---|---|
| `p_architecture_of_reuse_brussels → prog_architecture_of_reuse_bxl` | `identified_programme: no` | KEEP Projekt; tag work to `rotor_asbl_vzw` instead |
| `p_vandkunsten_component_reuse → prog_vandkunsten_component` | `identified_programme: no` | KEEP Projekt; tag to `vandkunsten` Akteur |
| `p_reuse_in_construction_zhaw → prog_reuse_in_construction_zhaw` | `identified_programme: no` | KEEP Projekt; tag to `zhaw` Akteur |
| `p_eth_circular_construction_student_reuse → prog_eth_circular_constr` | `identified_programme: no`; verified name = MAS DFAB | MERGE into `prog_mas_dfab` (single Programm) |
| `p_reuse_logistics → prog_reuse_logistics` | `identified_programme: no`; is subproject under verified `Urban Bricolage` SNSF project | Create `prog_urban_bricolage` (verified parent) + keep `p_reuse_logistics` as child Projekt linked via TEIL_VON_PROGRAMM |
| `p_rcmi_concular → plattform_rcmi_concular` | `entity_type=workflow feature`, `reduces_to_existing_node=Concular GmbH` | See C12 — drop Plattform, use Software/Tool shape |
| `p_re_use_hoefe → prog_re_use_hoefe (name "RE_USE Höfe Wien")` | "Wien" location is unverified; actual evidence is Basel/Winterthur/Ukraine | RELABEL to Programm OK (RE_USE Höfe IS a programme/publication) but drop "Wien" from name + add Stadt Basel/Winterthur + Land Ukraine |

**Evidence:** Direct quotes from each dossier's "Identification status" section.

### C15 — Stadt id mismatch: Plan 2 uses Vienna-related stadts but never creates `stadt_wien`
**Locations:** PLAN.md L201-202 (Phase 2 Stadt check)
**Wrong:** Phase 0d check is `WHERE s.name IN ['Amsterdam','Liverpool','Bordeaux']` — but MedUni and RE-USE Höfe reference Wien which isn't checked
**Correct:** Expand the existence check (run S21):
```cypher
MATCH (s:Stadt) WHERE s.name IN [
  'Amsterdam','Liverpool','Bordeaux','Wien','Winterthur',
  'Fribourg','Mérignac','Dundee','Weil am Rhein','Ingersheim',
  'Stuttgart','Anderlecht','Brussels','Canterbury','Delft','Eindhoven',
  'Coimbra','Utrecht','Paris','Esch-sur-Alzette','Dübendorf'
] RETURN s.id, s.name;
```
Create the missing ones. Likely missing: `stadt_amsterdam`, `stadt_duebendorf`, `stadt_liverpool`, `stadt_bordeaux`, `stadt_winterthur`, `stadt_fribourg`, `stadt_merignac`, `stadt_dundee`, `stadt_weil_am_rhein`, `stadt_ingersheim`, `stadt_coimbra`, `stadt_eindhoven`, `stadt_esch_sur_alzette`.

**Evidence:** Multiple dossiers reference cities Plan 2 doesn't account for.

---

## B. STRUCTURAL OMISSIONS

### O1 — MISSING: `HAT_BAUTEILEBENE` on every new Bauteilgruppe
**Status:** Every existing Bauteilgruppe (308 BGs) has this rel. Plan 2 mentions it in Phase 6 prelude but doesn't write per-BG values.
**Default:** `HAT_BAUTEILEBENE → be_bauteilgruppe`
**Exceptions:** Careno tile stocks (`bg_reuse_keramik_belag_careno_*`) and any "material charge" type → `be_materialcharge`.
**Evidence:** 2026-05-19 CORRECTIONS.md O1.

### O2 — MISSING: `HAT_STATUS` on every new Bauteilgruppe
**Status:** Every existing BG has this. Plan 2 omits per-BG values.
**Defaults:**

| BG group | Status |
|---|---|
| UMAR BGs | `status_realisiert` |
| Circl BGs (`bg_*_circl_*`) | `status_rueckgebaut` (dismantled 2025) — except `bg_planned_*` which keep `status_geplant` |
| ELEMENTA BGs | `status_geplant` |
| Schärenmoosstrasse new BGs | `status_geplant` (unbuilt competition) |
| Schärenmoosstrasse retained BGs (`bg_retained_*_sms_*`) | `status_realisiert` |
| LYSP8 BGs | `status_realisiert` (completed 02/2025 per dossier) |
| MedUni BGs | `status_rueckgebaut` (pre-demolition reuse) |
| Stuttgart 210 / Jugendtreff Ingersheim BGs | `status_realisiert` (built 2024) |
| Careno BGs | `status_realisiert` |
| Granby BGs | `status_realisiert` (active product line) |

**Evidence:** 2026-05-19 CORRECTIONS.md O2.

### O3 — MISSING: `HAT_RESSOURCENQUELLE` on every new Bauteilgruppe
**Status:** Existing BGs carry this; Plan 2 omits.
**Defaults by donor pattern:**

| BG pattern | Ressourcenquelle |
|---|---|
| Has `AUS_BAUWERK` (specific donor) | `rq_donorgebaeude` |
| From bauteilboerse / Rotor DC stock / general stockpile | `rq_lager` |
| Same-site / existing building / Bestandserhalt | `rq_baustelle` |

**Evidence:** 2026-05-19 CORRECTIONS.md O3. Verify ids via S17.

### O4 — MISSING: `HAT_AKTEURROLLE` and `HAT_AKTEURTYP` for every new Akteur
**Status:** This is the single largest connectivity loss in Plan 2. Existing 582 Akteure carry these typed edges to controlled-vocab hubs (~25 Akteurrolle + ~9 Akteurtyp). New 50+ actors in Plan 2 patch spec only have free-text `Akteurtyp` columns.
**Required addition:** For each new Akteur emit two rels:
- `Akteur -[HAT_AKTEURROLLE]-> ar_*`
- `Akteur -[HAT_AKTEURTYP]-> at_*`

**Default role-mapping table** (verify ar_* ids via S4):

| Actor archetype | HAT_AKTEURROLLE | HAT_AKTEURTYP |
|---|---|---|
| Architecture office | `ar_entwurf_planung` | `at_unternehmen` |
| Structural engineer | `ar_tragwerksplanung` | `at_unternehmen` |
| Building physics | `ar_fachplanung_nachweis` | `at_unternehmen` |
| Landscape architect | `ar_landschaftsplanung` | `at_unternehmen` |
| Building services / MEP | `ar_tga_gebaeudetechnik` | `at_unternehmen` |
| Façade specialist | `ar_fassade` | `at_unternehmen` |
| Reuse consultant | `ar_reuse_zirkularitaetsberatung` | `at_unternehmen` |
| Material supplier | `ar_materiallieferung_markt` | `at_unternehmen` |
| Material broker / platform | `ar_materialbroker` | `at_materialhub_bauteilboerse` |
| Deconstruction contractor | `ar_rueckbau_bauteilernte_logistik` | `at_unternehmen` |
| General contractor | `ar_bauausfuehrung_fertigung` | `at_unternehmen` |
| Public authority / funder | `ar_oeffentliche_hand_foerderung` | `at_oeffentliche_institution` |
| Research institute / university | `ar_forschung_dokumentation` | `at_forschung_lehre` |
| Software/tool provider | `ar_software_digitalisierung` | `at_software_tool_anbieter` |
| Person | depends on role | `at_person` |
| Programme operator / NGO | various | `at_ngo_verband_netzwerk` |
| Client / Bauherrschaft | `ar_bauherr_auftraggeber` | `at_unternehmen` or `at_oeffentliche_institution` |

**Estimated rel addition:** ~120 edges (60 actors × 2 typed rels).

### O5 — MISSING: `GEHÖRT_ZU` for every Person → Org pair
**Status:** Existing graph has 216 GEHÖRT_ZU edges ([rollback.md:37](_neo4j/review/round_002_followup/rollback.md#L37)). Plan 2 lists `GEHÖRT_ZU` as a column in actor tables but never writes the rel type.
**Required addition:** For every new Person Akteur where the dossier names an organisation:

| Person | Org |
|---|---|
| Daniel Hoffmann, Gian Trachsler, Martin Zeller | studio_trachsler_hoffmann |
| Stefan Pérez, Michael Schmidlin | perez_schmidlin_bauingenieure |
| Andreas Geser | andreas_geser_landschaftsarchitekten |
| Pascal Hentschel, Rebecca Brandmayer, Laia Meier | zirkular_gmbh |
| Hans Hammink | de_architekten_cie |
| Lionel Billiet, Sébastien Paulet | rotor_asbl_vzw |
| Markus Meissner, Thomas Romm | baukarussell |
| Will Shannon | assemble (or granby_workshop_cic) |
| Stefan Krötsch, Roman Kreuzer, Thomas Stark | htwg_konstanz |
| Andreas Kretzer, Katharina Raabe, Maximilian Stemmler | klingelhoefer_kroetsch |
| Michelle Schneider | zhaw_ike |
| Félix Dillmann | verein_re_win |
| Madlen Kobi, Elena Sischarenco, Vanessa Feri, Adam Przywara, Rahel Jud | university_of_fribourg |
| Dominik Campanella, Julius Schäufele, Lenard da Costa Kurek | concular |
| Catherine De Wolf, Fabio Gramazio, Matthias Kohler | eth_zurich (verify via S27) |
| Michaël Ghyoot | rotor_asbl_vzw |

**Estimated:** ~20+ edges.

### O6 — MISSING: `HAT_BAUOBJEKTROLLE` + `HAT_BAUOBJEKTKLASSE` on every new Bauwerk
**Status:** All 196 existing Bauwerk nodes carry these. Plan 2's new Bauwerks have only `HAT_STATUS`.
**Required additions:** See C8 table (8 receiving + 3 donor Bauwerks × 2 rels = ~22 edges).

### O7 — MISSING: project-level vocabulary (Plan 1 Phase 8)
**Status:** Plan 2 drops the rich project-level vocab linking pattern from Plan 1 Phase 8 (~60-80 high-value edges to central vocab hubs).
**Required addition:** Restore Plan 1 Phase 8 for the 5 batch-1 projects + extend to the 21 batch-2 projects. Apply the corrected rel names (HAT_INTERVENTION, HAT_NUTZUNG, REFERENZIERT_NORM, HAT_HUERDE, HAT_METHODE, HAT_WIRTSCHAFT, HAT_DOMINANT_AKZEPTANZ, HAT_DOMINANT_MARKTMODELL, NUTZT_SOFTWARE, NUTZT_TOOL, TEIL_VON_PROGRAMM, ERHALT_FOERDERUNG_DURCH). See PLAN_v2 Phase 8 for the full table.

### O8 — MISSING: `NUTZT_MATERIAL → mat_*` per BG
**Status:** Existing graph has 134+ NUTZT_MATERIAL edges ([rollback.md:39](_neo4j/review/round_002_followup/rollback.md#L39)). Plan 2 writes only HAT_MATERIALGRUPPE (coarser).
**Required addition:** For each new BG, emit `NUTZT_MATERIAL → mat_*` for the specific material(s). Use S8 to enumerate live mat_* ids. Estimated: ~80 edges.

### O9 — MISSING: `HAT_MATCHINGQUALITAET → mq_*` for Funktionswechsel cases
**Status:** Plan 2 doesn't link to any MatchingQualitaet node. Funktionswechsel (function change) cases are explicit in dossiers and `mq_spec_zweckaenderung` is the existing hub ([phase_g.patch.jsonl:54-79](_neo4j/review/round_002_followup/patches/phase_g.patch.jsonl#L54)).
**Required addition:**

| BG | Old function | New function |
|---|---|---|
| `bg_reuse_holz_belag_circl_window_frame_floor` | window frame | floorboard |
| `bg_reuse_holz_wand_medunicampus_doors_as_cladding` | door | wall cladding |
| `bg_reuse_daemmstoff_daemmung_circl_jeans_insulation` | jeans (clothing) | ceiling insulation |
| `bg_reuse_mehrere_wand_circl_clothing_felt` | business clothing | wall/tribune felt |
| `bg_reuse_mehrere_belag_granby_rock_terrazzo` | bricks/slates/skip waste | terrazzo aggregate |
| `bg_reuse_mehrere_belag_granby_brick_slate_terrazzo` | bricks/slates | terrazzo aggregate |
| `bg_dismantled_holz_mehrere_stuttgart21_station_clt` | concrete formwork | (donor batch; no FW yet) |
| `bg_reuse_holz_mehrere_stuttgart210_clt_structure` | concrete formwork | structural CLT |

Each gets `Bauteilgruppe -[HAT_MATCHINGQUALITAET]-> mq_spec_zweckaenderung` plus property `alte_funktion` / `neue_funktion` per `GRAPH_SCHEMA.md:400-401`.

**Evidence:** Phase G already uses this pattern at Projekt level; BG-level extension is the natural next step.

### O10 — MISSING: typed Bauwerk + Programm + Quelle properties
**Status:** PLAN.md drops typed properties from GRAPH_SCHEMA. Free-form values used instead.
**Required additions per node label:**

Bauwerk: `bgf_m2`, `fertigstellung_jahr`, `bau_jahr_von`, `bau_jahr_bis`, `entwurfsstart_jahr`, `nutzung_alt`, `nutzung_neu`, `adresse`, `bauwerkstatus`, `reuse_anteil_prozent`, `reuse_masse_t`, `wiederverwendungsrate_gewicht_prozent`.
Examples:
- `bw_circl_pavilion_amsterdam`: `bgf_m2: 2000, fertigstellung_jahr: 2017, bau_jahr_von: 2016, year_opened_date: "2017-09-05", date_dismantled: "2025-03"`
- `bw_lysp8_basel`: `bgf_m2: 2250, bau_jahr_bis: 2025, geschosse_anzahl: "6-10", number_of_units: 27, site_area_m2: 686, volume_m3: 7170, adresse: "Weinlagerstrasse 33, 4056 Basel"`
- `bw_jugendtreff_ingersheim`: `bgf_m2: 50, fertigstellung_jahr: 2024, adresse: "Baumwasenweg, 74379 Ingersheim"`
- `bw_meduni_campus_mariannengasse`: `reuse_masse_kg: 60400, adresse: "Mariannengasse, Vienna"`

Programm: `start_year` / `start_jahr`, `end_year` / `end_jahr`, `funding_amount_eur`, `funding_programme`, `lead_organisation`, `host_institution`, `eu_funding_programme`, `grant_agreement_reference`, `status`, `type`.
Examples:
- `prog_fcrbe`: `start_year: 2018, end_year: 2023, status: "concluded", eu_funding_programme: "Interreg North-West Europe", lead_organisation: "Rotor", type: "Interreg"`
- `prog_rebridge`: `start_year: 2025, end_year: 2028, status: "active", eu_funding_programme: "Research Fund for Coal and Steel (RFCS)", grant_agreement_reference: "101157419", eu_contribution_eur: 1695121.69, lead_organisation: "University of Stuttgart"`
- `prog_recreate` (existing): already enhanced in Phase C

Quelle: `url`, `quelltyp` enum value, `source_file`, `access_date`.

### O11 — MISSING: Wiederverwendungskette edge wiring
**Status:** Plan 2 declares 5 ketten but no `TEIL_VON_KETTE` edges from BGs and no kette-to-Bauwerk edges.
**Required addition:** For each kette (using `k_*` prefix per C10):

```
k_stuttgart21_clt_to_ingersheim:
  TEIL_VON_KETTE ← bg_reuse_holz_mehrere_stuttgart210_clt_structure
                 ← bg_reuse_holz_ausbau_stuttgart210_clt_secondary
                 ← bg_dismantled_holz_mehrere_stuttgart21_station_clt

k_ubs_altstetten_hall_to_sms:
  TEIL_VON_KETTE ← bg_reuse_mehrere_mehrere_sms_zuerich_ubs_hall

k_granby_rock_terrazzo_chain:
  TEIL_VON_KETTE ← bg_reuse_mehrere_belag_granby_rock_terrazzo
                 ← bg_reuse_ziegel_belag_granby_brick_slate_terrazzo

k_circl_larch_dismantling_chain:
  TEIL_VON_KETTE ← bg_dismantled_holz_mehrere_circl_larch_structure

k_careno_rotor_tile_cleaning:
  TEIL_VON_KETTE ← bg_reuse_keramik_belag_careno_historic_tiles
                 ← bg_reuse_keramik_belag_careno_mortar_cleaned
                 ← bg_reuse_keramik_belag_careno_rotor_stock
```

If the live graph has Bauwerk-to-Kette rels (check S34), wire them too:
- `bw_ubs_altstetten` → `k_ubs_altstetten_hall_to_sms` (donor side)
- `bw_schaerenmoosstrasse_zuerich` → `k_ubs_altstetten_hall_to_sms` (receiver side)
- `bw_circl_pavilion_amsterdam` → `k_circl_larch_dismantling_chain`
- `bw_meduni_campus_mariannengasse` → new `k_meduni_paternoster_to_aufzugmuseum` (NEW kette — see C16)
- `bw_generale_de_banque_brussels` → new `k_wabbes_handles_to_umar` (NEW kette — see C16)

### O12 — MISSING ketten: Plan 2 misses 2-3 obvious reuse chains
**Status:** Even the 5 ketten Plan 2 declares don't include obvious chains from the dossiers.
**Required additions:**
- `k_wabbes_handles_to_umar`: Jules Wabbes door handles from Brussels (Générale de Banque) → Rotor → UMAR (already evidenced in batch 1.md UMAR dossier)
- `k_meduni_paternoster_to_aufzugmuseum`: Paternoster cabins from MedUni Campus → Wiener Aufzugmuseum (explicitly stated in MedUni dossier line 80)
- `k_lysbueechel_to_elementa`: Lysbüchel Parkgarage RC components → ELEMENTA Walkeweg Baufelder C+D (evidenced in batch 1.md ELEMENTA dossier)
- `k_lysp8_zuerich_kitchens`: Zurich Wohnsiedlung kitchens → LYSP8 (LYSP8 dossier line 98)

### O13 — MISSING: Werner Sobek duplicate cleanup
**Status:** P0-A in 2026-05-19 PLAN is unresolved; Plan 2 drops UMAR from scope so the duplicate persists.
**Action:** Fold into Phase 1b:
- Verify: `MATCH (p:Projekt {id:'p_umar_unit'})-[r:ASSOZIIERT_MIT_PROJEKT|BETEILIGT_AN]-(a:Akteur) WHERE a.name CONTAINS 'Sobek' RETURN a.id, a.name`
- If 2 rows: delete the rel from the duplicate id (likely `Werner_Sobek`), keep `werner_sobek_p`.
- Optionally: `merge_node` Werner_Sobek → werner_sobek_p.

### O14 — MISSING: Phase 0 pre-flight Cypher
**Status:** Plan 2's Phase 0d is partial (4 queries). Replace with the full 40-section [pre_flight_validation.cypher](pre_flight_validation.cypher).

---

## C. FACTUAL / SCOPE CORRECTIONS

### F1 — Batch 1.md contains 3 projects, not 1
**Locations:** PLAN.md L64 (scope table treats batch 1.md as Schärenmoosstrasse only); PLAN.md L646 (`p_umar_unit and p_elementa_walkeweg = KEEP STUB`)
**Reality:** [batch 1.md](../../inbox/projects/batch%201.md) has 3 H1 headings: Schärenmoosstrasse (L1), UMAR (L236), ELEMENTA (L494).
**Action:** Expand scope. Add UMAR + ELEMENTA promotion to PLAN_v2 Phase 4 (4i, 4j). Migrate Plan 1's full enrichment for both into PLAN_v2 Phase 6 (BGs) + Phase 8 (project-level vocab).

### F2 — Circl merge direction (decision recorded)
**Locations:** PLAN.md Phase 1c
**Conflict:** 2026-05-19 Plan 1 P0-B says canonical = `p_pavilion_circl_amsterdam`; Plan 2 says canonical = `p_circl_abn_amro`; PARKED_DECISIONS line 47 implies `p_pavilion_circl_amsterdam → p_circl_abn_amro`.
**Decision:** Follow PARKED_DECISIONS. Canonical = `p_circl_abn_amro`. Migrate all properties from pavilion (especially year_completed=2017, year_opened="2017-09-05", date_dismantled="2025-03", gross_floor_area=2000m², all incoming BELEGT_IN edges except duplicates) onto the canonical with explicit UNION patches.

### F3 — Plan 2 misses 6+ Circl actors named in dossier
**Locations:** PLAN.md Phase 5 Circl section
**Wrong:** Only 10 Circl actors listed
**Correct:** Add (verify against S27 first):

| id | name | role | GEHÖRT_ZU |
|---|---|---|---|
| `traject` | TRAJECT | construction-team coordinator | — |
| `vermaat` | Vermaat | circular catering operator | — |
| `exasun` | Exasun | solar-panel supplier | — |
| `fagerhult` | Fagerhult | DC lighting supplier | — |
| `de_groot_en_visser` | De Groot & Visser | façade / solar-boiler | — |
| `donkergroen` | Donkergroen | landscape / plant-module actor (already exists?) | — |

**Evidence:** [Circl_Pavilion_Amsterdam.md:74-92](../../inbox/projects/BE_NL_graph_ready_dossiers/Circl_Pavilion_Amsterdam.md#L74).

### F4 — Plan 2 misses 14 LYSP8 actors
**Locations:** PLAN.md Phase 4a/5 LYSP8 section
**Wrong:** Only 3 actors mentioned (eitel_partner, stiftung_habitat, zirkular_gmbh)
**Correct:** Add per dossier [LYSP8_Basel.md:73-89](../../inbox/projects/DE_AT_CH_graph_ready_dossiers/LYSP8_Basel.md#L73). See [actor_extraction_per_dossier.md](actor_extraction_per_dossier.md) §LYSP8.

### F5 — Plan 2 misses 14+ Stuttgart 210 actors
**Locations:** PLAN.md Phase 4c
**Wrong:** Phase 4c instruction is "Enrich with programme context" — no actors named
**Correct:** Add 14 actors from dossier. See [actor_extraction_per_dossier.md](actor_extraction_per_dossier.md) §Stuttgart_210.
- Most critical: `zueblin_timber_gmbh` + `ed_zueblin_ag` are the *donor-side* actors for the Stuttgart 21 CLT formwork — without them, the donor Bauwerk lacks an institutional anchor.

### F6 — Plan 2 misses 8 MedUni actors (BauKarussell is the load-bearing one)
**Locations:** PLAN.md Phase 4b
**Wrong:** "Add actor rels from dossier" with no list
**Correct:** Add 8 actors per [MedUni_Campus_Mariannengasse_Wien.md:73-80](../../inbox/projects/DE_AT_CH_graph_ready_dossiers/MedUni_Campus_Mariannengasse_Wien.md#L73). BauKarussell + BIG + Markus Meissner + Thomas Romm + DRZ + Die Kümmerei + MedUni Wien + Wiener Aufzugmuseum.

### F7 — Plan 2 misses 10 FCRBE actors + 8 typed Programm properties
**Locations:** PLAN.md Phase 6f (FCRBE)
**Wrong:** Says "check whether its 34 pilot case studies already exist" — dossier says 37
**Correct:** Set typed Programm properties:
```
type: "Interreg"
lead_organisation: "Rotor"
start_year: 2018
end_year: 2023
status: "concluded"
eu_funding_programme: "Interreg North-West Europe"
short_description: "The project aimed to increase by 50% the amount of reclaimed building elements circulated in North-West Europe by 2032."
```
Add 10 partner actors + persons per [FCRBE_Facilitating_Circulation_Reclaimed_Building_Elements.md:69-80](../../inbox/projects/EU_consortia_graph_ready_dossiers/FCRBE_Facilitating_Circulation_Reclaimed_Building_Elements.md#L69).

### F8 — Plan 2 misses REBRIDGE properties + 5 Land + 4 Stadt
**Locations:** PLAN.md Phase 1d (REBRIDGE relabel)
**Wrong:** No typed properties; no geographic edges
**Correct:** Set Programm properties:
```
type: "other"  (RFCS structural research)
start_year: 2025
end_year: 2028
status: "active"
eu_funding_programme: "Research Fund for Coal and Steel (RFCS)"
grant_agreement_reference: "101157419"
eu_contribution_eur: 1695121.69
lead_organisation: "University of Stuttgart / Institute of Lightweight Structures and Conceptual Design"
```
Add LIEGT_IN_LAND edges to 5 partner countries (DE existing, NL existing, PT new=`land_portugal`, LU new=`land_luxemburg`, IT new=`land_italien`) and LIEGT_IN_STADT for 4 partner cities (Stuttgart existing, Delft existing, Eindhoven new=`stadt_eindhoven`, Coimbra new=`stadt_coimbra`).

### F9 — RE-USE Höfe is NOT in Wien
**Locations:** PLAN.md L152 (name "RE_USE Höfe Wien")
**Wrong:** Programme name includes "Wien"
**Correct:**
- `name: "RE_USE Höfe"` (drop Wien)
- `name_full: "RE-USE Höfe — zirkuläre Lieferketten anhand der Fensterwiederverwendung"`
- `aliases: ["RE_USE Höfe Wien", "REUSE Yards"]` (preserve search via alias)
- LIEGT_IN_STADT: `stadt_basel`, `stadt_winterthur` (per dossier)
- LIEGT_IN_LAND: `land_schweiz`, NEW `land_ukraine`
- New actors: `verein_re_win`, `zhaw_ike`, `michelle_schneider`, `felix_dillmann`

**Evidence:** [RE_USE_Hoefe_Wien.md:23](../../inbox/projects/DE_AT_CH_graph_ready_dossiers/RE_USE_Hoefe_Wien.md#L23): *"public sources checked do not verify Vienna and instead document RE-WIN/ZHAW, Basel/Winterthur, Switzerland-Ukraine window reuse chains"*.

### F10 — `prog_be_circular` lacks parent `prog_prec`
**Locations:** PLAN.md L182 (creates prog_be_circular only)
**Reality:** Careno dossier line 130: *"Programm: Be.Circular; Programme Régional pour l'Économie Circulaire"* — two-tier programme.
**Action:** Create `prog_prec` (PREC, Programme Régional pour l'Économie Circulaire — Brussels) AND `prog_be_circular` as child:
- `prog_be_circular -[TEIL_VON_PROGRAMM]-> prog_prec`
- `p_careno_becircular -[TEIL_VON_PROGRAMM]-> prog_be_circular`
- `p_careno_becircular -[ERHALT_FOERDERUNG_DURCH]-> brussels_capital_region` (NEW Akteur)

### F11 — Circl needs `prog_abn_amro_mission_2030`
**Locations:** PLAN.md Phase 4h (no programme attached to Circl)
**Reality:** Circl dossier line 218: `Circl TEIL_VON_PROGRAMM ABN AMRO Mission 2030`.
**Action:** Create `prog_abn_amro_mission_2030` Programm node and link `p_circl_abn_amro -[TEIL_VON_PROGRAMM]-> prog_abn_amro_mission_2030`.

### F12 — Stuttgart 210 needs `prog_holzbau_offensive_bw`
**Locations:** PLAN.md Phase 4c
**Reality:** Stuttgart 210 dossier line 89: *"Holzbau-Offensive Baden-Württemberg | Programm | funding"*.
**Action:** Create `prog_holzbau_offensive_bw`. Add `p_jugendtreff_ingersheim -[ERHALT_FOERDERUNG_DURCH]-> prog_holzbau_offensive_bw`.

### F13 — Reuse Logistics: dossier says it's a SUBPROJECT, not a Programm
**Locations:** PLAN.md L154 (relabel `p_reuse_logistics → prog_reuse_logistics`)
**Reality:** Dossier `identified_programme: no`; subproject of SNSF "Urban Bricolage" project.
**Action:**
- Create `prog_urban_bricolage` (verified parent SNSF project)
- Keep `p_reuse_logistics` as Projekt (subproject) linked via `TEIL_VON_PROGRAMM → prog_urban_bricolage`
- Add Stadt Fribourg + actors per dossier (Madlen Kobi, University of Fribourg, materialnomaden GmbH, etc.)

### F14 — Norm prefix correction (C11 cross-ref)
**Locations:** PLAN.md L502, L513
**Wrong:** Plan 2 emits `n_bs_5385_5_2009`
**Correct:** `norm_bs_5385_5_2009`. Add `REFERENZIERT_NORM` edges from Granby BGs to it.

### F15 — Quelle short names don't follow convention
**Locations:** PLAN.md Phase 3
**Drift:** Plan 2 names Quellen like `LYSP8 Basel dossier`, `MedUni Wien dossier`. Existing convention from `NAMING_AND_PROPERTIES_PLAN.md:711` is `id_suffix → short name` (e.g. `q_villa_welpeloo_enschede_s3 → "Welpeloo S3"`).
**Action:** For each new `qu_*_dossier`:
- `name`: short id-suffix (e.g. `LysP8 dossier`)
- `name_full`: full dossier title (e.g. `LysP8 Basel — Loeliger Strub / Zirkular / Stiftung Habitat dossier`)
- `quelltyp`: `"case_markdown"`
- `source_file`: relative path from `_neo4j/intake/inbox/projects/`

### F16 — Per-claim external Quellen recommended
**Locations:** PLAN.md Phase 3
**Drift:** One Quelle per dossier collapses 5-15 distinct sources.
**Action:** For high-value external URLs (≥3 BG references), create `external_reference` Quellen and route BG-specific BELEGT_IN edges to them. See [actor_extraction_per_dossier.md](actor_extraction_per_dossier.md) for the per-dossier external Quelle list.

### F17 — Drop OBK_27 only after logging
**Locations:** PLAN.md Phase 1a (`delete_node p_obk_27`)
**Risk:** 5 rels of unknown content are destroyed.
**Action:** Before delete, run snapshot Cypher:
```cypher
MATCH (n {id:'p_obk_27'})-[r]-(m)
RETURN type(r), m.id, m.name, properties(r);
```
Paste result into rollback.md before applying delete.

### F18 — Brussels-Capital Region is missing from Akteur list
**Locations:** PLAN.md Phase 5 (Careno section)
**Wrong:** Plan 2 omits `brussels_capital_region`
**Correct:** Add as new Akteur with `HAT_AKTEURROLLE → ar_oeffentliche_hand_foerderung`, `HAT_AKTEURTYP → at_oeffentliche_institution`, country=BE.

### F19 — Programme vs Akteur: Be.Circular
**Resolved:** Plan 1 noted ambiguity (Akteur vs Programm). Plan 2 (and PLAN_v2) decides: **Programm**. Do not create Akteur `be_circular_be_brussels`.

### F20 — REFAIR / Concular Plattform → use Software/Tool shape (cross-ref C12)
See C12 for full remediation.

### F21 — ETH Circular Construction: collapse to MAS DFAB
**Locations:** PLAN.md Phase 6g
**Wrong:** Plan 2 creates both `prog_eth_circular_constr` AND `prog_mas_dfab`
**Correct:** Keep only `prog_mas_dfab` (verified). The old Projekt `p_eth_circular_construction_student_reuse` gets its rels migrated to `prog_mas_dfab` via `merge_node`, with its aliases unioned into the new node's aliases array.

### F22 — Vandkunsten / ZHAW / Architecture-of-Reuse-Brussels: keep as Projekt (cross-ref C14)
Do not relabel to Programm — dossiers explicitly say `identified_programme: no`. See C14.

### F23 — Drop "Wien" from RE_USE Höfe and add real evidence (cross-ref F9)

### F24 — Donor Bauwerk id collision
**Locations:** PLAN.md L196 (`bw_ubs_datacenter_altstetten`); Plan 1 L198 (`bw_ubs_altstetten`).
**Resolution:** Pick **`bw_ubs_altstetten`** (Plan 1's shorter id) and alias `ubs_datacenter_altstetten`, `ubs_datenzentrum_altstetten`. Saves character budget on edge `r.id`s.

### F25 — `bauobjektrolle` text vs `HAT_BAUOBJEKTROLLE → bor_*` rel
**Locations:** PLAN.md Phase 6 (UMAR enrichment sets `bauobjektrolle = "Demonstrator / Reallabor / materialdepot"` text)
**Wrong:** Free-text property when a controlled vocab exists
**Correct:** Drop free-text. Add `HAT_BAUOBJEKTROLLE → bor_referenzobjekt` (Reallabor maps best to "reference object" since UMAR is a demonstrator).
Same pattern for Plan 2's `bauobjektklasse = "Wohnbau / Gewerbebau"` etc. — use `HAT_BAUOBJEKTKLASSE → bok_*` instead.

### F26 — Aliases must be unioned, not overwritten
**Locations:** PLAN.md L156, L255 (notes the need but doesn't enforce)
**Risk:** Existing aliases on `p_lysp8_basel`, `p_eth_circular_construction_student_reuse`, `imd_raadgevende_ingenieurs`, `cleveland_steel_tubes`, `rotor_dc`, `duncan_baker_brown`, `land_daenemark` (per `NAMING_AND_PROPERTIES_PLAN.md:61`) will be silently overwritten by canonicalize_node if the patch generator doesn't pre-read.
**Action:** Patch generator MUST read current aliases via S35/S36 and emit the UNION.

### F27 — `bt_belag` validation needed
**Locations:** PLAN.md BG ids using `belag` slot (Granby, LYSP8, Careno, MedUni)
**Risk:** `bt_belag` may not exist in the live graph (only `bt_boden` is documented in GRAPH_SCHEMA).
**Action:** Run S10. If `bt_belag` doesn't exist:
- Option A: rewrite affected BG ids to use `_boden_` slot
- Option B: create `bt_belag` as a deliberate schema extension (flag in rollback)

---

## D. Sequencing for the patch generator

1. **Run [pre_flight_validation.cypher](pre_flight_validation.cypher)** — confirm/deny every assumption above.
2. **Update this document** with live results (e.g. "S6 returns N rows; av_holzaufbereitung confirmed absent").
3. **Generate the JSONL patches** from PLAN_v2.md *only after* the above is resolved.
4. **Each patch declares a precondition Cypher** that asserts the prerequisite ids exist before the patch can apply.

---

## E. Net effect projection

If all corrections above are applied via PLAN_v2:

| Item | Plan 2 | PLAN_v2 | Δ |
|---|---:|---:|---:|
| New Bauwerk nodes | 1 | 11 | +10 |
| New Akteur nodes | ~16 | ~70 | +54 |
| New Programm nodes | 2 | 6 | +4 |
| New Tool nodes | 1 | 2 | +1 |
| New Software nodes | 1 | 3-4 | +2-3 |
| New Wiederverwendungskette nodes | 5 | 8-9 | +3-4 |
| New typed-rel edges (HAT_AKTEURROLLE, HAT_AKTEURTYP, HAT_BAUOBJEKTROLLE, NUTZT_MATERIAL, HAT_MATCHINGQUALITAET, GEHÖRT_ZU, etc.) | ~0 | ~250 | +250 |
| Project-level vocab edges (Plan 1 Phase 8 restored + extended) | ~10 | ~150 | +140 |

Roughly **+400 high-value graph edges** over Plan 2-as-written, all targeting central vocabulary hubs (the user's stated goal).

---

## §Z — Live validation results (2026-05-20)

[pre_flight_validation.cypher](pre_flight_validation.cypher) ran cleanly: 40 blocks parsed, 0 errors, results in [pre_flight_results.json](pre_flight_results.json). Live state at validation time: **2298 nodes / 17035 rels**, matching expected (S1 ✓).

### Confirmed (no change needed)

| ID | Finding | Live result |
|---|---|---|
| **C1-C5** | `HAT_SOFTWARE`, `HAT_TOOL`, `HAT_NORM`, `HAT_BAUAUFGABE`, `HAT_AKZEPTANZ`, `HAT_AUFBEREITUNGSVERFAHREN`, `HAT_PRUEFUNG_NACHWEIS`, `HAT_PRUEFUNGNACHWEIS`, `LIEFERT_MATERIAL_AUS`, `VERBUNDEN_MIT`, `LIEGT_IN` all absent | S3: All 11 confirmed absent ✓ |
| **C6** | `HAT_ZUSTANDSKLASSE` is NEW (first use) | S2: confirmed missing — declare as intentional schema extension in rollback |
| **C8/C9** | Receiving + donor Bauwerk nodes don't exist | (not directly checked but no `bw_circl_pavilion_amsterdam` etc. in S26's Projekt scope; safe to create) |
| **C15** | Multiple Stadt nodes need creation | S21: missing — `stadt_amsterdam`, `stadt_duebendorf`, `stadt_liverpool`, `stadt_bordeaux`, `stadt_fribourg`, `stadt_merignac`, `stadt_ingersheim`, `stadt_weil_am_rhein`, `stadt_dundee`, `stadt_canterbury`, `stadt_esch_sur_alzette`, `stadt_coimbra`, `stadt_stuttgart`, `stadt_wien`. Already present: stadt_basel, stadt_berlin, stadt_bruessel, stadt_eindhoven, stadt_paris, stadt_utrecht, stadt_winterthur, stadt_zuerich, stadt_brussel_anderlecht (use this for FCRBE's Anderlecht). |
| **F11** | Land Ukraine missing | S22: confirmed; `land_portugal`, `land_italien` also missing. `land_luxemburg` already exists ✓ |
| **F26** | Aliases UNION mandatory for `p_lysp8_basel` and `p_eth_circular_construction_student_reuse` | S36: confirmed (live aliases shown) |
| **O11** | `TEIL_VON_KETTE` is the live BG→Kette rel | S33: 210 existing rels confirm |
| **O11** | Bauwerk→Kette rels use `AUS_BAUWERK` (donor) + `EINGEBAUT_IN` (receiver) | S34: 14+14 rels confirm. Phase 7 should emit these BW-to-K edges too |
| All 23 target Projekte exist | S26 ✓ | |
| `r.id` integrity perfect | S38: 0 rows ✓ | |
| BELEGT_IN regression check perfect | S39: 0 rows ✓ | |

### Overrides — these CORRECTIONS entries were WRONG

| ID | Original claim | Live result | Action |
|---|---|---|---|
| **C10** | "Plan 2's `wk_*` prefix conflicts with `k_*`" | **S32: wk_* dominates (44 nodes) vs k_* (19 nodes)** | **REVERT** — use `wk_*` for new ketten (matches majority). Update PLAN_v2 Phase 7 ids back to `wk_*`. |
| **C13** | "`av_holzaufbereitung`, `av_remanufacturing`, `av_reinigung`, `av_rekonditionierung`, `av_qualitaetssicherung`, `av_entmoertelung_von_fliesen` are invented Plan 1 ids" | **S6: All 6 EXIST in the live graph (along with the Phase D children)** | **WITHDRAW** — Plan 1's Aufbereitungsverfahren ids are correct. No remediation needed. |
| **F8/F10** | "`land_luxemburg` is a NEW Land" | S22: already exists ✓ | No creation needed |

### Newly-discovered issues from live data

| ID | Finding | Action |
|---|---|---|
| **Z1** | `bt_belag` ABSENT (S10) | Rewrite all `bg_*_belag_*` ids in PLAN_v2 + actor_extraction to use `_boden_` slot. ~15 BG ids affected. |
| **Z2** | `norm_sia_schweiz` ABSENT (S25) | Plan 1 + PLAN_v2 reference this for SMS / UMAR / ELEMENTA. Either create as new Norm (`norm_sia_269`, `norm_sia_500`, `norm_sia_261` are the actual SIA-family standards) or drop the rel. **Recommendation:** create new Norm nodes per actual SIA standard (e.g. `norm_sia_269` for existing structures, `norm_sia_500` for accessibility) rather than the conflated `norm_sia_schweiz`. Or omit Norm linkage for SMS/UMAR/ELEMENTA until verified. |
| **Z3** | `software_opalis` ABSENT (S23) | Create as new Software node in Phase 2 (already in PLAN_v2; confirmed) |
| **Z4** | `norm_bs_5385_5_2009` ABSENT (S25) | Create in Phase 2 (already in PLAN_v2; confirmed) |
| **Z5** | `tool_retile`, `tool_rcmi` ABSENT (S24) | Create in Phase 2 (confirmed) |
| **Z6** | `software_ecotool`, `software_llmnt`, `software_refair` all ABSENT (S23) | Create in Phase 2 (confirmed) |
| **Z7** | **`prog_fcrbe` ALREADY EXISTS as Programm node** (S20) | PLAN_v2 Phase 1d "relabel p_fcrbe → prog_fcrbe" is **wrong** — both nodes exist. **Action:** `merge_node p_fcrbe → prog_fcrbe` (the Programm node is canonical; the Projekt is the duplicate). Same pattern needed for `p_interreg_nwe_fcrbe → prog_interreg_nwe` (both exist; see S20). |
| **Z8** | **`prog_reallabor_be_ware` ALREADY EXISTS as Programm node** (S20) | PLAN_v2 Phase 4d "promote `p_reallabor_be_ware` to full_projekt" should instead **merge into existing `prog_reallabor_be_ware` Programm**. PARKED_DECISIONS suggested PROMOTE but live state has TWO nodes for the same thing. |
| **Z9** | **Werner Sobek duplicate: `Werner_Sobek` has MORE rels (13) than `werner_sobek_p` (10)** (S28) | Plan 1 P0-A picked `werner_sobek_p` as canonical, but the higher-degree node is `Werner_Sobek`. Two options: (a) follow Plan 1, merge `Werner_Sobek → werner_sobek_p` (lose 3 rels by deduplication risk); (b) reverse direction, merge `werner_sobek_p → Werner_Sobek` (preserves all 13 rels of the higher-degree node). **Recommendation:** option (b) — merge `werner_sobek_p → Werner_Sobek`. `merge_node` redirects all rels; merge favors higher-degree node. |
| **Z10** | **Rotor fragmentation deeper than Plan 1 P0-C/STUB_AKTEUR_DECISIONS captured** (S29) | Five Rotor-family nodes: `Rotor` (deg 33), `rotordc` (deg 20), `rotor_dc` (deg 8 — has aliases), `rotor_asbl_vzw` (deg 6), `rotor_vzw` (deg 1). **STUB_AKTEUR_DECISIONS proposed `rotor_vzw → rotor_asbl_vzw`** — but `Rotor` (high-deg) is the obvious canonical. **Recommendation for PLAN_v2 Phase 1b:** (i) `merge_node rotor_vzw → Rotor` (not rotor_asbl_vzw — Rotor has 33 rels), (ii) `merge_node rotor_asbl_vzw → Rotor` (consolidate cooperative ids), (iii) `merge_node rotor_dc → rotordc` (RotorDC platform consolidation; preserve aliases via UNION). Flag for user before applying. |
| **Z11** | `Stadt stadt_brussel_anderlecht` already exists (S21) | Use this id for FCRBE's Anderlecht reference; don't create `stadt_anderlecht`. |
| **Z12** | Already-existing Persons saved | S27 confirms 74 of 86 expected actors PRESENT. Saves ~62 `add_node` ops in Phase 5. Truly NEW (12): `abn_amro`, `bam`, `bam_bouw_techniek`, `big_bundesimmobilien`, `la_fab`, `la_fabrique_de_bordeaux_metropole`, `meduni_wien`, `tu_delft`, `university_of_fribourg` (the others are alt-spelling aliases). PLUS the dossier-specific persons not in S27's check list (will need Phase 5 enumeration). |
| **Z13** | `software_concular` exists (S23) but Plan 2 didn't explicitly reuse it | Concular as a software/tool — use `software_concular` for Concular SaaS references; `concular` Akteur for the company. |
| **Z14** | All 30 Norm ids start with `norm_*` (S25) | Confirms C11. `norm_sia_schweiz` Plan 1 used does NOT exist — see Z2. |

### Updated PLAN_v2 actions

Based on §Z above, the following PLAN_v2 amendments are required:

1. **Phase 1b** — extend Rotor merge cleanup (Z10). Recommend asking user before applying.
2. **Phase 1c** — Werner Sobek direction (Z9). Recommend asking user.
3. **Phase 1d** — `p_fcrbe → prog_fcrbe` MERGE (not relabel; Z7). Same for `p_interreg_nwe_fcrbe → prog_interreg_nwe` (existing Programm).
4. **Phase 4d** — `p_reallabor_be_ware → prog_reallabor_be_ware` MERGE (Z8).
5. **Phase 7** — revert ket id prefix to `wk_*` (Z-C10 override).
6. **Phase 2** — drop `norm_sia_schweiz` references; either create proper SIA-* norms or omit (Z2).
7. **All BG ids** — rewrite `_belag_` → `_boden_` slot (Z1).
8. **Phase 5** — actor creation list shrinks: only 12 confirmed-truly-new orgs + dossier-specific persons. Update [actor_extraction_per_dossier.md](actor_extraction_per_dossier.md) per-dossier "Existing actors" sections.

---

**End of CORRECTIONS_2026-05-20.md.**
