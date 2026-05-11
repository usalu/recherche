---
name: Neo4j schema catalogue
overview: Design a clean, native Neo4j property-graph schema with a *minimal generic edge vocabulary* (IST, HAT, BENUTZT, GEHÖRT_ZU) and explicit hybrid-modeling rules so the same fact can live as a property, as a node, or as an edge depending on richness. Captures every piece of information currently in `_database/` + `clean_confirmed_edges.csv` + YAML frontmatter. First deliverable is the schema spec as Markdown; export tooling and Neo4j runtime are deferred.
todos:
  - id: spec-skeleton
    content: "Create _database/_system/NEO4J_SCHEMA.md with the new section skeleton: 1 Modeling philosophy, 2 Generic edge predicates, 3 Hybrid modeling rules, 4 Node Labels + properties, 5 Edge mapping table (legacy relation → generic edge + props), 6 Constraints/indexes, 7 Coverage checklist, 8 Renamings appendix."
    status: pending
  - id: philosophy-section
    content: "Write §1 'Modeling philosophy': three coexisting modes (Property-only / Edge-only / Reified-node), the principle 'narrow predicate vocabulary, expressive target labels + edge properties', when to use which mode."
    status: pending
  - id: predicates-section
    content: "Write §2 'Generic edge predicates'. Define the 4 core predicates (IST, HAT, BENUTZT, GEHÖRT_ZU) with allowed source/target labels, edge-property schema, and inverse-direction conventions."
    status: pending
  - id: hybrid-rules-section
    content: "Write §3 'Hybrid modeling rules'. For every YAML frontmatter field on ReuseEinsatz / Datenpunkt / Fallstudie / Bauobjekt / AkteurBeteiligung, state which of the three modes is used, with rationale."
    status: pending
  - id: labels-section
    content: "Write §4 'Node Labels'. Enumerate Labels across 4 families (Instance / Reified-relation / Vokabular / Auxiliary). For each Label list: id, title, properties (with origin), uniqueness constraint."
    status: pending
  - id: edge-mapping-section
    content: "Write §5 'Edge mapping table'. Map every legacy relation (24 populated + ~30 gap) from clean_confirmed_edges.csv to one of the 4 generic predicates with the required edge property values (art, rolle, anzahl, einheit, ...)."
    status: pending
  - id: constraints-section
    content: "Write §6 'Constraints & indexes'. UNIQUE constraint per Label.id, range indexes on heavy filterable properties, full-text index over German body_md."
    status: pending
  - id: coverage-section
    content: "Write §7 'Coverage checklist'. Verification table proving no source artefact is lost: every folder under _database/<entity>/, every relation in clean_confirmed_edges.csv, every YAML field has a destination."
    status: pending
  - id: renamings-appendix
    content: "Write §8 'Renamings & taxonomy fixes': Moebelsepearat→Moebel_separat, ort/Scwheiz→ort/Schweiz, tragwerkstyp axis split (wiederverwendetes/demontierbares lifted to ReuseEinsatz property), bauteiltyp/material drop-and-remap table from SCHEMA.md §5/§6."
    status: pending
---

## Goal

Produce one authoritative Markdown spec at `_database/_system/NEO4J_SCHEMA.md` that defines a native Neo4j property-graph schema using **only 4 generic edge types** (extensible if absolutely needed) and **three coexisting modeling modes** so each fact lands in its most natural shape — sometimes a property, sometimes only an edge to a node, sometimes a fully reified node with its own edges.

No code, no Neo4j instance — just the schema spec.

---

## §1 Modeling philosophy — three coexisting modes

The spec will codify these three modes as legitimate choices, **not** mistakes:

- **Mode A — Property on the node.** Used when the value is intrinsic, unshared, and has no internal structure. Example: `:ReuseEinsatz.bauteil_label = "Stahlträger / Stützen"`, `:Datenpunkt.wert_raw = "250 / 312 / 400"`.

- **Mode B — Edge to a vocab node (no edge properties).** Used when the value is a shared taxonomy term carrying its own knowledge body (German prose in `_database/<vocab>/<id>/index.md`). Example: `(:ReuseEinsatz)-[:HAT]->(:Huerde {id: 'Toleranzen'})`. Multiple `:ReuseEinsatz` nodes share the same `:Huerde` node.

- **Mode C — Reified node with edges and properties.** Used when the relation itself has structure (quantity, role, time, multiple participants). Example: `(:ReuseEinsatz)-[:BENUTZT]->(:Materialeinsatz {anzahl: 98, einheit: "t", anteil_prozent: 95})-[:IST]->(:Material {id: "Stahl"})`. Or the existing `:AkteurBeteiligung` for actor × case × role.

**Decision rule (will be in §1):**

```
Is the value a shared taxonomy term?       → at least Mode B
Does the relation carry quantity/role/time? → consider Mode C
Otherwise                                   → Mode A
Always allow Mode A in parallel ("shadow property")
  for fast property-equality filtering even when Mode B exists.
```

---

## §2 Generic edge predicates — 4 core (extensible)

Per your direction, only four base predicates. Direction is `(subject)-[:PREDICATE]->(object)`. Edge properties carry the role/quantity/quality.

### 2.1 `IST` — classification, identity, status, role

Says "this thing IS (an instance of / classified as / currently in the state of) the target".

| Property | Type | Meaning |
|---|---|---|
| `seit` | date? | optional start of validity |
| `bis` | date? | optional end of validity |
| `gewichtung` | float? | 0..1 confidence if the classification is uncertain |
| `quelle_id` | string? | source identifier |

Typical use:
- `(:ReuseEinsatz)-[:IST]->(:Bauteiltyp {id: "Stuetze"})` — IS-A a column
- `(:ReuseEinsatz)-[:IST]->(:ReuseEinsatzstatus {id: "realisiert"})` — IS in state realised
- `(:ReuseEinsatz)-[:IST]->(:ReuseStrategie {id: "Direkte_Wiederverwendung"})` — IS classified as direct reuse
- `(:Bauobjekt)-[:IST]->(:Bauobjektklasse {id: "Wohngebaeude"})`
- `(:AkteurBeteiligung)-[:IST]->(:Akteurrolle {id: "Architektur"})`
- `(:Datenpunkt)-[:IST]->(:Datenqualitaet {id: "belegt"})`

### 2.2 `HAT` — possession, manifestation of a qualitative attribute

Says "this thing HAS / exhibits the target as one of its features". Target is typically a vocab term with its own knowledge body.

| Property | Type | Meaning |
|---|---|---|
| `art` | string? | optional discriminator if the same predicate name covers several axes (e.g., `"huerde"`, `"prozessphase"`, `"pruefung"`, `"norm"`, `"schadstoff"`) |
| `anzahl` | int? | how many times / multiplicity |
| `intensitaet` | string? | qualitative strength (`"gering"`, `"mittel"`, `"hoch"`) |
| `quelle_id` | string? | source |

Typical use:
- `(:ReuseEinsatz)-[:HAT {art: "huerde"}]->(:Huerde {id: "Toleranzen"})`
- `(:ReuseEinsatz)-[:HAT {art: "prozessphase"}]->(:Prozessphase {id: "Rueckbau"})`
- `(:ReuseEinsatz)-[:HAT {art: "pruefung"}]->(:PruefungNachweis {id: "Sichtpruefung"})`
- `(:ReuseEinsatz)-[:HAT {art: "norm"}]->(:Norm {id: "ISO_20887"})`
- `(:ReuseEinsatz)-[:HAT {art: "schadstoff"}]->(:Schadstoff {id: "Asbest"})`
- `(:Bauobjekt)-[:HAT {art: "nutzung"}]->(:Nutzung {id: "Wohnen"})`

### 2.3 `BENUTZT` — instrumental usage

Says "this thing USES the target as a material, tool, method, or process to achieve its purpose". The defining predicate for quantitative material/process facts.

| Property | Type | Meaning |
|---|---|---|
| `anzahl` | float? | quantity used |
| `einheit` | string? | unit (`"t"`, `"m2"`, `"Stueck"`, …) |
| `anteil_prozent` | float? | share-of-total in percent (e.g., 95 for "95 % des tragenden Stahls") |
| `funktion_alt` | string? | original role of the used thing |
| `funktion_neu` | string? | new role |
| `aufbereitung` | string? | processing applied (free text, e.g. "Sandstrahlen") |
| `quelle_id` | string? | source |

Typical use:
- `(:ReuseEinsatz)-[:BENUTZT {anzahl: 98, einheit: "t", anteil_prozent: 95}]->(:Material {id: "Stahl"})`
- `(:ReuseEinsatz)-[:BENUTZT]->(:Methode {id: "Materialpass"})`
- `(:ReuseEinsatz)-[:BENUTZT]->(:Rueckbauverfahren {id: "Demontage"})`
- `(:ReuseEinsatz)-[:BENUTZT]->(:Aufbereitungsverfahren {id: "Sandstrahlen"})`
- `(:ReuseEinsatz)-[:BENUTZT]->(:SoftwareDigitaltool {id: "Madaster"})`

### 2.4 `GEHÖRT_ZU` — membership, containment, location, provenance

Says "this thing BELONGS TO a larger thing", in the broadest sense (parent case, project, building, chain, geographic location, donor source, citing source).

| Property | Type | Meaning |
|---|---|---|
| `rolle` | string? | the kind of belonging: `"fallstudie"`, `"projekt"`, `"einbauort"`, `"messung_objekt"`, `"misst"`, `"herkunft"`, `"kette"`, `"ort"`, `"beleg"`, `"foerderprogramm"`, `"kontext"`, `"akteur"`, `"kennwert"` |
| `position` | int? | ordering when part of a sequence (e.g., chain station number) |
| `seit` | date? | optional |
| `bis` | date? | optional |
| `quelle_id` | string? | source |

Typical use:
- `(:ReuseEinsatz)-[:GEHÖRT_ZU {rolle: "fallstudie"}]->(:Fallstudie {id: "K118_..."})`
- `(:ReuseEinsatz)-[:GEHÖRT_ZU {rolle: "projekt"}]->(:Projekt {id: "K118_..."})`
- `(:ReuseEinsatz)-[:GEHÖRT_ZU {rolle: "einbauort"}]->(:Bauobjekt {id: "K118_..."})` ← installed_in_bauobjekt
- `(:ReuseEinsatz)-[:GEHÖRT_ZU {rolle: "herkunft"}]->(:Bauobjekt {id: "ELYS_Basel"})` ← sourced_from (donor)
- `(:Datenpunkt)-[:GEHÖRT_ZU {rolle: "messung_objekt"}]->(:Bauobjekt)` ← measured_on
- `(:Datenpunkt)-[:GEHÖRT_ZU {rolle: "misst"}]->(:Kennwertdefinition)` ← measures_kennwertdefinition
- `(:ReuseEinsatz)-[:GEHÖRT_ZU {rolle: "beleg"}]->(:Quelle {id: "..."})` ← documented_in_quelle / citation (no separate BELEGT_DURCH predicate, per your instruction)
- `(:Bauobjekt)-[:GEHÖRT_ZU {rolle: "ort"}]->(:Ort {id: "Berlin"})` ← located_in_ort
- `(:Ort {id: "Berlin"})-[:GEHÖRT_ZU {rolle: "ort"}]->(:Ort {id: "Deutschland"})` ← Stadt-Land hierarchy
- `(:ReuseKettenstation)-[:GEHÖRT_ZU {rolle: "kette", position: 3}]->(:ReuseKette)`
- `(:AkteurBeteiligung)-[:GEHÖRT_ZU {rolle: "akteur"}]->(:Akteur)`
- `(:AkteurBeteiligung)-[:GEHÖRT_ZU {rolle: "fallstudie"}]->(:Fallstudie)`

### 2.5 Extension policy

Add a new predicate **only when** the relation:
1. cannot be naturally read as IST / HAT / BENUTZT / GEHÖRT_ZU even with a `rolle` / `art` property, and
2. is queried frequently enough that the discriminator-property pattern hurts.

The spec will explicitly flag any extension and provide rationale. Initial candidates flagged as "not added in v1" per your decision: `BELEGT_DURCH` (folded into `GEHÖRT_ZU {rolle: "beleg"}`), `WIDERSPRICHT` (folded into a property `widerspricht_id` on `:Datenpunkt`).

---

## §3 Hybrid modeling rules — per field

For each frontmatter field on the heavy nodes, state which of Mode A / B / C is used and why.

### 3.1 `:ReuseEinsatz`

| Field | Mode | Reason |
|---|---|---|
| `bauteil_label` (`"Stahlträger / Stützen"`) | A property | Free-text label, kept verbatim for fine granularity (per SCHEMA.md §4) |
| canonical `bauteiltyp` (e.g. `Traeger`) | B edge `IST→:Bauteiltyp` | Shared taxonomy with prose body |
| `material_label` (`"Brettschichtholz"`) | A property | Fine variant |
| canonical `material` (`Holz`) | B edge `BENUTZT→:Material` | Shared taxonomy |
| `menge_umfang` (`"98 t; 95 % des tragenden Stahls"`) | A property `menge_raw` + parsed Mode C onto the `BENUTZT` edge `{anzahl: 98, einheit: "t", anteil_prozent: 95}` | Raw kept, parsed values queryable |
| `alte_funktion` / `neue_funktion` | A properties | No taxonomy of functions exists yet; promote later if needed |
| `herkunft_label` | A property + (when donor exists as a `:Bauobjekt`) Mode C-light edge `GEHÖRT_ZU {rolle:"herkunft"}` | Donor edge if resolvable, free text otherwise |
| `pruefung_label` | A property (raw) + multiple Mode B `HAT {art:"pruefung"}` edges | Both: free-text composite + atomic linkable terms |
| `norm_recht_label` | Same pattern: A + multiple `HAT {art:"norm"}` |
| `huerde_label` | Same: A + multiple `HAT {art:"huerde"}` |
| `quelle_label` (`"[S1], [S6]"`) | A property (raw) + multiple Mode B edges `GEHÖRT_ZU {rolle:"beleg"}` to case-scoped `:Quelle` nodes | Splits and resolves shorthand |
| `reuse_einsatzstatus` | B edge `IST→:ReuseEinsatzstatus` + Mode A shadow property `status` | Edge for vocab linkage, property for fast filter |
| `reuse_strategie` | B edge `IST→:ReuseStrategie` |
| `bewertungslogik_abgrenzung` | B edge `IST→:BewertungslogikAbgrenzung` |
| `prozessphase` (list) | multiple B edges `HAT {art:"prozessphase"}` |
| `tragwerkstyp` (only material-typed values) | B edge `IST→:Tragwerkstyp` |
| `tragwerkstyp` (reuse-typed values like `wiederverwendetes_Tragwerk`) | A property `reuse_property: "wiederverwendetes_Tragwerk"` | Axis fix from review §7.8 |
| `body` (German prose) | A property `body_md` | Full-text index target |
| `legacy_paths`, `build_status` | A properties | Provenance metadata |

### 3.2 `:Datenpunkt`

| Field | Mode | Reason |
|---|---|---|
| `wert` raw (`"1.100"`, `"250 / 312 / 400"`) | A property `wert_raw` | Preserve verbatim |
| parsed numeric values | A property `wert_values: [1100]` or `[250, 312, 400]` | German-number-aware parsing |
| `einheit` raw | A property `einheit_raw` |
| canonical `einheit` | B edge `IST→:Einheit` + A shadow `einheit_norm` |
| `Vertrauensgrad` (`belegt`, `unklar`, …) | B edge `IST→:Datenqualitaet` + A shadow `vertrauensgrad` |
| `Bilanzgrenze`, `Methode/Datenmodell/Software` | A properties (free text) + optional B edge to `:Methode` / `:Datenmodell` / `:SoftwareDigitaltool` when value matches a known vocab term |
| `quelle_label` | same as `:ReuseEinsatz` |
| `kennwertdefinition` link | B edge `GEHÖRT_ZU {rolle:"misst"}->:Kennwertdefinition` |
| `bauobjekt` link | B edge `GEHÖRT_ZU {rolle:"messung_objekt"}->:Bauobjekt` |
| Conflicting values across datenpunkten | A property `widerspricht_id` (id of contradicting `:Datenpunkt`) | No separate edge type per your instruction |

### 3.3 `:Fallstudie` / `:Projekt` / `:Bauobjekt`

These three keep their separate identity even when sharing an id. Edges between them:
- `(:Fallstudie)-[:GEHÖRT_ZU {rolle:"projekt"}]->(:Projekt)` (inverse direction of `has_projekt` — direction normalised so all `GEHÖRT_ZU` point upward to container; alternative: keep as Mode-A property `projekt_id` on `:Fallstudie`. Decision in spec: edge, because navigation queries are bidirectional in Cypher.)
- `(:Projekt)-[:GEHÖRT_ZU {rolle:"bauobjekt"}]->(:Bauobjekt)` (`has_bauobjekt`)
- `(:Bauobjekt)-[:GEHÖRT_ZU {rolle:"ort"}]->(:Ort)` (geography)

Bauobjekt body fields (`nutzung`, `bauobjektklasse`, `bauobjektrolle`, `bauobjektstatus`, `bauaufgabe_intervention`) → B edges `IST→:<Label>`.

### 3.4 `:AkteurBeteiligung` (reified — Mode C)

Always Mode C. Properties: `id`. Edges:
- `GEHÖRT_ZU {rolle:"akteur"} → :Akteur`
- `GEHÖRT_ZU {rolle:"fallstudie"} → :Fallstudie`
- `GEHÖRT_ZU {rolle:"projekt"} → :Projekt`
- `GEHÖRT_ZU {rolle:"bauobjekt"} → :Bauobjekt`
- `IST → :Akteurrolle`

---

## §4 Node Labels — to be enumerated in the spec

### 4.1 Family — Instance nodes (heavy)

`:Fallstudie`, `:Projekt`, `:Bauobjekt`, `:Akteur`, `:ReuseEinsatz`, `:ReuseKette`, `:ReuseKettenstation`, `:Datenpunkt`, `:Quelle`, `:SoftwareDigitaltool`.

For each: id (unique key), title, body_md, plus the Mode-A properties enumerated in §3.

### 4.2 Family — Reified relation nodes

`:AkteurBeteiligung`, `:BauobjektBeteiligung`, `:Materialeinsatz` (new; optional Mode-C extraction of `BENUTZT` edges when the same Material is used in several quantities at the same `:ReuseEinsatz`).

### 4.3 Family — Controlled vocabulary nodes

All carry the **multi-label** `:<Label>:Vokabular` so taxonomy can be enumerated via one query. Roughly 35–40 vocab labels, grouped: Bauteil/Material/Tragwerk, Reuse-Semantik, Prozess, Anforderungen/Barrieren, Bauobjekt-Kontext, Geographie, Daten/Bewertung, Akteur-Rollen, Programme.

Each vocab node has at minimum: `id`, `title`, `body_md`.

### 4.4 Family — Auxiliary

`:BuildBatch` (one per migration batch, edge `(:Node)-[:GEHÖRT_ZU {rolle:"batch"}]->(:BuildBatch)` so `build_status: promoted_phase42` becomes queryable provenance).

---

## §5 Edge mapping table — legacy relation → generic

The spec will contain one table that maps every legacy relation name in [clean_confirmed_edges.csv](_database/_edges/clean_confirmed_edges.csv) and [SCHEMA.md §9](_database/_system/SCHEMA.md) to its new generic-predicate form, so the export can be rule-driven. Sketch (excerpt):

| Legacy relation | Generic | Edge properties | Notes |
|---|---|---|---|
| `belongs_to_fallstudie` | GEHÖRT_ZU | `rolle: "fallstudie"` | |
| `belongs_to_projekt` | GEHÖRT_ZU | `rolle: "projekt"` | |
| `has_bauteiltyp` | IST | — | |
| `installed_in_bauobjekt` | GEHÖRT_ZU | `rolle: "einbauort"` | |
| `measured_on_bauobjekt` | GEHÖRT_ZU | `rolle: "messung_objekt"` | |
| `measures_kennwertdefinition` | GEHÖRT_ZU | `rolle: "misst"` | |
| `uses_material` | BENUTZT | `anzahl`, `einheit`, `anteil_prozent` parsed from `menge_umfang` | |
| `has_huerde` | HAT | `art: "huerde"` | |
| `has_reuse_einsatzstatus` | IST | — | + shadow prop `status` on subject |
| `has_prozessphase` | HAT | `art: "prozessphase"` | |
| `has_akteurrolle` | IST | — | on `:AkteurBeteiligung` |
| `has_reuse_strategie` | IST | — | |
| `relates_to_bauobjekt` | GEHÖRT_ZU | `rolle: "bauobjekt"` | |
| `has_bewertungslogik_abgrenzung` | IST | — | |
| `has_projekt` (fallstudie→projekt) | GEHÖRT_ZU | `rolle: "projekt"` | direction normalised |
| `has_bauobjekt` (fallstudie→bauobjekt) | GEHÖRT_ZU | `rolle: "bauobjekt"` | |
| `has_rueckbauverfahren` | BENUTZT | — | |
| `part_of_reuse_kette` | GEHÖRT_ZU | `rolle: "kette"`, `position` | |
| `has_pruefung_nachweis` | HAT | `art: "pruefung"` | |
| `involves_akteur` | GEHÖRT_ZU | `rolle: "akteur"` | on `:AkteurBeteiligung` |
| `has_tragwerkstyp` | IST | — | only material-typed values; rest become property |
| `has_fuegung_verbindung` | HAT | `art: "fuegung"` | |
| `references_norm` | HAT | `art: "norm"` | |
| `has_leistungsanforderung` | HAT | `art: "leistung"` | |
| `has_aufbereitungsverfahren` *(gap)* | BENUTZT | — | |
| `has_logistik` *(gap)* | HAT | `art: "logistik"` | |
| `has_methode` *(gap)* | BENUTZT | — | |
| `has_funktionswechsel` *(gap)* | HAT | `art: "funktionswechsel"` + property `funktion_alt`/`funktion_neu` | |
| `has_bauteilzustand` *(gap)* | IST | — | |
| `has_bauteilebene` *(gap)* | IST | — | |
| `has_bauweise` *(gap)* | IST | — | |
| `has_bausystem` *(gap)* | IST | — | |
| `has_tragwerksprinzip` *(gap)* | IST | — | |
| `has_bauobjektklasse` *(gap)* | IST | — | |
| `has_bauobjektrolle` *(gap)* | IST | — | |
| `has_bauobjektstatus` *(gap)* | IST | — | |
| `has_nutzung` *(gap)* | HAT | `art: "nutzung"` | |
| `has_bauaufgabe_intervention` *(gap)* | HAT | `art: "intervention"` | |
| `located_in_ort` *(partly populated)* | GEHÖRT_ZU | `rolle: "ort"` | |
| `has_rechtliche_bedingung` *(gap)* | HAT | `art: "recht"` | |
| `has_schadstoff` *(gap)* | HAT | `art: "schadstoff"` | |
| `has_kontextmerkmal` *(gap)* | HAT | `art: "kontext"` | |
| `has_zertifizierung_bewertungssystem` *(gap)* | HAT | `art: "zertifizierung"` | |
| `has_datenmodell` *(gap)* | BENUTZT | — | |
| `has_dokumenttyp` *(gap)* | IST | — | (on `:Quelle`) |
| `has_tooltyp` *(gap)* | IST | — | (on `:SoftwareDigitaltool`) |
| `uses_software_digitaltool` *(gap)* | BENUTZT | — | |
| `documented_in_quelle` *(gap)* | GEHÖRT_ZU | `rolle: "beleg"` | replaces a hypothetical BELEGT_DURCH |
| `has_datenqualitaet` *(gap)* | IST | — | on `:Datenpunkt` |
| `involves_foerderprogramm` *(gap)* | GEHÖRT_ZU | `rolle: "foerderprogramm"` | |
| `has_programm_kontext` *(gap)* | GEHÖRT_ZU | `rolle: "kontext"` | |
| `has_wirtschaft` *(gap)* | HAT | `art: "wirtschaft"` | |
| donor link (currently only `herkunft_label`) | GEHÖRT_ZU | `rolle: "herkunft"` | new edge derived from labels |

This table is the export's rewrite rules.

---

## §6 Constraints & indexes

- `CREATE CONSTRAINT FOR (n:<Label>) REQUIRE n.id IS UNIQUE` for every Label.
- Range index on `:ReuseEinsatz.bauteil_label`, `:ReuseEinsatz.material_label`, `:Datenpunkt.wert_values`, `:Datenpunkt.einheit_norm`, `:Bauobjekt.title`.
- Full-text index `body_de` over `body_md` on `:Fallstudie`, `:Bauobjekt`, `:Akteur`, `:ReuseEinsatz`, `:Huerde`, `:Material`, `:Bauteiltyp` etc.

---

## §7 Coverage checklist

Table proving no information is lost:
- Every folder under `_database/<entity>/` → maps to one Label (Mode B/C) or to a property (Mode A).
- Every relation in `clean_confirmed_edges.csv` → mapped in §5.
- Every YAML frontmatter field on `:Fallstudie` / `:ReuseEinsatz` / `:Datenpunkt` / `:Bauobjekt` / `:AkteurBeteiligung` → mapped in §3.
- Every gap relation in [SCHEMA.md §9](_database/_system/SCHEMA.md) → listed in §5 with the generic predicate that will carry it once data is mined.

---

## §8 Renamings & taxonomy fixes appendix

- `Moebelsepearat` → `Moebel_separat`
- `ort/Scwheiz` → `ort/Schweiz`
- `tragwerkstyp` split: keep `Holztragwerk` / `Stahltragwerk` / `Betontragwerk` as `:Tragwerkstyp` vocab; lift `wiederverwendetes_Tragwerk` / `demontierbares_Tragwerk` to `:ReuseEinsatz.reuse_property`.
- Bauteiltyp drop-and-remap from SCHEMA.md §5 (marked "already applied").
- Material drop-and-merge from SCHEMA.md §6 (marked "already applied").

---

## Out of scope (this plan)

- Writing the export script (CSV via `neo4j-admin import` vs Python loader — to be decided after schema is signed off).
- Running a Neo4j instance.
- Filling the ~30 gap relations from prose — that's data mining, not schema work.
- Translating German labels to English — schema stays German.
