"""Find where rolle_text lives now (or used to)."""
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

    print("any edge with rolle_text:", q("MATCH ()-[r]->() WHERE r.rolle_text IS NOT NULL RETURN type(r) AS t, count(r) AS c ORDER BY c DESC")[:10])
    print()
    print("BETEILIGT_AN sample with evidence_excerpt set:")
    for r in q("MATCH (a:Akteur)-[r:BETEILIGT_AN]->(b) WHERE r.evidence_excerpt IS NOT NULL RETURN a.id, b.id, r.evidence_excerpt, r.evidence_basis, r.evidence_origin LIMIT 6"):
        print(" ", dict(r))
    print()
    print("BETEILIGT_AN with evidence_basis distribution:")
    for r in q("MATCH ()-[r:BETEILIGT_AN]->() RETURN r.evidence_basis AS b, count(r) AS c ORDER BY c DESC"):
        print(" ", r["b"], r["c"])

drv.close()
