# Batch 4 — UK + unidentified (2 projects)

**Workflow + categories to gather:** see [README.md](README.md).
**Full graph schema (node labels, controlled vocabularies, property names):** see [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md).
**Reference UK examples in archive:** [`55_Great_Suffolk_Street_London.md`](../../../../_archive/research/gebaeude/55_Great_Suffolk_Street_London.md), [`Holbein_Gardens_London.md`](../../../../_archive/research/gebaeude/Holbein_Gardens_London.md), [`Hastings_Pier_Visitor_Centre.md`](../../../../_archive/research/gebaeude/Hastings_Pier_Visitor_Centre.md).

## Graph nodes to populate

These are **physical buildings** — the core node is `Bauwerk`. Fill as many of the following node types and their properties as the public record allows. Consult [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for all controlled-vocabulary IDs and property names.

**Core nodes:** `Bauwerk` · `Akteur` (+ `Akteurrolle` + `Akteurtyp` + `GEHÖRT_ZU`) · `Bauteilgruppe`

**Per component batch:** `Bauteiltyp` · `Materialgruppe` · `WiederverwendungsArt` · `Beschaffungsweg` · `Rueckbauverfahren` · `Aufbereitungsverfahren` · `Verbindungstechnik` · `Logistik` · `Defekt` · `ZustandsKlasse` · `PruefungNachweis` · `Leistungsanforderung` · `Bauproduktstatus` · `Schadstoff`

**Per building:** `BauaufgabeIntervention` · `Nutzung` · `Bauobjektrolle` · `Bauobjektklasse` · `ZertifizierungBewertungssystem` · `Methode` · `Norm` · `LebenszyklusModul` · `Marktmodell` · `Akzeptanz` · `Huerde` · `HuerdeKategorie` · `Programm` · `Software` · `Tool` · `Wirtschaft`

**Geographic:** `Stadt` · `Land`

**Relationships to establish:** `BETEILIGT_AN` · `AUS_BAUWERK` · `EINGEBAUT_IN` · `LIEGT_IN_STADT` · `LIEGT_IN_LAND` · `ERHALT_FOERDERUNG_DURCH` · `TEIL_VON_PROGRAMM` · `BERECHNET_NACH_MODUL` · `HAT_WIRTSCHAFT`

Note: OBK 27 (project 2) is unidentified — confidence is the priority; if identification fails, document it as a negative finding. The actors under "Already linked" are known graph nodes — use them as research anchors and add any newly discovered actors with their roles. **Every factual claim needs a source citation. Unknown → write "unknown".**

---

## 1. Granby Workshop (Liverpool)

**Already linked:** Lewis Jones.

**Plausible starting context:** **Granby Workshop** is the social-enterprise design studio in Liverpool's Granby Four Streets area, spun out of the **Assemble** collective's Turner Prize-winning 2015 community-led restoration project. Lewis Jones is one of the Workshop founders. The Workshop produces handmade ceramics, door handles, mantelpieces, and tiles from salvaged materials — and the broader **Granby Four Streets Community Land Trust** restored a row of Victorian terraced houses on Cairns Street using reused brick, salvaged timber, and reclaimed fittings.

**Task:** Produce a dossier filling as many graph nodes and properties as possible. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## 2. OBK 27

**Already linked:** Cyril Pressacco, Thibaut Barrault.

**Plausible starting context:** Both linked actors are the architects of **Barrault Pressacco** (Paris), an architecture firm known for raw-material design (notably their Saint-Denis pierre-de-taille housing). The string "OBK 27" is most plausibly a French architectural shorthand for an address — best guesses:
- **27 rue Oberkampf**, Paris 11ᵉ (most likely — "OBK" = standard abbreviation for Oberkampf)
- **Office Bâti Kapital 27** or similar branded project code (less likely)
- Possibly a renovation project on rue Oberkampf 27 by Barrault Pressacco

**Task:** If the project can be identified, produce a dossier filling as many graph nodes and properties as possible. If identification fails after reasonable research, document as a negative finding — do not invent details. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## What to do with the dossiers once written

Hand each finished `.md` file back. For OBK 27 specifically: if the identification fails, the dossier should be short (≈ 1 page) documenting what was checked, and clearly labelled "**negative finding**" at the top so I know to handle it as a deletion candidate rather than a promotion.
