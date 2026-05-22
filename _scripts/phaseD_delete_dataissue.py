"""Phase D: delete the DataIssue audit ledger (nodes + incident edges).

Approved decision: DataIssue is an audit/meta label, not semantic graph content.
Deleting it (DETACH DELETE) makes the graph semantic. Batched via
CALL { ... } IN TRANSACTIONS so the delete does not run as one huge transaction.

Dry-run by default. Live requires:  --confirm "PHASE_D TO mit-bestand"
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402

COUNT = (
    "MATCH (d:DataIssue) OPTIONAL MATCH (d)-[r]-() "
    "RETURN count(DISTINCT d) AS nodes, count(r) AS edges"
)
DELETE = (
    "MATCH (d:DataIssue) "
    "CALL { WITH d DETACH DELETE d } IN TRANSACTIONS OF 2000 ROWS"
)
TOTALS = "MATCH (n) WITH count(n) AS nodes MATCH ()-[r]->() RETURN nodes, count(r) AS rels"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--confirm", default=None)
    args = ap.parse_args()

    uri, user, password, database = resolve_connection()
    from neo4j import GraphDatabase

    expected = f"PHASE_D TO {database}"
    live = args.confirm == expected
    if args.confirm and not live:
        raise SystemExit(f"Confirm must equal: {expected!r}")

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            di = session.run(COUNT).single()
            totals_before = session.run(TOTALS).single()
            result = {
                "mode": "live" if live else "dry-run",
                "dataissue_nodes": di["nodes"],
                "dataissue_incident_edges": di["edges"],
                "graph_before": {"nodes": totals_before["nodes"], "rels": totals_before["rels"]},
            }
            if live:
                # CALL IN TRANSACTIONS must run in an implicit (auto-commit) tx.
                session.run(DELETE).consume()
                remaining = session.run("MATCH (d:DataIssue) RETURN count(d) AS c").single()["c"]
                totals_after = session.run(TOTALS).single()
                result["remaining_dataissue"] = remaining
                result["graph_after"] = {"nodes": totals_after["nodes"], "rels": totals_after["rels"]}
            print(json.dumps(result, indent=2))
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
