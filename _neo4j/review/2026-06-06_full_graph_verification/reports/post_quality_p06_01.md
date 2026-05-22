# Post Quality Pass P6-01 — Q04 downgrade backlog apply

**Date:** 2026-06-06 · **Database:** `mit-bestand`
**Ledger:** [`ledger/post_quality_p06_01.csv`](../ledger/post_quality_p06_01.csv)
**Patch:** [`patches/quality_pass_q04_downgrades.patch.jsonl`](../patches/quality_pass_q04_downgrades.patch.jsonl)
**Apply report:** [`apply_reports/quality_pass_q04_downgrades.patch.apply_report.md`](../apply_reports/quality_pass_q04_downgrades.patch.apply_report.md)
**Apply:** applied

## Scope

Deferred from Q04 catalogue-edge pass: **13** residual PARTIAL rows where classification tokens appeared on the fetched page but the strict verbatim edge quote gate failed. Action: relabel `evidence_confidence` from `belegt` → `niedrig` (edges retained).

| rel type | count |
|---|---:|
| HAT_BAUTEILTYP | 12 |
| NUTZT_MATERIAL | 1 |

## Apply summary

| metric | value |
|---|---:|
| patch ops | 13 |
| load errors | 0 |
| rel updates | 13 |
| rel deletes | 0 |
| graph count delta | 2264 nodes / 15063 rels (unchanged) |

## Downgraded edges

| claim_id | from | to | rel type | notes |
|---|---|---|---|---|
| Q04-0002 | articonnex | bt_daemmung | HAT_BAUTEILTYP | classification present (isolant, laine); no strict quote |
| Q04-0004 | articonnex | bt_traeger | HAT_BAUTEILTYP | classification present (poutre); no strict quote |
| Q04-0021 | bauteilboerse_bremen | bt_gelaender | HAT_BAUTEILTYP | weak residual; actor hits only |
| Q04-0022 | bauteilboerse_bremen | bt_technik | HAT_BAUTEILTYP | weak residual; actor hits only |
| Q04-0023 | bauteilnetz_deutschland | bt_technik | HAT_BAUTEILTYP | weak residual; actor hits only |
| Q04-0024 | bauteilnetz_deutschland | bt_tuer | HAT_BAUTEILTYP | weak residual; actor hits only |
| Q04-0044 | genbyg | bt_ausbau | HAT_BAUTEILTYP | weak residual; actor hits only |
| Q04-0065 | r_place | bt_decke | HAT_BAUTEILTYP | classification present (plafond, dalles); no strict quote |
| Q04-0066 | r_place | bt_wand | HAT_BAUTEILTYP | classification present (cloison, cloisons); no strict quote |
| Q04-0081 | useagain_bauteilclick | bt_dach | HAT_BAUTEILTYP | classification present (dach); no strict quote |
| Q04-0082 | useagain_bauteilclick | bt_daemmung | HAT_BAUTEILTYP | classification present (dammung); no strict quote |
| Q04-0085 | useagain_bauteilclick | bt_wand | HAT_BAUTEILTYP | classification present (wand); no strict quote |
| Q04-0086 | articonnex | mat_daemmstoff | NUTZT_MATERIAL | classification present (isolant); no strict quote |

## Neo4j verification (read-cypher)

Targeted check on all 13 patch endpoints: **13/13** carry `evidence_confidence=niedrig` and `review_run=quality_pass_q04_2026_06_06`.

Q04-tagged rel confidence distribution after apply:

| evidence_confidence | count |
|---|---:|
| belegt | 26 |
| niedrig | 13 |

No `belegt` values remain on the downgraded edge set.

## Apply log

```bash
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_full_graph_verification/patches/quality_pass_q04_downgrades.patch.jsonl --database mit-bestand
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_full_graph_verification/patches/quality_pass_q04_downgrades.patch.jsonl --database mit-bestand --confirm "APPLY quality_pass_q04_downgrades.patch.jsonl TO mit-bestand"
```

Dry-run: 13 `would_update_rel`, 0 errors. Live apply: 13 rel property updates, graph counts unchanged.
