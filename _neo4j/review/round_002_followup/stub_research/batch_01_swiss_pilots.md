# Batch 1 — Swiss case-study pilots

**Decision after research:** promote to full Projekt.
**Project count:** 3.
**Common reference:** see [README.md](README.md) for schema, controlled vocab, ID conventions, and the K.118 reference example.

## Per-project research checklist

For each project below, ChatGPT/Perplexity should gather enough to produce:
- `_archive/research/gebaeude/<Name>.md` mirroring the K.118 case-study template (Sections 1–10).
- `_neo4j/intake/inbox/stub_promotion/<pid>.kg.jsonl` matching the contract.

The Akteure listed under "Existing actor links" already point to the project via `ASSOZIIERT_MIT_PROJEKT` — **do not re-create those**, just add new ones as needed.

---

### 1. `p_schaerenmoosstrasse_zuerich` — Schärenmoosstrasse Zürich

**Existing actor links:** Daniel Hoffmann, Gian Trachsler, Studio Trachsler Hoffmann.

**Likely identity:** Direct-reuse housing or fit-out project in Zürich-Schwamendingen (Schärenmoosstrasse area). Studio Trachsler Hoffmann is a Zürich architecture firm known for reuse-led design.

**To research:**
- [ ] Exact street address; intervention type (Neubau vs Umbau vs Aufstockung)
- [ ] Building type (Wohnen / Schule / Büro / ...)
- [ ] Year of design + completion
- [ ] Bauherr, Tragwerksplanung
- [ ] Which materials/elements are reused; donor sources
- [ ] Reuse-rate by mass/volume if published
- [ ] Certifications, norms, financing
- [ ] Sources: Studio Trachsler Hoffmann project page, hochparterre.ch, espazium.ch

---

### 2. `p_umar_unit` — UMAR Unit

**Existing actor links:** Werner Sobek, Dirk E. Hebel, Felix Heisel, Vanessa Propach.

**Likely identity:** **U**rban **M**ining **A**nd **R**ecycling unit in the **NEST** experimental building at Empa Dübendorf (Switzerland). Architects: Werner Sobek + KIT/ETH (Hebel + Heisel). Built 2017–2018.

**To research:**
- [ ] Confirm year (≈ 2018), location (Empa NEST, Dübendorf CH)
- [ ] All reused/upcycled elements: metal envelope, wood, brick, copper, plumbing fixtures
- [ ] Donor buildings + reuse chain
- [ ] Quantitative reuse-rate (~100 % design target?)
- [ ] Bauherr (Empa), Tragwerksplanung
- [ ] Publications: Sobek + Hebel + Heisel "Building from Waste", NEST UMAR project page (empa.ch), academic articles
- [ ] Norms / certifications

---

### 3. `p_elementa_walkeweg` — ELEMENTA / Walkeweg Basel

**Existing actor links:** Carla Ferrando Costansa, Pablo Garrido Arnaiz.

**Likely identity:** ELEMENTA / Walkeweg site in Basel — likely a reuse-focused housing or mixed-use development on Walkeweg. Architects in registry suggest a Spanish-named pair, possibly EMI Architekten or a similar Basel office. ELEMENTA is also a known Swiss precast/reuse brand.

**To research:**
- [ ] Disambiguate "ELEMENTA Walkeweg" — building, brand, or planning study?
- [ ] If building: location (Basel address), Bauherr, year
- [ ] Materials reused, donor sources
- [ ] Architect office of Ferrando Costansa / Garrido Arnaiz
- [ ] Publications: hochparterre.ch, espazium.ch, BaslerZeitung
- [ ] Whether it has been built or is still in planning

---

## Output deliverable per project

Two files. For Schärenmoosstrasse:
```
_archive/research/gebaeude/Schaerenmoosstrasse_Zuerich.md
_neo4j/intake/inbox/stub_promotion/p_schaerenmoosstrasse_zuerich.kg.jsonl
```

The JSONL should at minimum include:
- 1 `Projekt` node (use existing id `p_schaerenmoosstrasse_zuerich`; set `node_role: "full_projekt"`, `promoted_at`, `promoted_reason: "Phase L stub promotion"`)
- 1 `Quelle` node for the new archive markdown (id `q_<slug>_md`)
- 1+ `Bauwerk` nodes (receiver + any donor)
- 1+ `Bauteilgruppe` nodes
- New `Akteur` nodes only for actors NOT already in the existing actor links
- `Stadt` + `Land` (likely already exist: `stadt_zuerich`, `land_schweiz`)
- All the BELEGT_IN, LIEGT_IN_*, HAT_BAUTEILGRUPPE, NUTZT_BAUWERK, BETEILIGT_AN, HAT_AKTEURROLLE rels.

Existing rels (the ASSOZIIERT_MIT_PROJEKT from registry actors) stay untouched.
