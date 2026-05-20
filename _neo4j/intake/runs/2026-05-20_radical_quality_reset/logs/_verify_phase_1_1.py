"""Independent acceptance verification for Phase 1.1."""
import sys
sys.path.insert(0, r"E:/recherche/_scripts")
from neo4j_env import resolve_connection
from neo4j import GraphDatabase

uri, user, pw, _ = resolve_connection()
drv = GraphDatabase.driver(uri, auth=(user, pw))
with drv.session(database="mit-bestand") as s:
    total = s.run("MATCH (k:Wiederverwendungskette) RETURN count(k) AS n").single()["n"]
    wired = s.run(
        "MATCH (k:Wiederverwendungskette) "
        "WHERE exists{(k)-[:AUS_BAUWERK]->()} AND exists{(k)-[:EINGEBAUT_IN]->()} "
        "RETURN count(k) AS n"
    ).single()["n"]
    print(f"total Wiederverwendungskette: {total}")
    print(f"fully wired (AUS_BAUWERK+EINGEBAUT_IN): {wired}")

    demoted = s.run(
        "MATCH ()-[r]->() WHERE r.migration_origin = 'mig_1_1_demote_chains' "
        "RETURN type(r) AS t, count(r) AS n ORDER BY n DESC"
    )
    print("\ndemoted edges (migration_origin='mig_1_1_demote_chains'):")
    total_demoted = 0
    for row in demoted:
        print(f"  {row['t']}: {row['n']}")
        total_demoted += row["n"]
    print(f"  total: {total_demoted}")

    by_basis = s.run(
        "MATCH ()-[r]->() WHERE r.evidence_basis = 'demoted_from_kette' "
        "RETURN count(r) AS n"
    ).single()["n"]
    print(f"\nedges with evidence_basis='demoted_from_kette': {by_basis}")

    print("\nremaining 14 chain IDs:")
    for row in s.run("MATCH (k:Wiederverwendungskette) RETURN k.id AS id ORDER BY k.id"):
        print(f"  {row['id']}")
drv.close()
