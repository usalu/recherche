# Circular Construction / Bauteilreuse Knowledge Graph Patch Validation

## Edge validation

| Operation | Evidence found | Evidence level | Semantic fit | Risk/caveat | Status | Source citation |
|---|---|---:|---|---|---|---|
| 1. Berlin Schildow Pilot House → `s_asbest` | No direct source found tying asbestos to the Schildow pilot project or to a reused Bauteilgruppe. Existing pollutant research note also flags Schildow/asbestos as **INFER/RESEARCH**, not documented. | None / not established | `HAT_SCHADSTOFF` would be correct only with explicit pollutant evidence. | Do not infer asbestos from age, prefab concrete reuse, or demolition context. | **REJECT** | Internal research note / file citation from prior validation |
| 2. Europa Building Brussels → `s_asbest` | Yes. Council timeline states asbestos removal and demolition of 1960s constructions began in Nov. 2007 and ended Oct. 2008. | Project-level / demolition-phase evidence | Semantically acceptable for project-level `HAT_SCHADSTOFF`. | Do **not** attach asbestos to the reused timber window façade or any specific Bauteilgruppe without a BG/audit source. Better model: existing 1960s fabric / demolition works → asbestos. | **APPROVE WITH CAVEAT** | Council timeline source from prior validation |
| 3. Multi Brussels Reuse in MULTI → `s_asbest` | No project-specific asbestos evidence found. Rotor documents reuse work and codified reuse challenges, but not asbestos. General Belgian reuse-audit guidance mentions asbestos screening, but that is not project evidence. | None / not established | Edge would be semantically correct only if asbestos is documented. | General Brussels/Belgian asbestos risk is insufficient. Needs project asbestos inventory, demolition audit, or BG-specific source. | **REJECT** | Rotor / general Belgian audit guidance sources from prior validation |
| 4. Superlocal Expogebouw Bleijerheide → `s_asbest` | Yes. SUPERLOCAL source states the reused window frames/`kozijnen` contained asbestos and required costly processing; evaluation report also identifies harvesting/processing of frames because of asbestos. | **Bauteilgruppe-level**: window frames / `kozijnen` | Pollutant relation is correct, but best attached to the frame Bauteilgruppe rather than broadly to every reused element. | Project-level edge is acceptable only as a summary edge. Stronger modelling: `Expogebouw kozijnen` → `s_asbest`. | **APPROVE WITH CAVEAT** | SUPERLOCAL source and evaluation report from prior validation |
| 5. Recypark Demets Anderlecht → `rb_vergaberecht` | Partial evidence. Brussels public documentation refers to designation of the architect office for Recypark Demets; Recyparks are public regional facilities. | Project/procurement-level, not Bauteilgruppe | Semantically plausible if `rb_vergaberecht` means public procurement context. | Caveat: procurement-context evidence was found, not a source saying procurement law specifically constrained reuse choices. Better node: `rb_oeffentliche_ausschreibung` / `marché public` if available. | **APPROVE WITH CAVEAT** | Brussels public documentation sources from prior validation |
| 6. Zinneke Feder Masui4ever Brussels → `rb_vergaberecht` | Yes. The Masui4Ever/Zinneke case study explicitly says the ERDF grant subjected Zinneke to public procurement rules and discusses public procurement as a reuse lever. | Project-level legal/procurement evidence | Strong semantic fit. | No Bauteilgruppe issue; this is a project delivery/legal condition. | **APPROVE** | Masui4Ever/Zinneke case study from prior validation |
| 7. 55 Great Suffolk Street London → `rb_ce_ukca_marking_reused_steel` | Yes. ASBP case study says reclaimed steel quality/testing was coordinated, CE marking for reclaimed sections was achieved through EN 1090, and warranty issues were avoided because the steel was CE/UKCA marked. | **Bauteilgruppe-level**: reclaimed structural steel | Exact semantic fit. | Keep steel-specific; do not generalize CE/UKCA marking to other reused materials. | **APPROVE** | ASBP case study from prior validation |
| 8. Hastings Pier Visitor Centre → `rb_grade_ii_listing` | Yes. Hastings Pier is documented as a Grade II listed structure; renovation works included repair of the Grade II listed substructure and construction of a new visitor centre. | Site/project-level heritage condition | Good fit if the edge means the visitor-centre project occurred within a Grade II listed pier context. | The listed asset is the pier/substructure, not necessarily the new visitor-centre building itself. Also add/keep broader parent `rb_denkmalschutz`. | **APPROVE WITH CAVEAT** | Historic England / project sources from prior validation |
| 9. CascadeUp London secondary timber/glulam demonstrator → `vt_verleimung` | Yes for glued laminated secondary timber: WCTE paper says secondary timber was manufactured into `glulamST` and `CLST`. | Bauteilgruppe/material-product level | Fit is only partial: “Verleimung” is evidenced as lamination/manufacturing of engineered timber, not necessarily as the reversible assembly connection technique. | Better modelling: `glulamST/CLST` material/product or `Herstellungsverfahren: Verleimung/Laminierung`. For actual assembly connection, existing note says CascadeUp used a kit-of-parts with unspecified fasteners, so do not replace that with `vt_verleimung`. | **APPROVE WITH CAVEAT** | WCTE paper and connection-tech note from prior validation |

## Proposed new nodes

| Proposed node | Validation |
|---|---|
| `s_kmf` | **Approve as a generic pollutant/risk node only.** Do not create project pollutant edges unless old mineral-wool insulation is documented and the age/risk category is clear. Existing note treats KMF as old mineral-wool risk, not project-level evidence. |
| `rb_denkmalschutz` | **Approve** as a general heritage-protection parent. Link `rb_grade_ii_listing` as UK-specific child/instance. |
| `rb_materialpass` | **Approve** as a cross-country legal/process metadata node, but project edges require a source naming a material passport, inventory, PEMD, audit, or equivalent. |
| `norm_en_206` | **Approve** as concrete standard metadata; do not attach to a project unless documentation names EN 206 or a concrete requalification route. |
| `vt_holzduebel` | **Approve as a possible node**, but no edge unless a source explicitly says Holz­dübel/wooden dowels. Existing connection note warns not to misclassify beech screws as wood dowels. |
| `av_sandstrahlen` | **Approve as a processing-method node**, but project edges need explicit cleaning/surface-preparation evidence. |
| `pr_zerstoerungsfreie_pruefung` | **Approve as a testing/proof node.** Use as project-level `BELEGT` only where a source names ZfP/NDT; otherwise keep as Bauteilgruppe-level inference for structural steel/concrete/timber. |

## Summary

Approved outright:
- Zinneke Feder Masui4ever Brussels → `rb_vergaberecht`
- 55 Great Suffolk Street London → `rb_ce_ukca_marking_reused_steel`

Approved with caveat:
- Europa Building Brussels → `s_asbest`
- Superlocal Expogebouw Bleijerheide → `s_asbest`
- Recypark Demets Anderlecht → `rb_vergaberecht`
- Hastings Pier Visitor Centre → `rb_grade_ii_listing`
- CascadeUp London secondary timber/glulam demonstrator → `vt_verleimung`

Rejected:
- Berlin Schildow Pilot House → `s_asbest`
- Multi Brussels Reuse in MULTI → `s_asbest`

Main modelling cautions:
- Do not infer project-level pollutant evidence for every Bauteilgruppe.
- Do not approve KMF unless insulation age or risk category is clear enough.
- Keep CE/UKCA marking specific to reused structural steel.
- Treat `vt_verleimung` for CascadeUp as product manufacture/lamination evidence, not necessarily connection technique evidence.
