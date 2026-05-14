"""
Find all project-level duplicates across the full database:
- Same Bauwerk referenced by multiple Projekt nodes
- Overlapping Bauteilgruppen (same component in two projects)
- Near-identical project names
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, '_scripts')
from neo4j_env import resolve_connection
from neo4j import GraphDatabase

uri, user, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(user, pw))

def q(cypher, **params):
    with driver.session(database=db) as s:
        return list(s.run(cypher, **params))

SEP = '-' * 70

# ── 1. Same Bauwerk shared by multiple Projekt via HAT_BAUTEILGRUPPE ─────────
print('=== Projects sharing the same Bauwerk (eingebaut_in) ===')
rows = q('''
    MATCH (p1:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg1)-[:EINGEBAUT_IN]->(bw:Bauwerk)<-[:EINGEBAUT_IN]-(bg2)<-[:HAT_BAUTEILGRUPPE]-(p2:Projekt)
    WHERE p1.id < p2.id
    RETURN DISTINCT p1.id AS a, p1.name AS a_name, p2.id AS b, p2.name AS b_name, bw.name AS bauwerk
    ORDER BY bw.name
''')
for r in rows:
    print(f'  Bauwerk: {r["bauwerk"]}')
    print(f'    {r["a"]}  [{r["a_name"]}]')
    print(f'    {r["b"]}  [{r["b_name"]}]')
    print()

# ── 2. Same donor Bauwerk in multiple projects ────────────────────────────────
print('=== Projects sharing the same donor Bauwerk (AUS_BAUWERK) ===')
rows = q('''
    MATCH (p1:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg1)-[:AUS_BAUWERK]->(bw:Bauwerk)<-[:AUS_BAUWERK]-(bg2)<-[:HAT_BAUTEILGRUPPE]-(p2:Projekt)
    WHERE p1.id < p2.id
    RETURN DISTINCT p1.id AS a, p2.id AS b, bw.name AS donor
    ORDER BY donor
''')
for r in rows:
    print(f'  Donor: {r["donor"]}')
    print(f'    {r["a"]}')
    print(f'    {r["b"]}')
    print()

# ── 3. Projects with identical Bauteilgruppe name ────────────────────────────
print('=== Bauteilgruppe names appearing in multiple projects ===')
rows = q('''
    MATCH (p1:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg1)
    MATCH (p2:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg2)
    WHERE p1.id < p2.id AND bg1.name = bg2.name
    RETURN bg1.name AS bg_name, p1.id AS a, p2.id AS b
    ORDER BY bg1.name
''')
for r in rows:
    print(f'  BG: "{r["bg_name"]}"')
    print(f'    in {r["a"]}')
    print(f'    in {r["b"]}')
    print()

# ── 4. Projects with very similar names (check word overlap) ─────────────────
print('=== All Projekt ids+names for manual review ===')
rows = q('MATCH (p:Projekt) RETURN p.id AS id, p.name AS name, p.bewertung AS bew ORDER BY p.name')
for r in rows:
    print(f'  bew={r["bew"]}  {r["id"]:<65}  {r["name"]}')

driver.close()
