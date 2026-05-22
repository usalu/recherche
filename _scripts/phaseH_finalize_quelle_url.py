"""Phase H finalize: normalize empty Quelle.url to null, add url uniqueness.

After the dedup merge, the only remaining "duplicate" url is the empty string
shared by a handful of external_reference nodes. Empty strings are nulled (a url
is either a real value or absent), then a uniqueness constraint is added so
duplicate sources can never re-accumulate.

Dry-run by default. Live requires:  --confirm "PHASE_H TO mit-bestand"
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

NULL_EMPTY = "MATCH (q:Quelle) WHERE q.url = '' SET q.url = null"
CONSTRAINT = (
    "CREATE CONSTRAINT quelle_url_unique IF NOT EXISTS "
    "FOR (q:Quelle) REQUIRE q.url IS UNIQUE"
)
PROBE = {
    "empty_url": "MATCH (q:Quelle) WHERE q.url = '' RETURN count(q) AS c",
    "dup_raw_url": (
        "MATCH (q:Quelle) WHERE q.url IS NOT NULL "
        "WITH q.url AS u, count(*) AS c WHERE c > 1 RETURN count(u) AS c"
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

    expected = f"PHASE_H TO {database}"
    live = args.confirm == expected
    if args.confirm and not live:
        raise SystemExit(f"Confirm must equal: {expected!r}")

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            result = {"mode": "live" if live else "dry-run", "before": probe(session)}
            if live:
                session.run(NULL_EMPTY).consume()
                mid = probe(session)
                if mid["dup_raw_url"] != 0:
                    raise SystemExit("Refusing constraint: duplicate raw urls remain.")
                session.run(CONSTRAINT).consume()
                result["after"] = mid
                result["constraint"] = "quelle_url_unique created"
            print(json.dumps(result, indent=2))
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
