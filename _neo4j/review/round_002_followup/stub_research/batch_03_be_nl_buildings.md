# Batch 3 — Belgian / Dutch case-study buildings (3 projects)

**Workflow + categories to gather:** see [README.md](README.md).
**Full graph schema (node labels, controlled vocabularies, property names):** see [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md).
**Reference examples:** [`K118_Kopfbau_Halle_118_Winterthur.md`](../../../../_archive/research/gebaeude/K118_Kopfbau_Halle_118_Winterthur.md), [`Multi_Brussels_Reuse_in_MULTI.md`](../../../../_archive/research/gebaeude/Multi_Brussels_Reuse_in_MULTI.md), [`BlueCity_Offices_Rotterdam.md`](../../../../_archive/research/gebaeude/BlueCity_Offices_Rotterdam.md), [`Maison_DnA_Asse.md`](../../../../_archive/research/gebaeude/Maison_DnA_Asse.md).

## Graph nodes to populate

These are **physical buildings** — the core node is `Bauwerk`. Fill as many of the following node types and their properties as the public record allows. Consult [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for all controlled-vocabulary IDs and property names.

**Core nodes:** `Bauwerk` · `Akteur` (+ `Akteurrolle` + `Akteurtyp` + `GEHÖRT_ZU`) · `Bauteilgruppe`

**Per component batch:** `Bauteiltyp` · `Materialgruppe` · `WiederverwendungsArt` · `Beschaffungsweg` · `Rueckbauverfahren` · `Aufbereitungsverfahren` · `Verbindungstechnik` · `Logistik` · `Defekt` · `ZustandsKlasse` · `PruefungNachweis` · `Leistungsanforderung` · `Bauproduktstatus` · `Schadstoff`

**Per building:** `BauaufgabeIntervention` · `Nutzung` · `Bauobjektrolle` · `Bauobjektklasse` · `ZertifizierungBewertungssystem` · `Methode` · `Norm` · `LebenszyklusModul` · `Marktmodell` · `Akzeptanz` · `Huerde` · `HuerdeKategorie` · `Programm` · `Software` · `Tool` · `Wirtschaft`

**Geographic:** `Stadt` · `Land`

**Relationships to establish:** `BETEILIGT_AN` · `AUS_BAUWERK` · `EINGEBAUT_IN` · `LIEGT_IN_STADT` · `LIEGT_IN_LAND` · `ERHALT_FOERDERUNG_DURCH` · `TEIL_VON_PROGRAMM` · `BERECHNET_NACH_MODUL` · `HAT_WIRTSCHAFT`

Note: Pavilion Circl Amsterdam and Circl / ABN AMRO (projects 2 and 3) may be the same building under two names — if confirmed, produce one combined dossier and flag the duplicate explicitly.

The actors under "Already linked" are known graph nodes — use them as research anchors and add any newly discovered actors with their roles. **Every factual claim needs a source citation. Unknown → write "unknown".**

---

## 1. Careno Be.Circular

**Already linked:** Lionel Billiet, Sébastien Paulet.

**Plausible starting context:** "Be.Circular" is the Brussels-Capital regional circular-economy programme operated by Bruxelles Environnement / Leefmilieu Brussel since 2016. Be.Circular awards funding to circular-construction pilots. "Careno" most likely names a single Be.Circular-funded pilot project — could be a building, a refurbishment, a planning study, or a consultancy initiative. Both linked actors are Belgian.

**Task:** Produce a dossier filling as many graph nodes and properties as possible. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## 2. Pavilion Circl Amsterdam

**Already linked:** Hans Hammink.

**Plausible starting context:** **Circl Pavilion** at the ABN AMRO headquarters in Amsterdam-Zuid. Opened 2017. Designed by **de Architekten Cie.** with Hans Hammink as partner-in-charge. Built explicitly as a circular-economy demonstrator. Famous reused-materials inventory: denim insulation from old jeans, reclaimed window frames from old ABN AMRO offices, reclaimed door frames, reclaimed timber, reclaimed brick. Frequently cited in circular-construction literature.

**Task:** Produce a dossier filling as many graph nodes and properties as possible. If confirmed as the same building as project 3, produce one combined dossier and document the duplicate. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## 3. Circl / ABN AMRO urban mining context

**Already linked:** Michel Baars.

**Plausible starting context:** Almost certainly the same building as the Circl Pavilion above, framed here through the *urban mining supply chain* lens. Michel Baars founded **New Horizon Urban Mining** (Den Haag), the Dutch dismantling-and-resupply firm that supplied many salvaged components to Circl. This stub probably exists because the actor registry indexed the project from Baars' side rather than the architect's side.

**Task:** Produce a dossier filling as many graph nodes and properties as possible. If confirmed as the same building as project 2, produce one combined dossier and document the duplicate. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## What to do with the dossiers once written

Hand each finished `.md` file back. If your research confirms the Circl duplicate, please write **one combined dossier** for the building (filename suggestion: `Circl_Pavilion_ABN_AMRO_Amsterdam.md`) and a short note documenting that both stub names refer to it. I will handle the graph-level merge.
