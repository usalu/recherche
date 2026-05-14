"""Apply or dry-run a Neo4j review patch JSONL file.

Supported operations:
  - add_node           (id/labels/properties at root OR nested under 'record' key)
  - set_node_properties
  - canonicalize_node
  - set_property       (single property: id + property + value)
  - add_rel            (from + type + to + optional properties)
  - noop_reviewed      (log-only, no DB write)

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


SUPPORTED_OPS = {"add_node", "set_node_properties", "canonicalize_node", "set_property", "add_rel", "noop_reviewed"}
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
            if "op" not in record:
                errors.append({"line": lineno, "error": "missing required field: op"})
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


def rel_type_safe(rel_type: str) -> str:
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', rel_type):
        raise ValueError(f"unsafe relationship type: {rel_type!r}")
    return rel_type


def current_rel_exists(session, from_id: str, rel_type: str, to_id: str) -> bool:
    result = session.run(
        "MATCH (a {id: $from_id})-[r]->(b {id: $to_id}) "
        "WHERE type(r) = $rel_type RETURN count(r) AS c",
        from_id=from_id, to_id=to_id, rel_type=rel_type,
    ).single()
    return result is not None and int(result["c"]) > 0


def extract_add_node_fields(record: dict) -> tuple[str | None, list, dict]:
    """Support both flat and nested-record add_node formats."""
    if "record" in record and isinstance(record["record"], dict):
        inner = record["record"]
        return inner.get("id"), inner.get("labels") or [], dict(inner.get("properties") or {})
    return record.get("id"), record.get("labels") or [], dict(record.get("properties") or {})


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


def plan_record(session, record: dict, pending_node_ids: set[str] | None = None) -> dict:
    op = record.get("op")
    line = record.get("_line")
    pending = pending_node_ids or set()
    if op not in SUPPORTED_OPS:
        return {
            "line": line,
            "op": op,
            "status": "unsupported",
            "error": f"Unsupported operation {op!r}",
        }

    if op == "noop_reviewed":
        return {
            "line": line,
            "op": op,
            "id": record.get("target_id") or record.get("id"),
            "status": "noop_reviewed",
            "reason": record.get("reason") or record.get("evidence"),
        }

    if op == "set_property":
        node_id = record.get("id")
        prop_key = record.get("property")
        prop_value = record.get("value")
        if not node_id or not prop_key:
            return {"line": line, "op": op, "status": "invalid", "error": "set_property requires id and property"}
        existing = current_node(session, node_id)
        if existing is None and node_id not in pending:
            return {"line": line, "op": op, "id": node_id, "status": "missing_node"}
        if existing is None:
            return {"line": line, "op": op, "id": node_id, "status": "would_update", "note": "node created earlier in same patch"}
        same = existing["properties"].get(prop_key) == prop_value
        after_props = dict(existing["properties"])
        after_props[prop_key] = prop_value
        return {
            "line": line,
            "op": op,
            "id": node_id,
            "property": prop_key,
            "status": "noop_same" if same else "would_update",
            "before": existing,
            "after": {"labels": existing["labels"], "properties": after_props},
        }

    if op == "add_rel":
        from_id = record.get("from")
        to_id = record.get("to")
        rel_type = record.get("type")
        if not from_id or not to_id or not rel_type:
            return {"line": line, "op": op, "status": "invalid", "error": "add_rel requires from, type, to"}
        try:
            rel_type_safe(rel_type)
        except ValueError as exc:
            return {"line": line, "op": op, "status": "invalid", "error": str(exc)}
        from_exists = current_node(session, from_id) is not None or from_id in pending
        to_exists = current_node(session, to_id) is not None or to_id in pending
        if not from_exists:
            return {"line": line, "op": op, "status": "missing_endpoint", "error": f"from node {from_id!r} not found"}
        if not to_exists:
            return {"line": line, "op": op, "status": "missing_endpoint", "error": f"to node {to_id!r} not found"}
        # Only check for existing relationship when both nodes are in the live DB
        if from_id not in pending and to_id not in pending:
            exists = current_rel_exists(session, from_id, rel_type, to_id)
        else:
            exists = False
        return {
            "line": line,
            "op": op,
            "from": from_id,
            "rel_type": rel_type,
            "to": to_id,
            "status": "noop_existing_rel" if exists else "would_create_rel",
        }

    if op == "add_node":
        node_id, labels, properties = extract_add_node_fields(record)
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
    _safe_statuses = {
        "would_create", "would_update", "noop_existing", "noop_same",
        "would_create_rel", "noop_existing_rel", "noop_reviewed",
    }
    if status not in _safe_statuses:
        raise RuntimeError(f"Refusing to apply record with status {status!r}")
    if status in {"noop_existing", "noop_same", "noop_existing_rel", "noop_reviewed"}:
        return

    op = record["op"]
    if op == "noop_reviewed":
        return

    if op == "set_property":
        session.run(
            "MATCH (n {id: $id}) SET n[$key] = $value",
            id=record["id"],
            key=record["property"],
            value=record["value"],
        ).consume()
        return

    if op == "add_rel":
        rel_type = record["type"]
        props = dict(record.get("properties") or {})
        cypher = (
            f"MATCH (a {{id: $from_id}}), (b {{id: $to_id}}) "
            f"MERGE (a)-[r:`{rel_type}`]->(b) "
            "SET r += $props"
        )
        session.run(cypher, from_id=record["from"], to_id=record["to"], props=props).consume()
        return

    if op == "add_node":
        node_id, labels, properties = extract_add_node_fields(record)
        properties = {"id": node_id, **properties}
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
        row for row in payload["records"] if row["status"] in {"unsupported", "invalid", "missing_node", "missing_endpoint"}
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
            # Build pending-node set incrementally so add_rel records can
            # reference nodes created earlier in the same patch.
            pending_node_ids: set[str] = set()
            planned: list[dict] = []
            for record in records:
                row = plan_record(session, record, pending_node_ids)
                planned.append(row)
                if record.get("op") == "add_node" and row.get("status") == "would_create":
                    nid, _, _ = extract_add_node_fields(record)
                    if nid:
                        pending_node_ids.add(nid)
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
                row for row in planned if row["status"] in {"unsupported", "invalid", "missing_node", "missing_endpoint"}
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
    would_create_rel = status_counts.get("would_create_rel", 0)
    counts_after_expected = {
        "nodes": counts_before["nodes"] + would_create,
        "relationships": counts_before["relationships"] + would_create_rel,
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
