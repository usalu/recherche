# Batch 7 — Reuse platforms / matching tools (2 projects)

**Workflow + categories to gather:** see [README.md](README.md).
**Full graph schema (node labels, controlled vocabularies, property names):** see [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md).

These two entries are **digital platforms / matching tools** for reused building components, not buildings themselves. They are operators of a marketplace, a directory, or a software service. The dossier sections that apply are:

- Identification (platform name, operator, country, web presence, founding year)
- People and organizations (founders, current team, owner / parent organization, board)
- Operating model (free directory? brokered transactions? subscription? consultancy bundled?)
- Material focus (any building component, or specific categories — bricks, steel, glass, finishes?)
- Geographic scope (city, region, country, multi-country, EU-wide)
- Throughput / scale (number of listings, transaction volume in € or t, number of registered dealers / sellers / buyers — published figures only)
- Funding model (private equity, grants, programme-level funding, ticket / commission income)
- Sustainability / business outcomes claimed (CO₂ saved through brokered transactions, material tonnage matched)
- Linked case studies our archive may already cover where the platform mediated material sourcing (e.g. Madaster ↔ Liander Alliander HQ, Concular ↔ AWM Münster, Rotor DC ↔ Multi Brussels)
- Notable users / clients
- Sources for everything

Like teaching programmes and EU consortia, these dossiers do not need a Bauteil-Inventar or Quality/Defects section — those apply to the specific buildings the platform serves, which are separate case studies.

## Graph nodes to populate

These are **digital platforms or material-exchange operators** — the core nodes are `Akteur` (Akteurtyp → `at_materialhub_bauteilboerse` or `at_software_tool_anbieter`) and `Software` or `Tool`. Fill as many of the following node types and their properties as the public record allows. Consult [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for all controlled-vocabulary IDs and property names.

**Core nodes:** `Akteur` · `Software` · `Tool`

**Linked nodes:** `Beschaffungsweg` (which acquisition paths this platform enables) · `Methode` · `Land` · `Stadt` · `Programm` (funding programme) · `Quelle`

**Relationships:** `NUTZT_SOFTWARE` / `NUTZT_TOOL` (from projects that used this platform) · `GEHÖRT_ZU` · `ERHALT_FOERDERUNG_DURCH` · `LIEGT_IN_LAND`

The actors under "Already linked" are known graph nodes — use them as research anchors. **Every factual claim needs a source citation. Unknown → write "unknown".**

---

## 1. REFAIR Bordeaux reuse platform

**Already linked:** Orianne Scourzic, Tiphaine Berthomé.

**Plausible starting context:** Regional reuse-materials platform in the Bordeaux area (Nouvelle-Aquitaine, France). Likely operated by an association, cooperative, or local-government-backed entity. Both linked actors are French; Tiphaine Berthomé works on circular-construction projects in Nouvelle-Aquitaine. French regional reuse platforms typically receive seed funding from **ADEME** (Agence de la Transition Écologique), **Région Nouvelle-Aquitaine**, and **Bordeaux Métropole**.

**Task:** Produce a dossier filling as many graph nodes and properties as possible. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## 2. RCMI / Concular blueprint project

**Already linked:** Dominik Campanella.

**Plausible starting context:** **Concular** GmbH (Berlin) is a German reuse-matching platform founded by **Dominik Campanella** and Julius Schäufele, founded ~2019–2020, spun out of the Restado project. Concular operates a digital marketplace for reused building components in Germany and is one of the most-used reuse platforms in our archive (it shows up in AWM Münster, Impact Hub Berlin fit-out, and several other case studies). "RCMI" likely abbreviates a Concular sub-product or workflow — best guesses:
- **Reverse Construction Material Inventory** (a pre-demolition audit deliverable)
- **Reused Construction Material Index** (a price / availability index)
- A specific blueprint method that Concular markets as a service

**Task:** Produce a dossier filling as many graph nodes and properties as possible. If research shows RCMI is a Concular service rather than a separate entity, document that clearly — the entry can be reduced to a cross-reference to the existing Concular node at integration. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## What to do with the dossiers once written

Hand each finished `.md` file back. For RCMI: if research shows it is simply a Concular service rather than a separate organization, the dossier can be short — a few paragraphs documenting that "RCMI = Concular's audit deliverable" — and the entry can be reduced to a cross-reference to the existing Concular node at the integration step.
