# Post Quality Pass P6-02 — Superuse/ZRS/HarvestMAP team edges

**Date:** 2026-06-06 · **Database:** `mit-bestand`
**Ledger:** [`ledger/post_quality_p06_02.csv`](../ledger/post_quality_p06_02.csv)
**Patch:** [`patches/post_quality_p06_02.patch.jsonl`](../patches/post_quality_p06_02.patch.jsonl)
**Apply report:** [`apply_reports/post_quality_p06_02.patch.apply_report.md`](../apply_reports/post_quality_p06_02.patch.apply_report.md)
**Apply:** applied

## Scope

Deferred from Q05 Scope A: **9** `MISSING_EVIDENCE` `VERBUNDEN_MIT_AKTEUR` edges (Superuse Studios team, ZRS Ingenieure team, HarvestMAP/re:store operator links) that Q05 escalated because the strict two-endpoint web gate failed on generic firm pages.

| cluster | edges | prior Q05 action |
|---|---:|---|
| ZRS Ingenieure team | 4 | ESCALATE_HUMAN (2) + ADD_SOURCE (2) |
| Superuse Studios team | 3 | ESCALATE_HUMAN |
| HarvestMAP / re:store | 2 | ESCALATE_HUMAN + ADD_SOURCE |

Excluded from this pass: `Q05-EP09-r-0040` (`re_store_harvestmap_vienna` → `peter_kneidinger`, prior PARTIAL).

## Method

1. Strict web gate: **PROVEN** only when a fetched page names **both** person and organisation endpoints verbatim.
2. Sources used: ZRS contact/imprint, Superuse project credits, Abitare Harvest Map article, restore.or.at impressum. LinkedIn not needed — first-party pages sufficed.
3. No deletes: all 9 edges corroborated; patch adds `evidence_url`, `evidence_quote`, `evidence_confidence=belegt`, `connection_kind`, `review_run`.
4. Bonus: `zrs_ingenieure` node received `primary_source_url` + `source_urls` (was null).

## Verdict counts

| verdict | before | after |
|---|---:|---:|
| MISSING_EVIDENCE | 9 | 0 |
| PROVEN | 0 | 9 |

## Apply summary

| metric | value |
|---|---:|
| patch ops | 10 (9 rel + 1 node) |
| load errors | 0 |
| rel updates | 9 |
| node updates | 1 |
| rel deletes | 0 |
| graph count delta | 2264 nodes / 15063 rels (unchanged) |

## Upgraded edges

| claim_id | from | to | source | connection_kind |
|---|---|---|---|---|
| Q05-EP09-r-0032 | andrea_kessler | re_store_harvestmap_vienna | restore.or.at/impressum | geschaeftsfuehrung |
| Q05-EP09-r-0033 | andrea_klinge | zrs_ingenieure | zrs.berlin/en/contact | geschaeftsfuehrung |
| Q05-EP09-r-0034 | cesare_peeren | superuse_studios_2012architecten | abitare.it Harvest Map article | team_affiliation |
| Q05-EP09-r-0035 | christof_ziegert | zrs_ingenieure | zrs.berlin/en/contact | geschaeftsfuehrung |
| Q05-EP09-r-0036 | eike_roswag_klinge | zrs_ingenieure | zrs.berlin/en/contact | geschaeftsfuehrung |
| Q05-EP09-r-0037 | jan_jongert | superuse_studios_2012architecten | superuse-studios.com/projectplus/villa-welpeloo | design_team |
| Q05-EP09-r-0038 | jeroen_bergsma | superuse_studios_2012architecten | superuse-studios.com/projectplus/villa-welpeloo | design_team |
| Q05-EP09-r-0039 | materialnomaden | re_store_harvestmap_vienna | restore.or.at/impressum | platform_operator |
| Q05-EP09-r-0041 | uwe_seiler | zrs_ingenieure | zrs.berlin/en/contact | geschaeftsfuehrung |

## Neo4j verification (read-cypher)

Targeted check on all 9 edges: **9/9** carry `evidence_confidence=belegt`, non-null `evidence_url`, and `review_run=post_quality_p06_02_2026_06_06`.

## Apply log

```bash
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_full_graph_verification/patches/post_quality_p06_02.patch.jsonl --database mit-bestand
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_full_graph_verification/patches/post_quality_p06_02.patch.jsonl --database mit-bestand --confirm "APPLY post_quality_p06_02.patch.jsonl TO mit-bestand"
```

Dry-run: 9 `would_update_rel` + 1 `would_update`, 0 errors. Live apply: 9 rel property updates + 1 node update, graph counts unchanged.
