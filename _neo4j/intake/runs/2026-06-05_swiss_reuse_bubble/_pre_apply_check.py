import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

uri, user, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(user, pw))
queries = {
    "gruner": "MATCH (n) WHERE n.id IN ['gruner_reuse','gruner_reuse_platform'] RETURN n.id AS id, labels(n) AS labels",
    "k118_stub": "MATCH (z:Akteur {id:'zirkular'})-[r]->(p:Projekt {id:'p_k118_kopfbau_halle_118_winterthur'}) RETURN r.id AS id, type(r) AS typ",
    "elys_stub": "MATCH (z:Akteur {id:'zirkular'})-[r]->(p:Projekt {id:'p_elys_kultur_gewerbehaus_basel'}) RETURN r.id AS id, type(r) AS typ",
    "benjamin_q": "MATCH (q {id:'q_actor_benjamin_poignon_03'}) RETURN q.id AS id",
    "eth": "MATCH (n:Akteur {id:'eth_zuerich'}) RETURN n.id AS id",
    "zirkular_proj": "MATCH (z:Akteur {id:'zirkular'})-[r]->(p:Projekt) RETURN type(r) AS typ, p.id AS pid, r.id AS rid LIMIT 10",
    "q_urls": "UNWIND ['q_url_0f6a8243ac5d1567100a3117bc4594e6','q_actor_benjamin_poignon_03','q_url_72047630eba27e60c1f672463457463e','q_url_83aa2d2f1524132cce8dcbac4e8fb774','q_url_c19e3aef6ee77ca6de0e75bf46654fb0'] AS qid OPTIONAL MATCH (n {id:qid}) RETURN qid, n.id AS found",
    "actors": "UNWIND ['cirkla','gruner_reuse_platform','useagain_bauteilclick'] AS aid OPTIONAL MATCH (n:Akteur {id:aid}) RETURN aid, n.id AS found",
}
with driver.session(database=db) as s:
    for name, q in queries.items():
        print(f"=== {name} ===")
        for rec in s.run(q):
            print(dict(rec))
driver.close()
