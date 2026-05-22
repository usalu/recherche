# Agent G1 — Git Provenance Audit (MISSING_EVIDENCE)

**Date:** 2026-06-06  
**Source ledger:** `VERIFICATION_LEDGER_ELEMENT.csv`  
**Filter:** `verdict=MISSING_EVIDENCE`  
**Rows audited:** 877  
**Clusters:** 12 (by `claim_kind`, `rel_type_or_label`, `intake_run`, `review_run`)  
**Mode:** read-only git + repo + Neo4j read-cypher; no graph mutation  

## Root-cause buckets

| Bucket | Rows | Share | Meaning |
|---|---:|---:|---|
| `intake_script` | 48 | 5.5% | Element first introduced by an intake-run apply/import script without attaching evidence URLs. |
| `aggregate_stub` | 118 | 13.5% | Placeholder or aggregate node (Unbekannt/Aggregiert/cluster/miscast) — not a discrete sourced entity. |
| `never_sourced_import` | 688 | 78.4% | Imported from processed JSONL / legacy actor mesh / early graph batch; never carried `source_urls` or `evidence_url`. |
| `post_merge_orphan` | 23 | 2.6% | Survivor of merge, redirect synthesis (F09/P6), or edge purge that left provenance gap. |

## Cluster highlights (top 15 by row count)

| cluster | label | intake_run | review_run | rows | bucket | first git |
|---|---|---|---|---:|---|---|
| G01-C001 | Akteur | (null) | (null) | 435 | `never_sourced_import` (never_sourced_import:425;aggregate_stub:8;post_merge_orphan:2) | 2026-05-13 `152221403f24` |
| G01-C002 | VERBUNDEN_MIT_AKTEUR | (null) | (null) | 181 | `never_sourced_import` (never_sourced_import:167;post_merge_orphan:14) | 2026-05-23 `bd62286a9257` |
| G01-C003 | Bauwerk | (null) | (null) | 105 | `aggregate_stub` (aggregate_stub:105) | 2026-05-15 `d0ded72f31bf` |
| G01-C004 | BETEILIGT_AN | (null) | (null) | 51 | `never_sourced_import` (never_sourced_import:50;post_merge_orphan:1) | 2026-05-23 `bd62286a9257` |
| G01-C005 | NUTZT_SOFTWARE | (null) | (null) | 40 | `intake_script` (intake_script:37;post_merge_orphan:3) | 2026-05-20 `b32d72223534` |
| G01-C006 | Projekt | (null) | (null) | 20 | `never_sourced_import` (never_sourced_import:20) | 2026-05-14 `e70caed3fbcb` |
| G01-C007 | Programm | (null) | (null) | 13 | `never_sourced_import` (never_sourced_import:13) | 2026-05-16 `cafd4015e358` |
| G01-C008 | TEIL_VON_PROGRAMM | (null) | (null) | 12 | `intake_script` (intake_script:11;post_merge_orphan:1) | 2026-05-20 `3f004245ddea` |
| G01-C009 | Software | (null) | (null) | 11 | `never_sourced_import` (never_sourced_import:10;post_merge_orphan:1) | 2026-05-13 `152221403f24` |
| G01-C010 | Materialdepot | (null) | (null) | 5 | `aggregate_stub` (aggregate_stub:5) | 2026-05-15 `d0ded72f31bf` |
| G01-C011 | ERHALT_FOERDERUNG_DURCH | (null) | (null) | 3 | `never_sourced_import` (never_sourced_import:3) | 2026-05-16 `bd377b8a16d4` |
| G01-C012 | VERBUNDEN_MIT_AKTEUR | (null) | remediation_wave2_r04_2026_06_06 | 1 | `post_merge_orphan` (post_merge_orphan:1) | 2026-05-23 `bd62286a9257` |

## Findings

1. **Actor long tail (435 rows, G01-C001):** 425× `never_sourced_import`, 8× `aggregate_stub` (cluster/miscast names), 2× `post_merge_orphan` (F09 ledger rows). All have `intake_run=null`. Earliest git intro: **2026-05-13** `152221403f24` *migration ready* → `_neo4j/archieve/neo4j_batch01_first5_package/`. Repo walk first hit: `intake/runs/2026-05-20_radical_quality_reset/snapshot/nodes.jsonl`. Pre-dates the June 2026 evidence-on-properties contract.
2. **VMA mesh (182 rows, G01-C002 + C012):** 167 unsourced `VERBUNDEN_MIT_AKTEUR` edges with `review_run=null`; 14 F09 ledger-synthesis rows; 1 edge tagged `remediation_wave2_r04_2026_06_06` but still missing `evidence_url`. First git: **2026-05-23** `bd62286a9257` *source check 4*; repo hit in `trace_zitiert_quelle_to_urls/logs/information_source_url_ledger.jsonl` — structural actor mesh imported without edge evidence.
3. **Donor Bauwerk stubs (105 rows, G01-C003):** 100% `aggregate_stub`. `bw_*_donor` nodes from **2026-05-15** batch_015 project import (`d0ded72f`); geo coordinates attached via placeholder `processed/archive` sources, not fetchable URLs.
4. **Project participation edges (51 rows, G01-C004):** 50× `never_sourced_import` `BETEILIGT_AN` rels — project→actor links from early batch imports without `evidence_url`.
5. **Reuse→software edges (40 rows, G01-C005):** 37× `intake_script` — `NUTZT_SOFTWARE` rels minted in `radical_quality_reset/snapshot/relationships.jsonl` (**2026-05-20** `b32d7222`) without sourcing pass.
6. **Program/software vocabulary (36 rows, G01-C007–C009, C011):** `Programm`/`Software` nodes and funding edges from **2026-05-14–16** inbox_batch2 / Phase C imports; real entities but never given `source_urls` on import.
7. **F09 ledger debt (23 rows total):** `agent_id=F09` rows are **ledger coverage artifacts** only (`Synthesized by F09 for uncovered live element`); graph elements pre-existed. Bucket `post_merge_orphan` — not new graph defects.
8. **Materialdepot (5 rows, G01-C010):** Real stockholder sites identified by Agent 10 but graph nodes lack `source_urls`; first in batch_015 chains (**2026-05-15**). Classified `aggregate_stub` because depot nodes are project-derived abstractions, not independently sourced entities.

## Method

- Filtered `VERIFICATION_LEDGER_ELEMENT.csv` for `verdict=MISSING_EVIDENCE`.
- Enriched each row with live `intake_run` / `review_run` / `source_scope` from Neo4j (`mit-bestand`).
- Clustered on `(claim_kind, rel_type_or_label, intake_run, review_run)`.
- Per cluster: repo walk first hit in `intake/runs/`, `processed/`, `review/`; `git log -S <sample_id> --reverse` under `_neo4j/`.
- Per-row bucket assigned then cluster `root_cause_bucket` = majority vote (`bucket_breakdown` column).
- Bucket assigned from path patterns, agent notes, and naming heuristics.

**Output:** [`ledger/provenance_g01.csv`](../ledger/provenance_g01.csv) (12 cluster rows).
