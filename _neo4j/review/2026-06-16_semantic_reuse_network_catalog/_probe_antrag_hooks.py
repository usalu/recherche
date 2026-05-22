"""Probe graph for hooks that map to the Zukunft-Bau application."""

from __future__ import annotations

import sys
from pathlib import Path

from neo4j import GraphDatabase

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

QUERIES = {
    "bauteilboersen_present": """
        MATCH (a:Akteur)
        WHERE a.id IN ['concular','software_restado','restado','madaster','bauteilnetz_deutschland',
                       'bauteilnetz','opalis','cirkla']
        RETURN a.id AS id, a.name AS name
        ORDER BY id
    """,
    "claus_asam_present": """
        MATCH (a:Akteur)
        WHERE toLower(a.id) CONTAINS 'asam' OR toLower(a.name) CONTAINS 'asam'
        OPTIONAL MATCH (a)-[:BETEILIGT_AN]->(p:Projekt)
        RETURN a.id AS id, a.name AS name, collect(p.name) AS projects
    """,
    "plattenbau_projects": """
        MATCH (p:Projekt)
        WHERE toLower(p.id) CONTAINS 'platten' OR toLower(p.name) CONTAINS 'platten'
        RETURN p.id AS id, p.name AS name
    """,
    "bg_with_gwp": """
        MATCH (bg:Bauteilgruppe)
        WHERE bg.co2_beitrag_t IS NOT NULL OR bg.gwp IS NOT NULL OR bg.co2_einsparung_t IS NOT NULL
        RETURN count(bg) AS bgs_with_co2
    """,
    "bg_property_keys": """
        MATCH (bg:Bauteilgruppe)
        WITH bg LIMIT 400
        UNWIND keys(bg) AS k
        RETURN k AS property, count(*) AS n
        ORDER BY n DESC
        LIMIT 30
    """,
    "projekt_property_keys": """
        MATCH (p:Projekt)
        UNWIND keys(p) AS k
        RETURN k AS property, count(*) AS n
        ORDER BY n DESC
        LIMIT 30
    """,
    "software_nodes": """
        MATCH (sw:Software)
        RETURN sw.id AS id, sw.name AS name
        ORDER BY id
        LIMIT 40
    """,
    "regulation_questions": """
        MATCH (rf:Regulierungsfrage)
        RETURN rf.id AS id, rf.name AS name
        ORDER BY id
    """,
    "nachweis_forderungen": """
        MATCH (nf:Nachweisforderung)
        RETURN nf.id AS id, nf.name AS name
        ORDER BY id
    """,
    "label_counts": """
        MATCH (n)
        UNWIND labels(n) AS l
        RETURN l AS label, count(*) AS n
        ORDER BY n DESC
        LIMIT 40
    """,
    "k118_present": """
        MATCH (p:Projekt {id:'p_k118_kopfbau_halle_118_winterthur'})
        RETURN p.id AS id, p.name AS name, p.co2_einsparung_t AS co2_saved,
               p.wiederverwendungsrate_gewicht_prozent AS reuse_pct_weight
    """,
    "materialdepot": """
        MATCH (m:Materialdepot)
        RETURN count(m) AS depots
    """,
}


def main() -> None:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session(database=database) as session:
        for name, cypher in QUERIES.items():
            print(f"\n=== {name} ===")
            for row in session.run(cypher):
                print(dict(row))
    driver.close()


if __name__ == "__main__":
    main()
