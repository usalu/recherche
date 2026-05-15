# Reuse Knowledge Map — round 002 followup

**Date:** 2026-05-15
**Purpose:** For each underused / reuse-relevant vocab label, list every node and what we know about how it relates to actual projects, countries, materials and Bauteiltypen. Three classes of signal:

- `BELEGT` — found in [`_archive/research/gebaeude/<file>.md`](../../../_archive/research/gebaeude/). Safe to add a graph edge.
- `INFER` — reuse-domain knowledge (general). Not project-specific. Useful as metadata or research direction; **not auto-added as a graph edge**.
- `RESEARCH` — concrete prompt for external research / human follow-up.

**Reading rules:** treat each `BELEGT` row as a green-light to add an edge. Treat `INFER` as context for the user's mental model. Treat `RESEARCH` as a question to send to a research agent or look up in the source material later.

## Corpus shape (anchor for everything below)

| Country | Projects |
|---|---:|
| Deutschland | 11 |
| Belgien | 11 |
| Vereinigtes Königreich | 9 |
| Niederlande | 9 |
| Schweiz | 6 |
| Frankreich | 5 |
| USA | 4 |
| Finnland, Dänemark | 3 each |
| Norwegen, Japan, Luxemburg | 1 each |

| Material | Projects using it |
|---|---:|
| Stahl | 46 |
| Holz | 45 |
| Beton | 38 |
| Glas | 29 |
| Stahlbeton | 25 |
| Keramik | 20 |
| Ziegel | 19 |
| Naturstein | 13 |
| Dämmstoff | 13 |
| Aluminium | 10 |
| Kunststoff | 9 |
| Textil, Recyclingbeton | 3 each |
| Gusseisen | 2 |
| Bitumen, MDF, Faserzement, Lehm | 1 each |
| Stroh | 0 (mentioned in 5 files; round 003 to attach at BG level) |

The label sections that follow reference these projects/countries/materials so you can spot-check.

---

## 1. Schadstoff (5 nodes, 1 rel in live graph)

The most underused reuse-relevant vocab. Pollutant detection is mandatory for almost any pre-1990 building deconstruction, so this label is structurally important even when the current data doesn't reflect it.

### Existing nodes

| id | name | live usage | Archive evidence | Action |
|---|---|---:|---|---|
| `s_asbest` | Asbest | 1 (Recyclinghaus Hannover) | **BELEGT — 5 files:** Berlin_Schildow_Pilot_House, Europa_Building_Brussels, Multi_Brussels_Reuse_in_MULTI, Recyclinghaus_Hannover, Superlocal_Expogebouw_Bleijerheide | **Add 4 missing HAT_SCHADSTOFF rels** (Recyclinghaus already exists) |
| `s_bleifarbe` | Bleifarbe | 0 | not directly mentioned | INFER: relevant to pre-1960s painted timber/steel. Pre-1960 candidates in corpus: 55 Great Suffolk Street (1850s railway warehouse), Hastings Pier (1872), Big Dig Building (1900s). RESEARCH: confirm via source archive. |
| `s_holzschutzmittel` | Holzschutzmittel (PCP/Lindan) | 0 | not directly mentioned | INFER: relevant to pre-1989 structural timber (DDR Holzschutzanstriche, Western European Lindan). Candidates: Plattenpalast Berlin, Association House Gröditz/Plauen (DDR-era). RESEARCH: "Were the reused DDR-era timber elements in p_plattenpalast_berlin / Association House Plauen tested for PCP/Lindan?" |
| `s_pak` | PAK (Teerpappe, Parkettkleber) | 0 | template noise (76 files mention "tar" as substring; not real evidence) | INFER: relevant to pre-1970s tar-impregnated roof felt, parquet adhesives. Possible: Big Dig Building, Hastings Pier. RESEARCH: "PAK contamination in roofing tar / Parkettkleber for Big Dig Boston and Hastings Pier reused elements?" |
| `s_pcb` | PCB | 0 | not directly mentioned | INFER: relevant to pre-1980s sealants around windows/curtain-walls and transformer oil. Possible: BedZED, BioPartner 5 donor (Gorlaeus Hochhaus 1960s), CRCLR House Berlin (1960s brewery). RESEARCH: per donor building. |

### Schadstoff gap candidates (not currently in graph)

| id (proposed) | name | live evidence | Action |
|---|---|---|---|
| `s_kmf` | KMF (künstliche Mineralfasern, pre-1996) | **BELEGT — 4 files:** Circular_Pavilion_Paris, ELYS_Kultur_Gewerbehaus_Basel, Grande_Halle_de_Colombelles, Zinneke_Feder_Masui4ever_Brussels (all mention "Mineralwolle") | **Add `s_kmf` node** + 4 HAT_SCHADSTOFF rels. Caveat: not every Mineralwolle is KMF — only pre-1996 EU production. RESEARCH where the file specifies age of insulation. |
| `s_formaldehyd` | Formaldehyd | not directly mentioned | INFER: relevant to old chipboard / Spanplatte (pre-1986 production). Candidates: any project reusing Holzwerkstoff-Platten. RESEARCH per timber-panel reuse case. |
| `s_schwermetalle` | Schwermetalle (Pb, Hg, Cd) | not directly mentioned | INFER: relevant to old paint coatings (Pb) and electrical wiring/lamp ballasts (Hg, Cd). |
| `s_radon` | Radon | not directly mentioned | INFER: site-condition, not material-condition. Not a typical reuse-relevant Schadstoff unless reused stone from radon-rich quarries. Probably skip. |

### Research prompts (Schadstoff)

- *"Which of our 76 reuse projects involves pre-1990 source buildings (donor Bauwerk) and what's the documented pollutant-screening status for each?"*
- *"Which materials in our corpus most commonly carry Schadstoff risk in reuse contexts, by jurisdiction?"*
- *"What national reuse guidelines (DE/CH/AT/NL/UK) mandate Schadstoff testing before a reused element can be sold or re-installed?"*

---

## 2. Norm (16 nodes, 38 rels — sparse coverage)

Norms are the strongest country-bound vocab — every standard belongs to a national or EU body. The graph currently has the right country anchors (`usage_countries` property set on every Norm), but 6 of 16 sit unused.

### Existing-and-used (10 of 16)

| id | name | country anchor | projects | Note |
|---|---|---|---:|---|
| `norm_sci_p427` | SCI P427 protocol | UK | 5 | Used as expected — UK structural steel reuse |
| `norm_sci_p440` | SCI P440 Reuse of Structural Steel | UK | 2 | Same family |
| `norm_tek_norway` | Norwegian TEK | Norwegen | 5 | Norwegian building code |
| `norm_ns_3682` | NS 3682 (hollow-core slab reuse) | Norwegen | 2 | Norwegian reuse-specific |
| `norm_sia_schweiz` | SIA (Schweizer Standards) | Schweiz | 4 | Swiss generic reference |
| `norm_crow_cur_4_2023` | CROW-CUR Guideline 4:2023 | Niederlande, Finnland | 3 | Dutch hollow-core slab reuse |
| `norm_en_1090` | EN 1090 | EU/UK | 2 | Structural steel execution |
| `norm_en_1168` | EN 1168 (hollow-core slabs) | EU | 2 | Precast concrete product spec |
| `norm_historic_sections_book` | Historic Sections Book | UK | 2 | British historical steel tables |
| `norm_rt_2012` | RT 2012 | Frankreich | 1 | French thermal regulation |

### Unused — 6 nodes worth deciding on

| id | name | scope (tagged) | Action recommended |
|---|---|---|---|
| `norm_din_18940` | DIN 18940 | national_DE / building_materials | INFER: keep as seed — German general regulation, not yet referenced. RESEARCH: what does DIN 18940 actually govern? (this id may be wrong — 18940 doesn't match a major reuse standard) |
| `norm_din_en_15804` | DIN EN 15804 | european / EPD | INFER: relevant whenever an EPD is generated for a reused product. Currently 0 rels because our projects don't generate EPDs for reused parts. Keep as seed. |
| `norm_din_en_15978` | DIN EN 15978 | european / LCA | Same logic. Keep as seed. |
| `norm_iso_14040` | ISO 14040 | international / LCA framework | Keep as seed. |
| `norm_iso_14044` | ISO 14044 | international / LCA requirements | Keep as seed. |
| `norm_iso_20887` | ISO 20887 | international / Design for Disassembly | **One live rel** (Resilience La Ferme des Possibles, Frankreich). Add INFER tag: relevant to every Bauteilgruppe with `la_rueckbaubarkeit` (currently 9 BGs). RESEARCH: are those 9 BGs explicit about ISO 20887 in their sources? |

### Norm gap candidates (BELEGT in archive, not yet in graph)

| id (proposed) | name | evidence | Action |
|---|---|---|---|
| `norm_en_206` | EN 206 (Beton-Norm) | **BELEGT — 4 files:** Association_house_Groeditz, Association_house_Plauen, Berlin_Schildow_Pilot_House, Haus_HOS_Mehrfamilienhaus_Muehlhausen | **Add node + 4 REFERENZIERT_NORM rels.** Anchors all reused Beton/Stahlbeton to a real spec. |
| `norm_eurocode_generic` | Eurocode (general) | **BELEGT — 4 files:** Association_house_Groeditz, Association_house_Plauen, Berlin_Schildow_Pilot_House, Haus_HOS_Mehrfamilienhaus_Muehlhausen | INFER: better to split into EN 1992 (concrete), EN 1993 (steel), EN 1995 (timber) since they govern different materials. RESEARCH the source files to figure out which Eurocode part is meant. |
| `norm_nen_8700` | NEN 8700 (Dutch existing-structure assessment) | **BELEGT — 13 files** mention "NEN-" — Dutch standard prefix. RESEARCH which specific NEN (8700? 6700?). | Add node once the specific NEN is identified per project. |
| `norm_bs_en_generic` | BS EN | **BELEGT — 1 file:** Melkinlaituri Helsinki | INFER: probably refers to a British-standardised European norm. RESEARCH which one. |

### Research prompts (Norm)

- *"List the country-specific reuse standards for structural steel reuse in: DE, CH, NL, BE, FR, UK, NO."* — fills SCI gap for non-UK projects.
- *"For each material × country pairing in the corpus (e.g., Holz × Deutschland), what's the dominant standards body and the most-cited norm for reuse?"*
- *"Does the SIA family (Switzerland) have a specific reuse standard for prestressed concrete elements? (relates to potential K118 BGs)"*
- *"What German DIN standard, if any, governs the reuse of structural timber (Bauholz)?"* — likely DIN EN 14081 or DIN 68800; verify.
- *"Does the Belgian region of Wallonia / Brussels-Capital have a reuse-specific protocol?"* (Belgium is our 2nd-largest country in the corpus, 11 projects, but no specifically-Belgian Norm in the graph.)

---

## 3. Rechtliche Bedingung (9 nodes, 12 rels)

Legal/regulatory conditions. Country-bound. Most reuse work in Europe sits between Bauproduktenverordnung (CPR), Gewährleistung, and country-specific approval regimes.

### Existing nodes

| id | name | live usage | Archive evidence | Action |
|---|---|---:|---|---|
| `rb_bauordnungsrecht` | Bauordnungsrecht | 3 | **BELEGT — 29 files** (template-like signal: every German/Swiss/NL file mentions "MBO" or "Bauordnung"). Most useful for **all DE projects** (11) + **CH projects** (6). | RESEARCH: should this be split by country? E.g. `rb_mbo_deutschland`, `rb_kbo_schweiz`. Or kept as umbrella with country tag. |
| `rb_ce_ukca_marking_reused_steel` | CE/UKCA marking for reused steel | 3 | **BELEGT — 2 files:** 55 Great Suffolk Street, Brent Cross Town Primary Substation. Both UK. | INFER: every reused-steel project in EU could in principle reference CE marking ambiguity. Add the 2 BELEGT rels. RESEARCH: which other UK projects? |
| `rb_zulassung_im_einzelfall` | Zustimmung im Einzelfall | 3 | **BELEGT** (template noise — but real concept in DE for structural reuse without standard CE approval) | INFER: applies to most DE structural reuse cases. RESEARCH per-project. |
| `rb_boulder_deconstruction_ordinance_8366` | Boulder Deconstruction Ordinance 8366 | 1 | **BELEGT — 1 file:** Boulder_Fire_Station_3 | already correct; only 1 USA project applies. |
| `rb_grade_ii_listing` | Grade II Listing | 1 | **BELEGT — 2 more files:** Hastings_Pier_Visitor_Centre (UK), Lo_Reninge_Town_Hall_Facade (BE — different legal regime but flagged "denkmalgeschützt") | **Add 2 missing rels**, but be careful — Lo Reninge is Belgian, not UK Grade II. Use a generic `rb_denkmalschutz` instead. |
| `rb_vergaberecht` | Vergaberecht (public procurement) | 1 | **BELEGT — 3 files:** Grande_Halle_de_Colombelles (FR), Recypark_Demets_Anderlecht (BE), Zinneke_Feder_Masui4ever_Brussels (BE) | **Add 2 missing rels.** |
| `rb_eu_taxonomie` | EU-Taxonomie | 0 | not directly mentioned | INFER: relevant to financing/reporting on circular-economy projects. RESEARCH which projects had EU taxonomy reporting obligations. |
| `rb_gewaehrleistung` | Gewährleistung | 0 | template noise | INFER: applies to every reuse-as-construction-product transaction. The reason it's 0-rels is that no project file states this as a Bauteilgruppe-specific constraint — it's universal. RESEARCH: tag at project level instead of BG level. |
| `rb_produkthaftung` | Produkthaftung | 0 | not directly mentioned | INFER: extension of Gewährleistung. Probably absorb into `rb_gewaehrleistung` and treat as one concept. |

### Rechtliche Bedingung gap candidates

| id (proposed) | name | evidence | Action |
|---|---|---|---|
| `rb_denkmalschutz` | Denkmalschutz / Heritage protection | **BELEGT — 6 files:** 55 Great Suffolk Street (UK), Berlin Schildow (DE), BioPartner 5 (NL), Christ Pavilion (DE), Europa Building (BE) + Lo Reninge Town Hall (BE) | **Add as new node** (broader than UK Grade II). 6 rels to add. |
| `rb_materialpass` | Materialpass / Material passport | **BELEGT — 8 files:** 55 Great Suffolk Street, Jeugdkliniek Ithaka, Liander HQ Duiven, Multi Brussels, PLP London HQ + more | **Add new node** (NL leads adoption: Madaster). 8 rels. Note: this could equally live as a `Tool`/`Software` (Madaster, Concular, etc.) — depends on whether the user models the *practice* (pass requirement) vs the *tool* (Madaster). |
| `rb_bauproduktenverordnung_cpr` | Bauproduktenverordnung (CPR / Construction Products Regulation) | possible (1 file: 55 Great Suffolk mentions "CE marking", which is the CPR instrument) | INFER: parent concept of `rb_ce_ukca_marking_reused_steel`. RESEARCH: does the corpus discuss CPR explicitly? |
| `rb_kreislaufwirtschaftsgesetz_krwg` | KrWG / Kreislaufwirtschaftsgesetz | not directly mentioned in archive | INFER: German waste-framework law. Applies to every DE deconstruction. RESEARCH: should be tagged at DE-project level. |
| `rb_dibt_zustimmung` | DIBt-Zustimmung | possibly subsumed in ZiE above | INFER: refine ZiE into specific German regulatory approval paths. |

### Research prompts (Rechtliche Bedingung)

- *"For each project country (DE/CH/NL/BE/UK/FR/DK/SE/NO/IT/AT/USA), list the 2-3 most relevant legal regimes affecting structural-reuse projects: (a) building approval, (b) CE/product-equivalent marking, (c) public-procurement constraints, (d) liability/warranty."*
- *"Which Belgian (Brussels-Capital, Wallonia, Flanders) reuse-specific regulations or pilot programmes apply to public-sector reuse projects?"* — Belgium tied for largest country block (11) but no Belgian-specific RB node.
- *"How does Dutch Materialpass / Madaster reporting interact with the EU Taxonomy disclosure requirement?"*

---

## 4. Leistungsanforderung (12 nodes, 506 rels — heavily used at top, gaps at fire-class codes)

| id | name | live rels | Comment |
|---|---|---:|---|
| `la_dauerhaftigkeit` | Dauerhaftigkeit | 142 | Well-used. |
| `la_tragfaehigkeit` | Tragfähigkeit | 119 | Well-used. |
| `la_brandschutz` | Brandschutz | 94 | Well-used. |
| `la_feuchteschutz`, `la_waermeschutz`, `la_schallschutz` | (Feuchte, Wärme, Schall) | 60/44/28 | Standard envelope-physics performance criteria. |
| `la_rueckbaubarkeit` | Rückbaubarkeit | 9 | **Reuse-essential**. Surprisingly few BGs flag it; likely under-tagged. RESEARCH: which 9 BGs already carry it, what's their typical Bauteiltyp? Are all `vt_reversible_fuegung` (39 rels) BGs also `la_rueckbaubarkeit`? — that's the likely overlap. |
| `la_schadstofffreiheit` | Schadstofffreiheit | 7 | Couples directly with §1 above. Add for every BG where Schadstoff screening passed. |
| `la_feuerwiderstand` | Feuerwiderstand | 3 | Subset of Brandschutz. Keep separate (German practice). |
| `la_f90`, `la_r90`, `la_rei90` | Fire-resistance class codes | 0 | INFER: orphans, kept as seed with country scope. RESEARCH: should these be sub-nodes of `la_brandschutz` via a parent-child rel? Currently no parent rel-type for Leistungsanforderung. |

### Research prompts (Leistungsanforderung)

- *"For each Bauteiltyp in our corpus, which Leistungsanforderungen are mandatory by national code? (e.g. Wand-trennbar → DE: Brandschutz + Schallschutz; CH: SIA 181 for Schall)"*
- *"Is there an overlap between BGs with `la_rueckbaubarkeit=true` and BGs that use `vt_reversible_fuegung`? If yes, that's a sanity-check; if no, it's a tagging gap."*

---

## 5. Verbindungstechnik (8 nodes, 102 rels)

| id | name | live rels | Comment |
|---|---|---:|---|
| `vt_verschraubung` | Verschraubung | 40 | The reusability gold-standard. |
| `vt_reversible_fuegung` | Reversible Fügung (umbrella) | 39 | Concept node — overlaps with `vt_verschraubung`. INFER: consider tagging `vt_verschraubung` as a child of `vt_reversible_fuegung`. |
| `vt_verschweissung` | Verschweißung | 10 | Less reusable. |
| `vt_vermoertelung` | Vermörtelung | 7 | Irreversible — relevant for Naturstein/Ziegel reuse. |
| `vt_klemmverbindung` | Klemmverbindung | 4 | |
| `vt_mauerwerk_ausgleich`, `vt_steckverbindung` | (incidental) | 1 each | |
| `vt_verleimung` | Verleimung | 0 | **BELEGT — 1 file:** CascadeUp London (glulam demonstrator). **Add 1 rel.** RESEARCH: is glulam-reuse-through-debonding documented elsewhere? |

### Verbindungstechnik gap candidates

| id (proposed) | name | evidence | Action |
|---|---|---|---|
| `vt_holzduebel` | Holzdübel / Wooden dowel | **BELEGT — 2 files:** Plattenpalast Berlin, Recyclinghaus Hannover | **Add node + 2 rels.** Dübel-based timber connections are a reuse-prized technique (DE reuse community emphasises this). |
| `vt_nagelung` | Nagelverbindung | not directly mentioned | INFER: typical for old-stock timber, problematic for clean disassembly. RESEARCH per timber reuse case. |

### Research prompt
- *"Catalogue the Verbindungstechnik used in each timber-reuse BG to compute a 'reversibility index' per project."*

---

## 6. Aufbereitungsverfahren (11 nodes, 363 rels)

Most heavy-use nodes are already well-connected. Gap items:

| id | name | live rels | Comment |
|---|---|---:|---|
| `av_drahtglasschneiden` | Drahtglasschneiden | 0 | Specialty for wired-glass. Keep as seed. RESEARCH: any project reusing Drahtglas? |
| `av_sandstrahlen` (proposed) | Sandstrahlen / Sandblasting | not in graph | **BELEGT — 1 file:** BedZED (corrosion protection of reused steel). **Plus** "Korrosionsschutz" appears in 10 files — universal step for reused Stahl. **Add node + initial rel from BedZED.** RESEARCH per-project. |

---

## 7. PruefungNachweis (11 nodes)

| id | name | live rels | Comment |
|---|---|---:|---|
| `pr_zustandsbewertung` | Zustandsbewertung | 150 | Universal step. |
| `pr_eignungspruefung_baulehm` | Eignungsprüfung Baulehm | 0 | **BELEGT — 2 files:** Juch-Areal Recyclingzentrum Zürich, Villa Welpeloo Enschede. **Add 2 rels.** Caveat: these may be testing reused Lehm (relevant) or testing the substrate for something else — RESEARCH the source text. |
| `pr_abbrandbemessung` | Abbrandbemessung | 0 | **BELEGT — 1 file:** CRCLR House Impact Hub Berlin. Add at BG level (round 003 — needs specific BG within CRCLR). |

### PruefungNachweis gap candidates

| id (proposed) | name | evidence | Action |
|---|---|---|---|
| `pr_zerstoerungsfreie_pruefung` | Zerstörungsfreie Prüfung (ZfP / NDT) | **BELEGT — 4 files:** Holbein Gardens London, Impact Hub Berlin CRCLR, Peoples Pavilion Eindhoven, Plattenpalast Berlin | **Add node + 4 rels.** Reuse-essential for structural elements. |

---

## 8. Country × Material crosstab — auto-derived from existing data

Pure aggregation from `(p:Projekt)-[:LIEGT_IN_LAND]->(l:Land)` and `(p)-[:HAT_BAUTEILGRUPPE]->(bg)-[:NUTZT_MATERIAL]->(m:Material)`. Useful for spotting where a country has lots of one-material reuse — those project clusters are where country-specific Norms / Rechtliche Bedingungen are most needed.

| Country | Top materials in its reuse projects |
|---|---|
| Deutschland (11) | Holz, Beton, Stahl, Ziegel, Lehm |
| Belgien (11) | Stahl, Beton, Holz, Naturstein |
| Vereinigtes Königreich (9) | Stahl (dominant — SCI P427/P440 territory), Holz |
| Niederlande (9) | Holz, Stahl, Beton |
| Schweiz (6) | Stahl, Beton, Holz, Naturstein, Lehm (Juch-Areal) |
| Frankreich (5) | Holz, Stahl, Lehm |
| USA (4) | Stahl, Beton, Holz |
| Finnland (3) | Beton (Hollow-core slabs — CROW-CUR / NS 3682) |
| Dänemark (3) | Holz, Beton |
| Norwegen (1) | Beton (Hollow-core slabs) |

**Smart inference targets:**
- Every UK Stahl-reuse BG should reference `norm_sci_p427` and/or `norm_sci_p440` — currently only 5+2 do.
- Every Schweiz reuse BG should reference `norm_sia_schweiz` — currently 4 do, but Schweiz has 6 projects × several BGs each → likely 20+ rels missing. RESEARCH per BG.
- Every Finland/Norwegen hollow-core slab BG should reference `norm_crow_cur_4_2023` / `norm_en_1168` / `norm_ns_3682` together.
- Every DE reuse BG should reference `norm_en_206` if Beton, `norm_din_68800` if Holzschutz applies — RESEARCH if these names actually appear in source files at BG-level granularity.

---

## 9. Concrete add_rel queue (deterministic, ready to apply)

These are direct adds where the archive provides single-file evidence:

```text
# Schadstoff
ADD HAT_SCHADSTOFF: p_berlin_schildow_pilot_house         -> s_asbest
ADD HAT_SCHADSTOFF: p_europa_building_brussels             -> s_asbest
ADD HAT_SCHADSTOFF: p_multi_brussels_reuse_in_multi        -> s_asbest
ADD HAT_SCHADSTOFF: p_superlocal_expogebouw_bleijerheide   -> s_asbest

# Rechtliche Bedingung (Vergaberecht)
ADD HAT_RECHTLICHE_BEDINGUNG: p_recypark_demets_anderlecht -> rb_vergaberecht
ADD HAT_RECHTLICHE_BEDINGUNG: p_zinneke_feder_masui4ever_brussels -> rb_vergaberecht

# Rechtliche Bedingung (CE/UKCA — note: 55 Great Suffolk needs project country = UK to be sound)
ADD HAT_RECHTLICHE_BEDINGUNG: p_55_great_suffolk_street_london -> rb_ce_ukca_marking_reused_steel

# Grade II Listing (already only UK)
ADD HAT_RECHTLICHE_BEDINGUNG: p_hastings_pier_visitor_centre -> rb_grade_ii_listing

# Verbindungstechnik (Verleimung)
ADD HAT_VERBINDUNGSTECHNIK: p_cascadeup_london_secondary_timber_glulam_demonstrator -> vt_verleimung
```

That's **8 deterministic add_rel ops**. Note: most of these attach at Projekt level. Rels like `HAT_SCHADSTOFF` are typically BG-level — but in the absence of BG-specific evidence, project-level is honest because the file flags the schadstoff at project context, not BG-specific.

## 10. New-node queue (deterministic, with first rels)

```text
# Add s_kmf  (Schadstoff)
NEW NODE  s_kmf  "KMF (künstliche Mineralfasern, pre-1996)"  -> Schadstoff
  + 4 rels: Circular_Pavilion_Paris, ELYS_Kultur, Grande_Halle_Colombelles, Zinneke (caveat: confirm pre-1996 age in source)

# Add rb_denkmalschutz  (RechtlicheBedingung)
NEW NODE  rb_denkmalschutz  "Denkmalschutz / Heritage protection"  -> RechtlicheBedingung
  + 6 rels: 55_Great_Suffolk, Berlin_Schildow, BioPartner_5, Christ_Pavilion, Europa_Building, Lo_Reninge

# Add rb_materialpass  (RechtlicheBedingung)
NEW NODE  rb_materialpass  "Materialpass / Material Passport (Madaster, Concular)"
  + 8 rels: 55_Great_Suffolk, Jeugdkliniek_Ithaka, Liander, Multi_Brussels, PLP_London, ... (8 files total)

# Add norm_en_206  (Norm)
NEW NODE  norm_en_206  "EN 206 (Beton-Norm)"
  + 4 rels: Association_house_Groeditz, Association_house_Plauen, Berlin_Schildow, Haus_HOS

# Add vt_holzduebel  (Verbindungstechnik)
NEW NODE  vt_holzduebel  "Holzdübel"
  + 2 rels: Plattenpalast_Berlin, Recyclinghaus_Hannover

# Add av_sandstrahlen  (Aufbereitungsverfahren)
NEW NODE  av_sandstrahlen  "Sandstrahlen (Korrosionsschutz-Vorbereitung)"
  + 1 rel: BedZED_London_Hackbridge (others candidate via Korrosionsschutz mention — RESEARCH)

# Add pr_zerstoerungsfreie_pruefung  (PruefungNachweis)
NEW NODE  pr_zerstoerungsfreie_pruefung  "Zerstörungsfreie Prüfung (ZfP / NDT)"
  + 4 rels: Holbein_Gardens_London, Impact_Hub_Berlin_CRCLR, Peoples_Pavilion_Eindhoven, Plattenpalast_Berlin
```

That's **7 new nodes + 29 first-class rels**, all backed by archive evidence.

---

## 11. Research prompts catalog (for external research agent or human follow-up)

A copy-pasteable set. Each prompt fills a real gap in our graph.

### By country
1. *"For each EU country in our corpus (DE, NL, BE, FR, IT, AT, SE, DK, FI), what's the legal status of reusing structural steel/Beton/Holz under the Construction Products Regulation (CPR / Bauproduktenverordnung)?"*
2. *"What's the difference between Germany's ZiE/vBG path and the equivalent national one-off-approval regime in Switzerland (BAFU/SIA), Netherlands, Belgium, France, Norway?"*
3. *"Belgian region-specific reuse subsidies and rules: list active programmes in Brussels-Capital, Wallonia, Flanders as of 2024 — names, eligibility criteria, references."*
4. *"For Norway and Finland: which standards specifically permit reuse of hollow-core slabs in load-bearing applications, and what testing regime do they prescribe?"*

### By material
5. *"What national tests apply when reusing structural timber in Germany / Switzerland / Austria? (DIN 68800, ÖNORM B 3802, SN 564)"*
6. *"Reuse of Naturstein in heritage buildings — which countries have specific protocols (e.g., MaSta or DGStG in DE; protocols in IT, FR)?"*
7. *"Reuse of Aluminium structural elements — under what circumstances is recertification needed in Europe vs USA?"*
8. *"Bauteilreuse — Brandschutzanforderungen für gebrauchten Stahl in Deutschland: gibt es eine sondergeregelte F-Klassifikation oder muss F90/R90 in jedem Einzelfall durch Brandschutznachweis erbracht werden?"*

### By process
9. *"What documentation must accompany a reused steel beam to make it sellable as a construction product in the EU vs UK post-Brexit?"* (CPR + UKCA gap)
10. *"In which of our 76 source documents is a Materialpass / digital twin / Madaster export mentioned? Which BGs in those projects have machine-readable inventories?"* — partially answered above (8 files).
11. *"For each Aufbereitungsverfahren in our graph, what's the typical pass-rate (% of donor stock that ends up as reused after this step) for: Sandstrahlen + Korrosionsschutz on Stahl; Hobeln + Metalldetektion on Holz; Druckprüfung on Beton-Hollow-Core?"*

### By project
12. *"For each of our 27 stub Projekt nodes (LYSP8 Basel, Stuttgart 210, UMAR Unit, Circle House, Reallabor B(e) Ware, Schärenmoosstrasse Zürich, MedUni Mariannengasse, etc.) — does a primary source document or published case-study exist? If yes, summarise its reuse strategy, donor sources, and any Schadstoff findings."*
13. *"For BedZED's reused structural elements (project_id p_bedzed_london_hackbridge) — were they screened for PCB-bearing sealants given the donor buildings' 1960s-70s vintage?"*
14. *"Plattenpalast Berlin reused DDR-era Plattenbau panels — what was the documented Schadstoff testing for asbestos, PCB, and PCP/Lindan? What national/state-level protocol applies (Berlin Senate / Umweltbundesamt)?"*

---

## 12. Open items parked for #1 and #2 (reminder)

These are deliberately not addressed in this knowledge-map but are still on the worklist:

### #1 parked
- **2 multi-file Akteur** (BELEGT_IN ambiguous): `zirkular_cirkla` (29 files), `zrs_architekten` (2 files). Need per-project disambiguation.
- **15 no-archive-match Akteur** (registry-only, not in building research): bizh, citydev_brussels, dare_gmbh, denkstatt, edith_maryon_stift, eitel_partner, gibbins_architekten, glasfischer_glastec, heinrich_boell_stiftung, koimo_development, kunst_stoffe_ev, mehr_als_wohnen, rotor_vzw, stiftung_habitat, zusammenkunft_berlin. Either accept actor-registry as their only source (recommendation) or hunt them down in non-research material.

### #2 parked
- **24 stub Projekt nodes** awaiting promote-or-drop decision per [belegt_in_coverage_audit.json](belegt_in_coverage_audit.json):
  - Promote candidates: LYSP8 Basel, Stuttgart 210, UMAR Unit, Circle House, Reallabor B(e) Ware, Schärenmoosstrasse, ELEMENTA Walkeweg, MedUni Mariannengasse, OBK 27, Pavilion Circl Amsterdam, RE-USE Höfe, Circl / ABN AMRO, Granby Workshop, Vandkunsten component reuse.
  - Drop candidates: ZHAW research, Architecture of Reuse Brussels, Careno Be.Circular, ETH student reuse, FCRBE, REFAIR Bordeaux platform, Interreg NWE FCRBE, RCMI Concular, REBRIDGE, Reuse Logistics.

---

**Next concrete move:** apply the patch in §9 + §10 (8 add_rel + 7 new_node + 29 first-class rels = 44 ops) once you're happy with the inference choices. The RESEARCH prompts in §11 are best handed to a research agent or you-with-coffee separately.
