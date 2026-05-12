"""
Load planned graph vertices from neo4j_schema_visual_nodes_attachment.md into Neo4j.

For the full research graph (inventory + confirmed edges), see
import_database_folder_to_neo4j.py in this folder.

Environment (optional defaults in parentheses):
  NEO4J_URI       (neo4j://127.0.0.1:7687)
  NEO4J_USER      (neo4j)
  NEO4J_DATABASE  (neo4j) — must match the DB selected in Neo4j Browser (not `system`)
  NEO4J_PASSWORD  (required unless --dry-run)

Usage:
  pip install -r requirements-neo4j.txt
  set NEO4J_PASSWORD=...
  python _scripts/export_visual_attachment_to_neo4j.py
  python _scripts/export_visual_attachment_to_neo4j.py --dry-run
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

NODE_LINE = re.compile(r"^\s+\(:([A-Za-z]+)\s*\{([^}]*)\}\)\s*$")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_attachment_path() -> Path:
    return repo_root() / ".cursor" / "plans" / "neo4j_schema_visual_nodes_attachment.md"


def parse_props(body: str) -> dict:
    """Parse a Neo4j-style `{ k: "v", n: 1 }` map (strings and integers/floats only)."""
    props: dict = {}
    pos = 0
    n = len(body)
    while pos < n:
        while pos < n and body[pos] in " \t":
            pos += 1
        if pos >= n:
            break
        key_start = pos
        while pos < n and (body[pos].isalnum() or body[pos] == "_"):
            pos += 1
        key = body[key_start:pos]
        if not key:
            raise ValueError(f"Expected property key near position {pos} in: {body!r}")
        while pos < n and body[pos] in " \t":
            pos += 1
        if pos >= n or body[pos] != ":":
            raise ValueError(f"Expected ':' after key {key!r} in: {body!r}")
        pos += 1
        while pos < n and body[pos] in " \t":
            pos += 1
        if pos >= n:
            raise ValueError(f"Missing value for key {key!r}")
        if body[pos] == '"':
            pos += 1
            vstart = pos
            while pos < n and body[pos] != '"':
                pos += 1
            val = body[vstart:pos]
            if pos >= n:
                raise ValueError(f"Unterminated string for key {key!r}")
            pos += 1
        elif body[pos] == "-" or body[pos].isdigit():
            vstart = pos
            if body[pos] == "-":
                pos += 1
            while pos < n and body[pos].isdigit():
                pos += 1
            if pos < n and body[pos] == ".":
                pos += 1
                while pos < n and body[pos].isdigit():
                    pos += 1
            num = body[vstart:pos]
            val = float(num) if "." in num else int(num)
        else:
            raise ValueError(f"Unsupported value start {body[pos]!r} for key {key!r}")
        props[key] = val
        while pos < n and body[pos] in " \t":
            pos += 1
        if pos < n:
            if body[pos] != ",":
                raise ValueError(f"Expected ',' or end after value for {key!r}, got {body[pos]!r}")
            pos += 1
    return props


def iter_nodes_from_markdown(path: Path):
    in_block = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip("\n")
        if line.strip() == "```text":
            in_block = True
            continue
        if in_block and line.strip() == "```":
            break
        if not in_block:
            continue
        m = NODE_LINE.match(line)
        if not m:
            continue
        label, props_body = m.group(1), m.group(2)
        props = parse_props(props_body)
        if "id" not in props:
            raise ValueError(f"Node line missing id: {line}")
        yield label, props


def merge_batch(tx, label: str, batch: list[dict]):
    # Label validated by caller (alphanumeric only).
    cypher = f"UNWIND $rows AS row MERGE (n:`{label}` {{id: row.id}}) SET n += row.props"
    rows = []
    for p in batch:
        pid = p["id"]
        extra = {k: v for k, v in p.items() if k != "id"}
        rows.append({"id": pid, "props": extra})
    tx.run(cypher, rows=rows)


# Sample Bauwerk → Fallbeispiel links (plan Appendix F: rolle `fallbeispiel`) from visual attachment ids.
DEMO_FALL_BAU = [
    ("Berlin_Schildow_Pilot_Haus", "Berlin_Schildow_Pilot_Haus_Gebaeude"),
    ("55_Great_Suffolk_Street_London", "55_Great_Suffolk_Street_London_Lager"),
    ("K118_Halle_118_Winterthur", "K118_Halle_118_Winterthur"),
    ("AWM_Muenster_Circular_Office", "AWM_Muenster_Circular_Office"),
]


def merge_demo_edges(tx):
    """A few GEHÖRT_ZU edges so Explorer mode is not empty (catalogue file has vertices only)."""
    q = """
    UNWIND $pairs AS p
    MATCH (b:Bauwerk {id: p.bid}), (f:Fallbeispiel {id: p.fid})
    MERGE (b)-[:GEHÖRT_ZU {rolle: 'fallbeispiel'}]->(f)
    """
    rows = [{"fid": a, "bid": b} for a, b in DEMO_FALL_BAU]
    tx.run(q, pairs=rows)


def count_snapshot(session):
    nodes = session.run("MATCH (n) RETURN count(n) AS c").single()["c"]
    rels = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
    return int(nodes), int(rels)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--attachment",
        type=Path,
        default=default_attachment_path(),
        help="Path to neo4j_schema_visual_nodes_attachment.md",
    )
    ap.add_argument("--dry-run", action="store_true", help="Parse file only; do not connect.")
    ap.add_argument(
        "--verify-only",
        action="store_true",
        help="Only print node/relationship counts for NEO4J_DATABASE (no import).",
    )
    ap.add_argument(
        "--demo-edges",
        action="store_true",
        help="After import, MERGE four Bauwerk->Fallbeispiel GEHÖRT_ZU {rolle: 'fallbeispiel'} edges (plan Appendix F).",
    )
    ap.add_argument("--batch-size", type=int, default=200)
    args = ap.parse_args()

    path: Path = args.attachment

    if args.dry_run:
        if not path.is_file():
            print(f"Attachment not found: {path}", file=sys.stderr)
            return 1
        nodes = list(iter_nodes_from_markdown(path))
        print(f"Parsed {len(nodes)} nodes from {path}")
        by_label: dict[str, int] = {}
        for lab, _ in nodes:
            by_label[lab] = by_label.get(lab, 0) + 1
        for lab in sorted(by_label):
            print(f"  {lab}: {by_label[lab]}")
        return 0

    password = (os.environ.get("NEO4J_PASSWORD") or "").strip()
    if not password:
        print("NEO4J_PASSWORD is not set.", file=sys.stderr)
        return 1

    uri = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687").strip()
    user = os.environ.get("NEO4J_USER", "neo4j").strip()
    database = (os.environ.get("NEO4J_DATABASE") or "neo4j").strip() or "neo4j"

    try:
        from neo4j import GraphDatabase
    except ImportError:
        print("Install the driver: pip install -r requirements-neo4j.txt", file=sys.stderr)
        return 1

    driver = GraphDatabase.driver(uri, auth=(user, password))

    try:
        driver.verify_connectivity()
        print(f"Connected to {uri}  database=`{database}`  user=`{user}`")
        print(
            "If Neo4j Browser shows an empty graph: open the database dropdown "
            f"and select `{database}` (not `system`), or run  :use {database}"
        )

        def open_session():
            return driver.session(database=database)

        if args.verify_only:
            with open_session() as session:
                n, r = count_snapshot(session)
            print(f"Verify-only: {n} nodes, {r} relationships in database `{database}`.")
            return 0

        if not path.is_file():
            print(f"Attachment not found: {path}", file=sys.stderr)
            return 1

        nodes = list(iter_nodes_from_markdown(path))
        print(f"Parsed {len(nodes)} nodes from {path}")

        batches: dict[str, list[dict]] = {}
        for label, props in nodes:
            if not label.isalpha():
                print(f"Refusing non-alphabetic label: {label}", file=sys.stderr)
                return 1
            batches.setdefault(label, []).append(props)

        with open_session() as session:
            n0, r0 = count_snapshot(session)
            print(f"Before import: {n0} nodes, {r0} relationships")

            for label, plist in batches.items():
                for i in range(0, len(plist), args.batch_size):
                    chunk = plist[i : i + args.batch_size]
                    session.execute_write(merge_batch, label, chunk)
                print(f"  Loaded {len(plist)} nodes for :{label}")

            if args.demo_edges:
                session.execute_write(merge_demo_edges)
                print("  Merged demo :GEHÖRT_ZU edges (Bauwerk -> Fallbeispiel, 4 pairs)")

            n1, r1 = count_snapshot(session)
            print(f"After import: {n1} nodes, {r1} relationships in database `{database}`")
    finally:
        driver.close()

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
