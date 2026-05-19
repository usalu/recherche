# Graph-Ready Research Prompt — DE / AT / CH Large Urban Projects

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

1. `Stuttgart_210.md`
2. `LYSP8_Basel.md`
3. `Reallabor_Be_Ware.md`
4. `MedUni_Campus_Mariannengasse_Wien.md`
5. `RE_USE_Hoefe_Wien.md`

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

Research the following five building case studies.

---

## 1. Stuttgart 210

### Already linked graph actors

Use these as research anchors and include them first in the `Akteure` table:

| Actor | Status |
|---|---|
| Andreas Kretzer | already linked graph node |
| HFT Stuttgart | already linked graph node |
| HTWG Konstanz | already linked graph node |
| Katharina Raabe | already linked graph node |
| Klingelhöfer Krötsch | already linked graph node |
| Maximilian Stemmler | already linked graph node |
| Roman Kreuzer | already linked graph node |
| Stefan Krötsch | already linked graph node |
| Thomas Stark | already linked graph node |

### Search hypotheses

The following are only hypotheses. Verify or reject them using sources:

- The name "Stuttgart 210" plays on "Stuttgart 21" — likely a demonstrator using materials salvaged from Stuttgart-21 demolition sites.
- The project may be a research demonstrator, student design studio, or a built pilot building.
- The team mix (HFT Stuttgart + HTWG Konstanz + Klingelhöfer Krötsch + Thomas Stark) points to a teaching-research collaboration with a built or near-built output.
- Material donor source may be Stuttgart-21 site demolitions.

### Task

Produce `Stuttgart_210.md` using the exact dossier template above.

---

## 2. LYSP8 Basel (Lysbüchel)

### Already linked graph actors

Use these as research anchors and include them first in the `Akteure` table:

| Actor | Status |
|---|---|
| baubüro in situ | already linked graph node |
| Kerstin Müller | already linked graph node |
| Kevin Straub | already linked graph node |
| Loeliger Strub | already linked graph node |
| Marc Angst | already linked graph node |
| Marc Loeliger | already linked graph node |
| Martin Zeller | already linked graph node |
| Pascal Hentschel | already linked graph node |
| Zirkular | already linked graph node |

### Search hypotheses

The following are only hypotheses. Verify or reject them using sources:

- "LYSP8" refers to Lysbüchel, parcel 8 — an urban-transformation district in Basel-Saint-Johann.
- Lead architects are baubüro in situ and Loeliger Strub.
- Zirkular GmbH is the reuse and circularity consultant (Zirkular spun off from baubüro in situ).
- The project is likely one of the largest Swiss reuse-led mixed-use developments.
- Client may be SBB Immobilien or a Basel housing cooperative / foundation.

### Task

Produce `LYSP8_Basel.md` using the exact dossier template above.

---

## 3. Reallabor B(e) Ware

### Already linked graph actors

Use these as research anchors and include them first in the `Akteure` table:

| Actor | Status |
|---|---|
| Natural Building Lab (NBL) | already linked graph node |
| ZRS Architekten Ingenieure | already linked graph node |
| Andrea Klinge | already linked graph node |
| Christof Ziegert | already linked graph node |
| Eike Roswag-Klinge | already linked graph node |
| Matthew Crabbe | already linked graph node |
| NBL Studio | already linked graph node |
| Nina Pawlicki | already linked graph node |
| Sina Jansen | already linked graph node |
| Uwe Seiler | already linked graph node |

### Search hypotheses

The following are only hypotheses. Verify or reject them using sources:

- "Reallabor" is a German federal research format (BMBF / BBSR / Bundesstiftung Baukultur) — a real-world experimental zone with public funding.
- "B(e) Ware" plays on "Be Ware" (be aware) and "Bauen mit erprobten Waren" (building with proven goods).
- The programme is led by TU Berlin Natural Building Lab (Eike Roswag-Klinge) and ZRS Architekten (Christof Ziegert).
- It may have produced one or more built pilot buildings.
- `prog_reallabor_be_ware` is already in the graph — this stub may refer to the same node; confirm and cross-link any pilot buildings via `TEIL_VON_PROGRAMM`.

### Task

Produce `Reallabor_Be_Ware.md` using the exact dossier template above. If the programme produced multiple pilot buildings, list each under `Bauteilgruppen` only if construction details are documented; otherwise list them under `Programm` in the building-level categories table and note them as separate dossier candidates.

---

## 4. MedUni Campus Mariannengasse (Wien)

### Already linked graph actors

Use these as research anchors and include them first in the `Akteure` table:

| Actor | Status |
|---|---|
| Markus Meissner | already linked graph node |
| Thomas Romm | already linked graph node |

### Search hypotheses

The following are only hypotheses. Verify or reject them using sources:

- The project is a new medical-university campus for MedUni Wien on or near Mariannengasse, Vienna 9th district (Alsergrund).
- Thomas Romm (Forschen Planen Bauen) is involved in a reuse-driven design capacity.
- Markus Meissner is associated with Austrian sustainability and reuse projects.
- Client may be BIG Bundesimmobiliengesellschaft (Austrian federal building authority) acting for MedUni Wien.
- Reuse implementation may be at study or planning stage rather than built.

### Task

Produce `MedUni_Campus_Mariannengasse_Wien.md` using the exact dossier template above.

---

## 5. RE-USE Höfe (Wien)

### Already linked graph actors

Use these as research anchors and include them first in the `Akteure` table:

| Actor | Status |
|---|---|
| Félix Dillmann | already linked graph node |

### Search hypotheses

The following are only hypotheses. Verify or reject them using sources:

- RE-USE Höfe Wien is Vienna's public reuse-yard network, operated by city waste utility MA 48.
- Multiple "Höfe" (yards) around the city function as drop-off and low-cost resale points for usable goods.
- The network includes the 48er-Tandler flagship shop.
- This is more a programme / network than a single building — it may be best represented as a `Programm` node with multiple `Bauwerk` locations (each Hof) rather than a single `Bauwerk`.
- If the Höfe focus on furniture and household goods rather than structural building components, the connection to the reuse graph may be via `Beschaffungsweg` or `Marktmodell` rather than via component-batch nodes.

### Task

Produce `RE_USE_Hoefe_Wien.md` using the dossier template above. If your research determines this is better represented as a `Programm` node with sub-locations, document that clearly under `Identification status` and fill programme-relevant sections accordingly. Flag the schema-fit question so it can be resolved at integration.

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
