# Graph-Ready Research Prompt — Teaching and Research Programmes

Use this prompt to research circular-construction teaching and research programmes and produce graph-ready Markdown dossiers with source links for every factual value.

---

## Role

You are a careful architectural research assistant preparing programme dossiers for a circular-construction knowledge graph.

Your output must be structured for direct translation into graph nodes and relationships. These projects are **not buildings** — the core node is `Programm`, not `Bauwerk`. Built demonstrators produced by the programme are listed by name so they can be linked separately.

---

## Input files to consult

- `README.md` for workflow and categories to gather.
- `GRAPH_SCHEMA.md` for the full graph schema, controlled vocabulary IDs, node labels, relationship names, and property names.
- `K118_Kopfbau_Halle_118_Winterthur.md` for structural reference only — the dossier format is adapted for programmes, not buildings.

Do not invent schema categories. Use only the node labels, relationship names, and property names from `GRAPH_SCHEMA.md`.

---

## Critical rules

1. **Every factual value must have a source link in the same row.**
2. If a value cannot be verified from a reliable public source, write `unknown`.
3. Do not guess, infer, or treat search hypotheses as facts.
4. Keep hypotheses only in the `Search hypotheses checked` or `Negative findings` sections.
5. Prefer primary sources:
   - institution project or research pages
   - funder project databases (SNSF P3, Innosuisse, CORDIS, Realdania, etc.)
   - programme-leader publications and CVs
   - official programme reports
   - course catalogues and syllabi
6. Use secondary sources only when primary sources are unavailable.
7. For every source, record:
   - source ID
   - title
   - publisher / organization
   - URL
   - access date
   - exact claim supported
8. Do not remove rows from the required tables.
9. Do not omit unknown categories.
10. Use `unknown` instead of leaving a cell blank.
11. If a programme cannot be unambiguously identified, document that clearly under `Identification status`.
12. Keep factual claims short and atomic so each claim can be traced to a source.
13. Do not cite a source unless it directly supports the value in that row.
14. If several sources disagree, report the conflict in `Source conflicts`.

---

## Required deliverables

Produce one finished `.md` dossier per programme:

1. `ETH_Circular_Construction_Programme.md`
2. `ZHAW_Reuse_in_Construction.md`
3. `Architecture_of_Reuse_Brussels.md`
4. `Vandkunsten_Component_Reuse_Programme.md`

Each dossier must follow the exact structure below.

---

# Dossier template

```markdown
# [Programme name]

## Research status

| Field | Value | Source |
|---|---|---|
| research_status | complete / partial / unresolved | [S1](URL) |
| access_date | YYYY-MM-DD | researcher entry |
| main_identification_confidence | high / medium / low | [S1](URL) |
| unresolved_questions | unknown / short list | [S1](URL) |

---

## Identification status

| Field | Value | Source |
|---|---|---|
| identified_programme | yes / no / uncertain | [S1](URL) |
| verified_programme_name | value or unknown | [S1](URL) |
| alternative_names | value or unknown | [S1](URL) |
| reason_for_identification | short explanation or unknown | [S1](URL) |
| alternative_candidates_checked | value or unknown | [S1](URL) |

---

## Programm

| Property | Value | Source |
|---|---|---|
| name | value or unknown | [S1](URL) |
| alternative_names | value or unknown | [S1](URL) |
| type | teaching / research / teaching+research / funding / other | [S1](URL) |
| host_institution | value or unknown | [S1](URL) |
| department | value or unknown | [S1](URL) |
| start_year | value or unknown | [S1](URL) |
| end_year | value or unknown | [S1](URL) |
| status | active / concluded / ongoing | [S1](URL) |
| funding_programme | value or unknown | [S1](URL) |
| funding_amount_eur | value or unknown | [S1](URL) |
| grant_reference | value or unknown | [S1](URL) |
| short_description | value or unknown | [S1](URL) |

---

## Geographic nodes

| Node label | Property | Value | Source |
|---|---|---|---|
| Land | name | value or unknown | [S1](URL) |
| Stadt | name | value or unknown | [S1](URL) |

---

## Akteure

Include already linked actors first. Add newly discovered actors only if they are supported by a source.

| Actor | Akteurtyp | Rolle / Akteurrolle | Organization / GEHÖRT_ZU | Evidence | Source |
|---|---|---|---|---|---|
| value or unknown | value or unknown | value or unknown | value or unknown | short claim | [S1](URL) |

---

## Built demonstrators

List any built projects produced by or within this programme. Each becomes a separate Bauwerk node linked via TEIL_VON_PROGRAMM. Do not describe them in full here — list names only so they can be researched or cross-linked separately.

| Project name | City / Country | Status | Already in archive? | Notes | Source |
|---|---|---|---|---|---|
| value or unknown | value or unknown | built / planned / unknown | yes / no / unknown | short note | [S1](URL) |

---

## Published outputs (Quelle)

| Title | Type | Publisher | Year | DOI / URL | Source |
|---|---|---|---|---|---|
| value or unknown | book / report / paper / dataset / other | value or unknown | value or unknown | URL or unknown | [S1](URL) |

---

## Methods and approaches

| Category | Value | Evidence | Source |
|---|---|---|---|
| Methode | value or unknown | short claim | [S1](URL) |
| WiederverwendungsArt | value or unknown | short claim | [S1](URL) |
| Software | value or unknown | short claim | [S1](URL) |
| Tool | value or unknown | short claim | [S1](URL) |
| Norm | value or unknown | short claim | [S1](URL) |

---

## Funding and institutional context

| Field | Value | Evidence | Source |
|---|---|---|---|
| funding_body | value or unknown | short claim | [S1](URL) |
| grant_reference | value or unknown | short claim | [S1](URL) |
| parent_programme | value or unknown | short claim | [S1](URL) |
| industry_partners | value or unknown | short claim | [S1](URL) |
| research_context | value or unknown | short claim | [S1](URL) |
| public_private_context | value or unknown | short claim | [S1](URL) |

---

## Relationships

Only include relationships that are supported by direct evidence. Use graph relationship names exactly.

| Subject node | Relationship | Object node | Evidence | Source |
|---|---|---|---|---|
| value or unknown | BETEILIGT_AN | value or unknown | short claim | [S1](URL) |
| value or unknown | GEHÖRT_ZU | value or unknown | short claim | [S1](URL) |
| value or unknown | ERHALT_FOERDERUNG_DURCH | value or unknown | short claim | [S1](URL) |
| value or unknown | TEIL_VON_PROGRAMM | value or unknown | short claim | [S1](URL) |
| value or unknown | NUTZT_SOFTWARE | value or unknown | short claim | [S1](URL) |
| value or unknown | NUTZT_TOOL | value or unknown | short claim | [S1](URL) |
| value or unknown | LIEGT_IN_LAND | value or unknown | short claim | [S1](URL) |

---

## Search hypotheses checked

Use this section to separate unverified starting assumptions from verified facts.

| Hypothesis | Search terms / sources checked | Result | Source |
|---|---|---|---|
| value or unknown | value or unknown | confirmed / rejected / unresolved | [S1](URL) |

---

## Negative findings

List relevant categories that were searched but could not be verified.

| Topic searched | Sources checked | Result |
|---|---|---|
| value or unknown | value or unknown | unknown / not found / ambiguous |

---

## Source conflicts

| Topic | Source A says | Source B says | Resolution |
|---|---|---|---|
| value or unknown | value or unknown | value or unknown | value or unknown |

---

## Source register

| Source ID | Title | Publisher / organization | URL | Access date | Claims supported |
|---|---|---|---|---|---|
| S1 | value | value | URL | YYYY-MM-DD | value |
```

---

# Programme batch

Research the following four teaching and research programmes.

---

## 1. ETH Circular Construction — student-reuse demonstrator track

### Already linked graph actors

Use these as research anchors and include them first in the `Akteure` table:

| Actor | Status |
|---|---|
| Catherine De Wolf | already linked graph node |
| Fabio Gramazio | already linked graph node |
| Matthias Kohler | already linked graph node |

### Search hypotheses

The following are only hypotheses. Verify or reject them using sources:

- The programme is the Circular Engineering for Architecture (CEA) chair at ETH Zürich, led by Prof. Catherine De Wolf, established 2021.
- Gramazio Kohler Research (robotics-driven design and construction) collaborates with CEA on demonstrators combining reuse with computational fabrication.
- Host department is likely D-BAUG (Department of Civil, Environmental and Geomatic Engineering).
- The programme has produced built or prototyped demonstrators including possibly ReCrete footbridge and robotic reused-timber assemblies.
- Funding may come from ETH internal sources, SNSF, and industry partners such as Holcim, Implenia, or Bouygues.

### Task

Produce `ETH_Circular_Construction_Programme.md` using the exact dossier template above.

---

## 2. Reuse in Construction / ZHAW

### Already linked graph actors

Use these as research anchors and include them first in the `Akteure` table:

| Actor | Status |
|---|---|
| Andreas Sonderegger | already linked graph node |
| Eva Stricker | already linked graph node |
| Guido Brandi | already linked graph node |
| ZHAW | already linked graph node |

### Search hypotheses

The following are only hypotheses. Verify or reject them using sources:

- The programme is based at ZHAW Zürcher Hochschule für Angewandte Wissenschaften, specifically the Institut für Konstruktives Entwerfen (IKE) in Winterthur.
- Eva Stricker leads ZHAW's reuse research compendium — the foundational Swiss reference work on direct reuse.
- Funding may be from Innosuisse, SNF, or SBFI.
- Published outputs include a ZHAW Reuse Compendium (year, ISBN, and publisher to be verified).
- Industry partners may include Zirkular GmbH, baubüro in situ, Eberhard, Implenia, or Halter.
- Stricker is a primary chronicler of K.118 and other Swiss reuse buildings already in the archive.

### Task

Produce `ZHAW_Reuse_in_Construction.md` using the exact dossier template above.

---

## 3. Architecture of Reuse Brussels

### Already linked graph actors

Use these as research anchors and include them first in the `Akteure` table:

| Actor | Status |
|---|---|
| Christine Conix | already linked graph node |
| Lionel Devlieger | already linked graph node |
| Maarten Gielen | already linked graph node |

### Search hypotheses

The following are only hypotheses. Verify or reject them using sources:

- The programme is a teaching studio or design-research programme jointly involving Rotor (Devlieger + Gielen) and CONIX RDBM Architects (Christine Conix).
- Host institution is likely KU Leuven Faculty of Architecture (Brussels Campus), ULB La Cambre, or Sint-Lucas School of Architecture.
- Format may be a semester studio, design-research initiative, or lecture series.
- Outputs may include student theses, built demonstrators, or exhibitions.
- Funding may come from the Flemish Region, EU Erasmus+, or Brussels Region.

### Task

Produce `Architecture_of_Reuse_Brussels.md` using the exact dossier template above.

---

## 4. Vandkunsten Reused Construction Materials / Component Reuse

### Already linked graph actors

Use these as research anchors and include them first in the `Akteure` table:

| Actor | Status |
|---|---|
| Katrine West Kristensen | already linked graph node |
| Søren Nielsen | already linked graph node |
| Vandkunsten | already linked graph node |

### Search hypotheses

The following are only hypotheses. Verify or reject them using sources:

- Vandkunsten Architects (Copenhagen) runs a multi-year R&D programme on component reuse, likely co-funded by Realdania (Danish philanthropic foundation).
- Søren Nielsen is a partner or senior researcher known for circular-construction R&D at the firm, notably the Upcycle House and Upcycle Studios projects.
- The programme may be titled "Reused Construction Materials", "Genbrug i Byggeri", or a similar Danish-language name.
- Specific built outputs already in our archive may include Upcycle Studios Copenhagen.
- Additional funding may come from Innovationsfonden Danmark or Bolig- og Planstyrelsen.

### Task

Produce `Vandkunsten_Component_Reuse_Programme.md` using the exact dossier template above.

---

# Final quality checklist

Before handing back each `.md` dossier, check:

- [ ] Every required section is present.
- [ ] No table cells are blank.
- [ ] Unknown values are written as `unknown`.
- [ ] Every factual value has a source link in the same row.
- [ ] The source register contains every cited source.
- [ ] Hypotheses are not presented as facts.
- [ ] Already linked actors are included first.
- [ ] Newly discovered actors have sourced roles.
- [ ] Relationships use only approved relationship names.
- [ ] Node labels and categories match `GRAPH_SCHEMA.md`.
- [ ] Built demonstrators are listed by name in the dedicated table.
- [ ] Ambiguous programme identification is clearly documented.
- [ ] Negative findings are included.
- [ ] Source conflicts are noted if present.
