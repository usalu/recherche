from __future__ import annotations
import sys
from pathlib import Path
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402
from neo4j import GraphDatabase  # noqa: E402

PROBES = {
    "projekt_keys": "MATCH (p:Projekt) WITH p LIMIT 400 UNWIND keys(p) AS k RETURN k, count(*) AS n ORDER BY n DESC",
    "bauwerk_keys": "MATCH (b:Bauwerk) WITH b LIMIT 400 UNWIND keys(b) AS k RETURN k, count(*) AS n ORDER BY n DESC",
    "kennwert_keys": "MATCH (k:Kennwert) WITH k LIMIT 400 UNWIND keys(k) AS kk RETURN kk AS k, count(*) AS n ORDER BY n DESC",
    "akteur_keys": "MATCH (a:Akteur) WITH a LIMIT 700 UNWIND keys(a) AS k RETURN k, count(*) AS n ORDER BY n DESC",
    "akteurtyp": "MATCH (a:Akteur)-[:HAT_AKTEURTYP]->(t) RETURN t.name AS typ, count(*) AS n ORDER BY n DESC",
    "reuse_status": "MATCH (bg:Bauteilgruppe) WHERE bg.reuse_status IS NOT NULL RETURN bg.reuse_status AS s, count(*) AS n ORDER BY n DESC",
    "kennwert_sample_co2": "MATCH (k:Kennwert) WHERE k.category='co2_saving' RETURN k.kennwert AS name, k.wert AS wert, k.einheit AS einheit LIMIT 15",
    "kennwert_sample_reuse": "MATCH (k:Kennwert) WHERE k.category='reuse_share' RETURN k.kennwert AS name, k.wert AS wert, k.einheit AS einheit LIMIT 15",
}

def main() -> None:
    uri, user, password, database = resolve_connection()
    drv = GraphDatabase.driver(uri, auth=(user, password))
    with drv.session(database=database) as s:
        for name, q in PROBES.items():
            print(f"\n=== {name} ===")
            for r in s.run(q):
                print("  ", dict(r))
    drv.close()

if __name__ == "__main__":
    main()
