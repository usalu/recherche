"""Tidy source-trace review artefacts after the main URL migration."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase

THIS_FILE = Path(__file__).resolve()
RUN_DIR = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
REPORT_DIR = RUN_DIR / "reports"

sys.path.insert(0, str(REPO_ROOT / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MIGRATION_ORIGIN = "mig_trace_zitiert_quelle_to_urls_2026_05_23"
NOW = datetime.now(timezone.utc).isoformat()
REPORT_JSON = REPORT_DIR / "post_migration_review_markers.json"

NODE_LABELS = [
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
]


def rows(session, cypher: str, **params) -> list[dict]:
    result = session.run(cypher, **params)
    keys = result.keys()
    return [{key: record[key] for key in keys} for record in result]


def main() -> int:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    try:
        with driver.session(database=database) as session:
            stats = {}
            stats["dataissues_scoped"] = rows(
                session,
                """
                MATCH (di:DataIssue)
                WHERE di.source_trace_migration = $migration_origin
                SET di.source_scope = coalesce(di.source_scope, 'source_trace_review'),
                    di.migration_origin = coalesce(di.migration_origin, $migration_origin)
                RETURN count(di) AS count
                """,
                migration_origin=MIGRATION_ORIGIN,
            )[0]["count"]

            stats["concerns_ids_set"] = rows(
                session,
                """
                MATCH (di:DataIssue)-[r:CONCERNS]->(n)
                WHERE di.source_trace_migration = $migration_origin
                  AND r.id IS NULL
                SET r.id = 'r_' + di.id + '__CONCERNS__' + coalesce(n.id, elementId(n)),
                    r.source_scope = 'source_trace_review',
                    r.migration_origin = $migration_origin
                RETURN count(r) AS count
                """,
                migration_origin=MIGRATION_ORIGIN,
            )[0]["count"]

            stats["node_gaps_marked"] = rows(
                session,
                """
                MATCH (n)
                WHERE any(label IN labels(n) WHERE label IN $labels)
                  AND n.source_url IS NULL
                  AND (n.source_urls IS NULL OR size(n.source_urls) = 0)
                  AND NOT exists {
                    MATCH (n)-[r]-()
                    WHERE r.source_url IS NOT NULL
                       OR (r.source_urls IS NOT NULL AND size(r.source_urls) > 0)
                  }
                SET n.source_resolution_status = 'needs_source_url_review',
                    n.review_status = coalesce(n.review_status, 'needs_source_url_review'),
                    n.source_scope = coalesce(n.source_scope, 'source_trace_review'),
                    n.source_trace_migration = coalesce(n.source_trace_migration, $migration_origin),
                    n.source_trace_migrated_at = coalesce(n.source_trace_migrated_at, $now)
                MERGE (di:DataIssue {id: 'di_node_source_url_review__' + n.id})
                SET di.kind = 'node_missing_concrete_source_url',
                    di.severity = 'medium',
                    di.status = 'review_required',
                    di.review_status = 'needs_source_url_review',
                    di.source_scope = 'source_trace_review',
                    di.source_trace_migration = $migration_origin,
                    di.migration_origin = $migration_origin,
                    di.created_at = coalesce(di.created_at, $now),
                    di.ref_id = n.id,
                    di.ref_labels = labels(n),
                    di.description = 'Node has no concrete source_url/source_urls and no incident URL-bearing relationship after source trace migration.'
                MERGE (di)-[c:CONCERNS]->(n)
                SET c.id = coalesce(c.id, 'r_' + di.id + '__CONCERNS__' + n.id),
                    c.source_scope = 'source_trace_review',
                    c.migration_origin = $migration_origin
                RETURN count(n) AS count
                """,
                labels=NODE_LABELS,
                migration_origin=MIGRATION_ORIGIN,
                now=NOW,
            )[0]["count"]

            stats["node_gaps_after"] = rows(
                session,
                """
                MATCH (n)
                WHERE any(label IN labels(n) WHERE label IN $labels)
                  AND n.source_url IS NULL
                  AND (n.source_urls IS NULL OR size(n.source_urls) = 0)
                  AND NOT exists {
                    MATCH (n)-[r]-()
                    WHERE r.source_url IS NOT NULL
                       OR (r.source_urls IS NOT NULL AND size(r.source_urls) > 0)
                  }
                  AND coalesce(n.source_resolution_status, '') <> 'needs_source_url_review'
                RETURN labels(n) AS labels, count(n) AS count
                ORDER BY count DESC
                """,
                labels=NODE_LABELS,
            )

            stats["zq_remaining"] = rows(
                session,
                "MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r) AS count",
            )[0]["count"]
    finally:
        driver.close()

    REPORT_JSON.write_text(
        json.dumps(stats, ensure_ascii=False, indent=2, default=str) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(stats, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
