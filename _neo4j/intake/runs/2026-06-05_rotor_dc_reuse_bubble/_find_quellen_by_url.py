import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

urls = [
    "https://preuse.nweurope.eu/",
    "https://preuse.nweurope.eu/partners",
    "https://www.rotordb.org/en/projects/preuse-interreg-nwe",
    "https://opalis.eu/en/dealers/rotor-deconstruction",
    "https://rotordb.org/en/projects/multi-de-brouckere-tower",
]
uri, u, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, pw))
with driver.session(database=db) as s:
    for url in urls:
        rows = list(s.run(
            "MATCH (q:Quelle) WHERE q.url = $url OR q.url CONTAINS $frag RETURN q.id AS id, q.url AS url LIMIT 5",
            url=url,
            frag=url.split("//")[-1][:30],
        ))
        print(url, "->", rows if rows else "NOT FOUND")
driver.close()
