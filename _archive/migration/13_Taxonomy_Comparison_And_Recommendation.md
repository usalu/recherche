# Taxonomy Comparison And Recommendation

## Short Verdict

Your proposed structure is better for the final database.

The current preview is mostly correct in its entities/knots, but it hides too much relational meaning inside `_edges/*.csv`. For a clean SQLite + graph model, we should adopt your grouped taxonomy and add explicit relation entities/tables.

## Main Difference

Current preview:

```text
_database/
  core folders
  knot folders
  _edges/edges_reviewed.csv
```

Your proposal:

```text
DATABASE/
  CORE ENTITIES
  RELATION ENTITIES
  KNOT GROUPS
```

Recommended final:

Use your grouping, but treat relation entities as structured relation tables/folders generated from reviewed edges.

## Comparison By Group

| Your group | Current preview status | Recommendation |
|---|---|---|
| Core entities | Mostly present | Keep. Move `akteur_beteiligung` out of core and into relation entities. |
| Relation entities | Mostly missing as folders; currently stored as `_edges` rows | Add this layer. This is the biggest improvement. |
| Building / object knots | Partly present | Keep all in schema; populate only where real data exists. |
| Actor knots | Only `akteurrolle` populated | Keep `akteurtyp` and `akteurleistung` as empty schema slots for later. |
| Reuse knots | Mostly present | Keep. Add `funktionswechsel` as schema slot. |
| Component / material knots | Mostly present | Keep. Add `bauteilebene` and `bauteilzustand` as schema slots. |
| Structure / construction knots | Present | Keep. This matches our Tragwerk logic. |
| Process / method knots | Present | Keep. |
| Requirement / law / proof knots | Present | Keep. |
| Data / documentation knots | Mostly present | Add `quellentyp` or map it to `dokumenttyp`; decide one. |
| Digital platform knots | Partly present | Keep `tooltyp`; add `plattformfunktion` and `plattformzugang` as schema slots. |
| Economy / context knots | Partly present | Keep `wirtschaft`, `foerderprogramm`; add `programm_kontext` as schema slot. |

## Exact Entity Decision

### Core Entities

Use:

```text
fallstudie
projekt
bauobjekt
akteur
reuse_einsatz
reuse_kette
reuse_kettenstation
software_digitaltool
quelle
datenpunkt
```

Change from current preview:

```text
akteur_beteiligung
```

should not be core. It is a relation entity.

### Relation Entities

Use:

```text
akteur_beteiligung
bauobjekt_beteiligung
reuse_einsatz_bauteil
reuse_einsatz_material
reuse_einsatz_nachweis
reuse_einsatz_huerde
reuse_einsatz_logistik
reuse_einsatz_datenpunkt
reuse_einsatz_tool
```

Current situation:

- `akteur_beteiligung` already exists as nodes: 238
- `bauobjekt_beteiligung` exists as folder but has 0 nodes
- the others do not exist yet as folders
- their information currently lives in reviewed edge rows:
  - `has_bauteiltyp`: 848
  - `uses_material`: 592
  - `has_huerde`: 444
  - `has_bewertungslogik_abgrenzung`: 151
  - `has_pruefung_nachweis`: 48
  - `measures_kennwertdefinition`: 612

Recommendation:

Create relation entities from reviewed edges only after semantic QA. This makes the database easier to query and keeps edge properties like raw label, confidence, source file, role, primary/secondary status.

### Building / Object Knots

Use:

```text
bauobjektklasse
bauobjektrolle
bauobjektstatus
nutzung
bauaufgabe_intervention
gebaeudetypologie
ort
kontextmerkmal
```

Current populated:

```text
bauobjektklasse
bauaufgabe_intervention
ort
kontextmerkmal
```

Schema slots to keep but populate later:

```text
bauobjektrolle
bauobjektstatus
nutzung
gebaeudetypologie
```

### Actor Knots

Use:

```text
akteurtyp
akteurrolle
akteurleistung
```

Current populated:

```text
akteurrolle
```

Keep `akteurtyp` and `akteurleistung` as final schema slots, but do not generate fake nodes yet.

### Reuse Knots

Use:

```text
reuse_strategie
reuse_einsatzstatus
bewertungslogik_abgrenzung
ressourcenquelle
beschaffungsweg
funktionswechsel
```

Current populated:

```text
reuse_strategie
reuse_einsatzstatus
bewertungslogik_abgrenzung
ressourcenquelle
beschaffungsweg
```

Keep `funktionswechsel` as a schema slot.

### Component / Material Knots

Use:

```text
bauteiltyp
bauteilebene
material
bauteilzustand
schadstoff
```

Current populated:

```text
bauteiltyp
material
schadstoff
```

Keep `bauteilebene` and `bauteilzustand` as schema slots.

### Structure / Construction Knots

Use exactly:

```text
bauweise
bausystem
tragwerksprinzip
tragwerkstyp
fuegung_verbindung
```

This matches the semantic correction we made:

```text
term -> true entity -> derived structural type
```

Example:

```text
Betonfertigteil-System
  true entity: bausystem
  derived: tragwerkstyp/Betonfertigteil_Tragwerk
  component: bauteiltyp/Betonfertigteil
  material: material/Beton
```

### Process / Method Knots

Use:

```text
prozessphase
rueckbauverfahren
aufbereitungsverfahren
methode
logistik
```

Current preview matches this.

### Requirement / Law / Proof Knots

Use:

```text
leistungsanforderung
pruefung_nachweis
norm
rechtliche_bedingung
zertifizierung_bewertungssystem
huerde
```

Current preview matches this.

### Data / Documentation Knots

Use:

```text
kennwertdefinition
datenqualitaet
datenmodell
dokumenttyp
quellentyp
```

Current populated:

```text
kennwertdefinition
datenmodell
dokumenttyp
```

Decision needed:

Either add `quellentyp`, or use `dokumenttyp` for source type. I recommend adding `quellentyp` if you want to distinguish "PDF / website / report / database / interview" from document genre.

### Digital Platform Knots

Use:

```text
tooltyp
plattformfunktion
plattformzugang
```

Current populated:

```text
tooltyp
```

Keep `plattformfunktion` and `plattformzugang` as schema slots.

### Economy / Context Knots

Use:

```text
wirtschaft
foerderprogramm
programm_kontext
```

Current populated:

```text
wirtschaft
foerderprogramm
```

Keep `programm_kontext` as schema slot.

## Recommended Final Tree

```text
DATABASE/
  CORE ENTITIES/
    fallstudie
    projekt
    bauobjekt
    akteur
    reuse_einsatz
    reuse_kette
    reuse_kettenstation
    software_digitaltool
    quelle
    datenpunkt

  RELATION ENTITIES/
    akteur_beteiligung
    bauobjekt_beteiligung
    reuse_einsatz_bauteil
    reuse_einsatz_material
    reuse_einsatz_nachweis
    reuse_einsatz_huerde
    reuse_einsatz_logistik
    reuse_einsatz_datenpunkt
    reuse_einsatz_tool

  KNOTS/
    building_object
    actor
    reuse
    component_material
    structure_construction
    process_method
    requirement_law_proof
    data_documentation
    digital_platform
    economy_context
```

Physical folder version:

```text
_database/
  fallstudie/
  projekt/
  bauobjekt/
  akteur/
  reuse_einsatz/
  reuse_kette/
  reuse_kettenstation/
  software_digitaltool/
  quelle/
  datenpunkt/

  akteur_beteiligung/
  bauobjekt_beteiligung/
  reuse_einsatz_bauteil/
  reuse_einsatz_material/
  reuse_einsatz_nachweis/
  reuse_einsatz_huerde/
  reuse_einsatz_logistik/
  reuse_einsatz_datenpunkt/
  reuse_einsatz_tool/

  bauobjektklasse/
  bauobjektrolle/
  bauobjektstatus/
  nutzung/
  bauaufgabe_intervention/
  gebaeudetypologie/
  ort/
  kontextmerkmal/

  akteurtyp/
  akteurrolle/
  akteurleistung/

  reuse_strategie/
  reuse_einsatzstatus/
  bewertungslogik_abgrenzung/
  ressourcenquelle/
  beschaffungsweg/
  funktionswechsel/

  bauteiltyp/
  bauteilebene/
  material/
  bauteilzustand/
  schadstoff/

  bauweise/
  bausystem/
  tragwerksprinzip/
  tragwerkstyp/
  fuegung_verbindung/

  prozessphase/
  rueckbauverfahren/
  aufbereitungsverfahren/
  methode/
  logistik/

  leistungsanforderung/
  pruefung_nachweis/
  norm/
  rechtliche_bedingung/
  zertifizierung_bewertungssystem/
  huerde/

  kennwertdefinition/
  datenqualitaet/
  datenmodell/
  dokumenttyp/
  quellentyp/

  tooltyp/
  plattformfunktion/
  plattformzugang/

  wirtschaft/
  foerderprogramm/
  programm_kontext/
```

## What Should Change In Our Current Preview

1. Move `akteur_beteiligung` from core group to relation group.
2. Add relation entity layer instead of hiding everything in `_edges`.
3. Keep empty schema folders in the final schema, but do not invent nodes.
4. Add or decide against `quellentyp`.
5. Keep `bauteilboerse` out as entity; represent it via:

```text
software_digitaltool
tooltyp
plattformfunktion
plattformzugang
beschaffungsweg
ressourcenquelle
```

## Recommendation

Approve your taxonomy as the final conceptual database structure.

Then revise the final tree preview to match it before any final move.
