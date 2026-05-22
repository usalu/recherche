# Netherlands reuse bubble — apply summary

**Date:** 2026-06-06  
**Database:** `mit-bestand`  
**Review run:** `netherlands_reuse_bubble_2026_06_05`

## Result: applied successfully

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Nodes | 2 412 | 2 432 | **+20** |
| Relationships | 15 583 | 15 622 | **+39** |

## Phases

| Phase | New nodes | New rels | Notes |
|---|---:|---:|---|
| 0 — sources + dossier | 19 | 0 | 1 dossier + 18 `ExternalLink` quellen |
| 1 — Dutch urban-mining spine | 0 | 29 | superuse ↔ new_horizon ↔ insert ↔ madaster mesh |
| 2 — Repurpose / Madopt layer | 1 (`repurpose`) | 10 | demand-driven marketplace actor |
| **Total** | **20** | **39** | no duplicate Superuse/New Horizon nodes |

## Connectivity targets (post-apply)

| Test | Before | After | Target |
|---|---|---|---|
| `superuse_studios_2012architecten` spine | 0 | **4** | ≥4 |
| `new_horizon_urban_mining` spine | 0 | **5** | ≥4 |
| `madaster` Dutch mesh (excl. concular) | 0 | **5** | ≥4 |
| `insert_marketplace` spine | 0 | **4** | ≥3 |
| `superuse` ↔ `new_horizon` (Oogstkaart) | 0 | **linked** | yes |
| `repurpose` spine | — | **4** | ≥4 |
| Evidence-tagged rels (`review_run`) | 0 | **39** | — |

## Enriched actors (no duplicates)

- `superuse_studios_2012architecten` — harvest method + Oogstkaart lineage
- `new_horizon_urban_mining` — urban mining, donor buildings, Oogst Collectief
- `madaster` — NL passport origin + Circl case BELEGT_IN
- `insert_marketplace` — national circular marketplace
- `city_of_utrecht` — Dutch policy mesh (existing PREUSE/FCRBE spine unchanged)

## New entity

- `repurpose` (`:Akteur`) — Repurpose BV / Madopt operator

## Still deferred (sidecar)

See [`DEFERRED_NO_EVIDENCE.md`](DEFERRED_NO_EVIDENCE.md): `new_horizon` stub, demonstrator projects, Cirkelstad/CB'23 as nodes.

## Reports

- [`apply_summary.json`](apply_summary.json)
- [`connectivity_report.json`](connectivity_report.json)
- Plan: [`INTEGRATION_PLAN.md`](INTEGRATION_PLAN.md)
- Tests: [`CONNECTIVITY_TESTS.cypher`](CONNECTIVITY_TESTS.cypher)

## Re-run

```bash
python _neo4j/intake/runs/2026-06-05_netherlands_reuse_bubble/apply_netherlands_reuse_bubble.py
python _neo4j/intake/runs/2026-06-05_netherlands_reuse_bubble/apply_netherlands_reuse_bubble.py --commit
```
