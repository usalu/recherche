# Batch 6 — EU-funded consortia

**Decision after research:** **relabel** `Projekt` → `Programm` for all 4. These are multi-partner research consortia (Interreg / Horizon Europe / national R&D), not buildings. May also include **merge** of `p_interreg_nwe_fcrbe` into `p_fcrbe` if they refer to the same programme.
**Project count:** 4.
**Common reference:** see [README.md](README.md). Adjacent existing Programm nodes in the graph (some you'll cross-link to): `prg_disrupt`, `prg_recreate`, `prg_horizon_europe` (if present).

These programmes are well-documented online — the research should be quick (one official project page + one Interreg/CORDIS database entry per programme).

---

### 1. `p_fcrbe` — FCRBE — Facilitating the Circulation of Reclaimed Building Elements

**Existing actor links:** Hugo Topalov, Sarah Westerfeld.

**Likely identity:** **FCRBE** Interreg NWE 2017–2022 programme, lead partner Rotor (Brussels), Salvo (UK), Bellastock (FR), CSTC/WTCB (BE), Brussels Environment. Outputs: opalis.eu, futureusedmaterials.eu, FCRBE guidelines.

**To research:**
- [ ] Confirm the programme is FCRBE Interreg NWE (≈ €4.6M, 2018–2022)
- [ ] Full partner list (probably already partly in graph)
- [ ] Funder: Interreg North-West Europe + ERDF
- [ ] Outputs: 36 pilot reuse projects in NWE, Opalis dealer directory, online guides
- [ ] Sources: nweurope.eu/fcrbe, opalis.eu, FCRBE final report

---

### 2. `p_interreg_nwe_fcrbe` — Interreg NWE FCRBE

**Existing actor links:** Michaël Ghyoot.

**Likely identity:** Same as `p_fcrbe`. Michaël Ghyoot = Rotor partner, FCRBE project lead. **Strong MERGE candidate** into `p_fcrbe`.

**To research:**
- [ ] Confirm complete overlap with `p_fcrbe`
- [ ] If confirmed: emit `canonicalize_node` op merging `p_interreg_nwe_fcrbe` into `p_fcrbe` (keep `Interreg NWE FCRBE` as alias)

---

### 3. `p_rebridge_structural_reuse_project` — REBRIDGE structural reuse project

**Existing actor links:** Corentin Fivet.

**Likely identity:** **ReBridge** — likely a structural-reuse research project on bridges or bridge-girder reuse. Corentin Fivet = Structural Xploration Lab at EPFL Fribourg, known for structural reuse research (incl. ReCrete footbridge using reused concrete).

**To research:**
- [ ] Disambiguate ReBridge: could be (a) a specific SNSF/Innosuisse project on bridge reuse, (b) part of NCCR Digital Fabrication, or (c) an EPFL teaching studio
- [ ] Look at Fivet's SXL group at EPFL: sxl.epfl.ch
- [ ] Outputs: reused bridge girders, demonstrator bridges, publications
- [ ] Funder
- [ ] Sources: sxl.epfl.ch publications, EPFL news

---

### 4. `p_reuse_logistics` — Reuse Logistics

**Existing actor links:** Madlen Kobi.

**Likely identity:** Generic title — likely a research project on logistics/transport for reuse. Madlen Kobi = circular-economy researcher (ZHAW or EPFL or HSLU).

**To research:**
- [ ] Identify the specific project. Candidates: Innosuisse "Reuse Logistics" call, KTI/SBFI project, NFP-funded study
- [ ] Confirm Madlen Kobi's affiliation
- [ ] If too generic / unidentifiable: relabel as `Begriff` (concept) rather than `Programm`, or delete

---

## Output

For each programme: a short `.md` documenting the consortium + a small JSONL (label `Programm`, no Bauwerk/BG). For the FCRBE pair, also include the merge op.

```cypher
// FCRBE-merge verification BEFORE merging:
MATCH (p:Projekt {id: 'p_interreg_nwe_fcrbe'})-[r]-()
RETURN type(r), count(*);

MATCH (p:Projekt {id: 'p_fcrbe'})-[r]-()
RETURN type(r), count(*);
```
