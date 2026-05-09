# Phase 20 Clean Database Build Result

## What Exists Now

- `_database/` is the clean, import-ready ontology/database tree.
- `_manual_review/` contains only held-back conflict cases.
- `_graph/` remains untouched as staging/provenance.
- The old knowledge folders remain untouched.

## Build Counts

- Database index files: 3037
- Source archive nodes in `_database/quelle`: 663
- Manual-review node files: 27
- Build errors: 0
- REVIEW_REQUIRED node markers inside clean database nodes: 0
- Final manifest results:
  - `done`: 3120
  - `not_imported`: 7
  - `validation_rule_only`: 5

## Cleanliness Checks

- Excluded conflict folders are not in `_database`: `meta`, `akteurleistung`, `akteurtyp`, `beleg`, `gebaeudetypologie`, `plattformfunktion`, `plattformzugang`.
- Fake index nodes were not imported as real nodes.
- Wildcard/pseudo rules were kept as validation rules, not folders.
- All `REVIEW_REQUIRED` decisions were routed to `_manual_review`.
- No manual-review node path is duplicated inside `_database`.

## Semantic Spot Checks

- `_database/material/Ziegel/` exists.
- `_database/bauteiltyp/Betonfertigteil/` exists.
- `_database/tragwerkstyp/Dachtragwerk/` exists.
- `_database/software_digitaltool/Madaster/` exists.
- `_database/akteur/Madaster/` exists.
- `_database/datenmodell/Materialpass_Schema/` exists.
- `_database/dokumenttyp/Materialpass/` exists.
- `_database/prozessphase/Ausschreibung/` does not exist.
- `_database/datenmodell/Madaster/` does not exist.
- `_database/material/Metall/` does not exist; broad `Metall` stays in manual review.

## Manual Review Queue

These were intentionally kept out of the clean database for manual treatment:

- `bauteiltyp/Auflager_Widerlager`
- `bauteiltyp/Bauwerksteil`
- `bauteiltyp/Bruestung`
- `bauteiltyp/Fliese`
- `bauteiltyp/Holzrahmenelement`
- `bauteiltyp/Kern`
- `bauteiltyp/Kueche`
- `bauteiltyp/Landschaftselement`
- `bauteiltyp/Tragstruktur`
- `bauteiltyp/Treppenwange`
- `datenmodell/Gebaeuderessourcenpass`
- `datenpunkt/ELYS_Kultur_Gewerbehaus_Basel__003__Fenster`
- `datenpunkt/Timber_Square_London__001__Wiederverwendete_Stahltr_ger`
- `dokumenttyp/Gebaeuderessourcenpass`
- `fuegung_verbindung/Beton_Fertigteile_Verbindungen`
- `fuegung_verbindung/Composite_Verbindungen`
- `fuegung_verbindung/Holz_Verbindungen`
- `fuegung_verbindung/Stahl_Verbindungen`
- `fuegung_verbindung/Stahlseil`
- `huerde/Logistikproblem`
- `huerde/Performance_Nachweis`
- `material/Erde`
- `material/Guss`
- `material/Metall`
- `material/Recyclingbeton`
- `reuse_strategie/Temporaerer_Wiedereinbau`
- `zertifizierung_bewertungssystem/DGNB`

## Main Output Files

- `_migration/20_clean_database_build_manifest.csv`
- `_migration/20_clean_database_validation.md`
- `_database/_system/import_manifest_phase19.csv`
- `_database/_system/build_manifest_phase20.csv`
- `_database/_system/migration_notes.md`
- `_database/_system/validation_report.md`

## Recommended Next Steps

1. Approve `_database/` as the clean import base.
2. Review `_manual_review/nodes/` manually, one item at a time.
3. Add or refine empty controlled-knot folders where you want stronger vocabularies.
4. Import `_database/` into SQLite/Tolaria using typed path IDs: `entity/id`.
