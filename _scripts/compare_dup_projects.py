"""Compare every duplicate project pair found."""
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

def full_profile(pid):
    row = q('MATCH (p:Projekt {id:$id}) RETURN p', id=pid)
    if not row: return None
    p = dict(row[0]['p'])
    bgs   = q('MATCH (p:Projekt {id:$id})-[:HAT_BAUTEILGRUPPE]->(bg) OPTIONAL MATCH (bg)-[:AUS_BAUWERK]->(d) OPTIONAL MATCH (bg)-[:EINGEBAUT_IN]->(t) RETURN bg.name AS n, d.name AS donor, t.name AS target', id=pid)
    acts  = q('MATCH (a)-[:BETEILIGT_AN]->(p:Projekt {id:$id}) OPTIONAL MATCH (a)-[:HAT_AKTEURROLLE]->(ar) RETURN a.name AS a, collect(ar.name) AS r', id=pid)
    hurd  = q('MATCH (p:Projekt {id:$id})-[:HAT_HUERDE]->(h) RETURN h.name AS h', id=pid)
    srcs  = q('MATCH (p:Projekt {id:$id})-[:BELEGT_IN]->(q) RETURN q.name AS q', id=pid)
    rels  = q('MATCH (p:Projekt {id:$id})-[r]->(x) RETURN type(r) AS t, x.id AS xid, labels(x)[0] AS lbl', id=pid)
    return {'props': p, 'bgs': bgs, 'actors': acts, 'hurden': hurd, 'sources': srcs, 'rels': rels}

def print_profile(pid, label=''):
    d = full_profile(pid)
    if not d:
        print(f'  *** {pid} NOT FOUND ***')
        return
    p = d['props']
    print(f'\n  [{label}] {pid}')
    print(f'  name   : {p.get("name")}')
    print(f'  bew    : {p.get("bewertung")}  status: {p.get("projektstatus_text")}')
    if p.get('note'): print(f'  note   : {p["note"][:150]}')
    print(f'  total outgoing rels: {len(d["rels"])}')
    print(f'  Akteure ({len(d["actors"])}): {", ".join(a["a"] for a in d["actors"])}')
    print(f'  Bauteilgruppen ({len(d["bgs"])}):', )
    for bg in d['bgs']:
        print(f'    • {bg["n"]}')
        if bg.get("donor"):  print(f'      aus: {bg["donor"]}')
        if bg.get("target"): print(f'      ->:  {bg["target"]}')
    print(f'  Hürden: {[h["h"] for h in d["hurden"]]}')
    print(f'  Quellen: {[s["q"] for s in d["sources"]]}')

SEP = '=' * 70

# ── Pair 1: ELYS Basel ────────────────────────────────────────────────────────
print(f'\n{SEP}')
print('  DUPLICATE PAIR 1: ELYS Basel')
print(SEP)
print_profile('p_elys_kultur_gewerbehaus_basel',              'OLDER / simple')
print_profile('p_elys_kultur_und_gewerbehaus_basel_lysbuechelareal', 'NEWER / detailed')

# ── Pair 2: CRCLR House Berlin ────────────────────────────────────────────────
print(f'\n{SEP}')
print('  DUPLICATE PAIR 2: CRCLR House Berlin')
print(SEP)
print_profile('p_crclr_house_impact_hub_berlin',   'EXISTING (early batch)')
print_profile('p_bestandshalle_crclr_house',        'BATCH 016 detail')
print_profile('p_crclr_house_berlin_overview',      'BATCH 017 overview')

# ── Pair 3: Stubs ─────────────────────────────────────────────────────────────
print(f'\n{SEP}')
print('  STUBS (bew=0): no real data')
print(SEP)
print_profile('p_permanently_temporary_pavilion',  'STUB')
print_profile('p_rotor_dc_brussels_model',          'STUB')

driver.close()
