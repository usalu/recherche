"""Check rolle_text on edges that should NOT have been touched by migration."""
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
    for rid in [
        "r_bruxelles_proprete_net_brussel__BETEILIGT_AN__p_recypark_demets_anderlecht",
        "r_51n4e__BETEILIGT_AN__p_recypark_demets_anderlecht",
        "r_witteveen_bos__BETEILIGT_AN__p_recypark_demets_anderlecht",
        "r_bureau_greisch__BETEILIGT_AN__p_recypark_demets_anderlecht",
        "r_detang__BETEILIGT_AN__p_recypark_demets_anderlecht",
    ]:
        res = list(s.run(
            "MATCH ()-[r:BETEILIGT_AN {id: $rid}]->() RETURN properties(r) AS p",
            {"rid": rid},
        ))
        print(rid, res[0]["p"] if res else "NOT FOUND")
drv.close()
