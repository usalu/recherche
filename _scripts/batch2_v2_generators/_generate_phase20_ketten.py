"""Phase 20: Wiederverwendungskette expansion.

C1 — Create new ketten for 21 donor-receiver pairs not yet covered.
C2 — Add additional BGs to existing batch2 ketten where dossier evidence supports.

For Phase 20a: bulk-create wk_* nodes for each donor-receiver pair in the live graph.
For Phase 20b: add TEIL_VON_KETTE + AUS_BAUWERK + EINGEBAUT_IN to wire them.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent.parent  # _scripts/ (one level up after relocation to batch2_v2_generators/)
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection

SRC = 'batch2_v2_phase20_2026-05-20'


def short_id(bw_id: str, max_len: int = 35) -> str:
    """Strip bw_ prefix and abbreviate for kette id."""
    s = bw_id[3:] if bw_id.startswith('bw_') else bw_id
    return s[:max_len]


def main() -> int:
    from neo4j import GraphDatabase
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))

    pairs: list[dict] = []
    with driver.session(database=database) as session:
        rows = list(session.run('''MATCH (donor:Bauwerk)<-[:AUS_BAUWERK]-(bg:Bauteilgruppe)-[:EINGEBAUT_IN]->(receiver:Bauwerk)
            WHERE donor <> receiver
              AND NOT EXISTS { (bg)-[:TEIL_VON_KETTE]->(:Wiederverwendungskette) }
            RETURN donor.id AS donor, donor.name AS donor_name,
                   receiver.id AS receiver, receiver.name AS receiver_name,
                   collect(bg.id) AS bgs ORDER BY donor, receiver'''))
        for r in rows:
            kid = f'wk_{short_id(r["donor"])}_to_{short_id(r["receiver"])}'
            pairs.append({
                'id': kid,
                'donor': r['donor'],
                'donor_name': r['donor_name'],
                'receiver': r['receiver'],
                'receiver_name': r['receiver_name'],
                'bgs': list(r['bgs']),
            })
    driver.close()

    # Phase 20a: add_node for each new kette
    adds: list[dict] = []
    for p in pairs:
        name = (p['donor_name'] or p['donor'])[:12] + '→' + (p['receiver_name'] or p['receiver'])[:12]
        adds.append({
            'op': 'add_node',
            'id': p['id'],
            'labels': ['Wiederverwendungskette'],
            'properties': {
                'id': p['id'],
                'name': name[:25],
                'name_full': f'Reuse-Kette {p["donor_name"] or p["donor"]} → {p["receiver_name"] or p["receiver"]} (auto-discovered from {len(p["bgs"])} Bauteilgruppe link(s))',
                'source_scope': 'derived',
            },
            'reason': 'Phase 20a: Wiederverwendungskette auto-created from donor-receiver pair (Bauwerk -AUS_BAUWERK- BG -EINGEBAUT_IN- Bauwerk pattern).',
            'severity': 'LOW',
        })

    # Phase 20b: wire TEIL_VON_KETTE + Bauwerk-Kette donor/receiver edges
    rels: list[dict] = []
    for p in pairs:
        # Donor → Kette via AUS_BAUWERK
        rels.append({
            'op': 'add_rel',
            'from': p['donor'],
            'type': 'AUS_BAUWERK',
            'to': p['id'],
            'properties': {'id': f'r_{p["donor"]}__AUS_BAUWERK__{p["id"]}', 'source': SRC, 'evidence': 'INFER'},
            'reason': 'Phase 20b: donor Bauwerk → Kette.',
            'severity': 'LOW',
        })
        # Receiver → Kette via EINGEBAUT_IN
        rels.append({
            'op': 'add_rel',
            'from': p['receiver'],
            'type': 'EINGEBAUT_IN',
            'to': p['id'],
            'properties': {'id': f'r_{p["receiver"]}__EINGEBAUT_IN__{p["id"]}', 'source': SRC, 'evidence': 'INFER'},
            'reason': 'Phase 20b: receiver Bauwerk → Kette.',
            'severity': 'LOW',
        })
        # Each BG → Kette via TEIL_VON_KETTE
        for bg in p['bgs']:
            rels.append({
                'op': 'add_rel',
                'from': bg,
                'type': 'TEIL_VON_KETTE',
                'to': p['id'],
                'properties': {'id': f'r_{bg}__TEIL_VON_KETTE__{p["id"]}', 'source': SRC, 'evidence': 'INFER'},
                'reason': 'Phase 20b: BG → Kette.',
                'severity': 'LOW',
            })

    a = Path('e:/recherche/_neo4j/review/round_002_followup/patches/batch2/phase_batch2_v2_20a_kette_addnodes.patch.jsonl')
    b = Path('e:/recherche/_neo4j/review/round_002_followup/patches/batch2/phase_batch2_v2_20b_kette_rels.patch.jsonl')
    with a.open('w', encoding='utf-8') as f:
        for x in adds:
            f.write(json.dumps(x, ensure_ascii=False) + '\n')
    with b.open('w', encoding='utf-8') as f:
        for x in rels:
            f.write(json.dumps(x, ensure_ascii=False) + '\n')
    print(f'Wrote {len(adds)} Kette add_nodes to {a}')
    print(f'Wrote {len(rels)} Kette rel ops to {b}')
    print(f'Pairs covered: {len(pairs)}; total BGs wired: {sum(len(p["bgs"]) for p in pairs)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
