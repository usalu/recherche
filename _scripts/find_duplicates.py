import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, '_scripts')
from neo4j_env import resolve_connection
from neo4j import GraphDatabase

uri, user, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(user, pw))

with driver.session(database=db) as s:
    # Find all duplicate relationships
    rows = list(s.run('''
        MATCH (a)-[r]->(b)
        WITH a, type(r) AS t, b, collect(r) AS rels
        WHERE size(rels) > 1
        RETURN
            labels(a)[0] AS src_lbl,
            coalesce(a.name, a.id) AS src,
            t,
            labels(b)[0] AS tgt_lbl,
            coalesce(b.name, b.id) AS tgt,
            size(rels) AS cnt,
            [x IN rels | elementId(x)] AS rel_ids
        ORDER BY src, t, tgt
    '''))
    print(f'Duplicate relationship patterns found: {len(rows)}')
    total_excess = sum(r['cnt'] - 1 for r in rows)
    print(f'Excess relationships to delete: {total_excess}')
    print()
    for row in rows:
        src  = (row['src'] or '')[:40]
        tgt  = (row['tgt'] or '')[:35]
        print(f"  [{row['src_lbl']}] {src:<40} -[{row['t']}]-> [{row['tgt_lbl']}] {tgt:<35}  x{row['cnt']}")

# Also check duplicate nodes
with driver.session(database=db) as s:
    rows2 = list(s.run('''
        MATCH (n)
        WITH n.id AS nid, collect(n) AS nodes, labels(n)[0] AS lbl
        WHERE nid IS NOT NULL AND size(nodes) > 1
        RETURN lbl, nid, size(nodes) AS cnt
        ORDER BY cnt DESC
    '''))
    print(f'\nDuplicate node IDs: {len(rows2)}')
    for row in rows2:
        print(f"  [{row['lbl']}] {row['nid']}  x{row['cnt']}")

driver.close()
