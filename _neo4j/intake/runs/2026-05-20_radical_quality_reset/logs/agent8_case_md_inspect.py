"""Agent 8 — inspect the live :Quelle nodes with quelltyp='case_markdown'
so we can wire each dossier file to its existing q_<slug>_md node id."""
from __future__ import annotations
import json, sys
from pathlib import Path
REPO_ROOT = Path(r"E:/recherche")
sys.path.insert(0, str(REPO_ROOT / "_scripts"))
from neo4j_env import resolve_connection  # type: ignore
from neo4j import GraphDatabase  # type: ignore

uri,user,pw,db = resolve_connection()
db = "mit-bestand"
d = GraphDatabase.driver(uri, auth=(user,pw)); d.verify_connectivity()
s = d.session(database=db)
rows = list(s.run(
    "MATCH (q:Quelle) WHERE q.quelltyp IN ['case_markdown','research_markdown'] "
    "RETURN q.id AS id, q.quelltyp AS qt, q.name AS name, q.source_file AS sf "
    "ORDER BY q.quelltyp, q.id"
))
out = [{"id":r["id"],"quelltyp":r["qt"],"name":r["name"],"source_file":r["sf"]} for r in rows]
print(json.dumps({"count": len(out), "rows": out}, indent=2, ensure_ascii=False))
s.close(); d.close()
