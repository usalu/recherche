"""Trace and replace :ZITIERT_QUELLE with concrete URL properties.

Run from repo root:
    python _neo4j/intake/runs/2026-05-23_trace_zitiert_quelle_to_urls/logs/trace_zitiert_quelle_to_urls_runner.py

The migration is intentionally ledger-first:
- export every existing :ZITIERT_QUELLE edge;
- stamp resolvable URLs onto source nodes and information relationships;
- mark unresolved information relationships for review;
- delete only :ZITIERT_QUELLE edges stamped by this run.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from neo4j import GraphDatabase

THIS_FILE = Path(__file__).resolve()
RUN_DIR = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
LOG_DIR = RUN_DIR / "logs"
REPORT_DIR = RUN_DIR / "reports"
MIGRATION_DIR = RUN_DIR / "migrations"

sys.path.insert(0, str(REPO_ROOT / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

RUN_ID = "trace_zitiert_quelle_to_urls_2026-05-23"
MIGRATION_ORIGIN = "mig_trace_zitiert_quelle_to_urls_2026_05_23"
NOW = datetime.now(timezone.utc).isoformat()

ZQ_INVENTORY = LOG_DIR / "zitiert_quelle_edge_inventory.jsonl"
ZQ_LEDGER = LOG_DIR / "zitiert_quelle_resolution_ledger.jsonl"
INFO_LEDGER = LOG_DIR / "information_source_url_ledger.jsonl"
UNRESOLVED_LEDGER = LOG_DIR / "source_url_unresolved_review.jsonl"
REPORT_JSON = REPORT_DIR / "zitiert_quelle_trace_report.json"
REPORT_MD = REPORT_DIR / "zitiert_quelle_trace_report.md"
ROLLBACK_CYPHER = MIGRATION_DIR / "mig_trace_zitiert_quelle_rollback.cypher"
MIGRATION_NOTE = MIGRATION_DIR / "mig_trace_zitiert_quelle_to_urls.cypher"
FLAG_PATH = RUN_DIR / "PHASE_TRACE_ZITIERT_QUELLE_TO_URLS_DONE.flag"

SOURCE_LABELS = [
    "Dossier",
    "ResearchDocument",
    "SectionRef",
    "ExternalLink",
    "UrlMetadata",
    "OntologyAnchor",
]

VISIBILITY_LABELS = [
    "Projekt",
    "Bauwerk",
    "Akteur",
    "Bauteilgruppe",
    "Bauteiltyp",
    "Material",
    "Kennwert",
    "Huerde",
    "Methode",
    "Norm",
    "ResearchDocument",
    "Dossier",
    "SectionRef",
    "Programm",
    "ReuseRule",
]


def json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    return str(value)


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(json_safe(row), ensure_ascii=False, sort_keys=True))
            fh.write("\n")


def query_rows(session, cypher: str, **params) -> list[dict]:
    result = session.run(cypher, **params)
    keys = result.keys()
    return [json_safe({key: record[key] for key in keys}) for record in result]


def single_value(session, cypher: str, key: str = "count", **params) -> int:
    record = session.run(cypher, **params).single()
    if not record:
        return 0
    return int(record[key] or 0)


def write_run_notes() -> None:
    MIGRATION_NOTE.write_text(
        """// Q-EXT source trace migration.
// The executable implementation is logs/trace_zitiert_quelle_to_urls_runner.py.
// This note exists so the run directory has a Cypher migration pointer.
//
// High-level operations:
// 1. Copy URL endpoint properties into concrete source_url/source_urls properties.
// 2. Mark unresolved information relationships for review.
// 3. Delete only :ZITIERT_QUELLE relationships stamped by this run.
""",
        encoding="utf-8",
    )
    ROLLBACK_CYPHER.write_text(
        f"""// Rollback marker for {RUN_ID}.
// Full graph rollback should use:
//   _neo4j/review/backups/2026-05-23_pre_trace_zitiert_quelle_to_urls
//
// Property-only partial rollback is intentionally conservative:
// MATCH ()-[r]-()
// WHERE r.source_trace_migration = '{MIGRATION_ORIGIN}'
// REMOVE r.source_url, r.source_url_node_id, r.source_urls, r.source_url_node_ids,
//        r.source_url_status, r.source_url_http_code, r.source_url_wayback_snapshot,
//        r.source_url_last_checked_at, r.source_resolution_status,
//        r.source_trace_migration, r.source_trace_migrated_at,
//        r.superseded_by_migration, r.superseded_at, r.review_status;
//
// NOTE: deleted :ZITIERT_QUELLE relationships require restoring from the backup.
""",
        encoding="utf-8",
    )


def export_zq(session) -> tuple[list[dict], list[dict]]:
    inventory = query_rows(
        session,
        """
        MATCH (a)-[r:ZITIERT_QUELLE]->(b)
        RETURN elementId(r) AS rel_element_id,
               r.id AS rel_id,
               labels(a) AS start_labels,
               a.id AS start_id,
               labels(b) AS end_labels,
               b.id AS end_id,
               b.url AS end_url,
               properties(r) AS rel_props,
               properties(b) AS end_props
        ORDER BY start_id, end_id, rel_element_id
        """,
    )
    ledger: list[dict] = []
    for row in inventory:
        end_url = row.get("end_url")
        status = "resolved_url" if end_url else "retired_topology_artifact"
        action = "delete_after_replacement" if end_url else "delete_after_review_marker"
        props = row.get("rel_props") or {}
        ledger.append(
            {
                "zitiert_rel_element_id": row.get("rel_element_id"),
                "zitiert_rel_id": row.get("rel_id"),
                "start_id": row.get("start_id"),
                "start_labels": row.get("start_labels"),
                "end_id": row.get("end_id"),
                "end_labels": row.get("end_labels"),
                "resolved_url": end_url,
                "resolved_url_node_id": row.get("end_id") if end_url else None,
                "locator": props.get("locator"),
                "evidence_basis": props.get("evidence_basis"),
                "evidence_origin": props.get("evidence_origin"),
                "evidence_excerpt": props.get("evidence_excerpt"),
                "verification_status": props.get("verification_status"),
                "migration_origin": props.get("migration_origin"),
                "resolution_status": status,
                "replacement_action": action,
            }
        )
    write_jsonl(ZQ_INVENTORY, inventory)
    write_jsonl(ZQ_LEDGER, ledger)
    return inventory, ledger


def run_write_steps(session) -> dict:
    stats: dict[str, Any] = {}

    # Source nodes first, while :ZITIERT_QUELLE still exists.
    stats["source_nodes_from_zq"] = query_rows(
        session,
        """
        MATCH (s)-[:ZITIERT_QUELLE]->(u)
        WHERE u.url IS NOT NULL
        WITH s,
             collect(DISTINCT u.url) AS urls,
             collect(DISTINCT u.id) AS url_node_ids,
             collect(DISTINCT u.url_status) AS statuses
        SET s.source_urls = urls,
            s.source_url_node_ids = url_node_ids,
            s.source_count = size(urls),
            s.primary_source_url = coalesce(s.primary_source_url, urls[0]),
            s.source_url = CASE WHEN size(urls) = 1 THEN urls[0] ELSE s.source_url END,
            s.source_resolution_status = CASE
              WHEN size(urls) = 1 THEN 'single_url_from_legacy_zitiert_quelle'
              ELSE 'url_set_from_legacy_zitiert_quelle'
            END,
            s.source_trace_migration = $migration_origin,
            s.source_trace_migrated_at = $now
        RETURN count(s) AS count
        """,
        migration_origin=MIGRATION_ORIGIN,
        now=NOW,
    )[0]["count"]

    stats["zq_url_edges_stamped"] = query_rows(
        session,
        """
        MATCH ()-[r:ZITIERT_QUELLE]->(u)
        WHERE u.url IS NOT NULL
        SET r.source_url = u.url,
            r.source_url_node_id = u.id,
            r.source_url_status = u.url_status,
            r.source_url_http_code = u.url_http_code,
            r.source_url_wayback_snapshot = u.url_wayback_snapshot,
            r.source_url_last_checked_at = u.url_last_checked_at,
            r.source_resolution_status = 'resolved_url',
            r.review_status = coalesce(r.review_status, 'accepted_url_resolution'),
            r.source_trace_migration = $migration_origin,
            r.source_trace_migrated_at = $now,
            r.superseded_by_migration = $run_id,
            r.superseded_at = $now
        RETURN count(r) AS count
        """,
        migration_origin=MIGRATION_ORIGIN,
        run_id=RUN_ID,
        now=NOW,
    )[0]["count"]

    stats["zq_non_url_edges_marked"] = query_rows(
        session,
        """
        MATCH (a)-[r:ZITIERT_QUELLE]->(b)
        WHERE b.url IS NULL
        SET r.source_resolution_status = 'retired_topology_artifact',
            r.review_status = 'retired_topology_artifact',
            r.source_trace_migration = $migration_origin,
            r.source_trace_migrated_at = $now,
            r.superseded_by_migration = $run_id,
            r.superseded_at = $now
        MERGE (di:DataIssue {id: 'di_trace_zq_non_url__' + elementId(r)})
        SET di.kind = 'zitiert_quelle_non_url_artifact',
            di.severity = 'medium',
            di.status = 'review_required',
            di.review_status = 'retired_topology_artifact',
            di.source_trace_migration = $migration_origin,
            di.created_at = coalesce(di.created_at, $now),
            di.description = 'Legacy :ZITIERT_QUELLE did not terminate in a URL and was retired during URL trace migration.',
            di.start_id = a.id,
            di.end_id = b.id,
            di.legacy_rel_element_id = elementId(r)
        MERGE (di)-[:CONCERNS]->(a)
        MERGE (di)-[:CONCERNS]->(b)
        RETURN count(r) AS count
        """,
        migration_origin=MIGRATION_ORIGIN,
        run_id=RUN_ID,
        now=NOW,
    )[0]["count"]

    stats["direct_url_endpoint_relationships"] = query_rows(
        session,
        """
        MATCH ()-[r]->(u)
        WHERE type(r) <> 'ZITIERT_QUELLE'
          AND u.url IS NOT NULL
        SET r.source_url = coalesce(r.source_url, u.url),
            r.source_url_node_id = coalesce(r.source_url_node_id, u.id),
            r.source_url_status = coalesce(r.source_url_status, u.url_status),
            r.source_url_http_code = coalesce(r.source_url_http_code, u.url_http_code),
            r.source_url_wayback_snapshot = coalesce(r.source_url_wayback_snapshot, u.url_wayback_snapshot),
            r.source_url_last_checked_at = coalesce(r.source_url_last_checked_at, u.url_last_checked_at),
            r.source_resolution_status = coalesce(r.source_resolution_status, 'direct_url_endpoint'),
            r.source_trace_migration = coalesce(r.source_trace_migration, $migration_origin),
            r.source_trace_migrated_at = coalesce(r.source_trace_migrated_at, $now)
        RETURN count(r) AS count
        """,
        migration_origin=MIGRATION_ORIGIN,
        now=NOW,
    )[0]["count"]

    stats["source_id_single_url_relationships"] = query_rows(
        session,
        """
        MATCH ()-[r]->()
        WHERE type(r) <> 'ZITIERT_QUELLE'
          AND r.evidence_source_id IS NOT NULL
          AND r.source_url IS NULL
          AND (r.source_urls IS NULL OR size(r.source_urls) = 0)
        MATCH (s {id: r.evidence_source_id})
        WITH r, s,
             CASE
               WHEN s.url IS NOT NULL THEN [s.url]
               WHEN s.source_urls IS NOT NULL THEN s.source_urls
               ELSE []
             END AS urls,
             CASE
               WHEN s.url IS NOT NULL THEN [s.id]
               WHEN s.source_url_node_ids IS NOT NULL THEN s.source_url_node_ids
               ELSE []
             END AS url_node_ids
        WHERE size(urls) = 1
        SET r.source_url = urls[0],
            r.source_url_node_id = CASE WHEN size(url_node_ids) > 0 THEN url_node_ids[0] ELSE s.id END,
            r.source_resolution_status = 'evidence_source_id_single_url',
            r.source_trace_migration = $migration_origin,
            r.source_trace_migrated_at = $now
        RETURN count(r) AS count
        """,
        migration_origin=MIGRATION_ORIGIN,
        now=NOW,
    )[0]["count"]

    stats["source_id_multi_url_relationships"] = query_rows(
        session,
        """
        MATCH ()-[r]->()
        WHERE type(r) <> 'ZITIERT_QUELLE'
          AND r.evidence_source_id IS NOT NULL
          AND r.source_url IS NULL
          AND (r.source_urls IS NULL OR size(r.source_urls) = 0)
        MATCH (s {id: r.evidence_source_id})
        WITH r, s,
             CASE
               WHEN s.url IS NOT NULL THEN [s.url]
               WHEN s.source_urls IS NOT NULL THEN s.source_urls
               ELSE []
             END AS urls,
             CASE
               WHEN s.url IS NOT NULL THEN [s.id]
               WHEN s.source_url_node_ids IS NOT NULL THEN s.source_url_node_ids
               ELSE []
             END AS url_node_ids
        WHERE size(urls) > 1
        SET r.source_urls = urls,
            r.source_url_node_ids = url_node_ids,
            r.source_resolution_status = 'evidence_source_id_url_set_requires_row_review',
            r.review_status = coalesce(r.review_status, 'url_set_requires_row_review'),
            r.source_trace_migration = $migration_origin,
            r.source_trace_migrated_at = $now
        RETURN count(r) AS count
        """,
        migration_origin=MIGRATION_ORIGIN,
        now=NOW,
    )[0]["count"]

    stats["unresolved_relationships_marked"] = query_rows(
        session,
        """
        MATCH (a)-[r]->(b)
        WHERE type(r) <> 'ZITIERT_QUELLE'
          AND (r.evidence_origin IS NOT NULL OR r.evidence_source_id IS NOT NULL)
          AND r.source_url IS NULL
          AND (r.source_urls IS NULL OR size(r.source_urls) = 0)
        SET r.source_resolution_status = 'needs_source_url_review',
            r.review_status = coalesce(r.review_status, 'needs_source_url_review'),
            r.source_trace_migration = coalesce(r.source_trace_migration, $migration_origin),
            r.source_trace_migrated_at = coalesce(r.source_trace_migrated_at, $now)
        MERGE (di:DataIssue {id: 'di_source_url_review__' + elementId(r)})
        SET di.kind = 'relationship_missing_concrete_source_url',
            di.severity = CASE
              WHEN r.evidence_origin = 'source_curated' THEN 'high'
              WHEN r.evidence_origin = 'topology_synthesized' THEN 'medium'
              ELSE 'medium'
            END,
            di.status = 'review_required',
            di.review_status = 'needs_source_url_review',
            di.source_trace_migration = $migration_origin,
            di.created_at = coalesce(di.created_at, $now),
            di.rel_type = type(r),
            di.rel_element_id = elementId(r),
            di.start_id = a.id,
            di.end_id = b.id,
            di.evidence_source_id = r.evidence_source_id,
            di.evidence_origin = r.evidence_origin,
            di.description = 'Information-bearing relationship lacks a concrete URL after automatic source trace.'
        MERGE (di)-[:CONCERNS]->(a)
        MERGE (di)-[:CONCERNS]->(b)
        RETURN count(r) AS count
        """,
        migration_origin=MIGRATION_ORIGIN,
        now=NOW,
    )[0]["count"]

    stats["visibility_nodes_updated"] = query_rows(
        session,
        """
        MATCH (n)
        WHERE any(label IN labels(n) WHERE label IN $labels)
        CALL {
          WITH n
          MATCH (n)-[r]-()
          WITH collect(CASE WHEN r.source_url IS NULL THEN [] ELSE [r.source_url] END)
             + collect(CASE WHEN r.source_urls IS NULL THEN [] ELSE r.source_urls END) AS chunks
          UNWIND chunks AS chunk
          UNWIND chunk AS url
          WITH DISTINCT url WHERE url IS NOT NULL
          RETURN collect(url) AS urls
        }
        WITH n, urls
        WHERE size(urls) > 0
        SET n.source_urls = urls,
            n.source_count = size(urls),
            n.primary_source_url = coalesce(n.primary_source_url, urls[0]),
            n.source_resolution_status = coalesce(n.source_resolution_status, 'incident_relationship_source_urls'),
            n.source_trace_migration = coalesce(n.source_trace_migration, $migration_origin),
            n.source_trace_migrated_at = coalesce(n.source_trace_migrated_at, $now)
        RETURN count(n) AS count
        """,
        labels=VISIBILITY_LABELS,
        migration_origin=MIGRATION_ORIGIN,
        now=NOW,
    )[0]["count"]

    stats["zq_deleted"] = query_rows(
        session,
        """
        MATCH ()-[r:ZITIERT_QUELLE]->()
        WHERE r.superseded_by_migration = $run_id
        WITH r LIMIT 20000
        DELETE r
        RETURN count(r) AS count
        """,
        run_id=RUN_ID,
    )[0]["count"]

    return stats


def export_info_ledgers(session) -> tuple[list[dict], list[dict]]:
    info_rows = query_rows(
        session,
        """
        MATCH (a)-[r]->(b)
        WHERE type(r) <> 'ZITIERT_QUELLE'
          AND (
            r.source_trace_migration = $migration_origin
            OR r.source_url IS NOT NULL
            OR (r.source_urls IS NOT NULL AND size(r.source_urls) > 0)
          )
        RETURN elementId(r) AS rel_element_id,
               type(r) AS rel_type,
               labels(a) AS start_labels,
               a.id AS start_id,
               labels(b) AS end_labels,
               b.id AS end_id,
               r.source_url AS source_url,
               r.source_urls AS source_urls,
               r.source_url_node_id AS source_url_node_id,
               r.source_url_node_ids AS source_url_node_ids,
               r.evidence_source_id AS evidence_source_id,
               r.evidence_origin AS evidence_origin,
               r.evidence_basis AS evidence_basis,
               r.source_resolution_status AS source_resolution_status,
               r.review_status AS review_status
        ORDER BY rel_type, start_id, end_id, rel_element_id
        """,
        migration_origin=MIGRATION_ORIGIN,
    )
    unresolved_rows = query_rows(
        session,
        """
        MATCH (a)-[r]->(b)
        WHERE type(r) <> 'ZITIERT_QUELLE'
          AND (r.evidence_origin IS NOT NULL OR r.evidence_source_id IS NOT NULL)
          AND r.source_url IS NULL
          AND (r.source_urls IS NULL OR size(r.source_urls) = 0)
        RETURN elementId(r) AS rel_element_id,
               type(r) AS rel_type,
               labels(a) AS start_labels,
               a.id AS start_id,
               labels(b) AS end_labels,
               b.id AS end_id,
               r.evidence_source_id AS evidence_source_id,
               r.evidence_origin AS evidence_origin,
               r.evidence_basis AS evidence_basis,
               r.evidence_excerpt AS evidence_excerpt,
               r.source_resolution_status AS source_resolution_status,
               r.review_status AS review_status
        ORDER BY rel_type, start_id, end_id, rel_element_id
        """,
    )
    write_jsonl(INFO_LEDGER, info_rows)
    write_jsonl(UNRESOLVED_LEDGER, unresolved_rows)
    return info_rows, unresolved_rows


def audit(session) -> dict:
    return {
        "zitiert_quelle_remaining": single_value(
            session,
            "MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r) AS count",
        ),
        "cited_from_dossier_bad": single_value(
            session,
            """
            MATCH ()-[r:CITED_FROM_DOSSIER]->()
            WHERE r.source_url IS NULL OR r.locator IS NULL
            RETURN count(r) AS count
            """,
        ),
        "info_rels_missing_url_without_review": query_rows(
            session,
            """
            MATCH ()-[r]->()
            WHERE (r.evidence_origin IS NOT NULL OR r.evidence_source_id IS NOT NULL)
              AND type(r) <> 'ZITIERT_QUELLE'
              AND r.source_url IS NULL
              AND (r.source_urls IS NULL OR size(r.source_urls) = 0)
              AND coalesce(r.source_resolution_status, '') <> 'needs_source_url_review'
            RETURN type(r) AS rel_type, count(r) AS missing_url
            ORDER BY missing_url DESC
            """,
        ),
        "info_rels_missing_url_marked_review": query_rows(
            session,
            """
            MATCH ()-[r]->()
            WHERE (r.evidence_origin IS NOT NULL OR r.evidence_source_id IS NOT NULL)
              AND type(r) <> 'ZITIERT_QUELLE'
              AND r.source_url IS NULL
              AND (r.source_urls IS NULL OR size(r.source_urls) = 0)
              AND r.source_resolution_status = 'needs_source_url_review'
            RETURN type(r) AS rel_type, count(r) AS review_count
            ORDER BY review_count DESC
            """,
        ),
        "relationship_source_url_distribution": query_rows(
            session,
            """
            MATCH ()-[r]->()
            RETURN type(r) AS rel_type,
                   count(r) AS total,
                   sum(CASE WHEN r.source_url IS NOT NULL THEN 1 ELSE 0 END) AS with_source_url,
                   sum(CASE WHEN r.source_urls IS NOT NULL AND size(r.source_urls) > 0 THEN 1 ELSE 0 END) AS with_source_urls,
                   sum(CASE WHEN r.source_resolution_status = 'needs_source_url_review' THEN 1 ELSE 0 END) AS needs_review
            ORDER BY total DESC
            """,
        ),
        "source_trace_dataissues": single_value(
            session,
            """
            MATCH (di:DataIssue)
            WHERE di.source_trace_migration = $migration_origin
            RETURN count(di) AS count
            """,
            migration_origin=MIGRATION_ORIGIN,
        ),
    }


def write_report(report: dict) -> None:
    REPORT_JSON.write_text(
        json.dumps(json_safe(report), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    review_rows = report["audit"]["info_rels_missing_url_marked_review"]
    review_lines = "\n".join(
        f"- {row['rel_type']}: {row['review_count']}" for row in review_rows[:30]
    )
    write_stats = report["write_stats"]
    REPORT_MD.write_text(
        f"""# Trace `:ZITIERT_QUELLE` to concrete URLs

Completed UTC: {report['completed_at_utc']}
Database: {report['database']}
Migration: `{MIGRATION_ORIGIN}`

## Result

- Pre-existing `:ZITIERT_QUELLE` inventory rows: {report['zq_inventory_count']}
- Resolved URL legacy rows: {report['zq_resolved_url_count']}
- Non-URL legacy rows retired/review-marked: {report['zq_non_url_count']}
- `:ZITIERT_QUELLE` deleted: {write_stats.get('zq_deleted')}
- `:ZITIERT_QUELLE` remaining: {report['audit']['zitiert_quelle_remaining']}
- Source nodes stamped from legacy URL hops: {write_stats.get('source_nodes_from_zq')}
- Direct URL endpoint relationships stamped: {write_stats.get('direct_url_endpoint_relationships')}
- `evidence_source_id` single-URL relationships stamped: {write_stats.get('source_id_single_url_relationships')}
- `evidence_source_id` multi-URL relationships stamped: {write_stats.get('source_id_multi_url_relationships')}
- Relationships marked for source URL review: {write_stats.get('unresolved_relationships_marked')}
- Source trace `DataIssue` nodes: {report['audit']['source_trace_dataissues']}
- Bad `:CITED_FROM_DOSSIER` URL/locator rows: {report['audit']['cited_from_dossier_bad']}

## Review Queue By Relationship Type

{review_lines if review_lines else "- none"}

## Ledgers

- `{ZQ_INVENTORY.relative_to(REPO_ROOT)}`
- `{ZQ_LEDGER.relative_to(REPO_ROOT)}`
- `{INFO_LEDGER.relative_to(REPO_ROOT)}`
- `{UNRESOLVED_LEDGER.relative_to(REPO_ROOT)}`

## Backup

- `_neo4j/review/backups/2026-05-23_pre_trace_zitiert_quelle_to_urls`
""",
        encoding="utf-8",
    )
    FLAG_PATH.write_text(
        json.dumps(
            {
                "phase": RUN_ID,
                "completed_at_utc": report["completed_at_utc"],
                "zitiert_quelle_remaining": report["audit"]["zitiert_quelle_remaining"],
                "report": str(REPORT_JSON.relative_to(REPO_ROOT)),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    MIGRATION_DIR.mkdir(parents=True, exist_ok=True)
    write_run_notes()

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()

    try:
        with driver.session(database=database) as session:
            before = audit(session)
            inventory, zq_ledger = export_zq(session)
            write_stats = run_write_steps(session)
            info_rows, unresolved_rows = export_info_ledgers(session)
            after = audit(session)
    finally:
        driver.close()

    status_counts = Counter(row["resolution_status"] for row in zq_ledger)
    report = {
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "database": database,
        "run_id": RUN_ID,
        "migration_origin": MIGRATION_ORIGIN,
        "backup": "_neo4j/review/backups/2026-05-23_pre_trace_zitiert_quelle_to_urls",
        "before": before,
        "write_stats": write_stats,
        "audit": after,
        "zq_inventory_count": len(inventory),
        "zq_resolved_url_count": status_counts.get("resolved_url", 0),
        "zq_non_url_count": status_counts.get("retired_topology_artifact", 0),
        "information_ledger_count": len(info_rows),
        "unresolved_review_ledger_count": len(unresolved_rows),
        "files": {
            "zq_inventory": str(ZQ_INVENTORY.relative_to(REPO_ROOT)),
            "zq_ledger": str(ZQ_LEDGER.relative_to(REPO_ROOT)),
            "information_ledger": str(INFO_LEDGER.relative_to(REPO_ROOT)),
            "unresolved_review": str(UNRESOLVED_LEDGER.relative_to(REPO_ROOT)),
            "report_json": str(REPORT_JSON.relative_to(REPO_ROOT)),
            "report_md": str(REPORT_MD.relative_to(REPO_ROOT)),
        },
    }
    write_report(report)
    print(json.dumps(json_safe(report["audit"]), ensure_ascii=False, indent=2))
    print(f"Report: {REPORT_JSON.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
