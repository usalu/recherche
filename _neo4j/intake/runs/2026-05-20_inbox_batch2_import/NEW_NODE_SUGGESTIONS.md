# New node suggestions

**Context:** While writing Phases 10-15, the dossiers surfaced concepts that don't have a matching live vocab node. This file lists each gap with rationale, dossier evidence, and a recommended new node definition. Live IDs were verified via [pre_flight_validation.cypher](pre_flight_validation.cypher) sections S2-S25.

**Rule applied:** the user said *"connect to existing structure and taxonomy when possible; if not suggest a new node."* For every dossier value that didn't fit an existing vocab ID, this doc proposes a new node rather than fabricating a fit.

---

## A. Material nodes (Material label)

Live `mat_*` ids (19): mat_aluminium, mat_beton, mat_bitumen, mat_daemmstoff, mat_faserzement, mat_glas, mat_gusseisen, mat_holz, mat_keramik, mat_kunststoff, mat_lehm, mat_mdf, mat_naturstein, mat_recyclingbeton, mat_stahl, mat_stahlbeton, mat_stroh, mat_textil, mat_ziegel.

### A1 — `mat_messing` (brass)
**Evidence:** UMAR dossier (batch 1.md §2) — *Jules Wabbes door handles* are documented as brass (Belgian Wabbes-era handles, salvaged from Brussels Générale de Banque HQ via Rotor).
**Why needed:** Brass differs from steel, aluminium, gusseisen. No existing mat_* fits.
**Proposed:**
```jsonl
{"op":"add_node","id":"mat_messing","labels":["Material"],"properties":{"id":"mat_messing","name":"Messing","name_full":"Messing — Kupfer-Zink-Legierung (Tür-/Möbelbeschläge, oft historische Werte)","source_scope":"controlled_vocab_seed"}}
```
**Materialgruppe link (after add):** `mat_messing -[HAT_MATERIALGRUPPE]-> mg_metall`.

### A2 — `mat_kupfer` (copper)
**Evidence:** UMAR dossier — copper facade elements alongside aluminium.
**Why needed:** Copper is a distinct material with high salvage value.
**Proposed:**
```jsonl
{"op":"add_node","id":"mat_kupfer","labels":["Material"],"properties":{"id":"mat_kupfer","name":"Kupfer","name_full":"Kupfer (Fassade, Bedachung, Sanitärinstallation)","source_scope":"controlled_vocab_seed"}}
```
**Materialgruppe link:** `mat_kupfer -[HAT_MATERIALGRUPPE]-> mg_metall`.

### A3 — `mat_holz_clt` (CLT / Brettsperrholz)
**Evidence:** Stuttgart 210 dossier — "twelve reused geometrically complex solid timber formwork elements" from S21; UMAR has timber + CLT references; LysP8 explicitly states "CLT slabs".
**Why needed:** CLT (Brettsperrholz) is a structurally distinct engineered timber product; using mat_holz loses the engineering distinction.
**Proposed:**
```jsonl
{"op":"add_node","id":"mat_holz_clt","labels":["Material"],"properties":{"id":"mat_holz_clt","name":"CLT / Brettsperrholz","name_full":"Cross-Laminated Timber / Brettsperrholz — kreuzweise verleimtes Massivholzpaneel","source_scope":"controlled_vocab_seed"}}
```
**Materialgruppe link:** `mat_holz_clt -[HAT_MATERIALGRUPPE]-> mg_holz_biobasiert`.

### A4 — `mat_holz_larche` (larch)
**Evidence:** Circl dossier — "fully demountable locally sourced larch timber support structure".
**Why needed:** Species-specific timber matters for durability/decisions. But possibly overkill — could use mat_holz + property `holzart: "Lärche"`.
**Decision:** **Skip the new node**. Use property on the BG: `holzart_text: "Lärche (lokal)"` instead. Less ontological churn.

### A5 — `mat_pcm_phasenwechsel`
**Evidence:** Circl dossier — "tile floors with recycled concrete and PCM to regulate indoor climate".
**Why needed:** Phase-change materials are a distinct functional class (thermal storage).
**Proposed:**
```jsonl
{"op":"add_node","id":"mat_pcm_phasenwechsel","labels":["Material"],"properties":{"id":"mat_pcm_phasenwechsel","name":"PCM","name_full":"Phase Change Material — Phasenwechselmaterial für thermische Speicherung","source_scope":"controlled_vocab_seed"}}
```
**Materialgruppe link:** `mat_pcm_phasenwechsel -[HAT_MATERIALGRUPPE]-> mg_verbundstoff` (best fit; PCM is typically embedded in a matrix).

---

## B. Norm nodes (Norm label)

Live `norm_*` IDs include EN 206, EN 1090, EN 1992, EN 1995, EN 1996, EN 13162, EN 14081, EN 15804, EN 15978, DIN 4074, DIN 18008, DIN 18940, DIN 68800, ISO 14040, ISO 14044, ISO 20887, NEN 8700, NS 3682, CEN/TS 1090-201:2024, CEN/TS 17440, BS 5385-5:2009 (added in Phase 2), SIA 261/269/500 (added in Phase 2).

### B1 — `norm_sia_416` (Swiss building data standard)
**Evidence:** LysP8 dossier S2 (Swiss Arc page): *"building data nach SIA 416"*.
**Why needed:** SIA 416 is the canonical Swiss building-data standard (Geschossfläche, Volumen, Nutzfläche). Used everywhere in CH dossiers.
**Proposed:**
```jsonl
{"op":"add_node","id":"norm_sia_416","labels":["Norm"],"properties":{"id":"norm_sia_416","name":"SIA 416","name_full":"SIA 416 — Kennzahlen für Grundstücke und Gebäude (Schweiz)","source_scope":"controlled_vocab_seed"}}
```

### B2 — `norm_sia_380_1` (Swiss energy/thermal)
**Evidence:** Implicit in all Swiss reuse projects with thermal performance discussion (LysP8, UMAR, ELEMENTA).
**Why needed:** SIA 380/1 is the Swiss energy standard; complements SIA 261 (actions) + SIA 269 (existing structures).
**Proposed:**
```jsonl
{"op":"add_node","id":"norm_sia_380_1","labels":["Norm"],"properties":{"id":"norm_sia_380_1","name":"SIA 380/1","name_full":"SIA 380/1 — Heizwärmebedarf (Schweiz)","source_scope":"controlled_vocab_seed"}}
```

### B3 — `norm_nta_8085_clt_reuse` (Dutch CLT/wood reuse)
**Evidence:** Circl dossier — uses `bps_nta_8713` (already exists) for NL reuse standard. NTA 8085 (Dutch wood-reuse standard) may also be relevant if specifically cited; defer until verified.
**Decision:** **Skip until confirmed in a future dossier.**

---

## C. Akzeptanz nodes (Akzeptanz label)

Live `ak_*` IDs (5): ak_aesthetik_patinakultur, ak_breeam_zertifizierung, ak_dgnb_zertifizierung, ak_leed_zertifizierung, ak_oeffentlicher_bauherr_pilot.

### C1 — `ak_oeffentliche_sichtbarkeit_lernort` (public-engagement / knowledge-sharing venue)
**Evidence:** Circl dossier — "public restaurant, rooftop bar, exhibition space, lectures, and meeting venue"; Granby Workshop — "products held in V&A and Crafts Council permanent collections" (ak_aesthetik_patinakultur covers the aesthetic angle but not the *teaching/public-visibility* angle).
**Why needed:** Circl was explicitly a *Vorzeigeprojekt* with public-engagement function. The existing 5 ak_* values don't capture this.
**Proposed:**
```jsonl
{"op":"add_node","id":"ak_oeffentliche_sichtbarkeit_lernort","labels":["Akzeptanz"],"properties":{"id":"ak_oeffentliche_sichtbarkeit_lernort","name":"Sichtbarkeit / Lernort","name_full":"Öffentliche Sichtbarkeit + Lernort — Akzeptanzgewinn durch Pavillon-/Schaufenster-/Workshop-Funktion","scope_note":"Reuse-Projekt wird zum öffentlich zugänglichen Lern-, Demonstrations- und Veranstaltungsort. Stärkt soziale Akzeptanz unabhängig von Zertifizierung.","source_scope":"controlled_vocab_seed"}}
```
**Use:** Add `HAT_DOMINANT_AKZEPTANZ` edges from `p_circl_abn_amro`, `p_granby_workshop` (alongside existing `ak_aesthetik_patinakultur`), and ETH demonstrators to this node.

### C2 — `ak_humanitarian_purpose` (humanitarian / social purpose)
**Evidence:** RE-USE Höfe Windows-for-Ukraine — *"non-profit humanitarian window-reuse"*; BauKarussell explicit social-enterprise mission (long-term-unemployed employment).
**Why needed:** Distinct from "öffentlicher Bauherr pilot" — these are humanitarian-mission acceptance drivers.
**Proposed:**
```jsonl
{"op":"add_node","id":"ak_humanitarian_purpose","labels":["Akzeptanz"],"properties":{"id":"ak_humanitarian_purpose","name":"Humanitärer Zweck","name_full":"Humanitärer/Sozialer Zweck — Akzeptanzgewinn durch Mission jenseits ökonomischer/ökologischer Argumente (Soziale Beschäftigung, humanitäre Wiederverwendung, Sozialwohnungsbau)","scope_note":"Akzeptanztreiber: Projekt verfolgt explizit humanitäre oder sozialarbeiterische Mission, die isolierte Wirtschaftlichkeitsdebatte überschreibt.","source_scope":"controlled_vocab_seed"}}
```
**Use:** RE-USE Höfe, BauKarussell-mediated MedUni, Granby (CIC + Four Streets housing).

---

## D. Funktionswechsel nodes (Funktionswechsel label)

Live `fw_*` IDs (6): fw_dekorative_funktion, fw_gleiche_funktion, fw_konstruktive_funktion, fw_neue_funktion, fw_technische_funktion, fw_unbekannt.

### Existing coverage check
For the Funktionswechsel cases in Phase 6b (window-frame→floor, jeans→insulation, doors→cladding, business-clothing→felt, formwork→CLT structure, bricks/slates→terrazzo):
- "window frame → floor" → `fw_neue_funktion` ✓
- "jeans → ceiling insulation" → `fw_neue_funktion` ✓
- "doors → wall cladding" → `fw_neue_funktion` ✓
- "clothing → wall felt" → `fw_neue_funktion` ✓
- "formwork → CLT structure" → `fw_konstruktive_funktion` (was construction aid, now structural — closer fit than "neue Funktion")
- "bricks/slates → terrazzo aggregate" → `fw_neue_funktion` ✓

No new Funktionswechsel nodes needed — existing 6 are sufficient. **However:** Plan_v2 Phase 6b wires `HAT_MATCHINGQUALITAET → mq_spec_zweckaenderung` (MatchingQualitaet hub) but NOT `HAT_FUNKTIONSWECHSEL → fw_*`. Both rel types should be wired for fully redundant typing. Suggested follow-up: add `HAT_FUNKTIONSWECHSEL` edges to the 7 FW cases. (Edge type `HAT_FUNKTIONSWECHSEL` may not exist yet — verify via S2 of pre-flight before live apply.)

---

## E. Programm nodes (already created in Phase 2 / 1d-2 / 1d / new)

No further suggestions needed beyond what's already in batch2 v2:
- prog_be_circular, prog_prec, prog_abn_amro_mission_2030, prog_mas_dfab, prog_holzbau_offensive_bw, prog_urban_bricolage, prog_stuttgart_210, prog_rebridge, prog_re_use_hoefe, prog_nest_empa, prog_stiftung_pwg (11 new).

**Possible future additions** (not blocking):
- `prog_granby_four_streets` — Granby Four Streets neighbourhood regeneration context (Liverpool 8). Currently mentioned only in passing in Granby dossier; not yet a verified standalone programme.

---

## F. Region label (entirely new schema label)

**Context:** Brussels-Capital Region appears as a Region/Land-level actor; Nouvelle-Aquitaine (REFAIR dossier) similarly. Currently `brussels_capital_region` is Akteur, `Nouvelle-Aquitaine` is unused (no Akteur or Stadt yet).

**Question:** Introduce a `Region` label (sub-Land, super-Stadt)?

**Pros:**
- Cleaner hierarchical geography (Land → Region → Stadt).
- Matches French/Belgian/German administrative structures.

**Cons:**
- New label requires schema migration + Stadt/Land relationship adjustments.
- ~3 dossiers would benefit; many more don't need it.

**Recommendation:** **Defer**. Keep Brussels-Capital Region as Akteur (currently `client_pub` / `at_oeffentliche_institution`). Add `Nouvelle-Aquitaine` as Akteur in future batch if it gains rel density. Revisit when ≥10 region-level entities accumulate.

---

## G. Bauteiltyp `bt_belag` (already flagged in CORRECTIONS Z1)

**Status:** S10 confirmed `bt_belag` ABSENT. Phase 6a/6b/12 patches use `bt_boden` instead for all "Belag" slots (tiles, terrazzo, etc.).

**Question:** Introduce `bt_belag` (distinct from `bt_boden` for floor *surface* vs floor *structure*)?

**Pros:**
- Distinguishes Bodenbelag (surface treatment: tiles, terrazzo, carpet, linoleum) from Boden (structural floor: CLT, RC slab).
- Matches German construction taxonomy.

**Cons:**
- ~20+ existing BGs use `bt_boden` for both today; introducing `bt_belag` would create label drift.

**Recommendation:** **Defer**. Keep `bt_boden` as canonical for both. Add a property `belag_oder_tragend: "belag" | "tragend"` if disambiguation needed at BG level.

---

## H. Apply-tool / schema extensions (cross-cut)

### H1 — `HAT_FUNKTIONSWECHSEL` rel type
**Status:** Likely doesn't exist (S2 only checked the rels Plan v2 uses; Funktionswechsel rel wasn't checked). The 6 `fw_*` nodes in graph need a rel pointing to them — likely missing, since Phase G used `HAT_MATCHINGQUALITAET` instead.
**Verification needed:** `MATCH ()-[r]->(:Funktionswechsel) RETURN type(r), count(*)`.
**Decision pending:** if no rel type points to Funktionswechsel, introduce `HAT_FUNKTIONSWECHSEL` for the 7 FW BGs.

### H2 — `HAT_BAUOBJEKTROLLE` for Programms?
**Status:** Currently this rel type only targets Bauwerk per `GRAPH_SCHEMA.md:453`. Programms don't carry bauobjektrolle (they're not buildings).
**Decision:** No change needed.

---

## I. Summary table

| Category | New nodes recommended | Total |
|---|---|---:|
| Material | mat_messing, mat_kupfer, mat_holz_clt, mat_pcm_phasenwechsel | 4 |
| Norm | norm_sia_416, norm_sia_380_1 | 2 |
| Akzeptanz | ak_oeffentliche_sichtbarkeit_lernort, ak_humanitarian_purpose | 2 |
| **Total recommended** | | **8** |

| Category | Skipped (existing fits or speculative) |
|---|---|
| Material mat_holz_larche | use mat_holz + holzart property |
| Norm norm_nta_8085_clt_reuse | not yet verified in dossier evidence |
| Funktionswechsel | existing 6 values sufficient |
| Region label | defer; keep as Akteur for now |
| Bauteiltyp bt_belag | defer; keep bt_boden as canonical |
| HAT_FUNKTIONSWECHSEL rel | needs live verification first |

---

## J. Implementation

If accepted, write a `phase_batch2_v2_16_new_vocab.patch.jsonl` with the 8 add_node ops + their HAT_MATERIALGRUPPE links. Then update Phase 11 / Phase 12 BG-vocab scripts to use these new IDs where applicable:
- `bg_reuse_metall_tuer_umar_wabbes_handles` → add `NUTZT_MATERIAL → mat_messing`
- `bg_reuse_metall_fassade_umar_alu_copper` → add `NUTZT_MATERIAL → mat_kupfer`
- `bg_reuse_holz_mehrere_ingersheim_clt_structure`, `bg_dismantled_holz_mehrere_stuttgart21_donor_stock` → switch `NUTZT_MATERIAL → mat_holz_clt`
- `bg_reuse_mineralisch_boden_circl_pcm_tiles` → add `NUTZT_MATERIAL → mat_pcm_phasenwechsel`
- `p_lysp8_basel`, `p_umar_unit`, `p_elementa_walkeweg` → add `REFERENZIERT_NORM → norm_sia_416`
- `p_circl_abn_amro`, `p_granby_workshop`, `p_eggshell_pavilion`, `p_up_sticks_dundee` → add `HAT_DOMINANT_AKZEPTANZ → ak_oeffentliche_sichtbarkeit_lernort`
- `prog_re_use_hoefe`, `p_meduni_campus_mariannengasse`, `p_granby_workshop` → add `HAT_DOMINANT_AKZEPTANZ → ak_humanitarian_purpose`

**Estimated:** 8 add_nodes + ~15 follow-up edges in Phase 16.

---

**End of NEW_NODE_SUGGESTIONS.md.**
