"""Phase 1b: re-attach URL-less internal-document provenance as node properties.

Phase 1 dropped BELEGT_IN citations that pointed to URL-less internal research/
case markdown 'sources'. Those carried no web URL, so they were not kept as
`source_urls`. This step re-expresses them as a `legacy_internal_provenance_docs[]`
property on each cited node, read from the Phase 1 snapshot (no source nodes are
restored).

The property is deliberately named to signal LOWER importance than the main
`source_urls`: these are internal/legacy document pointers, not citable web
sources. Tools/consumers should always prefer `source_urls` over this property.

Usage:
  python phase1b_restore_provenance_docs.py
  python phase1b_restore_provenance_docs.py --commit
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from neo4j import GraphDatabase

OUT = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[4]
if str(REPO / "_scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "_scripts"))

from neo4j_env import resolve_connection  # noqa: E402

SNAPSHOT = OUT / "phase1_before.json"
PROP = "legacy_internal_provenance_docs"
OLD_PROP = "provenance_docs"


def provenance_label(props: dict[str, Any]) -> str:
    name = props.get("name") or props.get("title") or props.get("id")
    return str(name)


def build_plan() -> tuple[dict[str, list[str]], dict[str, Any]]:
    data = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    source_by_eid = {n["element_id"]: n["properties"] for n in data["source_nodes"]}
    url_less_eids = {
        eid for eid, props in source_by_eid.items() if not props.get("url")
    }

    plan: dict[str, set[str]] = defaultdict(set)
    skipped_self = 0
    skipped_no_from_id = 0
    edges_considered = 0
    for rel in data["deleted_relationships"]:
        if rel["type"] != "BELEGT_IN":
            continue
        if rel["to_element_id"] not in url_less_eids:
            continue
        edges_considered += 1
        from_id = rel.get("from_id")
        if not from_id:
            skipped_no_from_id += 1
            continue
        if from_id == rel.get("to_id"):
            skipped_self += 1
            continue
        plan[from_id].add(provenance_label(source_by_eid[rel["to_element_id"]]))

    plan_sorted = {k: sorted(v) for k, v in plan.items()}
    stats = {
        "url_less_source_nodes": len(url_less_eids),
        "url_less_belegt_in_edges": edges_considered,
        "cited_nodes_to_tag": len(plan_sorted),
        "self_citations_skipped": skipped_self,
        "edges_without_from_id_skipped": skipped_no_from_id,
        "total_provenance_values": sum(len(v) for v in plan_sorted.values()),
    }
    return plan_sorted, stats


def run(commit: bool) -> dict[str, Any]:
    plan, stats = build_plan()
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    report: dict[str, Any] = {
        "phase": "phase1b_restore_provenance_docs",
        "database": database,
        "commit": commit,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "stats": stats,
    }
    applied = 0
    missing_nodes = 0
    with driver.session(database=database) as session:
        renamed = 0
        if commit:
            renamed = session.run(
                f"""
                MATCH (n) WHERE n.{OLD_PROP} IS NOT NULL
                SET n.{PROP} = coalesce(n.{PROP}, []) +
                    [d IN n.{OLD_PROP} WHERE NOT d IN coalesce(n.{PROP}, [])]
                REMOVE n.{OLD_PROP}
                RETURN count(n) AS c
                """
            ).single()["c"]
        report["nodes_renamed_from_old_prop"] = renamed
        for from_id, docs in plan.items():
            exists = session.run(
                "MATCH (n {id:$id}) RETURN count(n) AS c", id=from_id
            ).single()["c"]
            if not exists:
                missing_nodes += 1
                continue
            if commit:
                session.run(
                    f"""
                    MATCH (n {{id:$id}})
                    WITH n, [d IN $docs WHERE NOT d IN coalesce(n.{PROP}, [])] AS new_docs
                    SET n.{PROP} = coalesce(n.{PROP}, []) + new_docs
                    """,
                    id=from_id,
                    docs=docs,
                ).consume()
                applied += 1
        report["nodes_missing_in_graph"] = missing_nodes
        report["nodes_tagged"] = applied if commit else 0
        if commit:
            report["verify_nodes_with_provenance"] = session.run(
                f"MATCH (n) WHERE n.{PROP} IS NOT NULL AND size(n.{PROP}) > 0 "
                "RETURN count(n) AS c"
            ).single()["c"]
    driver.close()

    report_path = OUT / (
        "phase1b_report.json" if commit else "phase1b_dry_run_report.json"
    )
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()
    report = run(args.commit)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
