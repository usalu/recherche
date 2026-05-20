# Patch Apply Report: phase_batch2_v2_4d_rcmi_strip.patch.jsonl

Generated: 2026-05-20T07:44:08.782748+00:00
Mode: dry-run
Database: mit-bestand

## Summary

| Metric | Value |
| --- | --- |
| records | 5 |
| load_errors | 0 |
| missing_endpoint | 1 |
| would_create_rel | 1 |
| would_delete_rel | 3 |

## Counts

| State | Nodes | Relationships |
| --- | --- | --- |
| before | 2298 | 17035 |
| after_expected | 2298 | 17033 |

## Rejected / Needs Review

| Line | Op | Id | Status | Error |
| --- | --- | --- | --- | --- |
| 4 | add_rel |  | missing_endpoint | to node 'tool_rcmi' not found |
