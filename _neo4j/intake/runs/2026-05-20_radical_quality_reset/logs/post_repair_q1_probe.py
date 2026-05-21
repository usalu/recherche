import sys
sys.path.insert(0, r'E:/recherche/_scripts')
from neo4j_env import resolve_connection
from neo4j import GraphDatabase

uri, user, pw, _ = resolve_connection()
drv = GraphDatabase.driver(uri, auth=(user, pw))
with drv.session(database='mit-bestand') as s:
    q1_any = s.run(
        """
        MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(rec),
              (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg)
        WHERE r.evidence_origin='curated'
        RETURN count(*) AS c
        """
    ).single()['c']
    q1_bw = s.run(
        """
        MATCH (donor:Bauwerk)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(rec:Bauwerk),
              (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg)
        WHERE r.evidence_origin='curated'
        RETURN count(*) AS c
        """
    ).single()['c']
    topo = s.run(
        "MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(rec) RETURN count(*) AS c"
    ).single()['c']
    hat_curated = s.run(
        "MATCH ()-[r:HAT_BAUTEILGRUPPE]->() WHERE r.evidence_origin='curated' RETURN count(r) AS c"
    ).single()['c']
    bg_with_both = s.run(
        "MATCH (bg:Bauteilgruppe) WHERE exists{(bg)<-[:FROM_DONOR]-()} AND exists{(bg)-[:INTO_RECEIVER]->()} RETURN count(bg) AS c"
    ).single()['c']
    print('q1_any_donor_receiver_curated_HAT:', q1_any)
    print('q1_bauwerk_only_curated_HAT:', q1_bw)
    print('topology_only_donor_bg_receiver:', topo)
    print('hat_bauteilgruppe_curated_total:', hat_curated)
    print('bg_with_both_edges:', bg_with_both)
drv.close()
