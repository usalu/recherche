# Round 002 Controlled Vocabulary Review: Methode + Rueckbauverfahren + Aufbereitungsverfahren

**Generated:** 2026-05-15
**Baseline reference:** [`../round_002_baseline/global_audit_report.md`](../round_002_baseline/global_audit_report.md)

## Result in Context

Clean family. 13 Methode + 5 Rueckbauverfahren + 11 Aufbereitungsverfahren
nodes, all well-populated except 2 orphans (kept as proposed seed). No
same-name duplicates. No structural merges identified.

`meth_zirkulaere_ausschreibung` (3 inbound) overlaps semantically with
`meth_reuse_ausschreibung` (19 inbound) but the former is broader
("circular procurement", not just reuse-procurement); kept distinct.

## Methode hub snapshot (live `mit-bestand`)

| id | name | inbound |
| --- | --- | ---: |
| meth_form_follows_availability | Form_Follows_Availability | 132 |
| meth_reuse_assessment | ReUse_Assessment | 102 |
| meth_building_material_scouting | Building_Material_Scouting | 60 |
| meth_bauteilkatalogisierung | Bauteilkatalogisierung | 53 |
| meth_materialinventur | Materialinventur | 48 |
| meth_design_for_disassembly | Design_for_Disassembly | 35 |
| meth_reversibilitaet | Reversibilitaet | 31 |
| meth_urban_mining | Urban_Mining | 22 |
| meth_reuse_ausschreibung | ReUse_Ausschreibung | 19 |
| meth_pre_deconstruction_audit | Pre_Deconstruction_Audit | 16 |
| meth_zirkulaere_ausschreibung | Zirkulaere_Ausschreibung | 3 |
| meth_wiederverwendungskriterien | Wiederverwendungskriterien | 1 |
| meth_abrissmonitoring | Abrissmonitoring | 0 |

## Rueckbauverfahren hub snapshot (live `mit-bestand`)

| id | name | inbound |
| --- | --- | ---: |
| rv_selektiver_rueckbau | Selektiver_Rueckbau | 87 |
| rv_ausbau_von_bauteilen | Ausbau_von_Bauteilen | 84 |
| rv_demontage | Demontage | 72 |
| rv_zerstoerungsarme_bergung | Zerstoerungsarme_Bergung | 13 |
| rv_betonfraesen | Betonfraesen | 4 |

## Aufbereitungsverfahren hub snapshot (live `mit-bestand`)

| id | name | inbound |
| --- | --- | ---: |
| av_reinigung | Reinigung | 85 |
| av_zuschnitt | Zuschnitt | 78 |
| av_rekonditionierung | Rekonditionierung | 74 |
| av_qualitaetssicherung | Qualitaetssicherung | 47 |
| av_reparatur | Reparatur | 35 |
| av_holzaufbereitung | Holzaufbereitung | 23 |
| av_remanufacturing | Remanufacturing | 8 |
| av_leuchten_refurbishment | Leuchten_Refurbishment | 5 |
| av_entmoertelung_von_fliesen | Entmoertelung_von_Fliesen | 4 |
| av_verstaerkung | Verstaerkung | 4 |
| av_drahtglasschneiden | Drahtglasschneiden | 0 |

## Same-name duplicates

None.

## Orphan check

| label | id | note |
| --- | --- | --- |
| Methode | meth_abrissmonitoring | seed — keep |
| Aufbereitungsverfahren | av_drahtglasschneiden | seed — specialty wire-glass cutting; keep |

## Candidate patch

`patches/controlled_vocabulary_methode_rueckbau.patch.jsonl` — 1 `noop_reviewed`.

## Human decision queue

None.

## Acceptance status

- Live DB reachable: yes (`mit-bestand`).
- Active patch is UTF-8 LF, dry-run safe.
- No deferred ops.
