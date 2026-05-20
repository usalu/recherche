"""Quick schema probe — print rel types between specific label pairs."""
from __future__ import annotations
import io
import sys
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402
from neo4j import GraphDatabase  # noqa: E402

PROBES = [
    ("Akteur", "Projekt"),
    ("Projekt", "Stadt"),
    ("Projekt", "Land"),
    ("Projekt", "Programm"),
    ("Projekt", "Marktmodell"),
    ("Projekt", "MatchingQualitaet"),
    ("Bauteilgruppe", "Marktmodell"),
    ("Bauteilgruppe", "Materialgruppe"),
    ("Bauteilgruppe", "Bauteiltyp"),
    ("Bauteilgruppe", "Norm"),
    ("Bauteilgruppe", "Quelle"),
    ("Bauwerk", "Quelle"),
    ("Akteur", "Norm"),
    ("Akteur", "Software"),
    ("Akteur", "Tool"),
    ("Projekt", "Software"),
    ("Projekt", "Tool"),
    ("Stadt", "Land"),
]

uri, user, password, db = resolve_connection()
drv = GraphDatabase.driver(uri, auth=(user, password))
with drv.session(database=db) as s:
    print("LABEL COUNTS:")
    for lbl in ["Akteur", "Projekt", "Bauwerk", "Bauteilgruppe", "Material",
                "Materialgruppe", "Stadt", "Land", "Programm", "Norm",
                "Software", "Tool", "Quelle", "Wiederverwendungskette",
                "Marktmodell", "MatchingQualitaet"]:
        r = s.run(f"MATCH (n:{lbl}) RETURN count(n) AS c").single()
        print(f"  {lbl:30s} {r['c']}")
    print("\nDIRECTED REL TYPES BETWEEN PAIRS (a-->b only):")
    for a, b in PROBES:
        rs = s.run(
            f"MATCH (x:{a})-[r]->(y:{b}) "
            f"RETURN type(r) AS t, count(*) AS c ORDER BY c DESC"
        )
        rels = [(rec["t"], rec["c"]) for rec in rs]
        print(f"  ({a})-->({b}):  {rels}")
        rs2 = s.run(
            f"MATCH (x:{a})<-[r]-(y:{b}) "
            f"RETURN type(r) AS t, count(*) AS c ORDER BY c DESC"
        )
        rels2 = [(rec["t"], rec["c"]) for rec in rs2]
        print(f"  ({a})<--({b}):  {rels2}")
drv.close()
