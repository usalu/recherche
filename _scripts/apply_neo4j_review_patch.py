"""Apply or dry-run a Neo4j review patch JSONL file.

Supported operations:
  - add_node                 (id/labels/properties at root OR nested under 'record' key)
  - set_node_properties      (id + properties dict)
  - canonicalize_node        (id + canonical_name + aliases)
  - set_property             (single property: id + property + value)
  - add_rel                  (from + type + to + optional properties)
  - noop_reviewed            (log-only, no DB write)
  - merge_node               (from + to: redirect rels, union labels/props, then delete from)
  - delete_node              (id; refused for Quelle/Datenqualitaet or nodes with BELEGT_IN)
  - delete_rel               (id OR from/type/to)
  - set_rel_properties       (id OR from/type/to + properties dict)
  - remove_node_properties   (id + properties: list of keys to remove)
  - remove_rel_properties    (id OR from/type/to + properties: list of keys)
  - rename_property          (id + from + to; node-scoped property rename)
  - move_property            (from_id + to_id + property; copy + remove)
  - replace_rel_type         (from + old_type + to + new_type; rebuilds rel under new type)

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


SUPPORTED_OPS = {
    "add_node", "set_node_properties", "canonicalize_node", "set_property",
    "add_rel", "noop_reviewed",
    "merge_node", "delete_node", "delete_rel", "set_rel_properties",
    "remove_node_properties", "remove_rel_properties",
    "rename_property", "move_property", "replace_rel_type",
}
LABEL_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
PROP_KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def prop_key_safe(key: str) -> str:
    if not PROP_KEY_RE.match(key):
        raise ValueError(f"unsafe property key: {key!r}")
    return key


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


def node_belegt_in_count(session, node_id: str) -> int:
    rec = session.run(
        "MATCH (n {id: $id}) "
        "OPTIONAL MATCH (n)-[r1:BELEGT_IN]->() "
        "OPTIONAL MATCH (n)<-[r2:BELEGT_IN]-() "
        "RETURN count(DISTINCT r1) + count(DISTINCT r2) AS c",
        id=node_id,
    ).single()
    return int(rec["c"]) if rec else 0


def node_rel_summary(session, node_id: str) -> dict[str, int]:
    """Return rel counts for a node, used for merge_node planning."""
    rec = session.run(
        "MATCH (n {id: $id}) "
        "OPTIONAL MATCH (n)<-[r_in]-() "
        "OPTIONAL MATCH (n)-[r_out]->() "
        "RETURN count(DISTINCT r_in) AS inbound, count(DISTINCT r_out) AS outbound",
        id=node_id,
    ).single()
    if rec is None:
        return {"inbound": 0, "outbound": 0}
    return {"inbound": int(rec["inbound"]), "outbound": int(rec["outbound"])}


def locate_rel(session, record: dict) -> dict | None:
    """Locate one relationship by id (rel property) or by endpoints+type.

    Returns {"rel_internal_id", "from", "to", "type", "properties", "count"}
    where count is how many matched (caller must refuse if >1 and no rel id).
    """
    rel_id = record.get("rel_id") or record.get("id")
    if rel_id:
        rows = list(
            session.run(
                "MATCH (a)-[r]->(b) WHERE r.id = $rid "
                "RETURN id(r) AS rid_internal, a.id AS from_id, b.id AS to_id, "
                "type(r) AS rel_type, properties(r) AS props",
                rid=rel_id,
            )
        )
        if not rows:
            return None
        return {
            "rel_internal_id": rows[0]["rid_internal"],
            "from": rows[0]["from_id"],
            "to": rows[0]["to_id"],
            "type": rows[0]["rel_type"],
            "properties": json_safe(dict(rows[0]["props"])),
            "count": len(rows),
        }
    from_id = record.get("from")
    to_id = record.get("to")
    rel_type = record.get("type")
    if not (from_id and to_id and rel_type):
        return None
    try:
        rel_type_safe(rel_type)
    except ValueError:
        return None
    rows = list(
        session.run(
            f"MATCH (a {{id: $from_id}})-[r:`{rel_type}`]->(b {{id: $to_id}}) "
            "RETURN id(r) AS rid_internal, a.id AS from_id, b.id AS to_id, "
            "type(r) AS rel_type, properties(r) AS props",
            from_id=from_id, to_id=to_id,
        )
    )
    if not rows:
        return None
    return {
        "rel_internal_id": rows[0]["rid_internal"],
        "from": rows[0]["from_id"],
        "to": rows[0]["to_id"],
        "type": rows[0]["rel_type"],
        "properties": json_safe(dict(rows[0]["props"])),
        "count": len(rows),
    }


def plan_merge_node(session, record: dict) -> dict:
    line = record.get("_line")
    from_id = record.get("from")
    to_id = record.get("to")
    if not from_id or not to_id:
        return {"line": line, "op": "merge_node", "status": "invalid", "error": "merge_node requires from and to"}
    if from_id == to_id:
        return {"line": line, "op": "merge_node", "status": "invalid", "error": "merge_node from == to"}
    src = current_node(session, from_id)
    dst = current_node(session, to_id)
    if src is None:
        return {
            "line": line, "op": "merge_node", "from": from_id, "to": to_id,
            "status": "noop_missing_source",
            "reason": "source node already absent — merge is idempotent",
        }
    if dst is None:
        return {
            "line": line, "op": "merge_node", "from": from_id, "to": to_id,
            "status": "missing_node", "error": f"merge target {to_id!r} not found",
        }
    src_rels = node_rel_summary(session, from_id)
    src_props = src["properties"]
    dst_props = dst["properties"]
    src_labels = src["labels"]
    dst_labels = dst["labels"]
    union_labels = list(dst_labels) + [lbl for lbl in src_labels if lbl not in dst_labels]
    union_props = dict(dst_props)
    for k, v in src_props.items():
        if k == "aliases":
            continue
        if k == "id":
            continue
        if k not in union_props or union_props[k] in (None, ""):
            union_props[k] = v
    # Source name preserved as alias on the survivor unless patch overrides.
    incoming_aliases = list(record.get("aliases") or [])
    src_name = src_props.get("name")
    if src_name and src_name != union_props.get("name") and src_name not in incoming_aliases:
        incoming_aliases.append(str(src_name))
    if incoming_aliases:
        union_props["aliases"] = merge_aliases(dst_props.get("aliases"), incoming_aliases)
    return {
        "line": line, "op": "merge_node",
        "from": from_id, "to": to_id,
        "status": "would_merge",
        "rel_inbound_to_redirect": src_rels["inbound"],
        "rel_outbound_to_redirect": src_rels["outbound"],
        "label_union": union_labels,
        "before": {"from": src, "to": dst},
        "after": {"labels": union_labels, "properties": union_props},
    }


def plan_delete_node(session, record: dict) -> dict:
    line = record.get("_line")
    node_id = record.get("id")
    if not node_id:
        return {"line": line, "op": "delete_node", "status": "invalid", "error": "delete_node requires id"}
    existing = current_node(session, node_id)
    if existing is None:
        return {"line": line, "op": "delete_node", "id": node_id, "status": "noop_missing"}
    forbidden_labels = {"Quelle", "Datenqualitaet"}
    blocked = forbidden_labels & set(existing["labels"])
    if blocked:
        return {
            "line": line, "op": "delete_node", "id": node_id, "status": "rejected",
            "error": f"delete_node refused for protected labels: {sorted(blocked)}",
        }
    evidence = node_belegt_in_count(session, node_id)
    if evidence > 0:
        return {
            "line": line, "op": "delete_node", "id": node_id, "status": "rejected",
            "error": f"delete_node refused: node has {evidence} BELEGT_IN evidence rel(s) attached",
        }
    rels = node_rel_summary(session, node_id)
    return {
        "line": line, "op": "delete_node", "id": node_id, "status": "would_delete_node",
        "rel_inbound_to_remove": rels["inbound"],
        "rel_outbound_to_remove": rels["outbound"],
        "before": existing,
    }


def plan_delete_rel(session, record: dict) -> dict:
    line = record.get("_line")
    located = locate_rel(session, record)
    if located is None:
        return {"line": line, "op": "delete_rel", "status": "noop_missing"}
    if located["count"] > 1:
        return {
            "line": line, "op": "delete_rel", "status": "invalid",
            "error": f"{located['count']} rels match — disambiguate with rel id",
        }
    return {
        "line": line, "op": "delete_rel", "status": "would_delete_rel",
        "from": located["from"], "to": located["to"], "type": located["type"],
        "before": located,
    }


def plan_set_rel_properties(session, record: dict) -> dict:
    line = record.get("_line")
    located = locate_rel(session, record)
    if located is None:
        return {"line": line, "op": "set_rel_properties", "status": "missing_rel", "error": "rel not found"}
    if located["count"] > 1:
        return {
            "line": line, "op": "set_rel_properties", "status": "invalid",
            "error": f"{located['count']} rels match — disambiguate with rel id",
        }
    props = dict(record.get("properties") or {})
    if not props:
        return {"line": line, "op": "set_rel_properties", "status": "invalid", "error": "no properties supplied"}
    after = dict(located["properties"])
    after.update(props)
    return {
        "line": line, "op": "set_rel_properties",
        "from": located["from"], "to": located["to"], "type": located["type"],
        "status": "would_update_rel" if after != located["properties"] else "noop_same_rel",
        "before": located,
        "after_properties": after,
    }


def plan_remove_node_properties(session, record: dict) -> dict:
    line = record.get("_line")
    node_id = record.get("id")
    keys = list(record.get("properties") or [])
    if not node_id or not keys:
        return {"line": line, "op": "remove_node_properties", "status": "invalid", "error": "id + properties (list) required"}
    try:
        for k in keys:
            prop_key_safe(k)
    except ValueError as exc:
        return {"line": line, "op": "remove_node_properties", "id": node_id, "status": "invalid", "error": str(exc)}
    existing = current_node(session, node_id)
    if existing is None:
        return {"line": line, "op": "remove_node_properties", "id": node_id, "status": "missing_node"}
    keys_present = [k for k in keys if k in existing["properties"]]
    if not keys_present:
        return {
            "line": line, "op": "remove_node_properties", "id": node_id,
            "status": "noop_same", "before": existing,
        }
    after = {k: v for k, v in existing["properties"].items() if k not in keys_present}
    return {
        "line": line, "op": "remove_node_properties", "id": node_id,
        "status": "would_update", "keys_removed": keys_present,
        "before": existing,
        "after": {"labels": existing["labels"], "properties": after},
    }


def plan_remove_rel_properties(session, record: dict) -> dict:
    line = record.get("_line")
    keys = list(record.get("properties") or [])
    if not keys:
        return {"line": line, "op": "remove_rel_properties", "status": "invalid", "error": "properties (list of keys) required"}
    try:
        for k in keys:
            prop_key_safe(k)
    except ValueError as exc:
        return {"line": line, "op": "remove_rel_properties", "status": "invalid", "error": str(exc)}
    located = locate_rel(session, record)
    if located is None:
        return {"line": line, "op": "remove_rel_properties", "status": "missing_rel", "error": "rel not found"}
    if located["count"] > 1:
        return {
            "line": line, "op": "remove_rel_properties", "status": "invalid",
            "error": f"{located['count']} rels match — disambiguate with rel id",
        }
    keys_present = [k for k in keys if k in located["properties"]]
    if not keys_present:
        return {"line": line, "op": "remove_rel_properties", "status": "noop_same_rel", "before": located}
    after = {k: v for k, v in located["properties"].items() if k not in keys_present}
    return {
        "line": line, "op": "remove_rel_properties",
        "from": located["from"], "to": located["to"], "type": located["type"],
        "status": "would_update_rel", "keys_removed": keys_present,
        "before": located, "after_properties": after,
    }


def plan_rename_property(session, record: dict) -> dict:
    line = record.get("_line")
    node_id = record.get("id")
    old_key = record.get("from")
    new_key = record.get("to")
    if not node_id or not old_key or not new_key:
        return {"line": line, "op": "rename_property", "status": "invalid", "error": "id + from + to required"}
    try:
        prop_key_safe(old_key)
        prop_key_safe(new_key)
    except ValueError as exc:
        return {"line": line, "op": "rename_property", "id": node_id, "status": "invalid", "error": str(exc)}
    existing = current_node(session, node_id)
    if existing is None:
        return {"line": line, "op": "rename_property", "id": node_id, "status": "missing_node"}
    if old_key not in existing["properties"]:
        if new_key in existing["properties"]:
            return {"line": line, "op": "rename_property", "id": node_id, "status": "noop_same"}
        return {
            "line": line, "op": "rename_property", "id": node_id,
            "status": "noop_missing_source", "reason": f"node has no property {old_key!r}",
        }
    if new_key in existing["properties"] and existing["properties"][new_key] != existing["properties"][old_key]:
        return {
            "line": line, "op": "rename_property", "id": node_id, "status": "rejected",
            "error": f"target property {new_key!r} already set to a different value",
        }
    after = {k: v for k, v in existing["properties"].items() if k != old_key}
    after[new_key] = existing["properties"][old_key]
    return {
        "line": line, "op": "rename_property", "id": node_id,
        "from_key": old_key, "to_key": new_key,
        "status": "would_update", "before": existing,
        "after": {"labels": existing["labels"], "properties": after},
    }


def plan_move_property(session, record: dict) -> dict:
    line = record.get("_line")
    from_id = record.get("from_id")
    to_id = record.get("to_id")
    prop = record.get("property")
    if not from_id or not to_id or not prop:
        return {"line": line, "op": "move_property", "status": "invalid", "error": "from_id + to_id + property required"}
    try:
        prop_key_safe(prop)
    except ValueError as exc:
        return {"line": line, "op": "move_property", "status": "invalid", "error": str(exc)}
    src = current_node(session, from_id)
    dst = current_node(session, to_id)
    if src is None:
        return {"line": line, "op": "move_property", "status": "missing_node", "error": f"from_id {from_id!r} not found"}
    if dst is None:
        return {"line": line, "op": "move_property", "status": "missing_node", "error": f"to_id {to_id!r} not found"}
    if prop not in src["properties"]:
        if dst["properties"].get(prop) is not None:
            return {"line": line, "op": "move_property", "status": "noop_same"}
        return {"line": line, "op": "move_property", "status": "noop_missing_source"}
    value = src["properties"][prop]
    existing_dst = dst["properties"].get(prop)
    if existing_dst is not None and existing_dst != value:
        return {
            "line": line, "op": "move_property", "status": "rejected",
            "error": f"to_id {to_id!r} already has {prop!r}={existing_dst!r}, would conflict with {value!r}",
        }
    return {
        "line": line, "op": "move_property",
        "from_id": from_id, "to_id": to_id, "property": prop,
        "status": "would_update", "value": value,
        "before": {"from": src, "to": dst},
    }


def plan_replace_rel_type(session, record: dict) -> dict:
    line = record.get("_line")
    from_id = record.get("from")
    to_id = record.get("to")
    old_type = record.get("old_type")
    new_type = record.get("new_type")
    if not (from_id and to_id and old_type and new_type):
        return {"line": line, "op": "replace_rel_type", "status": "invalid", "error": "from + to + old_type + new_type required"}
    try:
        rel_type_safe(old_type)
        rel_type_safe(new_type)
    except ValueError as exc:
        return {"line": line, "op": "replace_rel_type", "status": "invalid", "error": str(exc)}
    if old_type == new_type:
        return {"line": line, "op": "replace_rel_type", "status": "invalid", "error": "old_type == new_type"}
    located = locate_rel(session, {"from": from_id, "type": old_type, "to": to_id})
    new_exists = current_rel_exists(session, from_id, new_type, to_id)
    if located is None:
        return {
            "line": line, "op": "replace_rel_type",
            "from": from_id, "to": to_id, "old_type": old_type, "new_type": new_type,
            "status": "noop_missing_source" if new_exists else "missing_rel",
        }
    if located["count"] > 1:
        return {
            "line": line, "op": "replace_rel_type", "status": "invalid",
            "error": f"{located['count']} rels of type {old_type!r} between these nodes — disambiguate",
        }
    return {
        "line": line, "op": "replace_rel_type",
        "from": from_id, "to": to_id, "old_type": old_type, "new_type": new_type,
        "status": "noop_existing_rel" if new_exists else "would_replace_rel",
        "before": located,
    }


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

    if op == "merge_node":
        return plan_merge_node(session, record)
    if op == "delete_node":
        return plan_delete_node(session, record)
    if op == "delete_rel":
        return plan_delete_rel(session, record)
    if op == "set_rel_properties":
        return plan_set_rel_properties(session, record)
    if op == "remove_node_properties":
        return plan_remove_node_properties(session, record)
    if op == "remove_rel_properties":
        return plan_remove_rel_properties(session, record)
    if op == "rename_property":
        return plan_rename_property(session, record)
    if op == "move_property":
        return plan_move_property(session, record)
    if op == "replace_rel_type":
        return plan_replace_rel_type(session, record)

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
        "would_merge", "noop_missing_source",
        "would_delete_node", "noop_missing",
        "would_delete_rel",
        "would_update_rel", "noop_same_rel",
        "would_replace_rel",
    }
    _noop_statuses = {
        "noop_existing", "noop_same", "noop_existing_rel", "noop_reviewed",
        "noop_missing_source", "noop_missing", "noop_same_rel",
    }
    if status not in _safe_statuses:
        raise RuntimeError(f"Refusing to apply record with status {status!r}")
    if status in _noop_statuses:
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

    if op == "merge_node":
        from_id = record["from"]
        to_id = record["to"]
        # 1. Redirect inbound rels from source onto target, preserving type and props.
        inbound = list(
            session.run(
                "MATCH (s {id: $from_id})<-[r]-(x) "
                "RETURN id(r) AS rid, x.id AS x_id, type(r) AS rt, properties(r) AS rp",
                from_id=from_id,
            )
        )
        for row in inbound:
            rt = rel_type_safe(row["rt"])
            session.run(
                f"MATCH (x {{id: $x_id}}), (t {{id: $to_id}}) "
                f"MERGE (x)-[r2:`{rt}`]->(t) SET r2 += $props",
                x_id=row["x_id"], to_id=to_id, props=json_safe(dict(row["rp"] or {})),
            ).consume()
        # 2. Redirect outbound rels.
        outbound = list(
            session.run(
                "MATCH (s {id: $from_id})-[r]->(x) "
                "RETURN id(r) AS rid, x.id AS x_id, type(r) AS rt, properties(r) AS rp",
                from_id=from_id,
            )
        )
        for row in outbound:
            rt = rel_type_safe(row["rt"])
            session.run(
                f"MATCH (t {{id: $to_id}}), (x {{id: $x_id}}) "
                f"MERGE (t)-[r2:`{rt}`]->(x) SET r2 += $props",
                to_id=to_id, x_id=row["x_id"], props=json_safe(dict(row["rp"] or {})),
            ).consume()
        # 3. Union labels onto target.
        label_union = planned.get("label_union") or []
        labels_to_add = [lbl for lbl in label_union if LABEL_RE.match(lbl)]
        if labels_to_add:
            clause = "".join(f":`{lbl}`" for lbl in labels_to_add)
            session.run(f"MATCH (t {{id: $to_id}}) SET t{clause}", to_id=to_id).consume()
        # 4. Set merged properties on target (canonical wins; id stays).
        after_props = dict(planned["after"]["properties"])
        after_props["id"] = to_id
        session.run(
            "MATCH (t {id: $to_id}) SET t += $props",
            to_id=to_id, props=after_props,
        ).consume()
        # 5. Detach-delete the source.
        session.run("MATCH (s {id: $from_id}) DETACH DELETE s", from_id=from_id).consume()
        return

    if op == "delete_node":
        session.run("MATCH (n {id: $id}) DETACH DELETE n", id=record["id"]).consume()
        return

    if op == "delete_rel":
        before = planned.get("before") or {}
        rid_internal = before.get("rel_internal_id")
        if rid_internal is not None:
            session.run("MATCH ()-[r]-() WHERE id(r) = $rid DELETE r", rid=rid_internal).consume()
            return
        rt = rel_type_safe(planned["type"])
        session.run(
            f"MATCH (a {{id: $from_id}})-[r:`{rt}`]->(b {{id: $to_id}}) DELETE r",
            from_id=planned["from"], to_id=planned["to"],
        ).consume()
        return

    if op == "set_rel_properties":
        rid_internal = (planned.get("before") or {}).get("rel_internal_id")
        props = dict(record.get("properties") or {})
        if rid_internal is not None:
            session.run(
                "MATCH ()-[r]-() WHERE id(r) = $rid SET r += $props",
                rid=rid_internal, props=props,
            ).consume()
            return
        rt = rel_type_safe(planned["type"])
        session.run(
            f"MATCH (a {{id: $from_id}})-[r:`{rt}`]->(b {{id: $to_id}}) SET r += $props",
            from_id=planned["from"], to_id=planned["to"], props=props,
        ).consume()
        return

    if op == "remove_node_properties":
        keys = [prop_key_safe(k) for k in (planned.get("keys_removed") or [])]
        if not keys:
            return
        set_clauses = ", ".join(f"n.`{k}` = null" for k in keys)
        session.run(
            f"MATCH (n {{id: $id}}) SET {set_clauses}",
            id=record["id"],
        ).consume()
        return

    if op == "remove_rel_properties":
        keys = [prop_key_safe(k) for k in (planned.get("keys_removed") or [])]
        if not keys:
            return
        set_clauses = ", ".join(f"r.`{k}` = null" for k in keys)
        rid_internal = (planned.get("before") or {}).get("rel_internal_id")
        if rid_internal is not None:
            session.run(
                f"MATCH ()-[r]-() WHERE id(r) = $rid SET {set_clauses}",
                rid=rid_internal,
            ).consume()
            return
        rt = rel_type_safe(planned["type"])
        session.run(
            f"MATCH (a {{id: $from_id}})-[r:`{rt}`]->(b {{id: $to_id}}) SET {set_clauses}",
            from_id=planned["from"], to_id=planned["to"],
        ).consume()
        return

    if op == "rename_property":
        old_key = prop_key_safe(planned["from_key"])
        new_key = prop_key_safe(planned["to_key"])
        session.run(
            f"MATCH (n {{id: $id}}) SET n.`{new_key}` = n.`{old_key}`, n.`{old_key}` = null",
            id=record["id"],
        ).consume()
        return

    if op == "move_property":
        prop = prop_key_safe(record["property"])
        value = planned["value"]
        session.run(
            f"MATCH (a {{id: $from_id}}), (b {{id: $to_id}}) "
            f"SET b.`{prop}` = $value SET a.`{prop}` = null",
            from_id=record["from_id"], to_id=record["to_id"], value=value,
        ).consume()
        return

    if op == "replace_rel_type":
        old_t = rel_type_safe(record["old_type"])
        new_t = rel_type_safe(record["new_type"])
        before = planned.get("before") or {}
        props = json_safe(dict(before.get("properties") or {}))
        session.run(
            f"MATCH (a {{id: $from_id}}), (b {{id: $to_id}}) "
            f"MERGE (a)-[r2:`{new_t}`]->(b) SET r2 += $props",
            from_id=record["from"], to_id=record["to"], props=props,
        ).consume()
        session.run(
            f"MATCH (a {{id: $from_id}})-[r:`{old_t}`]->(b {{id: $to_id}}) DELETE r",
            from_id=record["from"], to_id=record["to"],
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
                row for row in planned if row["status"] in {
                    "unsupported", "invalid", "missing_node", "missing_endpoint",
                    "missing_rel", "rejected",
                }
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
    would_delete_nodes = status_counts.get("would_delete_node", 0)
    would_merge = status_counts.get("would_merge", 0)
    would_create_rel = status_counts.get("would_create_rel", 0)
    would_delete_rel = status_counts.get("would_delete_rel", 0)
    # would_replace_rel is +1/-1; net 0
    # merge rewires rels: planning records how many are inbound/outbound on source;
    # after MERGE many become noops on the target, so we cannot pre-compute exact
    # delta here. Best-effort: assume merge nets 0 rels (worst case parallels are deduped).
    counts_after_expected = {
        "nodes": counts_before["nodes"] + would_create - would_delete_nodes - would_merge,
        "relationships": counts_before["relationships"] + would_create_rel - would_delete_rel,
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
