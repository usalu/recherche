"""Read-only verifier for Phase 1.1 (Verifier 1 of 12).

Connects to mit-bestand via the official Neo4j Python driver and runs the
five live-query checks from the verification spec. Prints a JSON result.
"""

import json
import sys

from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "ENTWERFENMITBESTAND"
DB = "mit-bestand"


def main() -> None:
    out = {}
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    try:
        with driver.session(database=DB, default_access_mode="READ") as s:
            # check 5
            r = s.run("MATCH (k:Wiederverwendungskette) RETURN count(k) AS n").single()
            out["chains_total"] = r["n"]

            # check 6
            r = s.run(
                """
                MATCH (k:Wiederverwendungskette)
                WHERE NOT (exists{(k)-[:FROM_DONOR|AUS_BAUWERK]->()} AND exists{(k)-[:INTO_RECEIVER|EINGEBAUT_IN]->()})
                RETURN count(k) AS n
                """
            ).single()
            out["chains_unwired"] = r["n"]

            # check 7
            r = s.run(
                """
                MATCH ()-[r]->()
                WHERE r.migration_origin = 'mig_1_1_demote_chains'
                RETURN count(r) AS n
                """
            ).single()
            out["demoted_edges_total"] = r["n"]

            # breakdown by type for the report
            rows = s.run(
                """
                MATCH ()-[r]->()
                WHERE r.migration_origin = 'mig_1_1_demote_chains'
                RETURN type(r) AS t, count(r) AS n ORDER BY n DESC
                """
            ).data()
            out["demoted_edges_by_type"] = rows

            # check 8 — sample five demoted edges, confirm evidence_basis + evidence_source_id
            samples = s.run(
                """
                MATCH (a)-[r]->(b)
                WHERE r.migration_origin = 'mig_1_1_demote_chains'
                RETURN type(r) AS rel_type,
                       r.evidence_basis AS evidence_basis,
                       r.evidence_source_id AS evidence_source_id,
                       coalesce(a.id, elementId(a)) AS src,
                       coalesce(b.id, elementId(b)) AS dst
                ORDER BY rel_type, src
                LIMIT 5
                """
            ).data()
            out["sample_demoted_edges"] = samples

            # extra: confirm every demoted edge has the two required fields
            r = s.run(
                """
                MATCH ()-[r]->()
                WHERE r.migration_origin = 'mig_1_1_demote_chains'
                  AND (r.evidence_basis <> 'demoted_from_kette'
                       OR r.evidence_source_id IS NULL)
                RETURN count(r) AS n
                """
            ).single()
            out["demoted_edges_with_missing_provenance"] = r["n"]

            # extra: confirm chain wiring on remaining chains
            r = s.run(
                """
                MATCH (k:Wiederverwendungskette)
                RETURN
                  sum(CASE WHEN exists{(k)-[:AUS_BAUWERK]->()}
                           AND exists{(k)-[:EINGEBAUT_IN]->()}
                           THEN 1 ELSE 0 END) AS wired
                """
            ).single()
            out["chains_wired"] = r["wired"]
    finally:
        driver.close()

    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
