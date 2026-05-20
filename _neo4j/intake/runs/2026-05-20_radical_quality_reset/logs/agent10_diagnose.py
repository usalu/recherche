"""Diagnose the 47 Akteur->BELEGT_IN->q_actor_url edges that didn't get
canonicalised by Agent 10's first pass.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

REPO_ROOT = Path(r"E:/recherche")


def main() -> int:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection  # type: ignore
    from neo4j import GraphDatabase  # type: ignore

    uri, user, password, database = resolve_connection()
    if database != "mit-bestand":
        database = "mit-bestand"

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        with driver.session(database=database) as s:
            rows = s.run(
                """
                MATCH (a:Akteur)-[r:BELEGT_IN]->(q:Quelle)
                WHERE q.quelltyp='external_link_from_actor_registry'
                  AND NOT (
                       r.evidence_origin='curated'
                   AND r.evidence_basis='cell_citation'
                   AND r.evidence_confidence='belegt')
                RETURN a.id AS akteur, q.id AS quelle,
                       r.evidence_origin AS origin,
                       r.evidence_basis AS basis,
                       r.evidence_confidence AS conf,
                       r.evidence_source_id AS sid,
                       r.id AS rid
                """
            ).data()
            print(f"total non-canonical: {len(rows)}")
            for row in rows[:25]:
                print(json.dumps(row, default=str))
            # bucket by (origin,basis,conf)
            buckets = {}
            for row in rows:
                k = (row["origin"], row["basis"], row["conf"])
                buckets[k] = buckets.get(k, 0) + 1
            print("\nbuckets:")
            for k, v in sorted(buckets.items(), key=lambda x: -x[1]):
                print(f"  {k}: {v}")
            # which actors?
            akts = set(r["akteur"] for r in rows)
            print(f"\ndistinct akteurs: {len(akts)}")
            for a in sorted(akts)[:25]:
                print(f"  {a}")
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
