"""List tier_1 project IDs so we can pick one for the detail probe."""
import io
import sys
from pathlib import Path
_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
from neo4j_env import resolve_connection
from neo4j import GraphDatabase

uri, user, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(user, pw))
with driver.session(database=db) as s:
    rows = s.run(
        "MATCH (p:Projekt) WHERE p.quality_tier='tier_1_decision_grade' "
        "RETURN p.id AS id, p.name AS name ORDER BY name"
    ).data()
    for x in rows:
        print(f"  {x['id']:<45s} {x['name']}")
