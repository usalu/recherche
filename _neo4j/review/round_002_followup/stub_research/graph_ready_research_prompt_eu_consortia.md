# Graph-Ready Research Prompt — EU-Funded Research Consortia

Use this prompt to research EU-funded circular-construction research consortia and produce graph-ready Markdown dossiers with source links for every factual value.

---

## Role

You are a careful architectural research assistant preparing programme dossiers for a circular-construction knowledge graph.

Your output must be structured for direct translation into graph nodes and relationships. These projects are **multi-partner research consortia** — the core node is `Programm`, not `Bauwerk`. Pilot buildings produced by the consortium are listed by name so they can be linked separately.

---

## Input files to consult

- `README.md` for workflow and categories to gather.
- `GRAPH_SCHEMA.md` for the full graph schema, controlled vocabulary IDs, node labels, relationship names, and property names.

Do not invent schema categories. Use only the node labels, relationship names, and property names from `GRAPH_SCHEMA.md`.

---

## Critical rules

1. **Every factual value must have a source link in the same row.**
2. If a value cannot be verified from a reliable public source, write `unknown`.
3. Do not guess, infer, or treat search hypotheses as facts.
4. Keep hypotheses only in the `Search hypotheses checked` or `Negative findings` sections.
5. Prefer primary sources:
   - CORDIS for Horizon-funded projects (cordis.europa.eu)
   - Interreg programme websites (nweurope.eu for North-West Europe)
   - Programme deliverable PDFs (usually open-access)
   - Consortium partner websites
   - Official press releases
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

1. `FCRBE_Facilitating_Circulation_Reclaimed_Building_Elements.md`
2. `Interreg_NWE_FCRBE.md` — **Note:** projects 1 and 2 almost certainly refer to the same programme. If confirmed, produce one combined dossier for both and leave project 2 as a short duplicate note only.
3. `REBRIDGE_Structural_Reuse.md`
4. `Reuse_Logistics.md` — **Note:** if this project cannot be identified as a discrete initiative, produce a short negative-finding dossier instead.

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
| duplicate_of | value or unknown | [S1](URL) |
| alternative_candidates_checked | value or unknown | [S1](URL) |

---

## Programm

| Property | Value | Source |
|---|---|---|
| name | value or unknown | [S1](URL) |
| alternative_names | value or unknown | [S1](URL) |
| type | research consortium / Interreg / Horizon / national programme / other | [S1](URL) |
| lead_organisation | value or unknown | [S1](URL) |
| start_year | value or unknown | [S1](URL) |
| end_year | value or unknown | [S1](URL) |
| status | active / concluded / ongoing | [S1](URL) |
| eu_funding_programme | value or unknown | [S1](URL) |
| grant_agreement_reference | value or unknown | [S1](URL) |
| total_budget_eur | value or unknown | [S1](URL) |
| eu_contribution_eur | value or unknown | [S1](URL) |
| short_description | value or unknown | [S1](URL) |

---

## Geographic nodes

| Node label | Property | Value | Source |
|---|---|---|---|
| Land | name | value or unknown | [S1](URL) |
| Stadt | name | value or unknown | [S1](URL) |

---

## Akteure (all partner organisations and key individuals)

Include already linked actors first. Add newly discovered actors only if they are supported by a source.

| Actor | Akteurtyp | Rolle / Akteurrolle | Country | Evidence | Source |
|---|---|---|---|---|---|
| value or unknown | value or unknown | value or unknown | value or unknown | short claim | [S1](URL) |

---

## Pilot buildings produced

List any built projects produced by or within this consortium. Each becomes a separate Bauwerk node linked via TEIL_VON_PROGRAMM.

| Project name | City / Country | Status | Already in archive? | Notes | Source |
|---|---|---|---|---|---|
| value or unknown | value or unknown | built / planned / unknown | yes / no / unknown | short note | [S1](URL) |

---

## Published outputs and tools (Quelle / Software / Tool)

| Title / Name | Type | Publisher | Year | DOI / URL | Source |
|---|---|---|---|---|---|
| value or unknown | deliverable / toolkit / platform / dataset / paper / other | value or unknown | value or unknown | URL or unknown | [S1](URL) |

---

## Methods and regulatory approaches

| Category | Value | Evidence | Source |
|---|---|---|---|
| Methode | value or unknown | short claim | [S1](URL) |
| WiederverwendungsArt | value or unknown | short claim | [S1](URL) |
| Bauproduktstatus | value or unknown | short claim | [S1](URL) |
| Norm | value or unknown | short claim | [S1](URL) |
| Software | value or unknown | short claim | [S1](URL) |
| Tool | value or unknown | short claim | [S1](URL) |

---

## Funding and institutional context

| Field | Value | Evidence | Source |
|---|---|---|---|
| funding_body | value or unknown | short claim | [S1](URL) |
| grant_reference | value or unknown | short claim | [S1](URL) |
| parent_programme | value or unknown | short claim | [S1](URL) |
| follow_on_programmes | value or unknown | short claim | [S1](URL) |
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

Research the following four EU-funded consortia.

---

## 1. FCRBE — Facilitating the Circulation of Reclaimed Building Elements

### Already linked graph actors

Use these as research anchors and include them first in the `Akteure` table:

| Actor | Status |
|---|---|
| Hugo Topalov | already linked graph node |
| Sarah Westerfeld | already linked graph node |

### Task

Produce `FCRBE_Facilitating_Circulation_Reclaimed_Building_Elements.md` using the exact dossier template above. List all pilot buildings in the built-demonstrators table. Confirm whether `prog_fcrbe` in the graph already captures this data or needs updating.

---

## 2. Interreg NWE FCRBE

### Already linked graph actors

Use these as research anchors and include them first in the `Akteure` table:

| Actor | Status |
|---|---|
| Michaël Ghyoot | already linked graph node |

### Task

Confirm whether this is the same programme as project 1. If confirmed, produce `Interreg_NWE_FCRBE.md` as a short duplicate note (≈ 1 page) documenting the overlap, cross-referencing `FCRBE_Facilitating_Circulation_Reclaimed_Building_Elements.md`, and stating Michaël Ghyoot's specific role. Do not duplicate all tables. If research reveals a distinct programme, produce a full dossier using the template above.

---

## 3. REBRIDGE structural reuse project

### Already linked graph actors

Use these as research anchors and include them first in the `Akteure` table:

| Actor | Status |
|---|---|
| Corentin Fivet | already linked graph node |

### Task

Produce `REBRIDGE_Structural_Reuse.md` using the exact dossier template above.

---

## 4. Reuse Logistics

### Already linked graph actors

Use these as research anchors and include them first in the `Akteure` table:

| Actor | Status |
|---|---|
| Madlen Kobi | already linked graph node |

### Task

Attempt to identify a discrete project behind the name "Reuse Logistics" with Madlen Kobi as a linked actor. If identified, produce `Reuse_Logistics.md` using the full dossier template above. If no discrete project can be identified after reasonable research, produce `Reuse_Logistics.md` as a short negative-finding dossier. Mark `identified_programme` as `no` and `research_status` as `unresolved`. The entry may be re-categorised or deleted at integration.

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
- [ ] All consortium partner organisations are listed in the Akteure table.
- [ ] Built demonstrators / pilot buildings are listed by name in the dedicated table.
- [ ] The FCRBE / Interreg NWE FCRBE duplicate is explicitly resolved.
- [ ] Ambiguous programme identification is clearly documented.
- [ ] Negative findings are included.
- [ ] Source conflicts are noted if present.
