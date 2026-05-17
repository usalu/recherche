# Batch 3 — BE/NL case-study buildings (+ 1 merge candidate)

**Decision after research:** promote to full Projekt; **merge** `p_pavilion_circl_amsterdam` into `p_circl_abn_amro` if confirmed to be the same building.
**Project count:** 3 (counting the merge pair as one).
**Common reference:** see [README.md](README.md). Comparable existing cases: [`BlueCity_Offices_Rotterdam.md`](../../../../_archive/research/gebaeude/BlueCity_Offices_Rotterdam.md), [`Maison_DnA_Asse.md`](../../../../_archive/research/gebaeude/Maison_DnA_Asse.md), [`Multi_Brussels_Reuse_in_MULTI.md`](../../../../_archive/research/gebaeude/Multi_Brussels_Reuse_in_MULTI.md).

---

### 1. `p_careno_becircular` — Careno Be.Circular

**Existing actor links:** Lionel Billiet, Sébastien Paulet.

**Likely identity:** Reuse pilot funded by **Be.Circular** (Brussels regional circular-economy programme). "Careno" may be a project alias, a building, or a consultancy. Both actors appear to be Belgian (likely Brussels/Wallonia architects or engineers).

**To research:**
- [ ] What is "Careno" — building, programme, firm?
- [ ] Be.Circular funding cycle (year + amount)
- [ ] If a building: location, scope, reuse strategy, materials
- [ ] Architects + Bauherr
- [ ] Sources: becircular.brussels, Brussels Environment, Rotor or BC Architects portfolios

---

### 2. `p_pavilion_circl_amsterdam` — Pavilion Circl Amsterdam

**Existing actor links:** Hans Hammink.

**Likely identity:** **Circl Pavilion** at the ABN AMRO headquarters in Amsterdam-Zuid. Designed by de Architekten Cie. (Hans Hammink = partner), opened 2017. Often-cited reuse + circular pavilion: reused HSA jeans insulation, reused door frames, reused window frames from old ABN buildings.

**To research:**
- [ ] Confirm: same building as `p_circl_abn_amro`? If yes → **MERGE candidate** (keep `p_circl_abn_amro` as canonical).
- [ ] Reused materials inventory (well-documented online): denim insulation, kozijnen, plafondbalken, vloerdelen
- [ ] Year (2017 opening)
- [ ] Architects (de Architekten Cie. / Hans Hammink)
- [ ] Tragwerksplanung, Bauausführung
- [ ] Sources: circl.nl, deArchitektenCie.nl, ABN AMRO press

---

### 3. `p_circl_abn_amro` — Circl / ABN AMRO urban mining context

**Existing actor links:** Michel Baars.

**Likely identity:** Same as Circl Pavilion (above). Michel Baars = founder of **New Horizon Urban Mining**, the dismantling/reuse company that supplied many components for Circl. The `p_circl_abn_amro` framing emphasizes the *urban mining supply chain* angle.

**To research:**
- [ ] Confirm overlap with `p_pavilion_circl_amsterdam`
- [ ] If MERGE: keep `p_circl_abn_amro` as canonical id; emit a `canonicalize_node` op (alternative name in `aliases`) and redirect all rels from `p_pavilion_circl_amsterdam` to `p_circl_abn_amro`
- [ ] Michel Baars / New Horizon role
- [ ] Other Circl actors (Madaster involvement, denim insulation by ZDS)
- [ ] Sources: as above + New Horizon project page

---

## Output

- For Careno: write a new archive + JSONL.
- For Circl: write **one** archive (e.g. `Circl_Pavilion_ABN_AMRO_Amsterdam.md`) and one JSONL using `p_circl_abn_amro` as the canonical Projekt id. Then a tiny patch:

```cypher
// Verification before merge (run first):
MATCH (p1:Projekt {id: 'p_pavilion_circl_amsterdam'})-[r]-()
RETURN type(r), count(*) ORDER BY count(*) DESC;

// Merge after archive is ready (manual review required):
// op merge_node from=p_pavilion_circl_amsterdam to=p_circl_abn_amro
```
