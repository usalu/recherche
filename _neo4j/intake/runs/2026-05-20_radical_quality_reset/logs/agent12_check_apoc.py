"""Check apoc availability + sample reuse_share_facts representation."""
from __future__ import annotations
import json, sys
from pathlib import Path
REPO_ROOT = Path(r"E:/recherche")

def main():
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection
    from neo4j import GraphDatabase
    uri, user, pw, db = resolve_connection()
    db = "mit-bestand"
    drv = GraphDatabase.driver(uri, auth=(user, pw))
    with drv.session(database=db) as s:
        try:
            rec = s.run("RETURN apoc.version() AS v").single()
            print("apoc.version =", rec["v"])
        except Exception as e:
            print("apoc.version failed:", e)
        sample = list(s.run(
            "MATCH (p:Projekt) WHERE size(coalesce(p.reuse_share_facts,[]))>0 "
            "RETURN p.id AS id, p.reuse_share_facts AS rs LIMIT 3"
        ))
        for r in sample:
            print("\nproject:", r["id"])
            for entry in r["rs"]:
                print(" entry:", repr(entry)[:300])
        sample2 = list(s.run(
            "MATCH (p:Projekt) WHERE size(coalesce(p.co2_facts,[]))>0 "
            "RETURN p.id AS id, p.co2_facts AS rs LIMIT 3"
        ))
        print("\n--- co2_facts ---")
        for r in sample2:
            print("\nproject:", r["id"])
            for entry in r["rs"]:
                print(" entry:", repr(entry)[:300])
    drv.close()

if __name__ == "__main__":
    main()
