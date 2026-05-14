# Neo4j Batch Quick Reference

**Schema:** `neo4j_reuse_graph_v1_1` · **Updated:** 2026-05-13

---

## Current State

| Layer | Nodes | Relationships |
|-------|-------|---------------|
| Project files (batches 001–014) | ~1 312 | ~12 988 |
| Controlled vocabulary seed + deltas | ~280 | ~45 |
| **Total in graph (live)** | **1 538** | **12 787** |

**Progress:** 70 / 98 case studies processed (≈ 71 %) · 194 direct-reuse BTGs + 100 non/unclassified BTGs

---

## Projects Loaded

| # | Batch | Project | Nodes | Rels | bw | Notes |
|---|-------|---------|-------|------|-----|-------|
| 1 | 001 | Berlin-Schildow Pilot House | 14 | 98 | 4 | WBS70 concrete prefab; 2 source files merged |
| 2 | 001 | Bestandverplanzung Pavilion München | 7 | 50 | 2 | prefab concrete panels |
| 3 | 001 | Big Dig Building Boston | 12 | 81 | 2 | not built; counts_as_direct_reuse:false |
| 4 | 001 | Big Dig House Lexington MA | 14 | 119 | 4 | steel+concrete |
| 5 | 002 | BioPartner 5 Leiden/Oegstgeest | 21 | 137 | 5 | 5 BTGs |
| 6 | 002 | BlueCity Offices Rotterdam | 18 | 108 | 3 | 4 BTGs |
| 7 | 002 | Boulder Fire Station 3 | 18 | 114 | 4 | 4 BTGs + 2 non-reuse |
| 8 | 002 | Brent Cross Town Primary Substation | 23 | 138 | 4 | 4 BTGs |
| 9 | 002 | Brighton Waste House | 18 | 133 | 3 | 6 BTGs; `mat_textil` delta |
| 10 | 003 | Broethen Twin-House Hoyerswerda | 9 | 88 | 4 | WBS70 P2 concrete; `bsys_p2` delta |
| 11 | 003 | CascadeUp London (glulam demonstrator) | 13 | 146 | 2 | remanufacturing; counts_as_direct_reuse:false |
| 12 | 003 | Charles Malis Molenbeek | 19 | 138 | 2 | Bestandserhalt separated |
| 13 | 003 | Christ Pavilion Volkenroda | 22 | 211 | 2 | translocation chain; 2 Bauwerk nodes |
| 14 | 003 | Chiro d’Itterbeek Dilbeek | 28 | 357 | 3 | surplus flagged separately |
| 15 | 004 | Circular Centre Netherlands | 17 | 199 | 3 | planned reuse; counts_as_direct_reuse:false |
| 16 | 004 | Circular Pavilion Paris | 19 | 231 | 2 | fixed components only |
| 17 | 004 | CRCLR House Berlin | 21 | 306 | 4 | Dachstahl + Fenster + Fassade |
| 18 | 004 | ELYS Basel | 24 | 342 | 4 | 91 t CO₂ reuse; `norm_crow_cur` delta |
| 19 | 004 | Europa Building Brussels | 16 | 146 | 4 | 3 750 wooden window frames |
| 20 | 005 | La Ferme du Rail Paris | 23 | 363 | 3 | biosourced/reused mix |
| 21 | 005 | gjG House Gentbrugge | 14 | 115 | 4 | reused brick shell |
| 22 | 005 | Grande Halle de Colombelles | 23 | 390 | 3 | Lot 01 Réemploi separated |
| 23 | 005 | Grubenstrasse 29 / Werkhof 29 Zürich | 21 | 417 | 4 | Bauteiljagd supply chain |
| 24 | 005 | Härmälänranta Tampere | 17 | 153 | 3 | 25 hollow-core slabs; `prog_recreate` delta |
| 25 | 006 | Hastings Pier Visitor Centre | 19 | 226 | 3 | reclaimed hardwood cladding; `mat_mdf` delta |
| 26 | 006 | Haus HOS Mühlhausen | 15 | 237 | 4 | WBS70/Stahlbeton wall + floor + stair BTGs |
| 27 | 006 | Holbein Gardens London | 20 | 232 | 4 | |
| 28 | 006 | House of Fraser / TBC.London steel reuse chain | 26 | 360 | 4 | multi-actor reuse chain |
| 29 | 006 | Impact Hub Berlin CRCLR fit-out | 22 | 435 | 2 | interior fit-out; `norm_sci` delta |
| 30 | 007 | Institut de Botanique ULg Liège | 8 | 63 | 3 | |
| 31 | 007 | Jeugdkliniek Ithaka / Emergis Kloetinge | 24 | 239 | 4 | |
| 32 | 007 | Juch-Areal Recyclingzentrum Zürich | 20 | 161 | 3 | |
| 33 | 007 | K118 / Kopfbau Halle 118 Winterthur | 24 | 206 | 5 | `norm_sia` delta |
| 34 | 007 | KA13 / Kristian Augusts gate 13, Oslo | 20 | 207 | 5 | `norm_ns_3682`, `norm_tek_norway` delta |
| 35 | 008 | Kamikatsu Zero Waste Center / Hotel WHY | 18 | 215 | 3 | |
| 36 | 008 | Kindergarten Mööslistrasse Manegg Zürich | 24 | 286 | 3 | Bauteilkatalog; `tool_bauteilkatalog` delta |
| 37 | 008 | Liander / Alliander HQ Duiven | 15 | 150 | 3 | cautious vague-data modeling |
| 38 | 008 | Lo-Reninge Town Hall façade | 13 | 108 | 3 | only brick façade as direct reuse |
| 39 | 008 | Lokomotion Technology Centre Tampere | 17 | 136 | 3 | 27 hollow-core slabs; `norm_en_1168` delta |
| 40 | 009 | Lycée Michel Lucius Luxembourg | 18 | 186 | 4 | campus-internal reuse |
| 41 | 009 | Maison des Canaux Paris | 12 | 126 | 3 | cautious; weakly documented |
| 42 | 009 | Maison DnA Asse | 10 | 71 | 4 | reused brick outer structure |
| 43 | 009 | Maison Vignette Auderghem | 18 | 161 | 3 | façade bricks + tiles + bluestone |
| 44 | 009 | Mehrow Pilot House | 11 | 97 | 4 | WBS70 wall + slab; PRECS metrics |
| 45 | 010 | Melkinlaituri Primary School + Day-care, Helsinki | 13 | 96 | 3 | 64 hollow-core slabs; ReCreate commercial replication |
| 46 | 010 | Montessori Maassluis | 14 | 82 | 2 | planned/watchlist; `counts_as_direct_reuse:false` |
| 47 | 010 | MULTI Brussels — Reuse in MULTI | 17 | 134 | 3 | interior BTGs separated from concrete Bestandserhalt |
| 48 | 010 | Musée de Folklore Mouscron | 15 | 91 | 3 | |
| 49 | 010 | People’s Pavilion Eindhoven | 18 | 163 | 2 | temporary demonstrator; Pretty Plastic shingles excluded |
| 50 | 011 | Plattenpalast Berlin | 13 | 147 | 2 | WBS70 concrete prefab reuse |
| 51 | 011 | Plattenvereinigung Berlin | 18 | 190 | 2 | WBS70 prefab panels |
| 52 | 011 | PLP London HQ Circular Studio fit-out | 18 | 194 | 2 | loose furniture excluded; `mat_faserzement` delta |
| 53 | 011 | Re:Crete footbridge — reused concrete blocks | 9 | 98 | 2 | infrastructure prototype; not a building Hauptfall |
| 54 | 011 | Recyclinghaus Hannover | 22 | 304 | 4 | reuse + DfD separated; recycling concrete excluded |
| 55 | 012 | Recypark Demets, Anderlecht | 15 | 97 | 5 | |
| 56 | 012 | Résilience / La Ferme des Possibles, Stains | 34 | 220 | 3 | large complex; some BTGs unclassified |
| 57 | 012 | Resource Rows, Copenhagen | 9 | 63 | 3 | |
| 58 | 012 | Roots in the Sky, Blackfriars Crown Court | 21 | 132 | 2 | planned/failed appendix; `counts_as_direct_reuse:false` |
| 59 | 012 | Saxum Vineyard Equipment Barn, Paso Robles | 19 | 118 | 4 | |
| 60 | 013 | Superlocal Expogebouw, Bleijerheide | 20 | 212 | 2 | |
| 61 | 013 | Svanen Kindergarten, Gladsaxe | 20 | 243 | 5 | |
| 62 | 013 | The Green House, Utrecht | 22 | 234 | 3 | |
| 63 | 013 | Thoravej 29, Copenhagen | 16 | 178 | 4 | |
| 64 | 013 | Timber Square, London | 24 | 246 | 4 | |
| 65 | 014 | Træ High Rise, Aarhus | 32 | 218 | 3 | |
| 66 | 014 | Upcycle Studios, Copenhagen | 24 | 156 | 3 | |
| 67 | 014 | Verbiest / Karreveld, Brussels | 31 | 241 | 3 | |
| 68 | 014 | Villa Welpeloo, Enschede | 28 | 185 | 5 | |
| 69 | 014 | Woongroep Boschgaard, Den Bosch | 29 | 219 | 3 | |
| 70 | 014 | Zinneke / Feder / Masui4Ever, Brussels | 26 | 245 | 3 | 6th project in batch |

---

## Node Labels (project files)

| Label | Count (approx.) | Description |
|-------|----------------|-------------|
| Projekt | 70 | One per case study |
| Bauteilgruppe | 294 | Component group; counts_as_direct_reuse: 194 true / 60 false / 40 null |
| Bauwerk | ~140 | Donor or receiver building |
| Quelle | ~70 | Source markdown per project |
| Akteur | ~200 | Persons / organisations |
| Ort | ~140 | Stadt / Land |
| Prozessphase | ~75 | Reuse process phases |
| Nutzung | ~60 | Building use types (shared with seed) |
| Material | shared + delta | Includes `mat_faserzement` (batch 011 delta) |
| Bauteiltyp | shared | Pulled from seed |
| Huerde | shared | Pulled from seed |
| Bausystem | shared + delta | P2, secondary timber glulam, CLST (batch 003+) |
| Norm | shared + delta | EN 1168, CROW-CUR, SIA, NS, SCI P-series (batches 007–8+) |

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
