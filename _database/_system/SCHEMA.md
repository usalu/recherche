---
title: "Canonical Schema — Reuse Knowledge Base + Graph"
status: "live"
last_updated: "2026-05-12"
supersedes:
  - "_migration/00_Migration_Strategy.md (frozen, kept as history)"
  - "_database/_system/migration_notes.md (frozen, kept as history)"
---

# Canonical Schema

Single source of truth for the entity model, vocabulary, and editing rules.
Future agents and reviewers should read **only this file** to understand the system. The older migration documents are historical context for how the current state was reached; they should not be used to make new decisions.

---

## 1. Goal

A **knowledge base** + a **graph** in one repository.

- **Knowledge base** = filled `.md` files in German under `_database/<entity>/<id>/index.md`.
- **Graph** = typed edges in `_database/_edges/clean_confirmed_edges.csv`, folded into **Neo4j** on import (normative typing: `.cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md`). Optional local **SQLite** rebuild from the same tree is supported but not authoritative (see §12).

Editing happens in `_database/`.

---

## 2. Trees

| Tree | Status | Role |
|---|---|---|
| `_database/` | **LIVE — edit here** | Canonical knowledge + graph |
| `Gebäude/` | **LIVE — extraction source** | Hand-curated case-study Markdown with structured Entitäten-Mapping tables. Read-only for the schema; new cases get added here, then extracted into `_database/`. |
| `_migration/` | Frozen tooling | Build/repair/validate scripts and decision logs. Do not run automatically unless you know which script you need. |
| `_archive/legacy/` | **Pointer only** | Contains `README.md`: the old mirrored trees (`_graph/`, `_extract/`, `_manual_review/`, flat entity stubs) were **removed from git** after migration into `_database/` (recover from git history if needed). |
| `_archive/dropped_knots/` | Provenance | Knot folders dropped during consolidation; original prose preserved. |

---

## 3. Entity Model

### 3.1 Core entities (heavy nodes — instances are the data)

| Entity | Purpose |
|---|---|
| `fallstudie` | Researched case/article/example as knowledge container. |
| `projekt` | Architectural/construction project. |
| `bauobjekt` | Building, infrastructure, interior fit-out, pavilion, depot, donor object, receiver object. |
| `akteur` | Office, company, authority, institution, person/group. |
| `reuse_einsatz` | **Query center.** One concrete reuse use-case of a component / material / system. |
| `reuse_kette` | Complete reuse chain. |
| `reuse_kettenstation` | Station in the chain (donor, storage, processing, marketplace, transport, receiver). |
| `quelle` | Report, article, database, project page, interview, document. |
| `datenpunkt` | Any measured or reported value (number + unit + scope + source). |
| `software_digitaltool` | Concrete tool/platform (Madaster, Concular, Restado, …). |

### 3.2 Relation entities (edges-as-nodes)

| Entity | Connects |
|---|---|
| `akteur_beteiligung` | `akteur` × `projekt`/`fallstudie` × `akteurrolle` |
| `bauobjekt_beteiligung` | `bauobjekt` × `reuse_kette` × `bauobjektrolle` |

### 3.3 Controlled knots

Bauobjekt context: `bauobjektklasse`, `bauobjektrolle`, `bauobjektstatus`, `nutzung`, `bauaufgabe_intervention`, `ort`.

Reuse context: `reuse_strategie`, `bewertungslogik_abgrenzung`, `reuse_einsatzstatus`, `ressourcenquelle`, `beschaffungsweg`.

Bauteil/Material: `bauteiltyp`, `bauteilebene`, `material`, `bauteilzustand`, `funktionswechsel`.

Tragwerk/Bauweise: `bauweise`, `bausystem`, `tragwerksprinzip`, `tragwerkstyp`, `fuegung_verbindung`.

Process: `prozessphase`, `rueckbauverfahren`, `aufbereitungsverfahren`, `logistik`, `methode`.

Requirements & barriers: `pruefung_nachweis`, `leistungsanforderung`, `norm`, `rechtliche_bedingung`, `schadstoff`, `huerde`.

Data & evaluation: `kennwertdefinition`, `datenqualitaet`, `zertifizierung_bewertungssystem`, `datenmodell`, `dokumenttyp`, `tooltyp`.

Context: `programm_kontext`, `kontextmerkmal`, `wirtschaft`, `foerderprogramm`.

Roles: `akteurrolle`.

---

## 4. Granularity Principle

**In-between granularity.** Two failure modes to avoid:

- **Too granular** → noisy graph, hard to query, fragments the same concept across many small knots (`Treppenwange`, `Leuchte`, `Stahlseil` as standalone types).
- **Too broad** → loses analytical power (`Tragstruktur`, `Metall`, `Bauwerksteil` as fallback types).

When in doubt, prefer **fewer canonical knots + richer per-instance fields**:

- The exact label (e.g. `"Brettschichtholz"`, `"Sekundärstahl"`, `"feuerverzinkter Stahl"`) is preserved on the `reuse_einsatz` frontmatter (`material_label`, `bauteil_label`).
- The canonical knot captures the queryable family.
- The prose body of the canonical knot can document the variants.

This means **dropping `material/Brettschichtholz` does NOT lose the BSH information**; the `reuse_einsatz` for the BSH beam still says `material_label: "Brettschichtholz"`. Queries can use the label for fine filtering and the canonical material for coarse filtering.

---

## 5. Bauteiltyp (canonical — 15 types)

Family-level component types only. Anything more specific stays as `bauteil_label` on the `reuse_einsatz`.

```
Stuetze, Traeger, Decke, Wand, Fassade, Fenster, Tuer, Treppe,
Dach, Boden, Ausbau, Technik,
Fundament, Gelaender, Daemmung
```

**Why these 15:**
- The user's 12 (Stütze … Technik) are the practical reuse families.
- `Fundament` (7 edges) is structurally distinct from `Boden`/`Decke` and reuse-relevant in Bestandserhalt cases.
- `Gelaender` (16 edges) is a recurring reusable family covering Brüstung/Geländer/Balustrade.
- `Daemmung` (18 edges) is a component layer distinct from the substance `material/Daemmstoff`.

**Drop & remap (~218 edges):**

| Drop | Remap to | Edges | Rationale |
|---|---|---:|---|
| `Innenausbau` | `Ausbau` | 21 | Same concept, different name |
| `Festes_Einbauteil` | `Ausbau` | 13 | Built-in is fit-out |
| `Sanitaerobjekt` | `Technik` | 45 | TGA/sanitary belongs to Technik |
| `Leuchte` | `Technik` | 35 | Lighting = Technik |
| `Akustikelement` | `Ausbau` | 6 | Acoustic panels = fit-out |
| `PV_Anlage` | `Technik` | 4 | PV = Technik |
| `Betonfertigteil` | per case to `Träger`/`Decke`/`Wand`/`Stütze` + edge to `bausystem/Betonfertigteil_System` | 16 | Manufacturing system, not component family |
| `Mauerstein_Block` | per case to `Wand` + edge to `material/Ziegel` or `Naturstein` | 9 | Substance + element separately |
| `Gitterrost` | `Boden` | 3 | Grating is floor surface |
| `Beschattung_Sonnenschutz` | `Fassade` | 3 | Shading = facade element |
| `Platte_Paneel` | per case to `Wand`/`Boden`/`Decke`/`Fassade` | 63 | Generic panel; resolve by use |

The 27 manual-review nodes folded in:
- `Auflager_Widerlager`, `Bauwerksteil`, `Tragstruktur`, `Kern`, `Landschaftselement` → drop
- `Bruestung` → `Gelaender`
- `Fliese` → `Wand`/`Boden`/`Dach` + `material/Keramik`
- `Holzrahmenelement` → `Wand` + `bausystem/Holzrahmenbau`
- `Kueche` → `Ausbau`
- `Treppenwange` → `Treppe`

---

## 6. Material (canonical — 14 substances)

```
Beton, Stahlbeton, Recyclingbeton,
Stahl, Aluminium, Gusseisen,
Holz,
Glas,
Ziegel, Naturstein, Keramik,
Kunststoff,
Daemmstoff,
Lehm, Stroh
```

**Why this set:**
- User's 11 substances (Beton…Dämmstoff) are the canonical material classes.
- `Recyclingbeton` is chemically distinct (recycled aggregate) and analytically important — different LCA than ordinary Beton.
- `Lehm` and `Stroh` are real distinct materials in low-impact construction (Anna Heringer typology).
- `Gusseisen` is created per the 27-review decision — cast iron is reuse-relevant and not = Stahl.

**Drop & merge:**

| Drop | Merge into | Edges | Where the variant info lives |
|---|---|---:|---|
| `Sekundaerstahl` | `Stahl` | 1 | `reuse_einsatz.material_label` says "Sekundärstahl"; `ressourcenquelle/Recycling` edge |
| `Brettschichtholz` | `Holz` | 5 | `material_label` + `bauteilebene/System` |
| `Brettsperrholz` | `Holz` | 4 | same |
| `Mineralwolle` | `Daemmstoff` | 4 | `material_label` |
| `Polystyrol` | `Daemmstoff` | 2 | `material_label` |
| `Sanitarkeramik` | `Keramik` | 0 | `material_label` |
| `Granit` | `Naturstein` | 4 | `material_label` |
| `Marmor` | `Naturstein` | 3 | `material_label` |
| `Faserzement` | `Beton` | 1 | `material_label` |
| `Composite` | per case → 2 material edges (e.g. Beton+Stahl) | 5 | The composition |
| `Textil` | per case → `Daemmstoff` or `Kunststoff` | 5 | `material_label` |
| `Beton-Fertigteile_Verbindungen` (legacy) | `methode/Verbindungen_im_Betonfertigteilbau` | n/a | — |
| `Metall` | drop entirely; per case → `Stahl`/`Aluminium`/`Gusseisen` | (none in clean) | Force precision; mark uncertainty via `datenqualitaet/unklar` edge |
| `Erde` | `Lehm` | (in review) | — |
| `Guss` | `Gusseisen` (new) | (in review) | — |

**Rule:** add the variant as a prose subsection in `material/<canonical>/index.md`. The substance taxonomy stays small and queryable.

---

## 7. Tragwerk / Bauweise / Bausystem

These three are intentionally distinct axes; do not collapse them.

| Knot | Question it answers |
|---|---|
| `bauweise` | What is the dominant construction approach? (Holzbauweise, Massivbauweise, Stahlbauweise, Hybridbauweise, Fertigteilbauweise) |
| `bausystem` | Which named construction system? (Betonfertigteil_System, Holzrahmenbau, Holzskelettbau, Stahl_Skelettbau, Plattenbau) |
| `tragwerksprinzip` | Which structural principle? (Skeletttragwerk, Massivtragwerk, Fachwerk, Rahmen, Plattentragwerk) |
| `tragwerkstyp` | Which material-typed structural system? (Holztragwerk, Stahltragwerk, Betontragwerk, wiederverwendetes Tragwerk, demontierbares Tragwerk) |
| `fuegung_verbindung` | Which connection technique? (geschraubt, gesteckt, geschweißt, geklebt, vergossen, reversibel, irreversibel) |

**`fuegung_verbindung` is atomic.** Material-overview entries (`Beton_Fertigteile_Verbindungen`, `Holz_Verbindungen`, `Stahl_Verbindungen`, `Composite_Verbindungen`) move to `methode/Verbindungen_im_<Material>bau`.

---

## 8. Reuse semantics

Three orthogonal axes, every `reuse_einsatz` should carry one edge to each.

- `reuse_strategie`: Direct Reuse, Same-Site Reuse, Urban Mining, Design for Disassembly, Bestandserhalt, Recycling, Upcycling, Remanufacturing.
- `reuse_einsatzstatus`: realisiert, geplant, verworfen, vorgeschlagen, unklar, temporär, prototypisch.
- `bewertungslogik_abgrenzung`: zählt als Direct Reuse, zählt nicht, Bestandserhalt separat, Recycling separat, Möbel separat, geplant aber nicht realisiert, unklar.

This separation prevents the "Direct Reuse overcounting" failure: temporary, planned, decorative, or recycling cases are visible but bounded.

---

## 9. Relation vocabulary (edges)

**Authoritative inventory:** [_database/_system/RELATION_CATALOG_NEO4J.md](RELATION_CATALOG_NEO4J.md) lists every distinct `relation` token present in the edge CSVs (row counts per file) and how each maps to Neo4j relationship types under the research-graph plan (§7.1). Regenerate that file after edge changes:

```text
python _scripts/extract_database_relations.py
```

As of the last catalog run, **`clean_confirmed_edges.csv`** carries **13,746** rows with a non-empty `relation` value across **46** distinct predicates. The older paragraph below counted **8,850** edges across **24** predicates; that snapshot is superseded by the growth of the confirmed edge set and additional `has_*` relations promoted from case material.

**Ontology semantics (source → target entity types)** remain as documented in the per-entity rules elsewhere in this file; the catalogue focuses on **coverage and Neo4j folding**, not on re-stating every allowed endpoint pair here.

**Gaps to fill** (relations the case data implies but the graph doesn't yet carry — see §11):

```
has_ressourcenquelle, has_beschaffungsweg, has_aufbereitungsverfahren,
has_logistik, has_funktionswechsel,
has_bauteilzustand, has_bauteilebene, has_bauweise, has_bausystem,
has_tragwerksprinzip,
has_bauobjektklasse, has_bauobjektrolle, has_bauobjektstatus, has_nutzung,
has_bauaufgabe_intervention, located_in_ort,
has_rechtliche_bedingung, has_schadstoff, has_kontextmerkmal,
has_zertifizierung_bewertungssystem, has_datenmodell, has_dokumenttyp,
has_tooltyp, uses_software_digitaltool,
documented_in_quelle, has_datenqualitaet,
involves_foerderprogramm, has_programm_kontext,
has_methode, has_wirtschaft
```

These should be added per case from the Gebäude Entitäten-Mapping tables; currently only the labels exist, not the relations.

---

## 10. Where to edit

| Want to … | Edit here |
|---|---|
| Refine a knot definition in German prose | `_database/<entity>/<id>/index.md` |
| Add a new case study | New `Gebäude/<Case_Name>.md` with the Entitäten-Mapping table; then run extractor (TBD script) to fold into `_database/` |
| Add a new entity type | This file (§3) → then create the folder under `_database/` |
| Add a new bauteiltyp / material / etc. | This file (§5/§6) → then create the folder under `_database/<entity>/<new_id>/` |
| Fix a wrong edge | `_database/_edges/clean_confirmed_edges.csv` (then re-run Neo4j import; optional local SQLite rebuild) |
| Define a new relation | This file (§9) → then add edges manually or via extractor |

Do **not** edit:
- `_migration/` batch outputs and frozen decision logs (unless you intentionally rerun a documented migration step).
- `_archive/dropped_knots/` except deliberate provenance housekeeping.

The `_archive/legacy/README.md` file explains removed legacy trees; do not resurrect old paths as a second live source.

---

## 11. Integrity status

### 11.1 Wrong edges — RESOLVED

47 `rule_low` edges with Stahlbeton-flavored labels routed to `material/Stahl` were re-resolved to `material/Stahlbeton` (batch 40a). Resolver bug `material_reinforced_concrete_contains_stahl` no longer in use. 0 `rule_low` edges remain.

### 11.2 Sparse relations — STILL OPEN

The confirmed edge CSV now carries many more rows and predicates than the early migration snapshot (see §9 and `RELATION_CATALOG_NEO4J.md`). Batch 50a promoted 248 high-precision `has_reuse_strategie` edges for direct reuse from the `Gebäude/` Entitäten-Mapping tables. Batch 50b promoted 21 high-precision `has_fuegung_verbindung` edges from the BAUTEIL-INVENTAR connection labels. Batch 50c promoted 407 conservative `has_reuse_einsatzstatus` edges from project-status bullets to substantive reuse_einsatz nodes. Batch 50d promoted 394 `has_prozessphase` edges from explicit Eingriff/Aufbereitung labels. Batch 50e promoted 84 `has_rueckbauverfahren` edges from explicit dismantling-method labels. Many other case-context relations remain sparse (see §9 gaps); continue one relation at a time so each batch stays reviewable.

### 11.3 Encoding — RESOLVED

Promoted `index.md` files (batch 42) are UTF-8 without BOM. 0 mojibake titles remain. The legacy build script that introduced the regression should still be patched if it's ever rerun, but the live tree no longer carries the bug.

### 11.4 Path length — WORKAROUND IN PLACE

Some generated paths under `_database/akteur_beteiligung/` and `_database/reuse_einsatz/` exceed Windows MAX_PATH (260 chars). Use `git -c core.longpaths=true` for any git operation that touches them, or set `core.longpaths = true` once in your git config.

### 11.5 Index.md stub — RESOLVED

Batch 42 lifted German prose from `DATEIEN/*.staging_index.md` into `index.md` for 2,986 of 2,987 nodes. 1 canonical knot (`prozessphase/Pruefung`) is a stub awaiting human-written content. Editors opening `index.md` now see real knowledge instead of empty stubs.

### 11.6 Manual-review queue — RESOLVED

All 27 manual-review nodes have been processed (batch 43): 95 edges deleted (target dropped per schema), 19 single-target moves applied, 114 edges split per case via raw_label heuristics. `clean_edge_review_queue.csv` is empty. Historical `_manual_review/` copies that lived under `_archive/legacy/` were removed from the repository in 2026-05 (see `_archive/legacy/README.md`); use git history if you need the exact staging files.

---

## 12. Build & query

**Research graph (normative per plan).** Load `_database/` into Neo4j with `_scripts/import_database_folder_to_neo4j.py` (see `_database/_system/NEO4J_SCHEMA.md` and `.cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md`).

**Optional local SQLite (not tracked in git).** If you want a file-based SQL mirror for one-off queries, rebuild locally:

```text
python _migration/build_phase24_sqlite_database.py
# Writes: _database/_system/reuse_ontology.sqlite (ignored by git — see repo .gitignore)
```

Do not treat SQLite schema or queries as authoritative for Neo4j typing; the plan and `neo4j_relation_fold.py` are.

Query center in the **folder model** is still `reuse_einsatz`; expand from there to `fallstudie → projekt → bauobjekt`, `material`, `bauteiltyp`, `huerde`, `pruefung_nachweis`, `norm`, `kennwertdefinition`, `quelle`.

---

## 13. Notes for other agents

- **First read [HANDOFF.md](../../HANDOFF.md) at the repo root.** It tells you what's done, what's next, and the conventions you must follow.
- This file is the canonical schema. If it conflicts with `_migration/00_Migration_Strategy.md`, this file wins.
- Do not propose a new entity type without a §3.x update.
- Do not promote a raw label into a new knot if it can be expressed as `material_label` / `bauteil_label` on the `reuse_einsatz` frontmatter — see §4.
- When auditing edges, the source of truth is the Entitäten-Mapping table in `Gebäude/<case>.md`, not the existing edges (which were machine-generated and contain the issues in §11).
- Keep changes small and committed individually so the dirty-tree problem from the prior migration does not recur.
