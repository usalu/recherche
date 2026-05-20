"""Inspect BETEILIGT_AN keys."""
from __future__ import annotations
import sys
from pathlib import Path

REPO_ROOT = Path(r"E:/recherche")
sys.path.insert(0, str(REPO_ROOT / "_scripts"))
from neo4j_env import resolve_connection  # type: ignore
from neo4j import GraphDatabase  # type: ignore

uri, user, pw, _ = resolve_connection()
db = "mit-bestand"
drv = GraphDatabase.driver(uri, auth=(user, pw))
with drv.session(database=db) as s:
    def q(c):
        return list(s.run(c))

    print("BETEILIGT_AN edge count total:", q("MATCH ()-[r:BETEILIGT_AN]->() RETURN count(r) AS c")[0]["c"])
    print("BETEILIGT_AN keys observed:")
    for r in q("MATCH ()-[r:BETEILIGT_AN]->() UNWIND keys(r) AS k RETURN k, count(*) AS c ORDER BY c DESC"):
        print(" ", r["k"], r["c"])
    print()
    print("Sample BETEILIGT_AN with all properties:")
    for r in q("MATCH (a)-[r:BETEILIGT_AN]->(b) RETURN labels(a)[0] AS a_label, labels(b)[0] AS b_label, properties(r) LIMIT 5"):
        print(" ", dict(r))
drv.close()
