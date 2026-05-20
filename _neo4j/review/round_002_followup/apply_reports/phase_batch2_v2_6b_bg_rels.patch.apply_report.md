# Patch Apply Report: phase_batch2_v2_6b_bg_rels.patch.jsonl

Generated: 2026-05-20T08:18:29.031345+00:00
Mode: dry-run
Database: mit-bestand

## Summary

| Metric | Value |
| --- | --- |
| records | 384 |
| load_errors | 0 |
| missing_endpoint | 4 |
| would_create_rel | 380 |

## Counts

| State | Nodes | Relationships |
| --- | --- | --- |
| before | 2426 | 17238 |
| after_expected | 2426 | 17618 |

## Rejected / Needs Review

| Line | Op | Id | Status | Error |
| --- | --- | --- | --- | --- |
| 280 | add_rel |  | missing_endpoint | to node 'mg_mehrere' not found |
| 345 | add_rel |  | missing_endpoint | to node 'bt_mehrere' not found |
| 355 | add_rel |  | missing_endpoint | to node 'mg_mehrere' not found |
| 373 | add_rel |  | missing_endpoint | to node 'mg_mehrere' not found |
