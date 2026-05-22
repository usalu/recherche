"""validate_view_coverage.py — prove a view leaves no relationship behind.

A figure that quietly drops half its data still renders, still passes the styling
gate, and still looks convincing. This checks the claim instead: for every view
declaring a `coverage` block, it runs the view's own query, counts what actually
reaches the drawing, and compares that against the relationship count in the graph.

    python _scripts/validate_view_coverage.py            # every view with a coverage block
    python _scripts/validate_view_coverage.py --view huerden

Exit codes: 0 = every checked view is complete, 1 = something was dropped.

Declare coverage in views.json:

    "coverage": {
      "expect": "MATCH ()-[r:HAT_HUERDE]->() RETURN count(r) AS n",
      "of": "HAT_HUERDE relationships"
    }

Read-only, same guard as the renderer.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "_scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402
from neo4j_to_dot import (  # noqa: E402
    UnsafeQueryError,
    assert_read_only,
    fetch_aggregate,
    fetch_graph,
    fetch_matrix,
)
from render_neo4j_diagram import load_views  # noqa: E402


def expected(cypher: str, params: dict, database: str) -> int:
    assert_read_only(cypher)
    from neo4j import GraphDatabase

    uri, user, password, default_db = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        with driver.session(database=database or default_db, default_access_mode="READ") as s:
            record = s.run(cypher, params or {}).single()
            if record is None:
                return 0
            return int(list(record.values())[0])
    finally:
        driver.close()


def actual(view: dict, database: str) -> tuple[int, str]:
    """How many source relationships the view's own query actually carries."""
    mode = view.get("mode", "graph")
    params = view.get("params")
    budget = max(view.get("max_nodes", 300), 100_000)

    if mode == "matrix":
        matrix = fetch_matrix(view["cypher"], params=params, database=database, max_nodes=budget)
        plain = set(view.get("plain_cols", ()))
        total = sum(v for (r, c), v in matrix["cells"].items() if c not in plain)
        return int(total), f"{len(matrix['rows'])}x{len(matrix['cols'])} cells"
    if mode == "aggregate":
        _, edges = fetch_aggregate(view["cypher"], params=params, database=database, max_nodes=budget)
        return sum(e.count for e in edges), f"{len(edges)} aggregated edges"
    nodes, edges = fetch_graph(view["cypher"], params=params, database=database, max_nodes=budget)
    return sum(e.count for e in edges), f"{len(nodes)} nodes, {len(edges)} edges"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--view", help="Check one view instead of all")
    ap.add_argument("--database")
    args = ap.parse_args()

    views = load_views()
    if args.view:
        if args.view not in views:
            print(f"Unknown view {args.view!r}", file=sys.stderr)
            return 1
        targets = [views[args.view]]
    else:
        targets = [v for v in views.values() if v.get("coverage")]

    if not targets:
        print("No view declares a coverage block.", file=sys.stderr)
        return 1

    _, _, _, default_db = resolve_connection()
    database = args.database or default_db
    print(f"database: {database}\n")

    failures = 0
    checked = 0
    for view in targets:
        coverage = view.get("coverage")
        if not coverage:
            print(f"--  {view['name']:<28} no coverage block, skipped")
            continue
        checked += 1
        try:
            want = expected(coverage["expect"], view.get("params"), database)
            have, shape = actual(view, database)
        except (UnsafeQueryError, ValueError) as exc:
            print(f"FAIL {view['name']:<28} {exc}", file=sys.stderr)
            failures += 1
            continue
        except Exception as exc:
            print(f"FAIL {view['name']:<28} {type(exc).__name__}: {exc}", file=sys.stderr)
            failures += 1
            continue

        of = coverage.get("of", "relationships")
        if have == want:
            print(f"OK   {view['name']:<28} {have:>5} / {want:<5} {of}  ({shape})")
        else:
            missing = want - have
            print(
                f"FAIL {view['name']:<28} {have:>5} / {want:<5} {of}  "
                f"— {missing:+d} unaccounted ({shape})",
                file=sys.stderr,
            )
            failures += 1

    print()
    if failures:
        print(f"{failures} of {checked} view(s) drop data.", file=sys.stderr)
        return 1
    print(f"All {checked} checked view(s) carry every relationship they claim.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
