# Neo4j Repository Output Contract v1.1

This is the source-of-truth contract for transforming existing markdown building-reuse project files into repo-ready graph chunks for Neo4j/MCP ingestion.

## What changed in v1.1 after double-checking

The first contract was usable, but not complete enough for a repo with many agents. This version adds the missing pieces:

1. `controlled_vocabulary.seed.kg.jsonl` is now included. Project chunks may reference controlled nodes such as `bt_traeger`, `mat_stahl`, `h_technische_freigabe`, and `ar_architektur` without redefining them.
2. `constraints.cypher` is included so Neo4j can enforce unique node IDs and, on Neo4j 5+, relationship IDs.
3. The JSON schema now restricts labels and relationship types and rejects `null` values.
4. A manifest schema is included.
5. The contract now states that the importer must materialize top-level `id` as the Neo4j property `id` for nodes and relationships.
6. `Quelle` supports both the markdown source file and optional external sources cited inside the markdown.
7. `ZITIERT_QUELLE` was added for source-file-to-external-source references.
8. `Software`, `Tool`, `Programm`, and `BauaufgabeIntervention` are included so later files do not need ad-hoc schema changes.

## Final graph model

`Fallbeispiel` is removed. The central node is `Projekt`.

Core project-specific nodes:

```text
Projekt
Bauwerk
Bauteilgruppe
Akteur
Quelle
Wiederverwendungskette
```

Controlled/shared nodes:

```text
Bauteiltyp, Bauteilebene, Bauobjektklasse, Bauobjektrolle,
Material, Materialgruppe, Huerde, HuerdeKategorie,
Akteurrolle, Akteurtyp, WiederverwendungsArt, Status, Nutzung,
Stadt, Land, Prozessphase, PruefungNachweis, Leistungsanforderung, Norm,
Aufbereitungsverfahren, Rueckbauverfahren, Beschaffungsweg, Ressourcenquelle,
Logistik, Methode, Verbindungstechnik, RechtlicheBedingung, Schadstoff,
Wirtschaft, ZertifizierungBewertungssystem, Tragwerksprinzip, Bauweise,
Bausystem, Funktionswechsel, BauaufgabeIntervention, Programm, Software, Tool
```

## File layout

Recommended repo layout:

```text
neo4j_exports/
  controlled_vocabulary.seed.kg.jsonl
  cypher/constraints.cypher
  batches/
    batch_001/
      manifest.json
      p_project_slug.kg.jsonl
      p_second_project_slug.kg.jsonl
      controlled_terms.delta.jsonl
      validation_report.md
```

## Import order

1. Run `cypher/constraints.cypher` once.
2. Import `controlled_vocabulary.seed.kg.jsonl` once.
3. For every batch, validate `manifest.json`.
4. For each project `.kg.jsonl`, import all node records first, then relationship records.
5. Import `controlled_terms.delta.jsonl` only after review, or import with `review_status:"proposed"`.

## MCP/importer requirements

The importer must do idempotent upserts:

- node: `MERGE` by top-level `record.id`, set Neo4j property `id = record.id`, then merge/overwrite properties.
- relationship: `MERGE` by top-level `record.id`, set Neo4j relationship property `id = record.id`, then merge/overwrite properties.
- relationship endpoints must exist in the same project file, controlled vocabulary seed, or controlled terms delta.

Relationship records have this structure:

```json
{"record_type":"rel","id":"r_p_example__BELEGT_IN__q_example","from":"p_example","type":"BELEGT_IN","to":"q_example","properties":{"datenqualitaet":"Belegt"}}
```

## ID rules

Normalize names:

```text
lowercase
trim
replace ä -> ae, ö -> oe, ü -> ue, ß -> ss
replace accents with ASCII equivalents
replace all non-alphanumeric characters with underscore
collapse repeated underscores
remove leading/trailing underscores
```

Use these prefixes:

```text
p_ Projekt
bw_ Bauwerk
bg_ Bauteilgruppe
a_ Akteur
q_ Quelle
wk_ Wiederverwendungskette
bt_ Bauteiltyp
be_ Bauteilebene
bok_ Bauobjektklasse
bor_ Bauobjektrolle
mat_ Material
mg_ Materialgruppe
h_ Huerde
hk_ HuerdeKategorie
ar_ Akteurrolle
at_ Akteurtyp
wva_ WiederverwendungsArt
status_ Status
nut_ Nutzung
stadt_ Stadt
land_ Land
phase_ Prozessphase
pr_ PruefungNachweis
la_ Leistungsanforderung
norm_ Norm
av_ Aufbereitungsverfahren
rv_ Rueckbauverfahren
bweg_ Beschaffungsweg
rq_ Ressourcenquelle
log_ Logistik
meth_ Methode
vt_ Verbindungstechnik
rb_ RechtlicheBedingung
s_ Schadstoff
wi_ Wirtschaft
zbs_ ZertifizierungBewertungssystem
tp_ Tragwerksprinzip
bauw_ Bauweise
bsys_ Bausystem
fw_ Funktionswechsel
bai_ BauaufgabeIntervention
prog_ Programm
sw_ Software
tool_ Tool
```

Relationship IDs:

```text
r_<from>__<TYPE>__<to>
```

If the same relationship type between the same nodes needs multiple variants, append a qualifier:

```text
r_<from>__<TYPE>__<to>__section_5
```

## Property rules

Use properties only for scalar or project-specific values:

```text
name, raw_name, note, numeric metrics, booleans, dates, years, old/new function text
```

Do not use properties for reusable concepts. Use nodes instead.

Examples of node values, not properties:

```text
stadt, land, bauobjektklasse, bauobjektrolle, bauteiltyp, material,
materialgruppe, huerde, huerdekategorie, akteurrolle, akteurtyp, status,
nutzung, pruefung, norm, leistungsanforderung, prozessphase, tragwerksprinzip
```

## Datenqualitaet

`Datenqualitaet` is not a node. It appears only on `BELEGT_IN` relationships and is always:

```json
{"datenqualitaet":"Belegt"}
```

Uncertainty or source conflict goes into `note` or range properties on the relevant node, not into `datenqualitaet`.

## Kennwert

`Kennwert` is not a node. Metrics are properties on the scoped node:

```text
Projekt.flaeche_m2
Projekt.reuse_anteil_prozent
Bauwerk.baujahr
Bauteilgruppe.menge_t
Bauteilgruppe.menge_m3
Bauteilgruppe.anzahl
Bauteilgruppe.co2_einsparung_t
```

For conflicts use min/max or notes:

```json
{"flaeche_m2_min":4871,"flaeche_m2_max":7603,"note":"Conflicting source values"}
```

## Quelle handling

Every project file must include one `Quelle` node for the markdown file itself:

```json
{"record_type":"node","id":"q_crclr_house_impact_hub_berlin_md","labels":["Quelle"],"properties":{"name":"CRCLR_House_Impact_Hub_Berlin.md","quelltyp":"case_markdown"}}
```

If the markdown contains an external source list and the sources are easy to extract, add optional external `Quelle` nodes:

```json
{"record_type":"node","id":"q_crclr_s1","labels":["Quelle"],"properties":{"name":"Source label S1","quelltyp":"external_reference","url":"https://example.org"}}
{"record_type":"rel","id":"r_q_crclr_house_impact_hub_berlin_md__ZITIERT_QUELLE__q_crclr_s1","from":"q_crclr_house_impact_hub_berlin_md","type":"ZITIERT_QUELLE","to":"q_crclr_s1","properties":{}}
```

The project-specific graph can still use `BELEGT_IN` to the markdown source file. External source extraction is useful but should not block project migration.

## Required relationship vocabulary

Use only these relationship types unless the schema is deliberately updated:

```text
HAT_BAUTEILGRUPPE, NUTZT_BAUWERK, AUS_BAUWERK, EINGEBAUT_IN, TEIL_VON_KETTE, HAT_BAUTEILTYP, HAT_BAUTEILEBENE, HAT_BAUOBJEKTKLASSE, HAT_BAUOBJEKTROLLE, HAT_TRAGWERKSPRINZIP, HAT_BAUWEISE, HAT_BAUSYSTEM, HAT_STATUS, HAT_NUTZUNG, HAT_WIEDERVERWENDUNGSART, HAT_FUNKTIONSWECHSEL, HAT_INTERVENTION, NUTZT_MATERIAL, HAT_MATERIALGRUPPE, HAT_PROZESSPHASE, HAT_METHODE, HAT_RUECKBAUVERFAHREN, HAT_AUFBEREITUNG, HAT_BESCHAFFUNGSWEG, HAT_RESSOURCENQUELLE, HAT_LOGISTIK, HAT_VERBINDUNGSTECHNIK, HAT_PRUEFUNG, HAT_LEISTUNGSANFORDERUNG, REFERENZIERT_NORM, HAT_RECHTLICHE_BEDINGUNG, HAT_SCHADSTOFF, HAT_ZERTIFIZIERUNG, HAT_WIRTSCHAFTSASPEKT, HAT_HUERDE, HAT_HUERDEKATEGORIE, BETEILIGT_AN, HAT_AKTEURROLLE, HAT_AKTEURTYP, LIEGT_IN_STADT, LIEGT_IN_LAND, BELEGT_IN, ZITIERT_QUELLE, NUTZT_SOFTWARE, NUTZT_TOOL, TEIL_VON_PROGRAMM
```

## Minimum validity per project file

A project file is valid if:

1. exactly one `Projekt` node exists for a normal one-project file;
2. at least one `Quelle` node exists;
3. `Projekt` has `BELEGT_IN` to the markdown `Quelle`;
4. `Projekt` has at least one `Bauteilgruppe`;
5. every `Bauteilgruppe` has `HAT_BAUTEILTYP`, `NUTZT_MATERIAL`, and `BELEGT_IN`;
6. every `Bauwerk` has `HAT_BAUOBJEKTKLASSE`, `HAT_BAUOBJEKTROLLE`, and `BELEGT_IN`;
7. every `Akteur` has `HAT_AKTEURROLLE`, `HAT_AKTEURTYP` when inferable, and `BELEGT_IN`;
8. every `Material` used has `HAT_MATERIALGRUPPE` in the seed or project file;
9. every `Huerde` used has `HAT_HUERDEKATEGORIE` in the seed or delta;
10. every relationship endpoint exists in the same file, the controlled seed, or the reviewed delta.

## Controlled terms delta

Do not invent new controlled terms inside project files when an existing term fits. If a new term is necessary, place it in `controlled_terms.delta.jsonl` with `review_status:"proposed"`.

## Batch output from ChatGPT

For each batch of up to 5 source markdown files, output a folder containing:

```text
manifest.json
one .kg.jsonl file per project
controlled_terms.delta.jsonl, only when needed
validation_report.md
```

Do not paste full JSONL in chat unless requested. Save files and link them.
