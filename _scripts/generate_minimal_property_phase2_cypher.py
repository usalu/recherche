"""Generate grouped Cypher for Phase 2 minimal-property cleanup.

Phase 2 removes P1 `drop_candidate` properties from the post-Phase-1 audit.
These are generated/import/cache/debug fields. The output is grouped Cypher:
one statement per label/property or relationship-type/property pair.

This script does not mutate Neo4j.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


LABEL_RE = re.compile(r"^[^\W\d]\w*$", re.UNICODE)
PROP_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def safe_ident(value: str) -> str:
    if not LABEL_RE.match(value):
        raise ValueError(f"unsafe label/type: {value!r}")
    return value


def safe_prop(value: str) -> str:
    if not PROP_RE.match(value):
        raise ValueError(f"unsafe property: {value!r}")
    return value


def read_rows(path: Path, entity: str) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    return [
        {**row, "entity": entity}
        for row in rows
        if row.get("priority") == "P1" and row.get("action") == "drop_candidate"
    ]


def write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--audit-dir",
        type=Path,
        default=Path("_neo4j/review/2026-06-01_minimal_property_audit_post_phase1_p0_mit-bestand"),
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("_neo4j/review/2026-06-01_minimal_property_audit_post_phase1_p0_mit-bestand/phase2_p1_generated_metadata"),
    )
    args = parser.parse_args()

    audit_dir = args.audit_dir
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    rows.extend(read_rows(audit_dir / "node_property_minimization.csv", "node"))
    rows.extend(read_rows(audit_dir / "relationship_property_minimization.csv", "relationship"))
    rows.sort(key=lambda r: (r["entity"], r["group"], r["property"]))

    cypher_path = out_dir / "minimal_properties_phase2_p1_generated_metadata.cypher"
    summary_path = out_dir / "minimal_properties_phase2_p1_summary.json"
    report_path = out_dir / "MINIMAL_PROPERTIES_PHASE2_PLAN.md"

    lines = [
        "// Phase 2 P1 generated/import/cache/debug property cleanup.",
        "// Generated for review; backup before applying.",
        f"// Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
    ]
    summary_rows: list[dict[str, Any]] = []
    for idx, row in enumerate(rows, 1):
        group = safe_ident(row["group"])
        prop = safe_prop(row["property"])
        count = int(row["nodes_or_rels_with_property"])
        reason = row.get("reason") or ""
        if row["entity"] == "node":
            lines.extend(
                [
                    f"// P1.{idx}: node {group}.{prop} ({count}) - {reason}",
                    f"MATCH (n:`{group}`)",
                    f"WHERE n.`{prop}` IS NOT NULL",
                    f"REMOVE n.`{prop}`;",
                    "",
                ]
            )
        else:
            lines.extend(
                [
                    f"// P1.{idx}: relationship {group}.{prop} ({count}) - {reason}",
                    f"MATCH ()-[r:`{group}`]->()",
                    f"WHERE r.`{prop}` IS NOT NULL",
                    f"REMOVE r.`{prop}`;",
                    "",
                ]
            )
        summary_rows.append(
            {
                "index": idx,
                "entity": row["entity"],
                "group": group,
                "property": prop,
                "audit_count": count,
                "reason": reason,
            }
        )

    cypher_path.write_text("\n".join(lines), encoding="utf-8")
    summary = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "audit_dir": str(audit_dir),
        "cypher_path": str(cypher_path),
        "source_rows": len(rows),
        "node_rows": sum(1 for row in rows if row["entity"] == "node"),
        "relationship_rows": sum(1 for row in rows if row["entity"] == "relationship"),
        "audit_property_occurrences": sum(int(row["nodes_or_rels_with_property"]) for row in rows),
        "rows": summary_rows,
    }
    write_json(summary_path, summary)

    report_lines = [
        "# Minimal properties Phase 2 plan",
        "",
        f"**Generated UTC:** {summary['created_at_utc']}",
        "",
        "Scope: P1 `drop_candidate` properties from the post-Phase-1 audit.",
        "",
        "## Counts",
        "",
        f"- Statements: {summary['source_rows']}",
        f"- Node label/property rows: {summary['node_rows']}",
        f"- Relationship type/property rows: {summary['relationship_rows']}",
        f"- Audit property occurrences: {summary['audit_property_occurrences']}",
        "",
        "## Files",
        "",
        f"- Cypher: `{cypher_path}`",
        f"- Summary: `{summary_path}`",
        "",
        "## Protocol",
        "",
        "1. Count each statement before apply.",
        "2. Backup `mit-bestand`.",
        "3. Apply grouped Cypher.",
        "4. Verify all targeted P1 rows are zero.",
        "5. Rerun `_scripts/_gap_survey.py` and the minimal-property audit.",
        "",
    ]
    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "rows"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
