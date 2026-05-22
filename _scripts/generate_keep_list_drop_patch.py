"""Generate the keep-list 'drop' patch from the decision matrix.

Reads KEEP_LIST_DECISION_MATRIX.csv and, for every (label, property) pair whose
verdict is `drop`, finds the live nodes carrying that property and emits a
`remove_node_properties` JSONL patch. A keep-union guard ensures a property is
never removed from a node if ANY of that node's labels keeps it.

Only verdict == 'drop' is handled here (the mechanical, edge-safe removals).
migrate_then_drop / migrate_edge_then_drop / move_to_relationship / meta_separate
are handled by their own phase scripts.

Usage:
  python _scripts/generate_keep_list_drop_patch.py \
      --audit-dir _neo4j/review/2026-06-01_minimal_property_audit_current_mit-bestand
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import repo_root, resolve_connection  # noqa: E402

PROP_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
LABEL_RE = re.compile(r"^[^\W\d]\w*$", re.UNICODE)


def safe_prop(prop: str) -> str:
    if not PROP_RE.match(prop):
        raise ValueError(f"unsafe property key: {prop!r}")
    return prop


def safe_label(label: str) -> str:
    if not LABEL_RE.match(label):
        raise ValueError(f"unsafe label: {label!r}")
    return label


def generate(audit_dir: Path, out_dir: Path) -> dict[str, Any]:
    from neo4j import GraphDatabase

    audit_dir = audit_dir.resolve()
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    matrix = list(csv.DictReader(open(audit_dir / "KEEP_LIST_DECISION_MATRIX.csv", encoding="utf-8")))

    keep_by_label: dict[str, set[str]] = defaultdict(set)
    drop_pairs: list[tuple[str, str]] = []
    for r in matrix:
        if r["verdict"] in ("keep_core", "keep_semantic"):
            keep_by_label[r["label"]].add(r["property"])
        elif r["verdict"] == "drop":
            drop_pairs.append((r["label"], r["property"]))

    uri, user, password, database = resolve_connection()
    if not uri or not user or not password:
        raise SystemExit("Missing Neo4j connection settings.")

    remove_by_id: dict[str, set[str]] = defaultdict(set)
    per_pair_counts: list[dict[str, Any]] = []
    guarded = 0

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database, default_access_mode="READ") as session:
            before = session.run(
                "MATCH (n) WITH count(n) AS nodes MATCH ()-[r]->() RETURN nodes, count(r) AS rels"
            ).single()
            for label, prop in drop_pairs:
                lab = safe_label(label)
                p = safe_prop(prop)
                q = (
                    f"MATCH (n:`{lab}`) WHERE n.`{p}` IS NOT NULL "
                    "RETURN n.id AS id, labels(n) AS labels"
                )
                live = 0
                kept = 0
                for rec in session.run(q):
                    live += 1
                    node_id = rec["id"]
                    labels = rec["labels"]
                    if not node_id:
                        continue
                    # keep-union guard across all labels of this node
                    if any(prop in keep_by_label.get(l, set()) for l in labels):
                        kept += 1
                        continue
                    remove_by_id[str(node_id)].add(prop)
                guarded += kept
                per_pair_counts.append(
                    {"label": label, "property": prop, "live_nodes": live, "guarded_kept": kept}
                )
    finally:
        driver.close()

    patch_path = out_dir / "keep_list_drop.patch.jsonl"
    records = [
        {"op": "remove_node_properties", "id": nid, "properties": sorted(remove_by_id[nid])}
        for nid in sorted(remove_by_id)
    ]
    with patch_path.open("w", encoding="utf-8", newline="\n") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True) + "\n")

    total_removals = sum(len(v) for v in remove_by_id.values())
    summary = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "database": database,
        "drop_pairs": len(drop_pairs),
        "patch_records": len(records),
        "node_property_removals": total_removals,
        "guarded_keeps": guarded,
        "graph_counts_before": {"nodes": int(before["nodes"]), "rels": int(before["rels"])},
        "patch_path": str(patch_path.relative_to(repo_root())),
        "per_pair_counts": per_pair_counts,
    }
    (out_dir / "keep_list_drop_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({k: v for k, v in summary.items() if k != "per_pair_counts"}, indent=2))
    return summary


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--audit-dir", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, default=None)
    args = ap.parse_args()
    out_dir = args.out_dir or (args.audit_dir / "phaseA_drop")
    generate(args.audit_dir, out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
