import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, '_scripts')
from neo4j_env import resolve_connection
from neo4j import GraphDatabase
from collections import defaultdict

uri, user, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(user, pw))

def q(cypher, **params):
    with driver.session(database=db) as s:
        return list(s.run(cypher, **params))

# ── 1. Overview ──────────────────────────────────────────────────────────────
total_nodes = q('MATCH (n) RETURN count(n) AS c')[0]['c']
total_rels  = q('MATCH ()-[r]->() RETURN count(r) AS c')[0]['c']
print(f"\n{'='*60}")
print(f"  OVERVIEW")
print(f"{'='*60}")
print(f"  Total nodes        : {total_nodes:>6,}")
print(f"  Total relationships: {total_rels:>6,}")
print(f"  Avg rels / node    : {total_rels/total_nodes:.1f}")

# ── 2. Node labels ────────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"  NODE LABELS")
print(f"{'='*60}")
rows = q('CALL db.labels() YIELD label RETURN label ORDER BY label')
labels = [r['label'] for r in rows]
for label in labels:
    cnt = q(f'MATCH (n:`{label}`) RETURN count(n) AS c')[0]['c']
    bar = '█' * (cnt * 40 // max(1, total_nodes))
    print(f"  {label:<35} {cnt:>5}  {bar}")

# ── 3. Relationship types ─────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"  RELATIONSHIP TYPES")
print(f"{'='*60}")
rows = q('''
    MATCH ()-[r]->()
    RETURN type(r) AS t, count(r) AS c
    ORDER BY c DESC
''')
for r in rows:
    bar = '█' * (r['c'] * 40 // max(1, total_rels))
    print(f"  {r['t']:<40} {r['c']:>5}  {bar}")

# ── 4. Projekt summary ────────────────────────────────────────────────────────
print(f"\n{'='*60}")
print(f"  PROJEKTE")
print(f"{'='*60}")
rows = q('MATCH (p:Projekt) RETURN p.name AS name, p.bewertung AS bew ORDER BY p.name')
print(f"  Count: {len(rows)}")
bew_vals = [r['bew'] for r in rows if r['bew']]
if bew_vals:
    from collections import Counter
    bew_cnt = Counter(bew_vals)
    print(f"  Bewertung distribution:")
    for k, v in sorted(bew_cnt.items()):
        print(f"    {k}: {v}")
print(f"  Without bewertung: {sum(1 for r in rows if not r['bew'])}")

# ── 5. Connectivity: top connected nodes ─────────────────────────────────────
print(f"\n{'='*60}")
print(f"  TOP 15 MOST CONNECTED NODES")
print(f"{'='*60}")
rows = q('''
    MATCH (n)
    WITH n, labels(n)[0] AS lbl, COUNT { (n)--() } AS deg
    ORDER BY deg DESC LIMIT 15
    RETURN lbl, coalesce(n.name, n.id, toString(id(n))) AS name, deg
''')
for r in rows:
    print(f"  [{r['lbl']:<20}]  {r['name']:<40}  deg={r['deg']}")

# ── 6. Orphan nodes (no relationships) ───────────────────────────────────────
print(f"\n{'='*60}")
print(f"  ORPHAN NODES (no relationships)")
print(f"{'='*60}")
rows = q('''
    MATCH (n) WHERE NOT (n)--()
    RETURN labels(n)[0] AS lbl, count(n) AS c
    ORDER BY c DESC
''')
if rows:
    for r in rows:
        print(f"  {r['lbl']:<35} {r['c']:>5}")
else:
    print("  None")

# ── 7. Relationship pattern matrix (top pairs) ────────────────────────────────
print(f"\n{'='*60}")
print(f"  TOP 20 RELATIONSHIP PATTERNS  (src)-[type]->(tgt)")
print(f"{'='*60}")
rows = q('''
    MATCH (a)-[r]->(b)
    RETURN labels(a)[0] AS src, type(r) AS t, labels(b)[0] AS tgt, count(*) AS c
    ORDER BY c DESC LIMIT 20
''')
for r in rows:
    print(f"  ({r['src']:<20})-[{r['t']:<30}]->({r['tgt']:<20})  {r['c']:>5}")

# ── 8. Property coverage on Projekt ──────────────────────────────────────────
print(f"\n{'='*60}")
print(f"  PROJEKT PROPERTY COVERAGE")
print(f"{'='*60}")
rows = q('MATCH (p:Projekt) RETURN p')
if rows:
    all_keys = set()
    for r in rows:
        all_keys.update(r['p'].keys())
    print(f"  Total Projekt nodes: {len(rows)}")
    for k in sorted(all_keys):
        filled = sum(1 for r in rows if r['p'].get(k) not in (None, '', []))
        pct = 100 * filled // len(rows)
        bar = '█' * (pct // 5)
        print(f"  {k:<30} {filled:>3}/{len(rows)}  {pct:>3}%  {bar}")

driver.close()
print(f"\n{'='*60}\n")
