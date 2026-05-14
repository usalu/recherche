"""
Record and list logical versions of a Neo4j graph (metadata only).

Creates nodes labeled `GraphVersion` (not used by the research CSV import) with
counts and notes, and appends the same record to:

  `_database/_system/neo4j_graph_versions.jsonl`

so a history survives full `DETACH DELETE` wipes. Re-import with
`import_clean_confirmed_edges_csv_raw_neo4j.py --preserve-graph-versions` to
keep existing `GraphVersion` nodes while reloading edges.

Credentials: same as other Neo4j scripts (`.cursor/mcp.json` Neo4j-Official env,
overridden by NEO4J_URI, NEO4J_USERNAME / NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE).

Usage:
  python _scripts/neo4j_graph_version.py tag --tag post-import-2026-05-13 --notes "after CSV reload"
  python _scripts/neo4j_graph_version.py list
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_scripts_dir = Path(__file__).resolve().parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))
from neo4j_env import repo_root, resolve_connection

VERSION_LABEL = "GraphVersion"
MANIFEST_REL = Path("research") / "_system" / "neo4j_graph_versions.jsonl"


def manifest_path() -> Path:
    return repo_root() / MANIFEST_REL


def ensure_constraint(session) -> None:
    try:
        session.run(
            f"CREATE CONSTRAINT graphversion_tag_unique IF NOT EXISTS "
            f"FOR (v:`{VERSION_LABEL}`) REQUIRE v.tag IS UNIQUE"
        )
    except Exception as e:
        print(f"Note: could not create uniqueness constraint: {e}", file=sys.stderr)


def graph_counts(session) -> tuple[int, int]:
    nodes = session.run("MATCH (n) RETURN count(n) AS c").single()["c"]
    rels = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
    return int(nodes), int(rels)


def next_sequence(session) -> int:
    rec = session.run(
        f"MATCH (v:`{VERSION_LABEL}`) RETURN coalesce(max(v.sequence), 0) AS mx"
    ).single()
    return int(rec["mx"]) + 1


def cmd_tag(session, database: str, tag: str, notes: str) -> None:
    tag = tag.strip()
    if not tag:
        raise SystemExit("Empty --tag")
    ensure_constraint(session)
    n_nodes, n_rels = graph_counts(session)
    seq = next_sequence(session)
    session.run(
        f"CREATE (v:`{VERSION_LABEL}` {{"
        f"  tag: $tag,"
        f"  created: datetime(),"
        f"  database: $database,"
        f"  notes: $notes,"
        f"  node_count: $node_count,"
        f"  rel_count: $rel_count,"
        f"  sequence: $sequence"
        f"}})",
        tag=tag,
        database=database,
        notes=notes or None,
        node_count=n_nodes,
        rel_count=n_rels,
        sequence=seq,
    )
    record = {
        "tag": tag,
        "iso_utc": datetime.now(timezone.utc).isoformat(),
        "database": database,
        "notes": notes or None,
        "node_count": n_nodes,
        "rel_count": n_rels,
        "sequence": seq,
    }
    path = manifest_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(
        f"Recorded {VERSION_LABEL!r} tag={tag!r} sequence={seq} "
        f"nodes={n_nodes} rels={n_rels} manifest={path}"
    )


def cmd_list(session) -> None:
    rows = session.run(
        f"MATCH (v:`{VERSION_LABEL}`) "
        f"RETURN v.tag AS tag, v.sequence AS sequence, v.created AS created, "
        f"v.database AS database, v.node_count AS node_count, v.rel_count AS rel_count, "
        f"v.notes AS notes "
        f"ORDER BY v.sequence ASC"
    )
    printed = False
    for rec in rows:
        printed = True
        print(
            f"{rec['sequence']:>4}  {rec['tag']!s:40}  "
            f"n={rec['node_count']} r={rec['rel_count']}  {rec['created']}  {rec['database']!r}"
        )
        if rec["notes"]:
            print(f"         notes: {rec['notes']}")
    if not printed:
        print(f"No `{VERSION_LABEL}` nodes in this database.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_tag = sub.add_parser("tag", help="Create a GraphVersion node + append jsonl manifest")
    p_tag.add_argument("--tag", required=True, help="Unique tag, e.g. v1 or 2026-05-13-post-import")
    p_tag.add_argument("--notes", default="", help="Optional description")

    sub.add_parser("list", help="List GraphVersion nodes by sequence")

    args = parser.parse_args()

    uri, user, password, database = resolve_connection()
    if not uri or not user or not password:
        print(
            "Missing NEO4J_URI / user / password. "
            "Set env vars or configure .cursor/mcp.json (Neo4j-Official).",
            file=sys.stderr,
        )
        return 1

    try:
        from neo4j import GraphDatabase
    except ImportError:
        print("Install: pip install -r requirements-neo4j.txt", file=sys.stderr)
        return 1

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            if args.cmd == "tag":
                cmd_tag(session, database, args.tag, args.notes)
            elif args.cmd == "list":
                cmd_list(session)
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
