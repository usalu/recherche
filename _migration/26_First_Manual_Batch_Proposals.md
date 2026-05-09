# Phase 26 First Manual Batch Proposals

## Scope

Proposal-only pass for the five highest-impact review targets. No nodes or edges were migrated.

## Output

- _migration/26_first_manual_batch_edge_proposals.csv

## Counts

- Proposed edge decisions: 154
- High-confidence-if-source-clear proposals: 16
- Still review-required proposals: 138

## By Target

| target | rows |
|---|---:|
| material/Metall | 46 |
| huerde/Performance_Nachweis | 33 |
| bauteiltyp/Tragstruktur | 28 |
| bauteiltyp/Bauwerksteil | 27 |
| huerde/Logistikproblem | 20 |

## By Proposed Action

| action | rows |
|---|---:|
| keep_review | 87 |
| approve_move | 44 |
| delete_or_object_relation | 10 |
| approve_split | 9 |
| create_or_review | 4 |

## How To Use

1. Open the CSV.
2. Filter by proposal_confidence = CONFIDENT_IF_SOURCE_CLEAR first.
3. Check the source file before approving.
4. Keep anything mixed, broad, or uncertain in review.

## Important

These are not automatic migration rules. They are a review aid.
