# Round 002 Controlled Vocabulary Review: Status + WiederverwendungsArt

**Generated:** 2026-05-15
**Baseline reference:** [`../round_002_baseline/global_audit_report.md`](../round_002_baseline/global_audit_report.md)

## Result in Context

Mostly clean: 12 `Status` nodes, 11 `WiederverwendungsArt` nodes, no same-name
duplicates, no orphans. **One concept-duplicate** in `Status`:
`status_prototyp` (6 inbound) and `status_prototypisch` (3 inbound) carry
the same meaning ("prototype") with slightly different German morphology
(noun vs adjective). Merge candidate.

`WiederverwendungsArt` is internally consistent and covers the reuse-type
ladder cleanly.

## Status hub snapshot (live `mit-bestand`)

| id | name | inbound | classification |
| --- | --- | ---: | --- |
| status_gebaut | Gebaut | 185 | canonical |
| status_realisiert | Realisiert | 35 | canonical |
| status_unklar | Unklar | 14 | canonical |
| status_geplant | Geplant | 9 | canonical |
| status_rueckgebaut | Rueckgebaut | 9 | canonical |
| status_in_bau | In_Bau | 8 | canonical |
| status_prototyp | Prototyp | 6 | canonical |
| status_temporaer | Temporaer | 5 | canonical |
| status_prototypisch | Prototypisch | 3 | **merge** → `status_prototyp` |
| status_verworfen | Verworfen | 3 | canonical |
| status_vorgeschlagen | Vorgeschlagen | 3 | canonical |
| status_wettbewerb | Wettbewerb | 1 | canonical |

## WiederverwendungsArt hub snapshot (live `mit-bestand`)

| id | name | inbound |
| --- | --- | ---: |
| wva_direkte_wiederverwendung | Direkte_Wiederverwendung | 316 |
| wva_upcycling | Upcycling | 51 |
| wva_bestandserhalt | Bestandserhalt | 37 |
| wva_same_site_reuse | Same_Site_ReUse | 28 |
| wva_refurbishment | Refurbishment | 25 |
| wva_adaptives_reuse | Adaptives_ReUse | 23 |
| wva_urban_mining | Urban_Mining | 23 |
| wva_design_for_disassembly | Design_for_Disassembly | 22 |
| wva_recycling | Recycling | 17 |
| wva_remanufacturing | Remanufacturing | 10 |
| wva_weiterbauen_im_bestand | Weiterbauen_im_Bestand | 6 |

## Same-name duplicates / orphans

None / none.

## Candidate patch

`patches/controlled_vocabulary_status_wva.patch.jsonl` — 1 merge:

| op | from | to | severity |
| --- | --- | --- | --- |
| merge_node | status_prototypisch | status_prototyp | LOW |

The noun form `Prototyp` is the canonical, with `Prototypisch` preserved
as an alias on the survivor.

## Human decision queue

None.

## Acceptance status

- Live DB reachable: yes (`mit-bestand`).
- Active patch is UTF-8 LF, dry-run safe (`merge_node` supported by runner).
- No deferred ops.
