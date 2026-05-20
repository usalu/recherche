"""Verify BETEILIGT_AN direction + raw_role_evidence content."""
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

    print("outgoing Akteur-[:BETEILIGT_AN]->():", q("MATCH (a:Akteur)-[r:BETEILIGT_AN]->() WHERE r.rolle_text IS NOT NULL RETURN count(r) AS c")[0]["c"])
    print("incoming ()-[:BETEILIGT_AN]->(Akteur):", q("MATCH ()-[r:BETEILIGT_AN]->(a:Akteur) WHERE r.rolle_text IS NOT NULL RETURN count(r) AS c")[0]["c"])
    print("either direction:", q("MATCH (a:Akteur)-[r:BETEILIGT_AN]-() WHERE r.rolle_text IS NOT NULL RETURN count(DISTINCT r) AS c")[0]["c"])
    print("sample edge:", q("MATCH (a)-[r:BETEILIGT_AN]->(b) WHERE r.rolle_text IS NOT NULL RETURN labels(a)[0] AS a_label, labels(b)[0] AS b_label, r.rolle_text LIMIT 5"))
    print("sample raw_role_evidence:", q("MATCH (a:Akteur) WHERE size(coalesce(a.raw_role_evidence,[])) > 0 RETURN a.id, a.raw_role_evidence LIMIT 5"))
    print("sample empty raw_role_evidence:", q("MATCH (a:Akteur) WHERE a.raw_role_evidence IS NOT NULL AND size(a.raw_role_evidence) = 0 RETURN count(a) AS c")[0]["c"])

drv.close()
