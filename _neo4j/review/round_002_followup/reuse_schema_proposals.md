# Reuse Schema Proposals — research-driven changes

**Companion to:** [reuse_knowledge_map.md](reuse_knowledge_map.md)
**Last revised:** 2026-05-16 (after integrating 13 external research files at [_neo4j/intake/inbox/research/](../../intake/inbox/research/))
**Purpose:** Where the previous doc proposed *adding edges and nodes* to the existing schema, this one proposes *structural changes to the schema itself* — new labels, new relationship types, refinements — based on what the reuse-research literature treats as core and what the archive scan actually surfaces.

Each proposal has:
- **Evidence** — archive hits or domain-literature grounding
- **Rationale** — why current schema falls short
- **Schema delta** — exact label/rel/property additions
- **Migration** — how to land the change without breaking existing data
- **Acceptance** — verifiable success criteria

Decisions stay yours. Each section is independent; you can take any subset.

---

## 0. Connection-density priority ranking (revised after research integration)

The user's stated goal: **create nodes with more connections; avoid nodes with very few**. The proposals below are reordered by *expected connection density they generate* once landed, based on the 13 research files at [_neo4j/intake/inbox/research/](../../intake/inbox/research/).

| Tier | Proposal | Why high-density | Expected new edges |
|:---:|---|---|---:|
| 🔥 | **P-15** New label `Bauproduktstatus` (CE / hEN / Ü / abZ / ZiE / project-specific) | Every Projekt + every Bauteilgruppe with a reused product gets exactly one. | ≈ 75 + 306 = **~380** |
| 🔥 | **P-16** New Norm hub `norm_cen_ts_1090_201_2024` + country-specific implementations | Single Norm node attaches to every steel-reuse BG across UK/DE/CH/NL/BE/NO/FI. | **~70+** |
| 🔥 | **P-5** `TYPISCH_BEI_MATERIAL` / `_BAUTEILTYP` / `_ERA` for Schadstoff (was already strong) | One Schadstoff × Material rule creates 10-50 implicit risk-screening edges. | **~50** new rule rels |
| 🔥 | **P-17** Five new PruefungNachweis hubs (NDT, Korrosion, Festigkeitssortierung, Bohrkernpruefung, Dokumentenpruefung) | Each becomes a hub for one material × test combination across the corpus. | **~120+** Bauteilgruppe-level rels |
| 🔥 | **P-2** `BauwerkEra` + `HAT_ERA` + `TYPISCH_BEI_ERA` | Every donor Bauwerk gets one HAT_ERA, every relevant Schadstoff/PruefungNachweis hangs off the era matrix. | **~196 Bauwerk-era + ~30 typisch_bei rels** |
| 🔥 | **P-8** `LebenszyklusModul` (LCA A1-D) + 7 LCA Norm node refinements | Every BG with `co2_einsparung_t` (≈50 projects) anchors to a module + a Norm. | **~50 BG-module + ~12 module-Norm** |
| ⚡ | **P-1** `Defekt` (refined per UBA/SCI taxonomy) | Each reused BG carries 1-3 Defekt rels. | **~300-500** via round 003 |
| ⚡ | **P-6 (refined)** `vt_reversible_fuegung` as PARENT of Verbindungstechnik tree | Restructures existing 102 rels into a navigable tree (degree on parent ≈ 60). | restructure, +parent rels |
| ⚡ | **P-18** Country×Material reuse templates (Steel UK, HCS NO/FI, Lehm DE) | Each template node has every project of that pattern attached. | **~80** template-anchor rels |
| ⚡ | **P-7** `Layer` (Brand's shearing layers) | Every Bauteiltyp gets one parent layer rel (15 rels), but Layer→Bauteilgruppe transitive gives huge query power. | 15 rels, transitive ≈ 306 |
| 🌱 | **P-3** `Marktmodell` | Per-BG, round 003 work. | up to **~150** |
| 🌱 | **P-4** `GILT_IN_LAND` rel (Norm/RechtlicheBedingung → Land) | Direct rel conversion of existing property: ~16 Norm + ~9 RB = ~30 rels initially, but every new Norm/RB adds one. | **~30** initial, grows over time |
| 🌱 | **P-13** `MatchingQualitaet` (Donor-receiver match dimensions) | Per-BG round 003 work. | up to **~600** (3 dimensions × 200 reuse BGs) |
| ⚠ | **P-9** Akzeptanz refinements | Modest gain (refines 7 existing rels). | small |
| ⚠ | **P-10** Wirtschaft tightening | Modest gain. | small |
| ⚠ | **P-11** HuerdeKategorie tidy | Drop hk_unklar; rename. | cleanup |
| ⚠ | **P-12** Beschaffungsweg note | Docs only. | none |
| ⚠ | **P-14** Drop zero-rel orphans | Cleanup. | removes orphan dead-ends |
| ❌ | `vt_holzduebel` (was in §10 of knowledge_map) | **WITHDRAW** — research warns no project evidence supports the term; Recyclinghaus is beech-screws not dowels. |
| ❌ | `vt_verleimung` project edge for CascadeUp | **DOWNGRADE** — research clarifies CascadeUp's "Verleimung" was the glulam *manufacture*, not an assembly Verbindungstechnik. Model as `Herstellungsverfahren: Verleimung` instead. |
| ❌ | `la_f90` / `la_r90` / `la_rei90` as standalone Leistungsanforderung nodes | **DOWNGRADE** — these are fire-resistance *classes*, not requirements. Model as a property `feuerwiderstandsklasse` on the `HAT_LEISTUNGSANFORDERUNG`→`la_brandschutz` rel. Reduces 3 orphans. |
| ❌ | `s_radon` (was in §1 of knowledge_map proposals) | **WITHDRAW** — research confirms radon is a site condition, not a Bauteilreuse pollutant. Not modelled. |

### What "high-density" means in practice for a new node

A proposal is high-density when **the rule of creation guarantees many edges**, not when "round 003 might find some BGs to attach". Concretely:

- **Universal hubs**: One node every project/BG must reference (`Bauproduktstatus`, `LebenszyklusModul` for any LCA-claiming project, `norm_cen_ts_1090_201_2024` for any steel project). High-density by *structural necessity*.
- **Risk-rule matrices**: `Schadstoff × Material × Era` rels. Adding a single rule (`Asbest typical in Faserzement`) implicitly enriches every Faserzement project's risk profile.
- **Parent hubs**: `vt_reversible_fuegung` as parent of `vt_verschraubung`/`vt_klemmverbindung`/etc. The parent has degree = sum of children's degrees.
- **Country×material templates**: A `reuse_pattern_steel_uk` template that every UK steel project links to, plus the template links to SCI P427, CEN/TS 1090-201, lead paint screening, corrosion testing, fire performance, etc.

### What's deliberately downgraded

The research evidence pushed me to be more conservative on some earlier proposals:

- **`mat_stroh` archive_mentions tag** (knowledge_map §10): the term appears in 5 archive files but the research/scan rule is "no Material BG link without explicit `nutztMaterial Stroh` in the source." Kept as proposed seed.
- **Project-level `HAT_SCHADSTOFF` adds (knowledge_map §9)**: 3 of the 5 (`Berlin_Schildow` → `s_asbest`, `Multi_Brussels` → `s_asbest`) lack BG-specific evidence. Demote to `requiresVerificationFor`-style relation (see [graph_patch_validation.md](../../intake/inbox/research/graph_patch_validation.md) §1). Only `Europa Building` and `Superlocal Expogebouw` survive the audit as APPROVE-WITH-CAVEAT.

---

## P-1. New label `Defekt` (= Mängel / BeschädigungsArt)

**Evidence (archive scan):**
- Verformung mentioned in **36 files**
- Korrosion in **33 files**
- Riss in **27 files**
- Hohlraum/Delamination in 1 file
- Schimmel/Holzwurm/Pilzbefall: 0 in archive (but standard in reuse-assessment vocab)

These terms describe *conditions found on donor elements* — central to reuse assessment, yet the current schema has no category for them. They get half-buried in BG `note` properties or `pr_zustandsbewertung` rels without a typology.

**Rationale.** "Was a defect found, and which type?" is the second question (after "what material is it?") that every reuse-feasibility assessment asks. Without a typology you can't aggregate ("show me all reused Stahl-Träger that had Korrosion in our corpus") and can't drive material × era × defect crosstabs that are the basis of risk-rated reuse decisions.

**Schema delta.**

```text
NEW LABEL: Defekt
  id prefix:  def_
  example nodes:
    def_korrosion              "Korrosion"
    def_riss                   "Riss / Rissbildung"
    def_verformung             "Verformung / Setzung"
    def_karbonatisierung       "Karbonatisierung (Beton)"
    def_holzwurm_pilzbefall    "Holzwurm / Pilzbefall"
    def_hohlraum_delamination  "Hohlraum / Delamination"
    def_oberflaechenmangel     "Oberflächenmangel / Verfärbung"
    def_chemische_belastung    "Chemische Belastung (Salze, Säuren)"
    def_brandschaden           "Brandschaden"
    def_keine_befunde          "Keine relevanten Defekte" (positive findings)

NEW REL: HAT_DEFEKT
  domain: Bauteilgruppe  (or Bauwerk for site-level findings)
  range:  Defekt
  optional props: schweregrad (gering/mittel/hoch), aufbereitet_durch (-> Aufbereitungsverfahren)
```

**Migration.** Two-step:
1. Add the seed `Defekt` nodes (≈10).
2. Round 003 attaches `HAT_DEFEKT` to BGs as project content is reviewed. No bulk auto-add — domain detail lives in the source `.md`.

**Acceptance.** Schema patch includes `Defekt` in `kg_jsonl_record_schema.json` allowed labels, `HAT_DEFEKT` in rel types. The query `MATCH (m:Material)<-[:NUTZT_MATERIAL]-(bg:Bauteilgruppe)-[:HAT_DEFEKT]->(d:Defekt) RETURN m.name, d.name, count(bg)` returns a useful crosstab.

---

## P-2. New label `BauwerkEra` (donor-building age)

**Evidence (archive scan):**
- "post 1996" / new-built mentions: 15 files
- "1960er–1980er": 7 files
- "Nachkrieg / 1945–1960": 10 files
- "Vorkrieg / pre-1945": 5 files

Era is the single best **predictor of Schadstoff risk and structural variability** in reuse. Currently buried in Bauwerk `note` or `raw_description`.

**Rationale.** "Pre-1990 donor" is a flag that should auto-route a project into Schadstoff screening protocols. Today the schema can't even ask "show me all reuse cases sourcing from pre-1980 donor buildings" without parsing free text.

**Schema delta.**

```text
NEW LABEL: BauwerkEra
  id prefix:  era_
  example nodes:
    era_vor_1900               "vor 1900"
    era_1900_bis_1945          "1900–1945"
    era_nachkrieg_1945_1960    "Nachkriegszeit (1945–1960)"
    era_wirtschaftswunder_1960_1980  "1960er–1970er"
    era_1980_bis_1996          "1980–1996" (KMF / Asbest cutoff)
    era_post_1996              "nach 1996"

NEW REL: HAT_ERA
  domain: Bauwerk
  range:  BauwerkEra

NEW REL: TYPISCH_BEI_ERA
  domain: Schadstoff
  range:  BauwerkEra
  (Encodes: which pollutants are typical for which era — pure domain knowledge.)
  example: (s_asbest)-[:TYPISCH_BEI_ERA]->(era_1900_bis_1945)
           (s_asbest)-[:TYPISCH_BEI_ERA]->(era_nachkrieg_1945_1960)
           (s_asbest)-[:TYPISCH_BEI_ERA]->(era_wirtschaftswunder_1960_1980)
           (s_pcb)-[:TYPISCH_BEI_ERA]->(era_nachkrieg_1945_1960)
           (s_pcb)-[:TYPISCH_BEI_ERA]->(era_wirtschaftswunder_1960_1980)
           (s_pak)-[:TYPISCH_BEI_ERA]->(era_vor_1900)
           (s_pak)-[:TYPISCH_BEI_ERA]->(era_1900_bis_1945)
           (s_kmf)-[:TYPISCH_BEI_ERA]->(era_1980_bis_1996)
```

Optionally also a property on Bauwerk: `errichtungsjahr_ca` (int).

**Migration.**
1. Seed 6 BauwerkEra nodes.
2. Round 003 tags each donor `Bauwerk` with its era via `HAT_ERA` while reviewing the source `.md`.
3. Add `TYPISCH_BEI_ERA` matrix (one-shot, domain encoding).

**Power that unlocks.** A query like
```cypher
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)-[:AUS_BAUWERK]->(bw:Bauwerk)-[:HAT_ERA]->(era)
MATCH (s:Schadstoff)-[:TYPISCH_BEI_ERA]->(era)
WHERE NOT (bg)-[:HAT_DEFEKT]->() AND NOT (bg)-[:HAT_PRUEFUNG]->(:PruefungNachweis {id: "pr_schadstoffscreening"})
RETURN p.id, bg.id, s.name AS pollutant_to_screen
```
gives you the **risk-screening to-do list** automatically. Currently impossible.

**Acceptance.** Same as P-1, plus the query above returns a non-empty list of action items for actual pre-1996 reuse cases.

---

## P-3. New label `Marktmodell` (= Eigentumsmodell)

**Evidence (archive scan):**
- "Spende / donation": **20 files**
- "Leasing / Mietverhältnis": **6 files**
- "Materialpass" tied to Madaster/Concular: 8 files
- Reused-material platforms (Opalis, Rotor DC, Restado, Concular, Madaster): 13 unique mentions

**Rationale.** Reuse-research literature treats the *commercial model* (who owns the reused part across its second life) as a first-class concern. CE/CPR liability hinges on it. EU Taxonomy reporting hinges on it. Insurance treats Spende-Bauteile differently from Kauf-Bauteile. The current schema has no representation.

**Schema delta.**

```text
NEW LABEL: Marktmodell
  id prefix:  mm_
  example nodes:
    mm_kauf_neu                "Kauf als Bauprodukt (Neuware-äquivalent)"
    mm_kauf_gebraucht          "Kauf als Gebrauchtware"
    mm_spende                  "Spende"
    mm_leasing                 "Leasing / Mietverhältnis"
    mm_rueckkauf               "Rückkauf-Vereinbarung"
    mm_same_site               "Same-site Wiedereinbau (kein Markttransaktion)"
    mm_plattform_vermittelt    "Plattform-vermittelter Kauf (Madaster/Concular/Restado/Rotor DC/Opalis)"

NEW REL: HAT_MARKTMODELL
  domain: Bauteilgruppe  (or Beschaffungsweg)
  range:  Marktmodell
```

**Migration.** Could partially derive from existing `Beschaffungsweg` nodes which already track procurement-path. Consider merging Marktmodell with Beschaffungsweg or making Marktmodell a parent of Beschaffungsweg. Recommendation: **keep Beschaffungsweg as "logistical path" (Lager, Direktabnahme, etc.) and Marktmodell as "commercial structure"** — they're orthogonal axes.

**Acceptance.** All 20 spende-mention BGs and 6 leasing-mention BGs are linked to a Marktmodell. A query "show me all Leasing-based reuse cases" returns the 6.

---

## P-4. New rel `GILT_IN_LAND` for Norm / RechtlicheBedingung

**Evidence.** Country scope is the single most predictive attribute of a Norm or RechtlicheBedingung. Today it's a *property* (`n.usage_countries: ['Vereinigtes Königreich']`) — not a graph rel.

**Rationale.** Properties don't traverse. The query "find German Normen that apply to Beton" has to filter by string property; "find all Normen for projects in Belgium and Frankreich" requires array work. A rel makes both trivial.

**Schema delta.**

```text
NEW REL: GILT_IN_LAND
  domain: Norm | RechtlicheBedingung | Programm
  range:  Land
  (Multi-valued allowed: a Norm can apply in multiple countries.)
  example:
    (norm_sci_p427)-[:GILT_IN_LAND]->(land_vereinigtes_koenigreich)
    (norm_din_18940)-[:GILT_IN_LAND]->(land_deutschland)
    (norm_iso_14040)-[:GILT_IN_LAND]->(land_international)  # may need a "land_international" pseudo-node
```

For `international`/`europe` scope, either add pseudo-Land nodes (`land_international`, `land_eu`) or use a separate `Geltungsbereich` label.

**Migration.** Convert existing `n.usage_countries` property to `GILT_IN_LAND` rels — pure mechanical conversion via Cypher. Drop the array property after.

**Acceptance.** Every Norm with at least one referring project has its `GILT_IN_LAND` rel. Scoped seed Normen (DIN/ISO from §P-1) have explicit `GILT_IN_LAND` to their declared scope.

---

## P-5. New rel `TYPISCH_BEI_MATERIAL` for Schadstoff

**Evidence.** Domain knowledge, not archive-grep. Standard reuse-pre-deconstruction-audit checklists pair Schadstoffe with the materials/Bauteiltypen most likely to harbour them.

**Rationale.** Same as P-2: encode the rule once at schema level so the graph can drive risk screening per project.

**Schema delta.**

```text
NEW REL: TYPISCH_BEI_MATERIAL
  domain: Schadstoff
  range:  Material
  example pairs:
    (s_asbest)-[:TYPISCH_BEI_MATERIAL]->(mat_faserzement)
    (s_asbest)-[:TYPISCH_BEI_MATERIAL]->(mat_daemmstoff)
    (s_kmf)-[:TYPISCH_BEI_MATERIAL]->(mat_daemmstoff)
    (s_pak)-[:TYPISCH_BEI_MATERIAL]->(mat_holz)          # alte Holzschutzanstriche / Parkettkleber
    (s_pak)-[:TYPISCH_BEI_MATERIAL]->(mat_bitumen)        # Teerpappe
    (s_pcb)-[:TYPISCH_BEI_MATERIAL]->(mat_kunststoff)     # Dichtungsmassen
    (s_holzschutzmittel)-[:TYPISCH_BEI_MATERIAL]->(mat_holz)
    (s_bleifarbe)-[:TYPISCH_BEI_MATERIAL]->(mat_stahl)
    (s_bleifarbe)-[:TYPISCH_BEI_MATERIAL]->(mat_holz)

NEW REL: TYPISCH_BEI_BAUTEILTYP
  domain: Schadstoff
  range:  Bauteiltyp
  example pairs:
    (s_pcb)-[:TYPISCH_BEI_BAUTEILTYP]->(bt_fenster)       # Fenstersilikone vor 1989
    (s_pak)-[:TYPISCH_BEI_BAUTEILTYP]->(bt_dach)          # Teerdach
    (s_asbest)-[:TYPISCH_BEI_BAUTEILTYP]->(bt_dach)        # Asbestzement
    (s_holzschutzmittel)-[:TYPISCH_BEI_BAUTEILTYP]->(bt_traeger)
```

Together with P-2 (TYPISCH_BEI_ERA), this gives a 3-way matrix from which the system can derive "for any reuse case, list pollutants worth screening for".

**Migration.** Seed the matrix as a one-shot. About 25–35 rel records, all domain-justified.

**Acceptance.** No new Schadstoff is added without at least one TYPISCH_BEI_MATERIAL or TYPISCH_BEI_BAUTEILTYP or TYPISCH_BEI_ERA rel — the matrix becomes part of the seed contract.

---

## P-6. Refine `Methode` — split into three concept families

**Evidence.** Looking at current `Methode` nodes:
- `meth_form_follows_availability` (132 inbound) — **design method**
- `meth_reuse_assessment` (102) — **assessment workflow**
- `meth_building_material_scouting` (60) — **workflow**
- `meth_bauteilkatalogisierung` (53) — **inventory output / artifact**
- `meth_materialinventur` (48) — **inventory output / artifact**
- `meth_design_for_disassembly` (35) — **design method**
- `meth_reversibilitaet` (31) — **design property**
- `meth_pre_deconstruction_audit` (16) — **workflow** (also surfaced in archive scan)
- `meth_reuse_ausschreibung` (19) — **procurement method**
- `meth_zirkulaere_ausschreibung` (3) — **procurement method**

Three categories mixed into one label. Querying "design methods our projects use" can't separate them from workflows/artifacts.

**Rationale.** A clean split aligns with how the reuse-research community organizes practice: design intent vs. process step vs. produced artefact. The Bauteilkatalog node tree already distinguishes Tool/Software/Programm — Methode should follow.

**Schema delta (option A: split Methode into three labels).**

```text
SPLIT LABEL Methode:
  ENTWURFSMETHODE   (Design method): form_follows_availability, design_for_disassembly,
                                       reversibilitaet, urban_mining (as design concept)
  PROZESSMETHODE   (Process method): reuse_assessment, building_material_scouting,
                                       pre_deconstruction_audit, reuse_ausschreibung,
                                       zirkulaere_ausschreibung, abrissmonitoring
  INVENTARARTEFAKT (Inventory artefact): bauteilkatalogisierung, materialinventur,
                                            wiederverwendungskriterien
```

**Schema delta (option B: keep one label, add a HAT_METHODENKATEGORIE).** Simpler:

```text
NEW NODE LABEL: MethodenKategorie
  id prefix: mk_
  nodes: mk_entwurfsmethode, mk_prozessmethode, mk_inventarartefakt

NEW REL: HAT_METHODENKATEGORIE
  domain: Methode
  range:  MethodenKategorie
```

Option B is **less disruptive** (no rel re-typing). Recommend option B.

**Migration.** Add 3 MethodenKategorie nodes, link all 13 Methode nodes to one of them. No data lost.

**Acceptance.** Query `MATCH (mk:MethodenKategorie)<-[:HAT_METHODENKATEGORIE]-(m:Methode) RETURN mk.name, count(m)` shows 3 buckets summing to 13.

---

## P-7. New label `Layer` — Stewart Brand's shearing layers

**Evidence (archive scan):** explicit mention of layer-vocabulary in **14 files** (Skin/Structure/Services/Space plan/Stuff vocabulary).

**Rationale.** "Layered construction" / "shearing layers" (Stewart Brand, *How Buildings Learn*, 1994) is the canonical reuse-research framework for how building parts have different life-cycles and should be designed to separate. Site lasts forever; Stuff a year. The current graph captures Bauteiltyp (Wand, Decke, Fassade) but not the layer it belongs to. A reuse query "show me all 'Skin' reuses across projects" is currently impossible.

**Schema delta.**

```text
NEW LABEL: Layer (Brand's shearing layers)
  id prefix: layer_
  nodes:
    layer_site           "Site"             (lifespan: forever)
    layer_structure      "Structure"         (~30–300 years)
    layer_skin           "Skin / Fassade"   (~20 years)
    layer_services       "Services / TGA"   (~7–15 years)
    layer_space_plan     "Space plan"       (~3–30 years)
    layer_stuff          "Stuff / Loose Furniture" (~1–5 years)

NEW REL: TEILT_LAYER
  domain: Bauteiltyp (or Bauteilgruppe directly)
  range:  Layer
  Mapping current Bauteiltyp -> Layer:
    bt_fundament   -> layer_site / structure
    bt_traeger, bt_stuetze, bt_decke, bt_wand (if tragend) -> layer_structure
    bt_fassade, bt_dach, bt_fenster -> layer_skin
    bt_technik -> layer_services
    bt_ausbau, bt_tuer (innen), bt_treppe (innen), bt_gelaender -> layer_space_plan
    bt_boden (Bodenbelag) -> layer_space_plan
    bt_daemmung -> layer_structure (Außendämmung) / layer_skin (Vorhangfassade)
```

**Migration.** 6 Layer nodes + 15 TEILT_LAYER rels (one per Bauteiltyp, some Bauteiltyp may need multiple layers).

**Acceptance.** A query "expected lifespan-mismatch on a BG" becomes possible: a reused Stahlträger (Structure layer, ~100 yrs) reinstalled into a Stuff-layer use should raise a flag.

---

## P-8. New label `Lebenszyklus_Modul` — LCA scope

**Evidence (archive scan):**
- `lca:graue_energie` / embodied carbon: **10 files**
- `lca:gwp` / CO2-Einsparung: **63 files** (heavy)
- `lca:epd` / Umweltproduktdeklaration: 1 file
- `lca:modul_d` / Module D: 0 (but doctrine-relevant)

**Rationale.** Every reuse project that publishes CO2 savings is *implicitly* working with EN 15978 Module D (avoided burdens of next life-cycle). When a project says "1.5 t CO2 saved" without naming the LCA module, that number is **not comparable** to another project that includes A1–A3 (production stage) only. The schema can't represent this distinction today.

**Schema delta.**

```text
NEW LABEL: LebenszyklusModul (LCA scope, per EN 15978)
  id prefix: lz_
  nodes:
    lz_a1_a3   "Produkt (A1–A3: Rohstoffe, Transport, Herstellung)"
    lz_a4_a5   "Errichtung (A4 Transport, A5 Bauphase)"
    lz_b       "Nutzung (B1–B7: Erhaltung, Reparatur, Betrieb)"
    lz_c       "End of Life (C1–C4: Rückbau, Transport, Verarbeitung, Deponie)"
    lz_d       "Anrechenbarer Nutzen außerhalb der Systemgrenze (Modul D)"

NEW REL: BERECHNET_NACH_MODUL
  domain: Bauteilgruppe (or Projekt for project-wide totals)
  range:  LebenszyklusModul
  optional props: gwp_kg_co2_aequivalent (Float)

NEW REL: METHODENGRUNDLAGE_NORM
  domain: LebenszyklusModul or Projekt
  range:  Norm
  example: project's LCA methodologically grounded in (norm_din_en_15978), (norm_iso_14044)
```

Then `bg.co2_einsparung_t` (currently a free-form property) can be qualified: "this is Modul D credit", "this is A1–A3 avoided production".

**Migration.** 5 LebenszyklusModul nodes + retroactive tagging of existing `co2_einsparung_t` properties (likely all Modul D for reuse). The DIN_EN_15804/15978/ISO_14040/14044 Normen (currently zero-rel orphans) gain instant usefulness as METHODENGRUNDLAGE_NORM anchors.

**Acceptance.** Every BG with a non-null `co2_einsparung_t` either has `BERECHNET_NACH_MODUL` or is flagged `lca_module_unknown=true`. The 6 zero-rel LCA Normen each get at least one inbound METHODENGRUNDLAGE_NORM.

---

## P-9. New label `Stakeholder_Akzeptanz` (or expand existing Huerde)

**Evidence (archive scan):**
- "Akzeptanz / stakeholder acceptance / Nutzerakzeptanz": **19 files**
- Existing Huerde node `h_akzeptanzproblem` has 7 inbound rels — undercaptures.

**Rationale.** Reuse adoption barriers fall into ~5 well-known stakeholder buckets in the literature: client, designer/architect, contractor, end-user, authority. The current `h_akzeptanzproblem` is too coarse. The reuse-research community has standard typologies (e.g., Adams et al. 2017; Hradil et al. 2014).

**Schema delta (light-touch — refine the Huerde tree).**

```text
NEW HUERDEKATEGORIE-level nodes:
  hk_stakeholder_akzeptanz   "Stakeholder-Akzeptanz" (parent)

NEW HUERDE leaf nodes (children via HAT_HUERDEKATEGORIE):
  h_akzeptanz_bauherr        "Bauherr-/Auftraggeber-Akzeptanz"
  h_akzeptanz_planung        "Planer-/Architekturbüro-Akzeptanz"
  h_akzeptanz_bauausfuehrung "Ausführende-Akzeptanz"
  h_akzeptanz_nutzer         "Nutzer-/Mieter-Akzeptanz"
  h_akzeptanz_behoerde       "Behördliche Akzeptanz"
```

Existing `h_akzeptanzproblem` either becomes the parent or gets retired with `superseded_by`.

**Acceptance.** Refined acceptance Huerde have at least 1 rel each after round 003 (re-tagging via per-project review).

---

## P-10. Tighten `Wirtschaft` — concrete econ-aspect splits

**Evidence.** Current `Wirtschaft` nodes:
- `wi_kostenvergleich` (7) — comparison
- `wi_restwert` (2) — residual value
- `wi_finanzierung` (1) — financing
- `wi_geschaeftsmodell` (1) — business model
- `wi_lebenszykluskosten` (0) — life-cycle cost
- `wi_preisbildung` (0) — price formation

The set conflates *concepts* (Restwert, Lebenszykluskosten) with *methods* (Kostenvergleich, Preisbildung) and *models* (Geschaeftsmodell, Finanzierung).

**Rationale.** Reuse business literature treats these as four distinct axes:
1. Cost components (CapEx, OpEx, EoLCost)
2. Valuation method (LCC, Restwert)
3. Financing structure (loan, leasing, ESG-credit)
4. Business model (one-off, platform, take-back)

Aligning the schema to these four axes makes economic queries answerable.

**Schema delta.**

```text
RENAME/REFINE existing Wirtschaft nodes:
  wi_kostenvergleich        -> wi_kostenmethode_vergleich     (method)
  wi_restwert               -> wi_valuation_restwert          (valuation)
  wi_lebenszykluskosten     -> wi_valuation_lcc               (valuation)
  wi_preisbildung           -> wi_kostenmethode_preisbildung  (method)
  wi_finanzierung           -> wi_finanzierung_klassisch      (financing)
  wi_geschaeftsmodell       -> wi_modell_einmalprojekt        (business model)

ADD new Wirtschaft nodes:
  wi_capex_einsparung       "CapEx-Einsparung durch Reuse"
  wi_modell_plattform       "Plattform-Vermittlungsmodell"
  wi_modell_take_back       "Take-Back-Vereinbarung"
  wi_finanzierung_esg       "ESG/EU-Taxonomie-aligned financing"

OPTIONAL parent: WirtschaftsKategorie
  wk_kostenmethode, wk_valuation, wk_finanzierung, wk_geschaeftsmodell
```

**Migration.** Low risk — only 11 existing rels affected. Use `merge_node` for renames; `add_rel` for new ones via project content review.

---

## P-11. Reshape `HuerdeKategorie` to match research literature

**Evidence.** Current 10 categories include both 7 well-used (Technisch, Daten_Evidenz, Rechtlich, Logistisch, Umwelt_Gesundheit, Wirtschaftlich, Beschaffung_Markt) and 3 sparse (Planerisch=3, Sozial_Organisatorisch=3, Unklar=0).

**Rationale.** Reuse-barrier literature (Hradil et al. 2014; Iacovidou & Purnell 2016; Adams et al. 2017) consistently lists 6 high-level barrier categories:

| Literature category | Current node | Match |
|---|---|---|
| Technical | `hk_technisch` | ✅ |
| Economic | `hk_wirtschaftlich` | ✅ |
| Regulatory / Legal | `hk_rechtlich` | ✅ |
| Logistical | `hk_logistisch` | ✅ |
| Information / Knowledge | `hk_daten_evidenz` | ✅ |
| Cultural / Stakeholder | partly `hk_sozial_organisatorisch`, partly missing | ⚠ |

Plus you have `hk_umwelt_gesundheit` (HSE) and `hk_beschaffung_markt` (Market-supply), which are useful additions but not in the canonical 6.

**Schema delta.** Minor. Keep the 10. But:
- Retire `hk_unklar` (0 rels — never used).
- Possibly rename `hk_sozial_organisatorisch` → `hk_kulturell_akzeptanz` to align with literature terminology.
- The `hk_planerisch` (3 rels) might fold into `hk_technisch` since planning-stage barriers are usually technical-data gaps. RESEARCH needed.

---

## P-12. Document the `Beschaffungsweg ↔ Marktmodell` axis explicitly

(Cross-reference to P-3.)

**Current `Beschaffungsweg` nodes** track *logistical procurement path*: direct from donor, via storage, via platform, via reuse-centre. These are orthogonal to *commercial structure*.

**Schema delta.** Add a `Geltungsdimension` property on Beschaffungsweg distinguishing:
- `logistical_path` (the current intent)
- `commercial_structure` (if any node accidentally captures this — move to new Marktmodell label)

Or simpler: keep Beschaffungsweg as-is and just add Marktmodell (per P-3); the two complement each other.

---

## P-13. Add `Lieferkette` / `Donor-Receiver-Matching` concept

**Evidence (archive scan):**
- "Supply Chain / Lieferkette": **19 files**
- "Zeitliches Matching / Zeitfenster / lead time": 5 files
- "Geografisches Matching" / "lokale Verfügbarkeit": 0 files

**Rationale.** A core reuse-research framework treats donor-receiver match as a 3-axis problem:
- **Temporal** (does the donor stock become available in the time the receiver needs it?)
- **Geographic** (is it close enough that logistics aren't a deal-breaker?)
- **Specification** (does it match the design intent?)

Today the schema treats donor and receiver as endpoints of a single `AUS_BAUWERK` / `EINGEBAUT_IN` pair — without modeling the **matching quality**.

**Schema delta.**

```text
NEW REL: HAT_MATCHING_QUALITAET
  domain: Bauteilgruppe
  range:  MatchingQualitaet (new label)
  nodes:
    mq_temporal_easy     "Temporales Matching unproblematisch"
    mq_temporal_storage  "Temporales Matching durch Zwischenlagerung"
    mq_temporal_planned  "Temporales Matching durch geplante Beschaffung"
    mq_geographic_local  "Lokales geografisches Matching (< 50 km)"
    mq_geographic_regional "Regional (50–500 km)"
    mq_geographic_intl   "International / interkontinental"
    mq_spec_exact        "Exakte Spezifikations-Übereinstimmung"
    mq_spec_anpassung    "Spezifikations-Anpassung nötig"
    mq_spec_zweckaenderung "Zweckänderung (Funktionswechsel)"
```

A BG can carry 3 matching-quality rels (one per axis). Lets you query "all reuse cases where the spec required adaptation" — a key research question.

**Migration.** Round 003 tags per project. The seed of 9 MatchingQualitaet nodes is small.

---

## P-14. Drop or repurpose currently-zero unused vocab nodes

**Evidence.** Vocab nodes with 0 rels after all proposed additions still:

| label | id | recommendation |
|---|---|---|
| HuerdeKategorie | hk_unklar | drop |
| Methode | meth_abrissmonitoring (or attach via P-6 split) | keep with scope tag |
| Aufbereitungsverfahren | av_drahtglasschneiden | keep (specialty) |
| PruefungNachweis | pr_abbrandbemessung | keep (specialty) — attach in round 003 |
| Schadstoff | s_pak, s_pcb, s_bleifarbe, s_holzschutzmittel | keep, anchor via P-2 TYPISCH_BEI_ERA |
| Programm | prog_bbsm, prog_preuse, prog_zukunftbau, prog_kommunales_programm | keep with scope tag |
| Wirtschaft | wi_lebenszykluskosten, wi_preisbildung | repurpose per P-10 |
| Leistungsanforderung | la_f90, la_r90, la_rei90 | **REMOVE** — convert to property `feuerwiderstandsklasse` on `HAT_LEISTUNGSANFORDERUNG` rel pointing at `la_brandschutz` / `la_feuerwiderstand`. (Per research validation in [graph_patch_validation.md](../../intake/inbox/research/graph_patch_validation.md) — these are CLASSES, not requirements.) |

---

## P-15. 🔥 New label `Bauproduktstatus` (CE / hEN / Ü / abZ / ZiE / project-specific)

**Evidence ([bauteilreuse_legal_regime_matrix.md](../../intake/inbox/research/bauteilreuse_legal_regime_matrix.md) + [circular_construction_reuse_graph_gaps.md](../../intake/inbox/research/circular_construction_reuse_graph_gaps.md)).** The single biggest legal-regulatory variable across reuse projects is **which approval route the reused component takes**: CE-marked (under EU CPR), national `Ü`/abZ German conformity mark, project-specific `ZiE`/`vBG`, or "no formal status" (informal site reuse). Every project lives in exactly one of these regimes per reused element class, and that choice cascades to liability, insurance, warranty, and admissible test methods.

**Rationale.** The current `rb_ce_ukca_marking_reused_steel` is too narrow (UK + Steel only). The German DIBt framework explicitly lists **5 distinct approval paths** (`CE_hEN`, `Ü_Zeichen`, `abZ_aBG`, `ZiE_vBG`, `ProjectSpecificEngineerAssessment`). Multiple countries map similar regimes. Without a `Bauproduktstatus` node every project is ambiguous about its regulatory route. Every Projekt OR every reused BG must connect to exactly one — that's **~75 + 306 = ~380 edges from the structural rule alone**.

**Schema delta.**

```text
NEW LABEL: Bauproduktstatus
  id prefix: bps_
  example nodes:
    bps_ce_hen                 "CE-Marking unter harmonisierter EN-Norm (hEN)"
    bps_ce_eta                 "CE-Marking via Europäische Technische Bewertung (ETA)"
    bps_ue_zeichen             "Ü-Zeichen (DE, nationale Konformität)"
    bps_abz_abg                "abZ / aBG (DE, allgemeine bauaufsichtliche Zulassung)"
    bps_zie_vbg                "ZiE / vBG (DE, project-specific approval)"
    bps_ukca                   "UKCA marking (UK, post-Brexit equivalent of CE)"
    bps_baupg_ch               "BauPG-Status (CH, Schweizer Bauprodukteverordnung)"
    bps_pemd_fr                "PEMD-erfasst (FR, diagnostic produit/matériau/déchet)"
    bps_tracimat_be            "Tracimat-zertifiziert (BE, traceable deconstruction)"
    bps_project_specific       "Projektspezifische Ingenieurfreigabe ohne Marktzulassung"
    bps_bestand_no_status      "Bestand vor Ort weiterverwendet (kein neues Inverkehrbringen)"
    bps_unbekannt              "Status unbekannt / nicht dokumentiert"

NEW REL: HAT_BAUPRODUKTSTATUS
  domain: Bauteilgruppe  (preferred — different elements in a project can have different status)
  range:  Bauproduktstatus
  optional secondary domain: Projekt  (when one status is used throughout)
```

**Migration.** Round 003 tags each BG (or project) with its status. For deterministic seed:
- All **same-site reuse** BGs (Resource Rows, Thoravej 29) → `bps_bestand_no_status`
- All **UK CE-marked steel** projects → `bps_ce_hen` (e.g. 55 Great Suffolk Street has documented CE marking via EN 1090)
- All **Belgian projects involving Tracimat or pre-demolition inventories** → `bps_tracimat_be` (Multi Brussels, FCRBE pilot projects)
- All **French projects with PEMD diagnostic** → `bps_pemd_fr` (FR PEMD became mandatory for projects > 1000 m² since 2023)
- All **Boulder Fire Station 3** → `bps_project_specific` (US, no EU-CPR analogue)

**Acceptance.** Every reused BG carries one `HAT_BAUPRODUKTSTATUS` rel (≈ 306 rels minimum). Query `MATCH (bg)-[:HAT_BAUPRODUKTSTATUS]->(b:Bauproduktstatus) RETURN b.name, count(bg)` shows the legal landscape across the corpus.

---

## P-16. 🔥 Add `norm_cen_ts_1090_201_2024` and split `norm_eurocode_generic`

**Evidence ([missing_underused_norm_nodes_reuse_kg.md](../../intake/inbox/research/missing_underused_norm_nodes_reuse_kg.md) + [circular_construction_reuse_graph_gaps.md](../../intake/inbox/research/circular_construction_reuse_graph_gaps.md)).** CEN/TS 1090-201:2024 is the EU-wide technical specification for **reuse-oriented assessment of reclaimed structural steel** — published 2024, applies in every CEN member country. It complements the country-specific protocols (UK SCI P427, Dutch NTA 8713, French CTICM recommendations) and is the single most universal reuse-Norm yet to enter our graph.

Currently `norm_en_1090` (2 rels) exists but the reuse-specific CEN/TS 1090-201 doesn't. Also, `norm_eurocode_generic` (mentioned in 4 archive files: 2 Association_house files, Berlin_Schildow, Haus_HOS_Muehlhausen) is a placeholder that should split into **EN 1992 (concrete), EN 1993 (steel), EN 1995 (timber), EN 1996 (masonry)** so each material domain has its own Norm hub.

**Rationale.** A Norm node connected to one country is sparse. A Norm connected to a *material category × all countries that adopt it* becomes a hub with high inbound count. The 4 Eurocode parts × ~12 corpus countries each = potentially **48 Norm-country edges** + every BG of that material adds another. CEN/TS 1090-201 specifically generates ~40-70 inbound edges (every steel-reuse BG across UK/DE/CH/NL/BE/FI/NO).

**Schema delta.**

```text
NEW Norm nodes:
  norm_cen_ts_1090_201_2024  "CEN/TS 1090-201:2024 — Assessment of Reclaimed Structural Steel"
  norm_cen_ts_17440          "CEN/TS 17440 — Assessment of Existing Structures"
  norm_en_1992                "EN 1992 — Eurocode 2 (Concrete)"
  norm_en_1993                "EN 1993 — Eurocode 3 (Steel)"
  norm_en_1995                "EN 1995 — Eurocode 5 (Timber)"
  norm_en_1996                "EN 1996 — Eurocode 6 (Masonry)"
  norm_en_206                 "EN 206 — Concrete specification (already proposed in knowledge_map §10)"
  norm_en_14081               "EN 14081 — Strength-graded structural timber"
  norm_en_771                 "EN 771 — Masonry units (specification)"
  norm_en_13162               "EN 13162 — Mineral wool thermal insulation"
  norm_nen_8700               "NEN 8700 — Dutch existing-structure assessment"
  norm_ns_3682_already        (already exists — confirm)
  norm_crow_cur_4_2023_already (already exists)
  norm_sci_p427_already        (already exists)
  norm_sci_p440_already        (already exists)
  norm_din_4074                "DIN 4074 — Visual strength grading of structural timber (DE)"
  norm_din_68800               "DIN 68800 — Wood preservation and durability classes"
  norm_din_18008               "DIN 18008 — Glass in building (DE design code)"

RETIRE: norm_eurocode_generic
  → migrate any inbound rels to the specific Eurocode part by material context (Beton → EN 1992, Stahl → EN 1993, Holz → EN 1995, Mauerwerk → EN 1996).
```

**Migration.** Seed the new Norm nodes (≈ 13). Then GILT_IN_LAND rels per P-4 give each Norm its country anchors. Per-project edges only where archive evidence supports it (research warns explicitly).

**Acceptance.** Every Norm has GILT_IN_LAND rels to at least one Land. The 4 Eurocode files in the archive (`Association_house_Groeditz`, `Association_house_Plauen`, `Berlin_Schildow_Pilot_House`, `Haus_HOS_Mehrfamilienhaus_Muehlhausen`) get `REFERENZIERT_NORM` edges to the correct material-specific Eurocode part instead of a generic.

---

## P-17. 🔥 Five new high-density PruefungNachweis hubs

**Evidence ([testing_verification_bauteilreuse_kg.md](../../intake/inbox/research/testing_verification_bauteilreuse_kg.md)).** Reuse-research is consistent that 5 testing categories apply to *most* reused structural elements but are missing from our schema as named nodes:

| Proposed node | Applies to | Connection-density source |
|---|---|---|
| `pr_zerstoerungsfreie_pruefung` | Steel, Beton, Holz | every structural BG (~150+ candidates) |
| `pr_korrosionspruefung` | Stahl beams, columns, rebar | every reused Stahl BG (~111 BGs) |
| `pr_festigkeitssortierung_holz` | Reused structural Holz | every structural Holz BG (~60 BGs) |
| `pr_bohrkernpruefung_beton` | Reused Beton/Stahlbeton | every concrete-reuse BG (~87 BGs) |
| `pr_dokumentenpruefung_bestand` | All — provenance verification | every project (~75) |
| `pr_schadstoffpruefung` | Pre-1996 donor materials | parent of asbestos/PCB/PAK/KMF screening for every era-tagged BG |
| `pr_materialbeprobung` | All hazardous-substance-risk BGs | parent of Schadstoffscreening + chemische Analyse |
| `pr_feuchtepruefung` | Holz, Lehm, Dämmstoff | every biological-degradation-risk BG (~30 BGs) |
| `pr_brandschutznachweis` (generic) | All structural reuse | new generic parent of `pr_abbrandbemessung` |

**Rationale.** Each of these tests is **standards-required for the material class** — not project-specific evidence. The graph can model "this BG class requires this test category" without claiming "this specific BG was tested with this method" (project-level BELEGT). That distinction is exactly what research recommends (`Bauteilgruppe-level INFER` rels, not `Projekt-level BELEGT`).

**Schema delta.**

```text
NEW PruefungNachweis nodes (9 in total):
  pr_zerstoerungsfreie_pruefung    "Zerstörungsfreie Prüfung (ZfP / NDT)"
  pr_zerstoerende_pruefung         "Zerstörende Prüfung (parent / category)"
  pr_korrosionspruefung            "Korrosionsprüfung / Restdickenmessung"
  pr_festigkeitssortierung_holz    "Festigkeitssortierung Holz (visuell + NDT)"
  pr_bohrkernpruefung_beton        "Beton-Bohrkernprüfung (EN 12504-1)"
  pr_dokumentenpruefung_bestand    "Dokumentenprüfung / Herkunfts- und Bestandsnachweis"
  pr_schadstoffpruefung            "Schadstoffprüfung (parent of Asbest/PCB/etc. screenings)"
  pr_materialbeprobung             "Materialprobe / Beprobung"
  pr_feuchtepruefung               "Feuchteprüfung (Holz, Lehm, Dämmstoff)"
  pr_brandschutznachweis           "Brandschutznachweis (generic; parent of pr_abbrandbemessung)"

NEW REL: TYPISCH_BEI_MATERIAL  (extends P-5)
  Also applies between PruefungNachweis and Material:
    (pr_korrosionspruefung)-[:TYPISCH_BEI_MATERIAL]->(mat_stahl)
    (pr_korrosionspruefung)-[:TYPISCH_BEI_MATERIAL]->(mat_stahlbeton)  # for rebar
    (pr_festigkeitssortierung_holz)-[:TYPISCH_BEI_MATERIAL]->(mat_holz)
    (pr_bohrkernpruefung_beton)-[:TYPISCH_BEI_MATERIAL]->(mat_beton)
    (pr_bohrkernpruefung_beton)-[:TYPISCH_BEI_MATERIAL]->(mat_stahlbeton)
    (pr_feuchtepruefung)-[:TYPISCH_BEI_MATERIAL]->(mat_holz)
    (pr_feuchtepruefung)-[:TYPISCH_BEI_MATERIAL]->(mat_lehm)
    (pr_feuchtepruefung)-[:TYPISCH_BEI_MATERIAL]->(mat_daemmstoff)
    (pr_zerstoerungsfreie_pruefung)-[:TYPISCH_BEI_MATERIAL]->(mat_stahl)
    (pr_zerstoerungsfreie_pruefung)-[:TYPISCH_BEI_MATERIAL]->(mat_beton)
    (pr_zerstoerungsfreie_pruefung)-[:TYPISCH_BEI_MATERIAL]->(mat_stahlbeton)
    (pr_zerstoerungsfreie_pruefung)-[:TYPISCH_BEI_MATERIAL]->(mat_holz)
```

This gives ~25 `TYPISCH_BEI_MATERIAL` rels seeded once → drives queries like
```cypher
MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)<-[:TYPISCH_BEI_MATERIAL]-(pr:PruefungNachweis)
WHERE NOT (bg)-[:HAT_PRUEFUNG]->(pr)
RETURN bg.id AS bg, m.name AS material, pr.name AS recommended_test
```
which yields **~120-300 "missing test recommendation" rows** for round 003.

**Migration.** Seed the 9 new PruefungNachweis nodes + ~25 `TYPISCH_BEI_MATERIAL` rels. Per-BG project-level `BELEGT` edges only when archive source names the method.

**Acceptance.** Every Material in the structural-reuse cluster (Stahl, Beton, Stahlbeton, Holz, Lehm, Dämmstoff) has at least one `TYPISCH_BEI_MATERIAL`-inbound PruefungNachweis. Recommended-test query (above) returns ≥ 100 rows.

---

## P-18. ⚡ Country×Material reuse templates (Reuse pattern hubs)

**Evidence ([circular_construction_reuse_graph_gaps.md](../../intake/inbox/research/circular_construction_reuse_graph_gaps.md) ranks Top 20 country×material gaps).** The most reusable graph pattern in reuse research is the *country×material template*: a single "node" that bundles the relevant Norm, RechtlicheBedingung, PruefungNachweis, Schadstoff risks, and Bauproduktstatus for one material in one country. Steel-UK uses CEN/TS 1090-201 + SCI P427 + CE/UKCA + NDT + corrosion-coating-with-lead/chromate + bolted assembly. Hollow-core-NO uses NS 3682 + Eurocode 2 + bearing-zone testing + carbonation. Lehm-DE uses DIN 18940 family + project-specific approval + Eignungsprüfung.

**Rationale.** Each template is a **hub node**: it attaches to every project that fits the pattern (~5-15 projects per template), and it brings together the norms/tests/risks for that pattern (~5-10 vocab nodes). One template gives you a 10×10 = 100 high-quality 2-hop traversals.

**Schema delta.**

```text
NEW LABEL: ReusePattern
  id prefix:  rp_
  example nodes (top 8 by corpus relevance):
    rp_stahl_uk            "UK Stahl-Reuse Pattern (CE/UKCA + SCI P427)"
    rp_stahl_de            "DE Stahl-Reuse Pattern (CEN/TS 1090-201 + DIBt route)"
    rp_stahl_ch            "CH Stahl-Reuse Pattern (SIA 263 + BauPG)"
    rp_stahl_be            "BE Stahl-Reuse Pattern (CEN/TS 1090-201 + Tracimat)"
    rp_stahl_nl            "NL Stahl-Reuse Pattern (NTA 8713 + CB'23 + Bbl)"
    rp_beton_hcs_no_fi_nl  "Hollow-Core Slab Pattern (NS 3682 + EN 1168 + CROW-CUR)"
    rp_beton_de            "DE Beton-Reuse Pattern (DIBt + EN 206)"
    rp_holz_de_ch_at       "DE/CH/AT Holz-Reuse Pattern (EN 14081 + DIN 4074 / SIA 265)"
    rp_naturstein_be       "BE Naturstein Pattern (EN 12058 + Opalis sheets)"
    rp_lehm_de             "DE Lehm-Reuse Pattern (DIN 18940 family + project approval)"

NEW REL: FOLGT_REUSE_PATTERN
  domain: Bauteilgruppe (or Projekt for project-level summary)
  range:  ReusePattern

NEW REL: REUSE_PATTERN_USES_NORM, REUSE_PATTERN_USES_TEST, REUSE_PATTERN_HAS_RISIKO, REUSE_PATTERN_REQUIRES_STATUS
  domain: ReusePattern
  range:  Norm / PruefungNachweis / Schadstoff / Bauproduktstatus
```

A single pattern node like `rp_stahl_uk` then connects out to:
- CEN/TS 1090-201, SCI P427, SCI P440, EN 1090, EN 1993 (5 Norms)
- NDT, Korrosionspruefung, Schadstoffpruefung-Pb-paint, Schweissbarkeitspruefung (4 PruefungNachweis)
- s_bleifarbe, s_chrombasierte_beschichtungen (2 Schadstoff)
- bps_ce_hen, bps_ukca (2 Bauproduktstatus)
- vt_verschraubung, vt_reversible_fuegung (2 Verbindungstechnik)
- → **15 outbound rels** from the pattern, plus every UK steel BG inbound (~9 BGs).

**Migration.** Define top 8-10 patterns. Seed 8-10 nodes + ~150 outbound rels + tag every existing reuse BG with `FOLGT_REUSE_PATTERN`. Patterns can evolve incrementally.

**Acceptance.** Query "list all expected vocab attached to every UK steel project, even if specific BG doesn't yet carry them" returns the pattern-hub closure — drives audit completeness.

**Risk warning.** Templates can over-claim ("this BG follows the pattern so it must have all the pattern's properties"). Mitigate by treating `FOLGT_REUSE_PATTERN` as "*matches the pattern's typical setting*" — a navigational shortcut, not an assertion that every pattern attribute applies. Round 003 still confirms each specific edge as `BELEGT`.

---

## Summary of proposed schema changes

| # | Change | Risk | Connection density | Tier |
|---:|---|:---:|:---:|:---:|
| **P-15** | New label **Bauproduktstatus** (CE/hEN/Ü/abZ/ZiE/…) | Low | ~380 edges (every BG) | 🔥 |
| **P-16** | Add **norm_cen_ts_1090_201_2024** + 12 other Norm hubs + split Eurocode_generic | Low | ~70-100 (via GILT_IN_LAND + REFERENZIERT_NORM templates) | 🔥 |
| **P-17** | 9 new **PruefungNachweis hubs** + TYPISCH_BEI_MATERIAL seed | Low | ~25 seed rules + 100-300 inferred test recommendations | 🔥 |
| P-1 | New label **Defekt** + HAT_DEFEKT | Low | Round 003 ~300-500 | ⚡ |
| P-2 | **BauwerkEra** + HAT_ERA + TYPISCH_BEI_ERA | Low | ~196 + ~30 typisch rels | 🔥 |
| P-3 | **Marktmodell** + HAT_MARKTMODELL | Low | Up to 150 | 🌱 |
| P-4 | **GILT_IN_LAND** rel for Norm/RechtlicheBedingung | Very low | ~30 immediate + grows | 🌱 |
| P-5 | **TYPISCH_BEI_MATERIAL/_BAUTEILTYP/_ERA** for Schadstoff | Very low | ~50 seed rules | 🔥 |
| P-6 | Refine **Methode** via MethodenKategorie parent | Low | restructure | ⚡ |
| P-7 | New label **Layer** (Brand) + TEILT_LAYER | Low | 15 rels, big traversal | ⚡ |
| P-8 | **LebenszyklusModul** + BERECHNET_NACH_MODUL + METHODENGRUNDLAGE_NORM | Medium | ~50 BG-module + 12 module-Norm | 🔥 |
| P-9 | **Akzeptanz** stakeholder refinement | Low | small | ⚠ |
| P-10 | **Wirtschaft** tightening | Low | small | ⚠ |
| P-11 | **HuerdeKategorie** tidy | Very low | cleanup | ⚠ |
| P-12 | Document **Beschaffungsweg ↔ Marktmodell** | Very low | docs only | ⚠ |
| P-13 | **MatchingQualitaet** | Medium | up to 600 (round 003) | 🌱 |
| P-14 | Drop zero-rel orphans | Very low | removes dead-ends | ⚠ |
| **P-18** | **ReusePattern** country×material templates | Medium | ~150 outbound + 200-300 BG-inbound | 🔥/⚡ |

**Withdrawn (per research validation):**
- `vt_holzduebel` — research warns no project evidence supports the term
- `vt_verleimung` project edge for CascadeUp — was lamination of glulam (manufacture), not assembly
- `la_f90` / `la_r90` / `la_rei90` as standalone nodes — should be property of `HAT_LEISTUNGSANFORDERUNG` rel
- `s_radon` — site condition, not a Bauteilreuse pollutant

## Recommended order if you accept multiple proposals (density-first)

**Phase A — quick wins, high connectivity (≈1-2 sessions):**
1. **P-4** (GILT_IN_LAND) — cheapest. Property → rel conversion.
2. **P-16** (CEN/TS 1090-201 + Norm splits) — adds ~13 Norm nodes that become country hubs once P-4 lands.
3. **P-15** (Bauproduktstatus) — every BG gets one. Densest single proposal.

**Phase B — domain encoding via TYPISCH_BEI_* matrix (1 session):**
4. **P-5** + **P-17** + **P-2** together — Schadstoff/PruefungNachweis/BauwerkEra matrix. One seed file, drives ~100+ inferred edges.

**Phase C — LCA & structure layer (1 session):**
5. **P-8** (LebenszyklusModul) — qualifies every CO2 claim, anchors zero-rel LCA Normen.
6. **P-7** (Layer) — 15 rels, makes shearing-layer queries trivial.

**Phase D — round-003 enablers (round 003 itself):**
7. **P-1** (Defekt) — round 003 tags BGs as it walks them.
8. **P-3** (Marktmodell) — round 003 tags procurement structure per BG.
9. **P-13** (MatchingQualitaet) — round 003 tags donor-receiver match per BG.
10. **P-18** (ReusePattern templates) — once you have several Phase A-C clusters seeded, ReusePattern stitches them into navigable hubs.

**Phase E — refinements:**
11. **P-6** Methode split, **P-9** Akzeptanz, **P-10** Wirtschaft, **P-11** HuerdeKategorie tidy, **P-12** Beschaffungsweg note, **P-14** orphan audit.

## Research prompts that came out of this (additional to §11 of knowledge map)

1. *"For the era-categories I'm proposing (vor 1900 / 1900-1945 / Nachkrieg / 1960er-70er / 1980-1996 / post-1996), is the Asbest-Verbot date 1993 (DE) / 1995 (EU) the right inflection point, or should the era boundary sit at 1990?"*
2. *"Stewart Brand's shearing layers — has the reuse-research literature (Crowther; Geldermans; Habraken Open Building) refined or replaced the 6-layer model? Should the schema use a different layer taxonomy?"*
3. *"EN 15978 Module D — which projects in our corpus explicitly cite Module D credit, vs. which just publish a CO2-Einsparung number?"*
4. *"Akzeptanz-Hürden taxonomy: confirm the literature-standard 5-stakeholder split (Bauherr/Planer/Ausführer/Nutzer/Behörde) or substitute with a different framework (Adams 2017 vs Hradil 2014)?"*
5. *"Defekt typology — which reuse-assessment protocol (SCI P427 Annex C? SIA 269? CROW-CUR?) has the most useful defect-category list to seed our Defekt nodes from?"*
6. *"Marktmodell — does any EU member-state legislation distinguish 'Gebrauchtware' from 'Bauprodukt' for CE/CPR purposes, or is that gap exactly the regulatory hole reuse projects struggle with?"*
7. *"CEN/TS 1090-201:2024 — confirm which corpus projects already cite it (very few, since it's new) vs. which would cite it if they were assessed today. The Norm is universal across EU steel reuse and should anchor every steel reuse pattern."*
8. *"Bauproduktstatus by country mapping — confirm the 5-path German taxonomy (CE_hEN / Ü / abZ / ZiE / project-specific) matches the regulatory practice in CH (BauPG), NL (Bbl), BE (regional + Tracimat), FR (PEMD), DK (BR18) — or do these countries have additional/different categories?"*
9. *"For each of the 9 new PruefungNachweis hubs (P-17), is there a Bauteiltyp filter? E.g. NDT applies primarily to structural members (Träger, Stütze, Decke), not to Innenausbau or Möbel. Encode as TYPISCH_BEI_BAUTEILTYP?"*

## What NOT to add (research warnings consolidated)

Lessons from [graph_patch_validation.md](../../intake/inbox/research/graph_patch_validation.md) and other research files. **Resist these tempting additions:**

1. **`HAT_SCHADSTOFF` from Schadstoff name to project unless the source explicitly names the pollutant for the BG.** Berlin Schildow → s_asbest was REJECTED in patch validation. Multi Brussels → s_asbest was REJECTED.
2. **`vt_holzduebel` from a screw-based project.** Recyclinghaus uses beech-wood screws, not dowels. The naming overlap is misleading.
3. **`vt_verleimung` as an assembly Verbindungstechnik from CascadeUp.** That project's "Verleimung" was the manufacture of glulamST/CLST (a `Herstellungsverfahren`), not the assembly connection (which used unspecified fasteners).
4. **CE/UKCA marking edges to non-steel projects.** Only steel is the active CPR-conformity-questioned material in the corpus right now.
5. **`norm_eurocode_generic` left in place.** Use the specific Eurocode part (EN 1992/1993/1995/1996) or no edge.
6. **Country-inference Norm edges.** "Project in Germany → DIN" doesn't get a rel unless the source names the specific DIN.
7. **CO2-Einsparung property without `BERECHNET_NACH_MODUL`.** Numbers without method are uncomparable. Flag with `lca_module_unknown=true` if not specified.
8. **Material × Schadstoff edges (P-5 matrix) as project assertions.** They are DOMAIN-LEVEL risk rules, not project facts. Don't write `Projekt -[hatSchadstoff]-> Asbest` from these rules.

---

**Next step recommendation:** Phase A is the obvious starting point if you accept the high-density priority logic — P-4 + P-16 + P-15 in that order. Each is small, idempotent, and lands ~100-400 edges total. Then Phase B (P-5+P-17+P-2 matrix) gives the schema its risk-rule "brain" without touching project content.

If you want a single proposal to test first, **P-15 (Bauproduktstatus)** is the densest and simplest — every reused BG gets one rel from a deterministic country×project rule, and it unblocks every regulatory query thereafter.
