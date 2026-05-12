# Handoff — Next Agent

**Read this first.** It tells you everything you need to continue the work without re-discovering it.

---

## 1. What this repo is

A **knowledge base + research graph** for building-component reuse (German prose + typed links), aligned with the **Neo4j schema plan** (source of truth for labels, five relationship types, and folding rules):

[`.cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md`](.cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md)

- **Knowledge:** Markdown under `_database/<entity>/<id>/index.md` (wikilinks welcome; any Markdown editor works).
- **Graph in Neo4j:** Import from `_database/` via `_scripts/import_database_folder_to_neo4j.py` (see `_database/_system/NEO4J_SCHEMA.md`).
- **Optional local SQLite:** `_migration/build_phase24_sqlite_database.py` can still materialize `reuse_ontology.sqlite` for ad-hoc SQL; the file is **not committed** (see `.gitignore`). Do not treat SQLite as co-equal with the plan—Neo4j semantics win.

The user's goal, in his own words: *"an interconnected clear system that acts as a readable map without getting overwhelmed with unnecessary connections and wrong unclear ones."*

---

## 2. Where things live

| Path | Status | What |
|---|---|---|
| `_database/` | **LIVE — edit here** | Canonical Markdown knowledge + edge CSV |
| `_database/_system/SCHEMA.md` | **Canonical reference** | Ontology folder layout, vocabulary, editing rules. **Read second.** |
| `_database/_edges/clean_confirmed_edges.csv` | Derived | Canonical typed edges (folded on Neo4j import). |
| `_database/_system/NEO4J_SCHEMA.md` | **Normative (narrative)** | Mirrors the Neo4j plan; import tooling implements the same rules. |
| `_database/_system/reuse_ontology.sqlite` | Optional local | Rebuild with `_migration/build_phase24_sqlite_database.py` if needed; **not tracked in git**. |
| `Gebäude/` | **LIVE — extraction source** | 76 hand-written case-study `.md` files with structured Entitäten-Mapping tables. New cases get added here, then extracted into `_database/`. |
| `gebaeude/` | User-managed | Separate from `Gebäude/`. User will update independently. |
| `_migration/` | Frozen tooling | All build/repair/migration scripts, batch reports, and decision logs. The scripts you might run are listed in §6. |
| `_archive/legacy/` | **Pointer** | Only `README.md`: the old mirrored trees were **removed from git** in 2026-05 after consolidation into `_database/` (recover via git history). |
| `_archive/dropped_knots/` | Provenance | Knot folders dropped during consolidation; original prose preserved. |
| Top-level `*.md` | Optional stubs | Short entity-type stubs at repo root; safe to delete if your editor does not need them. |

---

## 3. State at handoff

- **Repo hygiene (2026-05-12 — second pass):** Removed the entire **`_archive/legacy/`** working tree from git (~500+ duplicate/staging files: old `_graph/`, `_extract/`, `_manual_review/`, flat entity stubs). Added **`_archive/legacy/README.md`** explaining recovery via git history. Removed **`clean_confirmed_edges.csv.before_*`** backups and duplicate **`_database/_system/clean_import_readiness_report.md`** (keep `_migration/22_*` as the frozen report). Added **`_scripts/verify_plan_coverage.py`** — run after structural changes; it must exit 0 before you assume Neo4j import safety.
- **Repo hygiene (2026-05-12):** Earlier pass removed committed SQLite, phase6 CSV copies under `_database/_edges/`, Tolaria-only system docs, and tracked `__pycache__/`.
- **3,043 nodes, 9,256 edges, 0 dangling endpoints, 0 type mismatches.**
- 30 relation labels populated. Gap batches completed:
  - **50a** `has_reuse_strategie`: 248 edges
  - **50b** `has_fuegung_verbindung`: 21 edges
  - **50c** `has_reuse_einsatzstatus`: 407 edges
  - **50d** `has_prozessphase`: 394 edges
  - **50e** `has_rueckbauverfahren`: 84 edges
  - **50f** `located_in_ort`: 74 edges (53 city-level ort nodes auto-created)
  - **50g** `has_huerde`: 284 edges (28 hürde knots matched via token rules)
  - **50h** `has_pruefung_nachweis`: 4 edges
  - **50i** `has_beschaffungsweg`: 17 edges
  - **50j** `has_aufbereitungsverfahren`: 27 edges
- 0 edges in the review queue, 0 `rule_low` edges, 0 mojibake titles.
- `bauteiltyp` = 15 canonical types (matches schema §5 exactly).
- `material` = 15 (matches schema §6 + Recyclingbeton + Gusseisen).
- Every node `index.md` carries the German prose.
- **Root is clean:** 5 directories + 29 `.md` files (27 type stubs + AGENTS.md + HANDOFF.md).
- 35 legacy root folders had been moved to `_archive/legacy/` during consolidation; the **contents** of that archive were later **removed from git** (2026-05) once `_database/` was verified as the single live tree — see `_archive/legacy/README.md`.
- All root `.md` stubs renamed to canonical entity names.
- Person entries (`dirk-hebel.md`, `kerstin-müller.md`) promoted to `_database/akteur/`.
- Branch: `wip/kinan2`. Not pushed.

---

## 4. What's done — for context (do NOT redo)

In order of recent commits (newest → oldest):

```
Add Dismantling Edges
Add Process Edges
Add Status Edges
8be3ba73 Add Connection Edges
0855c706 Add Strategy Edges
0751877d Add Handoff Guide
f9390dac Update Schema Status
c8f9887e Apply Review Decisions
fca38656 Consolidate Edge Targets
bf0bcd7e Promote German Prose
23ecbd5e Consolidate Taxonomy Nodes
b9257f08 Remap Stahlbeton Edges
71e3073e Add Canonical Schema
94c9ca60 Build Clean Database
5b761442 Fix Encoding Fields
```

If you want to know what each batch did: read the commit message + the diff CSV in `_migration/40_remap_diff_*.csv` + `_migration/43_decision_log.csv`.

---

## 5. What to do next — in priority order

### Step 1: Extract remaining gap relations (CONTINUING)

**WHAT.** The graph now carries 30 populated relation types. Several are still missing:

```
Remaining missing relations (from SCHEMA.md §9):
has_ressourcenquelle, has_logistik, has_funktionswechsel,
has_bauteilzustand, has_bauteilebene, has_bauweise, has_bausystem,
has_tragwerksprinzip,
has_bauobjektklasse, has_bauobjektrolle, has_bauobjektstatus, has_nutzung,
has_bauaufgabe_intervention,
has_rechtliche_bedingung, has_schadstoff, has_kontextmerkmal,
has_zertifizierung_bewertungssystem, has_datenmodell, has_dokumenttyp,
has_tooltyp, uses_software_digitaltool,
documented_in_quelle, has_datenqualitaet,
involves_foerderprogramm, has_programm_kontext,
has_methode, has_wirtschaft
```

Done in batch 50a: `has_reuse_strategie` for high-precision direct-reuse rows (248 edges). Remaining strategy variants such as adaptive reuse, Bestandserhalt, DfD, upcycling, and refurbishment still need a more careful row-level pass before adding edges.

Done in batch 50b: `has_fuegung_verbindung` for high-precision direct-reuse component rows (21 edges). Most connection labels are `unbekannt` or ambiguous and intentionally remain unlinked in the skip report.

Done in batch 50c: `has_reuse_einsatzstatus` from the case-level `Projektstatus` bullet to substantive `reuse_einsatz` nodes (407 edges). Special statuses such as `Temporaer`, `Prototypisch`, `Geplant`, `Verworfen`, and `Unklar` take precedence over plain `Realisiert` so the graph does not overcount temporary, planned, prototype, or unbuilt cases.

Done in batch 50d: `has_prozessphase` from explicit `Eingriff/Aufbereitung` labels (394 edges). The extractor maps broad phases such as `Rueckbau`, `Aufbereitung`, `Wiedereinbau`, `Transport`, `Lagerung`, `Pruefung`, and `Identifikation`; labels that are only unknown or not substantive remain skipped.

Done in batch 50e: `has_rueckbauverfahren` from explicit `Eingriff/Aufbereitung` labels (84 edges). Generic `Rueckgewinnung`, plain `Rueckbau`, and `Innenausbau` are intentionally skipped unless the label names a concrete method such as Demontage, Ausbau, selektiver Rueckbau, Bergung, or schonender Rueckbau.

**WHY.** This is what turns "consolidated graph" into the "interconnected readable map" the user described. Right now you can ask "which cases use Holz?" but not "which Holz reuse cases happened in Wohnungsbau in Switzerland with Direct Reuse strategy?" — that needs the case-context edges.

**HOW.**
1. Read each `Gebäude/<Case>.md`. Each has structured tables: ENTITÄTEN-MAPPING, BAUTEIL-INVENTAR, PROZESS UND LOGISTIK, TECHNIK LEISTUNG NORMEN, KENNWERTE.
2. The **BAUTEIL-INVENTAR** and **PROZESS UND LOGISTIK** tables are the richest source — they map per-Bauteil to material, Eingriff, Verbindung, Prüfung, Norm, Hürde. One row → multiple edges.
3. Match each row to its `_database/reuse_einsatz/<case>__NNN__<bauteil>` source (already extracted).
4. Emit an edge per row-cell using the relation vocabulary.
5. Write an extractor at `_migration/50_extract_gap_relations.py` modeled on `40_apply_edge_remap.py`.
6. Continue **one relation at a time** so each batch is reviewable. Good next candidates: `has_logistik` from explicit Transport/Lagerung/Materialmatching cues, `has_aufbereitungsverfahren` from stronger Aufbereitung labels, or source/procurement relations such as `has_ressourcenquelle` and `has_beschaffungsweg`.
7. After each batch: run `python _scripts/verify_plan_coverage.py`, re-import Neo4j, optionally rebuild local SQLite, spot-check 3-5 cases against the source `.md`, commit.

**BLAST RADIUS.** Adds new edges only — won't break existing ones if you dedup. You'll roughly double the edge count when this is fully done.

**VERIFY.**
- `wc -l _database/_edges/clean_confirmed_edges.csv` should grow.
- `python _scripts/verify_plan_coverage.py` must exit 0.
- For relation R: optional local SQLite → `SELECT count(*) FROM edges WHERE relation='has_R'` should be plausible vs the case data.
- For one case, count edges from its `reuse_einsatz/*` and compare against the case's BAUTEIL-INVENTAR table size.

**ESTIMATE.** 2-3 sessions. Per-relation script work is 30-60 min each.

---

### Step 2: Map the 5 unmapped `gebaeude/*` files

**WHAT.** The original extraction report was archived into `_database/quelle/` (see `extract_Gebaeude_Entity_Extraction_md` / `Legacy_extract_Gebaeude_Entity_Extraction` and `DATEIEN/Gebaeude_Entity_Extraction.md`). Per that report, these `gebaeude/*` files were never mapped:
```
gebaeude/Elementa.md
gebaeude/gebäude2_wiederverwendung_direct_reuse_examples.md
gebaeude/gebäude3_wiederverwendung_direct_reuse_examples.md
gebaeude/gebäude4_wiederverwendung_direct_reuse_examples.md
gebaeude/gebäude_wiederverwendung_direct_reuse_examples.md
gebaeude/index.md
```

**WHY.** They're outside the graph today. Some are aggregates (lists of cases), some may be single cases.

**HOW.** Read each. If single case → run case-graph extraction (model on the existing reuse_einsatz extraction logic from Phase 4 — see `_migration/migrate_phase4_case_graph.ps1` for reference, but **don't run it**; write a fresh, equivalent script). If aggregate → archive to `_database/quelle/`.

**ESTIMATE.** 1 session.

---

### Step 3: Surface cleanup — optional

**WHAT.** (1) Root `*.md` type stubs — keep only if your Markdown tool still needs them; otherwise delete for a cleaner root. (2) Empty or obsolete root files (`schema.sql`, etc.).

**NOTE.** Legacy **`_archive/legacy/_graph/`** was removed from git to shrink the repo; do not try to “restore” it from docs—use `_database/` + `_migration/` logs if you need migration history.

**RISK.** Some editors expect certain root files; delete stubs only when you are sure.

**ESTIMATE.** Low effort.

---

### Step 4: Patch the legacy build script (defensive)

**WHAT.** `_migration/build_phase20_clean_database.ps1` introduced the encoding bug + path-length issue. It's frozen and unlikely to run again, but if someone *does* re-run it, the regression returns.

**HOW.**
1. Patch it to write UTF-8 without BOM (`Set-Content -Encoding utf8NoBOM`).
2. Cap node-ID generation at 80 chars + short hash suffix (e.g. SHA1 first 6) to stay under Windows MAX_PATH.
3. Or — simpler — just delete the script (the live tree is now the source of truth, no need to rebuild from `_graph/`).

**ESTIMATE.** <1 hour. Skip if the user says "we'll never rerun that."

---

### Step 5: Write a top-level `CLAUDE.md` (or update this `HANDOFF.md`)

**WHAT.** A 10-line orientation file at repo root for any agent (Claude Code, Codex, etc).

**HOW.** Cover: live tree, schema location, build command, what not to touch, where to find tooling. Probably this `HANDOFF.md` already serves the purpose; rename it `CLAUDE.md` if you want it picked up by Claude Code's auto-context.

---

## 6. Tooling — what each script does

**`_scripts/`** (Neo4j + catalog helpers; run from repo root with `python _scripts/<file>.py`):

| Script | Purpose | Idempotent? |
|---|---|---|
| `verify_plan_coverage.py` | **Read-only gate.** Confirms every `node_inventory.csv` entity maps to the Neo4j importer and every CSV `relation` token folds to a rel type or explicit `SKIP_RELATIONS`. | Yes |
| `import_database_folder_to_neo4j.py` | Loads inventory + folded edges into Neo4j. | Yes |
| `extract_database_relations.py` | Regenerates `_database/_system/RELATION_CATALOG_NEO4J.md`. | Yes |

**`_migration/`** (historical / maintenance; run only when you intend to):

| Script | Purpose | Idempotent? |
|---|---|---|
| `40_apply_edge_remap.py` | Extensible edge-remap engine. Add a batch by writing a function and registering in `BATCHES`. (Older runs wrote `clean_confirmed_edges.csv.before_*` backups; those are no longer kept in git.) | Yes per-batch |
| `41_apply_folder_cleanup.py` | Folder rename/archive engine. Drives the `FOLDER_OPS` list. Regenerates `node_inventory.csv`. | Yes |
| `42_promote_prose_to_index.py` | Lifts `DATEIEN/*.staging_index.md` body into `index.md`. Run on all entities or specific ones (`python ... material bauteiltyp`). | Yes |
| `43_apply_manual_review_decisions.py` | Already run; processes the held-back edge queue. Don't rerun unless the queue refills. | One-shot |
| `build_phase24_sqlite_database.py` | **Optional.** Rebuilds local `reuse_ontology.sqlite` from the folder tree (file gitignored). | Yes |
| `migrate_phase*.ps1` | **Frozen historical builders.** Do not run. They built the original `_graph/` and `_database/`. |  |
| `repair_phase13_encoding_mojibake.ps1` | Symptom fix; no longer needed since promotion fixed the root cause. |  |

Diff reports / logs:
- `_migration/40_remap_diff_*.csv` — each remap batch's before/after
- `_migration/43_decision_log.csv` — full decision audit for the 27 manual reviews
- `_migration/24_SQLite_Build_Report.md` — generated each rebuild

### Neo4j import preflight (run in this order)

1. **`python _scripts/verify_plan_coverage.py`** — must print `OK` and exit `0`. If it fails, fix `node_inventory.csv` / edge folding before touching Neo4j.
2. **`python _scripts/extract_database_relations.py`** — regenerates `_database/_system/RELATION_CATALOG_NEO4J.md`; commit if git shows a change.
3. **`pip install -r requirements-neo4j.txt`** — installs the Neo4j Python driver (`neo4j` 5.x).
4. **Configure auth** — set `NEO4J_URI` (default `neo4j://127.0.0.1:7687`), `NEO4J_USER`, `NEO4J_DATABASE` (must match the DB selected in Browser; often `neo4j`), and **`NEO4J_PASSWORD`**, *or* pass **`--password-file`** to a local one-line secret file. Never commit secrets (`.neo4j_password` and `_database/_system/.neo4j_password` are gitignored).
5. **Wipe + reload in one run** (destroys all nodes/relationships in that database, then imports from `_database/`):

   ```text
   python _scripts/import_database_folder_to_neo4j.py --confirm-wipe --wipe
   ```

   Use this when the graph has stale labels (e.g. old experiments). The current importer maps both `fallstudie` and `projekt` inventory rows to **`Fallbeispiel`** — it does **not** create an English `Project` label.
6. **Smoke test in Neo4j Browser** — e.g. `CALL db.labels() YIELD label RETURN label ORDER BY label` and spot-check counts vs script stdout.

---

## 7. Conventions you must follow

### Git

- **Always commit small batches.** Each script run gets its own commit.
- Commit message format: exactly three words in the subject, imperative if possible. Do not mention AI/agent authors and do not add co-author trailers unless the user asks.
- **Use** `git -c core.longpaths=true` for any `git add` / `git commit` that touches `_database/`. Some paths exceed Windows MAX_PATH.
- **Never push** unless explicitly asked.
- **Never change git config** (the user has a rule about this — use per-command `-c`).
- **Never use** `--no-verify` or `--force` unless explicitly asked.
- If a file is locked by another process: `git update-index --assume-unchanged <file>` and note it. Don't fight it. The user may have editors open on the vault.

### Editing

- **Edit only `_database/`** for content/structure. `_archive/` (except intentional housekeeping) and `_migration/` batch outputs = read-only unless you are running a documented migration step.
- **Edit `_database/_system/SCHEMA.md`** when introducing new entities, relations, or vocabulary changes. The schema doc is canonical for the **folder ontology** — the **Neo4j plan** is canonical for graph typing and import folding (`NEO4J_SCHEMA.md`, `neo4j_relation_fold.py`).
- **After structural folder changes:** regenerate `node_inventory.csv` (e.g. `python _migration/41_apply_folder_cleanup.py` when that workflow applies), then **Neo4j import** if you maintain a database: `python _scripts/import_database_folder_to_neo4j.py`. Optionally rebuild local SQLite for SQL-only exploration: `python _migration/build_phase24_sqlite_database.py` (artifact not committed).

### Encoding

- All `.md` and `.csv` files in `_database/` should be UTF-8 **without BOM**, LF line endings.
- If you find mojibake (`Hürde` → `HÃ¼rde`, `—` → `â€"`): the source file was Windows-1252 misread as UTF-8. Fix at the source, don't paper over.

### When in doubt

- **Read SCHEMA.md before proposing a new entity or relation.**
- **Use `Gebäude/<case>.md` as ground truth** — the auto-extracted edges may have errors; the human-written tables are authoritative.
- **Check with user before:** deleting large archived trees, pushing, force-pushing, or other destructive git operations.

---

## 8. Failure modes you'll likely hit

### Path too long (Windows MAX_PATH = 260)

Symptom: `error: open(...): Filename too long` from git, or `FileNotFoundError` from Python.

Fix: use `git -c core.longpaths=true` per command. Long IDs are mostly in `_database/akteur_beteiligung/<case>__NNN__<long_actor_name>` and `_database/reuse_einsatz/<case>__NNN__<long_bauteil>`.

### File locked by another process

Symptom: `error: open(...): Permission denied` even though ACL is fine.

Fix: another process (editor, VSCode, Codex) holds it. Ask user to close or use `git update-index --assume-unchanged` to skip. Currently affected: `_migration/migrate_phase8_promote_repeated_actors.ps1` and `_migration/migrate_phase1_stable_knots.ps1`.

### Resolver substring bias

Symptom: An auto-routed edge points at the wrong target because the label resolver matched on a substring (e.g. "Stahlbeton" → matched "Stahl" → routed to `material/Stahl`).

Fix: search for the pattern, use the source's `bauteil_label` / `material_label` to choose the right canonical. The `40_apply_edge_remap.py` per-case dispatcher (batch 40d) is the model — extend it.

### SQLite FK constraint failure

Symptom: `sqlite3.IntegrityError: FOREIGN KEY constraint failed` when running `build_phase24_sqlite_database.py`.

Cause: an edge references a node that doesn't exist (renamed/archived folder + edges still target old name).

Fix: run `41_apply_folder_cleanup.py` to regenerate inventory; ensure edge remap and folder rename were applied together. The scripts are designed to be run in pairs: 40_apply_edge_remap.py THEN 41_apply_folder_cleanup.py.

---

## 9. Deferred / open questions for the user

These need user input before some next steps proceed:

1. **Can legacy top-level folders move to `_archive/legacy/`?** (Only if any still exist at repo root; most are already archived.)
2. **Are root `*.md` type stubs still needed for your editor?** (e.g. `projekt.md`, `material.md`.)
3. **`material/Lehm` and `material/Recyclingbeton` weren't in the user's listed canonical material set** but were kept as distinct (per schema). Confirm at next checkpoint.
4. **5 unmapped `gebaeude/*` files** — are they single cases (extract) or aggregates (archive)?

---

## 10. Pointers to the user's stated preferences

From conversation history (in user memory + earlier turns):

- **Granularity: in-between.** Not too fine (don't split `Treppe` into `Treppenwange`), not too coarse (don't have a fallback `material/Metall`). The schema's bauteiltyp = 15 + material = 15 are the user-confirmed level.
- **Variant info goes on `reuse_einsatz`**, not as new knots. Brettschichtholz, Sekundärstahl, etc. are preserved as `material_label` on the case node, not as separate `material/` entries.
- **Working language: German** for content; English/German mixed for code/scripts.
- **Documents are for him AND for future agents** — write clearly, with examples and "why" alongside "what."
- **Commit messages:** exactly three words in the subject, no AI/agent author mentions.
- **Don't ask 5 questions when you can do 4 of them and ask 1.** The user said "lets go" twice — he wants forward motion with sensible defaults, not paralysis. But check in at clean breakpoints.

---

## 11. The user's main goal — in case you forget

> "I had a lot of correct edges at some point but everything got mixed up because of the migration. Most importantly for me is to have an interconnected clear system that acts as a readable map without getting overwhelmed with unnecessary connections and wrong unclear ones. It's important to work in a clear documented way so I can use other agent models and make it clear for them in the repo."

Translation:
1. Knowledge in German `.md` files. ✅ Done (Option A).
2. Graph that connects them, clearly, no junk. ✅ Sparse skeleton done; flesh is Step 1 above.
3. Documented for handoff to future agents. ✅ This file + SCHEMA.md.

---

**Start with Step 1.** It's the highest-value remaining work. When you're done with it (or want a checkpoint), update §3 of this file with the new state and add a commit-list entry to §4.

Good luck.
