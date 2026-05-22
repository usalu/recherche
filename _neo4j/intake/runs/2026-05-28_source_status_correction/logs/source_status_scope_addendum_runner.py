"""Remove source_status from bookkeeping/source-inventory relationships."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from neo4j import GraphDatabase

THIS_FILE = Path(__file__).resolve()
RUN_DIR = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
LOG_DIR = RUN_DIR / "logs"
REPORT_DIR = RUN_DIR / "reports"

sys.path.insert(0, str(REPO_ROOT / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MIGRATION = "mig_source_status_scope_addendum_2026_05_28"
NOW = datetime.now(timezone.utc).isoformat()
BOOKKEEPING_REL_TYPES = ["ANCHORED_BY"]
SOURCE_INVENTORY_REL_TYPES = ["HAS_SOURCE_LINK"]
NON_FACT_REL_TYPES = [
    "ANCHORED_BY",
    "CITED_FROM_DOSSIER",
    "CONCERNS",
    "HAS_DATA_ISSUE",
    "HAS_SOURCE_LINK",
    "EXACT_MATCH_CANDIDATE",
]

BACKUP_JSONL = LOG_DIR / "removed_scope_source_status_backup.jsonl"
REPORT_JSON = REPORT_DIR / "source_status_scope_addendum_report.json"
REPORT_MD = REPORT_DIR / "source_status_scope_addendum_report.md"


def rows(session, cypher: str, **params: Any) -> list[dict[str, Any]]:
    result = session.run(cypher, **params)
    keys = result.keys()
    return [{key: record[key] for key in keys} for record in result]


def scalar(session, cypher: str, key: str = "count", **params: Any) -> Any:
    data = rows(session, cypher, **params)
    if not data:
        return None
    return data[0].get(key)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )


def write_jsonl(path: Path, payload: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in payload:
            fh.write(json.dumps(row, ensure_ascii=False, sort_keys=True, default=str))
            fh.write("\n")


def gates(session) -> dict[str, Any]:
    return {
        "all_non_fact_relationships_with_source_status": scalar(
            session,
            """
            MATCH ()-[r]->()
            WHERE type(r) IN $non_fact_rel_types
              AND r.source_status IS NOT NULL
            RETURN count(r) AS count
            """,
            non_fact_rel_types=NON_FACT_REL_TYPES,
        ),
        "anchored_by_needs_source_review": scalar(
            session,
            """
            MATCH ()-[r:ANCHORED_BY]->()
            WHERE r.review_status = 'needs_source_url_review'
               OR r.source_resolution_status = 'needs_source_url_review'
            RETURN count(r) AS count
            """,
        ),
        "fact_exact_status_without_url": scalar(
            session,
            """
            MATCH ()-[r]->()
            WHERE NOT type(r) IN $non_fact_rel_types
              AND r.source_status = 'exact'
              AND (r.source_url IS NULL OR NOT r.source_url STARTS WITH 'http')
            RETURN count(r) AS count
            """,
            non_fact_rel_types=NON_FACT_REL_TYPES,
        ),
        "fact_url_without_exact_status": scalar(
            session,
            """
            MATCH ()-[r]->()
            WHERE NOT type(r) IN $non_fact_rel_types
              AND r.source_url IS NOT NULL
              AND coalesce(r.source_status, '') <> 'exact'
              AND coalesce(r.review_status, '') <> 'needs_source_url_review'
              AND coalesce(r.source_resolution_status, '') <> 'needs_source_url_review'
            RETURN count(r) AS count
            """,
            non_fact_rel_types=NON_FACT_REL_TYPES,
        ),
    }


def main() -> int:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()

    report: dict[str, Any] = {
        "database": database,
        "migration": MIGRATION,
        "started_at": NOW,
        "rule": "ANCHORED_BY and HAS_SOURCE_LINK are not fact evidence edges.",
    }

    with driver.session(database=database) as session:
        report["pre_gates"] = gates(session)
        backup = rows(
            session,
            """
            MATCH (a)-[r]->(b)
            WHERE type(r) IN $rel_types
              AND (r.source_status IS NOT NULL
                OR r.review_status = 'needs_source_url_review'
                OR r.source_resolution_status = 'needs_source_url_review')
            RETURN elementId(r) AS rel_element_id,
                   type(r) AS rel_type,
                   labels(a) AS start_labels,
                   a.id AS start_id,
                   labels(b) AS end_labels,
                   b.id AS end_id,
                   properties(r) AS properties
            ORDER BY rel_type, start_id, end_id, rel_element_id
            """,
            rel_types=BOOKKEEPING_REL_TYPES + SOURCE_INVENTORY_REL_TYPES,
        )
        write_jsonl(BACKUP_JSONL, backup)
        report["backed_up_relationships"] = len(backup)

        stats: dict[str, Any] = {}
        stats["anchored_by_status_removed"] = scalar(
            session,
            """
            MATCH ()-[r]->()
            WHERE type(r) IN $bookkeeping_rel_types
              AND (r.source_status IS NOT NULL
                OR r.review_status = 'needs_source_url_review'
                OR r.source_resolution_status = 'needs_source_url_review')
            SET r.source_role = 'ontology_anchor',
                r.source_status_correction_previous = r.source_status,
                r.source_review_status_correction_previous = r.review_status,
                r.source_resolution_status_correction_previous = r.source_resolution_status,
                r.source_status_correction = $migration,
                r.source_status_corrected_at = $now,
                r.source_status_correction_reason = 'ontology_anchor_bookkeeping_not_fact_proof'
            REMOVE r.source_status,
                   r.source_status_reason,
                   r.source_status_migration,
                   r.source_status_normalized_at,
                   r.review_status,
                   r.source_resolution_status
            RETURN count(r) AS count
            """,
            bookkeeping_rel_types=BOOKKEEPING_REL_TYPES,
            migration=MIGRATION,
            now=NOW,
        )
        stats["has_source_link_status_removed"] = scalar(
            session,
            """
            MATCH ()-[r]->()
            WHERE type(r) IN $source_inventory_rel_types
              AND r.source_status IS NOT NULL
            SET r.source_role = 'source_inventory',
                r.source_status_correction_previous = r.source_status,
                r.source_status_correction = $migration,
                r.source_status_corrected_at = $now,
                r.source_status_correction_reason = 'source_link_inventory_not_fact_proof'
            REMOVE r.source_status,
                   r.source_status_reason,
                   r.source_status_migration,
                   r.source_status_normalized_at
            RETURN count(r) AS count
            """,
            source_inventory_rel_types=SOURCE_INVENTORY_REL_TYPES,
            migration=MIGRATION,
            now=NOW,
        )
        report["stats"] = stats
        report["post_gates"] = gates(session)

    write_json(REPORT_JSON, report)
    lines = [
        "# Source Status Scope Addendum",
        "",
        f"- Database: `{database}`",
        f"- Migration: `{MIGRATION}`",
        f"- Started: `{NOW}`",
        "",
        "## Rule",
        "",
        "`ANCHORED_BY` is ontology bookkeeping and `HAS_SOURCE_LINK` is source inventory. Neither is fact proof, so neither should carry `source_status`.",
        "",
        "## Writes",
        "",
        f"- `backed_up_relationships`: {report['backed_up_relationships']}",
    ]
    for key, value in stats.items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", "## Gates", ""])
    for key, value in report["post_gates"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Backup", "", f"- `{BACKUP_JSONL.as_posix()}`", ""])
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(stats, ensure_ascii=False, indent=2, sort_keys=True))
    print(json.dumps(report["post_gates"], ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
