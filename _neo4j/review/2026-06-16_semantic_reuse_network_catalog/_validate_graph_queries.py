"""Validate all graph catalog queries against live Neo4j."""

from __future__ import annotations

import sys
from pathlib import Path

from neo4j import GraphDatabase

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
sys.path.insert(0, str(REPO / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

from _graph_queries import GRAPH_NETWORKS  # noqa: E402


def main() -> None:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    failed = 0
    with driver.session(database=database) as session:
        for spec in GRAPH_NETWORKS:
            try:
                session.run(spec["cypher"].strip()).consume()
                print(f"OK  {spec['id']}")
            except Exception as exc:
                failed += 1
                print(f"FAIL {spec['id']}: {exc}")
    driver.close()
    if failed:
        raise SystemExit(f"{failed} query/queries failed")
    print(f"All {len(GRAPH_NETWORKS)} queries passed.")


if __name__ == "__main__":
    main()
