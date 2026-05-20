# patches/batch2/ — batch2 v2 (2026-05-20) apply units

50 JSONL patches applied to the `mit-bestand` Neo4j database during the multi-phase batch2 v2 import.

## Order of application

The full apply order is documented in [`../../../../intake/runs/2026-05-20_inbox_batch2_import/APPLY_ORDER.md`](../../../../intake/runs/2026-05-20_inbox_batch2_import/APPLY_ORDER.md).

Each `phase_batch2_v2_N_*.patch.jsonl` has matching apply reports at:

- `../../apply_reports/phase_batch2_v2_N_*.patch.apply_report.json`
- `../../apply_reports/phase_batch2_v2_N_*.patch.apply_report.md`

## Rollback

See [`../../rollback.md` §Phase batch2 v2](../../rollback.md) for the combined-effect ledger and rollback procedure.

The pre-apply full graph backup is at `_neo4j/review/backups/batch2_v2_pre_apply/` (still valid).

## DO NOT MOVE THESE FILES

They are referenced by name from:

- `_neo4j/review/round_002_followup/rollback.md`
- `_neo4j/intake/runs/2026-05-20_inbox_batch2_import/HANDOFF.md`
- `_neo4j/intake/runs/2026-05-20_inbox_batch2_import/APPLY_ORDER.md`
- The orchestrator script `_scripts/_apply_batch2_v2_all.py`

Renaming or moving them would invalidate the apply trail.

## Generators

Most of these patches were produced by one-shot generator scripts. The generators live in `_scripts/batch2_v2_generators/` — see that folder's README for the script → patch mapping. The patches in this folder are the byte-frozen output that was actually applied; they take precedence over anything the generators would produce on re-run.
