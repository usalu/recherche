"""Phase 6.4 — delete 35 bg_reuse_ orphans + all non-reuse BGs.

Reads bauteilgruppe_id_map.csv, extracts the bg_reuse_ orphan ids
(action=no_batch_equiv AND id starts with bg_reuse_), passes them
as a list parameter to the Neo4j driver, runs DETACH DELETE.
Then deletes all non-reuse BG nodes by prefix.
"""
from __future__ import annotations
import csv
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[3] / "_scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402

PLAN_DIR = Path(__file__).resolve().parent


def main() -> int:
    # 1. Load bg_reuse_ orphans from CSV
    orphans = []
    with (PLAN_DIR / "bauteilgruppe_id_map.csv").open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["action"] == "no_batch_equiv" and row["live_bg_id"].startswith("bg_reuse_"):
                orphans.append(row["live_bg_id"])
    print(f"bg_reuse_ orphans to delete: {len(orphans)}")

    from neo4j import GraphDatabase
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password), connection_timeout=30)

    try:
        with driver.session(database=database) as s:
            # Pre-check
            r = s.run(
                "MATCH (bg:Bauteilgruppe) WHERE bg.id IN $ids RETURN count(bg) AS n",
                {"ids": orphans},
            ).single()
            print(f"  matched in graph: {r['n']}/{len(orphans)}")

            r = s.run(
                "MATCH (bg:Bauteilgruppe) "
                "WHERE bg.id STARTS WITH 'bg_retained_' "
                "   OR bg.id STARTS WITH 'bg_planned_' "
                "   OR bg.id STARTS WITH 'bg_dismantled_' "
                "   OR bg.id STARTS WITH 'bg_candidate_' "
                "RETURN count(bg) AS n"
            ).single()
            print(f"non-reuse BGs to delete: {r['n']}")

            # 2. Delete bg_reuse_ orphans
            res = s.run(
                "MATCH (bg:Bauteilgruppe) WHERE bg.id IN $ids "
                "DETACH DELETE bg",
                {"ids": orphans},
            )
            summary = res.consume()
            print(f"  bg_reuse_ orphans: deleted {summary.counters.nodes_deleted} nodes, "
                  f"{summary.counters.relationships_deleted} rels")

            # 3. Delete non-reuse BGs
            res = s.run(
                "MATCH (bg:Bauteilgruppe) "
                "WHERE bg.id STARTS WITH 'bg_retained_' "
                "   OR bg.id STARTS WITH 'bg_planned_' "
                "   OR bg.id STARTS WITH 'bg_dismantled_' "
                "   OR bg.id STARTS WITH 'bg_candidate_' "
                "DETACH DELETE bg"
            )
            summary = res.consume()
            print(f"  non-reuse BGs: deleted {summary.counters.nodes_deleted} nodes, "
                  f"{summary.counters.relationships_deleted} rels")

            # 4. Post-check
            r = s.run("MATCH (bg:Bauteilgruppe) RETURN count(bg) AS n").single()
            print(f"\nTotal :Bauteilgruppe after deletes: {r['n']}  (expected ~304)")
            r = s.run(
                "MATCH (bg:Bauteilgruppe) WHERE NOT bg.id STARTS WITH 'bg_reuse_' "
                "RETURN count(bg) AS n"
            ).single()
            print(f"Non-bg_reuse_ remaining: {r['n']}  (expected 0)")
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
