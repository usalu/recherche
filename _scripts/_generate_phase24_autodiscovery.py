"""Phase 24: Auto-discovery patches.

24a — VERBUNDEN_MIT_AKTEUR for actor pairs sharing >= 2 projects (no existing peer link)
24b — mat_mehrere → mg_mehrere (orphaned Material in Phase 2d)
24c — (skipped: Programme parents already wired in Phase 1d / 4b)
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection

SRC = 'batch2_v2_phase24_2026-05-20'


def main() -> int:
    from neo4j import GraphDatabase
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))

    pairs: list[tuple[str, str, int]] = []
    with driver.session(database=database) as session:
        rows = list(session.run('''
            MATCH (a1:Akteur)-[:BETEILIGT_AN]->(p)<-[:BETEILIGT_AN]-(a2:Akteur)
            WHERE elementId(a1) < elementId(a2)
            WITH a1, a2, count(DISTINCT p) AS shared
            WHERE shared >= 2
              AND NOT EXISTS { (a1)-[:VERBUNDEN_MIT_AKTEUR]-(a2) }
            RETURN a1.id AS a1, a2.id AS a2, shared
            ORDER BY shared DESC, a1.id'''))
        pairs = [(r['a1'], r['a2'], r['shared']) for r in rows]
    driver.close()

    ops: list[dict] = []
    for (a1, a2, shared) in pairs:
        rid = f'r_{a1}__VERBUNDEN_MIT_AKTEUR__{a2}'
        ops.append({
            'op': 'add_rel',
            'from': a1,
            'type': 'VERBUNDEN_MIT_AKTEUR',
            'to': a2,
            'properties': {
                'id': rid,
                'source': SRC,
                'evidence': 'INFER',
                'inference_basis': f'shared {shared} project(s)',
            },
            'reason': 'Phase 24a: peer link inferred from shared project participation (>= 2 projects).',
            'severity': 'LOW',
        })

    # 24b — mat_mehrere → mg_mehrere
    ops.append({
        'op': 'add_rel',
        'from': 'mat_mehrere',
        'type': 'HAT_MATERIALGRUPPE',
        'to': 'mg_mehrere',
        'properties': {
            'id': 'r_mat_mehrere__HAT_MATERIALGRUPPE__mg_mehrere',
            'source': SRC,
        },
        'reason': 'Phase 24b: mat_mehrere placeholder Material → mg_mehrere placeholder Materialgruppe.',
        'severity': 'LOW',
    })

    out = Path('e:/recherche/_neo4j/review/round_002_followup/patches/batch2/phase_batch2_v2_24_autodiscovery.patch.jsonl')
    with out.open('w', encoding='utf-8') as f:
        for op in ops:
            f.write(json.dumps(op, ensure_ascii=False) + '\n')
    print(f'Wrote {len(ops)} ops to {out}')
    print(f'  - {len(pairs)} VERBUNDEN_MIT_AKTEUR peer links')
    print(f'  - 1 mat_mehrere → mg_mehrere')
    return 0


if __name__ == '__main__':
    sys.exit(main())
