# Round 002 Controlled Vocabulary Review: Bauobjektrolle + Bauobjektklasse

**Generated:** 2026-05-15
**Baseline reference:** [`../round_002_baseline/global_audit_report.md`](../round_002_baseline/global_audit_report.md)

## Result in Context

Clean family. 6 `Bauobjektrolle` and 8 `Bauobjektklasse` nodes, all
populated with at least 1 inbound link, no same-name duplicates, no orphans.

No structural patch operations are needed.

## Bauobjektrolle hub snapshot (live `mit-bestand`)

| id | name | Bauwerk inbound |
| --- | --- | ---: |
| bor_donorobjekt | Donorobjekt | 99 |
| bor_empfaengerobjekt | Empfaengerobjekt | 68 |
| bor_bestandsobjekt | Bestandsobjekt | 22 |
| bor_same_site_donor_receiver | Same_Site_Donor_Receiver | 18 |
| bor_zwischenlager | Zwischenlager | 9 |
| bor_referenzobjekt | Referenzobjekt | 1 |

## Bauobjektklasse hub snapshot (live `mit-bestand`)

| id | name | Bauwerk inbound |
| --- | --- | ---: |
| bok_gebaeude | Gebaeude | 153 |
| bok_infrastruktur | Infrastruktur | 18 |
| bok_depot_lager | Depot_Lager | 15 |
| bok_pavillon | Pavillon | 11 |
| bok_gebaeudeteil | Gebaeudeteil | 8 |
| bok_innenausbau | Innenausbau | 5 |
| bok_quartier_areal | Quartier_Areal | 3 |
| bok_reuse_centre | Reuse_Centre | 1 |

## Same-name duplicates / orphans

None / none.

## Candidate patch

`patches/controlled_vocabulary_bauobjekt.patch.jsonl` — 1 `noop_reviewed`.

## Human decision queue

None.

## Acceptance status

- Live DB reachable: yes (`mit-bestand`).
- Active patch is UTF-8 LF, dry-run safe.
- No deferred ops.
