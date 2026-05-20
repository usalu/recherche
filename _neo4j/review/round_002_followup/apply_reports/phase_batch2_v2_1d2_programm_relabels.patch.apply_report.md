# Patch Apply Report: phase_batch2_v2_1d2_programm_relabels.patch.jsonl

Generated: 2026-05-20T01:29:46.288130+00:00
Mode: dry-run
Database: mit-bestand

## Summary

| Metric | Value |
| --- | --- |
| records | 6 |
| load_errors | 0 |
| missing_node | 3 |
| would_create | 3 |

## Counts

| State | Nodes | Relationships |
| --- | --- | --- |
| before | 2298 | 17035 |
| after_expected | 2301 | 17035 |

## Rejected / Needs Review

| Line | Op | Id | Status | Error |
| --- | --- | --- | --- | --- |
| 2 | merge_node |  | missing_node | merge target 'prog_stuttgart_210' not found |
| 4 | merge_node |  | missing_node | merge target 'prog_rebridge' not found |
| 6 | merge_node |  | missing_node | merge target 'prog_re_use_hoefe' not found |
