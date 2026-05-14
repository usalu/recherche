import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, '_scripts')
from neo4j_env import resolve_connection
from neo4j import GraphDatabase

uri, user, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(user, pw))

TARGET = [
    'p_opalis_plattformfall', 'p_preuse_interreg_nwe',
    'p_crclr_house_berlin_overview', 'p_bestandshalle_crclr_house',
]

with driver.session(database=db) as s:
    # 1. Duplicate BETEILIGT_AN: same actor -> same project, multiple edges
    rows = list(s.run('''
        MATCH (a:Akteur)-[r:BETEILIGT_AN]->(p:Projekt)
        WHERE p.id IN $ids
        WITH a, p, collect(elementId(r)) AS eids
        WHERE size(eids) > 1
        RETURN a.name AS actor, a.id AS actor_id, p.id AS proj, size(eids) AS cnt, eids[1..] AS extras
        ORDER BY p.id, a.id
    ''', ids=TARGET))
    print('--- Duplicate BETEILIGT_AN ---')
    for row in rows:
        print(f'  {row["actor"]} -> {row["proj"]}  ({row["cnt"]}x)  extra_eids={row["extras"]}')

    # 2. All dup rels touching these projects
    rows2 = list(s.run('''
        MATCH (a)-[r]->(b)
        WHERE (b:Projekt AND b.id IN $ids) OR (a:Projekt AND a.id IN $ids)
        WITH a, type(r) AS t, b, collect(elementId(r)) AS eids
        WHERE size(eids) > 1
        RETURN a.id AS src, t, b.id AS tgt, size(eids) AS cnt, eids[1..] AS extras
        ORDER BY t, a.id
    ''', ids=TARGET))
    print('\n--- All duplicate rels on target projects ---')
    for row in rows2:
        print(f'  ({row["src"]})-[{row["t"]}]->({row["tgt"]})  {row["cnt"]}x  extras={row["extras"]}')

    # 3. CRCLR: what unique data does each have?
    print('\n--- CRCLR overview vs. detail comparison ---')
    for pid in ['p_crclr_house_berlin_overview', 'p_bestandshalle_crclr_house']:
        bg_cnt = list(s.run('MATCH (p:Projekt {id:$id})-[:HAT_BAUTEILGRUPPE]->(bg) RETURN count(bg) AS c', id=pid))[0]['c']
        act_cnt = list(s.run('MATCH (a)-[:BETEILIGT_AN]->(p:Projekt {id:$id}) RETURN count(a) AS c', id=pid))[0]['c']
        h_cnt = list(s.run('MATCH (p:Projekt {id:$id})-[:HAT_HUERDE]->(h) RETURN count(h) AS c', id=pid))[0]['c']
        rel_total = list(s.run('MATCH (p:Projekt {id:$id})-[r]-() RETURN count(r) AS c', id=pid))[0]['c']
        p_props = list(s.run('MATCH (p:Projekt {id:$id}) RETURN p', id=pid))[0]['p']
        print(f'  {pid}')
        print(f'    bew={p_props.get("bewertung")} status={p_props.get("projektstatus_text")}')
        print(f'    total_rels={rel_total}  bauteilgruppen={bg_cnt}  akteure={act_cnt}  hurden={h_cnt}')

driver.close()
