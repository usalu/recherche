"""Post-apply gap check for round 004."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j_env import resolve_connection
from neo4j import GraphDatabase

uri, user, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(user, pw))
with driver.session(database=db) as s:
    # projects with no component or work links
    rows = s.run(
        "MATCH (p:Projekt) "
        "WHERE NOT EXISTS {(p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)} "
        "AND NOT EXISTS {(p)-[:HAT_BAUARBEIT]->()} "
        "RETURN p.id AS pid, p.name AS name"
    ).data()
    print("projects_no_comp_or_work:", len(rows))
    for r in rows:
        print(" ", r.get("pid"), r.get("name"))

    # deferred unknown-donor Bauteilgruppen
    rows2 = s.run(
        "MATCH (bg:Bauteilgruppe) "
        "WHERE bg.donor_resolution_status = 'unknown' "
        "RETURN bg.id AS bgid, bg.name AS name "
        "ORDER BY bgid"
    ).data()
    print("unknown_donor_status:", len(rows2))
    for r in rows2:
        print(" ", r.get("bgid"))

    # resource_source (resolved but no exact building)
    rows3 = s.run(
        "MATCH (bg:Bauteilgruppe) "
        "WHERE bg.donor_resolution_status = 'resource_source' "
        "RETURN count(bg) AS c"
    ).single()
    print("resource_source_resolved:", rows3["c"])

    # exact_building + same_site
    rows4 = s.run(
        "MATCH (bg:Bauteilgruppe) "
        "WHERE bg.donor_resolution_status IN ['exact_building','same_site'] "
        "RETURN bg.donor_resolution_status AS s, count(bg) AS c"
    ).data()
    for r in rows4:
        print(f"  {r['s']}: {r['c']}")

driver.close()
