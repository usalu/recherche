"""Phase J: collapse parallel duplicate edges, then backfill deterministic r.id.

After Phase F removed bookkeeping props, many relationships that differed only by
those props became exact duplicates (same from/type/to). They are collapsed to a
single edge (survivor = the one with the most remaining properties; the target is
identical so no evidence link is lost). Then every relationship still missing an
id gets the deterministic id `r_<from>__<TYPE>__<to>` (unique once parallels are
gone), satisfying the per-type rel-id uniqueness constraints and the gap survey.

Dry-run by default. Live requires:  --confirm "PHASE_J TO mit-bestand"
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

DEDUP = (
    "MATCH (a)-[r]->(b) "
    "WITH a, type(r) AS t, b, collect(r) AS rels "
    "WHERE size(rels) > 1 "
    "WITH rels, reduce(best = rels[0], x IN rels | "
    "  CASE WHEN size(keys(x)) > size(keys(best)) THEN x ELSE best END) AS keep "
    "UNWIND [x IN rels WHERE elementId(x) <> elementId(keep)] AS dead "
    "CALL (dead) { DELETE dead } IN TRANSACTIONS OF 1000 ROWS"
)
BACKFILL = (
    "MATCH (a)-[r]->(b) "
    "WHERE r.id IS NULL AND a.id IS NOT NULL AND b.id IS NOT NULL "
    "CALL (a, r, b) { "
    "  SET r.id = 'r_' + a.id + '__' + type(r) + '__' + b.id "
    "} IN TRANSACTIONS OF 2000 ROWS"
)
PROBE = {
    "rels": "MATCH ()-[r]->() RETURN count(r) AS c",
    "rid_null": "MATCH ()-[r]->() WHERE r.id IS NULL RETURN count(r) AS c",
    "parallel_dups": (
        "MATCH (a)-[r]->(b) WITH a, type(r) AS t, b, count(*) AS c "
        "WHERE c > 1 RETURN coalesce(sum(c - 1), 0) AS c"
    ),
}


def probe(session) -> dict:
    return {k: session.run(q).single()["c"] for k, q in PROBE.items()}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--confirm", default=None)
    args = ap.parse_args()

    uri, user, password, database = resolve_connection()
    from neo4j import GraphDatabase

    expected = f"PHASE_J TO {database}"
    live = args.confirm == expected
    if args.confirm and not live:
        raise SystemExit(f"Confirm must equal: {expected!r}")

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            result = {"mode": "live" if live else "dry-run", "before": probe(session)}
            if live:
                session.run(DEDUP).consume()
                session.run(BACKFILL).consume()
                result["after"] = probe(session)
            print(json.dumps(result, indent=2))
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
