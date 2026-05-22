"""Phase 0 encoding normalization for mit-bestand.

Dry-run by default. The script fixes deterministic UTF-8-as-Latin-1 mojibake
patterns in string properties and reports unrecoverable U+FFFD replacement
characters separately. It intentionally does not guess text that has already
lost bytes to U+FFFD.

Usage:
  python phase0_fix_encoding.py
  python phase0_fix_encoding.py --commit
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Iterable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from neo4j import GraphDatabase

REPO = Path(__file__).resolve().parents[4]
if str(REPO / "_scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "_scripts"))

from neo4j_env import resolve_connection  # noqa: E402

OUT = Path(__file__).resolve().parent
REPORT_PATH = OUT / "phase0_encoding_report.json"

MOJIBAKE_MARKERS = ("Ã", "Â", "â", "ð", "Ð")
REPLACEMENT = "\uFFFD"


def maybe_fix_mojibake(value: str) -> str:
    """Repair common mojibake only when a round-trip improves the string."""
    if not any(marker in value for marker in MOJIBAKE_MARKERS):
        return value
    try:
        repaired = value.encode("latin-1").decode("utf-8")
    except UnicodeError:
        return value
    if repaired != value and REPLACEMENT not in repaired:
        return repaired
    return value


def normalize_value(value: Any) -> tuple[Any, bool, bool]:
    """Return (new_value, changed, contains_unrecoverable_replacement)."""
    if isinstance(value, str):
        fixed = maybe_fix_mojibake(value)
        return fixed, fixed != value, REPLACEMENT in fixed
    if isinstance(value, list):
        changed = False
        unresolved = False
        new_items: list[Any] = []
        for item in value:
            new_item, item_changed, item_unresolved = normalize_value(item)
            new_items.append(new_item)
            changed = changed or item_changed
            unresolved = unresolved or item_unresolved
        return new_items, changed, unresolved
    return value, False, False


def prop_updates(props: dict[str, Any]) -> tuple[dict[str, Any], dict[str, list[str]]]:
    updates: dict[str, Any] = {}
    unresolved: dict[str, list[str]] = {}
    for key, value in props.items():
        new_value, changed, has_unresolved = normalize_value(value)
        if changed:
            updates[key] = new_value
        if has_unresolved:
            unresolved.setdefault(key, []).append(str(value)[:240])
    return updates, unresolved


def summarize_unresolved(unresolved_rows: Iterable[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in unresolved_rows:
        for key in row.get("keys", []):
            counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def run(commit: bool) -> dict[str, Any]:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    now = datetime.now(timezone.utc).isoformat()
    report: dict[str, Any] = {
        "phase": "phase0_fix_encoding",
        "database": database,
        "commit": commit,
        "created_at_utc": now,
        "node_updates": 0,
        "relationship_updates": 0,
        "property_updates": 0,
        "unresolved_replacement_nodes": 0,
        "unresolved_replacement_relationships": 0,
        "unresolved_property_counts": {},
        "examples": [],
    }

    with driver.session(database=database) as session:
        node_rows = session.run(
            "MATCH (n) RETURN elementId(n) AS eid, labels(n) AS labels, properties(n) AS props"
        )
        for record in node_rows:
            updates, unresolved = prop_updates(dict(record["props"]))
            if updates:
                report["node_updates"] += 1
                report["property_updates"] += len(updates)
                if commit:
                    session.run(
                        "MATCH (n) WHERE elementId(n) = $eid SET n += $updates",
                        eid=record["eid"],
                        updates=updates,
                    ).consume()
            if unresolved:
                report["unresolved_replacement_nodes"] += 1
                if len(report["examples"]) < 25:
                    report["examples"].append(
                        {
                            "kind": "node",
                            "element_id": record["eid"],
                            "labels": list(record["labels"]),
                            "keys": sorted(unresolved),
                            "values": unresolved,
                        }
                    )

        rel_rows = session.run(
            "MATCH ()-[r]->() RETURN elementId(r) AS eid, type(r) AS type, properties(r) AS props"
        )
        for record in rel_rows:
            updates, unresolved = prop_updates(dict(record["props"]))
            if updates:
                report["relationship_updates"] += 1
                report["property_updates"] += len(updates)
                if commit:
                    session.run(
                        "MATCH ()-[r]->() WHERE elementId(r) = $eid SET r += $updates",
                        eid=record["eid"],
                        updates=updates,
                    ).consume()
            if unresolved:
                report["unresolved_replacement_relationships"] += 1
                if len(report["examples"]) < 25:
                    report["examples"].append(
                        {
                            "kind": "relationship",
                            "element_id": record["eid"],
                            "type": record["type"],
                            "keys": sorted(unresolved),
                            "values": unresolved,
                        }
                    )

    unresolved_counts: dict[str, int] = {}
    for example in report["examples"]:
        for key in example["keys"]:
            unresolved_counts[key] = unresolved_counts.get(key, 0) + 1
    report["unresolved_property_counts_from_examples"] = unresolved_counts

    REPORT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    driver.close()
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", action="store_true", help="Write deterministic repairs.")
    args = parser.parse_args()
    report = run(args.commit)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    if report["unresolved_replacement_nodes"] or report["unresolved_replacement_relationships"]:
        print(
            "\nWARNING: U+FFFD replacement characters remain. Bytes are already lost; "
            "review phase0_encoding_report.json before deciding whether to manually edit or strip.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
