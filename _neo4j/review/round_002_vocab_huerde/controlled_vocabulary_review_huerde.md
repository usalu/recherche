# Round 002 Controlled Vocabulary Review: Huerde + HuerdeKategorie

**Generated:** 2026-05-15
**Baseline reference:** [`../round_002_baseline/global_audit_report.md`](../round_002_baseline/global_audit_report.md)

## Result in Context

Clean family. 28 `Huerde` nodes and 10 `HuerdeKategorie` parents, no
same-name duplicates, every `Huerde` carries its `HAT_HUERDEKATEGORIE`
parent link. One parent category (`hk_unklar`) is orphaned — no `Huerde`
nodes are categorized as "Unklar". Recommended to keep as seed entry.

## HuerdeKategorie hub snapshot (live `mit-bestand`)

| id | name | Huerde children (inbound) |
| --- | --- | ---: |
| hk_technisch | Technisch | 63 |
| hk_daten_evidenz | Daten_Evidenz | 35 |
| hk_rechtlich | Rechtlich | 27 |
| hk_logistisch | Logistisch | 13 |
| hk_umwelt_gesundheit | Umwelt_Gesundheit | 8 |
| hk_wirtschaftlich | Wirtschaftlich | 7 |
| hk_beschaffung_markt | Beschaffung_Markt | 4 |
| hk_planerisch | Planerisch | 3 |
| hk_sozial_organisatorisch | Sozial_Organisatorisch | 3 |
| **hk_unklar** | Unklar | **0** |

## Huerde hub snapshot (live `mit-bestand`)

Top 10 by inbound, the full 28 are listed below.

| id | name | inbound |
| --- | --- | ---: |
| h_technische_freigabe | Technische_Freigabe | 179 |
| h_datenluecke | Datenluecke | 132 |
| h_kompatibilitaetsproblem | Kompatibilitaetsproblem | 59 |
| h_materialqualitaet_unklar | Materialqualitaet_Unklar | 53 |
| h_anschlussproblem | Anschlussproblem | 46 |
| h_gewaehrleistung | Gewaehrleistung | 45 |
| h_witterung_feuchte | Witterung_Feuchte | 44 |
| h_brandschutzkonflikt | Brandschutzkonflikt | 41 |
| h_toleranzen | Toleranzen | 40 |
| h_verfuegbarkeitsproblem | Verfuegbarkeitsproblem | 34 |

Tail (inbound ≤ 13): `h_mengenunsicherheit (32)`,
`h_bruch_beschaedigungsrisiko (29)`, `h_heterogenitaet_chargen (27)`,
`h_hygieneanforderung (25)`, `h_aufbereitungsaufwand (24)`,
`h_zustand_unklar (23)`, `h_entwurfsbindung (22)`,
`h_dauerhaftigkeit_restlebensdauer (20)`,
`h_unkonventionelles_material (19)`, `h_fehlende_lagerflaeche (13)`,
`h_haftung (13)`, `h_terminunsicherheit (13)`, `h_bauproduktstatus (11)`,
`h_schadstoffbelastung (9)`, `h_akzeptanzproblem (7)`,
`h_fehlende_standardisierung (6)`, `h_ausschreibungsproblem (4)`,
`h_fehlende_datenstandards (4)`.

## Same-name duplicates

None.

## Missing-parent check

None. Every `Huerde` has `HAT_HUERDEKATEGORIE`.

## Orphan check

`hk_unklar` has 0 `Huerde` children. Kept as a deliberately reserved
fallback category; no patch action.

## Candidate patch

`patches/controlled_vocabulary_huerde.patch.jsonl` — 1 `noop_reviewed`
operation recording the inspection.

## Human decision queue

- **hk_unklar**: keep as reserved fallback (current state) or remove. No
  semantic pressure either way.

## Acceptance status

- Live DB reachable: yes (`mit-bestand`).
- Active patch is UTF-8 LF, dry-run safe.
- No deferred ops.
