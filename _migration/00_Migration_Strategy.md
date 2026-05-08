# Migration Strategy: Old Repo to New Knowledge Graph

Status: planning only. No legacy content has been moved.

This document explains how to migrate the current Markdown repo into the new SQLite/Tolaria-ready structure. The companion control sheet is:

- `legacy_to_new_map.csv` - one row for every Markdown file found in the repo, excluding the final database draft files.
- `content_pattern_audit.csv` - one row per Markdown file with detected headings, tables, links, URLs, source sections, case-table markers, platform terms, certification terms, donor/receiver terms, and numeric-value markers.
- `folder_content_audit.csv` - folder-level count of files, URLs, tables, high-risk content markers, and empty files.
- `high_risk_review.csv` - rows that must be manually reviewed before migration.
- `canonical_duplicate_review.csv` - likely canonical target collisions, excluding harmless index merges.
- `duplicate_target_review.csv` - all duplicate primary targets, including index merges.
- `target_reference_review.csv` - duplicate references across primary and secondary targets.
- `content_risk_review.csv` - files where content markers suggest extra care even if the semantic target is probably correct.

Current inventory covered by the control sheet:

- Markdown files checked: 567
- Final database/inventory drafts excluded intentionally
- `_migration` planning files excluded from the old-repo inventory
- Index files included
- Root overview files included
- Generated extraction notes included as import/staging material

Triple-check status:

- Filesystem vs. `legacy_to_new_map.csv`: all 567 legacy Markdown files accounted for.
- Rows with missing action or target: 0.
- Placeholder root-index targets such as `target_entity_index_for_*`: 0 after correction.
- Empty legacy files found: `beispiel.md`; mapped to archive/import source.
- High-risk rows: tracked in `high_risk_review.csv`.
- Content-pattern risk rows: tracked in `content_risk_review.csv`.
- Canonical target collisions: tracked in `canonical_duplicate_review.csv`.

## 1. Main Decision

Do not migrate old folders 1:1.

The old repo mixes four different semantic levels:

1. Real entities: actors, projects, buildings, platforms, sources.
2. Controlled knots: material, bauteiltyp, prozessphase, norm, huerde.
3. Relation/event nodes: reuse_einsatz, reuse_kette, actor roles, building roles.
4. Source/staging notes: reports, prompts, extracted tables, contact lists, old indexes.

The new graph should separate those levels before any file is moved.

## 2. Final Target Model

Core entities:

- `fallstudie`
- `projekt`
- `bauobjekt`
- `akteur`
- `reuse_einsatz`
- `reuse_kette`
- `reuse_kettenstation`
- `software_digitaltool`
- `quelle`
- `datenpunkt`

Relation entities:

- `akteur_beteiligung`
- `bauobjekt_beteiligung`
- `reuse_einsatz_bauteil`
- `reuse_einsatz_material`
- `reuse_einsatz_nachweis`
- `reuse_einsatz_huerde`
- `reuse_einsatz_logistik`
- `reuse_einsatz_datenpunkt`
- `reuse_einsatz_tool`
- `beleg`

Controlled knots:

- `bauteiltyp`
- `bauteilebene`
- `material`
- `bauteilzustand`
- `schadstoff`
- `bauweise`
- `bausystem`
- `tragwerksprinzip`
- `tragwerkstyp`
- `fuegung_verbindung`
- `reuse_strategie`
- `reuse_einsatzstatus`
- `bewertungslogik_abgrenzung`
- `ressourcenquelle`
- `beschaffungsweg`
- `funktionswechsel`
- `prozessphase`
- `rueckbauverfahren`
- `aufbereitungsverfahren`
- `methode`
- `logistik`
- `leistungsanforderung`
- `pruefung_nachweis`
- `norm`
- `rechtliche_bedingung`
- `zertifizierung_bewertungssystem`
- `huerde`
- `kennwertdefinition`
- `datenqualitaet`
- `datenmodell`
- `dokumenttyp`
- `tooltyp`
- `plattformfunktion`
- `plattformzugang`
- `wirtschaft`
- `foerderprogramm`
- `programm_kontext`
- `bauobjektklasse`
- `bauobjektrolle`
- `bauobjektstatus`
- `bauaufgabe_intervention`
- `gebaeudetypologie`
- `nutzung`
- `ort`
- `akteurtyp`
- `akteurrolle`
- `akteurleistung`
- `kontextmerkmal`

## 3. Migration Actions

Every old file receives exactly one migration action in the control sheet:

- `move_as_core` - file becomes a real node, usually `akteur` or `software_digitaltool`.
- `move_as_knot` - file becomes a controlled vocabulary node.
- `semantic_move` - old folder is misleading; move to a more precise semantic target.
- `semantic_split` - file contains more than one semantic concept; split into several target nodes.
- `split_into_case_graph` - rich building/case file; extract case, project, buildings, reuse cases, data points, and sources.
- `split_platform_profile` - Bauteilboerse/platform file; split into platform, operator actor, procurement path, source type, platform function.
- `split_into_knots` - file contains multiple knot types, e.g. material-specific connections.
- `keep_or_split_case` - already a case but still needs extraction of subnodes.
- `archive_as_source` - keep as raw evidence/staging; do not create graph node directly.
- `archive_or_source` - report-like file; use as evidence unless it is clearly an external source.
- `merge_into_index` - index/root overview content goes into the new index or archive.
- `keep_meta` - repo/migration documentation, outside content graph.
- `semantic_review` - needs manual review before migration.
- `semantic_review_split` - unsorted or ambiguous file; must not be auto-imported.

## 4. Folder-by-Folder Migration

### `Gebaeude` and `gebaeude`

These are the most important content stores. Do not migrate a file as only one `bauobjekt`.

Each building example becomes:

- one `fallstudie`
- one or more `projekt`
- one or more `bauobjekt`
- one or more `reuse_einsatz`
- zero or more `reuse_kette`
- zero or more `reuse_kettenstation`
- many `datenpunkt`
- many `quelle`

Rules:

- Donor and receiver are `bauobjektrolle`, not separate entity types.
- Bestandserhalt is not automatically Direct Reuse.
- Planned reuse is not the same as realized reuse.
- Furniture/decorative loose objects must be marked through `bewertungslogik_abgrenzung`.
- Every quantity, area, cost, CO2 value, reuse percentage, and date becomes `datenpunkt`.
- Every source conflict stays visible; do not smooth values.

Files with multiple cases or analysis content, such as direct reuse example lists and entity-analysis files, become `90_import_rohdaten` or `quelle`, not case nodes.

### `bauteil`

Old `bauteil` files are generic component types.

Move to:

- `bauteiltyp`

Do not confuse these with concrete reused components. Concrete reused packages are `reuse_einsatz`.

Examples:

- `bauteil/Traeger.md` -> `bauteiltyp/Traeger`
- `bauteil/Deckenplatte.md` -> `bauteiltyp/Deckenplatte`
- `bauteil/Betonfertigteil.md` -> `bauteiltyp/Betonfertigteil`

### `material`

Most files stay in `material`.

Exception:

- `*_Verbindungen.md` files move/split to `fuegung_verbindung`, with a link back to the material.

Examples:

- `material/Stahl.md` -> `material/Stahl`
- `material/Stahl_Verbindungen.md` -> `fuegung_verbindung/Stahl_Verbindungen` + `material/Stahl`
- `material/Holz_Verbindungen.md` -> `fuegung_verbindung/Holz_Verbindungen` + `material/Holz`

### `tragwerkssystem`

This folder is semantically too broad. Use the logic already agreed:

First classify the true entity:

- Bauaufgabe
- Bauweise
- Bausystem
- Tragwerksprinzip
- Tragwerkstyp
- Bauteiltyp
- Fuegung/Verbindung
- Reuse strategy

Then derive the appropriate structural type.

High-risk mappings:

- `Aufstockung_in_Holzbauweise` -> `bauaufgabe_intervention/Aufstockung` + `bauweise/Holzbauweise` + `tragwerkstyp/Holztragwerk`
- `Betonfertigteil_System` -> `bausystem/Betonfertigteil_System` + `tragwerkstyp/Betonfertigteiltragwerk`
- `Dachtragwerk_und_Fachwerk` -> `tragwerkstyp/Dachtragwerk` + `tragwerksprinzip/Fachwerk`
- `Design_for_Disassembly` -> `reuse_strategie/Design_for_Disassembly` + `methode/Design_for_Disassembly`
- `Reversible_Fuegung` -> `fuegung_verbindung/Reversible_Fuegung` + `tragwerkstyp/Demontierbares_Tragwerk`
- `Tragende_Wand` -> `bauteiltyp/Tragende_Wand` + `tragwerksprinzip/Wandtragwerk`
- `to_sort/*` -> manual review only, no auto-import

### `verbindung`

Rename to:

- `fuegung_verbindung`

Preserve demountability, reversibility, material compatibility, and proof implications.

### `abbruchmethode`

Rename to:

- `rueckbauverfahren`

Reason: this is not generic demolition; in reuse it is deconstruction/harvesting logic.

### `aufbereitungsmethode`

Rename to:

- `aufbereitungsverfahren`

Use for cleaning, repair, remanufacturing, refurbishing, quality assurance.

### `pruefung`

Rename to:

- `pruefung_nachweis`

Reason: many files are not just tests, but proof paths: static proof, fire proof, material proof, condition assessment.

### `norm`

Split carefully:

- Real norms stay in `norm`: DIN, EN, ISO.
- Requirement-like files move to `leistungsanforderung`: `F90`, `R90`, `REI90`, `Feuerwiderstand`, `Brandschutzanforderung`.
- Regulatory classification like `EU_Taxonomie` moves to `rechtliche_bedingung` and links to `datenmodell/Taxonomie`.

### `recht`

Move to:

- `rechtliche_bedingung`

Do not merge with `huerde`. Law is the condition; huerde is the obstacle or effect.

### `kennwert`

Rename to:

- `kennwertdefinition`

These files define value types. Actual values from case files become `datenpunkt`.

### `dokument`

Most files become:

- `dokumenttyp`

But concrete databases/tools are reviewed:

- `Opalis_Datenbank` -> `software_digitaltool/Opalis`
- `Materialdatenbank` -> `datenmodell/Materialdatenbank`

### `methode`

Keep real methods in `methode`.

Move or link ambiguous items:

- `Materialpass` -> `dokumenttyp/Materialpass` + `datenmodell/Materialpass_Schema`
- `Bestandserhalt` -> `reuse_strategie/Bestandserhalt` + `bewertungslogik_abgrenzung/Bestandserhalt_separat`
- `Design_for_Disassembly` -> `reuse_strategie/Design_for_Disassembly` + method notes

### `reuse_strategie`

Keep, but connect every strategy to `bewertungslogik_abgrenzung`.

Critical distinction:

- Direct Reuse
- Bestandserhalt
- Recycling
- Refurbishment
- Upcycling
- Design for Disassembly without actual reuse
- planned but not realized reuse

### `logistik`

Mostly stays `logistik`.

Exception:

- `ReUse_Centre` should also become `bauobjektklasse/Reuse_Centre` and possible `reuse_kettenstation`.

### `bauteilboerse`

Do not preserve as a core entity.

Each file becomes a platform profile:

- `software_digitaltool/<platform>`
- `tooltyp/digitale_bauteilboerse` or related type
- `plattformfunktion`
- `beschaffungsweg/Digitale_Plattform`
- `ressourcenquelle/Bauteilboerse`
- `akteur/<operator_if_named>`

This is a high-duplicate folder. Canonicalization is mandatory against:

- `werkzeug/*`
- `akteur/06_bauteilboersen_marktplaetze_handel/*`
- `akteur/08_digitale_plattformen_daten/*`

Additional correction from the content audit:

- `akteur/06_bauteilboersen_marktplaetze_handel/*` is not pure actor content. These files are hybrid marketplace/operator profiles. Keep the operator as `akteur`, but also create or link `software_digitaltool`, `tooltyp/Bauteilboerse`, `beschaffungsweg/Bauteilboerse`, and `ressourcenquelle/Bauteilboerse`.
- `akteur/08_digitale_plattformen_daten/Madaster.md` is primarily a platform/material-cadastre profile, with actor/operator data attached.
- `akteur/08_digitale_plattformen_daten/Abriss_Atlas.md` is primarily a digital monitoring/GIS tool, not primarily an actor.
- `akteur/05_reuse_beratung_prozessdienstleister/Concular.md` is a hybrid actor/platform/process profile. It must create or link `akteur/Concular`, `software_digitaltool/Concular_Plattform`, `software_digitaltool/Restado`, relevant methods, and resource-pass/data-model concepts.

### `werkzeug`, `software`, `tools`

Most files become:

- `software_digitaltool`

But classify first:

- generic BIM/IFC/GIS concepts may become `datenmodell` or `tooltyp`
- material passports may become `dokumenttyp` and `datenmodell`
- DGNB resource pass connects to `zertifizierung_bewertungssystem/DGNB`
- duplicate marketplace files merge with `bauteilboerse` platform nodes

### `akteur`

Each real organization becomes:

- `akteur`

Old subfolder names become:

- `akteurtyp`
- sometimes `akteurrolle`

Examples:

- `04_planung_architektur_ingenieurwesen` -> actor type / capability
- `06_bauteilboersen_marktplaetze_handel` -> actor type plus platform relation
- `08_digitale_plattformen_daten` -> actor type and possible software relation

Do not create separate entity classes for Architekt, Bauherr, Tragwerksplaner. Those are roles in `akteur_beteiligung`.

### `person`

Real person profiles become:

- `akteur` with `akteurtyp/Person`

Contact lists and interview-priority lists become:

- `quelle` or `90_import_rohdaten`

They must not become one giant person node.

### `projekt`

Most old files are not concrete projects. They are intervention/project-type vocabulary.

Move to:

- `bauaufgabe_intervention`
- `kontextmerkmal`
- `reuse_einsatzstatus`

Concrete projects should be extracted from case files instead.

### `fallstudie`

Keep real case studies as `fallstudie`, but extract subnodes.

Some platform/program cases need semantic move:

- `Opalis` -> `software_digitaltool/Opalis` plus optional platform case
- `PREUSE` -> `foerderprogramm/PREUSE` and/or research project

### `bericht`

Treat as source/evidence by default:

- `quelle`

If a report contains structured actor/case/tool knowledge, extract it into those canonical nodes and attach the report as evidence.

### `ort`

Move to `ort`, but normalize hierarchy and spelling.

Known risk:

- `Scwheiz` should become `Schweiz`; the migration map now targets `ort/Schweiz` while preserving the legacy typo path as alias/evidence.

### `root *.md`

Root-level category files are old overview/type files.

Default action:

- merge into the relevant new index
- or archive as old schema/source note

Loose people:

- `dirk-hebel.md` -> `akteur/Dirk_Hebel`
- `kerstin-mueller.md` equivalent -> `akteur/Kerstin_Mueller`

Root type stubs:

- `bauteilboerse.md`, `tool.md`, `interview.md`, `gastprofessur.md`, `professur.md`, and similar one-screen type files are not content nodes. They merge into the relevant target index or vocabulary.
- `nachhaltiges-bauen.md` is a very short professorship/profile stub. It can become `akteur/Nachhaltiges_Bauen` only if later enriched; otherwise archive or merge it as a type stub.

## 5. Content Extraction Rules

### Controlled-knot file

Extract:

- title
- aliases
- old type
- short definition
- relevance
- fachinhalt
- examples
- challenges/open questions
- sources
- links to related knots

Create:

- one knot node
- optional edges to materials, components, phases, proofs, norms

### Building/case file

Extract:

- `fallstudie`: title, decision, rating, confidence, warnings, scope
- `projekt`: name, type, dates, status, intervention
- `bauobjekt`: physical objects, donor, receiver, same-site object, depot
- `reuse_einsatz`: every reused component/material package
- `reuse_kette`: donor to receiver chain
- `reuse_kettenstation`: donor, storage, processor, platform, transport, receiver
- `akteur`: all named actors
- `akteur_beteiligung`: actor roles
- `datenpunkt`: all numeric values
- `quelle`: all cited URLs, PDFs, reports
- `huerde`: barriers with cause/effect/solution
- `bewertungslogik_abgrenzung`: whether it counts as Direct Reuse

Never flatten the case into one building node.

### Platform file

Extract:

- platform name
- operator
- country/region
- platform type
- platform function
- component categories
- listing data fields
- logistics/storage model
- quality/proof model
- business model
- source URLs

Create or link:

- `software_digitaltool`
- `akteur`
- `tooltyp`
- `plattformfunktion`
- `beschaffungsweg`
- `ressourcenquelle`
- `reuse_kettenstation` if it includes depot/storage/market station

### Actor file

Extract:

- canonical actor name
- actor type
- actor roles/capabilities
- region
- related projects/cases/tools
- sources

Roles are relations, not entity types.

### Report/source file

Extract:

- source metadata
- source type
- date if present
- author/publisher if present
- cited URLs
- claims that become `datenpunkt` or evidence edges

Do not duplicate knowledge already in canonical nodes.

## 6. Failure Modes and Prevention

### Duplicate nodes

Risk:

- Restado, RotorDC, Opalis, Madaster, Concular, Cycle Up, SalvoWEB, Loopfront appear in multiple folders.

Prevention:

- canonical node first
- all old paths stored in `legacy_paths`
- duplicate report before migration
- no new node if normalized name already exists

### Wrong semantic level

Risk:

- `Bauteilboerse` becomes a core entity.
- `Architekt` becomes a core entity.
- `Donorgebaeude` becomes a core entity.
- `F90` stays as a norm.
- `Aufstockung` stays as a project.

Prevention:

- use type decision tree before import
- roles become relation attributes
- project/intervention types become knots

### Lost evidence

Risk:

- sources at the bottom of old files disappear during splitting.

Prevention:

- every migrated node keeps `legacy_paths`
- every source URL becomes `quelle`
- every extracted claim receives a `beleg` edge

### Data conflicts hidden

Risk:

- area, CO2, cost, quantity, and percentage conflicts get averaged.

Prevention:

- every value becomes its own `datenpunkt`
- mark `datenqualitaet`
- use `quellenkonflikt = true`
- choose preferred value only with explanation

### Direct Reuse overcounting

Risk:

- Bestandserhalt, recycling, loose furniture, planned reuse, or DfD get counted as actual Direct Reuse.

Prevention:

- mandatory `bewertungslogik_abgrenzung`
- mandatory `reuse_einsatzstatus`
- separate `Bestandserhalt` from `Direct Reuse`

### Broken links

Risk:

- renaming umlauts, folders, or slugs breaks old Markdown links.

Prevention:

- migration alias table
- old path stored in every target node
- update links only after target exists
- run broken-link audit after each batch

### Index knowledge lost

Risk:

- index files contain gaps, clusters, and category-level thinking.

Prevention:

- migrate every `index.md` into target index or `meta`
- never delete old index before reviewing `Offene Luecken`

### Over-splitting

Risk:

- too many small entities create a noisy graph.

Prevention:

- only core entities become heavy nodes
- stable controlled terms become knots
- one-off concepts become fields or aliases unless repeated

### Under-splitting

Risk:

- rich case files stay as one note and Tolaria cannot query donor, receiver, material, hurdle, law, logistics.

Prevention:

- building/case files must use `split_into_case_graph`
- every reused component package becomes `reuse_einsatz`

## 7. Migration Phases

### Phase 0: Freeze

- freeze final entity list
- freeze relation vocabulary
- freeze slug rules
- do not move content yet

### Phase 1: Review control sheet

- open `legacy_to_new_map.csv`
- filter `semantic_review`, `semantic_review_split`, `semantic_split`, `split_platform_profile`
- manually confirm high-risk rows

### Phase 2: Create empty target skeleton

Create target folders only, no content moves yet.

Every new entity follows:

```text
ENTITY/
  ID/
    index.md
    DATEIEN/
```

### Phase 3: Migrate easy knots

Do first:

- `material`
- `bauteil`
- `prozessphase`
- `leistungsanforderung`
- `schadstoff`
- `huerde`
- `wirtschaft`
- `datenmodell`

Reason: they are stable references for later case extraction.

### Phase 4: Migrate semantic correction folders

Do next:

- `tragwerkssystem`
- `norm`
- `recht`
- `methode`
- `dokument`
- `abbruchmethode`
- `aufbereitungsmethode`
- `pruefung`
- `verbindung`

Reason: these contain misfiled concepts that affect many links.

### Phase 5: Canonicalize actors and platforms

Do before building cases:

- `akteur`
- `person`
- `bauteilboerse`
- `werkzeug`
- `software`
- `tools`

Reason: case files reference these repeatedly.

### Phase 6: Migrate cases/buildings

Do after knots and actors exist:

- `Gebaeude`
- `gebaeude`
- `fallstudie`

For each case:

1. create `fallstudie`
2. create/link `projekt`
3. create/link `bauobjekt`
4. create `reuse_einsatz` per component package
5. create `reuse_kette` and stations
6. create all data points
7. attach sources
8. mark gaps and conflicts

### Phase 7: Migrate reports and loose files

Use:

- `bericht`
- root `*.md`
- `_extract`

as evidence, internal source, or archive.

### Phase 8: Tolaria graph validation

Before considering migration complete:

- no duplicate canonical platform nodes
- no orphan `reuse_einsatz`
- every `reuse_einsatz` has required minimum fields
- every `datenpunkt` has unit, source, and confidence
- every source conflict is preserved
- every old file path appears in `legacy_paths` or archive
- every index file was handled

## 8. Minimum Fields

### `reuse_einsatz`

Required:

- `id`
- `titel`
- `fallstudie`
- `projekt`
- `receiver_bauobjekt`
- `bauteiltyp`
- `material`
- `reuse_einsatzstatus`
- `bewertungslogik_abgrenzung`
- `ressourcenquelle` or `donor_bauobjekt`
- `datenqualitaet`
- `quelle`
- `legacy_paths`

### `datenpunkt`

Required:

- `id`
- `kennwertdefinition`
- `wert`
- `einheit`
- `bezugsobjekt`
- `bilanzrahmen`
- `quelle`
- `datenqualitaet`
- `quellenkonflikt`
- `legacy_paths`

### `software_digitaltool`

Required:

- `id`
- `titel`
- `tooltyp`
- `plattformfunktion`
- `region`
- `operator_akteur` if known
- `beschaffungsweg`
- `ressourcenquelle`
- `quelle`
- `legacy_paths`

### `akteur`

Required:

- `id`
- `titel`
- `akteurtyp`
- `region`
- `leistungen`
- `quelle`
- `legacy_paths`

## 9. Do-Not-Migrate-Automatically List

These categories need manual semantic review:

- `tragwerkssystem/to_sort/*`
- root overview files
- `person/*` contact and priority lists
- `bericht/*` detailed internal reports
- `_extract/*`
- `gebaeude/*direct_reuse_examples*`
- any file with duplicate target in `legacy_to_new_map.csv`

## 10. Success Criteria

The migration is successful only when:

- all 567 old Markdown files are accounted for
- every target node has a semantic type
- every old index is preserved or merged
- rich building examples are queryable by material, bauteiltyp, city, country, hurdle, law, norm, logistics, actor, platform, and reuse status
- Bauteilboersen are searchable as digital platforms without becoming a redundant core entity
- `reuse_einsatz` is the main query center
- no Direct Reuse claim is accepted without status, source, and evaluation logic
