"""find_sources.py - print the source URLs for any node in mit-bestand.

Usage:
    python _scripts/find_sources.py <node_id>
    python _scripts/find_sources.py <node_id> --full
    python _scripts/find_sources.py <node_id> --json

Examples:
    python _scripts/find_sources.py p_holbein_gardens_london
    python _scripts/find_sources.py p_stuttgart_210 --full
    python _scripts/find_sources.py rotordc --json

Fast path shows the denormalised node URL inventory. --full separates exact
fact sources from candidate review leads. The legacy :ZITIERT_QUELLE hop has
been removed from the live graph.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from neo4j import GraphDatabase

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "_scripts"))
# noinspection PyUnresolvedReferences
from neo4j_env import resolve_connection  # type: ignore

DATABASE = "mit-bestand"


def fetch_quick(driver, node_id: str) -> dict:
    """Use denormalised source_urls as node-level URL inventory. Fast."""
    with driver.session(database=DATABASE, default_access_mode="READ") as s:
        row = s.run(
            "MATCH (n {id: $id}) "
            "RETURN n.primary_source_url AS primary_url, "
            "       n.source_urls AS urls, n.source_count AS n, "
            "       n.candidate_source_urls AS candidate_urls, "
            "       n.candidate_source_count AS candidate_n, "
            "       labels(n) AS labels, n.name AS name",
            id=node_id,
        ).single()
        return dict(row) if row else {}


def fetch_full(driver, node_id: str) -> dict[str, list[dict]]:
    """Graph traversal using direct URL properties on exact fact edges."""
    with driver.session(database=DATABASE, default_access_mode="READ") as s:
        node_inventory = s.run(
            """
            MATCH (n {id: $id})
            WITH n, CASE
              WHEN n.source_urls IS NOT NULL THEN n.source_urls
              WHEN n.source_url IS NOT NULL THEN [n.source_url]
              ELSE []
            END AS urls
            UNWIND urls AS url
            RETURN DISTINCT url AS url,
                   null AS title,
                   n.id AS context_id,
                   labels(n) AS context_labels,
                   'NODE_SOURCE_URLS' AS rel_type,
                   null AS locator,
                   null AS evidence_source_id,
                   null AS excerpt,
                   n.source_resolution_status AS source_resolution_status,
                   n.review_status AS review_status,
                   'node_inventory' AS source_status
            ORDER BY url
            """,
            id=node_id,
        )
        exact_sources = s.run(
            """
            MATCH (n {id: $id})-[rel]-(other)
            WHERE rel.source_status = 'exact'
              AND rel.source_url IS NOT NULL
            WITH rel, other, rel.source_url AS url
            OPTIONAL MATCH (ext)
            WHERE (ext:ExternalLink OR ext:SectionRef)
              AND ext.url = url
            WITH url, rel, other, collect(ext.title)[0] AS title
            RETURN DISTINCT url AS url,
                   title AS title,
                   other.id AS context_id,
                   labels(other) AS context_labels,
                   type(rel) AS rel_type,
                   rel.locator AS locator,
                   rel.evidence_source_id AS evidence_source_id,
                   rel.evidence_excerpt AS excerpt,
                   rel.source_resolution_status AS source_resolution_status,
                   rel.review_status AS review_status,
                   rel.source_status AS source_status
            ORDER BY url, rel_type, context_id
            """,
            id=node_id,
        )
        candidate_sources = s.run(
            """
            MATCH (n {id: $id})-[rel]-(other)
            WHERE rel.source_status = 'candidate'
              AND rel.candidate_source_urls IS NOT NULL
            WITH rel, other, CASE
              WHEN rel.candidate_source_urls IS NOT NULL THEN rel.candidate_source_urls ELSE []
            END AS urls
            UNWIND urls AS url
            RETURN DISTINCT url AS url,
                   null AS title,
                   other.id AS context_id,
                   labels(other) AS context_labels,
                   type(rel) AS rel_type,
                   rel.locator AS locator,
                   rel.evidence_source_id AS evidence_source_id,
                   rel.evidence_excerpt AS excerpt,
                   rel.source_resolution_status AS source_resolution_status,
                   rel.review_status AS review_status,
                   rel.source_status AS source_status
            ORDER BY source_resolution_status, url, rel_type, context_id
            """,
            id=node_id,
        )
        return {
            "node_source_inventory": [dict(r) for r in node_inventory],
            "exact_sources": [dict(r) for r in exact_sources],
            "candidate_sources": [dict(r) for r in candidate_sources],
        }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("node_id", help="The id of any node in mit-bestand, e.g. p_holbein_gardens_london")
    ap.add_argument("--full", action="store_true", help="Include relationship context and excerpt per URL")
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
                exact_sources = full["exact_sources"]
                candidate_sources = full["candidate_sources"]
                print(
                    json.dumps(
                        {
                            "id": args.node_id,
                            "name": quick.get("name"),
                            "labels": quick.get("labels"),
                            "source_count": quick.get("n"),
                            "sources": exact_sources,
                            "exact_sources": exact_sources,
                            "candidate_sources": candidate_sources,
                            "node_source_inventory": full["node_source_inventory"],
                        },
                        indent=2,
                        default=str,
                        ensure_ascii=False,
                    )
                )
            else:
                print(f"# {args.node_id} - {quick.get('name') or '(no name)'}")
                print(f"# labels: {', '.join(quick.get('labels') or [])}")
                print(f"# {quick.get('n') or 0} node inventory URL(s)")
                if quick.get("candidate_n"):
                    print(f"# {quick.get('candidate_n')} candidate URL(s) need review")
                print()
                exact_sources = full["exact_sources"]
                candidate_sources = full["candidate_sources"]
                if not exact_sources:
                    print("(no exact fact sources found via relationship source_url properties)")
                else:
                    print("## Exact fact sources")
                    for r in exact_sources:
                        print(f"- {r['url']}")
                        labels = ", ".join(r.get("context_labels") or [])
                        print(f"    via:     {r.get('rel_type') or '?'}")
                        print(f"    context: {r.get('context_id') or '?'} ({labels or '?'})")
                        if r.get("locator"):
                            print(f"    locator: {r['locator']}")
                        if r.get("evidence_source_id"):
                            print(f"    source:  {r['evidence_source_id']}")
                        if r.get("title"):
                            print(f"    title:   {r['title']}")
                        if r.get("source_resolution_status"):
                            print(f"    status:  {r['source_resolution_status']}")
                        if r.get("source_status"):
                            print(f"    source_status: {r['source_status']}")
                        excerpt = r.get("excerpt")
                        if excerpt:
                            excerpt_short = excerpt if len(excerpt) <= 200 else excerpt[:200] + "..."
                            print(f"    excerpt: {excerpt_short}")
                        print()
                if candidate_sources:
                    print("## Candidate review leads")
                    for r in candidate_sources:
                        print(f"- {r['url']}")
                        labels = ", ".join(r.get("context_labels") or [])
                        print(f"    via:     {r.get('rel_type') or '?'}")
                        print(f"    context: {r.get('context_id') or '?'} ({labels or '?'})")
                        if r.get("source_resolution_status"):
                            print(f"    status:  {r['source_resolution_status']}")
                        print("    source_status: candidate")
                        print()
                if full["node_source_inventory"]:
                    print("## Node URL inventory")
                    for r in full["node_source_inventory"][:25]:
                        print(f"- {r['url']}")
        else:
            urls = quick.get("urls") or []
            primary = quick.get("primary_url")
            candidate_urls = quick.get("candidate_urls") or []
            if args.json:
                print(
                    json.dumps(
                        {
                            "id": args.node_id,
                            "name": quick.get("name"),
                            "labels": quick.get("labels"),
                            "primary_source_url": primary,
                            "source_count": quick.get("n") or 0,
                            "candidate_source_count": quick.get("candidate_n") or 0,
                            "candidate_source_urls": candidate_urls,
                            "source_url_inventory": urls,
                        },
                        indent=2,
                        ensure_ascii=False,
                    )
                )
            else:
                print(f"# {args.node_id} - {quick.get('name') or '(no name)'}")
                print(f"# labels: {', '.join(quick.get('labels') or [])}")
                if primary:
                    print(f"# PRIMARY: {primary}")
                print(f"# NODE URL INVENTORY ({len(urls)}):")
                if not urls:
                    print("    (no node-level URL inventory yet)")
                for url in urls[:25]:
                    print(f"  * {url}")
                if len(urls) > 25:
                    print(f"  * ... and {len(urls) - 25} more")
                if candidate_urls:
                    print(f"# REVIEW CANDIDATES ({len(candidate_urls)}):")
                    for url in candidate_urls[:10]:
                        print(f"  - {url}")
                    if len(candidate_urls) > 10:
                        print(f"  - ... and {len(candidate_urls) - 10} more")
    finally:
        driver.close()


if __name__ == "__main__":
    main()
