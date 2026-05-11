---
name: Neo4j schema catalogue
overview: Design a clean, native property-graph schema for Neo4j that captures all information currently spread across the SQLite database, the edge CSV, and the YAML frontmatter under `_database/`. This first deliverable is the schema catalogue (Labels + Relationships + properties + constraints) as a Markdown spec; the export script and runtime are deferred.
todos:
  - id: spec-skeleton
    content: "Create _database/_system/NEO4J_SCHEMA.md with the section skeleton: Design decisions, Node Labels (Families A–D), Relationship Types (Groups G1–G8), Constraints & indexes, Coverage checklist, Renamings appendix."
    status: pending
  - id: design-section
    content: "Write the 'Design decisions' section: naming, one-label-per-entity, fallstudie/projekt/bauobjekt split, reified relations kept vs lifted, :Vokabular super-label, free-text label promotion strategy, Datenpunkt typing, Tragwerkstyp axis split, Quelle redesign, :Einheit vocab, typo fixes."
    status: pending
  - id: labels-section
    content: "Enumerate every Node Label across the 4 families. For each Label list: id key, title, properties (with origin in YAML frontmatter or SQLite), uniqueness constraint, indicative node count."
    status: pending
  - id: rels-section
    content: "Enumerate every Relationship Type across the 8 groups. For each rel-type list: source label(s) → target label, direction, cardinality, edge properties (raw_label, confidence, resolution_rule, seite, excerpt), populated-vs-gap status with current count."
    status: pending
  - id: constraints-section
    content: List all UNIQUE constraints, range/text indexes, and the full-text index over German body_md fields.
    status: pending
  - id: coverage-section
    content: "Write the coverage checklist: a table mapping every source artefact (folder under _database/<entity>/, every relation in clean_confirmed_edges.csv, every frontmatter field on ReuseEinsatz/Datenpunkt/Fallstudie/Bauobjekt) to its destination in the new schema. Explicitly list the ~30 gap relations from SCHEMA.md §9 as schema-present, data-empty."
    status: pending
  - id: renamings-appendix
    content: "Renamings appendix: Moebelsepearat → Moebel_separat, ort/Scwheiz → ort/Schweiz, tragwerkstyp split (wiederverwendetes_Tragwerk, demontierbares_Tragwerk → ReuseEinsatz.reuse_property), and the bauteiltyp/material drop-and-remap table from SCHEMA.md §5/§6 marked as 'already applied'."
    status: pending
isProject: false
---

## Goal

Produce one authoritative Markdown spec at `_database/_system/NEO4J_SCHEMA.md` that:

- Lists every Neo4j **Node Label** (with properties + uniqueness keys) we will create.
- Lists every Neo4j **Relationship Type** (with direction, endpoint labels, properties, cardinality).
- Spells out the design decisions that fix the inconsistencies flagged in [DATABASE_REVIEW_2026-05-11.md](DATABASE_REVIEW_2026-05-11.md).
- Maps every source artefact (folder under `_database/<entity>/`, edge row in `_database/_edges/clean_confirmed_edges.csv`, YAML frontmatter field) to where it lives in the new schema, so we can verify nothing is lost.

No code, no Neo4j instance, no export tooling — those come after the schema is signed off.

---

## Design decisions (will be the first section of the spec)

1. **Naming conventions.** Domain is German → keep German labels in PascalCase (`:Fallstudie`, `:ReuseEinsatz`, `:Bauteiltyp`). Relationships in SCREAMING_SNAKE following current edge names (`HAS_BAUTEILTYP`, `USES_MATERIAL`). This is also Neo4j idiom and lets the existing `clean_confirmed_edges.csv` be uppercase-mapped 1:1.

2. **One Label per entity type, not a generic `:Node`.** The current SQLite table `nodes` carries `entity` as a column; Neo4j gets that for free via labels. Unique constraint per label: `CREATE CONSTRAINT FOR (n:<Label>) REQUIRE n.id IS UNIQUE`.

3. **Resolve the "Fallstudie / Projekt / Bauobjekt share the same id" problem.** Keep them as three distinct nodes (they model three different things: research container, architectural project, physical building) joined by `(:Fallstudie)-[:HAS_PROJEKT]->(:Projekt)-[:REALIZES_BAUOBJEKT]->(:Bauobjekt)`. The shared id stops being a problem because Neo4j scopes uniqueness by label.

4. **Reified relationships kept where they carry context, lifted to edges where they don't.**
   - `:AkteurBeteiligung` stays as a node — it carries the 3-way relation `actor × case × role` plus optional time/phase, which a plain edge would lose.
   - `:BauobjektBeteiligung` stays for the same reason in `reuse_kette` context.
   - `:Datenpunkt` stays as a node — it's a measurement with `wert`, `einheit`, `bilanzgrenze`, `vertrauensgrad`, multiple source citations.
   - `:ReuseKettenstation` stays.
   - Edge-as-edge for `:HAS_BAUTEILTYP` etc.

5. **Super-label `:Vokabular` on all controlled-knot Labels.** Lets queries do `MATCH (v:Vokabular)` to enumerate the taxonomy without listing every label. Heavy/instance nodes do NOT get `:Vokabular`.

6. **Promote free-text `_label` fields to explicit edges where the target exists; keep as properties otherwise.**
   - `quelle_label` "S4, S2" → split, resolve against `:Quelle` nodes (which need to be created from each case's source register), create `[:CITES {raw_label: 'S4'}]` edges. Where resolution fails, retain `quelle_label_raw` as a property on the node.
   - `herkunft_label` → if a `:Bauobjekt` with that name exists, create `[:SOURCED_FROM_BAUOBJEKT]`. Otherwise keep `herkunft_label` as a property.
   - `alte_funktion` / `neue_funktion` → keep as properties on `:ReuseEinsatz` for now; future enhancement is `(:ReuseEinsatz)-[:FUNKTIONSWECHSEL_FROM]->(:Funktion)` + `[:FUNKTIONSWECHSEL_TO]`.
   - `bauteil_label`, `material_label` → keep as properties on `:ReuseEinsatz` in parallel with the canonical `[:HAS_BAUTEILTYP]` / `[:USES_MATERIAL]` edges (preserves the fine-grained label per the §4 granularity principle).

7. **Datenpunkt becomes a typed measurement.**
   - `wert_raw` (string, as-is, e.g. `"250 / 312 / 400"`)
   - `wert_values` (list of floats, parsed from German number format)
   - `einheit_raw` (string), `einheit_normalized` (controlled — see vocab `:Einheit`)
   - `vertrauensgrad` → edge `[:HAS_DATENQUALITAET]->(:Datenqualitaet)` plus property
   - `bilanzgrenze`, `methode_text` as properties
   - Multiple `quelle_label` entries → multiple `[:CITES]` edges
   - Add `:CONTRADICTS` self-relationship between datenpunkt nodes with the same `kennwertdefinition` but different values, when explicitly flagged.

8. **Split the `:Tragwerkstyp` axis mixing.** Per [SCHEMA.md §3.3 / DATABASE_REVIEW §7.8](_database/_system/SCHEMA.md): `Holztragwerk`, `Stahltragwerk`, `Betontragwerk` stay as `:Tragwerkstyp:Vokabular`. `wiederverwendetes_Tragwerk` and `demontierbares_Tragwerk` move to a property `reuse_property` on the `:ReuseEinsatz` (since they're really reuse-strategy flags). Documented as a one-time migration mapping in the spec.

9. **Fix taxonomy typos in the schema doc.** `Moebelsepearat` → `Moebel_separat`; `ort/Scwheiz` → `ort/Schweiz`. Recorded in a "renamings" appendix so the export script can apply them.

10. **Add a new `:Quelle` model that actually works.** Properties: `id`, `case_id` (since `[S1]` is case-local), `citation_short` (`S1`), `citation_full` (free text from `Gebäude/<case>.md` source register), `quelle_typ` (Publikation, Pre_Demolition_Audit, Materialpass, …), `url`, `seite`. Linked via `[:CITES]` from `:ReuseEinsatz`, `:Datenpunkt`, `:Fallstudie`, `:AkteurBeteiligung`. This becomes a separate Label group "Evidence layer".

11. **Add `:Einheit` controlled vocab** (`m2`, `t`, `kg`, `kgCO2e`, `tCO2e`, `m3`, `Stueck`, `EUR`, …) so `einheit` becomes queryable.

---

## Node Labels — to be enumerated in the spec

Grouped into 4 families. Counts are indicative based on §9 of the review.

### Family A — Core instance nodes (~10 Labels, ~2.0k nodes)

- `:Fallstudie`, `:Projekt`, `:Bauobjekt`, `:Akteur`, `:ReuseEinsatz`, `:ReuseKette`, `:ReuseKettenstation`, `:Datenpunkt`, `:Quelle`, `:SoftwareDigitaltool`

For each Label, the spec will list:
- `id` (unique key)
- `title`
- Properties (e.g. for `:ReuseEinsatz`: `bauteil_label`, `material_label`, `menge_umfang_raw`, `menge_umfang_value`, `menge_umfang_unit`, `alte_funktion`, `neue_funktion`, `herkunft_label`, `pruefung_label`, `norm_recht_label`, `huerde_label`, `body_md`, `legacy_paths`)
- Source: which folder + frontmatter fields it draws from.

### Family B — Reified relation nodes (~3 Labels)

- `:AkteurBeteiligung` (actor × case × role × optional phase)
- `:BauobjektBeteiligung` (building × reuse_kette × role)
- (Possibly future) `:Funktionswechsel` once mining `alte_funktion`/`neue_funktion` is done — flagged as v2.

### Family C — Controlled vocabulary nodes (~40 Labels, all `:<Label>:Vokabular`)

Bauteil/Material/Tragwerk:
- `:Bauteiltyp`, `:Material`, `:Bauteilebene`, `:Bauteilzustand`, `:Funktionswechsel`, `:Tragwerkstyp`, `:Tragwerksprinzip`, `:Bauweise`, `:Bausystem`, `:FuegungVerbindung`

Reuse semantics:
- `:ReuseStrategie`, `:ReuseEinsatzstatus`, `:BewertungslogikAbgrenzung`, `:Ressourcenquelle`, `:Beschaffungsweg`

Process & methods:
- `:Prozessphase`, `:Rueckbauverfahren`, `:Aufbereitungsverfahren`, `:Logistik`, `:Methode`

Requirements & barriers:
- `:Huerde`, `:PruefungNachweis`, `:Leistungsanforderung`, `:Norm`, `:RechtlicheBedingung`, `:Schadstoff`

Bauobjekt context:
- `:Bauobjektklasse`, `:Bauobjektrolle`, `:Bauobjektstatus`, `:Nutzung`, `:BauaufgabeIntervention`, `:Kontextmerkmal`

Geography:
- `:Ort` (with self-loop `[:PART_OF]` for hierarchy — Stadt → Land)

Data & evaluation:
- `:Kennwertdefinition`, `:Datenqualitaet`, `:ZertifizierungBewertungssystem`, `:Datenmodell`, `:Dokumenttyp`, `:Tooltyp`, `:Einheit` (new)

Actors & roles:
- `:Akteurrolle`

Programs / context:
- `:Wirtschaft`, `:Foerderprogramm`, `:ProgrammKontext`

### Family D — Auxiliary / housekeeping

- `:BuildBatch` (one node per migration batch, with `[:CREATED_BY_BATCH]` from every node — preserves the `build_status: promoted_phase42` traceability without polluting every node).
- `:LegacyPath` (one node per legacy file path; `[:LEGACY_PATH]` from the canonical node) — optional; can be a property if not needed for queries.

---

## Relationship Types — to be enumerated in the spec

Grouped into 8 families. Direction, endpoint labels, cardinality, and properties listed for each.

### G1 — Containment & structural
`BELONGS_TO_FALLSTUDIE`, `BELONGS_TO_PROJEKT`, `HAS_PROJEKT`, `HAS_BAUOBJEKT`, `REALIZES_BAUOBJEKT`, `PART_OF_REUSE_KETTE`, `PART_OF` (Ort→Ort)

### G2 — ReuseEinsatz → canonical taxonomies (the ~30 `HAS_*` relations)
All 24 populated + the ~30 gap relations enumerated in [SCHEMA.md §9](_database/_system/SCHEMA.md). The spec will tag each as `populated` / `gap` so we know where the data is currently dense vs sparse.

### G3 — Reuse provenance / building-to-building
`INSTALLED_IN_BAUOBJEKT`, `SOURCED_FROM_BAUOBJEKT`, `DONATES_TO` (Bauobjekt→Bauobjekt, derived).

### G4 — Actor participation
`INVOLVES_AKTEUR`, `RELATES_TO_BAUOBJEKT` (from AkteurBeteiligung), `HAS_AKTEURROLLE`, optional shortcut `PARTICIPATED_IN` (Akteur→Projekt).

### G5 — Measurement
`MEASURED_ON_BAUOBJEKT`, `MEASURES_KENNWERTDEFINITION`, `HAS_DATENQUALITAET`, `HAS_EINHEIT`, `CONTRADICTS` (Datenpunkt→Datenpunkt).

### G6 — Geography
`LOCATED_IN_ORT` (Bauobjekt → Ort), `PART_OF` (Ort → Ort).

### G7 — Evidence / citation
`CITES` (ReuseEinsatz | Datenpunkt | Fallstudie | AkteurBeteiligung → Quelle), with edge properties `raw_label` (`"[S1]"`), `seite`, `excerpt`.

### G8 — Programme / context
`INVOLVES_FOERDERPROGRAMM`, `HAS_PROGRAMM_KONTEXT`, `USES_SOFTWARE_DIGITALTOOL`.

For each relationship the spec will state:
- Allowed source label(s) and target label
- Cardinality (1:1 / N:1 / N:M)
- Edge properties (currently mostly empty, but `field`, `raw_label`, `confidence`, `resolution_rule` from [clean_confirmed_edges.csv](_database/_edges/clean_confirmed_edges.csv) carry over)
- Current populated count vs gap (per review §3)

---

## Constraints & indexes (last section of the spec)

- `CREATE CONSTRAINT FOR (n:<Label>) REQUIRE n.id IS UNIQUE` for every Label.
- `CREATE INDEX FOR (n:ReuseEinsatz) ON (n.bauteil_label)` and similar text-search indexes on heavy nodes.
- Full-text index `body_text` covering `:Fallstudie`, `:Bauobjekt`, `:Akteur`, `:ReuseEinsatz`, `:Huerde`, `:Material`, `:Bauteiltyp` for German prose search.
- Composite uniqueness for `:Datenpunkt` is provided by `id` (already `<case>__<NNN>__<metric>`).

---

## Verification / coverage checklist (also in the spec)

A table that maps each source artefact to where it ends up:

- Every folder under `_database/<entity>/` → maps to one Label (or to a property if collapsed).
- Every relation in `_database/_edges/clean_confirmed_edges.csv` → maps to one `:HAS_*` or `:USES_*` relationship type.
- Every YAML frontmatter field on `:ReuseEinsatz` / `:Datenpunkt` / `:Fallstudie` → maps to a property or an edge.
- Every gap relation in [SCHEMA.md §9](_database/_system/SCHEMA.md) → listed in the relationship catalogue as `gap`, so they exist in the graph schema even before they have data.

This ensures we don't lose information on the way to Neo4j.

---

## Out of scope (this plan)

- Writing the export script (Python loader vs neo4j-admin import — to be decided once schema is signed off).
- Running a Neo4j instance (Docker / Aura / Desktop — to be decided).
- Filling the ~30 gap relations from prose — that is a separate data-mining task, not a schema task.
- Translating German labels to English — schema stays German.