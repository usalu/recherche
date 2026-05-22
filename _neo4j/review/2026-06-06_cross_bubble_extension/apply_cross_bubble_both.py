"""Apply both cross-bubble extension patches to mit-bestand."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO / "_scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "_scripts"))

from apply_neo4j_review_patch import run as run_patch_apply  # noqa: E402
from neo4j import GraphDatabase  # noqa: E402
from neo4j_env import resolve_connection  # noqa: E402

OUT = Path(__file__).resolve().parent
PATCHES = [
    "cross_bubble_extension.patch.jsonl",
    "cross_bubble_extension_phase2.patch.jsonl",
]


def graph_counts(session) -> dict[str, int]:
    row = session.run(
        "MATCH (n) WITH count(n) AS nodes MATCH ()-[r]->() RETURN nodes, count(r) AS rels"
    ).single()
    return {"nodes": row["nodes"], "relationships": row["rels"]}


def apply(commit: bool, database: str) -> dict:
    uri, user, password, default_db = resolve_connection()
    db = database or default_db
    driver = GraphDatabase.driver(uri, auth=(user, password))
    report: dict = {
        "run": "cross_bubble_extension_2026_06_06",
        "commit": commit,
        "database": db,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "patches": [],
    }
    try:
        with driver.session(database=db) as session:
            report["counts_before"] = graph_counts(session)

        for patch_name in PATCHES:
            patch_path = OUT / "patches" / patch_name

            class Args:
                patch = patch_path
                database = db
                dry_run = not commit
                confirm = "" if not commit else f"APPLY {patch_name} TO {db}"
                report_dir = OUT / "apply_reports"

            result = run_patch_apply(Args())
            summary = result.get("summary") or {}
            report["patches"].append(
                {
                    "patch": patch_name,
                    "dry_run": result.get("dry_run"),
                    "summary": summary,
                    "counts_before": result.get("counts_before"),
                    "counts_after_actual": result.get("counts_after_actual"),
                }
            )

        with driver.session(database=db) as session:
            report["counts_after"] = graph_counts(session)
    finally:
        driver.close()

    (OUT / "apply_both_summary.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--database", default="")
    args = parser.parse_args()
    print(json.dumps(apply(commit=args.commit, database=args.database), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
