# Patch Apply Report: phase_batch2_v2_4e_refair_strip.patch.jsonl

Generated: 2026-05-20T07:44:11.473539+00:00
Mode: dry-run
Database: mit-bestand

## Summary

| Metric | Value |
| --- | --- |
| records | 8 |
| load_errors | 0 |
| missing_endpoint | 3 |
| would_delete_rel | 5 |

## Counts

| State | Nodes | Relationships |
| --- | --- | --- |
| before | 2298 | 17035 |
| after_expected | 2298 | 17030 |

## Rejected / Needs Review

| Line | Op | Id | Status | Error |
| --- | --- | --- | --- | --- |
| 6 | add_rel |  | missing_endpoint | to node 'la_fabrique_de_bordeaux_metropole' not found |
| 7 | add_rel |  | missing_endpoint | to node 'la_fabrique_de_bordeaux_metropole' not found |
| 8 | add_rel |  | missing_endpoint | from node 'la_fabrique_de_bordeaux_metropole' not found |
