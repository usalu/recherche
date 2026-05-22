"""Probe relationship types for the 8 core snapshot queries."""

from __future__ import annotations

import sys
from pathlib import Path

from neo4j import GraphDatabase

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

QUERIES = {
    "rel_types_all": """
        CALL db.relationshipTypes() YIELD relationshipType
        RETURN relationshipType ORDER BY relationshipType
    """,
    "bg_outgoing_rels": """
        MATCH (bg:Bauteilgruppe)-[r]->(m)
        RETURN type(r) AS rel, labels(m) AS target, count(*) AS n
        ORDER BY n DESC LIMIT 30
    """,
    "bg_incoming_rels": """
        MATCH (bg:Bauteilgruppe)<-[r]-(m)
        RETURN type(r) AS rel, labels(m) AS source, count(*) AS n
        ORDER BY n DESC LIMIT 30
    """,
    "kennwert_context": """
        MATCH (k:Kennwert)<-[r]-(m)
        RETURN type(r) AS rel, labels(m) AS source, count(*) AS n
        ORDER BY n DESC LIMIT 20
    """,
    "kennwert_props": """
        MATCH (k:Kennwert) UNWIND keys(k) AS key
        RETURN key, count(*) AS n ORDER BY n DESC LIMIT 25
    """,
    "regfrage_rels": """
        MATCH (rf:Regulierungsfrage)-[r]-(m)
        RETURN type(r) AS rel, labels(m) AS other,
               CASE WHEN startNode(r)=rf THEN 'out' ELSE 'in' END AS dir,
               count(*) AS n
        ORDER BY n DESC LIMIT 30
    """,
    "nachweis_rels": """
        MATCH (nf:Nachweisforderung)-[r]-(m)
        RETURN type(r) AS rel, labels(m) AS other,
               CASE WHEN startNode(r)=nf THEN 'out' ELSE 'in' END AS dir,
               count(*) AS n
        ORDER BY n DESC LIMIT 30
    """,
    "law_gilt_in_land": """
        MATCH (l)-[r:GILT_IN_LAND|GILT_IN]->(land:Land)
        RETURN type(r) AS rel, labels(l) AS lawlabels, count(*) AS n
        ORDER BY n DESC LIMIT 30
    """,
    "huerde_rels": """
        MATCH (h:Huerde)-[r]-(m)
        RETURN type(r) AS rel, labels(m) AS other,
               CASE WHEN startNode(r)=h THEN 'out' ELSE 'in' END AS dir,
               count(*) AS n
        ORDER BY n DESC LIMIT 30
    """,
    "k118_bg_sample": """
        MATCH (p:Projekt {id:'p_k118_kopfbau_halle_118_winterthur'})-[r]->(bg:Bauteilgruppe)
        RETURN type(r) AS rel, bg.id AS bg_id, bg.name AS name, bg.alte_funktion AS alt,
               bg.neue_funktion AS neu, bg.tragend AS tragend
        LIMIT 25
    """,
    "actor_country_rel": """
        MATCH (a:Akteur)-[r]->(land:Land)
        RETURN type(r) AS rel, count(*) AS n ORDER BY n DESC LIMIT 10
    """,
    "donor_receiver_rels": """
        MATCH (bg:Bauteilgruppe)-[r:AUS_SPENDER|IN_EMPFANGSOBJEKT|AUS_SPENDEROBJEKT]->(b)
        RETURN type(r) AS rel, labels(b) AS target, count(*) AS n
        ORDER BY n DESC LIMIT 10
    """,
}


def main() -> None:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session(database=database) as session:
        for name, cypher in QUERIES.items():
            print(f"\n=== {name} ===")
            try:
                for row in session.run(cypher):
                    print(dict(row))
            except Exception as exc:  # noqa: BLE001
                print(f"ERROR: {exc}")
    driver.close()


if __name__ == "__main__":
    main()
