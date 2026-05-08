# Final Legacy Coverage Report

- Source map: _migration/legacy_to_new_map.csv
- Unique mapped legacy paths: 567
- Phase 5 source/meta nodes created: 102
- Missing after phase 5: 0

## Entity Counts

- akteur: 56
- akteur_beteiligung: 238
- akteurleistung: 0
- akteurrolle: 0
- akteurtyp: 0
- aufbereitungsverfahren: 7
- bauaufgabe_intervention: 3
- bauobjekt: 88
- bauobjekt_beteiligung: 0
- bauobjektklasse: 1
- bauobjektrolle: 0
- bauobjektstatus: 0
- bausystem: 3
- bauteilebene: 0
- bauteiltyp: 20
- bauteilzustand: 0
- bauweise: 2
- beleg: 0
- beschaffungsweg: 2
- bewertungslogik_abgrenzung: 0
- datenmodell: 9
- datenpunkt: 619
- datenqualitaet: 0
- dokumenttyp: 16
- fallstudie: 99
- foerderprogramm: 5
- fuegung_verbindung: 12
- funktionswechsel: 0
- gebaeudetypologie: 0
- huerde: 13
- kennwertdefinition: 5
- kontextmerkmal: 2
- leistungsanforderung: 13
- logistik: 6
- material: 14
- meta: 6
- methode: 11
- norm: 8
- nutzung: 0
- ort: 12
- plattformfunktion: 0
- plattformzugang: 0
- programm_kontext: 0
- projekt: 89
- prozessphase: 9
- pruefung_nachweis: 11
- quelle: 96
- rechtliche_bedingung: 6
- ressourcenquelle: 1
- reuse_einsatz: 637
- reuse_einsatzstatus: 1
- reuse_kette: 43
- reuse_kettenstation: 86
- reuse_strategie: 8
- rueckbauverfahren: 5
- schadstoff: 5
- software_digitaltool: 76
- tooltyp: 2
- tragwerksprinzip: 4
- tragwerkstyp: 9
- wirtschaft: 6
- zertifizierung_bewertungssystem: 1

## Notes

- The migration is staged in _graph; legacy files were copied, not moved.
- quelle and meta nodes are preservation nodes for indexes, reports, archive material, and system notes that did not belong cleanly in a semantic entity.
- Detailed extraction from case tables is in reuse_einsatz, datenpunkt, and akteur_beteiligung.
