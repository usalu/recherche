"""Scan every live Neo4j node property for cleanup planning.

This is intentionally read-only. It exports the complete node property bags
plus compact inventories that make graph-wide cleanup reviewable before any
patch is generated.

Usage:
  python _scripts/scan_neo4j_node_properties.py
  python _scripts/scan_neo4j_node_properties.py --out-dir _neo4j/review/node_property_scan_manual
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import repo_root, resolve_connection  # noqa: E402


CORE_KEYS = {"id", "name", "name_full", "aliases", "note", "scope_note", "source_scope", "source_file"}
KNOWN_LEGACY_KEYS = {
    "akteur_kontext_text",
    "classified_at",
    "dateiname",
    "filename",
    "not_yet_referenced_in_corpus",
    "scope",
    "stars_ignored",
    "titel",
    "topic",
    "usage_countries",
    "usage_project_count",
    "usage_project_ids",
}
PROVENANCE_HINT_KEYS = {
    "source",
    "source_file",
    "source_scope",
    "url",
    "urls",
    "url_status",
    "quelltyp",
    "evidence",
    "evidence_urls",
    "evidence_quote",
}
CASE_SPECIFIC_LABELS = {
    "Akteur",
    "Bauwerk",
    "Bauteilgruppe",
    "Materialdepot",
    "Programm",
    "Projekt",
    "Quelle",
    "Software",
    "Tool",
    "Wiederverwendungskette",
}


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


def stable_json(value: Any) -> str:
    return json.dumps(json_safe(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def value_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    if isinstance(value, list):
        inner = sorted({value_type(v) for v in value})
        return "list[" + ",".join(inner) + "]"
    return type(value).__name__


def text_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list) and all(isinstance(v, str) for v in value):
        return " | ".join(value)
    return ""


def short_value(value: Any, limit: int = 220) -> str:
    text = stable_json(value) if not isinstance(value, str) else value
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(json_safe(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def csv_write(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def default_out_dir(database: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_node_property_scan_%H%M%SZ")
    safe_db = re.sub(r"[^A-Za-z0-9_.-]+", "_", database or "neo4j")
    return repo_root() / "_neo4j" / "review" / f"{stamp}_{safe_db}"


def issue(
    issues: list[dict[str, Any]],
    severity: str,
    category: str,
    row: dict[str, Any],
    detail: str,
    prop: str | None = None,
    value: Any = None,
) -> None:
    props = row["properties"]
    issues.append(
        {
            "severity": severity,
            "category": category,
            "element_id": row["element_id"],
            "labels": row["labels"],
            "node_id": props.get("id"),
            "node_name": props.get("name"),
            "property": prop,
            "detail": detail,
            "value_sample": short_value(value) if value is not None else "",
        }
    )


def classify_property_key(key: str) -> list[str]:
    flags: list[str] = []
    if key in CORE_KEYS:
        flags.append("core")
    if key in KNOWN_LEGACY_KEYS:
        flags.append("known_legacy_review")
    if key.lower() != key:
        flags.append("mixed_case_key")
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
        flags.append("non_standard_key")
    if "quelle" in key.lower() and key not in {"quelltyp"}:
        flags.append("quelle_as_property_review")
    if "source" in key.lower() or "url" in key.lower() or "evidence" in key.lower():
        flags.append("provenance_key")
    return flags


def is_provenance_like_key(key: str) -> bool:
    lower = key.lower()
    return key in PROVENANCE_HINT_KEYS or "source" in lower or "url" in lower or "evidence" in lower


def is_case_specific(labels: list[str]) -> bool:
    return any(label in CASE_SPECIFIC_LABELS for label in labels)


def scan(out_dir: Path) -> dict[str, Any]:
    try:
        from neo4j import GraphDatabase
    except ImportError as exc:
        raise SystemExit("Install: pip install -r requirements-neo4j.txt") from exc

    uri, user, password, database = resolve_connection()
    if not uri or not user or not password:
        raise SystemExit("Missing Neo4j connection settings.")

    out_dir.mkdir(parents=True, exist_ok=False)
    nodes_path = out_dir / "nodes_properties.jsonl"
    property_inventory_path = out_dir / "property_inventory.csv"
    property_key_summary_path = out_dir / "property_key_summary.csv"
    issues_path = out_dir / "node_property_issues.jsonl"
    issues_csv_path = out_dir / "node_property_issues.csv"
    label_summary_path = out_dir / "label_summary.csv"
    value_samples_path = out_dir / "value_samples.json"
    report_path = out_dir / "REPORT.md"
    manifest_path = out_dir / "manifest.json"

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database, default_access_mode="READ") as session:
            counts = session.run(
                "MATCH (n) WITH count(n) AS nodes "
                "MATCH ()-[r]->() RETURN nodes, count(r) AS relationships"
            ).single()
            graph_counts = {
                "nodes": counts["nodes"],
                "relationships": counts["relationships"],
            }
            rows = [
                json_safe(dict(record))
                for record in session.run(
                    "MATCH (n) "
                    "RETURN elementId(n) AS element_id, labels(n) AS labels, properties(n) AS properties "
                    "ORDER BY elementId(n)"
                )
            ]
    finally:
        driver.close()

    label_counts: Counter[str] = Counter()
    key_counts: Counter[str] = Counter()
    label_key_counts: Counter[tuple[str, str]] = Counter()
    label_key_types: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    label_key_empty_strings: Counter[tuple[str, str]] = Counter()
    label_key_blank_lists: Counter[tuple[str, str]] = Counter()
    label_key_unique: dict[tuple[str, str], set[str]] = defaultdict(set)
    label_key_samples: dict[tuple[str, str], list[Any]] = defaultdict(list)
    key_labels: dict[str, Counter[str]] = defaultdict(Counter)
    issues: list[dict[str, Any]] = []
    long_texts: list[dict[str, Any]] = []

    with nodes_path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            props = row["properties"]
            labels = row["labels"]
            for label in labels:
                label_counts[label] += 1

            enriched = {
                "element_id": row["element_id"],
                "labels": labels,
                "node_id": props.get("id"),
                "name": props.get("name"),
                "property_count": len(props),
                "property_keys": sorted(props),
                "properties": props,
            }
            f.write(json.dumps(enriched, ensure_ascii=False, sort_keys=True) + "\n")

            if props.get("id") in (None, ""):
                issue(issues, "high", "missing_id", row, "Node has no non-empty id property.")
            if props.get("name") in (None, ""):
                issue(issues, "medium", "missing_name", row, "Node has no non-empty name property.")
            if props.get("source_scope") in (None, ""):
                issue(
                    issues,
                    "medium",
                    "missing_source_scope",
                    row,
                    "Node has no source_scope property.",
                )
            if is_case_specific(labels) and props.get("source_scope") in (None, ""):
                issue(
                    issues,
                    "high",
                    "missing_source_scope_case_label",
                    row,
                    "Case-specific/source-bearing label has no source_scope property.",
                )

            for key, value in props.items():
                key_counts[key] += 1
                key_flags = classify_property_key(key)
                if "known_legacy_review" in key_flags:
                    issue(
                        issues,
                        "medium",
                        "known_legacy_property",
                        row,
                        "Property key is known from previous cleanup plans or legacy imports.",
                        key,
                        value,
                    )
                if "quelle_as_property_review" in key_flags:
                    issue(
                        issues,
                        "medium",
                        "possible_quelle_denormalization",
                        row,
                        "Quelle/source reference may belong on BELEGT_IN or relationship provenance, not node property bag.",
                        key,
                        value,
                    )

                txt = text_value(value)
                if txt:
                    if len(txt) > 500:
                        issue(
                            issues,
                            "low",
                            "long_text_property",
                            row,
                            f"Text/list property is {len(txt)} characters.",
                            key,
                            value,
                        )
                        long_texts.append(
                            {
                                "element_id": row["element_id"],
                                "labels": labels,
                                "node_id": props.get("id"),
                                "property": key,
                                "length": len(txt),
                                "sample": short_value(txt, 500),
                            }
                        )
                    if not is_provenance_like_key(key) and re.search(r"https?://|www\.", txt, flags=re.I):
                        issue(
                            issues,
                            "medium",
                            "url_in_non_url_property",
                            row,
                            "URL-like text appears in a non-URL/provenance property.",
                            key,
                            value,
                        )
                    if re.search(r"(^|[\\/])(_archive|research|_database)([\\/]|$)", txt, flags=re.I):
                        issue(
                            issues,
                            "high",
                            "legacy_path_reference",
                            row,
                            "Property references retired/legacy file structures; verify before reuse.",
                            key,
                            value,
                        )
                    if txt.strip() == "":
                        issue(
                            issues,
                            "low",
                            "blank_string_property",
                            row,
                            "Property is a blank string.",
                            key,
                            value,
                        )

                if isinstance(value, list) and len(value) == 0:
                    issue(issues, "low", "blank_list_property", row, "Property is an empty list.", key, value)

                for label in labels:
                    lk = (label, key)
                    label_key_counts[lk] += 1
                    label_key_types[lk][value_type(value)] += 1
                    key_labels[key][label] += 1
                    if value == "":
                        label_key_empty_strings[lk] += 1
                    if value == []:
                        label_key_blank_lists[lk] += 1
                    if len(label_key_unique[lk]) < 1001:
                        label_key_unique[lk].add(stable_json(value))
                    samples = label_key_samples[lk]
                    sample_text = short_value(value)
                    if sample_text and sample_text not in samples and len(samples) < 5:
                        samples.append(sample_text)

    inventory_rows: list[dict[str, Any]] = []
    for (label, key), present in sorted(label_key_counts.items()):
        total = label_counts[label]
        type_counts = label_key_types[(label, key)]
        flags = classify_property_key(key)
        if len(type_counts) > 1:
            flags.append("type_drift")
        inventory_rows.append(
            {
                "label": label,
                "property": key,
                "nodes_with_property": present,
                "label_node_count": total,
                "coverage_pct": round((present / total) * 100, 2) if total else 0,
                "missing_count": total - present,
                "types": "; ".join(f"{k}:{v}" for k, v in sorted(type_counts.items())),
                "unique_values_seen_cap_1001": len(label_key_unique[(label, key)]),
                "empty_string_count": label_key_empty_strings[(label, key)],
                "empty_list_count": label_key_blank_lists[(label, key)],
                "flags": "; ".join(flags),
                "sample_values": " || ".join(label_key_samples[(label, key)]),
            }
        )

    key_summary_rows = []
    for key, count in sorted(key_counts.items(), key=lambda item: (-item[1], item[0])):
        flags = classify_property_key(key)
        key_summary_rows.append(
            {
                "property": key,
                "nodes_with_property": count,
                "label_count": len(key_labels[key]),
                "labels": "; ".join(f"{label}:{n}" for label, n in sorted(key_labels[key].items())),
                "flags": "; ".join(flags),
            }
        )

    label_rows = []
    for label, count in sorted(label_counts.items()):
        label_keys = sorted(key for (lk_label, key), _ in label_key_counts.items() if lk_label == label)
        label_rows.append(
            {
                "label": label,
                "node_count": count,
                "distinct_property_keys": len(label_keys),
                "property_keys": "; ".join(label_keys),
            }
        )

    for (label, key), types in sorted(label_key_types.items()):
        if len(types) > 1:
            issue(
                issues,
                "medium",
                "property_type_drift",
                {"element_id": "", "labels": [label], "properties": {}},
                f"{label}.{key} has multiple value types: "
                + ", ".join(f"{k}:{v}" for k, v in sorted(types.items())),
                key,
            )

    with issues_path.open("w", encoding="utf-8", newline="\n") as f:
        for row in issues:
            f.write(json.dumps(json_safe(row), ensure_ascii=False, sort_keys=True) + "\n")

    csv_write(
        property_inventory_path,
        inventory_rows,
        [
            "label",
            "property",
            "nodes_with_property",
            "label_node_count",
            "coverage_pct",
            "missing_count",
            "types",
            "unique_values_seen_cap_1001",
            "empty_string_count",
            "empty_list_count",
            "flags",
            "sample_values",
        ],
    )
    csv_write(
        property_key_summary_path,
        key_summary_rows,
        ["property", "nodes_with_property", "label_count", "labels", "flags"],
    )
    csv_write(label_summary_path, label_rows, ["label", "node_count", "distinct_property_keys", "property_keys"])
    csv_write(
        issues_csv_path,
        issues,
        [
            "severity",
            "category",
            "element_id",
            "labels",
            "node_id",
            "node_name",
            "property",
            "detail",
            "value_sample",
        ],
    )

    issue_counts = Counter(row["category"] for row in issues)
    issue_severity_counts = Counter(row["severity"] for row in issues)
    flagged_inventory = [row for row in inventory_rows if row["flags"]]
    type_drift = [row for row in inventory_rows if "type_drift" in row["flags"]]
    legacy_inventory = [row for row in inventory_rows if "known_legacy_review" in row["flags"]]
    missing_core = {
        "missing_id": issue_counts["missing_id"],
        "missing_name": issue_counts["missing_name"],
        "missing_source_scope": issue_counts["missing_source_scope"],
        "missing_source_scope_case_label": issue_counts["missing_source_scope_case_label"],
    }
    top_issue_rows = sorted(
        issue_counts.items(),
        key=lambda item: (-item[1], item[0]),
    )[:20]
    top_keys = key_summary_rows[:25]
    largest_labels = sorted(label_rows, key=lambda row: (-int(row["node_count"]), row["label"]))[:25]

    value_samples = {
        "long_text_properties_top_100": sorted(long_texts, key=lambda row: -row["length"])[:100],
        "type_drift": type_drift,
        "legacy_properties": legacy_inventory,
    }
    write_json(value_samples_path, value_samples)

    report_lines = [
        "# Node property scan",
        "",
        f"**Created UTC:** {datetime.now(timezone.utc).isoformat()}",
        f"**Database:** `{database}`",
        f"**Connection:** `{uri}` as `{user}`",
        f"**Graph counts:** {graph_counts['nodes']} nodes / {graph_counts['relationships']} relationships",
        "",
        "## Outputs",
        "",
        "| File | Purpose |",
        "|---|---|",
        "| `nodes_properties.jsonl` | Every node with labels, id/name, property keys, and full property bag. |",
        "| `property_inventory.csv` | Per-label property coverage, types, samples, and flags. |",
        "| `property_key_summary.csv` | Graph-wide property-key frequency and label distribution. |",
        "| `node_property_issues.jsonl` / `.csv` | Review queue for cleanup candidates. |",
        "| `label_summary.csv` | Labels, node counts, and property-key sets. |",
        "| `value_samples.json` | Long text, type drift, and known legacy key slices. |",
        "",
        "## Headline counts",
        "",
        f"- Labels: {len(label_counts)}",
        f"- Distinct node property keys: {len(key_counts)}",
        f"- Label/property pairs: {len(inventory_rows)}",
        f"- Issue rows: {len(issues)}",
        f"- Missing `id`: {missing_core['missing_id']}",
        f"- Missing `name`: {missing_core['missing_name']}",
        f"- Missing `source_scope` on any label: {missing_core['missing_source_scope']}",
        f"- Missing `source_scope` on case/source-bearing labels: {missing_core['missing_source_scope_case_label']}",
        f"- Label/property type drift pairs: {len(type_drift)}",
        f"- Known legacy label/property pairs: {len(legacy_inventory)}",
        "",
        "## Issue categories",
        "",
        "| Category | Count |",
        "|---|---:|",
    ]
    report_lines.extend(f"| `{category}` | {count} |" for category, count in top_issue_rows)
    report_lines.extend(
        [
            "",
            "## Severity",
            "",
            "| Severity | Count |",
            "|---|---:|",
        ]
    )
    report_lines.extend(f"| `{severity}` | {count} |" for severity, count in sorted(issue_severity_counts.items()))
    report_lines.extend(
        [
            "",
            "## Largest labels",
            "",
            "| Label | Nodes | Distinct props |",
            "|---|---:|---:|",
        ]
    )
    report_lines.extend(
        f"| `{row['label']}` | {row['node_count']} | {row['distinct_property_keys']} |"
        for row in largest_labels
    )
    report_lines.extend(
        [
            "",
            "## Most common property keys",
            "",
            "| Property | Nodes | Labels | Flags |",
            "|---|---:|---:|---|",
        ]
    )
    report_lines.extend(
        f"| `{row['property']}` | {row['nodes_with_property']} | {row['label_count']} | {row['flags']} |"
        for row in top_keys
    )
    report_lines.extend(
        [
            "",
            "## Read this before cleanup",
            "",
            "- This scan is read-only and does not decide semantic merges.",
            "- `known_legacy_review` means the key has appeared in old cleanup plans or legacy imports; inspect value samples before removal.",
            "- `possible_quelle_denormalization` is a review cue only. Actual provenance should remain traceable through `Quelle`, `BELEGT_IN`, and relationship provenance.",
            "- Any patch should be generated separately, dry-run with `_scripts/apply_neo4j_review_patch.py`, backed up first, and reviewed by label/key slice.",
            "",
        ]
    )
    report_path.write_text("\n".join(report_lines), encoding="utf-8")

    files = [
        nodes_path,
        property_inventory_path,
        property_key_summary_path,
        issues_path,
        issues_csv_path,
        label_summary_path,
        value_samples_path,
        report_path,
    ]
    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "database": database,
        "connection": {"uri": uri, "user": user},
        "counts": graph_counts,
        "outputs": {path.name: str(path.relative_to(repo_root())) for path in files},
        "checksums_sha256": {path.name: sha256_file(path) for path in files},
        "headline": {
            "labels": len(label_counts),
            "distinct_node_property_keys": len(key_counts),
            "label_property_pairs": len(inventory_rows),
            "issue_rows": len(issues),
            "missing_core": missing_core,
            "type_drift_pairs": len(type_drift),
            "known_legacy_pairs": len(legacy_inventory),
        },
    }
    write_json(manifest_path, manifest)
    return {"out_dir": str(out_dir), **manifest["headline"], "counts": graph_counts}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    _, _, _, database = resolve_connection()
    out_dir = args.out_dir or default_out_dir(database)
    result = scan(out_dir)
    print(json.dumps(json_safe(result), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
