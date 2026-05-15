# Reuse Schema Proposals — research-driven changes

**Companion to:** [reuse_knowledge_map.md](reuse_knowledge_map.md)
**Purpose:** Where the previous doc proposed *adding edges and nodes* to the existing schema, this one proposes *structural changes to the schema itself* — new labels, new relationship types, refinements — based on what the reuse-research literature treats as core and what the archive scan actually surfaces.

Each proposal has:
- **Evidence** — archive hits or domain-literature grounding
- **Rationale** — why current schema falls short
- **Schema delta** — exact label/rel/property additions
- **Migration** — how to land the change without breaking existing data
- **Acceptance** — verifiable success criteria

Decisions stay yours. Each section is independent; you can take any subset.

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

---

## Summary of proposed schema changes

| # | Change | Risk | Impact |
|---:|---|:---:|:---:|
| P-1 | New label **Defekt** + HAT_DEFEKT | Low | **High** (enables defect crosstabs) |
| P-2 | New label **BauwerkEra** + HAT_ERA + TYPISCH_BEI_ERA | Low | **High** (drives Schadstoff risk screening) |
| P-3 | New label **Marktmodell** + HAT_MARKTMODELL | Low | Medium-High |
| P-4 | New rel **GILT_IN_LAND** for Norm/RechtlicheBedingung | Very low | Medium |
| P-5 | New rels **TYPISCH_BEI_MATERIAL** / **_BAUTEILTYP** for Schadstoff | Very low | Medium |
| P-6 | Refine **Methode** via MethodenKategorie parent | Low | Medium |
| P-7 | New label **Layer** (Brand's shearing layers) + TEILT_LAYER | Low | Medium |
| P-8 | New label **LebenszyklusModul** + BERECHNET_NACH_MODUL + METHODENGRUNDLAGE_NORM | Medium | **High** for LCA-conscious projects |
| P-9 | Refine **Huerde** with stakeholder-specific Akzeptanz nodes | Low | Low-Medium |
| P-10 | Tighten **Wirtschaft** (renames + new nodes) | Low | Low-Medium |
| P-11 | Tidy **HuerdeKategorie** (drop hk_unklar, possibly rename hk_sozial_organisatorisch) | Very low | Low |
| P-12 | Document Beschaffungsweg ↔ Marktmodell axis | Very low | Low |
| P-13 | New label **MatchingQualitaet** + HAT_MATCHING_QUALITAET | Medium | Medium-High |
| P-14 | Audit / drop zero-rel orphans where appropriate | Very low | Low |

## Recommended order if you accept multiple proposals

1. **P-4** (GILT_IN_LAND) — cheapest, unlocks country queries. Property → rel conversion.
2. **P-2** (BauwerkEra) + **P-5** (Schadstoff TYPISCH_* rels) — domain-knowledge encoding, immediately usable for risk screening.
3. **P-1** (Defekt) + **P-7** (Layer) — both add categorical depth. Round 003 work is where they get filled with real data.
4. **P-8** (LebenszyklusModul) — needed if user wants to publish comparable CO2 numbers.
5. **P-3** (Marktmodell) + **P-13** (MatchingQualitaet) — make the reuse research story tellable.
6. **P-6** (Methode split), **P-9** (Akzeptanz), **P-10** (Wirtschaft), **P-11** (HuerdeKategorie), **P-12** (Beschaffungsweg note), **P-14** (orphan audit) — refinements after the core gaps close.

## Research prompts that came out of this (additional to §11 of knowledge map)

1. *"For the era-categories I'm proposing (vor 1900 / 1900-1945 / Nachkrieg / 1960er-70er / 1980-1996 / post-1996), is the Asbest-Verbot date 1993 (DE) / 1995 (EU) the right inflection point, or should the era boundary sit at 1990?"*
2. *"Stewart Brand's shearing layers — has the reuse-research literature (Crowther; Geldermans; Habraken Open Building) refined or replaced the 6-layer model? Should the schema use a different layer taxonomy?"*
3. *"EN 15978 Module D — which projects in our corpus explicitly cite Module D credit, vs. which just publish a CO2-Einsparung number?"*
4. *"Akzeptanz-Hürden taxonomy: confirm the literature-standard 5-stakeholder split (Bauherr/Planer/Ausführer/Nutzer/Behörde) or substitute with a different framework (Adams 2017 vs Hradil 2014)?"*
5. *"Defekt typology — which reuse-assessment protocol (SCI P427 Annex C? SIA 269? CROW-CUR?) has the most useful defect-category list to seed our Defekt nodes from?"*
6. *"Marktmodell — does any EU member-state legislation distinguish 'Gebrauchtware' from 'Bauprodukt' for CE/CPR purposes, or is that gap exactly the regulatory hole reuse projects struggle with?"*

---

**Next step recommendation:** decide which P-N proposals are in scope. Each is independently shippable. Cheapest first wins (P-4, then P-5, then P-2). Then P-1 and P-8 are the two biggest unlocks for the reuse research questions the corpus is actually trying to answer.
