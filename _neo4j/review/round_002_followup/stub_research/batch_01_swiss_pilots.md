# Batch 1 — Swiss case-study pilots (3 projects)

**Workflow + categories to gather:** see [README.md](README.md).
**Full graph schema (node labels, controlled vocabularies, property names):** see [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md).
**Reference example (depth + structure):** [`K118_Kopfbau_Halle_118_Winterthur.md`](../../../../_archive/research/gebaeude/K118_Kopfbau_Halle_118_Winterthur.md).

## Graph nodes to populate

These are **physical buildings** — the core node is `Bauwerk`. Fill as many of the following node types and their properties as the public record allows. Consult [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for all controlled-vocabulary IDs and property names.

**Core nodes:** `Bauwerk` · `Akteur` (+ `Akteurrolle` + `Akteurtyp` + `GEHÖRT_ZU`) · `Bauteilgruppe`

**Per component batch:** `Bauteiltyp` · `Materialgruppe` · `WiederverwendungsArt` · `Beschaffungsweg` · `Rueckbauverfahren` · `Aufbereitungsverfahren` · `Verbindungstechnik` · `Logistik` · `Defekt` · `ZustandsKlasse` · `PruefungNachweis` · `Leistungsanforderung` · `Bauproduktstatus` · `Schadstoff`

**Per building:** `BauaufgabeIntervention` · `Nutzung` · `Bauobjektrolle` · `Bauobjektklasse` · `ZertifizierungBewertungssystem` · `Methode` · `Norm` · `LebenszyklusModul` · `Marktmodell` · `Akzeptanz` · `Huerde` · `HuerdeKategorie` · `Programm` · `Software` · `Tool` · `Wirtschaft`

**Geographic:** `Stadt` · `Land`

**Relationships to establish:** `BETEILIGT_AN` · `AUS_BAUWERK` · `EINGEBAUT_IN` · `LIEGT_IN_STADT` · `LIEGT_IN_LAND` · `ERHALT_FOERDERUNG_DURCH` · `TEIL_VON_PROGRAMM` · `BERECHNET_NACH_MODUL` · `HAT_WIRTSCHAFT`

The actors under "Already linked" are known graph nodes — use them as research anchors and add any newly discovered actors with their roles. **Every factual claim needs a source citation. Unknown → write "unknown".**

---

## 1. Schärenmoosstrasse Zürich

**Already linked:** Daniel Hoffmann, Gian Trachsler, Studio Trachsler Hoffmann.

**Plausible starting context:** Studio Trachsler Hoffmann is a Zürich architecture office known for reuse-led design. The street Schärenmoosstrasse runs through Zürich-Schwamendingen. The project is most likely a residential building, a school, or a mixed-use housing development on that street.

**Task:** Produce a dossier filling as many graph nodes and properties as possible. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## 2. UMAR Unit (NEST, Empa Dübendorf)

**Already linked:** Werner Sobek, Dirk E. Hebel, Felix Heisel, Vanessa Propach.

**Plausible starting context:** "UMAR" almost certainly stands for **Urban Mining and Recycling** — the experimental residential unit inside the NEST building at Empa in Dübendorf (Switzerland). Designed by Werner Sobek with Dirk Hebel and Felix Heisel (then both at ETH Zürich, now Hebel at KIT Karlsruhe), opened in 2018, designed as a fully-disassemblable demonstration. This is a well-documented case — research should be quick and thorough.

**Task:** Produce a dossier filling as many graph nodes and properties as possible. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## 3. ELEMENTA / Walkeweg Basel

**Already linked:** Carla Ferrando Costansa, Pablo Garrido Arnaiz.

**Plausible starting context:** The actor names suggest a Spanish-speaking architect duo working in Basel. "Walkeweg" is a street in Basel (Gellert / Breite district). "ELEMENTA" is also the brand name of a Swiss precast-concrete reuse system marketed by Element AG. The combination "ELEMENTA Walkeweg" most likely refers to a residential or mixed-use development on Walkeweg that uses the ELEMENTA precast-reuse system, or a building by EMI Architekten / Esch Sintzel / another Basel office.

**Task:** Produce a dossier filling as many graph nodes and properties as possible. If the project cannot be unambiguously identified, document that as a negative finding. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## What to do with the dossiers once written

Hand each finished `.md` file back. I'll handle:
- Translating it into the graph chunk (knowledge categories → nodes + relationships)
- Reconciling new actor names against the existing actor registry
- Cross-linking newly mentioned donor buildings to existing receiver projects in the graph (e.g. K.118's ELYS Basel donor is already a known node, so if your dossier mentions ELYS, that link gets made automatically)
- Promoting the project from stub to full record
