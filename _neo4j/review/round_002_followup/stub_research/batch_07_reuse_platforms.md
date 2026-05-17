# Batch 7 — Reuse platforms / tools

**Decision after research:** **relabel** `Projekt` → `Plattform` (a new label) **or** add as instances of the existing `Tool` / `Software` labels, whichever fits better per platform. These are digital marketplaces / matching tools, not buildings.
**Project count:** 2.
**Common reference:** see [README.md](README.md). Adjacent existing nodes: `Tool` and `Software` labels already exist (Madaster, Concular, Restado, Rotor inventory tools, Opalis directory).

---

### 1. `p_refair_bordeaux_reemploi_platform` — REFAIR Bordeaux reuse platform

**Existing actor links:** Orianne Scourzic, Tiphaine Berthomé.

**Likely identity:** **REFAIR** (Réemploi Aquitaine) — a reuse-materials platform based in Bordeaux. Likely a Bordeaux Métropole or ADEME-funded plateforme de réemploi. Both actors are French; Tiphaine Berthomé works in circular construction in Nouvelle-Aquitaine.

**To research:**
- [ ] Confirm REFAIR programme + operator
- [ ] Platform type: physical reuse-yard? digital marketplace? mixed model?
- [ ] Founder, funders (ADEME, Région Nouvelle-Aquitaine, Bordeaux Métropole?)
- [ ] Year of launch
- [ ] Material flows handled (t/year)
- [ ] Sources: refair-bordeaux.fr or similar; ademe.fr; press in Sud Ouest

---

### 2. `p_rcmi_concular` — RCMI / Concular blueprint project

**Existing actor links:** Dominik Campanella.

**Likely identity:** **Concular** GmbH (Berlin) — reuse-matching platform founded by Dominik Campanella + Julius Schäufele. "RCMI" likely = **Reverse Construction Material Inventory** or a Concular sub-product/blueprint. Already partially modeled in graph as a Tool (`concular`).

**To research:**
- [ ] Decode RCMI acronym (Concular has a few sub-products; check concular.com)
- [ ] Whether this is a separate Programm/Tool or a workflow within Concular
- [ ] Linked existing Akteur: `concular` (likely already in graph as Tool)
- [ ] Sources: concular.com, Campanella interviews

---

## Output

For each:
- A short `.md` documenting the platform (operator, year, scope, model)
- A small JSONL with the node labeled `Plattform` (or `Tool` / `Software` if more fitting) — keep the existing id, just change the label
- If the platform is already represented as a `Tool` node elsewhere in the graph: emit a `canonicalize_node` merge op

**Note:** since `Plattform` is a label not currently in the contract schema, adding it would require another contract drift update. Easier route: use the existing `Tool` or `Software` label.
