import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

uri, user, pw, db = resolve_connection()
d = GraphDatabase.driver(uri, auth=(user, pw))
with d.session(database=db) as s:
    print("=== TEIL_VON_PROGRAMM sample ===")
    for r in s.run(
        """
        MATCH (p:Projekt)-[:TEIL_VON_PROGRAMM]->(pr:Programm)
        WHERE pr.id IN ['prog_re_use_hoefe','prog_reallabor_be_ware','prog_interreg_nwe','prog_fcrbe','prog_preuse']
        RETURN pr.id, count(p) AS n, collect(p.id)[0..8] AS sample
        """
    ):
        print(dict(r))

    print("\n=== orphan program projekte with geo ===")
    for r in s.run(
        """
        MATCH (a:Akteur)-[:BETEILIGT_AN]->(pr:Programm)
        WHERE a.id IN ['edith_maryon_stift','heinrich_boell_stiftung','koimo_development']
        OPTIONAL MATCH (p:Projekt)-[:TEIL_VON_PROGRAMM]->(pr)
        RETURN a.id AS actor, pr.id AS program, collect({id:p.id, name:p.name, adresse:p.adresse}) AS projekte
        """
    ):
        print(dict(r))

    print("\n=== interreg actor ===")
    for r in s.run(
        """
        MATCH (a:Akteur {id:'interreg_nwe'})
        OPTIONAL MATCH (a)-[r]-(n)
        RETURN type(r), labels(n), n.id, n.name
        """
    ):
        print(dict(r))

    print("\n=== bauwerk paths for orphans ===")
    for r in s.run(
        """
        UNWIND ['mamout_architectes','superuse_on_site'] AS aid
        MATCH (a:Akteur {id:aid})
        OPTIONAL MATCH (a)-[:NUTZT_BAUWERK|HAT_BAUWERK]->(b:Bauwerk)
        RETURN aid, collect({id:b.id, adresse:b.adresse}) AS bauwerke
        """
    ):
        print(dict(r))

d.close()
