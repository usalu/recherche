# Patch Apply Report: phase_batch2_v2_9_bridges.patch.jsonl

Generated: 2026-05-20T07:27:21.848923+00:00
Mode: dry-run
Database: mit-bestand

## Summary

| Metric | Value |
| --- | --- |
| records | 23 |
| load_errors | 0 |
| missing_endpoint | 9 |
| would_create_rel | 14 |

## Counts

| State | Nodes | Relationships |
| --- | --- | --- |
| before | 2298 | 17035 |
| after_expected | 2298 | 17049 |

## Rejected / Needs Review

| Line | Op | Id | Status | Error |
| --- | --- | --- | --- | --- |
| 6 | add_rel |  | missing_endpoint | from node 'tu_delft' not found |
| 7 | add_rel |  | missing_endpoint | from node 'tu_delft' not found |
| 12 | add_rel |  | missing_endpoint | to node 'tool_rcmi' not found |
| 13 | add_rel |  | missing_endpoint | from node 'la_fabrique_de_bordeaux_metropole' not found |
| 14 | add_rel |  | missing_endpoint | to node 'software_opalis' not found |
| 15 | add_rel |  | missing_endpoint | to node 'prog_urban_bricolage' not found |
| 21 | add_rel |  | missing_endpoint | to node 'prog_mas_dfab' not found |
| 22 | add_rel |  | missing_endpoint | to node 'prog_mas_dfab' not found |
| 23 | add_rel |  | missing_endpoint | to node 'prog_mas_dfab' not found |
