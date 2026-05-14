"""
Migrate unique data from duplicate projects then delete the duplicates.
Targets (all from batches 015-019):
  - p_elys_kultur_und_gewerbehaus_basel_lysbuechelareal  -> keep p_elys_kultur_gewerbehaus_basel
  - p_bestandshalle_crclr_house                          -> keep p_crclr_house_impact_hub_berlin
  - p_crclr_house_berlin_overview                        -> keep p_crclr_house_impact_hub_berlin
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, '_scripts')
from neo4j_env import resolve_connection
from neo4j import GraphDatabase

uri, user, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(user, pw))

def run(cypher, **params):
    with driver.session(database=db) as s:
        result = s.run(cypher, **params)
        return result.consume().counters

DRY_RUN = '--dry-run' in sys.argv

def do(label, cypher, **params):
    print(f'  {label}')
    if DRY_RUN:
        print(f'    [DRY RUN] {cypher[:120]}')
        return
    c = run(cypher, **params)
    changes = {k: v for k, v in vars(c).items() if isinstance(v, int) and v > 0}
    print(f'    => {changes}')

print('=' * 60)
print('  MIGRATION + DEDUPLICATION')
print('=' * 60)

# ─────────────────────────────────────────────────────────────
# STEP 1: ELYS Basel
# p_elys_kultur_und_gewerbehaus_basel_lysbuechelareal -> DELETED
# Its 4 BG nodes get linked to the richer older project
# ─────────────────────────────────────────────────────────────
print('\n[1] ELYS Basel: migrate BGs from detailed -> older, then delete detailed')

# Re-attach all BG nodes from the detailed project to the older project
do(
    'Re-link BGs: detailed ELYS -> older ELYS',
    '''
    MATCH (dup:Projekt {id: $dup})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
    MATCH (keep:Projekt {id: $keep})
    MERGE (keep)-[:HAT_BAUTEILGRUPPE]->(bg)
    ''',
    dup='p_elys_kultur_und_gewerbehaus_basel_lysbuechelareal',
    keep='p_elys_kultur_gewerbehaus_basel'
)

# Delete the duplicate project node (DETACH removes its rels; BGs/actors/sources remain)
do(
    'Delete duplicate ELYS projekt node',
    'MATCH (p:Projekt {id: $id}) DETACH DELETE p',
    id='p_elys_kultur_und_gewerbehaus_basel_lysbuechelareal'
)

# ─────────────────────────────────────────────────────────────
# STEP 2: Bestandshalle CRCLR House
# Migrate 2 unique BGs then delete
# ─────────────────────────────────────────────────────────────
print('\n[2] Bestandshalle CRCLR House: migrate unique BGs, then delete')

do(
    'Re-link BGs: Bestandshalle -> main CRCLR',
    '''
    MATCH (dup:Projekt {id: $dup})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
    MATCH (keep:Projekt {id: $keep})
    MERGE (keep)-[:HAT_BAUTEILGRUPPE]->(bg)
    ''',
    dup='p_bestandshalle_crclr_house',
    keep='p_crclr_house_impact_hub_berlin'
)

do(
    'Delete duplicate Bestandshalle projekt node',
    'MATCH (p:Projekt {id: $id}) DETACH DELETE p',
    id='p_bestandshalle_crclr_house'
)

# ─────────────────────────────────────────────────────────────
# STEP 3: CRCLR Overview
# Migrate Concular actor then delete
# ─────────────────────────────────────────────────────────────
print('\n[3] CRCLR Overview: migrate Concular actor, then delete')

do(
    'Re-link Concular BETEILIGT_AN -> main CRCLR',
    '''
    MATCH (a:Akteur {id: $actor})-[:BETEILIGT_AN]->(dup:Projekt {id: $dup})
    MATCH (keep:Projekt {id: $keep})
    MERGE (a)-[:BETEILIGT_AN]->(keep)
    ''',
    actor='a_concular',
    dup='p_crclr_house_berlin_overview',
    keep='p_crclr_house_impact_hub_berlin'
)

do(
    'Delete duplicate CRCLR overview projekt node',
    'MATCH (p:Projekt {id: $id}) DETACH DELETE p',
    id='p_crclr_house_berlin_overview'
)

# ─────────────────────────────────────────────────────────────
# Verify
# ─────────────────────────────────────────────────────────────
print('\n[verification]')
with driver.session(database=db) as s:
    deleted = ['p_elys_kultur_und_gewerbehaus_basel_lysbuechelareal',
               'p_bestandshalle_crclr_house', 'p_crclr_house_berlin_overview']
    for pid in deleted:
        r = list(s.run('MATCH (p:Projekt {id:$id}) RETURN count(p) AS c', id=pid))[0]['c']
        status = 'STILL EXISTS' if r else 'deleted OK'
        print(f'  {pid}: {status}')

    # Check BGs migrated
    r = list(s.run('''
        MATCH (p:Projekt {id:"p_crclr_house_impact_hub_berlin"})-[:HAT_BAUTEILGRUPPE]->(bg)
        RETURN count(bg) AS c
    '''))[0]['c']
    print(f'  p_crclr_house_impact_hub_berlin  BGs now: {r}')

    r = list(s.run('''
        MATCH (p:Projekt {id:"p_elys_kultur_gewerbehaus_basel"})-[:HAT_BAUTEILGRUPPE]->(bg)
        RETURN count(bg) AS c
    '''))[0]['c']
    print(f'  p_elys_kultur_gewerbehaus_basel  BGs now: {r}')

    # Total project count
    r = list(s.run('MATCH (p:Projekt) RETURN count(p) AS c'))[0]['c']
    print(f'  Total Projekt nodes remaining: {r}')

driver.close()
print('\nDone.')
