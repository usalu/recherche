# Patch Apply Report: phase_batch2_v2_8_project_vocab.patch.jsonl

Generated: 2026-05-20T07:26:26.183943+00:00
Mode: dry-run
Database: mit-bestand

## Summary

| Metric | Value |
| --- | --- |
| records | 73 |
| load_errors | 0 |
| missing_endpoint | 18 |
| noop_existing_rel | 1 |
| would_create_rel | 54 |

## Counts

| State | Nodes | Relationships |
| --- | --- | --- |
| before | 2298 | 17035 |
| after_expected | 2298 | 17089 |

## Rejected / Needs Review

| Line | Op | Id | Status | Error |
| --- | --- | --- | --- | --- |
| 8 | add_rel |  | missing_endpoint | to node 'norm_sia_500' not found |
| 9 | add_rel |  | missing_endpoint | to node 'norm_sia_261' not found |
| 19 | add_rel |  | missing_endpoint | to node 'norm_sia_269' not found |
| 27 | add_rel |  | missing_endpoint | to node 'software_ecotool' not found |
| 29 | add_rel |  | missing_endpoint | to node 'zbs_ecotool' not found |
| 31 | add_rel |  | missing_endpoint | to node 'norm_sia_269' not found |
| 35 | add_rel |  | missing_endpoint | to node 'tool_retile' not found |
| 45 | add_rel |  | missing_endpoint | to node 'software_llmnt' not found |
| 53 | add_rel |  | missing_endpoint | to node 'norm_sia_269' not found |
| 65 | add_rel |  | missing_endpoint | from node 'p_jugendtreff_ingersheim' not found |
| 66 | add_rel |  | missing_endpoint | from node 'p_jugendtreff_ingersheim' not found |
| 67 | add_rel |  | missing_endpoint | from node 'p_jugendtreff_ingersheim' not found |
| 68 | add_rel |  | missing_endpoint | from node 'p_jugendtreff_ingersheim' not found |
| 69 | add_rel |  | missing_endpoint | from node 'p_jugendtreff_ingersheim' not found |
| 70 | add_rel |  | missing_endpoint | from node 'p_eggshell_pavilion' not found |
| 71 | add_rel |  | missing_endpoint | from node 'p_eggshell_pavilion' not found |
| 72 | add_rel |  | missing_endpoint | from node 'p_up_sticks_dundee' not found |
| 73 | add_rel |  | missing_endpoint | from node 'p_up_sticks_dundee' not found |
