---
name: Neo4j schema catalogue
overview: Cleaned Neo4j schema. One Label :Fallbeispiel per case (art property distinguishes Gebäude/Brücke/Pavillon/etc.). :Bauteilgruppe is the reified reuse-Einsatz. Measurements are properties on whichever node owns them (Fallbeispiel, Bauteilgruppe, or BENUTZT-edge). All source attribution is via :BELEGT_IN edges (claim → :Quelle) — no quelle properties anywhere. Five generic edges (IST, HAT, BENUTZT, GEHÖRT_ZU, BELEGT_IN). Cleanups — drop :Tragwerkstyp / :Bauteilgruppentyp / :Bauobjektklasse / :Einheit / :Kennwertdefinition / :AkteurBeteiligung / :ReuseKettenstation / all measurement Labels; merge :Foerderprogramm+:ProgrammKontext → :Programm; rename :BewertungslogikAbgrenzung → :WiederverwendungsArt; rename :ReuseKette → :Wiederverwendungskette.
todos:
  - id: spec-skeleton
    content: "Create _database/_system/NEO4J_SCHEMA.md with the 4-section structure: §1 Node-type catalogue, §2 Nodes (per-Label property tables), §3 Edge-type catalogue, §4 Edges (per-edge-type property tables). Plus appendices for principles, constraints, coverage, renamings."
    status: pending
  - id: write-1
    content: "Write §1 Node-type catalogue: the 6 instance Labels and the ~30 vocab Labels with one-line purpose each."
    status: pending
  - id: write-2
    content: "Write §2 Nodes: per-Label property table (name | type | required | source field | notes). Property placement rules — building-level on :Fallbeispiel, component-level on :Bauteilgruppe, relational on edges."
    status: pending
  - id: write-3
    content: "Write §3 Edge-type catalogue: 5 generic edges with source/target Label families and the legacy relations folded in."
    status: pending
  - id: write-4
    content: "Write §4 Edges: per-edge-type property table. None of IST/HAT/BENUTZT/GEHÖRT_ZU carry a quelle_id; the only citation edge is :BELEGT_IN with optional `eigenschaft` to scope citation to a specific property of the source node."
    status: pending
  - id: appendices
    content: "Write the appendices: A modeling principles, B constraints & indexes, C coverage checklist, D renamings & dropped/merged vocabs."
    status: pending
---

# Goal

Author `_database/_system/NEO4J_SCHEMA.md` in this exact four-part order:

1. **§1 Node-type catalogue** — the list of all Labels.
2. **§2 Nodes** — for each Label, complete property table.
3. **§3 Edge-type catalogue** — the list of 5 edge types.
4. **§4 Edges** — for each edge type, complete property table.

Plus appendices for principles, constraints, coverage, renamings.

Below is the concrete content draft for those four sections so you can confirm before I write the file.

---

# §1 Node-type catalogue

## §1.A Instance Labels (6)

| Label | Purpose | Replaces |
|---|---|---|
| `:Fallbeispiel` | A single case study — one physical object plus the surrounding research narrative. The `art` property distinguishes Gebäude / Brücke / Pavillon / Halle / Lager / Innenausbau / Anlage. | legacy :Fallstudie + :Projekt + :Bauobjekt (merged into one) |
| `:Bauteilgruppe` | A group of components in a Fallbeispiel — the reified reuse-Einsatz (when reused) or original-construction group (when not). | legacy :ReuseEinsatz |
| `:Akteur` | Office / company / authority / institution / person | unchanged |
| `:Quelle` | Source / citation / document. Replaces unresolved `quelle_label` shorthand by becoming a real node per case. | unchanged (but now reachable via :BELEGT) |
| `:SoftwareDigitaltool` | Concrete platform (Madaster, Concular, …) | unchanged |
| `:Wiederverwendungskette` | OPTIONAL named multi-Bauteilgruppe reuse program. Only used when a documented chain orchestrates several Bauteilgruppen; for single-component chains the stations live as GEHÖRT_ZU edges directly on the Bauteilgruppe. | renamed from :ReuseKette; :ReuseKettenstation dropped |

## §1.B Vocabulary Labels (all multi-labelled `:<Label>:Vokabular`)

Grouped here only for reading; in the spec they're listed alphabetically.

**Bauteil & Material:**
- `:Bauteiltyp` — 15 canonical component families (Stütze, Träger, Decke, Wand, Fassade, Fenster, Tür, Treppe, Dach, Boden, Ausbau, Technik, Fundament, Geländer, Dämmung)
- `:Material` — 15 substances (Beton, Stahlbeton, Recyclingbeton, Stahl, Aluminium, Gusseisen, Holz, Glas, Ziegel, Naturstein, Keramik, Kunststoff, Dämmstoff, Lehm, Stroh)
- `:Bauteilebene`
- `:Bauteilzustand`
- `:Funktionswechsel`
- `:FuegungVerbindung`

**Konstruktion:**
- `:Bauweise`
- `:Bausystem`
- `:Tragwerksprinzip`

**Reuse:**
- `:ReuseStrategie` (Direct Reuse, Same-Site Reuse, Urban Mining, DfD, Bestandserhalt, Recycling, Upcycling, Remanufacturing)
- `:ReuseEinsatzstatus` (realisiert, geplant, verworfen, vorgeschlagen, unklar, temporär, prototypisch)
- `:WiederverwendungsArt` *(renamed from :BewertungslogikAbgrenzung; absorbs the dropped :Bauteilgruppentyp)* — zaehlt_als_Direct_Reuse, zaehlt_nicht, Bestandserhalt_separat, Recycling_separat, Moebel_separat, geplant_aber_nicht_realisiert, unklar, plus wiederverwendet, original, hybrid

**Beschaffung:**
- `:Ressourcenquelle`
- `:Beschaffungsweg`

**Prozess:**
- `:Prozessphase` (Rueckbau, Aufbereitung, Wiedereinbau, Transport, Lagerung, Pruefung, Identifikation, Entwurf, Ausschreibung, Bestandserfassung, Betrieb_und_Rueckbauplanung)
- `:Rueckbauverfahren`
- `:Aufbereitungsverfahren`
- `:Logistik`
- `:Methode`

**Anforderungen & Hürden:**
- `:Huerde` (27 hurdle types)
- `:PruefungNachweis`
- `:Leistungsanforderung`
- `:Norm`
- `:RechtlicheBedingung`
- `:Schadstoff`

**Fallbeispiel-Kontext:** (former :Bauobjektklasse is dropped — its info lives in `Fallbeispiel.art`)
- `:Bauobjektrolle` (donor / receiver / standalone)
- `:Bauobjektstatus` (bestehend / abgerissen / geplant)
- `:Nutzung` (Wohnen / Büro / Produktion / Kultur / …)
- `:BauaufgabeIntervention` (Neubau / Umbau / Sanierung / Aufstockung / Rückbau)
- `:Kontextmerkmal`

**Geographie:**
- `:Ort` (with self-loop GEHÖRT_ZU for Stadt → Land)

**Akteure:**
- `:Akteurrolle` (kept as dictionary; the role is carried on the edge property `rolle`, not as an outgoing edge)

**Daten & Bewertung:**
- `:Datenqualitaet`
- `:Datenmodell`
- `:Dokumenttyp`
- `:Tooltyp`
- `:ZertifizierungBewertungssystem`

**Wirtschaft & Programme:**
- `:Wirtschaft`
- `:Programm` *(merged :Foerderprogramm + :ProgrammKontext, with `programm_typ` property: `foerderung` / `forschungskontext`)*

## §1.C Dropped Labels (none in the final schema)

- `:Bauwerk`, `:Gebaeude`, `:Pavillon`, `:Halle`, `:Lager`, `:Innenausbau`, `:Anlage`, `:Bruecke` — all collapsed into `:Fallbeispiel.art`.
- `:Fallstudie`, `:Projekt`, `:Bauobjekt` — merged into `:Fallbeispiel`.
- `:ReuseEinsatz` → `:Bauteilgruppe`.
- `:Datenpunkt` and ~26 typed measurement Labels (Flaeche, CO2_Einsparung, Masse, …) — replaced by direct properties on the most relevant node.
- `:AkteurBeteiligung` — collapsed to a `HAT {art:'akteur', rolle:...}` edge.
- `:BauwerkBeteiligung` — same pattern.
- `:ReuseKettenstation` — collapsed to GEHÖRT_ZU edges from `:Bauteilgruppe` to `:Fallbeispiel` with `rolle ∈ {herkunft, zwischenlager, verarbeitung, transport, einbauort}` and `position`.
- `:Bauobjektklasse` — collapsed into `:Fallbeispiel.art` (same Halle/Lager-pattern: all values were really kinds of one parent concept).
- `:Tragwerkstyp` — dropped (review §7.8: mixed axis with Material; reuse-typed values moved to :WiederverwendungsArt).
- `:Bauteilgruppentyp` — merged into `:WiederverwendungsArt`.
- `:Einheit` — kept as a property string only.
- `:Kennwertdefinition` — kept as documentation in the spec, not as a Neo4j Label.
- `:BuildBatch` — provenance lives as `build_status` and `legacy_paths` properties on each node.

---

# §2 Nodes — properties per Label

Property table columns: **name** | **type** | **req** | **source field / origin** | **notes**.

## §2.A `:Fallbeispiel`

The central case-study node. One per case; replaces the legacy fallstudie + projekt + bauobjekt triple sharing the same id.

| name | type | req | source | notes |
|---|---|---|---|---|
| `id` | string | ✓ | folder slug | UNIQUE |
| `title` | string | ✓ | YAML `title` | |
| `art` | string | ✓ | derived from legacy `bauobjektklasse` | one of `"Gebaeude"`, `"Bruecke"`, `"Pavillon"`, `"Halle"`, `"Lager"`, `"Innenausbau"`, `"Anlage"` |
| `body_md` | string | ✓ | merged from legacy fallstudie + projekt + bauobjekt body | concatenated under `## Fallstudie` / `## Projekt` / `## Bauobjekt` subheaders |
| `legacy_paths` | list&lt;string&gt; | – | provenance | |
| `build_status` | string? | – | YAML | |

**Building-level measurement properties** (each scalar; conflicting values stored in `*_alt` list and `*_quelle` parallel property):

| name | type | source kennwert |
|---|---|---|
| `flaeche_m2` | float? | Fläche |
| `projektflaeche_m2` | float? | Projektflaeche |
| `gebaeudemasse_t` | float? | Gebaeudemasse erhalten |
| `wohneinheiten` | int? | Wohneinheiten |
| `fertigstellung_jahr` | int? | Fertigstellung |
| `entwurfsbeginn_jahr` | int? | Entwurfsbeginn |
| `bauzeit_monate` | int? | Bauzeit |
| `lebensdauer_jahre` | int? | Lebensdauer |
| `restlebensdauer_jahre` | float? | Restlebensdauer |
| `kosten_eur` | float? | Kosten |
| `budget_eur` | float? | Budget |
| `co2_footprint_kg` | float? | CO₂-Footprint |
| `energieverbrauch_kwh_a` | float? | Energieverbrauch |
| `wassereinsparung_m3` | float? | Wassereinsparung |
| `bestandslager_m3` | float? | Bestandslager |

For each measurement property, the export creates parallel:
- `<name>_alt: list<float>?` — alternate values from conflicting sources
- `<name>_einheit: string?` — only if the unit isn't already in the name
- `<name>_vertrauensgrad: string?` — `belegt` / `teilweise_belegt` / `unklar` / `umstritten`
- `<name>_bilanzgrenze: string?` — boundary qualifier

**No source attribution as properties.** Every citation is a `:BELEGT_IN` edge to a `:Quelle` node, optionally scoped to a specific property via the edge property `eigenschaft` (see §4.E).

## §2.B `:Bauteilgruppe`

The reified reuse-Einsatz. One per group of related components in a Fallbeispiel.

| name | type | req | source | notes |
|---|---|---|---|---|
| `id` | string | ✓ | legacy reuse_einsatz id | UNIQUE |
| `title` | string | ✓ | YAML | |
| `bauteil_label` | string | ✓ | YAML | raw fine label (`"Stahlträger / Stützen"`) |
| `material_label` | string | ✓ | YAML | raw fine label (`"Brettschichtholz"`) — canonical material is the `BENUTZT→:Material` edge |
| `alte_funktion` | string? | – | YAML | |
| `neue_funktion` | string? | – | YAML | |
| `herkunft_label` | string? | – | YAML | raw donor description; resolved donor is the `GEHÖRT_ZU {rolle:'herkunft'}→:Fallbeispiel` edge |
| `pruefung_label_raw` | string? | – | YAML | |
| `norm_recht_label_raw` | string? | – | YAML | |
| `huerde_label_raw` | string? | – | YAML | |
| `body_md` | string | ✓ | German prose | |
| `legacy_paths` | list&lt;string&gt; | – | | |
| `build_status` | string? | – | YAML | |
| `menge_umfang_raw` | string? | – | YAML | verbatim, e.g. `"98 t; 95 % des tragenden Stahls"` |

**Component-group measurement properties** (parallel `*_alt`/`*_quelle`/`*_vertrauensgrad` as for Fallbeispiel):

| name | type | source kennwert |
|---|---|---|
| `masse_t` | float? | Masse |
| `anzahl_stueck` | int? | Stückzahl |
| `volumen_m3` | float? | Volumen |
| `flaeche_m2` | float? | Komponentenfläche |
| `anteil_prozent` | float? | Reuse_Anteil / Anteil an Baukosten |
| `co2_einsparung_kg` | float? | CO₂-Einsparung |
| `co2_reduktion_kg` | float? | CO₂-Reduktion Materialien |
| `geerntete_materialien_t` | float? | Geerntete Materialien |
| `sekundaere_materialien_t` | float? | Sekundäre Materialien |
| `abfall_vermieden_t` | float? | Abfall vermieden |
| `zielwert_reuse_prozent` | float? | Zielwert Reuse |

Note: when the measurement is **inherently relational** (e.g. "98 t of steel reused" — a property of the BENUTZT relation between this Bauteilgruppe and `:Material/Stahl`), it lives on the `BENUTZT` edge (`anzahl`, `einheit`, `anteil_prozent` — see §4.C), NOT on the Bauteilgruppe node.

**Source attribution.** The legacy `quelle_label_raw` ("S4, S2") is not kept as a property. Each shorthand resolves to a `:Quelle` node (case-scoped, e.g. `K118_Kopfbau__S4`); a `:BELEGT_IN` edge connects this Bauteilgruppe to that `:Quelle`. Multiple sources → multiple edges. Edge property `eigenschaft` optionally scopes which Bauteilgruppe property the source supports.

## §2.C `:Akteur`

| name | type | req | source | notes |
|---|---|---|---|---|
| `id` | string | ✓ | folder slug | UNIQUE |
| `title` | string | ✓ | YAML | |
| `body_md` | string | ✓ | | |
| `legacy_paths` | list&lt;string&gt; | – | | |

## §2.D `:Quelle`

These are descriptive properties of the source itself, not citations *to* another source — so they stay as properties on the `:Quelle` node.

| name | type | req | source | notes |
|---|---|---|---|---|
| `id` | string | ✓ | folder slug, or case-scoped derived (e.g. `K118_Kopfbau__S4`) | UNIQUE |
| `title` | string | ✓ | YAML | |
| `body_md` | string | ✓ | | |
| `case_id` | string? | – | case the shorthand was scoped to | |
| `citation_short` | string? | – | `"S4"` — the within-case shorthand | |
| `citation_full` | string? | – | full reference text (Autor, Jahr, Titel, Verlag, …) | |
| `url` | string? | – | | |
| `seite_default` | string? | – | default page if the BELEGT_IN edge has none | |
| `quelle_typ` | string? | – | optional, prefer `IST→:Dokumenttyp` edge | redundant; can be omitted |

## §2.E `:SoftwareDigitaltool`

| name | type | req | source | notes |
|---|---|---|---|---|
| `id` | string | ✓ | folder slug | UNIQUE |
| `title` | string | ✓ | YAML | |
| `body_md` | string | ✓ | | |
| `url` | string? | – | | |

## §2.F `:Wiederverwendungskette` (optional)

| name | type | req | source | notes |
|---|---|---|---|---|
| `id` | string | ✓ | folder slug | UNIQUE |
| `title` | string | ✓ | YAML | |
| `body_md` | string | ✓ | | |
| `start_jahr` | int? | – | | |
| `end_jahr` | int? | – | | |

## §2.G Vocabulary Labels (shared property shape)

All vocab Labels — every entry in §1.B — carry the second Label `:Vokabular` and share:

| name | type | req | source | notes |
|---|---|---|---|---|
| `id` | string | ✓ | folder slug under `_database/<vocab>/<id>/` | UNIQUE |
| `title` | string | ✓ | YAML | |
| `body_md` | string | ✓ | German prose | |
| `legacy_paths` | list&lt;string&gt; | – | | |

Special additions:

- `:Ort`: optional `iso_country` (string), `koordinaten` (string).
- `:Programm`: required `programm_typ` (string, `"foerderung"` or `"forschungskontext"`).
- `:WiederverwendungsArt`: required `axis` (string, `"einordnung"` for legacy BewertungslogikAbgrenzung values, `"grundtyp"` for wiederverwendet/original/hybrid).

---

# §3 Edge-type catalogue

| Edge | Subject Labels | Object Labels | Card. | Purpose |
|---|---|---|---|---|
| `IST` | `:Fallbeispiel`, `:Bauteilgruppe`, `:Akteur`, `:Quelle`, `:SoftwareDigitaltool`, `:Wiederverwendungskette` | vocab | N:1 per axis | classification / identity / status |
| `HAT` | `:Fallbeispiel`, `:Bauteilgruppe` | vocab (rich body) **or** `:Akteur` (with `art:'akteur', rolle:...`) | N:M | qualitative attribute / actor participation |
| `BENUTZT` | `:Bauteilgruppe`, `:Fallbeispiel` | `:Material`, `:Methode`, `:Rueckbauverfahren`, `:Aufbereitungsverfahren`, `:SoftwareDigitaltool`, `:Datenmodell` | N:M | instrumental usage; quantitative carrier (anzahl, einheit, anteil_prozent) for material |
| `GEHÖRT_ZU` | any | `:Fallbeispiel`, `:Wiederverwendungskette`, `:Ort`, `:Programm` | N:1 / N:M | membership / containment / location / station-in-chain / origin |
| `BELEGT_IN` | any node carrying a citable claim (`:Fallbeispiel`, `:Bauteilgruppe`, `:Akteur`, `:Wiederverwendungskette`) | `:Quelle` | N:M | citation / evidence — the only place where source attribution lives |

## Legacy relations folded in

- **IST:** `has_bauteiltyp`, `has_reuse_einsatzstatus`, `has_reuse_strategie`, `has_bewertungslogik_abgrenzung` (→ now `:WiederverwendungsArt`), `has_akteurrolle` (dropped — role is edge property), `has_datenqualitaet`, `has_bauteilebene`, `has_bauteilzustand`, `has_funktionswechsel`, `has_bauweise`, `has_bausystem`, `has_tragwerksprinzip`, `has_bauobjektrolle`, `has_bauobjektstatus`, `has_dokumenttyp`, `has_tooltyp`, `has_datenmodell`, `has_zertifizierung_bewertungssystem`.
- **HAT:** `has_huerde`, `has_prozessphase`, `has_pruefung_nachweis`, `references_norm`, `has_leistungsanforderung`, `has_schadstoff`, `has_kontextmerkmal`, `has_rechtliche_bedingung`, `has_nutzung`, `has_bauaufgabe_intervention`, `has_fuegung_verbindung`, `has_logistik`, `has_wirtschaft`, plus actor participation `has_akteurrolle` collapsed onto `HAT {art:'akteur', rolle:...}`.
- **BENUTZT:** `uses_material`, `uses_software_digitaltool`, `has_methode`, `has_rueckbauverfahren`, `has_aufbereitungsverfahren`.
- **GEHÖRT_ZU:** `installed_in_bauobjekt` → `rolle:'einbauort'`; new `sourced_from_bauobjekt` → `rolle:'herkunft'`; `part_of_reuse_kette` → `rolle:'kette'` (now to `:Wiederverwendungskette`); `located_in_ort` → `rolle:'ort'`; `relates_to_bauobjekt` → `rolle:'fallbeispiel'`; `involves_akteur` (dropped; folded into HAT); `involves_foerderprogramm` → `rolle:'programm'` to `:Programm`; `has_programm_kontext` → `rolle:'programm'` to `:Programm`; `measured_on_bauobjekt`, `measures_kennwertdefinition` → both dropped (measurements are properties now).
- **BELEGT_IN:** replaces unresolved `quelle_label` shorthand on every node and every `quelle_id` previously stored as edge property. Replaces the planned `documented_in_quelle` gap relation. Direction is **(claim) → (:Quelle)**.

---

# §4 Edges — properties per edge type

**Note:** None of the four edges below carry a `quelle_id` or `quelle_label`. Source attribution lives exclusively on `:BELEGT_IN` edges from the source node (§4.E). When a claim made by an edge needs citation, the citation hangs off the edge's source node, optionally scoped via the `eigenschaft` property on `:BELEGT_IN`.

## §4.A `:IST`

| name | type | req | notes |
|---|---|---|---|
| `seit` | date? | – | start of validity |
| `bis` | date? | – | end of validity |
| `gewichtung` | float? | – | 0..1 confidence |

## §4.B `:HAT`

| name | type | req | notes |
|---|---|---|---|
| `art` | string | ✓ | one of `"huerde"`, `"prozessphase"`, `"pruefung"`, `"norm"`, `"leistung"`, `"schadstoff"`, `"kontext"`, `"recht"`, `"nutzung"`, `"intervention"`, `"fuegung"`, `"logistik"`, `"wirtschaft"`, `"zertifizierung"`, `"akteur"` |
| `rolle` | string? | – | required when `art='akteur'` — e.g. `"Architektur"`, `"Tragwerksplanung"`, `"Bauherr_Auftraggeber"`. Validated against `:Akteurrolle.id` |
| `anzahl` | int? | – | multiplicity |
| `intensitaet` | string? | – | qualitative strength |
| `seit` | date? | – | |
| `bis` | date? | – | |

## §4.C `:BENUTZT`

| name | type | req | notes |
|---|---|---|---|
| `anzahl` | float? | – | quantity used |
| `einheit` | string? | – | unit (`"t"`, `"m2"`, `"Stueck"`, …) |
| `anteil_prozent` | float? | – | share-of-total |
| `funktion_alt` | string? | – | original role of the consumed thing |
| `funktion_neu` | string? | – | new role |
| `aufbereitung` | string? | – | processing applied (free text) |

## §4.D `:GEHÖRT_ZU`

| name | type | req | notes |
|---|---|---|---|
| `rolle` | string | ✓ | one of `"fallbeispiel"`, `"einbauort"`, `"herkunft"`, `"zwischenlager"`, `"verarbeitung"`, `"transport"`, `"kette"`, `"ort"`, `"programm"` |
| `position` | int? | – | ordering in a sequence (e.g., station number in a chain) |
| `seit` | date? | – | |
| `bis` | date? | – | |

## §4.E `:BELEGT_IN`

The only place source attribution lives. Direction: **(claim) → (:Quelle)**.

| name | type | req | notes |
|---|---|---|---|
| `eigenschaft` | string? | – | scopes the citation to a specific property/aspect of the source node, e.g. `"flaeche_m2"`, `"co2_einsparung_kg"`, `"strategie"`, `"huerden"`. If omitted, the citation is at node level — "this whole Fallbeispiel/Bauteilgruppe is documented in this source". |
| `seite` | string? | – | page number |
| `excerpt` | string? | – | quoted excerpt |
| `raw_label` | string? | – | original shorthand, e.g. `"S4"`, `"[S1]"` |

---

# Appendix A — Modeling principles

- Three modes coexist:
  - **Mode A** — node property (intrinsic scalar/list value).
  - **Mode B** — edge to a vocab node (taxonomy term with body).
  - **Mode C** — reified node (the relation has internal structure — used only for `:Bauteilgruppe`).
- **Measurement placement rule:** a measurement belongs to whichever node naturally owns it. Building-level → `:Fallbeispiel`. Component-group-level → `:Bauteilgruppe`. Inherently relational quantities (material reused in t) → on the `BENUTZT` edge.
- **Role placement rule:** a role IS a property of an attachment edge, not its own node. `:HAT {art:'akteur', rolle:'Architektur'}->(:Akteur)`. Vocab `:Akteurrolle` is kept as dictionary, not as an edge target.
- **Citation placement rule:** source attribution NEVER lives as a property. Every citation is a `:BELEGT_IN` edge from the claim-bearing node to a `:Quelle` node, with optional `eigenschaft` to scope which property/aspect of the source node is being cited.
- Naming: German PascalCase Labels, SCREAMING_SNAKE edges, snake_case properties.
- Every Label: `CREATE CONSTRAINT FOR (n:<Label>) REQUIRE n.id IS UNIQUE`.

# Appendix B — Constraints & indexes

- UNIQUE id per Label.
- Range indexes on `:Fallbeispiel(art)`, `:Fallbeispiel(flaeche_m2)`, `:Fallbeispiel(fertigstellung_jahr)`, `:Bauteilgruppe(bauteil_label)`, `:Bauteilgruppe(material_label)`, `:Bauteilgruppe(masse_t)`, `:Bauteilgruppe(co2_einsparung_kg)`.
- Full-text index `body_de` on all instance + vocab Labels.

# Appendix C — Coverage checklist

Verification table proving every:
- folder under `_database/<entity>/` → destination Label (or merged into a property);
- legacy relation in `clean_confirmed_edges.csv` → one of the 5 edge types (mapping in §3);
- YAML frontmatter field on legacy `fallstudie` / `projekt` / `bauobjekt` / `reuse_einsatz` / `datenpunkt` / `akteur_beteiligung` → destination property in §2.

Items explicitly not preserved: legacy `belongs_to_fallstudie` / `belongs_to_projekt` edges (no separate target Label); legacy `measured_on_bauobjekt` (measurement is now a property); legacy `:AkteurBeteiligung` / `:BauwerkBeteiligung` / `:ReuseKettenstation` / `:Datenpunkt` / `:Bauobjektklasse` / `:Tragwerkstyp` / `:Bauteilgruppentyp` / `:Einheit` / `:Kennwertdefinition` nodes (information preserved via edges, properties, or vocab merges).

# Appendix D — Renamings, drops, merges

| Change | Action |
|---|---|
| `:Fallstudie` + `:Projekt` + `:Bauobjekt` (shared id) | merge into `:Fallbeispiel` with `art` property |
| `:ReuseEinsatz` | rename to `:Bauteilgruppe` |
| `:ReuseKette` | rename to `:Wiederverwendungskette` (kept) |
| `:ReuseKettenstation` | drop — stations become GEHÖRT_ZU edges on `:Bauteilgruppe` |
| `:BewertungslogikAbgrenzung` | rename to `:WiederverwendungsArt` (absorbs `:Bauteilgruppentyp` values) |
| `:Bauteilgruppentyp` | merge into `:WiederverwendungsArt` |
| `:Tragwerkstyp` | drop (axis mix per review §7.8) |
| `:Bauobjektklasse` | drop (Halle/Lager-pattern: values collapse into `:Fallbeispiel.art`) |
| `:Einheit` | drop as Label; remains as property strings |
| `:Kennwertdefinition` | drop as Label; remains in spec as documentation of kennwert names |
| `:AkteurBeteiligung` | drop; role goes on `HAT {art:'akteur', rolle:...}` edge |
| `:BauwerkBeteiligung` | drop; same pattern |
| `:Datenpunkt` and ~26 measurement Labels (`:Flaeche`, `:CO2_Einsparung`, …) | drop; measurements become properties on `:Fallbeispiel` / `:Bauteilgruppe` / `BENUTZT` edge |
| `:BuildBatch` | drop; `build_status` and `legacy_paths` stay as properties |
| `:Foerderprogramm` + `:ProgrammKontext` | merge into `:Programm` with `programm_typ` property |
| `:BELEGT` (Quelle → claim) | rename + reverse to `:BELEGT_IN` (claim → Quelle) |
| All `*_quelle`, `*_quellen`, `quelle_id`, `quelle_label_raw` properties on any node or edge | drop — replaced exclusively by `:BELEGT_IN` edges with optional `eigenschaft` property to scope which property/aspect of the source node is being cited |
| `Moebelsepearat` | rename to `Moebel_separat` |
| `ort/Scwheiz` | rename to `ort/Schweiz` |
| Bauteiltyp drop-and-remap (SCHEMA.md §5) | already applied — noted in spec |
| Material drop-and-merge (SCHEMA.md §6) | already applied — noted in spec |

---

## Out of scope (this plan)

- Writing the export script.
- Running a Neo4j instance.
- Filling the ~30 gap relations from prose.
- Translating German labels to English.
