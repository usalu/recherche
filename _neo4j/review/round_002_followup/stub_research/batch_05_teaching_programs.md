# Batch 5 — Teaching / research programmes (4 projects)

**Workflow + categories to gather:** see [README.md](README.md).
**Full graph schema (node labels, controlled vocabularies, property names):** see [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md).

## Graph nodes to populate

These are **research or teaching programmes** — the core node is `Programm`. Fill as many of the following node types and their properties as the public record allows. Consult [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for all controlled-vocabulary IDs and property names.

**Core node:** `Programm`

**Linked nodes:** `Akteur` (+ `Akteurrolle` + `Akteurtyp` + `GEHÖRT_ZU`) · `Land` · `Stadt` · `Methode` · `WiederverwendungsArt` · `Software` · `Tool` · `Quelle` · `Norm`

**Relationships:** `BETEILIGT_AN` · `GEHÖRT_ZU` · `ERHALT_FOERDERUNG_DURCH` · `TEIL_VON_PROGRAMM` (link built demonstrators) · `NUTZT_SOFTWARE` · `NUTZT_TOOL` · `LIEGT_IN_LAND`

**Also list** any built demonstrators by name so they can be linked as `Bauwerk` nodes via `TEIL_VON_PROGRAMM`. The actors under "Already linked" are known graph nodes — use them as research anchors. **Every factual claim needs a source citation. Unknown → write "unknown".**

---

## 1. ETH Circular Construction — student-reuse demonstrator track

**Already linked:** Catherine De Wolf, Fabio Gramazio, Matthias Kohler.

**Plausible starting context:** ETH Zürich's circular-construction track, led by **Prof. Catherine De Wolf** at the **Circular Engineering for Architecture (CEA)** chair (established 2021). Gramazio Kohler Research is ETH's robotics-driven design + construction lab — they collaborate with CEA on demonstrators that combine reuse with computational fabrication.

**Task:** Produce a dossier filling as many graph nodes and properties as possible. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## 2. Reuse in Construction / ZHAW

**Already linked:** Andreas Sonderegger, Eva Stricker, Guido Brandi, ZHAW.

**Plausible starting context:** ZHAW Zürcher Hochschule für Angewandte Wissenschaften — specifically the **Institut für Konstruktives Entwerfen (IKE)** at Departement Architektur, Gestaltung und Bauingenieurwesen in Winterthur. **Eva Stricker** has led ZHAW's reuse research compendium — the foundational Swiss reference work on direct reuse, with detailed case studies of K.118 and many other Swiss buildings. Andreas Sonderegger and Guido Brandi are ZHAW colleagues.

**Task:** Produce a dossier filling as many graph nodes and properties as possible. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## 3. Architecture of Reuse Brussels

**Already linked:** Christine Conix, Lionel Devlieger, Maarten Gielen.

**Plausible starting context:** A teaching programme or design studio in Brussels jointly run by **Rotor** (Devlieger + Gielen, the cooperative behind Rotor DC and Opalis) and **CONIX RDBM Architects** (Christine Conix, an Antwerp-based firm with reuse practice). Host institution is most likely **KU Leuven Faculty of Architecture** (Brussels Campus), **ULB La Cambre**, or **Sint-Lucas School of Architecture**.

**Task:** Produce a dossier filling as many graph nodes and properties as possible. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## 4. Vandkunsten Reused Construction Materials / Component Reuse

**Already linked:** Katrine West Kristensen, Søren Nielsen, Vandkunsten.

**Plausible starting context:** **Vandkunsten Architects** (Copenhagen, founded 1970) — a long-established Danish firm with a strong sustainability and reuse practice. **Søren Nielsen** is a partner / senior researcher known for circular-construction R&D at the firm, notably the **Upcycle House** and **Upcycle Studios** projects in Copenhagen. Katrine West Kristensen is a Vandkunsten researcher in this stream. This stub likely refers to a multi-year Vandkunsten R&D programme on component reuse, very probably co-funded by **Realdania** (the Danish philanthropic foundation that funds most of the country's experimental architecture R&D).

**Task:** Produce a dossier filling as many graph nodes and properties as possible. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## What to do with the dossiers once written

Hand each finished `.md` file back. For these four entries: the dossier itself does not need a Bauteil-Inventar or Quality/Defects section — those apply to the built outputs of the programme, which are separate case studies. The programme dossier should however **list those built outputs by name** so I can cross-link them in the graph if they're already documented or flag them as future case-study candidates.
