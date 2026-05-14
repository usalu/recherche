from pathlib import Path
from _scripts.neo4j_env import resolve_connection
from neo4j import GraphDatabase

uri, user, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(user, pw))
with driver.session(database=db) as s:
    db_ids = set(row[0] for row in s.run('MATCH (p:Projekt) RETURN p.id'))
driver.close()

merged = {
    'Berlin_Schildow_Pilot_House_2': 'p_berlin_schildow_pilot_house',
    'Bestandshalle_CRCLR_House': 'p_crclr_house_impact_hub_berlin',
    'CRCLR_House': 'p_crclr_house_impact_hub_berlin',
    'ELYS_Kultur_und_Gewerbehaus_Basel_Lysbuechelareal': 'p_elys_kultur_gewerbehaus_basel',
}

disk_folders = sorted(d.name for d in Path('_database/fallstudie').iterdir() if d.is_dir())
not_covered = []
for folder in disk_folders:
    if folder in merged:
        canonical = merged[folder]
        status = 'OK' if canonical in db_ids else 'CANONICAL MISSING'
        print(f'  MERGED {folder} -> {canonical} [{status}]')
        continue
    base = folder.lower().replace('-', '_')
    # exact match first, then prefix/substring match
    eid = 'p_' + base
    if eid in db_ids:
        continue
    # substring: any db id that starts with or contains the base slug
    matches = [i for i in db_ids if i.startswith(eid) or base in i]
    if matches:
        continue  # covered by a longer ID
    not_covered.append((folder, eid))

print()
if not_covered:
    print('NOT IN NEO4J:')
    for f, e in not_covered:
        print(f'  {f}  (expected id: {e})')
else:
    print('ALL COVERED - nothing missing.')
print(f'Disk: {len(disk_folders)} folders | DB: {len(db_ids)} Projekt nodes')
