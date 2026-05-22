"""Phase C: remove topology-duplicate node properties after migrating edges.

Edges created first (idempotent MERGE) so no relationship is lost:
  Bauteilgruppe.primary_material_id -> (BG)-[:NUTZT_MATERIAL]->(:Material {id})
  Akteur.land (ISO2)                -> (Akteur)-[:LIEGT_IN_LAND]->(:Land {country_iso2})
  Bauwerk/Materialdepot.land (name) -> (n)-[:LIEGT_IN_LAND]->(:Land {name})

Then drop:
  Bauteilgruppe: primary_material_id, primary_bauteiltyp_id  (HAT_BAUTEILTYP already 100%)
  Akteur:        land
  Bauwerk:       land
  Materialdepot: land

Dry-run by default. Live requires:  --confirm "PHASE_C TO mit-bestand"
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402

MERGE_MATERIAL = (
    "MATCH (b:Bauteilgruppe) WHERE b.primary_material_id IS NOT NULL "
    "AND NOT (b)-[:NUTZT_MATERIAL]->(:Material) "
    "MATCH (m:Material {id: b.primary_material_id}) "
    "MERGE (b)-[r:NUTZT_MATERIAL]->(m) RETURN count(r) AS edges"
)
MERGE_AKTEUR_LAND = (
    "MATCH (a:Akteur) WHERE a.land IS NOT NULL "
    "AND NOT (a)-[:LIEGT_IN_LAND]->(:Land) "
    "MATCH (l:Land {country_iso2: a.land}) "
    "MERGE (a)-[r:LIEGT_IN_LAND]->(l) RETURN count(r) AS edges"
)
MERGE_BW_MD_LAND = (
    "MATCH (n) WHERE (n:Bauwerk OR n:Materialdepot) AND n.land IS NOT NULL "
    "AND NOT (n)-[:LIEGT_IN_LAND]->(:Land) "
    "MATCH (l:Land) WHERE l.name = n.land "
    "MERGE (n)-[r:LIEGT_IN_LAND]->(l) RETURN count(r) AS edges"
)
DROP_BG = "MATCH (b:Bauteilgruppe) REMOVE b.primary_material_id, b.primary_bauteiltyp_id"
DROP_AKTEUR = "MATCH (a:Akteur) REMOVE a.land"
DROP_BW = "MATCH (b:Bauwerk) REMOVE b.land"
DROP_MD = "MATCH (m:Materialdepot) REMOVE m.land"

PROBE = {
    "bg_primary_material_id": "MATCH (b:Bauteilgruppe) WHERE b.primary_material_id IS NOT NULL RETURN count(b) AS c",
    "bg_primary_bauteiltyp_id": "MATCH (b:Bauteilgruppe) WHERE b.primary_bauteiltyp_id IS NOT NULL RETURN count(b) AS c",
    "akteur_land": "MATCH (a:Akteur) WHERE a.land IS NOT NULL RETURN count(a) AS c",
    "bw_md_land": "MATCH (n) WHERE (n:Bauwerk OR n:Materialdepot) AND n.land IS NOT NULL RETURN count(n) AS c",
    "bg_nutzt_material": "MATCH (:Bauteilgruppe)-[r:NUTZT_MATERIAL]->() RETURN count(r) AS c",
    "akteur_liegt_in_land": "MATCH (:Akteur)-[r:LIEGT_IN_LAND]->() RETURN count(r) AS c",
}


def probe(session) -> dict:
    return {k: session.run(q).single()["c"] for k, q in PROBE.items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--confirm", default=None)
    args = ap.parse_args()

    uri, user, password, database = resolve_connection()
    from neo4j import GraphDatabase

    expected = f"PHASE_C TO {database}"
    live = args.confirm == expected
    if args.confirm and not live:
        raise SystemExit(f"Confirm must equal: {expected!r}")

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            result = {"mode": "live" if live else "dry-run", "before": probe(session)}
            if live:
                result["edges_merged"] = {
                    "nutzt_material": session.run(MERGE_MATERIAL).single()["edges"],
                    "akteur_land": session.run(MERGE_AKTEUR_LAND).single()["edges"],
                    "bw_md_land": session.run(MERGE_BW_MD_LAND).single()["edges"],
                }
                for q in (DROP_BG, DROP_AKTEUR, DROP_BW, DROP_MD):
                    session.run(q).consume()
                result["after"] = probe(session)
            print(json.dumps(result, indent=2))
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
