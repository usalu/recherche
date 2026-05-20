"""Deeper probe for Phase 1.1 verifier.

Looks at evidence_basis breakdown by type for migration_origin='mig_1_1_demote_chains',
and pulls 5 sample edges PER type (with derivation_note) for the audit.
"""

import json
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "ENTWERFENMITBESTAND"
DB = "mit-bestand"


def main() -> None:
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    out = {}
    try:
        with driver.session(database=DB, default_access_mode="READ") as s:
            out["breakdown_by_type_basis"] = s.run(
                """
                MATCH ()-[r]->()
                WHERE r.migration_origin = 'mig_1_1_demote_chains'
                RETURN type(r) AS t, r.evidence_basis AS basis, count(r) AS n
                ORDER BY t, basis
                """
            ).data()

            out["samples_by_type"] = s.run(
                """
                MATCH (a)-[r]->(b)
                WHERE r.migration_origin = 'mig_1_1_demote_chains'
                WITH type(r) AS t, collect({
                    rel_type: type(r),
                    evidence_basis: r.evidence_basis,
                    evidence_source_id: r.evidence_source_id,
                    derivation_note: r.derivation_note,
                    evidence_origin: r.evidence_origin,
                    src: coalesce(a.id, elementId(a)),
                    dst: coalesce(b.id, elementId(b))
                })[0..2] AS samples
                RETURN t, samples
                ORDER BY t
                """
            ).data()

            row = s.run(
                """
                MATCH ()-[r]->()
                WHERE r.migration_origin = 'mig_1_1_demote_chains'
                  AND r.evidence_source_id IS NULL
                RETURN count(r) AS n
                """
            ).single()
            out["demoted_with_null_source_id"] = row["n"]

            row = s.run(
                """
                MATCH (k:Wiederverwendungskette)
                RETURN
                  sum(CASE WHEN exists{(k)-[:FROM_DONOR|AUS_BAUWERK]->()}
                           AND exists{(k)-[:INTO_RECEIVER|EINGEBAUT_IN]->()}
                           THEN 1 ELSE 0 END) AS wired_now,
                  count(k) AS total
                """
            ).single()
            out["chains_wired_via_new_or_old_types"] = {
                "total": row["total"],
                "wired": row["wired_now"],
            }

            out["surviving_chain_ids"] = [
                r["id"]
                for r in s.run(
                    "MATCH (k:Wiederverwendungskette) RETURN k.id AS id ORDER BY id"
                ).data()
            ]
    finally:
        driver.close()

    print(json.dumps(out, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
