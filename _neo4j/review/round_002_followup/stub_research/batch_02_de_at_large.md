# Batch 2 — Large urban / DE-AT-CH projects (5 projects)

**Workflow + categories to gather:** see [README.md](README.md).
**Full graph schema (node labels, controlled vocabularies, property names):** see [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md).
**Reference examples:** [`K118_Kopfbau_Halle_118_Winterthur.md`](../../../../_archive/research/gebaeude/K118_Kopfbau_Halle_118_Winterthur.md). Comparable larger-scale case: [`Resource_Rows_Copenhagen.md`](../../../../_archive/research/gebaeude/Resource_Rows_Copenhagen.md).

## Graph nodes to populate

These are **physical buildings** (some projects span multiple buildings or an entire quarter) — the core node is `Bauwerk`. Fill as many of the following node types and their properties as the public record allows. Consult [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for all controlled-vocabulary IDs and property names.

**Core nodes:** `Bauwerk` (receiver + donor + depot) · `Akteur` (+ `Akteurrolle` + `Akteurtyp` + `GEHÖRT_ZU`) · `Bauteilgruppe`

**Per component batch:** `Bauteiltyp` · `Materialgruppe` · `WiederverwendungsArt` · `Beschaffungsweg` · `Rueckbauverfahren` · `Aufbereitungsverfahren` · `Verbindungstechnik` · `Logistik` · `Defekt` · `ZustandsKlasse` · `PruefungNachweis` · `Leistungsanforderung` · `Bauproduktstatus` · `Schadstoff`

**Per building:** `BauaufgabeIntervention` · `Nutzung` · `Bauobjektrolle` · `Bauobjektklasse` · `ZertifizierungBewertungssystem` · `Methode` · `Norm` · `LebenszyklusModul` · `Marktmodell` · `Akzeptanz` · `Huerde` · `HuerdeKategorie` · `Programm` · `Software` · `Tool` · `Wirtschaft`

**Geographic:** `Stadt` · `Land`

**Relationships to establish:** `BETEILIGT_AN` · `AUS_BAUWERK` · `EINGEBAUT_IN` · `LIEGT_IN_STADT` · `LIEGT_IN_LAND` · `ERHALT_FOERDERUNG_DURCH` · `TEIL_VON_PROGRAMM` · `BERECHNET_NACH_MODUL` · `HAT_WIRTSCHAFT`

The actors under "Already linked" are known graph nodes — use them as research anchors and add any newly discovered actors with their roles. **Every factual claim needs a source citation. Unknown → write "unknown".**

---

## 1. Stuttgart 210

**Already linked:** Andreas Kretzer, HFT Stuttgart, HTWG Konstanz, Katharina Raabe, Klingelhöfer Krötsch (architects), Maximilian Stemmler, Roman Kreuzer, Stefan Krötsch, Thomas Stark.

**Plausible starting context:** The name plays on "Stuttgart 21", the long-running Stuttgart rail-station mega-project. "Stuttgart 210" most likely refers to a research demonstrator, student-design studio, or pilot building that uses salvage material from the Stuttgart-21 teardowns as donor source. The team mix (HFT Stuttgart academic + HTWG Konstanz academic + Klingelhöfer Krötsch architects + Thomas Stark sustainability) points to a teaching-research collaboration with a built or near-built outcome.

**Task:** Produce a dossier filling as many graph nodes and properties as possible. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## 2. LYSP8 Basel (Lysbüchel)

**Already linked:** baubüro in situ (multiple mentions), Kerstin Müller, Kevin Straub, Loeliger Strub, Marc Angst, Marc Loeliger, Martin Zeller, Pascal Hentschel, Zirkular (multiple mentions).

**Plausible starting context:** "Lys-P8" parses as Lysbüchel, parcel 8 — the Lysbüchel urban-transformation district in Basel-Saint-Johann. Lead architects baubüro in situ and Loeliger Strub. Zirkular GmbH provides reuse planning (Zirkular spun off from baubüro in situ during K.118). This is likely one of the largest Swiss reuse-led mixed-use developments.

**Task:** Produce a dossier filling as many graph nodes and properties as possible. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## 3. Reallabor B(e) Ware

**Already linked:** Natural Building Lab (NBL), ZRS Architekten Ingenieure, Andrea Klinge, Christof Ziegert, Eike Roswag-Klinge, Matthew Crabbe, NBL Studio, Nina Pawlicki, Sina Jansen, Uwe Seiler.

**Plausible starting context:** "Reallabor" is a German federal-research format (BMBF / BBSR / Bundesstiftung Baukultur) — a real-world experimental zone. "B(e) Ware" plays on "Be Ware" (be aware) and "Bauen mit erprobten Waren" (building with proven goods). Lead: TU Berlin Natural Building Lab (Eike Roswag-Klinge chair) + ZRS Architekten (earth-construction specialist, Christof Ziegert). Likely a multi-year program with one or more pilot buildings.

**Task:** Produce a dossier filling as many graph nodes and properties as possible. Note that `prog_reallabor_be_ware` already exists in the graph — link any built pilot buildings to it via `TEIL_VON_PROGRAMM`. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## 4. MedUni Campus Mariannengasse (Wien)

**Already linked:** Markus Meissner, Thomas Romm.

**Plausible starting context:** New medical-university campus of MedUni Wien at Mariannengasse in Vienna's 9th district (Alsergrund). Thomas Romm is a Vienna architect / urban researcher (Forschen Planen Bauen) known for reuse-driven design and the Re-Use Map initiative. Markus Meissner is associated with several Austrian sustainability and reuse projects.

**Task:** Produce a dossier filling as many graph nodes and properties as possible. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## 5. RE-USE Höfe (Wien)

**Already linked:** Félix Dillmann.

**Plausible starting context:** Vienna's public reuse-yard network operated by city waste utility **MA 48**. Multiple "Höfe" (yards) around the city where citizens drop off and pick up usable goods. The network includes the **48er-Tandler** flagship shop. This is more a programme / network than a single project — translation into our schema may be best as a recurring programme node with multiple Hof locations as sub-buildings.

**Task:** Produce a dossier filling as many graph nodes and properties as possible. Note that this may be better represented as a `Programm` node with multiple `Bauwerk` locations (each Hof) rather than a single building — flag this if that is the case. See [GRAPH_SCHEMA.md](GRAPH_SCHEMA.md) for the complete vocabulary.

---

## What to do with the dossiers once written

Hand each finished `.md` file back. Same handling as batch 1: I do the schema translation and graph integration.
