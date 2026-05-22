"""Phase B: migrate Kennwert/Norm provenance to BELEGT_IN edges, then drop props.

Kennwert and Norm carry their only provenance as node properties (no BELEGT_IN
edges). Before removing those properties we create the edges so provenance is
preserved on the graph topology.

  Kennwert.source_id          -> (Kennwert)-[:BELEGT_IN]->(source node)
  Norm.evidence_source_id     -> (Norm)-[:BELEGT_IN]->(source node)

Then drop:
  Kennwert: source_id, source_urls, primary_source_url
  Norm:     evidence_source_id, evidence_origin, evidence_confidence, evidence_basis

Dry-run by default. Live requires:  --confirm "PHASE_B TO mit-bestand"
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

MERGE_KENNWERT = (
    "MATCH (k:Kennwert) WHERE k.source_id IS NOT NULL "
    "MATCH (q {id: k.source_id}) "
    "MERGE (k)-[r:BELEGT_IN]->(q) RETURN count(r) AS edges"
)
MERGE_NORM = (
    "MATCH (n:Norm) WHERE n.evidence_source_id IS NOT NULL "
    "MATCH (q {id: n.evidence_source_id}) "
    "MERGE (n)-[r:BELEGT_IN]->(q) RETURN count(r) AS edges"
)
DROP_KENNWERT = "MATCH (k:Kennwert) REMOVE k.source_id, k.source_urls, k.primary_source_url"
DROP_NORM = (
    "MATCH (n:Norm) REMOVE n.evidence_source_id, n.evidence_origin, "
    "n.evidence_confidence, n.evidence_basis"
)

PROBE = {
    "kennwert_source_id": "MATCH (k:Kennwert) WHERE k.source_id IS NOT NULL RETURN count(k) AS c",
    "norm_evidence_source_id": "MATCH (n:Norm) WHERE n.evidence_source_id IS NOT NULL RETURN count(n) AS c",
    "kennwert_belegt_in": "MATCH (:Kennwert)-[r:BELEGT_IN]->() RETURN count(r) AS c",
    "norm_belegt_in": "MATCH (:Norm)-[r:BELEGT_IN]->() RETURN count(r) AS c",
}


def probe(session) -> dict:
    return {k: session.run(q).single()["c"] for k, q in PROBE.items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--confirm", default=None)
    args = ap.parse_args()

    uri, user, password, database = resolve_connection()
    from neo4j import GraphDatabase

    expected = f"PHASE_B TO {database}"
    live = args.confirm == expected
    if args.confirm and not live:
        raise SystemExit(f"Confirm must equal: {expected!r}")

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            before = probe(session)
            result = {"mode": "live" if live else "dry-run", "before": before}
            if live:
                k_edges = session.run(MERGE_KENNWERT).single()["edges"]
                n_edges = session.run(MERGE_NORM).single()["edges"]
                session.run(DROP_KENNWERT).consume()
                session.run(DROP_NORM).consume()
                result["edges_merged"] = {"kennwert": k_edges, "norm": n_edges}
                result["after"] = probe(session)
            print(json.dumps(result, indent=2))
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
