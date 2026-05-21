"""find_sources.py — print the source URLs for any node in mit-bestand.

Usage:
    python _scripts/find_sources.py <node_id>
    python _scripts/find_sources.py <node_id> --full
    python _scripts/find_sources.py <node_id> --json

Examples:
    python _scripts/find_sources.py p_holbein_gardens_london
    python _scripts/find_sources.py p_stuttgart_210 --full
    python _scripts/find_sources.py rotordc --json

Wraps Query 1 and Query 2 from QUELLE_QUERY_GUIDE.md. Fast path uses the
denormalised .source_urls array; --full does the graph traversal and includes
excerpts.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from neo4j import GraphDatabase

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "_scripts"))
# noinspection PyUnresolvedReferences
from neo4j_env import resolve_connection  # type: ignore

DATABASE = "mit-bestand"


def fetch_quick(driver, node_id: str) -> dict:
    """Use the denormalised source_urls array. Fast."""
    with driver.session(database=DATABASE, default_access_mode="READ") as s:
        row = s.run(
            "MATCH (n {id: $id}) "
            "RETURN n.source_urls AS urls, n.source_count AS n, "
            "labels(n) AS labels, n.name AS name",
            id=node_id,
        ).single()
        return dict(row) if row else {}


def fetch_full(driver, node_id: str) -> list[dict]:
    """Graph traversal — includes dossier, S-ref label, and excerpt."""
    with driver.session(database=DATABASE, default_access_mode="READ") as s:
        rows = s.run(
            "MATCH (n {id: $id}) "
            "OPTIONAL MATCH (n)-[bel:BELEGT_IN]->(d:Dossier)-[z:ZITIERT_QUELLE]->(ext:ExternalLink) "
            "RETURN ext.url AS url, ext.title AS title, "
            "       d.id AS dossier, z.locator AS sref, "
            "       bel.evidence_excerpt AS excerpt "
            "ORDER BY dossier, sref",
            id=node_id,
        )
        return [dict(r) for r in rows]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("node_id", help="The id of any node in mit-bestand (e.g. p_holbein_gardens_london)")
    ap.add_argument("--full", action="store_true", help="Include dossier + S-ref + excerpt per URL")
    ap.add_argument("--json", action="store_true", help="Emit JSON instead of human text")
    args = ap.parse_args()

    uri, user, password, _db = resolve_connection()
    if not uri:
        sys.exit("Missing Neo4j connection. Check .cursor/mcp.json.")
    driver = GraphDatabase.driver(uri, auth=(user, password))

    try:
        quick = fetch_quick(driver, args.node_id)
        if not quick:
            sys.exit(f"No node with id={args.node_id!r}")

        if args.full:
            full = fetch_full(driver, args.node_id)
            if args.json:
                print(json.dumps({
                    "id": args.node_id,
                    "name": quick.get("name"),
                    "labels": quick.get("labels"),
                    "source_count": quick.get("n"),
                    "sources": full,
                }, indent=2, default=str, ensure_ascii=False))
            else:
                print(f"# {args.node_id} — {quick.get('name') or '(no name)'}")
                print(f"# labels: {', '.join(quick.get('labels') or [])}")
                print(f"# {quick.get('n') or 0} source URL(s)")
                print()
                if not full or all(r.get("url") is None for r in full):
                    print("(no sources found via traversal)")
                else:
                    for r in full:
                        if not r.get("url"):
                            continue
                        print(f"- {r['url']}")
                        print(f"    dossier: {r.get('dossier') or '?'}    sref: {r.get('sref') or '?'}")
                        title = r.get("title")
                        if title:
                            print(f"    title:   {title}")
                        excerpt = r.get("excerpt")
                        if excerpt:
                            excerpt_short = excerpt if len(excerpt) <= 200 else excerpt[:200] + "…"
                            print(f"    excerpt: {excerpt_short}")
                        print()
        else:
            urls = quick.get("urls") or []
            if args.json:
                print(json.dumps({
                    "id": args.node_id,
                    "name": quick.get("name"),
                    "labels": quick.get("labels"),
                    "source_count": quick.get("n") or 0,
                    "urls": urls,
                }, indent=2, ensure_ascii=False))
            else:
                print(f"# {args.node_id} — {quick.get('name') or '(no name)'}")
                print(f"# {len(urls)} source URL(s)")
                for u in urls:
                    print(u)
    finally:
        driver.close()


if __name__ == "__main__":
    main()
