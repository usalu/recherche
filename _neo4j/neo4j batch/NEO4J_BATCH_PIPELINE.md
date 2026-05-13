# Neo4j Batch Pipeline

**Context:** Circular Building Reuse Research Database
**Updated:** 2026-05-13
**Schema:** `neo4j_reuse_graph_v1_1`
**Scale:** ~98 case studies total · 9 processed · ~89 remaining · ~18 batches projected

---

## Overview: Two-Layer Architecture

### Layer 1 — Research Database (`_database/`)
Canonical source of truth. Human-curated markdown files, one folder per entity.

```
_database/
├── _system/SCHEMA.md          ← ontology definition
├── _edges/                    ← confirmed edge set (CSV)
└── fallstudie/{CaseName}/     ← ~98 case study folders
    └── index.md
```

### Layer 2 — Neo4j Graph (`_neo4j/neo4j batch/`)
Optimized for queries and network analysis. JSONL format, modular per project.

```
_neo4j/neo4j batch/
├── neo4j_repo_output_contract_v1_1/
│   └── neo4j_repo_output_contract_v2/
│       ├── controlled_vocabulary.seed.kg.jsonl   ← 330 nodes, 43 rels (load once)
│       ├── cypher/constraints.cypher              ← run once
│       └── VALIDATION_CHECKLIST.md
├── neo4j_batch_001_exports/batches/batch_001/    ← 4 projects
├── neo4j_batch_002_exports/batches/batch_002/    ← 5 projects
└── neo4j_batch_{NNN}_exports/batches/batch_{NNN}/ ← future batches
```

---

## Batch Convention

### Folder & File Naming
```
neo4j_batch_{NNN}_exports/
└── batches/
    └── batch_{NNN}/
        ├── manifest.json
        ├── AGENT_NOTES.md
        ├── validation_report.md
        ├── controlled_terms.delta.jsonl    ← new vocab terms only; empty if none
        └── p_{project_slug}.kg.jsonl       ← one file per project
```

Rules:
- `{NNN}` is **zero-padded 3 digits**: `001`, `002`, `003` …
- Each batch covers **5 case study files** (≈ manageable review unit).
- Batches are **append-only** — never modify a published batch file in place.
- Two source files for the same project → merge into one `p_` file (document in `AGENT_NOTES.md`).

### Progress Register

| Batch | Projects (count) | Status | Notes |
|-------|-----------------|--------|-------|
| 001 | Berlin-Schildow, Bestandverplanzung München, Big Dig Building Boston, Big Dig House Lexington (4) | ✅ done | Schildow files 1+2 merged |
| 002 | BioPartner 5 Leiden, BlueCity Rotterdam, Boulder FS3, Brent Cross London, Brighton Waste House (5) | ✅ done | `mat_textil` delta |
| 003 | Broethen Hoyerswerda, CascadeUp London, Charles Malis Molenbeek, Christ Pavilion Volkenroda, Chiro Dilbeek (5) | ✅ done | `bsys_p2`, `bsys_secondary_timber_glulamst`, `bsys_clst` delta |
| 004 | Circular Centre NL, Circular Pavilion Paris, CRCLR House Berlin, ELYS Basel, Europa Building Brussels (5) | ✅ done | `norm_crow_cur_guideline_4_2023` delta |
| 005 | Ferme du Rail Paris, gjG House Gentbrugge, Grande Halle Colombelles, Grubenstrasse 29 Zürich, Härmälänranta Tampere (5) | ✅ done | `mat_bitumen`, `prog_recreate` delta |
| 006 | Hastings Pier, Haus HOS Mühlhausen, Holbein Gardens London, House of Fraser Oxford St, Impact Hub CRCLR fitout (5) | ✅ done | `mat_mdf`, `norm_sci_p427/440` delta |
| 007 | Institut Botanique Liège, Jeugdkliniek Kloetinge, Juch-Areal Zürich, K118 Winterthur, KA13 Oslo (5) | ✅ done | `norm_ns_3682`, `norm_tek_norway`, `norm_sia`, `tool_bim_bauteilkatalog` delta |
| 008 | Kamikatsu, Kindergarten Manegg Zürich, Liander HQ Duiven, Lo-Reninge, Lokomotion Tampere (5) | ✅ done | `norm_en_1168`, `tool_bauteilkatalog` delta |
| 009 | Lycée Michel Lucius Luxembourg, Maison des Canaux, Maison DnA Asse, Maison Vignette Auderghem, Mehrow (5) | ✅ done | no delta |
| 010 | — | ⏳ next | |
| … | … | … | ~11 further batches to full coverage |

**Projection:** 98 total – 44 done = **54 remaining** ÷ 5/batch ≈ **11 more batches**.

---

## Import Procedure

### One-time setup (run once per database lifetime)
```bash
# 1. Constraints — enforce unique IDs
cypher-shell < "_neo4j/neo4j batch/neo4j_repo_output_contract_v1_1/neo4j_repo_output_contract_v2/cypher/constraints.cypher"

# 2. Controlled vocabulary seed — idempotent MERGE, safe to re-run
python _scripts/import_jsonl_to_neo4j.py \
  "_neo4j/neo4j batch/neo4j_repo_output_contract_v1_1/neo4j_repo_output_contract_v2/controlled_vocabulary.seed.kg.jsonl"
```

### Per-batch import
```bash
BATCH_DIR="_neo4j/neo4j batch/neo4j_batch_003_exports/batches/batch_003"

# 3. Delta vocabulary (skip if file is empty)
python _scripts/import_jsonl_to_neo4j.py "$BATCH_DIR/controlled_terms.delta.jsonl"

# 4. Project files — importer handles node-before-rel ordering internally
for f in "$BATCH_DIR"/p_*.kg.jsonl; do
  python _scripts/import_jsonl_to_neo4j.py "$f"
done
```

**All imports use `MERGE` on `id` — re-running a batch is safe and idempotent.**

---

## Controlled Vocabulary Governance

The global seed holds all shared taxonomy nodes: `Bauteiltyp`, `Material`, `Huerde`,
`Akteurrolle`, `Status`, `Nutzung`, `Norm`, `WiederverwendungsArt`, etc.

### When a new term appears in a source file
1. Search the seed first — the concept may exist under a slightly different spelling.
2. If genuinely new: add it to the **batch's own `controlled_terms.delta.jsonl`** only.
3. After a term appears in **3+ batches**, promote it to the seed in a seed revision.

### Seed revision procedure
```
1. Collect all delta terms used by ≥3 different batches.
2. Append to controlled_vocabulary.seed.kg.jsonl.
3. Bump the contract version tag in the README.
4. Empty the relevant delta files (they now reference the seed).
```

**Never add terms to the seed mid-batch** — it breaks batch reproducibility.

---

## Per-Project File Rules

Each `p_{slug}.kg.jsonl` must satisfy (full checklist: `VALIDATION_CHECKLIST.md`):

| Rule | How to check |
|------|-------------|
| Exactly 1 `Projekt` node | `record_type=node, labels=[Projekt]` |
| At least 1 `Quelle` node, `quelltyp: case_markdown` | scan labels |
| Every `Bauteilgruppe` has `counts_as_direct_reuse` (bool) | property check |
| All `BELEGT_IN` carry `datenqualitaet: "Belegt"` | property check |
| All relationship endpoints resolvable (in file + seed + delta) | endpoint scan |
| No `Fallbeispiel`, `Kennwert`, or `Datenqualitaet` nodes | label blacklist |
| Every non-`Quelle` node has ≥ 2 edges inside the file | degree check |
| Metrics are scalar properties, not separate nodes | no `Kennwert` nodes |

---

## Validation Before Import

```python
# validate_batch.py — run from workspace root
# Usage: python validate_batch.py "_neo4j/neo4j batch/neo4j_batch_003_exports/batches/batch_003"
import json, glob, sys, os

SEED = "_neo4j/neo4j batch/neo4j_repo_output_contract_v1_1/neo4j_repo_output_contract_v2/controlled_vocabulary.seed.kg.jsonl"
BATCH = sys.argv[1]

known_ids = set()
errors = []

files_to_scan = [SEED, os.path.join(BATCH, "controlled_terms.delta.jsonl")] + \
                sorted(glob.glob(os.path.join(BATCH, "p_*.kg.jsonl")))

for path in files_to_scan:
    if not os.path.exists(path):
        continue
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
                if r.get("record_type") == "node":
                    known_ids.add(r["id"])
            except json.JSONDecodeError as e:
                errors.append(f"{path}:{i} JSON error: {e}")

for path in sorted(glob.glob(os.path.join(BATCH, "p_*.kg.jsonl"))):
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if r.get("record_type") == "rel":
                if r["from"] not in known_ids:
                    errors.append(f"{path}:{i} unknown from={r['from']}")
                if r["to"] not in known_ids:
                    errors.append(f"{path}:{i} unknown to={r['to']}")

if errors:
    for e in errors:
        print("ERROR:", e)
    sys.exit(1)
else:
    print(f"OK — {len(known_ids)} IDs resolved, no endpoint errors.")
```

---

## Selecting the Next 5 Cases

When preparing a new batch, choose cases where the source `index.md` is reasonably complete:

```powershell
# Update $done as batches complete
$done = @(
    "Berlin_Schildow_Pilot_House","Berlin_Schildow_Pilot_House_2",
    "Bestandverplanzung_Pavilion_Muenchen",
    "Big_Dig_Building_Boston","Big_Dig_House_Lexington_Massachusetts",
    "BioPartner_5_Leiden_Oegstgeest","BlueCity_Offices_Rotterdam",
    "Boulder_Fire_Station_3","Brent_Cross_Town_Primary_Substation_London",
    "Brighton_Waste_House_Brighton",
    "Broethen_Twin_House_Hoyerswerda","CascadeUp_London",
    "Charles_Malis_Molenbeek","Christ_Pavilion_Volkenroda","Chiro_d_Itterbeek_Dilbeek",
    "Circular_Centre_Netherlands","Circular_Pavilion_Paris",
    "CRCLR_House_Impact_Hub_Berlin","ELYS_Kultur_Gewerbehaus_Basel","Europa_Building_Brussels",
    "Ferme_du_Rail_Paris","gjG_House_Gentbrugge",
    "Grande_Halle_de_Colombelles","Grubenstrasse_29_Werkhof_29_Zuerich",
    "Harmalanranta_A_Kruunu_ReCreate_Tampere",
    "Hastings_Pier_Visitor_Centre","Haus_HOS_Mehrfamilienhaus_Muehlhausen",
    "Holbein_Gardens_London","House_of_Fraser_318_Oxford_Street_TBC_London",
    "Impact_Hub_Berlin_CRCLR_Fitout",
    "Institut_de_Botanique_ULg_Liege","Jeugdkliniek_Ithaka_Emergis_Kloetinge",
    "Juch_Areal_Recyclingzentrum_Zuerich","K118_Kopfbau_Halle_118_Winterthur",
    "KA13_Kristian_Augusts_Gate_13_Oslo",
    "Kamikatsu_Zero_Waste_Center_Hotel_WHY","Kindergarten_Moeoeslistrasse_Manegg_Zuerich",
    "Liander_Alliander_HQ_Duiven","Lo_Reninge_Town_Hall_Facade",
    "Lokomotion_Technology_Centre_Mini_Pilot_Tampere",
    "Lycee_Michel_Lucius_Conversion_Luxembourg","Maison_des_Canaux_Paris",
    "Maison_DnA_Asse","Maison_Vignette_Auderghem","Mehrow_Pilot_House"
)
Get-ChildItem "_database\fallstudie" -Directory |
    Where-Object { $done -notcontains $_.Name } |
    Select-Object -First 5 -ExpandProperty Name
```

Grouping tips:
- Cases in the **same country** share Stadt/Land nodes → fewer endpoints to define.
- Cases using the **same material** (timber, steel, concrete) keep delta empty.
- Avoid mixing highly uncertain cases with well-documented ones in the same batch.

---

## Useful Queries

**Import progress:**
```cypher
MATCH (p:Projekt)-[:BELEGT_IN]->(q:Quelle)
RETURN count(p) AS loaded, collect(q.name) AS sources
```

**Direct-reuse component coverage:**
```cypher
MATCH (btg:Bauteilgruppe)
RETURN btg.counts_as_direct_reuse AS flag, count(*) AS count
```

**Material flows:**
```cypher
MATCH (donor:Bauwerk)<-[:AUS_BAUWERK]-(btg:Bauteilgruppe)-[:EINGEBAUT_IN]->(receiver:Bauwerk),
      (btg)-[:NUTZT_MATERIAL]->(m:Material)
WHERE btg.counts_as_direct_reuse = true
RETURN m.name, count(*) AS uses ORDER BY uses DESC
```

**Barrier frequency across all cases:**
```cypher
MATCH (btg:Bauteilgruppe)-[:HAT_HUERDE]->(h:Huerde)
WHERE btg.counts_as_direct_reuse = true
RETURN h.name, count(*) AS n ORDER BY n DESC LIMIT 15
```

**Actor network — most connected firms:**
```cypher
MATCH (a:Akteur)-[:BETEILIGT_AN]->(p:Projekt)
RETURN a.name, count(p) AS projects ORDER BY projects DESC LIMIT 15
```

---

## File Locations Reference

| Path | Purpose |
|------|---------|
| `_database/fallstudie/` | ~98 source case study folders |
| `_database/_system/SCHEMA.md` | Ontology definition |
| `_neo4j/neo4j batch/neo4j_repo_output_contract_v1_1/…/controlled_vocabulary.seed.kg.jsonl` | Global taxonomy seed (330 nodes) |
| `_neo4j/neo4j batch/neo4j_repo_output_contract_v1_1/…/cypher/constraints.cypher` | DB constraints |
| `_neo4j/neo4j batch/neo4j_batch_{NNN}_exports/batches/batch_{NNN}/` | Per-batch JSONL output |
| `_neo4j/archieve/` | Legacy v1 batch (different schema — keep separate) |

---

## Environment

```
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=ENTWERFENMITBESTAND
```

---

## Supporting Scripts

| Script | Purpose |
|--------|---------|
| `import_database_folder_to_neo4j.py` | Legacy: imports directly from `_database/` |
| `neo4j_relation_fold.py` | Maps relation names to Neo4j types |
| `akteur_org_neo4j_label.py` | Resolves :Person vs org labels |
| `ort_geo_label.py` | Resolves :Land vs :Stadt |
| `export_neo4j_schema.py` | Dumps live schema from running Neo4j |
| `neo4j_graph_version.py` | Version tracking for graph state |
