"""Post-migration property cleanup for mit-bestand (Phases 0–6, 8, 4b, 5b, 9).

Dry-run by default. Commit mode writes phase reports and applies graph updates.

Usage:
  python property_cleanup_apply.py --phase 0
  python property_cleanup_apply.py --phase 1 --commit
  python property_cleanup_apply.py --through 8 --commit
  python property_cleanup_apply.py --through 9 --commit
  python property_cleanup_apply.py --phase 4b --commit
"""

from __future__ import annotations

import argparse
import csv
import fnmatch
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from neo4j import GraphDatabase

REPO = Path(__file__).resolve().parents[3]
if str(REPO / "_scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "_scripts"))

from neo4j_env import resolve_connection  # noqa: E402

OUT = Path(__file__).resolve().parent
ARCHIVE = OUT / "archive"
SIDECAR = OUT / "sidecar"
ENTITY_METADATA = SIDECAR / "entity_metadata.jsonl"
DROP_LIST = OUT / "source_title_drop_patterns.txt"
RUN = "property_cleanup_2026_06_05"
RUN_4B = f"{RUN}_phase4b"
RUN_5B = f"{RUN}_phase5b"
NOW = datetime.now(timezone.utc).isoformat()

PHASE4B_REL_KEYS = ["review_status", "evidence_status", "review_run"]

REGULATION_BASELINE = {
    "triggers": 1100,
    "erfordert": 1483,
    "gestuetzt_auf_regelwerk": 167,
    "gilt_in_land": 281,
}

PHASE1_NODE_KEYS = [
    "phase3_legacy_property_migration",
    "phase3_updated_at_utc",
    "phase6_property_migration",
    "phase6_updated_at_utc",
    "phase7_property_migration",
    "phase7_updated_at_utc",
    "phase8_property_migration",
    "phase8_updated_at_utc",
    "phaseB_property_migration",
    "phaseB_updated_at_utc",
    "renamed_at",
    "renamed_in_run",
    "legacy_id",
    "review_run",
]

PHASE2_NF_KEYS = [
    "legacy_rechtsgrundlagen_from_variant_a",
    "legacy_rechtsgrundlagen_urls_from_variant_a",
    "legacy_jurisdiktion_from_variant_a",
    "rechtsgrundlagen",
    "rechtsgrundlagen_urls",
    "jurisdiktion",
]

PHASE2_RF_KEYS = [
    "rechtsgrundlagen",
    "rechtsgrundlagen_urls",
    "jurisdiktion",
    "source_scope",
    "review_run",
    "updated_at_utc",
]

PHASE3_ARCHIVE_KEYS = [
    "legacy_internal_provenance_docs",
    "legacy_rechtsgrundlagen",
    "legacy_rechtsgrundlagen_urls",
    "legacy_jurisdiktion",
    "legacy_rechtliche_bedingungen",
    "legacy_marktmodell",
    "legacy_huerde_categories",
    "legacy_applicability_confidences",
    "legacy_applicability_rel_ids",
    "applies_in_land_ids",
    "applies_in_land_names",
    "applies_to_material_ids",
    "applies_to_material_names",
    "relevant_for_project_ids",
    "relevant_for_project_names",
    "lca_method_rechtsgrundlagen",
    "merged_legacy_leistungsanforderungen",
    "merged_legacy_pruefung_ids",
]

PHASE4_REL_KEYS = [
    "review_run",
    "updated_at_utc",
    "created_at",
    "created_at_utc",
    "batch_id",
    "enrichment_run",
    "migrated_at",
    "import_decision",
    "import_source_slice",
    "import_original_evidence_confidence",
    "import_source_file",
    "candidate_source_urls",
    "candidate_source_basis",
    "source_resolution_status",
    "source_status",
    "source_status_reason",
    "merged_legacy_rel_ids",
    "merged_legacy_reltypes",
    "legacy_rel_id",
    "legacy_methode_id",
    "legacy_methode_name",
    "legacy_aufbereitung_id",
    "legacy_aufbereitung_name",
    "legacy_ressourcenquelle_id",
    "legacy_ressourcenquelle_name",
    "legacy_internal_provenance_docs",
    "applicability_reason",
    "support_rules",
    "input_source",
    "original_source_excerpt",
    "via_bauteilgruppe_id",
    "semantic_basis",
    "evidence_basis",
    "evidence_url",
    "evidence_quote",
    "source_project_id",
    "source_project_name",
    "evidence_urls",
    "source_chain_id",
    "case_evidence_snippets",
]

PHASE5_NODE_DROP_KEYS = ["source_scope", "evidence_status", "evidence_basis", "primary_source_url"]

PHASE6_REUSERULE_KEEP = {"id", "name"}


def graph_stats(session) -> dict[str, Any]:
    nodes = session.run("MATCH (n) RETURN count(n) AS c").single()["c"]
    rels = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
    node_keys = session.run(
        "MATCH (n) UNWIND keys(n) AS k RETURN count(DISTINCT k) AS c"
    ).single()["c"]
    rel_keys = session.run(
        "MATCH ()-[r]->() UNWIND keys(r) AS k RETURN count(DISTINCT k) AS c"
    ).single()["c"]
    node_occ = session.run(
        "MATCH (n) RETURN sum(size(keys(n))) AS s"
    ).single()["s"]
    rel_occ = session.run(
        "MATCH ()-[r]->() RETURN sum(size(keys(r))) AS s"
    ).single()["s"]
    return {
        "nodes": nodes,
        "relationships": rels,
        "distinct_node_keys": node_keys,
        "distinct_rel_keys": rel_keys,
        "node_property_occurrences": node_occ,
        "rel_property_occurrences": rel_occ,
        "avg_node_props": round(node_occ / nodes, 3) if nodes else 0,
        "avg_rel_props": round(rel_occ / rels, 3) if rels else 0,
    }


def count_nodes_with_key(session, key: str) -> int:
    return session.run(
        f"MATCH (n) WHERE n.`{key}` IS NOT NULL RETURN count(n) AS c"
    ).single()["c"]


def count_rels_with_key(session, key: str) -> int:
    return session.run(
        f"MATCH ()-[r]->() WHERE r.`{key}` IS NOT NULL RETURN count(r) AS c"
    ).single()["c"]


def remove_node_key(session, key: str, commit: bool) -> int:
    before = count_nodes_with_key(session, key)
    if commit and before:
        session.run(f"MATCH (n) WHERE n.`{key}` IS NOT NULL REMOVE n.`{key}`").consume()
    return before


def remove_rel_key(session, key: str, commit: bool) -> int:
    before = count_rels_with_key(session, key)
    if commit and before:
        session.run(f"MATCH ()-[r]->() WHERE r.`{key}` IS NOT NULL REMOVE r.`{key}`").consume()
    return before


def export_node_property(session, key: str, path: Path) -> int:
    rows = list(
        session.run(
            f"""
            MATCH (n)
            WHERE n.`{key}` IS NOT NULL
            RETURN n.id AS node_id, labels(n) AS labels, n.`{key}` AS value
            ORDER BY n.id
            """
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(
                json.dumps(
                    {
                        "node_id": row["node_id"],
                        "labels": row["labels"],
                        "property": key,
                        "value": row["value"],
                        "export_run": RUN,
                        "exported_at_utc": NOW,
                    },
                    ensure_ascii=False,
                    default=str,
                )
                + "\n"
            )
    return len(rows)


def export_merged_rel_audit(session, path: Path) -> int:
    rows = list(
        session.run(
            """
            MATCH (a)-[r]->(b)
            WHERE r.merged_legacy_rel_ids IS NOT NULL
               OR r.merged_legacy_reltypes IS NOT NULL
            RETURN elementId(r) AS element_id,
                   type(r) AS reltype,
                   a.id AS from_id,
                   b.id AS to_id,
                   r.merged_legacy_rel_ids AS merged_legacy_rel_ids,
                   r.merged_legacy_reltypes AS merged_legacy_reltypes
            ORDER BY reltype, element_id
            """
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(dict(row), ensure_ascii=False, default=str) + "\n")
    return len(rows)


def export_nf_legacy(session, path: Path) -> int:
    rows = list(
        session.run(
            """
            MATCH (nf:Nachweisforderung)
            WHERE nf.legacy_rechtsgrundlagen_from_variant_a IS NOT NULL
               OR nf.legacy_rechtsgrundlagen_urls_from_variant_a IS NOT NULL
               OR nf.legacy_jurisdiktion_from_variant_a IS NOT NULL
            RETURN nf.id AS node_id,
                   nf.legacy_rechtsgrundlagen_from_variant_a AS legacy_rechtsgrundlagen_from_variant_a,
                   nf.legacy_rechtsgrundlagen_urls_from_variant_a AS legacy_rechtsgrundlagen_urls_from_variant_a,
                   nf.legacy_jurisdiktion_from_variant_a AS legacy_jurisdiktion_from_variant_a
            ORDER BY nf.id
            """
        )
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(dict(row), ensure_ascii=False, default=str) + "\n")
    return len(rows)


def property_matrix(session) -> tuple[list[dict], list[dict]]:
    node_rows = [
        dict(r)
        for r in session.run(
            """
            MATCH (n)
            UNWIND labels(n) AS label
            UNWIND keys(n) AS property
            RETURN label, property, count(*) AS occurrences
            ORDER BY label, occurrences DESC, property
            """
        )
    ]
    rel_rows = [
        dict(r)
        for r in session.run(
            """
            MATCH ()-[r]->()
            UNWIND keys(r) AS property
            RETURN type(r) AS reltype, property, count(*) AS occurrences
            ORDER BY reltype, occurrences DESC, property
            """
        )
    ]
    return node_rows, rel_rows


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def regulation_parity(session) -> dict[str, int]:
    return {
        "gestuetzt_auf_regelwerk": session.run(
            "MATCH ()-[r:GESTUETZT_AUF_REGELWERK]->() RETURN count(r) AS c"
        ).single()["c"],
        "gilt_in_land": session.run(
            "MATCH ()-[r:GILT_IN_LAND]->() RETURN count(r) AS c"
        ).single()["c"],
        "triggers": session.run(
            "MATCH ()-[r:TRIGGERS_REGULIERUNGSFRAGE]->() RETURN count(r) AS c"
        ).single()["c"],
        "erfordert": session.run(
            "MATCH ()-[r:ERFORDERT_NACHWEIS]->() RETURN count(r) AS c"
        ).single()["c"],
    }


def acceptance_checks(session) -> dict[str, int]:
    checks = {
        "nodes_with_phase_keys": session.run(
            """
            MATCH (n)
            WHERE any(k IN keys(n) WHERE k STARTS WITH 'phase')
            RETURN count(n) AS c
            """
        ).single()["c"],
        "legacy_internal_provenance_docs": count_nodes_with_key(
            session, "legacy_internal_provenance_docs"
        ),
        "rf_rechtsgrundlagen": session.run(
            "MATCH (n:Regulierungsfrage) WHERE n.rechtsgrundlagen IS NOT NULL RETURN count(n) AS c"
        ).single()["c"],
        "import_decision_rels": count_rels_with_key(session, "import_decision"),
        "merged_legacy_rel_ids_rels": count_rels_with_key(session, "merged_legacy_rel_ids"),
        "source_scope_nodes": count_nodes_with_key(session, "source_scope"),
        "reuse_rule_nodes": session.run("MATCH (n:ReuseRule) RETURN count(n) AS c").single()["c"],
        "review_status_rels": count_rels_with_key(session, "review_status"),
        "evidence_status_rels": count_rels_with_key(session, "evidence_status"),
        "review_run_rels": count_rels_with_key(session, "review_run"),
        "metadata_sidecar_key_nodes": count_nodes_with_key(session, "metadata_sidecar_key"),
        "metadata_sidecar_key_rels": count_rels_with_key(session, "metadata_sidecar_key"),
        "source_titles_nodes": count_nodes_with_key(session, "source_titles"),
        "nodes_with_md_in_source_titles": session.run(
            """
            MATCH (n)
            WHERE n.source_titles IS NOT NULL
              AND any(t IN n.source_titles WHERE t CONTAINS '.md')
            RETURN count(n) AS c
            """
        ).single()["c"],
        "nodes_with_source_urls": count_nodes_with_key(session, "source_urls"),
        "rels_with_source_url": count_rels_with_key(session, "source_url"),
    }
    return checks


def rel_sidecar_key(reltype: str, from_id: str, to_id: str) -> str:
    return f"rel:{reltype}:{from_id}->{to_id}"


def node_sidecar_key(node_id: str) -> str:
    return f"node:{node_id}"


def append_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")


def load_drop_patterns(path: Path) -> list[str]:
    if not path.exists():
        return []
    patterns: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        patterns.append(line)
    return patterns


def title_matches_pattern(title: str, pattern: str) -> bool:
    if pattern.startswith("contains:"):
        return pattern[9:] in title
    if pattern.startswith("="):
        return title == pattern[1:]
    if pattern.startswith(".") and "*" not in pattern and "?" not in pattern:
        return fnmatch.fnmatch(title, f"*{pattern}") or title.endswith(pattern)
    return fnmatch.fnmatch(title, pattern)


def matched_patterns_for_title(title: str, patterns: list[str]) -> list[str]:
    return [p for p in patterns if title_matches_pattern(title, p)]


def write_sidecar_manifest(extra: dict[str, Any]) -> None:
    manifest = {
        "run": RUN,
        "updated_at_utc": datetime.now(timezone.utc).isoformat(),
        "entity_metadata_file": "entity_metadata.jsonl",
        **extra,
    }
    SIDECAR.mkdir(parents=True, exist_ok=True)
    (SIDECAR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def phase0(session, commit: bool) -> dict[str, Any]:
    stats = graph_stats(session)
    node_rows, rel_rows = property_matrix(session)
    write_csv(OUT / "node_property_matrix.csv", node_rows, ["label", "property", "occurrences"])
    write_csv(OUT / "rel_property_matrix.csv", rel_rows, ["reltype", "property", "occurrences"])
    baseline = {
        "run": RUN,
        "created_at_utc": NOW,
        "stats": stats,
        "regulation_parity": regulation_parity(session),
        "acceptance": acceptance_checks(session),
        "top_node_keys": dict(
            Counter(r["property"] for r in node_rows).most_common(40)
        ),
        "top_rel_keys": dict(Counter(r["property"] for r in rel_rows).most_common(40)),
    }
    (OUT / "baseline_property_scan.json").write_text(
        json.dumps(baseline, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return {"phase": 0, "stats": stats, "node_pairs": len(node_rows), "rel_pairs": len(rel_rows)}


def phase1(session, commit: bool) -> dict[str, Any]:
    removed = {k: remove_node_key(session, k, commit) for k in PHASE1_NODE_KEYS}
    return {"phase": 1, "removed_by_key": removed, "total_removals": sum(removed.values())}


def phase2(session, commit: bool) -> dict[str, Any]:
    nf_export = export_nf_legacy(session, ARCHIVE / "nachweisforderung_variant_a_legacy.jsonl")
    removed_nf = {k: remove_node_key(session, k, commit) for k in PHASE2_NF_KEYS}
    removed_rf = {k: remove_node_key(session, k, commit) for k in PHASE2_RF_KEYS}
    parity = regulation_parity(session)
    return {
        "phase": 2,
        "nf_export_rows": nf_export,
        "removed_nf": removed_nf,
        "removed_rf": removed_rf,
        "regulation_parity": parity,
    }


def phase3(session, commit: bool) -> dict[str, Any]:
    exports = {}
    for key in PHASE3_ARCHIVE_KEYS:
        exports[key] = export_node_property(session, key, ARCHIVE / f"{key}.jsonl")
    markt = session.run(
        """
        MATCH (bg:Bauteilgruppe)
        WHERE bg.legacy_marktmodell IS NOT NULL
        OPTIONAL MATCH (bg)-[:HAT_BESCHAFFUNGSWEG]->()
        WITH bg, count(*) AS c
        RETURN count(bg) AS legacy_total,
               sum(CASE WHEN c > 0 THEN 1 ELSE 0 END) AS with_beschaffungsweg
        """
    ).single()
    removed = {k: remove_node_key(session, k, commit) for k in PHASE3_ARCHIVE_KEYS}
    return {
        "phase": 3,
        "exports": exports,
        "marktmodell_guard": dict(markt),
        "removed_by_key": removed,
        "total_removals": sum(removed.values()),
    }


def phase4(session, commit: bool) -> dict[str, Any]:
    merged_export = export_merged_rel_audit(session, ARCHIVE / "merged_rel_audit.jsonl")
    removed = {k: remove_rel_key(session, k, commit) for k in PHASE4_REL_KEYS}
    rels_before = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
    return {
        "phase": 4,
        "merged_rel_export_rows": merged_export,
        "removed_by_key": removed,
        "total_removals": sum(removed.values()),
        "relationship_count": rels_before,
    }


def phase5(session, commit: bool) -> dict[str, Any]:
    fold = session.run(
        """
        MATCH (n)
        WHERE n.source_url IS NOT NULL AND n.source_urls IS NOT NULL
        RETURN count(n) AS c
        """
    ).single()["c"]
    folded = 0
    if commit and fold:
        session.run(
            """
            MATCH (n)
            WHERE n.source_url IS NOT NULL
            SET n.source_urls = [u IN coalesce(n.source_urls, [])
              WHERE u IS NOT NULL AND trim(u) <> '']
              + CASE WHEN n.source_url IN coalesce(n.source_urls, [])
                THEN [] ELSE [n.source_url] END
            REMOVE n.source_url
            """
        ).consume()
        folded = fold

    only_url = session.run(
        """
        MATCH (n)
        WHERE n.source_url IS NOT NULL AND n.source_urls IS NULL
        RETURN count(n) AS c
        """
    ).single()["c"]
    if commit and only_url:
        session.run(
            """
            MATCH (n)
            WHERE n.source_url IS NOT NULL AND n.source_urls IS NULL
            SET n.source_urls = [n.source_url]
            REMOVE n.source_url
            """
        ).consume()

    removed_nodes = {k: remove_node_key(session, k, commit) for k in PHASE5_NODE_DROP_KEYS}

    rel_evidence_status = count_rels_with_key(session, "evidence_status")
    if commit and rel_evidence_status:
        session.run(
            """
            MATCH ()-[r]->()
            WHERE r.evidence_status IS NOT NULL AND r.confidence IS NOT NULL
            REMOVE r.evidence_status
            """
        ).consume()
    remaining_evidence_status = count_rels_with_key(session, "evidence_status")
    if commit and remaining_evidence_status:
        session.run(
            "MATCH ()-[r]->() WHERE r.evidence_status IS NOT NULL REMOVE r.evidence_status"
        ).consume()

    if commit:
        session.run(
            """
            MATCH ()-[r]->()
            WHERE r.evidence_url IS NOT NULL AND r.source_url IS NULL
            SET r.source_url = r.evidence_url
            """
        ).consume()
        session.run(
            """
            MATCH ()-[r]->()
            WHERE r.evidence_quote IS NOT NULL AND r.source_quote IS NULL
            SET r.source_quote = r.evidence_quote
            """
        ).consume()
        for k in ("evidence_url", "evidence_quote"):
            remove_rel_key(session, k, True)

    return {
        "phase": 5,
        "folded_source_url_into_array": folded,
        "promoted_singleton_source_url": only_url,
        "removed_nodes": removed_nodes,
        "evidence_status_rels_before": rel_evidence_status,
        "evidence_status_rels_after": count_rels_with_key(session, "evidence_status"),
    }


def phase6(session, commit: bool) -> dict[str, Any]:
    rows = list(
        session.run(
            """
            MATCH (n:ReuseRule)
            RETURN n.id AS id, labels(n) AS labels, properties(n) AS properties
            ORDER BY n.id
            """
        )
    )
    export_path = ARCHIVE / "reuse_rule_nodes.jsonl"
    export_path.parent.mkdir(parents=True, exist_ok=True)
    with export_path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(dict(row), ensure_ascii=False, default=str) + "\n")

    rel_count = session.run(
        "MATCH (rr:ReuseRule)-[r]->() RETURN count(r) AS c"
    ).single()["c"]

    stripped = 0
    if commit:
        for row in rows:
            props = row["properties"]
            drop_keys = [k for k in props if k not in PHASE6_REUSERULE_KEEP]
            if not drop_keys:
                continue
            remove_clause = ", ".join(f"n.`{k}`" for k in drop_keys)
            session.run(
                f"MATCH (n:ReuseRule {{id: $id}}) REMOVE {remove_clause}",
                id=row["id"],
            ).consume()
            stripped += len(drop_keys)

    return {
        "phase": 6,
        "option": "B_strip_keep_edges",
        "reuse_rule_nodes": len(rows),
        "outgoing_rels_preserved": rel_count,
        "properties_stripped": stripped,
        "export_rows": len(rows),
    }


def phase8(session, commit: bool) -> dict[str, Any]:
    stats = graph_stats(session)
    checks = acceptance_checks(session)
    parity = regulation_parity(session)
    report = {
        "run": RUN,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "stats": stats,
        "acceptance": checks,
        "regulation_parity": parity,
    }
    (OUT / "phase8_final_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    summary_lines = [
        "# Property cleanup apply summary",
        "",
        f"- Run: `{RUN}`",
        f"- Completed: {report['completed_at_utc']}",
        "",
        "## Final stats",
        "",
        f"- Nodes: {stats['nodes']}",
        f"- Relationships: {stats['relationships']}",
        f"- Distinct node keys: {stats['distinct_node_keys']} (was 107)",
        f"- Distinct rel keys: {stats['distinct_rel_keys']} (was 63)",
        f"- Avg props/node: {stats['avg_node_props']} (was 8.2)",
        f"- Avg props/rel: {stats['avg_rel_props']} (was 4.3)",
        "",
        "## Acceptance",
        "",
    ]
    for k, v in checks.items():
        summary_lines.append(f"- `{k}`: {v}")
    summary_lines.extend(
        [
            "",
            "## Regulation parity",
            "",
        ]
    )
    for k, v in parity.items():
        summary_lines.append(f"- `{k}`: {v}")
    (OUT / "CLEANUP_APPLY_SUMMARY.md").write_text(
        "\n".join(summary_lines) + "\n", encoding="utf-8"
    )
    return report


def phase4b(session, commit: bool) -> dict[str, Any]:
    rows = list(
        session.run(
            """
            MATCH (a)-[r]->(b)
            WHERE r.review_status IS NOT NULL
               OR r.evidence_status IS NOT NULL
               OR r.review_run IS NOT NULL
            RETURN elementId(r) AS element_id,
                   type(r) AS reltype,
                   a.id AS from_id,
                   labels(a) AS from_labels,
                   b.id AS to_id,
                   labels(b) AS to_labels,
                   r.id AS rel_id,
                   r.review_status AS review_status,
                   r.evidence_status AS evidence_status,
                   r.review_run AS review_run,
                   r.source_url AS source_url,
                   r.source_quote AS source_quote,
                   r.confidence AS confidence,
                   r.basis AS basis
            ORDER BY reltype, from_id, to_id
            """
        )
    )

    sidecar_rows: list[dict[str, Any]] = []
    qa_rows: list[dict[str, Any]] = []
    reltype_counts: Counter[str] = Counter()

    for row in rows:
        reltype = row["reltype"]
        from_id = row["from_id"]
        to_id = row["to_id"]
        key = rel_sidecar_key(reltype, from_id, to_id)
        reltype_counts[reltype] += 1
        archived = {
            k: row[k]
            for k in PHASE4B_REL_KEYS
            if row[k] is not None
        }
        sidecar_rows.append(
            {
                "sidecar_key": key,
                "entity_kind": "relationship",
                "reltype": reltype,
                "from_id": from_id,
                "from_labels": row["from_labels"],
                "to_id": to_id,
                "to_labels": row["to_labels"],
                "rel_id": row["rel_id"],
                "element_id": row["element_id"],
                "export_runs": [RUN_4B],
                "exported_at_utc": NOW,
                "archived_properties": archived,
                "kept_on_graph": {
                    "source_url": row["source_url"],
                    "source_quote": row["source_quote"],
                    "confidence": row["confidence"],
                    "basis": row["basis"],
                },
            }
        )
        if row["review_status"] == "needs_source_url_review":
            qa_rows.append(
                {
                    "sidecar_key": key,
                    "reltype": reltype,
                    "from_id": from_id,
                    "to_id": to_id,
                    "confidence": row["confidence"],
                    "source_url": row["source_url"],
                    "review_status": row["review_status"],
                }
            )

    if commit and sidecar_rows:
        append_jsonl(ENTITY_METADATA, sidecar_rows)
        for row in sidecar_rows:
            session.run(
                """
                MATCH (a {id: $from_id})-[r]->(b {id: $to_id})
                WHERE type(r) = $reltype
                SET r.metadata_sidecar_key = $key
                REMOVE r.review_status, r.evidence_status, r.review_run
                """,
                from_id=row["from_id"],
                to_id=row["to_id"],
                reltype=row["reltype"],
                key=row["sidecar_key"],
            ).consume()

    qa_path = SIDECAR / "qa" / "needs_source_url_review.csv"
    if qa_rows:
        qa_path.parent.mkdir(parents=True, exist_ok=True)
        write_csv(
            qa_path,
            qa_rows,
            [
                "sidecar_key",
                "reltype",
                "from_id",
                "to_id",
                "confidence",
                "source_url",
                "review_status",
            ],
        )

    write_sidecar_manifest(
        {
            "phase4b": {
                "export_run": RUN_4B,
                "relationship_rows": len(sidecar_rows),
                "qa_needs_source_url_review": len(qa_rows),
                "by_reltype": dict(reltype_counts),
            }
        }
    )

    return {
        "phase": "4b",
        "relationship_rows": len(sidecar_rows),
        "qa_needs_source_url_review": len(qa_rows),
        "by_reltype": dict(reltype_counts),
        "review_status_rels_after": count_rels_with_key(session, "review_status"),
        "evidence_status_rels_after": count_rels_with_key(session, "evidence_status"),
        "review_run_rels_after": count_rels_with_key(session, "review_run"),
        "metadata_sidecar_key_rels_after": count_rels_with_key(session, "metadata_sidecar_key"),
        "regulation_parity": regulation_parity(session),
    }


def phase5b(session, commit: bool, drop_list: Path | None = None) -> dict[str, Any]:
    patterns = load_drop_patterns(drop_list or DROP_LIST)
    graph_rows = list(
        session.run(
            """
            MATCH (n)
            WHERE n.source_titles IS NOT NULL AND size(n.source_titles) > 0
            RETURN elementId(n) AS element_id,
                   n.id AS node_id,
                   labels(n) AS labels,
                   n.source_titles AS source_titles,
                   n.source_urls AS source_urls
            ORDER BY n.id
            """
        )
    )

    sidecar_rows: list[dict[str, Any]] = []
    label_counts: Counter[str] = Counter()
    removed_title_count = 0
    matched_pattern_counts: Counter[str] = Counter()

    for row in graph_rows:
        titles = list(row["source_titles"] or [])
        removed: list[str] = []
        matched_for_node: set[str] = set()
        for title in titles:
            hits = matched_patterns_for_title(title, patterns)
            if hits:
                removed.append(title)
                matched_for_node.update(hits)
                for hit in hits:
                    matched_pattern_counts[hit] += 1
        if not removed:
            continue

        removed_title_count += len(removed)
        node_id = row["node_id"]
        key = node_sidecar_key(node_id)
        primary_label = row["labels"][0] if row["labels"] else "Unknown"
        label_counts[primary_label] += 1
        sidecar_rows.append(
            {
                "sidecar_key": key,
                "entity_kind": "node",
                "node_id": node_id,
                "labels": row["labels"],
                "element_id": row["element_id"],
                "export_runs": [RUN_5B],
                "exported_at_utc": NOW,
                "archived_properties": {
                    "source_titles": {
                        "removed": removed,
                        "matched_patterns": sorted(matched_for_node),
                        "original_full": titles,
                    }
                },
                "kept_on_graph": {
                    "source_urls": row["source_urls"],
                },
            }
        )

    if commit and sidecar_rows:
        append_jsonl(ENTITY_METADATA, sidecar_rows)
        for row in sidecar_rows:
            session.run(
                """
                MATCH (n {id: $node_id})
                SET n.metadata_sidecar_key = $key
                REMOVE n.source_titles
                """,
                node_id=row["node_id"],
                key=row["sidecar_key"],
            ).consume()

    manifest_extra = {
        "phase5b": {
            "export_run": RUN_5B,
            "drop_list": str(drop_list or DROP_LIST),
            "patterns_loaded": patterns,
            "node_rows": len(sidecar_rows),
            "removed_title_entries": removed_title_count,
            "by_label": dict(label_counts),
            "matched_pattern_hits": dict(matched_pattern_counts),
        }
    }
    if (SIDECAR / "manifest.json").exists():
        existing = json.loads((SIDECAR / "manifest.json").read_text(encoding="utf-8"))
        manifest_extra = {**existing, **manifest_extra}
    write_sidecar_manifest(manifest_extra)

    return {
        "phase": "5b",
        "patterns_loaded": patterns,
        "node_rows": len(sidecar_rows),
        "removed_title_entries": removed_title_count,
        "by_label": dict(label_counts),
        "matched_pattern_hits": dict(matched_pattern_counts),
        "source_titles_nodes_after": count_nodes_with_key(session, "source_titles"),
        "nodes_with_md_in_source_titles_after": session.run(
            """
            MATCH (n)
            WHERE n.source_titles IS NOT NULL
              AND any(t IN n.source_titles WHERE t CONTAINS '.md')
            RETURN count(n) AS c
            """
        ).single()["c"],
        "metadata_sidecar_key_nodes_after": count_nodes_with_key(session, "metadata_sidecar_key"),
        "nodes_with_source_urls_after": count_nodes_with_key(session, "source_urls"),
    }


def capture_regulation_drift(session) -> dict[str, Any]:
    parity = regulation_parity(session)
    drift_by_label = [
        dict(r)
        for r in session.run(
            """
            MATCH (a)-[r:TRIGGERS_REGULIERUNGSFRAGE|ERFORDERT_NACHWEIS]->()
            WHERE r.review_run = 'regulation_graph_vocab_2026_06_04'
            RETURN type(r) AS reltype,
                   labels(a)[0] AS from_label,
                   count(*) AS c
            ORDER BY reltype, c DESC, from_label
            """
        )
    ]
    sample_paths = [
        dict(r)
        for r in session.run(
            """
            MATCH p=(a)-[r:TRIGGERS_REGULIERUNGSFRAGE|ERFORDERT_NACHWEIS]->(b)
            WHERE r.review_run = 'regulation_graph_vocab_2026_06_04'
            RETURN type(r) AS reltype,
                   a.id AS from_id,
                   labels(a)[0] AS from_label,
                   b.id AS to_id,
                   labels(b)[0] AS to_label
            ORDER BY reltype, from_id
            LIMIT 20
            """
        )
    ]
    drift_report = {
        "run": RUN,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "baseline": REGULATION_BASELINE,
        "current": parity,
        "delta": {
            k: parity[k] - REGULATION_BASELINE[k] for k in REGULATION_BASELINE
        },
        "by_start_label_with_review_run": drift_by_label,
        "sample_paths": sample_paths,
    }
    (OUT / "regulation_drift_report.json").write_text(
        json.dumps(drift_report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return drift_report


def phase9(session, commit: bool) -> dict[str, Any]:
    drift_path = OUT / "regulation_drift_report.json"
    if drift_path.exists():
        drift_report = json.loads(drift_path.read_text(encoding="utf-8"))
    else:
        drift_report = capture_regulation_drift(session)

    parity = regulation_parity(session)
    stats = graph_stats(session)
    checks = acceptance_checks(session)
    report = {
        "run": RUN,
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "stats": stats,
        "acceptance": checks,
        "regulation_parity": parity,
        "regulation_drift": drift_report["delta"],
    }
    (OUT / "phase9_final_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary_path = OUT / "CLEANUP_APPLY_SUMMARY.md"
    prior = summary_path.read_text(encoding="utf-8") if summary_path.exists() else ""
    addon = [
        "",
        "## Follow-up (Phases 4b, 5b, 9)",
        "",
        f"- Completed: {report['completed_at_utc']}",
        f"- Sidecar file: `{SIDECAR.relative_to(REPO).as_posix()}/entity_metadata.jsonl`",
        "",
        "### Sidecar counts",
        "",
        f"- Rel `metadata_sidecar_key`: {checks['metadata_sidecar_key_rels']}",
        f"- Node `metadata_sidecar_key`: {checks['metadata_sidecar_key_nodes']}",
        f"- Remaining `review_status` rels: {checks['review_status_rels']}",
        f"- Remaining `source_titles` nodes: {checks['source_titles_nodes']}",
        f"- Nodes with `.md` in `source_titles`: {checks['nodes_with_md_in_source_titles']}",
        "",
        "### Regulation drift vs baseline",
        "",
    ]
    for k, v in drift_report["delta"].items():
        addon.append(f"- `{k}`: {parity[k]} (baseline {REGULATION_BASELINE[k]}, delta {v:+d})")
    if "## Follow-up (Phases 4b, 5b, 9)" not in prior:
        summary_path.write_text(prior.rstrip() + "\n" + "\n".join(addon) + "\n", encoding="utf-8")

    agents_path = REPO / "AGENTS.md"
    if agents_path.exists():
        agents = agents_path.read_text(encoding="utf-8")
        marker = "## Sidecar metadata (property cleanup 4b/5b)"
        sidecar_note = (
            f"{marker}\n\n"
            f"- Offloaded rel QA metadata and filtered `source_titles` live under "
            f"`_neo4j/review/2026-06-05_post_migration_property_cleanup/sidecar/`.\n"
            f"- Graph pointer property: `metadata_sidecar_key` on nodes and relationships.\n"
            f"- Drop-list for titles: `source_title_drop_patterns.txt` in the same review folder.\n"
        )
        if marker not in agents:
            insert_at = agents.find("## Nicht mehr als Standard verwenden")
            if insert_at >= 0:
                agents = agents[:insert_at] + sidecar_note + "\n" + agents[insert_at:]
            else:
                agents = agents.rstrip() + "\n\n" + sidecar_note
            agents_path.write_text(agents, encoding="utf-8")

    return report


PHASES: dict[str, Callable[..., dict[str, Any]]] = {
    "0": phase0,
    "1": phase1,
    "2": phase2,
    "3": phase3,
    "4": phase4,
    "5": phase5,
    "6": phase6,
    "8": phase8,
    "4b": phase4b,
    "5b": phase5b,
    "9": phase9,
}

LEGACY_ORDER = ["0", "1", "4", "2", "3", "5", "6", "8"]
FOLLOWUP_ORDER = ["4b", "5b", "9"]
ALL_ORDER = LEGACY_ORDER + FOLLOWUP_ORDER


def resolve_phase_order(phase: str | None, through: str | None) -> list[str]:
    if phase is not None:
        if phase not in PHASES:
            raise SystemExit(f"Unknown phase: {phase}")
        return [phase]
    if through is None:
        raise SystemExit("Specify --phase or --through")
    if through not in ALL_ORDER:
        raise SystemExit(f"Unknown --through value: {through}")
    if through in FOLLOWUP_ORDER:
        return [p for p in FOLLOWUP_ORDER if FOLLOWUP_ORDER.index(p) <= FOLLOWUP_ORDER.index(through)]
    return [p for p in LEGACY_ORDER if LEGACY_ORDER.index(p) <= LEGACY_ORDER.index(through)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", type=str, choices=sorted(PHASES.keys(), key=lambda x: ALL_ORDER.index(x) if x in ALL_ORDER else 99))
    parser.add_argument("--through", type=str)
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--drop-list", type=Path, default=DROP_LIST)
    args = parser.parse_args()

    if not args.phase and not args.through:
        parser.error("Specify --phase or --through")

    order = resolve_phase_order(args.phase, args.through)

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()

    reports: dict[str, Any] = {"run": RUN, "commit": args.commit, "phases": {}}
    try:
        with driver.session(database=database) as session:
            before_stats = graph_stats(session)
            reports["before"] = before_stats
            if set(order) & {"4b", "5b", "9"}:
                reports["regulation_drift_precapture"] = capture_regulation_drift(session)
            for phase_id in order:
                print(f"=== Phase {phase_id} ({'commit' if args.commit else 'dry-run'}) ===")
                if phase_id == "5b":
                    result = phase5b(session, args.commit, args.drop_list)
                else:
                    result = PHASES[phase_id](session, args.commit)
                reports["phases"][phase_id] = result
                suffix = "report" if args.commit else "dry_run_report"
                out = OUT / f"phase{phase_id}_{suffix}.json"
                out.write_text(
                    json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                print(json.dumps(result, ensure_ascii=False, indent=2))
            reports["after"] = graph_stats(session)
    finally:
        driver.close()

    (OUT / ("apply_report.json" if args.commit else "dry_run_apply_report.json")).write_text(
        json.dumps(reports, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
