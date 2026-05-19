# Batch 6 — EU-funded research consortia (4 projects)

**Workflow + categories to gather:** see [README.md](README.md).
**Full graph schema (node labels, controlled vocabularies, property names):** see [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md).

## Graph nodes to populate

These are **multi-partner research consortia** — the core node is `Programm`. FCRBE and Interreg NWE FCRBE may be the same programme under two names — if confirmed, produce a single combined dossier. Fill as many of the following node types and their properties as the public record allows. Consult [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for all controlled-vocabulary IDs and property names.

**Core node:** `Programm`

**Linked nodes:** `Akteur` (+ `Akteurrolle` + `Akteurtyp` + `GEHÖRT_ZU`) · `Land` · `Stadt` · `Methode` · `WiederverwendungsArt` · `Software` · `Tool` · `Quelle` · `Norm` · `Bauproduktstatus`

**Relationships:** `BETEILIGT_AN` · `GEHÖRT_ZU` · `ERHALT_FOERDERUNG_DURCH` · `TEIL_VON_PROGRAMM` (link built demonstrators) · `NUTZT_SOFTWARE` · `NUTZT_TOOL` · `LIEGT_IN_LAND`

**Also list** any built demonstrators or pilot buildings by name so they can be linked as `Bauwerk` nodes via `TEIL_VON_PROGRAMM`. Note: `prog_fcrbe` and `prog_interreg_nwe` already exist in the graph — confirm whether these stubs refer to the same nodes or distinct ones. The actors under "Already linked" are known graph nodes — use them as research anchors. **Every factual claim needs a source citation. Unknown → write "unknown".**

---

## 1. FCRBE — Facilitating the Circulation of Reclaimed Building Elements

**Already linked:** Hugo Topalov, Sarah Westerfeld.

**Plausible starting context:** Interreg North-West Europe project, lead by **Rotor** (Brussels). Run 2017–2022 (or thereabouts), budget ≈ €4.6 million. Partners typically include Rotor (BE, coordinator), Salvo (UK, salvage-trade umbrella), Bellastock (FR, architecture / urban research), Brussels Environment (BE, regulator), CSTC / BBRI Belgian Building Research Institute, possibly Glasgow Caledonian University. Notable outputs: **Opalis dealer directory** (opalis.eu — the European reclaimed-materials dealer index), **futureusedmaterials.eu**, ~36 pilot reuse buildings in NWE region, technical guidelines, public webinars.

**Task:** Produce a dossier filling as many graph nodes and properties as possible. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## 2. Interreg NWE FCRBE

**Already linked:** Michaël Ghyoot.

**Plausible starting context:** Almost certainly the same programme as FCRBE above. **Michaël Ghyoot** is a Rotor partner and the FCRBE project lead. This stub likely exists because the actor registry indexed the programme from the Interreg-administrative angle, while project 1 above came from the FCRBE-acronym angle.

**Task:** Confirm overlap with FCRBE (project 1). If confirmed as the same programme, produce one combined dossier. Fill as many graph nodes and properties as possible. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## 3. REBRIDGE structural reuse project

**Already linked:** Corentin Fivet.

**Plausible starting context:** Research project on structural reuse, very likely focused on **bridges** or **bridge girders** as a reuse source. **Corentin Fivet** leads the **Structural Xploration Lab (SXL)** at EPFL Fribourg, which is the leading European academic group on structural reuse — they also built the ReCrete footbridge from reused concrete. REBRIDGE may be an SNSF / Innosuisse / NCCR Digital Fabrication / Horizon Europe funded project.

**Task:** Produce a dossier filling as many graph nodes and properties as possible. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## 4. Reuse Logistics

**Already linked:** Madlen Kobi.

**Plausible starting context:** Generic-sounding name — likely a research project on **logistics for reuse** (transport, storage, broker matching) rather than a building. **Madlen Kobi** is a Swiss circular-economy researcher — affiliation likely ZHAW, HSLU Luzern, or ETH. The project may be funded by Innosuisse, SBFI, or a Swiss federal programme on construction sustainability.

**Task:** If the project can be identified as a discrete initiative, produce a dossier filling as many graph nodes and properties as possible. If it cannot be identified, document as a negative finding — the entry can be re-categorised or deleted at integration. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## What to do with the dossiers once written

Hand each finished `.md` file back. For the FCRBE / Interreg NWE FCRBE pair: if confirmed as the same programme, one combined dossier is fine (e.g. `FCRBE_Interreg_NWE.md`) with a short note documenting that both stub names refer to it. For Reuse Logistics: if identification fails, a short "negative finding" dossier is acceptable.
