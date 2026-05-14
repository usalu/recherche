# Round 001 Apply Test Summary

Live apply performed: no. The live database remains protected; mutation requires the exact confirmation phrase.

Required phrase for blocker apply: `APPLY accepted_blockers.patch.jsonl TO mit-bestand`

## Dry-run Results

| Patch | Records | Would create | Would update | Noop same | Load errors |
| --- | ---: | ---: | ---: | ---: | ---: |
| accepted_blockers | 2 | 2 | 0 | 0 | 0 |
| global_technical | 27 | 2 | 11 | 14 | 0 |
| canonicalization_candidates | 25 | 0 | 11 | 14 | 0 |

## Staging Overlay Audit

- | missing_endpoints | 0 |
- Overlay uses accepted_blockers.patch.jsonl; no batch export files were overwritten.

## Review Queues

- `needs_review.patch.jsonl`: 25 canonicalization candidates.
- `rejected.patch.jsonl`: 0 records.
