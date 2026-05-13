from neo4j import GraphDatabase
d = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j','ENTWERFENMITBESTAND'))
with d.session() as s:
    total_n = s.run('MATCH (n) RETURN count(n) AS c').single()['c']
    total_r = s.run('MATCH ()-[r]->() RETURN count(r) AS c').single()['c']
    projects = s.run('MATCH (p:Projekt) RETURN p.name AS name, p.bewertung AS bw ORDER BY p.name').data()
    btg = s.run('MATCH (b:Bauteilgruppe) RETURN b.counts_as_direct_reuse AS flag, count(*) AS n').data()
    labels = s.run('MATCH (n:Projekt) RETURN n.id AS pid, n.name AS name, n.bewertung AS bw ORDER BY n.name').data()

print(f'Nodes: {total_n}  Rels: {total_r}')
print(f'Projects ({len(projects)}):')
for p in projects:
    print(f'  bw={p["bw"]}  {p["name"]}')
print('BTG flags:')
for b in btg:
    print(f'  {b["flag"]}: {b["n"]}')
d.close()
