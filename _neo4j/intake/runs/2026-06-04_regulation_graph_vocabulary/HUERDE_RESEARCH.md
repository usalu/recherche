# Huerde — can it be connected to Projekte/Bauteilgruppen with evidence?

**Short answer: yes — and cleanly**, if we (a) adopt the academic barrier taxonomy as controlled
vocabulary, and (b) connect by *evidenced derivation* (material/component → technical barriers) and
*project context/case sources* (project → market/organisational barriers) — replacing today's
`inferiert` `HAT_HUERDE` edges.

## Evidence base (researched)
- **Taxonomy:** Rakhshan, Morel, Alaka & Charef (2020), *Components reuse in the building sector – A
  systematic review*, Waste Management & Research — **6 categories, 23 sub-categories**; the most
  pronounced are **perception, risk, compliance, market**.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC7472835/
- **Material-specificity:** concrete-reuse barriers = logistics (transport/storage), **service-life /
  quality uncertainty**, certification, labour; **steel = inherently reusable → far fewer barriers**;
  composites = separation. (incl. SEGRO case study; concrete-precedents review.)
  https://www.sciencedirect.com/science/article/pii/S0959652622048090

## Controlled barrier vocabulary (your ~11 market-Huerde → taxonomy)
| Huerde node | Taxonomy category | Connects best to |
|---|---|---|
| h_mengenunsicherheit, h_verfuegbarkeitsproblem | Market / supply | **Projekt** |
| h_akzeptanzproblem | Social / perception | **Projekt** |
| h_ausschreibungsproblem | Regulatory / procurement | **Projekt** (→ also `rw_zirkulaere_vergabe`) |
| h_terminunsicherheit, h_entwurfsbindung | Organisational / management | **Projekt** |
| h_fehlende_lagerflaeche, h_witterung_feuchte | Logistics | **Projekt** |
| h_aufbereitungsaufwand | Economic / labour | **Projekt** / Bauteilgruppe |
| h_heterogenitaet_chargen, h_unkonventionelles_material | Technical / quality | **Bauteilgruppe** |

> Clean split: **technical/quality barriers → Bauteilgruppe** (derivable from material); **market /
> organisational / perception barriers → Projekt** (case/context-driven). This is exactly why the old
> per-Bauteilgruppe spray was wrong — most barriers are *project-level*, not component-level.

## Two evidenced ways to connect (both real, pick per barrier)

### A) Derived from material/component (Bauteilgruppe) — evidenced by the taxonomy
- Concrete Bauteilgruppe → `h_heterogenitaet_chargen` / service-life uncertainty / storage logistics
  (evidence: Rakhshan 2020 + concrete-precedents review).
- Composite Bauteilgruppe → separation barrier (evidence: ISO 20887 + SEGRO case).
- **Steel Bauteilgruppe → deliberately few/none** (literature: steel is inherently reusable) — the
  evidence tells us *not* to over-attach. The opposite of the old generic spray.
- Edge form: `(Bauteilgruppe)-[:HAT_HUERDE {evidence_url, source_quote, basis:'material_derived'}]->(Huerde)`.

### B) Project-documented (Projekt) — gold standard
- For the **33–86 projects that have a real case-study source** (FCRBE / Rotor / zirkular.net /
  academic — already in graph as `BELEGT_IN`/`ExternalLink`), the case text states the barriers the
  project actually faced. Connect only those, citing the project's own source.
- Edge form: `(Projekt)-[:HAT_HUERDE {evidence_url:<project source>, basis:'case_documented'}]->(Huerde)`.

## Honest caveat (so it stays evidence-not-generic)
- **Derived (A)** = "this barrier is *typical* for this material" (taxonomy-backed likelihood), not
  proof this project hit it — same status as the era→pollutant rules. Label it `material_derived`.
- **Documented (B)** = proof the project faced it (project source). Strongest; label `case_documented`.
- Either way, **every edge carries a real source** — unlike the current `HAT_HUERDE` (`inferiert`, 0 sources).

## Recommendation
**Rescue Huerde as a small, evidenced "Reuse-Hemmnis" vocabulary** (the ~11 market barriers, organised
by the Rakhshan 6 categories), and:
1. **Delete** all current `inferiert` `HAT_HUERDE` edges (930) + the ~13 regulatory Huerde (redundant).
2. **Reconnect** with evidence: technical barriers → Bauteilgruppe (material-derived, taxonomy-cited);
   market/organisational barriers → Projekt (case-documented where a source exists, else taxonomy-derived
   at project level).
3. Add `rw_*`-style evidence: the Rakhshan review as the backing source for the barrier vocabulary.

This is **feasible and clean** — it turns Huerde from the least-evidenced label into a sourced one.
Effort: ~1 research/extraction pass (taxonomy is done; per-project case extraction is the main work,
and only for projects that already have a source).

## Decision
- [ ] **B-clean:** rescue Huerde this way (controlled vocab + evidenced A/B connections).
- [ ] **A-simple:** still delete Huerde entirely (if the barriers axis isn't worth the extraction pass).
