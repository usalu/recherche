# Phase A Execution Plan — concrete records

**Companion to:** [reuse_schema_proposals.md](reuse_schema_proposals.md)
**Date:** 2026-05-16
**Status:** ready to convert to JSONL patches once you sign off.

This doc lists **every concrete record** for Phase A (P-21 + P-4 + P-5 + P-2). Each section has:
- Pre-flight findings against the live graph
- Revisions surfaced during concrete check
- Exact records to apply (op, id, properties, target)
- Test queries to run before & after
- Open blockers

You can read top-to-bottom and decide line-by-line.

---

## 0. Revisions discovered while drilling down

Concrete pre-flight uncovered five issues that change the plan:

| Issue | Impact | Resolution |
|---|---|---|
| **Brummen Town Hall**, **1 Triton Square**, **Portland Decon Program**, **Gainesville six-house** are NOT in the corpus | 4 of ~20 P-21 quantitative-backfill targets have no project node to attach to | **Drop these 4 projects from P-21**; redirect their data into a follow-up "external comparison data" sidecar doc, not into the graph |
| **`p_crclr_house_impact_hub_berlin` + `p_impact_hub_berlin_crclr_fitout`** are two project nodes for the same building | Quantitative backfill would double-attach | **Stop and merge these two before P-21** (one merge_node op; would also surface in any later round-003 review) |
| **`rb_bauordnungsrecht.usage_countries = ['Finnland']`** is wrong | The current `usage_countries` array reflects *project-usage*, not actual *jurisdiction* | **Flip the model:** GILT_IN_LAND should be seeded from the research legal-regime matrix (every country has Bauordnungsrecht), NOT from project-usage data. Throw out `usage_countries` as the seed and replace with the research matrix |
| **3 new Schadstoff nodes (s_kmf, s_formaldehyd, s_schwermetalle)** must exist before P-5 TYPISCH_BEI_MATERIAL rels can target them | P-5 depends on adding them | **Add Schadstoff nodes first** as Step 0 of Phase A |
| **Country-specific Asbest-ban dates** (DE 1993, NL 1994, FR 1997, BE 1998, UK 2000, US no single date) | A single era boundary at "1993" oversimplifies | **Model two things separately:** (1) Era nodes by broad period (era_vor_1990, era_1990_2000, era_post_2000); (2) `asbest_verbot_jahr` integer property on Land. TYPISCH_BEI_ERA uses generic eras |

---

## Step 0. Pre-Phase A: 3 cleanup ops needed first

```jsonl
{"op":"merge_node","from":"p_impact_hub_berlin_crclr_fitout","to":"p_crclr_house_impact_hub_berlin","reason":"Same project, two stub nodes from intake. Merge before quantitative backfill so P-21 properties don't double-attach.","severity":"MEDIUM"}
{"op":"add_node","id":"s_kmf","labels":["Schadstoff"],"properties":{"id":"s_kmf","name":"KMF — Künstliche Mineralfasern (alte Mineralwolle vor 1996/2000)","scope":"european","standards_body":"DE: TRGS 521","topic":"old_mineral_wool"},"reason":"P-5 dependency: TYPISCH_BEI_MATERIAL rules cite s_kmf. Add node first.","severity":"LOW"}
{"op":"add_node","id":"s_formaldehyd","labels":["Schadstoff"],"properties":{"id":"s_formaldehyd","name":"Formaldehyd (MDF / Spanplatten)","scope":"european","standards_body":"EU REACH","topic":"composite_wood_emissions"},"reason":"P-5 dependency","severity":"LOW"}
{"op":"add_node","id":"s_schwermetalle","labels":["Schadstoff"],"properties":{"id":"s_schwermetalle","name":"Schwermetalle (Pb, Cd, Hg, Cr) in Beschichtungen / Laborbauten","scope":"international","topic":"coating_lacquer_pigment_heavy_metals"},"reason":"P-5 dependency","severity":"LOW"}
```

**Total Step 0:** 1 merge + 3 add_node = 4 ops.

**Test queries (before applying):**
```cypher
// Verify the two CRCLR stubs both exist
MATCH (p:Projekt) WHERE p.id IN ['p_crclr_house_impact_hub_berlin','p_impact_hub_berlin_crclr_fitout']
RETURN p.id, p.name, count{(p)<-[:HAT_BAUTEILGRUPPE]-()} AS bg_count
// Expected: 2 rows; one is the canonical (with most BGs), one is the fitout stub
```

**Test queries (after applying):**
```cypher
// Should be 0 — fitout stub merged in
MATCH (p:Projekt {id:'p_impact_hub_berlin_crclr_fitout'}) RETURN count(p)
// Schadstoff nodes should be 8
MATCH (n:Schadstoff) RETURN count(n)
```

---

## Step 1. P-4: GILT_IN_LAND rel — full record list

Decision per §0: **seed from research legal-regime matrix, not from `usage_countries` property.** That property is observation-of-use, not jurisdiction. Once GILT_IN_LAND is seeded, remove `usage_countries` from the schema (rename to `observed_countries` so the difference is documented).

### Norm GILT_IN_LAND (10 records — narrow, jurisdiction-only)

Norms are country-bound by definition. From research [missing_underused_norm_nodes_reuse_kg.md](../../intake/inbox/research/missing_underused_norm_nodes_reuse_kg.md):

```jsonl
{"op":"add_rel","from":"norm_sci_p427","type":"GILT_IN_LAND","to":"land_vereinigtes_koenigreich","properties":{"id":"r_norm_sci_p427__GILT_IN_LAND__land_vereinigtes_koenigreich","evidence":"BELEGT","source":"SCI P427 is a UK Steel Construction Institute protocol"},"reason":"P-4 seed","severity":"LOW"}
{"op":"add_rel","from":"norm_sci_p440","type":"GILT_IN_LAND","to":"land_vereinigtes_koenigreich","properties":{"id":"r_norm_sci_p440__GILT_IN_LAND__land_vereinigtes_koenigreich","evidence":"BELEGT","source":"SCI P440"},"reason":"P-4 seed","severity":"LOW"}
{"op":"add_rel","from":"norm_tek_norway","type":"GILT_IN_LAND","to":"land_norwegen","properties":{"id":"r_norm_tek_norway__GILT_IN_LAND__land_norwegen","evidence":"BELEGT","source":"Norwegian TEK17 building regulation"},"reason":"P-4 seed","severity":"LOW"}
{"op":"add_rel","from":"norm_ns_3682","type":"GILT_IN_LAND","to":"land_norwegen","properties":{"id":"r_norm_ns_3682__GILT_IN_LAND__land_norwegen","evidence":"BELEGT","source":"Norwegian Standard NS 3682:2022"},"reason":"P-4 seed","severity":"LOW"}
{"op":"add_rel","from":"norm_sia_schweiz","type":"GILT_IN_LAND","to":"land_schweiz","properties":{"id":"r_norm_sia_schweiz__GILT_IN_LAND__land_schweiz","evidence":"BELEGT","source":"SIA = Schweizerischer Ingenieur- und Architektenverein"},"reason":"P-4 seed","severity":"LOW"}
{"op":"add_rel","from":"norm_rt_2012","type":"GILT_IN_LAND","to":"land_frankreich","properties":{"id":"r_norm_rt_2012__GILT_IN_LAND__land_frankreich","evidence":"BELEGT","source":"French RT 2012 thermal regulation"},"reason":"P-4 seed","severity":"LOW"}
{"op":"add_rel","from":"norm_crow_cur_4_2023","type":"GILT_IN_LAND","to":"land_niederlande","properties":{"id":"r_norm_crow_cur_4_2023__GILT_IN_LAND__land_niederlande","evidence":"BELEGT","source":"CROW-CUR is a Dutch standards body"},"reason":"P-4 seed","severity":"LOW"}
{"op":"add_rel","from":"norm_historic_sections_book","type":"GILT_IN_LAND","to":"land_vereinigtes_koenigreich","properties":{"id":"r_norm_historic_sections_book__GILT_IN_LAND__land_vereinigtes_koenigreich","evidence":"BELEGT","source":"UK historical steel sections reference book"},"reason":"P-4 seed","severity":"LOW"}
{"op":"add_rel","from":"norm_en_1090","type":"GILT_IN_LAND","to":"land_eu","properties":{"id":"r_norm_en_1090__GILT_IN_LAND__land_eu","evidence":"BELEGT","source":"EN standard, applies EU-wide"},"reason":"P-4 seed; depends on adding land_eu pseudo-node","severity":"LOW"}
{"op":"add_rel","from":"norm_en_1168","type":"GILT_IN_LAND","to":"land_eu","properties":{"id":"r_norm_en_1168__GILT_IN_LAND__land_eu","evidence":"BELEGT","source":"EN standard, applies EU-wide"},"reason":"P-4 seed","severity":"LOW"}
```

**Blocker discovered:** `land_eu` and `land_international` pseudo-nodes don't exist. We need them to anchor EU-wide / international standards. Add as Step 1a:

```jsonl
{"op":"add_node","id":"land_eu","labels":["Land"],"properties":{"id":"land_eu","name":"Europäische Union (Geltungsbereich)","scope_type":"supranational"},"reason":"Anchor node for EU-wide standards (EN 1090, EN 1168, CPR, etc.)","severity":"LOW"}
{"op":"add_node","id":"land_international","labels":["Land"],"properties":{"id":"land_international","name":"International (ISO / IEC Geltungsbereich)","scope_type":"international"},"reason":"Anchor node for ISO/IEC standards","severity":"LOW"}
{"op":"add_node","id":"land_eea","labels":["Land"],"properties":{"id":"land_eea","name":"Europäischer Wirtschaftsraum (EU+EEA)","scope_type":"supranational"},"reason":"For Norway under EEA-CPR","severity":"LOW"}
```

Note: these are not real countries; they're scope-anchor nodes. The `scope_type` property distinguishes them. If you'd rather model this differently (e.g., a separate `Geltungsbereich` label), say so — flexible.

**Test queries:**
```cypher
// Before: Norm has usage_countries property
MATCH (n:Norm) WHERE n.usage_countries IS NOT NULL RETURN count(n)
// Expected: 9

// After: each above Norm has at least one GILT_IN_LAND
MATCH (n:Norm)-[:GILT_IN_LAND]->(l:Land) RETURN n.id, collect(l.id)
// Expected: 10 rows with the mappings above
```

### RechtlicheBedingung GILT_IN_LAND (more complex — multi-country)

From [bauteilreuse_legal_regime_matrix.md](../../intake/inbox/research/bauteilreuse_legal_regime_matrix.md):

| RechtlicheBedingung | Applies in countries (per research) | Records |
|---|---|---:|
| `rb_bauordnungsrecht` | DE, UK, BE, NL, CH, FR, FI, DK, NO, JP, LU, USA | 12 |
| `rb_zulassung_im_einzelfall` | DE, UK (as "alternative materials"), BE, NL, CH, FR, NO, FI, DK, USA | 10 |
| `rb_ce_ukca_marking_reused_steel` | UK (UKCA), DE (CE/CPR) | 2 |
| `rb_gewaehrleistung` | every corpus country (warranty laws universal) | 12 |
| `rb_produkthaftung` | every corpus country | 12 |
| `rb_vergaberecht` | every corpus country with public procurement | 12 |
| `rb_eu_taxonomie` | EU-only | 1 (land_eu) |
| `rb_grade_ii_listing` | UK only | 1 |
| `rb_boulder_deconstruction_ordinance_8366` | USA (Boulder) only | 1 |

**Total:** ~63 GILT_IN_LAND rels for RB. That's a lot for one phase. **Revision proposal:** seed only the country-specific RBs first (Grade II, Boulder, CE/UKCA), and the universal RBs (Bauordnungsrecht, Gewährleistung, Produkthaftung, Vergaberecht) get a single rel to a new pseudo-node `land_generisch_universal` OR a property `is_universal: true`.

**Recommendation:** add `is_universal: true` as a property on the 4 universal RB nodes, instead of 4 × 12 = 48 rels. Saves rel count and is more honest.

**Final RB rels (15 total):**

```jsonl
# Universal RBs get a property
{"op":"set_node_properties","id":"rb_bauordnungsrecht","properties":{"is_universal":true,"scope_note":"Building approval law applies in every corpus country; specific instruments differ (DE MBO, UK Building Regs, etc.)"},"reason":"P-4: avoid 12 redundant rels","severity":"LOW"}
{"op":"set_node_properties","id":"rb_zulassung_im_einzelfall","properties":{"is_universal":true,"scope_note":"Project-specific approval route. Country-specific instruments (DE ZiE/vBG, UK alt-materials, USA IBC 104.11, NL equivalence, FR ATEx). Each country implements differently."},"reason":"P-4","severity":"LOW"}
{"op":"set_node_properties","id":"rb_gewaehrleistung","properties":{"is_universal":true,"scope_note":"Warranty / Sachmängelhaftung applies universally; decennial liability adds 10-year strong form in FR, BE, LU"},"reason":"P-4","severity":"LOW"}
{"op":"set_node_properties","id":"rb_produkthaftung","properties":{"is_universal":true,"scope_note":"Product liability applies universally; EU has CPR-specific path"},"reason":"P-4","severity":"LOW"}
{"op":"set_node_properties","id":"rb_vergaberecht","properties":{"is_universal":true,"scope_note":"Public procurement law applies universally; EU has GPP plus Taxonomie alignment"},"reason":"P-4","severity":"LOW"}

# Country-specific RBs get GILT_IN_LAND
{"op":"add_rel","from":"rb_ce_ukca_marking_reused_steel","type":"GILT_IN_LAND","to":"land_vereinigtes_koenigreich","properties":{"id":"r_rb_ce_ukca_marking_reused_steel__GILT_IN_LAND__land_vereinigtes_koenigreich","evidence":"BELEGT","source":"UKCA post-Brexit + CE pre-Brexit"},"reason":"P-4","severity":"LOW"}
{"op":"add_rel","from":"rb_ce_ukca_marking_reused_steel","type":"GILT_IN_LAND","to":"land_eu","properties":{"id":"r_rb_ce_ukca_marking_reused_steel__GILT_IN_LAND__land_eu","evidence":"BELEGT","source":"CPR is EU-wide"},"reason":"P-4","severity":"LOW"}
{"op":"add_rel","from":"rb_eu_taxonomie","type":"GILT_IN_LAND","to":"land_eu","properties":{"id":"r_rb_eu_taxonomie__GILT_IN_LAND__land_eu","evidence":"BELEGT","source":"EU regulation"},"reason":"P-4","severity":"LOW"}
{"op":"add_rel","from":"rb_grade_ii_listing","type":"GILT_IN_LAND","to":"land_vereinigtes_koenigreich","properties":{"id":"r_rb_grade_ii_listing__GILT_IN_LAND__land_vereinigtes_koenigreich","evidence":"BELEGT","source":"UK listed-building system"},"reason":"P-4","severity":"LOW"}
{"op":"add_rel","from":"rb_boulder_deconstruction_ordinance_8366","type":"GILT_IN_LAND","to":"land_usa","properties":{"id":"r_rb_boulder_deconstruction_ordinance_8366__GILT_IN_LAND__land_usa","evidence":"BELEGT","source":"Boulder, CO city ordinance"},"reason":"P-4","severity":"LOW"}
```

**Total P-4 records:** 13 Norm rels + 3 pseudo-Land nodes + 5 RB property updates + 5 RB rels = **26 ops**. (Down from 60+ thanks to `is_universal` property optimization.)

**Test queries:**
```cypher
// Universal RBs flagged correctly
MATCH (n:RechtlicheBedingung {is_universal: true}) RETURN n.id
// Expected: 5 nodes

// Country-specific RBs have ≥ 1 GILT_IN_LAND
MATCH (n:RechtlicheBedingung)-[:GILT_IN_LAND]->(l:Land) RETURN n.id, collect(l.id)
// Expected: 4 country-specific RBs, each with 1-2 Land targets
```

---

## Step 2. P-5: Schadstoff TYPISCH_BEI_MATERIAL / _BAUTEILTYP

After Step 0 creates s_kmf, s_formaldehyd, s_schwermetalle, we have 8 Schadstoff nodes total. The matrix below is the **complete TYPISCH_BEI_X seed** from [schadstoff_reuse_knowledge_graph_research.md](../../intake/inbox/research/schadstoff_reuse_knowledge_graph_research.md), with material/Bauteiltyp evidence cited inline.

### TYPISCH_BEI_MATERIAL rules (20 rels)

```jsonl
# s_asbest — fibre cement, sprayed insulation, pipe/sealant
{"op":"add_rel","from":"s_asbest","type":"TYPISCH_BEI_MATERIAL","to":"mat_faserzement","properties":{"id":"r_s_asbest__TYPISCH_BEI_MATERIAL__mat_faserzement","evidence":"INFER","source":"FCRBE hazardous substance guidance: Asbestos primarily in Faserzement / Asbestzement panels and pipes"},"reason":"P-5 domain rule","severity":"LOW"}
{"op":"add_rel","from":"s_asbest","type":"TYPISCH_BEI_MATERIAL","to":"mat_daemmstoff","properties":{"id":"r_s_asbest__TYPISCH_BEI_MATERIAL__mat_daemmstoff","evidence":"INFER","source":"FCRBE: asbestos sprayed coatings and old insulation"},"reason":"P-5 domain rule","severity":"LOW"}
{"op":"add_rel","from":"s_asbest","type":"TYPISCH_BEI_MATERIAL","to":"mat_bitumen","properties":{"id":"r_s_asbest__TYPISCH_BEI_MATERIAL__mat_bitumen","evidence":"INFER","source":"FCRBE: old bitumen layers and gaskets"},"reason":"P-5 domain rule","severity":"LOW"}

# s_kmf — mineral wool
{"op":"add_rel","from":"s_kmf","type":"TYPISCH_BEI_MATERIAL","to":"mat_daemmstoff","properties":{"id":"r_s_kmf__TYPISCH_BEI_MATERIAL__mat_daemmstoff","evidence":"INFER","source":"DE TRGS 521: pre-1996 mineral wool potentially biopersistent"},"reason":"P-5 domain rule","severity":"LOW"}

# s_pak — coal tar, roofing felt, parquet adhesives
{"op":"add_rel","from":"s_pak","type":"TYPISCH_BEI_MATERIAL","to":"mat_bitumen","properties":{"id":"r_s_pak__TYPISCH_BEI_MATERIAL__mat_bitumen","evidence":"INFER","source":"FCRBE: tarred bitumen products and roofing felt are primary PAH carriers"},"reason":"P-5 domain rule","severity":"LOW"}
{"op":"add_rel","from":"s_pak","type":"TYPISCH_BEI_MATERIAL","to":"mat_holz","properties":{"id":"r_s_pak__TYPISCH_BEI_MATERIAL__mat_holz","evidence":"INFER","source":"FCRBE: creosote-treated timber (pier, railway, industrial timber)"},"reason":"P-5 domain rule","severity":"LOW"}

# s_pcb — sealants on prestressed/precast concrete, glazing putty, paints
{"op":"add_rel","from":"s_pcb","type":"TYPISCH_BEI_MATERIAL","to":"mat_stahlbeton","properties":{"id":"r_s_pcb__TYPISCH_BEI_MATERIAL__mat_stahlbeton","evidence":"INFER","source":"FCRBE / US EPA: elastic sealants in joints of precast concrete elements (1950–1980)"},"reason":"P-5 domain rule","severity":"LOW"}
{"op":"add_rel","from":"s_pcb","type":"TYPISCH_BEI_MATERIAL","to":"mat_kunststoff","properties":{"id":"r_s_pcb__TYPISCH_BEI_MATERIAL__mat_kunststoff","evidence":"INFER","source":"FCRBE: PCB in elastic sealants/glazing compounds"},"reason":"P-5 domain rule","severity":"LOW"}

# s_holzschutzmittel — pretreated exterior/structural timber
{"op":"add_rel","from":"s_holzschutzmittel","type":"TYPISCH_BEI_MATERIAL","to":"mat_holz","properties":{"id":"r_s_holzschutzmittel__TYPISCH_BEI_MATERIAL__mat_holz","evidence":"INFER","source":"FCRBE: PCP, Lindan, CCA salts in pretreated structural/exterior timber"},"reason":"P-5 domain rule","severity":"LOW"}

# s_bleifarbe — painted timber, painted steel, painted aluminium, painted concrete trim
{"op":"add_rel","from":"s_bleifarbe","type":"TYPISCH_BEI_MATERIAL","to":"mat_holz","properties":{"id":"r_s_bleifarbe__TYPISCH_BEI_MATERIAL__mat_holz","evidence":"INFER","source":"FCRBE: lead-paint coatings on painted timber joinery (windows, doors)"},"reason":"P-5 domain rule","severity":"LOW"}
{"op":"add_rel","from":"s_bleifarbe","type":"TYPISCH_BEI_MATERIAL","to":"mat_stahl","properties":{"id":"r_s_bleifarbe__TYPISCH_BEI_MATERIAL__mat_stahl","evidence":"INFER","source":"FCRBE: lead paint on old steel (railings, radiators, structural steel)"},"reason":"P-5 domain rule","severity":"LOW"}
{"op":"add_rel","from":"s_bleifarbe","type":"TYPISCH_BEI_MATERIAL","to":"mat_aluminium","properties":{"id":"r_s_bleifarbe__TYPISCH_BEI_MATERIAL__mat_aluminium","evidence":"INFER","source":"FCRBE: lead/chromate primers on aluminium"},"reason":"P-5 domain rule","severity":"LOW"}

# s_formaldehyd — engineered wood products
{"op":"add_rel","from":"s_formaldehyd","type":"TYPISCH_BEI_MATERIAL","to":"mat_mdf","properties":{"id":"r_s_formaldehyd__TYPISCH_BEI_MATERIAL__mat_mdf","evidence":"INFER","source":"UBA: formaldehyde in MDF / chipboard / OSB before emission tightening"},"reason":"P-5 domain rule","severity":"LOW"}
{"op":"add_rel","from":"s_formaldehyd","type":"TYPISCH_BEI_MATERIAL","to":"mat_holz","properties":{"id":"r_s_formaldehyd__TYPISCH_BEI_MATERIAL__mat_holz","evidence":"INFER","source":"UBA: urea-formaldehyde-bonded engineered timber"},"reason":"P-5 domain rule (engineered timber subset)","severity":"LOW"}

# s_schwermetalle — coatings, lacquers, galvanized surfaces, old paint
{"op":"add_rel","from":"s_schwermetalle","type":"TYPISCH_BEI_MATERIAL","to":"mat_stahl","properties":{"id":"r_s_schwermetalle__TYPISCH_BEI_MATERIAL__mat_stahl","evidence":"INFER","source":"Swiss pollutant guidance: Pb/Cr/Cd/Zn in old coatings on steel"},"reason":"P-5 domain rule","severity":"LOW"}
{"op":"add_rel","from":"s_schwermetalle","type":"TYPISCH_BEI_MATERIAL","to":"mat_holz","properties":{"id":"r_s_schwermetalle__TYPISCH_BEI_MATERIAL__mat_holz","evidence":"INFER","source":"FCRBE: lead/chromate paints on painted timber"},"reason":"P-5 domain rule","severity":"LOW"}
{"op":"add_rel","from":"s_schwermetalle","type":"TYPISCH_BEI_MATERIAL","to":"mat_aluminium","properties":{"id":"r_s_schwermetalle__TYPISCH_BEI_MATERIAL__mat_aluminium","evidence":"INFER","source":"FCRBE: chromate conversion coatings on aluminium"},"reason":"P-5 domain rule","severity":"LOW"}
{"op":"add_rel","from":"s_schwermetalle","type":"TYPISCH_BEI_MATERIAL","to":"mat_keramik","properties":{"id":"r_s_schwermetalle__TYPISCH_BEI_MATERIAL__mat_keramik","evidence":"INFER","source":"FCRBE: heavy metals in old ceramic tile glazes"},"reason":"P-5 domain rule","severity":"LOW"}
```

### TYPISCH_BEI_BAUTEILTYP rules (10 rels)

```jsonl
# s_asbest by Bauteiltyp
{"op":"add_rel","from":"s_asbest","type":"TYPISCH_BEI_BAUTEILTYP","to":"bt_dach","properties":{"id":"r_s_asbest__TYPISCH_BEI_BAUTEILTYP__bt_dach","evidence":"INFER","source":"Asbestos roofing tiles and gutters"},"reason":"P-5 domain rule","severity":"LOW"}
{"op":"add_rel","from":"s_asbest","type":"TYPISCH_BEI_BAUTEILTYP","to":"bt_daemmung","properties":{"id":"r_s_asbest__TYPISCH_BEI_BAUTEILTYP__bt_daemmung","evidence":"INFER","source":"Sprayed asbestos insulation, pipe lagging"},"reason":"P-5 domain rule","severity":"LOW"}

# s_pcb by Bauteiltyp
{"op":"add_rel","from":"s_pcb","type":"TYPISCH_BEI_BAUTEILTYP","to":"bt_fenster","properties":{"id":"r_s_pcb__TYPISCH_BEI_BAUTEILTYP__bt_fenster","evidence":"INFER","source":"PCB-bearing glazing putty / window sealants pre-1989"},"reason":"P-5 domain rule","severity":"LOW"}
{"op":"add_rel","from":"s_pcb","type":"TYPISCH_BEI_BAUTEILTYP","to":"bt_fassade","properties":{"id":"r_s_pcb__TYPISCH_BEI_BAUTEILTYP__bt_fassade","evidence":"INFER","source":"PCB sealants in curtain-wall facade joints"},"reason":"P-5 domain rule","severity":"LOW"}

# s_pak by Bauteiltyp
{"op":"add_rel","from":"s_pak","type":"TYPISCH_BEI_BAUTEILTYP","to":"bt_dach","properties":{"id":"r_s_pak__TYPISCH_BEI_BAUTEILTYP__bt_dach","evidence":"INFER","source":"Tar/bitumen roof membranes"},"reason":"P-5 domain rule","severity":"LOW"}
{"op":"add_rel","from":"s_pak","type":"TYPISCH_BEI_BAUTEILTYP","to":"bt_boden","properties":{"id":"r_s_pak__TYPISCH_BEI_BAUTEILTYP__bt_boden","evidence":"INFER","source":"Old parquet adhesives pre-1970"},"reason":"P-5 domain rule","severity":"LOW"}
{"op":"add_rel","from":"s_pak","type":"TYPISCH_BEI_BAUTEILTYP","to":"bt_fundament","properties":{"id":"r_s_pak__TYPISCH_BEI_BAUTEILTYP__bt_fundament","evidence":"INFER","source":"Tar-based foundation waterproofing"},"reason":"P-5 domain rule","severity":"LOW"}

# s_bleifarbe by Bauteiltyp
{"op":"add_rel","from":"s_bleifarbe","type":"TYPISCH_BEI_BAUTEILTYP","to":"bt_fenster","properties":{"id":"r_s_bleifarbe__TYPISCH_BEI_BAUTEILTYP__bt_fenster","evidence":"INFER","source":"Painted timber/metal window frames"},"reason":"P-5 domain rule","severity":"LOW"}
{"op":"add_rel","from":"s_bleifarbe","type":"TYPISCH_BEI_BAUTEILTYP","to":"bt_tuer","properties":{"id":"r_s_bleifarbe__TYPISCH_BEI_BAUTEILTYP__bt_tuer","evidence":"INFER","source":"Painted door joinery"},"reason":"P-5 domain rule","severity":"LOW"}
{"op":"add_rel","from":"s_bleifarbe","type":"TYPISCH_BEI_BAUTEILTYP","to":"bt_traeger","properties":{"id":"r_s_bleifarbe__TYPISCH_BEI_BAUTEILTYP__bt_traeger","evidence":"INFER","source":"Painted structural steel beams"},"reason":"P-5 domain rule","severity":"LOW"}
```

**Total P-5 records:** 18 TYPISCH_BEI_MATERIAL + 10 TYPISCH_BEI_BAUTEILTYP = **28 ops**.

**Risk-screening query enabled after this lands:**
```cypher
// For each reused BG, what pollutants should be screened?
MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)<-[:TYPISCH_BEI_MATERIAL]-(s:Schadstoff)
WHERE NOT (bg)-[:HAT_PRUEFUNG]->(:PruefungNachweis {id: 'pr_schadstoffscreening'})
RETURN bg.id, m.name AS material, collect(DISTINCT s.name) AS pollutants_to_screen
ORDER BY size(pollutants_to_screen) DESC
LIMIT 25
```
Expected: every BG using mat_holz returns Holzschutzmittel + Bleifarbe + Formaldehyd + Schwermetalle + PAK (if creosote-treated). Every mat_daemmstoff BG returns KMF + Asbest. Etc.

---

## Step 3. P-2: BauwerkEra nodes + country-specific Asbest-Verbot

### Era nodes (6 nodes)

Era boundaries follow major regulatory inflection points common across Europe:

```jsonl
{"op":"add_node","id":"era_vor_1900","labels":["BauwerkEra"],"properties":{"id":"era_vor_1900","name":"vor 1900","year_from":null,"year_to":1899,"notes":"Pre-industrial / Wilhelmine. PAK from coal tar high; lime mortars; structural variance very high."},"reason":"P-2 seed","severity":"LOW"}
{"op":"add_node","id":"era_1900_1945","labels":["BauwerkEra"],"properties":{"id":"era_1900_1945","name":"1900–1945","year_from":1900,"year_to":1945,"notes":"Industrialisation; reinforced concrete commercialised; PAK still high; some early asbestos products."},"reason":"P-2 seed","severity":"LOW"}
{"op":"add_node","id":"era_nachkrieg_1945_1970","labels":["BauwerkEra"],"properties":{"id":"era_nachkrieg_1945_1970","name":"Nachkrieg 1945–1970","year_from":1945,"year_to":1970,"notes":"Wiederaufbau / Wirtschaftswunder. Highest asbestos use; PCB sealants begin; mineral wool widely installed."},"reason":"P-2 seed","severity":"LOW"}
{"op":"add_node","id":"era_1970_1990","labels":["BauwerkEra"],"properties":{"id":"era_1970_1990","name":"1970–1990","year_from":1970,"year_to":1990,"notes":"Still high asbestos / PCB / KMF; energy crisis drives insulation upgrades; first heavy-metal restrictions."},"reason":"P-2 seed","severity":"LOW"}
{"op":"add_node","id":"era_1990_2000","labels":["BauwerkEra"],"properties":{"id":"era_1990_2000","name":"1990–2000","year_from":1990,"year_to":2000,"notes":"Country-specific asbestos bans (DE 1993, NL 1994, FR 1997, BE 1998, UK 2000); KMF biopersistence rules tighten."},"reason":"P-2 seed","severity":"LOW"}
{"op":"add_node","id":"era_post_2000","labels":["BauwerkEra"],"properties":{"id":"era_post_2000","name":"nach 2000","year_from":2000,"year_to":null,"notes":"Modern. Asbestos banned across EU/EEA; tight formaldehyde emission limits."},"reason":"P-2 seed","severity":"LOW"}
```

### Country-specific Asbest-Verbot property on Land (12 set_node_properties)

```jsonl
{"op":"set_node_properties","id":"land_deutschland","properties":{"asbest_verbot_jahr":1993,"kmf_grenzwert_jahr":1996,"pcb_verbot_jahr":1989},"reason":"P-2 country asbestos-ban dates from research","severity":"LOW"}
{"op":"set_node_properties","id":"land_niederlande","properties":{"asbest_verbot_jahr":1994,"pcb_verbot_jahr":1985},"reason":"P-2","severity":"LOW"}
{"op":"set_node_properties","id":"land_frankreich","properties":{"asbest_verbot_jahr":1997,"pcb_verbot_jahr":1987},"reason":"P-2","severity":"LOW"}
{"op":"set_node_properties","id":"land_belgien","properties":{"asbest_verbot_jahr":1998,"pcb_verbot_jahr":1986},"reason":"P-2","severity":"LOW"}
{"op":"set_node_properties","id":"land_vereinigtes_koenigreich","properties":{"asbest_verbot_jahr":2000,"pcb_verbot_jahr":1986},"reason":"P-2","severity":"LOW"}
{"op":"set_node_properties","id":"land_schweiz","properties":{"asbest_verbot_jahr":1990,"pcb_verbot_jahr":1986},"reason":"P-2","severity":"LOW"}
{"op":"set_node_properties","id":"land_norwegen","properties":{"asbest_verbot_jahr":1980,"pcb_verbot_jahr":1980},"reason":"P-2","severity":"LOW"}
{"op":"set_node_properties","id":"land_daenemark","properties":{"asbest_verbot_jahr":1986,"pcb_verbot_jahr":1986},"reason":"P-2","severity":"LOW"}
{"op":"set_node_properties","id":"land_finnland","properties":{"asbest_verbot_jahr":1994,"pcb_verbot_jahr":1990},"reason":"P-2","severity":"LOW"}
{"op":"set_node_properties","id":"land_usa","properties":{"asbest_verbot_jahr":null,"asbest_neshap_year":1973,"pcb_verbot_jahr":1979,"asbest_note":"No federal ban; NESHAP demolition/renovation inspection rules apply from 1973"},"reason":"P-2","severity":"LOW"}
{"op":"set_node_properties","id":"land_japan","properties":{"asbest_verbot_jahr":2004,"pcb_verbot_jahr":1974},"reason":"P-2","severity":"LOW"}
{"op":"set_node_properties","id":"land_luxemburg","properties":{"asbest_verbot_jahr":2002,"pcb_verbot_jahr":1986},"reason":"P-2","severity":"LOW"}
```

### TYPISCH_BEI_ERA rules — Schadstoff × Era (15 rels)

```jsonl
{"op":"add_rel","from":"s_asbest","type":"TYPISCH_BEI_ERA","to":"era_1900_1945","properties":{"id":"r_s_asbest__TYPISCH_BEI_ERA__era_1900_1945","evidence":"INFER","source":"Early asbestos cement products"},"reason":"P-2","severity":"LOW"}
{"op":"add_rel","from":"s_asbest","type":"TYPISCH_BEI_ERA","to":"era_nachkrieg_1945_1970","properties":{"id":"r_s_asbest__TYPISCH_BEI_ERA__era_nachkrieg_1945_1970","evidence":"INFER","source":"Peak asbestos use"},"reason":"P-2","severity":"LOW"}
{"op":"add_rel","from":"s_asbest","type":"TYPISCH_BEI_ERA","to":"era_1970_1990","properties":{"id":"r_s_asbest__TYPISCH_BEI_ERA__era_1970_1990","evidence":"INFER","source":"Still high; bans not yet"},"reason":"P-2","severity":"LOW"}

{"op":"add_rel","from":"s_pcb","type":"TYPISCH_BEI_ERA","to":"era_nachkrieg_1945_1970","properties":{"id":"r_s_pcb__TYPISCH_BEI_ERA__era_nachkrieg_1945_1970","evidence":"INFER","source":"Most PCB-containing sealants installed 1955–1980"},"reason":"P-2","severity":"LOW"}
{"op":"add_rel","from":"s_pcb","type":"TYPISCH_BEI_ERA","to":"era_1970_1990","properties":{"id":"r_s_pcb__TYPISCH_BEI_ERA__era_1970_1990","evidence":"INFER","source":"Pre-ban PCB"},"reason":"P-2","severity":"LOW"}

{"op":"add_rel","from":"s_pak","type":"TYPISCH_BEI_ERA","to":"era_vor_1900","properties":{"id":"r_s_pak__TYPISCH_BEI_ERA__era_vor_1900","evidence":"INFER","source":"Coal-tar products dominant"},"reason":"P-2","severity":"LOW"}
{"op":"add_rel","from":"s_pak","type":"TYPISCH_BEI_ERA","to":"era_1900_1945","properties":{"id":"r_s_pak__TYPISCH_BEI_ERA__era_1900_1945","evidence":"INFER","source":"Continued coal-tar use"},"reason":"P-2","severity":"LOW"}
{"op":"add_rel","from":"s_pak","type":"TYPISCH_BEI_ERA","to":"era_nachkrieg_1945_1970","properties":{"id":"r_s_pak__TYPISCH_BEI_ERA__era_nachkrieg_1945_1970","evidence":"INFER","source":"Tar parquet adhesives and roofing"},"reason":"P-2","severity":"LOW"}

{"op":"add_rel","from":"s_kmf","type":"TYPISCH_BEI_ERA","to":"era_1970_1990","properties":{"id":"r_s_kmf__TYPISCH_BEI_ERA__era_1970_1990","evidence":"INFER","source":"Pre-1996 biopersistent mineral wool"},"reason":"P-2","severity":"LOW"}
{"op":"add_rel","from":"s_kmf","type":"TYPISCH_BEI_ERA","to":"era_1990_2000","properties":{"id":"r_s_kmf__TYPISCH_BEI_ERA__era_1990_2000","evidence":"INFER","source":"Pre-ban old mineral wool persists"},"reason":"P-2","severity":"LOW"}

{"op":"add_rel","from":"s_holzschutzmittel","type":"TYPISCH_BEI_ERA","to":"era_nachkrieg_1945_1970","properties":{"id":"r_s_holzschutzmittel__TYPISCH_BEI_ERA__era_nachkrieg_1945_1970","evidence":"INFER","source":"PCP, Lindan, CCA pretreatment peak"},"reason":"P-2","severity":"LOW"}
{"op":"add_rel","from":"s_holzschutzmittel","type":"TYPISCH_BEI_ERA","to":"era_1970_1990","properties":{"id":"r_s_holzschutzmittel__TYPISCH_BEI_ERA__era_1970_1990","evidence":"INFER","source":"Continued use pre-bans (1989)"},"reason":"P-2","severity":"LOW"}

{"op":"add_rel","from":"s_bleifarbe","type":"TYPISCH_BEI_ERA","to":"era_vor_1900","properties":{"id":"r_s_bleifarbe__TYPISCH_BEI_ERA__era_vor_1900","evidence":"INFER","source":"Pure lead-paint era"},"reason":"P-2","severity":"LOW"}
{"op":"add_rel","from":"s_bleifarbe","type":"TYPISCH_BEI_ERA","to":"era_1900_1945","properties":{"id":"r_s_bleifarbe__TYPISCH_BEI_ERA__era_1900_1945","evidence":"INFER","source":"Pre-1949 (FR), pre-1948 (BE), pre-1978 (US) — see Land.lead_paint_ban_year"},"reason":"P-2","severity":"LOW"}

{"op":"add_rel","from":"s_formaldehyd","type":"TYPISCH_BEI_ERA","to":"era_nachkrieg_1945_1970","properties":{"id":"r_s_formaldehyd__TYPISCH_BEI_ERA__era_nachkrieg_1945_1970","evidence":"INFER","source":"Early urea-formaldehyde MDF/chipboard"},"reason":"P-2","severity":"LOW"}
```

**Total P-2 records:** 6 era nodes + 12 country property updates + 15 TYPISCH_BEI_ERA rels = **33 ops**.

**Test queries:**
```cypher
// Per-country asbestos-ban year visible
MATCH (l:Land) WHERE l.asbest_verbot_jahr IS NOT NULL RETURN l.name, l.asbest_verbot_jahr ORDER BY l.asbest_verbot_jahr
// Expected: 11 countries with years 1980 (NO) → 2004 (JP)

// Risk-screening enabled (combined with P-5):
MATCH (bg:Bauteilgruppe)-[:AUS_BAUWERK]->(bw:Bauwerk)
OPTIONAL MATCH (bw)-[:HAT_ERA]->(era:BauwerkEra)  // empty until round 003 tags donors
MATCH (bg)-[:NUTZT_MATERIAL]->(m:Material)<-[:TYPISCH_BEI_MATERIAL]-(s:Schadstoff)
WHERE era IS NULL OR (s)-[:TYPISCH_BEI_ERA]->(era)
RETURN bg.id AS bg, collect(DISTINCT s.name) AS pollutants_to_consider
```

---

## Step 4. P-21: Project quantitative property backfill (concrete only)

**Revisions per §0:** drop Brummen / 1 Triton / Portland / Gainesville (not in corpus). Drop "Boulder 75% diversion" (Boulder Fire Station 3 is the corpus project; it's not the Boulder Community Hospital that has the 75% target). Drop SUPERLOCAL exact figures (€1376/m²) since they refer to a specific 3D-unit deconstruction, not the project as a whole.

### 16 projects with research-evidenced numbers + their exact `set_node_properties` ops

```jsonl
{"op":"set_node_properties","id":"p_k118_kopfbau_halle_118_winterthur","properties":{"ghg_reduktion_pct_konstruktion":60,"co2_einsparung_t_min":500,"co2_einsparung_t_max":500,"quantitative_quellen_konflikt":true,"quellen_konflikt_note":"ZHAW/IOP states 500 t CO₂, separate source states 500 t primary material; store both as source-specific claims","lca_module_scope":"unclear","property_source":"ZHAW/IOP K.118 case study"},"reason":"P-21 quantitative backfill from research","severity":"LOW"}
{"op":"set_node_properties","id":"p_ka13_kristian_augusts_gate_13_oslo","properties":{"reuse_anteil_pct":80,"ghg_reduktion_pct":70,"bgf_m2":4297,"property_source":"FutureBuilt KA13 page","lca_module_scope":"unclear"},"reason":"P-21","severity":"LOW"}
{"op":"set_node_properties","id":"p_thoravej_29_copenhagen","properties":{"co2_reduktion_pct":88,"material_reuse_anteil_pct":95,"abfall_reduktion_pct":90,"property_source":"DTU via Pihlmann Architects project source; DGNB Gold pre-cert","lca_module_scope":"unclear","quantitative_quellen_konflikt":false},"reason":"P-21","severity":"LOW"}
{"op":"set_node_properties","id":"p_resource_rows_copenhagen","properties":{"co2_reduktion_pct_50y":29,"abfall_eingespart_t":463,"upcycle_anteil_pct":29,"wirtschaftliches_ergebnis":"kostenneutral","property_source":"Lendager Resource Rows page + RIBA reporting","lca_module_scope":"50y_lifecycle"},"reason":"P-21","severity":"LOW"}
{"op":"set_node_properties","id":"p_55_great_suffolk_street_london","properties":{"co2_einsparung_stahl_t":50,"embodied_carbon_a1_a5_kg_per_m2":386,"property_source":"ASBP case study + NLA + project research file","lca_module_scope":"a1_a5","quantitative_quellen_konflikt":false},"reason":"P-21","severity":"LOW"}
{"op":"set_node_properties","id":"p_brent_cross_town_primary_substation_london","properties":{"co2_einsparung_t_min":66,"co2_einsparung_t_max":99.2,"reused_stahl_anteil_pct":45,"co2_reduktion_pct":40,"co2_eingespart_verlust_t":22,"quantitative_quellen_konflikt":true,"quellen_konflikt_note":"Sources disagree on 66 vs 99.2 t CO₂e","property_source":"ASBP + Arup + local research file","lca_module_scope":"unclear"},"reason":"P-21","severity":"LOW"}
{"op":"set_node_properties","id":"p_superlocal_expogebouw_bleijerheide","properties":{"foerderprogramm":"Urban Innovative Actions","property_source":"UIA journal Kerkrade SuperCircular Estate","abfall_reduktion_pct":null,"co2_reduktion_pct":null,"quantitative_quellen_konflikt":false,"note":"Cost figures €1376/m² and €3989/m² refer to specific 3D-unit deconstruction and Type B housing; do not apply to project as a whole"},"reason":"P-21 conservative","severity":"LOW"}
{"op":"set_node_properties","id":"p_boulder_fire_station_3","properties":{"foerderprogramm":null,"local_regulation":"Boulder Deconstruction Ordinance 8366","property_source":"Boulder Fire Station 3 corpus file","note":"75% diversion is a Boulder Community Hospital figure, not this station"},"reason":"P-21 conservative","severity":"LOW"}
{"op":"set_node_properties","id":"p_harmalanranta_a_kruunu_recreate_mini_pilot_tampere","properties":{"foerderprogramm":"Horizon 2020 ReCreate","reused_bauteiltyp":"hollow_core_slabs","property_source":"ReCreate Finnish pilot pages"},"reason":"P-21","severity":"LOW"}
{"op":"set_node_properties","id":"p_liander_alliander_hq_duiven","properties":{"zertifizierung":"BREEAM-NL Outstanding","material_passport":"Madaster","property_source":"Material District + Archello + CityLoops report"},"reason":"P-21","severity":"LOW"}
{"op":"set_node_properties","id":"p_multi_brussels_reuse_in_multi","properties":{"material_passport":"Madaster","first_renovation_madaster_belgium":true,"co2_neutral_office":true,"property_source":"Immobel + Rotor"},"reason":"P-21","severity":"LOW"}
{"op":"set_node_properties","id":"p_europa_building_brussels","properties":{"reclaimed_windows_count":3750,"reclaimed_windows_source":"Demolitions across Europe","property_source":"Architectural Digest + research file","note":"Asbestos removal during 1960s building demolition documented (Council timeline 2007–2008)"},"reason":"P-21","severity":"LOW"}
{"op":"set_node_properties","id":"p_crclr_house_impact_hub_berlin","properties":{"reused_mdf_documented":true,"property_source":"Impact Hub Berlin / CRCLR fitout sources","note":"Black MDF boards explicitly reused as cupboard doors / wall panels"},"reason":"P-21","severity":"LOW"}
{"op":"set_node_properties","id":"p_circle_house_lisbjerg_denmark","properties":{"design_for_disassembly":true,"material_passport":"GXN demonstrator passport","demontagebarkeit_pct":90,"property_source":"GXN PDF + BLOXHUB","note":"Project may be a stub — verify before adding edges"},"reason":"P-21 conservative — Circle House is a stub Projekt","severity":"LOW"}
```

**Open blocker for Step 4:** `p_circle_house` is currently a `cross_reference_stub` Projekt (per the stub list). Setting properties on a stub is technically fine, but it's worth deciding now whether to **promote** Circle House to a full Projekt during this phase. Per the coverage audit ([reuse_knowledge_graph_coverage_audit.md](../../intake/inbox/research/reuse_knowledge_graph_coverage_audit.md)), Circle House is rated "A/B" evidence — promotable. Recommendation: promote it (small node_role change) before setting properties.

```jsonl
{"op":"set_node_properties","id":"p_circle_house","properties":{"node_role":"full_projekt","promoted_at":"2026-05-16","promoted_reason":"Circle House has A/B-evidence case study (GXN/BLOXHUB) and was tagged as stub from registry-only association. Promoted to full Projekt for P-21 quantitative attachment."},"reason":"P-21 prep: promote Circle House from stub","severity":"MEDIUM"}
```

**Total P-21 records:** 14 set_node_properties + 1 stub-promotion = **15 ops**.

**Test queries:**
```cypher
// Before: count projects with any of the new properties
MATCH (p:Projekt) WHERE p.ghg_reduktion_pct IS NOT NULL OR p.reuse_anteil_pct IS NOT NULL OR p.embodied_carbon_a1_a5_kg_per_m2 IS NOT NULL RETURN count(p)
// Expected: ~0

// After: at least 13 projects with property_source set
MATCH (p:Projekt) WHERE p.property_source IS NOT NULL RETURN count(p)
// Expected: 14

// Source-conflict flag visible
MATCH (p:Projekt {quantitative_quellen_konflikt: true}) RETURN p.id, p.quellen_konflikt_note
// Expected: 2 rows (K.118 + Brent Cross)
```

---

## Phase A grand totals

| Step | New nodes | New rels | Node-property writes | Total ops |
|---|---:|---:|---:|---:|
| 0 cleanup (CRCLR merge + 3 Schadstoff) | 3 | merge × 1 | — | 4 |
| 1 P-4 (incl. land_eu/eea/international pseudo-nodes) | 3 | 18 | 5 | 26 |
| 2 P-5 (Schadstoff TYPISCH) | — | 28 | — | 28 |
| 3 P-2 (BauwerkEra + Land properties + TYPISCH_BEI_ERA) | 6 | 15 | 12 | 33 |
| 4 P-21 (project quantitative) | — | — | 15 | 15 |
| **TOTAL** | **12 nodes** | **62 rels** | **32 property writes** | **106 ops** |

---

## Apply order recommendation

The patch can land as **one combined JSONL** with the ops in this exact order (dependencies first):

1. Step 0 cleanup (CRCLR merge first — affects later property writes; then 3 Schadstoff nodes — needed by P-5)
2. Step 1 P-4 pseudo-Land nodes (`land_eu`, `land_eea`, `land_international`) — needed by Norm GILT_IN_LAND
3. Step 1 P-4 Norm GILT_IN_LAND rels
4. Step 1 P-4 RB universal properties + country-specific GILT_IN_LAND rels
5. Step 2 P-5 TYPISCH_BEI_MATERIAL + _BAUTEILTYP rels
6. Step 3 P-2 era nodes
7. Step 3 P-2 Land asbest_verbot_jahr / pcb_verbot_jahr / kmf_grenzwert_jahr properties
8. Step 3 P-2 TYPISCH_BEI_ERA rels
9. Step 4 P-21 Circle House stub→full promotion
10. Step 4 P-21 quantitative property writes (14 projects)

Single JSONL file: `_neo4j/review/round_002_followup/patches/phase_a.patch.jsonl` (106 records).

---

## Pre-apply checklist (you do this before I run the apply)

- [ ] Confirm CRCLR merge target is `p_crclr_house_impact_hub_berlin` (canonical) vs `p_impact_hub_berlin_crclr_fitout` (stub). Both exist; merge direction matters.
- [ ] Confirm 3 new pseudo-Land nodes (`land_eu`, `land_eea`, `land_international`) are acceptable, or substitute with a new `Geltungsbereich` label.
- [ ] Confirm `is_universal: true` property on the 4 universal RBs (Bauordnungsrecht, Gewährleistung, Produkthaftung, Vergaberecht, ZiE) is preferable to creating 4 × 12 = 48 individual GILT_IN_LAND rels.
- [ ] Confirm era boundary choices (1900 / 1945 / 1970 / 1990 / 2000). Belgium asbest-ban (1998) and UK (2000) span the 1990–2000 era as a class — accepted.
- [ ] Confirm Circle House promotion from stub to full Projekt before P-21 properties land.
- [ ] Confirm `quantitative_quellen_konflikt: true` flag on K.118 + Brent Cross is the right modelling.

## Post-apply verification (one combined query)

```cypher
RETURN
  (MATCH (n:Schadstoff) RETURN count(n)) AS schadstoff_count,        // expect 8
  (MATCH ()-[r:TYPISCH_BEI_MATERIAL]->() RETURN count(r)) AS typisch_mat, // expect 18
  (MATCH ()-[r:TYPISCH_BEI_BAUTEILTYP]->() RETURN count(r)) AS typisch_bt, // expect 10
  (MATCH (e:BauwerkEra) RETURN count(e)) AS era_count,                // expect 6
  (MATCH ()-[r:TYPISCH_BEI_ERA]->() RETURN count(r)) AS typisch_era,   // expect 15
  (MATCH ()-[r:GILT_IN_LAND]->() RETURN count(r)) AS gilt_in_land,    // expect 18
  (MATCH (l:Land) WHERE l.asbest_verbot_jahr IS NOT NULL RETURN count(l)) AS land_with_verbot, // expect 11
  (MATCH (p:Projekt) WHERE p.property_source IS NOT NULL RETURN count(p)) AS p21_backfilled  // expect 14
```

---

## Blockers I want you to decide before I generate the JSONL

1. **CRCLR merge direction.** Which is canonical: `p_crclr_house_impact_hub_berlin` (longer name, currently 21 BELEGT_IN refs) or `p_impact_hub_berlin_crclr_fitout`?
2. **Pseudo-Land nodes vs new `Geltungsbereich` label.** Pseudo-Land is faster (no new label, fits existing rel type GILT_IN_LAND), but `Geltungsbereich` is semantically cleaner.
3. **`is_universal: true` vs 48 individual rels** for the 4 universal RBs.
4. **Circle House promotion** — flip stub to full?
5. **Era boundary choices.** Any pushback on 1900 / 1945 / 1970 / 1990 / 2000?

Once these 5 are settled, I'll generate the patch JSONL and dry-run it before any live apply.