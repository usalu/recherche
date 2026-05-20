"""Apply all batch2 v2 patches in sequence with the correct confirm phrase per file.

Stops on first error. Records the result of each patch.

Usage:
  python _scripts/_apply_batch2_v2_all.py --start 1 --end 36
  python _scripts/_apply_batch2_v2_all.py --start 1 --end 7   # Stage 1 only
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PATCH_DIR = Path('e:/recherche/_neo4j/review/round_002_followup/patches/batch2')

# Per APPLY_ORDER.md
SEQUENCE = [
    ('phase_batch2_v2_1a_deletes.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_1a2_delete_obk27.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_1b_akteur_merges.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_1c_circl_merge.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_1d_programm_merges.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_1d2a_programm_adds.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_1d2b_programm_merges.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_2_shared_nodes.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_2b_bauwerks.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_2c_bauwerk_rels.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_3a_quellen_case.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_3b_belegt_in_edges.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_4a_projekt_promote.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_4b_projekt_rels.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_5a_new_akteure.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_5b_akteur_typed_rels.patch.jsonl', 'jsonl'),
    # Phase 5c GEHÖRT_ZU template — superseded by Phase 15; skip if Phase 15 will run.
    ('phase_batch2_v2_6a_bg_addnodes.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_6b_bg_rels.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_7a_ketten_addnodes.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_7b_kette_rels.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_8_project_vocab.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_9_bridges.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_4c_eth_merge.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_4d_rcmi_strip.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_4d2_rcmi_delete.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_4e_refair_strip.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_4e2_refair_delete.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_10_huerde_wirtschaft.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_11_bg_vocab.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_12a_deferred_bg_addnodes.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_12b_deferred_bg_rels.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_13a_more_actors_addnodes.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_13b_more_actors_rels.patch.jsonl', 'jsonl'),
    ('phase_batch2_v2_14_external_quellen.patch.jsonl', 'jsonl'),
    # Phase 15 GEHÖRT_ZU Cypher runs at the end via direct cypher (different mechanism)
]


def run_jsonl_patch(filename: str) -> tuple[int, str]:
    """Apply one JSONL patch with the correct confirm phrase."""
    confirm = f'APPLY {filename} TO mit-bestand'
    path = PATCH_DIR / filename
    cmd = [
        sys.executable, '_scripts/apply_neo4j_review_patch.py',
        '--patch', str(path),
        '--confirm', confirm,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = (proc.stdout or '') + (proc.stderr or '')
    return proc.returncode, out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--start', type=int, default=1, help='1-based index of first patch to apply')
    ap.add_argument('--end', type=int, default=len(SEQUENCE), help='1-based index of last patch (inclusive)')
    ap.add_argument('--dry-run', action='store_true', help='Print commands without executing')
    args = ap.parse_args()

    total = len(SEQUENCE)
    start = max(1, args.start)
    end = min(total, args.end)

    log_path = Path('e:/recherche/_neo4j/intake/runs/2026-05-20_inbox_batch2_import/apply_log.jsonl')
    log_path.parent.mkdir(parents=True, exist_ok=True)

    print(f'Applying patches {start}-{end} of {total}')
    print(f'Log: {log_path}')
    print()

    success_count = 0
    error_count = 0
    log_entries: list[dict] = []

    with log_path.open('a', encoding='utf-8') as log_f:
        for idx in range(start, end + 1):
            filename, kind = SEQUENCE[idx - 1]
            print(f'[{idx}/{total}] {filename}', flush=True)
            t0 = datetime.now(timezone.utc).isoformat()

            if args.dry_run:
                print(f'  (dry-run) would apply {filename}')
                continue

            rc, output = run_jsonl_patch(filename)
            t1 = datetime.now(timezone.utc).isoformat()

            entry = {
                'idx': idx,
                'filename': filename,
                'rc': rc,
                'started_at': t0,
                'finished_at': t1,
                'output_tail': output[-2000:] if len(output) > 2000 else output,
            }
            log_f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            log_f.flush()

            if rc != 0:
                error_count += 1
                print(f'  FAILED (rc={rc}). Last lines:')
                for line in output.splitlines()[-15:]:
                    try:
                        print(f'    {line}')
                    except UnicodeEncodeError:
                        print(f'    {line.encode("ascii", "replace").decode("ascii")}')
                print()
                print('STOPPING.')
                return 2

            # Parse "summary" from tail for a brief
            summary_line = ''
            for line in output.splitlines():
                if '"records":' in line or '"would_create' in line or '"created' in line or '"applied' in line:
                    summary_line = line.strip()
                    break
            print(f'  OK')
            success_count += 1

    print()
    print(f'Done. {success_count} applied, {error_count} errors.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
