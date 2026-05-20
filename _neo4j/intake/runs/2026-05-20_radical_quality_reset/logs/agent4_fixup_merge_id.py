"""Post-merge fixup: apoc.refactor.mergeNodes with properties:'combine'
turned the scalar `id` property into a list for each merged :Akteur.
Reset it to the canonical scalar (the merge-target id)."""

from pathlib import Path
import sys
from datetime import datetime, timezone

REPO_ROOT = Path(r"E:/recherche")
sys.path.insert(0, str(REPO_ROOT / "_scripts"))
from neo4j_env import resolve_connection  # type: ignore
from neo4j import GraphDatabase  # type: ignore

uri, user, pw, _db = resolve_connection()
db = "mit-bestand"

# (canonical_id, expected element that proves this node is the merged target)
CANON_IDS = [
    "baubuero_in_situ",
    "plp_architecture",
    "ZRS_Architekten_Ingenieure",
    "loeliger_strub",
    "zedfactory_bill_dunster",
    "opera",
    "bellastock",
]

driver = GraphDatabase.driver(uri, auth=(user, pw))
try:
    with driver.session(database=db) as s:
        # 1. Inspect: which Akteur have a list id (using apoc.meta.cypher.type).
        rows = list(s.run(
            "MATCH (a:Akteur) "
            "WHERE a.id IS NOT NULL "
            "  AND apoc.meta.cypher.type(a.id) IN ['LIST OF STRING NOT NULL','STRING LIST','LIST OF STRING'] "
            "RETURN a.id AS id_list, a.aliases AS aliases, a.name AS name"
        ))
        print("nodes with list-typed id (pre-fix):", len(rows))
        for r in rows:
            print(" ", r["name"], "->", r["id_list"], "aliases=", r["aliases"])

        # 2. Fix: for each canonical id, find the matching node and set id := canonical scalar.
        for canon in CANON_IDS:
            res = s.run(
                "MATCH (a:Akteur) "
                "WHERE apoc.meta.cypher.type(a.id) IN "
                "      ['LIST OF STRING NOT NULL','STRING LIST','LIST OF STRING'] "
                "  AND $canon IN a.id "
                "SET a.id = $canon "
                "RETURN a.id AS id, a.aliases AS aliases, a.name AS name",
                canon=canon,
            ).single()
            if res:
                print(f"FIX: {res['name']!r} -> id={res['id']!r}, aliases={res['aliases']}")
            else:
                print(f"noop: {canon}")

        # 3. Verify no list-typed ids remain on Akteur.
        leftover = s.run(
            "MATCH (a:Akteur) "
            "WHERE apoc.meta.cypher.type(a.id) IN "
            "      ['LIST OF STRING NOT NULL','STRING LIST','LIST OF STRING'] "
            "RETURN count(a) AS c"
        ).single()["c"]
        print("remaining list-typed Akteur.id:", leftover)

        # 4. Spot-check each merged canon node.
        for canon in CANON_IDS:
            row = s.run(
                "MATCH (a:Akteur {id:$canon}) "
                "RETURN a.id AS id, a.name AS name, a.aliases AS aliases, "
                "       size([(a)--() | 1]) AS degree",
                canon=canon,
            ).single()
            if row:
                print(f"  OK  {row['id']:<32} deg={row['degree']:>3} name={row['name']!r} aliases={row['aliases']}")
            else:
                print(f"  MISSING {canon}")
finally:
    driver.close()
