import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

ids = [
    "software_planular", "tool_swiss_inv", "software_cirkla_scan", "prog_swircular",
    "prog_innosuisse_reuse_legal_framework_ch", "c33_circular_construction_catalyst",
    "circular_hub_zurich", "circular_economy_switzerland", "sumami", "repurpose", "mineka",
]
uri, u, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, pw))
with driver.session(database=db) as s:
    for i in ids:
        r = s.run(
            "MATCH (n {id: $id}) RETURN n.id AS id, n.primary_source_url AS u, n.source_urls AS urls",
            id=i,
        ).single()
        print(i, dict(r) if r else "MISSING")
driver.close()
