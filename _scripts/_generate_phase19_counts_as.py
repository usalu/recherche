"""Phase 19: Backfill counts_as_* properties on 61 batch2 BGs.

Derive from reuse_status:
  reuse → counts_as_direct_reuse=true, others=false
  retained → counts_as_bestandserhalt=true, counts_as_direct_reuse=false
  planned → all 4 nulls (decision deferred to post-build)
  dismantled → counts_as_direct_reuse=false (component is now donor stock)
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection

SRC = 'batch2_v2_phase19_2026-05-20'


def derive_props(reuse_status: str) -> dict:
    """Map reuse_status → counts_as_* flags."""
    if reuse_status == 'reuse':
        return {
            'counts_as_direct_reuse': True,
            'counts_as_bestandserhalt': False,
            'counts_as_recycling': False,
            'counts_as_remanufacturing': False,
        }
    if reuse_status == 'retained':
        return {
            'counts_as_direct_reuse': False,
            'counts_as_bestandserhalt': True,
            'counts_as_recycling': False,
            'counts_as_remanufacturing': False,
        }
    if reuse_status == 'dismantled':
        # Donor stock — not yet reused; properties pending receiver project.
        return {
            'counts_as_direct_reuse': False,
            'counts_as_bestandserhalt': False,
        }
    if reuse_status == 'planned':
        # No decision until built; leave None (don't backfill)
        return {}
    return {}


def main() -> int:
    from neo4j import GraphDatabase
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    bgs: list[dict] = []
    with driver.session(database=database) as session:
        rows = list(session.run('''MATCH (bg:Bauteilgruppe)
            WHERE bg.source_scope = "case_markdown"
              AND bg.counts_as_direct_reuse IS NULL
            RETURN bg.id AS id, bg.reuse_status AS status'''))
        for r in rows:
            bgs.append({'id': r['id'], 'status': r['status']})
    driver.close()

    ops: list[dict] = []
    for bg in bgs:
        props = derive_props(bg['status'] or '')
        if not props:
            continue
        ops.append({
            'op': 'set_node_properties',
            'id': bg['id'],
            'properties': props,
            'reason': f"Phase 19 B2: counts_as_* derived from reuse_status='{bg['status']}'.",
            'severity': 'LOW',
        })

    out = Path('e:/recherche/_neo4j/review/round_002_followup/patches/batch2/phase_batch2_v2_19_counts_as.patch.jsonl')
    with out.open('w', encoding='utf-8') as f:
        for op in ops:
            f.write(json.dumps(op, ensure_ascii=False) + '\n')
    print(f'Wrote {len(ops)} counts_as_* backfill ops (from {len(bgs)} BGs; planned-status BGs skipped) to {out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
