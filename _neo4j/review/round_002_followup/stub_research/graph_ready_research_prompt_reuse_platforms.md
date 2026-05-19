# Graph-Ready Research Prompt — Reuse Platforms and Matching Tools

Use this prompt to research digital reuse platforms, material-exchange operators, and matching tools, and produce graph-ready Markdown dossiers with source links for every factual value.

---

## Role

You are a careful architectural research assistant preparing dossiers for a circular-construction knowledge graph.

Your output must be structured for direct translation into graph nodes and relationships. These entries are **platform operators and digital tools** — the core nodes are `Akteur` (the operating organisation) and `Software` or `Tool` (the platform itself), not `Bauwerk` or `Programm`.

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
   - official platform website
   - company registration databases (Infogreffe, KvK, Handelsregister, Companies House)
   - funder pages (ADEME, Région, BPI France, etc.)
   - peer-reviewed publications citing the platform
   - press coverage and interviews with named founders
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
11. If a platform cannot be unambiguously identified, document that clearly under `Identification status`.
12. Keep factual claims short and atomic so each claim can be traced to a source.
13. Do not cite a source unless it directly supports the value in that row.
14. If several sources disagree, report the conflict in `Source conflicts`.

---

## Required deliverables

Produce one finished `.md` dossier per platform:

1. `REFAIR_Bordeaux.md`
2. `RCMI_Concular.md` — **Note:** if RCMI turns out to be a Concular workflow feature rather than a distinct entity, produce a short cross-reference dossier instead of a full dossier.

Each dossier must follow the exact structure below.

---

# Dossier template

```markdown
# [Platform / Operator name]

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
| identified_entity | yes / no / uncertain | [S1](URL) |
| verified_name | value or unknown | [S1](URL) |
| alternative_names | value or unknown | [S1](URL) |
| entity_type | platform operator / tool only / workflow feature / other | [S1](URL) |
| reason_for_identification | short explanation or unknown | [S1](URL) |
| reduces_to_existing_node | value or unknown | [S1](URL) |
| alternative_candidates_checked | value or unknown | [S1](URL) |

---

## Akteur (operating organisation)

| Property | Value | Source |
|---|---|---|
| name | value or unknown | [S1](URL) |
| alternative_names | value or unknown | [S1](URL) |
| akteurtyp | at_materialhub_bauteilboerse / at_software_tool_anbieter / at_forschungseinrichtung / other | [S1](URL) |
| legal_form | value or unknown | [S1](URL) |
| registration_number | value or unknown | [S1](URL) |
| founded_year | value or unknown | [S1](URL) |
| headquarters_city | value or unknown | [S1](URL) |
| headquarters_country | value or unknown | [S1](URL) |
| website | value or unknown | [S1](URL) |
| short_description | value or unknown | [S1](URL) |

---

## Software / Tool node

| Property | Value | Source |
|---|---|---|
| platform_name | value or unknown | [S1](URL) |
| node_type | Software / Tool / both | [S1](URL) |
| platform_type | marketplace / inventory / matching / assessment / other | [S1](URL) |
| current_url | value or unknown | [S1](URL) |
| first_published | value or unknown | [S1](URL) |
| last_updated | value or unknown | [S1](URL) |
| open_access | yes / no / freemium / unknown | [S1](URL) |
| data_standard_used | value or unknown | [S1](URL) |
| short_description | value or unknown | [S1](URL) |

---

## Geographic nodes

| Node label | Property | Value | Source |
|---|---|---|---|
| Land | name | value or unknown | [S1](URL) |
| Region | name | value or unknown | [S1](URL) |
| Stadt | name | value or unknown | [S1](URL) |

---

## Akteure (people)

Include already linked actors first. Add newly discovered actors only if they are supported by a source.

| Person | Role | Organisation | Evidence | Source |
|---|---|---|---|---|
| value or unknown | value or unknown | value or unknown | short claim | [S1](URL) |

---

## Scale and throughput

| Field | Value | Evidence | Source |
|---|---|---|---|
| geographic_scope | regional / national / European / global / unknown | short claim | [S1](URL) |
| active_seller_organisations | value or unknown | short claim | [S1](URL) |
| active_buyer_organisations | value or unknown | short claim | [S1](URL) |
| approx_listings_at_peak | value or unknown | short claim | [S1](URL) |
| physical_depot | yes / no / unknown | short claim | [S1](URL) |
| depot_address | value or unknown | short claim | [S1](URL) |

---

## Funding and institutional context

| Field | Value | Evidence | Source |
|---|---|---|---|
| funding_body | value or unknown | short claim | [S1](URL) |
| grant_reference | value or unknown | short claim | [S1](URL) |
| revenue_model | value or unknown | short claim | [S1](URL) |
| public_funding_share | value or unknown | short claim | [S1](URL) |
| industry_partners | value or unknown | short claim | [S1](URL) |

---

## Linked case studies (buildings or projects using this platform)

| Project name | City / Country | Already in archive? | Notes | Source |
|---|---|---|---|---|
| value or unknown | value or unknown | yes / no / unknown | short note | [S1](URL) |

---

## Relationships

Only include relationships that are supported by direct evidence. Use graph relationship names exactly.

| Subject node | Relationship | Object node | Evidence | Source |
|---|---|---|---|---|
| value or unknown | NUTZT_SOFTWARE | value or unknown | short claim | [S1](URL) |
| value or unknown | NUTZT_TOOL | value or unknown | short claim | [S1](URL) |
| value or unknown | GEHÖRT_ZU | value or unknown | short claim | [S1](URL) |
| value or unknown | ERHALT_FOERDERUNG_DURCH | value or unknown | short claim | [S1](URL) |
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

# Platform batch

Research the following two platform entries.

---

## 1. REFAIR — Bordeaux reuse platform

### Already linked graph actors

Use these as research anchors and include them first in the `Akteure` table:

| Actor | Status |
|---|---|
| Orianne Scourzic | already linked graph node |
| Tiphaine Berthomé | already linked graph node |

### Search hypotheses

The following are only hypotheses. Verify or reject them using sources:

- REFAIR is a physical and/or online reuse platform based in the Bordeaux metropolitan area, Région Nouvelle-Aquitaine, France.
- The platform may operate a physical depot or showroom alongside an online listing service.
- Primary funders may include ADEME, Région Nouvelle-Aquitaine, and Bordeaux Métropole.
- Orianne Scourzic and/or Tiphaine Berthomé may be co-founders or key staff.
- The platform may be registered as an association (loi 1901), SCOP, or SAS.
- The platform may be linked to Cd2e (Centre de Ressources Technologies Propres) or the Cluster Eskal Eureka.
- A commercial listing tool or data standard may have been developed in-house or adapted from an existing one.

### Task

Produce `REFAIR_Bordeaux.md` using the exact dossier template above.

---

## 2. RCMI / Concular blueprint

### Already linked graph actors

Use these as research anchors and include them first in the `Akteure` table:

| Actor | Status |
|---|---|
| Dominik Campanella | already linked graph node |

### Search hypotheses

The following are only hypotheses. Verify or reject them using sources:

- RCMI may stand for "Reverse Construction Material Inventory" or similar — a Concular audit-and-inventory workflow.
- If so, RCMI is not a separate entity but a product, feature, or methodology within the Concular platform.
- Concular GmbH is a Berlin-based construction-material platform with Dominik Campanella as a co-founder or key figure.
- If RCMI is confirmed as a workflow or product feature (not a separate company or programme), the dossier should reduce to a cross-reference note: document the relationship clearly and point to the existing Concular node rather than creating a duplicate.
- If RCMI is a distinct project, initiative, or pilot with its own identity, produce a full dossier.

### Task

Research whether RCMI has an independent identity separate from Concular. Based on findings:

- **If RCMI is a Concular feature / workflow:** produce `RCMI_Concular.md` as a short cross-reference dossier (≈ 1–2 pages). State clearly under `Identification status` that RCMI reduces to the existing Concular node. Document what the feature/workflow does, who developed it, and in what context. Dominik Campanella's role must be sourced.
- **If RCMI is an independent entity:** produce a full `RCMI_Concular.md` using the dossier template above.

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
- [ ] The `Akteur` (operator) and `Software`/`Tool` nodes are clearly distinguished.
- [ ] Geographic scope and any physical depot are documented.
- [ ] The RCMI / Concular duplicate question is explicitly resolved.
- [ ] Linked case studies are listed if known.
- [ ] Ambiguous identification is clearly documented.
- [ ] Negative findings are included.
- [ ] Source conflicts are noted if present.
