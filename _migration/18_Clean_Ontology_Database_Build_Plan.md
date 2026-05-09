# Clean Ontology Database Build Plan

Status: upgraded plan after semantic normalization.  
No final move has been done.

## Decision

Build the final database from `_graph`, but do not import `_graph` directly.

Final rule:

- `_database` contains only clean ontology folders and confident normalized nodes.
- `_manual_review` contains all `REVIEW_REQUIRED` and conflict-prone nodes.
- `_graph` remains the staging graph and evidence workspace.
- `quelle` archives the old knowledge once, so no source content is lost.

This means cleanliness wins over maximum automatic import.

## Current State Checked

Current staged `_graph`:

```text
62 folders
2,492 staged node folders
```

Largest staged folders:

```text
reuse_einsatz              637
datenpunkt                 619
akteur_beteiligung         238
fallstudie                  99
quelle                      96
projekt                     89
bauobjekt                   88
reuse_kettenstation         86
software_digitaltool        76
akteur                      65
bauteiltyp                  53
reuse_kette                 43
kennwertdefinition          31
huerde                      30
material                    27
```

Final schema decision:

```text
55 folders included in clean final ontology
7 folders excluded from first clean database
```

Normalization decision map:

```text
124 CONFIDENT decisions
27 REVIEW_REQUIRED decisions
```

## Final Clean Tree

Empty folders are allowed. They are schema structure, not fake data.

```text
_database/

  _system/
    schema.md
    import_manifest.md
    migration_notes.md
    validation_report.md

  _edges/
    edges_reviewed.csv
    edges_review_queue.csv

  quelle/
    OLD_FILE_ID/
      index.md
      DATEIEN/original_old_file.md

  fallstudie/
  projekt/
  bauobjekt/
  akteur/
  reuse_einsatz/
  reuse_kette/
  reuse_kettenstation/
  akteur_beteiligung/
  bauobjekt_beteiligung/
  datenpunkt/
  software_digitaltool/

  bauobjektklasse/
  bauobjektrolle/
  bauobjektstatus/
  nutzung/
  bauaufgabe_intervention/
  ort/

  reuse_strategie/
  bewertungslogik_abgrenzung/
  reuse_einsatzstatus/
  ressourcenquelle/
  beschaffungsweg/

  bauteiltyp/
  bauteilebene/
  material/
  bauteilzustand/
  funktionswechsel/

  bauweise/
  bausystem/
  tragwerksprinzip/
  tragwerkstyp/
  fuegung_verbindung/

  prozessphase/
  rueckbauverfahren/
  aufbereitungsverfahren/
  logistik/

  pruefung_nachweis/
  leistungsanforderung/
  norm/
  rechtliche_bedingung/
  schadstoff/
  huerde/

  kennwertdefinition/
  datenqualitaet/
  zertifizierung_bewertungssystem/
  datenmodell/
  dokumenttyp/

  programm_kontext/
  kontextmerkmal/
  wirtschaft/
  foerderprogramm/

  akteurrolle/
  tooltyp/
  methode/
```

## Folders Excluded From Clean Database

These must not enter `_database` in the automatic build:

```text
meta/
akteurleistung/
akteurtyp/
beleg/
gebaeudetypologie/
plattformfunktion/
plattformzugang/
```

Reason: redundant, immature, empty, or better represented by clean folders.

## Manual Review At The End

These nodes should stay outside `_database` until you migrate them manually one by one.

Target holding area:

```text
_manual_review/
  nodes/
    ENTITY/
      ID/
        index.md
  review_queue.md
```

Manual queue:

```text
_graph/datenpunkt/Timber_Square_London__001__Wiederverwendete_Stahltr_ger
_graph/datenpunkt/ELYS_Kultur_Gewerbehaus_Basel__003__Fenster
_graph/bauteiltyp/Tragstruktur
_graph/bauteiltyp/Bauwerksteil
_graph/bauteiltyp/Treppenwange
_graph/bauteiltyp/Kueche
_graph/bauteiltyp/Bruestung
_graph/bauteiltyp/Holzrahmenelement
_graph/bauteiltyp/Kern
_graph/bauteiltyp/Fliese
_graph/bauteiltyp/Auflager_Widerlager
_graph/bauteiltyp/Landschaftselement
_graph/material/Recyclingbeton
_graph/material/Metall
_graph/material/Guss
_graph/material/Erde
_graph/fuegung_verbindung/Beton_Fertigteile_Verbindungen
_graph/fuegung_verbindung/Holz_Verbindungen
_graph/fuegung_verbindung/Stahl_Verbindungen
_graph/fuegung_verbindung/Composite_Verbindungen
_graph/fuegung_verbindung/Stahlseil
_graph/reuse_strategie/Temporaerer_Wiedereinbau
_graph/huerde/Logistikproblem
_graph/huerde/Performance_Nachweis
_graph/datenmodell/Gebaeuderessourcenpass
_graph/dokumenttyp/Gebaeuderessourcenpass
_graph/zertifizierung_bewertungssystem/DGNB
```

Important: source evidence for these still remains in `quelle`; they are only excluded from clean semantic import.

## Clean Import Logic

### 1. Create Schema First

Create every included folder under `_database`, even when empty.

This protects the ontology shape:

```text
entity/id/index.md
```

No bare slugs. Every node ID is path-typed.

### 2. Archive Sources Once

Final `quelle` should contain all old knowledge files once.

Target:

```text
_database/quelle/OLD_FILE_ID/index.md
_database/quelle/OLD_FILE_ID/DATEIEN/original_old_file.md
```

This preserves the full old knowledge base without duplicating full old text into every domain node.

### 3. Import Core Graph Nodes

Import clean core nodes:

```text
fallstudie
projekt
bauobjekt
akteur
reuse_einsatz
reuse_kette
reuse_kettenstation
akteur_beteiligung
bauobjekt_beteiligung
datenpunkt
software_digitaltool
```

But skip:

- fake `index` nodes,
- duplicate-ID datapoints marked for review,
- any node listed in manual review.

### 4. Apply Only CONFIDENT Normalization

Use `_migration/17_Semantic_Normalization_Decisions.md` as the rule source.

Examples:

```text
_graph/material/Beton_Fertigteile
  -> _database/bauteiltyp/Betonfertigteil

_graph/bauteiltyp/Ziegel
  -> _database/material/Ziegel

_graph/bauteiltyp/Dachtragwerk
  -> _database/tragwerkstyp/Dachtragwerk

_graph/prozessphase/Ausschreibung
  -> method/procurement/document split, not prozessphase

_graph/datenmodell/Materialpass
  -> _database/datenmodell/Materialpass_Schema

_graph/software_digitaltool/Madaster
  -> _database/software_digitaltool/Madaster

_graph/akteur/Madaster
  -> _database/akteur/Madaster
```

For `move/merge`, create one clean target node with aliases/source references.

For `move/split`, do not create a vague old node. Create only clean target facts or edges.

### 5. Build Reuse Mapping

Every building example should map through `reuse_einsatz`.

Clean pattern:

```text
fallstudie
  documents -> projekt

projekt
  has_object -> bauobjekt
  has_actor_participation -> akteur_beteiligung

reuse_einsatz
  belongs_to -> fallstudie
  in_project -> projekt
  used_in -> bauobjekt
  has_material -> material
  has_component_type -> bauteiltyp
  has_strategy -> reuse_strategie
  has_status -> reuse_einsatzstatus
  has_process_phase -> prozessphase
  has_hurdle -> huerde
  has_requirement -> leistungsanforderung
  has_proof -> pruefung_nachweis
  has_norm -> norm
  has_source -> quelle

akteur_beteiligung
  actor -> akteur
  role -> akteurrolle
  in_project -> projekt
```

This keeps examples, buildings, actors, and ontology knots connected without turning everything into one flat folder.

### 6. Import Controlled Knots

Controlled knots should be clean, broad enough to map many cases, and not too broad to be meaningless.

Important canonical examples:

```text
prozessphase/
  Identifikation/
  Dokumentation/
  Pruefung/
  Rueckbau/
  Transport/
  Lagerung/
  Aufbereitung/
  Planung/
  Wiedereinbau/
  Betrieb/

bauteiltyp/
  Stuetze/
  Traeger/
  Decke/
  Wand/
  Fassade/
  Fenster/
  Tuer/
  Treppe/
  Dach/
  Boden/
  Innenausbau/
  Festes_Einbauteil/
  Technik_TGA/
  Sanitaerobjekt/
  Leuchte/
  PV_Anlage/
  Platte_Paneel/
  Betonfertigteil/
  Fundament/

material/
  Beton/
  Stahlbeton/
  Stahl/
  Sekundaerstahl/
  Holz/
  Brettschichtholz/
  Brettsperrholz/
  Glas/
  Aluminium/
  Ziegel/
  Naturstein/
  Granit/
  Marmor/
  Keramik/
  Kunststoff/
  Daemmstoff/
  Mineralwolle/
  Polystyrol/
  Lehm/
  Stroh/
  Composite/
```

Broad fallback nodes are not imported automatically when they are marked `REVIEW_REQUIRED`.

## Validation Gates Before Import

The clean build is accepted only if all checks pass:

```text
1. No folder from the excluded list exists in _database.
2. No REVIEW_REQUIRED node exists in _database.
3. No fake index case nodes exist.
4. No bare slug node IDs are used in edges.
5. Every edge source and target exists as entity/id.
6. Every old file is archived once in quelle.
7. No duplicate same-meaning node exists across folders.
8. Same label across folders is allowed only with different semantic type.
9. Prozessphase contains only canonical phases.
10. Norm contains only actual named standards.
11. Material contains only material classes, not component types.
12. Bauteiltyp contains only component families, not materials or full objects.
13. Software_digitaltool contains actual tools/platforms, not generic categories.
14. Datenmodell contains schemas/data structures, not tools.
15. Dokumenttyp contains document/pass/report types, not tools.
```

## Next Step Sequence

### Step A: Generate Dry-Run Manifest

Create:

```text
_migration/19_clean_build_dry_run_manifest.csv
```

Columns:

```text
old_path,target_path,action,status,reason
```

This is the exact final move list before touching folders.

### Step B: Generate Manual Review Queue

Create:

```text
_migration/19_manual_review_queue.csv
```

Only the 27 `REVIEW_REQUIRED` rows.

### Step C: Build Clean Database In New Folder

Create:

```text
_database/
```

Do not overwrite old folders. Do not delete `_graph`.

### Step D: Validate

Generate:

```text
_database/_system/validation_report.md
```

If validation fails, stop and fix the build plan, not the old source.

### Step E: Manual Review Later

After clean import works, manually review `_manual_review` one node at a time.

Only after a manual decision:

```text
_manual_review/... -> _database/clean_entity/clean_id
```

## Recommended Immediate Action

Do not migrate yet.

Next, generate the two dry-run files:

```text
_migration/19_clean_build_dry_run_manifest.csv
_migration/19_manual_review_queue.csv
```

Then inspect those before creating `_database`.

