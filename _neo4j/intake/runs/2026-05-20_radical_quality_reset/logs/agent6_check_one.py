"""Direct query of two specific edges from snapshot."""
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
        "r_abn_amro__BETEILIGT_AN__p_circl_abn_amro",
        "r_bam_bouw_techniek__BETEILIGT_AN__p_circl_abn_amro",
        "r_tu_delft__BETEILIGT_AN__p_circl_abn_amro",
        "r_big_bundesimmobilien__BETEILIGT_AN__p_meduni_campus_mariannengasse",
    ]:
        res = list(s.run(
            "MATCH ()-[r:BETEILIGT_AN {id: $rid}]->() RETURN properties(r) AS p",
            {"rid": rid},
        ))
        print(rid, res[0]["p"] if res else "MISSING")
drv.close()
