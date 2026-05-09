# Clean End Result Preview

## Status

This is a proposal only. Nothing should be moved into the final database until this structure is approved.

Current situation:

- Old folders stay where they are.
- `_graph` is a staging graph.
- `_graph` contains useful extracted knowledge, but also duplicate preservation text, generated helper nodes, review nodes, and possible over-linking.

The clean final result should be a new reviewed graph, not a blind rename of `_graph`.

Recommended final root:

```text
_database/
  entity/
    id/
      index.md
      DATEIEN/
```

Alternative name:

```text
_graph_final/
```

## Clean Principle

One node should mean one semantic thing.

Do not store the same old file text everywhere. The full old source should live once as `quelle`. Other nodes should contain structured summaries, facts, and links back to source.

## Final Core Entities

These are the main database entities that should remain in the clean final version.

```text
fallstudie/
projekt/
bauobjekt/
reuse_einsatz/
reuse_kette/
reuse_kettenstation/
akteur/
akteur_beteiligung/
software_digitaltool/
quelle/
```

Meaning:

- `fallstudie`: the researched case/narrative.
- `projekt`: the planning/building project.
- `bauobjekt`: the physical building/object.
- `reuse_einsatz`: one concrete reused component/material use.
- `reuse_kette`: chain from donor/source to receiver/use.
- `reuse_kettenstation`: steps in that chain.
- `akteur`: real organizations/persons/platform operators.
- `akteur_beteiligung`: actor role in a specific case/project.
- `software_digitaltool`: platforms/tools like Restado, RotorDC, Madaster.
- `quelle`: original old file or source dossier.

## Final Knot Entities

These should stay as controlled vocabulary / classification knots.

```text
bauteiltyp/
material/
tragwerkstyp/
tragwerksprinzip/
bausystem/
bauweise/
bauaufgabe_intervention/
fuegung_verbindung/
reuse_strategie/
prozessphase/
aufbereitungsverfahren/
rueckbauverfahren/
logistik/
huerde/
bewertungslogik_abgrenzung/
pruefung_nachweis/
leistungsanforderung/
norm/
rechtliche_bedingung/
kennwertdefinition/
wirtschaft/
schadstoff/
foerderprogramm/
ort/
datenmodell/
dokumenttyp/
tooltyp/
beschaffungsweg/
ressourcenquelle/
zertifizierung_bewertungssystem/
```

Meaning:

- These are not usually case documents.
- They are reusable knots for graph filtering and comparison.
- They should be compact and canonical.
- They should not contain huge copied legacy text unless they are source dossiers.

## Entities To Keep Out Of Final For Now

These folders currently exist but should not be moved into a clean final database unless they become necessary.

```text
akteurleistung/
akteurtyp/
bauobjekt_beteiligung/
bauobjektrolle/
bauobjektstatus/
bauteilebene/
bauteilzustand/
beleg/
datenqualitaet/
funktionswechsel/
gebaeudetypologie/
nutzung/
plattformfunktion/
plattformzugang/
programm_kontext/
```

Reason:

- They currently have zero nodes or are not mature enough.
- They can be added later if the data really needs them.

## Clean File Shape

Every final node should look like this:

```text
_database/reuse_einsatz/Multi_Brussels_Reuse_in_MULTI__001__Blausteinbloecke_Fassadenplatten/
  index.md
  DATEIEN/
```

`index.md` should contain:

```yaml
---
id: "Multi_Brussels_Reuse_in_MULTI__001__Blausteinbloecke_Fassadenplatten"
entity: "reuse_einsatz"
title: "Blausteinbloecke / Fassadenplatten"
node_kind: "core"
source_status: "reviewed"
legacy_source: "quelle/Gebaeude_Multi_Brussels_Reuse_in_MULTI"
fallstudie: "fallstudie/Multi_Brussels_Reuse_in_MULTI"
projekt: "projekt/Multi_Brussels_Reuse_in_MULTI"
bauobjekt: "bauobjekt/Multi_Brussels_Reuse_in_MULTI"
primary_bauteiltyp: "bauteiltyp/Fassade"
secondary_bauteiltyp:
  - "bauteiltyp/Platte_Paneel"
material:
  - "material/Naturstein"
huerde:
  - "huerde/Bruch_Beschaedigungsrisiko"
  - "huerde/Aufbereitungsaufwand"
---
```

Body:

```md
# Blausteinbloecke / Fassadenplatten

## Kurzbeschreibung

Wiederverwendete Blausteinbloecke bzw. Fassadenplatten aus dem MULTI-Bestand.

## Einsatz

- Alte Funktion: Fassadenbekleidung
- Neue Funktion: Terrasse, Wandbekleidung, Plinthe / Innenraum
- Umfang: 82 Bloecke bzw. ca. 280 m2 / 140 t laut Quelle

## Aufbereitung

Demontage, Saegen, Remanufacturing, Wiederverlegung.

## Unsicherheiten

- Normen nicht belegt
- genaue Pruefwerte nicht belegt
```

## Clean Example: MULTI Brussels

Old file:

```text
Gebäude/Multi_Brussels_Reuse_in_MULTI.md
```

Clean final result:

```text
_database/quelle/Gebaeude_Multi_Brussels_Reuse_in_MULTI/index.md
_database/fallstudie/Multi_Brussels_Reuse_in_MULTI/index.md
_database/projekt/Multi_Brussels_Reuse_in_MULTI/index.md
_database/bauobjekt/Multi_Brussels_Reuse_in_MULTI/index.md
_database/reuse_einsatz/Multi_Brussels_Reuse_in_MULTI__001__Blausteinbloecke_Fassadenplatten/index.md
_database/reuse_einsatz/Multi_Brussels_Reuse_in_MULTI__002__Blaustein_Flagstones/index.md
_database/reuse_einsatz/Multi_Brussels_Reuse_in_MULTI__003__Granitboden/index.md
_database/reuse_einsatz/Multi_Brussels_Reuse_in_MULTI__004__Granitplatten_Terrasse/index.md
_database/reuse_einsatz/Multi_Brussels_Reuse_in_MULTI__005__Aluminiumprofile/index.md
_database/reuse_einsatz/Multi_Brussels_Reuse_in_MULTI__006__Aufzugsmotoren/index.md
_database/reuse_einsatz/Multi_Brussels_Reuse_in_MULTI__007__Tueren_Waende_Einbauten/index.md
```

Important:

- The full old Markdown text should live in `quelle`.
- `fallstudie` should summarize the case, not duplicate the whole old file.
- `reuse_einsatz` should hold only the relevant row/facts.
- Edges should hold graph relations.

## Edge Shape

Edges should be imported from reviewed CSV, not guessed from folder names.

Recommended clean edge file:

```text
_database/_edges/edges_reviewed.csv
```

Columns:

```text
source, relation, target, confidence, source_field, raw_label, source_file, review_status
```

Example:

```csv
source,relation,target,confidence,source_field,raw_label,source_file,review_status
reuse_einsatz/Multi_Brussels_Reuse_in_MULTI__001__Blausteinbloecke_Fassadenplatten,primary_bauteiltyp,bauteiltyp/Fassade,reviewed,bauteil_label,"Blausteinbloecke / Fassadenplatten",Gebäude/Multi_Brussels_Reuse_in_MULTI.md,approved
reuse_einsatz/Multi_Brussels_Reuse_in_MULTI__001__Blausteinbloecke_Fassadenplatten,uses_material,material/Naturstein,reviewed,material_label,"Belgischer Blaustein",Gebäude/Multi_Brussels_Reuse_in_MULTI.md,approved
```

## What Must Be Cleaned Before Final Move

1. Remove duplicate full legacy text from generated `fallstudie`, `projekt`, `bauobjekt`, and `reuse_einsatz` nodes.
2. Keep full old content once in `quelle`.
3. Split `has_bauteiltyp` into:
   - `primary_bauteiltyp`
   - `secondary_bauteiltyp`
   - or review if uncertain.
4. Remove empty entity folders from the final result.
5. Do not import unresolved review rows as facts.
6. Normalize IDs to avoid broken umlaut-safe slugs.
7. Review 10-15 representative buildings before batch-finalizing.

## What The Final Move Should Do

Only after approval:

1. Create `_database`.
2. Copy only approved entity folders/nodes from `_graph`.
3. Rewrite generated nodes into clean summaries.
4. Write reviewed edge CSV.
5. Keep `_graph` as migration staging/archive.
6. Keep old folders untouched unless you explicitly approve archiving them.

## Decision Needed

Before final move, approve or change:

- Final root name: `_database` or `_graph_final`
- Whether full old file text lives only in `quelle`
- Whether `primary_bauteiltyp` / `secondary_bauteiltyp` is the right edge model
- Which empty/immature entities should be excluded
