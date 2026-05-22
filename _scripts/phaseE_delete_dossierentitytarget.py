"""Phase E: delete the DossierEntityTarget staging layer.

Approved decision: the only source of truth is the direct BELEGT_IN links.
DossierEntityTarget nodes are dossier-row unfolding/matching scaffolding whose
only edges are CITED_FROM_DOSSIER (citation, fully redundant with BELEGT_IN -
all cited Quellen also have a direct BELEGT_IN) and EXACT_MATCH_CANDIDATE
(entity-matching staging). Deleting the nodes removes both edge types.

Dry-run by default. Live requires:  --confirm "PHASE_E TO mit-bestand"
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
    "MATCH (d:DossierEntityTarget) "
    "OPTIONAL MATCH (d)-[r]-() "
    "RETURN count(DISTINCT d) AS nodes, count(r) AS edges"
)
# Safety re-check: cited Quellen that would lose their ONLY provenance.
SAFETY = (
    "MATCH (q:Quelle)<-[:CITED_FROM_DOSSIER]-(:DossierEntityTarget) "
    "WHERE NOT (q)<-[:BELEGT_IN]-() "
    "RETURN count(DISTINCT q) AS quelle_losing_only_provenance"
)
DELETE = (
    "MATCH (d:DossierEntityTarget) "
    "CALL { WITH d DETACH DELETE d } IN TRANSACTIONS OF 2000 ROWS"
)
TOTALS = "MATCH (n) WITH count(n) AS nodes MATCH ()-[r]->() RETURN nodes, count(r) AS rels"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--confirm", default=None)
    args = ap.parse_args()

    uri, user, password, database = resolve_connection()
    from neo4j import GraphDatabase

    expected = f"PHASE_E TO {database}"
    live = args.confirm == expected
    if args.confirm and not live:
        raise SystemExit(f"Confirm must equal: {expected!r}")

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            di = session.run(COUNT).single()
            safety = session.run(SAFETY).single()["quelle_losing_only_provenance"]
            totals_before = session.run(TOTALS).single()
            result = {
                "mode": "live" if live else "dry-run",
                "dossierentitytarget_nodes": di["nodes"],
                "incident_edges": di["edges"],
                "quelle_losing_only_provenance": safety,
                "graph_before": {"nodes": totals_before["nodes"], "rels": totals_before["rels"]},
            }
            if safety and safety > 0:
                result["ABORT"] = "Refusing: some cited Quellen have no BELEGT_IN fallback."
                print(json.dumps(result, indent=2))
                return 1
            if live:
                session.run(DELETE).consume()
                remaining = session.run(
                    "MATCH (d:DossierEntityTarget) RETURN count(d) AS c"
                ).single()["c"]
                totals_after = session.run(TOTALS).single()
                result["remaining_dossierentitytarget"] = remaining
                result["graph_after"] = {"nodes": totals_after["nodes"], "rels": totals_after["rels"]}
            print(json.dumps(result, indent=2))
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
