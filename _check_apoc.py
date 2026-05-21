import sys
sys.path.insert(0, '_scripts')
from neo4j_env import resolve_connection
from neo4j import GraphDatabase

uri, user, password, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(user, password))
with driver.session(database='mit-bestand') as s:
    try:
        r = s.run('CALL apoc.help("mergeNodes") YIELD name RETURN name LIMIT 1').single()
        print('APOC mergeNodes:', r['name'] if r else 'NOT FOUND')
    except Exception as e:
        print('APOC mergeNodes NOT available:', e)
driver.close()
