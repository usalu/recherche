"""Audit live Neo4j properties for an extreme-minimum cleanup.

The script is read-only. It scans node and relationship property keys, classifies
each label/key or reltype/key pair into keep/drop/review buckets, and writes
CSV/Markdown artifacts for patch planning.

Usage:
  python _scripts/audit_neo4j_minimal_properties.py
  python _scripts/audit_neo4j_minimal_properties.py --out-dir _neo4j/review/minimal_property_audit_manual
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


VOCAB_LABELS = {
    "Akzeptanz",
    "Akteurrolle",
    "Akteurtyp",
    "Aufbereitungsverfahren",
    "BauaufgabeIntervention",
    "Bauobjektklasse",
    "Bauobjektrolle",
    "Bauproduktstatus",
    "Bausystem",
    "Bauweise",
    "Bauteilebene",
    "Bauteiltyp",
    "Beschaffungsweg",
    "Defekt",
    "Funktionswechsel",
    "Huerde",
    "HuerdeKategorie",
    "Layer",
    "Leistungsanforderung",
    "Logistik",
    "Marktmodell",
    "MatchingQualitaet",
    "Material",
    "Materialgruppe",
    "Methode",
    "Nutzung",
    "Prozessphase",
    "PruefungNachweis",
    "RechtlicheBedingung",
    "Ressourcenquelle",
    "Rueckbauverfahren",
    "Schadstoff",
    "Status",
    "Tragwerksprinzip",
    "Verbindungstechnik",
    "WiederverwendungsArt",
    "Wirtschaft",
    "Zertifizierungssystem",
    "ZustandsKlasse",
}

ENTITY_LABELS = {
    "Akteur",
    "Bauwerk",
    "Bauteilgruppe",
    "Dossier",
    "Land",
    "Materialdepot",
    "Programm",
    "Projekt",
    "Software",
    "Stadt",
    "Tool",
    "Wiederverwendungskette",
}

SOURCE_LABELS = {"Quelle", "ExternalLink", "ResearchDocument", "SectionRef"}
REVIEW_META_LABELS = {"DataIssue", "DossierEntityTarget", "DeprecatedType", "GraphVersion", "ReuseRule"}
FACT_LABELS = {"Kennwert", "LCAModule"}

ABSOLUTE_NODE_KEEP = {"id"}
HUMAN_NODE_KEEP = {"name"}
VOCAB_KEEP = {"scope_note"}
SOURCE_KEEP = {"url", "quelltyp", "title", "name", "name_full", "source_file"}
GEO_KEEP = {"country_iso2", "iso2", "iso3"}
GRAPH_VERSION_KEEP = {"tag", "created_at_utc", "node_count", "relationship_count"}
KENNWERT_KEEP = {"kennwert", "wert", "wert_text", "einheit", "bilanzgrenze", "method", "fact_index"}

GENERATED_PREFIXES = (
    "_",
    "raw_",
    "candidate_",
    "source_trace_",
    "url_probe_",
    "url_body_",
    "url_last_",
    "url_response_",
)
GENERATED_EXACT = {
    "actor_registry_loader_seen",
    "also_in_dossier",
    "also_in_edge",
    "also_in_node",
    "also_in_research",
    "created_at",
    "created_by",
    "detected_at",
    "extracted_at",
    "first_seen_in_dossier",
    "first_seen_in_research",
    "found_at",
    "found_by",
    "last_seen_by",
    "loader",
    "migration_origin",
    "ref_id",
    "ref_label",
    "ref_labels",
    "resolution_note",
    "source_trace_migrated_at",
    "text_content_loaded_at",
    "unfolding_origin",
}
PROVENANCE_EXACT = {
    "evidence_basis",
    "evidence_confidence",
    "evidence_origin",
    "evidence_quote",
    "evidence_source_id",
    "evidence_terms",
    "source",
    "source_detail",
    "source_file",
    "source_origin",
    "source_resolution_status",
    "source_scope",
    "source_status",
    "source_type",
    "source_url",
    "source_urls",
    "url",
    "urls",
}
DERIVABLE_EXACT = {
    "candidate_source_count",
    "usage_countries",
    "usage_project_count",
    "usage_project_ids",
}
DUPLICATES_RELATIONSHIP_EXACT = {
    "akteurtyp",
    "land",
    "primary_bauteiltyp_id",
    "primary_material_id",
    "reuse_status",
    "status",
}
LEGACY_EXACT = {
    "akteur_kontext_text",
    "classified_at",
    "dateiname",
    "filename",
    "not_yet_referenced_in_corpus",
    "scope",
    "stars_ignored",
    "titel",
    "topic",
}
REL_KEEP = {"id"}
REL_REVIEW_KEEP = {"confidence", "review_status", "source", "source_detail", "source_type"}


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
        inner = ",".join(sorted({value_type(v) for v in value}))
        return f"list[{inner}]"
    return type(value).__name__


def short_value(value: Any, limit: int = 220) -> str:
    text = value if isinstance(value, str) else stable_json(value)
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
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_minimal_property_audit_%H%M%SZ")
    safe_db = re.sub(r"[^A-Za-z0-9_.-]+", "_", database or "neo4j")
    return repo_root() / "_neo4j" / "review" / f"{stamp}_{safe_db}"


def first_label_bucket(labels: list[str]) -> str:
    label_set = set(labels)
    if label_set & SOURCE_LABELS:
        return "source"
    if label_set & FACT_LABELS:
        return "fact"
    if label_set & REVIEW_META_LABELS:
        return "review_meta"
    if label_set & ENTITY_LABELS:
        return "entity"
    if label_set & VOCAB_LABELS:
        return "vocab"
    return "other"


def is_generated_key(key: str) -> bool:
    lower = key.lower()
    return key in GENERATED_EXACT or lower.startswith(GENERATED_PREFIXES) or lower.endswith("_at")


def classify_node_property(label: str, key: str, label_count: int, present: int) -> tuple[str, str, str]:
    """Return action, priority, reason."""
    bucket = first_label_bucket([label])
    lower = key.lower()
    coverage = present / label_count if label_count else 0

    if key in ABSOLUTE_NODE_KEEP:
        return "keep_minimum", "P0", "identity handle required by constraints and patch tooling"
    if key in HUMAN_NODE_KEEP:
        return "keep_minimum", "P0", "human caption / browser display"
    if label in VOCAB_LABELS and key in VOCAB_KEEP:
        return "keep_minimum", "P1", "controlled vocabulary definition"
    if label == "Land" and key in GEO_KEEP:
        return "keep_minimum", "P1", "stable external geography code"
    if label == "GraphVersion" and key in GRAPH_VERSION_KEEP:
        return "keep_minimum", "P1", "graph release metadata"
    if label == "Kennwert" and key in KENNWERT_KEEP:
        return "keep_or_model_fact", "P1", "literal quantitative fact; keep unless moved to relation model"
    if bucket == "source" and key in SOURCE_KEEP:
        return "keep_minimum", "P1", "minimum source identity / retrieval locator"

    if label in REVIEW_META_LABELS and label != "GraphVersion":
        if key in {"description", "severity", "status", "kind", "message", "subject_id", "subject_label", "rel_type", "start_id", "end_id", "rel_element_id"}:
            return "drop_or_archive_meta_node", "P0", "review/debug graph object; archive or compact before semantic cleanup"

    if key in LEGACY_EXACT:
        return "drop_candidate", "P0", "known legacy/intake key from older cleanup plans"
    if key in DERIVABLE_EXACT:
        return "drop_candidate", "P0", "derivable by query; should not live as stored property"
    if key in DUPLICATES_RELATIONSHIP_EXACT or lower.endswith("_id") or lower.endswith("_ids"):
        return "review_relationship_duplicate", "P0", "likely duplicates graph topology; replace with relationships or aliases only if needed"
    if is_generated_key(key):
        return "drop_candidate", "P1", "generated/import/cache/debug metadata"
    if key in PROVENANCE_EXACT or "evidence" in lower or "source" in lower or "url" in lower:
        if bucket == "source" and key in {"url", "source_file"}:
            return "keep_minimum", "P1", "source locator"
        return "move_to_provenance_model", "P1", "provenance should be on Quelle/BELEGT_IN/relationship provenance, not semantic node bag"
    if coverage < 0.05 and key not in {"name_full", "aliases", "note"}:
        return "review_sparse", "P2", "sparse property; verify it is not one-off import residue"
    if key == "name_full":
        return "review_keep_if_distinct", "P2", "keep only when materially different from name"
    if key in {"aliases", "note"}:
        return "review_keep_if_used", "P2", "human curation aid; keep only if actively queried"
    return "review_domain_property", "P3", "domain-specific value; decide per label"


def classify_rel_property(rel_type: str, key: str, rel_count: int, present: int) -> tuple[str, str, str]:
    lower = key.lower()
    coverage = present / rel_count if rel_count else 0
    if key in REL_KEEP:
        return "keep_minimum", "P0", "relationship identity handle required by current constraints"
    if key in REL_REVIEW_KEEP:
        return "review_keep_or_provenance", "P1", "may be real edge evidence/status; keep only if queried"
    if key in LEGACY_EXACT or key in DERIVABLE_EXACT:
        return "drop_candidate", "P0", "legacy or query-derivable relationship metadata"
    if is_generated_key(key):
        return "drop_candidate", "P1", "generated/import/cache/debug metadata"
    if "evidence" in lower or "source" in lower or "url" in lower:
        return "review_keep_or_source_edge", "P1", "edge provenance can be valid, but normalize to source_type/source_detail or BELEGT_IN"
    if lower.endswith("_id") or lower.endswith("_ids"):
        return "review_duplicate_id", "P2", "likely duplicates endpoint identity"
    if coverage < 0.05:
        return "review_sparse", "P2", "sparse relationship property"
    return "review_domain_property", "P3", "domain-specific edge value"


def summarize_values(rows: list[dict[str, Any]], entity_key: str, type_key: str) -> tuple[list[dict[str, Any]], Counter[str]]:
    counts: Counter[str] = Counter()
    types: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    samples: dict[tuple[str, str], list[str]] = defaultdict(list)
    empty_count: Counter[tuple[str, str]] = Counter()
    unique_cap: dict[tuple[str, str], set[str]] = defaultdict(set)

    for row in rows:
        group = row[type_key]
        props = row["properties"]
        counts[group] += 1
        for key, value in props.items():
            pair = (group, key)
            types[pair][value_type(value)] += 1
            if value in ("", []):
                empty_count[pair] += 1
            if len(unique_cap[pair]) < 1001:
                unique_cap[pair].add(stable_json(value))
            sample = short_value(value)
            if sample and sample not in samples[pair] and len(samples[pair]) < 4:
                samples[pair].append(sample)

    summary = []
    for (group, key), type_counter in sorted(types.items()):
        present = sum(type_counter.values())
        total = counts[group]
        if entity_key == "node":
            action, priority, reason = classify_node_property(group, key, total, present)
        else:
            action, priority, reason = classify_rel_property(group, key, total, present)
        type_string = "; ".join(f"{k}:{v}" for k, v in sorted(type_counter.items()))
        drift = len(type_counter) > 1
        summary.append(
            {
                "entity": entity_key,
                "group": group,
                "property": key,
                "total_in_group": total,
                "nodes_or_rels_with_property": present,
                "coverage_pct": round((present / total) * 100, 2) if total else 0,
                "missing_count": total - present,
                "types": type_string,
                "type_drift": "yes" if drift else "",
                "empty_count": empty_count[(group, key)],
                "unique_values_seen_cap_1001": len(unique_cap[(group, key)]),
                "action": action,
                "priority": priority,
                "reason": reason,
                "sample_values": " || ".join(samples[(group, key)]),
            }
        )
    return summary, counts


def action_totals(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    totals: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in summary:
        key = (row["entity"], row["action"], row["priority"])
        target = totals.setdefault(
            key,
            {
                "entity": row["entity"],
                "action": row["action"],
                "priority": row["priority"],
                "pairs": 0,
                "property_occurrences": 0,
            },
        )
        target["pairs"] += 1
        target["property_occurrences"] += int(row["nodes_or_rels_with_property"])
    return sorted(totals.values(), key=lambda r: (r["priority"], r["entity"], r["action"]))


def scan(out_dir: Path) -> dict[str, Any]:
    try:
        from neo4j import GraphDatabase
    except ImportError as exc:
        raise SystemExit("Install: pip install -r requirements-neo4j.txt") from exc

    uri, user, password, database = resolve_connection()
    if not uri or not user or not password:
        raise SystemExit("Missing Neo4j connection settings.")

    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=False)
    node_summary_path = out_dir / "node_property_minimization.csv"
    rel_summary_path = out_dir / "relationship_property_minimization.csv"
    action_totals_path = out_dir / "action_totals.csv"
    patch_ready_path = out_dir / "patch_ready_drop_candidates.csv"
    semantic_minimum_path = out_dir / "semantic_minimum_proposal.md"
    report_path = out_dir / "REPORT.md"
    manifest_path = out_dir / "manifest.json"

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database, default_access_mode="READ") as session:
            counts_record = session.run(
                "MATCH (n) WITH count(n) AS nodes "
                "MATCH ()-[r]->() RETURN nodes, count(r) AS relationships"
            ).single()
            graph_counts = {
                "nodes": counts_record["nodes"],
                "relationships": counts_record["relationships"],
            }
            node_rows = [
                {
                    "element_id": record["element_id"],
                    "labels": record["labels"],
                    "label": record["label"],
                    "properties": json_safe(record["properties"]),
                }
                for record in session.run(
                    "MATCH (n) "
                    "WITH n, labels(n) AS labels "
                    "UNWIND labels AS label "
                    "RETURN elementId(n) AS element_id, labels, label, properties(n) AS properties "
                    "ORDER BY label, elementId(n)"
                )
            ]
            rel_rows = [
                {
                    "element_id": record["element_id"],
                    "type": record["type"],
                    "properties": json_safe(record["properties"]),
                }
                for record in session.run(
                    "MATCH ()-[r]->() "
                    "RETURN elementId(r) AS element_id, type(r) AS type, properties(r) AS properties "
                    "ORDER BY type, elementId(r)"
                )
            ]
    finally:
        driver.close()

    node_summary, node_label_counts = summarize_values(node_rows, "node", "label")
    rel_summary, rel_type_counts = summarize_values(rel_rows, "relationship", "type")
    totals = action_totals(node_summary + rel_summary)

    patch_ready = [
        row
        for row in node_summary + rel_summary
        if row["action"] == "drop_candidate" and row["priority"] in {"P0", "P1"}
    ]
    patch_ready.sort(
        key=lambda r: (
            r["priority"],
            r["entity"],
            -int(r["nodes_or_rels_with_property"]),
            r["group"],
            r["property"],
        )
    )

    fields = [
        "entity",
        "group",
        "property",
        "total_in_group",
        "nodes_or_rels_with_property",
        "coverage_pct",
        "missing_count",
        "types",
        "type_drift",
        "empty_count",
        "unique_values_seen_cap_1001",
        "action",
        "priority",
        "reason",
        "sample_values",
    ]
    csv_write(node_summary_path, node_summary, fields)
    csv_write(rel_summary_path, rel_summary, fields)
    csv_write(action_totals_path, totals, ["entity", "action", "priority", "pairs", "property_occurrences"])
    csv_write(patch_ready_path, patch_ready, fields)

    node_action_counts = Counter(row["action"] for row in node_summary)
    rel_action_counts = Counter(row["action"] for row in rel_summary)
    top_drop = patch_ready[:40]
    type_drift = [row for row in node_summary + rel_summary if row["type_drift"]]
    meta_node_counts = {label: node_label_counts[label] for label in sorted(REVIEW_META_LABELS) if node_label_counts[label]}

    proposal_lines = [
        "# Semantic minimum property proposal",
        "",
        f"**Created UTC:** {datetime.now(timezone.utc).isoformat()}",
        f"**Database:** `{database}`",
        f"**Graph counts:** {graph_counts['nodes']} nodes / {graph_counts['relationships']} relationships",
        "",
        "## Minimum rule set",
        "",
        "| Object | Minimum properties | Notes |",
        "|---|---|---|",
        "| All semantic nodes | `id`, `name` | `name_full`, `aliases`, `note` only when actively useful. |",
        "| Controlled vocabulary nodes | `id`, `name`, `scope_note` | Drop import/debug fields; keep definitions. |",
        "| `Quelle` / source nodes | `id`, `name`, `url`, `quelltyp`, maybe `source_file` | Probe/cache state should be external or normalized, not spread across node bags. |",
        "| `Kennwert` facts | `id`, `kennwert`, `wert`/`wert_text`, `einheit`, `method`, `bilanzgrenze` | Keep only if the graph keeps fact nodes; otherwise model as relationships. |",
        "| Relationships | `id` plus normalized provenance only where needed | Edge provenance should be consistent, not arbitrary evidence/cache fields. |",
        "| Review/meta nodes | none in semantic graph | Archive/compact `DataIssue` and similar nodes unless they are part of active QA workflow. |",
        "",
        "## Patch-ready drop candidates",
        "",
        "These are classification candidates only. Review samples before generating a patch.",
        "",
        "| Priority | Entity | Group | Property | Occurrences | Reason |",
        "|---|---|---|---|---:|---|",
    ]
    proposal_lines.extend(
        f"| {row['priority']} | {row['entity']} | `{row['group']}` | `{row['property']}` | "
        f"{row['nodes_or_rels_with_property']} | {row['reason']} |"
        for row in top_drop
    )
    proposal_lines.extend(
        [
            "",
            "## Do not blindly delete",
            "",
            "- `source_scope` is messy but provenance-critical; normalize before removing.",
            "- `evidence_*` may be wrong on semantic nodes but still needs migration into a source/edge model if it is the only provenance.",
            "- `primary_material_id`, `primary_bauteiltyp_id`, `reuse_status`, `land`, and similar fields likely duplicate relationships; confirm relationship coverage first.",
            "- `DataIssue` volume should be handled as a graph-model decision, not a property-only cleanup.",
            "",
            "## Type drift pairs",
            "",
            "| Entity | Group | Property | Types | Action |",
            "|---|---|---|---|---|",
        ]
    )
    proposal_lines.extend(
        f"| {row['entity']} | `{row['group']}` | `{row['property']}` | {row['types']} | {row['action']} |"
        for row in sorted(type_drift, key=lambda r: (r["entity"], r["group"], r["property"]))
    )
    semantic_minimum_path.write_text("\n".join(proposal_lines) + "\n", encoding="utf-8")

    report_lines = [
        "# Minimal property audit",
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
        "| `node_property_minimization.csv` | Every label/property pair classified for minimum retention. |",
        "| `relationship_property_minimization.csv` | Every reltype/property pair classified for minimum retention. |",
        "| `action_totals.csv` | Counts by action bucket and priority. |",
        "| `patch_ready_drop_candidates.csv` | P0/P1 drop candidates only. |",
        "| `semantic_minimum_proposal.md` | Human-readable minimum schema proposal. |",
        "",
        "## Action totals",
        "",
        "| Entity | Action | Priority | Pairs | Occurrences |",
        "|---|---|---|---:|---:|",
    ]
    report_lines.extend(
        f"| {row['entity']} | `{row['action']}` | {row['priority']} | {row['pairs']} | {row['property_occurrences']} |"
        for row in totals
    )
    report_lines.extend(
        [
            "",
            "## Review/meta node counts",
            "",
            "| Label | Nodes |",
            "|---|---:|",
        ]
    )
    report_lines.extend(f"| `{label}` | {count} |" for label, count in meta_node_counts.items())
    report_lines.extend(
        [
            "",
            "## Node action bucket counts",
            "",
            "| Action | Label/property pairs |",
            "|---|---:|",
        ]
    )
    report_lines.extend(f"| `{action}` | {count} |" for action, count in sorted(node_action_counts.items()))
    report_lines.extend(
        [
            "",
            "## Relationship action bucket counts",
            "",
            "| Action | Reltype/property pairs |",
            "|---|---:|",
        ]
    )
    report_lines.extend(f"| `{action}` | {count} |" for action, count in sorted(rel_action_counts.items()))
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    files = [
        node_summary_path,
        rel_summary_path,
        action_totals_path,
        patch_ready_path,
        semantic_minimum_path,
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
            "node_label_property_pairs": len(node_summary),
            "relationship_type_property_pairs": len(rel_summary),
            "patch_ready_drop_pairs": len(patch_ready),
            "patch_ready_drop_occurrences": sum(int(row["nodes_or_rels_with_property"]) for row in patch_ready),
            "type_drift_pairs": len(type_drift),
            "review_meta_node_counts": meta_node_counts,
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
