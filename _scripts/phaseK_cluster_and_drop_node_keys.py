"""Phase K: reduce node property keys - drop bookkeeping + cluster synonyms.

No data loss, no fabricated connections. Two operations:
  A. DROP 13 pure-bookkeeping keys (no unique data; provenance lives on edges).
  B. CLUSTER synonym keys:
       - title -> name (coalesce; distinct title kept as alias) on Quelle
       - {scope_note, short_description, definition, notes, hinweis} -> beschreibung
         (concatenated with ' | '; nothing dropped)

Dry-run by default. Live requires:  --confirm "PHASE_K TO mit-bestand"
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

DROP_KEYS = [
    "evidence_source_id", "evidence_origin", "evidence_confidence", "evidence_basis",
    "source_resolution_status", "source_count", "source_url_node_ids",
    "suggested_graph_action", "source_scope", "access_date", "review_run",
    "strict_source_url_cleanup", "strict_invalid_url_cleanup",
]
DESC_SYNONYMS = ["scope_note", "short_description", "definition", "notes", "hinweis"]

DROP_QUERY = (
    "MATCH (n) WHERE " + " OR ".join(f"n.`{k}` IS NOT NULL" for k in DROP_KEYS) + " "
    "CALL (n) { REMOVE " + ", ".join(f"n.`{k}`" for k in DROP_KEYS) + " } "
    "IN TRANSACTIONS OF 2000 ROWS"
)

# Title -> name / aliases on Quelle.
TITLE_TO_NAME = "MATCH (q:Quelle) WHERE q.title IS NOT NULL SET q.name = coalesce(q.name, q.title)"
TITLE_TO_ALIAS = (
    "MATCH (q:Quelle) WHERE q.title IS NOT NULL AND q.title <> q.name "
    "SET q.aliases = CASE WHEN q.title IN coalesce(q.aliases, []) "
    "THEN q.aliases ELSE coalesce(q.aliases, []) + q.title END"
)
TITLE_REMOVE = "MATCH (q:Quelle) WHERE q.title IS NOT NULL CALL (q) { REMOVE q.title } IN TRANSACTIONS OF 2000 ROWS"

# Description synonyms -> beschreibung.
_desc_list = "[x IN [n.beschreibung, " + ", ".join(f"n.`{k}`" for k in DESC_SYNONYMS) + "] WHERE x IS NOT NULL AND x <> '']"
DESC_CLUSTER = (
    "MATCH (n) WHERE " + " OR ".join(f"n.`{k}` IS NOT NULL" for k in DESC_SYNONYMS) + " "
    f"WITH n, {_desc_list} AS vals "
    "SET n.beschreibung = reduce(s = '', v IN vals | CASE WHEN s = '' THEN v ELSE s + ' | ' + v END) "
    "REMOVE " + ", ".join(f"n.`{k}`" for k in DESC_SYNONYMS)
)

PROBE = {
    "distinct_node_keys": "MATCH (n) UNWIND keys(n) AS k RETURN count(DISTINCT k) AS c",
    "drop_key_nodes": "MATCH (n) WHERE " + " OR ".join(f"n.`{k}` IS NOT NULL" for k in DROP_KEYS) + " RETURN count(n) AS c",
    "title_nodes": "MATCH (q:Quelle) WHERE q.title IS NOT NULL RETURN count(q) AS c",
    "desc_synonym_nodes": "MATCH (n) WHERE " + " OR ".join(f"n.`{k}` IS NOT NULL" for k in DESC_SYNONYMS) + " RETURN count(n) AS c",
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

    expected = f"PHASE_K TO {database}"
    live = args.confirm == expected
    if args.confirm and not live:
        raise SystemExit(f"Confirm must equal: {expected!r}")

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            result = {"mode": "live" if live else "dry-run", "before": probe(session)}
            if live:
                session.run(DROP_QUERY).consume()
                session.run(TITLE_TO_NAME).consume()
                session.run(TITLE_TO_ALIAS).consume()
                session.run(TITLE_REMOVE).consume()
                session.run(DESC_CLUSTER).consume()
                result["after"] = probe(session)
            print(json.dumps(result, indent=2))
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
