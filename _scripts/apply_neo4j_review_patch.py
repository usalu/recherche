"""Apply or dry-run a Neo4j review patch JSONL file.

Supported operations for the first controlled workflow:
  - add_node
  - set_node_properties
  - canonicalize_node

The default is a dry-run. Live mutation requires the exact phrase:

  APPLY <patch-file-name> TO <database>

Examples:
  python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/round_001/patches/accepted_blockers.patch.jsonl
  python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/round_001/patches/accepted_blockers.patch.jsonl --confirm "APPLY accepted_blockers.patch.jsonl TO mit-bestand"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import repo_root, resolve_connection  # noqa: E402


SUPPORTED_OPS = {"add_node", "set_node_properties", "canonicalize_node"}
LABEL_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


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


def load_patch(path: Path) -> tuple[list[dict], list[dict]]:
    records: list[dict] = []
    errors: list[dict] = []
    with path.open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append({"line": lineno, "error": f"JSON parse error: {exc}"})
                continue
            if "op" not in record or "reason" not in record:
                errors.append({"line": lineno, "error": "missing required op/reason"})
            records.append({**record, "_line": lineno})
    return records, errors


def label_clause(labels: list[str]) -> str:
    if not labels:
        raise ValueError("add_node requires at least one label")
    unsafe = [label for label in labels if not LABEL_RE.match(label)]
    if unsafe:
        raise ValueError(f"unsafe label(s): {unsafe}")
    return "".join(f":`{label}`" for label in labels)


def report_dir_for_patch(patch_path: Path, explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit if explicit.is_absolute() else repo_root() / explicit
    resolved = patch_path.resolve()
    parts = list(resolved.parts)
    if "patches" in parts:
        patch_idx = parts.index("patches")
        if patch_idx > 0:
            return Path(*parts[:patch_idx]) / "apply_reports"
    return repo_root() / "_neo4j" / "review" / "apply_reports"


def get_counts(session) -> dict[str, int]:
    rec = session.run(
        "MATCH (n) WITH count(n) AS nodes "
        "MATCH ()-[r]->() RETURN nodes, count(r) AS relationships"
    ).single()
    return {"nodes": int(rec["nodes"]), "relationships": int(rec["relationships"])}


def current_node(session, node_id: str) -> dict | None:
    rec = session.run(
        "MATCH (n {id: $id}) RETURN labels(n) AS labels, properties(n) AS properties",
        id=node_id,
    ).single()
    if rec is None:
        return None
    return {"labels": list(rec["labels"]), "properties": json_safe(dict(rec["properties"]))}


def merge_aliases(existing: Any, incoming: list[str]) -> list[str]:
    aliases: list[str] = []
    if isinstance(existing, list):
        aliases.extend(str(item) for item in existing if str(item).strip())
    elif isinstance(existing, str) and existing.strip():
        aliases.append(existing)
    for alias in incoming:
        alias = str(alias).strip()
        if alias and alias not in aliases:
            aliases.append(alias)
    return aliases


def plan_record(session, record: dict) -> dict:
    op = record.get("op")
    line = record.get("_line")
    if op not in SUPPORTED_OPS:
        return {
            "line": line,
            "op": op,
            "status": "unsupported",
            "error": f"Unsupported operation {op!r}",
        }

    if op == "add_node":
        node_id = record.get("id")
        labels = record.get("labels") or []
        properties = dict(record.get("properties") or {})
        if not node_id or not labels:
            return {"line": line, "op": op, "status": "invalid", "error": "add_node requires id and labels"}
        try:
            label_clause(labels)
        except ValueError as exc:
            return {"line": line, "op": op, "id": node_id, "status": "invalid", "error": str(exc)}
        existing = current_node(session, node_id)
        return {
            "line": line,
            "op": op,
            "id": node_id,
            "status": "noop_existing" if existing else "would_create",
            "before": existing,
            "after": {
                "labels": labels,
                "properties": {"id": node_id, **properties},
            },
        }

    if op == "set_node_properties":
        node_id = record.get("id")
        properties = dict(record.get("properties") or {})
        if not node_id:
            return {"line": line, "op": op, "status": "invalid", "error": "set_node_properties requires id"}
        existing = current_node(session, node_id)
        if existing is None:
            return {"line": line, "op": op, "id": node_id, "status": "missing_node"}
        after_props = dict(existing["properties"])
        after_props.update(properties)
        return {
            "line": line,
            "op": op,
            "id": node_id,
            "status": "would_update" if after_props != existing["properties"] else "noop_same",
            "before": existing,
            "after": {"labels": existing["labels"], "properties": after_props},
        }

    node_id = record.get("id")
    canonical_name = record.get("canonical_name")
    aliases = list(record.get("aliases") or [])
    if not node_id or not canonical_name:
        return {"line": line, "op": op, "status": "invalid", "error": "canonicalize_node requires id and canonical_name"}
    existing = current_node(session, node_id)
    if existing is None:
        return {"line": line, "op": op, "id": node_id, "status": "missing_node"}
    before_props = existing["properties"]
    candidate_aliases = [alias for alias in aliases if alias != canonical_name]
    old_name = before_props.get("name")
    if old_name and old_name != canonical_name:
        candidate_aliases.append(str(old_name))
    after_props = dict(before_props)
    after_props["name"] = canonical_name
    merged_aliases = merge_aliases(before_props.get("aliases"), candidate_aliases)
    if merged_aliases:
        after_props["aliases"] = merged_aliases
    return {
        "line": line,
        "op": op,
        "id": node_id,
        "status": "would_update" if after_props != before_props else "noop_same",
        "before": existing,
        "after": {"labels": existing["labels"], "properties": after_props},
    }


def apply_record(session, record: dict, planned: dict) -> None:
    status = planned.get("status")
    if status not in {"would_create", "would_update", "noop_existing", "noop_same"}:
        raise RuntimeError(f"Refusing to apply record with status {status!r}")
    if status in {"noop_existing", "noop_same"}:
        return

    op = record["op"]
    if op == "add_node":
        node_id = record["id"]
        labels = record["labels"]
        properties = {"id": node_id, **dict(record.get("properties") or {})}
        cypher = (
            f"MERGE (n{label_clause(labels)} {{id: $id}}) "
            "SET n += $properties"
        )
        session.run(cypher, id=node_id, properties=properties).consume()
        return

    if op == "set_node_properties":
        session.run(
            "MATCH (n {id: $id}) SET n += $properties",
            id=record["id"],
            properties=dict(record.get("properties") or {}),
        ).consume()
        return

    if op == "canonicalize_node":
        after = planned["after"]["properties"]
        session.run(
            "MATCH (n {id: $id}) SET n.name = $name, n.aliases = $aliases",
            id=record["id"],
            name=after.get("name"),
            aliases=after.get("aliases", []),
        ).consume()
        return

    raise RuntimeError(f"Unsupported op reached apply path: {op!r}")


def write_reports(report_dir: Path, patch_path: Path, payload: dict) -> tuple[Path, Path]:
    report_dir.mkdir(parents=True, exist_ok=True)
    stem = patch_path.stem
    json_path = report_dir / f"{stem}.apply_report.json"
    md_path = report_dir / f"{stem}.apply_report.md"
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    summary = payload["summary"]
    lines = [
        f"# Patch Apply Report: {patch_path.name}",
        "",
        f"Generated: {payload['generated_at_utc']}",
        f"Mode: {'dry-run' if payload['dry_run'] else 'live apply'}",
        f"Database: {payload['database']}",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | --- |",
    ]
    for key, value in summary.items():
        lines.append(f"| {key} | {value} |")
    lines.extend(
        [
            "",
            "## Counts",
            "",
            "| State | Nodes | Relationships |",
            "| --- | --- | --- |",
            f"| before | {payload['counts_before']['nodes']} | {payload['counts_before']['relationships']} |",
            f"| after_expected | {payload['counts_after_expected']['nodes']} | {payload['counts_after_expected']['relationships']} |",
        ]
    )
    if payload.get("counts_after_actual"):
        lines.append(
            f"| after_actual | {payload['counts_after_actual']['nodes']} | {payload['counts_after_actual']['relationships']} |"
        )
    lines.extend(["", "## Rejected / Needs Review", ""])
    rejected = [
        row for row in payload["records"] if row["status"] in {"unsupported", "invalid", "missing_node"}
    ]
    if rejected:
        lines.extend(["| Line | Op | Id | Status | Error |", "| --- | --- | --- | --- | --- |"])
        for row in rejected:
            lines.append(
                f"| {row.get('line', '')} | {row.get('op', '')} | {row.get('id', '')} | "
                f"{row.get('status', '')} | {row.get('error', '')} |"
            )
    else:
        lines.append("None.")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def run(args: argparse.Namespace) -> dict:
    try:
        from neo4j import GraphDatabase
    except ImportError as exc:
        raise SystemExit("Install: pip install -r requirements-neo4j.txt") from exc

    patch_path = args.patch.resolve()
    records, load_errors = load_patch(patch_path)
    uri, user, password, default_database = resolve_connection()
    database = args.database or default_database
    if not uri or not user or not password or not database:
        raise SystemExit("Missing Neo4j connection settings.")

    expected_confirm = f"APPLY {patch_path.name} TO {database}"
    dry_run = args.dry_run or not args.confirm
    if args.confirm:
        if args.confirm != expected_confirm:
            raise SystemExit(
                "Refusing live patch apply. Confirmation must exactly equal: "
                f"{expected_confirm!r}"
            )
        dry_run = False

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            counts_before = get_counts(session)
            planned = [plan_record(session, record) for record in records]
            if load_errors:
                planned.extend(
                    {
                        "line": error.get("line"),
                        "op": None,
                        "status": "invalid",
                        "error": error["error"],
                    }
                    for error in load_errors
                )

            rejected = [
                row for row in planned if row["status"] in {"unsupported", "invalid", "missing_node"}
            ]
            if rejected and not dry_run:
                raise SystemExit("Refusing live apply while rejected/invalid records exist.")

            if not dry_run:
                for record, row in zip(records, planned):
                    apply_record(session, record, row)

            counts_after_actual = None if dry_run else get_counts(session)
    finally:
        driver.close()

    status_counts = Counter(row["status"] for row in planned)
    would_create = status_counts.get("would_create", 0)
    counts_after_expected = {
        "nodes": counts_before["nodes"] + would_create,
        "relationships": counts_before["relationships"],
    }
    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "patch": str(patch_path.relative_to(repo_root())),
        "database": database,
        "dry_run": dry_run,
        "confirmation_required": expected_confirm,
        "counts_before": counts_before,
        "counts_after_expected": counts_after_actual or counts_after_expected,
        "counts_after_actual": counts_after_actual,
        "summary": {
            "records": len(records),
            "load_errors": len(load_errors),
            **dict(sorted(status_counts.items())),
        },
        "records": planned,
    }
    report_dir = report_dir_for_patch(patch_path, args.report_dir)
    json_path, md_path = write_reports(report_dir, patch_path, payload)
    payload["report_files"] = [
        str(json_path.resolve().relative_to(repo_root())),
        str(md_path.resolve().relative_to(repo_root())),
    ]
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--patch", type=Path, required=True)
    parser.add_argument("--database", default="")
    parser.add_argument("--dry-run", action="store_true", default=True)
    parser.add_argument("--confirm", default="")
    parser.add_argument("--report-dir", type=Path, default=None)
    args = parser.parse_args()
    result = run(args)
    print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
