import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j_env import resolve_connection
from neo4j import GraphDatabase

uri, u, p, d = resolve_connection()
drv = GraphDatabase.driver(uri, auth=(u, p))
with drv.session(database=d) as s:
    queries = {
        "wk_count": "MATCH (wk:Wiederverwendungskette) RETURN count(wk) AS c",
        "aus": "MATCH ()-[r:AUS_SPENDER]->() RETURN count(r) AS c",
        "in_emp": "MATCH ()-[r:IN_EMPFANGSOBJEKT]->() RETURN count(r) AS c",
        "wk_sample": "MATCH (wk:Wiederverwendungskette) RETURN wk.id LIMIT 3",
        "wk_rels": """
            MATCH (wk:Wiederverwendungskette)-[r]-(n)
            RETURN type(r) AS rel, labels(n)[0] AS label, count(*) AS c
            ORDER BY c DESC LIMIT 15
        """,
        "useagain": "MATCH (a:Akteur) WHERE a.id CONTAINS 'useagain' RETURN a.id LIMIT 5",
        "cstb": "MATCH (a:Akteur) WHERE a.id CONTAINS 'cstb' RETURN a.id LIMIT 5",
        "gm": "MATCH ()-[r:HAT_GESCHAEFTSMODELL]->(x) RETURN labels(x)[0], count(r) AS c",
        "path_test": """
            MATCH (a:Akteur {id:'useagain_bauteilclick'}), (b:Akteur {id:'cstb'})
            RETURN a.id, b.id
        """,
        "donor_pattern": """
            MATCH (donor)-[r:AUS_SPENDER]->(target)
            RETURN labels(donor)[0] AS donor_label, labels(target)[0] AS target_label, count(*) AS c
            ORDER BY c DESC LIMIT 10
        """,
        "receiver_pattern": """
            MATCH (src)-[r:IN_EMPFANGSOBJEKT]->(recv)
            RETURN labels(src)[0] AS src_label, labels(recv)[0] AS recv_label, count(*) AS c
            ORDER BY c DESC LIMIT 10
        """,
        "path": """
            MATCH p = shortestPath(
              (:Akteur {id:'useagain_bauteilclick'})-[:VERBUNDEN_MIT_AKTEUR*..12]-(:Akteur {id:'cstb'})
            )
            RETURN [n IN nodes(p) | n.id] AS hops, length(p) AS distance
        """,
        "vma_tagged": """
            MATCH ()-[r:VERBUNDEN_MIT_AKTEUR]->()
            WHERE r.review_run IS NOT NULL
            RETURN count(r) AS tagged, count(*) FILTER (WHERE r.review_run IS NULL) AS untagged
        """,
        "gm_nodes": """
            MATCH (p:Projekt)-[:HAT_GESCHAEFTSMODELL]->(gm:Geschaeftsmodell)
            RETURN gm.id AS id, gm.name AS name, count(DISTINCT p) AS projects
            ORDER BY projects DESC LIMIT 10
        """,
    }
    for name, q in queries.items():
        rows = [dict(r) for r in s.run(q)]
        print(name, rows)
drv.close()
