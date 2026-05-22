"""Generate the Phase 1 minimal-property cleanup patch.

Input is the read-only minimization audit. Output is a JSONL review patch for
P0 property removals that can be targeted by stable node/relationship `id`
properties. Relationship rows without `r.id` are written to a separate Cypher
review file instead of being smuggled into an ambiguous patch.

Usage:
  python _scripts/generate_minimal_property_phase1_patch.py
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
        raise ValueError(f"unsafe label/type: {label!r}")
    return label


def json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted(json_safe(v) for v in value)
    return str(value)


def read_p0_rows(audit_csv: Path) -> list[dict[str, str]]:
    with audit_csv.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return [
        row
        for row in rows
        if row.get("priority") == "P0" and row.get("action") == "drop_candidate"
    ]


def write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(json_safe(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def generate(audit_dir: Path, out_dir: Path) -> dict[str, Any]:
    try:
        from neo4j import GraphDatabase
    except ImportError as exc:
        raise SystemExit("Install: pip install -r requirements-neo4j.txt") from exc

    audit_dir = audit_dir.resolve()
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    audit_csv = audit_dir / "patch_ready_drop_candidates.csv"
    rows = read_p0_rows(audit_csv)
    node_rows = [r for r in rows if r["entity"] == "node"]
    rel_rows = [r for r in rows if r["entity"] == "relationship"]

    uri, user, password, database = resolve_connection()
    if not uri or not user or not password:
        raise SystemExit("Missing Neo4j connection settings.")

    node_props_by_id: dict[str, set[str]] = defaultdict(set)
    rel_props_by_id: dict[str, set[str]] = defaultdict(set)
    rel_unaddressed: list[dict[str, Any]] = []
    source_counts: list[dict[str, Any]] = []

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database, default_access_mode="READ") as session:
            before_counts = session.run(
                "MATCH (n) WITH count(n) AS nodes "
                "MATCH ()-[r]->() RETURN nodes, count(r) AS relationships"
            ).single()
            for row in node_rows:
                label = safe_label(row["group"])
                prop = safe_prop(row["property"])
                q = (
                    f"MATCH (n:`{label}`) WHERE n.`{prop}` IS NOT NULL "
                    "RETURN n.id AS id ORDER BY n.id"
                )
                ids = [rec["id"] for rec in session.run(q)]
                missing_id = sum(1 for node_id in ids if not node_id)
                for node_id in ids:
                    if node_id:
                        node_props_by_id[str(node_id)].add(prop)
                source_counts.append(
                    {
                        "entity": "node",
                        "group": label,
                        "property": prop,
                        "audit_count": int(row["nodes_or_rels_with_property"]),
                        "live_count": len(ids),
                        "missing_id": missing_id,
                    }
                )

            for row in rel_rows:
                rel_type = safe_label(row["group"])
                prop = safe_prop(row["property"])
                q = (
                    f"MATCH ()-[r]->() WHERE type(r) = $rel_type AND r.`{prop}` IS NOT NULL "
                    "RETURN elementId(r) AS element_id, r.id AS rel_id ORDER BY elementId(r)"
                )
                rels = [dict(rec) for rec in session.run(q, rel_type=rel_type)]
                with_id = 0
                without_id = 0
                for rel in rels:
                    rel_id = rel.get("rel_id")
                    if isinstance(rel_id, str) and rel_id:
                        rel_props_by_id[str(rel_id)].add(prop)
                        with_id += 1
                    else:
                        rel_unaddressed.append(
                            {
                                "type": rel_type,
                                "property": prop,
                                "element_id": rel["element_id"],
                            }
                        )
                        without_id += 1
                source_counts.append(
                    {
                        "entity": "relationship",
                        "group": rel_type,
                        "property": prop,
                        "audit_count": int(row["nodes_or_rels_with_property"]),
                        "live_count": len(rels),
                        "with_id": with_id,
                        "without_id": without_id,
                    }
                )
    finally:
        driver.close()

    patch_path = out_dir / "minimal_properties_phase1_p0.patch.jsonl"
    cypher_path = out_dir / "minimal_properties_phase1_unaddressed_relationships.cypher"
    summary_path = out_dir / "minimal_properties_phase1_summary.json"
    report_path = out_dir / "MINIMAL_PROPERTIES_PHASE1_REPORT.md"

    patch_records: list[dict[str, Any]] = []
    for node_id in sorted(node_props_by_id):
        patch_records.append(
            {
                "op": "remove_node_properties",
                "id": node_id,
                "properties": sorted(node_props_by_id[node_id]),
            }
        )
    for rel_id in sorted(rel_props_by_id):
        patch_records.append(
            {
                "op": "remove_rel_properties",
                "rel_id": rel_id,
                "properties": sorted(rel_props_by_id[rel_id]),
            }
        )

    with patch_path.open("w", encoding="utf-8", newline="\n") as f:
        for record in patch_records:
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    unaddressed_groups: dict[tuple[str, str], int] = defaultdict(int)
    for row in rel_unaddressed:
        unaddressed_groups[(row["type"], row["property"])] += 1
    cypher_lines = [
        "// Phase 1 P0 relationship-property cleanup for rels without r.id.",
        "// Generated for review only; apply after backup if accepted.",
        f"// Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
    ]
    for (rel_type, prop), count in sorted(unaddressed_groups.items()):
        cypher_lines.extend(
            [
                f"// {count} relationships: {rel_type}.{prop}",
                f"MATCH ()-[r:`{rel_type}`]->()",
                f"WHERE r.`{prop}` IS NOT NULL",
                f"REMOVE r.`{prop}`;",
                "",
            ]
        )
    cypher_path.write_text("\n".join(cypher_lines), encoding="utf-8")

    summary = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "database": database,
        "connection": {"uri": uri, "user": user},
        "audit_dir": str(audit_dir.relative_to(repo_root())),
        "source_rows": len(rows),
        "node_source_rows": len(node_rows),
        "relationship_source_rows": len(rel_rows),
        "patch_path": str(patch_path.relative_to(repo_root())),
        "cypher_review_path": str(cypher_path.relative_to(repo_root())),
        "patch_records": len(patch_records),
        "node_patch_records": len(node_props_by_id),
        "relationship_patch_records": len(rel_props_by_id),
        "node_properties_to_remove": sum(len(v) for v in node_props_by_id.values()),
        "relationship_properties_to_remove": sum(len(v) for v in rel_props_by_id.values()),
        "unaddressed_relationship_properties": len(rel_unaddressed),
        "unaddressed_groups": [
            {"type": rel_type, "property": prop, "count": count}
            for (rel_type, prop), count in sorted(unaddressed_groups.items())
        ],
        "graph_counts_before_generation": {
            "nodes": int(before_counts["nodes"]),
            "relationships": int(before_counts["relationships"]),
        },
        "source_counts": source_counts,
    }
    write_json(summary_path, summary)

    report_lines = [
        "# Minimal properties Phase 1 P0 patch",
        "",
        f"**Generated UTC:** {summary['created_at_utc']}",
        f"**Database:** `{database}`",
        "",
        "## Outputs",
        "",
        f"- Patch: `{summary['patch_path']}`",
        f"- Unaddressed rel Cypher: `{summary['cypher_review_path']}`",
        f"- Summary: `{str(summary_path.relative_to(repo_root()))}`",
        "",
        "## Counts",
        "",
        f"- Patch records: {summary['patch_records']}",
        f"- Node patch records: {summary['node_patch_records']}",
        f"- Relationship patch records: {summary['relationship_patch_records']}",
        f"- Node property removals: {summary['node_properties_to_remove']}",
        f"- Relationship property removals via JSONL patch: {summary['relationship_properties_to_remove']}",
        f"- Relationship property removals parked as Cypher: {summary['unaddressed_relationship_properties']}",
        "",
        "## Unaddressed relationship rows",
        "",
    ]
    if summary["unaddressed_groups"]:
        report_lines.extend(["| Type | Property | Count |", "|---|---|---:|"])
        report_lines.extend(
            f"| `{row['type']}` | `{row['property']}` | {row['count']} |"
            for row in summary["unaddressed_groups"]
        )
    else:
        report_lines.append("_None._")
    report_lines.extend(
        [
            "",
            "## Apply protocol",
            "",
            "1. Backup `mit-bestand`.",
            "2. Dry-run the JSONL patch.",
            "3. Apply the JSONL patch only if dry-run reports zero errors.",
            "4. Review the Cypher file separately; it handles rels without `r.id`.",
            "5. Rerun `_scripts/_gap_survey.py` and the minimal-property audit.",
            "",
        ]
    )
    report_path.write_text("\n".join(report_lines), encoding="utf-8")

    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--audit-dir",
        type=Path,
        default=repo_root() / "_neo4j" / "review" / "2026-06-01_minimal_property_audit_mit-bestand",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=repo_root() / "_neo4j" / "review" / "2026-06-01_minimal_property_audit_mit-bestand" / "phase1_p0",
    )
    args = parser.parse_args()
    summary = generate(args.audit_dir, args.out_dir)
    print(json.dumps(json_safe(summary), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
