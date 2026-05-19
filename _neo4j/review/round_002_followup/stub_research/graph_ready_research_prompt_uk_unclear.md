# Graph-Ready Research Prompt — UK Buildings and Unidentified Projects

Use this prompt to research circular-construction case studies and produce graph-ready Markdown dossiers with source links for every factual value.

---

## Role

You are a careful architectural research assistant preparing building case-study dossiers for a circular-construction knowledge graph.

Your output must be structured for direct translation into graph nodes and relationships.

---

## Input files to consult

- `README.md` for workflow and categories to gather.
- `GRAPH_SCHEMA.md` for the full graph schema, controlled vocabulary IDs, node labels, relationship names, and property names.
- `K118_Kopfbau_Halle_118_Winterthur.md` as the reference example for depth and structure.
- `55_Great_Suffolk_Street_London.md`, `Holbein_Gardens_London.md`, and `Hastings_Pier_Visitor_Centre.md` as UK-specific reference examples.

Do not invent schema categories. Use only the node labels, relationship names, and property names from `GRAPH_SCHEMA.md`.

---

## Critical rules

1. **Every factual value must have a source link in the same row.**
2. If a value cannot be verified from a reliable public source, write `unknown`.
3. Do not guess, infer, or treat search hypotheses as facts.
4. Keep hypotheses only in the `Search hypotheses checked` or `Negative findings` sections.
5. Prefer primary sources:
   - architect / engineer project pages
   - client or owner pages
   - university / research institution pages
   - official reports
   - public planning documents
   - technical PDFs
   - product-system documentation
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
11. If a project cannot be unambiguously identified, document that clearly under `Identification status`.
12. Keep factual claims short and atomic so each claim can be traced to a source.
13. Do not cite a source unless it directly supports the value in that row.
14. If several sources disagree, report the conflict in `Source conflicts`.

---

## Required deliverables

Produce one finished `.md` dossier per project:

1. `Granby_Workshop_Liverpool.md`
2. `OBK_27.md` — **Note:** this project is currently unidentified. If identification fails after reasonable research, produce a short negative-finding dossier (≈ 1 page) rather than a full dossier, and mark `identified_project` as `no`.

Each dossier must follow the exact structure below.

---

# Dossier template

```markdown
# [Project name]

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
| identified_project | yes / no / uncertain | [S1](URL) |
| verified_project_name | value or unknown | [S1](URL) |
| alternative_names | value or unknown | [S1](URL) |
| reason_for_identification | short explanation or unknown | [S1](URL) |
| alternative_candidates_checked | value or unknown | [S1](URL) |

---

## Bauwerk

| Property | Value | Source |
|---|---|---|
| name | value or unknown | [S1](URL) |
| alternative_names | value or unknown | [S1](URL) |
| address | value or unknown | [S1](URL) |
| street | value or unknown | [S1](URL) |
| postal_code | value or unknown | [S1](URL) |
| city | value or unknown | [S1](URL) |
| country | value or unknown | [S1](URL) |
| latitude_longitude | value or unknown | [S1](URL) |
| year_design | value or unknown | [S1](URL) |
| year_construction_start | value or unknown | [S1](URL) |
| year_completed | value or unknown | [S1](URL) |
| year_opened | value or unknown | [S1](URL) |
| current_status | value or unknown | [S1](URL) |
| building_type | value or unknown | [S1](URL) |
| bauaufgabe_intervention | value or unknown | [S1](URL) |
| bauobjektrolle | value or unknown | [S1](URL) |
| bauobjektklasse | value or unknown | [S1](URL) |
| use / nutzung | value or unknown | [S1](URL) |
| gross_floor_area | value or unknown | [S1](URL) |
| site_area | value or unknown | [S1](URL) |
| volume | value or unknown | [S1](URL) |
| number_of_storeys | value or unknown | [S1](URL) |
| number_of_units | value or unknown | [S1](URL) |
| construction_system | value or unknown | [S1](URL) |
| circularity_relevance | value or unknown | [S1](URL) |
| short_description | value or unknown | [S1](URL) |

---

## Geographic nodes

| Node label | Property | Value | Source |
|---|---|---|---|
| Stadt | name | value or unknown | [S1](URL) |
| Land | name | value or unknown | [S1](URL) |

---

## Akteure

Include already linked actors first. Add newly discovered actors only if they are supported by a source.

| Actor | Akteurtyp | Rolle / Akteurrolle | Organization / GEHÖRT_ZU | Evidence | Source |
|---|---|---|---|---|---|
| value or unknown | value or unknown | value or unknown | value or unknown | short claim | [S1](URL) |

---

## Bauteilgruppen / component batches

Create one row for every reused, recycled, circular, demountable, separable, or specially sourced component batch.

| Bauteilgruppe | Bauteiltyp | Materialgruppe | WiederverwendungsArt | Beschaffungsweg | Evidence | Source |
|---|---|---|---|---|---|---|
| value or unknown | value or unknown | value or unknown | value or unknown | value or unknown | short claim | [S1](URL) |

---

## Component technical properties

| Bauteilgruppe | Rueckbauverfahren | Aufbereitungsverfahren | Verbindungstechnik | Logistik | Evidence | Source |
|---|---|---|---|---|---|---|
| value or unknown | value or unknown | value or unknown | value or unknown | value or unknown | short claim | [S1](URL) |

---

## Quality, compliance, and risk

| Bauteilgruppe | Defekt | ZustandsKlasse | PruefungNachweis | Leistungsanforderung | Bauproduktstatus | Schadstoff | Evidence | Source |
|---|---|---|---|---|---|---|---|---|
| value or unknown | value or unknown | value or unknown | value or unknown | value or unknown | value or unknown | value or unknown | short claim | [S1](URL) |

---

## Building-level graph categories

| Category | Value | Evidence | Source |
|---|---|---|---|
| ZertifizierungBewertungssystem | value or unknown | short claim | [S1](URL) |
| Methode | value or unknown | short claim | [S1](URL) |
| Norm | value or unknown | short claim | [S1](URL) |
| LebenszyklusModul | value or unknown | short claim | [S1](URL) |
| Marktmodell | value or unknown | short claim | [S1](URL) |
| Akzeptanz | value or unknown | short claim | [S1](URL) |
| Huerde | value or unknown | short claim | [S1](URL) |
| HuerdeKategorie | value or unknown | short claim | [S1](URL) |
| Programm | value or unknown | short claim | [S1](URL) |
| Software | value or unknown | short claim | [S1](URL) |
| Tool | value or unknown | short claim | [S1](URL) |
| Wirtschaft | value or unknown | short claim | [S1](URL) |

---

## Funding, program, and institutional context

| Field | Value | Evidence | Source |
|---|---|---|---|
| funding_body | value or unknown | short claim | [S1](URL) |
| program | value or unknown | short claim | [S1](URL) |
| research_context | value or unknown | short claim | [S1](URL) |
| client_or_owner | value or unknown | short claim | [S1](URL) |
| public_private_context | value or unknown | short claim | [S1](URL) |

---

## Economy / Wirtschaft

| Field | Value | Evidence | Source |
|---|---|---|---|
| cost_total | value or unknown | short claim | [S1](URL) |
| cost_reuse_related | value or unknown | short claim | [S1](URL) |
| cost_comparison | value or unknown | short claim | [S1](URL) |
| business_model | value or unknown | short claim | [S1](URL) |
| market_model | value or unknown | short claim | [S1](URL) |
| economic_barriers | value or unknown | short claim | [S1](URL) |
| economic_benefits | value or unknown | short claim | [S1](URL) |

---

## Relationships

Only include relationships that are supported by direct evidence. Use graph relationship names exactly.

| Subject node | Relationship | Object node | Evidence | Source |
|---|---|---|---|---|
| value or unknown | BETEILIGT_AN | value or unknown | short claim | [S1](URL) |
| value or unknown | AUS_BAUWERK | value or unknown | short claim | [S1](URL) |
| value or unknown | EINGEBAUT_IN | value or unknown | short claim | [S1](URL) |
| value or unknown | LIEGT_IN_STADT | value or unknown | short claim | [S1](URL) |
| value or unknown | LIEGT_IN_LAND | value or unknown | short claim | [S1](URL) |
| value or unknown | ERHALT_FOERDERUNG_DURCH | value or unknown | short claim | [S1](URL) |
| value or unknown | TEIL_VON_PROGRAMM | value or unknown | short claim | [S1](URL) |
| value or unknown | BERECHNET_NACH_MODUL | value or unknown | short claim | [S1](URL) |
| value or unknown | HAT_WIRTSCHAFT | value or unknown | short claim | [S1](URL) |

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

# Project batch

Research the following two case studies. Confidence and accurate sourcing take priority over completeness, especially for project 2.

---

## 1. Granby Workshop (Liverpool)

### Already linked graph actors

Use these as research anchors and include them first in the `Akteure` table:

| Actor | Status |
|---|---|
| Lewis Jones | already linked graph node |

### Task

Produce `Granby_Workshop_Liverpool.md` using the exact dossier template above. If the stub covers both the Workshop and the housing restoration, document both aspects within the same dossier and flag the disambiguation under `Identification status`.

---

## 2. OBK 27

### Already linked graph actors

Use these as research anchors and include them first in the `Akteure` table:

| Actor | Status |
|---|---|
| Cyril Pressacco | already linked graph node |
| Thibaut Barrault | already linked graph node |

### Task

First, attempt to identify the project by cross-referencing Barrault Pressacco's portfolio. If identified, produce `OBK_27.md` using the full dossier template above. If the project cannot be identified after reasonable research, produce `OBK_27.md` as a short negative-finding dossier documenting what was checked — do not invent details. Mark `identified_project` as `no` and `research_status` as `unresolved`. The entry may be deleted at integration.

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
- [ ] Ambiguous project identification is clearly documented.
- [ ] Negative findings are included.
- [ ] Source conflicts are noted if present.
- [ ] For OBK 27: if unidentified, the file is clearly labelled as a negative finding.
