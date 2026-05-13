# Neo4j Batch Quick Reference

**Schema:** `neo4j_reuse_graph_v1_1` · **Updated:** 2026-05-13

---

## Current State

| Layer | Nodes | Relationships |
|-------|-------|---------------|
| Project files (batches 001+002) | 145 | 978 |
| Controlled vocabulary seed | 330 | 43 |
| **Total in graph** | **475** | **1 021** |

**Progress:** 9 / 98 case studies processed (≈ 9 %)

---

## Projects Loaded

| # | Batch | Project | Nodes | Rels | Bewertung | Notes |
|---|-------|---------|-------|------|-----------|-------|
| 1 | 001 | Berlin-Schildow Pilot House | 14 | 98 | 4 | WBS70 concrete prefab |
| 2 | 001 | Bestandverplanzung Pavilion München | 7 | 50 | 2 | prefab concrete panels |
| 3 | 001 | Big Dig Building Boston | 12 | 81 | 2 | NOT built; counts_as_direct_reuse:false |
| 4 | 001 | Big Dig House Lexington MA | 14 | 119 | 4 | 3 BTGs; steel+concrete |
| 5 | 002 | BioPartner 5 Leiden/Oegstgeest | 21 | 137 | 5 | 5 BTGs |
| 6 | 002 | BlueCity Offices Rotterdam | 18 | 108 | 3 | 4 BTGs |
| 7 | 002 | Boulder Fire Station 3 | 18 | 114 | 4 | 4 BTGs + 2 non-reuse |
| 8 | 002 | Brent Cross Town Primary Substation | 23 | 138 | 4 | 4 BTGs |
| 9 | 002 | Brighton Waste House | 18 | 133 | 3 | 6 BTGs incl. mat_textil |

---

## Node Labels (project files)

| Label | Count (approx.) | Description |
|-------|----------------|-------------|
| Projekt | 9 | One per case study |
| Bauteilgruppe | ~41 | Component group; carries counts_as_direct_reuse |
| Bauwerk | ~18 | Donor or receiver building |
| Quelle | ~9 | Source markdown per project |
| Akteur | ~24 | Persons / organisations |
| Ort | ~15 | Stadt / Land |
| Prozessphase | ~12 | Reuse process phases |
| Nutzung | ~10 | Building use types (shared with seed) |
| Material | shared | Pulled from seed |
| Bauteiltyp | shared | Pulled from seed |
| Huerde | shared | Pulled from seed |

---

## Relationship Types (v1_1 — 38 types)

| Rel type | Connects |
|----------|---------|
| `AUS_BAUWERK` | Bauteilgruppe → Bauwerk (donor) |
| `EINGEBAUT_IN` | Bauteilgruppe → Bauwerk (receiver) |
| `NUTZT_MATERIAL` | Bauteilgruppe → Material |
| `HAT_BAUTEILTYP` | Bauteilgruppe → Bauteiltyp |
| `HAT_BAUTEILEBENE` | Bauteilgruppe → Bauteilebene |
| `HAT_AUFBEREITUNG` | Bauteilgruppe → Aufbereitungsverfahren |
| `HAT_HUERDE` | Bauteilgruppe → Huerde |
| `HAT_REUSE_ART` | Bauteilgruppe → WiederverwendungsArt |
| `HAT_BAUTEILZUSTAND` | Bauteilgruppe → Bauteilzustand |
| `HAT_LOGISTIK` | Bauteilgruppe → Logistik |
| `HAT_BESCHAFFUNGSWEG` | Bauteilgruppe → Beschaffungsweg |
| `HAT_REUSE_EINSATZ` | Bauteilgruppe → ReuseEinsatz |
| `HAT_FUEGUNG` | Bauteilgruppe → FuegungVerbindung |
| `BELEGT_IN` | Bauteilgruppe → Quelle (+ datenqualitaet prop) |
| `BETEILIGT_AN` | Akteur → Projekt |
| `HAT_AKTEURROLLE` | Akteur → Akteurrolle |
| `LIEGT_IN` | Bauwerk → Ort |
| `BEFINDET_SICH_IN` | Ort → Ort (Stadt in Land) |
| `HAT_NUTZUNG` | Bauwerk → Nutzung |
| `HAT_BAUWEISE` | Bauwerk → Bauweise |
| `HAT_BAUSYSTEM` | Bauwerk → Bausystem |
| `HAT_TRAGWERK` | Bauwerk → Tragwerkstyp |
| `HAT_STATUS` | Bauwerk → Bauobjektstatus |
| `HAT_BAUAUFGABE` | Projekt → Bauaufgabe |
| `HAT_PROZESSPHASE` | Projekt → Prozessphase |
| `HAT_FOERDERPROGRAMM` | Projekt → Foerderprogramm |
| `HAT_NORM` | Projekt → Norm |
| `HAT_ZERTIFIZIERUNG` | Projekt → Zertifizierung |
| `IST_BAUTEILGRUPPE_VON` | Bauteilgruppe → Projekt |
| `DONOR_BAUWERK` | Projekt → Bauwerk (donor) |
| `RECEIVER_BAUWERK` | Projekt → Bauwerk (receiver) |
| `QUELLE_FUER` | Quelle → Projekt |
| + 6 others | (see VALIDATION_CHECKLIST.md) |

---

## Common Queries

**All projects with review score:**
```cypher
MATCH (p:Projekt) RETURN p.name, p.bewertung ORDER BY p.bewertung DESC
```

**Component groups with direct reuse flag:**
```cypher
MATCH (btg:Bauteilgruppe)-[:IST_BAUTEILGRUPPE_VON]->(p:Projekt)
WHERE btg.counts_as_direct_reuse = true
RETURN p.name, btg.name, btg.bauteiltyp_name
ORDER BY p.name
```

**Material flows (donor → component → receiver):**
```cypher
MATCH (donor:Bauwerk)<-[:AUS_BAUWERK]-(btg:Bauteilgruppe)-[:EINGEBAUT_IN]->(recv:Bauwerk),
      (btg)-[:NUTZT_MATERIAL]->(m:Material)
WHERE btg.counts_as_direct_reuse = true
RETURN donor.name, m.name, btg.name, recv.name
ORDER BY m.name
```

**Barriers ranked by frequency:**
```cypher
MATCH (btg:Bauteilgruppe)-[:HAT_HUERDE]->(h:Huerde)
RETURN h.name, count(*) AS n ORDER BY n DESC LIMIT 15
```

**Actors across projects:**
```cypher
MATCH (a:Akteur)-[:BETEILIGT_AN]->(p:Projekt)
RETURN a.name, count(p) AS projects ORDER BY projects DESC LIMIT 15
```

**Seed vocabulary size by label:**
```cypher
MATCH (n) WHERE NOT (n:Projekt OR n:Bauteilgruppe OR n:Bauwerk OR n:Akteur OR n:Quelle OR n:Ort OR n:Prozessphase)
RETURN labels(n)[0] AS label, count(*) AS count ORDER BY count DESC
```

---

## `counts_as_direct_reuse` Rules

Set **`true`** when the component is physically reused without re-manufacturing.
Set **`false`** when:
- The project was proposed but not built
- The component is entirely new material
- The node represents context (site, infrastructure) rather than a reused component

---

## Batch Locations

```
_neo4j/neo4j batch/
├── neo4j_batch_001_exports/batches/batch_001/  (4 projects)
├── neo4j_batch_002_exports/batches/batch_002/  (5 projects)
└── neo4j_repo_output_contract_v1_1/
    └── neo4j_repo_output_contract_v2/
        ├── controlled_vocabulary.seed.kg.jsonl
        └── cypher/constraints.cypher
```

See [NEO4J_BATCH_PIPELINE.md](NEO4J_BATCH_PIPELINE.md) for import procedure and governance.
