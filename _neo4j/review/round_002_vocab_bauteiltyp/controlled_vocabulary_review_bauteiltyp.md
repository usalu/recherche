# Round 002 Controlled Vocabulary Review: Bauteiltyp + Bauteilebene

**Generated:** 2026-05-15
**Baseline reference:** [`../round_002_baseline/global_audit_report.md`](../round_002_baseline/global_audit_report.md)

## Result in Context

Both families are clean. The live `mit-bestand` graph has exactly the 15
canonical `Bauteiltyp` nodes the schema targets and 6 `Bauteilebene` nodes,
all well-populated, with no same-name duplicates and no orphans.

No structural patch operations are needed for this family.

## Bauteiltyp hub snapshot (live `mit-bestand`)

| id | name | Bauteilgruppen (inbound) |
| --- | --- | ---: |
| bt_fassade | Fassade | 80 |
| bt_wand | Wand | 75 |
| bt_traeger | Traeger | 57 |
| bt_decke | Decke | 50 |
| bt_ausbau | Ausbau | 45 |
| bt_boden | Boden | 44 |
| bt_stuetze | Stuetze | 39 |
| bt_technik | Technik | 38 |
| bt_fenster | Fenster | 29 |
| bt_dach | Dach | 22 |
| bt_tuer | Tuer | 19 |
| bt_daemmung | Daemmung | 14 |
| bt_gelaender | Gelaender | 13 |
| bt_treppe | Treppe | 12 |
| bt_fundament | Fundament | 8 |

15 canonical types — matches schema target exactly.

## Bauteilebene hub snapshot (live `mit-bestand`)

| id | name | Bauteilgruppen (inbound) |
| --- | --- | ---: |
| be_bauteilgruppe | Bauteilgruppe | 246 |
| be_system | System | 21 |
| be_oberflaechenschicht | Oberflaechenschicht | 6 |
| be_einzelbauteil | Einzelbauteil | 2 |
| be_gebaeudeteil | Gebaeudeteil | 1 |
| be_materialcharge | Materialcharge | 1 |

Granularity ladder is intentional and matches the schema.

## Same-name duplicates

None.

## Orphan check

None. Every `Bauteiltyp` and `Bauteilebene` node has at least one inbound
`HAT_BAUTEILTYP` / `HAT_BAUTEILEBENE` link.

## Hierarchy check

`Bauteilebene` has no parent label in the current schema. `Bauteiltyp`
likewise has no parent label. No `HAT_*KATEGORIE` parent to verify.

## Candidate patch

`patches/controlled_vocabulary_bauteiltyp.patch.jsonl` — 2 `noop_reviewed`
operations to record that the families were inspected and accepted.

## Human decision queue

None.

## Acceptance status

- Live DB reachable: yes (`mit-bestand`).
- Active patch is UTF-8 LF, dry-run safe.
- No deferred ops.
