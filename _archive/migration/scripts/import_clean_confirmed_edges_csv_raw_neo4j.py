"""
Load `_database/_edges/clean_confirmed_edges.csv` into Neo4j as a literal graph:

  - Node labels = `source_entity` / `target_entity` (CSV strings, unchanged).
  - Relationship type = `relation` (CSV string, unchanged).
  - Nodes keyed by `id` (= `source_id` / `target_id`); property `ref` = full `source` / `target`.
  - Each relationship carries all CSV columns as properties (raw row mirror).

Wipes the target database first (DETACH DELETE all nodes).

Credentials default from `.cursor/mcp.json` → `mcpServers` → `Neo4j-Official` → `env`.
Environment variables override those values when set.

  NEO4J_URI, NEO4J_USERNAME (or NEO4J_USER), NEO4J_PASSWORD, NEO4J_DATABASE

Usage:
  pip install -r requirements-neo4j.txt
  python _scripts/import_clean_confirmed_edges_csv_raw_neo4j.py
  python _scripts/import_clean_confirmed_edges_csv_raw_neo4j.py --dry-run
  python _scripts/import_clean_confirmed_edges_csv_raw_neo4j.py --preserve-graph-versions
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

_scripts_dir = Path(__file__).resolve().parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))
from neo4j_env import repo_root, resolve_connection

IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def validate_ident(name: str, ctx: str) -> str:
    if not name or not IDENT.match(name):
        raise ValueError(f"Invalid Neo4j identifier for {ctx}: {name!r}")
    return name


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV has no header")
        required = {
            "source",
            "source_entity",
            "source_id",
            "relation",
            "target",
            "target_entity",
            "target_id",
        }
        missing = required - set(reader.fieldnames)
        if missing:
            raise ValueError(f"CSV missing columns: {sorted(missing)}")
        rows: list[dict[str, str]] = []
        for raw in reader:
            row = {k: (raw.get(k) or "").strip() for k in reader.fieldnames}
            rows.append(row)
        return rows


def rel_props_from_row(row: dict[str, str]) -> dict[str, str | None]:
    """All CSV fields on the relationship; empty strings stored as null."""
    out: dict[str, str | None] = {}
    for k, v in row.items():
        out[k] = v if v != "" else None
    return out


def group_rows(
    rows: list[dict[str, str]],
) -> dict[tuple[str, str, str], list[dict[str, str]]]:
    groups: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        try:
            sl = validate_ident(row["source_entity"], "source_entity")
            tl = validate_ident(row["target_entity"], "target_entity")
            rt = validate_ident(row["relation"], "relation")
        except ValueError:
            continue
        if not row["source_id"] or not row["target_id"]:
            continue
        groups[(sl, tl, rt)].append(row)
    return groups


def wipe_database(session, preserve_graph_versions: bool) -> None:
    if preserve_graph_versions:
        session.run(
            "MATCH (n) WHERE NOT n:GraphVersion DETACH DELETE n"
        )
    else:
        session.run("MATCH (n) DETACH DELETE n")


def import_groups(
    session,
    groups: dict[tuple[str, str, str], list[dict[str, str]]],
) -> None:
    for (sl, tl, rt), batch in groups.items():
        cypher = (
            f"UNWIND $rows AS row "
            f"MERGE (a:`{sl}` {{id: row.source_id}}) "
            f"SET a.ref = row.source "
            f"MERGE (b:`{tl}` {{id: row.target_id}}) "
            f"SET b.ref = row.target "
            f"CREATE (a)-[r:`{rt}`]->(b) "
            f"SET r += row.props"
        )

        rows_param = [
            {
                "source_id": row["source_id"],
                "target_id": row["target_id"],
                "source": row["source"],
                "target": row["target"],
                "props": rel_props_from_row(row),
            }
            for row in batch
        ]

        def work(tx):
            tx.run(cypher, rows=rows_param)

        session.execute_write(work)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv",
        type=Path,
        default=repo_root() / "_database" / "_edges" / "clean_confirmed_edges.csv",
        help="Path to clean_confirmed_edges.csv",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse CSV and print stats only; do not connect to Neo4j.",
    )
    parser.add_argument(
        "--preserve-graph-versions",
        action="store_true",
        help="Wipe all nodes except :GraphVersion (see neo4j_graph_version.py) before import.",
    )
    args = parser.parse_args()

    csv_path: Path = args.csv
    if not csv_path.is_file():
        print(f"CSV not found: {csv_path}", file=sys.stderr)
        return 1

    rows = read_csv_rows(csv_path)
    groups = group_rows(rows)
    kept = sum(len(b) for b in groups.values())
    skipped = len(rows) - kept
    print(f"Rows in CSV: {len(rows)}")
    print(f"Rows queued for import: {kept} (skipped invalid/empty ids: {skipped})")
    print(f"Distinct (source_label, target_label, rel_type) groups: {len(groups)}")

    if args.dry_run:
        return 0

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
            print(f"Wiping database {database!r} …")
            wipe_database(session, args.preserve_graph_versions)
            print("Importing …")
            import_groups(session, groups)
        print("Done.")
    finally:
        driver.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
