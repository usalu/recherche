# Neo4j Batch Analysis — Batches 001–009

**Analysis Date:** 2026-05-13
**Schema Version:** `neo4j_reuse_graph_v1_1`
**Format:** JSONL (modular, per-project files + global controlled vocabulary seed)
**Location:** `_neo4j/neo4j batch/`

---

## Executive Summary

Nine production batches have been generated under schema `neo4j_reuse_graph_v1_1`, covering **44 case-study projects** across Germany, Belgium, Netherlands, France, Switzerland, United Kingdom, Norway, Finland, Luxembourg, Japan, and the United States. The architecture is modular: a single global controlled-vocabulary seed file provides all taxonomy nodes; per-project `.kg.jsonl` files carry the case-specific graph; delta files extend the vocabulary when new terms are needed.

**Combined Metrics (project files, excluding seed):**

| | 001 | 002 | 003 | 004 | 005 | 006 | 007 | 008 | 009 | Total |
|---|---|---|---|---|---|---|---|---|---|---|
| Projects | 4 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | **44** |
| Nodes | 47 | 98 | 91 | 97 | 98 | 102 | 96 | 87 | 69 | **785** |
| Rels | 348 | 630 | 940 | 1 224 | 1 438 | 1 490 | 876 | 895 | 641 | **8 482** |
| Delta nodes | 0 | 1 | 3 | 1 | 3 | 4 | 5 | 5 | 0 | 22 |

**Live graph (DB: `mit-bestand`):** 1 063 nodes · 8 389 rels · 143 direct-reuse BTGs + 52 non-reuse BTGs

**Global controlled vocabulary seed:** 330 nodes, 43 rels (loaded once before any batch).

**All validations passed** — no `Fallbeispiel` nodes, no `Kennwert` nodes, all `BELEGT_IN` carry `datenqualitaet: "Belegt"`, minimum degree ≥ 2 for every project-file node.

---

## 1. Schema & Architecture

### 1.1 File Layout (`_neo4j/neo4j batch/`)

```
neo4j_repo_output_contract_v1_1/neo4j_repo_output_contract_v2/
├── controlled_vocabulary.seed.kg.jsonl   ← 330 nodes, 43 rels — load once
├── cypher/constraints.cypher             ← run once before any import
├── schemas/                              ← JSON schema for JSONL validation
└── VALIDATION_CHECKLIST.md

neo4j_batch_001_exports/batches/batch_001/
├── manifest.json
├── AGENT_NOTES.md
├── validation_report.md
├── controlled_terms.delta.jsonl          ← empty for batch_001
├── p_berlin_schildow_pilot_house.kg.jsonl
├── p_bestandverplanzung_pavilion_muenchen.kg.jsonl
├── p_big_dig_building_boston.kg.jsonl
└── p_big_dig_house_lexington_massachusetts.kg.jsonl

neo4j_batch_002_exports/neo4j_exports/batches/batch_002/
├── manifest.json
├── AGENT_NOTES.md
├── validation_report.md
├── controlled_terms.delta.jsonl          ← 1 node (mat_textil) + 1 rel
├── p_biopartner_5_leiden_oegstgeest.kg.jsonl
├── p_bluecity_offices_rotterdam.kg.jsonl
├── p_boulder_fire_station_3.kg.jsonl
├── p_brent_cross_town_primary_substation_london.kg.jsonl
└── p_brighton_waste_house_brighton.kg.jsonl
```

### 1.2 JSONL Record Format

Each line in a `.kg.jsonl` file is a self-contained JSON object:

```json
{ "record_type": "node", "id": "...", "labels": ["..."], "properties": { ... } }
{ "record_type": "rel",  "id": "...", "from": "...", "type": "...", "to": "...", "properties": { ... } }
```

### 1.3 Import Order (per batch)

1. Run `cypher/constraints.cypher` once on the database.
2. Import `controlled_vocabulary.seed.kg.jsonl` once (idempotent `MERGE`).
3. For each batch: import `controlled_terms.delta.jsonl` if non-empty.
4. Import each `p_*.kg.jsonl`: all `node` records first, then all `rel` records.

### 1.4 Modeling Rules Applied

| Rule | Status |
|------|--------|
| `Projekt` as central aggregation node (no `Fallbeispiel`) | ✅ |
| `Bauteilgruppe` as concrete occurrence node | ✅ |
| `Quelle` as source-of-truth; every record linked via `BELEGT_IN` | ✅ |
| `BELEGT_IN` always carries `datenqualitaet: "Belegt"` | ✅ |
| `bewertung` stored as scalar property on `Projekt` | ✅ |
| Quantitative metrics as properties (area, mass, CO₂, dates) | ✅ |
| `counts_as_direct_reuse` flag on `Bauteilgruppe` | ✅ |
| No `Kennwert` nodes | ✅ |
| External URLs as `external_sources` array on `Quelle`, not separate nodes | ✅ |
| Taxonomy (Stadt, Land, Bauobjektklasse, Bauobjektrolle, etc.) as connected nodes | ✅ |

---

## 2. Batch 001 — Case Studies

**Source files:** 5 → **4 projects** (Berlin-Schildow 1 & 2 merged)
**Schema:** `neo4j_reuse_graph_v1_1`

### 2.1 Berlin-Schildow Pilot House (Germany)

| Attribute | Value |
|-----------|-------|
| **Source files** | `Berlin_Schildow_Pilot_House.md` + `Berlin_Schildow_Pilot_House_2.md` (merged) |
| **Year** | 2005 |
| **Rating** | 4 / 5 |
| **Location** | Schildow / Berlin, Germany |
| **Type** | Single/two-generation house (Neubau mit WBS70-Fertigteilen) |
| **File** | `p_berlin_schildow_pilot_house.kg.jsonl`: 14 nodes, 98 rels |

**Bauteilgruppen:**
- Zugeschnittene WBS70-Stahlbetonfertigteile (200 parts, 245 m³, from Berliner Plattenbau; transport 33 km; element age 18 years) — `counts_as_direct_reuse: true`

**Actors:** Claus Asam, IEMB/TU Berlin, Architekturbüro Conclus, Hervé/Joel Biele, Familie Lange

**Merge note:** The second source file is self-labelled "ANHANG/ZUSAMMENFÜHREN" and describes the same uncertain Schildow pilot identity; both files point to the same canonical `Projekt` node.

---

### 2.2 Bestandverplanzung Pavilion, München (Germany)

| Attribute | Value |
|-----------|-------|
| **Year** | 2008 |
| **Rating** | 2 / 5 |
| **Location** | München, Germany |
| **File** | `p_bestandverplanzung_pavilion_muenchen.kg.jsonl`: 7 nodes, 50 rels |

**Bauteilgruppen:**
- Betonfertigteil-Paneele aus Olympiadorf-Bungalows — `counts_as_direct_reuse: true`

**Actors:** (none individually named in source)

---

### 2.3 Big Dig Building, Boston/Cambridge (USA) ⚠ Not a built reuse case

| Attribute | Value |
|-----------|-------|
| **Year** | 2008 |
| **Rating** | 2 / 5 |
| **Location** | Boston/Cambridge, USA |
| **File** | `p_big_dig_building_boston.kg.jsonl`: 12 nodes, 81 rels |

**Bauteilgruppen:**
- Geplante Big-Dig-Infrastrukturbauteile — `counts_as_direct_reuse: false`

**Note:** Proposed/aborted reuse concept; `Projekt.counts_as_built_direct_reuse = false`. Retained for knowledge completeness and concept documentation.

**Actors:** Single Speed Design, John Hong, Jinhee Park, Paul Pedini

---

### 2.4 Big Dig House, Lexington, Massachusetts (USA)

| Attribute | Value |
|-----------|-------|
| **Rating** | 4 / 5 |
| **Location** | Lexington, Massachusetts, USA |
| **File** | `p_big_dig_house_lexington_massachusetts.kg.jsonl`: 14 nodes, 119 rels |

**Bauteilgruppen (3):**
- Wiederverwendete Stahlträger und Stahlstützen
- Wiederverwendete Inverset-Stahlbetonpaneele
- Wiederverwendete Ramp-, Pier- und Roadway-Komponenten

**Actors:** Paul Pedini, Single Speed Design, John Hong, Jinhee Park

---

## 3. Batch 002 — Case Studies

**Schema:** `neo4j_reuse_graph_v1_1`
**New controlled term:** `mat_textil` (introduced for Brighton Waste House)

### 3.1 BioPartner 5, Leiden/Oegstgeest (Netherlands)

| Attribute | Value |
|-----------|-------|
| **Rating** | 5 / 5 |
| **Location** | Leiden / Oegstgeest, Netherlands |
| **File** | `p_biopartner_5_leiden_oegstgeest.kg.jsonl`: 21 nodes, 137 rels |

**Bauteilgruppen (5):**
- Wiederverwendete Stahlträger, Stützen und Rahmen
- Wiederverwendete Innenwände und Trennwände
- Wiederverwendete Pflaster-, Naturstein- und Bodenmaterialien
- Wiederverwendete Sanitärobjekte
- Abbruchschutt / Mauerwerkspuin in grüner Fassade

**Actors:** BioPartner Center Leiden, Popma ter Steege Architecten (PTSA), IMd Raadgevende Ingenieurs, De Vries en Verburg, Vic Obdam Staalbouw, Deerns, STONE22, Leiden University (donor source)

---

### 3.2 BlueCity Offices, Rotterdam (Netherlands)

| Attribute | Value |
|-----------|-------|
| **Rating** | 3 / 5 |
| **Location** | Rotterdam, Netherlands |
| **File** | `p_bluecity_offices_rotterdam.kg.jsonl`: 18 nodes, 108 rels |

**Bauteilgruppen (4):**
- Red-Cedar-Fensterrahmen als Trennwände / innere Fassade
- Wiederverwendeter Stahl im Büroausbau
- Betonblöcke als Trennwände
- Mögliche wiederverwendete Balustraden

**Actors:** BlueCity/Blue City 010 BV, Superuse Studios, COUP, Workspot, Floris Schiferli, Bik Bouw

---

### 3.3 Boulder Fire Station 3 (USA)

| Attribute | Value |
|-----------|-------|
| **Rating** | 4 / 5 |
| **Location** | Boulder, Colorado, USA |
| **File** | `p_boulder_fire_station_3.kg.jsonl`: 18 nodes, 114 rels |

**Bauteilgruppen (4):**
- 89 salvaged wide-flange steel members (`counts_as_direct_reuse: true`)
- Boulder Community Hospital structural steel stockpile (`counts_as_direct_reuse: true`)
- Neue Glulam Columns im Hybridtragwerk (`counts_as_direct_reuse: false` — new material)
- PV-Dach / große Dachfläche (`counts_as_direct_reuse: false` — new construction)

**Actors:** City of Boulder, Davis Partnership Architects, KL&A Engineers and Builders, Mark Young Construction, Boulder Community Health / BCH (donor), Full Metal Iron

---

### 3.4 Brent Cross Town Primary Substation, London (UK)

| Attribute | Value |
|-----------|-------|
| **Rating** | 4 / 5 |
| **Location** | London, United Kingdom |
| **File** | `p_brent_cross_town_primary_substation_london.kg.jsonl`: 23 nodes, 138 rels |

**Bauteilgruppen (4):**
- Reclaimed tubular steel columns
- Reclaimed tubular bracing members
- Ovaler Substation-Screen
- Neue façade support members (`counts_as_direct_reuse: false`)

**Actors:** Brent Cross South Limited Partnership, Related Argent, London Borough of Barnet, IF_DO, Arup, Whitby Wood, Bourne Special Projects/Bourne Group, Galldris Group, Cleveland Steel and Tubes, Lakwena

---

### 3.5 Brighton Waste House (UK)

| Attribute | Value |
|-----------|-------|
| **Rating** | 3 / 5 |
| **Location** | Brighton, United Kingdom |
| **File** | `p_brighton_waste_house_brighton.kg.jsonl`: 18 nodes, 133 rels |
| **Delta term** | `mat_textil` introduced here |

**Bauteilgruppen (6):**
- Wiederverwendete Betonblöcke
- Holz und Sperrholz aus Reststücken
- Gebrauchte Teppichfliesen als Fassaden-/Außenschicht
- Vinylbanner als Dampfbremse
- Zahnbürsten und Medienabfall als Hohlraumfüllung
- Denim jeans als Dämm-/Hohlraumfüllung (`mat_textil` — new vocabulary term)

**Actors:** University of Brighton, Duncan Baker-Brown/BBM Sustainable Design, Cat Fletcher/Freegle, Mears Group, Greater Brighton Metropolitan College, Studierende/Schulkinder/Freiwillige

---

## 4. Node Type Distribution

### 4.1 Global Controlled Vocabulary Seed (330 nodes)

| Label | Count | Label | Count |
|-------|-------|-------|-------|
| Huerde | 28 | Akteurrolle | 21 |
| Material | 15 | Bauteiltyp | 15 |
| Leistungsanforderung | 13 | Methode | 13 |
| Status | 12 | Akteurtyp | 11 |
| Aufbereitungsverfahren | 11 | WiederverwendungsArt | 11 |
| Programm | 11 | Ressourcenquelle | 9 |
| Nutzung | 9 | Beschaffungsweg | 8 |
| Bauobjektklasse | 8 | Norm | 7 |
| Verbindungstechnik | 7 | Bauweise | 6 |
| Bauteilebene | 6 | Bauobjektrolle | 6 |
| Funktionswechsel | 6 | RechtlicheBedingung | 6 |
| ZertifizierungBewertungssystem | 5 | Bausystem | 5 |
| Rueckbauverfahren | 5 | Schadstoff | 5 |
| Prozessphase | 10 | HuerdeKategorie | 10 |
| Logistik | 10 | Materialgruppe | 10 |
| BauaufgabeIntervention | 10 | Tragwerksprinzip | 4 |
| Wirtschaft | 6 | PruefungNachweis | 11 |

### 4.2 Project-File Node Types (145 nodes across both batches)

| Label | Description |
|-------|-------------|
| **Quelle** | Source markdown files (1–2 per project) |
| **Projekt** | Central aggregation node (1 per project) |
| **Bauwerk** | Buildings — donor, receiver, existing, new |
| **Bauteilgruppe** | Reused/tracked component groups |
| **Akteur** | Organizations and individuals |
| **Stadt** | Cities |
| **Land** | Countries |
| **Norm** | Specific standards referenced by a project |
| **RechtlicheBedingung** | Legal/regulatory conditions (project-specific) |
| **Tool** | Digital tools or software used in projects |
| **Wiederverwendungskette** | Reuse chain nodes (multi-step reuse sequences) |

---

## 5. Relationship Types

All relationship types found across both batches:

### 5.1 Core Provenance

| Type | Semantics |
|------|-----------|
| `BELEGT_IN` | Any node → Quelle; always carries `datenqualitaet: "Belegt"` |

### 5.2 Geographic

| Type | Semantics |
|------|-----------|
| `LIEGT_IN_STADT` | Entity located in Stadt |
| `LIEGT_IN_LAND` | Stadt/Entity located in Land |

### 5.3 Project Structure

| Type | Semantics |
|------|-----------|
| `HAT_BAUTEILGRUPPE` | Projekt → Bauteilgruppe |
| `HAT_BAUOBJEKTKLASSE` | Bauwerk → Bauobjektklasse |
| `HAT_BAUOBJEKTROLLE` | Bauwerk → Bauobjektrolle |
| `HAT_NUTZUNG` | Bauwerk/Bauteilgruppe → Nutzung |
| `HAT_STATUS` | Entity → Status |
| `HAT_INTERVENTION` | Projekt → BauaufgabeIntervention |
| `TEIL_VON_PROGRAMM` | Projekt → Programm |

### 5.4 Component Reuse Chain

| Type | Semantics |
|------|-----------|
| `AUS_BAUWERK` | Bauteilgruppe originated from Bauwerk (donor) |
| `EINGEBAUT_IN` | Bauteilgruppe installed in Bauwerk (receiver) |
| `HAT_BAUTEILTYP` | Bauteilgruppe → Bauteiltyp |
| `HAT_BAUTEILEBENE` | Bauteilgruppe → Bauteilebene |
| `HAT_WIEDERVERWENDUNGSART` | Bauteilgruppe → WiederverwendungsArt |
| `HAT_AUFBEREITUNG` | Bauteilgruppe → Aufbereitungsverfahren |
| `HAT_RUECKBAUVERFAHREN` | Bauteilgruppe → Rueckbauverfahren |
| `HAT_BAUSYSTEM` | Bauteilgruppe/Bauwerk → Bausystem |
| `HAT_BAUWEISE` | Bauteilgruppe/Bauwerk → Bauweise |
| `HAT_TRAGWERKSPRINZIP` | Bauwerk → Tragwerksprinzip |
| `HAT_FUNKTIONSWECHSEL` | Bauteilgruppe → Funktionswechsel |
| `TEIL_VON_KETTE` | Bauteilgruppe → Wiederverwendungskette |
| `NUTZT_MATERIAL` | Bauteilgruppe → Material |
| `NUTZT_BAUWERK` | Bauteilgruppe → Bauwerk (secondary association) |

### 5.5 Actor Network

| Type | Semantics |
|------|-----------|
| `BETEILIGT_AN` | Akteur → Projekt |
| `HAT_AKTEURROLLE` | Akteur/Beteiligung → Akteurrolle |
| `HAT_AKTEURTYP` | Akteur → Akteurtyp |

### 5.6 Supply Chain & Logistics

| Type | Semantics |
|------|-----------|
| `HAT_BESCHAFFUNGSWEG` | Bauteilgruppe → Beschaffungsweg |
| `HAT_RESSOURCENQUELLE` | Bauteilgruppe → Ressourcenquelle |
| `HAT_LOGISTIK` | Bauteilgruppe → Logistik |

### 5.7 Technical Requirements & Barriers

| Type | Semantics |
|------|-----------|
| `HAT_HUERDE` | Bauteilgruppe/Projekt → Huerde |
| `HAT_LEISTUNGSANFORDERUNG` | Bauteilgruppe → Leistungsanforderung |
| `HAT_PRUEFUNG` | Bauteilgruppe/Leistungsanforderung → PruefungNachweis |
| `REFERENZIERT_NORM` | Entity → Norm |
| `HAT_ZERTIFIZIERUNG` | Entity → ZertifizierungBewertungssystem |
| `HAT_RECHTLICHE_BEDINGUNG` | Entity → RechtlicheBedingung |

### 5.8 Methods & Tools

| Type | Semantics |
|------|-----------|
| `HAT_METHODE` | Projekt → Methode |
| `NUTZT_TOOL` | Projekt/Akteur → Tool |

---

## 6. Key Graph Patterns

### 6.1 Project Hub

```
Quelle (source markdown)
  ↑ BELEGT_IN ← all project-file nodes
Projekt
  ├─ HAT_BAUTEILGRUPPE → Bauteilgruppe (1–6 per project)
  ├─ LIEGT_IN_STADT → Stadt → LIEGT_IN_LAND → Land
  ├─ HAT_STATUS → Status
  ├─ HAT_INTERVENTION → BauaufgabeIntervention
  ├─ TEIL_VON_PROGRAMM → Programm
  └─ HAT_METHODE → Methode
```

### 6.2 Component Reuse Chain

```
Bauwerk (donor)
  ← AUS_BAUWERK ← Bauteilgruppe → EINGEBAUT_IN → Bauwerk (receiver)
       ├─ NUTZT_MATERIAL → Material
       ├─ HAT_BAUTEILTYP → Bauteiltyp
       ├─ HAT_WIEDERVERWENDUNGSART → WiederverwendungsArt
       ├─ HAT_AUFBEREITUNG → Aufbereitungsverfahren
       ├─ HAT_RUECKBAUVERFAHREN → Rueckbauverfahren
       ├─ HAT_HUERDE → Huerde
       ├─ HAT_LEISTUNGSANFORDERUNG → Leistungsanforderung
       ├─ HAT_BESCHAFFUNGSWEG → Beschaffungsweg
       └─ TEIL_VON_KETTE → Wiederverwendungskette
```

### 6.3 Actor Network

```
Akteur
  ├─ HAT_AKTEURROLLE → Akteurrolle
  ├─ HAT_AKTEURTYP → Akteurtyp
  ├─ BETEILIGT_AN → Projekt
  └─ NUTZT_TOOL → Tool
```

### 6.4 `counts_as_direct_reuse` Filter

The `Bauteilgruppe.counts_as_direct_reuse` boolean flag enables filtered queries:
- `true` (default): component counts as genuine direct structural/architectural reuse
- `false`: component is new material, context element, or proposed-only concept

Batch 001: 1 node with `false` (Big Dig Building — proposed concept).
Batch 002: 6 nodes with `false` (new structural elements / photovoltaic / context elements).

---

## 7. Data Quality & Validation

| Check | Batch 001 | Batch 002 |
|-------|-----------|-----------|
| JSONL syntax | PASS | PASS |
| JSON schema | PASS | PASS |
| Manifest schema | PASS | PASS |
| Relationship endpoints | PASS | PASS |
| `BELEGT_IN` always `datenqualitaet: "Belegt"` | PASS | PASS |
| No `Fallbeispiel` or `Kennwert` nodes | PASS | PASS |
| Node degree ≥ 2 (project-file graph) | PASS | PASS |
| No forbidden legacy properties | PASS | PASS |

**Conflicting numeric values** are stored as `min`/`max` properties or `note` fields rather than collapsed.

---

## 8. Geographic & Thematic Scope

### 8.1 Countries Represented

| Country | Projects |
|---------|---------|
| Germany | Berlin-Schildow Pilot House, Bestandverplanzung Pavilion München |
| USA | Big Dig Building Boston, Big Dig House Lexington, Boulder Fire Station 3 |
| Netherlands | BioPartner 5 Leiden, BlueCity Offices Rotterdam |
| UK | Brent Cross Town Substation London, Brighton Waste House |

### 8.2 Reuse Strategies Represented

1. **Concrete prefabricated element reuse** — WBS70 panels (Schildow), prefab pavilion panels (München)
2. **Infrastructure element reuse** — Big Dig Highway sections (Lexington)
3. **Structural steel reuse** — Big Dig House, BioPartner 5, Boulder FS3, Brent Cross
4. **Interior component reuse** — BlueCity window frames, partitions; BioPartner sanitary fixtures
5. **Waste stream / salvage integration** — Brighton Waste House (textiles, toothbrushes, vinyl banners)
6. **Landscape/hardscape reuse** — BioPartner 5 pavings and masonry rubble in façade

### 8.3 Rating Distribution

| Rating | Count | Projects |
|--------|-------|---------|
| 5 / 5 | 1 | BioPartner 5 |
| 4 / 5 | 4 | Berlin-Schildow, Big Dig House, Boulder FS3, Brent Cross |
| 3 / 5 | 2 | BlueCity Offices, Brighton Waste House |
| 2 / 5 | 2 | Bestandverplanzung München, Big Dig Building (non-built) |

---

## 9. Import Considerations

### 9.1 Constraint & Index Recommendations

```cypher
// constraints.cypher (already provided in repo)
CREATE CONSTRAINT FOR (n:Projekt) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT FOR (n:Bauteilgruppe) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT FOR (n:Quelle) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT FOR (n:Akteur) REQUIRE n.id IS UNIQUE;

// Useful indexes
CREATE INDEX FOR (n:Bauteilgruppe) ON (n.counts_as_direct_reuse);
CREATE INDEX FOR (n:Projekt) ON (n.bewertung);
```

### 9.2 Example Cypher Queries

**All built direct-reuse component groups:**
```cypher
MATCH (btg:Bauteilgruppe)
WHERE btg.counts_as_direct_reuse = true
RETURN btg.id, btg.name
```

**Trace a component from donor to receiver:**
```cypher
MATCH (donor:Bauwerk)<-[:AUS_BAUWERK]-(btg:Bauteilgruppe)-[:EINGEBAUT_IN]->(receiver:Bauwerk)
RETURN donor.name, btg.name, receiver.name
```

**Actor network for a project:**
```cypher
MATCH (a:Akteur)-[:BETEILIGT_AN]->(p:Projekt),
      (a)-[:HAT_AKTEURROLLE]->(ar:Akteurrolle)
WHERE p.id = 'p_brent_cross_town_primary_substation'
RETURN a.name, ar.name
```

**Barrier landscape across all projects:**
```cypher
MATCH (btg:Bauteilgruppe)-[:HAT_HUERDE]->(h:Huerde),
      (btg)<-[:HAT_BAUTEILGRUPPE]-(p:Projekt)
RETURN p.name, h.name
ORDER BY p.name
```

---

## 10. Next Steps

1. **Batch 003+** — continue ingesting remaining case studies from `_database/fallstudie/`
2. **Archieve batch reconciliation** — the older `_neo4j/archieve/` batch (schema `direct_reuse_neo4j_clean_v1`) covers different projects (55 Great Suffolk, Gröditz, Plauen, AWM Münster, BedZED); decide whether to re-model these under v1_1 or migrate the old JSON
3. **Production import** — load constraints → seed → batch_001 → batch_002 into staging Neo4j; run APOC checks
4. **`counts_as_direct_reuse` audit** — verify the 6 batch_002 `false` flags against source texts
5. **Delta vocabulary review** — confirm `mat_textil` coverage; check if any batch_001 projects need analogous additions

---

**Document prepared:** 2026-05-13
**Analysis scope:** Batches 001 & 002 — 9 projects, 145 project-file nodes, 978 project-file relationships
**Global seed:** 330 nodes, 43 rels
**Data source:** `_neo4j/neo4j batch/` JSONL exports, manifests, and validation reports
