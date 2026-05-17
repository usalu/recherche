# Batch 5 — Teaching / research programs

**Decision after research:** **relabel** `Projekt` → `Programm` for all 4 — these are pedagogical / research initiatives, not buildings. The actor links stay (they're meaningful), but the node should carry `Programm` instead of `Projekt` semantics.
**Project count:** 4.
**Common reference:** see [README.md](README.md). Existing `Programm` nodes in the graph (17 of them) include things like `prg_disrupt`, `prg_recreate`, etc.

The output for this batch is **simpler** than for Building case studies — there's no Bauwerk, no Bauteilgruppe, no Material reuse to inventory. Just:
- The `Programm` node (renamed from `Projekt`)
- A `Quelle` for the source documentation
- Stadt / Land
- Linked Akteure with rolls (`ar_forschung_dokumentation`, `ar_reuse_beratung`)
- Optionally: linked case-study Projekte that the programme produced

---

### 1. `p_eth_circular_construction_student_reuse` — ETH Circular Construction (student reuse demonstrator/news)

**Existing actor links:** Catherine De Wolf, Fabio Gramazio, Matthias Kohler.

**Likely identity:** ETH Zürich's circular-construction teaching + research track. Catherine De Wolf = professor at ETH for Circular Engineering for Architecture (CEA, est. 2021). Gramazio Kohler = robotics-driven design + construction lab.

**To research:**
- [ ] Confirm scope: ETH Zürich CEA chair + student projects (likely the demonstrators tracked here)
- [ ] Notable student demonstrator projects (e.g., **Re-Crete** pavilion, **Save** salvage, robot-assembled reuse)
- [ ] Dates (CEA chair founded 2021; specific demonstrators from 2022 onwards)
- [ ] Funding: ETH internal? SNSF? Industry partners?
- [ ] Linked sources: ethz.ch/cea, gramaziokohler.arch.ethz.ch, publications in CEA Journal
- [ ] List of derived case-study Projekte (some may already be in graph: ReCrete footbridge, K.118 connection?)

---

### 2. `p_reuse_in_construction_zhaw` — Reuse in Construction / ZHAW

**Existing actor links:** Andreas Sonderegger, Eva Stricker, Guido Brandi, ZHAW.

**Likely identity:** ZHAW Zürcher Hochschule für Angewandte Wissenschaften — Institute for Constructive Engineering (IKE) reuse research line. Eva Stricker = lead researcher (compiled K.118 + several Swiss reuse case studies). Andreas Sonderegger + Guido Brandi = ZHAW IKE colleagues.

**To research:**
- [ ] Programme/research-line title (likely "Wiederverwendung im Bauwesen" or similar)
- [ ] Outputs (ZHAW Reuse Compendium, K.118 case study, ELYS Basel coverage)
- [ ] Programme runtime + funding (Innosuisse?)
- [ ] Sources: zhaw.ch/ike, ZHAW Compendium (link), Stricker publications

---

### 3. `p_architecture_of_reuse_brussels` — Architecture of Reuse Brussels

**Existing actor links:** Christine Conix, Lionel Devlieger, Maarten Gielen.

**Likely identity:** Probably a teaching programme / studio jointly run by Rotor (Devlieger + Gielen) and Christine Conix (CONIX RDBM Architects, Antwerp) at one of the Brussels architecture schools (KU Leuven Faculty of Architecture, ULB, or Université Saint-Luc). "Architecture of Reuse" is a recurring studio theme in Brussels.

**To research:**
- [ ] Host institution (KU Leuven / ULB / VUB / La Cambre)
- [ ] Programme dates + studio cycles
- [ ] Notable student / studio outputs
- [ ] Sources: rotordc.com, conixrdbm.com, the school's website

---

### 4. `p_vandkunsten_component_reuse` — Vandkunsten Reused Construction Materials / Component Reuse

**Existing actor links:** Katrine West Kristensen, Søren Nielsen, Vandkunsten.

**Likely identity:** **Vandkunsten Architects** (Copenhagen) reuse R&D line. Søren Nielsen = Vandkunsten partner known for circular/reuse design (e.g., Upcycle House, Upcycle Studios). Katrine West Kristensen = Vandkunsten researcher.

**To research:**
- [ ] Programme title (likely a Realdania-funded R&D project on component reuse)
- [ ] Connection to existing graph projects: `p_upcycle_studios_copenhagen` (already in graph)
- [ ] Outputs: pilot buildings, research reports
- [ ] Funding (Realdania, Innovation Fund Denmark?)
- [ ] Sources: vandkunsten.com, realdania.dk

---

## Output

For each, produce:
- A short `.md` documenting the programme (not a full case-study template — programme template is simpler)
- A small JSONL with:
  - **`Programm` node** (id stays `p_<slug>`, but label changes from `Projekt` to `Programm`)
  - `Quelle`, `Stadt`, `Land`, linked Akteure with `ar_forschung_dokumentation` rolle
  - Optional: linked Projekte the programme produced

A label change in JSONL is done as an `add_node` op with the new label list + `remove_label` op for the old label (or via Cypher: `MATCH (n {id:'...'}) REMOVE n:Projekt SET n:Programm`).

**Recommendation:** treat the relabel as the *last step* — first promote with `node_role: full_programm`, then do the label flip separately for safety.
